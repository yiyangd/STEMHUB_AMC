import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 118
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2020_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2020 AMC 10B Problems 1-10"
NEXT_START = "2020 AMC 10B Problem 11"

ANS={1:("D","5"),2:("E","45"),3:("E",r"16:3"),4:("D","7"),5:("B","420"),6:("B","55"),7:("A","7"),8:("D","8"),9:("D","4"),10:("C",r"3\pi\sqrt7")}

OV={
1:(r"What is the value of \[1-(-2)-3-(-4)-5-(-6)?\]",[("A","-20"),("B","-3"),("C","3"),("D","5"),("E","21")]),
2:(r"Carl has $5$ cubes each having side length $1$, and Kate has $5$ cubes each having side length $2$. What is the total volume of the $10$ cubes?",[("A","24"),("B","25"),("C","28"),("D","40"),("E","45")]),
3:(r"The ratio of $w$ to $x$ is $4:3$, the ratio of $y$ to $z$ is $3:2$, and the ratio of $z$ to $x$ is $1:6$. What is the ratio of $w$ to $y$?",[("A",r"$4:3$"),("B",r"$3:2$"),("C",r"$8:3$"),("D",r"$4:1$"),("E",r"$16:3$")]),
4:(r"The acute angles of a right triangle are $a^\circ$ and $b^\circ$, where $a>b$ and both $a$ and $b$ are prime numbers. What is the least possible value of $b$?",[("A","2"),("B","3"),("C","5"),("D","7"),("E","11")]),
5:(r"How many distinguishable arrangements are there of $1$ brown tile, $1$ purple tile, $2$ green tiles, and $3$ yellow tiles in a row from left to right? Tiles of the same color are indistinguishable.",[("A","210"),("B","420"),("C","630"),("D","840"),("E","1050")]),
6:(r"Driving along a highway, Megan noticed that her odometer showed $15951$ miles, a palindrome. Two hours later, the odometer displayed the next higher palindrome. What was her average speed, in miles per hour, during this $2$-hour period?",[("A","50"),("B","55"),("C","60"),("D","65"),("E","70")]),
7:(r"How many positive even multiples of $3$ less than $2020$ are perfect squares?",[("A","7"),("B","8"),("C","9"),("D","10"),("E","12")]),
8:(r"Points $P$ and $Q$ lie in a plane with $PQ=8$. How many locations for point $R$ are there such that $\triangle PQR$ is a right triangle with area $12$ square units?",[("A","2"),("B","4"),("C","6"),("D","8"),("E","12")]),
9:(r"How many ordered pairs of integers $(x,y)$ satisfy \[x^{2020}+y^2=2y?\]",[("A","1"),("B","2"),("C","3"),("D","4"),("E","infinitely many")]),
10:(r"A three-quarter sector of a circle of radius $4$ inches together with its interior can be rolled up to form the lateral surface area of a right circular cone by taping together along the two radii. What is the volume of the cone in cubic inches?",[("A",r"$3\pi\sqrt5$"),("B",r"$4\pi\sqrt3$"),("C",r"$3\pi\sqrt7$"),("D",r"$6\pi\sqrt3$"),("E",r"$6\pi\sqrt7$")]),
}

KEY_OVERRIDES={1:"Evaluate subtraction of negative numbers carefully.",2:"Use cube volume as side length cubed.",3:"Chain ratios through a common variable.",4:"Use the fact that acute angles of a right triangle sum to 90 degrees.",5:"Use permutations of a multiset.",6:"Find the next palindrome and divide distance by time.",7:"A square divisible by 6 has a base divisible by 6.",8:"Separate right-angle cases at P, Q, and R.",9:"Complete the square in y.",10:"Use arc length as the cone base circumference."}

