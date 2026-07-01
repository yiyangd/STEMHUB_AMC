import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 57
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2011_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16,17,18,19,20}
SKIPPED = []
BATCH_LABEL = "2011 AMC 10A Problems 11-20"
NEXT_START = "2011 AMC 10A Problem 21"

ANS = {
    11: ("B", r"\frac{25}{32}"),
    12: ("A", "13"),
    13: ("A", "12"),
    14: ("B", r"\frac{1}{12}"),
    15: ("C", "440"),
    16: ("B", r"2\sqrt{6}"),
    17: ("C", "25"),
    18: ("C", "2"),
    19: ("E", "62"),
    20: ("D", r"\frac{1}{3}"),
}

OV = {
    11: (r"Square $EFGH$ has one vertex on each side of square $ABCD$. Point $E$ is on $\overline{AB}$ with $AE=7\cdot EB$. What is the ratio of the area of $EFGH$ to the area of $ABCD$?", [("A",r"\frac{49}{64}"),("B",r"\frac{25}{32}"),("C",r"\frac{7\sqrt2}{8}"),("D",r"\frac{5}{8}"),("E",r"\frac{14}{4}")]),
    12: (r"The players on a basketball team made some three-point shots, some two-point shots, and some one-point free throws. They scored as many points with two-point shots as with three-point shots. Their number of successful free throws was one more than their number of successful two-point shots. The team's total score was $61$ points. How many free throws did they make?", [("A","13"),("B","14"),("C","15"),("D","16"),("E","17")]),
    13: (r"How many even integers are there between $200$ and $700$ whose digits are all different and come from the set $\{1,2,5,7,8,9\}$?", [("A","12"),("B","20"),("C","72"),("D","120"),("E","200")]),
    14: (r"A pair of standard $6$-sided fair dice is rolled once. The sum of the numbers rolled determines the diameter of a circle. What is the probability that the numerical value of the area of the circle is less than the numerical value of the circle's circumference?", [("A",r"\frac{1}{36}"),("B",r"\frac{1}{12}"),("C",r"\frac{1}{6}"),("D",r"\frac{1}{4}"),("E",r"\frac{5}{18}")]),
    15: (r"Roy bought a new battery-gasoline hybrid car. On a trip the car ran exclusively on its battery for the first $40$ miles, then ran exclusively on gasoline for the rest of the trip, using gasoline at a rate of $0.02$ gallons per mile. On the whole trip he averaged $55$ miles per gallon. How long was the trip in miles?", [("A","140"),("B","240"),("C","440"),("D","640"),("E","840")]),
    16: (r"Which of the following is equal to $\sqrt{9-6\sqrt2}+\sqrt{9+6\sqrt2}$?", [("A",r"3\sqrt2"),("B",r"2\sqrt6"),("C",r"7\sqrt2"),("D",r"3\sqrt3"),("E",r"6\sqrt2")]),
    17: (r"In the eight-term sequence $A,B,C,D,E,F,G,H$, the value of $C$ is $5$ and the sum of any three consecutive terms is $30$. What is $A+H$?", [("A","17"),("B","18"),("C","25"),("D","26"),("E","43")]),
    18: (r"Circles $A$, $B$, and $C$ each have radius $1$. Circles $A$ and $B$ share one point of tangency. Circle $C$ has a point of tangency with the midpoint of $\overline{AB}$. What is the area inside circle $C$ but outside circles $A$ and $B$?", [("A",r"3-\frac{\pi}{2}"),("B",r"\frac{\pi}{2}"),("C","2"),("D",r"\frac{3\pi}{4}"),("E",r"1+\frac{\pi}{2}")]),
    19: (r"In 1991 the population of a town was a perfect square. Ten years later, after an increase of $150$ people, the population was $9$ more than a perfect square. Now, in 2011, with an increase of another $150$ people, the population is once again a perfect square. Which of the following is closest to the percent growth of the town's population during this twenty-year period?", [("A","42"),("B","47"),("C","52"),("D","57"),("E","62")]),
    20: (r"Two points on the circumference of a circle of radius $r$ are selected independently and at random. From each point a chord of length $r$ is drawn in a clockwise direction. What is the probability that the two chords intersect?", [("A",r"\frac{1}{6}"),("B",r"\frac{1}{5}"),("C",r"\frac{1}{4}"),("D",r"\frac{1}{3}"),("E",r"\frac{1}{2}")]),
}

KEY_OVERRIDES = {
    11: "Use coordinates for the rotated inner square and compare side lengths.",
    12: "Translate point totals into variables for made shots and solve a linear equation.",
    13: "Count by hundreds digit and units digit, since the number must be even and in range.",
    14: "Convert the area-versus-circumference condition into a condition on the dice sum.",
    15: "Use total miles divided by gasoline gallons to express the overall miles per gallon.",
    16: "Recognize each radical as a square of a binomial radical.",
    17: "Use equal three-term sums to show the sequence repeats with period three.",
    18: "Compute circular overlap areas using the geometry of unit circles whose centers are $\sqrt2$ apart.",
    19: "Turn the population statements into square equations and factor the total growth.",
    20: "A chord of length equal to the radius subtends a $60^\circ$ arc; count starting positions that interleave endpoints.",
}

