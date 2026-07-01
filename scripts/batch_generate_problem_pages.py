from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 53
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2010_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2010 AMC 10B Problems 1-10"
NEXT_START = "2010 AMC 10B Problem 11"

ANS={1:("C","-297"),2:("C","25"),3:("C","5"),4:("C","10"),5:("B","3"),6:("B","25"),7:("D","32"),8:("E","5"),9:("D","3"),10:("C","24")}

OV={
1:(r"What is $100(100-3)-(100\cdot100-3)$?",[("A",r"$-20{,}000$"),("B",r"$-10{,}000$"),("C",r"$-297$"),("D",r"$-6$"),("E","$0$")]),
2:(r"Makayla attended two meetings during her $9$-hour work day. The first meeting took $45$ minutes and the second meeting took twice as long. What percent of her work day was spent attending meetings?",[("A","$15$"),("B","$20$"),("C","$25$"),("D","$30$"),("E","$35$")]),
3:(r"A drawer contains red, green, blue, and white socks with at least $2$ of each color. What is the minimum number of socks that must be pulled from the drawer to guarantee a matching pair?",[("A","$3$"),("B","$4$"),("C","$5$"),("D","$8$"),("E","$9$")]),
4:(r"For a real number $x$, define $\heartsuit(x)$ to be the average of $x$ and $x^2$. What is $\heartsuit(1)+\heartsuit(2)+\heartsuit(3)$?",[("A","$3$"),("B","$6$"),("C","$10$"),("D","$12$"),("E","$20$")]),
5:(r"A month with $31$ days has the same number of Mondays and Wednesdays. How many of the seven days of the week could be the first day of this month?",[("A","$2$"),("B","$3$"),("C","$4$"),("D","$5$"),("E","$6$")]),
6:(r"A circle is centered at $O$, $AB$ is a diameter, and $C$ is a point on the circle with $\angle COB=50^\circ$. What is the degree measure of $\angle CAB$?",[("A","$20$"),("B","$25$"),("C","$45$"),("D","$50$"),("E","$65$")]),
7:(r"A triangle has side lengths $10$, $10$, and $12$. A rectangle has width $4$ and area equal to the area of the triangle. What is the perimeter of this rectangle?",[("A","$16$"),("B","$24$"),("C","$28$"),("D","$32$"),("E","$36$")]),
8:(r"A ticket to a school play costs $x$ dollars, where $x$ is a whole number. A group of 9th graders buys tickets costing a total of $48$, and a group of 10th graders buys tickets costing a total of $64$. How many values of $x$ are possible?",[("A","$1$"),("B","$2$"),("C","$3$"),("D","$4$"),("E","$5$")]),
9:(r"Larry's teacher asked him to substitute numbers for $a,b,c,d,$ and $e$ in $a-(b-(c-(d+e)))$. Larry ignored the parentheses but added and subtracted correctly and obtained the correct result by coincidence. The numbers substituted for $a,b,c,$ and $d$ were $1,2,3,$ and $4$, respectively. What number did Larry substitute for $e$?",[("A",r"$-5$"),("B",r"$-3$"),("C","$0$"),("D","$3$"),("E","$5$")]),
10:(r"Shelby drives her scooter at $30$ miles per hour if it is not raining, and $20$ miles per hour if it is raining. Today she drove in the sun in the morning and in the rain in the evening, for a total of $16$ miles in $40$ minutes. How many minutes did she drive in the rain?",[("A","$18$"),("B","$21$"),("C","$24$"),("D","$27$"),("E","$30$")]),
}

KEY_OVERRIDES={1:"Expand carefully and keep the parentheses separate.",2:"Convert all time to minutes and compare meeting time with the full workday.",3:"Use the pigeonhole principle with four sock colors.",4:"Evaluate the defined average for each input.",5:"A 31-day month has three extra weekdays beyond four full weeks.",6:"Use the inscribed angle theorem.",7:"Find the isosceles triangle's height, then match rectangle area.",8:"The ticket price must divide both total costs.",9:"Compare the correct expression with the expression Larry evaluated without parentheses.",10:"Use time variables and distance equals rate times time."}

