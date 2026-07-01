import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 74
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2013_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2013 AMC 10B Problems 1-10"
NEXT_START = "2013 AMC 10B Problem 11"

ANS={1:("C",r"\frac{7}{12}"),2:("A","600"),3:("C",r"-5"),4:("D","149"),5:("B",r"-15"),6:("C","24.75"),7:("B",r"\frac{\sqrt3}{2}"),8:("B","16"),9:("D","160"),10:("C","20")}

OV={
1:(r"What is $\frac{2+4+6}{1+3+5}-\frac{1+3+5}{2+4+6}$?",[("A",r"-\frac1{36}"),("B",r"\frac5{12}"),("C",r"\frac7{12}"),("D",r"\frac{49}{20}"),("E",r"\frac{43}{3}")]),
2:(r"Mr. Green measures his rectangular garden as $15$ steps by $20$ steps. Each step is $2$ feet long. He expects half a pound of potatoes per square foot. How many pounds of potatoes does he expect?",[("A","600"),("B","800"),("C","1000"),("D","1200"),("E","1400")]),
3:(r"On a January day, the high temperature was $16$ degrees higher than the low temperature, and the average of the high and low temperatures was $3^\circ$. What was the low temperature?",[("A",r"-13"),("B",r"-8"),("C",r"-5"),("D","3"),("E","11")]),
4:(r"When counting from $3$ to $201$, $53$ is the $51$st number counted. When counting backwards from $201$ to $3$, $53$ is the $n$th number counted. What is $n$?",[("A","146"),("B","147"),("C","148"),("D","149"),("E","150")]),
5:(r"Positive integers $a$ and $b$ are each less than $6$. What is the smallest possible value of $2a-ab$?",[("A",r"-20"),("B",r"-15"),("C",r"-10"),("D","0"),("E","2")]),
6:(r"The average age of $33$ fifth-graders is $11$. The average age of $55$ of their parents is $33$. What is the average age of all these parents and fifth-graders?",[("A","22"),("B","23.25"),("C","24.75"),("D","26.25"),("E","28")]),
7:(r"Six points are equally spaced around a circle of radius $1$. Three of these points are vertices of a triangle that is neither equilateral nor isosceles. What is the area of this triangle?",[("A",r"\frac{\sqrt3}{3}"),("B",r"\frac{\sqrt3}{2}"),("C","1"),("D",r"\sqrt2"),("E",r"2\sqrt3")]),
8:(r"Ray's car averages $40$ miles per gallon, and Tom's car averages $10$ miles per gallon. Ray and Tom each drive the same number of miles. What is the cars' combined rate in miles per gallon?",[("A","10"),("B","16"),("C","25"),("D","30"),("E","40")]),
9:(r"Three positive integers are each greater than $1$, have product $27000$, and are pairwise relatively prime. What is their sum?",[("A","100"),("B","137"),("C","156"),("D","160"),("E","165")]),
10:(r"A basketball team's players were successful on $50\%$ of their two-point shots and $40\%$ of their three-point shots, resulting in $54$ points. They attempted $50\%$ more two-point shots than three-point shots. How many three-point shots did they attempt?",[("A","10"),("B","15"),("C","20"),("D","25"),("E","30")]),
}

KEY_OVERRIDES={1:"Compute the two sums first, then subtract fractions.",2:"Convert steps to feet before computing area and yield.",3:"Use average and difference to recover the two temperatures.",4:"Counting backward changes the position to a distance from 201.",5:"Factor the expression and maximize the negative factor.",6:"Use a weighted average by group size.",7:"The only scalene triangle from three vertices of a regular hexagon has side lengths $1,\sqrt3,2$.",8:"For equal distances, add gallons used and divide total miles by total gallons.",9:"Pairwise relatively prime factors must receive whole prime-power blocks.",10:"Use variables for shot attempts and expected made-shot points."}

