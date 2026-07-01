from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 38
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2008_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 10}
SKIPPED = [
    "2008 AMC 10A Problem 9 skipped: OCR makes the fractional expression unreliable.",
]
BATCH_LABEL = "2008 AMC 10A Problems 1-8, 10"
NEXT_START = "2008 AMC 10A Problem 11"

ANS = {
    1: ("D", "4:30 PM"),
    2: ("A", "12.5"),
    3: ("A", "6"),
    4: ("C", "3"),
    5: ("B", "502"),
    6: ("D", "6"),
    7: ("E", "9"),
    8: ("A", "750"),
    10: ("E", "4"),
}


OV = {
    1: (r"A bakery owner turns on his doughnut machine at $8{:}30$ AM. At $11{:}10$ AM the machine has completed one third of the day's job. At what time will the doughnut machine complete the job?", [("A", "1:50 PM"), ("B", "3:00 PM"), ("C", "3:30 PM"), ("D", "4:30 PM"), ("E", "5:50 PM")]),
    2: (r"A square is drawn inside a rectangle. The ratio of the width of the rectangle to a side of the square is $2:1$. The ratio of the rectangle's length to its width is $2:1$. What percent of the rectangle's area is inside the square?", [("A", "$12.5$"), ("B", "$25$"), ("C", "$50$"), ("D", "$75$"), ("E", "$87.5$")]),
    3: (r"For the positive integer $n$, let $\langle n\rangle$ denote the sum of all the positive divisors of $n$ with the exception of $n$ itself. For example, $\langle4\rangle=1+2=3$ and $\langle12\rangle=1+2+3+4+6=16$. What is $\langle\langle\langle6\rangle\rangle\rangle$?", [("A", "$6$"), ("B", "$12$"), ("C", "$24$"), ("D", "$32$"), ("E", "$36$")]),
    4: (r"Suppose that $\frac{2}{3}$ of $10$ bananas are worth as much as $8$ oranges. How many oranges are worth as much as $\frac{1}{2}$ of $5$ bananas?", [("A", "$2$"), ("B", r"$\frac52$"), ("C", "$3$"), ("D", r"$\frac72$"), ("E", "$4$")]),
    5: (r"Which of the following is equal to the product $\frac84\cdot\frac{12}{8}\cdot\frac{16}{12}\cdots\frac{2008}{2004}$?", [("A", "$251$"), ("B", "$502$"), ("C", "$1004$"), ("D", "$2008$"), ("E", "$4016$")]),
    6: (r"A triathlete competes in a triathlon in which the swimming, biking, and running segments are all of the same length. The triathlete swims at $3$ kilometers per hour, bikes at $20$ kilometers per hour, and runs at $10$ kilometers per hour. Which of the following is closest to the triathlete's average speed, in kilometers per hour, for the entire race?", [("A", "$3$"), ("B", "$4$"), ("C", "$5$"), ("D", "$6$"), ("E", "$7$")]),
    7: (r"The fraction $\frac{(3^{2008})^2-(3^{2006})^2}{(3^{2007})^2-(3^{2005})^2}$ simplifies to which of the following?", [("A", r"$\frac14$"), ("B", r"$\frac94$"), ("C", "$3$"), ("D", r"$\frac92$"), ("E", "$9$")]),
    8: (r"Heather compares the price of a new computer at two different stores. Store A offers $15\%$ off the sticker price followed by a $\$90$ rebate, and store B offers $25\%$ off the same sticker price with no rebate. Heather saves $\$15$ by buying the computer at store A instead of store B. What is the sticker price of the computer, in dollars?", [("A", "$750$"), ("B", "$900$"), ("C", "$1000$"), ("D", "$1050$"), ("E", "$1500$")]),
    10: (r"Each of the sides of a square $S_1$ with area $16$ is bisected, and a smaller square $S_2$ is constructed using the bisection points as vertices. The same process is carried out on $S_2$ to construct an even smaller square $S_3$. What is the area of $S_3$?", [("A", r"$\frac12$"), ("B", "$1$"), ("C", "$2$"), ("D", "$3$"), ("E", "$4$")]),
}


KEY_OVERRIDES = {
    1: "Use constant work rate: one third of the job determines the full time.",
    2: "Express rectangle dimensions in terms of the square side and compare areas.",
    3: "Iterate the proper-divisor-sum function carefully.",
    4: "Convert both fruit values through a common banana-to-orange ratio.",
    5: "Use telescoping cancellation in a product of fractions.",
    6: "For equal distances, average speed is total distance divided by total time, not the arithmetic mean of speeds.",
    7: "Factor differences of squares and cancel common powers.",
    8: "Translate discounts and rebates into equations in the sticker price.",
    10: "Joining side midpoints of a square creates a new square with half the area.",
}


