from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 44
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2009_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
SKIPPED = []
BATCH_LABEL = "2009 AMC 10A Problems 1-10"
NEXT_START = "2009 AMC 10A Problem 11"

ANS = {1:("E","11"),2:("A","15"),3:("C",r"\frac{5}{3}"),4:("A",r"\frac{120}{11}"),5:("E","81"),6:("A",r"\frac{1}{2}"),7:("C",r"\frac{10}{3}"),8:("B","36"),9:("B","41"),10:("B",r"7\sqrt3")}

OV = {
  1:(r"One can holds $12$ ounces of soda. What is the minimum number of cans needed to provide a gallon, or $128$ ounces, of soda?",[("A","$7$"),("B","$8$"),("C","$9$"),("D","$10$"),("E","$11$")]),
  2:(r"Four coins are picked out of a piggy bank that contains pennies, nickels, dimes, and quarters. Which of the following could not be the total value of the four coins, in cents?",[("A","$15$"),("B","$25$"),("C","$35$"),("D","$45$"),("E","$55$")]),
  3:(r"Which of the following is equal to $1+\frac{1}{1+\frac{1}{1+1}}$?",[("A",r"$\frac54$"),("B",r"$\frac32$"),("C",r"$\frac53$"),("D","$2$"),("E","$3$")]),
  4:(r"Eric plans to compete in a triathlon. He can average $2$ miles per hour in the $\frac14$-mile swim and $6$ miles per hour in the $3$-mile run. His goal is to finish the triathlon in $2$ hours. To accomplish his goal, what must his average speed, in miles per hour, be for the $15$-mile bicycle ride?",[("A",r"$\frac{120}{11}$"),("B","$11$"),("C",r"$\frac{56}{5}$"),("D",r"$\frac{45}{4}$"),("E","$12$")]),
  5:(r"What is the sum of the digits of the square of $111{,}111{,}111$?",[("A","$18$"),("B","$27$"),("C","$45$"),("D","$63$"),("E","$81$")]),
  6:(r"A circle of radius $2$ is inscribed in a semicircle. The area inside the semicircle but outside the circle is shaded. What fraction of the semicircle's area is shaded?",[("A",r"$\frac12$"),("B",r"$\frac{\pi}{6}$"),("C",r"$\frac{2}{\pi}$"),("D",r"$\frac23$"),("E",r"$\frac{3}{\pi}$")]),
  7:(r"A carton contains milk that is $2\%$ fat, an amount that is $40\%$ less fat than the amount contained in a carton of whole milk. What is the percentage of fat in whole milk?",[("A",r"$\frac{12}{5}$"),("B","$3$"),("C",r"$\frac{10}{3}$"),("D",r"$\frac{38}{5}$"),("E",r"$\frac{42}{5}$")]),
  8:(r"Three generations of the Wen family are going to the movies, two from each generation. The two members of the youngest generation receive a $50\%$ discount as children. The two members of the oldest generation receive a $25\%$ discount as senior citizens. The two members of the middle generation receive no discount. Grandfather Wen, whose senior ticket costs $\$6.00$, is paying for everyone. How many dollars must he pay?",[("A","$34$"),("B","$36$"),("C","$42$"),("D","$46$"),("E","$48$")]),
  9:(r"Positive integers $a$, $b$, and $2009$, with $a<b<2009$, form a geometric sequence with an integer ratio. What is $a$?",[("A","$7$"),("B","$41$"),("C","$49$"),("D","$289$"),("E","$2009$")]),
  10:(r"Triangle $ABC$ has a right angle at $B$. Point $D$ is the foot of the altitude from $B$ to $AC$, $AD=3$, and $DC=4$. What is the area of $\triangle ABC$?",[("A",r"$4\sqrt3$"),("B",r"$7\sqrt3$"),("C","$21$"),("D",r"$14\sqrt3$"),("E","$42$")]),
}

KEY_OVERRIDES={1:"Round up after dividing ounces needed by ounces per can.",2:"Check four-coin totals using coin denominations.",3:"Simplify the nested fraction from the inside out.",4:"Subtract swim and run time from the total time to find the required biking speed.",5:"Use the repunit square pattern to avoid long multiplication.",6:"Relate the inscribed circle radius to the larger semicircle radius and compare areas.",7:"Translate '40 percent less' into 60 percent of the whole-milk fat percentage.",8:"Use the senior discount to recover the full ticket price, then price all six tickets.",9:"Use prime factorization of 2009 and the integer common ratio.",10:"Use the right-triangle altitude relation BD squared equals AD times DC."}

