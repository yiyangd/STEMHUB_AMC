import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 107
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2018_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,16,17,18,19,20}
SKIPPED = ["2018 AMC 10B Problem 15 skipped: wrapping-paper geometry depends on the missing figure."]
BATCH_LABEL = "2018 AMC 10B Problems 11-14,16-20"
NEXT_START = "2018 AMC 10B Problem 21"

ANS={11:("C",r"p^2+26"),12:("C","50"),13:("C","505"),14:("D","225"),16:("E","4"),17:("B","7"),18:("D","96"),19:("E","11"),20:("B","2017")}

OV={
11:(r"Which of the following expressions is never a prime number when $p$ is a prime number?",[("A",r"$p^2+16$"),("B",r"$p^2+24$"),("C",r"$p^2+26$"),("D",r"$p^2+46$"),("E",r"$p^2+96$")]),
12:(r"Line segment $AB$ is a diameter of a circle with $AB=24$. Point $C$, not equal to $A$ or $B$, lies on the circle. As point $C$ moves around the circle, the centroid of $\triangle ABC$ traces out a closed curve missing two points. To the nearest positive integer, what is the area of the region bounded by this curve?",[("A","25"),("B","38"),("C","50"),("D","63"),("E","75")]),
13:(r"How many of the first $2018$ numbers in the sequence $101,1001,10001,100001,\ldots$ are divisible by $101$?",[("A","253"),("B","504"),("C","505"),("D","506"),("E","1009")]),
14:(r"A list of $2018$ positive integers has a unique mode, which occurs exactly $10$ times. What is the least number of distinct values that can occur in the list?",[("A","202"),("B","223"),("C","224"),("D","225"),("E","234")]),
16:(r"Let $a_1,a_2,\ldots,a_{2018}$ be a strictly increasing sequence of positive integers such that $a_1+a_2+\cdots+a_{2018}=2018^{2018}$. What is the remainder when $a_1^3+a_2^3+\cdots+a_{2018}^3$ is divided by $6$?",[("A","0"),("B","1"),("C","2"),("D","3"),("E","4")]),
17:(r"In rectangle $PQRS$, $PQ=8$ and $QR=6$. Points $A$ and $B$ lie on $PQ$, points $C$ and $D$ lie on $QR$, points $E$ and $F$ lie on $RS$, and points $G$ and $H$ lie on $SP$ so that $AP=BQ<4$ and the convex octagon $ABCDEFGH$ is equilateral. The side length can be expressed as $k+m\sqrt n$, where $k,m,n$ are integers and $n$ is squarefree. What is $k+m+n$?",[("A","1"),("B","7"),("C","21"),("D","92"),("E","106")]),
18:(r"Three young brother-sister pairs from different families need to take a trip in a van. These six children will occupy the second and third rows in the van, each of which has three seats. To avoid disruptions, siblings may not sit right next to each other in the same row, and no child may sit directly in front of his or her sibling. How many seating arrangements are possible?",[("A","60"),("B","72"),("C","92"),("D","96"),("E","120")]),
19:(r"Joey and Chloe and their daughter Zoe all have the same birthday. Joey is $1$ year older than Chloe, and Zoe is exactly $1$ year old today. Today is the first of the $9$ birthdays on which Chloe's age will be an integral multiple of Zoe's age. What will be the sum of the two digits of Joey's age the next time his age is a multiple of Zoe's age?",[("A","7"),("B","8"),("C","9"),("D","10"),("E","11")]),
20:(r"A function $f$ is defined recursively by $f(1)=f(2)=1$ and $f(n)=f(n-1)-f(n-2)+n$ for all integers $n\ge3$. What is $f(2018)$?",[("A","2016"),("B","2017"),("C","2018"),("D","2019"),("E","2020")]),
}

KEY_OVERRIDES={11:"Use modular arithmetic to find an expression that is always divisible by 3.",12:"A centroid is an affine image of the moving vertex, so the traced curve is a smaller circle.",13:"Use the repeating powers of 10 modulo 101.",14:"A unique mode limits every other value to at most 9 occurrences.",16:"Use the congruence $n^3\equiv n\pmod 6$.",17:"Turn the equilateral octagon into a right-triangle equation at each rectangle corner.",18:"Count perfect matchings of sibling pairs among allowed seat pairs, then label and order the siblings.",19:"Translate age multiples into divisor counts.",20:"Look for a short periodic pattern in $f(n)-n$."}

