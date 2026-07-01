from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 39
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2008_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
SKIPPED = []
BATCH_LABEL = "2008 AMC 10A Problems 11-20"
NEXT_START = "2008 AMC 10A Problem 21"

ANS = {
    11: ("D", "8"),
    12: ("C", "3.4r"),
    13: ("D", r"(\frac15+\frac17)(t-1)=1"),
    14: ("D", "2.7"),
    15: ("D", "150"),
    16: ("B", r"\frac19"),
    17: ("B", r"54+9\pi"),
    18: ("B", r"\frac{59}{4}"),
    19: ("C", r"(3+\sqrt{10})\pi"),
    20: ("D", "98"),
}


OV = {
    11: (r"While Steve and LeRoy are fishing $1$ mile from shore, their boat springs a leak, and water comes in at a constant rate of $10$ gallons per minute. The boat will sink if it takes in more than $30$ gallons of water. Steve starts rowing toward the shore at a constant rate of $4$ miles per hour while LeRoy bails water out of the boat. What is the slowest rate, in gallons per minute, at which LeRoy can bail if they are to reach the shore without sinking?", [("A", "$2$"), ("B", "$4$"), ("C", "$6$"), ("D", "$8$"), ("E", "$10$")]),
    12: (r"In a collection of red, blue, and green marbles, there are $25\%$ more red marbles than blue marbles, and there are $60\%$ more green marbles than red marbles. Suppose that there are $r$ red marbles. What is the total number of marbles in that collection?", [("A", "$2.85r$"), ("B", "$3r$"), ("C", "$3.4r$"), ("D", "$3.85r$"), ("E", "$4.25r$")]),
    13: (r"Doug can paint a room in $5$ hours. Dave can paint the same room in $7$ hours. Doug and Dave paint the room together and take a one-hour break for lunch. Let $t$ be the total time, in hours, required for them to complete the job working together, including lunch. Which of the following equations is satisfied by $t$?", [("A", r"$(\frac15+\frac17)(t+1)=1$"), ("B", r"$(\frac15+\frac17)t+1=1$"), ("C", r"$(\frac15+\frac17)t=1$"), ("D", r"$(\frac15+\frac17)(t-1)=1$"), ("E", r"$(5+7)t=1$")]),
    14: (r"Older television screens have aspect ratio $4:3$. A movie has aspect ratio $2:1$ and is shown on an older television screen with a $27$-inch diagonal by letterboxing, using dark strips of equal height at the top and bottom. What is the height, in inches, of each darkened strip?", [("A", "$2$"), ("B", "$2.25$"), ("C", "$2.5$"), ("D", "$2.7$"), ("E", "$3$")]),
    15: (r"Yesterday Han drove $1$ hour longer than Ian at an average speed $5$ miles per hour faster than Ian. Jan drove $2$ hours longer than Ian at an average speed $10$ miles per hour faster than Ian. Han drove $70$ miles more than Ian. How many more miles did Jan drive than Ian?", [("A", "$120$"), ("B", "$130$"), ("C", "$140$"), ("D", "$150$"), ("E", "$160$")]),
    16: (r"Points $A$ and $B$ lie on a circle centered at $O$, and $\angle AOB=60^\circ$. A second circle is internally tangent to the first and tangent to both $OA$ and $OB$. What is the ratio of the area of the smaller circle to that of the larger circle?", [("A", r"$\frac1{16}$"), ("B", r"$\frac19$"), ("C", r"$\frac18$"), ("D", r"$\frac16$"), ("E", r"$\frac14$")]),
    17: (r"An equilateral triangle has side length $6$. What is the area of the region containing all points that are outside the triangle and not more than $3$ units from a point of the triangle?", [("A", r"$36+24\sqrt3$"), ("B", r"$54+9\pi$"), ("C", r"$54+18\sqrt3+6\pi$"), ("D", r"$(2\sqrt3+3)^2\pi$"), ("E", r"$9(\sqrt3+1)^2\pi$")]),
    18: (r"A right triangle has perimeter $32$ and area $20$. What is the length of its hypotenuse?", [("A", r"$\frac{57}{4}$"), ("B", r"$\frac{59}{4}$"), ("C", r"$\frac{61}{4}$"), ("D", r"$\frac{63}{4}$"), ("E", r"$\frac{65}{4}$")]),
    19: (r"Rectangle $PQRS$ lies in a plane with $PQ=RS=2$ and $QR=SP=6$. The rectangle is rotated $90^\circ$ clockwise about $R$, then rotated $90^\circ$ clockwise about the point that $S$ moved to after the first rotation. What is the length of the path traveled by point $P$?", [("A", r"$(2\sqrt3+5)\pi$"), ("B", r"$6\pi$"), ("C", r"$(3+\sqrt{10})\pi$"), ("D", r"$(\sqrt3+2\sqrt5)\pi$"), ("E", r"$2\sqrt{10}\pi$")]),
    20: (r"Trapezoid $ABCD$ has bases $AB$ and $CD$ and diagonals intersecting at $K$. Suppose that $AB=9$, $DC=12$, and the area of $\triangle AKD$ is $24$. What is the area of trapezoid $ABCD$?", [("A", "$92$"), ("B", "$94$"), ("C", "$96$"), ("D", "$98$"), ("E", "$100$")]),
}


