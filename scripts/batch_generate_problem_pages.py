import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 89
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2015_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16}
SKIPPED = []
BATCH_LABEL = "2015 AMC 10B Problems 11-16"
NEXT_START = "2015 AMC 10B Problem 17"

ANS={11:("B",r"\frac25"),12:("A","11"),13:("E",r"\frac{281}{13}"),14:("D","16.5"),15:("B","47"),16:("C",r"\frac1{80}")}

OV={
11:(r"Among the positive integers less than $100$, each of whose digits is a prime number, one is selected at random. What is the probability that the selected number is prime?",[("A",r"\frac8{99}"),("B",r"\frac25"),("C",r"\frac9{20}"),("D",r"\frac12"),("E",r"\frac9{16}")]),
12:(r"For how many integers $x$ is the point $(x,-x)$ inside or on the circle of radius $10$ centered at $(5,5)$?",[("A","11"),("B","12"),("C","13"),("D","14"),("E","15")]),
13:(r"The line $12x+5y=60$ forms a triangle with the coordinate axes. What is the sum of the lengths of the altitudes of this triangle?",[("A","20"),("B",r"\frac{360}{17}"),("C",r"\frac{107}{5}"),("D",r"\frac{43}{2}"),("E",r"\frac{281}{13}")]),
14:(r"Let $a$, $b$, and $c$ be three distinct one-digit numbers. What is the maximum value of the sum of the roots of the equation $(x-a)(x-b)+(x-b)(x-c)=0$?",[("A","15"),("B","15.5"),("C","16"),("D","16.5"),("E","17")]),
15:(r"The town of Hamlet has $3$ people for each horse, $4$ sheep for each cow, and $3$ ducks for each person. Which of the following could not possibly be the total number of people, horses, sheep, cows, and ducks in Hamlet?",[("A","41"),("B","47"),("C","59"),("D","61"),("E","66")]),
16:(r"Al, Bill, and Cal will each randomly be assigned a whole number from $1$ to $10$, inclusive, with no two of them getting the same number. What is the probability that Al's number will be a whole number multiple of Bill's and Bill's number will be a whole number multiple of Cal's?",[("A",r"\frac9{1000}"),("B",r"\frac1{90}"),("C",r"\frac1{80}"),("D",r"\frac1{72}"),("E",r"\frac2{121}")]),
}

KEY_OVERRIDES={11:"Count eligible digit-prime numbers, then count which are prime.",12:"Substitute the point into the circle inequality.",13:"Use the 5-12-13 intercept triangle and area-altitude relations.",14:"Use Vieta's formula and maximize the weighted digit sum.",15:"Translate population ratios into a linear combination.",16:"Count ordered triples forming a divisibility chain."}

SOL={
11:[("Count eligible numbers",r"The prime digits are $2,3,5,7$. There are $4$ one-digit eligible numbers and $4\cdot4=16$ two-digit eligible numbers, for $20$ total."),("Count prime one-digit numbers",r"All four one-digit eligible numbers are prime."),("Count prime two-digit numbers",r"A two-digit prime cannot end in $2$ or $5$, so only endings $3$ and $7$ need checking. The eligible primes are $23,37,53,$ and $73$."),("Compute probability",r"There are $4+4=8$ prime numbers among $20$ eligible numbers, so the probability is $\frac8{20}=\frac25$."),("Conclude",r"The answer is $\boxed{\frac25}$."),],
12:[("Use the circle inequality",r"A point $(x,-x)$ is inside or on the circle centered at $(5,5)$ with radius $10$ if \[(x-5)^2+(-x-5)^2\le100.\]"),("Simplify",r"This becomes $(x-5)^2+(x+5)^2\le100$, so $2x^2+50\le100$."),("Find integer x",r"Thus $x^2\le25$, so $x$ can be any integer from $-5$ to $5$."),("Count",r"There are $11$ integers in that range."),("Conclude",r"The answer is $\boxed{11}$."),],
13:[("Find the intercepts",r"The line $12x+5y=60$ meets the axes at $(5,0)$ and $(0,12)$, so the triangle has legs $5$ and $12$."),("Recognize the right triangle",r"The hypotenuse is $13$, making this a $5$-$12$-$13$ triangle."),("Use area to find altitudes",r"The altitudes to the two legs are $12$ and $5$. The area is $\frac12\cdot5\cdot12=30$, so the altitude to the hypotenuse is $\frac{2\cdot30}{13}=\frac{60}{13}$."),("Add the altitudes",r"The sum is $12+5+\frac{60}{13}=17+\frac{60}{13}=\frac{281}{13}$."),("Conclude",r"The answer is $\boxed{\frac{281}{13}}$."),],
14:[("Use the sum of roots",r"Expand the equation: \[(x-a)(x-b)+(x-b)(x-c)=0.\] The coefficient of $x$ is $-(a+2b+c)$ and the coefficient of $x^2$ is $2$."),("Apply Vieta's formula",r"The sum of the roots is \[\frac{a+2b+c}{2}.\]"),("Maximize the weighted digit sum",r"Because $b$ has weight $2$, choose the largest digit for $b$. Take $b=9$, and then take $a$ and $c$ as $8$ and $7$."),("Compute",r"The maximum sum of roots is \[\frac{8+2\cdot9+7}{2}=\frac{33}{2}=16.5.\]"),("Conclude",r"The answer is $\boxed{16.5}$."),],
15:[("Translate each ratio",r"Let the number of horses be $h$ and cows be $c$. Then people number $3h$, ducks number $3(3h)=9h$, and sheep number $4c$."),("Write the total",r"The total population is \[h+3h+9h+c+4c=13h+5c.\]"),("Test the choices",r"We need to know which choice cannot be written as $13h+5c$ with nonnegative integers $h,c$."),("Find the impossible value",r"$41=13\cdot2+5\cdot3$, $59=13\cdot3+5\cdot4$, $61=13\cdot2+5\cdot7$, and $66=13\cdot2+5\cdot8$. But $47$ has no such representation."),("Conclude",r"The impossible total is $\boxed{47}$."),],
16:[("Count total assignments",r"Al, Bill, and Cal receive distinct numbers from $1$ to $10$, so there are $10\cdot9\cdot8=720$ ordered assignments."),("Interpret the divisibility chain",r"We need Cal's number to divide Bill's number and Bill's number to divide Al's number, with all three numbers distinct."),("Count by Bill's number",r"If Bill has $2$, there are $4$ choices for Al and $1$ for Cal. For Bill $3$, there are $2$ choices. For Bill $4$, there are $2$ choices. For Bill $5$, there is $1$ choice. Larger Bill values give no possible larger multiple for Al up to $10$."),("Add favorable assignments",r"The favorable count is $4+2+2+1=9$."),("Compute probability",r"The probability is $\frac9{720}=\frac1{80}$."),("Conclude",r"The answer is $\boxed{\frac1{80}}$."),],
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
    if n in {10,17} and notes == "题面包含图形":
        notes = ""
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in set() else notes
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
        if r["year"] == "2015" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2015 AMC 10B Answer Key\n\n"
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












































