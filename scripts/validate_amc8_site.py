from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "amc8"
DEFAULT_SOURCE = Path(r"D:\AMC8_Codex\output")
SOURCE = DEFAULT_SOURCE
REPORT = ROOT / "docs" / "audits" / "amc8_site_validation.md"
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
EXPECTED_PROBLEMS = 250
EXPECTED_IMAGES = 76
EXPECTED_PDF_REFERENCES = 96
PUBLIC_ROOT_FILES = {
    "index.html",
    "all_years_index.html",
    "textbook_index.html",
    "all_problems.csv",
    "taxonomy.md",
    "method_index.md",
    "common_errors.md",
    "prerequisite_map.md",
    "site_manifest.json",
}
TEXT_SUFFIXES = {".html", ".md", ".csv", ".json"}
LOCAL_PATH_RE = re.compile(r"(?i)(?:\b[A-Z]:[\\/]|file://|https?://(?:localhost|127\.0\.0\.1)(?::\d+)?)")
MARKDOWN_LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
CSS_EXTERNAL_URL_RE = re.compile(r"(?i)url\(\s*['\"]?(?:https?:)?//")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def relative_name(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str, str]] = []
        self.images: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.lower(): value or "" for name, value in attrs}
        for attribute in ("href", "src"):
            if attribute in values:
                self.references.append((tag.lower(), attribute, values[attribute]))
        if tag.lower() == "img":
            self.images.append((values.get("src", ""), values.get("alt", "")))


def local_target(page: Path, raw_url: str) -> tuple[Path | None, str | None]:
    url = raw_url.strip()
    if not url or url.startswith("#"):
        return None, None
    parsed = urlsplit(url)
    if parsed.scheme.lower() in {"http", "https", "mailto", "tel", "javascript", "data"}:
        return None, None
    if url.startswith("//"):
        return None, None
    if parsed.scheme:
        return None, f"unsupported URL scheme: {url}"

    path_part = unquote(parsed.path)
    if not path_part:
        return page, None
    if "\\" in path_part:
        return None, f"backslash in public URL: {url}"
    candidate = (page.parent / path_part).resolve(strict=False)
    root = ROOT.resolve()
    if not is_within(candidate, root):
        return None, f"link escapes repository root: {url}"
    if path_part.endswith("/"):
        candidate = candidate / "index.html"
    return candidate, None


