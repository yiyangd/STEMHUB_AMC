import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 127
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2022_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8}
SKIPPED = ["2022 AMC 10A Problem 9 skipped: coloring count depends on the missing region-adjacency diagram.", "2022 AMC 10A Problem 10 skipped: index-card geometry depends on the missing cut-corner diagram."]
BATCH_LABEL = "2022 AMC 10A Problems 1-8"
NEXT_START = "2022 AMC 10A Problem 11"

ANS={1:("D",r"\frac{109}{33}"),2:("B","7"),3:("E","5"),4:("E",r"\frac{100\ell m}{x}"),5:("C",r"2-\sqrt2"),6:("A",r"3-2a"),7:("B","6"),8:("D","36")}

OV={
1:(r"What is the value of \[3+\frac{1}{3+\frac{1}{3+\frac13}}?\]",[("A",r"$\frac{31}{10}$"),("B",r"$\frac{49}{15}$"),("C",r"$\frac{33}{10}$"),("D",r"$\frac{109}{33}$"),("E",r"$\frac{15}{4}$")]),
2:(r"Mike cycled $15$ laps in $57$ minutes at a constant speed. Approximately how many laps did he complete in the first $27$ minutes?",[("A","5"),("B","7"),("C","9"),("D","11"),("E","13")]),
3:(r"The sum of three numbers is $96$. The first number is $6$ times the third number, and the third number is $40$ less than the second number. What is the absolute value of the difference between the first and second numbers?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
4:(r"Suppose $1$ kilometer equals $m$ miles, and $1$ gallon equals $\ell$ liters. Which expression gives the fuel efficiency in liters per $100$ kilometers for a car that gets $x$ miles per gallon?",[("A",r"$\frac{x}{100\ell m}$"),("B",r"$\frac{x\ell m}{100}$"),("C",r"$\frac{\ell m}{100x}$"),("D",r"$\frac{100}{x\ell m}$"),("E",r"$\frac{100\ell m}{x}$")]),
5:(r"Square $ABCD$ has side length $1$. Points $P,Q,R,$ and $S$ each lie on a side of $ABCD$ such that $APQCRS$ is an equilateral convex hexagon with side length $s$. What is $s$?",[("A",r"$\frac{\sqrt2}{3}$"),("B",r"$\frac12$"),("C",r"$2-\sqrt2$"),("D",r"$1-\frac{\sqrt2}{4}$"),("E",r"$\frac23$")]),
6:(r"Which expression is equal to \[\left|a-2-\sqrt{(a-1)^2}\right|\] for $a<0$?",[("A",r"$3-2a$"),("B",r"$1-a$"),("C","1"),("D",r"$a+1$"),("E","3")]),
7:(r"The least common multiple of a positive integer $n$ and $18$ is $180$, and the greatest common divisor of $n$ and $45$ is $15$. What is the sum of the digits of $n$?",[("A","3"),("B","6"),("C","8"),("D","9"),("E","12")]),
8:(r"A data set consists of $6$ not necessarily distinct positive integers: $1,7,5,2,5,$ and $X$. The average of the $6$ numbers equals a value in the data set. What is the sum of all positive values of $X$?",[("A","10"),("B","26"),("C","32"),("D","36"),("E","40")]),
}

KEY_OVERRIDES={1:"Evaluate a continued fraction from the inside out.",2:"Use a constant-rate proportion.",3:"Set up a linear equation from three number relationships.",4:"Convert miles per gallon into liters per 100 kilometers.",5:"Use an isosceles right corner triangle in the square.",6:"Use square root of a square as absolute value.",7:"Use prime exponents from lcm and gcd conditions.",8:"Test which data-set value can equal the mean."}

SOL={
1:[("Start from the innermost denominator",r"Work from the inside out. First, \[3+\frac13=\frac{10}{3}.\]"),("Move one layer outward",r"The next denominator is \[3+\frac{1}{10/3}=3+\frac{3}{10}=\frac{33}{10}.\]"),("Evaluate the whole expression",r"Now the original expression is \[3+\frac{1}{33/10}=3+\frac{10}{33}.\]"),("Combine",r"Thus \[3+\frac{10}{33}=\frac{99}{33}+\frac{10}{33}=\frac{109}{33}.\]"),("Conclude",r"The answer is $\boxed{\frac{109}{33}}$."),],
2:[("Use constant speed",r"Since Mike cycles at a constant speed, laps are proportional to time."),("Set up the proportion",r"In $57$ minutes he cycles $15$ laps, so in $27$ minutes he cycles \[15\cdot\frac{27}{57}.\]"),("Approximate",r"This equals \[\frac{405}{57}\approx7.1.\]"),("Choose the closest answer",r"The closest answer choice is $7$."),("Conclude",r"The answer is $\boxed{7}$."),],
3:[("Name the third number",r"Let the third number be $t$. Then the first number is $6t$, and the second number is $t+40$."),("Use the sum",r"The three numbers add to $96$, so \[6t+(t+40)+t=96.\]"),("Solve",r"This gives \[8t+40=96,\] so $t=7$."),("Find the first two numbers",r"The first number is $6t=42$, and the second number is $t+40=47$."),("Conclude",r"The absolute difference is \[|42-47|=\boxed{5}.\]"),],
4:[("Interpret x miles per gallon",r"The car travels $x$ miles using $1$ gallon, which is $\ell$ liters."),("Convert miles to kilometers",r"Since $1$ kilometer is $m$ miles, $x$ miles is \[\frac{x}{m}\] kilometers."),("Find liters per kilometer",r"The fuel use is \[\frac{\ell}{x/m}=\frac{\ell m}{x}\] liters per kilometer."),("Scale to 100 kilometers",r"For $100$ kilometers, multiply by $100$: \[\frac{100\ell m}{x}.\]"),("Conclude",r"The answer is $\boxed{\frac{100\ell m}{x}}$."),],
5:[("Locate the key right triangle",r"Because the hexagon has side length $s$, the leftover segments near a corner of the square have length $1-s$."),("Use the diagonal side of the hexagon",r"In the corner near $B$, the segment $PQ$ is a side of the equilateral hexagon, so $PQ=s$. It is also the hypotenuse of an isosceles right triangle with legs $1-s$."),("Set up the equation",r"Thus \[s=(1-s)\sqrt2.\]"),("Solve",r"We get \[s=\sqrt2-s\sqrt2,\] so \[(1+\sqrt2)s=\sqrt2.\] Therefore \[s=\frac{\sqrt2}{1+\sqrt2}=2-\sqrt2.\]"),("Conclude",r"The answer is $\boxed{2-\sqrt2}$."),],
6:[("Replace the square root carefully",r"For any real $u$, $\sqrt{u^2}=|u|$. Here $u=a-1$. Since $a<0$, $a-1<0$, so \[|a-1|=1-a.\]"),("Substitute",r"The expression becomes \[\left|a-2-(1-a)\right|.\]"),("Simplify inside",r"Inside the absolute value, \[a-2-1+a=2a-3.\]"),("Remove the absolute value",r"Because $a<0$, $2a-3<0$, so \[|2a-3|=3-2a.\]"),("Conclude",r"The answer is $\boxed{3-2a}$."),],
7:[("Use prime factors",r"Write \[18=2\cdot3^2,\quad180=2^2\cdot3^2\cdot5,\quad45=3^2\cdot5.\]"),("Use the lcm condition",r"The lcm of $n$ and $18$ is $180$, so $n$ must contribute $2^2$ and $5$, and it cannot contain prime powers beyond those in $180$."),("Use the gcd condition",r"The gcd of $n$ and $45$ is $15=3\cdot5$. Therefore $n$ has exactly one factor of $3$ and at least one factor of $5$."),("Determine n",r"Combining the exponent conditions gives \[n=2^2\cdot3\cdot5=60.\]"),("Conclude",r"The sum of the digits of $60$ is $\boxed{6}$."),],
8:[("Write the average",r"The known five numbers sum to \[1+7+5+2+5=20.\] Thus the average is \[\frac{20+X}{6}.\]"),("Test possible data values",r"The average must equal one of the data values: $1,2,5,7,$ or $X$."),("Find possible X values",r"If the average is $5$, then $20+X=30$, so $X=10$. If the average is $7$, then $20+X=42$, so $X=22$. If the average is $X$, then $20+X=6X$, so $X=4$."),("Reject impossible cases",r"An average of $1$ or $2$ is impossible because the known sum is already $20$."),("Add",r"The positive possible values are $10,22,4$, and their sum is \[10+22+4=36.\]"),("Conclude",r"The answer is $\boxed{36}$."),],
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
        if r["year"] == "2022" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2022 AMC 10A Answer Key\n\n"
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












