SOL={
11:[("Look for a guaranteed divisor",r"When a problem asks which expression is never prime, a useful first thought is to look for a small divisor that always appears. Since the constants differ by small amounts, checking residues modulo $3$ is efficient."),("Handle the even prime separately",r"If $p=2$, then choice C gives \[p^2+26=4+26=30,\] which is not prime."),("Use odd primes modulo 3",r"For any odd prime $p$, either $p=3$ or $p$ is not divisible by $3$. In both cases, $p^2\equiv0$ or $1\pmod3$. If $p=3$, then $p^2+26=35$, not prime. If $p$ is not divisible by $3$, then $p^2\equiv1\pmod3$."),("Check choice C",r"Because $26\equiv2\pmod3$, we get \[p^2+26\equiv1+2\equiv0\pmod3.\] The expression is larger than $3$, so it is composite."),("Conclude",r"Choice C, $p^2+26$, is never prime. The answer is $\boxed{p^2+26}$."),],
12:[("Focus on what actually moves",r"The points $A$ and $B$ stay fixed, while only $C$ moves around the circle. Since the centroid is the average of the three vertices, the motion of the centroid is a scaled copy of the motion of $C$."),("Choose coordinates",r"Put the center of the circle at the origin and let $A=(-12,0)$ and $B=(12,0)$. Then a moving point $C=(x,y)$ satisfies \[x^2+y^2=12^2.\]"),("Find the centroid",r"The centroid $G$ of $\triangle ABC$ is \[G=\left(\frac{-12+12+x}{3},\frac{0+0+y}{3}\right)=\left(\frac{x}{3},\frac{y}{3}\right).\]"),("Identify the traced curve",r"As $C$ moves on a circle of radius $12$, the point $G$ moves on a circle of radius $12/3=4$. The two missing positions corresponding to $C=A$ or $C=B$ do not change the area enclosed by the curve."),("Compute the area",r"The bounded region has area \[\pi\cdot4^2=16\pi\approx50.3.\] To the nearest positive integer, this is $50$."),("Conclude",r"The answer is $\boxed{50}$."),],
13:[("Rewrite the sequence",r"The terms are $10^2+1,10^3+1,10^4+1,\ldots$. The first $2018$ terms correspond to exponents $2$ through $2019$."),("Use the key modular fact",r"Since \[10^2=100\equiv-1\pmod{101},\] powers of $10$ repeat every $4$ exponents modulo $101$."),("Find the exponents that work",r"We need $10^k+1\equiv0\pmod{101}$, which means $10^k\equiv-1\pmod{101}$. This happens when \[k\equiv2\pmod4.\]"),("Count the exponents",r"From $2$ through $2019$, the working exponents are \[2,6,10,\ldots,2018.\] This arithmetic sequence has \[\frac{2018-2}{4}+1=505\] terms."),("Conclude",r"There are $\boxed{505}$ divisible terms."),],
14:[("Understand what a unique mode allows",r"The mode occurs exactly $10$ times, and it must be unique. Therefore every other value may occur at most $9$ times."),("Separate the mode from the rest",r"After placing the modal value $10$ times, there are \[2018-10=2008\] remaining entries to fill."),("Pack the remaining entries efficiently",r"To minimize the number of distinct values, each nonmodal value should appear as many times as possible, namely $9$ times."),("Count the needed nonmodal values",r"We need enough groups of size at most $9$ to cover $2008$ entries: \[\left\lceil\frac{2008}{9}\right\rceil=224.\]"),("Add the modal value",r"These $224$ values are in addition to the one modal value, so the least number of distinct values is \[224+1=225.\]"),("Conclude",r"The answer is $\boxed{225}$."),],
16:[("Look for a congruence that connects cubes to numbers",r"The sequence itself is not specified, so we should look for a fact that works for every integer. Modulo $6$, every integer has the same remainder as its cube."),("State the useful fact",r"For any integer $n$, \[n^3\equiv n\pmod6.\] This can be checked from residues $0,1,2,3,4,5$ modulo $6$."),("Apply it to the whole sum",r"Therefore \[a_1^3+a_2^3+\cdots+a_{2018}^3\equiv a_1+a_2+\cdots+a_{2018}\pmod6.\]"),("Use the given sum",r"The given sum is $2018^{2018}$. Since $2018\equiv2\pmod6$, we need $2^{2018}\pmod6$. Powers of $2$ modulo $6$ alternate $2,4,2,4,\ldots$, so an even exponent gives $4$."),("Conclude",r"The remainder is $\boxed{4}$."),],
17:[("Name the octagon side length",r"Let the common side length of the equilateral octagon be $t$. The rectangle has width $8$ and height $6$, so the horizontal straight side on top has length $8-2x=t$ for some corner cut length $x$."),("Use the vertical side similarly",r"Let the corresponding vertical corner cut length be $y$. Then the vertical straight side has length \[6-2y=t.\] Thus \[x=\frac{8-t}{2},\qquad y=\frac{6-t}{2}.\]"),("Use the slanted side",r"Each slanted side of the octagon is also length $t$. At a corner it forms a right triangle with legs $x$ and $y$, so \[t^2=x^2+y^2.\]"),("Substitute and solve",r"Substitute the expressions for $x$ and $y$: \[t^2=\left(\frac{8-t}{2}\right)^2+\left(\frac{6-t}{2}\right)^2.\] Multiplying by $4$ gives \[4t^2=(8-t)^2+(6-t)^2.\] This simplifies to \[t^2+14t-50=0.\]"),("Take the positive root",r"The positive solution is \[t=-7+3\sqrt{11}.\] Thus $k=-7$, $m=3$, and $n=11$."),("Conclude",r"So \[k+m+n=-7+3+11=7.\] The answer is $\boxed{7}$."),],
18:[("Model the seats as a small grid",r"Think of the two van rows as a $2$ by $3$ grid of seats. A sibling pair is forbidden to occupy two seats that are directly side-by-side in the same row or directly one in front of the other."),("Count allowed seat-pairs",r"There are $\binom62=15$ possible unordered pairs of seats. The forbidden pairs are $4$ horizontal adjacent pairs and $3$ vertical pairs, for $7$ forbidden pairs. So there are $15-7=8$ allowed unordered seat-pairs for one sibling pair."),("Pair all seats into allowed sibling-pair positions",r"Now we need to divide all $6$ seats into $3$ allowed pairs. A direct check of the $2$ by $3$ grid gives exactly two such complete pairings: the two diagonal pairing patterns that avoid all same-column and adjacent same-row conflicts."),("Assign the families",r"The $3$ different sibling pairs can be assigned to these three allowed seat-pairs in \[3!\] ways."),("Order brother and sister within each assigned pair",r"Within each family pair, the brother and sister can swap seats, giving $2$ choices for each of the $3$ families, or $2^3$ choices."),("Multiply",r"Therefore the number of seating arrangements is \[2\cdot3!\cdot2^3=2\cdot6\cdot8=96.\] The answer is $\boxed{96}$."),],
19:[("Translate ages into divisibility",r"Let Chloe's age today be $C$. Zoe is $1$ today, so on Zoe's $s$-th birthday, Zoe's age is $s$ and Chloe's age is $C+s-1$."),("Convert Chloe's condition",r"Chloe's age is a multiple of Zoe's age when \[s\mid C+s-1.\] Since $s$ divides $s$, this is equivalent to \[s\mid C-1.\]"),("Use the number of birthdays",r"The problem says there are exactly $9$ such birthdays, so $C-1$ must have exactly $9$ positive divisors. The only reasonable positive integer under $100$ with $9$ divisors here is \[36=2^2\cdot3^2,\] so $C=37$."),("Check Joey's condition",r"Joey is $1$ year older than Chloe, so Joey is $38$ today. On Zoe's $s$-th birthday, Joey's age is $38+s-1=37+s$."),("Find the next multiple",r"We need $s\mid37+s$, which is equivalent to $s\mid37$. The next value after $s=1$ is $s=37$, so Joey's age then is \[37+37=74.\]"),("Conclude",r"The sum of the digits of $74$ is $7+4=11$. The answer is $\boxed{11}$."),],
20:[("Remove the obvious growing part",r"Because the recurrence includes a $+n$ term, it is natural to compare $f(n)$ with $n$. Define \[g(n)=f(n)-n.\]"),("Find the recurrence for g",r"Substitute $f(n)=g(n)+n$ into the recurrence: \[g(n)+n=(g(n-1)+n-1)-(g(n-2)+n-2)+n.\] After simplifying, \[g(n)=g(n-1)-g(n-2)+1.\]"),("Compute a short pattern",r"From $f(1)=1$ and $f(2)=1$, we get $g(1)=0$ and $g(2)=-1$. Then the recurrence gives \[0,-1,0,2,3,2,0,-1,\ldots\] for $g(n)$."),("Use periodicity",r"The pattern repeats every $6$ terms. Since \[2018\equiv2\pmod6,\] we use the second value in the pattern, which is $g(2018)=-1$."),("Finish",r"Thus \[f(2018)=2018+g(2018)=2018-1=2017.\]"),("Conclude",r"The answer is $\boxed{2017}$."),],
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
        if r["year"] == "2018" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2018 AMC 10B Answer Key\n\n"
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












































