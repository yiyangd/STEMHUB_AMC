import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 113
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2019_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16,17,18,19}
SKIPPED = ["2019 AMC 10B Problem 20 skipped: shaded circle/semicircle region depends on the missing figure."]
BATCH_LABEL = "2019 AMC 10B Problems 11-19"
NEXT_START = "2019 AMC 10B Problem 21"

ANS={11:("A","5"),12:("C","22"),13:("A","-5"),14:("C","12"),15:("A",r"\frac{28}{3}"),16:("A",r"2:3"),17:("C",r"\frac13"),18:("C",r"\frac65"),19:("C","117")}

OV={
11:(r"Two jars each contain the same number of marbles, and every marble is either blue or green. In Jar 1 the ratio of blue to green marbles is $9:1$, and in Jar 2 the ratio is $8:1$. There are $95$ green marbles in all. How many more blue marbles are in Jar 1 than in Jar 2?",[("A","5"),("B","10"),("C","25"),("D","45"),("E","50")]),
12:(r"What is the greatest possible sum of the digits in the base-seven representation of a positive integer less than $2019$?",[("A","11"),("B","14"),("C","22"),("D","23"),("E","27")]),
13:(r"What is the sum of all real numbers $x$ for which the median of the numbers $4,6,8,17,$ and $x$ is equal to the mean of those five numbers?",[("A","-5"),("B","0"),("C","5"),("D",r"$\frac{15}{4}$"),("E",r"$\frac{35}{4}$")]),
14:(r"The base-ten representation for $19!$ is $121,6T5,100,40M,832,H00$, where $T,M,$ and $H$ denote missing digits. What is $T+M+H$?",[("A","3"),("B","8"),("C","12"),("D","14"),("E","17")]),
15:(r"Two right triangles, $T_1$ and $T_2$, have areas $1$ and $2$, respectively. One side length of one triangle is congruent to a different side length in the other, and another side length of the first triangle is congruent to yet another side length in the other. What is the square of the product of the third side lengths of $T_1$ and $T_2$?",[("A",r"$\frac{28}{3}$"),("B","10"),("C",r"$\frac{32}{3}$"),("D",r"$\frac{34}{3}$"),("E","12")]),
16:(r"In $\triangle ABC$ with a right angle at $C$, point $D$ lies in the interior of $AB$ and point $E$ lies in the interior of $BC$ so that $AC=CD$, $DE=EB$, and $AC:DE=4:3$. What is the ratio $AD:DB$?",[("A",r"$2:3$"),("B",r"$2:5$"),("C",r"$1:1$"),("D",r"$3:5$"),("E",r"$3:2$")]),
17:(r"A red ball and a green ball are randomly and independently tossed into bins numbered with positive integers so that for each ball, the probability that it is tossed into bin $k$ is $2^{-k}$ for $k=1,2,3,\ldots$. What is the probability that the red ball is tossed into a higher-numbered bin than the green ball?",[("A",r"$\frac14$"),("B",r"$\frac27$"),("C",r"$\frac13$"),("D",r"$\frac38$"),("E",r"$\frac37$")]),
18:(r"Henry walks $\frac34$ of the way from his home to his gym, which is $2$ kilometers away. Then he changes his mind and walks $\frac34$ of the way back toward home. He keeps changing his mind after walking $\frac34$ of the distance toward the opposite endpoint. He gets very close to walking back and forth between a point $A$ kilometers from home and a point $B$ kilometers from home. What is $|A-B|$?",[("A",r"$\frac23$"),("B","1"),("C",r"$1\frac15$"),("D",r"$1\frac14$"),("E",r"$1\frac12$")]),
19:(r"Let $S$ be the set of all positive integer divisors of $100000$. How many numbers are the product of two distinct elements of $S$?",[("A","98"),("B","100"),("C","117"),("D","119"),("E","121")]),
}

KEY_OVERRIDES={11:"Use equal jar totals to write green counts in terms of one variable.",12:"Compare with $2019$ in base seven and maximize digits lexicographically.",13:"Break into cases based on the possible median.",14:"Compute or identify the decimal form of $19!$.",15:"Match the shared side lengths between two right triangles.",16:"Use coordinates and the section ratio on the hypotenuse.",17:"Use symmetry and subtract the probability of a tie.",18:"Set up limiting positions for the back-and-forth process.",19:"Count exponent pairs for products of distinct divisors."}

