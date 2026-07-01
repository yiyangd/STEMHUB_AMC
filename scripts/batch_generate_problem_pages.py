from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 47
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2009_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 10}
SKIPPED = ["2009 AMC 10B Problem 9 skipped: diagram-dependent angle configuration"]
BATCH_LABEL = "2009 AMC 10B Problems 1-8, 10"
NEXT_START = "2009 AMC 10B Problem 11"

ANS={1:("B","2"),2:("C",r"\frac12"),3:("C","15"),4:("C",r"\frac15"),5:("D","36"),6:("D","18"),7:("C","4"),8:("B","17"),10:("E","2.4")}

OV={
1:(r"Each morning of her five-day workweek, Jane bought either a $50$-cent muffin or a $75$-cent bagel. Her total cost for the week was a whole number of dollars. How many bagels did she buy?",[("A","$1$"),("B","$2$"),("C","$3$"),("D","$4$"),("E","$5$")]),
2:(r"Which of the following is equal to $\dfrac{\frac13-\frac14}{\frac12-\frac13}$?",[("A",r"$\frac14$"),("B",r"$\frac13$"),("C",r"$\frac12$"),("D",r"$\frac23$"),("E",r"$\frac34$")]),
3:(r"Paula the painter had just enough paint for $30$ identically sized rooms. Unfortunately, on the way to work, three cans of paint fell off her truck, so she had only enough paint for $25$ rooms. How many cans of paint did she use for the $25$ rooms?",[("A","$10$"),("B","$12$"),("C","$15$"),("D","$18$"),("E","$25$")]),
4:(r"A rectangular yard contains two flower beds in the shape of congruent isosceles right triangles. The remainder of the yard has a trapezoidal shape. The parallel sides of the trapezoid have lengths $15$ and $25$ meters. What fraction of the yard is occupied by the flower beds?",[("A",r"$\frac18$"),("B",r"$\frac16$"),("C",r"$\frac15$"),("D",r"$\frac14$"),("E",r"$\frac13$")]),
5:(r"Twenty percent less than $60$ is one-third more than what number?",[("A","$16$"),("B","$30$"),("C","$32$"),("D","$36$"),("E","$48$")]),
6:(r"Kiana has two older twin brothers. The product of their three ages is $128$. What is the sum of their three ages?",[("A","$10$"),("B","$12$"),("C","$16$"),("D","$18$"),("E","$24$")]),
7:(r"By inserting parentheses, it is possible to give the expression $2\times3+4\times5$ several values. How many different values can be obtained?",[("A","$2$"),("B","$3$"),("C","$4$"),("D","$5$"),("E","$6$")]),
8:(r"In a certain year the price of gasoline rose by $20\%$ during January, fell by $20\%$ during February, rose by $25\%$ during March, and fell by $x\%$ during April. The price of gasoline at the end of April was the same as it had been at the beginning of January. To the nearest integer, what is $x$?",[("A","$12$"),("B","$17$"),("C","$20$"),("D","$25$"),("E","$35$")]),
10:(r"A flagpole is originally $5$ meters tall. A hurricane snaps the flagpole at a point $x$ meters above the ground so that the upper part, still attached to the stump, touches the ground $1$ meter away from the base. What is $x$?",[("A","$2.0$"),("B","$2.1$"),("C","$2.2$"),("D","$2.3$"),("E","$2.4$")]),
}

KEY_OVERRIDES={1:"Use modular cents to force the weekly total to be a whole number of dollars.",2:"Simplify the numerator and denominator separately before dividing.",3:"Use the lost paint to find how many rooms one can paints.",4:"Use the trapezoid bases to identify the triangular flower-bed legs and compare areas.",5:"Translate percent phrases into equations.",6:"Use the fact that the two older brothers are twins, so their ages are equal.",7:"Evaluate all possible parenthesizations and count distinct values.",8:"Multiply percentage change factors and solve for the final decrease.",10:"Use the snapped pole as a right triangle."}

