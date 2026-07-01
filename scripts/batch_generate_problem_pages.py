import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 102
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2017_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2017 AMC 10B Problems 21-25"
NEXT_START = "2018 AMC 10A Problem 1"

ANS={21:("D",r"\frac{17}{6}"),22:("D",r"\frac{140}{37}"),23:("C","9"),24:("C","108"),25:("E","100")}

OV={
21:(r"In $\triangle ABC$, $AB=6$, $AC=8$, $BC=10$, and $D$ is the midpoint of $BC$. What is the sum of the radii of the circles inscribed in $\triangle ADB$ and $\triangle ADC$?",[("A",r"$\frac54$"),("B",r"$\frac{11}{6}$"),("C",r"$2\sqrt2$"),("D",r"$\frac{17}{6}$"),("E","3")]),
22:(r"The diameter $AB$ of a circle of radius $2$ is extended to a point $D$ outside the circle so that $BD=3$. Point $E$ is chosen so that $ED=5$ and line $ED$ is perpendicular to line $AD$. Segment $AE$ intersects the circle at point $C$ between $A$ and $E$. What is the area of $\triangle ABC$?",[("A",r"$\frac{120}{37}$"),("B",r"$\frac{140}{39}$"),("C",r"$\frac{145}{39}$"),("D",r"$\frac{140}{37}$"),("E",r"$\frac{120}{31}$")]),
23:(r"Let $N=123456789101112\cdots4344$ be the $79$-digit number formed by writing the integers from $1$ to $44$ in order, one after the other. What is the remainder when $N$ is divided by $45$?",[("A","1"),("B","4"),("C","9"),("D","18"),("E","44")]),
24:(r"The vertices of an equilateral triangle lie on the hyperbola $xy=1$, and a vertex of this hyperbola is the centroid of the triangle. What is the square of the area of the triangle?",[("A","48"),("B","60"),("C","108"),("D","120"),("E","169")]),
25:(r"Last year Isabella took $7$ math tests and received $7$ different scores, each an integer between $91$ and $100$, inclusive. After each test she noticed that the average of her test scores was an integer. Her score on the seventh test was $95$. What was her score on the sixth test?",[("A","92"),("B","94"),("C","96"),("D","98"),("E","100")]),
}

KEY_OVERRIDES={21:"Use area over semiperimeter to find inradii of the two subtriangles.",22:"Use coordinates and circle-line intersection.",23:"Use the Chinese remainder theorem modulo 5 and modulo 9.",24:"Center the triangle at the hyperbola vertex and rotate coordinates by 120 degrees.",25:"Use divisibility of prefix sums by the number of tests."}

