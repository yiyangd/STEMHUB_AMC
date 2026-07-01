import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 110
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2019_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,17,18,19,20}
SKIPPED = ["2019 AMC 10A Problem 16 skipped: shaded region depends on the missing 13-circle figure."]
BATCH_LABEL = "2019 AMC 10A Problems 11-15,17-20"
NEXT_START = "2019 AMC 10A Problem 21"

ANS={11:("C","37"),12:("E",r"d<\mu<M"),13:("D","110"),14:("D","19"),15:("E","8078"),17:("D","1260"),18:("D","16"),19:("B","2018"),20:("B",r"\frac1{14}")}

OV={
11:(r"How many positive integer divisors of $201^9$ are perfect squares or perfect cubes, or both?",[("A","32"),("B","36"),("C","37"),("D","39"),("E","41")]),
12:(r"Melanie computes the mean $\mu$, the median $M$, and the modes of the $365$ values that are the dates in the months of $2019$. Thus her data consist of twelve $1$s, twelve $2$s, $\ldots$, twelve $28$s, eleven $29$s, eleven $30$s, and seven $31$s. Let $d$ be the median of the modes. Which statement is true?",[("A",r"$\mu<d<M$"),("B",r"$M<d<\mu$"),("C",r"$d=M=\mu$"),("D",r"$d<M<\mu$"),("E",r"$d<\mu<M$")]),
13:(r"Let $\triangle ABC$ be an isosceles triangle with $BC=AC$ and $\angle ACB=40^\circ$. Construct the circle with diameter $BC$, and let $D$ and $E$ be the other intersection points of the circle with sides $AC$ and $AB$, respectively. Let $F$ be the intersection of the diagonals of quadrilateral $BCDE$. What is the degree measure of $\angle BFC$?",[("A","90"),("B","100"),("C","105"),("D","110"),("E","120")]),
14:(r"For a set of four distinct lines in a plane, there are exactly $N$ distinct points that lie on two or more of the lines. What is the sum of all possible values of $N$?",[("A","14"),("B","16"),("C","18"),("D","19"),("E","21")]),
15:(r"A sequence is defined recursively by $a_1=1$, $a_2=\frac37$, and \[a_n=\frac{a_{n-2}a_{n-1}}{2a_{n-2}-a_{n-1}}\] for all $n\ge3$. Then $a_{2019}$ can be written as $\frac pq$, where $p$ and $q$ are relatively prime positive integers. What is $p+q$?",[("A","2020"),("B","4039"),("C","6057"),("D","6061"),("E","8078")]),
17:(r"A child builds towers using identically shaped cubes of different colors. How many different towers with a height of $8$ cubes can the child build with $2$ red cubes, $3$ blue cubes, and $4$ green cubes? One cube will be left out.",[("A","24"),("B","288"),("C","312"),("D","1260"),("E","40320")]),
18:(r"For some positive integer $k$, the repeating base-$k$ representation of the base-ten fraction $\frac7{51}$ is $0.\overline{23}_k=0.232323\ldots_k$. What is $k$?",[("A","13"),("B","14"),("C","15"),("D","16"),("E","17")]),
19:(r"What is the least possible value of $(x+1)(x+2)(x+3)(x+4)+2019$, where $x$ is a real number?",[("A","2017"),("B","2018"),("C","2019"),("D","2020"),("E","2021")]),
20:(r"The numbers $1,2,\ldots,9$ are randomly placed into the $9$ squares of a $3\times3$ grid. Each square gets one number, and each number is used once. What is the probability that the sum of the numbers in each row and each column is odd?",[("A",r"$\frac1{21}$"),("B",r"$\frac1{14}$"),("C",r"$\frac5{63}$"),("D",r"$\frac2{21}$"),("E",r"$\frac17$")]),
}

KEY_OVERRIDES={11:"Count exponent pairs using inclusion-exclusion for square and cube divisors.",12:"Compute mode median, data median, and mean separately.",13:"Use Thales' theorem to turn circle-diameter intersections into right angles.",14:"List possible intersection patterns of four lines.",15:"Take reciprocals to turn the recurrence into an arithmetic sequence.",17:"Split into cases according to which cube color is left out.",18:"Convert a repeating base-$k$ decimal into a fraction.",19:"Center the four consecutive factors around one variable.",20:"Reduce the condition to parity patterns in a $3\times3$ grid."}

