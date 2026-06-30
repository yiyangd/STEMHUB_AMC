from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 16
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2004_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
SKIPPED = []
BATCH_LABEL = "2004 AMC 10B Problem 1-10"
NEXT_START = "2004 AMC 10B Problem 11"

ANS = {
    1: ("C", "363"),
    2: ("B", "18"),
    3: ("A", "3"),
    4: ("B", "12"),
    5: ("D", "9"),
    6: ("C", r"99!\cdot100!"),
    7: ("A", "5"),
    8: ("A", "13"),
    9: ("B", r"100+75\pi"),
    10: ("D", "10"),
}


OV = {
    1: (
        r"Each row of the Misty Moon Amphitheater has $33$ seats. Rows $12$ through $22$ are reserved for a youth club. How many seats are reserved for this club?",
        [("A", "$297$"), ("B", "$330$"), ("C", "$363$"), ("D", "$396$"), ("E", "$726$")],
    ),
    4: (
        r"A standard six-sided die is rolled, and $P$ is the product of the five numbers that are visible. What is the largest number that is certain to divide $P$?",
        [("A", "$6$"), ("B", "$12$"), ("C", "$24$"), ("D", "$144$"), ("E", "$720$")],
    ),
    5: (
        r"In the expression $c\cdot a^b-d$, the values of $a$, $b$, $c$, and $d$ are $0$, $1$, $2$, and $3$, although not necessarily in that order. What is the maximum possible value of the result?",
        [("A", "$5$"), ("B", "$6$"), ("C", "$8$"), ("D", "$9$"), ("E", "$10$")],
    ),
    6: (
        r"Which of the following numbers is a perfect square?",
        [("A", r"$98!\cdot99!$"), ("B", r"$98!\cdot100!$"), ("C", r"$99!\cdot100!$"), ("D", r"$99!\cdot101!$"), ("E", r"$100!\cdot101!$")],
    ),
    9: (
        r"A square has sides of length $10$, and a circle centered at one of its vertices has radius $10$. What is the area of the union of the regions enclosed by the square and the circle?",
        [("A", r"$200+25\pi$"), ("B", r"$100+75\pi$"), ("C", r"$75+100\pi$"), ("D", r"$100+100\pi$"), ("E", r"$100+125\pi$")],
    ),
}


KEY_OVERRIDES = {
    1: "Count inclusive rows, then multiply by the number of seats per row.",
    2: "Count two-digit numbers containing a 7 without double-counting 77.",
    3: "Work backward through a doubling sequence.",
    4: "Take the greatest common divisor of all possible visible products.",
    5: "Maximize an exponential expression by choosing the base and exponent carefully.",
    6: "Rewrite one factorial product as an obvious square.",
    7: "Set up an exchange-rate equation and solve for the original dollar amount.",
    8: "Model northeast and northwest directions as right-triangle vectors.",
    9: "Use inclusion-exclusion for the area of a square and a circle.",
    10: "Use the sum of the first n odd numbers.",
}


