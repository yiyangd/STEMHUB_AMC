import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 116
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2020_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16,17,18,20}
SKIPPED = ["2020 AMC 10A Problem 19 skipped: path counting depends on the missing dodecahedron face adjacency figure."]
BATCH_LABEL = "2020 AMC 10A Problems 11-18,20"
NEXT_START = "2020 AMC 10A Problem 21"

ANS={11:("C","1976.5"),12:("C","96"),13:("B",r"\frac58"),14:("D","440"),15:("E","23"),16:("B","0.4"),17:("E","5100"),18:("C","96"),20:("D","360")}

OV={
11:(r"What is the median of the following list of $4040$ numbers? \[1,2,3,\ldots,2020,1^2,2^2,3^2,\ldots,2020^2\]",[("A","1974.5"),("B","1975.5"),("C","1976.5"),("D","1977.5"),("E","1978.5")]),
12:(r"Triangle $AMC$ is isosceles with $AM=AC$. Medians $MV$ and $CU$ are perpendicular to each other, and $MV=CU=12$. What is the area of $\triangle AMC$?",[("A","48"),("B","72"),("C","96"),("D","144"),("E","192")]),
13:(r"A frog sitting at $(1,2)$ begins random unit jumps parallel to the coordinate axes. Each direction is chosen independently at random. The sequence ends when the frog reaches a side of the square with vertices $(0,0),(0,4),(4,4),(4,0)$. What is the probability that the sequence ends on a vertical side?",[("A",r"$\frac12$"),("B",r"$\frac58$"),("C",r"$\frac23$"),("D",r"$\frac34$"),("E",r"$\frac78$")]),
14:(r"Real numbers $x$ and $y$ satisfy $x+y=4$ and $xy=-2$. What is the value of \[\frac{x^3}{y^2}+\frac{y^3}{x^2}+x+y?\]",[("A","360"),("B","400"),("C","420"),("D","440"),("E","480")]),
15:(r"A positive integer divisor of $12!$ is chosen at random. The probability that the divisor chosen is a perfect square can be expressed as $\frac mn$, where $m$ and $n$ are relatively prime positive integers. What is $m+n$?",[("A","3"),("B","5"),("C","12"),("D","18"),("E","23")]),
16:(r"A point is chosen at random within the square with vertices $(0,0),(2020,0),(2020,2020),(0,2020)$. The probability that the point is within $d$ units of a lattice point is $\frac12$. What is $d$ to the nearest tenth?",[("A","0.3"),("B","0.4"),("C","0.5"),("D","0.6"),("E","0.7")]),
17:(r"Define \[P(x)=(x-1^2)(x-2^2)\cdots(x-100^2).\] How many integers $n$ are there such that $P(n)\le0$?",[("A","4900"),("B","4950"),("C","5000"),("D","5050"),("E","5100")]),
18:(r"Let $(a,b,c,d)$ be an ordered quadruple of not necessarily distinct integers, each in $\{0,1,2,3\}$. For how many such quadruples is $ad-bc$ odd?",[("A","48"),("B","64"),("C","96"),("D","128"),("E","192")]),
20:(r"Quadrilateral $ABCD$ satisfies $\angle ABC=\angle ACD=90^\circ$, $AC=20$, and $CD=30$. Diagonals $AC$ and $BD$ intersect at $E$, and $AE=5$. What is the area of quadrilateral $ABCD$?",[("A","330"),("B","340"),("C","350"),("D","360"),("E","370")]),
}

KEY_OVERRIDES={11:"Locate the two middle entries after merging numbers and squares.",12:"Use coordinates for the perpendicular equal medians.",13:"Solve a small system of harmonic probability equations.",14:"Use symmetric sums of powers.",15:"Count square divisors by even prime exponents.",16:"Use one unit cell and area of small disks around lattice points.",17:"Count sign intervals between consecutive square roots.",18:"Work modulo 2 and count invertible binary matrices.",20:"Use coordinates on diagonal AC and the circle with diameter AC."}

