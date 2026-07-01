import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 98
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2017_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16,17,18,19,20}
SKIPPED = []
BATCH_LABEL = "2017 AMC 10A Problems 11-20"
NEXT_START = "2017 AMC 10A Problem 21"

ANS={11:("D","20"),12:("E","three rays with a common endpoint"),13:("D","9"),14:("D","23%"),15:("C",r"\frac34"),16:("B","3"),17:("D","7"),18:("D","4"),19:("C","28"),20:("D","1239")}

OV={
11:(r"The region consisting of all points in three-dimensional space within $3$ units of line segment $AB$ has volume $216\pi$. What is the length $AB$?",[("A","6"),("B","12"),("C","18"),("D","20"),("E","24")]),
12:(r"Let $S$ be the set of points $(x,y)$ in the coordinate plane such that two of the three quantities $3$, $x+2$, and $y-4$ are equal and the third of the three quantities is no greater than this common value. Which of the following is a correct description of $S$?",[("A","a single point"),("B","two intersecting lines"),("C","three lines whose pairwise intersections are three distinct points"),("D","a triangle"),("E","three rays with a common endpoint")]),
13:(r"Define a sequence recursively by $F_0=0$, $F_1=1$, and $F_n$ is the remainder when $F_{n-1}+F_{n-2}$ is divided by $3$, for all $n\ge2$. Thus the sequence starts $0,1,1,2,0,2,\ldots$. What is $F_{2017}+F_{2018}+F_{2019}+F_{2020}+F_{2021}+F_{2022}+F_{2023}+F_{2024}$?",[("A","6"),("B","7"),("C","8"),("D","9"),("E","10")]),
14:(r"Every week Roger pays for a movie ticket and a soda out of his allowance. Last week, Roger's allowance was $A$ dollars. The cost of his movie ticket was $20\%$ of the difference between $A$ and the cost of his soda, while the cost of his soda was $5\%$ of the difference between $A$ and the cost of his movie ticket. To the nearest whole percent, what fraction of $A$ did Roger pay for his movie ticket and soda?",[("A","9%"),("B","19%"),("C","22%"),("D","23%"),("E","25%")]),
15:(r"Chloe chooses a real number uniformly at random from the interval $[0,2017]$. Independently, Laurent chooses a real number uniformly at random from the interval $[0,4034]$. What is the probability that Laurent's number is greater than Chloe's number?",[("A",r"$\frac12$"),("B",r"$\frac23$"),("C",r"$\frac34$"),("D",r"$\frac56$"),("E",r"$\frac78$")]),
16:(r"There are $10$ horses, named Horse $1$, Horse $2$, ..., Horse $10$. Horse $k$ runs one lap in exactly $k$ minutes. At time $0$ all the horses are together at the starting point. Let $T>0$ be the least time, in minutes, such that at least $5$ of the horses are again at the starting point. What is the sum of the digits of $T$?",[("A","2"),("B","3"),("C","4"),("D","5"),("E","6")]),
17:(r"Distinct points $P$, $Q$, $R$, $S$ lie on the circle $x^2+y^2=25$ and have integer coordinates. The distances $PQ$ and $RS$ are irrational numbers. What is the greatest possible value of the ratio $\frac{PQ}{RS}$?",[("A",r"$\sqrt3$"),("B",r"$\sqrt5$"),("C",r"$3\sqrt5$"),("D","7"),("E",r"$5\sqrt2$")]),
18:(r"Amelia has a coin that lands heads with probability $\frac13$, and Blaine has a coin that lands heads with probability $\frac25$. Amelia and Blaine alternately toss their coins until someone gets a head; the first one to get a head wins. All coin tosses are independent. Amelia goes first. The probability that Amelia wins is $\frac pq$, where $p$ and $q$ are relatively prime positive integers. What is $q-p$?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
19:(r"Alice refuses to sit next to either Bob or Carla. Derek refuses to sit next to Eric. How many ways are there for the five of them to sit in a row of $5$ chairs under these conditions?",[("A","12"),("B","16"),("C","28"),("D","32"),("E","40")]),
20:(r"Let $S(n)$ equal the sum of the digits of positive integer $n$. For example, $S(1507)=13$. For a particular positive integer $n$, $S(n)=1274$. Which of the following could be the value of $S(n+1)$?",[("A","1"),("B","3"),("C","12"),("D","1239"),("E","1265")]),
}

KEY_OVERRIDES={11:"Model the solid as a cylinder plus two hemispheres.",12:"Split into the three possible equal-pair cases.",13:"Find the period of the Fibonacci-like sequence modulo 3.",14:"Set up two linear equations for ticket and soda costs.",15:"Average the conditional probability over Chloe's choice.",16:"Find the smallest time divisible by at least five numbers from 1 to 10.",17:"List possible irrational distances between integer points on the circle.",18:"Use a recursive probability equation after both players miss.",19:"Use inclusion-exclusion on forbidden adjacent pairs.",20:"Adding 1 changes digit sum by 1 minus 9 times the number of trailing 9s."}

SOL={
11:[("Recognize the shape",r"All points within $3$ units of a line segment form a cylinder of radius $3$ around the segment, plus two hemispherical caps at the ends."),("Write the volume",r"If $AB=L$, the cylinder volume is \[\pi(3^2)L=9\pi L.\] The two hemispheres together make one sphere of radius $3$, with volume \[\frac43\pi(3^3)=36\pi.\]"),("Use the given volume",r"The total volume is \[9\pi L+36\pi=216\pi.\]"),("Solve",r"Divide by $9\pi$: \[L+4=24,\] so $L=20$."),("Conclude",r"The length $AB$ is $\boxed{20}$."),],
12:[("Compare the three quantities in cases",r"The three quantities are $3$, $x+2$, and $y-4$. We look at which two are equal, then impose that the third is no greater than the common value."),("Case 1: 3 equals x plus 2",r"If $3=x+2$, then $x=1$. The third quantity must satisfy $y-4\le3$, so $y\le7$. This is a vertical ray ending at $(1,7)$."),("Case 2: 3 equals y minus 4",r"If $3=y-4$, then $y=7$. The third quantity must satisfy $x+2\le3$, so $x\le1$. This is a horizontal ray ending at $(1,7)$."),("Case 3: x plus 2 equals y minus 4",r"If $x+2=y-4$, then $y=x+6$. The third quantity must satisfy $3\le x+2$, so $x\ge1$. This is a ray starting at $(1,7)$."),("Conclude",r"The set is three rays with common endpoint $(1,7)$, so the answer is $\boxed{\text{E}}$."),],
13:[("Generate the pattern",r"The sequence is Fibonacci-like modulo $3$. Starting from $0,1$, we get \[0,1,1,2,0,2,2,1,0,1,\ldots\]"),("Find the period",r"Once the pair $(0,1)$ appears again, the recursion repeats. This happens after $8$ terms, so the period is $8$."),("Locate the requested indices",r"Since $2016$ is divisible by $8$, the terms $F_{2017}$ through $F_{2024}$ correspond to one full period after $F_{2016}$."),("Sum one period",r"The period values are \[0,1,1,2,0,2,2,1,\] whose sum is $9$."),("Conclude",r"The requested sum is $\boxed{9}$."),],
14:[("Name the costs",r"Let $t$ be the ticket cost and $s$ be the soda cost. The problem gives \[t=0.20(A-s),\quad s=0.05(A-t).\]"),("Clear decimals",r"These become \[5t=A-s,\quad 20s=A-t.\] Equivalently, \[5t+s=A,\quad t+20s=A.\]"),("Relate ticket and soda",r"Subtracting the equations gives $4t=19s$, so $t=\frac{19}{4}s$."),("Find the total fraction",r"Substitute into $5t+s=A$: \[5\cdot\frac{19}{4}s+s=\frac{99}{4}s=A.\] Thus $s=\frac{4A}{99}$ and $t=\frac{19A}{99}$."),("Add and round",r"The total is \[t+s=\frac{23A}{99}\approx0.2323A,\] which is about $23\%$ of $A$."),("Conclude",r"The answer is $\boxed{23\%}$."),],
15:[("Condition on Chloe's number",r"Suppose Chloe chooses $c$, where $0\le c\le2017$. Laurent is uniform on $[0,4034]$, so the chance Laurent's number is greater than $c$ is \[\frac{4034-c}{4034}=1-\frac{c}{4034}.\]"),("Average over Chloe's interval",r"The average value of Chloe's number over $[0,2017]$ is $\frac{2017}{2}$."),("Compute the probability",r"Therefore the desired probability is \[1-\frac{2017/2}{4034}=1-\frac14=\frac34.\]"),("Check reasonableness",r"Laurent's interval is twice as long as Chloe's, so the probability should be greater than $\frac12$. The value $\frac34$ is reasonable."),("Conclude",r"The answer is $\boxed{\frac34}$."),],
16:[("Translate starting point into divisibility",r"Horse $k$ is back at the starting point exactly at times that are multiples of $k$."),("Restate the goal",r"We need the least positive integer $T$ that is divisible by at least five numbers from $1$ through $10$."),("Check times below 12",r"Before $12$, the best examples are $6$, $8$, and $10$. Each is divisible by only four numbers from $1$ through $10$: for example, $6$ is divisible by $1,2,3,6$."),("Test 12",r"At $T=12$, the divisors among $1$ through $10$ include \[1,2,3,4,6,\] so at least five horses are at the starting point."),("Sum digits",r"The least such time is $12$, and its digit sum is $1+2=3$."),("Conclude",r"The answer is $\boxed{3}$."),],
17:[("List the integer points idea",r"The integer points on $x^2+y^2=25$ include axis points such as $(5,0)$ and $(0,5)$, and the points from $3$-$4$-$5$ triangles such as $(3,4)$ and $(4,3)$ with all sign choices."),("Find the smallest irrational distance",r"The smallest possible nonzero squared distance between two distinct integer points is $1^2+1^2=2$, for example between $(3,4)$ and $(4,3)$. This gives irrational distance $\sqrt2$."),("Find the largest irrational distance",r"The diameter is $10$, but that distance is rational. Checking the farthest integer-point pairs that do not give a perfect-square distance gives squared distance $98$, for example between $(-3,-4)$ and $(4,3)$."),("Take the ratio",r"The greatest possible ratio is \[\frac{\sqrt{98}}{\sqrt2}=\sqrt{49}=7.\]"),("Conclude",r"The answer is $\boxed{7}$."),],
18:[("Let P be Amelia's win probability",r"Amelia can win immediately by tossing heads, which has probability $\frac13$."),("Handle the reset case",r"If Amelia tosses tails and then Blaine tosses tails, the game returns to the same situation. That probability is \[\frac23\cdot\frac35=\frac25.\]"),("Set up the equation",r"Therefore \[P=\frac13+\frac25P.\]"),("Solve",r"\[\frac35P=\frac13,\quad P=\frac59.\] Thus $p=5$ and $q=9$."),("Compute the requested value",r"$q-p=9-5=4$."),("Conclude",r"The answer is $\boxed{4}$."),],
19:[("Start with all arrangements",r"Without restrictions, the five people can sit in $5!=120$ ways."),("Define forbidden adjacencies",r"Let $X$ be the event Alice sits next to Bob, $Y$ the event Alice sits next to Carla, and $Z$ the event Derek sits next to Eric. We want to avoid all three."),("Count single forbidden events",r"Each adjacent pair can be treated as a block, so \[|X|=|Y|=|Z|=2\cdot4!=48.\]"),("Count overlaps",r"For $X\cap Y$, Alice must sit between Bob and Carla, giving $2\cdot3!=12$ arrangements. For $X\cap Z$ and $Y\cap Z$, there are two blocks, giving $2\cdot2\cdot3!=24$ each."),("Count the triple overlap",r"For $X\cap Y\cap Z$, use the Bob-Alice-Carla block in $2$ orders and the Derek-Eric block in $2$ orders, then arrange two blocks: $2\cdot2\cdot2!=8$."),("Apply inclusion-exclusion",r"The valid number is \[120-(48+48+48)+(12+24+24)-8=28.\]"),("Conclude",r"The answer is $\boxed{28}$."),],
20:[("Understand what adding 1 does",r"If $n$ does not end in $9$, then $S(n+1)=S(n)+1$. If $n$ ends in trailing $9$s, those $9$s become $0$s, causing a drop."),("Write the general change",r"If $n$ has exactly $k$ trailing $9$s, then adding $1$ changes the digit sum by \[+1-9k.\]"),("Apply to S(n)=1274",r"Thus \[S(n+1)=1274+1-9k=1275-9k\] for some integer $k\ge0$."),("Test the choices",r"Among the choices, only $1239$ has the form $1275-9k$, since \[1275-1239=36=9\cdot4.\]"),("Conclude",r"The possible value is $\boxed{1239}$."),],
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
        if r["year"] == "2017" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2017 AMC 10A Answer Key\n\n"
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












































