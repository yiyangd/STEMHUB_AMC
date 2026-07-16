from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = Path(r"D:\AMC12_Codex")
ANSWER_KEYS = {
    "A": "CEBEBDBDEDECAEDBBEBDCDAEE",
    "B": "EBCECCDDBECBEBEBAAEAACACC",
}
EXPECTED_DIAGRAMS = {("A", "6"), ("A", "14"), ("A", "21"), ("B", "2"), ("B", "15")}
ORIGINAL_MISSING = {
    *(f"2021 Fall AMC 12A Problem {no}" for no in [10, 17, 18, 19, 20, 21, 24, 25]),
    *(f"2021 Fall AMC 12B Problem {no}" for no in [11, 13, 14, 15, 17, 18, 19, 21, 22, 24, 25]),
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def embedded_problems(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    marker = "const problems = "
    start = text.index(marker) + len(marker)
    rows, _ = json.JSONDecoder().raw_decode(text[start:])
    return rows


def main() -> None:
    amc10_fields, amc10 = read_csv(ROOT / "amc10" / "all_problems.csv")
    amc12_fields, amc12 = read_csv(ROOT / "amc12" / "all_problems.csv")
    annual_fields, annual_fall = read_csv(ROOT / "amc12" / "years" / "2021_fall" / "2021_fall_problems.csv")
    _, upstream_amc12 = read_csv(UPSTREAM / "output" / "all_problems.csv")
    if len(amc10) != 1150 or len(amc12) != 1200 or len(amc10) + len(amc12) != 2350:
        raise ValueError("Published AMC10/AMC12 totals are not 1150/1200/2350")
    if amc12 != upstream_amc12:
        raise ValueError("Published AMC12 aggregate is not identical to the validated upstream aggregate")
    if any("difficulty" in field.lower() or "难度" in field for field in amc10_fields + amc12_fields + annual_fields):
        raise ValueError("A difficulty field was introduced")

    fall = [row for row in amc12 if row["year"] == "2021 Fall"]
    spring = [row for row in amc12 if row["year"] == "2021 Spring"]
    if fall != annual_fall:
        raise ValueError("Published Fall annual and aggregate rows differ")
    expected_keys = {(form, str(no)) for form in "AB" for no in range(1, 26)}
    if len(fall) != 50 or {(row["form"], row["problem_no"]) for row in fall} != expected_keys:
        raise ValueError("Published Fall rows are not complete A1-A25/B1-B25")

    spring_by_key = {(row["form"], row["problem_no"]): normalize(row["statement"]) for row in spring}
    duplicates = [
        row["source"]
        for row in fall
        if normalize(row["statement"]) == spring_by_key[(row["form"], row["problem_no"])]
    ]
    if duplicates:
        raise ValueError(f"Fall statements duplicate Spring: {duplicates}")
    for row in fall:
        no = int(row["problem_no"])
        expected_answer = ANSWER_KEYS[row["form"]][no - 1]
        if row["answer"] != expected_answer:
            raise ValueError(f"Answer mismatch: {row['source']}")
        if not all(f"({letter})" in row["statement"] or f"\\textbf{{{letter}}}" in row["statement"] for letter in "ABCDE"):
            raise ValueError(f"Incomplete choices: {row['source']}")
        if not row["major_category"] or not row["minor_category"]:
            raise ValueError(f"Missing category: {row['source']}")
    diagram_rows = {
        (row["form"], row["problem_no"])
        for row in fall
        if "题面包含图形" in row["notes"]
    }
    if diagram_rows != EXPECTED_DIAGRAMS:
        raise ValueError(f"Diagram notes mismatch: {diagram_rows}")

    index_path = ROOT / "amc12" / "index.html"
    index_text = index_path.read_text(encoding="utf-8")
    index_rows = embedded_problems(index_path)
    index_fall = [row for row in index_rows if row["year"] == "2021 Fall"]
    if len(index_rows) != 1200 or index_fall != fall:
        raise ValueError("AMC12 overview embedded data is not synchronized")
    if index_text.count("data-stemhub-i18n-assets") != 3 or index_text.count("<!-- STEMHUB I18N ASSETS -->") != 1:
        raise ValueError("AMC12 bilingual asset block was damaged")
    map_start = index_text.index("const detailPages = new Map")
    map_end = index_text.index("]);", map_start) + 3
    if "2021 Fall AMC 12" in index_text[map_start:map_end]:
        raise ValueError("AMC12 overview still links to a stale Fall detail page")

    stale_dirs = list((ROOT / "amc12" / "problems").glob("2021-fall-amc-12?-problem-*"))
    if stale_dirs:
        raise ValueError(f"Stale Fall detail directories remain: {stale_dirs}")
    manifest = json.loads((ROOT / "problem_pages_manifest.json").read_text(encoding="utf-8"))
    if len(manifest) != 2086 or any(item.get("source", "").startswith("2021 Fall AMC 12") for item in manifest):
        raise ValueError("Problem-page manifest still contains stale Fall entries or an unexpected total")

    _, triage = read_csv(ROOT / "missing_problem_triage.csv")
    fall_triage = [row for row in triage if row["contest"] == "AMC 12" and row["year"] == "2021 Fall"]
    if len(triage) != 264 or len(fall_triage) != 50:
        raise ValueError("Corrected Fall rows did not all re-enter triage")
    triage_sources = {row["source"] for row in fall_triage}
    if not ORIGINAL_MISSING.issubset(triage_sources):
        raise ValueError("One or more of the 19 originally missing Fall rows did not re-enter triage")
    fall_statuses = Counter(row["triage_status"] for row in fall_triage)
    if fall_statuses != Counter({"ready_to_generate": 29, "needs_diagram": 5, "solution_high_risk": 16}):
        raise ValueError(f"Unexpected repaired Fall triage distribution: {fall_statuses}")

    source_manifest = json.loads((ROOT / "docs" / "audits" / "2021_fall_source_manifest.json").read_text(encoding="utf-8"))
    for form, source in source_manifest["canonical_pdfs"].items():
        upstream_source = UPSTREAM / source["path"]
        if sha256(upstream_source) != source["sha256"]:
            raise ValueError(f"Fall {form} source hash no longer matches the recorded provenance")
    quarantined = source_manifest["quarantined_source"]
    spring_pdf = UPSTREAM / "input" / "2021AMC_Spring.pdf"
    quarantine_pdf = UPSTREAM / quarantined["path"]
    if sha256(spring_pdf) != quarantined["sha256"] or sha256(quarantine_pdf) != quarantined["sha256"]:
        raise ValueError("Quarantined mislabeled Fall source is not the audited Spring duplicate")

    report = [
        "# 2021 Fall AMC 12 Repair Validation",
        "",
        f"- Validated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "- Result: PASS",
        "- AMC12 rows: 1,200",
        "- Combined AMC10/AMC12 rows: 2,350",
        "- 2021 Fall rows: 50 (A: 25, B: 25)",
        "- Normalized Spring/Fall statement duplicates: 0",
        "- Verified answer letters: 50/50",
        "- Rows with complete A-E choice markers: 50/50",
        "- Explicit diagram rows: A6, A14, A21, B2, B15",
        "- Stale Fall detail pages remaining: 0",
        "- Stale Fall manifest entries remaining: 0",
        "- Current problem-page manifest entries: 2,086",
        "- Current missing/triage rows: 264",
        "- Repaired Fall triage: ready_to_generate=29, needs_diagram=5, solution_high_risk=16",
        "",
        "## Source provenance",
        "",
    ]
    for form in "AB":
        source = source_manifest["canonical_pdfs"][form]
        report.append(
            f"- AMC 12{form}: {source['document_title']}; {source['exam_date']}; "
            f"{source['page_count']} pages; SHA-256 `{source['sha256']}`; {source['url']}"
        )
    report += [
        "",
        "## Release checks",
        "",
        "- Published annual CSV equals the Fall slice of `amc12/all_problems.csv`.",
        "- Published AMC12 aggregate equals the validated upstream aggregate.",
        "- The overview embeds all 1,200 rows and the corrected 50-row Fall slice.",
        "- The overview bilingual asset block remains present exactly once.",
        "- The detail-link map contains no invalidated Fall link.",
        "- No CSV schema contains a difficulty field.",
        "- All 19 originally missing Fall rows are present in the new triage, along with the 31 invalidated rows.",
        "",
        "Teaching solutions were intentionally not regenerated in this repair round.",
    ]
    output = ROOT / "docs" / "audits" / "2021_fall_repair_validation.md"
    output.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "report": str(output), "fall_triage": fall_statuses}, ensure_ascii=False, default=dict, indent=2))


if __name__ == "__main__":
    main()
