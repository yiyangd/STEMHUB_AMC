import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 84
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2015_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2015 AMC 10A Problems 1-10"
NEXT_START = "2015 AMC 10A Problem 11"

ANS={1:("C",r"\frac15"),2:("D","9"),3:("D","22"),4:("B",r"\frac16"),5:("E","95"),6:("B",r"\frac32"),7:("B","21"),8:("B","4"),9:("D","The first height is 21% more than the second."),10:("C","2")}

OV={
1:(r"What is the value of $\left(2^0-1+5^2+0\right)^{-1}\times5$?",[("A","-125"),("B","-120"),("C",r"\frac15"),("D",r"\frac5{24}"),("E","25")]),
2:(r"A box contains a collection of triangular and square tiles. There are $25$ tiles in the box, containing $84$ edges total. How many square tiles are there in the box?",[("A","3"),("B","5"),("C","7"),("D","9"),("E","11")]),
3:(r"Ann made a $3$-step staircase using $18$ toothpicks. How many toothpicks does she need to add to complete a $5$-step staircase?",[("A","9"),("B","18"),("C","20"),("D","22"),("E","24")]),
4:(r"Pablo, Sofia, and Mia got some candy eggs at a party. Pablo had three times as many eggs as Sofia, and Sofia had twice as many eggs as Mia. Pablo decides to give some of his eggs to Sofia and Mia so that all three will have the same number of eggs. What fraction of his eggs should Pablo give to Sofia?",[("A",r"\frac1{12}"),("B",r"\frac16"),("C",r"\frac14"),("D",r"\frac13"),("E",r"\frac12")]),
5:(r"Mr. Patrick teaches math to $15$ students. He was grading tests and found that when he graded everyone's test except Payton's, the average grade for the class was $80$. After he graded Payton's test, the class average became $81$. What was Payton's score on the test?",[("A","81"),("B","85"),("C","91"),("D","94"),("E","95")]),
6:(r"The sum of two positive numbers is $5$ times their difference. What is the ratio of the larger number to the smaller?",[("A",r"\frac52"),("B",r"\frac32"),("C",r"\frac95"),("D","2"),("E",r"\frac54")]),
7:(r"How many terms are there in the arithmetic sequence $13,16,19,\ldots,70,73$?",[("A","20"),("B","21"),("C","24"),("D","60"),("E","61")]),
8:(r"Two years ago Pete was three times as old as his cousin Claire. Two years before that, Pete was four times as old as Claire. In how many years will the ratio of their ages be $2:1$?",[("A","2"),("B","4"),("C","5"),("D","6"),("E","8")]),
9:(r"Two right circular cylinders have the same volume. The radius of the second cylinder is $10\%$ more than the radius of the first. What is the relationship between the heights of the two cylinders?",[("A","The second height is 10% less than the first."),("B","The first height is 10% more than the second."),("C","The second height is 21% less than the first."),("D","The first height is 21% more than the second."),("E","The second height is 80% of the first.")]),
10:(r"How many rearrangements of $abcd$ are there in which no two adjacent letters are also adjacent letters in the alphabet? For example, no such rearrangement could include either $ab$ or $ba$.",[("A","0"),("B","1"),("C","2"),("D","3"),("E","4")]),
}

KEY_OVERRIDES={1:"Simplify inside the parentheses before applying the reciprocal.",2:"Use a system for triangular and square tiles.",3:"Use the toothpick count formula for an n-step staircase.",4:"Scale the three people's amounts to a simple ratio.",5:"Compare total class scores before and after one test is added.",6:"Convert the sum-difference condition into an equation for the ratio.",7:"Use the arithmetic sequence nth-term formula.",8:"Set up ages at two different times.",9:"Equal volumes mean radius squared and height vary inversely.",10:"Count the few valid permutations after excluding alphabet-adjacent pairs."}