SOL = {
    1: [("Find the time for one third", r"From $8{:}30$ AM to $11{:}10$ AM is $2$ hours $40$ minutes, or $160$ minutes. That is one third of the job."), ("Scale to the whole job", r"If $160$ minutes is one third, then the full job takes $3\cdot160=480$ minutes, which is $8$ hours."), ("Add to the start time", r"Starting at $8{:}30$ AM, adding $8$ hours gives $4{:}30$ PM."), ("Answer", r"The machine completes the job at $\boxed{4{:}30\text{ PM}}$." )],
    2: [("Choose a convenient square side", r"Let the side of the square be $s$. The rectangle's width is twice that, so its width is $2s$."), ("Find the rectangle length", r"The rectangle's length is twice its width, so the length is $4s$."), ("Compare areas", r"The square area is $s^2$, and the rectangle area is $(2s)(4s)=8s^2$."), ("Convert to percent", r"The fraction inside the square is $\frac{s^2}{8s^2}=\frac18=12.5\%$."), ("Answer", r"The answer is $\boxed{12.5\%}$." )],
    3: [("Evaluate the first layer", r"The proper positive divisors of $6$ are $1,2,3$, and their sum is $1+2+3=6$. Thus $\langle6\rangle=6$."), ("Notice the fixed value", r"Since applying the operation to $6$ gives $6$ again, every additional application also gives $6$."), ("Apply all three brackets", r"Therefore $\langle\langle\langle6\rangle\rangle\rangle=6$."), ("Answer", r"The answer is $\boxed{6}$." )],
    4: [("Find the banana amount equivalent to 8 oranges", r"Two thirds of $10$ bananas is $\frac{2}{3}\cdot10=\frac{20}{3}$ bananas. This is worth $8$ oranges."), ("Find the target banana amount", r"One half of $5$ bananas is $\frac52$ bananas."), ("Scale the value", r"The number of oranges equivalent to $\frac52$ bananas is $8\cdot\frac{(5/2)}{(20/3)}=8\cdot\frac{15}{40}=3$."), ("Answer", r"The answer is $\boxed{3}$ oranges." )],
    5: [("Recognize the telescoping pattern", r"The product is $\frac84\cdot\frac{12}{8}\cdot\frac{16}{12}\cdots\frac{2008}{2004}$. Every numerator after the first cancels with the next denominator."), ("Cancel", r"After cancellation, only the final numerator and first denominator remain: $\frac{2008}{4}$."), ("Compute", r"$\frac{2008}{4}=502$."), ("Answer", r"The product is $\boxed{502}$." )],
    6: [("Use equal segment lengths", r"Let each segment have length $d$. The total distance is $3d$."), ("Compute total time", r"The total time is $\frac d3+\frac d{20}+\frac d{10}=d\left(\frac13+rac1{20}+rac1{10}\right)=d\cdot\frac{29}{60}$."), ("Find average speed", r"Average speed is total distance divided by total time, so it is $\frac{3d}{29d/60}=\frac{180}{29}\approx6.2$."), ("Choose the closest option", r"The closest listed speed is $6$ kilometers per hour."), ("Answer", r"The answer is $\boxed{6}$." )],
    7: [("Use difference of squares", r"Both numerator and denominator have the form $A^2-B^2=(A-B)(A+B)$, but factoring powers of $3$ is even faster."), ("Factor the numerator", r"$(3^{2008})^2-(3^{2006})^2=3^{4016}-3^{4012}=3^{4012}(3^4-1)$."), ("Factor the denominator", r"$(3^{2007})^2-(3^{2005})^2=3^{4014}-3^{4010}=3^{4010}(3^4-1)$."), ("Cancel", r"The common factor $(3^4-1)$ cancels, leaving $3^{4012}/3^{4010}=3^2=9$."), ("Answer", r"The expression simplifies to $\boxed{9}$." )],
    8: [("Let the sticker price be x", r"Store A's final price is $0.85x-90$. Store B's final price is $0.75x$."), ("Use the savings statement", r"Heather saves $15$ by buying at Store A, so Store B's price is $15$ more than Store A's price: $0.75x-(0.85x-90)=15$."), ("Solve", r"This gives $-0.10x+90=15$, so $0.10x=75$, and $x=750$."), ("Answer", r"The sticker price is $\boxed{750}$ dollars." )],
    10: [("Understand the midpoint square", r"When the side midpoints of a square are connected, the new square has diagonals equal to the side length of the original square."), ("Compare areas", r"A square whose diagonal is $d$ has area $\frac{d^2}{2}$. Therefore the midpoint square has half the area of the original square."), ("Apply twice", r"Starting from area $16$, the first new square has area $8$, and the second new square has area $4$."), ("Answer", r"The area of $S_3$ is $\boxed{4}$." )],
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
        if r["year"] == "2008" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Review notes: Skipped Problem 9 because OCR makes the fractional expression unreliable.\n",
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
        + "- Answer verification source: AoPS 2008 AMC 10A Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批跳过 2008 AMC 10A Problem 9：OCR 中分式结构不可靠。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
