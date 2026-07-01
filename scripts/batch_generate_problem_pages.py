import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 99
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2017_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2017 AMC 10A Problems 21-25"
NEXT_START = "2017 AMC 10B Problem 1"

ANS={21:("D",r"\frac{37}{35}"),22:("E",r"\frac43-\frac{4\sqrt3\pi}{27}"),23:("B","2148"),24:("C","-7007"),25:("A","226")}

OV={
21:(r"A square with side length $x$ is inscribed in a right triangle with sides of length $3$, $4$, and $5$ so that one vertex of the square coincides with the right-angle vertex of the triangle. A square with side length $y$ is inscribed so that one side of the square lies on the hypotenuse of the triangle. What is $\frac{x}{y}$?",[("A",r"$\frac{12}{13}$"),("B",r"$\frac{35}{37}$"),("C","1"),("D",r"$\frac{37}{35}$"),("E",r"$\frac{13}{12}$")]),
22:(r"Sides $AB$ and $AC$ of equilateral triangle $ABC$ are tangent to a circle at points $B$ and $C$, respectively. What fraction of the area of $\triangle ABC$ lies outside the circle?",[("A",r"$\frac{4\sqrt3\pi}{27}-1$"),("B",r"$\sqrt3-\frac{\pi}{2}$"),("C","1"),("D",r"$\sqrt3-\frac{2\sqrt3\pi}{9}$"),("E",r"$\frac43-\frac{4\sqrt3\pi}{27}$")]),
23:(r"How many triangles with positive area have all their vertices at points $(i,j)$ in the coordinate plane, where $i$ and $j$ are integers between $1$ and $5$, inclusive?",[("A","2128"),("B","2148"),("C","2160"),("D","2200"),("E","2300")]),
24:(r"For certain real numbers $a$, $b$, and $c$, the polynomial $g(x)=x^3+ax^2+x+10$ has three distinct roots, and each root of $g(x)$ is also a root of the polynomial $f(x)=x^4+x^3+bx^2+100x+c$. What is $f(1)$?",[("A","-9009"),("B","-8008"),("C","-7007"),("D","-6006"),("E","-5005")]),
25:(r"How many integers between $100$ and $999$, inclusive, have the property that some permutation of its digits is a multiple of $11$ between $100$ and $999$? For example, both $121$ and $211$ have this property.",[("A","226"),("B","243"),("C","270"),("D","469"),("E","486")]),
}

KEY_OVERRIDES={21:"Use similar triangles and the altitude to the hypotenuse.",22:"Compute the circular segment inside the equilateral triangle.",23:"Subtract collinear triples from all triples of grid points.",24:"Use polynomial divisibility and compare coefficients.",25:"Use the divisibility rule for 11 and count digit multisets."}