SOL={
1:[("Simplify the inside first",r"Inside the parentheses, $2^0=1$ and $5^2=25$. So \[2^0-1+5^2+0=1-1+25=25.\]"),("Apply the reciprocal",r"The exponent $-1$ means reciprocal, so $25^{-1}=\frac1{25}$."),("Multiply by 5",r"The whole expression is $\frac1{25}\cdot5=\frac15$."),("Conclude",r"The answer is $\boxed{\frac15}$."),],
2:[("Name the tile counts",r"Let $t$ be the number of triangular tiles and $s$ be the number of square tiles. Then $t+s=25$."),("Use the edge count",r"Triangles have $3$ edges and squares have $4$ edges, so $3t+4s=84$."),("Subtract the equations",r"Multiply the first equation by $3$ to get $3t+3s=75$. Subtracting from $3t+4s=84$ gives $s=9$."),("Conclude",r"There are $\boxed{9}$ square tiles."),],
3:[("Look for the total staircase count",r"For an $n$-step toothpick staircase, the total number of toothpicks is $n(n+3)$. This matches the given $3$-step staircase because $3(3+3)=18$."),("Find the five-step total",r"A $5$-step staircase needs $5(5+3)=40$ toothpicks."),("Compute how many to add",r"Ann already has $18$ toothpicks in the $3$-step staircase, so she must add $40-18=22$ toothpicks."),("Conclude",r"The answer is $\boxed{22}$."),],
4:[("Choose a simple scale",r"Let Mia have $m$ eggs. Then Sofia has $2m$, and Pablo has $3(2m)=6m$."),("Find the equal final amount",r"The total is $m+2m+6m=9m$, so if all three end equal, each person must have $3m$."),("Find what Sofia needs",r"Sofia starts with $2m$ and must end with $3m$, so Pablo gives Sofia $m$ eggs."),("Convert to a fraction of Pablo's eggs",r"Pablo started with $6m$ eggs, so the fraction he gives to Sofia is $\frac{m}{6m}=\frac16$."),("Conclude",r"The answer is $\boxed{\frac16}$."),],
5:[("Find the total before Payton",r"There are $14$ graded tests before Payton's test. Their average is $80$, so their total is $14\cdot80=1120$."),("Find the total after Payton",r"After all $15$ tests are graded, the average is $81$, so the total is $15\cdot81=1215$."),("Subtract",r"Payton's score is the difference between these totals: $1215-1120=95$."),("Conclude",r"The answer is $\boxed{95}$."),],
6:[("Name the numbers",r"Let the larger number be $L$ and the smaller number be $S$. The difference is $L-S$."),("Translate the sentence",r"The sum is five times the difference, so \[L+S=5(L-S).\]"),("Solve for the ratio",r"Expanding gives $L+S=5L-5S$, so $6S=4L$. Thus $\frac{L}{S}=\frac{6}{4}=\frac32$."),("Conclude",r"The ratio of the larger to the smaller is $\boxed{\frac32}$."),],
7:[("Use the arithmetic sequence formula",r"The sequence starts at $13$ and has common difference $3$. The $n$th term is $13+3(n-1)$."),("Set the last term",r"The last term is $73$, so \[13+3(n-1)=73.\]"),("Solve",r"Then $3(n-1)=60$, so $n-1=20$ and $n=21$."),("Conclude",r"There are $\boxed{21}$ terms."),],
8:[("Set current ages",r"Let Pete's current age be $P$ and Claire's current age be $C$."),("Use the two past statements",r"Two years ago, $P-2=3(C-2)$. Four years ago, $P-4=4(C-4)$."),("Solve the system",r"The first equation gives $P=3C-4$, and the second gives $P=4C-12$. Equating them gives $C=8$, so $P=20$."),("Find when the ratio is 2 to 1",r"In $t$ years, \[\frac{20+t}{8+t}=2.\] Thus $20+t=16+2t$, so $t=4$."),("Conclude",r"The answer is $\boxed{4}$."),],
9:[("Write the volume relationship",r"Cylinder volume is $\pi r^2h$. If the second radius is $10\%$ more, then $r_2=1.1r_1$."),("Keep volume the same",r"Equal volumes give \[\pi r_1^2h_1=\pi(1.1r_1)^2h_2.\] So $h_1=1.21h_2$."),("Interpret the percentage",r"If $h_1=1.21h_2$, then the first height is $21\%$ more than the second."),("Conclude",r"The answer is $\boxed{\text{The first height is 21% more than the second.}}$"),],
10:[("List possible arrangements efficiently",r"There are only $4!=24$ arrangements, but the restrictions are strong: $a$ cannot sit next to $b$, $b$ cannot sit next to $c$, and $c$ cannot sit next to $d$."),("Search by placing b",r"The letter $b$ cannot be next to either $a$ or $c$, so its neighbors, if it has two, must include $d$. This quickly leaves only arrangements where the alphabet-adjacent pairs are separated."),("Identify the valid orders",r"The valid rearrangements are $bdac$ and $cadb$. Each avoids $ab,ba,bc,cb,cd,$ and $dc$ as adjacent pairs."),("Count",r"There are exactly $2$ valid rearrangements."),("Conclude",r"The answer is $\boxed{2}$."),],
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
    if n in {10,17} and notes == "题面包含图形":
        notes = ""
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in {3} else notes
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
        if r["year"] == "2015" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {3},
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
        + "- Answer verification source: AoPS 2015 AMC 10A Answer Key\n\n"
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












































