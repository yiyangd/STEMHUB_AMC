from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 30
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2006_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11, 12, 13, 14, 16, 17, 18, 20}
SKIPPED = [
    "2006 AMC 10B Problem 15 skipped: statement depends on a diagram for the rhombus configuration.",
    "2006 AMC 10B Problem 19 skipped: statement and shaded region depend on a diagram.",
]
BATCH_LABEL = "2006 AMC 10B Problems 11-14, 16-18, 20"
NEXT_START = "2006 AMC 10B Problem 21"

ANS = {
    11: ("C", "4"),
    12: ("E", r"\frac{9}{4}"),
    13: ("E", r"\frac{7}{6}"),
    14: ("D", r"\frac{9}{2}"),
    16: ("E", "Saturday"),
    17: ("D", r"\frac{1}{3}"),
    18: ("C", "3"),
    20: ("E", "40,400"),
}


OV = {
    11: (
        r"What is the tens digit in the sum $7!+8!+9!+\cdots+2006!$?",
        [("A", "$1$"), ("B", "$3$"), ("C", "$4$"), ("D", "$6$"), ("E", "$9$")],
    ),
    12: (
        r"The lines $x=\frac14y+a$ and $y=\frac14x+b$ intersect at the point $(1,2)$. What is $a+b$?",
        [("A", "$0$"), ("B", r"$\frac34$"), ("C", "$1$"), ("D", "$2$"), ("E", r"$\frac94$")],
    ),
    13: (
        r"Joe and JoAnn each bought $12$ ounces of coffee in a $16$-ounce cup. Joe drank $2$ ounces of his coffee and then added $2$ ounces of cream. JoAnn added $2$ ounces of cream, stirred the coffee well, and then drank $2$ ounces. What is the resulting ratio of the amount of cream in Joe's coffee to that in JoAnn's coffee?",
        [("A", r"$\frac67$"), ("B", r"$\frac{13}{14}$"), ("C", "$1$"), ("D", r"$\frac{14}{13}$"), ("E", r"$\frac76$")],
    ),
    14: (
        r"Let $a$ and $b$ be the roots of the equation $x^2-mx+2=0$. Suppose that $a+\frac1b$ and $b+\frac1a$ are the roots of the equation $x^2-px+q=0$. What is $q$?",
        [("A", r"$\frac52$"), ("B", r"$\frac72$"), ("C", "$4$"), ("D", r"$\frac92$"), ("E", "$8$")],
    ),
    16: (
        r"Leap Day, February $29$, $2004$, occurred on a Sunday. On what day of the week will Leap Day, February $29$, $2020$, occur?",
        [("A", "Tuesday"), ("B", "Wednesday"), ("C", "Thursday"), ("D", "Friday"), ("E", "Saturday")],
    ),
    17: (
        r"Bob and Alice each have a bag that contains one ball of each of the colors blue, green, orange, red, and violet. Alice randomly selects one ball from her bag and puts it into Bob's bag. Bob then randomly selects one ball from his bag and puts it into Alice's bag. What is the probability that after this process, the contents of the two bags are the same?",
        [("A", r"$\frac{1}{10}$"), ("B", r"$\frac16$"), ("C", r"$\frac15$"), ("D", r"$\frac13$"), ("E", r"$\frac12$")],
    ),
    18: (
        r"Let $a_1,a_2,\ldots$ be a sequence for which $a_1=2$, $a_2=3$, and $a_n=\frac{a_{n-1}}{a_{n-2}}$ for each positive integer $n\ge3$. What is $a_{2006}$?",
        [("A", "$1$"), ("B", "$2$"), ("C", "$3$"), ("D", r"$\frac23$"), ("E", r"$\frac32$")],
    ),
    20: (
        r"In rectangle $ABCD$, we have $A=(6,-22)$, $B=(2006,178)$, and $D=(8,y)$ for some integer $y$. What is the area of rectangle $ABCD$?",
        [("A", "$4000$"), ("B", "$4040$"), ("C", "$4400$"), ("D", "$40,000$"), ("E", "$40,400$")],
    ),
}


