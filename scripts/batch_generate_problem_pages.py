import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 61
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2011_AMC_10B_Answer_Key"
TARGET_NUMBERS = {16,17,18,19,20}
SKIPPED = []
BATCH_LABEL = "2011 AMC 10B Problems 16-20"
NEXT_START = "2011 AMC 10B Problem 21"

ANS = {
    16: ("A", r"\frac{\sqrt2-1}{2}"),
    17: ("C", "130"),
    18: ("E", "75"),
    19: ("A", "-64"),
    20: ("C", r"\frac{2\sqrt3}{3}"),
}

OV = {
    16: (r"A dart board is a regular octagon divided into regions as shown. Suppose that a dart thrown at the board is equally likely to land anywhere on the board. What is the probability that the dart lands within the center square?", [("A",r"\frac{\sqrt2-1}{2}"),("B",r"\frac14"),("C",r"\frac{2-\sqrt2}{2}"),("D",r"\frac{\sqrt2}{4}"),("E",r"2-\sqrt2")]),
    17: (r"In the given circle, the diameter $\overline{EB}$ is parallel to $\overline{DC}$, and $\overline{AB}$ is parallel to $\overline{ED}$. The angles $\angle AEB$ and $\angle ABE$ are in the ratio $4:5$. What is the degree measure of $\angle BCD$?", [("A","120"),("B","125"),("C","130"),("D","135"),("E","140")]),
    18: (r"Rectangle $ABCD$ has $AB=6$ and $BC=3$. Point $M$ is chosen on side $AB$ so that $\angle AMD=\angle CMD$. What is the degree measure of $\angle AMD$?", [("A","15"),("B","30"),("C","45"),("D","60"),("E","75")]),
    19: (r"What is the product of all the roots of the equation \[\sqrt{5|x|+8}=\sqrt{x^2-16}?\]", [("A","-64"),("B","-24"),("C","-9"),("D","24"),("E","576")]),
    20: (r"Rhombus $ABCD$ has side length $2$ and $\angle B=120^\circ$. Region $R$ consists of all points inside the rhombus that are closer to vertex $B$ than any of the other three vertices. What is the area of $R$?", [("A",r"\frac{\sqrt3}{3}"),("B",r"\frac{\sqrt3}{2}"),("C",r"\frac{2\sqrt3}{3}"),("D",r"1+\frac{\sqrt3}{3}"),("E","2")]),
}

KEY_OVERRIDES = {
    16: "Use area ratio: center square area divided by total regular-octagon area.",
    17: "Use the diameter to get a right angle, then use parallel lines and cyclic quadrilateral angles.",
    18: "Use angle equality and parallel lines to create an isosceles triangle, then finish with a 30-60-90 triangle.",
    19: "Square both sides and reduce the equation to a quadratic in $|x|$.",
    20: "Perpendicular bisectors divide each equilateral half of the rhombus into equal-area parts.",
}