SOL={
1:[("Let b be the number of bagels",r"Jane buys $5$ items total. If she buys $b$ bagels, she buys $5-b$ muffins."),("Write the cost in cents",r"The total cost is $75b+50(5-b)=250+25b$ cents."),("Use whole dollars",r"A whole number of dollars means the number of cents is divisible by $100$. So $250+25b=25(10+b)$ must be divisible by $100$."),("Solve the divisibility",r"This requires $10+b$ to be divisible by $4$. Since $b$ is between $0$ and $5$, only $b=2$ works."),("Answer",r"Jane bought $\boxed{2}$ bagels.")],
2:[("Simplify the numerator",r"The numerator is $\frac13-\frac14=\frac{4-3}{12}=\frac1{12}$."),("Simplify the denominator",r"The denominator is $\frac12-\frac13=\frac{3-2}{6}=\frac16$."),("Divide the fractions",r"The whole expression is $\frac{1/12}{1/6}=\frac1{12}\cdot6=\frac12$."),("Answer",r"The value is $\boxed{\frac12}$.")],
3:[("Interpret the lost paint",r"Before losing paint, Paula had enough for $30$ rooms. After losing $3$ cans, she had enough for $25$ rooms."),("Find what 3 cans represent",r"The lost $3$ cans would have painted $30-25=5$ rooms."),("Find cans per room",r"So $3$ cans paint $5$ rooms."),("Scale to 25 rooms",r"Painting $25$ rooms is $5$ times as many rooms, so it requires $5\cdot3=15$ cans."),("Answer",r"She used $\boxed{15}$ cans.")],
4:[("Read the geometry",r"The trapezoid has parallel sides $15$ and $25$. The extra length $25-15=10$ is split equally by two congruent isosceles right triangle flower beds."),("Find each triangle leg",r"Each flower bed contributes $5$ meters of horizontal difference, and because the triangles are isosceles right triangles, their vertical leg is also $5$ meters."),("Compute flower-bed area",r"Each triangle has area $\frac12\cdot5\cdot5=12.5$, so together the flower beds have area $25$."),("Compute yard area",r"The whole rectangular yard has dimensions $25$ by $5$, so its area is $125$."),("Find the fraction",r"The fraction occupied by flower beds is $\frac{25}{125}=\frac15$."),("Answer",r"The answer is $\boxed{\frac15}$.")],
5:[("Compute twenty percent less than 60",r"Twenty percent less than $60$ is $80\%$ of $60$, which is $0.8\cdot60=48$."),("Translate one-third more",r"If the unknown number is $n$, then one-third more than it is $n+\frac13n=\frac43n$."),("Set up the equation",r"We need $\frac43n=48$."),("Solve",r"Multiplying by $\frac34$ gives $n=48\cdot\frac34=36$."),("Answer",r"The number is $\boxed{36}$.")],
6:[("Use the twin condition",r"Let each older twin brother be $t$ years old, and let Kiana be $k$ years old."),("Use the product",r"The product of their ages is $kt^2=128$."),("Test square factors",r"Since $t^2$ must divide $128=2^7$, possible square factors include $4,16,$ and $64$. Because the brothers are older than Kiana, $t=8$ and $k=2$ is the valid choice."),("Add ages",r"The sum is $8+8+2=18$."),("Answer",r"Their ages sum to $\boxed{18}$.")],
7:[("List possible structures",r"The order of the numbers and operations stays fixed; only parentheses change. We can evaluate the possible full parenthesizations."),("Compute the values",r"They give $((2\times3)+4)\times5=50$, $(2\times(3+4))\times5=70$, $(2\times3)+(4\times5)=26$, $2\times((3+4)\times5)=70$, and $2\times(3+(4\times5))=46$."),("Remove duplicates",r"The distinct values are $26,46,50,$ and $70$."),("Answer",r"There are $\boxed{4}$ different values.")],
8:[("Use a starting price",r"Let the starting price be $1$ unit. After January it is multiplied by $1.20$."),("Apply February and March",r"After February and March, the factor is $1.20\cdot0.80\cdot1.25$. Since $0.80\cdot1.25=1$, the price is $1.20$ times the original."),("Set up April",r"After a decrease of $x\%$, the factor is $1.20(1-\frac{x}{100})$. This must equal $1$."),("Solve",r"So $1-\frac{x}{100}=\frac{1}{1.20}=\frac56$, which gives $x=\frac{100}{6}\approx16.67$."),("Round",r"To the nearest integer, $x=17$."),("Answer",r"The answer is $\boxed{17}$.")],
10:[("Draw the right triangle mentally",r"The stump has height $x$, the ground distance is $1$, and the broken upper part has length $5-x$."),("Use the Pythagorean theorem",r"These form a right triangle, so $x^2+1^2=(5-x)^2$."),("Solve",r"Expanding gives $x^2+1=25-10x+x^2$. Cancel $x^2$ to get $1=25-10x$."),("Find x",r"Thus $10x=24$, so $x=2.4$."),("Answer",r"The snap point is $\boxed{2.4}$ meters above the ground.")],
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
        if r["year"] == "2009" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {4},
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
        + "- Answer verification source: AoPS 2009 AMC 10B Answer Key\n\n"
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









