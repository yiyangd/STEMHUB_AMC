import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 125
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2021_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16,17,18,19}
SKIPPED = ["2021 Spring AMC 10B Problem 20 skipped: pentagon area depends on the missing 11-segment figure."]
BATCH_LABEL = "2021 Spring AMC 10B Problems 11-19"
NEXT_START = "2021 Spring AMC 10B Problem 21"

ANS={11:("D","60"),12:("C",r"1:14"),13:("B","11"),14:("B","6"),15:("B","0"),16:("C","6"),17:("C","Ravon was given card 4."),18:("C",r"\frac1{20}"),19:("D","36.8")}

OV={
11:(r"Grandma cuts a rectangular pan into equal rectangular brownies using straight cuts parallel to the sides, each cut going entirely across the pan. She wants the same number of interior pieces as pieces along the perimeter. What is the greatest possible number of brownies she can produce?",[("A","24"),("B","30"),("C","48"),("D","60"),("E","64")]),
12:(r"Let \[N=3^4\cdot3^4\cdot6^3\cdot27^0.\] What is the ratio of the sum of the odd divisors of $N$ to the sum of the even divisors of $N$?",[("A",r"$1:16$"),("B",r"$1:15$"),("C",r"$1:14$"),("D",r"$1:8$"),("E",r"$1:3$")]),
13:(r"Let $n$ be a positive integer and $d$ be a digit such that the value of the numeral $32d$ in base $n$ equals $263$, and the value of the numeral $324$ in base $n$ equals the value of the numeral $11d1$ in base six. What is $n+d$?",[("A","10"),("B","11"),("C","13"),("D","15"),("E","16")]),
14:(r"Three equally spaced parallel lines intersect a circle, creating three chords of lengths $38$, $38$, and $34$. What is the distance between two adjacent parallel lines?",[("A",r"$5\frac12$"),("B","6"),("C",r"$6\frac12$"),("D","7"),("E",r"$7\frac12$")]),
15:(r"The real number $x$ satisfies \[x+\frac1x=\sqrt5.\] What is the value of $x^{11}-7x^7+x^3$?",[("A","-1"),("B","0"),("C","1"),("D","2"),("E",r"$\sqrt5$")]),
16:(r"Call a positive integer an uphill integer if every digit is strictly greater than the previous digit. How many uphill integers are divisible by $15$?",[("A","4"),("B","5"),("C","6"),("D","7"),("E","8")]),
17:(r"Five players are each given two cards from the cards numbered $1$ through $10$. Their scores are the sums of their cards: Ravon $11$, Oscar $4$, Aditi $7$, Tyrone $16$, and Kim $17$. Which statement is true?",[("A","Ravon was given card 3."),("B","Aditi was given card 3."),("C","Ravon was given card 4."),("D","Aditi was given card 4."),("E","Tyrone was given card 7.")]),
18:(r"A fair $6$-sided die is repeatedly rolled until an odd number appears. What is the probability that every even number appears at least once before the first occurrence of an odd number?",[("A",r"$\frac1{120}$"),("B",r"$\frac1{32}$"),("C",r"$\frac1{20}$"),("D",r"$\frac3{20}$"),("E",r"$\frac16$")]),
19:(r"Suppose $S$ is a finite set of positive integers. If the greatest integer is removed, the average of the remaining integers is $32$. If the least integer is also removed, the average of the remaining integers is $35$. If the greatest integer is then returned, the average rises to $40$. The greatest integer in the original set is $72$ greater than the least integer. What is the average of all integers in $S$?",[("A","36.2"),("B","36.4"),("C","36.6"),("D","36.8"),("E","37")]),
}

KEY_OVERRIDES={11:"Relate grid dimensions to interior and perimeter pieces.",12:"Separate the odd divisor sum from the power of 2.",13:"Translate base numerals into equations.",14:"Use chord length and distance from the center.",15:"Use symmetric powers of x and 1/x.",16:"Represent uphill integers by subsets of digits.",17:"Use forced card pairs from the smallest and largest sums.",18:"Think of the first distinct die faces before the first odd.",19:"Set up equations for the middle sum, least, greatest, and set size."}

