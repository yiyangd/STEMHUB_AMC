import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRIAGE_STATUSES = [
    "ready_to_generate",
    "needs_diagram",
    "ocr_or_statement_risk",
    "solution_high_risk",
    "needs_answer_verification",
    "manual_review",
]


SOURCE_RE = re.compile(
    r"(?P<source>\d{4}(?:\s+(?:Spring|Fall))?\s+AMC\s+(?:10|12)[AB]\s+Problem\s+\d+)",
    re.IGNORECASE,
)


def read_csv_rows(contest_dir):
    path = ROOT / contest_dir / "all_problems.csv"
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_manifest_sources():
    path = ROOT / "problem_pages_manifest.json"
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return {row.get("source", "") for row in data if row.get("source")}


def normalize_source(source):
    return re.sub(r"\s+", " ", source.strip())


def collect_previous_reasons():
    reasons = defaultdict(list)
    progress_path = ROOT / "problem_pages_progress.md"
    report_path = ROOT / "problem_pages_report.md"
    text = ""
    for path in [progress_path, report_path, ROOT / "resume_prompt.md"]:
        if path.exists():
            text += "\n" + path.read_text(encoding="utf-8", errors="ignore")

    for line in text.splitlines():
        if "skipped" not in line.lower() and "Skipped reasons" not in line:
            continue
        fragments = re.split(r";\s*", line.strip())
        for fragment in fragments:
            if not SOURCE_RE.search(fragment):
                continue
            # Keep single-problem fragments separate; this prevents a diagram
            # note for one skipped problem from being assigned to every source
            # mentioned on the same progress line.
            for match in SOURCE_RE.finditer(fragment):
                source = normalize_source(match.group("source"))
                reason = fragment.strip().lstrip("- ").strip()
                if reason and reason not in reasons[source]:
                    reasons[source].append(reason)
        # Older "Review notes" lines sometimes mention sources without
        # semicolon-separated reasons. Preserve them as a fallback only when no
        # more specific fragment was recorded above.
        if ";" in line:
            continue
        for match in SOURCE_RE.finditer(line):
            source = normalize_source(match.group("source"))
            reason = line.strip().lstrip("- ").strip()
            if reason and reason not in reasons[source]:
                reasons[source].append(reason)
    return reasons


def has_choices(statement):
    return all(f"({letter})" in statement for letter in "ABCDE")


def looks_ocr_risky(statement, previous_reason):
    s = statement.lower()
    r = previous_reason.lower()
    ocr_markers = [
        "ocr",
        "truncated",
        "ambiguous",
        "corrupt",
        "damaged",
        "missing",
        "choices are missing",
        "expression is unreliable",
        "formula",
        "symbol",
        "radical ambiguity",
        "fraction ambiguity",
        "omits",
        "lacks",
    ]
    if any(marker in r for marker in ocr_markers):
        return True
    if len(statement.strip()) < 80:
        return True
    if "?" not in statement and "What" not in statement and "Find" not in statement:
        return True
    if any(bad in statement for bad in ["鈭", "鈮", "蟺", "漏", "矨", "燱"]):
        return True
    if not has_choices(statement):
        # Some newer CSV rows omit choices even when the stem is good. Treat
        # hard problems with missing choices as OCR risk; easier stems can be
        # answer-key verified during generation.
        return True
    return False


def looks_diagram_dependent(row, previous_reason):
    note = row.get("notes", "")
    s = row.get("statement", "").lower()
    r = previous_reason.lower()
    if "题面包含图形" in note:
        return True
    diagram_markers = [
        "diagram",
        "figure",
        "shaded",
        "grid",
        "graph",
        "map",
        "layout",
        "drawing",
        "original figure",
        "missing figure",
        "depends on the missing",
        "requires the original",
    ]
    if any(marker in r for marker in diagram_markers):
        return True
    if any(marker in s for marker in ["figure below", "shown below", "diagram", "shaded region", "grid shown"]):
        return True
    return False


