import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 104
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2018_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11,12,14,15,16,17,18,19,20}
SKIPPED = ["2018 AMC 10A Problem 13 skipped: folding crease length depends on the missing triangle diagram."]
BATCH_LABEL = "2018 AMC 10A Problems 11-12, 14-20"
NEXT_START = "2018 AMC 10A Problem 21"

ANS={11:("E","84"),12:("C","3"),14:("A","80"),15:("D","69"),16:("D","13"),17:("C","4"),18:("D","3281"),19:("E",r"\frac25"),20:("B","1022")}

OV={
11:(r"When $7$ fair standard $6$-sided dice are thrown, the probability that the sum of the numbers on the top faces is $10$ can be written as $\frac{n}{6^7}$, where $n$ is a positive integer. What is $n$?",[("A","42"),("B","49"),("C","56"),("D","63"),("E","84")]),
12:(r"How many ordered pairs of real numbers $(x,y)$ satisfy the system $x+3y=3$ and $\big||x|-|y|\big|=1$?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","8")]),
14:(r"What is the greatest integer less than or equal to $\frac{3^{100}+2^{100}}{3^{96}+2^{96}}$?",[("A","80"),("B","81"),("C","96"),("D","97"),("E","625")]),
15:(r"Two circles of radius $5$ are externally tangent to each other and are internally tangent to a circle of radius $13$ at points $A$ and $B$. The distance $AB$ can be written in the form $\frac{m}{n}$, where $m$ and $n$ are relatively prime positive integers. What is $m+n$?",[("A","21"),("B","29"),("C","58"),("D","69"),("E","93")]),
16:(r"Right triangle $ABC$ has leg lengths $AB=20$ and $BC=21$. Including $AB$ and $BC$, how many line segments with integer length can be drawn from vertex $B$ to a point on hypotenuse $AC$?",[("A","5"),("B","8"),("C","12"),("D","13"),("E","15")]),
17:(r"Let $S$ be a set of $6$ integers taken from $\{1,2,\ldots,12\}$ with the property that if $a$ and $b$ are elements of $S$ with $a<b$, then $b$ is not a multiple of $a$. What is the least possible value of an element in $S$?",[("A","2"),("B","3"),("C","4"),("D","5"),("E","7")]),
18:(r"How many nonnegative integers can be written in the form $a_7\cdot3^7+a_6\cdot3^6+\cdots+a_1\cdot3+a_0$, where $a_i\in\{-1,0,1\}$ for $0\le i\le7$?",[("A","512"),("B","729"),("C","1094"),("D","3281"),("E","59048")]),
19:(r"A number $m$ is randomly selected from $\{11,13,15,17,19\}$, and a number $n$ is randomly selected from $\{1999,2000,2001,\ldots,2018\}$. What is the probability that $mn$ has a units digit of $1$?",[("A",r"$\frac15$"),("B",r"$\frac14$"),("C",r"$\frac3{10}$"),("D",r"$\frac7{20}$"),("E",r"$\frac25$")]),
20:(r"A scanning code consists of a $7\times7$ grid of squares, with some squares colored black and the rest white. There must be at least one square of each color. A scanning code is called symmetric if it does not change under rotations by multiples of $90^\circ$ or reflections across diagonals or midlines of the square. What is the total number of possible symmetric scanning codes?",[("A","510"),("B","1022"),("C","8190"),("D","8192"),("E","65,534")]),
}

KEY_OVERRIDES={11:"Count positive integer dice outcomes with stars and bars.",12:"Split the absolute-value equation into linear cases.",14:"Factor powers and bound the expression between consecutive integers.",15:"Use similar triangles formed by the centers and tangency points.",16:"Count circle-hypotenuse intersections for each possible integer distance.",17:"Use divisibility restrictions to rule out smaller minimum elements.",18:"Use uniqueness and symmetry of balanced ternary representations.",19:"Count compatible units digits.",20:"Count orbits of grid cells under the full square symmetry group."}