SOL={
11:[("Use a common jar size",r"Let each jar contain $N$ marbles. Jar 1 has blue:green ratio $9:1$, so its green count is $\frac{N}{10}$. Jar 2 has ratio $8:1$, so its green count is $\frac{N}{9}$."),("Use the total green count",r"The total number of green marbles is $95$, so \[\frac{N}{10}+\frac{N}{9}=95.\]"),("Solve for N",r"\[\frac{19N}{90}=95,\] so \[N=450.\]"),("Find blue counts",r"Jar 1 has \[\frac9{10}\cdot450=405\] blue marbles. Jar 2 has \[\frac89\cdot450=400\] blue marbles."),("Compare",r"The difference is \[405-400=5.\]"),("Conclude",r"The answer is $\boxed{5}$."),],
12:[("Convert the upper bound to base seven",r"We compare with $2019$ in base $7$. Since $7^3=343$, \[2019=5\cdot343+6\cdot49+1\cdot7+3,\] so \[2019=5613_7.\]"),("Maximize digits below 5613_7",r"To get a large digit sum while staying below $5613_7$, try making an earlier digit smaller and all later digits $6$."),("Check the best possibilities",r"If the first digit is less than $5$, the best number is $4666_7$, with digit sum $4+6+6+6=22$. If the first digit is $5$ but the second is less than $6$, the best number is $5566_7$, also with digit sum $22$."),("Rule out larger sums",r"If the first two digits are $56$, then the third digit must be less than $1$ to stay below $5613_7$, giving at most $5606_7$ with digit sum $17$."),("Conclude",r"The greatest possible digit sum is $\boxed{22}$."),],
13:[("Compute the mean expression",r"The five numbers have sum \[4+6+8+17+x=35+x,\] so their mean is \[\frac{35+x}{5}.\]"),("Consider possible medians",r"The median must be one of the middle values after inserting $x$ into $4,6,8,17$. We check intervals for $x$."),("Find the working case",r"If $x\le4$, the ordered list has median $6$. Setting mean equal to median gives \[\frac{35+x}{5}=6,\] so $x=-5$, which fits $x\le4$."),("Check other intervals",r"If $4\le x\le6$, the median is $6$, again giving $x=-5$, which does not fit. If $6\le x\le8$, the median is $x$, giving $x=\frac{35}{4}$, which does not fit. If $x\ge8$, the median is $8$, giving $x=5$, which does not fit."),("Conclude",r"The only real value is $x=-5$, so the requested sum is $\boxed{-5}$."),],
14:[("Recognize the factorial",r"We only need three missing digits of $19!$. The value is \[19!=121645100408832000.\]"),("Match the grouped format",r"Grouped in threes, this is \[121,\ 645,\ 100,\ 408,\ 832,\ 000.\]"),("Read the missing digits",r"Comparing with \[121,\ 6T5,\ 100,\ 40M,\ 832,\ H00,\] we get \[T=4,\quad M=8,\quad H=0.\]"),("Add",r"\[T+M+H=4+8+0=12.\]"),("Conclude",r"The answer is $\boxed{12}$."),],
15:[("Understand the side matching",r"The two right triangles have different areas, so the two shared side lengths cannot simply be the two legs in both triangles. The useful configuration is that one triangle's leg and hypotenuse are the two legs of the other triangle."),("Set up variables",r"Let $T_1$ have legs $a$ and $b$ and hypotenuse $c$, with area $1$. Then \[ab=2.\] Let $T_2$ have legs $a$ and $c$, with area $2$. Then \[ac=4.\]"),("Express b and c",r"From $ab=2$ and $ac=4$, \[b=\frac2a,\qquad c=\frac4a.\]"),("Use the right triangle condition for T_1",r"Since $c$ is the hypotenuse of $T_1$, \[c^2=a^2+b^2.\] Substituting gives \[\frac{16}{a^2}=a^2+\frac4{a^2},\] so \[a^4=12.\]"),("Find the third side product",r"The third side of $T_1$ not used in $T_2$ is $b=\frac2a$. The third side of $T_2$ is its hypotenuse, whose square is \[a^2+c^2=a^2+\frac{16}{a^2}.\] Therefore the square of the product is \[\frac4{a^2}\left(a^2+\frac{16}{a^2}\right)=4+\frac{64}{a^4}=4+\frac{64}{12}=\frac{28}{3}.\]"),("Conclude",r"The answer is $\boxed{\frac{28}{3}}$."),],
16:[("Choose convenient lengths",r"Since $AC:DE=4:3$ and $AC=CD$, set \[AC=CD=4,\qquad DE=EB=3.\] Place $C=(0,0)$ and $A=(4,0)$, with $B$ on the positive $y$-axis."),("Use coordinates for E and D",r"Let $E=(0,e)$ and $B=(0,e+3)$. If $D$ divides $\overline{AB}$ so that $AD:DB=t:(1-t)$, then \[D=(4(1-t),\,t(e+3)).\]"),("Use the two distance conditions",r"The conditions $CD=4$ and $DE=3$ give \[[4(1-t)]^2+[t(e+3)]^2=16,\] and \[[4(1-t)]^2+[t(e+3)-e]^2=9.\]"),("Solve the system",r"The nondegenerate solution is \[e=5,\qquad t=\frac25.\]"),("Convert t to the ratio",r"Since $t$ is the fraction of the way from $A$ to $B$, \[AD:DB=t:(1-t)=\frac25:\frac35=2:3.\]"),("Conclude",r"The answer is $\boxed{2:3}$."),],
17:[("Use symmetry",r"Because the red and green balls have the same independent distribution, the probability that red is higher equals the probability that green is higher."),("Subtract the tie probability",r"Let $P$ be the probability that the two balls land in the same bin. Then \[P(\text{red higher})=\frac{1-P}{2}.\]"),("Compute the tie probability",r"The probability both balls land in bin $k$ is \[(2^{-k})^2=4^{-k}.\] Thus \[P=\sum_{k=1}^{\infty}4^{-k}=\frac{1/4}{1-1/4}=\frac13.\]"),("Finish",r"So \[P(\text{red higher})=\frac{1-\frac13}{2}=\frac13.\]"),("Conclude",r"The answer is $\boxed{\frac13}$."),],
18:[("Track positions from home",r"Let home be position $0$ and the gym be position $2$. Henry's long-term motion approaches two positions: a lower point $A$ and an upper point $B$."),("Write the move toward the gym",r"Starting at $A$ and walking $\frac34$ of the way toward $2$ gives \[B=A+\frac34(2-A)=\frac32+\frac{A}{4}.\]"),("Write the move toward home",r"Starting at $B$ and walking $\frac34$ of the way toward $0$ gives \[A=B+\frac34(0-B)=\frac{B}{4}.\]"),("Solve the system",r"From $A=\frac{B}{4}$, we have $B=4A$. Substitute into the first equation: \[4A=\frac32+\frac{A}{4}.\] Then \[16A=6+A,\] so \[A=\frac25,\quad B=\frac85.\]"),("Find the distance between limits",r"\[|A-B|=\frac85-\frac25=\frac65=1\frac15.\]"),("Conclude",r"The answer is $\boxed{\frac65}$."),],
19:[("Represent divisors by exponent pairs",r"Since \[100000=10^5=2^5\cdot5^5,\] every divisor in $S$ has the form $2^a5^b$ with $0\le a,b\le5$."),("Represent products",r"The product of two divisors has the form $2^u5^v$, where $u$ and $v$ can range from $0$ to $10$. Without the distinctness restriction, that gives $11\cdot11=121$ possible exponent pairs."),("Account for distinct divisors",r"We need the two chosen divisors to be distinct. A product exponent pair is impossible only when it can be made in exactly one way, by multiplying a divisor by itself."),("Find the impossible corner cases",r"The only exponent pairs with a unique split in both coordinates are \[(0,0),(0,10),(10,0),(10,10).\] Each would require using the same corner divisor twice, which is not allowed."),("Subtract",r"Therefore the number of possible products is \[121-4=117.\]"),("Conclude",r"The answer is $\boxed{117}$."),],
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
        if r["year"] == "2019" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2019 AMC 10B Answer Key\n\n"
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












