SOL={
21:[("Notice the right triangle",r"Since $6^2+8^2=10^2$, triangle $ABC$ is right at $A$. The midpoint $D$ of the hypotenuse is $5$ units from each vertex, so $AD=BD=CD=5$."),("Find the first inradius",r"Triangle $ADB$ has side lengths $5,5,6$. Its area is half of rectangle-style base $6$ and height $4$, so the area is $12$. Its semiperimeter is \[\frac{5+5+6}{2}=8.\] Thus its inradius is \[\frac{12}{8}=\frac32.\]"),("Find the second inradius",r"Triangle $ADC$ has side lengths $5,5,8$. Its height to side $8$ is $3$, so its area is also $12$. Its semiperimeter is \[\frac{5+5+8}{2}=9.\] Thus its inradius is \[\frac{12}{9}=\frac43.\]"),("Add",r"The sum of the two radii is \[\frac32+\frac43=\frac{9+8}{6}=\frac{17}{6}.\]"),("Conclude",r"The answer is $\boxed{\frac{17}{6}}$."),],
22:[("Set coordinates",r"Let the circle be centered at the origin, with $A=(-2,0)$ and $B=(2,0)$. Since $BD=3$, point $D=(5,0)$."),("Place E",r"Line $AD$ is horizontal, so $ED$ is vertical. Since $ED=5$, take $E=(5,5)$; the reflected choice would give the same area."),("Find line AE",r"Parametrize segment $AE$ by \[(x,y)=(-2,0)+t(7,5).\] The point $A$ corresponds to $t=0$."),("Intersect with the circle",r"The circle is $x^2+y^2=4$. Substituting $x=-2+7t$, $y=5t$ gives the second intersection at \[t=\frac{14}{37}.\] Thus \[C=\left(\frac{24}{37},\frac{70}{37}\right).\]"),("Compute area",r"Using $AB=4$ as the base, the height of $C$ above $AB$ is $\frac{70}{37}$. Therefore \[[ABC]=\frac12\cdot4\cdot\frac{70}{37}=\frac{140}{37}.\]"),("Conclude",r"The answer is $\boxed{\frac{140}{37}}$."),],
23:[("Work modulo 5 and 9",r"Since $45=5\cdot9$, find the remainder modulo $5$ and modulo $9$."),("Modulo 5",r"The last digit of $N$ is $4$, because the final integer written is $44$. So \[N\equiv4\pmod5.\]"),("Modulo 9",r"A number is congruent modulo $9$ to the sum of its digits. The digit sum of $N$ is congruent to \[1+2+\cdots+44=\frac{44\cdot45}{2}=990,\] which is divisible by $9$."),("Combine the conditions",r"We need a number less than $45$ that is $0$ modulo $9$ and $4$ modulo $5$. The multiples of $9$ are $0,9,18,27,36$, and only $9$ is congruent to $4$ modulo $5$."),("Conclude",r"The remainder is $\boxed{9}$."),],
24:[("Center at the hyperbola vertex",r"The vertex of the branch $xy=1$ in the first quadrant is $(1,1)$. Let this be the centroid of the equilateral triangle."),("Describe one vertex by a vector",r"Write one triangle vertex as $(1+u,1+v)$. Because it lies on $xy=1$, \[(1+u)(1+v)=1,\] or \[u+v+uv=0.\]"),("Rotate for the other vertices",r"The other two vertices are obtained by rotating vector $(u,v)$ by $120^\circ$ and $240^\circ$ about the centroid. Requiring those two rotated points to also satisfy $xy=1$ gives the same type of equation for the two rotated vectors."),("Solve the system",r"The nondegenerate solutions give \[u^2+v^2=8.\] This is the squared distance from the centroid to each vertex."),("Convert radius to area",r"If the distance from the centroid to a vertex is $r$, then an equilateral triangle has side length $\sqrt3\,r$ and area \[\frac{\sqrt3}{4}(\sqrt3 r)^2=\frac{3\sqrt3}{4}r^2.\] With $r^2=8$, the area is $6\sqrt3$."),("Square the area",r"The square of the area is \[(6\sqrt3)^2=108.\]"),("Conclude",r"The answer is $\boxed{108}$."),],
25:[("Translate averages into divisibility",r"After each of the first $k$ tests, the average is an integer, so the sum of the first $k$ scores is divisible by $k$."),("Use the seventh score",r"Let $S_6$ be the sum of the first six scores. Since the seventh score is $95$, the total $S_6+95$ is divisible by $7$. Also $S_6$ is divisible by $6$."),("Find S6",r"The first six scores are six distinct integers from $91$ through $100$, excluding $95$. Their sum must be between $563$ and $584$. The multiples of $6$ in this range are $564,570,576,582$. Only $570$ makes $S_6+95$ divisible by $7$."),("Use the fifth average",r"Let the sixth score be $s_6$. The sum after five tests is $S_6-s_6$, and it must be divisible by $5$. Since $S_6=570$ is divisible by $5$, $s_6$ must also be divisible by $5$."),("Use distinct scores",r"The seventh score is already $95$, and scores are distinct. The only remaining score between $91$ and $100$ divisible by $5$ is $100$."),("Conclude",r"Her sixth test score was $\boxed{100}$."),],
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












































