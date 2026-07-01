from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 41
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2008_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
SKIPPED = []
BATCH_LABEL = "2008 AMC 10B Problems 1-10"
NEXT_START = "2008 AMC 10B Problem 11"

ANS = {
    1: ("E", "6"),
    2: ("B", "4"),
    3: ("D", "x^{1/2}"),
    4: ("C", "400000"),
    5: ("A", "0"),
    6: ("C", r"\frac{1}{10}"),
    7: ("C", "100"),
    8: ("C", "9"),
    9: ("A", "1"),
    10: ("A", r"\sqrt{10}"),
}


OV = {
    1: (r"A basketball player made $5$ baskets during a game. Each basket was worth either $2$ or $3$ points. How many different numbers could represent the total points scored by the player?", [("A", "$2$"), ("B", "$3$"), ("C", "$4$"), ("D", "$5$"), ("E", "$6$")]),
    2: (r"A $4\times4$ block of calendar dates is shown: $\begin{matrix}1&2&3&4\\8&9&10&11\\15&16&17&18\\22&23&24&25\end{matrix}$. The order of the numbers in the second row is to be reversed. Then the order of the numbers in the fourth row is to be reversed. Finally, the numbers on each diagonal are to be added. What will be the positive difference between the two diagonal sums?", [("A", "$2$"), ("B", "$4$"), ("C", "$6$"), ("D", "$8$"), ("E", "$10$")]),
    3: (r"Assume that $x$ is a positive real number. Which is equivalent to $\sqrt[3]{x\sqrt{x}}$?", [("A", r"$x^{1/6}$"), ("B", r"$x^{1/4}$"), ("C", r"$x^{3/8}$"), ("D", r"$x^{1/2}$"), ("E", "$x$")]),
    4: (r"A semipro baseball league has teams with $21$ players each. League rules state that a player must be paid at least $\$15{,}000$, and that the total of all players' salaries for each team cannot exceed $\$700{,}000$. What is the maximum possible salary, in dollars, for a single player?", [("A", "$270{,}000$"), ("B", "$385{,}000$"), ("C", "$400{,}000$"), ("D", "$430{,}000$"), ("E", "$700{,}000$")]),
    5: (r"For real numbers $a$ and $b$, define $a\$b=(a-b)^2$. What is $(x-y)^2\$(y-x)^2$?", [("A", "$0$"), ("B", "$x^2+y^2$"), ("C", "$2x^2$"), ("D", "$2y^2$"), ("E", "$4xy$")]),
    6: (r"Points $B$ and $C$ lie on $\overline{AD}$. The length of $AB$ is $4$ times the length of $BD$, and the length of $AC$ is $9$ times the length of $CD$. The length of $BC$ is what fraction of the length of $AD$?", [("A", r"$\frac{1}{36}$"), ("B", r"$\frac{1}{13}$"), ("C", r"$\frac{1}{10}$"), ("D", r"$\frac{5}{36}$"), ("E", r"$\frac{1}{5}$")]),
    7: (r"An equilateral triangle of side length $10$ is completely filled in by non-overlapping equilateral triangles of side length $1$. How many small triangles are required?", [("A", "$10$"), ("B", "$25$"), ("C", "$100$"), ("D", "$250$"), ("E", "$1000$")]),
    8: (r"A class collects $\$50$ to buy flowers for a classmate who is in the hospital. Roses cost $\$3$ each, and carnations cost $\$2$ each. No other flowers are to be used. How many different bouquets could be purchased for exactly $\$50$?", [("A", "$1$"), ("B", "$7$"), ("C", "$9$"), ("D", "$16$"), ("E", "$17$")]),
    9: (r"A quadratic equation $ax^2-2ax+b=0$ has two real solutions. What is the average of the solutions?", [("A", "$1$"), ("B", "$2$"), ("C", r"$\frac{b}{a}$"), ("D", r"$\frac{2b}{a}$"), ("E", r"$\frac{2b-a}{a}$")]),
    10: (r"Points $A$ and $B$ are on a circle of radius $5$ and $AB=6$. Point $C$ is the midpoint of the minor arc $AB$. What is the length of the line segment $AC$?", [("A", r"$\sqrt{10}$"), ("B", r"$\sqrt{7}$"), ("C", r"$\sqrt{14}$"), ("D", r"$\sqrt{15}$"), ("E", r"$4\sqrt{2}$")]),
}


