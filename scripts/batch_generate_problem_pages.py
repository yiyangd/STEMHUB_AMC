import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 79
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2014_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,17,18,20}
SKIPPED = ["2014 AMC 10A Problem 16 skipped: shaded region depends on missing diagram", "2014 AMC 10A Problem 19 skipped: cube stack line segment depends on missing diagram"]
BATCH_LABEL = "2014 AMC 10A Problems 11-20 excluding 16 and 19"
NEXT_START = "2014 AMC 10A Problem 21"

ANS={11:("C",r"\$219.95"),12:("C",r"54\sqrt3-18\pi"),13:("C",r"3+\sqrt3"),14:("D","60"),15:("C","210"),17:("D",r"\frac{5}{24}"),18:("B","17"),20:("D","991")}

OV={
11:(r"A customer who intends to purchase an appliance has three coupons, only one of which may be used. Coupon 1 gives $10\%$ off the listed price if the listed price is at least $\$50$. Coupon 2 gives $\$20$ off the listed price if the listed price is at least $\$100$. Coupon 3 gives $18\%$ off the amount by which the listed price exceeds $\$100$. For which listed price will coupon 1 offer a greater price reduction than either coupon 2 or coupon 3?",[("A",r"\$179.95"),("B",r"\$199.95"),("C",r"\$219.95"),("D",r"\$239.95"),("E",r"\$259.95")]),
12:(r"A regular hexagon has side length $6$. Congruent arcs with radius $3$ are drawn with center at each of the vertices, creating circular sectors. What is the area of the region inside the hexagon but outside the sectors?",[("A",r"27\sqrt3-9\pi"),("B",r"27\sqrt3-6\pi"),("C",r"54\sqrt3-18\pi"),("D",r"54\sqrt3-12\pi"),("E",r"108\sqrt3-9\pi")]),
13:(r"Equilateral triangle $ABC$ has side length $1$, and squares $ABDE$, $BCHI$, and $CAFG$ lie outside the triangle. What is the area of hexagon $DEFGHI$?",[("A",r"\frac{12+3\sqrt3}{6}"),("B",r"\frac94"),("C",r"3+\sqrt3"),("D",r"\frac{6+3\sqrt3}{2}"),("E","6")]),
14:(r"The $y$-intercepts, $P$ and $Q$, of two perpendicular lines intersecting at the point $A(6,8)$ have a sum of zero. What is the area of $\triangle APQ$?",[("A","45"),("B","48"),("C","54"),("D","60"),("E","72")]),
15:(r"David drives from his home to the airport to catch a flight. He drives $35$ miles in the first hour, but realizes that he will be $1$ hour late if he continues at this speed. He increases his speed by $15$ miles per hour for the rest of the way to the airport and arrives $30$ minutes early. How many miles is the airport from his home?",[("A","140"),("B","175"),("C","210"),("D","245"),("E","280")]),
17:(r"Three fair six-sided dice are rolled. What is the probability that the values shown on two of the dice sum to the value shown on the remaining die?",[("A",r"\frac16"),("B",r"\frac{13}{72}"),("C",r"\frac7{36}"),("D",r"\frac5{24}"),("E",r"\frac29")]),
18:(r"A square in the coordinate plane has vertices whose $y$-coordinates are $0$, $1$, $4$, and $5$. What is the area of the square?",[("A","16"),("B","17"),("C","25"),("D","26"),("E","27")]),
20:(r"The product $(8)(888\ldots8)$, where the second factor has $k$ digits, is an integer whose digits have a sum of $1000$. What is $k$?",[("A","901"),("B","911"),("C","919"),("D","991"),("E","999")]),
}

KEY_OVERRIDES={11:"Translate each coupon into a reduction formula and compare inequalities.",12:"Subtract six equal circular sectors from the area of a regular hexagon.",13:"Decompose the outer hexagon into three squares and four equilateral-triangle pieces.",14:"Use slopes of perpendicular lines and the y-intercepts as the triangle base.",15:"Compare the two remaining-travel times after the first hour.",17:"Count ordered dice triples by choosing which die equals the sum of the other two.",18:"Use the vertical components of perpendicular side vectors of a square.",20:"Find the digit pattern in 8 times a k-digit number made of all 8s."}

