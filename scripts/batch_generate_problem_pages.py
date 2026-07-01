import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 115
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2020_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2020 AMC 10A Problems 1-10"
NEXT_START = "2020 AMC 10A Problem 11"

ANS={1:("E",r"\frac56"),2:("C","30"),3:("A","-1"),4:("E","26"),5:("C","18"),6:("B","100"),7:("C","10"),8:("B","9900"),9:("B","18"),10:("B","658")}

OV={
1:(r"What value of $x$ satisfies \[x-\frac34=\frac5{12}-\frac13?\]",[("A",r"$-\frac23$"),("B",r"$\frac7{36}$"),("C",r"$\frac7{12}$"),("D",r"$\frac23$"),("E",r"$\frac56$")]),
2:(r"The numbers $3,5,7,a,$ and $b$ have an average of $15$. What is the average of $a$ and $b$?",[("A","0"),("B","15"),("C","30"),("D","45"),("E","60")]),
3:(r"Assuming $a\ne3$, $b\ne4$, and $c\ne5$, what is the value in simplest form of \[\frac{a-3}{5-c}\cdot\frac{b-4}{3-a}\cdot\frac{c-5}{4-b}?\]",[("A","-1"),("B","1"),("C","abc"),("D",r"$1-\frac1{60abc}$"),("E",r"$1-\frac{abc}{60}$")]),
4:(r"A driver travels for $2$ hours at $60$ miles per hour, during which her car gets $30$ miles per gallon of gasoline. She is paid $\$0.50$ per mile, and her only expense is gasoline at $\$2.00$ per gallon. What is her net rate of pay, in dollars per hour, after this expense?",[("A","20"),("B","22"),("C","24"),("D","25"),("E","26")]),
5:(r"What is the sum of all real numbers $x$ for which \[|x^2-12x+34|=2?\]",[("A","12"),("B","15"),("C","18"),("D","21"),("E","25")]),
6:(r"How many $4$-digit positive integers having only even digits are divisible by $5$?",[("A","80"),("B","100"),("C","125"),("D","200"),("E","500")]),
7:(r"The $25$ integers from $-10$ to $14$, inclusive, can be arranged to form a $5$ by $5$ square in which each row, column, and main diagonal has the same sum. What is this common sum?",[("A","2"),("B","5"),("C","10"),("D","25"),("E","50")]),
8:(r"What is the value of \[1+2+3-4+5+6+7-8+\cdots+197+198+199-200?\]",[("A","9800"),("B","9900"),("C","10000"),("D","10100"),("E","10200")]),
9:(r"A single bench section can hold either $7$ adults or $11$ children. When $N$ bench sections are connected end to end, an equal number of adults and children seated together will occupy all the bench space. What is the least possible positive integer value of $N$?",[("A","9"),("B","18"),("C","27"),("D","36"),("E","77")]),
10:(r"Seven cubes, whose volumes are $1,8,27,64,125,216,$ and $343$ cubic units, are stacked vertically to form a tower in which the volumes decrease from bottom to top. Except for the bottom cube, the bottom face of each cube lies completely on top of the cube below it. What is the total surface area of the tower, including the bottom?",[("A","644"),("B","658"),("C","664"),("D","720"),("E","749")]),
}

KEY_OVERRIDES={1:"Clear fractions or add the same fraction to both sides.",2:"Use total sum from the average.",3:"Pair each factor with its negative counterpart.",4:"Compute revenue, gas cost, then net hourly rate.",5:"Split the absolute value equation into two quadratics.",6:"Count digit choices with divisibility by 5.",7:"Use the total sum of all entries in a magic square.",8:"Group the terms in blocks of four.",9:"Use a least common multiple condition for equal counts.",10:"Add cube surface areas and subtract hidden contact faces."}

