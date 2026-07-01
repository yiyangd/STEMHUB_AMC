import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 63
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2012_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2012 AMC 10A Problems 1-10"
NEXT_START = "2012 AMC 10A Problem 11"

ANS = {
    1: ("D", "25"),
    2: ("E", "$4$ by $8$"),
    3: ("E", "15"),
    4: ("C", "4"),
    5: ("B", "200"),
    6: ("D", r"\frac{15}{2}"),
    7: ("C", r"\frac47"),
    8: ("D", "7"),
    9: ("D", r"\frac13"),
    10: ("C", "8"),
}

OV = {
    1: (r"Cagney can frost a cupcake every $20$ seconds and Lacey can frost a cupcake every $30$ seconds. Working together, how many cupcakes can they frost in $5$ minutes?", [("A","10"),("B","15"),("C","20"),("D","25"),("E","30")]),
    2: (r"A square with side length $8$ is cut in half, creating two congruent rectangles. What are the dimensions of one of these rectangles?", [("A", "$2$ by $4$"),("B", "$2$ by $6$"),("C", "$2$ by $8$"),("D", "$4$ by $4$"),("E", "$4$ by $8$")]),
    3: (r"A bug crawls along a number line, starting at $-2$. It crawls to $-6$, then turns around and crawls to $5$. How many units does the bug crawl altogether?", [("A","9"),("B","11"),("C","13"),("D","14"),("E","15")]),
    4: (r"Let $\angle ABC=24^\circ$ and $\angle ABD=20^\circ$. What is the smallest possible degree measure for $\angle CBD$?", [("A","0"),("B","2"),("C","4"),("D","6"),("E","12")]),
    5: (r"Last year $100$ adult cats, half of whom were female, were brought into the Smallville Animal Shelter. Half of the adult female cats were accompanied by a litter of kittens. The average number of kittens per litter was $4$. What was the total number of cats and kittens received by the shelter last year?", [("A","150"),("B","200"),("C","250"),("D","300"),("E","400")]),
    6: (r"The product of two positive numbers is $9$. The reciprocal of one of these numbers is $4$ times the reciprocal of the other number. What is the sum of the two numbers?", [("A",r"\frac{10}{3}"),("B",r"\frac{20}{3}"),("C","7"),("D",r"\frac{15}{2}"),("E","8")]),
    7: (r"In a bag of marbles, $\frac35$ of the marbles are blue and the rest are red. If the number of red marbles is doubled and the number of blue marbles stays the same, what fraction of the marbles will be red?", [("A",r"\frac25"),("B",r"\frac37"),("C",r"\frac47"),("D",r"\frac35"),("E",r"\frac45")]),
    8: (r"The sums of three whole numbers taken in pairs are $12$, $17$, and $19$. What is the middle number?", [("A","4"),("B","5"),("C","6"),("D","7"),("E","8")]),
    9: (r"A pair of six-sided fair dice are labeled so that one die has only even numbers, two each of $2,4,$ and $6$, and the other die has only odd numbers, two each of $1,3,$ and $5$. The pair of dice is rolled. What is the probability that the sum of the numbers on top of the two dice is $7$?", [("A",r"\frac16"),("B",r"\frac15"),("C",r"\frac14"),("D",r"\frac13"),("E",r"\frac12")]),
    10: (r"Mary divides a circle into $12$ sectors. The central angles of these sectors, measured in degrees, are all integers and they form an arithmetic sequence. What is the degree measure of the smallest possible sector angle?", [("A","5"),("B","6"),("C","8"),("D","10"),("E","12")]),
}

KEY_OVERRIDES = {
    1: "Add work rates and multiply by the total time.",
    2: "Cutting an $8$ by $8$ square in half halves one dimension and keeps the other unchanged.",
    3: "Distance traveled on a number line is the sum of absolute changes, not just final displacement.",
    4: "To minimize the angle between two rays, place them on the same side of the common ray.",
    5: "Count female cats, litters, and kittens separately before adding the original adult cats.",
    6: "Turn the reciprocal condition into a ratio between the two positive numbers.",
    7: "Use convenient total marbles to track the changing red and blue counts.",
    8: "Add the pairwise sums to get twice the sum of the three numbers.",
    9: "Count the equally likely displayed values on the even die and odd die.",
    10: "Use the arithmetic-sequence sum formula and integer constraints.",
}

