import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 121
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2021_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2021 Spring AMC 10A Problems 1-10"
NEXT_START = "2021 Spring AMC 10A Problem 11"

ANS={1:("D","8"),2:("C","1950"),3:("D","14238"),4:("D","3195"),5:("B",r"\frac{8k-168}{k-12}"),6:("A",r"\frac{12}{13}"),7:("D","Happy snakes are not purple."),8:("E","75"),9:("D","1"),10:("C",r"3^{128}-2^{128}")}

OV={
1:(r"What is the value of \[(2^2-2)-(3^2-3)+(4^2-4)?\]",[("A","1"),("B","2"),("C","5"),("D","8"),("E","12")]),
2:(r"Portia's high school has $3$ times as many students as Lara's high school. The two high schools have a total of $2600$ students. How many students does Portia's high school have?",[("A","600"),("B","650"),("C","1950"),("D","2000"),("E","2050")]),
3:(r"The sum of two natural numbers is $17,402$. One of the two numbers is divisible by $10$. If the units digit of that number is erased, the other number is obtained. What is the difference of these two numbers?",[("A","10272"),("B","11700"),("C","13362"),("D","14238"),("E","15426")]),
4:(r"A cart rolls down a hill, traveling $5$ inches the first second and accelerating so that each successive $1$-second interval it travels $7$ inches more than during the previous $1$-second interval. The cart takes $30$ seconds to reach the bottom of the hill. How far, in inches, does it travel?",[("A","215"),("B","360"),("C","2992"),("D","3195"),("E","3242")]),
5:(r"The quiz scores of a class with $k>12$ students have a mean of $8$. The mean of a collection of $12$ of these quiz scores is $14$. What is the mean of the remaining quiz scores in terms of $k$?",[("A",r"$\frac{14-8}{k-12}$"),("B",r"$\frac{8k-168}{k-12}$"),("C",r"$\frac{14}{12}-\frac{8}{k}$"),("D",r"$\frac{14(k-12)}{k^2}$"),("E",r"$\frac{14(k-12)}{8k}$")]),
6:(r"Chantal and Jean start hiking from a trailhead toward a fire tower. Jean is wearing a heavy backpack and walks slower. Chantal starts walking at $4$ miles per hour. Halfway to the tower, the trail becomes really steep, and Chantal slows down to $2$ miles per hour. After reaching the tower, she immediately turns around and descends the steep part of the trail at $3$ miles per hour. She meets Jean at the halfway point. What was Jean's average speed, in miles per hour, until they meet?",[("A",r"$\frac{12}{13}$"),("B","1"),("C",r"$\frac{13}{12}$"),("D",r"$\frac{24}{13}$"),("E","2")]),
7:(r"Tom has a collection of $13$ snakes, $4$ of which are purple and $5$ of which are happy. He observes that all of his happy snakes can add, none of his purple snakes can subtract, and all of his snakes that cannot subtract also cannot add. Which of these conclusions can be drawn about Tom's snakes?",[("A","Purple snakes can add."),("B","Purple snakes are happy."),("C","Snakes that can add are purple."),("D","Happy snakes are not purple."),("E","Happy snakes cannot subtract.")]),
8:(r"When a student multiplied the number $66$ by the repeating decimal $1.\overline{ab}$, where $a$ and $b$ are digits, he did not notice the notation and just multiplied $66$ times $1.ab$. Later he found that his answer is $0.5$ less than the correct answer. What is the two-digit integer $ab$?",[("A","15"),("B","30"),("C","45"),("D","60"),("E","75")]),
9:(r"What is the least possible value of $(xy-1)^2+(x+y)^2$ for real numbers $x$ and $y$?",[("A","0"),("B",r"$\frac14$"),("C",r"$\frac12$"),("D","1"),("E","2")]),
10:(r"Which of the following is equivalent to \[(2+3)(2^2+3^2)(2^4+3^4)(2^8+3^8)(2^{16}+3^{16})(2^{32}+3^{32})(2^{64}+3^{64})?\]",[("A",r"$3^{127}+2^{127}$"),("B",r"$3^{127}+2^{127}+2\cdot3^{63}+3\cdot2^{63}$"),("C",r"$3^{128}-2^{128}$"),("D",r"$3^{128}+2^{128}$"),("E",r"$5^{127}$")]),
}

KEY_OVERRIDES={1:"Evaluate powers and signs carefully.",2:"Use a simple ratio model for the two schools.",3:"Represent the erased-units relationship algebraically.",4:"Sum an arithmetic sequence.",5:"Convert means to total sums.",6:"Choose a convenient distance and compare time traveled.",7:"Use implications and their contrapositives carefully.",8:"Compare a repeating decimal with its truncated version.",9:"Expand and use nonnegative squares.",10:"Use repeated difference-of-squares telescoping."}

