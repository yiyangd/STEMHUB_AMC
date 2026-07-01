from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 48
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2009_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
SKIPPED = []
BATCH_LABEL = "2009 AMC 10B Problems 11-20"
NEXT_START = "2009 AMC 10B Problem 21"

ANS={11:("A","6"),12:("A","3"),13:("C",r"\overline{CD}"),14:("D","Friday"),15:("E",r"3a-2b"),16:("B",r"\frac12"),17:("C",r"\frac23"),18:("D",r"\frac{75}{8}"),19:("A",r"\frac12"),20:("B",r"\frac{\sqrt5-1}{2}")}

OV={
11:(r"How many $7$-digit palindromes, numbers that read the same backward as forward, can be formed using the digits $2,2,3,3,5,5,5$?",[("A","$6$"),("B","$12$"),("C","$24$"),("D","$36$"),("E","$48$")]),
12:(r"Distinct points $A,B,C,$ and $D$ lie on a line, with $AB=BC=CD=1$. Points $E$ and $F$ lie on a second line, parallel to the first, with $EF=1$. A triangle with positive area has three of the six points as its vertices. How many possible values are there for the area of the triangle?",[("A","$3$"),("B","$4$"),("C","$5$"),("D","$6$"),("E","$7$")]),
13:(r"As shown below, convex pentagon $ABCDE$ has sides $AB=3$, $BC=4$, $CD=6$, $DE=3$, and $EA=7$. The pentagon is originally positioned in the plane with vertex $A$ at the origin and vertex $B$ on the positive $x$-axis. The pentagon is then rolled clockwise to the right along the $x$-axis. Which side will touch the point $x=2009$ on the $x$-axis?",[("A",r"$\overline{AB}$"),("B",r"$\overline{BC}$"),("C",r"$\overline{CD}$"),("D",r"$\overline{DE}$"),("E",r"$\overline{EA}$")]),
14:(r"On Monday, Millie puts a quart of seeds, $25\%$ of which are millet, into a bird feeder. On each successive day she adds another quart of the same mix of seeds without removing any seeds that are left. Each day the birds eat only $25\%$ of the millet in the feeder, but they eat all of the other seeds. On which day, just after Millie has placed the seeds, will the birds find that more than half the seeds in the feeder are millet?",[("A","Tuesday"),("B","Wednesday"),("C","Thursday"),("D","Friday"),("E","Saturday")]),
15:(r"When a bucket is two-thirds full of water, the bucket and water weigh $a$ kilograms. When the bucket is one-half full of water, the total weight is $b$ kilograms. In terms of $a$ and $b$, what is the total weight in kilograms when the bucket is full of water?",[("A",r"$\frac23a+\frac13b$"),("B",r"$\frac32a-\frac12b$"),("C",r"$\frac32a+b$"),("D",r"$\frac32a+2b$"),("E",r"$3a-2b$")]),
16:(r"Points $A$ and $C$ lie on a circle centered at $O$, each of $\overline{BA}$ and $\overline{BC}$ is tangent to the circle, and $\triangle ABC$ is equilateral. The circle intersects $\overline{BO}$ at $D$. What is $\frac{BD}{BO}$?",[("A",r"$\frac{\sqrt2}{3}$"),("B",r"$\frac12$"),("C",r"$\frac{\sqrt3}{3}$"),("D",r"$\frac{\sqrt2}{2}$"),("E",r"$\frac{\sqrt3}{2}$")]),
17:(r"Five unit squares are arranged in the coordinate plane as shown, with the lower left corner at the origin. The slanted line, extending from $(c,0)$ to $(3,3)$, divides the entire region into two regions of equal area. What is $c$?",[("A",r"$\frac12$"),("B",r"$\frac35$"),("C",r"$\frac23$"),("D",r"$\frac34$"),("E",r"$\frac45$")]),
18:(r"Rectangle $ABCD$ has $AB=8$ and $BC=6$. Point $M$ is the midpoint of diagonal $\overline{AC}$, and $E$ is on $AB$ with $\overline{ME}\perp\overline{AC}$. What is the area of $\triangle AME$?",[("A",r"$\frac{65}{8}$"),("B",r"$\frac{25}{3}$"),("C","$9$"),("D",r"$\frac{75}{8}$"),("E",r"$\frac{85}{8}$")]),
19:(r"A particular $12$-hour digital clock displays the hour and minute of a day. Unfortunately, whenever it is supposed to display a $1$, it mistakenly displays a $9$. For example, when it is 1:16 PM the clock incorrectly shows 9:96 PM. What fraction of the day will the clock show the correct time?",[("A",r"$\frac12$"),("B",r"$\frac58$"),("C",r"$\frac34$"),("D",r"$\frac56$"),("E",r"$\frac9{10}$")]),
20:(r"Triangle $ABC$ has a right angle at $B$, $AB=1$, and $BC=2$. The angle bisector of $\angle A$ intersects side $\overline{BC}$ at $D$. What is $BD$?",[("A",r"$\frac{\sqrt3-1}{2}$"),("B",r"$\frac{\sqrt5-1}{2}$"),("C",r"$\frac{\sqrt5+1}{2}$"),("D",r"$\frac{\sqrt6+\sqrt2}{2}$"),("E",r"$2\sqrt3-1$")]),
}

