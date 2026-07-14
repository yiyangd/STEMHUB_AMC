from __future__ import annotations

import argparse
import html
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "bilingual_migration_report.md"
MARKER_START = "<!-- STEMHUB I18N ASSETS -->"
MARKER_END = "<!-- /STEMHUB I18N ASSETS -->"
ASSET_VERSION = "20260714"
BLOCK_RE = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END) + r"\s*", re.DOTALL)
BADGE_RE = re.compile(r'(<span\b(?=[^>]*\bclass="[^"]*\bbadge\b[^"]*")[^>]*)(>)([^<]*)(</span>)', re.IGNORECASE)


def detail_pages() -> list[Path]:
    pages: list[Path] = []
    for contest in ("amc10", "amc12"):
        pages.extend(sorted((ROOT / contest / "problems").glob("*/index.html")))
    return pages


def asset_block(page: Path) -> str:
    relative_assets = os.path.relpath(ROOT / "assets", page.parent).replace("\\", "/")
    return (
        f"  {MARKER_START}\n"
        f'  <link rel="stylesheet" href="{relative_assets}/language-switcher.css?v={ASSET_VERSION}" data-stemhub-i18n-assets>\n'
        f'  <script defer src="{relative_assets}/i18n-dictionary.js?v={ASSET_VERSION}" data-stemhub-i18n-assets></script>\n'
        f'  <script defer src="{relative_assets}/language-switcher.js?v={ASSET_VERSION}" data-stemhub-i18n-assets></script>\n'
        f"  {MARKER_END}\n"
    )


def recover_legacy_chinese(value: str) -> str:
    """Recover UTF-8 text that was decoded with a GBK code page in early pages."""
    if not value:
        return ""
    try:
        recovered = value.encode("gbk").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return ""
    return recovered if re.search(r"[\u3400-\u9fff]", recovered) else ""


def add_badge_aliases(text: str) -> tuple[str, int]:
    aliases = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal aliases
        opening, separator, content, closing = match.groups()
        if "data-i18n-raw=" in opening:
            return match.group(0)
        raw = html.unescape(content).strip()
        recovered = recover_legacy_chinese(raw)
        if not recovered:
            return match.group(0)
        aliases += 1
        return f'{opening} data-i18n-raw="{html.escape(recovered, quote=True)}"{separator}{content}{closing}'

    return BADGE_RE.sub(replace, text), aliases


def migrate_page(page: Path, check_only: bool) -> tuple[bool, str | None, int]:
    text = page.read_text(encoding="utf-8")
    block = asset_block(page)
    expected_path = re.search(r'href="([^"]+language-switcher\.css(?:\?[^\"]*)?)"', block).group(1)
    existing = BLOCK_RE.search(text)
    changed = False
    if existing:
        current = existing.group(0)
        valid = (
            text.count(MARKER_START) == 1
            and text.count(MARKER_END) == 1
            and text.count("data-stemhub-i18n-assets") == 3
            and expected_path in current
        )
        if valid:
            pass
        elif check_only:
            return False, "asset block is incomplete or points to the wrong relative path", 0
        else:
            text = BLOCK_RE.sub(block, text, count=1)
            changed = True
    else:
        if "</head>" not in text:
            return False, "missing </head>", 0
        if check_only:
            return False, "missing asset block", 0
        text = text.replace("</head>", block + "</head>", 1)
        changed = True
    updated, aliases = add_badge_aliases(text)
    if updated != text:
        if check_only:
            return False, "recoverable legacy taxonomy text is missing data-i18n-raw", aliases
        text = updated
        changed = True
    if not check_only:
        page.write_text(text, encoding="utf-8")
        return changed, None, aliases
    return False, None, aliases


def write_report(total: int, changed: int, aliases: int, failures: list[str], check_only: bool) -> None:
    mode = "validation" if check_only else "migration"
    lines = [
        "# Bilingual Migration Report",
        "",
        f"- Mode: {mode}",
        f"- Detail pages inspected: {total}",
        f"- Detail pages updated: {changed}",
        f"- Pages with bilingual asset blocks: {total - len(failures)}",
        f"- Legacy taxonomy aliases recovered: {aliases}",
        f"- Validation failures: {len(failures)}",
        "",
        "## Scope",
        "",
        "- Added the shared bilingual CSS, dictionary, and language-switching script to each AMC10/AMC12 problem detail page.",
        "- Preserved the existing problem statements, choices, answers, teaching solutions, MathJax markup, and AoPS links.",
        "- The switcher defaults to Chinese, persists in localStorage, and accepts ?lang=zh or ?lang=en.",
        "",
        "## Maintenance Note",
        "",
        "The overview pages in this deployment repository are published HTML artifacts. The upstream AMC10/AMC12 overview builders are outside this repository, so rerunning those pipelines may replace the bilingual overview shell. Reapply the website migration or port the shared asset references and localization hooks into the upstream builders before publishing new overview files.",
    ]
    if failures:
        lines += ["", "## Failures", ""] + [f"- {failure}" for failure in failures]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Add or validate STEMHUB bilingual assets on detail pages.")
    parser.add_argument("--check", action="store_true", help="Validate the existing asset blocks without changing pages.")
    args = parser.parse_args()
    pages = detail_pages()
    changed = 0
    aliases = 0
    failures: list[str] = []
    for page in pages:
        did_change, failure, page_aliases = migrate_page(page, args.check)
        changed += int(did_change)
        aliases += page_aliases
        if failure:
            failures.append(f"{page.relative_to(ROOT)}: {failure}")
    write_report(len(pages), changed, aliases, failures, args.check)
    if failures:
        raise SystemExit("Bilingual detail-page validation failed:\n" + "\n".join(failures))
    print(f"Bilingual {('validation' if args.check else 'migration')} passed for {len(pages)} detail pages; updated {changed}.")


if __name__ == "__main__":
    main()