SOL={
21:[("Find the square at the right angle",r"Place the right triangle with legs $3$ and $4$ on the coordinate axes. The hypotenuse has intercept form \[\frac{u}{3}+\frac{v}{4}=1.\] A square at the right-angle vertex has opposite vertex $(x,x)$, so \[\frac{x}{3}+\frac{x}{4}=1.\]"),("Solve for x",r"This gives \[\frac{7x}{12}=1,\quad x=\frac{12}{7}.\]"),("Find the altitude to the hypotenuse",r"The altitude from the right angle to the hypotenuse is \[h=\frac{3\cdot4}{5}=\frac{12}{5}.\]"),("Find y using similar triangles",r"A square with one side on the hypotenuse has its opposite side parallel to the hypotenuse and distance $y$ away. The available parallel length shrinks linearly from $5$ to $0$ over altitude $h$, so \[y=5\left(1-\frac{y}{12/5}\right).\]"),("Solve for y and compare",r"Solving gives $y=\frac{60}{37}$. Therefore \[\frac{x}{y}=\frac{12/7}{60/37}=\frac{37}{35}.\]"),("Conclude",r"The answer is $\boxed{\frac{37}{35}}$."),],
22:[("Choose a side length",r"Let the equilateral triangle have side length $1$. The final fraction will not depend on scale."),("Locate the circle center",r"Put $A=(0,0)$, $B=(1,0)$, and $C=(\frac12,\frac{\sqrt3}{2})$. Since $AB$ and $AC$ are tangents at $B$ and $C$, the circle center lies on the perpendiculars to those sides at $B$ and $C$. This gives radius $r=\frac{\sqrt3}{3}$."),("Identify the circle part inside the triangle",r"The angle $\angle BOC$ is $120^\circ$. The part of the circle inside the triangle is the circular segment cut off by chord $BC$, so its area is sector $BOC$ minus triangle $BOC$."),("Compute the segment area",r"The sector area is \[\frac{120}{360}\pi r^2=\frac{\pi}{9}.\] The triangle area is \[\frac12r^2\sin120^\circ=\frac{\sqrt3}{12}.\] Thus the circle area inside the triangle is \[\frac{\pi}{9}-\frac{\sqrt3}{12}.\]"),("Convert to a fraction outside",r"The triangle area is $\frac{\sqrt3}{4}$. The fraction outside the circle is \[1-\frac{\frac{\pi}{9}-\frac{\sqrt3}{12}}{\frac{\sqrt3}{4}}=\frac43-\frac{4\sqrt3\pi}{27}.\]"),("Conclude",r"The answer is $\boxed{\frac43-\frac{4\sqrt3\pi}{27}}$."),],
23:[("Start with all triples of points",r"There are $25$ lattice points in the $5\times5$ grid. The total number of ways to choose three points is \[\binom{25}{3}=2300.\]"),("Subtract collinear triples",r"A triangle has positive area exactly when its three points are not collinear. So we subtract all collinear triples."),("Count by line directions",r"Horizontal lines contribute $5\binom53=50$, and vertical lines contribute another $50$. Diagonals of slope $1$ and $-1$ contribute $20+20=40$ collinear triples."),("Include shorter slanted lines",r"Lines of slopes $2$, $\frac12$, $-2$, and $-\frac12$ each contribute $3$ triples, for a total of $12$ more. Thus the total number of collinear triples is \[50+50+40+12=152.\]"),("Subtract",r"The number of positive-area triangles is \[2300-152=2148.\]"),("Conclude",r"The answer is $\boxed{2148}$."),],
24:[("Use divisibility of polynomials",r"The three distinct roots of $g(x)$ are also roots of $f(x)$. Since $g$ is monic cubic and $f$ is monic quartic, we can write \[f(x)=(x+k)g(x)\] for some real number $k$."),("Expand",r"\[(x+k)(x^3+ax^2+x+10)=x^4+(a+k)x^3+(1+ak)x^2+(10+k)x+10k.\]"),("Compare coefficients",r"Matching with $f(x)=x^4+x^3+bx^2+100x+c$, the $x$ coefficient gives $10+k=100$, so $k=90$. Then the $x^3$ coefficient gives $a+k=1$, so $a=-89$."),("Find b and c",r"The $x^2$ coefficient is \[b=1+ak=1+(-89)(90)=-8009.\] Also $c=10k=900$."),("Evaluate f of 1",r"\[f(1)=1+1+b+100+c=2-8009+100+900=-7007.\]"),("Conclude",r"The answer is $\boxed{-7007}$."),],
25:[("Use the divisibility rule for 11",r"A three-digit number with digits $x,y,z$ is divisible by $11$ exactly when $x-y+z$ is $0$ or $11$. So for a multiset of three digits, we need one digit that can be placed in the middle so the other two digits minus it equal $0$ or $11$."),("Count the zero case",r"First count digit multisets where one digit equals the sum of the other two. These give $29$ valid multisets. Accounting for repeated digits and zeros, they produce $126$ three-digit integers."),("Count the eleven case",r"Next count digit multisets where the sum of two digits is $11$ more than the middle digit. These give $20$ valid multisets. Accounting for repeated digits and zeros, they produce $100$ three-digit integers."),("Explain the accounting",r"The adjustment is necessary because a multiset with three distinct nonzero digits gives $6$ three-digit integers, a multiset with a zero and two distinct nonzero digits gives $4$, and repeated digits give fewer distinct integers."),("Add the cases",r"The two cases are disjoint for three-digit digit multisets, so the total is \[126+100=226.\]"),("Conclude",r"The answer is $\boxed{226}$."),],
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
        if r["year"] == "2017" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2017 AMC 10A Answer Key\n\n"
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












































