from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 12
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2003_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21, 22, 23, 24, 25}
SKIPPED = []
BATCH_LABEL = "2003 AMC 10B Problem 21-25"
NEXT_START = "2004 AMC 10A Problem 1"

ANS = {
    21: ("C", r"\frac{9}{32}"),
    22: ("B", "March 9"),
    23: ("D", r"\frac{1}{2}"),
    24: ("E", r"\frac{123}{40}"),
    25: ("B", "30"),
}


OV = {
    21: (
        r"A bag contains two red beads and two green beads. You reach into the bag and pull out a bead, replacing it with a red bead regardless of the color you pulled out. What is the probability that all beads in the bag are red after three such replacements?",
        [("A", r"$\frac18$"), ("B", r"$\frac{5}{32}$"), ("C", r"$\frac{9}{32}$"), ("D", r"$\frac38$"), ("E", r"$\frac{7}{16}$")],
    ),
    22: (
        r"A clock chimes once at $30$ minutes past each hour and chimes on the hour according to the hour. For example, at $1$ PM there is one chime and at noon and midnight there are twelve chimes. Starting at $11{:}15$ AM on February $26$, $2003$, on what date will the $2003$rd chime occur?",
        [("A", "March 8"), ("B", "March 9"), ("C", "March 10"), ("D", "March 20"), ("E", "March 21")],
    ),
    23: (
        r"A regular octagon $ABCDEFGH$ has area $1$ square unit. What is the area of rectangle $ABEF$?",
        [("A", r"$1-\frac{\sqrt2}{2}$"), ("B", r"$\frac{\sqrt2}{4}$"), ("C", r"$\frac{\sqrt2-1}{2}$"), ("D", r"$\frac12$"), ("E", r"$\frac{1+\sqrt2}{4}$")],
    ),
    24: (
        r"The first four terms in an arithmetic sequence are $x+y$, $x-y$, $xy$, and $\frac{x}{y}$, in that order. What is the fifth term?",
        [("A", r"$-\frac{15}{8}$"), ("B", r"$-\frac65$"), ("C", "$0$"), ("D", r"$\frac{27}{20}$"), ("E", r"$\frac{123}{40}$")],
    ),
    25: (
        r"How many distinct four-digit numbers are divisible by $3$ and have $23$ as their last two digits?",
        [("A", "$27$"), ("B", "$30$"), ("C", "$33$"), ("D", "$81$"), ("E", "$90$")],
    ),
}


KEY_OVERRIDES = {
    21: "Use complement counting on the two original green beads that must both be drawn at least once.",
    22: "Count chimes in repeated 12-hour or 24-hour blocks, then handle the leftover chimes carefully.",
    23: "Decompose a regular octagon into a central rectangle and congruent corner triangles.",
    24: "Use equal common differences to create equations for x and y, then find the next term.",
    25: "Use the divisibility-by-3 rule and count valid first two digits by residues modulo 3.",
}


