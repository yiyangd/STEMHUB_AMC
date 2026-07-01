from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 42
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2008_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
SKIPPED = []
BATCH_LABEL = "2008 AMC 10B Problems 11-20"
NEXT_START = "2008 AMC 10B Problem 21"

ANS = {
    11: ("B", "53"),
    12: ("A", "2500"),
    13: ("B", "4015"),
    14: ("B", r"(-\frac{5\sqrt3}{3},5)"),
    15: ("A", "6"),
    16: ("A", r"\frac{3}{8}"),
    17: ("B", "0.189"),
    18: ("B", "900"),
    19: ("E", r"48\pi-36\sqrt3"),
    20: ("B", r"\frac{7}{18}"),
}

OV = {
    11: (r"Suppose that $(u_n)$ is a sequence of real numbers satisfying $u_{n+2}=2u_{n+1}+u_n$, and that $u_3=9$ and $u_6=128$. What is $u_5$?", [("A", "$40$"), ("B", "$53$"), ("C", "$68$"), ("D", "$88$"), ("E", "$104$")]),
    12: (r"Postman Pete has a pedometer to count his steps. The pedometer records up to $99999$ steps, then flips over to $00000$ on the next step. Pete plans to determine his mileage for a year. On January 1 Pete sets the pedometer to $00000$. During the year, the pedometer flips from $99999$ to $00000$ forty-four times. On December 31 the pedometer reads $50000$. Pete takes $1800$ steps per mile. Which of the following is closest to the number of miles Pete walked during the year?", [("A", "$2500$"), ("B", "$3000$"), ("C", "$3500$"), ("D", "$4000$"), ("E", "$4500$")]),
    13: (r"For each positive integer $n$, the mean of the first $n$ terms of a sequence is $n$. What is the $2008$th term of the sequence?", [("A", "$2008$"), ("B", "$4015$"), ("C", "$4016$"), ("D", "$4{,}030{,}056$"), ("E", "$4{,}032{,}064$")]),
    14: (r"Triangle $OAB$ has $O=(0,0)$, $B=(5,0)$, and $A$ in the first quadrant. In addition, $\angle ABO=90^\circ$ and $\angle AOB=30^\circ$. Suppose that $\overline{OA}$ is rotated $90^\circ$ counterclockwise about $O$. What are the coordinates of the image of $A$?", [("A", r"$(-\frac{10\sqrt3}{3},5)$"), ("B", r"$(-\frac{5\sqrt3}{3},5)$"), ("C", r"$(\sqrt3,5)$"), ("D", r"$(\frac{5\sqrt3}{3},5)$"), ("E", r"$(\frac{10\sqrt3}{3},5)$")]),
    15: (r"How many right triangles have integer leg lengths $a$ and $b$ and a hypotenuse of length $b+1$, where $b<100$?", [("A", "$6$"), ("B", "$7$"), ("C", "$8$"), ("D", "$9$"), ("E", "$10$")]),
    16: (r"Two fair coins are to be tossed once. For each head that results, one fair die is to be rolled. What is the probability that the sum of the die rolls is odd? Note that if no die is rolled, their sum is $0$.", [("A", r"$\frac{3}{8}$"), ("B", r"$\frac{1}{2}$"), ("C", r"$\frac{43}{72}$"), ("D", r"$\frac{5}{8}$"), ("E", r"$\frac{2}{3}$")]),
    17: (r"A poll shows that $70\%$ of all voters approve of the mayor's work. On three separate occasions a pollster selects a voter at random. What is the probability that on exactly one of these three occasions the voter approves of the mayor's work?", [("A", "$0.063$"), ("B", "$0.189$"), ("C", "$0.233$"), ("D", "$0.333$"), ("E", "$0.441$")]),
    18: (r"Bricklayer Brenda would take $9$ hours to build a chimney alone, and bricklayer Brandon would take $10$ hours to build it alone. When they work together they talk a lot, and their combined output is decreased by $10$ bricks per hour. Working together, they build the chimney in $5$ hours. How many bricks are in the chimney?", [("A", "$500$"), ("B", "$900$"), ("C", "$950$"), ("D", "$1000$"), ("E", "$1900$")]),
    19: (r"A cylindrical tank with radius $4$ feet and height $9$ feet is lying on its side. The tank is filled with water to a depth of $2$ feet. What is the volume of the water, in cubic feet?", [("A", r"$24\pi-36\sqrt2$"), ("B", r"$24\pi-24\sqrt3$"), ("C", r"$36\pi-36\sqrt3$"), ("D", r"$36\pi-24\sqrt2$"), ("E", r"$48\pi-36\sqrt3$")]),
    20: (r"The faces of a cubical die are marked with the numbers $1,2,2,3,3,$ and $4$. The faces of a second cubical die are marked with the numbers $1,3,4,5,6,$ and $8$. Both dice are thrown. What is the probability that the sum of the two top numbers will be $5$, $7$, or $9$?", [("A", r"$\frac{5}{18}$"), ("B", r"$\frac{7}{18}$"), ("C", r"$\frac{11}{18}$"), ("D", r"$\frac{3}{4}$"), ("E", r"$\frac{8}{9}$")]),
}

