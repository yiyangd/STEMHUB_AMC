import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 59
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2011_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2011 AMC 10B Problems 1-10"
NEXT_START = "2011 AMC 10B Problem 11"

ANS = {
    1: ("C", r"\frac{7}{12}"),
    2: ("E", "95"),
    3: ("A", "3.75"),
    4: ("C", r"\frac{B-A}{2}"),
    5: ("E", "224"),
    6: ("A", "30"),
    7: ("B", "72"),
    8: ("B", "The temperature was cooler than $80^\circ F$ or it was not sunny."),
    9: ("D", r"\frac{4\sqrt3}{3}"),
    10: ("B", "9"),
}

OV = {
    1: (r"What is $\frac{2+4+6}{1+3+5}-\frac{1+3+5}{2+4+6}$?", [("A",r"-\frac{1}{36}"),("B",r"\frac{5}{12}"),("C",r"\frac{7}{12}"),("D",r"\frac{147}{60}"),("E",r"\frac{43}{3}")]),
    2: (r"Josanna's test scores to date are $90,80,70,60,$ and $85$. Her goal is to raise her test average at least $3$ points with her next test. What is the minimum test score she would need to accomplish this goal?", [("A","80"),("B","82"),("C","85"),("D","90"),("E","95")]),
    3: (r"At a store, when a length is reported as $x$ inches that means the length is at least $x-0.5$ inches and at most $x+0.5$ inches. Suppose the dimensions of a rectangular tile are reported as $2$ inches by $3$ inches. In square inches, what is the minimum area for the rectangle?", [("A","3.75"),("B","4.5"),("C","5"),("D","6"),("E","8.75")]),
    4: (r"LeRoy and Bernardo went on a week-long trip together and agreed to share the costs equally. At the end of the trip LeRoy had paid $A$ dollars and Bernardo had paid $B$ dollars, where $A<B$. How many dollars must LeRoy give to Bernardo so that they share the costs equally?", [("A",r"\frac{A+B}{2}"),("B",r"\frac{A-B}{2}"),("C",r"\frac{B-A}{2}"),("D",r"B-A"),("E",r"A+B")]),
    5: (r"In multiplying two positive integers $a$ and $b$, Ron reversed the digits of the two-digit number $a$. His erroneous product was $161$. What is the correct value of the product of $a$ and $b$?", [("A","116"),("B","161"),("C","204"),("D","214"),("E","224")]),
    6: (r"On Halloween Casper ate $\frac13$ of his candies and then gave $2$ candies to his brother. The next day he ate $\frac13$ of his remaining candies and then gave $4$ candies to his sister. On the third day he ate his final $8$ candies. How many candies did Casper have at the beginning?", [("A","30"),("B","39"),("C","48"),("D","57"),("E","66")]),
    7: (r"The sum of two angles of a triangle is $\frac65$ of a right angle, and one of these two angles is $30^\circ$ larger than the other. What is the degree measure of the largest angle in the triangle?", [("A","69"),("B","72"),("C","90"),("D","102"),("E","108")]),
    8: (r"At a certain beach, if it is at least $80^\circ F$ and sunny, then the beach will be crowded. On June 10 the beach was not crowded. What can be said about the weather conditions on June 10?", [("A",r"The temperature was cooler than $80^\circ F$ and it was not sunny."),("B",r"The temperature was cooler than $80^\circ F$ or it was not sunny."),("C",r"If the temperature was at least $80^\circ F$, then it was sunny."),("D",r"If the temperature was cooler than $80^\circ F$, then it was sunny."),("E",r"If the temperature was cooler than $80^\circ F$, then it was not sunny.")]),
    9: (r"In the diagram, $\triangle ABC$ is a $3$-$4$-$5$ triangle with $AC=3$, $BC=4$, and $AB=5$. Point $D$ lies on $\overline{AB}$, point $E$ lies on $\overline{BC}$, and $DE\perp AB$. The area of $\triangle EBD$ is one third of the area of $\triangle ABC$. What is $BD$?", [("A",r"\frac43"),("B",r"\sqrt5"),("C",r"\frac94"),("D",r"\frac{4\sqrt3}{3}"),("E",r"\frac52")]),
    10: (r"Consider the set of numbers $\{1,10,10^2,10^3,\ldots,10^{10}\}$. The ratio of the largest element of the set to the sum of the other ten elements is closest to which integer?", [("A","1"),("B","9"),("C","10"),("D","11"),("E","101")]),
}