SOL = {
    21: [
        ("Identify what must happen", r"A bead becomes red permanently if it is green when drawn, because it is replaced by a red bead. After three draws, all beads are red exactly when both original green beads have been drawn at least once."),
        ("Use the complement", r"It is easier to count the opposite event: at least one of the two original green beads is never drawn. Then subtract from $1$."),
        ("Compute the chance one specific green is missed", r"Pick one original green bead. On each draw, as long as we are asking whether this particular bead is avoided, there are $3$ acceptable beads out of $4$. So the probability it is missed for all three draws is $(3/4)^3=27/64$."),
        ("Correct for double-counting", r"If both original green beads are missed, then every draw must be one of the two original red beads or red replacements. The probability is $(1/2)^3=1/8=8/64$."),
        ("Apply inclusion-exclusion", r"The probability at least one green is missed is $2\cdot\frac{27}{64}-\frac{8}{64}=\frac{46}{64}$. Therefore the probability both greens are drawn is $1-\frac{46}{64}=\frac{18}{64}=\frac{9}{32}$. The answer is $\boxed{\frac{9}{32}}$."),
    ],
    22: [
        ("Look for a repeating block", r"The clock pattern repeats every $12$ hours. In a $12$-hour period, the hour chimes add to $1+2+\cdots+12=78$, and there are $12$ half-hour chimes."),
        ("Count chimes per half-day and per day", r"Thus each $12$-hour block has $78+12=90$ chimes. Each full day has $180$ chimes."),
        ("Remove full days", r"Starting at $11{:}15$ AM on February $26$, after $11$ full days the clock has chimed $11\cdot180=1980$ times. That brings us to $11{:}15$ AM on March $9$, with $2003-1980=23$ chimes left."),
        ("Count the remaining chimes", r"From $11{:}15$ AM, the next chimes are: $11{:}30$ gives $1$, noon gives $12$ more for a total of $13$, $12{:}30$ gives $14$, $1{:}00$ gives $15$, $1{:}30$ gives $16$, $2{:}00$ gives $18$, $2{:}30$ gives $19$, $3{:}00$ gives $22$, and $3{:}30$ gives $23$."),
        ("State the date", r"The $2003$rd chime occurs on March $9$, so the answer is $\boxed{\text{March 9}}$."),
    ],
    23: [
        ("Name the side length", r"Let the side length of the regular octagon be $s$. In the usual orientation, $AB$ and $EF$ are horizontal sides of length $s$, and rectangle $ABEF$ has width $s$."),
        ("Find the rectangle height", r"The slanted sides of the octagon are at $45^\circ$, so the vertical contribution of each slanted side is $s/\sqrt2$. The distance from $AB$ to $EF$ is $s+2\cdot s/\sqrt2=s(1+\sqrt2)$."),
        ("Write the rectangle area", r"Therefore \[[ABEF]=s\cdot s(1+\sqrt2)=s^2(1+\sqrt2).\]"),
        ("Relate this to the whole octagon", r"The regular octagon can be divided into this central rectangle plus two congruent strips of right isosceles triangles whose total area equals another $s^2(1+\sqrt2)$. Equivalently, the area of the octagon is $2s^2(1+\sqrt2)$."),
        ("Use the given octagon area", r"Since the octagon has area $1$, the rectangle has half that area: \[[ABEF]=\frac12.\] The answer is $\boxed{\frac12}$."),
    ],
    24: [
        ("Use equal differences", r"In an arithmetic sequence, consecutive differences are equal. The first difference is $(x-y)-(x+y)=-2y$."),
        ("Set up equations from the next differences", r"The second difference is $xy-(x-y)=xy-x+y$, so $xy-x+y=-2y$, or $xy-x+3y=0$. The third difference is $\frac{x}{y}-xy$, so $\frac{x}{y}-xy=-2y$."),
        ("Solve for x in terms of y", r"From $xy-x+3y=0$, we get $x(y-1)=-3y$, so $x=\frac{3y}{1-y}$."),
        ("Use the third difference", r"Multiplying $\frac{x}{y}-xy=-2y$ by $y$ gives $x-xy^2=-2y^2$. Substitute $x=\frac{3y}{1-y}$ and simplify; this gives $3(1+y)=-2y$, so $y=-\frac35$."),
        ("Find the fourth and fifth terms", r"Then $x=\frac{3y}{1-y}=-\frac98$, and $\frac{x}{y}=\frac{15}{8}$. The common difference is $-2y=\frac65$, so the fifth term is \[\frac{15}{8}+\frac65=\frac{75}{40}+\frac{48}{40}=\frac{123}{40}.\] The answer is $\boxed{\frac{123}{40}}$."),
    ],
    25: [
        ("Write the number by its digits", r"Every number has the form $ab23$, where $a$ is from $1$ to $9$ and $b$ is from $0$ to $9$."),
        ("Use the divisibility rule", r"A number is divisible by $3$ exactly when the sum of its digits is divisible by $3$. Here the digit sum is $a+b+2+3=a+b+5$."),
        ("Convert to a residue condition", r"We need $a+b+5\equiv0\pmod3$, so $a+b\equiv1\pmod3$."),
        ("Count residues for a and b", r"Among $1,2,\ldots,9$, the residues $0,1,2$ each occur $3$ times. Among $0,1,\ldots,9$, the residue counts are $4$ for residue $0$ and $3$ each for residues $1$ and $2$."),
        ("Add the valid cases", r"The pairs with $a+b\equiv1\pmod3$ are $(0,1),(1,0),(2,2)$ by residue. The count is $3\cdot3+3\cdot4+3\cdot3=9+12+9=30$. The answer is $\boxed{30}$."),
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {20, 23}) else notes
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
        if r["year"] == "2003" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {20, 23},
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
        + "- Review notes: Corrected 2003 AMC 10B Problem 10 answer choice from the AoPS answer key; Problem 20 uses the diagram data stated in text and should be visually reviewed later.\n",
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
        + "- Answer verification source: AoPS 2003 AMC 10B Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批完成 2003 AMC 10B Problems 21-25，至此 2003B 已完成，除 Problem 4 和 19 因图形/OCR 问题跳过。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