SOL={
1:[("Isolate x",r"The equation is \[x-\frac34=\frac5{12}-\frac13.\] Add $\frac34$ to both sides."),("Use a common denominator",r"\[x=\frac5{12}-\frac4{12}+\frac9{12}.\]"),("Compute",r"\[x=\frac{5-4+9}{12}=\frac{10}{12}=\frac56.\]"),("Conclude",r"The answer is $\boxed{\frac56}$."),],
2:[("Use the average to find the total",r"Five numbers have average $15$, so their total is \[5\cdot15=75.\]"),("Subtract the known numbers",r"The known numbers add to \[3+5+7=15.\] Therefore \[a+b=75-15=60.\]"),("Find the average of a and b",r"The average of $a$ and $b$ is \[\frac{a+b}{2}=\frac{60}{2}=30.\]"),("Conclude",r"The answer is $\boxed{30}$."),],
3:[("Look for sign pairs",r"Each denominator is the negative of a similar numerator: \[3-a=-(a-3),\quad4-b=-(b-4),\quad5-c=-(c-5).\]"),("Rewrite the denominator product",r"The denominator \[(5-c)(3-a)(4-b)\] equals \[-(c-5)\cdot-(a-3)\cdot-(b-4).\] There are three negative signs, so the denominator is the negative of the numerator product."),("Cancel safely",r"Since $a\ne3$, $b\ne4$, and $c\ne5$, none of these factors is zero, so cancellation is valid."),("Compute the expression",r"The expression is \[-1.\]"),("Conclude",r"The answer is $\boxed{-1}$."),],
4:[("Find distance traveled",r"The driver travels for $2$ hours at $60$ miles per hour, so she drives \[2\cdot60=120\] miles."),("Compute revenue",r"She is paid $\$0.50$ per mile, so her pay is \[120\cdot0.50=\$60.\]"),("Compute gasoline cost",r"At $30$ miles per gallon, $120$ miles uses \[\frac{120}{30}=4\] gallons. At $\$2$ per gallon, this costs $\$8$."),("Find net hourly rate",r"Her net pay is \[60-8=52\] dollars over $2$ hours, so her net rate is \[\frac{52}{2}=26\] dollars per hour."),("Conclude",r"The answer is $\boxed{26}$."),],
5:[("Split the absolute value equation",r"The equation \[|x^2-12x+34|=2\] means \[x^2-12x+34=2\] or \[x^2-12x+34=-2.\]"),("Solve the first equation",r"\[x^2-12x+32=0=(x-4)(x-8),\] so $x=4$ or $x=8$."),("Solve the second equation",r"\[x^2-12x+36=0=(x-6)^2,\] so $x=6$."),("Add distinct real solutions",r"The real numbers are $4,6,8$, and their sum is \[4+6+8=18.\]"),("Conclude",r"The answer is $\boxed{18}$."),],
6:[("Use divisibility by 5",r"A number divisible by $5$ must end in $0$ or $5$. Since all digits must be even, the last digit must be $0$."),("Count the first digit",r"The thousands digit must be even and nonzero, so it has $4$ choices: $2,4,6,8$."),("Count the middle digits",r"Each of the hundreds and tens digits can be any of $0,2,4,6,8$, giving $5$ choices each."),("Multiply",r"The total number is \[4\cdot5\cdot5\cdot1=100.\]"),("Conclude",r"The answer is $\boxed{100}$."),],
7:[("Use the total sum",r"In a $5$ by $5$ magic square, the sum of the five row sums equals the sum of all $25$ entries."),("Find the total of the integers",r"The integers from $-10$ to $14$ have average \[\frac{-10+14}{2}=2,\] and there are $25$ of them. Their total is \[25\cdot2=50.\]"),("Divide among rows",r"If each row has common sum $S$, then \[5S=50.\]"),("Solve",r"\[S=10.\]"),("Conclude",r"The common sum is $\boxed{10}$."),],
8:[("Group in blocks of four",r"The signs repeat as three plus signs and one minus sign. Group the terms as \[(1+2+3-4)+(5+6+7-8)+\cdots.\]"),("Find a general block",r"The block starting at $4j+1$ is \[(4j+1)+(4j+2)+(4j+3)-(4j+4)=8j+2.\]"),("Count blocks",r"There are $200/4=50$ blocks, with $j=0,1,\ldots,49$."),("Sum",r"The total is \[\sum_{j=0}^{49}(8j+2)=8\cdot\frac{49\cdot50}{2}+100=9800+100=9900.\]"),("Conclude",r"The answer is $\boxed{9900}$."),],
9:[("Convert seating to section fractions",r"One adult uses $\frac17$ of a bench section, and one child uses $\frac1{11}$ of a section."),("Use equal numbers",r"If there are $x$ adults and $x$ children, then the number of sections used is \[\frac{x}{7}+\frac{x}{11}=\frac{18x}{77}.\]"),("Make N an integer",r"We need \[N=\frac{18x}{77}\] to be a positive integer. Since $\gcd(18,77)=1$, the smallest possible $x$ is $77$."),("Compute N",r"Then \[N=\frac{18\cdot77}{77}=18.\]"),("Conclude",r"The least possible value is $\boxed{18}$."),],
10:[("Find side lengths",r"The cube volumes are $1^3,2^3,\ldots,7^3$, so the side lengths are $1,2,\ldots,7$. They are stacked with side length $7$ on bottom and $1$ on top."),("Start with separate surface areas",r"If the cubes were separate, their total surface area would be \[6(1^2+2^2+\cdots+7^2)=6\cdot140=840.\]"),("Subtract hidden contact faces",r"When a cube of side $k$ sits on a larger cube, the contact hides area $k^2$ on the bottom of the small cube and $k^2$ on the top of the large cube. For $k=1,2,\ldots,6$, subtract \[2(1^2+2^2+\cdots+6^2)=2\cdot91=182.\]"),("Compute",r"The visible surface area is \[840-182=658.\]"),("Conclude",r"The answer is $\boxed{658}$."),],
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












































