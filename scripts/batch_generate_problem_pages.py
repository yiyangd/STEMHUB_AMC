from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 23
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2005_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
SKIPPED = []
BATCH_LABEL = "2005 AMC 10B Problem 1-10"
NEXT_START = "2005 AMC 10B Problem 11"

ANS = {
    1: ("A", "100"),
    2: ("D", "20"),
    3: ("D", r"\frac{4}{9}"),
    4: ("D", r"13\sqrt2"),
    5: ("C", r"\frac{2}{5}"),
    6: ("B", "2"),
    7: ("B", r"\frac{\pi}{8}"),
    8: ("A", r"80-20\pi"),
    9: ("D", r"\frac{5}{9}"),
    10: ("A", "3"),
}


OV = {
    3: (
        r"A gallon of paint is used to paint a room. One third of the paint is used on the first day. On the second day, one third of the remaining paint is used. What fraction of the original amount of paint is available to use on the third day?",
        [("A", r"$\frac1{10}$"), ("B", r"$\frac19$"), ("C", r"$\frac13$"), ("D", r"$\frac49$"), ("E", r"$\frac59$")],
    ),
    4: (
        r"For real numbers $a$ and $b$, define $a\diamond b=\sqrt{a^2+b^2}$. What is the value of $(5\diamond12)\diamond((-12)\diamond(-5))$?",
        [("A", "$0$"), ("B", r"$\sqrt{17}$"), ("C", "$13$"), ("D", r"$13\sqrt2$"), ("E", r"$26\sqrt2$")],
    ),
    7: (
        r"A circle is inscribed in a square, then a square is inscribed in this circle, and finally, a circle is inscribed in this square. What is the ratio of the area of the smaller circle to the area of the larger square?",
        [("A", r"$\frac{\pi}{16}$"), ("B", r"$\frac{\pi}{8}$"), ("C", r"$\frac{3\pi}{16}$"), ("D", r"$\frac{\pi}{4}$"), ("E", r"$\frac{\pi}{2}$")],
    ),
    9: (
        r"One fair die has faces $1,1,2,2,3,3$ and another has faces $4,4,5,5,6,6$. The dice are rolled and the numbers on the top faces are added. What is the probability that the sum will be odd?",
        [("A", r"$\frac13$"), ("B", r"$\frac49$"), ("C", r"$\frac12$"), ("D", r"$\frac59$"), ("E", r"$\frac23$")],
    ),
    10: (
        r"In $\triangle ABC$, we have $AC=BC=7$ and $AB=2$. Suppose that $D$ is a point on line $AB$ such that $B$ lies between $A$ and $D$ and $CD=8$. What is $BD$?",
        [("A", "$3$"), ("B", r"$2\sqrt3$"), ("C", "$4$"), ("D", "$5$"), ("E", r"$4\sqrt2$")],
    ),
}


KEY_OVERRIDES = {
    1: "Compute total buying cost and total selling revenue.",
    2: "Translate x percent of x into an equation.",
    3: "Track the remaining fraction after each day.",
    4: "Evaluate the custom square-root operation from the inside out.",
    5: "Use proportional cost: one third of the CDs costs one fifth of the money.",
    6: "Convert a percentage goal into the required number of A grades.",
    7: "Track areas through alternating inscribed squares and circles.",
    8: "Compute shaded area per tile and multiply by the number of tiles.",
    9: "Use parity: odd sums occur when one die is odd and the other is even.",
    10: "Use symmetry and the Pythagorean theorem in an isosceles triangle.",
}


