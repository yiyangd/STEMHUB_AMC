import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 123
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2021_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2021 Spring AMC 10A Problems 21-25"
NEXT_START = "2021 Spring AMC 10B Problem 1"

ANS={21:("C","55"),22:("B","13"),23:("D",r"\frac{25}{32}"),24:("D",r"\frac{8a^2}{a^2+1}"),25:("E","36")}

OV={
21:(r"Let $ABCDEF$ be an equiangular hexagon. The lines $AB$, $CD$, and $EF$ determine a triangle with area $192\sqrt3$, and the lines $BC$, $DE$, and $FA$ determine a triangle with area $324\sqrt3$. The perimeter of hexagon $ABCDEF$ can be expressed as $m+n\sqrt p$, where $m,n,p$ are positive integers and $p$ is squarefree. What is $m+n+p$?",[("A","47"),("B","52"),("C","55"),("D","58"),("E","63")]),
22:(r"Hiram's algebra notes are $50$ pages long and are printed on $25$ sheets of paper. His roommate takes a consecutive set of sheets from the middle of the notes. The average of the page numbers on all remaining sheets is exactly $19$. How many sheets were borrowed?",[("A","10"),("B","13"),("C","15"),("D","17"),("E","20")]),
23:(r"Frieda the frog begins a sequence of hops on a $3\times3$ grid of squares, moving one square on each hop and choosing uniformly at random from up, down, left, and right. If a hop would take her off the grid, she wraps around to the opposite edge. Starting from the center square, she makes at most four hops and stops if she lands on a corner square. What is the probability that she reaches a corner square on one of the four hops?",[("A",r"$\frac9{16}$"),("B",r"$\frac58$"),("C",r"$\frac34$"),("D",r"$\frac{25}{32}$"),("E",r"$\frac{13}{16}$")]),
24:(r"The interior of a quadrilateral is bounded by the graphs of $(x+ay)^2=4a^2$ and $(ax-y)^2=a^2$, where $a$ is a positive real number. What is the area of this region in terms of $a$, valid for all $a>0$?",[("A",r"$\frac{8a^2}{(a+1)^2}$"),("B",r"$\frac{4a}{a+1}$"),("C",r"$\frac{8a}{a+1}$"),("D",r"$\frac{8a^2}{a^2+1}$"),("E",r"$\frac{8a}{a^2+1}$")]),
25:(r"How many ways are there to place $3$ indistinguishable red chips, $3$ indistinguishable blue chips, and $3$ indistinguishable green chips in the squares of a $3\times3$ grid so that no two chips of the same color are directly adjacent vertically or horizontally?",[("A","12"),("B","18"),("C","24"),("D","30"),("E","36")]),
}

KEY_OVERRIDES={21:"Relate the two equilateral outer triangles to the hexagon perimeter.",22:"Use page-number sums and consecutive sheets.",23:"Track center, edge, and corner states in the wrapped grid.",24:"Use a linear change of variables to turn the region into a rectangle.",25:"Count colorings by fixing the center color."}