SOL={
11:[("Factor the number first",r"The base is \[201=3\cdot67,\] so \[201^9=3^9\cdot67^9.\] Every divisor has the form $3^a67^b$, where $0\le a,b\le9$."),("Count square divisors",r"A divisor is a perfect square when both exponents are even. The possible exponents are \[0,2,4,6,8,\] giving $5$ choices for each prime. So there are \[5\cdot5=25\] square divisors."),("Count cube divisors",r"A divisor is a perfect cube when both exponents are multiples of $3$. The possible exponents are \[0,3,6,9,\] giving $4$ choices for each prime. So there are \[4\cdot4=16\] cube divisors."),("Subtract overlap",r"A divisor counted in both groups must have both exponents divisible by $6$. The possible exponents are $0$ and $6$, so the overlap has \[2\cdot2=4\] divisors."),("Use inclusion-exclusion",r"The total number that are squares or cubes is \[25+16-4=37.\]"),("Conclude",r"The answer is $\boxed{37}$."),],
12:[("Find the modes first",r"The most frequent dates are $1,2,\ldots,28$, each appearing $12$ times. Therefore the modes are the numbers $1$ through $28$."),("Find d",r"The median of the modes is the average of the $14$th and $15$th numbers in $1,2,\ldots,28$: \[d=\frac{14+15}{2}=14.5.\]"),("Find the data median M",r"There are $365$ data values, so the median is the $183$rd value. The dates $1$ through $15$ account for $15\cdot12=180$ values, so the $183$rd value is $16$. Thus $M=16$."),("Estimate the mean",r"The total of all dates in 2019 is \[7(1+\cdots+31)+4(1+\cdots+30)+(1+\cdots+28)=5738.\] Hence \[\mu=\frac{5738}{365}\approx15.72.\]"),("Compare",r"We have \[14.5<15.72<16,\] so \[d<\mu<M.\]"),("Conclude",r"The answer is $\boxed{d<\mu<M}$."),],
13:[("Use the circle with diameter BC",r"Any angle subtending diameter $BC$ is a right angle. Since $D$ and $E$ lie on the circle with diameter $BC$, we get \[\angle BDC=90^\circ,\qquad \angle BEC=90^\circ.\]"),("Relate the right angles to the triangle sides",r"Point $D$ lies on $AC$, so $BD\perp AC$. Point $E$ lies on $AB$, so $CE\perp AB$."),("Recognize the diagonals",r"In quadrilateral $BCDE$, the diagonals are $BD$ and $CE$. Their intersection is $F$, so $\angle BFC$ is the angle between the two altitudes $BD$ and $CE$."),("Find the base angle of ABC",r"Because $AC=BC$ and $\angle C=40^\circ$, the base angles are \[\angle A=\angle B=\frac{180^\circ-40^\circ}{2}=70^\circ.\]"),("Convert to the angle at F",r"The angle between lines perpendicular to $AC$ and $AB$ is supplementary to $\angle A$ at this intersection, so \[\angle BFC=180^\circ-70^\circ=110^\circ.\]"),("Conclude",r"The answer is $\boxed{110^\circ}$."),],
14:[("Start with the maximum",r"With four lines and no parallel lines or three-line concurrency, every pair intersects in a different point. This gives \[\binom42=6\] points."),("List ways to reduce intersections",r"Parallel lines remove intersection points, while three or four concurrent lines merge several pairwise intersections into one point."),("Find possible values",r"The possible values are: $0$ if all four lines are parallel; $1$ if all four are concurrent; $3$ if three are parallel and the fourth crosses them; $4$ if three are concurrent and the fourth crosses them, or if there are two pairs of parallel lines; $5$ if exactly one pair is parallel; and $6$ in general position."),("Notice what is missing",r"There is no way to get exactly $2$ distinct intersection points from four distinct lines. The intersection pattern always creates one of the listed values."),("Add",r"The sum is \[0+1+3+4+5+6=19.\]"),("Conclude",r"The answer is $\boxed{19}$."),],
15:[("Look for a simpler sequence",r"The recurrence is complicated because it uses fractions of previous terms. A natural move is to take reciprocals."),("Take reciprocals",r"From \[a_n=\frac{a_{n-2}a_{n-1}}{2a_{n-2}-a_{n-1}},\] we get \[\frac1{a_n}=\frac{2a_{n-2}-a_{n-1}}{a_{n-2}a_{n-1}}=\frac2{a_{n-1}}-\frac1{a_{n-2}}.\]"),("Define b_n",r"Let $b_n=\frac1{a_n}$. Then \[b_n=2b_{n-1}-b_{n-2},\] which means the differences $b_n-b_{n-1}$ are constant."),("Find the arithmetic sequence",r"We have \[b_1=1,\qquad b_2=\frac73.\] The common difference is \[\frac73-1=\frac43.\] Thus \[b_n=1+(n-1)\frac43.\]"),("Compute the target term",r"\[b_{2019}=1+2018\cdot\frac43=\frac{8075}{3}.\] Therefore \[a_{2019}=\frac3{8075}.\]"),("Conclude",r"Thus $p+q=3+8075=\boxed{8078}$."),],
17:[("Use cases based on the omitted cube",r"There are $2+3+4=9$ cubes available, but a tower uses $8$, so exactly one cube is left out. The count depends on which color is omitted."),("Leave out a red cube",r"Then the tower uses $1$ red, $3$ blue, and $4$ green cubes. The number of arrangements is \[\frac{8!}{1!3!4!}=280.\]"),("Leave out a blue cube",r"Then the tower uses $2$ red, $2$ blue, and $4$ green cubes, giving \[\frac{8!}{2!2!4!}=420.\]"),("Leave out a green cube",r"Then the tower uses $2$ red, $3$ blue, and $3$ green cubes, giving \[\frac{8!}{2!3!3!}=560.\]"),("Add cases",r"The total number of towers is \[280+420+560=1260.\]"),("Conclude",r"The answer is $\boxed{1260}$."),],
18:[("Convert the repeating base-k decimal",r"Let \[x=0.\overline{23}_k.\] Multiplying by $k^2$ shifts the repeating block two places: \[k^2x=23.\overline{23}_k.\]"),("Subtract to remove the repetition",r"Thus \[(k^2-1)x=23_k.\] In base ten, $23_k=2k+3$, so \[x=\frac{2k+3}{k^2-1}.\]"),("Use the given fraction",r"The problem says \[x=\frac7{51},\] so \[\frac{2k+3}{k^2-1}=\frac7{51}.\]"),("Solve",r"Cross-multiplying gives \[51(2k+3)=7(k^2-1).\] This simplifies to \[7k^2-102k-160=0.\]"),("Choose the positive integer root",r"Testing the answer choices or factoring gives $k=16$."),("Conclude",r"The answer is $\boxed{16}$."),],
19:[("Center the four factors",r"The factors $x+1,x+2,x+3,x+4$ are symmetric around $x+\frac52$. Let \[y=x+\frac52.\]"),("Rewrite in pairs",r"Then \[(x+1)(x+4)=\left(y-\frac32\right)\left(y+\frac32\right)=y^2-\frac94,\] and \[(x+2)(x+3)=\left(y-\frac12\right)\left(y+\frac12\right)=y^2-\frac14.\]"),("Use z=y^2",r"Let $z=y^2$, where $z\ge0$. The product becomes \[\left(z-\frac94\right)\left(z-\frac14\right)=z^2-\frac52z+\frac9{16}.\]"),("Minimize the quadratic",r"This upward-opening quadratic has vertex at \[z=\frac{5}{4}.\] The minimum product is \[\left(\frac54\right)^2-\frac52\cdot\frac54+\frac9{16}=-1.\]"),("Add 2019",r"The least possible value of the full expression is \[-1+2019=2018.\]"),("Conclude",r"The answer is $\boxed{2018}$."),],
20:[("Reduce to parity",r"Only odd or even matters. The five odd numbers are $1,3,5,7,9$, and the four even numbers are $2,4,6,8$."),("Count parity patterns",r"Once the five positions for odd numbers are chosen, the actual odd numbers can be arranged in $5!$ ways and the evens in $4!$ ways. These factors will cancel, so we count valid placements of five odd positions among nine squares."),("State the row and column condition",r"A row or column has odd sum exactly when it contains an odd number of odd entries. With five odd entries total, each row and each column must contain either $1$ or $3$ odd entries."),("Count valid patterns",r"The valid patterns have one row containing $3$ odd entries, and the other two odd entries must be placed in the same column. There are $3$ choices for the full odd row and $3$ choices for that column, giving \[3\cdot3=9\] valid parity patterns."),("Compute probability",r"There are \[\binom95=126\] ways to choose the five odd positions. Therefore the probability is \[\frac9{126}=\frac1{14}.\]"),("Conclude",r"The answer is $\boxed{\frac1{14}}$."),],
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
        if r["year"] == "2019" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2019 AMC 10A Answer Key\n\n"
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












































