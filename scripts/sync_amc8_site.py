from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(r"D:\AMC8_Codex\output")
TARGET = ROOT / "amc8"
YEARS = (2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025)
CSV_FIELDS = (
    "year",
    "contest",
    "form",
    "problem_no",
    "source",
    "statement",
    "answer",
    "major_category",
    "minor_category",
    "tags",
    "key_idea",
    "notes",
)
PUBLIC_ROOT_FILES = (
    "all_years_index.html",
    "textbook_index.html",
    "all_problems.csv",
    "taxonomy.md",
    "method_index.md",
    "common_errors.md",
    "prerequisite_map.md",
)
YEAR_FILE_TEMPLATES = ("{year}.html", "{year}_classified.md", "{year}_problems.csv")
EXPECTED_PROBLEMS = len(YEARS) * 25
EXPECTED_IMAGES = 76
EXPECTED_PDF_REFERENCES = 96

SITE_NAV_STYLE = """\
<style id="stemhub-site-nav-style">
.stemhub-site-nav{max-width:1180px;margin:12px auto 0;padding:0 18px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.stemhub-site-nav a{display:inline-flex;align-items:center;min-height:38px;padding:7px 12px;border:1px solid #cbd5e1;border-radius:999px;background:#fff;color:#1e3a5f;text-decoration:none;font:700 14px/1.2 system-ui,-apple-system,"Segoe UI",sans-serif}
.stemhub-site-nav a:hover,.stemhub-site-nav a:focus-visible{border-color:#2563eb;color:#1d4ed8;box-shadow:0 0 0 3px rgba(37,99,235,.14);outline:0}
@media(max-width:480px){.stemhub-site-nav{padding:0 12px}.stemhub-site-nav a{flex:1 1 auto;justify-content:center;font-size:13px}}
</style>"""