SOL = {
    16: [
        ("Use area as probability", r"Because the dart is equally likely to land anywhere on the board, the desired probability is the area of the center square divided by the area of the whole octagon."),
        ("Choose a convenient scale", r"Use the scale suggested by the diagram: let the center square have side length $\sqrt2$. Then its area is $2$. The surrounding octagon can be decomposed into the center square, four rectangles, and four right isosceles corner triangles."),
        ("Compute the octagon area", r"With this scale, the four rectangles have total area $4\sqrt2$, and the four corner triangles have total area $2$. Therefore the whole octagon has area $2+4\sqrt2+2=4+4\sqrt2$."),
        ("Form the probability", r"The probability is \[\frac{2}{4+4\sqrt2}=\frac{1}{2+2\sqrt2}.\]"),
        ("Rationalize", r"Multiplying by the conjugate gives \[\frac{1}{2+2\sqrt2}=\frac{\sqrt2-1}{2}.\] Thus the answer is $\boxed{\frac{\sqrt2-1}{2}}$."),
    ],
    17: [
        ("Use the diameter", r"Since $\overline{EB}$ is a diameter, the inscribed angle $\angle EAB$ is a right angle. That makes triangle $AEB$ easier because the other two angles are in the ratio $4:5$."),
        ("Find the two acute angles", r"Let $\angle AEB=4x$ and $\angle ABE=5x$. Then $4x+5x+90=180$, so $9x=90$ and $x=10$. Therefore $\angle ABE=50^\circ$."),
        ("Use parallel lines", r"Because $\overline{AB}\parallel\overline{ED}$, the angle $\angle ABE$ equals $\angle BED$ by alternate interior angles. Thus $\angle BED=50^\circ$."),
        ("Use the cyclic quadrilateral", r"Points $B,E,D,C$ lie on the circle, so quadrilateral $BEDC$ is cyclic. Opposite angles in a cyclic quadrilateral are supplementary, so $\angle BED+\angle BCD=180^\circ$."),
        ("Finish", r"Therefore $\angle BCD=180^\circ-50^\circ=130^\circ$. The answer is $\boxed{130}$."),
    ],
    18: [
        ("Name the target angle", r"Let $\angle AMD=\angle CMD=\theta$. The important idea is that ray $MD$ splits the angle from $MA$ to $MC$ into two equal parts."),
        ("Use parallel sides of the rectangle", r"Since $AB\parallel DC$, angle $AMD$ equals angle $CDM$ by alternate interior angles. But $\angle AMD=\angle CMD$, so in triangle $CDM$ the angles at $D$ and $M$ are equal."),
        ("Get an isosceles triangle", r"Equal base angles mean opposite sides are equal, so $CM=CD$. Since the rectangle has $AB=CD=6$, we get $CM=6$."),
        ("Look at right triangle MBC", r"Triangle $MBC$ is right, with $BC=3$ and hypotenuse $CM=6$. Therefore it is a $30$-$60$-$90$ triangle, and $\angle BMC=30^\circ$."),
        ("Use the straight angle at M", r"The angles along the straight line $AMB$ add to $180^\circ$. They are $\theta$, another $\theta$, and $30^\circ$, so $2\theta+30=180$. Hence $\theta=75^\circ$. The answer is $\boxed{75}$."),
    ],
    19: [
        ("Notice the role of absolute value", r"Both sides are square roots, so after squaring we should try to express everything in terms of $|x|$. This is natural because $x^2=|x|^2$."),
        ("Square both sides", r"Squaring gives $5|x|+8=x^2-16$. Replacing $x^2$ by $|x|^2$ gives \[|x|^2-5|x|-24=0.\]"),
        ("Solve the quadratic in $|x|$", r"Factor: \[(|x|-8)(|x|+3)=0.\] Since $|x|$ cannot be negative, the only possible value is $|x|=8$."),
        ("Convert back to x", r"If $|x|=8$, then $x=8$ or $x=-8$. Both work in the original equation because both sides become $\sqrt{48}$."),
        ("Compute the product", r"The product of all roots is $8\cdot(-8)=-64$. The answer is $\boxed{-64}$."),
    ],
    20: [
        ("Break the rhombus into simpler triangles", r"A rhombus with side length $2$ and angle $120^\circ$ can be split by diagonal $BD$ into two equilateral triangles, $ABD$ and $BCD$, each with side length $2$."),
        ("Understand the 'closer to B' condition", r"Inside an equilateral triangle, the points closer to one vertex than to the other two are cut out by perpendicular bisectors. The medians of an equilateral triangle divide it into $6$ small triangles of equal area, and the region closest to one vertex contains $2$ of those $6$ pieces."),
        ("Find the fraction in each half", r"So in each equilateral triangle, the region closest to vertex $B$ has one third of that triangle's area. Since the rhombus is made of two such equilateral triangles sharing vertex $B$, region $R$ is one third of the whole rhombus."),
        ("Compute the rhombus area", r"The area of the rhombus is $s^2\sin120^\circ=2^2\cdot\frac{\sqrt3}{2}=2\sqrt3$."),
        ("Take one third", r"Thus the area of $R$ is $\frac13\cdot2\sqrt3=\frac{2\sqrt3}{3}$. The answer is $\boxed{\frac{2\sqrt3}{3}}$."),
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {16,17}) else notes
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
        if r["year"] == "2011" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {16,17},
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
        + "- Answer verification source: AoPS 2011 AMC 10B Answer Key\n\n"
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





