def looks_solution_high_risk(row, previous_reason):
    r = previous_reason.lower()
    if any(marker in r for marker in ["high-risk", "high risk", "risk is high", "long proof", "dedicated"]):
        return True
    if ("careful" in r and "derivation" in r) or ("longer" in r and "derivation" in r) or ("risk" in r and "derivation" in r):
        return True
    problem_no = int(row["problem_no"])
    major = row.get("major_category", "")
    minor = row.get("minor_category", "")
    key = row.get("key_idea", "")
    statement = row.get("statement", "")
    hard_markers = [
        "recurrence",
        "recursive",
        "functional equation",
        "lattice",
        "complex",
        "polynomial",
        "tangent",
        "incircle",
        "circumcircle",
        "sphere",
        "pyramid",
        "octahedron",
        "probability",
        "expected",
        "最大",
        "最小",
        "递推",
        "复数",
        "切",
        "圆",
        "空间",
        "枚举",
    ]
    if problem_no >= 21:
        return True
    if problem_no >= 17 and major in {"几何", "组合数学", "综合题"}:
        return True
    combined = " ".join([minor, key, statement]).lower()
    if problem_no >= 16 and any(marker.lower() in combined for marker in hard_markers):
        return True
    return False


def classify(row, previous_reasons):
    previous_reason = " | ".join(previous_reasons)
    if looks_diagram_dependent(row, previous_reason):
        return "needs_diagram", previous_reason or "statement/notes indicate diagram dependence"
    if looks_ocr_risky(row.get("statement", ""), previous_reason):
        return "ocr_or_statement_risk", previous_reason or "statement appears incomplete, lacks choices, or has OCR-risk markers"
    if "answer" in previous_reason.lower() and "key" in previous_reason.lower():
        return "needs_answer_verification", previous_reason
    if looks_solution_high_risk(row, previous_reason):
        return "solution_high_risk", previous_reason or "late/problem-specific derivation risk; should be reviewed before unattended generation"
    return "ready_to_generate", previous_reason or "complete non-diagram statement with moderate-risk topic"


def sort_key(row):
    year = str(row["year"])
    year_base = int(re.match(r"\d{4}", year).group(0))
    season_rank = 0
    if "Spring" in year:
        season_rank = 1
    elif "Fall" in year:
        season_rank = 2
    contest_rank = 10 if row["contest"] == "AMC 10" else 12
    form_rank = 0 if row["form"] == "A" else 1
    return (contest_rank, year_base, season_rank, form_rank, int(row["problem_no"]))


def make_markdown(rows):
    total = len(rows)
    by_contest = Counter(row["contest"] for row in rows)
    by_status = Counter(row["triage_status"] for row in rows)
    by_contest_status = defaultdict(Counter)
    for row in rows:
        by_contest_status[row["contest"]][row["triage_status"]] += 1

    ready = [row for row in rows if row["triage_status"] == "ready_to_generate"][:20]
    diagram = [row for row in rows if row["triage_status"] == "needs_diagram"][:60]
    dangerous = [
        row
        for row in rows
        if row["triage_status"] in {"solution_high_risk", "ocr_or_statement_risk", "manual_review"}
    ][:80]

    lines = [
        "# Missing Problem Triage",
        "",
        f"- Generated at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"- Missing total: {total}",
        f"- AMC10 missing total: {by_contest.get('AMC 10', 0)}",
        f"- AMC12 missing total: {by_contest.get('AMC 12', 0)}",
        "",
        "## Status Counts",
        "",
        "| triage_status | count |",
        "|---|---:|",
    ]
    for status in TRIAGE_STATUSES:
        lines.append(f"| `{status}` | {by_status.get(status, 0)} |")

    lines += ["", "## Status Counts By Contest", ""]
    lines += ["| contest | ready | diagram | OCR/statement | solution high-risk | answer verification | manual review |"]
    lines += ["|---|---:|---:|---:|---:|---:|---:|"]
    for contest in ["AMC 10", "AMC 12"]:
        c = by_contest_status[contest]
        lines.append(
            f"| {contest} | {c['ready_to_generate']} | {c['needs_diagram']} | {c['ocr_or_statement_risk']} | "
            f"{c['solution_high_risk']} | {c['needs_answer_verification']} | {c['manual_review']} |"
        )

    lines += ["", "## Recommended Next 20 Ready-To-Generate Problems", ""]
    if ready:
        for row in ready:
            lines.append(
                f"- `{row['source']}` ({row['major_category']} / {row['minor_category']}): {row['missing_reason_guess']}"
            )
    else:
        lines.append("- None. The remaining missing set should be reviewed before automatic generation.")

    lines += ["", "## Most Need Manual Diagram Support", ""]
    if diagram:
        for row in diagram:
            lines.append(f"- `{row['source']}`: {row['missing_reason_guess']}")
    else:
        lines.append("- None detected.")

    lines += ["", "## Highest-Risk / Not Recommended For Automatic Generation", ""]
    if dangerous:
        for row in dangerous:
            lines.append(
                f"- `{row['source']}` [{row['triage_status']}]: {row['missing_reason_guess']}"
            )
    else:
        lines.append("- None detected.")

    lines += [
        "",
        "## Suggested Next Step",
        "",
        "Use the ready-to-generate list first. Keep diagram-dependent items in a separate manual-image workflow, and handle OCR/high-risk items only after checking the original PDF or AoPS statement.",
        "",
    ]
    return "\n".join(lines)


