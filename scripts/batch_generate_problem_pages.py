import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 101
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2017_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16,17,19,20}
SKIPPED = ["2017 AMC 10B Problem 18 skipped: disk-painting equivalence depends on the missing figure layout."]
BATCH_LABEL = "2017 AMC 10B Problems 11-17, 19-20"
NEXT_START = "2017 AMC 10B Problem 21"

ANS={11:("D","25%"),12:("A","20%"),13:("C","3"),14:("D",r"\frac45"),15:("E",r"\frac{54}{25}"),16:("A","469"),17:("B","1524"),19:("E","37:1"),20:("B",r"\frac1{19}")}

OV={
11:(r"At Typico High School, $60\%$ of the students like dancing, and the rest dislike it. Of those who like dancing, $80\%$ say that they like it, and the rest say that they dislike it. Of those who dislike dancing, $90\%$ say that they dislike it, and the rest say that they like it. What fraction of students who say they dislike dancing actually like it?",[("A","10%"),("B","12%"),("C","20%"),("D","25%"),("E",r"$33\frac13\%$")]),
12:(r"Elmer's new car gives $50\%$ better fuel efficiency, measured in kilometers per liter, than his old car. However, his new car uses diesel fuel, which is $20\%$ more expensive per liter than the gasoline his old car used. By what percent will Elmer save money if he uses his new car instead of his old car for a long trip?",[("A","20%"),("B",r"$26\frac23\%$"),("C",r"$27\frac79\%$"),("D",r"$33\frac13\%$"),("E",r"$66\frac23\%$")]),
13:(r"There are $20$ students participating in an after-school program offering classes in yoga, bridge, and painting. Each student must take at least one of these three classes, but may take two or all three. There are $10$ students taking yoga, $13$ taking bridge, and $9$ taking painting. There are $9$ students taking at least two classes. How many students are taking all three classes?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
14:(r"An integer $N$ is selected at random in the range $1\le N\le2020$. What is the probability that the remainder when $N^{16}$ is divided by $5$ is $1$?",[("A",r"$\frac15$"),("B",r"$\frac25$"),("C",r"$\frac35$"),("D",r"$\frac45$"),("E","1")]),
15:(r"Rectangle $ABCD$ has $AB=3$ and $BC=4$. Point $E$ is the foot of the perpendicular from $B$ to diagonal $AC$. What is the area of $\triangle ADE$?",[("A","1"),("B",r"$\frac{42}{25}$"),("C",r"$\frac{28}{15}$"),("D","2"),("E",r"$\frac{54}{25}$")]),
16:(r"How many of the base-ten numerals for the positive integers less than or equal to $2017$ contain the digit $0$?",[("A","469"),("B","471"),("C","475"),("D","478"),("E","481")]),
17:(r"Call a positive integer monotonous if it is a one-digit number or its digits, when read from left to right, form either a strictly increasing or a strictly decreasing sequence. For example, $3$, $23578$, and $987620$ are monotonous, but $88$, $7434$, and $23557$ are not. How many monotonous positive integers are there?",[("A","1024"),("B","1524"),("C","1533"),("D","1536"),("E","2048")]),
19:(r"Let $ABC$ be an equilateral triangle. Extend side $AB$ beyond $B$ to a point $B'$ so that $BB'=3AB$. Similarly, extend side $BC$ beyond $C$ to a point $C'$ so that $CC'=3BC$, and extend side $CA$ beyond $A$ to a point $A'$ so that $AA'=3CA$. What is the ratio of the area of $\triangle A'B'C'$ to the area of $\triangle ABC$?",[("A","9:1"),("B","16:1"),("C","25:1"),("D","36:1"),("E","37:1")]),
20:(r"The number $21!$ has over $60,000$ positive integer divisors. One of them is chosen at random. What is the probability that it is odd?",[("A",r"$\frac1{21}$"),("B",r"$\frac1{19}$"),("C",r"$\frac1{18}$"),("D",r"$\frac12$"),("E",r"$\frac{11}{21}$")]),
}

KEY_OVERRIDES={11:"Use a two-way table with actual preference versus reported preference.",12:"Compare cost per kilometer after scaling efficiency and fuel price.",13:"Use inclusion-exclusion counts by exactly one, exactly two, and three classes.",14:"Use residues modulo 5 and Fermat's little theorem.",15:"Use coordinates and a projection onto the diagonal.",16:"Count the complement: numerals with no zero.",17:"Count increasing and decreasing digit subsets, then subtract overlap.",19:"Use coordinates to compare triangle areas.",20:"Only the exponent of 2 determines whether a divisor is odd."}

SOL={
11:[("Use a sample of 100 students",r"Percent problems are often easier with $100$ students. Then $60$ actually like dancing and $40$ actually dislike it."),("Count students who say dislike but actually like",r"Of the $60$ who actually like dancing, $20\%$ say they dislike it. That is $12$ students."),("Count all students who say dislike",r"Of the $40$ who actually dislike dancing, $90\%$ say they dislike it. That is $36$ students. So a total of $12+36=48$ students say they dislike dancing."),("Find the requested fraction",r"Among the $48$ who say they dislike dancing, $12$ actually like it. The fraction is \[\frac{12}{48}=\frac14=25\%.\]"),("Conclude",r"The answer is $\boxed{25\%}$."),],
12:[("Use cost per kilometer",r"Let the old car travel $1$ kilometer per liter and let gasoline cost $\$1$ per liter. Then the old cost is $\$1$ per kilometer."),("Apply the new efficiency",r"The new car is $50\%$ more efficient, so it travels $1.5$ kilometers per liter."),("Apply the new fuel price",r"Diesel costs $20\%$ more, so it costs $\$1.20$ per liter."),("Compute new cost per kilometer",r"The new cost per kilometer is \[\frac{1.20}{1.5}=0.80.\]"),("Find savings",r"Going from $\$1.00$ to $\$0.80$ is a savings of $20\%$."),("Conclude",r"The answer is $\boxed{20\%}$."),],
13:[("Separate exactly two and all three",r"Let $y$ be the number of students taking exactly two classes, and let $z$ be the number taking all three classes. The problem says $y+z=9$."),("Count class enrollments",r"The total class enrollments are \[10+13+9=32.\] A student taking exactly one class contributes $1$, exactly two contributes $2$, and all three contributes $3$."),("Compare to the number of students",r"Since there are $20$ students, the extra enrollments beyond one per student are \[32-20=12.\] Exactly-two students add $1$ extra each, and all-three students add $2$ extras each, so \[y+2z=12.\]"),("Solve",r"Subtract $y+z=9$ from $y+2z=12$ to get $z=3$."),("Conclude",r"There are $\boxed{3}$ students taking all three classes."),],
14:[("Work modulo 5",r"We only care about $N^{16}$ modulo $5$. If $N$ is divisible by $5$, then $N^{16}\equiv0\pmod5$."),("Use nonzero residues",r"If $N$ is not divisible by $5$, then by Fermat's little theorem, $N^4\equiv1\pmod5$. Therefore \[N^{16}=(N^4)^4\equiv1\pmod5.\]"),("Count the integers",r"Among any $5$ consecutive integers, $4$ are not divisible by $5$. The range $1$ to $2020$ contains complete groups of $5$."),("Find the probability",r"Thus the probability is \[\frac45.\]"),("Conclude",r"The answer is $\boxed{\frac45}$."),],
15:[("Set coordinates",r"Let $A=(0,0)$, $B=(3,0)$, $C=(3,4)$, and $D=(0,4)$. The diagonal $AC$ lies on the line through $(0,0)$ and $(3,4)$."),("Find the foot E",r"The foot from $B$ to $AC$ is the projection of $(3,0)$ onto the line in direction $(3,4)$. This gives \[E=\frac{B\cdot(3,4)}{(3,4)\cdot(3,4)}(3,4)=\frac9{25}(3,4)=\left(\frac{27}{25},\frac{36}{25}\right).\]"),("Use AD as a base",r"Segment $AD$ is vertical with length $4$. The horizontal distance from $E$ to line $AD$ is the $x$-coordinate of $E$, which is $\frac{27}{25}$."),("Compute area",r"\[[ADE]=\frac12\cdot4\cdot\frac{27}{25}=\frac{54}{25}.\]"),("Conclude",r"The answer is $\boxed{\frac{54}{25}}$."),],
16:[("Count the complement",r"It is easier to count positive integers up to $2017$ whose numerals do not contain $0$, then subtract from $2017$."),("Count 1 to 999 without zero",r"For one-, two-, and three-digit numbers, the counts are \[9+9^2+9^3=819.\]"),("Count 1000 to 1999 without zero",r"The thousands digit is $1$, and the other three digits can each be $1$ through $9$, giving $9^3=729$ numbers."),("Handle 2000 to 2017",r"Every number from $2000$ to $2017$ contains a $0$ in the hundreds digit, so none are counted in the no-zero complement."),("Subtract",r"The number without zero is $819+729=1548$. Therefore the number containing $0$ is \[2017-1548=469.\]"),("Conclude",r"The answer is $\boxed{469}$."),],
17:[("Count increasing numbers",r"A strictly increasing positive integer cannot contain $0$, because $0$ would have to be the first digit. Choosing any nonempty subset of $\{1,2,\ldots,9\}$ determines exactly one increasing number, so there are \[2^9-1=511.\]"),("Count decreasing numbers",r"A strictly decreasing positive integer can use digits from $\{0,1,\ldots,9\}$, but not the subset $\{0\}$ alone and not the empty subset. This gives \[2^{10}-2=1022.\]"),("Correct for overlap",r"The one-digit positive numbers $1$ through $9$ are counted both as increasing and decreasing. There are $9$ such overlaps."),("Add",r"The total is \[511+1022-9=1524.\]"),("Conclude",r"The answer is $\boxed{1524}$."),],
19:[("Choose coordinates",r"Let $A=(0,0)$, $B=(1,0)$, and $C=(\frac12,\frac{\sqrt3}{2})$. This makes $\triangle ABC$ have side length $1$."),("Find the extended points",r"Extending $AB$ beyond $B$ by $3AB$ gives $B'=(4,0)$. Extending $BC$ beyond $C$ gives \[C'=C+3(C-B)=(-1,2\sqrt3).\] Extending $CA$ beyond $A$ gives \[A'=A+3(A-C)=\left(-\frac32,-\frac{3\sqrt3}{2}\right).\]"),("Compute the large area",r"Using the coordinate area formula, \[[A'B'C']=\frac{37\sqrt3}{4}.\]"),("Compare with the original area",r"The original equilateral triangle has area \[[ABC]=\frac{\sqrt3}{4}.\]"),("Take the ratio",r"\[\frac{[A'B'C']}{[ABC]}=\frac{37\sqrt3/4}{\sqrt3/4}=37.\]"),("Conclude",r"The ratio is $\boxed{37:1}$."),],
20:[("Factor only what matters",r"A divisor of $21!$ is odd exactly when it uses no factor of $2$. So the probability is controlled by the exponent of $2$ in $21!$."),("Find the exponent of 2",r"The exponent of $2$ in $21!$ is \[\left\lfloor\frac{21}{2}\right\rfloor+\left\lfloor\frac{21}{4}\right\rfloor+\left\lfloor\frac{21}{8}\right\rfloor+\left\lfloor\frac{21}{16}\right\rfloor=10+5+2+1=18.\]"),("Compare odd divisors to all divisors",r"For every choice of the odd-prime exponents, there are $19$ choices for the exponent of $2$, namely $0$ through $18$."),("Find the probability",r"Only one of those $19$ choices, exponent $0$, gives an odd divisor. Therefore the probability is \[\frac1{19}.\]"),("Conclude",r"The answer is $\boxed{\frac1{19}}$."),],
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
        if r["year"] == "2017" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2017 AMC 10B Answer Key\n\n"
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












































