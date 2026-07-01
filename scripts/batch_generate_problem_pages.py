import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 66
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2012_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2012 AMC 10B Problems 1-10"
NEXT_START = "2012 AMC 10B Problem 11"

ANS = {1:("C","64"),2:("E","200"),3:("B",r"(1000,1988)"),4:("A","1"),5:("D",r"\$22"),6:("A",r"larger than $x-y$"),7:("D","48"),8:("B","12"),9:("A","1"),10:("D","9")}

OV = {
1:(r"Each third-grade classroom at Pearl Creek Elementary has $18$ students and $2$ pet rabbits. How many more students than rabbits are there in all $4$ third-grade classrooms?",[("A","48"),("B","56"),("C","64"),("D","72"),("E","80")]),
2:(r"A circle of radius $5$ is inscribed in a rectangle as shown. The ratio of the length of the rectangle to its width is $2:1$. What is the area of the rectangle?",[("A","50"),("B","100"),("C","125"),("D","150"),("E","200")]),
3:(r"The point $(1000,2012)$ is reflected across the line $y=2000$. What are the coordinates of the reflected point?",[("A",r"(998,2012)"),("B",r"(1000,1988)"),("C",r"(1000,2024)"),("D",r"(1000,4012)"),("E",r"(1012,2012)")]),
4:(r"When Ringo places his marbles into bags with $6$ marbles per bag, he has $4$ marbles left over. When Paul does the same, he has $3$ marbles left over. Ringo and Paul pool their marbles and place them into as many bags as possible, with $6$ marbles per bag. How many marbles will be left over?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
5:(r"Anna eats dinner at a restaurant where the sales tax is $10\%$. She leaves a $15\%$ tip on the meal price before tax, and tax is calculated on the pre-tip amount. She spends $\$27.50$ total. What is the cost of her dinner without tax or tip?",[("A",r"\$18"),("B",r"\$20"),("C",r"\$21"),("D",r"\$22"),("E",r"\$24")]),
6:(r"To estimate $x-y$, where $x>y>0$, Xiaoli rounded $x$ up by a small amount, rounded $y$ down by the same amount, and then subtracted her values. Which statement is necessarily correct?",[("A",r"Her estimate is larger than $x-y$"),("B",r"Her estimate is smaller than $x-y$"),("C",r"Her estimate equals $x-y$"),("D",r"Her estimate equals $y-x$"),("E",r"Her estimate is $0$")]),
7:(r"For a science project, Sammy observed a chipmunk and a squirrel stashing acorns in holes. The chipmunk hid $3$ acorns in each hole. The squirrel hid $4$ acorns in each hole. They each hid the same number of acorns, although the squirrel needed $4$ fewer holes. How many acorns did the chipmunk hide?",[("A","30"),("B","36"),("C","42"),("D","48"),("E","54")]),
8:(r"What is the sum of all integer solutions to $1<(x-2)^2<25$?",[("A","10"),("B","12"),("C","15"),("D","19"),("E","25")]),
9:(r"Two integers have a sum of $26$. When two more integers are added to the first two, the sum is $41$. Finally, when two more integers are added to the previous four, the sum is $57$. What is the minimum number of even integers among the $6$ integers?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
10:(r"How many ordered pairs of positive integers $(M,N)$ satisfy the equation $\frac{M}{6}=\frac{6}{N}$?",[("A","6"),("B","7"),("C","8"),("D","9"),("E","10")]),
}

KEY_OVERRIDES = {1:"Compare total students and rabbits across four classrooms.",2:"Use the circle diameter as the rectangle width, then apply the 2:1 ratio.",3:"Reflecting across a horizontal line preserves x and mirrors y.",4:"Add remainders modulo 6.",5:"Tax and tip are both percentages of the pre-tax meal price.",6:"Track the effect of increasing the first number and decreasing the second.",7:"Use equal total acorns and a difference of four holes.",8:"Solve the compound inequality for integer values.",9:"Use parity of each added pair sum.",10:"Cross-multiply and count divisors of 36."}

SOL = {
1:[("Count one classroom",r"One classroom has $18$ students and $2$ rabbits, so it has $18-2=16$ more students than rabbits."),("Scale to four classrooms",r"There are $4$ identical classrooms, so the total difference is $4\cdot16=64$."),("Check by totals",r"There are $72$ students and $8$ rabbits in all, and $72-8=64$."),("Conclude",r"The answer is $\boxed{64}$."),],
2:[("Use the inscribed circle",r"The circle is inscribed, so its diameter equals the rectangle's width. The radius is $5$, so the diameter is $10$."),("Use the ratio",r"The rectangle's length-to-width ratio is $2:1$, so if the width is $10$, the length is $20$."),("Find area",r"The area is $10\cdot20=200$."),("Conclude",r"The answer is $\boxed{200}$."),],
3:[("Understand the mirror line",r"The line $y=2000$ is horizontal, so reflection across it keeps the $x$-coordinate unchanged."),("Measure vertical distance",r"The point has $y=2012$, which is $12$ units above $2000$. Its reflection will be $12$ units below $2000$."),("Find new y",r"The reflected $y$-coordinate is $2000-12=1988$."),("Conclude",r"The reflected point is $\boxed{(1000,1988)}$."),],
4:[("Use remainders",r"Ringo's marble count is congruent to $4$ modulo $6$, and Paul's is congruent to $3$ modulo $6$."),("Add the remainders",r"Together their count is congruent to $4+3=7$ modulo $6$."),("Reduce modulo 6",r"A remainder of $7$ is the same as a remainder of $1$ after making one more full bag."),("Conclude",r"There will be $\boxed{1}$ marble left over."),],
5:[("Let the meal price be p",r"Let $p$ be the cost before tax and tip. The tax is $10\%$ of $p$, and the tip is $15\%$ of $p$."),("Write the total",r"The total is $p+0.10p+0.15p=1.25p$."),("Solve",r"Since $1.25p=27.50$, we get $p=27.50/1.25=22$."),("Conclude",r"The meal cost before tax and tip was $\boxed{\$22}$."),],
6:[("Model the rounding",r"Suppose Xiaoli rounds $x$ up by $d$ and rounds $y$ down by the same $d$, where $d>0$."),("Write her estimate",r"Her estimate is $(x+d)-(y-d)=x-y+2d$."),("Compare",r"Because $2d>0$, her estimate is larger than $x-y$."),("Conclude",r"The necessarily correct statement is $\boxed{\text{her estimate is larger than }x-y}$."),],
7:[("Name the number of chipmunk holes",r"Let the chipmunk dig $h$ holes. Then it hides $3h$ acorns."),("Use the squirrel's holes",r"The squirrel uses $4$ fewer holes, so it uses $h-4$ holes and hides $4(h-4)$ acorns."),("Set equal totals",r"They hid the same number of acorns, so $3h=4(h-4)$. This gives $3h=4h-16$, so $h=16$."),("Find acorns",r"The chipmunk hid $3\cdot16=48$ acorns. The answer is $\boxed{48}$."),],
8:[("Convert the upper bound",r"The inequality $(x-2)^2<25$ means $-5<x-2<5$, so $-3<x<7$."),("Use the lower bound",r"The inequality $1<(x-2)^2$ means $|x-2|>1$, so $x<1$ or $x>3$."),("List integer solutions",r"Combining these gives $x=-2,-1,0,4,5,6$."),("Add",r"Their sum is $-2-1+0+4+5+6=12$. The answer is $\boxed{12}$."),],
9:[("Look at sums in pairs",r"The first two integers sum to $26$, an even number. The next two add $41-26=15$, an odd number. The last two add $57-41=16$, an even number."),("Minimize evens",r"An even sum can be made by two odd integers, giving no even integers. An odd sum must be made by one even and one odd integer, giving at least one even integer."),("Apply to the three pairs",r"Choose the first pair both odd, the second pair one even and one odd, and the third pair both odd. This is possible and uses only one even integer."),("Conclude",r"The minimum number of even integers is $\boxed{1}$."),],
10:[("Cross-multiply",r"From $\frac{M}{6}=\frac{6}{N}$, cross-multiplication gives $MN=36$."),("Turn the problem into divisor counting",r"For each positive divisor $M$ of $36$, there is exactly one positive integer $N=36/M$."),("Count divisors",r"Since $36=2^2\cdot3^2$, it has $(2+1)(2+1)=9$ positive divisors."),("Conclude",r"There are $\boxed{9}$ ordered pairs."),],
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
        if r["year"] == "2012" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2012 AMC 10B Answer Key\n\n"
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


































