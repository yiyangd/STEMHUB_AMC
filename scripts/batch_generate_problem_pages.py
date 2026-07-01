import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 112
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2019_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2019 AMC 10B Problems 1-10"
NEXT_START = "2019 AMC 10B Problem 11"

ANS={1:("D",r"\frac9{10}"),2:("E","27"),3:("B","154"),4:("A",r"(-1,2)"),5:("E","Lines $AB$ and $A'B'$ are perpendicular to each other."),6:("C","10"),7:("B","21"),8:("B",r"12-4\sqrt3"),9:("A",r"\{-1,0\}"),10:("A","0")}

OV={
1:(r"Alicia had two containers. The first was $\frac56$ full of water and the second was empty. She poured all the water from the first container into the second container, at which point the second container was $\frac34$ full of water. What is the ratio of the volume of the first container to the volume of the second container?",[("A",r"$\frac58$"),("B",r"$\frac45$"),("C",r"$\frac78$"),("D",r"$\frac9{10}$"),("E",r"$\frac{11}{12}$")]),
2:(r"Consider the statement, \"If $n$ is not prime, then $n-2$ is prime.\" Which of the following values of $n$ is a counterexample to this statement?",[("A","11"),("B","15"),("C","19"),("D","21"),("E","27")]),
3:(r"In a high school with $500$ students, $40\%$ of the seniors play a musical instrument, while $30\%$ of the non-seniors do not play a musical instrument. In all, $46.8\%$ of the students do not play a musical instrument. How many non-seniors play a musical instrument?",[("A","66"),("B","154"),("C","186"),("D","220"),("E","266")]),
4:(r"All lines with equation $ax+by=c$ such that $a,b,c$ form an arithmetic progression pass through a common point. What are the coordinates of that point?",[("A",r"$(-1,2)$"),("B",r"$(0,1)$"),("C",r"$(1,-2)$"),("D",r"$(1,0)$"),("E",r"$(1,2)$")]),
5:(r"Triangle $ABC$ lies in the first quadrant. Points $A,B,C$ are reflected across the line $y=x$ to points $A',B',C'$, respectively. Assume that none of the vertices lie on $y=x$. Which statement is not always true?",[("A",r"Triangle $A'B'C'$ lies in the first quadrant."),("B",r"Triangles $ABC$ and $A'B'C'$ have the same area."),("C",r"The slope of line $AA'$ is $-1$."),("D",r"The slopes of lines $AA'$ and $CC'$ are the same."),("E",r"Lines $AB$ and $A'B'$ are perpendicular to each other.")]),
6:(r"A positive integer $n$ satisfies \[(n+1)!+(n+2)!=n!\cdot440.\] What is the sum of the digits of $n$?",[("A","2"),("B","5"),("C","10"),("D","12"),("E","15")]),
7:(r"Each piece of candy in a store costs a whole number of cents. Casper has exactly enough money to buy either $12$ red candies, $14$ green candies, $15$ blue candies, or $n$ purple candies. A purple candy costs $20$ cents. What is the smallest possible value of $n$?",[("A","18"),("B","21"),("C","24"),("D","25"),("E","28")]),
8:(r"A square and four equilateral triangles are arranged so that each triangle has a side lying on a side of the square, each triangle has side length $2$, and the third vertices of the triangles meet at the center of the square. The region inside the square but outside the triangles is shaded. What is the area of the shaded region?",[("A","4"),("B",r"$12-4\sqrt3$"),("C",r"$3\sqrt3$"),("D",r"$4\sqrt3$"),("E",r"$16-\sqrt3$")]),
9:(r"The function $f$ is defined by \[f(x)=\lfloor |x|\rfloor-|\lfloor x\rfloor|\] for all real numbers $x$, where $\lfloor r\rfloor$ is the greatest integer less than or equal to $r$. What is the range of $f$?",[("A",r"$\{-1,0\}$"),("B","The set of nonpositive integers"),("C",r"$\{-1,0,1\}$"),("D",r"$\{0\}$"),("E","The set of nonnegative integers")]),
10:(r"In a given plane, points $A$ and $B$ are $10$ units apart. How many points $C$ are there in the plane such that the perimeter of $\triangle ABC$ is $50$ units and the area of $\triangle ABC$ is $100$ square units?",[("A","0"),("B","2"),("C","4"),("D","8"),("E","infinitely many")]),
}

