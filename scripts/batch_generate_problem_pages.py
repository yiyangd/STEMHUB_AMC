import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 78
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2014_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2014 AMC 10A Problems 1-10"
NEXT_START = "2014 AMC 10A Problem 11"

ANS={1:("C",r"\frac{25}{2}"),2:("C","Thursday"),3:("E","52"),4:("B","3"),5:("C","3"),6:("A",r"\frac{bde}{ac}"),7:("B","1"),8:("D",r"\frac{17!18!}{2}"),9:("C","3"),10:("B",r"a+4")}

OV={
1:(r"What is $10\cdot\left(\frac12+\frac15+\frac1{10}\right)^{-1}$?",[("A","3"),("B","8"),("C",r"\frac{25}{2}"),("D",r"\frac{170}{3}"),("E","170")]),
2:(r"Roy's cat eats $\frac13$ of a can of cat food every morning and $\frac14$ of a can every evening. Before feeding his cat on Monday morning, Roy opened a box containing $6$ cans of cat food. On what day of the week did the cat finish eating all the cat food in the box?",[("A","Tuesday"),("B","Wednesday"),("C","Thursday"),("D","Friday"),("E","Saturday")]),
3:(r"Bridget bakes $48$ loaves of bread for her bakery. She sells half of them in the morning for $\$2.50$ each. In the afternoon she sells two thirds of what she has left, and because they are not fresh, she charges only half price. In the late afternoon she sells the remaining loaves at a dollar each. Each loaf costs $\$0.75$ for her to make. In dollars, what is her profit for the day?",[("A","24"),("B","36"),("C","44"),("D","48"),("E","52")]),
4:(r"Walking down Jane Street, Ralph passed four houses in a row, each painted a different color. He passed the orange house before the red house, and he passed the blue house before the yellow house. The blue house was not next to the yellow house. How many orderings of the colored houses are possible?",[("A","2"),("B","3"),("C","4"),("D","5"),("E","6")]),
5:(r"On an algebra quiz, $10\%$ of the students scored $70$ points, $35\%$ scored $80$ points, $30\%$ scored $90$ points, and the rest scored $100$ points. What is the difference between the mean and median score of the students' scores on this quiz?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
6:(r"Suppose that $a$ cows give $b$ gallons of milk in $c$ days. At this rate, how many gallons of milk will $d$ cows give in $e$ days?",[("A",r"\frac{bde}{ac}"),("B",r"\frac{ac}{bde}"),("C",r"\frac{abde}{c}"),("D",r"\frac{bcde}{a}"),("E",r"\frac{abc}{de}")]),
7:(r"Nonzero real numbers $x$, $y$, $a$, and $b$ satisfy $x<a$ and $y<b$. How many of the following inequalities must be true? $\text{(I) }x+y<a+b$, $\text{(II) }x-y<a-b$, $\text{(III) }xy<ab$, $\text{(IV) }\frac{x}{y}<\frac{a}{b}$.",[("A","0"),("B","1"),("C","2"),("D","3"),("E","4")]),
8:(r"Which of the following numbers is a perfect square?",[("A",r"\frac{14!15!}{2}"),("B",r"\frac{15!16!}{2}"),("C",r"\frac{16!17!}{2}"),("D",r"\frac{17!18!}{2}"),("E",r"\frac{18!19!}{2}")]),
9:(r"The two legs of a right triangle, which are altitudes, have lengths $2\sqrt3$ and $6$. How long is the third altitude of the triangle?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
10:(r"Five positive consecutive integers starting with $a$ have average $b$. What is the average of five consecutive integers that start with $b$?",[("A",r"a+3"),("B",r"a+4"),("C",r"a+5"),("D",r"a+6"),("E",r"a+7")]),
}

KEY_OVERRIDES={1:"Use common denominators, then take the reciprocal at the correct time.",2:"Convert the morning and evening amounts to one daily total, then track the final partial day.",3:"Separate revenue and cost before computing profit.",4:"Count all ordered arrangements satisfying two before-after conditions, then remove adjacent cases.",5:"Use percentage weights for the mean and cumulative percentages for the median.",6:"Find the rate per cow per day, then multiply by the new number of cows and days.",7:"Prove the one always-true inequality and disprove the others with counterexamples.",8:"Rewrite n!(n+1)!/2 as a square times (n+1)/2.",9:"Compute the area two ways to find the altitude to the hypotenuse.",10:"The average of five consecutive integers is the middle term."}

SOL={
1:[("Read the exponent carefully",r"The exponent $-1$ means reciprocal. So we first simplify the expression inside the parentheses, and only then take its reciprocal."),("Use a common denominator",r"The common denominator is $10$: \[\frac12+\frac15+\frac1{10}=\frac5{10}+\frac2{10}+\frac1{10}=\frac8{10}=\frac45.\]"),("Take the reciprocal",r"Now $\left(\frac45\right)^{-1}=\frac54$. Multiplying by $10$ gives $10\cdot\frac54=\frac{50}{4}=\frac{25}{2}$."),("Check the size",r"The sum inside is less than $1$, so its reciprocal is greater than $1$. A final answer around $12.5$ is reasonable."),("Conclude",r"The answer is $\boxed{\frac{25}{2}}$."),],
2:[("Combine one full day of food",r"Each day the cat eats $\frac13+\frac14=\frac7{12}$ of a can. Thinking in twelfths makes the arithmetic cleaner."),("Convert the supply",r"Six cans is $\frac{72}{12}$ of a can. After $10$ full days, the cat has eaten $10\cdot\frac7{12}=\frac{70}{12}$ cans, so there is still $\frac{2}{12}$ can left."),("Locate the day",r"Starting on Monday, after $10$ full days we have reached Wednesday evening of the next week. The next feeding is Thursday morning."),("Finish on the partial day",r"On Thursday morning the cat wants $\frac13=\frac4{12}$ of a can, but only $\frac2{12}$ remains. Therefore the cat finishes the box during that Thursday morning feeding."),("Conclude",r"The answer is $\boxed{\text{Thursday}}$."),],
3:[("Separate revenue from cost",r"Profit is revenue minus cost. It is safer to compute all the money Bridget receives first, then subtract the total cost of making the loaves."),("Compute morning revenue",r"She sells half of $48$, which is $24$ loaves, at $\$2.50$ each. This gives $24\cdot2.50=60$ dollars."),("Compute afternoon and late-afternoon revenue",r"She has $24$ loaves left. She sells $\frac23\cdot24=16$ at half price, which is $\$1.25$ each, for $20$ dollars. The remaining $8$ loaves sell for $8$ more dollars."),("Subtract cost",r"Her total revenue is $60+20+8=88$ dollars. Her cost is $48\cdot0.75=36$ dollars, so her profit is $88-36=52$ dollars."),("Conclude",r"The answer is $\boxed{52}$."),],
4:[("Start with the before-after conditions",r"Without the non-adjacent condition, half of all arrangements have orange before red, and half of those have blue before yellow. Thus $24/4=6$ arrangements satisfy the two order conditions."),("Remove the forbidden adjacent cases",r"Now count the cases where blue is immediately before yellow. Treat $BY$ as one block, along with $O$ and $R$, giving three objects."),("Apply orange before red",r"Among the $3!=6$ arrangements of $BY$, $O$, and $R$, exactly half have $O$ before $R$. So $3$ of the $6$ otherwise valid arrangements are forbidden."),("Subtract",r"The valid number of arrangements is $6-3=3$."),("Conclude",r"The answer is $\boxed{3}$."),],
5:[("Find the median first",r"The cumulative percentage at $70$ and $80$ is $10\%+35\%=45\%$. Adding the $90$ scores reaches $75\%$, so the middle score must be $90$."),("Compute the mean with percentages",r"The remaining percentage is $25\%$, since $100-10-35-30=25$. The mean is \[0.10(70)+0.35(80)+0.30(90)+0.25(100).\]"),("Evaluate",r"This equals $7+28+27+25=87$. So the mean is $87$ and the median is $90$."),("Take the difference",r"The question asks for the difference, not which is larger. The difference is $90-87=3$."),("Conclude",r"The answer is $\boxed{3}$."),],
6:[("Find one cow's one-day rate",r"The phrase 'at this rate' suggests finding a unit rate. If $a$ cows produce $b$ gallons in $c$ days, then one cow in one day produces $\frac{b}{ac}$ gallons."),("Scale to d cows",r"If one cow produces $\frac{b}{ac}$ gallons per day, then $d$ cows produce $\frac{bd}{ac}$ gallons per day."),("Scale to e days",r"Over $e$ days, multiply by $e$: \[\frac{bd}{ac}\cdot e=\frac{bde}{ac}.\]"),("Check direct proportionality",r"The answer should increase when $b$, $d$, or $e$ increases, and decrease when $a$ or $c$ increases. The expression $\frac{bde}{ac}$ has exactly that behavior."),("Conclude",r"The answer is $\boxed{\frac{bde}{ac}}$."),],
7:[("Prove the easy one",r"Since $x<a$ and $y<b$, adding the two inequalities gives $x+y<a+b$. So statement I must be true."),("Remember what 'must be true' means",r"To disprove a statement, one counterexample is enough. We need examples that still satisfy $x<a$ and $y<b$."),("Use one counterexample for II, III, and IV",r"Take $x=-3$, $y=-4$, $a=1$, and $b=4$. Then $x<a$ and $y<b$ are both true."),("Test the remaining statements",r"For II, $x-y=1$ but $a-b=-3$, so $1<-3$ is false. For III, $xy=12$ but $ab=4$, so $12<4$ is false. For IV, $\frac{x}{y}=\frac34$ but $\frac{a}{b}=\frac14$, so $\frac34<\frac14$ is false."),("Conclude",r"Only statement I must be true, so the answer is $\boxed{1}$."),],
8:[("Look for a common structure",r"Each choice has the form $\frac{n!(n+1)!}{2}$. Rewrite this as \[\frac{n!(n+1)n!}{2}=(n!)^2\cdot\frac{n+1}{2}.\]"),("Use the square factor",r"The factor $(n!)^2$ is already a perfect square. Therefore the whole expression is a perfect square exactly when $\frac{n+1}{2}$ is a perfect square."),("Test the possible n values",r"The choices correspond to $n=14,15,16,17,18$. Then $\frac{n+1}{2}$ is $\frac{15}{2},8,\frac{17}{2},9,\frac{19}{2}$."),("Identify the square",r"Only $9$ is a perfect square, and it occurs when $n=17$. That corresponds to $\frac{17!18!}{2}$."),("Conclude",r"The answer is $\boxed{\frac{17!18!}{2}}$."),],
9:[("Use the two given legs",r"The right triangle has legs $2\sqrt3$ and $6$. Its area is \[\frac12(2\sqrt3)(6)=6\sqrt3.\]"),("Find the hypotenuse",r"By the Pythagorean Theorem, the hypotenuse is \[\sqrt{(2\sqrt3)^2+6^2}=\sqrt{12+36}=4\sqrt3.\]"),("Use area again",r"The third altitude is the altitude to the hypotenuse. If its length is $h$, then the area is also $\frac12(4\sqrt3)h$."),("Solve for h",r"Set the two area expressions equal: \[\frac12(4\sqrt3)h=6\sqrt3.\] Dividing by $2\sqrt3$ gives $h=3$."),("Conclude",r"The answer is $\boxed{3}$."),],
10:[("Use the middle term idea",r"For five consecutive integers, the average is the middle number. The five integers starting with $a$ are $a,a+1,a+2,a+3,a+4$, so their average is $a+2$."),("Relate b to a",r"The problem says this average is $b$, so $b=a+2$."),("Build the second list",r"The next list starts with $b$: $b,b+1,b+2,b+3,b+4$. Its average is its middle term, $b+2$."),("Substitute",r"Since $b=a+2$, the new average is $b+2=a+4$."),("Conclude",r"The answer is $\boxed{a+4}$."),],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in set()) else notes
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
        + "- Answer verification source: AoPS 2014 AMC 10A Answer Key\n\n"
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












