def embedded_problems(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    marker = re.search(r"\bconst\s+problems\s*=\s*", text)
    if marker is None:
        raise ValueError(f"Embedded problems marker not found: {path}")
    start = marker.end()
    rows, _ = json.JSONDecoder().raw_decode(text[start:])
    if not isinstance(rows, list):
        raise ValueError(f"Embedded problems payload is not a list: {path}")
    return rows


def format_detail(value: object, limit: int = 360) -> str:
    text = str(value).replace("\r", " ").replace("\n", " ").replace("|", "\\|")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def main() -> None:
    global SOURCE
    parser = argparse.ArgumentParser(
        description="Validate the published STEMHUB AMC 8 subtree against a validated AMC8_Codex output."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"Validated AMC 8 output directory (default: {DEFAULT_SOURCE})",
    )
    args = parser.parse_args()
    SOURCE = args.source.resolve()

    checks: list[tuple[str, bool, str]] = []

    def check(name: str, condition: bool, detail: object) -> None:
        checks.append((name, bool(condition), format_detail(detail)))

    check("AMC 8 publication directory exists", SITE.is_dir(), relative_name(SITE))
    if not SITE.is_dir():
        write_report(checks)
        raise SystemExit(1)

    # Aggregate CSV baseline and exact 10-year key set.
    try:
        fields, rows = read_csv(SITE / "all_problems.csv")
    except Exception as exc:
        fields, rows = [], []
        check("Aggregate CSV is readable", False, exc)
    else:
        check("Aggregate CSV is readable", True, "UTF-8 CSV parsed successfully")
    check("Aggregate CSV has the exact 12-column schema", fields == list(CSV_FIELDS), fields)
    check("Aggregate CSV contains exactly 250 rows", len(rows) == EXPECTED_PROBLEMS, len(rows))

    expected_keys = {(str(year), str(no)) for year in YEARS for no in range(1, 26)}
    actual_keys = {(row.get("year", ""), row.get("problem_no", "")) for row in rows}
    check(
        "Years and problem numbers are exactly the real 10 × 1-25 set",
        actual_keys == expected_keys and len(rows) == len(actual_keys),
        f"years={sorted({row.get('year', '') for row in rows})}; unique keys={len(actual_keys)}",
    )
    check("No 2021 data exists in the aggregate CSV", all(row.get("year") != "2021" for row in rows), "2021 rows=0")
    check(
        "contest is AMC 8 and form is empty for every row",
        all(row.get("contest") == "AMC 8" and row.get("form") == "" for row in rows),
        f"contest values={sorted({row.get('contest', '') for row in rows})}; non-empty forms={sum(bool(row.get('form')) for row in rows)}",
    )
    check(
        "Source labels are exact and unique",
        len({row.get("source", "") for row in rows}) == EXPECTED_PROBLEMS
        and all(
            row.get("source") == f"{row.get('year')} AMC 8 Problem {row.get('problem_no')}"
            for row in rows
        ),
        f"unique source labels={len({row.get('source', '') for row in rows})}",
    )
    check("No difficulty field was introduced", "difficulty" not in {field.lower() for field in fields}, fields)

    # Strict publication allowlist.
    root_files = {path.name for path in SITE.iterdir() if path.is_file()}
    root_dirs = {path.name for path in SITE.iterdir() if path.is_dir()}
    expected_root_dirs = {str(year) for year in YEARS} | {"assets", "problems"}
    check("Root files match the public allowlist", root_files == PUBLIC_ROOT_FILES, sorted(root_files))
    check("Root directories match the public allowlist", root_dirs == expected_root_dirs, sorted(root_dirs))

    annual_errors: list[str] = []
    annual_rows = 0
    for year in YEARS:
        year_dir = SITE / str(year)
        expected_names = {f"{year}.html", f"{year}_classified.md", f"{year}_problems.csv"}
        if not year_dir.is_dir():
            annual_errors.append(f"missing {year}/")
            continue
        names = {path.name for path in year_dir.iterdir()}
        if names != expected_names:
            annual_errors.append(f"{year}: unexpected set {sorted(names)}")
        try:
            year_fields, year_rows = read_csv(year_dir / f"{year}_problems.csv")
            annual_rows += len(year_rows)
            if year_fields != list(CSV_FIELDS) or len(year_rows) != 25:
                annual_errors.append(f"{year}: schema={year_fields}, rows={len(year_rows)}")
            if year_rows != [row for row in rows if row.get("year") == str(year)]:
                annual_errors.append(f"{year}: rows differ from aggregate")
        except Exception as exc:
            annual_errors.append(f"{year}: {exc}")
    check(
        "Ten annual directories contain only HTML/Markdown/CSV and exact 25-row slices",
        not annual_errors and annual_rows == EXPECTED_PROBLEMS,
        "all 10 years match" if not annual_errors else "; ".join(annual_errors[:8]),
    )

    expected_slugs = {f"{year}-amc-8-problem-{no}" for year in YEARS for no in range(1, 26)}
    problem_root = SITE / "problems"
    actual_slugs = {path.name for path in problem_root.iterdir() if path.is_dir()} if problem_root.is_dir() else set()
    detail_files = list(problem_root.glob("*/index.html")) if problem_root.is_dir() else []
    detail_extra = [
        relative_name(path)
        for path in problem_root.rglob("*")
        if path.is_file() and path.name != "index.html"
    ] if problem_root.is_dir() else []
    check(
        "Exactly 250 expected detail-page directories exist",
        actual_slugs == expected_slugs and len(detail_files) == EXPECTED_PROBLEMS and not detail_extra,
        f"slugs={len(actual_slugs)}; detail pages={len(detail_files)}; unexpected files={detail_extra[:5]}",
    )

    image_root = SITE / "assets" / "problems"
    image_files = sorted(path for path in image_root.rglob("*") if path.is_file()) if image_root.is_dir() else []
    check(
        "Exactly 76 local PNG diagram images are published",
        len(image_files) == EXPECTED_IMAGES and all(path.suffix.lower() == ".png" for path in image_files),
        f"images={len(image_files)}; extensions={dict(Counter(path.suffix.lower() for path in image_files))}",
    )

    # Entrypoint equivalence and embedded runtime data.
    overview = SITE / "all_years_index.html"
    entrypoint = SITE / "index.html"
    check(
        "amc8/index.html is an exact copy of all_years_index.html",
        entrypoint.is_file() and overview.is_file() and entrypoint.read_bytes() == overview.read_bytes(),
        "identical publication entrypoints",
    )
    embedded_errors: list[str] = []
    try:
        overview_rows = embedded_problems(overview)
        if len(overview_rows) != EXPECTED_PROBLEMS:
            embedded_errors.append(f"overview embeds {len(overview_rows)}")
        for year in YEARS:
            year_payload = embedded_problems(SITE / str(year) / f"{year}.html")
            if len(year_payload) != 25:
                embedded_errors.append(f"{year} embeds {len(year_payload)}")
    except Exception as exc:
        embedded_errors.append(str(exc))
    check(
        "Overview and annual pages embed the expected problem counts",
        not embedded_errors,
        "overview=250 and every year=25" if not embedded_errors else "; ".join(embedded_errors),
    )

    # Parse every public HTML page, validate navigation, links, images, and alt text.
    html_files = sorted(SITE.rglob("*.html"))
    broken_references: list[str] = []
    external_images: list[str] = []
    missing_alts: list[str] = []
    image_references: set[Path] = set()
    missing_site_nav: list[str] = []
    css_external_urls: list[str] = []
    residual_input_links: list[str] = []
    forbidden_form_controls: list[str] = []
    for page in html_files:
        text = page.read_text(encoding="utf-8")
        if 'data-stemhub-site-nav="1"' not in text:
            missing_site_nav.append(relative_name(page))
        if CSS_EXTERNAL_URL_RE.search(text):
            css_external_urls.append(relative_name(page))
        if re.search(r'(?i)(?:href|src)=["\'][^"\']*(?:\.\./)+input/', text):
            residual_input_links.append(relative_name(page))
        if re.search(r'(?i)(?:id=["\']formFilter["\']|data-form=|name=["\']form["\']|id=["\']difficulty["\'])', text):
            forbidden_form_controls.append(relative_name(page))

        parser = ReferenceParser()
        try:
            parser.feed(text)
        except Exception as exc:
            broken_references.append(f"{relative_name(page)}: HTML parse failed: {exc}")
            continue
        for tag, attribute, raw_url in parser.references:
            parsed = urlsplit(raw_url.strip())
            is_external = parsed.scheme.lower() in {"http", "https", "data"} or raw_url.startswith("//")
            if tag == "img" and is_external:
                external_images.append(f"{relative_name(page)} -> {raw_url}")
            target, error = local_target(page, raw_url)
            if error:
                broken_references.append(f"{relative_name(page)} -> {raw_url}: {error}")
            elif target is not None and not target.exists():
                broken_references.append(f"{relative_name(page)} -> {raw_url}")
            if tag == "img" and target is not None:
                image_references.add(target.resolve(strict=False))
        for src, alt in parser.images:
            if not alt.strip():
                missing_alts.append(f"{relative_name(page)} -> {src}")

    check("All 263 public HTML pages have STEMHUB/AMC10/AMC12 navigation", len(html_files) == 263 and not missing_site_nav, f"pages={len(html_files)}; missing nav={missing_site_nav[:5]}")
    check("All static local HTML links and resources resolve", not broken_references, "no broken references" if not broken_references else "; ".join(broken_references[:8]))
    check("No external images or CSS image hotlinks exist", not external_images and not css_external_urls, f"external img={external_images[:4]}; external CSS={css_external_urls[:4]}")
    check("Every embedded image has non-empty alt text", not missing_alts, "all image alt text present" if not missing_alts else "; ".join(missing_alts[:8]))
    expected_image_set = {path.resolve() for path in image_files}
    check("Every published diagram image is referenced by a page", image_references == expected_image_set, f"referenced={len(image_references)}; published={len(expected_image_set)}")
    check("No detail page links to an unpublished local input PDF", not residual_input_links, f"residual pages={residual_input_links[:8]}")
    check("AMC 8 HTML contains no A/B form or difficulty controls", not forbidden_form_controls, f"pages={forbidden_form_controls[:8]}")

    # Markdown links are public entry points too.
    markdown_errors: list[str] = []
    markdown_external_images: list[str] = []
    for page in sorted(SITE.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        for image_marker, raw_url in MARKDOWN_LINK_RE.findall(text):
            parsed = urlsplit(raw_url)
            if image_marker and (parsed.scheme.lower() in {"http", "https", "data"} or raw_url.startswith("//")):
                markdown_external_images.append(f"{relative_name(page)} -> {raw_url}")
            target, error = local_target(page, raw_url)
            if error:
                markdown_errors.append(f"{relative_name(page)} -> {raw_url}: {error}")
            elif target is not None and not target.exists():
                markdown_errors.append(f"{relative_name(page)} -> {raw_url}")
    check("All local Markdown links resolve", not markdown_errors, "no broken Markdown links" if not markdown_errors else "; ".join(markdown_errors[:8]))
    check("Markdown contains no external image hotlinks", not markdown_external_images, markdown_external_images[:8])

    # Local-path leakage and temporary/internal artifacts.
    leaked_paths: list[str] = []
    for path in sorted(SITE.rglob("*")):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            try:
                text = path.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                leaked_paths.append(f"{relative_name(path)}: not UTF-8")
                continue
            if LOCAL_PATH_RE.search(text):
                leaked_paths.append(relative_name(path))
    check("No absolute local paths, file URLs, or localhost URLs leak into publication files", not leaked_paths, leaked_paths[:8])

    temp_artifacts = [
        relative_name(path)
        for path in SITE.rglob("*")
        if any(part.lower() in {"tmp", "temp", "__pycache__", ".pytest_cache"} for part in path.parts)
        or path.suffix.lower() in {".tmp", ".bak", ".pyc"}
    ]
    check("No temporary, cache, backup, or internal audit artifacts are published", not temp_artifacts, temp_artifacts[:8])

    # Deterministic managed-file manifest and source provenance.
    manifest_errors: list[str] = []
    try:
        manifest = json.loads((SITE / "site_manifest.json").read_text(encoding="utf-8"))
        entries = manifest.get("files", [])
        manifest_paths = {entry.get("path") for entry in entries}
        actual_paths = {
            path.relative_to(SITE).as_posix()
            for path in SITE.rglob("*")
            if path.is_file() and path.name != "site_manifest.json"
        }
        if manifest_paths != actual_paths:
            manifest_errors.append(
                f"manifest paths={len(manifest_paths)}, actual managed paths={len(actual_paths)}"
            )
        for entry in entries:
            path = SITE / str(entry.get("path", ""))
            if not path.is_file():
                manifest_errors.append(f"missing {entry.get('path')}")
                continue
            if entry.get("sha256") != sha256(path) or entry.get("bytes") != path.stat().st_size:
                manifest_errors.append(f"hash/size mismatch {entry.get('path')}")
        declared = {
            "problem_count": EXPECTED_PROBLEMS,
            "detail_page_count": EXPECTED_PROBLEMS,
            "diagram_image_count": EXPECTED_IMAGES,
            "html_page_count": 263,
            "navigation_injected_page_count": 263,
            "local_pdf_links_replaced": EXPECTED_PDF_REFERENCES,
            "upstream_artifacts_verified": 363,
            "managed_file_count_excluding_manifest": len(actual_paths),
        }
        for key, expected in declared.items():
            if manifest.get(key) != expected:
                manifest_errors.append(f"{key}={manifest.get(key)!r}, expected {expected!r}")
        upstream_manifest = SOURCE / "manifest.json"
        if not upstream_manifest.is_file() or manifest.get("source_manifest_sha256") != sha256(upstream_manifest):
            manifest_errors.append("source manifest provenance hash is missing or stale")
    except Exception as exc:
        manifest_errors.append(str(exc))
    check("site_manifest.json covers every managed file with current SHA-256 and counts", not manifest_errors, "manifest current" if not manifest_errors else "; ".join(manifest_errors[:8]))

    # Copied data and teaching documents must be byte-identical to the validated source.
    source_drift: list[str] = []
    source_pairs = [
        (SOURCE / name, SITE / name)
        for name in (
            "all_problems.csv",
            "taxonomy.md",
            "method_index.md",
            "common_errors.md",
            "prerequisite_map.md",
        )
    ]
    for year in YEARS:
        source_pairs.extend(
            [
                (SOURCE / str(year) / f"{year}_classified.md", SITE / str(year) / f"{year}_classified.md"),
                (SOURCE / str(year) / f"{year}_problems.csv", SITE / str(year) / f"{year}_problems.csv"),
            ]
        )
    for source_path, site_path in source_pairs:
        if not source_path.is_file() or not site_path.is_file() or sha256(source_path) != sha256(site_path):
            source_drift.append(relative_name(site_path))
    check("Protected CSV/taxonomy/textbook Markdown is byte-identical to AMC8_Codex", not source_drift, "25 copied data/document files match" if not source_drift else source_drift[:8])

    # The repository home and fallback page must expose the new contest without
    # implying that AMC 8 has A/B forms.
    home_path = ROOT / "index.html"
    not_found_path = ROOT / "404.html"
    dictionary_path = ROOT / "assets" / "i18n-dictionary.js"
    try:
        home_text = home_path.read_text(encoding="utf-8")
        not_found_text = not_found_path.read_text(encoding="utf-8")
        dictionary_text = dictionary_path.read_text(encoding="utf-8")
    except Exception as exc:
        home_text = not_found_text = dictionary_text = ""
        integration_read_error = str(exc)
    else:
        integration_read_error = ""

    home_requirements = {
        'href="amc8/"': "AMC 8 entry",
        'href="amc8/all_problems.csv"': "AMC 8 CSV download",
        'href="amc8/taxonomy.md"': "AMC 8 taxonomy download",
        'href="amc8/textbook_index.html"': "AMC 8 textbook entry",
        "<strong>57</strong>": "57 year labels",
        "<strong>2600</strong>": "2,600 total problems",
        "<strong>2002-2025</strong>": "coverage through 2025",
        "A/B + 单卷": "honest mixed form structure",
    }
    missing_home = [label for needle, label in home_requirements.items() if needle not in home_text]
    check(
        "STEMHUB home exposes AMC 8 with current aggregate counts and honest form wording",
        not integration_read_error and not missing_home,
        "home integration current" if not missing_home and not integration_read_error else integration_read_error or missing_home,
    )

    check(
        "The site 404 page links to AMC 8",
        '/STEMHUB_AMC/amc8/' in not_found_text,
        "AMC 8 fallback link present" if '/STEMHUB_AMC/amc8/' in not_found_text else "AMC 8 fallback link missing",
    )
    i18n_ok = dictionary_text.count('"home.searchAmc8"') == 2 and dictionary_text.count('"home.amc8Description"') == 2 and dictionary_text.count('"home.formStructure"') == 2 and dictionary_text.count('"home.formStructureValue"') == 2
    check(
        "Home-page Chinese/English dictionary covers the AMC 8 integration",
        i18n_ok,
        "AMC 8 keys present in both languages" if i18n_ok else "AMC 8 home keys are incomplete",
    )

    home_link_errors: list[str] = []
    if home_text:
        parser = ReferenceParser()
        parser.feed(home_text)
        for _, _, raw_url in parser.references:
            target, error = local_target(home_path, raw_url)
            if error:
                home_link_errors.append(f"{raw_url}: {error}")
            elif target is not None and not target.exists():
                home_link_errors.append(f"{raw_url}: missing {relative_name(target)}")
    check(
        "All local links and assets on the STEMHUB home page resolve",
        not home_link_errors,
        "home links resolve" if not home_link_errors else home_link_errors[:8],
    )

    write_report(checks)
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        print(f"AMC 8 site validation FAILED: {len(checks) - len(failed)}/{len(checks)} checks passed")
        for name in failed:
            print(f"- {name}")
        raise SystemExit(1)
    print(f"AMC 8 site validation PASSED: {len(checks)}/{len(checks)} checks passed")
    print(f"Report: {REPORT}")


def write_report(checks: list[tuple[str, bool, str]]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    passed = sum(result for _, result, _ in checks)
    status = "PASS" if passed == len(checks) else "FAIL"
    lines = [
        "# AMC 8 Site Validation",
        "",
        f"- Result: **{status}**",
        f"- Checks passed: **{passed}/{len(checks)}**",
        "- Publication subtree: `amc8/`",
        "- Validated source: `AMC8_Codex/output`",
        "",
        "| # | Check | Result | Detail |",
        "|---:|---|:---:|---|",
    ]
    for index, (name, result, detail) in enumerate(checks, 1):
        lines.append(f"| {index} | {name} | {'PASS' if result else 'FAIL'} | {detail} |")
    lines.extend(
        [
            "",
            "## Publication contract",
            "",
            "The publication contains only the AMC 8 overview/textbook entry points, ten annual datasets/pages, 250 problem-detail pages, 76 locally hosted diagram PNGs, and the public taxonomy/method documents. Original PDFs, local audit artifacts, screenshots, temporary files, and local filesystem paths are intentionally excluded.",
            "",
        ]
    )
    REPORT.write_text("\n".join(lines), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