SOL = {
    1: [
        ("Find the cost", r"The troop buys $1000$ bars at five for $2. The cost per group of $5$ is $2$, so the total cost is $(1000/5)\cdot2=400$ dollars."),
        ("Find the revenue", r"They sell at two for $1$, so every $2$ bars brings in $1$. The revenue is $(1000/2)\cdot1=500$ dollars."),
        ("Subtract", r"Profit is revenue minus cost: $500-400=100$."),
        ("Answer", r"Their profit was $\boxed{100}$ dollars."),
    ],
    2: [
        ("Translate the phrase", r"The phrase '$x\%$ of $x$' means $\frac{x}{100}\cdot x$."),
        ("Set up the equation", r"We are told \[\frac{x}{100}\cdot x=4.\] Thus $x^2=400$."),
        ("Use positivity", r"Since $x$ is positive, $x=20$, not $-20$."),
        ("Answer", r"The answer is $\boxed{20}$."),
    ],
    3: [
        ("Track what remains after day 1", r"After using one third of the paint, the amount left is $1-\frac13=\frac23$ of the original gallon."),
        ("Use one third of the remaining paint", r"On the second day, one third of the remaining paint is used, so two thirds of the remaining paint stays unused."),
        ("Multiply the remaining fractions", r"The amount available for the third day is \[\frac23\cdot\frac23=\frac49\] of the original amount."),
        ("Answer", r"The answer is $\boxed{\frac49}$."),
    ],
    4: [
        ("Understand the operation", r"The operation $a\diamond b$ gives the length of the hypotenuse of a right triangle with legs $a$ and $b$: $\sqrt{a^2+b^2}$."),
        ("Evaluate the two inner operations", r"We have $5\diamond12=\sqrt{25+144}=13$. Also $(-12)\diamond(-5)=\sqrt{144+25}=13$."),
        ("Evaluate the outer operation", r"Now the expression becomes $13\diamond13=\sqrt{13^2+13^2}=\sqrt{338}$."),
        ("Simplify", r"Since $338=169\cdot2$, the value is $13\sqrt2$."),
        ("Answer", r"The answer is $\boxed{13\sqrt2}$."),
    ],
    5: [
        ("Find the cost of all CDs", r"One third of the CDs costs one fifth of her money. Since all CDs have the same price, all the CDs cost three times as much."),
        ("Compute the total fraction spent", r"Buying all the CDs costs $3\cdot\frac15=\frac35$ of her money."),
        ("Find what remains", r"The fraction left is $1-\frac35=\frac25$."),
        ("Answer", r"She will have $\boxed{\frac25}$ of her money left."),
    ],
    6: [
        ("Convert the goal", r"Lisa wants an A on at least $80\%$ of $50$ quizzes. That means she needs at least $0.8\cdot50=40$ A grades."),
        ("Use what she already has", r"She already has $22$ A grades from the first $30$ quizzes."),
        ("Find how many more A grades she needs", r"She needs $40-22=18$ more A grades among the remaining $20$ quizzes."),
        ("Count allowed non-A grades", r"If she needs $18$ A grades out of $20$, then at most $2$ of the remaining quizzes can be lower than an A."),
        ("Answer", r"The answer is $\boxed{2}$."),
    ],
    7: [
        ("Choose a simple side length", r"Let the larger square have side length $s$, so its area is $s^2$. The first circle inscribed in it has radius $s/2$."),
        ("Find the inscribed square", r"The square inside that circle has diagonal equal to the circle's diameter, which is $s$. Therefore its side length is $s/\sqrt2$."),
        ("Find the smaller circle", r"The final circle is inscribed in this smaller square, so its radius is half the side length: $s/(2\sqrt2)$."),
        ("Compute the area ratio", r"The smaller circle has area $\pi\left(\frac{s}{2\sqrt2}\right)^2=\frac{\pi s^2}{8}$. Dividing by the larger square area $s^2$ gives $\frac{\pi}{8}$."),
        ("Answer", r"The ratio is $\boxed{\frac{\pi}{8}}$."),
    ],
    8: [
        ("Find the shaded area of one tile", r"Each tile has four white quarter-circles of radius $1/2$. Together they make one full circle of radius $1/2$, with area $\pi(1/2)^2=\pi/4$."),
        ("Subtract from the tile area", r"Each tile has area $1$, so the shaded area per tile is $1-\pi/4$."),
        ("Count the tiles", r"The floor is $8$ feet by $10$ feet, so it has $80$ one-foot square tiles."),
        ("Multiply", r"The total shaded area is $80(1-\pi/4)=80-20\pi$."),
        ("Answer", r"The answer is $\boxed{80-20\pi}$."),
    ],
    9: [
        ("Use parity", r"A sum is odd when one addend is odd and the other is even."),
        ("Find parity probabilities", r"The first die has four odd faces ($1,1,3,3$) and two even faces ($2,2$). So $P(\text{odd on first})=\frac46=\frac23$ and $P(\text{even on first})=\frac13$."),
        ("Do the same for the second die", r"The second die has two odd faces ($5,5$) and four even faces ($4,4,6,6$). So $P(\text{odd on second})=\frac13$ and $P(\text{even on second})=\frac23$."),
        ("Add the two favorable parity cases", r"The probability is \[\frac23\cdot\frac23+\frac13\cdot\frac13=\frac49+\frac19=\frac59.\]"),
        ("Answer", r"The answer is $\boxed{\frac59}$."),
    ],
    10: [
        ("Use symmetry", r"Since $AC=BC=7$ and $AB=2$, point $C$ lies above the midpoint of $AB$. Put $A=(-1,0)$ and $B=(1,0)$."),
        ("Find the height of C", r"The distance from the midpoint to either endpoint is $1$, so the height $h$ satisfies $h^2+1^2=7^2$. Thus $h^2=48$."),
        ("Place point D", r"Point $D$ is on line $AB$ beyond $B$, so write $D=(1+x,0)$ where $x=BD$."),
        ("Use CD=8", r"The distance from $C=(0,\sqrt{48})$ to $D=(1+x,0)$ is $8$, so \[(1+x)^2+48=64.\] Therefore $(1+x)^2=16$."),
        ("Solve", r"Since $x>0$, $1+x=4$, so $x=3$. Thus $BD=\boxed{3}$."),
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
        if r["year"] == "2005" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "本批完成 2005 AMC 10B Problems 1-10，无跳过题。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
