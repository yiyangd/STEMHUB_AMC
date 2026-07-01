import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 108
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2018_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2018 AMC 10B Problems 21-25"
NEXT_START = "2019 AMC 10A Problem 1"

ANS={21:("C","340"),22:("C","0.29"),23:("B","2"),24:("C",r"\frac{15\sqrt3}{32}"),25:("C","199")}

OV={
21:(r"Mary chose an even $4$-digit number $n$. She wrote down all the divisors of $n$ in increasing order. At some moment Mary wrote $323$ as a divisor of $n$. What is the smallest possible value of the next divisor written to the right of $323$?",[("A","324"),("B","330"),("C","340"),("D","361"),("E","646")]),
22:(r"Real numbers $x$ and $y$ are chosen independently and uniformly at random from the interval $[0,1]$. Which of the following numbers is closest to the probability that $x,y,$ and $1$ are the side lengths of an obtuse triangle?",[("A","0.21"),("B","0.25"),("C","0.29"),("D","0.50"),("E","0.79")]),
23:(r"How many ordered pairs $(a,b)$ of positive integers satisfy \[ab+63=20\operatorname{lcm}(a,b)+12\gcd(a,b),\] where $\gcd(a,b)$ denotes the greatest common divisor of $a$ and $b$, and $\operatorname{lcm}(a,b)$ denotes their least common multiple?",[("A","0"),("B","2"),("C","4"),("D","6"),("E","8")]),
24:(r"Let $ABCDEF$ be a regular hexagon with side length $1$. Denote by $X,Y,$ and $Z$ the midpoints of $AB,CD,$ and $EF$, respectively. What is the area of the convex hexagon whose interior is the intersection of the interiors of $\triangle ACE$ and $\triangle XYZ$?",[("A",r"$\frac{3\sqrt3}{8}$"),("B",r"$\frac{7\sqrt3}{16}$"),("C",r"$\frac{15\sqrt3}{32}$"),("D",r"$\frac{\sqrt3}{2}$"),("E",r"$\frac{9\sqrt3}{16}$")]),
25:(r"Let $\lfloor x\rfloor$ denote the greatest integer less than or equal to $x$. How many real numbers $x$ satisfy the equation \[x^2+10000\lfloor x\rfloor=10000x?\]",[("A","197"),("B","198"),("C","199"),("D","200"),("E","201")]),
}

KEY_OVERRIDES={21:"Use least common multiples to test which next divisor can occur in a 4-digit even multiple of 323.",22:"Translate the probability into an area in the unit square.",23:"Write $a=gx$ and $b=gy$ with $\gcd(x,y)=1$.",24:"Use coordinates and polygon intersection area.",25:"Fix $\lfloor x\rfloor$ and count intervals that contain a solution."}

