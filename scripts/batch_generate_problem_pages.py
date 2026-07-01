import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 97
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2017_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2017 AMC 10A Problems 1-10"
NEXT_START = "2017 AMC 10A Problem 11"

ANS={1:("C","127"),2:("D","13"),3:("B","78"),4:("B","14"),5:("C","4"),6:("B","If Lewis did not receive an A, then he got at least one multiple choice question wrong."),7:("A","30%"),8:("B","245"),9:("C","65"),10:("B","17")}

OV={
1:(r"What is the value of $2(2(2(2(2(2+1)+1)+1)+1)+1)+1$?",[("A","70"),("B","97"),("C","127"),("D","159"),("E","729")]),
2:(r"Pablo buys popsicles for his friends. The store sells single popsicles for $\$1$ each, $3$-popsicle boxes for $\$2$, and $5$-popsicle boxes for $\$3$. What is the greatest number of popsicles that Pablo can buy with $\$8$?",[("A","8"),("B","11"),("C","12"),("D","13"),("E","15")]),
3:(r"Tamara has three rows of two $6$-feet by $2$-feet flower beds in her garden. The beds are separated and also surrounded by $1$-foot-wide walkways, as shown on the diagram. What is the total area of the walkways, in square feet?",[("A","72"),("B","78"),("C","90"),("D","120"),("E","150")]),
4:(r"Mia is helping her mom pick up $30$ toys that are strewn on the floor. Mia's mom manages to put $3$ toys into the toy box every $30$ seconds, but each time immediately after those $30$ seconds have elapsed, Mia takes $2$ toys out of the box. How much time, in minutes, will it take Mia and her mom to put all $30$ toys into the box for the first time?",[("A","13.5"),("B","14"),("C","14.5"),("D","15"),("E","15.5")]),
5:(r"The sum of two nonzero real numbers is $4$ times their product. What is the sum of the reciprocals of the two numbers?",[("A","1"),("B","2"),("C","4"),("D","8"),("E","12")]),
6:(r"Ms. Carroll promised that anyone who got all the multiple choice questions right on the upcoming exam would receive an A on the exam. Which of these statements necessarily follows logically?",[("A","If Lewis did not receive an A, then he got all of the multiple choice questions wrong."),("B","If Lewis did not receive an A, then he got at least one of the multiple choice questions wrong."),("C","If Lewis got at least one of the multiple choice questions wrong, then he did not receive an A."),("D","If Lewis received an A, then he got all of the multiple choice questions right."),("E","If Lewis received an A, then he got at least one of the multiple choice questions right.")]),
7:(r"Jerry and Silvia wanted to go from the southwest corner of a square field to the northeast corner. Jerry walked due east and then due north to reach the goal, but Silvia headed northeast and reached the goal walking in a straight line. Which of the following is closest to how much shorter Silvia's trip was, compared to Jerry's trip?",[("A","30%"),("B","40%"),("C","50%"),("D","60%"),("E","70%")]),
8:(r"At a gathering of $30$ people, there are $20$ people who all know each other and $10$ people who know no one. People who know each other hug, and people who do not know each other shake hands. How many handshakes occur?",[("A","240"),("B","245"),("C","290"),("D","480"),("E","490")]),
9:(r"Minnie rides on a flat road at $20$ kilometers per hour, downhill at $30$ kph, and uphill at $5$ kph. Penny rides on a flat road at $30$ kph, downhill at $40$ kph, and uphill at $10$ kph. Minnie goes from town $A$ to town $B$, a distance of $10$ km all uphill, then from town $B$ to town $C$, a distance of $15$ km all downhill, and then back to town $A$, a distance of $20$ km on the flat. Penny goes the other way around using the same route. How many more minutes does it take Minnie to complete the $45$-km ride than it takes Penny?",[("A","45"),("B","60"),("C","65"),("D","90"),("E","95")]),
10:(r"Joy has $30$ thin rods, one each of every integer length from $1$ cm through $30$ cm. She places the rods with lengths $3$ cm, $7$ cm, and $15$ cm on a table. She then wants to choose a fourth rod that she can put with these three to form a quadrilateral with positive area. How many of the remaining rods can she choose as the fourth rod?",[("A","16"),("B","17"),("C","18"),("D","19"),("E","20")]),
}