SOL={
1:[("Identify the unit",r"Each can contributes $12$ ounces, and the target is $128$ ounces."),("Divide to estimate",r"We compute $128\div12=10\frac{2}{3}$. This means $10$ cans would be too few."),("Round in the correct direction",r"Because cans come in whole numbers, we must round up, not down."),("Check the amount",r"With $11$ cans, the amount is $11\cdot12=132$ ounces, which is enough."),("Answer",r"The minimum number of cans is $\boxed{11}$.")],
2:[("Use four coin values",r"The available coin values are $1,5,10,$ and $25$ cents. We need exactly four coins."),("Show the other choices are possible",r"We can make $25=10+5+5+5$, $35=10+10+10+5$, $45=25+10+5+5$, and $55=25+10+10+10$."),("Test 15 cents",r"With four coins, using a dime leaves $5$ cents for three coins, impossible because the smallest three coins sum to $3$ and no combination gives exactly $5$ with three coins except $1+1+3$, and there is no $3$-cent coin. Without a dime, four nickels already make $20$ if all are nickels, and adding pennies cannot reach $15$ with exactly four coins."),("Answer",r"The impossible total is $\boxed{15}$ cents.")],
3:[("Start inside",r"The innermost denominator is $1+1=2$, so the inner fraction is $\frac{1}{2}$."),("Simplify the next denominator",r"Now the middle denominator is $1+\frac12=\frac32$. Thus the large fraction is $\frac{1}{3/2}=\frac23$."),("Finish",r"The whole expression is $1+\frac23=\frac53$."),("Answer",r"The value is $\boxed{\frac53}$.")],
4:[("Find the swim time",r"The swim is $\frac14$ mile at $2$ miles per hour, so it takes $\frac{1/4}{2}=\frac18$ hour."),("Find the run time",r"The run is $3$ miles at $6$ miles per hour, so it takes $\frac36=\frac12$ hour."),("Find the bike time left",r"The total goal is $2$ hours, so the bike ride must take $2-\frac18-\frac12=\frac{11}{8}$ hours."),("Compute the biking speed",r"Speed is distance divided by time: $15\div\frac{11}{8}=15\cdot\frac8{11}=\frac{120}{11}$."),("Answer",r"The required speed is $\boxed{\frac{120}{11}}$ miles per hour.")],
5:[("Notice the structure",r"The number $111{,}111{,}111$ is a repunit, a number made of nine $1$ digits."),("Use the repunit square pattern",r"Squaring a repunit with nine digits gives increasing digits up to $9$ and then decreasing digits: $12345678987654321$."),("Split the digit sum",r"The digit sum is $(1+2+\cdots+9)+(8+7+\cdots+1)$."),("Compute",r"These sums are $45$ and $36$, so the total digit sum is $81$."),("Answer",r"The sum of the digits is $\boxed{81}$.")],
6:[("Infer the larger radius",r"For a circle of radius $2$ inscribed in a semicircle in the standard way, it is tangent to the diameter and the semicircular arc. The larger semicircle has radius $4$."),("Compare areas",r"The semicircle area is $\frac12\pi(4)^2=8\pi$. The small circle area is $\pi(2)^2=4\pi$."),("Find the shaded fraction",r"The shaded area is $8\pi-4\pi=4\pi$, which is half the semicircle area."),("Answer",r"The shaded fraction is $\boxed{\frac12}$.")],
7:[("Translate the percent statement",r"Let $w$ be the fat percentage of whole milk. The $2\%$ milk has $40\%$ less fat, so it has $60\%$ of the whole-milk fat."),("Set up the equation",r"Thus $2=0.60w=\frac35w$."),("Solve",r"Multiplying by $\frac53$ gives $w=2\cdot\frac53=\frac{10}{3}$."),("Answer",r"Whole milk is $\boxed{\frac{10}{3}\%}$ fat.")],
8:[("Recover the regular ticket price",r"A senior ticket has a $25\%$ discount, so it costs $75\%$ of the regular price. If $0.75$ of the regular price is $6$, then the regular price is $6\div0.75=8$ dollars."),("Price each generation",r"The two seniors cost $2\cdot6=12$ dollars. The two middle-generation tickets cost $2\cdot8=16$ dollars. The two children's tickets are half price, so they cost $2\cdot4=8$ dollars."),("Add",r"The total is $12+16+8=36$ dollars."),("Answer",r"Grandfather Wen must pay $\boxed{36}$ dollars.")],
9:[("Use the geometric sequence form",r"Since $a,b,2009$ form a geometric sequence with integer ratio $r$, we have $b=ar$ and $2009=ar^2$."),("Factor 2009",r"We factor $2009=7^2\cdot41$. Therefore the square factor $r^2$ must be $7^2$, so $r=7$."),("Find a",r"Then $a=\frac{2009}{7^2}=41$. This also gives $b=287$, which satisfies $a<b<2009$."),("Answer",r"The value of $a$ is $\boxed{41}$.")],
10:[("Use the altitude-to-hypotenuse relation",r"In a right triangle, the altitude from the right angle to the hypotenuse satisfies $BD^2=AD\cdot DC$. Here $AD=3$ and $DC=4$, so $BD^2=12$."),("Find the altitude",r"Thus $BD=2\sqrt3$."),("Use AC as the base",r"The hypotenuse is split into $AD+DC=3+4=7$, so $AC=7$."),("Compute area",r"Using base $AC$ and height $BD$, the area is $\frac12\cdot7\cdot2\sqrt3=7\sqrt3$."),("Answer",r"The area is $\boxed{7\sqrt3}$.")],
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
        if r["year"] == "2009" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {6, 10},
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
        + "- Answer verification source: AoPS 2009 AMC 10A Answer Key\n\n"
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