KEY_OVERRIDES = {
    1: "Compute the two simple sums first, then subtract the fractions.",
    2: "Translate a desired average increase into a required total score.",
    3: "Use the smallest possible dimensions allowed by the rounding rule.",
    4: "Equal sharing means each person should end up paying half the total cost.",
    5: "Factor the erroneous product to recover the reversed two-digit number.",
    6: "Work backward from the final number of candies.",
    7: "Use the sum of two angles and their difference to find the triangle's angles.",
    8: "Use the contrapositive/negation of an AND statement.",
    9: "Use similarity and the area ratio between the smaller and larger right triangles.",
    10: "Use the geometric-series sum and compare the resulting ratio to nearby integers.",
}

SOL = {
    1: [
        ("Compute the sums", r"The numerator $2+4+6$ is $12$, and the denominator $1+3+5$ is $9$. So the expression becomes $\frac{12}{9}-\frac{9}{12}$."),
        ("Simplify each fraction", r"We have $\frac{12}{9}=\frac43$ and $\frac{9}{12}=\frac34$."),
        ("Subtract with a common denominator", r"Using denominator $12$, $\frac43=\frac{16}{12}$ and $\frac34=\frac9{12}$."),
        ("Finish", r"The difference is $\frac{16}{12}-\frac9{12}=\frac7{12}$. The answer is $\boxed{\frac7{12}}$."),
    ],
    2: [
        ("Find the current total", r"Josanna's five scores add to $90+80+70+60+85=385$. Her current average is $385/5=77$."),
        ("Set the target average", r"She wants to raise her average by at least $3$ points, so after the next test the average should be at least $80$."),
        ("Translate to a total", r"After six tests, an average of $80$ requires a total of $6\cdot80=480$ points."),
        ("Find the needed score", r"She already has $385$ points, so she needs $480-385=95$ on the next test. The answer is $\boxed{95}$."),
    ],
    3: [
        ("Use the lower bounds", r"To minimize the area, choose the smallest possible value for each reported dimension. A reported length of $2$ inches could be as small as $1.5$ inches."),
        ("Find the other smallest dimension", r"A reported length of $3$ inches could be as small as $2.5$ inches."),
        ("Multiply for area", r"The minimum possible area is $1.5\cdot2.5=3.75$ square inches."),
        ("Conclude", r"The answer is $\boxed{3.75}$."),
    ],
    4: [
        ("Find each person's fair share", r"Together they paid $A+B$ dollars. If they share equally, each person should pay $\frac{A+B}{2}$."),
        ("Compare LeRoy's payment to his share", r"LeRoy has already paid $A$ dollars. Since $A<B$, he paid less than half, so he must pay Bernardo the difference between his fair share and what he already paid."),
        ("Compute the difference", r"That amount is $\frac{A+B}{2}-A=\frac{A+B-2A}{2}=\frac{B-A}{2}$."),
        ("Conclude", r"LeRoy must give Bernardo $\boxed{\frac{B-A}{2}}$ dollars."),
    ],
    5: [
        ("Factor the wrong product", r"The erroneous product was $161$, and $161=7\cdot23$. Since Ron reversed a two-digit number, the reversed version of $a$ is likely one of these two factors."),
        ("Identify the reversed number", r"The reversed number must be two digits, so it is $23$, not $7$. Therefore the original value of $a$ was $32$."),
        ("Find the other factor", r"If the wrong product used $23$, then $b=7$."),
        ("Compute the correct product", r"The correct product is $32\cdot7=224$. The answer is $\boxed{224}$."),
    ],
    6: [
        ("Work backward", r"Forward fractions can be messy, so start from the end. On the third day Casper ate his final $8$ candies, so he had $8$ candies after giving $4$ to his sister the previous day."),
        ("Undo the gift to his sister", r"Before giving away $4$ candies, he had $8+4=12$ candies. This was after he ate $\frac13$ of that day's starting amount, so $12$ is $\frac23$ of what he had at the start of the second day."),
        ("Undo the second-day eating", r"If $\frac23$ of the second-day starting amount is $12$, then the second-day starting amount was $18$."),
        ("Undo the first day", r"After the first day gift of $2$ candies, he had $18$, so before that gift he had $20$. This was $\frac23$ of his original amount, so the original amount was $30$."),
        ("Conclude", r"Casper began with $\boxed{30}$ candies."),
    ],
    7: [
        ("Convert the right angle information", r"A right angle is $90^\circ$, so $\frac65$ of a right angle is $\frac65\cdot90=108^\circ$."),
        ("Set up the two angles", r"Let the smaller of the two angles be $x$. Then the larger of the two is $x+30$. Their sum is $108$, so $x+(x+30)=108$."),
        ("Solve for the two angles", r"This gives $2x=78$, so $x=39$. The two angles are $39^\circ$ and $69^\circ$."),
        ("Find the third angle", r"The third angle is $180-108=72^\circ$. Comparing $39$, $69$, and $72$, the largest angle is $72^\circ$."),
        ("Conclude", r"The answer is $\boxed{72}$."),
    ],
    8: [
        ("Name the condition", r"The statement says: if the temperature is at least $80^\circ F$ and it is sunny, then the beach is crowded. In symbols, $(T\text{ and }S)\Rightarrow C$."),
        ("Use the given fact", r"On June 10 the beach was not crowded, so $C$ was false. Therefore the condition $T\text{ and }S$ could not have been true."),
        ("Negate the AND statement", r"The negation of '$T$ and $S$' is 'not $T$ or not $S$.' This means the temperature was cooler than $80^\circ F$ or it was not sunny."),
        ("Conclude", r"The answer is $\boxed{\text{cooler than }80^\circ F\text{ or not sunny}}$."),
    ],
    9: [
        ("Use the diagram relationship", r"The large triangle $ABC$ is a $3$-$4$-$5$ right triangle, and $DE\perp AB$. The smaller triangle $EBD$ shares angle $B$ with the large triangle and has a right angle, so $\triangle EBD\sim\triangle ABC$."),
        ("Use area ratio to get side ratio", r"The area of $\triangle EBD$ is one third of the area of $\triangle ABC$. For similar triangles, areas scale as the square of side lengths, so the side-length scale factor is $\sqrt{\frac13}=\frac{1}{\sqrt3}$."),
        ("Match corresponding sides", r"Side $BD$ in the smaller triangle corresponds to side $BC=4$ in the large triangle. Therefore $BD=4\cdot\frac{1}{\sqrt3}=\frac{4}{\sqrt3}$."),
        ("Rationalize", r"Rationalizing gives $BD=\frac{4\sqrt3}{3}$."),
        ("Conclude", r"The answer is $\boxed{\frac{4\sqrt3}{3}}$."),
    ],
    10: [
        ("Identify the largest element", r"The largest element is $10^{10}$. The sum of the other ten elements is $1+10+10^2+\cdots+10^9$."),
        ("Use the geometric sum", r"The denominator is a geometric series: \[1+10+10^2+\cdots+10^9=\frac{10^{10}-1}{9}.\]"),
        ("Form the ratio", r"The ratio is \[\frac{10^{10}}{(10^{10}-1)/9}=\frac{9\cdot10^{10}}{10^{10}-1}.\] This is just slightly bigger than $9$."),
        ("Choose the closest integer", r"Since the ratio is a tiny bit more than $9$ and much closer to $9$ than to $10$, the closest integer is $9$. The answer is $\boxed{9}$."),
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {9}) else notes
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {9},
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


























