import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 95
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2016_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16,17,18,19,20}
SKIPPED = []
BATCH_LABEL = "2016 AMC 10B Problems 11-20"
NEXT_START = "2016 AMC 10B Problem 21"

ANS={11:("B","336"),12:("D","0.7"),13:("D","100"),14:("D","50"),15:("C","7"),16:("E","4"),17:("D","729"),18:("E","7"),19:("D",r"\frac{10}{91}"),20:("C",r"\sqrt{13}")}

OV={
11:(r"Carl decided to fence in his rectangular garden. He bought $20$ fence posts, placed one on each of the four corners, and spaced out the rest evenly along the edges of the garden, leaving exactly $4$ yards between neighboring posts. The longer side of his garden, including the corners, has twice as many posts as the shorter side, including the corners. What is the area, in square yards, of Carl's garden?",[("A","256"),("B","336"),("C","384"),("D","448"),("E","512")]),
12:(r"Two different numbers are selected at random from $\{1,2,3,4,5\}$ and multiplied together. What is the probability that the product is even?",[("A","0.2"),("B","0.4"),("C","0.5"),("D","0.7"),("E","0.8")]),
13:(r"At Megapolis Hospital one year, multiple-birth statistics were as follows: sets of twins, triplets, and quadruplets accounted for $1000$ of the babies born. There were four times as many sets of triplets as sets of quadruplets, and there were three times as many sets of twins as sets of triplets. How many of these $1000$ babies were in sets of quadruplets?",[("A","25"),("B","40"),("C","64"),("D","100"),("E","160")]),
14:(r"How many squares whose sides are parallel to the axes and whose vertices have coordinates that are integers lie entirely within the region bounded by the line $y=\pi x$, the line $y=-0.1$, and the line $x=5.1$?",[("A","30"),("B","41"),("C","45"),("D","50"),("E","57")]),
15:(r"All the numbers $1,2,3,4,5,6,7,8,9$ are written in a $3\times3$ array of squares, one number in each square, in such a way that if two numbers are consecutive then they occupy squares that share an edge. The numbers in the four corners add up to $18$. What is the number in the center?",[("A","5"),("B","6"),("C","7"),("D","8"),("E","9")]),
16:(r"The sum of an infinite geometric series is a positive number $S$, and the second term in the series is $1$. What is the smallest possible value of $S$?",[("A",r"$\frac{1+\sqrt5}{2}$"),("B","2"),("C",r"$\sqrt5$"),("D","3"),("E","4")]),
17:(r"All the numbers $2,3,4,5,6,7$ are assigned to the six faces of a cube, one number to each face. For each of the eight vertices of the cube, a product of three numbers is computed, where the three numbers are the numbers assigned to the three faces that include that vertex. What is the greatest possible value of the sum of these eight products?",[("A","312"),("B","343"),("C","625"),("D","729"),("E","1680")]),
18:(r"In how many ways can $345$ be written as the sum of an increasing sequence of two or more consecutive positive integers?",[("A","1"),("B","3"),("C","5"),("D","6"),("E","7")]),
19:(r"Rectangle $ABCD$ has $AB=5$ and $BC=4$. Point $E$ lies on $AB$ so that $EB=1$, point $G$ lies on $BC$ so that $CG=1$, and point $F$ lies on $CD$ so that $DF=2$. Segments $AG$ and $AC$ intersect $EF$ at $Q$ and $P$, respectively. What is the value of $\frac{PQ}{EF}$?",[("A",r"$\frac{\sqrt{13}}{16}$"),("B",r"$\frac{\sqrt2}{13}$"),("C",r"$\frac9{82}$"),("D",r"$\frac{10}{91}$"),("E",r"$\frac19$")]),
20:(r"A dilation of the plane, that is, a size transformation with a positive scale factor, sends the circle of radius $2$ centered at $A(2,2)$ to the circle of radius $3$ centered at $A'(5,6)$. What distance does the origin $O(0,0)$ move under this transformation?",[("A","0"),("B","3"),("C",r"$\sqrt{13}$"),("D","4"),("E","5")]),
}

KEY_OVERRIDES={11:"Convert posts into intervals along each side.",12:"Count the complement: products that are odd.",13:"Track sets versus babies carefully.",14:"Count integer-coordinate squares by side length and left edge.",15:"View consecutive entries as a Hamiltonian path on the grid.",16:"Optimize the sum formula for a geometric series.",17:"Pair opposite cube faces and maximize a product of pair sums.",18:"Use the formula for a consecutive integer sum.",19:"Use coordinates and line intersections, then compare parameters on EF.",20:"Find the center and scale factor of the dilation."}