SOL = {
    1: [
        ("Count the rows carefully", r"Rows $12$ through $22$ are inclusive. That means the number of reserved rows is $22-12+1=11$."),
        ("Multiply by seats per row", r"Each row has $33$ seats, so the number of reserved seats is $11\cdot33=363$."),
        ("Check", r"Counting inclusively is the main trap; there are $11$ rows, not $10$."),
        ("Answer", r"The answer is $\boxed{363}$."),
    ],
    2: [
        ("Separate the positions", r"A two-digit number has a tens digit from $1$ to $9$ and a ones digit from $0$ to $9$. We want at least one digit to be $7$."),
        ("Count numbers with tens digit 7", r"The numbers $70$ through $79$ give $10$ possibilities."),
        ("Count numbers with ones digit 7", r"The numbers ending in $7$ are $17,27,\ldots,97$, giving $9$ possibilities. But $77$ has already been counted."),
        ("Combine without double-counting", r"The total is $10+9-1=18$."),
        ("Answer", r"There are $\boxed{18}$ such integers."),
    ],
    3: [
        ("Recognize the doubling pattern", r"Each practice has twice as many free throws as the previous one. To go backward, divide by $2$ each time."),
        ("Work backward from the fifth practice", r"The fifth practice is $48$, so the fourth is $24$, the third is $12$, the second is $6$, and the first is $3$."),
        ("Check forward", r"Starting with $3$ gives $3,6,12,24,48$, which matches the fifth practice."),
        ("Answer", r"Jenny made $\boxed{3}$ free throws at the first practice."),
    ],
    4: [
        ("List the possible products", r"A standard die shows the numbers $1$ through $6$. If one face is hidden, then $P$ is $720$ divided by the hidden number, since $1\cdot2\cdot3\cdot4\cdot5\cdot6=720$."),
        ("Compute possible P values", r"The possible products are $720,360,240,180,144,$ and $120$."),
        ("Find what always divides P", r"The largest number certain to divide every possible $P$ is the greatest common divisor of those values."),
        ("Calculate the gcd", r"The common divisor is $12$. For example, $24$ does not always work because $180$ is not divisible by $24$."),
        ("Answer", r"The answer is $\boxed{12}$."),
    ],
    5: [
        ("Use the structure of the expression", r"The expression is $c\cdot a^b-d$. To maximize it, we want $d$ as small as possible and $c\cdot a^b$ as large as possible."),
        ("Choose d", r"Since the available values are $0,1,2,3$, choose $d=0$ so nothing is subtracted."),
        ("Maximize the power", r"The largest useful power from the remaining numbers is $3^2=9$, using $a=3$ and $b=2$. Then the remaining value for $c$ is $1$."),
        ("Compute", r"This gives $1\cdot3^2-0=9$. Trying to make $c=2$ leaves only $3^1$, which gives $6$, so $9$ is larger."),
        ("Answer", r"The maximum possible value is $\boxed{9}$."),
    ],
    6: [
        ("Look for a factorial relationship", r"A product is a perfect square when every prime factor appears an even number of times. The easiest way is to make the expression visibly equal to something squared."),
        ("Use the choice with consecutive factorials", r"Since $100!=100\cdot99!$, we have \[99!\cdot100!=99!\cdot100\cdot99!.\]"),
        ("Rewrite as a square", r"Because $100=10^2$, the product is \[(10\cdot99!)^2.\]"),
        ("Answer", r"Thus $99!\cdot100!$ is a perfect square, so the answer is $\boxed{99!\cdot100!}$."),
    ],
    7: [
        ("Translate the exchange rate", r"For every $7$ U.S. dollars, Isabella receives $10$ Canadian dollars. If she starts with $d$ U.S. dollars, she receives $\frac{10}{7}d$ Canadian dollars."),
        ("Use the spending information", r"After spending $60$ Canadian dollars, she has $d$ Canadian dollars left. So \[\frac{10}{7}d-60=d.\]"),
        ("Solve for d", r"Subtracting $d$ gives $\frac{3}{7}d=60$, so $d=140$."),
        ("Find the digit sum", r"The sum of the digits of $140$ is $1+4+0=5$."),
        ("Answer", r"The answer is $\boxed{5}$."),
    ],
    8: [
        ("Represent the directions", r"From the airport, St. Paul is $8$ miles northeast, while Minneapolis is $10$ miles northwest. These directions are perpendicular diagonal directions."),
        ("Use components", r"The east-west separation is $\frac{8}{\sqrt2}+\frac{10}{\sqrt2}=\frac{18}{\sqrt2}=9\sqrt2$, while the north-south components cancel because both cities are equally northward in direction from the airport."),
        ("Estimate", r"Since $\sqrt2\approx1.414$, the distance is $9\sqrt2\approx12.7$ miles."),
        ("Choose the closest value", r"The closest listed value is $\boxed{13}$."),
    ],
    9: [
        ("Use inclusion-exclusion", r"The union area is square area plus circle area minus the overlap area."),
        ("Compute the square and circle areas", r"The square area is $10^2=100$. The circle has radius $10$, so its area is $100\pi$."),
        ("Find the overlap", r"Since the circle is centered at a vertex of the square, the part of the circle inside the square is exactly one quarter of the circle, with area $25\pi$."),
        ("Subtract the overlap", r"The union area is \[100+100\pi-25\pi=100+75\pi.\]"),
        ("Answer", r"The answer is $\boxed{100+75\pi}$."),
    ],
    10: [
        ("Identify the row sizes", r"The rows have $1,3,5,\ldots$ cans, increasing by $2$ each row. These are the positive odd numbers."),
        ("Use the odd-number sum", r"The sum of the first $n$ positive odd numbers is $n^2$."),
        ("Set up the total", r"If there are $n$ rows and $100$ cans, then $n^2=100$."),
        ("Solve", r"Thus $n=10$."),
        ("Answer", r"The display contains $\boxed{10}$ rows."),
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
        if r["year"] == "2004" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in set(),
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
        + "- Review notes: Corrected 2003 AMC 10B Problem 10 answer choice from the AoPS answer key; Problem 20 uses the diagram data stated in text and should be visually reviewed later.\n",
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
        + "- Answer verification source: AoPS 2003 AMC 10B Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批完成 2004 AMC 10B Problems 1-10，无跳过题。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
