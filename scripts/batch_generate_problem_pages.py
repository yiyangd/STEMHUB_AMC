import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 56
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2011_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2011 AMC 10A Problems 1-10"
NEXT_START = "2011 AMC 10A Problem 11"

ANS = {
    1: ("D", r"\$28.00"),
    2: ("E", "15"),
    3: ("D", r"\frac{7}{18}"),
    4: ("A", "92"),
    5: ("C", r"\frac{88}{7}"),
    6: ("C", "20"),
    7: ("B", r"|-3x|+5=0"),
    8: ("C", "40"),
    9: ("A", r"ac+ad+bc+bd"),
    10: ("B", "11"),
}

OV = {
    1: (r"A cell phone plan costs $\$20$ each month, plus $5$ cents per text message sent, plus $10$ cents for each minute used over $30$ hours. In January Michelle sent $100$ text messages and talked for $30.5$ hours. How much did she have to pay?", [("A", r"\$24.00"),("B", r"\$24.50"),("C", r"\$25.50"),("D", r"\$28.00"),("E", r"\$30.00")]),
    2: (r"A small bottle of shampoo can hold $35$ milliliters, whereas a large bottle can hold $500$ milliliters. Jasmine wants to buy the minimum number of small bottles necessary to completely fill a large bottle. How many bottles must she buy?", [("A","11"),("B","12"),("C","13"),("D","14"),("E","15")]),
    3: (r"Suppose $[a\ b]$ denotes the average of $a$ and $b$, and $\{a\ b\ c\}$ denotes the average of $a,b,c$. What is $\{\{1\ 1\ 0\}\ [0\ 1]\ 0\}$?", [("A",r"\frac{2}{9}"),("B",r"\frac{5}{18}"),("C",r"\frac{1}{3}"),("D",r"\frac{7}{18}"),("E",r"\frac{2}{3}")]),
    4: (r"Let $X$ and $Y$ be the following sums of arithmetic sequences: $X=10+12+14+\cdots+100$ and $Y=12+14+16+\cdots+102$. What is the value of $Y-X$?", [("A","92"),("B","98"),("C","100"),("D","102"),("E","112")]),
    5: (r"At an elementary school, the students in third grade, fourth grade, and fifth grade run an average of $12$, $15$, and $10$ minutes per day, respectively. There are twice as many third graders as fourth graders, and twice as many fourth graders as fifth graders. What is the average number of minutes run per day by these students?", [("A","12"),("B",r"\frac{37}{3}"),("C",r"\frac{88}{7}"),("D","13"),("E","14")]),
    6: (r"Set $A$ has $20$ elements, and set $B$ has $15$ elements. What is the smallest possible number of elements in $A\cup B$, the union of $A$ and $B$?", [("A","5"),("B","15"),("C","20"),("D","35"),("E","300")]),
    7: (r"Which of the following equations does NOT have a solution?", [("A",r"(x+7)^2=0"),("B",r"|-3x|+5=0"),("C",r"\sqrt{-x}-2=0"),("D",r"\sqrt{x}-8=0"),("E",r"|-3x|-4=0")]),
    8: (r"Last summer $30\%$ of the birds living on Town Lake were geese, $25\%$ were swans, $10\%$ were herons, and $35\%$ were ducks. What percent of the birds that were not swans were geese?", [("A","20"),("B","30"),("C","40"),("D","50"),("E","60")]),
    9: (r"A rectangular region is bounded by the graphs of $y=a$, $y=-b$, $x=-c$, and $x=d$, where $a,b,c,d$ are all positive numbers. Which expression represents the area of this region?", [("A",r"ac+ad+bc+bd"),("B",r"ac-ad+bc-bd"),("C",r"ac+ad-bc-bd"),("D",r"-ac-ad+bc+bd"),("E",r"ac-ad-bc+bd")]),
    10: (r"A majority of the $30$ students in Ms. Deameanor's class bought pencils at the school bookstore. Each of these students bought the same number of pencils, and this number was greater than $1$. The cost of a pencil in cents was greater than the number of pencils each student bought, and the total cost of all the pencils was $\$17.71$. What was the cost of a pencil in cents?", [("A","7"),("B","11"),("C","17"),("D","23"),("E","77")]),
}

