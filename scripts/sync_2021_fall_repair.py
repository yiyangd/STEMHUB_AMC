from __future__ import annotations

import csv
import json
import re
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = Path(r"D:\AMC12_Codex")
AMC12 = ROOT / "amc12"
FALL_PREFIX = "2021 Fall AMC 12"
ANSWER_KEYS = {
    "A": "CEBEBDBDEDECAEDBBEBDCDAEE",
    "B": "EBCECCDDBECBEBEBAAEAACACC",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def validate_upstream() -> None:
    fall = read_csv(UPSTREAM / "output" / "2021_fall" / "2021_fall_problems.csv")
    spring = read_csv(UPSTREAM / "output" / "2021_spring" / "2021_spring_problems.csv")
    expected = {(form, str(no)) for form in "AB" for no in range(1, 26)}
    actual = {(row["form"], row["problem_no"]) for row in fall}
    if len(fall) != 50 or actual != expected:
        raise ValueError("Upstream 2021 Fall CSV is not a complete A1-A25/B1-B25 dataset")
    spring_by_key = {(row["form"], row["problem_no"]): normalize(row["statement"]) for row in spring}
    for row in fall:
        no = int(row["problem_no"])
        if row["answer"] != ANSWER_KEYS[row["form"]][no - 1]:
            raise ValueError(f"Upstream answer mismatch: {row['source']}")
        if normalize(row["statement"]) == spring_by_key[(row["form"], row["problem_no"])]:
            raise ValueError(f"Upstream Fall statement still duplicates Spring: {row['source']}")


def replace_embedded_problems(target: Path, source: Path) -> int:
    target_text = target.read_text(encoding="utf-8")
    source_text = source.read_text(encoding="utf-8")
    marker = "const problems = "
    source_start = source_text.index(marker) + len(marker)
    problems, source_end = json.JSONDecoder().raw_decode(source_text[source_start:])
    target_start = target_text.index(marker) + len(marker)
    _, target_end = json.JSONDecoder().raw_decode(target_text[target_start:])
    updated = target_text[:target_start] + json.dumps(problems, ensure_ascii=False) + target_text[target_start + target_end :]
    target.write_text(updated, encoding="utf-8")
    return len(problems)


def source_from_slug(slug: str) -> str:
    parts = slug.split("-")
    if len(parts) < 5 or parts[-2] != "problem":
        return ""
    form_token = parts[-3]
    if not re.fullmatch(r"(10|12)[ab]", form_token):
        return ""
    year_parts = parts[:-4]
    year = " ".join(part.capitalize() if not part.isdigit() else part for part in year_parts)
    return f"{year} AMC {form_token[:-1]}{form_token[-1].upper()} Problem {parts[-1]}"


def refresh_detail_map(manifest: list[dict]) -> int:
    index_path = AMC12 / "index.html"
    text = index_path.read_text(encoding="utf-8")
    entries: dict[str, str] = {}
    problems_dir = AMC12 / "problems"
    for child in sorted(problems_dir.iterdir()):
        if child.is_dir() and (child / "index.html").exists():
            source = source_from_slug(child.name)
            if source:
                entries[source] = f"problems/{child.name}/"
    for item in manifest:
        if item.get("contest") == "AMC 12":
            entries[str(item["source"])] = str(item["relative_url"])
    pairs = ", ".join(
        f"[{json.dumps(source, ensure_ascii=False)}, {json.dumps(url, ensure_ascii=False)}]"
        for source, url in sorted(entries.items())
    )
    replacement = f"const detailPages = new Map([{pairs}]);"
    updated, count = re.subn(r"const detailPages = new Map\(\[[\s\S]*?\]\);", replacement, text, count=1)
    if count != 1:
        raise ValueError("Could not replace AMC12 detailPages map")
    index_path.write_text(updated, encoding="utf-8")
    return len(entries)


def copy_published_data() -> None:
    annual_source = UPSTREAM / "output" / "2021_fall"
    annual_target = AMC12 / "years" / "2021_fall"
    annual_target.mkdir(parents=True, exist_ok=True)
    for name in ["2021_fall_problems.csv", "2021_fall_classified.md", "2021_fall.html"]:
        shutil.copy2(annual_source / name, annual_target / name)

    for source_name, target_name in [
        ("all_problems.csv", "all_problems.csv"),
        ("taxonomy.md", "taxonomy.md"),
        ("manifest.json", "manifest.json"),
        ("progress_report.md", "progress_report.md"),
        ("resume_prompt.md", "resume_prompt.md"),
        ("validation_report.md", "validation_report.md"),
    ]:
        shutil.copy2(UPSTREAM / "output" / source_name, AMC12 / target_name)

    audit_dir = ROOT / "docs" / "audits"
    audit_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        UPSTREAM / "sources" / "2021_fall" / "source_manifest.json",
        audit_dir / "2021_fall_source_manifest.json",
    )


def remove_stale_pages_and_manifest() -> tuple[int, int, list[dict]]:
    manifest_path = ROOT / "problem_pages_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    removed_entries = [item for item in manifest if item.get("source", "").startswith(FALL_PREFIX)]
    kept = [item for item in manifest if not item.get("source", "").startswith(FALL_PREFIX)]
    manifest_path.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")

    problems_dir = (AMC12 / "problems").resolve()
    removed_dirs = 0
    for child in list(problems_dir.glob("2021-fall-amc-12?-problem-*")):
        resolved = child.resolve()
        if resolved.parent != problems_dir:
            raise ValueError(f"Refusing to remove path outside AMC12 problems: {resolved}")
        shutil.rmtree(resolved)
        removed_dirs += 1
    return len(removed_entries), removed_dirs, kept


def main() -> None:
    validate_upstream()
    copy_published_data()
    embedded_count = replace_embedded_problems(AMC12 / "index.html", UPSTREAM / "output" / "all_years_index.html")
    removed_entries, removed_dirs, manifest = remove_stale_pages_and_manifest()
    detail_link_count = refresh_detail_map(manifest)
    result = {
        "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "embedded_amc12_rows": embedded_count,
        "removed_fall_manifest_entries": removed_entries,
        "removed_fall_detail_directories": removed_dirs,
        "remaining_manifest_entries": len(manifest),
        "amc12_detail_links": detail_link_count,
        "next_action": "Re-triage all 50 corrected 2021 Fall rows; do not restore stale teaching pages.",
    }
    result_path = ROOT / "docs" / "audits" / "2021_fall_sync_result.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
