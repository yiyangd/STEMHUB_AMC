import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 94
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2016_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2016 AMC 10B Problems 1-10"
NEXT_START = "2016 AMC 10B Problem 11"

ANS={1:("D","10"),2:("B",r"\frac12"),3:("D","4032"),4:("B","Monday"),5:("D","22"),6:("B","4"),7:("C","135"),8:("A","0"),9:("C","8"),10:("D","33.3")}

OV={
1:(r"What is the value of $\frac{2a^{-1}+\frac{a^{-1}}2}{a}$ when $a=\frac12$?",[("A","1"),("B","2"),("C","5"),("D","10"),("E","20")]),
2:(r"If $n\heartsuit m=n^3m^2$, what is $\frac{2\heartsuit4}{4\heartsuit2}$?",[("A",r"$\frac14$"),("B",r"$\frac12$"),("C","1"),("D","2"),("E","4")]),
3:(r"Let $x=-2016$. What is the value of $\left||x|-x\right|-|x|-x$?",[("A","-2016"),("B","0"),("C","2016"),("D","4032"),("E","6048")]),
4:(r"Zoey read $15$ books, one at a time. The first book took her $1$ day to read, the second book took her $2$ days to read, the third book took her $3$ days to read, and so on, with each book taking $1$ more day to read than the previous book. Zoey finished the first book on a Monday, and the second on a Wednesday. On what day of the week did she finish her $15$th book?",[("A","Sunday"),("B","Monday"),("C","Wednesday"),("D","Friday"),("E","Saturday")]),
5:(r"The mean age of Amanda's $4$ cousins is $8$, and their median age is $5$. What is the sum of the ages of Amanda's youngest and oldest cousins?",[("A","13"),("B","16"),("C","19"),("D","22"),("E","25")]),
6:(r"Laura added two three-digit positive integers. All six digits in these numbers are different. Laura's sum is a three-digit number $S$. What is the smallest possible value for the sum of the digits of $S$?",[("A","1"),("B","4"),("C","5"),("D","15"),("E","21")]),
7:(r"The ratio of the measures of two acute angles is $5:4$, and the complement of one of these two angles is twice as large as the complement of the other. What is the sum of the degree measures of the two angles?",[("A","75"),("B","90"),("C","135"),("D","150"),("E","270")]),
8:(r"What is the tens digit of $2015^{2016}-2017$?",[("A","0"),("B","1"),("C","3"),("D","5"),("E","8")]),
9:(r"All three vertices of $\triangle ABC$ lie on the parabola defined by $y=x^2$, with $A$ at the origin and $BC$ parallel to the $x$-axis. The area of the triangle is $64$. What is the length of $BC$?",[("A","4"),("B","6"),("C","8"),("D","10"),("E","16")]),
10:(r"A thin piece of wood of uniform density in the shape of an equilateral triangle with side length $3$ inches weighs $12$ ounces. A second piece of the same type of wood, with the same thickness, also in the shape of an equilateral triangle, has side length of $5$ inches. Which of the following is closest to the weight, in ounces, of the second piece?",[("A","14.0"),("B","16.0"),("C","20.0"),("D","33.3"),("E","55.6")]),
}

KEY_OVERRIDES={1:"Substitute carefully after simplifying negative exponents.",2:"Evaluate the custom operation in numerator and denominator.",3:"Work from the innermost absolute value outward.",4:"Use cumulative reading days modulo 7.",5:"Use mean for total and median for the middle pair.",6:"Minimize a three-digit sum using place value and distinct digits.",7:"Turn the angle ratio and complement condition into an equation.",8:"Use modular arithmetic modulo 100 to get the tens digit.",9:"Use symmetry of a horizontal chord on the parabola.",10:"Weights scale with area, not side length."}

