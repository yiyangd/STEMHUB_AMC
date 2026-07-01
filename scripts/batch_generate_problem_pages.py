import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 109
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2019_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,9,10}
SKIPPED = ["2019 AMC 10A Problem 8 skipped: symmetry question depends on the missing recurring-pattern figure."]
BATCH_LABEL = "2019 AMC 10A Problems 1-7,9-10"
NEXT_START = "2019 AMC 10A Problem 11"

ANS={1:("C","2"),2:("A","0"),3:("D","12"),4:("B","76"),5:("D","90"),6:("C","3"),7:("C","6"),9:("B","996"),10:("C","26")}

OV={
1:(r"What is the value of \[2^{\left(0^{\left(1^9\right)}\right)}+\left(\left(2^0\right)^1\right)^9?\]",[("A","0"),("B","1"),("C","2"),("D","3"),("E","4")]),
2:(r"What is the hundreds digit of $20!-15!$?",[("A","0"),("B","1"),("C","2"),("D","4"),("E","5")]),
3:(r"Ana and Bonita were born on the same date in different years, $n$ years apart. Last year Ana was $5$ times as old as Bonita. This year Ana's age is the square of Bonita's age. What is $n$?",[("A","3"),("B","5"),("C","9"),("D","12"),("E","15")]),
4:(r"A box contains $28$ red balls, $20$ green balls, $19$ yellow balls, $13$ blue balls, $11$ white balls, and $9$ black balls. What is the minimum number of balls that must be drawn from the box without replacement to guarantee that at least $15$ balls of a single color will be drawn?",[("A","75"),("B","76"),("C","79"),("D","84"),("E","91")]),
5:(r"What is the greatest number of consecutive integers whose sum is $45$?",[("A","9"),("B","25"),("C","45"),("D","90"),("E","120")]),
6:(r"For how many of the following types of quadrilaterals does there exist a point in the plane of the quadrilateral that is equidistant from all four vertices: a square; a rectangle that is not a square; a rhombus that is not a square; a parallelogram that is not a rectangle or a rhombus; an isosceles trapezoid that is not a parallelogram?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
7:(r"Two lines with slopes $\frac12$ and $2$ intersect at $(2,2)$. What is the area of the triangle enclosed by these two lines and the line $x+y=10$?",[("A","4"),("B",r"$4\sqrt2$"),("C","6"),("D","8"),("E",r"$6\sqrt2$")]),
9:(r"What is the greatest three-digit positive integer $n$ for which the sum of the first $n$ positive integers is not a divisor of the product of the first $n$ positive integers?",[("A","995"),("B","996"),("C","997"),("D","998"),("E","999")]),
10:(r"A rectangular floor that is $10$ feet wide and $17$ feet long is tiled with $170$ one-foot square tiles. A bug walks from one corner to the opposite corner in a straight line. Including the first and the last tile, how many tiles does the bug visit?",[("A","17"),("B","25"),("C","26"),("D","27"),("E","28")]),
}

KEY_OVERRIDES={1:"Evaluate exponent towers from the inside out.",2:"Use divisibility by $1000$ to get the hundreds digit.",3:"Translate the age conditions into equations.",4:"Use the pigeonhole principle with the largest number that still avoids 15 of one color.",5:"Use symmetric consecutive integers around zero.",6:"Recognize which quadrilaterals are cyclic.",7:"Find the three line intersections and compute triangle area.",9:"Analyze when $\frac{n(n+1)}2$ divides $n!$.",10:"Use the grid-line crossing formula $m+n-\gcd(m,n)$."}

SOL={
1:[("Work from the inside outward",r"Exponent expressions should be evaluated from the top or innermost part first. Here $1^9=1$, so the exponent on $0$ is $1$."),("Evaluate the first term",r"Thus \[0^{(1^9)}=0^1=0,\] and the first term is \[2^0=1.\]"),("Evaluate the second term",r"In the second term, \[2^0=1,\quad (2^0)^1=1^1=1,\] and then \[\left((2^0)^1\right)^9=1^9=1.\]"),("Add",r"The whole expression is \[1+1=2.\]"),("Conclude",r"The answer is $\boxed{2}$."),],
2:[("Look only at the last three digits",r"The hundreds digit is determined by the number modulo $1000$. We do not need to compute the factorials."),("Factor the expression",r"\[20!-15!=15!(16\cdot17\cdot18\cdot19\cdot20-1).\]"),("Notice the factor 1000",r"The number $15!$ contains at least three factors of $2$ and three factors of $5$, so $1000\mid15!$."),("Use divisibility",r"Therefore $20!-15!$ is divisible by $1000$, no matter what the second factor is."),("Conclude",r"The last three digits are $000$, so the hundreds digit is $\boxed{0}$."),],
3:[("Name the younger age",r"Let Bonita's age this year be $b$. Since Ana's age this year is the square of Bonita's age, Ana is $b^2$ years old."),("Translate last year's condition",r"Last year Bonita was $b-1$ and Ana was $b^2-1$. The condition says \[b^2-1=5(b-1).\]"),("Solve the equation",r"Rearrange: \[b^2-1=5b-5\quad\Rightarrow\quad b^2-5b+4=0.\] So \[(b-1)(b-4)=0.\]"),("Choose the meaningful age",r"The value $b=1$ would make Bonita age $0$ last year, which does not fit the statement that Ana was $5$ times as old as Bonita. Thus $b=4$."),("Find the age gap",r"Ana is $b^2=16$ this year, and Bonita is $4$, so \[n=16-4=12.\]"),("Conclude",r"The answer is $\boxed{12}$."),],
4:[("Think about the worst case",r"To guarantee $15$ balls of one color, first imagine drawing as many balls as possible while still avoiding that outcome."),("Cap each color below 15",r"For red, green, and yellow, we can draw at most $14$ of each without reaching $15$. For blue, white, and black, we can draw all of them because their totals are below $15$."),("Add the safe maximum",r"The maximum number drawn without having $15$ of one color is \[14+14+14+13+11+9=75.\]"),("Force the guarantee",r"After $75$ draws, it is still possible to avoid $15$ of any color. The next draw must create $15$ of some color."),("Conclude",r"The minimum guaranteed number is \[75+1=\boxed{76}.\]"),],
5:[("Remember that consecutive integers may include negatives",r"To make many consecutive integers have a relatively small positive sum, we should center the list near $0$ so negative and positive terms cancel."),("Use a symmetric block",r"The integers \[-44,-43,\ldots,-1,0,1,\ldots,44\] sum to $0$ and contain $89$ integers."),("Add one more integer",r"If we append $45$, the sum becomes \[0+45=45.\] The list from $-44$ to $45$ contains \[45-(-44)+1=90\] consecutive integers."),("Explain why this is maximal",r"If $k$ consecutive integers start at $a$, their sum is \[\frac{k(2a+k-1)}2=45.\] Thus \[k(2a+k-1)=90,\] so $k$ must be a positive divisor of $90$. No value of $k$ can exceed $90$."),("Conclude",r"The construction with $90$ integers is maximal, so the answer is $\boxed{90}$."),],
6:[("Translate the condition",r"A point equidistant from all four vertices is the center of a circle passing through all four vertices. So the question asks which quadrilaterals are always cyclic."),("Count rectangles",r"Every rectangle is cyclic because its diagonals are equal and bisect each other. This includes the square and the non-square rectangle, giving two types."),("Check rhombi and general parallelograms",r"A rhombus is cyclic only when it is a square, so a non-square rhombus does not always work. A parallelogram is cyclic only when it is a rectangle, so the listed non-rectangle parallelogram also does not work."),("Check isosceles trapezoids",r"Every isosceles trapezoid is cyclic. Its base angles match in pairs, which makes opposite angles supplementary."),("Conclude",r"The working types are square, non-square rectangle, and non-parallelogram isosceles trapezoid: $3$ types. The answer is $\boxed{3}$."),],
7:[("Write equations for the two sloped lines",r"The line with slope $\frac12$ through $(2,2)$ is \[y-2=\frac12(x-2),\] so \[y=\frac{x}{2}+1.\] The line with slope $2$ is \[y-2=2(x-2),\] so \[y=2x-2.\]"),("Find intersections with the third line",r"The third line is $x+y=10$, or $y=10-x$. Intersecting with $y=\frac{x}{2}+1$ gives $(6,4)$. Intersecting with $y=2x-2$ gives $(4,6)$."),("Identify the triangle",r"The three vertices are \[(2,2),\quad(6,4),\quad(4,6).\] This coordinate setup makes the area straightforward."),("Compute area by determinant",r"Using vectors from $(2,2)$, \[\vec u=(4,2),\qquad \vec v=(2,4).\] The area is \[\frac12|4\cdot4-2\cdot2|=\frac12(12)=6.\]"),("Conclude",r"The answer is $\boxed{6}$."),],
9:[("Rewrite the divisibility question",r"The sum of the first $n$ positive integers is \[\frac{n(n+1)}2,\] and the product is $n!$. We need the greatest three-digit $n$ for which this sum does not divide $n!$."),("Check odd n",r"If $n$ is odd, then \[\frac{n(n+1)}2=n\cdot\frac{n+1}{2}.\] Both factors are at most $n$, and they are relatively prime, so this product divides $n!$."),("Check large candidates",r"The greatest three-digit number $999$ is odd, so it works as a divisor and is not the answer. The number $998$ is even, and \[\frac{998\cdot999}{2}=499\cdot999.\] The factors of $999$ are all present in $998!$, so this also divides $998!$."),("Find the first failure",r"For $n=996$, \[\frac{996\cdot997}{2}=498\cdot997.\] The factor $997$ is prime and greater than $996$, so it cannot appear in $996!$."),("Conclude",r"Therefore the greatest three-digit $n$ for which the sum does not divide the product is $\boxed{996}$."),],
10:[("Think about grid crossings",r"A straight diagonal path enters a new tile whenever it crosses an interior vertical or horizontal grid line. Starting tile counts as one."),("Count vertical and horizontal crossings",r"In a $10$ by $17$ rectangle, the path crosses $9$ interior vertical grid lines and $16$ interior horizontal grid lines."),("Avoid double-counting corner crossings",r"If the path goes exactly through an interior grid intersection, a vertical and horizontal crossing happen at the same time. The number of such interior intersections is \[\gcd(10,17)-1=0,\] since $10$ and $17$ are relatively prime."),("Compute the number of tiles",r"The number of visited tiles is \[1+9+16-0=26.\] Equivalently, this is \[10+17-\gcd(10,17)=26.\]"),("Conclude",r"The bug visits $\boxed{26}$ tiles."),],
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












