SOL={
1:[("Compute sums",r"The even sum is $2+4+6=12$, and the odd sum is $1+3+5=9$."),("Substitute",r"The expression becomes $\frac{12}{9}-\frac{9}{12}=\frac43-\frac34$."),("Use a common denominator",r"With denominator $12$, this is $\frac{16}{12}-\frac9{12}=\frac7{12}$."),("Conclude",r"The answer is $\boxed{\frac7{12}}$."),],
2:[("Convert dimensions",r"Each step is $2$ feet, so the garden is $30$ feet by $40$ feet."),("Find area",r"The area is $30\cdot40=1200$ square feet."),("Apply yield",r"At half a pound per square foot, the expected yield is $1200\cdot\frac12=600$ pounds."),("Conclude",r"The answer is $\boxed{600}$."),],
3:[("Name the low temperature",r"Let the low temperature be $L$. Then the high temperature is $L+16$."),("Use the average",r"Their average is $3$, so $\frac{L+(L+16)}{2}=3$."),("Solve",r"This gives $2L+16=6$, so $2L=-10$ and $L=-5$."),("Conclude",r"The low temperature was $\boxed{-5^\circ}$."),],
4:[("Count backward directly",r"When counting backward from $201$, the first number is $201$, the second is $200$, and so on."),("Use the position formula",r"The position of $53$ is $201-53+1$. The $+1$ is important because both endpoints are included."),("Compute",r"We get $201-53+1=149$."),("Conclude",r"Thus $n=\boxed{149}$."),],
5:[("Factor the expression",r"The expression is $2a-ab=a(2-b)$. Since $a$ is positive, to make the value as small as possible we want $a$ large and $2-b$ as negative as possible."),("Choose b",r"The largest possible $b$ less than $6$ is $5$, giving $2-b=-3$."),("Choose a",r"The largest possible $a$ is also $5$, so the smallest value is $5(2-5)=-15$."),("Conclude",r"The answer is $\boxed{-15}$."),],
6:[("Find total ages",r"The $33$ fifth-graders have total age $33\cdot11=363$. The $55$ parents have total age $55\cdot33=1815$."),("Add people and ages",r"Together there are $33+55=88$ people and total age $363+1815=2178$."),("Compute weighted average",r"The average is $2178/88=24.75$."),("Conclude",r"The answer is $\boxed{24.75}$."),],
7:[("Understand the possible triangle",r"Six equally spaced points form a regular hexagon. A triangle that is neither equilateral nor isosceles must use gaps of $1$, $2$, and $3$ steps around the hexagon."),("Find side lengths",r"These correspond to chord lengths $1$, $\sqrt3$, and $2$ in a unit circle."),("Recognize the triangle",r"A triangle with sides $1$, $\sqrt3$, and $2$ is a $30$-$60$-$90$ right triangle."),("Compute area",r"Its area is $\frac12\cdot1\cdot\sqrt3=\frac{\sqrt3}{2}$. The answer is $\boxed{\frac{\sqrt3}{2}}$."),],
8:[("Use a common distance",r"Suppose each person drives $40$ miles. Ray uses $1$ gallon, while Tom uses $4$ gallons."),("Combine miles and gallons",r"Together they drive $80$ miles and use $5$ gallons."),("Compute rate",r"The combined rate is $80/5=16$ miles per gallon."),("Conclude",r"The answer is $\boxed{16}$."),],
9:[("Factor the product",r"We have $27000=27\cdot1000=3^3\cdot2^3\cdot5^3$."),("Use pairwise relative primality",r"Since the three integers are pairwise relatively prime, powers of the same prime cannot be split between different integers. Each prime-power block must go entirely into one of the three numbers."),("Assign the blocks",r"The three numbers greater than $1$ must therefore be $2^3=8$, $3^3=27$, and $5^3=125$ in some order."),("Add",r"Their sum is $8+27+125=160$. The answer is $\boxed{160}$."),],
10:[("Name the attempts",r"Let the number of three-point attempts be $x$. Then the number of two-point attempts is $1.5x$."),("Compute expected successful points",r"The three-point shots produce $0.40x$ makes, worth $3(0.40x)=1.2x$ points. The two-point shots produce $0.50(1.5x)$ makes, worth $2\cdot0.50\cdot1.5x=1.5x$ points."),("Use total points",r"The total is $1.2x+1.5x=2.7x=54$."),("Solve",r"Thus $x=20$. The answer is $\boxed{20}$."),],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {16,17}) else notes
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
        if r["year"] == "2013" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2013 AMC 10B Answer Key\n\n"
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










