KEY_OVERRIDES={1:"Represent the same water volume two ways.",2:"A counterexample must make the hypothesis true and the conclusion false.",3:"Set up equations from percentages.",4:"Use the arithmetic progression condition to rewrite the line equation.",5:"Understand how reflection across $y=x$ affects slopes.",6:"Factor out $n!$.",7:"Use least common multiples.",8:"Subtract the four equilateral triangle areas from the square area.",9:"Separate $x\ge0$ and $x<0$.",10:"Use base-height area and the triangle inequality."}

SOL={
1:[("Name the container volumes",r"Let the volume of the first container be $F$ and the volume of the second be $S$. The actual amount of water does not change when Alicia pours it."),("Write the same water amount two ways",r"The first container was $\frac56$ full, so the water volume was \[\frac56F.\] After pouring, the second container was $\frac34$ full, so the same water volume was \[\frac34S.\]"),("Set up the equation",r"Thus \[\frac56F=\frac34S.\]"),("Solve for the ratio",r"\[\frac{F}{S}=\frac{3/4}{5/6}=\frac34\cdot\frac65=\frac9{10}.\]"),("Conclude",r"The answer is $\boxed{\frac9{10}}$."),],
2:[("Recall what a counterexample must do",r"A counterexample to an if-then statement must make the hypothesis true and the conclusion false."),("Apply the hypothesis",r"The hypothesis says $n$ is not prime. So we only test answer choices that are not prime: $15,21,$ and $27$."),("Test the conclusion",r"For $n=15$, $n-2=13$ is prime. For $n=21$, $n-2=19$ is prime. For $n=27$, $n-2=25$ is not prime."),("Identify the counterexample",r"The value $27$ makes the hypothesis true but the conclusion false."),("Conclude",r"The answer is $\boxed{27}$."),],
3:[("Set variables",r"Let $S$ be the number of seniors. Then $500-S$ students are non-seniors."),("Translate not playing an instrument",r"If $40\%$ of seniors play, then $60\%$ of seniors do not play. If $30\%$ of non-seniors do not play, then the total number who do not play is \[0.60S+0.30(500-S).\]"),("Use the total percentage",r"Since $46.8\%$ of $500$ students do not play, that number is \[0.468\cdot500=234.\] So \[0.60S+0.30(500-S)=234.\]"),("Solve for seniors",r"\[0.30S+150=234,\] so \[S=280.\] Therefore there are $500-280=220$ non-seniors."),("Find non-seniors who play",r"Since $30\%$ of non-seniors do not play, $70\%$ do play. Thus \[0.70\cdot220=154.\]"),("Conclude",r"The answer is $\boxed{154}$."),],
4:[("Use the arithmetic progression condition",r"If $a,b,c$ form an arithmetic progression, then \[b=\frac{a+c}{2},\] so \[c=2b-a.\]"),("Substitute into the line",r"The line equation becomes \[ax+by=2b-a.\] Move all terms to one side: \[a(x+1)+b(y-2)=0.\]"),("Find a point that works for all a and b",r"For this equation to hold for every allowed arithmetic progression, both coefficients must be zero: \[x+1=0,\qquad y-2=0.\]"),("Solve",r"This gives \[x=-1,\qquad y=2.\]"),("Conclude",r"All such lines pass through $\boxed{(-1,2)}$."),],
5:[("Understand the reflection",r"Reflecting across $y=x$ swaps coordinates: $(u,v)$ becomes $(v,u)$. This preserves distances, area, and the first quadrant."),("Check the always-true statements",r"Because reflection is an isometry, the reflected triangle has the same area. Also the segment from a point to its reflection is perpendicular to $y=x$, so each line like $AA'$ has slope $-1$."),("Analyze slopes of reflected lines",r"If a line has slope $m$, then after reflecting across $y=x$, its slope becomes $\frac1m$ when both slopes are defined."),("Test perpendicularity",r"For two lines to be perpendicular, their slopes should multiply to $-1$. But \[m\cdot\frac1m=1,\] not $-1$."),("Conclude",r"Thus lines $AB$ and $A'B'$ are not always perpendicular. The answer is $\boxed{\text{E}}$."),],
6:[("Factor out n!",r"Use \[(n+1)!=(n+1)n!,\qquad (n+2)!=(n+2)(n+1)n!.\]"),("Rewrite the equation",r"The left side becomes \[n!\big((n+1)+(n+2)(n+1)\big)=n!(n+1)(n+3).\]"),("Cancel n!",r"Since $n!>0$, the equation reduces to \[(n+1)(n+3)=440.\]"),("Solve",r"The factor pair $20\cdot22=440$ gives \[n+1=20,\qquad n+3=22,\] so $n=19$."),("Conclude",r"The sum of the digits of $19$ is $1+9=\boxed{10}$."),],
7:[("Translate the money condition",r"Let Casper's amount of money be $M$ cents. Because candy prices are whole numbers of cents, $M$ must be divisible by $12$, $14$, and $15$."),("Find the smallest possible money amount",r"The least common multiple is \[\operatorname{lcm}(12,14,15)=420.\]"),("Use purple candy",r"Purple candy costs $20$ cents, so if $M=420$, then \[n=\frac{420}{20}=21.\]"),("Check minimality",r"Any smaller amount that works for the first three colors would have to be a smaller positive multiple of $420$, which is impossible."),("Conclude",r"The smallest possible value of $n$ is $\boxed{21}$."),],
8:[("Use the triangle height",r"Each equilateral triangle has side length $2$, so its height is \[\frac{\sqrt3}{2}\cdot2=\sqrt3.\] Since the third vertices meet at the center of the square, the distance from the center to each side of the square is $\sqrt3$."),("Find the square area",r"The square's side length is twice that distance: \[2\sqrt3.\] So the area of the square is \[(2\sqrt3)^2=12.\]"),("Find the triangle areas",r"Each equilateral triangle has area \[\frac{\sqrt3}{4}\cdot2^2=\sqrt3.\] Four such triangles have total area $4\sqrt3$."),("Subtract",r"The shaded region is inside the square but outside the four triangles, so its area is \[12-4\sqrt3.\]"),("Conclude",r"The answer is $\boxed{12-4\sqrt3}$."),],
9:[("Consider nonnegative x",r"If $x\ge0$, then $|x|=x$ and $\lfloor x\rfloor\ge0$. Therefore \[f(x)=\lfloor x\rfloor-|\lfloor x\rfloor|=0.\]"),("Consider negative integers",r"If $x$ is a negative integer, then $|x|$ is a positive integer and $|\lfloor x\rfloor|=|x|$, so again $f(x)=0$."),("Consider negative nonintegers",r"Let $x=-m-\alpha$, where $m$ is a nonnegative integer and $0<\alpha<1$. Then \[\lfloor |x|\rfloor=m,\qquad \lfloor x\rfloor=-m-1,\] so \[|\lfloor x\rfloor|=m+1.\]"),("Find the value",r"For negative nonintegers, \[f(x)=m-(m+1)=-1.\]"),("Conclude",r"The range is $\boxed{\{-1,0\}}$."),],
10:[("Use the area to find the height",r"Take $AB$ as the base. Since $AB=10$ and the area is $100$, the height from $C$ to line $AB$ must satisfy \[\frac12\cdot10\cdot h=100.\] Thus $h=20$."),("Use the perimeter condition",r"The perimeter is $50$, so \[AC+BC=40.\]"),("Find the smallest possible AC+BC at height 20",r"For points $C$ at distance $20$ from line $AB$, the shortest possible value of $AC+BC$ occurs above the midpoint of $AB$. That minimum is \[2\sqrt{5^2+20^2}=2\sqrt{425}>40.\]"),("Compare",r"Even the smallest possible value of $AC+BC$ is greater than $40$, so the perimeter condition cannot be met."),("Conclude",r"There are $\boxed{0}$ possible points $C$."),],
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












