SOL={
11:[("Turn each coupon into a formula",r"Let the listed price be $p$. Coupon 1 saves $0.10p$, coupon 2 saves $20$, and coupon 3 saves $0.18(p-100)$."),("Beat coupon 2",r"For coupon 1 to beat coupon 2, we need $0.10p>20$, so $p>200$."),("Beat coupon 3",r"For coupon 1 to beat coupon 3, we need $0.10p>0.18(p-100)$. This simplifies to $18>0.08p$, so $p<225$."),("Use the choices",r"The price must be greater than $200$ and less than $225$. Among the choices, only $\$219.95$ lies in that interval."),("Conclude",r"The answer is $\boxed{\$219.95}$."),],
12:[("Find the hexagon area",r"A regular hexagon of side length $6$ is made of six equilateral triangles of side $6$. Its area is $6\cdot\frac{\sqrt3}{4}\cdot6^2=54\sqrt3$."),("Understand each sector",r"At each vertex of a regular hexagon, the interior angle is $120^\circ$. The drawn sector has radius $3$, so one sector has area $\frac{120}{360}\pi(3^2)=3\pi$."),("Subtract all six sectors",r"There are six congruent sectors. Their total area is $6\cdot3\pi=18\pi$."),("Compute the shaded area",r"The shaded region is the part of the hexagon outside these sectors, so its area is $54\sqrt3-18\pi$."),("Conclude",r"The answer is $\boxed{54\sqrt3-18\pi}$."),],
13:[("Decompose the hexagon",r"The outer hexagon contains the original equilateral triangle, the three outward squares, and three small corner triangles between neighboring squares."),("Count the easy pieces",r"Each square has area $1$, so the three squares have area $3$. The central equilateral triangle has area $\frac{\sqrt3}{4}$."),("Find one corner triangle",r"At a vertex such as $A$, the two square sides sticking out have length $1$. The angle between them is $360^\circ-90^\circ-60^\circ-90^\circ=120^\circ$."),("Compute the three corner areas",r"One such triangle has area $\frac12\cdot1\cdot1\cdot\sin120^\circ=\frac{\sqrt3}{4}$. There are three of them, contributing $\frac{3\sqrt3}{4}$."),("Add all pieces",r"The total area is $3+\frac{\sqrt3}{4}+\frac{3\sqrt3}{4}=3+\sqrt3$."),("Conclude",r"The answer is $\boxed{3+\sqrt3}$."),],
14:[("Name the intercepts",r"Let $P=(0,p)$ and $Q=(0,q)$. The problem says their intercepts sum to zero, so $q=-p$."),("Write the slopes",r"The slopes of the two lines through $A(6,8)$ are $\frac{8-p}{6}$ and $\frac{8+p}{6}$."),("Use perpendicular slopes",r"Perpendicular nonvertical lines have slope product $-1$, so \[\frac{(8-p)(8+p)}{36}=-1.\] Thus $64-p^2=-36$, and $p^2=100$."),("Find the triangle area",r"The distance $PQ$ is $20$, and the horizontal distance from $A$ to the $y$-axis is $6$. Thus \[[APQ]=\frac12\cdot20\cdot6=60.\]"),("Conclude",r"The answer is $\boxed{60}$."),],
15:[("Compare the same remaining distance",r"After the first hour, David has traveled $35$ miles. Let the total distance be $D$, so the remaining distance is $D-35$."),("Translate the time information",r"If he stays at $35$ mph, he is $1$ hour late. If he drives the rest at $50$ mph, he is $30$ minutes early. The difference between those remaining travel times is therefore $1.5$ hours."),("Set up the equation",r"\[\frac{D-35}{35}-\frac{D-35}{50}=1.5.\] This compares only the part of the trip after the first hour."),("Solve",r"The left side is $(D-35)\left(\frac1{35}-\frac1{50}\right)=(D-35)\frac{15}{1750}$. Therefore $D-35=175$."),("Conclude",r"So $D=210$, and the answer is $\boxed{210}$."),],
17:[("Count ordered outcomes",r"Rolling three dice gives $6^3=216$ ordered outcomes. Ordered counting is natural because the dice can be thought of as first, second, and third."),("Choose the die that is the sum",r"There are $3$ choices for which die shows the value equal to the sum of the other two dice."),("Count the two smaller dice",r"If the other two values are $x$ and $y$, then $x+y\le6$. The number of ordered pairs with sum $2,3,4,5,6$ is $1+2+3+4+5=15$."),("Compute the probability",r"Thus there are $3\cdot15=45$ favorable ordered outcomes. The probability is $\frac{45}{216}=\frac5{24}$."),("Conclude",r"The answer is $\boxed{\frac5{24}}$."),],
18:[("Think in side vectors",r"A square can be described by one side vector $(u,v)$ and the perpendicular side vector $(-v,u)$. Starting from one vertex, the four $y$-coordinates differ by $0$, $v$, $u$, and $u+v$."),("Match the given y-coordinates",r"The set of $y$-coordinates is $\{0,1,4,5\}$. This matches $0$, $1$, $4$, and $1+4$, so the vertical components of the two side vectors can be $1$ and $4$."),("Find the side length squared",r"If perpendicular side vectors have vertical components $1$ and $4$, their horizontal components can be arranged so the side length squared is $1^2+4^2=17$."),("Connect area and side length",r"The area of a square is the square of its side length. Therefore the area is $17$."),("Conclude",r"The answer is $\boxed{17}$."),],
20:[("Look at small cases",r"Compute a few products: $8\cdot88=704$, $8\cdot888=7104$, and $8\cdot8888=71104$. The pattern is a leading $7$, then several $1$'s, then $04$."),("Describe the pattern",r"For a $k$-digit number made entirely of $8$'s, with $k\ge2$, the product has digits $7$, then $k-2$ copies of $1$, then $04$."),("Find the digit sum",r"The digit sum is therefore $7+(k-2)\cdot1+0+4=k+9$."),("Set the required sum",r"The digit sum is given as $1000$, so $k+9=1000$. Hence $k=991$."),("Conclude",r"The answer is $\boxed{991}$."),],
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
    if n == 17 and notes == "题面包含图形":
        notes = ""
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in {12,13} else notes
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
        if r["year"] == "2014" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {12,13},
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
        + "- Answer verification source: AoPS 2014 AMC 10A Answer Key\n\n"
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












































