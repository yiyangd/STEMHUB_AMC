import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 92
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2016_AMC_10A_Answer_Key"
TARGET_NUMBERS = {12,13,14,16,17,18,19,20}
SKIPPED = [
    "2016 AMC 10A Problem 11 skipped: shaded rectangle area depends on the original diagram.",
    "2016 AMC 10A Problem 15 skipped: cookie-circle layout depends on the original diagram."
]
BATCH_LABEL = "2016 AMC 10A Problems 12-14, 16-20"
NEXT_START = "2016 AMC 10A Problem 21"

ANS={12:("A",r"p<\frac18"),13:("B","2"),14:("C","337"),16:("D",r"reflection about the line $y=x$"),17:("A","12"),18:("C","6"),19:("E","20"),20:("B","14")}

OV={
12:(r"Three distinct integers are selected at random between $1$ and $2016$, inclusive. Which of the following is a correct statement about the probability $p$ that the product of the three integers is odd?",[("A",r"$p<\frac18$"),("B",r"$p=\frac18$"),("C",r"$\frac18<p<\frac13$"),("D",r"$p=\frac13$"),("E",r"$p>\frac13$")]),
13:(r"Five friends sat in a movie theater in a row containing $5$ seats, numbered $1$ to $5$ from left to right. During the movie Ada went to the lobby. When she returned, Bea had moved two seats to the right, Ceci had moved one seat to the left, and Dee and Edie had switched seats, leaving an end seat for Ada. In which seat had Ada been sitting before she got up?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
14:(r"How many ways are there to write $2016$ as the sum of twos and threes, ignoring order? For example, $1008\cdot2+0\cdot3$ and $402\cdot2+404\cdot3$ are two such ways.",[("A","236"),("B","336"),("C","337"),("D","403"),("E","672")]),
16:(r"A triangle with vertices $A(0,2)$, $B(-3,2)$, and $C(-3,0)$ is reflected about the $x$-axis. Then the image $\triangle A'B'C'$ is rotated counterclockwise about the origin by $90^\circ$ to produce $\triangle A''B''C''$. Which of the following transformations will return $\triangle A''B''C''$ to $\triangle ABC$?",[("A",r"counterclockwise rotation about the origin by $90^\circ$"),("B",r"clockwise rotation about the origin by $90^\circ$"),("C",r"reflection about the $x$-axis"),("D",r"reflection about the line $y=x$"),("E",r"reflection about the $y$-axis")]),
17:(r"Let $N$ be a positive multiple of $5$. One red ball and $N$ green balls are arranged in a line in random order. Let $P(N)$ be the probability that at least $\frac35$ of the green balls are on the same side of the red ball. Observe that $P(5)=1$ and that $P(N)$ approaches $\frac45$ as $N$ grows large. What is the sum of the digits of the least value of $N$ such that $P(N)<\frac{321}{400}$?",[("A","12"),("B","14"),("C","16"),("D","18"),("E","20")]),
18:(r"Each vertex of a cube is to be labeled with an integer $1$ through $8$, with each integer being used once, in such a way that the sum of the four numbers on the vertices of a face is the same for each face. Arrangements that can be obtained from each other through rotations of the cube are considered to be the same. How many different arrangements are possible?",[("A","1"),("B","3"),("C","6"),("D","12"),("E","24")]),
19:(r"In rectangle $ABCD$, $AB=6$ and $BC=3$. Point $E$ between $B$ and $C$, and point $F$ between $E$ and $C$ are such that $BE=EF=FC$. Segments $AE$ and $AF$ intersect $BD$ at $P$ and $Q$, respectively. The ratio $BP:PQ:QD$ can be written as $r:s:t$, where the greatest common factor of $r$, $s$, and $t$ is $1$. What is $r+s+t$?",[("A","7"),("B","9"),("C","12"),("D","15"),("E","20")]),
20:(r"For some particular value of $N$, when $(a+b+c+d+1)^N$ is expanded and like terms are combined, the resulting expression contains exactly $1001$ terms that include all four variables $a$, $b$, $c$, and $d$, each to some positive power. What is $N$?",[("A","9"),("B","14"),("C","16"),("D","17"),("E","19")]),
}

KEY_OVERRIDES={12:"Use parity: the product is odd exactly when all selected integers are odd.",13:"Translate each friend's movement into a seat-position constraint.",14:"Solve a nonnegative integer equation and use parity to count solutions.",16:"Represent reflections and rotations as coordinate transformations.",17:"Count possible positions of the red ball that leave enough green balls on one side.",18:"Count valid labelings on a fixed cube, then divide by the 24 cube rotations.",19:"Use coordinates so distances along the diagonal become proportional to x-coordinates.",20:"Count exponent quadruples with positive powers using stars and bars."}

SOL={
12:[("Recognize when the product is odd",r"A product of integers is odd only if every factor is odd. So this problem is really asking for the probability that all three selected integers are odd."),("Count the odds and evens",r"From $1$ to $2016$, exactly half the numbers are odd, so there are $1008$ odd integers and $2016$ integers total."),("Compare with one-half cubed",r"Because the selections are distinct and made without replacement, the probability is \[p=\frac{1008}{2016}\cdot\frac{1007}{2015}\cdot\frac{1006}{2014}.\] The first factor is $\frac12$, while the next two factors are each slightly less than $\frac12$."),("Place the probability",r"Therefore $p$ is slightly less than \[\frac12\cdot\frac12\cdot\frac12=\frac18.\]"),("Conclude",r"The correct statement is $p<\frac18$, so the answer is $\boxed{\text{A}}$."),],
13:[("Turn the story into seat positions",r"Number the seats $1$ through $5$. Bea moves two seats to the right, so Bea must have started in seat $1$, $2$, or $3$. Ceci moves one seat to the left, so Ceci must have started in seat $2$, $3$, $4$, or $5$."),("Use the returned arrangement",r"After Ada returns, the only empty seat is an end seat. Since Bea, Ceci, Dee, and Edie occupy four seats after their moves, we can test the constraints by tracking where those four people land."),("Find the forced positions",r"The only consistent possibility has Bea starting in seat $1$ and moving to seat $3$, while Ceci starts in seat $3$ and moves to seat $2$. Dee and Edie simply exchange the two remaining non-Ada starting seats, seats $4$ and $5$."),("Locate Ada's original seat",r"That leaves seat $2$ as Ada's original seat. After the moves, seat $1$ is empty, which is an end seat, so Ada can return there."),("Conclude",r"Ada had been sitting in seat $\boxed{2}$."),],
14:[("Choose variables for the numbers of twos and threes",r"Let $x$ be the number of twos and $y$ be the number of threes. Ignoring order means that a choice of $(x,y)$ gives exactly one way."),("Set up the equation",r"We need \[2x+3y=2016,\] where $x$ and $y$ are nonnegative integers."),("Use parity",r"The term $2x$ is even and $2016$ is even, so $3y$ must be even. Since $3$ is odd, $y$ must be even."),("Count possible y-values",r"The largest possible value of $y$ is $\lfloor 2016/3\rfloor=672$. The even values from $0$ through $672$ are \[0,2,4,\ldots,672,\] which gives $\frac{672}{2}+1=337$ choices."),("Conclude",r"For each such $y$, $x$ is determined, so there are $\boxed{337}$ ways."),],
16:[("Represent the first transformation",r"Reflecting a point $(x,y)$ about the $x$-axis changes it to $(x,-y)$. This is a good way to avoid drawing the triangle."),("Apply the rotation",r"A counterclockwise rotation by $90^\circ$ sends a point $(u,v)$ to $(-v,u)$. Starting from $(x,-y)$, the rotation gives \[(x,-y)\mapsto (y,x).\]"),("Recognize the combined effect",r"The rule $(x,y)\mapsto(y,x)$ is exactly reflection about the line $y=x$. So the two given transformations together act like one reflection over $y=x$."),("Undo the transformation",r"A reflection is its own inverse: applying the same reflection again returns every point to its original position."),("Conclude",r"The needed transformation is reflection about the line $y=x$, so the answer is $\boxed{\text{D}}$."),],
17:[("Focus on the red ball's position",r"Once the red ball is placed, suppose there are $k$ green balls on its left. Then there are $N-k$ green balls on its right. Each value $k=0,1,\ldots,N$ is equally likely."),("Translate the condition",r"At least $\frac35$ of the green balls are on the same side of the red ball exactly when \[k\ge \frac{3N}{5}\quad\text{or}\quad N-k\ge \frac{3N}{5}.\] The second inequality is $k\le\frac{2N}{5}$."),("Count favorable positions",r"Because $N$ is a multiple of $5$, the values $0$ through $\frac{2N}{5}$ give $\frac{2N}{5}+1$ possibilities, and the values $\frac{3N}{5}$ through $N$ give another $\frac{2N}{5}+1$ possibilities. Thus \[P(N)=\frac{\frac{4N}{5}+2}{N+1}.\]"),("Solve the inequality",r"We need \[\frac{\frac{4N}{5}+2}{N+1}<\frac{321}{400}.\] Multiplying through gives $320N+800<321N+321$, so $N>479$."),("Use the multiple-of-5 condition",r"The least positive multiple of $5$ greater than $479$ is $480$. The sum of its digits is $4+8+0=12$."),("Conclude",r"The answer is $\boxed{12}$."),],
18:[("Fix the cube first",r"Start by counting labelings on a cube whose positions are fixed. Since each face must have the same sum and the total of all labels is $1+2+\cdots+8=36$, each face must sum to $18$."),("Choose the labels on one face",r"A face must contain four labels whose sum is $18$. The possible four-element sets are \[(1,2,7,8),(1,3,6,8),(1,4,5,8),(1,4,6,7),(2,3,5,8),(2,3,6,7),(2,4,5,7),(3,4,5,6).\]"),("Count compatible side arrangements",r"For a chosen ordered top face $a,b,c,d$, the bottom labels $e,f,g,h$ must make each side face sum to $18$. The side equations force \[e+f=c+d,\quad f+g=a+d,\quad g+h=a+b,\quad h+e=b+c.\] Checking the eight possible top-face sets gives $16,16,16,24,24,16,16,16$ fixed-cube arrangements respectively, for a total of $144$."),("Remove rotations",r"The problem considers rotations of the cube to be the same. A labeled cube with eight distinct labels has no nontrivial rotational symmetry, so each arrangement is counted exactly $24$ times among the fixed-position labelings."),("Divide",r"The number of different arrangements is \[\frac{144}{24}=6.\]"),("Conclude",r"The answer is $\boxed{6}$."),],
19:[("Put the rectangle on coordinates",r"Let $B=(0,0)$, $C=(3,0)$, $A=(0,6)$, and $D=(3,6)$. Then $E=(1,0)$ and $F=(2,0)$ because $BE=EF=FC$."),("Write the diagonal",r"The diagonal $BD$ goes from $(0,0)$ to $(3,6)$, so its equation is $y=2x$. Distances along this diagonal are proportional to the $x$-coordinate."),("Find P",r"Line $AE$ passes through $(0,6)$ and $(1,0)$, so $y=6-6x$. Intersecting with $y=2x$ gives $2x=6-6x$, so $x=\frac34$."),("Find Q",r"Line $AF$ passes through $(0,6)$ and $(2,0)$, so $y=6-3x$. Intersecting with $y=2x$ gives $2x=6-3x$, so $x=\frac65$."),("Convert to a ratio",r"Along $BD$, the relevant $x$-coordinates are $0$, $\frac34$, $\frac65$, and $3$. Thus \[BP:PQ:QD=\frac34:\left(\frac65-\frac34\right):\left(3-\frac65\right)=\frac34:\frac9{20}:\frac95.\] Multiplying by $20$ gives $15:9:36=5:3:12$."),("Conclude",r"Thus $r+s+t=5+3+12=\boxed{20}$."),],
20:[("Interpret a term in the expansion",r"A term from $(a+b+c+d+1)^N$ is determined by the exponents of $a,b,c,d$, and the remaining exponent of $1$. The term includes all four variables when the exponents of $a,b,c,d$ are all positive."),("Convert to a counting problem",r"Let those positive exponents be $x_1,x_2,x_3,x_4$. Since some factors may contribute the $1$, we need \[x_1+x_2+x_3+x_4\le N,\quad x_i\ge1.\]"),("Remove the positivity condition",r"Set $y_i=x_i-1$. Then $y_i\ge0$ and \[y_1+y_2+y_3+y_4\le N-4.\]"),("Use stars and bars",r"The number of nonnegative quadruples with sum at most $N-4$ is \[\binom{N}{4}.\] This is a standard stars-and-bars result: add a slack variable for the unused degree."),("Find N",r"We need \[\binom{N}{4}=1001.\] Since \[\binom{14}{4}=\frac{14\cdot13\cdot12\cdot11}{24}=1001,\] we get $N=14$."),("Conclude",r"The answer is $\boxed{14}$."),],
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
    if n in {10,17} and notes == "题面包含图形":
        notes = ""
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in {10} else notes
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
        if r["year"] == "2016" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {10},
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
        + "- Answer verification source: AoPS 2016 AMC 10A Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + ("本批无跳过题。\n" if not SKIPPED else "本批跳过题：\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n")
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()












