SOL = {
    11: [
        ("Choose a scale", r"Because the question asks for an area ratio, we can choose a convenient scale. Let $EB=1$, so $AE=7$ and the side length of square $ABCD$ is $8$."),
        ("Place the first vertex", r"Put $A=(0,8)$, $B=(8,8)$, $C=(8,0)$, and $D=(0,0)$. Then $E=(7,8)$. If $F$ lies on side $BC$, the horizontal change from $E$ to $F$ is $1$."),
        ("Use the square rotation", r"For the rotated square to land one vertex on each side, the vertical drop from $E$ to $F$ is $7$. Thus the side vector of the inner square can be taken as $(1,-7)$. Its squared side length is $1^2+7^2=50$."),
        ("Compare areas", r"The area of square $EFGH$ is $50$. The area of square $ABCD$ is $8^2=64$. So the ratio is $\frac{50}{64}=\frac{25}{32}$."),
        ("Conclude", r"The answer is $\boxed{\frac{25}{32}}$."),
    ],
    12: [
        ("Name the made shots", r"Let $x$ be the number of made three-point shots and $y$ be the number of made two-point shots. The number of free throws is then $y+1$."),
        ("Use the equal point condition", r"The team scored as many points from two-point shots as from three-point shots, so $2y=3x$. This means the points from three-point shots are also $2y$."),
        ("Write the total score", r"The total score is points from threes plus points from twos plus free throws: $2y+2y+(y+1)=61$."),
        ("Solve", r"This gives $5y+1=61$, so $5y=60$ and $y=12$. Therefore the number of free throws is $y+1=13$."),
        ("Conclude", r"The answer is $\boxed{13}$."),
    ],
    13: [
        ("Use the range first", r"The number is between $200$ and $700$, so its hundreds digit can only be $2$ or $5$ from the allowed set. A hundreds digit of $1$ is too small, and $7,8,9$ are too large."),
        ("Use evenness", r"The units digit must be even. From the allowed digits, the even choices are $2$ and $8$. Digits also have to be different."),
        ("Count when the hundreds digit is 2", r"If the hundreds digit is $2$, then the units digit cannot also be $2$, so it must be $8$. The tens digit can be any of $1,5,7,9$, giving $4$ numbers."),
        ("Count when the hundreds digit is 5", r"If the hundreds digit is $5$, then the units digit can be $2$ or $8$. After choosing the units digit, there are $4$ choices left for the tens digit, giving $2\cdot4=8$ numbers."),
        ("Add the cases", r"The total is $4+8=12$. The answer is $\boxed{12}$."),
    ],
    14: [
        ("Translate diameter into radius", r"Let the dice sum be $s$. Then the circle has diameter $s$ and radius $\frac{s}{2}$."),
        ("Compare area and circumference", r"The area is $\pi\left(\frac{s}{2}\right)^2=\frac{\pi s^2}{4}$, and the circumference is $\pi s$. We need $\frac{\pi s^2}{4}<\pi s$."),
        ("Simplify the inequality", r"Since $s$ is positive, divide by $\pi s$ to get $\frac{s}{4}<1$, so $s<4$. The only possible dice sums are therefore $2$ and $3$."),
        ("Count dice outcomes", r"There is $1$ way to roll a sum of $2$ and $2$ ways to roll a sum of $3$, for $3$ favorable outcomes out of $36$ total."),
        ("Compute the probability", r"The probability is $\frac{3}{36}=\frac{1}{12}$. The answer is $\boxed{\frac{1}{12}}$."),
    ],
    15: [
        ("Let the total distance be unknown", r"Let the whole trip length be $D$ miles. The first $40$ miles use no gasoline, so only $D-40$ miles use gasoline."),
        ("Write the gasoline used", r"The car uses gasoline at $0.02$ gallons per mile, so the gasoline used is $0.02(D-40)$ gallons."),
        ("Use miles per gallon", r"The whole-trip average is $55$ miles per gallon, so \[\frac{D}{0.02(D-40)}=55.\] This equation uses total miles divided by gasoline gallons."),
        ("Solve", r"Multiply both sides by the denominator: $D=55\cdot0.02(D-40)=1.1(D-40)$. Thus $D=1.1D-44$, so $0.1D=44$ and $D=440$."),
        ("Conclude", r"The trip was $\boxed{440}$ miles long."),
    ],
    16: [
        ("Look for squared binomials", r"Expressions like $9\pm6\sqrt2$ often come from squaring $\sqrt a\pm\sqrt b$, because $(\sqrt a\pm\sqrt b)^2=a+b\pm2\sqrt{ab}$."),
        ("Match the numbers", r"We need $a+b=9$ and $2\sqrt{ab}=6\sqrt2$, so $ab=18$. The pair $a=6$, $b=3$ works."),
        ("Rewrite each radical", r"Therefore $9+6\sqrt2=(\sqrt6+\sqrt3)^2$ and $9-6\sqrt2=(\sqrt6-\sqrt3)^2$. Both square roots are nonnegative, so the square roots are $\sqrt6+\sqrt3$ and $\sqrt6-\sqrt3$."),
        ("Add", r"The sum is $(\sqrt6-\sqrt3)+(\sqrt6+\sqrt3)=2\sqrt6$. The answer is $\boxed{2\sqrt6}$."),
    ],
    17: [
        ("Compare neighboring sums", r"The sums $A+B+C$ and $B+C+D$ are both $30$. Subtracting the common $B+C$ shows $A=D$."),
        ("See the repeating pattern", r"Similarly, comparing $B+C+D$ with $C+D+E$ gives $B=E$, and comparing $C+D+E$ with $D+E+F$ gives $C=F$. So the sequence repeats every three terms."),
        ("Use the value of C", r"Since $C=5$, we also have $F=5$. The sequence has the form $A,B,5,A,B,5,A,B$."),
        ("Use one three-term sum", r"Because $A+B+C=30$, we have $A+B+5=30$, so $A+B=25$."),
        ("Find A plus H", r"The eighth term $H$ is $B$, so $A+H=A+B=25$. The answer is $\boxed{25}$."),
    ],
    18: [
        ("Reconstruct the geometry", r"Circles $A$ and $B$ are unit circles tangent to each other. Circle $C$ is a unit circle tangent at the midpoint between their centers, so the center of $C$ is one unit above that midpoint in the diagram."),
        ("Find the overlap with one circle", r"The distance from the center of circle $C$ to the center of circle $A$ is $\sqrt2$. For two unit circles with center distance $\sqrt2$, the overlap consists of two $90^\circ$ sectors minus a square-like pair of right triangles. Its area is $\frac{\pi}{2}-1$."),
        ("Use symmetry", r"Circle $C$ overlaps circle $A$ and circle $B$ in two congruent regions. These two overlap regions do not overlap each other except at a boundary point, so the total area of circle $C$ covered by circles $A$ or $B$ is $2\left(\frac{\pi}{2}-1\right)=\pi-2$."),
        ("Subtract from circle C", r"Circle $C$ has area $\pi$. The area inside circle $C$ but outside circles $A$ and $B$ is $\pi-(\pi-2)=2$."),
        ("Conclude", r"The answer is $\boxed{2}$."),
    ],
    19: [
        ("Name the square populations", r"Let the 1991 population be $n^2$ and the 2011 population be $p^2$. Since the population increased by $300$ over the twenty years, we have $p^2-n^2=300$."),
        ("Factor the difference of squares", r"The equation becomes $(p-n)(p+n)=300$. The two factors must have the same parity, so the useful factor pairs are $(2,150)$, $(6,50)$, and $(10,30)$."),
        ("Test the middle-year condition", r"These pairs give possible $(n,p)$ values $(74,76)$, $(22,28)$, and $(10,20)$. The 2001 population is $n^2+150$, and it must be $9$ more than a square, so $n^2+141$ must be a square. Only $n=22$ works, since $22^2+141=625=25^2$."),
        ("Compute percent growth", r"The initial population was $22^2=484$ and the total increase was $300$. The percent growth is $\frac{300}{484}\cdot100\%\approx61.98\%$."),
        ("Choose the closest answer", r"The closest choice is $62$. The answer is $\boxed{62}$."),
    ],
    20: [
        ("Convert chord length to arc size", r"In a circle of radius $r$, a chord of length $r$ forms an equilateral triangle with the two radii to its endpoints. Therefore each chord subtends a $60^\circ$ central angle."),
        ("Fix the first chord", r"Because the circle is symmetric, fix the first starting point at angle $0^\circ$. Its clockwise chord ends at $60^\circ$. Now only the starting angle of the second chord is random."),
        ("Use endpoint interleaving", r"Two chords intersect inside the circle exactly when their endpoints alternate around the circle. For the fixed chord with endpoints $0^\circ$ and $60^\circ$, this happens if exactly one endpoint of the second chord lies on the arc from $0^\circ$ to $60^\circ$."),
        ("Count favorable starting angles", r"The second starting angle works if it lies between $0^\circ$ and $60^\circ$, or if its ending angle lies there, which means the starting angle lies between $300^\circ$ and $360^\circ$. These intervals have total length $120^\circ$."),
        ("Compute the probability", r"The probability is $\frac{120}{360}=\frac13$. The answer is $\boxed{\frac13}$."),
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {18}) else notes
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
        if r["year"] == "2011" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {18},
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
        + "- Answer verification source: AoPS 2011 AMC 10A Answer Key\n\n"
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