SOL = {
    1: [
        ("Convert the time", r"Five minutes is $5\cdot60=300$ seconds. Working in seconds matches the frosting rates in the problem."),
        ("Find each person's output", r"Cagney frosts one cupcake every $20$ seconds, so in $300$ seconds Cagney can frost $300/20=15$ cupcakes. Lacey frosts one every $30$ seconds, so Lacey can frost $300/30=10$ cupcakes."),
        ("Add the outputs", r"Since they work together on separate cupcakes, their outputs add. The total is $15+10=25$."),
        ("Conclude", r"Together they can frost $\boxed{25}$ cupcakes."),
    ],
    2: [
        ("Start with the square", r"The original square has dimensions $8$ by $8$. Cutting it into two congruent rectangles means each rectangle has half the area of the square."),
        ("Think about the cut", r"A straight cut through the middle parallel to a side keeps one dimension equal to $8$ and cuts the other dimension from $8$ to $4$."),
        ("Check the area", r"Each rectangle is $4$ by $8$, with area $32$, exactly half of the square's area $64$."),
        ("Conclude", r"The dimensions are $\boxed{4\text{ by }8}$."),
    ],
    3: [
        ("Separate the two parts of the trip", r"The bug first moves from $-2$ to $-6$. That distance is $|-6-(-2)|=4$ units."),
        ("Find the second distance", r"Then the bug moves from $-6$ to $5$. That distance is $|5-(-6)|=11$ units."),
        ("Add distances, not endpoints", r"The bug turned around, so the total distance is $4+11=15$, not just the distance from the starting point to the ending point."),
        ("Conclude", r"The bug crawls $\boxed{15}$ units altogether."),
    ],
    4: [
        ("Understand the geometry", r"Both angles have vertex $B$ and share ray $BA$. We want the smallest possible angle between rays $BC$ and $BD$."),
        ("Place the rays close together", r"The smallest angle happens when $BC$ and $BD$ are on the same side of $BA$, because then the smaller angle between them is the difference of the two given angles."),
        ("Subtract", r"The difference is $24^\circ-20^\circ=4^\circ$."),
        ("Conclude", r"The smallest possible measure of $\angle CBD$ is $\boxed{4^\circ}$."),
    ],
    5: [
        ("Count the adult female cats", r"There were $100$ adult cats, and half were female. So there were $50$ adult female cats."),
        ("Count the litters", r"Half of the adult female cats had litters, so there were $25$ litters of kittens."),
        ("Count the kittens", r"Each litter had an average of $4$ kittens, so the shelter received $25\cdot4=100$ kittens."),
        ("Add adults and kittens", r"The shelter received $100$ adult cats and $100$ kittens, for a total of $200$ animals. The answer is $\boxed{200}$."),
    ],
    6: [
        ("Name the numbers", r"Let the two positive numbers be $a$ and $b$, with $ab=9$. The reciprocal condition says one reciprocal is four times the other. We may write $\frac1a=4\cdot\frac1b$."),
        ("Turn reciprocals into a ratio", r"From $\frac1a=\frac4b$, cross-multiply to get $b=4a$."),
        ("Use the product", r"Substitute into $ab=9$: $a(4a)=9$, so $4a^2=9$ and $a=\frac32$ because the numbers are positive. Then $b=4a=6$."),
        ("Find the sum", r"The sum is $\frac32+6=\frac{15}{2}$. The answer is $\boxed{\frac{15}{2}}$."),
    ],
    7: [
        ("Choose a convenient total", r"Since $\frac35$ of the marbles are blue, use $5$ marbles as a convenient model. Then $3$ are blue and $2$ are red."),
        ("Double only the red marbles", r"Doubling the red marbles changes the red count from $2$ to $4$, while the blue count stays $3$."),
        ("Find the new total", r"The new total is $4+3=7$ marbles in this model."),
        ("Compute the red fraction", r"The fraction that are red is $\frac47$. The answer is $\boxed{\frac47}$."),
    ],
    8: [
        ("Name the numbers", r"Let the three whole numbers be $a,b,c$. Their pairwise sums are $12$, $17$, and $19$."),
        ("Add the pairwise sums", r"Adding all three pairwise sums counts each number twice: $(a+b)+(a+c)+(b+c)=2(a+b+c)$."),
        ("Find the total", r"The given sums add to $12+17+19=48$, so $2(a+b+c)=48$ and $a+b+c=24$."),
        ("Recover the numbers", r"If one pair sums to $12$, then the remaining number is $24-12=12$. Similarly the other remaining numbers are $24-17=7$ and $24-19=5$. The numbers are $5,7,12$."),
        ("Conclude", r"The middle number is $\boxed{7}$."),
    ],
    9: [
        ("Reduce the dice to value choices", r"Each even value $2,4,6$ appears twice, so each has probability $\frac13$ on the even die. Similarly, each odd value $1,3,5$ has probability $\frac13$ on the odd die."),
        ("List sums of 7", r"The pairs that sum to $7$ are $(2,5)$, $(4,3)$, and $(6,1)$."),
        ("Count among value pairs", r"There are $3\cdot3=9$ equally likely value pairs, and $3$ of them sum to $7$."),
        ("Compute the probability", r"The probability is $\frac39=\frac13$. The answer is $\boxed{\frac13}$."),
    ],
    10: [
        ("Use the sum of all central angles", r"The $12$ sector angles add to $360^\circ$. Since they form an arithmetic sequence, let the first angle be $a$ and common difference be $d$, where $a$ and $d$ are integers."),
        ("Apply the arithmetic-sequence sum", r"The sum is \[\frac{12}{2}(2a+11d)=360,\] so $2a+11d=60$."),
        ("Minimize the first angle", r"To make $a$ small, make $d$ as large as possible while keeping $a$ positive and integral. Since $2a=60-11d$, $d$ must be even. The largest even $d$ with positive $a$ is $d=4$."),
        ("Compute a", r"Then $2a=60-44=16$, so $a=8$."),
        ("Conclude", r"The smallest possible sector angle is $\boxed{8^\circ}$."),
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