SOL={
11:[("Translate the dice condition",r"Let the seven dice show $x_1,\ldots,x_7$, where each $x_i\ge1$. We need \[x_1+x_2+\cdots+x_7=10.\]"),("Remove the minimum value",r"Set $y_i=x_i-1$. Then $y_i\ge0$ and \[y_1+\cdots+y_7=3.\]"),("Use stars and bars",r"The number of nonnegative solutions is \[\binom{3+7-1}{7-1}=\binom96=84.\] Since the sum is only $10$, no die can exceed $6$, so no extra restriction is needed."),("Connect to probability",r"There are $6^7$ total equally likely outcomes, so $n=84$."),("Conclude",r"The answer is $\boxed{84}$."),],
12:[("Split the absolute value",r"The equation $\big||x|-|y|\big|=1$ means either $|x|-|y|=1$ or $|y|-|x|=1$."),("Consider linear sign cases",r"This creates four line possibilities: $x=y+1$, $x=-y+1$, $x=y-1$, and $x=-y-1$, together with suitable signs. We can intersect these candidate lines with $x+3y=3$."),("Find the distinct solutions",r"Checking the sign-consistent cases gives \[(x,y)=\left(\frac32,\frac12\right),\quad (0,1),\quad (-3,2).\]"),("Verify",r"Each satisfies $x+3y=3$ and $\big||x|-|y|\big|=1$."),("Conclude",r"There are $\boxed{3}$ ordered pairs."),],
14:[("Factor out the smaller powers",r"\[\frac{3^{100}+2^{100}}{3^{96}+2^{96}}=\frac{81\cdot3^{96}+16\cdot2^{96}}{3^{96}+2^{96}}.\]"),("Show it is less than 81",r"The numerator is less than $81(3^{96}+2^{96})$, so the fraction is less than $81$."),("Show it is greater than 80",r"To be greater than $80$, we need \[81\cdot3^{96}+16\cdot2^{96}>80\cdot3^{96}+80\cdot2^{96},\] which reduces to \[3^{96}>64\cdot2^{96}.\] This is true because \[\left(\frac32\right)^{96}>2^6=64.\]"),("Conclude the floor",r"The expression is between $80$ and $81$, so the greatest integer less than or equal to it is $\boxed{80}$."),],
15:[("Use the centers",r"Let $X$ be the center of the large circle and $Y,Z$ the centers of the two smaller circles. Since the small circles are internally tangent to the large circle, $XY=XZ=13-5=8$."),("Use external tangency",r"The two small circles are externally tangent, so $YZ=5+5=10$."),("Relate center triangle to tangent-point triangle",r"The tangent points $A$ and $B$ lie on rays $XY$ and $XZ$. Thus $\triangle XAB$ is similar to $\triangle XYZ$."),("Scale lengths",r"The scale factor from $\triangle XYZ$ to $\triangle XAB$ is \[\frac{XA}{XY}=\frac{13}{8}.\] Therefore \[\frac{AB}{YZ}=\frac{13}{8},\quad AB=10\cdot\frac{13}{8}=\frac{65}{4}.\]"),("Find m plus n",r"Thus $m=65$ and $n=4$, so $m+n=69$."),("Conclude",r"The answer is $\boxed{69}$."),],
16:[("Think of circles centered at B",r"A segment from $B$ to the hypotenuse has length $r$ exactly when the circle centered at $B$ with radius $r$ intersects segment $AC$."),("Find the shortest possible distance",r"The shortest distance from $B$ to hypotenuse $AC$ is the altitude. Since the right triangle has legs $20$ and $21$ and hypotenuse $29$, the altitude is \[\frac{20\cdot21}{29}=\frac{420}{29}\approx14.48.\]"),("List possible integer lengths",r"The maximum distance to the hypotenuse occurs at endpoint $C$, giving length $21$. Thus integer lengths can be $15,16,17,18,19,20,21$."),("Count intersections",r"For each length $15$ through $20$, the circle intersects the hypotenuse in two points. For length $21$, it intersects at endpoint $C$ only."),("Add",r"The number of segments is \[6\cdot2+1=13.\]"),("Conclude",r"The answer is $\boxed{13}$."),],
17:[("Show 4 is possible",r"The set \[\{4,6,7,9,10,11\}\] works: no larger element in the set is a multiple of a smaller one. So the least possible value is at most $4$."),("Rule out 1",r"If $1$ were in the set, every other positive integer would be a multiple of it, so no set of size $6$ could work."),("Rule out 2",r"If $2$ is the least element, then all even numbers greater than $2$ are forbidden. The only possible additional elements are among $3,5,7,9,11$, but $9$ is a multiple of $3$, so we cannot get five compatible additional elements."),("Rule out 3",r"If $3$ is the least element, then $6,9,12$ are forbidden. Among the remaining candidates, pairs like $4,8$ and $5,10$ cannot both be chosen, so again we cannot make a valid set of six."),("Conclude",r"The least possible value is $\boxed{4}$."),],
18:[("Recognize balanced ternary",r"The expression uses powers of $3$ with coefficients $-1$, $0$, and $1$. Such a representation is unique: if two different coefficient choices gave the same number, their difference would give a nontrivial base-$3$ representation with coefficients too small to cancel the highest nonzero term."),("Count all represented integers",r"There are $3^8$ choices for the coefficients $a_0,\ldots,a_7$, so there are $3^8=6561$ represented integers."),("Use symmetry",r"For every positive represented integer, changing every coefficient sign gives the corresponding negative integer. The value $0$ is represented once."),("Count nonnegative values",r"Therefore the number of nonnegative represented integers is \[\frac{6561+1}{2}=3281.\]"),("Conclude",r"The answer is $\boxed{3281}$."),],
19:[("Use units digits only",r"The units digit of $mn$ depends only on the units digits of $m$ and $n$."),("Count n by units digit",r"The integers from $1999$ through $2018$ are $20$ consecutive integers, so each units digit occurs exactly twice."),("Check each m",r"For $m$ ending in $1$, $n$ must end in $1$: $2$ choices. For $m$ ending in $3$, $n$ must end in $7$: $2$ choices. For $m$ ending in $7$, $n$ must end in $3$: $2$ choices. For $m$ ending in $9$, $n$ must end in $9$: $2$ choices. For $m=15$, no units digit makes the product end in $1$."),("Compute probability",r"There are $5\cdot20=100$ equally likely pairs and $8$ favorable pairs, so the probability is \[\frac8{100}=\frac25.\]"),("Conclude",r"The answer is $\boxed{\frac25}$."),],
20:[("Find the independent cell groups",r"A fully symmetric $7\times7$ grid must be constant on each orbit of cells under the symmetries of the square."),("Count the orbits",r"For a $7\times7$ grid, these symmetries create $10$ cell orbits. One way to see this is to classify cells by their sorted distances from the center in horizontal and vertical directions."),("Choose colors by orbit",r"Each orbit can independently be colored black or white, so there are \[2^{10}=1024\] symmetric colorings before the color condition."),("Exclude one-color grids",r"The problem requires at least one square of each color, so exclude the all-black and all-white grids."),("Conclude",r"The total is \[1024-2=\boxed{1022}.\]"),],
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
        if r["year"] == "2018" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2018 AMC 10A Answer Key\n\n"
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












