SOL={
11:[("Count posts by side type",r"Let the shorter side have $s$ posts including its two corner posts. Then the longer side has $2s$ posts including its corners."),("Avoid double-counting corners",r"If we add the post counts from all four sides, the four corner posts are each counted twice. Thus the total number of distinct posts is \[2s+2(2s)-4=6s-4.\]"),("Use the total number of posts",r"Since Carl bought $20$ posts, \[6s-4=20,\] so $s=4$. The shorter side has $4$ posts and the longer side has $8$ posts."),("Convert posts to lengths",r"A side with $k$ posts has $k-1$ intervals between posts. Since neighboring posts are $4$ yards apart, the shorter side is $(4-1)\cdot4=12$ yards and the longer side is $(8-1)\cdot4=28$ yards."),("Find the area",r"The area is \[12\cdot28=336.\]"),("Conclude",r"The answer is $\boxed{336}$."),],
12:[("Use the complement",r"The product is even unless both selected numbers are odd. It is easier to count odd products first."),("Count all pairs",r"There are \[\binom52=10\] ways to choose two different numbers from $\{1,2,3,4,5\}$."),("Count odd-product pairs",r"The odd numbers are $1,3,5$, so there are \[\binom32=3\] pairs whose product is odd."),("Find even-product pairs",r"Therefore $10-3=7$ pairs have even product."),("Convert to probability",r"The probability is \[\frac7{10}=0.7.\]"),("Conclude",r"The answer is $\boxed{0.7}$."),],
13:[("Track sets, not just babies",r"Let $q$ be the number of sets of quadruplets. Then there are $4q$ sets of triplets and $3(4q)=12q$ sets of twins."),("Convert sets to babies",r"The quadruplet sets contain $4q$ babies. The triplet sets contain $3(4q)=12q$ babies. The twin sets contain $2(12q)=24q$ babies."),("Use the total",r"Together these account for \[4q+12q+24q=40q\] babies. This equals $1000$, so $q=25$."),("Answer the actual question",r"The question asks for babies in sets of quadruplets, not the number of quadruplet sets. That number is $4q=100$."),("Conclude",r"The answer is $\boxed{100}$."),],
14:[("Describe a square by its lower-left corner",r"Let a square have side length $s$ and lower-left corner $(i,j)$, where $s$, $i$, and $j$ are integers. Since the square must lie above $y=-0.1$, we need $j\ge0$."),("Use the vertical boundary",r"The right side must be at or left of $x=5.1$. Since the right side has integer coordinate $i+s$, this means $i+s\le5$."),("Use the slanted boundary",r"The line $y=\pi x$ is increasing, so the most restrictive top corner is the upper-left corner $(i,j+s)$. We need \[j+s\le\pi i.\]"),("Count by side length",r"For $s=1$, valid $i$ values are $1,2,3,4$, giving $3+6+9+12=30$ choices for $j$. For $s=2$, valid $i$ values $1,2,3$ give $2+5+8=15$ choices. For $s=3$, valid $i$ values $1,2$ give $1+4=5$ choices. Larger $s$ gives none."),("Add",r"The total number of squares is \[30+15+5=50.\]"),("Conclude",r"The answer is $\boxed{50}$."),],
15:[("View the grid as a path",r"Because consecutive numbers must share an edge, the numbers $1$ through $9$ form a path through all nine squares of the $3\times3$ grid."),("Use a checkerboard coloring",r"Color the four corners and the center black, and the four edge-middle squares white. Any edge move changes color, so the path alternates colors."),("Place the odd numbers",r"A path of $9$ squares must visit $5$ squares of one color and $4$ of the other. Therefore the positions of $1,3,5,7,9$ must be exactly the five black squares: the four corners and the center."),("Use the corner sum",r"The odd numbers $1+3+5+7+9$ have sum $25$. The four corners sum to $18$, so the center must be \[25-18=7.\]"),("Conclude",r"The number in the center is $\boxed{7}$."),],
16:[("Write the geometric series",r"Let the first term be $a$ and the common ratio be $r$. Since the second term is $1$, we have $ar=1$, so $a=\frac1r$."),("Use the sum formula",r"For an infinite geometric series, \[S=\frac{a}{1-r}=\frac{1}{r(1-r)}.\] The sum is positive and the series converges, so $0<r<1$."),("Minimize S by maximizing the denominator",r"To make $S$ as small as possible, maximize $r(1-r)$ for $0<r<1$."),("Maximize the quadratic",r"The expression $r(1-r)$ is largest at $r=\frac12$, where its value is $\frac14$."),("Compute the minimum",r"Thus the smallest possible sum is \[S=\frac{1}{1/4}=4.\]"),("Conclude",r"The answer is $\boxed{4}$."),],
17:[("Pair opposite faces",r"At each vertex of a cube, one face from each of three opposite-face pairs meets. If the opposite pairs have sums $A$, $B$, and $C$, then the sum of the eight vertex products is $ABC$."),("Explain the product structure",r"This works because expanding $(\text{one pair sum})(\text{second pair sum})(\text{third pair sum})$ chooses one face label from each opposite pair, exactly matching the eight vertices."),("Choose the best pair sums",r"We must split $2,3,4,5,6,7$ into three pairs. Their total sum is $27$, so the product of the three pair sums is largest when the pair sums are as balanced as possible."),("Make the sums equal",r"We can pair the numbers as $(2,7)$, $(3,6)$, and $(4,5)$, giving pair sums $9$, $9$, and $9$."),("Compute",r"The greatest possible sum of the eight products is \[9\cdot9\cdot9=729.\]"),("Conclude",r"The answer is $\boxed{729}$."),],
18:[("Use the formula for consecutive sums",r"Suppose the sequence has length $k\ge2$ and first term $a$. Then \[345=a+(a+1)+\cdots+(a+k-1)=\frac{k(2a+k-1)}2.\]"),("Solve for the first term",r"Rearranging gives \[2a=\frac{690}{k}-k+1.\] Thus $k$ must divide $690$, and the right side must be a positive even integer."),("Test possible lengths",r"The valid lengths are \[k=2,3,5,6,10,15,23.\] These give positive integer first terms $172,114,67,55,30,16,4$, respectively."),("Understand why this list is complete",r"Any longer sequence would have too large a minimum sum, and any valid length must divide $690$, so checking these divisors covers all possibilities."),("Count",r"There are $7$ valid lengths, hence $7$ representations."),("Conclude",r"The answer is $\boxed{7}$."),],
19:[("Put the rectangle on coordinates",r"Let $A=(0,4)$, $B=(5,4)$, $C=(5,0)$, and $D=(0,0)$. Then $E=(4,4)$, $G=(5,1)$, and $F=(2,0)$."),("Parametrize EF",r"Every point on $EF$ can be written as \[E+u(F-E)=(4-2u,4-4u),\quad 0\le u\le1.\] Distances along $EF$ are proportional to changes in $u$."),("Find P on AC",r"Line $AC$ goes from $(0,4)$ to $(5,0)$. Solving its intersection with $EF$ gives $u=\frac47$ for point $P$."),("Find Q on AG",r"Line $AG$ goes from $(0,4)$ to $(5,1)$. Solving its intersection with $EF$ gives $u=\frac6{13}$ for point $Q$."),("Compare the positions on EF",r"Since both points lie on the same segment $EF$, \[\frac{PQ}{EF}=\left|\frac47-\frac6{13}\right|=\left|\frac{52-42}{91}\right|=\frac{10}{91}.\]"),("Conclude",r"The answer is $\boxed{\frac{10}{91}}$."),],
20:[("Identify the scale factor",r"The circle radius changes from $2$ to $3$, so the dilation has scale factor \[k=\frac32.\]"),("Use the center of dilation",r"Let the center of dilation be $C$. A point $X$ maps to $C+k(X-C)$. Since $A=(2,2)$ maps to $A'=(5,6)$, \[A'=C+\frac32(A-C).\]"),("Solve for C",r"Rearranging gives \[A'=\frac32A-\frac12C,\] so \[C=3A-2A'.\] Therefore \[C=3(2,2)-2(5,6)=(-4,-6).\]"),("Map the origin",r"The origin maps to \[C+\frac32(O-C)=C-\frac32C=-\frac12C=(2,3).\]"),("Find the movement distance",r"The origin moves from $(0,0)$ to $(2,3)$, a distance \[\sqrt{2^2+3^2}=\sqrt{13}.\]"),("Conclude",r"The answer is $\boxed{\sqrt{13}}$."),],
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
        if r["year"] == "2016" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2016 AMC 10B Answer Key\n\n"
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












