SOL={
21:[("Factor the known divisor",r"The divisor $323$ factors as \[323=17\cdot19.\] Since $n$ is even and $323\mid n$, the number $n$ must be an even multiple of $323$."),("Think about what the next divisor means",r"We want the smallest possible divisor larger than $323$ that can appear next. If a candidate $d$ is the next divisor, then $n$ must be a multiple of both $323$ and $d$, so $n$ must be a multiple of $\operatorname{lcm}(323,d)$."),("Eliminate smaller answer choices",r"For $d=324$ or $d=330$, the greatest common divisor with $323$ is $1$. Thus the least common multiples are already larger than $10000$, so no $4$-digit $n$ can have both $323$ and either of these as divisors."),("Test 340",r"For $d=340$, we have \[\operatorname{lcm}(323,340)=6460,\] because the two numbers share the factor $17$. This is an even $4$-digit number."),("Check that it really works",r"The divisors of $6460$ immediately around $323$ are \[\cdots,190,323,340,380,\cdots.\] Therefore $340$ can indeed be the next divisor after $323$."),("Conclude",r"The smallest possible next divisor is $\boxed{340}$."),],
22:[("Draw the sample space mentally",r"The pair $(x,y)$ is chosen uniformly from the unit square $0\le x\le1$, $0\le y\le1$. So the desired probability is an area."),("Apply the triangle inequality",r"Since the third side is $1$, the numbers form a triangle exactly when \[x+y>1.\] This is the region above the diagonal line $x+y=1$."),("Apply the obtuse condition",r"Because $x$ and $y$ are at most $1$, the side of length $1$ is the longest side. The triangle is obtuse when \[1^2>x^2+y^2.\] This is the inside of the quarter circle $x^2+y^2<1$."),("Find the area",r"The desired region is inside the quarter circle but above the triangle $x+y\le1$. Its area is \[\frac{\pi}{4}-\frac12\approx0.7854-0.5=0.2854.\]"),("Choose the closest option",r"The closest listed value is $0.29$."),("Conclude",r"The answer is $\boxed{0.29}$."),],
23:[("Use gcd and relatively prime parts",r"Let $g=\gcd(a,b)$, and write \[a=gx,\qquad b=gy,\] where $\gcd(x,y)=1$. Then $\operatorname{lcm}(a,b)=gxy$."),("Substitute into the equation",r"The equation becomes \[g^2xy+63=20gxy+12g.\] Rearranging gives \[gxy(g-20)=12g-63.\]"),("Bound possible g values",r"If $g>20$, both sides are positive. Also $xy\ge1$, so \[g(g-20)\le12g-63.\] This forces $g$ to be between $21$ and $29$. If $g\le20$, a quick check of the signs and small values gives no valid positive integer $xy$."),("Test the possible values",r"For $21\le g\le29$, the formula \[xy=\frac{12g-63}{g(g-20)}\] is an integer only when $g=21$, giving \[xy=9.\]"),("Use relative primality",r"Since $\gcd(x,y)=1$ and $xy=9$, the only ordered possibilities are \[(x,y)=(1,9)\quad\text{or}\quad(9,1).\]"),("Conclude",r"Thus there are $\boxed{2}$ ordered pairs."),],
24:[("Set useful coordinates",r"Place the regular hexagon on the coordinate plane with \[A=(1,0),\ C=\left(-\frac12,\frac{\sqrt3}{2}\right),\ E=\left(-\frac12,-\frac{\sqrt3}{2}\right).\] The needed midpoints are \[X=\left(\frac34,\frac{\sqrt3}{4}\right),\ Y=\left(-\frac34,\frac{\sqrt3}{4}\right),\ Z=\left(0,-\frac{\sqrt3}{2}\right).\]"),("Find the intersection polygon",r"The intersection of $\triangle ACE$ and $\triangle XYZ$ is a hexagon. Its vertices come from intersecting the boundary lines of the two triangles."),("List the vertices",r"Solving the simple line intersections gives the hexagon vertices \[\left(-\frac18,-\frac{3\sqrt3}{8}\right),\left(\frac14,-\frac{\sqrt3}{4}\right),\left(\frac58,\frac{\sqrt3}{8}\right),\left(\frac14,\frac{\sqrt3}{4}\right),\left(-\frac12,\frac{\sqrt3}{4}\right),\left(-\frac12,0\right).\]"),("Use the shoelace formula",r"Applying the shoelace formula to these vertices gives area \[\frac{15\sqrt3}{32}.\] This is a good place to use coordinates because it avoids trying to visually estimate several small triangular pieces."),("Conclude",r"The answer is \[\boxed{\frac{15\sqrt3}{32}}.\]"),],
25:[("Fix the floor value",r"Let \[m=\lfloor x\rfloor.\] Then $x$ lies in the interval $[m,m+1)$, and the equation becomes \[x^2+10000m=10000x.\]"),("Use the fractional part",r"Write $x=m+y$, where $0\le y<1$. Then $x-m=y$, so the equation is equivalent to \[x^2=10000y.\]"),("Turn existence into an interval test",r"For a fixed integer $m$, define \[H(y)=10000y-(m+y)^2.\] We need a zero of $H(y)$ for some $0\le y<1$."),("Check the endpoints",r"At $y=0$, \[H(0)=-m^2\le0.\] For all relevant $m$, the function is increasing on $0\le y\le1$, so a solution exists exactly when \[H(1)=10000-(m+1)^2>0,\] with the special endpoint $m=0,y=0$ included."),("Count the integers m",r"The inequality \[10000-(m+1)^2>0\] means \[|m+1|<100.\] Thus \[m=-100,-99,\ldots,98,\] which gives $199$ integer values of $m$."),("Conclude",r"Each such interval gives one solution, so there are $\boxed{199}$ real numbers $x$."),],
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












































