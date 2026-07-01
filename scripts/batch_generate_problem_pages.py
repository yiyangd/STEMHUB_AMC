import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 62
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2011_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2011 AMC 10B Problems 21-25"
NEXT_START = "2012 AMC 10A Problem 1"

ANS = {
    21: ("B", "31"),
    22: ("A", r"5\sqrt2-7"),
    23: ("D", "6"),
    24: ("B", r"\frac{50}{99}"),
    25: ("D", r"\frac{1509}{128}"),
}

OV = {
    21: (r"Brian writes down four integers $w>x>y>z$ whose sum is $44$. The pairwise positive differences of these numbers are $1,3,4,5,6,$ and $9$. What is the sum of the possible values for $w$?", [("A","16"),("B","31"),("C","48"),("D","62"),("E","93")]),
    22: (r"A pyramid has a square base with sides of length $1$ and has lateral faces that are equilateral triangles. A cube is placed within the pyramid so that one face is on the base of the pyramid and its opposite face has all its edges on the lateral faces of the pyramid. What is the volume of this cube?", [("A",r"5\sqrt2-7"),("B",r"7-4\sqrt3"),("C",r"\frac{2\sqrt2}{27}"),("D",r"\frac{\sqrt2}{9}"),("E",r"\frac{\sqrt3}{9}")]),
    23: (r"What is the hundreds digit of $2011^{2011}$?", [("A","1"),("B","4"),("C","5"),("D","6"),("E","9")]),
    24: (r"A lattice point in an $xy$-coordinate system is any point $(x,y)$ where both $x$ and $y$ are integers. The graph of $y=mx+2$ passes through no lattice point with $0<x\le100$ for all $m$ such that $\frac12<m<a$. What is the maximum possible value of $a$?", [("A",r"\frac{51}{101}"),("B",r"\frac{50}{99}"),("C",r"\frac{51}{100}"),("D",r"\frac{52}{101}"),("E",r"\frac{13}{25}")]),
    25: (r"Let $T_1$ be a triangle with side lengths $2011,2012,$ and $2013$. For $n\ge1$, if $T_n=\triangle ABC$ and $D,E,F$ are the points of tangency of the incircle of $\triangle ABC$ to the sides $AB,BC,$ and $AC$, respectively, then $T_{n+1}$ is a triangle with side lengths $AD,BE,$ and $CF$, if it exists. What is the perimeter of the last triangle in the sequence $(T_n)$?", [("A",r"\frac{1509}{8}"),("B",r"\frac{1509}{32}"),("C",r"\frac{1509}{64}"),("D",r"\frac{1509}{128}"),("E",r"\frac{1509}{256}")]),
}

KEY_OVERRIDES = {
    21: "Represent the four numbers by adjacent gaps and test the possible gap patterns.",
    22: "Use a diagonal cross-section of the pyramid so the cube becomes a rectangle inside a 45-45-90 triangle.",
    23: "Find the last three digits with modular arithmetic, then read the hundreds digit.",
    24: "The first rational slope greater than $1/2$ with denominator at most $100$ creates the limiting value.",
    25: "Track how the side lengths change when incircle tangency lengths become the next triangle.",
}