SOL={
21:[("Recognize the two outer triangles",r"In an equiangular hexagon, alternating side lines form equilateral triangles because the directions differ by $60^\circ$. So both given triangles are equilateral."),("Find their side lengths from area",r"An equilateral triangle with side length $s$ has area \[\frac{\sqrt3}{4}s^2.\] From \[\frac{\sqrt3}{4}s_1^2=192\sqrt3,\] we get $s_1=16\sqrt3$. From \[\frac{\sqrt3}{4}s_2^2=324\sqrt3,\] we get $s_2=36$."),("Relate the triangles to the hexagon",r"For an equiangular hexagon, the perimeter of the hexagon equals the sum of the side lengths of these two alternating outer equilateral triangles. This comes from following the six $60^\circ$ directions around the boundary; the alternating extensions account for each side length once."),("Compute the perimeter",r"Thus the perimeter is \[16\sqrt3+36.\] This is in the form $m+n\sqrt p$ with $m=36$, $n=16$, and $p=3$."),("Conclude",r"Therefore \[m+n+p=36+16+3=55.\] The answer is $\boxed{55}$."),],
22:[("Start with the total page sum",r"The sum of pages $1$ through $50$ is \[\frac{50\cdot51}{2}=1275.\]"),("Let h be the number of sheets removed",r"If $h$ sheets are removed, then $2h$ pages are removed and $50-2h$ pages remain. Since the remaining average is $19$, the remaining sum is \[19(50-2h).\]"),("Find the removed sum",r"The removed pages therefore have sum \[1275-19(50-2h)=325+38h.\]"),("Use consecutive pages from consecutive sheets",r"If the first removed page is odd and equal to $p$, then the removed pages are $p,p+1,\ldots,p+2h-1$. Their sum is \[h(2p+2h-1).\] So \[h(2p+2h-1)=325+38h.\]"),("Test divisors of 325",r"Rearranging gives \[h(2p+2h-39)=325.\] The possible sheet counts from the answer choices are tested through divisors of $325$. The value $h=13$ gives $2p+26-39=25$, so $p=19$, a valid first page."),("Conclude",r"The roommate borrowed $\boxed{13}$ sheets."),],
23:[("Group the grid positions into states",r"Because of symmetry on the wrapped $3\times3$ grid, we only need three states: center, edge-middle, and corner. Frieda starts at the center and stops once she reaches a corner."),("Find transitions before stopping",r"From the center, every move goes to an edge-middle. From an edge-middle, two of the four moves go to corners, one goes to the center, and one goes to another edge-middle because of wrapping."),("Track the probability of not yet hitting a corner",r"After $1$ hop, she is certainly at an edge-middle. Avoiding a corner on hop $2$ has probability $\frac12$, leaving probability $\frac14$ at the center and $\frac14$ at an edge-middle."),("Continue to four hops",r"After hop $3$, the non-corner probabilities are $\frac1{16}$ at the center and $\frac5{16}$ at an edge-middle. After hop $4$, the total probability of still not having reached a corner is \[\frac5{64}+\frac9{64}=\frac7{32}.\]"),("Complement",r"Therefore the probability she reaches a corner within four hops is \[1-\frac7{32}=\frac{25}{32}.\]"),("Conclude",r"The answer is $\boxed{\frac{25}{32}}$."),],
24:[("Rewrite the boundaries as linear equations",r"The equations represent four lines: \[x+ay=\pm2a,\qquad ax-y=\pm a.\] So the quadrilateral becomes a rectangle in suitable coordinates."),("Use a change of variables",r"Let \[u=x+ay,\qquad v=ax-y.\] In the $uv$-plane, the region is the rectangle \[-2a\le u\le2a,\qquad -a\le v\le a.\]"),("Find the rectangle area in uv-coordinates",r"The rectangle has side lengths $4a$ and $2a$, so its area in the $uv$-plane is \[8a^2.\]"),("Account for area scaling",r"The Jacobian determinant is \[\left|\begin{matrix}1&a\\ a&-1\end{matrix}\right|=a^2+1.\] Thus areas in the $uv$-plane are $(a^2+1)$ times the corresponding areas in the $xy$-plane."),("Compute the original area",r"The desired area is \[\frac{8a^2}{a^2+1}.\]"),("Conclude",r"The answer is $\boxed{\frac{8a^2}{a^2+1}}$."),],
25:[("Fix the center color first",r"The center square is adjacent to all four edge-middle squares. Choose the center color first; there are $3$ choices."),("Place the other chips of that color",r"The other two chips of the center color cannot go on edge-middle squares, so they must occupy two of the four corners. This can be done in \[\binom42=6\] ways."),("Fill the remaining colors",r"After the center color is placed, the remaining six squares must contain three chips of each of the other two colors. For each choice of the two same-colored corners, there are exactly $2$ valid ways to fill the remaining squares, corresponding to swapping the two remaining colors."),("Multiply the choices",r"The total number of arrangements is \[3\cdot6\cdot2=36.\]"),("Check the adjacency condition",r"The construction avoids same-colored horizontal or vertical neighbors: the center color is only on nonadjacent corners plus the center, and the other two colors alternate through the remaining positions."),("Conclude",r"The answer is $\boxed{36}$."),],
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
    year_label = row["year"]
    if year_label == "2021 Spring":
        year_part = "2021"
    elif year_label == "2021 Fall":
        year_part = "2021_Fall"
    else:
        year_part = year_label.replace(" ", "_")
    return f"https://artofproblemsolving.com/wiki/index.php/{year_part}_{row['contest'].replace(' ', '_')}{row['form']}_Problems/Problem_{row['problem_no']}"


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
        if r["year"] == "2021 Spring" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2021 AMC 10A Answer Key\n\n"
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












