KEY_OVERRIDES={1:"Evaluate nested arithmetic from the inside outward.",2:"Compare value per dollar and check leftover money.",3:"Compute the outside rectangle, then subtract flower-bed area.",4:"Track the net gain per 30 seconds and handle the final moment carefully.",5:"Divide the given equation by the product.",6:"Use the contrapositive of a conditional statement.",7:"Compare the side-walk path with the diagonal of a square.",8:"Count all pairs, then subtract hugging pairs.",9:"Use time equals distance divided by rate for each segment.",10:"Apply the quadrilateral inequality: the longest side must be shorter than the sum of the other three."}

SOL={
1:[("Start at the innermost parentheses",r"The expression is built by repeatedly doubling and adding $1$. The innermost value is $2+1=3$."),("Repeat the same operation",r"Now apply $2(\text{previous})+1$ repeatedly: \[3\mapsto7\mapsto15\mapsto31\mapsto63\mapsto127.\]"),("Check the number of steps",r"There are six 2's in the nested expression, so after starting with $2+1$, we need five more double-plus-one moves. The sequence above accounts for all of them."),("Conclude",r"The value is $\boxed{127}$."),],
2:[("Compare the deals",r"A single popsicle gives $1$ popsicle per dollar. A $3$-popsicle box gives $1.5$ popsicles per dollar, and a $5$-popsicle box gives $\frac53$ popsicles per dollar. The $5$-box is the best deal."),("Try the best deal first",r"With $\$8$, Pablo can buy two $5$-popsicle boxes for $\$6$, giving $10$ popsicles and leaving $\$2$."),("Use the remaining money efficiently",r"With the remaining $\$2$, he should buy one $3$-popsicle box, not two singles."),("Count the popsicles",r"The total is \[10+3=13.\]"),("Conclude",r"The greatest possible number is $\boxed{13}$."),],
3:[("Find the outer rectangle",r"The garden has two flower beds in each row, each $6$ feet wide, with $1$-foot walkways around and between them. So the total width is \[2\cdot6+3\cdot1=15.\]"),("Find the outer height",r"There are three rows of flower beds, each $2$ feet tall, with $1$-foot walkways around and between rows. So the total height is \[3\cdot2+4\cdot1=10.\]"),("Compute total and bed areas",r"The whole rectangular garden area is $15\cdot10=150$. There are $6$ flower beds, each with area $6\cdot2=12$, so the flower-bed area is $72$."),("Subtract",r"The walkway area is \[150-72=78.\]"),("Conclude",r"The answer is $\boxed{78}$ square feet."),],
4:[("Understand the cycle",r"Every $30$ seconds, Mia's mom puts in $3$ toys. Then Mia removes $2$ toys. Usually this gives a net gain of $1$ toy per $30$ seconds."),("Do not overshoot the final moment",r"The question asks when all $30$ toys are in the box for the first time. This can happen immediately after Mom puts in $3$ toys, before Mia removes any."),("Get close to 30",r"After $27$ full cycles, the box has $27$ toys, and $27$ cycles take $27\cdot30$ seconds."),("Use one final mom move",r"In the next $30$ seconds, Mom adds $3$ toys, bringing the total to $30$ for the first time."),("Convert time",r"The total time is \[28\cdot30=840\text{ seconds}=14\text{ minutes}.\]"),("Conclude",r"The answer is $\boxed{14}$."),],
5:[("Name the two numbers",r"Let the two nonzero real numbers be $x$ and $y$. The problem says \[x+y=4xy.\]"),("Recognize the target",r"The sum of the reciprocals is \[\frac1x+\frac1y=\frac{x+y}{xy}.\]"),("Substitute the given relationship",r"Since $x+y=4xy$, we get \[\frac{x+y}{xy}=\frac{4xy}{xy}=4.\]"),("Check why nonzero matters",r"The numbers are nonzero, so dividing by $xy$ is valid."),("Conclude",r"The answer is $\boxed{4}$."),],
6:[("Translate the promise",r"The promise has the form: if a student gets all multiple choice questions right, then that student receives an A."),("Use the contrapositive",r"The logically equivalent contrapositive is: if a student did not receive an A, then the student did not get all multiple choice questions right."),("Interpret not all right",r"Not getting all of them right means getting at least one multiple choice question wrong."),("Choose the matching statement",r"This matches choice B. The other choices add assumptions that the promise does not guarantee."),("Conclude",r"The necessarily true statement is $\boxed{\text{B}}$."),],
7:[("Let the square side be s",r"Jerry walks one side length east and one side length north, for total distance $2s$."),("Find Silvia's distance",r"Silvia walks along the diagonal of the square, which has length $s\sqrt2$."),("Compute the fractional decrease",r"The amount shorter is \[2s-s\sqrt2=s(2-\sqrt2).\] As a fraction of Jerry's trip, this is \[\frac{2-\sqrt2}{2}=1-\frac{\sqrt2}{2}.\]"),("Approximate",r"Since $\sqrt2\approx1.414$, the fraction is about \[1-0.707=0.293,\] or $29.3\%$."),("Conclude",r"The closest choice is $\boxed{30\%}$."),],
8:[("Count all possible pairs",r"Every pair of people either hugs or shakes hands. There are \[\binom{30}{2}=435\] total pairs."),("Count hugging pairs",r"The $20$ people who all know each other hug each other. That accounts for \[\binom{20}{2}=190\] hugging pairs."),("Understand the isolated group",r"The other $10$ people know no one, so every pair involving at least one of them is a handshake."),("Subtract",r"The number of handshakes is \[435-190=245.\]"),("Conclude",r"The answer is $\boxed{245}$."),],
9:[("Compute Minnie's time",r"Minnie rides $10$ km uphill at $5$ kph, $15$ km downhill at $30$ kph, and $20$ km flat at $20$ kph. Her time is \[\frac{10}{5}+\frac{15}{30}+\frac{20}{20}=2+\frac12+1=3.5\text{ hours}.\]"),("Compute Penny's route carefully",r"Penny goes the other way around. She rides $20$ km flat at $30$ kph, then $15$ km uphill at $10$ kph, then $10$ km downhill at $40$ kph."),("Add Penny's time",r"Her time is \[\frac{20}{30}+\frac{15}{10}+\frac{10}{40}=\frac23+\frac32+\frac14=\frac{29}{12}\text{ hours}.\]"),("Find the difference",r"Minnie's time is $\frac72=\frac{42}{12}$ hours, so the difference is \[\frac{42}{12}-\frac{29}{12}=\frac{13}{12}\text{ hours}.\]"),("Convert to minutes",r"\[\frac{13}{12}\cdot60=65\text{ minutes}.\]"),("Conclude",r"The answer is $\boxed{65}$."),],
10:[("Use the quadrilateral condition",r"Four positive side lengths can form a quadrilateral with positive area exactly when the longest side is shorter than the sum of the other three sides."),("Handle x when it is not the longest",r"Let the fourth rod have length $x$. If $x\le15$, the longest side is $15$, so we need \[15<3+7+x,\] which gives $x>5$."),("Handle x when it is the longest",r"If $x\ge15$, then $x$ is at least tied for longest, and we need \[x<3+7+15=25.\]"),("Combine the range",r"Together the possible integer values are \[6\le x\le24.\]"),("Remove unavailable rods",r"There are $19$ integers from $6$ through $24$, but rods of lengths $7$ and $15$ are already on the table. So $19-2=17$ remaining rods work."),("Conclude",r"The answer is $\boxed{17}$."),],
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
        if r["year"] == "2017" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2017 AMC 10A Answer Key\n\n"
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












