SOL={
1:[("Substitute the easy part first",r"When $a=\frac12$, its reciprocal is $a^{-1}=2$. The expression has several layers, so first replace every $a^{-1}$ by $2$."),("Simplify the numerator",r"The numerator is \[2a^{-1}+\frac{a^{-1}}2=2\cdot2+\frac22=4+1=5.\]"),("Divide by a",r"The full expression is \[\frac{5}{a}=\frac{5}{1/2}=10.\]"),("Check the direction",r"Because $a=\frac12$ is less than $1$, dividing by $a$ should make the numerator larger, not smaller. Getting $10$ from numerator $5$ is reasonable."),("Conclude",r"The answer is $\boxed{10}$."),],
2:[("Understand the operation",r"The definition $n\heartsuit m=n^3m^2$ means we cube the first input and square the second input."),("Evaluate the numerator",r"\[2\heartsuit4=2^3\cdot4^2=8\cdot16=128.\]"),("Evaluate the denominator",r"\[4\heartsuit2=4^3\cdot2^2=64\cdot4=256.\]"),("Take the ratio",r"Therefore \[\frac{2\heartsuit4}{4\heartsuit2}=\frac{128}{256}=\frac12.\]"),("Conclude",r"The answer is $\boxed{\frac12}$."),],
3:[("Start inside the absolute values",r"Since $x=-2016$, we have $|x|=2016$. The expression should be evaluated from the inside outward."),("Compute the inner difference",r"\[|x|-x=2016-(-2016)=4032.\] Its absolute value is still $4032$."),("Substitute into the whole expression",r"The expression becomes \[4032-|x|-x=4032-2016-(-2016).\]"),("Simplify carefully",r"The last two terms cancel in the sense that $-2016+2016=0$, leaving $4032$."),("Conclude",r"The answer is $\boxed{4032}$."),],
4:[("Think in days after the first book",r"Zoey finishes the first book on Monday. To find the weekday for the $15$th book, we only need the number of days from the end of book $1$ to the end of book $15$."),("Add the remaining reading times",r"Books $2$ through $15$ take \[2+3+\cdots+15=\frac{15\cdot16}{2}-1=119\] days."),("Reduce modulo 7",r"Since $119=17\cdot7$, this is a whole number of weeks. The weekday does not change."),("Check with the given information",r"Book $2$ finished $2$ days after Monday, which is Wednesday, matching the problem statement. So our day-count convention is correct."),("Conclude",r"Zoey finished the $15$th book on $\boxed{\text{Monday}}$."),],
5:[("Use the mean to find the total",r"The mean age of $4$ cousins is $8$, so the total of their ages is \[4\cdot8=32.\]"),("Use the median for the middle two",r"With $4$ ages in order, the median is the average of the two middle ages. A median of $5$ means the two middle ages have sum $10$."),("Subtract to get the outside pair",r"The youngest and oldest ages are the two ages not in the middle pair. Their sum is \[32-10=22.\]"),("Notice why individual ages are unnecessary",r"We do not need to know the four ages separately. The question asks for a sum, and the mean and median already give the two needed sums."),("Conclude",r"The answer is $\boxed{22}$."),],
6:[("Find a lower bound for S",r"To make the sum of two three-digit numbers as small as possible with six distinct digits, use $1$ and $2$ in the hundreds places and use $0,3,4,5$ in the remaining places. The smallest possible sum is at least \[100+200+10(0+3)+(4+5)=339.\]"),("Rule out digit sums below 4",r"A three-digit number with digit sum less than $4$ is at most $300$, because the largest such number is $300$. But $S$ must be at least $339$."),("Show digit sum 4 is possible",r"We need an example, not just a lower bound. The sum \[157+243=400\] uses six different digits in the two addends, and $400$ has digit sum $4$."),("Conclude minimality",r"No digit sum below $4$ is possible, and digit sum $4$ is possible."),("Final answer",r"The smallest possible digit sum is $\boxed{4}$."),],
7:[("Represent the two angles",r"Let the acute angles be $5x$ and $4x$. Their sum will be $9x$, so our goal is to find $x$."),("Compare the complements",r"The smaller angle $4x$ has the larger complement, $90-4x$. The larger angle $5x$ has complement $90-5x$."),("Use the twice-as-large condition",r"The larger complement is twice the smaller complement, so \[90-4x=2(90-5x).\]"),("Solve",r"This gives $90-4x=180-10x$, so $6x=90$ and $x=15$."),("Find the requested sum",r"The two angles sum to $9x=9\cdot15=135$ degrees."),("Conclude",r"The answer is $\boxed{135}$."),],
8:[("Aim for the last two digits",r"The tens digit is determined by the number modulo $100$. So we study $2015^{2016}-2017$ modulo $100$."),("Simplify the base",r"Since $2015\equiv15\pmod{100}$, we need $15^{2016}\pmod{100}$."),("Find the pattern",r"\[15^2=225\equiv25\pmod{100}.\] Multiplying by $15^2$ keeps an even power congruent to $25$ modulo $100$, so $15^{2016}\equiv25\pmod{100}$."),("Subtract",r"Thus \[2015^{2016}-2017\equiv25-17=8\pmod{100}.\] The last two digits are $08$."),("Conclude",r"The tens digit is $\boxed{0}$."),],
9:[("Use the horizontal chord",r"Because $BC$ is parallel to the $x$-axis, points $B$ and $C$ have the same $y$-coordinate. On the parabola $y=x^2$, equal $y$-values occur at opposite $x$-values."),("Name the points",r"Let \[B=(-t,t^2),\quad C=(t,t^2),\quad A=(0,0).\] Then $BC=2t$."),("Use the area",r"The base is $2t$ and the height from $A$ to the horizontal line $BC$ is $t^2$. So the area is \[\frac12(2t)(t^2)=t^3.\]"),("Solve for t",r"The area is $64$, so $t^3=64$ and $t=4$."),("Find BC",r"Therefore $BC=2t=8$."),("Conclude",r"The answer is $\boxed{8}$."),],
10:[("Use area scaling",r"The wood has uniform density and the same thickness, so weight is proportional to area. For similar equilateral triangles, area scales as the square of side length."),("Find the scale factor",r"The side length changes from $3$ to $5$, so the area and weight scale by \[\left(\frac53\right)^2=\frac{25}{9}.\]"),("Compute the new weight",r"The second weight is \[12\cdot\frac{25}{9}=\frac{100}{3}\approx33.3.\]"),("Choose the closest option",r"The choices are decimals, and $33.3$ is exactly the closest listed value."),("Conclude",r"The answer is $\boxed{33.3}$ ounces."),],
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












