PDF_LINK_RE = re.compile(
    r'<a\s+href="(?:\.\./)+input/[^"<>]+"[^>]*>(.*?)</a>',
    flags=re.IGNORECASE | re.DOTALL,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def expected_slugs(rows: list[dict[str, str]]) -> set[str]:
    return {
        f"{int(row['year'])}-amc-8-problem-{int(row['problem_no'])}"
        for row in rows
    }


def verify_upstream_artifacts(source: Path, publishable_files: set[Path]) -> None:
    manifest_path = source / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Missing upstream AMC 8 manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("Upstream AMC 8 manifest has no artifacts list")

    by_path: dict[str, dict[str, object]] = {}
    for entry in artifacts:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            continue
        raw_path = str(entry["path"]).replace("\\", "/")
        relative = raw_path.removeprefix("output/")
        by_path[relative] = entry

    errors: list[str] = []
    for path in sorted(publishable_files, key=lambda item: item.as_posix().lower()):
        relative = path.relative_to(source).as_posix()
        entry = by_path.get(relative)
        if entry is None:
            errors.append(f"missing manifest artifact: {relative}")
            continue
        expected_size = entry.get("size_bytes")
        expected_hash = str(entry.get("sha256", "")).upper()
        if expected_size != path.stat().st_size or expected_hash != sha256(path):
            errors.append(f"stale manifest artifact: {relative}")
    if errors:
        raise ValueError("Upstream AMC 8 artifact verification failed: " + "; ".join(errors[:8]))


def ensure_source_is_publishable(source: Path) -> list[dict[str, str]]:
    if not source.is_dir():
        raise FileNotFoundError(f"AMC 8 source output does not exist: {source}")
    if source.is_symlink():
        raise ValueError("AMC 8 source output may not be a symbolic link")

    missing = [name for name in PUBLIC_ROOT_FILES if not (source / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing public source files: {', '.join(missing)}")

    fields, rows = read_csv(source / "all_problems.csv")
    if fields != list(CSV_FIELDS):
        raise ValueError(f"Unexpected AMC 8 CSV schema: {fields}")
    if len(rows) != EXPECTED_PROBLEMS:
        raise ValueError(f"Expected {EXPECTED_PROBLEMS} AMC 8 rows, found {len(rows)}")

    expected_keys = {(str(year), str(problem_no)) for year in YEARS for problem_no in range(1, 26)}
    actual_keys = {(row["year"], row["problem_no"]) for row in rows}
    if actual_keys != expected_keys or len(actual_keys) != len(rows):
        raise ValueError("AMC 8 rows are not the exact 10-year × 25-problem key set")
    if any(row["contest"] != "AMC 8" or row["form"] != "" for row in rows):
        raise ValueError("AMC 8 contest/form fields do not match the protected baseline")
    if any(row["source"] != f"{row['year']} AMC 8 Problem {row['problem_no']}" for row in rows):
        raise ValueError("AMC 8 source labels do not match the required format")
    if len({row["source"] for row in rows}) != EXPECTED_PROBLEMS:
        raise ValueError("AMC 8 source labels are not unique")

    for year in YEARS:
        year_dir = source / str(year)
        expected_names = {template.format(year=year) for template in YEAR_FILE_TEMPLATES}
        if not year_dir.is_dir():
            raise FileNotFoundError(f"Missing AMC 8 year directory: {year_dir}")
        actual_names = {path.name for path in year_dir.iterdir() if path.is_file()}
        if actual_names != expected_names:
            raise ValueError(f"Unexpected files in {year_dir}: {sorted(actual_names ^ expected_names)}")
        if any(path.is_dir() or path.is_symlink() for path in year_dir.iterdir()):
            raise ValueError(f"Unexpected directory or symlink in {year_dir}")

    slugs = expected_slugs(rows)
    problem_root = source / "problems"
    actual_problem_dirs = {path.name for path in problem_root.iterdir() if path.is_dir()}
    if actual_problem_dirs != slugs:
        raise ValueError("AMC 8 detail-page directories do not match the aggregate CSV")
    if any(path.is_file() or path.is_symlink() for path in problem_root.iterdir()):
        raise ValueError("Unexpected file or symlink at the AMC 8 problems root")
    for slug in sorted(slugs):
        entries = list((problem_root / slug).iterdir())
        if len(entries) != 1 or entries[0].name != "index.html" or not entries[0].is_file():
            raise ValueError(f"Detail page directory is not publishable: {slug}")

    asset_root = source / "assets" / "problems"
    asset_files = [path for path in asset_root.rglob("*") if path.is_file()]
    if len(asset_files) != EXPECTED_IMAGES or any(path.suffix.lower() != ".png" for path in asset_files):
        raise ValueError(
            f"Expected exactly {EXPECTED_IMAGES} PNG diagram assets, found {len(asset_files)} files"
        )
    if any(path.is_symlink() for path in asset_root.rglob("*")):
        raise ValueError("Diagram asset tree may not contain symbolic links")

    publishable_files = {source / name for name in PUBLIC_ROOT_FILES}
    for year in YEARS:
        publishable_files.update(
            source / str(year) / template.format(year=year)
            for template in YEAR_FILE_TEMPLATES
        )
    publishable_files.update(
        source / "problems" / slug / "index.html" for slug in slugs
    )
    publishable_files.update(asset_files)
    if len(publishable_files) != 363:
        raise ValueError(f"Expected 363 upstream public source files, found {len(publishable_files)}")
    verify_upstream_artifacts(source, publishable_files)
    return rows


def navigation_html(relative_root: str) -> str:
    return (
        '<nav class="stemhub-site-nav" data-stemhub-site-nav="1" '
        'aria-label="STEMHUB 竞赛导航">'
        f'<a href="{relative_root}index.html">STEMHUB 首页</a>'
        f'<a href="{relative_root}amc10/index.html">AMC 10</a>'
        f'<a href="{relative_root}amc12/index.html">AMC 12</a>'
        "</nav>"
    )


def make_public_html(text: str, relative_root: str, strip_pdf_links: bool = False) -> tuple[str, int]:
    if 'data-stemhub-site-nav="1"' in text or 'id="stemhub-site-nav-style"' in text:
        raise ValueError("Upstream HTML already contains the STEMHUB publication navigation marker")
    if not re.search(r"</head\s*>", text, flags=re.IGNORECASE):
        raise ValueError("HTML is missing </head>")
    if not re.search(r"<body(?:\s[^>]*)?>", text, flags=re.IGNORECASE):
        raise ValueError("HTML is missing <body>")

    text = re.sub(
        r"</head\s*>",
        SITE_NAV_STYLE + "\n</head>",
        text,
        count=1,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(<body(?:\s[^>]*)?>)",
        lambda match: match.group(1) + "\n" + navigation_html(relative_root),
        text,
        count=1,
        flags=re.IGNORECASE,
    )

    replacements = 0
    if strip_pdf_links:
        text, replacements = PDF_LINK_RE.subn(
            lambda match: (
                '<span class="local-pdf-reference">'
                + match.group(1)
                + "（来源已核验；发布版未附原始 PDF）</span>"
            ),
            text,
        )
    # Generated detail pages contain indentation-only spacer lines. Removing
    # only those lines keeps visible content unchanged and avoids publishing
    # trailing-whitespace noise on every problem page.
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    return text, replacements


def copy_file(source: Path, target: Path) -> None:
    if source.is_symlink():
        raise ValueError(f"Refusing to publish a symbolic link: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def write_html(source: Path, target: Path, relative_root: str, strip_pdf_links: bool = False) -> int:
    text = source.read_text(encoding="utf-8")
    public_text, replacements = make_public_html(text, relative_root, strip_pdf_links)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(public_text, encoding="utf-8", newline="\n")
    return replacements


def managed_manifest(stage: Path, source: Path, pdf_replacements: int) -> dict[str, object]:
    files = []
    for path in sorted(stage.rglob("*"), key=lambda item: item.as_posix().lower()):
        if path.is_file() and path.name != "site_manifest.json":
            files.append(
                {
                    "path": path.relative_to(stage).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    upstream_manifest = source / "manifest.json"
    return {
        "schema_version": 1,
        "site": "STEMHUB AMC 8",
        "publication_root": "amc8/",
        "source_project": "AMC8_Codex/output",
        "source_manifest_sha256": sha256(upstream_manifest) if upstream_manifest.is_file() else None,
        "years": list(YEARS),
        "problem_count": EXPECTED_PROBLEMS,
        "detail_page_count": EXPECTED_PROBLEMS,
        "diagram_image_count": EXPECTED_IMAGES,
        "html_page_count": sum(1 for item in files if str(item["path"]).endswith(".html")),
        "navigation_injected_page_count": sum(
            1 for item in files if str(item["path"]).endswith(".html")
        ),
        "local_pdf_links_replaced": pdf_replacements,
        "upstream_artifacts_verified": 363,
        "managed_file_count_excluding_manifest": len(files),
        "files": files,
    }


def assert_managed_destination(path: Path) -> None:
    root = ROOT.resolve()
    if path.resolve(strict=False) != (root / "amc8").resolve(strict=False):
        raise ValueError(f"Refusing to replace an unmanaged destination: {path}")


def assert_ephemeral_path(path: Path, prefix: str) -> None:
    root = ROOT.resolve()
    resolved = path.resolve(strict=False)
    if resolved.parent != root or not path.name.startswith(prefix):
        raise ValueError(f"Refusing to remove an unmanaged temporary path: {path}")


def publish_stage(stage: Path, target: Path) -> None:
    assert_managed_destination(target)
    assert_ephemeral_path(stage, ".amc8-staging-")
    backup = ROOT / f".amc8-backup-{os.getpid()}"
    assert_ephemeral_path(backup, ".amc8-backup-")
    if backup.exists():
        raise FileExistsError(f"Refusing to overwrite stale backup: {backup}")

    target_was_present = target.exists()
    try:
        if target_was_present:
            target.rename(backup)
        stage.rename(target)
    except Exception:
        if target_was_present and backup.exists() and not target.exists():
            backup.rename(target)
        raise
    else:
        if backup.exists():
            shutil.rmtree(backup)


def sync(source: Path) -> dict[str, object]:
    source = source.resolve()
    rows = ensure_source_is_publishable(source)
    slugs = expected_slugs(rows)

    stage = ROOT / f".amc8-staging-{os.getpid()}"
    assert_ephemeral_path(stage, ".amc8-staging-")
    if stage.exists():
        raise FileExistsError(f"Refusing to overwrite stale staging directory: {stage}")
    stage.mkdir()
    try:
        overview_source = source / "all_years_index.html"
        write_html(overview_source, stage / "all_years_index.html", "../")
        write_html(overview_source, stage / "index.html", "../")
        write_html(source / "textbook_index.html", stage / "textbook_index.html", "../")

        for name in PUBLIC_ROOT_FILES:
            if name not in {"all_years_index.html", "textbook_index.html"}:
                copy_file(source / name, stage / name)

        for year in YEARS:
            year_text = source / str(year) / f"{year}.html"
            write_html(year_text, stage / str(year) / f"{year}.html", "../../")
            for template in YEAR_FILE_TEMPLATES[1:]:
                name = template.format(year=year)
                copy_file(source / str(year) / name, stage / str(year) / name)

        pdf_replacements = 0
        for slug in sorted(slugs):
            pdf_replacements += write_html(
                source / "problems" / slug / "index.html",
                stage / "problems" / slug / "index.html",
                "../../../",
                strip_pdf_links=True,
            )
        if pdf_replacements != EXPECTED_PDF_REFERENCES:
            raise ValueError(
                f"Expected to replace {EXPECTED_PDF_REFERENCES} local PDF links, replaced {pdf_replacements}"
            )

        for asset in sorted((source / "assets" / "problems").rglob("*.png")):
            relative = asset.relative_to(source / "assets" / "problems")
            copy_file(asset, stage / "assets" / "problems" / relative)

        manifest = managed_manifest(stage, source, pdf_replacements)
        (stage / "site_manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        publish_stage(stage, TARGET)
        return manifest
    finally:
        if stage.exists():
            assert_ephemeral_path(stage, ".amc8-staging-")
            shutil.rmtree(stage)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish the validated AMC8_Codex output into the self-contained STEMHUB AMC 8 subtree."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"Validated AMC 8 output directory (default: {DEFAULT_SOURCE})",
    )
    args = parser.parse_args()
    manifest = sync(args.source)
    print(
        "AMC 8 site synchronized: "
        f"{manifest['problem_count']} problems, "
        f"{manifest['detail_page_count']} detail pages, "
        f"{manifest['diagram_image_count']} diagram images, "
        f"{manifest['managed_file_count_excluding_manifest']} managed files."
    )


if __name__ == "__main__":
    main()