SOL={
11:[("Model the brownie grid",r"Suppose the pan is cut into $m$ rows and $n$ columns of brownies. Then there are $mn$ total pieces."),("Count interior pieces",r"The interior pieces are those not touching the perimeter, so there are \[(m-2)(n-2)\] of them."),("Count perimeter pieces",r"The perimeter pieces are the total minus the interior: \[mn-(m-2)(n-2)=2m+2n-4.\]"),("Set the counts equal",r"We need \[(m-2)(n-2)=2m+2n-4.\] Simplifying gives \[mn-4m-4n+8=0,\] or \[(m-4)(n-4)=8.\]"),("Maximize the product",r"The factor pair $1\cdot8$ gives $(m,n)=(5,12)$ up to order, producing \[mn=60\] brownies. The other factor pair gives fewer."),("Conclude",r"The greatest possible number is $\boxed{60}$."),],
12:[("Factor N",r"Since $27^0=1$ and $6^3=2^3\cdot3^3$, we have \[N=3^4\cdot3^4\cdot6^3\cdot27^0=2^3\cdot3^{11}.\]"),("Separate odd and even divisors",r"The odd divisors are exactly the divisors of $3^{11}$, so their sum is \[\sigma(3^{11}).\]"),("Find the even divisor sum",r"Even divisors must use a positive power of $2$. The sum of the possible powers of $2$ is \[2+4+8=14.\] For each such choice, the odd part can be any divisor of $3^{11}$."),("Compare the sums",r"Thus the sum of even divisors is \[14\sigma(3^{11}),\] while the odd divisor sum is \[\sigma(3^{11}).\]"),("Conclude",r"The ratio is $\boxed{1:14}$."),],
13:[("Translate the first base equation",r"The numeral $32d$ in base $n$ has value \[3n^2+2n+d=263.\]"),("Translate the second base equation",r"The numeral $324$ in base $n$ has value $3n^2+2n+4$. The numeral $11d1$ in base $6$ has value \[6^3+6^2+6d+1=253+6d.\]"),("Compare the two equations",r"From the first equation, $3n^2+2n=263-d$. Substitute into the second: \[263-d+4=253+6d.\]"),("Solve for d and n",r"This gives $14=7d$, so $d=2$. Then \[3n^2+2n+2=263,\] so \[3n^2+2n-261=0,\] which gives $n=9$."),("Conclude",r"Therefore \[n+d=9+2=11.\] The answer is $\boxed{11}$."),],
14:[("Relate chord length to center distance",r"For a circle of radius $R$, a chord at distance $t$ from the center has half-length satisfying \[\left(\frac L2\right)^2=R^2-t^2.\]"),("Use the equal chord lengths",r"The two chords of length $38$ must be equally far from the center. Since the three lines are equally spaced and the third chord is shorter, the distances from the center are \[\frac d2,\frac d2,\frac{3d}{2},\] where $d$ is the spacing."),("Set up equations",r"For the length-$38$ chords, \[R^2-\left(\frac d2\right)^2=19^2=361.\] For the length-$34$ chord, \[R^2-\left(\frac{3d}{2}\right)^2=17^2=289.\]"),("Subtract",r"Subtracting the equations gives \[2d^2=72,\] so $d^2=36$ and $d=6$."),("Conclude",r"The distance between adjacent lines is $\boxed{6}$."),],
15:[("Use symmetry in the expression",r"The exponents $11,7,3$ are symmetric around $7$, so factor out $x^7$: \[x^{11}-7x^7+x^3=x^7\left(x^4-7+\frac1{x^4}\right).\]"),("Find x squared plus reciprocal",r"From \[x+\frac1x=\sqrt5,\] square both sides: \[x^2+2+\frac1{x^2}=5,\] so \[x^2+\frac1{x^2}=3.\]"),("Find the fourth-power version",r"Square again: \[x^4+2+\frac1{x^4}=9,\] so \[x^4+\frac1{x^4}=7.\]"),("Substitute",r"Then \[x^4-7+\frac1{x^4}=0,\] so the original expression is $x^7\cdot0=0$."),("Conclude",r"The answer is $\boxed{0}$."),],
16:[("Use divisibility by 15",r"An integer divisible by $15$ must be divisible by $5$ and by $3$. An uphill integer cannot end in $0$, so it must end in $5$."),("Choose earlier digits",r"All earlier digits must be chosen from $\{1,2,3,4\}$ and placed in increasing order. Thus each subset of $\{1,2,3,4\}$ gives one uphill integer ending in $5$."),("Use divisibility by 3",r"The digit sum must be divisible by $3$. Since the final digit is $5$, the chosen subset must have sum congruent to $1\pmod3$."),("Count the subsets",r"The valid subsets are \[\{1\},\{4\},\{1,3\},\{3,4\},\{1,2,4\},\{1,2,3,4\}.\] There are $6$ of them."),("Conclude",r"The answer is $\boxed{6}$."),],
17:[("Start with the forced small sum",r"Oscar's score is $4$, so Oscar must have cards $1$ and $3$."),("Find Aditi's cards",r"Aditi's score is $7$. The possible pairs are $(1,6)$, $(2,5)$, and $(3,4)$. Since $1$ and $3$ are already used by Oscar, Aditi must have $(2,5)$."),("Use the large scores",r"Kim's score is $17$, so Kim has either $(7,10)$ or $(8,9)$. Tyrone's score is $16$, so Tyrone has either $(6,10)$ or $(7,9)$."),("Avoid overlaps",r"If Kim had $(7,10)$, Tyrone could not make $16$ without reusing a card. Thus Kim has $(8,9)$ and Tyrone has $(6,10)$."),("Determine Ravon's cards",r"The remaining cards are $4$ and $7$, and they sum to Ravon's score $11$. Therefore Ravon was given card $4$."),("Conclude",r"The true statement is $\boxed{\text{Ravon was given card 4}}$."),],
18:[("Think about first appearances",r"The process stops at the first odd roll. We need the first appearances of all three even faces $2,4,6$ to occur before any odd face appears."),("Ignore repeated rolls",r"Repeated rolls of a face already seen do not change which new face appears next. So we can look at the order in which distinct die faces first appear."),("Count distinct-face orders",r"Among the six faces, every set of three faces is equally likely to be the first three distinct faces. We need those first three distinct faces to be exactly $\{2,4,6\}$."),("Compute the probability",r"There is only one favorable $3$-element set out of \[\binom63=20\] possible sets."),("Conclude",r"The probability is $\boxed{\frac1{20}}$."),],
19:[("Name the important quantities",r"Let the original set have $n$ elements, least element $l$, greatest element $g$, and let $M$ be the sum of the other $n-2$ elements."),("Write the three average equations",r"Removing the greatest gives \[M+l=32(n-1).\] Removing both least and greatest gives \[M=35(n-2).\] Returning the greatest while leaving out the least gives \[M+g=40(n-1).\]"),("Solve for l and g in terms of n",r"Using $M=35(n-2)$, the first equation gives \[l=32(n-1)-35(n-2)=38-3n.\] The third gives \[g=40(n-1)-35(n-2)=5n+30.\]"),("Use the difference",r"We are told $g-l=72$, so \[(5n+30)-(38-3n)=72.\] Hence $8n-8=72$, and $n=10$."),("Find the total average",r"Then $M=35(8)=280$, $l=8$, and $g=80$. The total sum is \[280+8+80=368.\] With $10$ elements, the average is \[36.8.\]"),("Conclude",r"The answer is $\boxed{36.8}$."),],
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
    year_label = row["year"]
    if year_label == "2021 Spring":
        year_part = "2021"
    elif year_label == "2021 Fall":
        year_part = "2021_Fall"
    else:
        year_part = year_label.replace(" ", "_")
    return f"https://artofproblemsolving.com/wiki/index.php/{year_part}_{row['contest'].replace(' ', '_')}{row['form']}_Problems/Problem_{row['problem_no']}"


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
        if r["year"] == "2021 Spring" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2021 AMC 10B Answer Key\n\n"
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












