KEY_OVERRIDES = {
    11: "For large factorials, use place-value divisibility and only keep terms that can affect the tens digit.",
    12: "Substitute the intersection point into both line equations to solve for the constants.",
    13: "Track the actual amount of cream left after a mixed portion is removed.",
    14: "Use Vieta's formulas and multiply the transformed roots directly.",
    16: "Count weekday shifts between leap days using days modulo 7.",
    17: "Condition on Alice's transferred color and ask what Bob must return to restore both bags.",
    18: "Look for the repeating cycle in the recursively defined sequence.",
    20: "Use perpendicular side vectors of a rectangle and the dot product to find the missing coordinate and area.",
}


SOL = {
    11: [
        ("Decide which factorials matter", r"We only need the tens digit, so any term that is a multiple of $100$ cannot change it. Since $10!$ and every larger factorial contain the factors $2^2\cdot5^2=100$, all terms from $10!$ onward end in at least two zeros."),
        ("Reduce the sum", r"That means the tens digit of $7!+8!+9!+\cdots+2006!$ is the same as the tens digit of $7!+8!+9!$."),
        ("Compute the smaller factorials", r"We have $7!=5040$, $8!=40320$, and $9!=362880$. Adding gives \
\[5040+40320+362880=408240.\]"),
        ("Read the requested digit", r"The tens digit of $408240$ is $4$. The large later factorials do not change that digit because they all contribute $00$ in the last two places."),
        ("Answer", r"Therefore the answer is $\boxed{4}$."),
    ],
    12: [
        ("Use the meaning of intersection", r"If the two lines intersect at $(1,2)$, then $x=1$ and $y=2$ must satisfy both equations. This is more direct than trying to solve the two lines symbolically."),
        ("Find $a$", r"Substitute $(x,y)=(1,2)$ into $x=\frac14y+a$: \
\[1=\frac14\cdot2+a=\frac12+a.\] Thus $a=\frac12$."),
        ("Find $b$", r"Substitute the same point into $y=\frac14x+b$: \
\[2=\frac14\cdot1+b.\] Therefore $b=2-\frac14=\frac74$."),
        ("Add the constants", r"Now \
\[a+b=\frac12+\frac74=\frac24+\frac74=\frac94.\]"),
        ("Answer", r"The answer is $\boxed{\frac94}$."),
    ],
    13: [
        ("Track Joe's cream", r"Joe first drinks $2$ ounces of pure coffee, so no cream is removed. Then he adds $2$ ounces of cream. Joe therefore has $2$ ounces of cream in his cup."),
        ("Track JoAnn's mixture", r"JoAnn adds $2$ ounces of cream to $12$ ounces of coffee, making $14$ ounces total. Since the mixture is stirred well, the cream is evenly distributed."),
        ("Find how much cream JoAnn drinks", r"The fraction of JoAnn's mixture that is cream is $\frac{2}{14}=\frac17$. When she drinks $2$ ounces, she removes $2\cdot\frac17=\frac27$ ounces of cream."),
        ("Find JoAnn's remaining cream", r"JoAnn started with $2$ ounces of cream and drank $\frac27$ ounces of it, so she has $2-\frac27=\frac{12}{7}$ ounces of cream left."),
        ("Form the ratio", r"The requested ratio is Joe's cream to JoAnn's cream: \
\[\frac{2}{12/7}=2\cdot\frac7{12}=\frac76.\]"),
        ("Answer", r"Therefore the answer is $\boxed{\frac76}$."),
    ],
    14: [
        ("Record what Vieta gives", r"Since $a$ and $b$ are roots of $x^2-mx+2=0$, Vieta's formulas tell us that $ab=2$. We do not actually need the value of $m$."),
        ("Understand what $q$ represents", r"For the equation $x^2-px+q=0$, the constant term $q$ is the product of its two roots. So \
\[q=\left(a+\frac1b\right)\left(b+\frac1a\right).\]"),
        ("Multiply carefully", r"Expanding gives \
\[ab+1+1+\frac1{ab}.\] The two middle terms are $a\cdot\frac1a=1$ and $\frac1b\cdot b=1$."),
        ("Substitute $ab=2$", r"Thus \
\[q=2+1+1+\frac12=\frac92.\]"),
        ("Answer", r"The answer is $\boxed{\frac92}$."),
    ],
    16: [
        ("Think in four-year jumps", r"We are comparing Leap Day to Leap Day, so it is natural to move in four-year intervals: $2004$ to $2008$, then to $2012$, $2016$, and $2020$."),
        ("Find the weekday shift for one interval", r"From February $29$ of one leap year to February $29$ of the next leap year is $4\cdot365+1=1461$ days. Since $1461\equiv5\pmod7$, each four-year leap-day jump moves the weekday forward $5$ days."),
        ("Count the intervals", r"There are four such jumps from $2004$ to $2020$. The total shift is $4\cdot5=20$ days, and $20\equiv6\pmod7$."),
        ("Apply the shift", r"Starting from Sunday, moving forward $6$ days gives Saturday."),
        ("Answer", r"Leap Day in $2020$ occurred on $\boxed{\text{Saturday}}$."),
    ],
    17: [
        ("Condition on Alice's first move", r"Suppose Alice transfers a blue ball. The same reasoning applies no matter which color she transfers, so we can focus on this one case."),
        ("Describe the bags after Alice's move", r"Alice is missing blue and still has one of each of the other four colors. Bob now has two blue balls and one of each of the other four colors, for $6$ balls total."),
        ("Identify what Bob must return", r"For the bags to end with the same contents as before, Alice must get a blue ball back. If Bob returns any other color, Alice will still be missing blue and will have two of another color."),
        ("Compute the probability", r"Bob has $2$ blue balls among his $6$ balls, so the probability that he returns blue is $\frac26=\frac13$."),
        ("Answer", r"Therefore the answer is $\boxed{\frac13}$."),
    ],
    18: [
        ("Compute early terms", r"For recursive sequence problems, a good first move is to list terms until a pattern appears. We are given $a_1=2$ and $a_2=3$."),
        ("Use the recurrence", r"Now \
\[a_3=\frac{a_2}{a_1}=\frac32,\quad a_4=\frac{a_3}{a_2}=\frac12,\quad a_5=\frac{a_4}{a_3}=\frac13,\quad a_6=\frac{a_5}{a_4}=\frac23.\]"),
        ("Notice the cycle", r"Continuing one more term gives $a_7=\frac{a_6}{a_5}=2$, which is the same as $a_1$. Then $a_8=3$, matching $a_2$. So the sequence repeats every $6$ terms."),
        ("Use the index modulo 6", r"Since $2006=6\cdot334+2$, the $2006$th term is in the same position of the cycle as $a_2$."),
        ("Answer", r"Thus $a_{2006}=a_2=\boxed{3}$."),
    ],
    20: [
        ("Use rectangle geometry", r"In rectangle $ABCD$, the sides $AB$ and $AD$ meet at a right angle. So the vectors $\overrightarrow{AB}$ and $\overrightarrow{AD}$ must be perpendicular."),
        ("Write the two vectors", r"From $A=(6,-22)$ to $B=(2006,178)$, \
\[\overrightarrow{AB}=(2000,200).\] From $A=(6,-22)$ to $D=(8,y)$, \
\[\overrightarrow{AD}=(2,y+22).\]"),
        ("Use the dot product", r"Perpendicular vectors have dot product $0$, so \
\[(2000)(2)+200(y+22)=0.\] This gives $4000+200y+4400=0$, hence $200y=-8400$ and $y=-42$."),
        ("Find side lengths", r"Now $AD=(2,-20)$, so $AD=\sqrt{2^2+(-20)^2}=\sqrt{404}$. Also $AB=\sqrt{2000^2+200^2}=\sqrt{4,040,000}=100\sqrt{404}$."),
        ("Compute area", r"The area of the rectangle is \
\[(\sqrt{404})(100\sqrt{404})=100\cdot404=40,400.\]"),
        ("Answer", r"The answer is $\boxed{40,400}$."),
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
        + "- Review notes: Skipped Problems 15 and 19 because they require diagrams.\n",
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
        + "本批跳过 2006 AMC 10B Problems 15, 19：题面依赖图形。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