SOL={
1:[("Evaluate the first part",r"The first expression is $100(100-3)=100\cdot97=9700$."),("Evaluate the second part",r"The expression in parentheses is $100\cdot100-3=10000-3=9997$."),("Subtract",r"So the value is $9700-9997=-297$."),("Answer",r"The answer is $\boxed{-297}$.")],
2:[("Find meeting time",r"The first meeting took $45$ minutes. The second took twice as long, so it took $90$ minutes."),("Add meeting time",r"The total meeting time was $45+90=135$ minutes."),("Convert the workday",r"A $9$-hour workday is $9\cdot60=540$ minutes."),("Find the percent",r"The fraction of the day spent in meetings is $\frac{135}{540}=\frac14$, or $25\%$."),("Answer",r"She spent $\boxed{25\%}$ of her workday in meetings.")],
3:[("Think worst case",r"To avoid a matching pair as long as possible, we could pull one sock of each color."),("Use four colors",r"There are four colors, so it is possible to pull $4$ socks without a match: one red, one green, one blue, and one white."),("Force the match",r"The next sock, the fifth sock, must match one of those four colors."),("Answer",r"The minimum number is $\boxed{5}$ socks.")],
4:[("Write the operation",r"The value $\heartsuit(x)$ is the average of $x$ and $x^2$, so $\heartsuit(x)=\frac{x+x^2}{2}$."),("Evaluate each term",r"We get $\heartsuit(1)=1$, $\heartsuit(2)=\frac{2+4}{2}=3$, and $\heartsuit(3)=\frac{3+9}{2}=6$."),("Add",r"The sum is $1+3+6=10$."),("Answer",r"The answer is $\boxed{10}$.")],
5:[("Use full weeks",r"A $31$-day month contains four full weeks, accounting for $28$ days. Each weekday occurs at least four times."),("Look at the extra days",r"The remaining $3$ days are consecutive weekdays starting with the first day of the month. Only these extra days can make weekday counts differ."),("Require Mondays and Wednesdays to match",r"The extra three-day block must contain both Monday and Wednesday, or contain neither of them."),("Count starts",r"Starting on Monday gives Monday-Tuesday-Wednesday, which contains both. Starting on Thursday gives Thursday-Friday-Saturday, and starting on Friday gives Friday-Saturday-Sunday, which contain neither. These are $3$ possibilities."),("Answer",r"There are $\boxed{3}$ possible first weekdays.")],
6:[("Identify the arc",r"The central angle $\angle COB=50^\circ$ measures the minor arc $CB$."),("Use the inscribed angle theorem",r"Angle $\angle CAB$ is an inscribed angle that intercepts the same arc $CB$."),("Take half",r"An inscribed angle has half the measure of its intercepted arc, so $\angle CAB=\frac12\cdot50^\circ=25^\circ$."),("Answer",r"The angle measure is $\boxed{25^\circ}$.")],
7:[("Find the triangle height",r"The triangle is isosceles with equal sides $10$ and base $12$. The altitude to the base splits the base into two segments of length $6$."),("Use the Pythagorean theorem",r"The height is $\sqrt{10^2-6^2}=\sqrt{100-36}=8$."),("Find the triangle area",r"The area is $\frac12\cdot12\cdot8=48$."),("Find the rectangle length",r"The rectangle has width $4$ and area $48$, so its length is $12$."),("Compute perimeter",r"The perimeter is $2(4+12)=32$."),("Answer",r"The rectangle's perimeter is $\boxed{32}$.")],
8:[("Interpret x",r"The ticket price $x$ must be a whole number of dollars."),("Use both groups",r"Since one group spent $48$ dollars and the other spent $64$ dollars, $x$ must divide both $48$ and $64$."),("Find common divisors",r"The common divisors are the divisors of $\gcd(48,64)=16$: $1,2,4,8,16$."),("Count",r"There are $5$ possible values of $x$."),("Answer",r"The answer is $\boxed{5}$.")],
9:[("Evaluate the correct expression",r"With $a=1$, $b=2$, $c=3$, and $d=4$, the correct expression is $1-(2-(3-(4+e)))$. This simplifies to $-2-e$."),("Evaluate Larry's expression",r"Ignoring parentheses but keeping the signs in order gives $1-2-3-4+e=e-8$."),("Set them equal",r"Larry got the correct result by coincidence, so $e-8=-2-e$."),("Solve",r"Then $2e=6$, so $e=3$."),("Answer",r"Larry substituted $\boxed{3}$ for $e$.")],
10:[("Use hours",r"Forty minutes is $\frac23$ hour. Let $t$ be the number of hours Shelby drove in the rain."),("Write the sunny time",r"Then she drove for $\frac23-t$ hours in the sun."),("Write the distance equation",r"The total distance is $20t+30(\frac23-t)=16$."),("Solve",r"This becomes $20t+20-30t=16$, so $10t=4$ and $t=0.4$ hours."),("Convert to minutes",r"The time in rain was $0.4\cdot60=24$ minutes."),("Answer",r"She drove in the rain for $\boxed{24}$ minutes.")],
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
        if r["year"] == "2010" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2010 AMC 10B Answer Key\n\n"
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
