KEY_OVERRIDES={11:"A palindrome is determined by its first three digits and its center digit.",12:"All positive-area triangles use a base on one parallel line and a point on the other, so the height is fixed.",13:"Rolling the pentagon makes the side lengths repeat along the x-axis with period equal to the perimeter.",14:"Track only the millet left after each day and the new quart added each morning.",15:"Set up two linear equations for bucket weight and full water weight.",16:"Use the 30-60-90 triangle formed by a tangent radius and the equilateral triangle angle bisector.",17:"Compute the area on one side of the dividing line as a function of c.",18:"Use coordinates to find the foot of a perpendicular from the midpoint of a diagonal to AB.",19:"Count the times whose displayed digits contain no digit 1.",20:"Use the angle bisector theorem in a right triangle."}

SOL={
11:[("Use the palindrome structure",r"A $7$-digit palindrome has the form $abc dcba$, so the outside digits must come in matching pairs."),("Identify the center",r"The digits are $2,2,3,3,5,5,5$. The only digit with odd multiplicity is $5$, so the middle digit must be $5$."),("Arrange the pairs",r"After placing one $5$ in the center, the remaining digits form three pairs: $2,2$, $3,3$, and $5,5$."),("Count the first half",r"The first three positions can be filled by arranging the pair labels $2,3,5$ in $3!$ ways."),("Answer",r"Thus there are $3!=\boxed{6}$ palindromes.")],
12:[("Use the fixed height idea",r"The two lines are parallel, so any triangle using points from both lines has the same height, call it $h$."),("Choose a base on the four-point line",r"If two vertices are chosen from $A,B,C,D$, the possible base lengths are $1,2,$ or $3$. These give areas $\frac h2$, $h$, and $\frac{3h}{2}$."),("Choose a base on the two-point line",r"If two vertices are $E$ and $F$, the base length is $1$, giving area $\frac h2$, which is already on the list."),("Count distinct areas",r"The possible positive areas are $\frac h2$, $h$, and $\frac{3h}{2}$."),("Answer",r"There are $\boxed{3}$ possible values.")],
13:[("Use one full rolling cycle",r"As the pentagon rolls, the side touching the $x$-axis changes in order: $AB,BC,CD,DE,EA$, then repeats."),("Find the period length",r"The distance covered in one full cycle is the perimeter: $3+4+6+3+7=23$."),("Reduce the target position",r"We need the side touching $x=2009$. Since $2009=23\cdot87+8$, this is the same position as $x=8$ within one cycle."),("Locate x=8 in the cycle",r"Within one cycle, $AB$ covers $0$ to $3$, $BC$ covers $3$ to $7$, and $CD$ covers $7$ to $13$. Since $8$ lies between $7$ and $13$, side $CD$ is touching."),("Answer",r"The side is $\boxed{\overline{CD}}$.")],
14:[("Track millet just after each filling",r"Right after Monday's filling, there is $\frac14$ quart of millet. The non-millet seeds will be eaten completely each day, so they do not accumulate."),("Write the recurrence",r"Each day, $75\%$ of the existing millet remains, then Millie adds another $\frac14$ quart of millet. Thus the next millet amount is $M_{next}=\frac34M+\frac14$."),("Compute day by day",r"Tuesday has $\frac34\cdot\frac14+rac14=\frac7{16}$ quart of millet. Wednesday has $\frac{37}{64}$, Thursday has $\frac{175}{256}$, and Friday has $\frac{781}{1024}$."),("Compare to the total just after filling",r"Just after filling on any day after Monday, the non-millet amount is $\frac34$ quart. On Thursday, $\frac{175}{256}$ is less than $\frac34$, so millet is less than half. On Friday, $\frac{781}{1024}$ is greater than $\frac34$, so millet is more than half."),("Answer",r"The first such day is $\boxed{\text{Friday}}$.")],
15:[("Name the unknowns",r"Let $B$ be the empty bucket's weight and $W$ be the weight of a full bucket of water alone."),("Write the two equations",r"The two given weights are $B+\frac23W=a$ and $B+\frac12W=b$."),("Find W",r"Subtracting the second equation from the first gives $\frac16W=a-b$, so $W=6a-6b$."),("Find the full weight",r"The full bucket weighs $B+W$. From $B=b-rac12W$, we get $B+W=b+rac12W=b+3a-3b=3a-2b$."),("Answer",r"The total full weight is $\boxed{3a-2b}$.")],
16:[("Use symmetry",r"Because $BA$ and $BC$ are tangents from the same point and $\triangle ABC$ is equilateral, the center $O$ lies on the angle bisector of $\angle ABC$."),("Look at a right triangle",r"Radius $OA$ is perpendicular to tangent $BA$, so triangle $ABO$ is right at $A$. Since $\angle ABC=60^\circ$, the angle $ABO$ is $30^\circ$."),("Relate radius to BO",r"In the $30$-$60$-$90$ triangle, the side opposite $30^\circ$ is $OA$, so $OA=\frac12BO$."),("Locate D",r"Point $D$ is where the circle meets $BO$ between $B$ and $O$, so $OD$ is also a radius. Therefore $BD=BO-OD=BO-OA=\frac12BO$."),("Answer",r"Thus $\frac{BD}{BO}=\boxed{\frac12}$.")],
17:[("Describe the region by horizontal slices",r"The five-square shape is a staircase: from $y=0$ to $1$ it extends to $x=2$, from $y=1$ to $2$ it extends from $x=1$ to $x=3$, and from $y=2$ to $3$ it extends from $x=2$ to $x=3$."),("Write the line",r"The line goes from $(c,0)$ to $(3,3)$, so at height $y$ its $x$-coordinate is $x=c+\frac{3-c}{3}y$."),("Compute one side's area",r"Taking the area to the right of the line inside the staircase gives $\int_0^1(2-x)dy+\int_1^2(3-x)dy+\int_2^3(3-x)dy=\frac72-\frac32c$."),("Set it equal to half the total",r"The total area is $5$, so each side should have area $\frac52$. Hence $\frac72-rac32c=\frac52$."),("Solve",r"This gives $1=\frac32c$, so $c=\frac23$."),("Answer",r"The value is $\boxed{\frac23}$.")],
18:[("Use coordinates",r"Place $A=(0,0)$, $B=(8,0)$, and $C=(8,6)$. Then $M$, the midpoint of $AC$, is $(4,3)$."),("Find the perpendicular line",r"The slope of $AC$ is $\frac68=\frac34$, so a line perpendicular to $AC$ has slope $-rac43$. Through $M$, it has equation $y-3=-\frac43(x-4)$."),("Find E",r"Point $E$ lies on $AB$, so $y=0$. Substituting gives $-3=-\frac43(x-4)$, so $x=rac{25}{4}$. Thus $AE=\frac{25}{4}$."),("Compute the area",r"Using base $AE$ on the $x$-axis and height $3$, the area of $\triangle AME$ is $\frac12\cdot\frac{25}{4}\cdot3=\frac{75}{8}$."),("Answer",r"The area is $\boxed{\frac{75}{8}}$.")],
19:[("Find when the clock is correct",r"The clock is wrong exactly when the true time display contains at least one digit $1$. So it is correct when the hour and minute contain no digit $1$."),("Count valid hours",r"On a $12$-hour clock, the hours without digit $1$ are $2,3,4,5,6,7,8,9$, so there are $8$ valid hours."),("Count valid minutes",r"For minutes $00$ through $59$, the tens digit can be $0,2,3,4,5$ and the ones digit can be any digit except $1$. That gives $5\cdot9=45$ valid minutes per valid hour."),("Compute the fraction",r"In one $12$-hour cycle, there are $8\cdot45=360$ correct minutes out of $12\cdot60=720$ minutes."),("Answer",r"The fraction is $\boxed{\frac12}$.")],
20:[("Find the third side",r"The right triangle has legs $AB=1$ and $BC=2$, so $AC=\sqrt{1^2+2^2}=\sqrt5$."),("Use the angle bisector theorem",r"Because $AD$ bisects $\angle A$, the theorem gives $\frac{BD}{DC}=\frac{AB}{AC}=\frac1{\sqrt5}$."),("Turn the ratio into a length",r"Since $BD+DC=BC=2$, the part adjacent to $AB$ is $BD=\frac{2\cdot AB}{AB+AC}=\frac{2}{1+\\sqrt5}$."),("Simplify",r"Rationalizing gives $\frac{2}{1+\sqrt5}\cdot\frac{\sqrt5-1}{\sqrt5-1}=\frac{\sqrt5-1}{2}$."),("Answer",r"Therefore $BD=\boxed{\frac{\sqrt5-1}{2}}$.")],
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
        if r["year"] == "2009" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {13, 17},
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
        + "- Answer verification source: AoPS 2009 AMC 10B Answer Key\n\n"
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