SOL={
11:[("Understand the middle positions",r"There are $4040$ numbers, so the median is the average of the $2020$th and $2021$st numbers after sorting."),("Count small squares",r"The list contains the integers $1,2,\ldots,2020$ and the squares $1^2,2^2,\ldots,2020^2$. Most large squares are far above $2020$, so near the middle we compare integers with the first few squares."),("Count numbers at most 1976",r"All integers $1$ through $1976$ contribute $1976$ numbers. The squares at most $1976$ are $1^2$ through $44^2$, contributing $44$ more. Thus there are \[1976+44=2020\] numbers at most $1976$."),("Find the next number",r"The next integer is $1977$, while the next square is $45^2=2025$. So the $2021$st number is $1977$."),("Compute the median",r"The median is \[\frac{1976+1977}{2}=1976.5.\]"),("Conclude",r"The answer is $\boxed{1976.5}$."),],
12:[("Set coordinates",r"Let the base be $MC=b$ on the $x$-axis, with $M=(-b/2,0)$, $C=(b/2,0)$, and $A=(0,h)$. This uses the symmetry from $AM=AC$."),("Write the median vectors",r"The midpoint of $AC$ is $V=(b/4,h/2)$, so \[\overrightarrow{MV}=\left(\frac{3b}{4},\frac{h}{2}\right).\] The midpoint of $AM$ is $U=(-b/4,h/2)$, so \[\overrightarrow{CU}=\left(-\frac{3b}{4},\frac{h}{2}\right).\]"),("Use perpendicularity",r"The medians are perpendicular, so their dot product is $0$: \[-\frac{9b^2}{16}+\frac{h^2}{4}=0.\] Hence \[h^2=\frac{9b^2}{4}.\]"),("Use the median length",r"Since $MV=12$, \[\left(\frac{3b}{4}\right)^2+\left(\frac{h}{2}\right)^2=144.\] Substituting $h^2=\frac{9b^2}{4}$ gives \[\frac{9b^2}{16}+\frac{9b^2}{16}=144,\] so $b^2=128$."),("Find the area",r"The area is \[\frac12 bh.\] Since $h=\frac{3b}{2}$, the area is \[\frac12 b\cdot\frac{3b}{2}=\frac{3b^2}{4}=\frac{3\cdot128}{4}=96.\]"),("Conclude",r"The answer is $\boxed{96}$."),],
13:[("Turn the random walk into probabilities",r"Let $p(x,y)$ be the probability that the frog eventually exits through a vertical side when starting at $(x,y)$."),("Use symmetry",r"By symmetry about the horizontal midline, let \[a=p(1,2),\quad b=p(1,1)=p(1,3),\quad c=p(2,2),\quad d=p(2,1)=p(2,3).\] Also $p=1$ on vertical sides and $p=0$ on horizontal sides."),("Write averaging equations",r"At each interior point, the probability is the average of the four neighboring probabilities. Thus \[a=\frac{1+c+2b}{4},\quad b=\frac{1+d+a}{4},\quad c=\frac{a+d}{2},\quad d=\frac{2b+c}{4}.\]"),("Solve the small system",r"Solving gives \[a=\frac58,\quad b=\frac12,\quad c=\frac12,\quad d=\frac38.\]"),("Use the starting point",r"The frog starts at $(1,2)$, so the desired probability is $a$."),("Conclude",r"The answer is $\boxed{\frac58}$."),],
14:[("Combine the fractional terms",r"The expression is \[\frac{x^3}{y^2}+\frac{y^3}{x^2}+x+y.\] Since $x+y=4$, the last part is already $4$."),("Use a common denominator",r"\[\frac{x^3}{y^2}+\frac{y^3}{x^2}=\frac{x^5+y^5}{x^2y^2}.\] Because $xy=-2$, the denominator is \[x^2y^2=4.\]"),("Find power sums",r"Let $S_k=x^k+y^k$. With $x+y=4$ and $xy=-2$, the recurrence is \[S_k=4S_{k-1}+2S_{k-2}.\]"),("Compute S5",r"We get \[S_1=4,\quad S_2=20,\quad S_3=88,\quad S_4=392,\quad S_5=1744.\]"),("Finish",r"The expression is \[\frac{1744}{4}+4=436+4=440.\]"),("Conclude",r"The answer is $\boxed{440}$."),],
15:[("Factor 12 factorial",r"The prime factorization is \[12!=2^{10}3^5 5^2 7^1 11^1.\]"),("Count all divisors",r"The total number of positive divisors is \[(10+1)(5+1)(2+1)(1+1)(1+1)=792.\]"),("Count square divisors",r"A divisor is a perfect square exactly when every prime exponent is even. The choices are $6$ even exponents for $2$, $3$ for $3$, $2$ for $5$, and only $1$ each for $7$ and $11$."),("Find the probability",r"The number of square divisors is \[6\cdot3\cdot2\cdot1\cdot1=36.\] So the probability is \[\frac{36}{792}=\frac1{22}.\]"),("Conclude",r"Thus $m+n=1+22=\boxed{23}$."),],
16:[("Use one unit square",r"Because lattice points repeat every unit, the large $2020$ by $2020$ square behaves like many unit squares. Boundary effects do not change the probability."),("Find the area near lattice points",r"In one unit square, being within distance $d$ of a lattice point gives four quarter-circles of radius $d$, one at each corner. For $d<\frac12$, their total area is \[\pi d^2.\]"),("Set the probability",r"The probability is this area inside a unit square, so \[\pi d^2=\frac12.\]"),("Solve",r"\[d=\frac{1}{\sqrt{2\pi}}\approx0.399.\]"),("Round",r"To the nearest tenth, $d=0.4$."),("Conclude",r"The answer is $\boxed{0.4}$."),],
17:[("Understand the sign changes",r"The roots are $1^2,2^2,\ldots,100^2$. At each root, $P(n)=0$, so all $100$ square values count."),("Look between consecutive squares",r"For $j^2<n<(j+1)^2$, exactly $100-j$ factors are negative. The product is negative when $100-j$ is odd, which happens when $j$ is odd."),("Count integers in a negative interval",r"Between $j^2$ and $(j+1)^2$, excluding endpoints, there are \[(j+1)^2-j^2-1=2j\] integers."),("Sum over odd j",r"The odd values $j=1,3,\ldots,99$ give \[2(1+3+\cdots+99)=2\cdot2500=5000\] negative integer inputs."),("Add the roots",r"Including the $100$ roots where $P(n)=0$, the total is \[5000+100=5100.\]"),("Conclude",r"The answer is $\boxed{5100}$."),],
18:[("Reduce to parity",r"The expression $ad-bc$ is odd only depends on whether $a,b,c,d$ are odd or even."),("View it as a determinant",r"Modulo $2$, subtraction is the same as addition, and $ad-bc$ is the determinant of the matrix \[\begin{pmatrix}a&b\\ c&d\end{pmatrix}.\] We need this determinant to be $1$ modulo $2$."),("Count binary matrices",r"Over the field with two elements, a $2$ by $2$ matrix has determinant $1$ exactly when its two rows are nonzero and different. There are $3$ choices for the first nonzero row and $2$ choices for the second row, for $6$ parity patterns."),("Lift to actual values",r"Each parity choice has $2$ actual values in $\{0,1,2,3\}$: one even and one odd. Thus each parity pattern corresponds to $2^4=16$ quadruples."),("Multiply",r"The total is \[6\cdot16=96.\]"),("Conclude",r"The answer is $\boxed{96}$."),],
20:[("Place AC on an axis",r"Set $A=(0,0)$ and $C=(20,0)$. Since $AE=5$, point $E=(5,0)$."),("Place D",r"Because $\angle ACD=90^\circ$ and $CD=30$, take \[D=(20,30).\] Then diagonal $BD$ passes through $E$."),("Find the line BD",r"The line through $E=(5,0)$ and $D=(20,30)$ has slope $2$, so \[BD:\ y=2(x-5).\]"),("Use the right angle at B",r"The condition $\angle ABC=90^\circ$ means $B$ lies on the circle with diameter $AC$. That circle is \[(x-10)^2+y^2=100.\] Intersecting with $y=2(x-5)$ gives $(2,-6)$ and $(10,10)$."),("Choose the correct intersection",r"Since $E$ is the intersection of diagonals, $B$ and $D$ must lie on opposite sides of $E$ along line $BD$. Thus $B=(2,-6)$."),("Compute area",r"Using coordinates for $A(0,0)$, $B(2,-6)$, $C(20,0)$, and $D(20,30)$, the shoelace formula gives area $360$."),("Conclude",r"The answer is $\boxed{360}$."),],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if notes == "题面包含图形" else notes
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
        if r["year"] == "2020" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2020 AMC 10A Answer Key\n\n"
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












