SOL={
1:[("Handle subtraction signs first",r"Subtracting a negative number is the same as adding its opposite. So the expression becomes \[1+2-3+4-5+6.\]"),("Group positives and negatives",r"The positive terms are $1,2,4,6$, and the negative terms are $-3,-5$."),("Compute",r"\[1+2+4+6-3-5=13-8=5.\]"),("Conclude",r"The answer is $\boxed{5}$."),],
2:[("Find each type of cube volume",r"A cube with side length $1$ has volume $1^3=1$. A cube with side length $2$ has volume $2^3=8$."),("Count Carl's cubes",r"Carl has $5$ cubes of volume $1$, so his total volume is \[5\cdot1=5.\]"),("Count Kate's cubes",r"Kate has $5$ cubes of volume $8$, so her total volume is \[5\cdot8=40.\]"),("Add",r"The total volume is \[5+40=45.\]"),("Conclude",r"The answer is $\boxed{45}$."),],
3:[("Use x as the common reference",r"The ratio $w:x=4:3$ means \[w=\frac43x.\] The ratio $z:x=1:6$ means \[z=\frac16x.\]"),("Find y in terms of x",r"The ratio $y:z=3:2$ gives \[y=\frac32z=\frac32\cdot\frac16x=\frac14x.\]"),("Compare w and y",r"Now \[\frac{w}{y}=\frac{\frac43x}{\frac14x}=\frac{16}{3}.\]"),("Write as a ratio",r"Thus \[w:y=16:3.\]"),("Conclude",r"The answer is $\boxed{16:3}$."),],
4:[("Use the right triangle angle sum",r"The two acute angles in a right triangle add to $90^\circ$, so \[a+b=90.\]"),("Use the prime condition",r"We need two prime numbers with $a>b$ and sum $90$. To make $b$ as small as possible, test small primes for $b$."),("Test small values",r"If $b=2$, then $a=88$, not prime. If $b=3$, then $a=87$, not prime. If $b=5$, then $a=85$, not prime."),("Find the first success",r"If $b=7$, then $a=83$, which is prime."),("Conclude",r"The least possible value of $b$ is $\boxed{7}$."),],
5:[("Count all tile positions",r"There are $1+1+2+3=7$ tiles total."),("Use a multiset permutation",r"If all tiles were distinct, there would be $7!$ arrangements. But the $2$ green tiles are identical and the $3$ yellow tiles are identical."),("Divide by repeated colors",r"The number of distinguishable arrangements is \[\frac{7!}{2!\,3!}.\]"),("Compute",r"\[\frac{5040}{2\cdot6}=420.\]"),("Conclude",r"The answer is $\boxed{420}$."),],
6:[("Find the next higher palindrome",r"The odometer reads $15951$. The next higher five-digit palindrome keeps the form $abcba$. Increasing from $15951$, the next one is $16061$."),("Compute distance traveled",r"The distance is \[16061-15951=110\] miles."),("Use time",r"The trip took $2$ hours, so the average speed was \[\frac{110}{2}=55\] miles per hour."),("Conclude",r"The answer is $\boxed{55}$."),],
7:[("Translate the divisibility condition",r"A positive even multiple of $3$ is a multiple of $6$. If a perfect square is divisible by $6$, then its square root must be divisible by both $2$ and $3$, hence by $6$."),("Write the square root",r"Let the square be $m^2$. Since $m^2<2020$, we have $m<\sqrt{2020}<45$."),("Count possible roots",r"The positive multiples of $6$ less than $45$ are \[6,12,18,24,30,36,42.\]"),("Count squares",r"Each gives one valid square, so there are $7$ such squares."),("Conclude",r"The answer is $\boxed{7}$."),],
8:[("Separate right-angle cases",r"The right angle of $\triangle PQR$ could be at $P$, at $Q$, or at $R$."),("Right angle at P or Q",r"If the right angle is at $P$, then $PR$ is perpendicular to $PQ$ and the area condition gives \[\frac12\cdot8\cdot PR=12,\] so $PR=3$. There are $2$ such points. Similarly, there are $2$ points when the right angle is at $Q$."),("Right angle at R",r"If the right angle is at $R$, then $R$ lies on the circle with diameter $PQ$. The area condition says the distance from $R$ to line $PQ$ is $3$."),("Count points on the circle",r"The circle with diameter $PQ$ has radius $4$. The two lines parallel to $PQ$ at distance $3$ from it each intersect the circle in $2$ points, giving $4$ more points."),("Add",r"The total number of locations is \[2+2+4=8.\]"),("Conclude",r"The answer is $\boxed{8}$."),],
9:[("Complete the square in y",r"The equation \[x^{2020}+y^2=2y\] becomes \[x^{2020}+(y-1)^2=1.\]"),("Use nonnegativity",r"Both terms on the left are nonnegative integers, so each is at most $1$."),("Case x=0",r"If $x=0$, then \[(y-1)^2=1,\] so $y=0$ or $y=2$."),("Case x is nonzero",r"If $x=\pm1$, then $x^{2020}=1$, so $(y-1)^2=0$ and $y=1$. If $|x|\ge2$, then $x^{2020}>1$, impossible."),("Count ordered pairs",r"The solutions are \[(0,0),(0,2),(1,1),(-1,1),\] for $4$ ordered pairs."),("Conclude",r"The answer is $\boxed{4}$."),],
10:[("Use the sector arc length",r"The sector has radius $4$, so the cone's slant height will be $4$. The arc length of a three-quarter circle of radius $4$ is \[\frac34\cdot2\pi\cdot4=6\pi.\]"),("Find the cone radius",r"When rolled into a cone, that arc becomes the base circumference. Thus \[2\pi r=6\pi,\] so $r=3$."),("Find the cone height",r"The slant height, radius, and height form a right triangle: \[h^2+3^2=4^2.\] Therefore \[h=\sqrt7.\]"),("Compute volume",r"The cone volume is \[\frac13\pi r^2h=\frac13\pi\cdot9\cdot\sqrt7=3\pi\sqrt7.\]"),("Conclude",r"The answer is $\boxed{3\pi\sqrt7}$."),],
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
        if r["year"] == "2020" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2020 AMC 10B Answer Key\n\n"
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












