KEY_OVERRIDES = {
    1: "Break the monthly bill into base cost, text-message cost, and extra-minute cost.",
    2: "Use ceiling division because a partial bottle still requires buying a whole bottle.",
    3: "Evaluate nested averages from the inside outward.",
    4: "Compare two shifted arithmetic sums term by term.",
    5: "Use a weighted average because the grade levels have different numbers of students.",
    6: "The smallest union occurs when the smaller set is entirely contained in the larger set.",
    7: "Check whether each equation can reach zero using squares, square roots, and absolute values.",
    8: "Condition on the group that is not swans, then compute the geese fraction inside that group.",
    9: "Find the rectangle's width and height from coordinate boundaries, then multiply.",
    10: "Factor the total cost into students, pencils per student, and cents per pencil.",
}

SOL = {
    1: [
        ("Separate the parts of the bill", r"The plan has three possible costs: the fixed monthly cost, text messages, and minutes over $30$ hours. Listing these pieces prevents us from mixing hours and minutes."),
        ("Compute the text-message cost", r"Michelle sent $100$ text messages. At $5$ cents each, the text cost is $100\cdot5=500$ cents, or $\$5.00$."),
        ("Compute the extra-minute cost", r"She talked for $30.5$ hours, which is $0.5$ hour over the included $30$ hours. Since $0.5$ hour is $30$ minutes, the extra-minute cost is $30\cdot10=300$ cents, or $\$3.00$."),
        ("Add the costs", r"The total is $\$20.00+\$5.00+\$3.00=\$28.00$. The answer is $\boxed{\$28.00}$."),
    ],
    2: [
        ("Translate the question", r"Each small bottle contributes $35$ milliliters. Jasmine needs enough small bottles so that their total capacity is at least $500$ milliliters."),
        ("Divide to estimate", r"Compute $500\div35$. Since $35\cdot14=490$, fourteen bottles are close but not enough."),
        ("Remember whole bottles", r"Jasmine cannot buy a fraction of a bottle. Because $14$ bottles hold only $490$ milliliters, she needs one more bottle."),
        ("Conclude", r"The minimum number is $15$. The answer is $\boxed{15}$."),
    ],
    3: [
        ("Work from the inside outward", r"The notation is nested, so we first evaluate the expressions inside the outer braces. The average of $1,1,0$ is $\frac{1+1+0}{3}=\frac23$."),
        ("Evaluate the bracketed average", r"Next, $[0\ 1]$ means the average of $0$ and $1$, which is $\frac12$."),
        ("Use the outer average", r"Now the full expression is the average of $\frac23$, $\frac12$, and $0$: \[\frac{\frac23+\frac12+0}{3}.\]"),
        ("Calculate carefully", r"Since $\frac23+\frac12=\frac76$, dividing by $3$ gives $\frac76\cdot\frac13=\frac7{18}$. The answer is $\boxed{\frac7{18}}$."),
    ],
    4: [
        ("Compare the sums instead of evaluating both", r"The two sums have the same number of terms, and most terms overlap. This is a good sign that subtracting term by term will be faster than finding each sum separately."),
        ("Identify what changes", r"The sum $X$ starts with $10$ and ends with $100$. The sum $Y$ starts with $12$ and ends with $102$. All the middle even terms from $12$ through $100$ appear in both sums."),
        ("Cancel the common terms", r"When we compute $Y-X$, the common terms cancel. What remains is $102-10$."),
        ("Finish", r"Therefore $Y-X=92$. The answer is $\boxed{92}$."),
    ],
    5: [
        ("Choose convenient group sizes", r"The fifth grade is the smallest group. Let there be $n$ fifth graders. Then there are $2n$ fourth graders and $4n$ third graders."),
        ("Compute total running time", r"The third graders contribute $4n\cdot12=48n$ minutes. The fourth graders contribute $2n\cdot15=30n$ minutes. The fifth graders contribute $n\cdot10=10n$ minutes."),
        ("Compute total students", r"The total number of students is $4n+2n+n=7n$. The total running time is $48n+30n+10n=88n$."),
        ("Find the weighted average", r"The average is $\frac{88n}{7n}=\frac{88}{7}$. The answer is $\boxed{\frac{88}{7}}$."),
    ],
    6: [
        ("Think about overlap", r"The union $A\cup B$ contains everything that is in either set. To make the union as small as possible, we want the two sets to overlap as much as possible."),
        ("Use the smaller set", r"Set $B$ has only $15$ elements, while set $A$ has $20$. The greatest possible overlap happens when every element of $B$ is already inside $A$."),
        ("Find the union size", r"If $B\subseteq A$, then adding $B$ contributes no new elements beyond the $20$ already in $A$. So the smallest possible union has $20$ elements."),
        ("Conclude", r"The answer is $\boxed{20}$."),
    ],
    7: [
        ("Use basic output facts", r"Squares are always nonnegative, square roots are always nonnegative, and absolute values are always nonnegative. The equation that cannot reach zero will usually be the one that adds a positive number to something nonnegative."),
        ("Check choice B first", r"For choice B, $|-3x|\ge0$ for every real $x$. Therefore $|-3x|+5\ge5$, so it can never equal $0$. This already shows B has no solution."),
        ("Confirm the others are solvable", r"Choice A works with $x=-7$. Choice C works with $x=-4$, since $\sqrt{-(-4)}-2=0$. Choice D works with $x=64$. Choice E works when $|-3x|=4$, such as $x=\frac43$."),
        ("Conclude", r"Only choice B has no solution. The answer is $\boxed{|-3x|+5=0}$."),
    ],
    8: [
        ("Identify the new denominator", r"The question is not asking what percent of all birds were geese. It asks what percent of the birds that were not swans were geese. So we must remove the swans from the denominator."),
        ("Find the non-swan group", r"Since $25\%$ were swans, the non-swan birds make up $100\%-25\%=75\%$ of the birds."),
        ("Compare geese to non-swans", r"Geese are $30\%$ of all birds. Among the non-swans, the geese fraction is $\frac{30}{75}$."),
        ("Convert to a percent", r"The fraction $\frac{30}{75}=\frac25=40\%$. The answer is $\boxed{40}$."),
    ],
    9: [
        ("Find the vertical distance", r"The top boundary is $y=a$ and the bottom boundary is $y=-b$. The height is the difference $a-(-b)=a+b$."),
        ("Find the horizontal distance", r"The left boundary is $x=-c$ and the right boundary is $x=d$. The width is $d-(-c)=c+d$."),
        ("Multiply width and height", r"The rectangle's area is $(a+b)(c+d)$. Expanding gives \[(a+b)(c+d)=ac+ad+bc+bd.\]"),
        ("Conclude", r"The answer is $\boxed{ac+ad+bc+bd}$."),
    ],
    10: [
        ("Translate total cost into factors", r"The total cost was $\$17.71$, or $1771$ cents. This equals \[(\text{number of students})(\text{pencils per student})(\text{cents per pencil}).\]"),
        ("Use the majority condition", r"A majority of $30$ students means more than $15$ students bought pencils. So the number of buying students is an integer factor of $1771$ greater than $15$."),
        ("Factor the total", r"The number factors as $1771=23\cdot77=23\cdot7\cdot11$. Since the pencil cost must be one of the answer choices, we can test which choice leaves a product that can include more than $15$ students and more than $1$ pencil per student."),
        ("Find the consistent choice", r"If the cost is $11$ cents, then $1771\div11=161=23\cdot7$. This works: $23$ students each bought $7$ pencils, and $11>7$."),
        ("Conclude", r"The cost of one pencil was $\boxed{11}$ cents."),
    ],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in set()) else notes
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
        if r["year"] == "2011" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in set(),
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
        + "- Answer verification source: AoPS 2011 AMC 10A Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批无跳过题。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()





