SOL = {
    21: [
        ("Use the largest difference", r"Since $w$ is the largest number and $z$ is the smallest, the largest pairwise difference must be $w-z=9$."),
        ("Think in adjacent gaps", r"Let the adjacent gaps be $w-x$, $x-y$, and $y-z$. These three gaps add to $9$, and all pairwise differences are made by adding consecutive gaps."),
        ("Find the possible gap patterns", r"The six differences must be $1,3,4,5,6,9$. The adjacent gaps have to be three of these numbers and sum to $9$. The two working orders are $(5,1,3)$ and $(3,1,5)$, which produce exactly the required six differences."),
        ("Convert each pattern to w", r"For gaps $(5,1,3)$, the numbers are $w,w-5,w-6,w-9$. Their sum is $4w-20=44$, so $w=16$. For gaps $(3,1,5)$, the numbers are $w,w-3,w-4,w-9$, giving $4w-16=44$, so $w=15$."),
        ("Add possible values", r"The possible values of $w$ are $16$ and $15$, and their sum is $31$. The answer is $\boxed{31}$."),
    ],
    22: [
        ("Take the right cross-section", r"A spatial problem becomes much easier if we slice through the apex and a diagonal of the square base. The cross-section of the pyramid is a $45$-$45$-$90$ triangle with base $\sqrt2$ and equal sides $1$."),
        ("Describe the cube in the cross-section", r"If the cube has side length $s$, then in this diagonal cross-section it appears as a rectangle of height $s$ and width $s\sqrt2$, because the width is the diagonal of the cube's top face."),
        ("Use the side triangles", r"The two small triangles on the left and right of the rectangle are also $45$-$45$-$90$ triangles, so each has horizontal leg $s$. Therefore the full base length satisfies \[\sqrt2=s+s\sqrt2+s=(2+\sqrt2)s.\]"),
        ("Solve for the cube side", r"Thus \[s=\frac{\sqrt2}{2+\sqrt2}=\sqrt2-1.\]"),
        ("Compute the volume", r"The cube's volume is $s^3=(\sqrt2-1)^3=5\sqrt2-7$. The answer is $\boxed{5\sqrt2-7}$."),
    ],
    23: [
        ("Only the last three digits matter", r"The hundreds digit is determined by the number modulo $1000$. Since $2011\equiv11\pmod{1000}$, we need $11^{2011}\pmod{1000}$."),
        ("Use modulo 8 and 125", r"Because $1000=8\cdot125$, we can work modulo $8$ and modulo $125$. Modulo $8$, $2011\equiv3$, and an odd power of $3$ is $3$ modulo $8$."),
        ("Compute modulo 125", r"Modulo $125$, $2011\equiv11$. Since powers repeat with period dividing $100$, $11^{2011}\equiv11^{11}\pmod{125}$. Now $11^2\equiv-4$, $11^8\equiv6$, so $11^{11}=11^8\cdot11^2\cdot11\equiv6(-4)(11)\equiv111\pmod{125}$."),
        ("Combine the congruences", r"So the last three digits have the form $111+125k$. We need $111+125k\equiv3\pmod8$. Since $111\equiv7$ and $125\equiv5$, this gives $7+5k\equiv3\pmod8$, so $k\equiv4\pmod8$."),
        ("Read the hundreds digit", r"Taking $k=4$ gives $111+500=611$. Therefore the hundreds digit is $\boxed{6}$."),
    ],
    24: [
        ("Translate lattice points into slope fractions", r"The line is $y=mx+2$. Since $2$ is already an integer, a lattice point with integer $x$ occurs exactly when $mx$ is an integer."),
        ("Connect this to denominators", r"If $m=\frac pq$ in lowest terms and $q\le100$, then choosing $x=q$ makes $mx=p$ an integer, so the line hits a lattice point. Therefore the interval must avoid every rational number greater than $\frac12$ whose reduced denominator is at most $100$."),
        ("Find the first dangerous slope", r"For an even denominator $q$, the smallest fraction above $\frac12$ is at least $\frac12+\frac1q\ge\frac12+rac1{100}=\frac{51}{100}$. For an odd denominator $q$, it is $\frac{(q+1)/2}{q}=\frac12+rac1{2q}$, minimized by the largest odd $q\le100$, namely $q=99$."),
        ("Compute that value", r"With $q=99$, the fraction is $\frac{50}{99}$, and it is the first rational slope greater than $\frac12$ that would create a lattice point with $0<x\le100$."),
        ("Conclude", r"Thus the largest possible upper endpoint is $a=\frac{50}{99}$. The answer is $\boxed{\frac{50}{99}}$."),
    ],
    25: [
        ("Understand one step of the process", r"Suppose a triangle has side lengths $m-1,m,m+1$. Tangent segments from the same vertex to the incircle are equal, so if the new side lengths are $x,y,z$, they satisfy $x+y=m-1$, $x+z=m$, and $y+z=m+1$."),
        ("Solve the tangent lengths", r"Adding the first two equations and subtracting the third gives $2x=m-2$, so $x=\frac m2-1$. Similarly, $y=\frac m2$ and $z=\frac m2+1$. Thus the next triangle again has side lengths of the form $m'-1,m',m'+1$, where $m'=\frac m2$."),
        ("Track the middle side", r"The first triangle has middle side $m=2012$. Each valid step halves the middle side: $2012,1006,503,\frac{503}{2},\ldots$."),
        ("Find when the triangle stops existing", r"A triangle with sides $m-1,m,m+1$ exists exactly when $(m-1)+m>m+1$, which simplifies to $m>2$. The last middle side greater than $2$ is $\frac{503}{128}$; the next would be $\frac{503}{256}<2$."),
        ("Compute the last perimeter", r"For the last triangle, the side lengths are $\frac{503}{128}-1$, $\frac{503}{128}$, and $\frac{503}{128}+1$. Their sum is $3\cdot\frac{503}{128}=\frac{1509}{128}$. The answer is $\boxed{\frac{1509}{128}}$."),
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






