KEY_OVERRIDES = {
    11: "Balance leaking and bailing over the rowing time so the water stays at or below 30 gallons.",
    12: "Write blue and green counts in terms of the red count r.",
    13: "Subtract the lunch break from total time to get actual painting time.",
    14: "Use a 3-4-5 television screen and compare the movie height with the screen height.",
    15: "Set up Ian's time and speed, then reuse Han's condition to compute Jan's extra distance.",
    16: "Use the angle bisector and tangency distances in a 60-degree sector.",
    17: "Use the outer offset area formula: perimeter times radius plus a full circle of corner arcs.",
    18: "Use area and perimeter relations for the legs and hypotenuse of a right triangle.",
    19: "Add two quarter-circle arc lengths with different rotation centers.",
    20: "Use diagonal intersection ratios in a trapezoid to relate triangle area to trapezoid height.",
}


SOL = {
    11: [("Find the rowing time", r"The boat is $1$ mile from shore and rows at $4$ miles per hour, so the trip takes $\frac14$ hour, or $15$ minutes."), ("Find the incoming water", r"Water enters at $10$ gallons per minute for $15$ minutes, so $150$ gallons would enter without bailing."), ("Limit the net water", r"The boat can take at most $30$ gallons, so LeRoy must remove at least $150-30=120$ gallons during the $15$ minutes."), ("Compute the rate", r"The slowest bailing rate is $120/15=8$ gallons per minute."), ("Answer", r"The answer is $\boxed{8}$." )],
    12: [("Express blue in terms of red", r"There are $25\%$ more red marbles than blue marbles, so $r=1.25b$. Therefore $b=\frac{r}{1.25}=0.8r$."), ("Express green in terms of red", r"There are $60\%$ more green marbles than red marbles, so $g=1.6r$."), ("Add the three colors", r"The total is $r+0.8r+1.6r=3.4r$."), ("Answer", r"The total number of marbles is $\boxed{3.4r}$." )],
    13: [("Find the combined work rate", r"Doug paints $\frac15$ of the room per hour, and Dave paints $\frac17$ of the room per hour. Together their rate is $\frac15+\frac17$."), ("Account for lunch", r"The total time is $t$, but one hour is lunch, so the actual painting time is $t-1$."), ("Set completed work equal to 1", r"Rate times working time equals one full room: $(\frac15+\frac17)(t-1)=1$."), ("Answer", r"The correct equation is $\boxed{(\frac15+\frac17)(t-1)=1}$." )],
    14: [("Find screen dimensions", r"A $4:3$ screen with diagonal $27$ is a scaled $3$-$4$-$5$ triangle. The scale factor is $27/5=5.4$, so the screen width is $21.6$ and height is $16.2$."), ("Fit the movie width", r"The movie has aspect ratio $2:1$ and uses the full screen width $21.6$, so its height is $21.6/2=10.8$."), ("Find total dark height", r"The unused vertical height is $16.2-10.8=5.4$ inches."), ("Split into two strips", r"The top and bottom strips have equal height, so each is $5.4/2=2.7$ inches."), ("Answer", r"Each strip is $\boxed{2.7}$ inches high." )],
    15: [("Let Ian's time and speed be variables", r"Let Ian drive for $t$ hours at $v$ miles per hour. Ian's distance is $tv$."), ("Use Han's information", r"Han drives for $t+1$ hours at speed $v+5$, and he drives $70$ more miles than Ian. Thus $(t+1)(v+5)-tv=70$."), ("Simplify Han's equation", r"Expanding gives $v+5t+5=70$, so $v+5t=65$."), ("Compute Jan's extra distance", r"Jan's extra distance over Ian is $(t+2)(v+10)-tv=2v+10t+20=2(v+5t)+20=2\cdot65+20=150$."), ("Answer", r"Jan drove $\boxed{150}$ more miles than Ian." )],
    16: [("Use symmetry", r"The smaller circle tangent to both rays $OA$ and $OB$ has its center on the angle bisector of the $60^\circ$ angle."), ("Relate radius to distance from O", r"If the smaller circle has radius $r$ and its center is distance $x$ from $O$, then $r=x\sin30^\circ=\frac{x}{2}$, so $x=2r$."), ("Use internal tangency", r"Let the larger circle have radius $R$. Internal tangency gives $x+r=R$. Since $x=2r$, we get $3r=R$."), ("Compare areas", r"The area ratio is $\frac{r^2}{R^2}=\frac{r^2}{(3r)^2}=\frac19$."), ("Answer", r"The answer is $\boxed{\frac19}$." )],
    17: [("Think of expanding the triangle", r"The desired region is the outside band within distance $3$ of the triangle. For a convex figure, this outside area equals perimeter times the distance plus the area of a circle of that radius from the rounded corners."), ("Compute the side bands", r"The equilateral triangle has perimeter $18$. With distance $3$, the rectangular side bands contribute $18\cdot3=54$."), ("Compute the corner arcs", r"The three rounded corner sectors together make one full circle of radius $3$, contributing $\pi\cdot3^2=9\pi$."), ("Add", r"The outside region has area $54+9\pi$."), ("Answer", r"The answer is $\boxed{54+9\pi}$." )],
    18: [("Name the sides", r"Let the legs be $a$ and $b$, and let the hypotenuse be $c$. The area condition gives $\frac12ab=20$, so $ab=40$."), ("Use the perimeter", r"The perimeter is $a+b+c=32$, so $a+b=32-c$."), ("Use the Pythagorean relation", r"Because $c^2=a^2+b^2=(a+b)^2-2ab$, we have $c^2=(32-c)^2-80$."), ("Solve", r"Expanding and simplifying gives $64c=944$, so $c=\frac{944}{64}=\frac{59}{4}$."), ("Answer", r"The hypotenuse is $\boxed{\frac{59}{4}}$." )],
    19: [("Break the path into two arcs", r"Point $P$ moves along a quarter-circle during each $90^\circ$ rotation. We need the radius of each arc."), ("First rotation", r"In the original rectangle, $PR=\sqrt{2^2+6^2}=2\sqrt{10}$. A quarter-circle with this radius has length $\frac{\pi}{2}\cdot2\sqrt{10}=\pi\sqrt{10}$."), ("Second rotation", r"After the first rotation, the new center is where $S$ moved. The distance from that point to the moved point $P$ is $6$, so the second quarter-circle has length $\frac{\pi}{2}\cdot6=3\pi$."), ("Add arcs", r"The total path length is $\pi\sqrt{10}+3\pi=(3+\sqrt{10})\pi$."), ("Answer", r"The answer is $\boxed{(3+\sqrt{10})\pi}$." )],
    20: [("Use the diagonal ratio", r"In a trapezoid, the diagonals divide each other in the ratio of the bases. Since $AB:CD=9:12=3:4$, point $K$ is $\frac37$ of the way from $A$ to $C$."), ("Relate K to the height", r"Let the trapezoid height be $h$. Then $K$ is at height $\frac47h$ above base $CD$."), ("Compute triangle AKD area", r"Using coordinates or equivalent base-height reasoning, the area of $\triangle AKD$ is $\frac{18h}{7}$. We are given this area is $24$, so $\frac{18h}{7}=24$."), ("Find h and the trapezoid area", r"Thus $h=\frac{28}{3}$. The trapezoid area is $\frac12(9+12)h=\frac{21}{2}\cdot\frac{28}{3}=98$."), ("Answer", r"The area is $\boxed{98}$." )],
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
        if r["year"] == "2008" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2008 AMC 10A Answer Key\n\n"
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