KEY_OVERRIDES = {
    1: "Count possible totals by tracking how many 3-point baskets were made.",
    2: "Update only the diagonal entries after reversing the two rows.",
    3: "Convert radicals to fractional exponents and simplify.",
    4: "Maximize one salary by minimizing the other 20 salaries.",
    5: "Notice that $(x-y)^2$ and $(y-x)^2$ are equal before applying the operation.",
    6: "Normalize the whole segment length and locate B and C as fractions of AD.",
    7: "Use area scaling for similar equilateral triangles.",
    8: "Count nonnegative integer solutions to a two-variable cost equation.",
    9: "Use Vieta's formula for the sum of roots.",
    10: "Use chord length and half-angle geometry in the circle.",
}


SOL = {
    1: [("Identify the flexible choice", r"The player made exactly $5$ baskets. The only thing that can change is how many of those baskets were worth $3$ points instead of $2$ points."), ("Start from the lowest possible total", r"If all $5$ baskets were worth $2$ points, the total would be $5\cdot2=10$ points."), ("See how each 3-point basket changes the total", r"Changing one basket from $2$ points to $3$ points adds exactly $1$ point. If the player made $k$ three-point baskets, where $k=0,1,2,3,4,5$, the total is $10+k$."), ("Count the possible values", r"The six possible totals are $10,11,12,13,14,15$."), ("Answer", r"There are $\boxed{6}$ different possible totals.")],
    2: [("Write the rows after the reversals", r"The first and third rows stay the same. The second row becomes $11,10,9,8$, and the fourth row becomes $25,24,23,22$."), ("Find one diagonal sum", r"The diagonal from upper left to lower right is $1+10+17+22=50$."), ("Find the other diagonal sum", r"The diagonal from upper right to lower left is $4+9+16+25=54$."), ("Take the positive difference", r"The problem asks for the positive difference, so we compute $54-50=4$."), ("Answer", r"The difference is $\boxed{4}.")],
    3: [("Convert the square root first", r"Because $x$ is positive, we can safely use exponent rules. The expression inside the cube root is $x\sqrt{x}=x\cdot x^{1/2}$."), ("Combine the exponents inside", r"Multiplying powers with the same base means adding exponents, so $x\cdot x^{1/2}=x^{3/2}$."), ("Apply the cube root", r"Taking a cube root is the same as raising to the power $\frac13$. Thus $\sqrt[3]{x^{3/2}}=(x^{3/2})^{1/3}$."), ("Simplify the exponent", r"When a power is raised to a power, multiply exponents: $\frac32\cdot\frac13=\frac12$."), ("Answer", r"The expression is $\boxed{x^{1/2}}$.")],
    4: [("Understand how to maximize one player", r"To make one player's salary as large as possible, the other $20$ players should be paid as little as the rules allow."), ("Compute the minimum total for the other players", r"Each of the other $20$ players must receive at least $\$15{,}000$, so together they must receive at least $20\cdot15{,}000=300{,}000$ dollars."), ("Use the team salary cap", r"The team total cannot exceed $\$700{,}000$. After reserving $\$300{,}000$ for the other players, the most left for one player is $700{,}000-300{,}000=400{,}000$."), ("Check that this is possible", r"This salary is allowed because the other $20$ players can each be paid exactly $\$15{,}000$, making the total exactly $\$700{,}000$."), ("Answer", r"The maximum possible salary is $\boxed{400{,}000}$ dollars.")],
    5: [("Compare the two inputs to the operation", r"The expression uses $(x-y)^2$ and $(y-x)^2$. Since $y-x=-(x-y)$, their squares are equal."), ("Name the common value", r"Let $u=(x-y)^2$. Then $(y-x)^2$ is also $u$."), ("Apply the definition carefully", r"The operation is $a\$b=(a-b)^2$. Therefore $(x-y)^2\$(y-x)^2=u\$u=(u-u)^2$."), ("Finish", r"Since $u-u=0$, the result is $0^2=0$."), ("Answer", r"The value is $\boxed{0}$.")],
    6: [("Normalize the segment", r"Fractions are easier if we let $AD=1$. Then all positions can be measured as distances from $A$."), ("Locate B", r"We know $AB=4BD$ and $AB+BD=AD=1$. So $4BD+BD=1$, giving $BD=\frac15$ and $AB=\frac45$."), ("Locate C", r"Similarly, $AC=9CD$ and $AC+CD=1$. Thus $9CD+CD=1$, so $CD=\frac1{10}$ and $AC=\frac9{10}$."), ("Find BC", r"Both $B$ and $C$ are measured from $A$, so $BC=AC-AB=\frac9{10}-\frac45=\frac9{10}-\frac8{10}=\frac1{10}$."), ("Answer", r"The length of $BC$ is $\boxed{\frac1{10}}$ of $AD$.")],
    7: [("Use similarity instead of drawing every triangle", r"All the small triangles are equilateral and have side length $1$, while the large triangle has side length $10$. The triangles are similar."), ("Convert side scale to area scale", r"Area scales by the square of the side-length scale. Since the side-length ratio is $10:1$, the area ratio is $10^2:1^2=100:1$."), ("Interpret the area ratio", r"Because the large triangle is completely filled without overlap, the number of small triangles equals the ratio of the large area to one small area."), ("Answer", r"The required number of small triangles is $\boxed{100}$.")],
    8: [("Set up the cost equation", r"Let $r$ be the number of roses and $c$ be the number of carnations. The total cost condition is $3r+2c=50$."), ("Think about possible rose counts", r"Both $r$ and $c$ must be nonnegative integers. Also, $50-3r$ must be even because it equals $2c$."), ("Use parity", r"Since $50$ is even and $3r$ has the same parity as $r$, the number $r$ must be even."), ("List the valid rose counts", r"The largest possible $r$ is $16$, since $3\cdot17>50$. The even values from $0$ to $16$ are $0,2,4,6,8,10,12,14,16$, giving $9$ choices."), ("Answer", r"There are $\boxed{9}$ different bouquets.")],
    9: [("Recall what the average of roots needs", r"If the two solutions are $r_1$ and $r_2$, their average is $\frac{r_1+r_2}{2}$. So we only need the sum of the roots."), ("Use Vieta's formula", r"For $Ax^2+Bx+C=0$, the sum of the roots is $-\frac{B}{A}$. Here $A=a$ and $B=-2a$."), ("Compute the sum", r"The sum of the two solutions is $-\frac{-2a}{a}=2$, assuming $a\ne0$ as required for a quadratic equation."), ("Find the average", r"The average is $\frac{2}{2}=1$."), ("Answer", r"The average of the solutions is $\boxed{1}$.")],
    10: [("Relate the chord to a central angle", r"Let $O$ be the center of the circle. Since $AB=6$ in a circle of radius $5$, half the chord has length $3$. If $\angle AOC=\theta$, then the midpoint $C$ of the minor arc means $\angle AOB=2\theta$."), ("Use the right triangle from the chord", r"Dropping a perpendicular from $O$ to chord $AB$ gives a right triangle with hypotenuse $5$ and half-chord $3$. Thus $\sin\theta=\frac35$ and $\cos\theta=\frac45$."), ("Find the chord AC", r"The segment $AC$ is a chord subtending central angle $\theta$, so $AC=2\cdot5\sin(\theta/2)$."), ("Use the half-angle formula", r"Since $\cos\theta=\frac45$, we get $\sin(\theta/2)=\sqrt{\frac{1-\cos\theta}{2}}=\sqrt{\frac{1/5}{2}}=\frac1{\sqrt{10}}$."), ("Finish", r"Therefore $AC=10\cdot\frac1{\sqrt{10}}=\sqrt{10}$."), ("Answer", r"The length of $AC$ is $\boxed{\sqrt{10}}$.")],
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
        if r["year"] == "2008" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Review notes: none.\n",
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
        + "- Answer verification source: AoPS 2008 AMC 10B Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批无跳过题。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()



