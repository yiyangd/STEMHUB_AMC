from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 31
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2006_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21, 22, 25}
SKIPPED = [
    "2006 AMC 10B Problem 23 skipped: statement depends on a diagram for the area partition.",
    "2006 AMC 10B Problem 24 skipped: statement and choices are truncated by OCR and depend on a diagram.",
]
BATCH_LABEL = "2006 AMC 10B Problems 21, 22, 25"
NEXT_START = "2007 AMC 10A Problem 1"

ANS = {
    21: ("C", r"\frac{8}{63}"),
    22: ("D", "$1.65"),
    25: ("B", "5"),
}


OV = {
    21: (
        r"For a particular peculiar pair of dice, the probabilities of rolling $1,2,3,4,5,$ and $6$ on each die are in the ratio $1:2:3:4:5:6$. What is the probability of rolling a total of $7$ on the two dice?",
        [("A", r"$\frac{4}{63}$"), ("B", r"$\frac18$"), ("C", r"$\frac{8}{63}$"), ("D", r"$\frac16$"), ("E", r"$\frac27$")],
    ),
    22: (
        r"Elmo makes $N$ sandwiches for a fundraiser. For each sandwich he uses $B$ globs of peanut butter at $4$ cents per glob and $J$ blobs of jam at $5$ cents per blob. The cost of the peanut butter and jam to make all the sandwiches is $\$2.53$. Assume that $B$, $J$, and $N$ are all positive integers with $N>1$. What is the cost of the jam Elmo uses to make the sandwiches?",
        [("A", "$1.05"), ("B", "$1.25"), ("C", "$1.45"), ("D", "$1.65"), ("E", "$1.85")],
    ),
    25: (
        r"Mr. Jones has eight children of different ages. On a family trip his oldest child, who is $9$, spots a license plate with a $4$-digit number in which each of two digits appears two times. \"Look, daddy!\" she exclaims. \"That number is evenly divisible by the age of each of us kids!\" \"That's right,\" replies Mr. Jones, \"and the last two digits just happen to be my age.\" Which of the following is not the age of one of Mr. Jones's children?",
        [("A", "$4$"), ("B", "$5$"), ("C", "$6$"), ("D", "$7$"), ("E", "$8$")],
    ),
}


KEY_OVERRIDES = {
    21: "Use weighted probability: each ordered dice outcome has probability proportional to the product of the two face weights.",
    22: "Use integer factorization and modular constraints on the per-sandwich cost.",
    25: "Use divisibility by ages 1 through 9 and the special repeated-digit structure of the license plate.",
}


SOL = {
    21: [
        ("Turn the ratio into probabilities", r"The weights for faces $1$ through $6$ are $1,2,3,4,5,6$. Their total is $1+2+3+4+5+6=21$, so the probability of rolling face $k$ on one die is $\frac{k}{21}$."),
        ("List the ways to total 7", r"The ordered pairs that sum to $7$ are $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$. Because the dice are rolled separately, order matters."),
        ("Add weighted probabilities", r"For a pair $(i,j)$, the probability is $\frac{i}{21}\cdot\frac{j}{21}$. Therefore the numerator weight is \[1\cdot6+2\cdot5+3\cdot4+4\cdot3+5\cdot2+6\cdot1=56.\]"),
        ("Divide by the total weight", r"The denominator is $21^2=441$, so the probability is $\frac{56}{441}=\frac{8}{63}$."),
        ("Answer", r"The answer is $\boxed{\frac{8}{63}}$."),
    ],
    22: [
        ("Write the cost equation", r"For one sandwich, the peanut butter and jam cost $4B+5J$ cents. For $N$ sandwiches, the total is \[N(4B+5J)=253.\]"),
        ("Factor the total", r"Since $253=11\cdot23$ and $N>1$, the possible values of $N$ are $11$ or $23$ if the per-sandwich cost is an integer factor greater than $1$."),
        ("Test the per-sandwich costs", r"If $N=23$, then $4B+5J=11$, but positive integers $B,J$ cannot make $11$ because the smallest possible cost is $4+5=9$ and the next possibilities skip $11$. If $N=11$, then $4B+5J=23$."),
        ("Solve for positive integers", r"The equation $4B+5J=23$ has the positive solution $B=2$, $J=3$, since $4\cdot2+5\cdot3=8+15=23$."),
        ("Find the total jam cost", r"Each sandwich uses $3$ blobs of jam at $5$ cents each, so jam costs $15$ cents per sandwich. For $11$ sandwiches, the jam cost is $11\cdot15=165$ cents, or $\$1.65$."),
        ("Answer", r"The answer is $\boxed{\$1.65}$."),
    ],
    25: [
        ("Translate the ages condition", r"The oldest child is $9$, and there are eight children of different ages. So the children's ages are eight different numbers chosen from $1,2,\ldots,9$, and the license number is divisible by all eight of them."),
        ("Use the repeated-digit condition", r"The license number has four digits with exactly two digits appearing twice. We need such a number that is divisible by $9$ and by seven other ages from $1$ through $8$."),
        ("Look for the missing age", r"Testing divisibility is efficient here because the possible ages are only $1$ through $9$. The number $5544$ has two $5$s and two $4$s, and it is divisible by $1,2,3,4,6,7,8,$ and $9$."),
        ("Check the divisibility", r"Indeed, $5544$ is even, its last two digits $44$ are divisible by $4$, its digit sum is $18$ so it is divisible by $3$ and $9$, and $5544\div7=792$. Also $5544\div8=693$."),
        ("Identify the age not included", r"The divisors from $1$ to $9$ that work are $1,2,3,4,6,7,8,9$. The only missing possible age among the answer choices is $5$."),
        ("Answer", r"Therefore $\boxed{5}$ is not the age of one of Mr. Jones's children."),
    ],
}


