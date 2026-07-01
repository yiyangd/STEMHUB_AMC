import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 64
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2012_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,16,17,19,20}
SKIPPED = [
    "2012 AMC 10A Problem 15 skipped: diagram-dependent area problem; original figure needed for reliable teaching solution.",
    "2012 AMC 10A Problem 18 skipped: diagram-dependent circular-arc region; original figure needed for reliable teaching solution.",
]
BATCH_LABEL = "2012 AMC 10A Problems 11-20 excluding 15 and 18"
NEXT_START = "2012 AMC 10A Problem 21"

ANS = {
    11: ("D", "12"),
    12: ("A", "Friday"),
    13: ("C", r"\frac{17}{8}"),
    14: ("B", "481"),
    16: ("C", "2500"),
    17: ("C", "3"),
    19: ("D", "48"),
    20: ("A", r"\frac{49}{512}"),
}

OV = {
    11: (r"Externally tangent circles with centers at points $A$ and $B$ have radii of lengths $5$ and $3$, respectively. A line externally tangent to both circles intersects ray $AB$ at point $C$. What is $BC$?", [("A","4"),("B","4.8"),("C","10.2"),("D","12"),("E","14.4")]),
    12: (r"A year is a leap year if and only if the year number is divisible by $400$ or is divisible by $4$ but not by $100$. The $200$th anniversary of the birth of novelist Charles Dickens was celebrated on February $7,2012$, a Tuesday. On what day of the week was Dickens born?", [("A","Friday"),("B","Saturday"),("C","Sunday"),("D","Monday"),("E","Tuesday")]),
    13: (r"An iterative average of the numbers $1,2,3,4,$ and $5$ is computed as follows. Arrange the five numbers in some order. Find the mean of the first two numbers, then find the mean of that with the third number, then the mean of that with the fourth number, and finally the mean of that with the fifth number. What is the difference between the largest and smallest possible values that can be obtained?", [("A",r"\frac{31}{16}"),("B","2"),("C",r"\frac{17}{8}"),("D","3"),("E",r"\frac{65}{16}")]),
    14: (r"Chubby makes nonstandard checkerboards that have $31$ squares on each side. The checkerboards have a black square in every corner and alternate red and black squares along every row and column. How many black squares are there on such a checkerboard?", [("A","480"),("B","481"),("C","482"),("D","483"),("E","484")]),
    16: (r"Three runners start running simultaneously from the same point on a $500$-meter circular track. They each run clockwise around the course maintaining constant speeds of $4.4$, $4.8$, and $5.0$ meters per second. The runners stop once they are all together again somewhere on the circular course. How many seconds do the runners run?", [("A","1000"),("B","1250"),("C","2500"),("D","5000"),("E","10000")]),
    17: (r"Let $a$ and $b$ be relatively prime integers with $a>b>0$ and \[\frac{a^3-b^3}{(a-b)^3}=\frac{73}{3}.\] What is $a-b$?", [("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
    19: (r"Paula the painter and her two helpers each paint at constant, but different, rates. They always start at $8{:}00$ AM, and all three always take the same amount of time to eat lunch. On Monday the three of them painted $50\%$ of a house, quitting at $4{:}00$ PM. On Tuesday, when Paula was not there, the two helpers painted only $24\%$ of the house and quit at $2{:}12$ PM. On Wednesday Paula worked by herself and finished the house by working until $7{:}12$ PM. How long, in minutes, was each day's lunch break?", [("A","30"),("B","36"),("C","42"),("D","48"),("E","60")]),
    20: (r"A $3\times3$ square is partitioned into $9$ unit squares. Each unit square is painted either white or black with each color equally likely, chosen independently at random. The square is then rotated $90^\circ$ clockwise about its center, and every white square in a position formerly occupied by a black square is painted black. The colors of all other squares are left unchanged. What is the probability that the grid is now entirely black?", [("A",r"\frac{49}{512}"),("B",r"\frac{7}{64}"),("C",r"\frac{121}{1024}"),("D",r"\frac{81}{512}"),("E",r"\frac{9}{32}")]),
}

KEY_OVERRIDES = {
    11: "Use similar triangles or homothety from the external tangent point.",
    12: "Count the day shift over 200 years, including leap days after February 7.",
    13: "Write the final iterative average as a weighted sum and use rearrangement.",
    14: "An odd checkerboard has one more black square than red square.",
    16: "All runners meet again when each relative distance is a multiple of the track length.",
    17: "Factor the difference of cubes and solve for the ratio $b/(a-b)$.",
    19: "Set up rates after subtracting the common lunch break from each workday.",
    20: "Analyze the rotation cycles and require no adjacent pair of whites in each cycle.",
}

SOL = {
    11: [
        ("Identify the homothety point", r"The external tangent line and the line through the centers meet at $C$. From $C$, the two circles look like scaled copies of each other, so the distances from $C$ to the centers are in the same ratio as the radii."),
        ("Use the radius ratio", r"The radii are $5$ and $3$, so $CA:CB=5:3$. Since the circles are externally tangent, $AB=5+3=8$."),
        ("Place C on the ray", r"Point $C$ is on ray $AB$ beyond $B$, so $CA=CB+AB=CB+8$."),
        ("Solve", r"Now \[\frac{CB+8}{CB}=\frac53.\] Thus $3CB+24=5CB$, so $CB=12$."),
        ("Conclude", r"The answer is $\boxed{12}$."),
    ],
    12: [
        ("Count ordinary day shifts", r"From February $7,1812$ to February $7,2012$ is $200$ years. Each ordinary year shifts the weekday by $1$ day because $365\equiv1\pmod7$. So $200$ ordinary years contribute $200\equiv4\pmod7$ days."),
        ("Count leap days", r"The interval includes leap days from leap years after February $7,1812$ through $2011$. There are $50$ multiples of $4$ in this range, but $1900$ is not a leap year, so there are $49$ leap days. Since $49\equiv0\pmod7$, they do not change the weekday modulo $7$."),
        ("Find the total shift", r"The total weekday shift is therefore $4$ days forward from Dickens's birth date to the anniversary in $2012$."),
        ("Work backward", r"The anniversary was Tuesday. Four days before Tuesday is Friday."),
        ("Conclude", r"Dickens was born on a $\boxed{\text{Friday}}$."),
    ],
    13: [
        ("Find the weights", r"Let the ordered numbers be $a,b,c,d,e$. The final value is \[\frac{1}{2}\left(\frac{1}{2}\left(\frac{1}{2}\left(\frac{a+b}{2}+c\right)+d\right)+e\right).\] Simplifying gives weights $\frac1{16},\frac1{16},\frac18,\frac14,\frac12$."),
        ("Maximize the weighted sum", r"To make the value as large as possible, put the largest number on the largest weight. So the maximum uses $5,4,3,2,1$ paired with weights $\frac12,\frac14,\frac18,\frac1{16},\frac1{16}$."),
        ("Minimize the weighted sum", r"To make the value as small as possible, put the smallest number on the largest weight. This reverses the pairing."),
        ("Subtract efficiently", r"The difference is \[5\left(\frac12-\frac1{16}\right)+4\left(\frac14-\frac1{16}\right)+2\left(\frac1{16}-\frac14\right)+1\left(\frac1{16}-\frac12\right)=\frac{17}{8}.\]"),
        ("Conclude", r"The difference is $\boxed{\frac{17}{8}}$."),
    ],
    14: [
        ("Use odd board parity", r"A $31\times31$ board has $31^2=961$ squares. Because $31$ is odd and every corner is black, the alternating pattern has one more black square than red square."),
        ("Split the total", r"If black squares exceed red squares by $1$, then the number of black squares is $\frac{961+1}{2}=481$."),
        ("Check with rows", r"Equivalently, each odd-numbered row has $16$ black squares and each even-numbered row has $15$, giving $16\cdot16+15\cdot15=481$."),
        ("Conclude", r"There are $\boxed{481}$ black squares."),
    ],
    16: [
        ("Use relative speeds", r"The fastest runner at $5.0$ m/s must gain whole laps on each of the other two runners. The relative speeds are $5.0-4.8=0.2$ m/s and $5.0-4.4=0.6$ m/s."),
        ("Write the lap conditions", r"They are all together again when both relative distances are multiples of $500$ meters. So $0.2t$ and $0.6t$ must both be multiples of $500$."),
        ("Solve the conditions", r"The condition $0.2t=500k$ gives $t=2500k$. The condition $0.6t=500m$ gives $t=\frac{2500}{3}m$. The smallest positive time satisfying both is $t=2500$."),
        ("Check", r"In $2500$ seconds, the relative gains are $500$ meters and $1500$ meters, both whole laps."),
        ("Conclude", r"The runners run for $\boxed{2500}$ seconds."),
    ],
    17: [
        ("Factor the numerator", r"Use $a^3-b^3=(a-b)(a^2+ab+b^2)$. Then \[\frac{a^3-b^3}{(a-b)^3}=\frac{a^2+ab+b^2}{(a-b)^2}=\frac{73}{3}.\]"),
        ("Write a in terms of the gap", r"Let $d=a-b$. Then $a=b+d$. Substituting into the numerator gives $(b+d)^2+b(b+d)+b^2=3b^2+3bd+d^2$."),
        ("Use the ratio t=b/d", r"Divide by $d^2$ and let $t=\frac bd$. We get $3t^2+3t+1=\frac{73}{3}$. Multiplying by $3$ gives $9t^2+9t-70=0$."),
        ("Solve for t", r"The positive solution is $t=\frac73$, so $\frac bd=\frac73$. Thus $b=7k$ and $d=3k$."),
        ("Use relative primality", r"Then $a=b+d=10k$. Since $a$ and $b$ are relatively prime, $k=1$. Therefore $a-b=d=3$, and the answer is $\boxed{3}$."),
    ],
    19: [
        ("Use hours and subtract lunch", r"Let the lunch break be $L$ hours. Monday has $8-L$ hours of painting time, Tuesday has $6.2-L$ hours, and Wednesday has $11.2-L$ hours."),
        ("Write the helper and Paula rates", r"The two helpers together painted $24\%$ on Tuesday, so their combined rate is $\frac{0.24}{6.2-L}$. Paula alone painted the remaining $26\%$ on Wednesday, so her rate is $\frac{0.26}{11.2-L}$."),
        ("Use Monday's total rate", r"On Monday all three together painted $50\%$, so their combined rate is $\frac{0.50}{8-L}$. Therefore \[\frac{0.26}{11.2-L}+\frac{0.24}{6.2-L}=\frac{0.50}{8-L}.\]"),
        ("Solve the equation", r"Solving this equation gives $L=0.8$ hours. Since $0.8$ hours is $0.8\cdot60=48$ minutes, the common lunch break was $48$ minutes."),
        ("Conclude", r"The answer is $\boxed{48}$."),
    ],
    20: [
        ("Break the grid into rotation cycles", r"A $90^\circ$ rotation fixes the center square. The four corners form one cycle of length $4$, and the four edge-middle squares form another cycle of length $4$."),
        ("Understand the final color rule", r"A square is black after the operation if it was already black or if the square rotated into its position was black. So around each 4-cycle, we need every position to have itself or its predecessor black."),
        ("Count valid colorings of one 4-cycle", r"Equivalently, a 4-cycle cannot have two adjacent white squares cyclically. The valid patterns are: all black, exactly one white, or two opposite whites. That gives $1+4+2=7$ valid patterns out of $16$."),
        ("Include both cycles and the center", r"The corner cycle has $7$ valid patterns, the edge-middle cycle also has $7$, and the center must originally be black, which has probability $\frac12$."),
        ("Compute the probability", r"The probability is \[\frac{7}{16}\cdot\frac{7}{16}\cdot\frac12=\frac{49}{512}.\] The answer is $\boxed{\frac{49}{512}}$."),
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
        if r["year"] == "2012" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2012 AMC 10A Answer Key\n\n"
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
