SOL={
1:[("Evaluate each parenthesis first",r"The safest first step is not to combine signs too quickly. Compute each grouped expression: \[2^2-2=2,\quad 3^2-3=6,\quad 4^2-4=12.\]"),("Keep the middle minus sign",r"The original expression subtracts the second group, so it becomes \[2-6+12.\]"),("Finish the arithmetic",r"Now \[2-6+12=-4+12=8.\]"),("Conclude",r"The answer is $\boxed{8}$."),],
2:[("Set up the smaller school first",r"Let Lara's high school have $x$ students. Portia's school has $3x$ students."),("Use the total",r"Together they have $x+3x=4x$ students, and this total is $2600$."),("Solve for x",r"So \[4x=2600,\] giving \[x=650.\]"),("Find Portia's school size",r"Portia has \[3x=3\cdot650=1950\] students."),("Conclude",r"The answer is $\boxed{1950}$."),],
3:[("Represent the digit erasing",r"If erasing the units digit of the number divisible by $10$ gives the other number, then the larger number is $10x$ and the other number is $x$."),("Use the sum",r"Their sum is \[10x+x=11x=17402.\]"),("Solve for x",r"Thus \[x=\frac{17402}{11}=1582.\]"),("Find the difference",r"The difference between the two numbers is \[10x-x=9x=9\cdot1582=14238.\]"),("Conclude",r"The answer is $\boxed{14238}$."),],
4:[("Recognize the distance pattern",r"The cart travels $5$ inches in the first second, then $12$, then $19$, and so on. These distances form an arithmetic sequence with first term $5$ and common difference $7$."),("Use the arithmetic sequence sum",r"There are $30$ one-second intervals. The sum is \[S_{30}=\frac{30}{2}\left(2\cdot5+29\cdot7\right).\]"),("Compute the inside",r"The expression inside the parentheses is \[10+203=213.\]"),("Finish the sum",r"So \[S_{30}=15\cdot213=3195.\]"),("Conclude",r"The answer is $\boxed{3195}$."),],
5:[("Translate means into totals",r"A mean is a total divided by the number of scores. Since the whole class has $k$ students with mean $8$, the total score is \[8k.\]"),("Find the known subgroup total",r"The $12$ selected scores have mean $14$, so their total is \[12\cdot14=168.\]"),("Subtract to get the remaining total",r"The remaining students therefore have total score \[8k-168.\]"),("Divide by the number remaining",r"There are $k-12$ remaining students, so their mean is \[\frac{8k-168}{k-12}.\]"),("Conclude",r"The answer is $\boxed{\frac{8k-168}{k-12}}$."),],
6:[("Choose a convenient distance",r"Because only ratios of speed matter, choose the halfway distance to be $12$ miles. Then the full trip to the tower is $24$ miles."),("Compute Chantal's time to the halfway point",r"Chantal walks the first $12$ miles at $4$ miles per hour, taking \[\frac{12}{4}=3\] hours."),("Compute the steep uphill and downhill time",r"She then walks $12$ miles uphill at $2$ mph, taking $6$ hours, and comes back down $12$ miles at $3$ mph, taking $4$ hours."),("Find Jean's distance and time",r"When they meet at the halfway point, Jean has walked $12$ miles. The total time is \[3+6+4=13\] hours."),("Compute Jean's average speed",r"Jean's average speed is \[\frac{12}{13}\] miles per hour."),("Conclude",r"The answer is $\boxed{\frac{12}{13}}$."),],
7:[("Translate each statement into logic",r"Happy snakes can add means $H\Rightarrow A$. Purple snakes cannot subtract means $P\Rightarrow \text{not }S$. Snakes that cannot subtract also cannot add means $\text{not }S\Rightarrow \text{not }A$."),("Combine the purple statements",r"If a snake is purple, then it cannot subtract. If it cannot subtract, then it cannot add. Therefore \[P\Rightarrow \text{not }A.\]"),("Compare with happy snakes",r"If a snake is happy, then it can add. But purple snakes cannot add, so a happy snake cannot be purple."),("Choose the conclusion",r"The conclusion that must be true is: happy snakes are not purple."),("Conclude",r"The answer is $\boxed{\text{Happy snakes are not purple}}$."),],
8:[("Write the two decimals algebraically",r"Let $x$ be the two-digit number $ab$. Then \[1.\overline{ab}=1+\frac{x}{99}\] and \[1.ab=1+\frac{x}{100}.\]"),("Find the difference before multiplying",r"The difference between the correct number and the mistaken number is \[\frac{x}{99}-\frac{x}{100}=\frac{x}{9900}.\]"),("Use the given product difference",r"After multiplying by $66$, the student's answer is $0.5$ too small, so \[66\cdot\frac{x}{9900}=\frac12.\]"),("Solve for x",r"Since $\frac{66}{9900}=\frac{1}{150}$, we get \[\frac{x}{150}=\frac12,\] so $x=75$."),("Conclude",r"The answer is $\boxed{75}$."),],
9:[("Expand both squares",r"The expression is \[(xy-1)^2+(x+y)^2=x^2y^2-2xy+1+x^2+2xy+y^2.\]"),("Notice the cancellation",r"The terms $-2xy$ and $2xy$ cancel, leaving \[x^2y^2+x^2+y^2+1.\]"),("Use nonnegative squares",r"The terms $x^2y^2$, $x^2$, and $y^2$ are all nonnegative for real $x,y$. Therefore the expression is at least $1$."),("Check that the bound is attainable",r"At $x=0$ and $y=0$, the expression equals \[0+0+0+1=1.\]"),("Conclude",r"The least possible value is $\boxed{1}$."),],
10:[("Look for a telescoping product",r"The factors have the form $2^{2^m}+3^{2^m}$. Such expressions pair naturally with difference of squares."),("Multiply by a harmless factor",r"Since $3-2=1$, multiplying the product by $3-2$ does not change its value."),("Collapse the first few factors",r"We get \[(3-2)(3+2)=3^2-2^2,\] then \[(3^2-2^2)(3^2+2^2)=3^4-2^4.\] The same pattern continues."),("Continue through the final factor",r"After multiplying through the factor $3^{64}+2^{64}$, the product becomes \[3^{128}-2^{128}.\]"),("Conclude",r"The answer is $\boxed{3^{128}-2^{128}}$."),],
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












