def esc(x, quote=True):
    return html.escape(str(x), quote=quote)


def slug(src: str) -> str:
    s = src.lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9-]", "", s)
    return re.sub(r"-+", "-", s).strip("-")


def source_from_slug(sl: str) -> str:
    p = sl.split("-")
    if len(p) < 5 or p[-2] != "problem":
        return ""
    f = p[-3]
    if not re.fullmatch(r"(10|12)[ab]", f):
        return ""
    return f"{' '.join(x.capitalize() if not x.isdigit() else x for x in p[:-4])} AMC {f[:-1]}{f[-1].upper()} Problem {p[-1]}"


def split_choices(st: str):
    ms = list(re.finditer(r"\s*\(([A-E])\)\s*", st))
    if len(ms) < 5:
        return st.strip(), []
    stem = st[: ms[0].start()].strip()
    out = []
    for i, m in enumerate(ms):
        out.append((m.group(1), st[m.end() : (ms[i + 1].start() if i + 1 < len(ms) else len(st))].strip()))
    return stem, out


def aops(row):
    return f"https://artofproblemsolving.com/wiki/index.php/{row['year']}_{row['contest'].replace(' ', '_')}{row['form']}_Problems/Problem_{row['problem_no']}"


def render(row):
    n = int(row["problem_no"])
    statement, choices = OV.get(n, (row["statement"], None))
    stem, parsed = split_choices(statement)
    choices = choices or parsed
    ans, val = ANS[n]
    tags = "".join(f'<span class="badge">{esc(t)}</span>' for t in (row.get("tags") or "").split(";") if t)
    notes = row.get("notes") or ""
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in set()) else notes
    note_html = f'<section class="section"><h2>Notes</h2><p>{esc(note)}</p></section>' if note else ""
    choices_html = "".join(
        f'<li class="choice {"correct" if k == ans else ""}"><span class="choice-key">{esc(k)}</span><span>{esc(v, False)}</span></li>'
        for k, v in choices
    )
    steps = "".join(
        f'<section class="step"><h3>Step {i}: {esc(t)}</h3>'
        + "".join(f'<p>{esc(part.strip(), False)}</p>' for part in re.split(r"\n\s*\n", b) if part.strip())
        + "</section>"
        for i, (t, b) in enumerate(SOL[n], 1)
    )
    src = row["source"]
    key_idea = KEY_OVERRIDES.get(n, row.get("key_idea", ""))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(src)} - STEMHUB AMC</title><style>:root{{--bg:#f7f4ee;--panel:#fff;--ink:#1e2832;--line:#d8ddd8;--blue:#2166a5;--chip:#eef3f7}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,"Segoe UI",Arial,sans-serif}}.site-nav{{display:flex;justify-content:space-between;gap:16px;background:#10283d;color:#fff;padding:10px clamp(18px,4vw,32px)}}.site-brand,.site-links a{{color:#fff;text-decoration:none}}.site-links{{display:flex;flex-wrap:wrap;gap:8px}}.site-links a{{border:1px solid rgba(255,255,255,.18);border-radius:6px;padding:7px 10px}}main{{width:min(1000px,calc(100% - 36px));margin:0 auto;padding:28px 0 48px}}.back{{display:inline-flex;padding:8px 12px;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--blue);text-decoration:none;font-weight:700}}h1{{font-size:clamp(28px,4vw,40px)}}.meta{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px}}.badge{{display:inline-flex;min-height:24px;padding:3px 8px;border-radius:999px;background:var(--chip);font-size:12px}}.badge.major{{background:#e8f0dc;color:#35592f}}.section{{background:#fff;border:1px solid var(--line);border-radius:8px;padding:18px;margin-top:14px}}.statement{{font-size:18px;line-height:1.65}}.choices{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}.choice{{display:grid;grid-template-columns:38px 1fr;gap:10px;border:1px solid var(--line);border-radius:6px;padding:8px 10px}}.choice.correct{{border-color:#abc8a6;background:#f1f8ef}}.choice-key{{display:grid;place-items:center;width:28px;height:28px;border-radius:999px;background:#e8f0dc;font-weight:750}}.answer{{padding:6px 10px;border-radius:6px;background:#eef6f1;color:#315c34;font-weight:750}}.step{{border-left:3px solid var(--blue);padding-left:14px;margin-top:16px}}.step h3{{font-size:16px}}.step p,.section p{{line-height:1.65;color:#33414e}}</style><script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\(','\\)']],displayMath:[['\\\\[','\\\\]']]}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script></head><body><nav class="site-nav"><a class="site-brand" href="../../../">STEMHUB AMC</a><div class="site-links"><a href="../../../">Home</a><a href="../../../amc10/">AMC 10</a><a href="../../../amc12/">AMC 12</a><a href="../../">Back to Overview</a></div></nav><main><a class="back" href="../../">Back to AMC 10 Overview</a><h1>{esc(src)}</h1><div class="meta"><span class="badge">{row['year']}</span><span class="badge">{row['contest']}{row['form']}</span><span class="badge">Problem {row['problem_no']}</span><span class="badge major">{esc(row['major_category'])}</span><span class="badge">{esc(row['minor_category'])}</span>{tags}</div><section class="section"><h2>Problem Statement</h2><p class="statement">{esc(stem, False)}</p></section><section class="section"><h2>Choices</h2><ol class="choices">{choices_html}</ol></section><section class="section"><h2>Answer</h2><span class="answer">{ans}. {esc(val, False)}</span></section><section class="section"><h2>Solution</h2>{steps}</section><section class="section"><h2>Key Idea</h2><p>{esc(key_idea)}</p></section>{note_html}<section class="section references"><h2>Reference</h2><p>Answer verified with <a href="{ANSWER_KEY_URL}">AoPS Answer Key</a>. Related page: <a href="{aops(row)}">AoPS problem page</a>.</p></section></main></body></html>'''


def update_index(contest):
    path = ROOT / contest / "index.html"
    text = path.read_text(encoding="utf-8")
    mp = {}
    for f in (ROOT / contest / "problems").glob("*/index.html"):
        src = source_from_slug(f.parent.name)
        if src:
            mp[src] = f"problems/{f.parent.name}/"
    pairs = ", ".join(f"[{json.dumps(k, ensure_ascii=False)}, {json.dumps(v, ensure_ascii=False)}]" for k, v in sorted(mp.items()))
    text = re.sub(r"const detailPages = new Map\(\[[\s\S]*?\]\);", f"const detailPages = new Map([{pairs}]);", text, count=1)
    path.write_text(text, encoding="utf-8")


def validate(items):
    fails = []
    for it in items:
        t = Path(it["output_path"]).read_text(encoding="utf-8")
        main = t.split("<main>", 1)[1].split("</main>", 1)[0]
        if "displayMath:[['\\\\[','\\\\]']]" not in t:
            fails.append(it["source"] + " bad MathJax config")
        if "\\\\[" in main or "\\\\]" in main:
            fails.append(it["source"] + " double display delimiter in body")
        if t.count('<section class="step">') < 4:
            fails.append(it["source"] + " fewer than 4 steps")
        if "AoPS Answer Key" not in t:
            fails.append(it["source"] + " missing AoPS answer key reference")
    if fails:
        raise RuntimeError("\n".join(fails))


def main():
    start = datetime.now().astimezone().isoformat(timespec="seconds")
    csv_path = ROOT / CONTEST_DIR / "all_problems.csv"
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        all_rows = list(csv.DictReader(f))
    rows = [
        r
        for r in all_rows
        if r["year"] == "2006" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
    ]
    rows.sort(key=lambda r: int(r["problem_no"]))
    if len(rows) != len(TARGET_NUMBERS):
        raise RuntimeError(f"Expected {len(TARGET_NUMBERS)} rows, found {len(rows)}")

    manifest_path = ROOT / "problem_pages_manifest.json"
    existing = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
    existing_sources = {x.get("source") for x in existing if x.get("source")}

    items = []
    new_count = 0
    updated_count = 0
    for r in rows:
        sl = slug(r["source"])
        out = ROOT / CONTEST_DIR / "problems" / sl
        existed = (out / "index.html").exists()
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(render(r), encoding="utf-8")
        a, v = ANS[int(r["problem_no"])]
        if r["source"] in existing_sources:
            updated_count += 1
        else:
            new_count += 1
        items.append(
            {
                "contest": r["contest"],
                "year": r["year"],
                "form": r["form"],
                "problem_no": r["problem_no"],
                "source": r["source"],
                "slug": sl,
                "output_path": str(out / "index.html"),
                "relative_url": f"problems/{sl}/",
                "aops_url": aops(r),
                "aops_answer_key_url": ANSWER_KEY_URL,
                "aops_verified": True,
                "answer": f"{a}. {v}",
                "has_answer": True,
                "has_choices": True,
                "has_solution": True,
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in set(),
                "batch_number": BATCH_NUMBER,
            }
        )

    update_index("amc10")
    update_index("amc12")
    validate(items)

    by = {x.get("source"): x for x in existing if x.get("source")}
    for it in items:
        by[it["source"]] = it
    merged = sorted(by.values(), key=lambda x: (str(x.get("contest")), str(x.get("year")), str(x.get("form")), int(x.get("problem_no", 0))))
    manifest_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

    end = datetime.now().astimezone().isoformat(timespec="seconds")
    progress_path = ROOT / "problem_pages_progress.md"
    old = progress_path.read_text(encoding="utf-8").rstrip() + "\n\n" if progress_path.exists() else f"# Problem Pages Progress\n\n- Overall start time: {start}\n\n"
    skipped_text = "; ".join(SKIPPED)
    progress_path.write_text(
        old
        + f"## Batch {BATCH_NUMBER}: {BATCH_LABEL}\n\n"
        + f"- Start time: {start}\n"
        + f"- End time: {end}\n"
        + "- Processed contest: AMC 10\n"
        + f"- Processed range: {BATCH_LABEL}\n"
        + f"- Generated count: {new_count}\n"
        + f"- Updated existing count: {updated_count}\n"
        + f"- Skipped count: {len(SKIPPED)}\n"
        + (f"- Skipped reasons: {skipped_text}\n" if SKIPPED else "- Skipped reasons: none\n")
        + "- Validation result: passed\n"
        + "- Commit hash: pending\n"
        + "- Pushed: pending\n"
        + f"- Next batch should start from: {NEXT_START}\n"
        + "- Review notes: Skipped Problems 23 and 24 because they require diagrams or have truncated OCR.\n",
        encoding="utf-8",
    )

    report_path = ROOT / "problem_pages_report.md"
    latest = "\n".join(f"- `{it['source']}` -> `amc10/problems/{it['slug']}/`" for it in items)
    report_path.write_text(
        "# Problem Pages Report\n\n"
        + f"- Total manifest entries: {len(merged)}\n"
        + f"- Latest batch: {BATCH_NUMBER} ({BATCH_LABEL})\n"
        + f"- Latest new generated count: {new_count}\n"
        + f"- Latest updated existing count: {updated_count}\n"
        + f"- Latest skipped count: {len(SKIPPED)}\n"
        + "- MathJax validation: passed\n"
        + "- Answer verification source: AoPS 2006 AMC 10B Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批跳过 2006 AMC 10B Problems 23, 24：题面依赖图形或 OCR 截断。\n"
        + "2006 AMC 10B 已完成可可靠生成部分。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