def update_progress(rows):
    counts = Counter(row["triage_status"] for row in rows)
    by_contest = Counter(row["contest"] for row in rows)
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    progress_path = ROOT / "problem_pages_progress.md"
    old = progress_path.read_text(encoding="utf-8")
    old = re.sub(r"\n## Missing/Skipped Problem Triage\n\n[\s\S]*?(?=\n## |\Z)", "\n", old).rstrip() + "\n\n"
    progress_path.write_text(
        old
        + "## Missing/Skipped Problem Triage\n\n"
        + f"- Time: {now}\n"
        + f"- Missing total: {len(rows)}\n"
        + f"- AMC10 missing total: {by_contest.get('AMC 10', 0)}\n"
        + f"- AMC12 missing total: {by_contest.get('AMC 12', 0)}\n"
        + "- Status counts: "
        + ", ".join(f"{status}={counts.get(status, 0)}" for status in TRIAGE_STATUSES)
        + "\n"
        + "- Output files: `missing_problem_triage.csv`, `missing_problem_triage.md`\n"
        + "- Validation result: pending commit\n",
        encoding="utf-8",
    )


def update_resume(rows):
    ready = [row for row in rows if row["triage_status"] == "ready_to_generate"][:20]
    counts = Counter(row["triage_status"] for row in rows)
    lines = [
        "请继续 STEMHUB AMC problem teaching pages 补完阶段。",
        "",
        "当前状态：missing/skipped problem triage 已生成并通过本地验证。",
        f"- Missing total: {len(rows)}",
        "- Status counts: "
        + ", ".join(f"{status}={counts.get(status, 0)}" for status in TRIAGE_STATUSES),
        "",
        "下一步建议：优先从 `missing_problem_triage.md` 的 ready_to_generate 列表中挑 5-10 道题生成详情页；diagram/OCR/high-risk 题先不要硬编。",
        "",
        "推荐下一批：",
    ]
    if ready:
        lines.extend(f"- {row['source']}" for row in ready[:10])
    else:
        lines.append("- 没有自动推荐题；请先人工检查 diagram/OCR/high-risk 列表。")
    lines += [
        "",
        "继续要求：每批生成、验证 MathJax/manifest/detail links/teaching steps，然后 commit/push；不要提交 PDF、input、tmp、缓存文件。",
    ]
    (ROOT / "resume_prompt.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    manifest_sources = read_manifest_sources()
    previous_reasons = collect_previous_reasons()

    missing = []
    for contest_dir in ["amc10", "amc12"]:
        for row in read_csv_rows(contest_dir):
            source = normalize_source(row["source"])
            if source in manifest_sources:
                continue
            status, reason = classify(row, previous_reasons.get(source, []))
            missing.append(
                {
                    "contest": row["contest"],
                    "year": row["year"],
                    "form": row["form"],
                    "problem_no": row["problem_no"],
                    "source": source,
                    "major_category": row.get("major_category", ""),
                    "minor_category": row.get("minor_category", ""),
                    "tags": row.get("tags", ""),
                    "notes": row.get("notes", ""),
                    "missing_reason_guess": reason,
                    "triage_status": status,
                }
            )

    missing.sort(key=sort_key)

    csv_path = ROOT / "missing_problem_triage.csv"
    fields = [
        "contest",
        "year",
        "form",
        "problem_no",
        "source",
        "major_category",
        "minor_category",
        "tags",
        "notes",
        "missing_reason_guess",
        "triage_status",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(missing)

    (ROOT / "missing_problem_triage.md").write_text(make_markdown(missing), encoding="utf-8")
    update_progress(missing)
    update_resume(missing)

    print(json.dumps({
        "missing_total": len(missing),
        "status_counts": Counter(row["triage_status"] for row in missing),
        "contest_counts": Counter(row["contest"] for row in missing),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