KEY_OVERRIDES = {
    11: "Use the recurrence backward from u6 and u3 to solve for u5.",
    12: "Translate pedometer rollovers into total steps, then divide by steps per mile.",
    13: "Convert mean information into partial sums, then subtract consecutive sums.",
    14: "Find A by trigonometry, then apply the 90-degree coordinate rotation rule.",
    15: "Use the Pythagorean theorem to turn the condition into a count of odd integers.",
    16: "Condition on how many heads occur, then compute when the die-roll sum is odd.",
    17: "Use the binomial probability for exactly one approval in three independent selections.",
    18: "Set the combined work rate equal to the sum of individual rates minus 10 bricks per hour.",
    19: "Compute a circular segment area and multiply by the tank length.",
    20: "Count favorable ordered die-face pairs with repeated labels treated as distinct faces.",
}

SOL = {
    11: [("Choose nearby unknowns", r"The recurrence relates three consecutive terms, and the question asks for $u_5$ while giving $u_3$ and $u_6$. So let $u_4=y$ and $u_5=x$."), ("Write equations from the recurrence", r"Using $u_5=2u_4+u_3$, we get $x=2y+9$. Using $u_6=2u_5+u_4$, we get $128=2x+y$."), ("Solve the two equations", r"Substitute $x=2y+9$ into $128=2x+y$: $128=2(2y+9)+y=5y+18$. Thus $5y=110$ and $y=22$."), ("Find the requested term", r"Now $x=2y+9=2\cdot22+9=53$."), ("Answer", r"Therefore $u_5=\boxed{53}$.")],
    12: [("Understand one rollover", r"The pedometer flips after recording $99999$ and taking one more step, so each full flip represents $100000$ steps."), ("Count total steps", r"There were $44$ full flips and then the display ended at $50000$. That means Pete walked $44\cdot100000+50000=4{,}450{,}000$ steps."), ("Convert steps to miles", r"At $1800$ steps per mile, the distance is $\frac{4{,}450{,}000}{1800}\approx2472.2$ miles."), ("Choose the closest option", r"Among the choices, $2500$ is closest to $2472.2$."), ("Answer", r"The closest number of miles is $\boxed{2500}$.")],
    13: [("Translate mean into sum", r"If the mean of the first $n$ terms is $n$, then the sum of the first $n$ terms is $n\cdot n=n^2$."), ("Use consecutive partial sums", r"The $2008$th term is the sum of the first $2008$ terms minus the sum of the first $2007$ terms."), ("Compute the difference", r"So the term is $2008^2-2007^2$. Use the difference of squares: $(2008-2007)(2008+2007)=1\cdot4015=4015$."), ("Answer", r"The $2008$th term is $\boxed{4015}$.")],
    14: [("Locate point A", r"Because $\angle ABO=90^\circ$ and $B=(5,0)$, segment $AB$ is vertical, so $A$ has $x$-coordinate $5$."), ("Use the 30-degree angle", r"The line $OA$ makes a $30^\circ$ angle with the positive $x$-axis. Therefore $\tan30^\circ=\frac{y}{5}$, so $y=5\tan30^\circ=\frac{5\sqrt3}{3}$."), ("Apply the rotation rule", r"A $90^\circ$ counterclockwise rotation about the origin sends $(x,y)$ to $(-y,x)$."), ("Substitute A's coordinates", r"Thus $A=(5,\frac{5\sqrt3}{3})$ maps to $(-\frac{5\sqrt3}{3},5)$."), ("Answer", r"The image is $\boxed{(-\frac{5\sqrt3}{3},5)}$.")],
    15: [("Start with the Pythagorean theorem", r"The legs are $a$ and $b$, and the hypotenuse is $b+1$, so $a^2+b^2=(b+1)^2$."), ("Simplify", r"Expanding gives $a^2+b^2=b^2+2b+1$, so $a^2=2b+1$. Therefore $b=\frac{a^2-1}{2}$."), ("Find which a-values work", r"For $b$ to be an integer, $a$ must be odd. Also $b<100$ means $\frac{a^2-1}{2}<100$, so $a^2<201$."), ("Count positive leg lengths", r"The positive odd values greater than $1$ with square less than $201$ are $3,5,7,9,11,13$. The value $a=1$ would give $b=0$, not a triangle leg."), ("Answer", r"There are $\boxed{6}$ such right triangles.")],
    16: [("Condition on the number of heads", r"The number of dice rolled equals the number of heads among two coins. We consider $0$, $1$, or $2$ heads."), ("Handle zero heads", r"If there are no heads, no die is rolled and the sum is $0$, which is even. This case contributes no success."), ("Handle one head", r"Exactly one head occurs with probability $\frac12$. Then one die is rolled, and it is odd with probability $\frac12$, contributing $\frac12\cdot\frac12=\frac14$."), ("Handle two heads", r"Two heads occur with probability $\frac14$. Two dice have an odd sum when one die is odd and the other is even, which has probability $\frac12$. This contributes $\frac14\cdot\frac12=\frac18$."), ("Add the successful cases", r"The total probability is $\frac14+\frac18=\frac38$."), ("Answer", r"The probability is $\boxed{\frac38}$.")],
    17: [("Identify success and failure", r"An approval has probability $0.7$, and a non-approval has probability $0.3$. We want exactly one approval in three selections."), ("Choose where the approval happens", r"The one approval can occur in any one of the $3$ selections."), ("Compute one pattern", r"For a fixed pattern such as approve, not approve, not approve, the probability is $0.7(0.3)^2$."), ("Multiply by the number of patterns", r"Thus the probability is $3\cdot0.7\cdot(0.3)^2=3\cdot0.7\cdot0.09=0.189$."), ("Answer", r"The probability is $\boxed{0.189}$.")],
    18: [("Let the chimney size be N", r"Let $N$ be the number of bricks in the chimney. Brenda's rate is $\frac{N}{9}$ bricks per hour, and Brandon's rate is $\frac{N}{10}$ bricks per hour."), ("Account for the lost output", r"Together, their actual rate is decreased by $10$ bricks per hour, so it is $\frac{N}{9}+\frac{N}{10}-10$."), ("Use the five-hour completion time", r"Since they finish $N$ bricks in $5$ hours, their actual rate is also $\frac{N}{5}$. Therefore $\frac{N}{9}+\frac{N}{10}-10=\frac{N}{5}$."), ("Solve", r"The left rate before subtracting is $\frac{19N}{90}$. So $\frac{19N}{90}-\frac{18N}{90}=10$, giving $\frac{N}{90}=10$ and $N=900$."), ("Answer", r"The chimney contains $\boxed{900}$ bricks.")],
    19: [("Look at the circular cross-section", r"Because the tank lies on its side, the water volume equals the area of a circular segment in the end circle times the tank length $9$."), ("Find the segment geometry", r"The radius is $4$, and the water depth is $2$ from the bottom. So the water line is $2$ feet below the center, making the distance from the center to the chord equal to $2$."), ("Find the central angle", r"In the right triangle from the center to the chord midpoint, $\cos\theta=\frac{2}{4}=\frac12$, so $\theta=60^\circ$. The full sector angle for the water segment is $120^\circ=\frac{2\pi}{3}$."), ("Compute the segment area", r"The sector area is $\frac12\cdot4^2\cdot\frac{2\pi}{3}=\frac{16\pi}{3}$. The triangle area is $\frac12\cdot4^2\sin120^\circ=4\sqrt3$. So the segment area is $\frac{16\pi}{3}-4\sqrt3$."), ("Multiply by the tank length", r"The volume is $9(\frac{16\pi}{3}-4\sqrt3)=48\pi-36\sqrt3$."), ("Answer", r"The volume is $\boxed{48\pi-36\sqrt3}$ cubic feet.")],
    20: [("Treat repeated labels as separate faces", r"Each die has $6$ faces, so there are $36$ equally likely ordered outcomes. The repeated numbers on the first die count as separate faces."), ("Count outcomes from the first die face 1", r"If the first die shows $1$, the second die must show $4$, $6$, or $8$, giving $3$ favorable outcomes."), ("Count outcomes from the two faces labeled 2 and 3", r"For each face labeled $2$, the second die can show $3$ or $5$, giving $2\cdot2=4$ outcomes. For each face labeled $3$, the second die can show $4$ or $6$, giving another $4$ outcomes."), ("Count outcomes from the first die face 4", r"If the first die shows $4$, the second die can show $1$, $3$, or $5$, giving $3$ outcomes."), ("Compute the probability", r"There are $3+4+4+3=14$ favorable outcomes out of $36$, so the probability is $\frac{14}{36}=\frac{7}{18}$."), ("Answer", r"The probability is $\boxed{\frac{7}{18}}$.")],
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




