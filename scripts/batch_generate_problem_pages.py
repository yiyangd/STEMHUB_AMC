import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 76
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2013_AMC_10B_Answer_Key"
TARGET_NUMBERS = {16,17,18,19,20}
SKIPPED = []
BATCH_LABEL = "2013 AMC 10B Problems 16-20"
NEXT_START = "2013 AMC 10B Problem 21"

ANS={16:("B","13.5"),17:("E","103"),18:("D","46"),19:("D",r"-2+\sqrt3"),20:("B","2")}

OV={
16:(r"In $\triangle ABC$, medians $AD$ and $CE$ intersect at $P$. Given $PE=1.5$, $PD=2$, and $DE=2.5$, what is the area of quadrilateral $AEDC$?",[("A","13"),("B","13.5"),("C","14"),("D","14.5"),("E","15")]),
17:(r"Alex has $75$ red tokens and $75$ blue tokens. At one booth he can give two red tokens and receive a silver token and a blue token. At another booth he can give three blue tokens and receive a silver token and a red token. Alex continues until no more exchanges are possible. How many silver tokens will he have?",[("A","62"),("B","82"),("C","83"),("D","102"),("E","103")]),
18:(r"The number $2013$ has the property that its units digit is the sum of its other digits: $2+0+1=3$. How many integers less than $2013$ but greater than $1000$ share this property?",[("A","33"),("B","34"),("C","45"),("D","46"),("E","58")]),
19:(r"The real numbers $c,b,a$ form an arithmetic sequence with $a\ge b\ge c\ge0$. The quadratic $ax^2+bx+c$ has exactly one root. What is this root?",[("A",r"-7-4\sqrt3"),("B",r"-2-\sqrt3"),("C",r"-1"),("D",r"-2+\sqrt3"),("E",r"-7+4\sqrt3")]),
20:(r"The number $2013$ is expressed as $2013=\frac{a_1!a_2!\cdots a_m!}{b_1!b_2!\cdots b_n!}$, where $a_1\ge a_2\ge\cdots\ge a_m$ and $b_1\ge b_2\ge\cdots\ge b_n$ are positive integers and $a_1+b_1$ is as small as possible. What is $|a_1-b_1|$?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
}

KEY_OVERRIDES={16:"Use centroid ratios and the area ratio between triangle PDE and triangle ABC.",17:"Track how many times each exchange is used and identify the only reachable terminal state.",18:"Count four-digit numbers whose unit digit is the sum of the first three digits.",19:"Use the arithmetic-sequence condition and discriminant zero.",20:"Use the prime factor 61 to force large factorials, then construct the minimum."}

SOL={
16:[("Use centroid ratios",r"Since $AD$ and $CE$ are medians, their intersection $P$ is the centroid. A centroid divides each median in a $2:1$ ratio, so $AD=3\cdot PD=6$ and $CE=3\cdot PE=4.5$."),("Look at triangle PDE",r"The sides of $\triangle PDE$ are $1.5$, $2$, and $2.5$, so it is a right triangle. Its area is $\frac12\cdot1.5\cdot2=1.5$."),("Relate this to triangle ABC",r"In any triangle, the triangle formed by the centroid and two side midpoints has area $\frac1{12}$ of the whole triangle. Thus $[ABC]=12\cdot1.5=18$."),("Find the requested quadrilateral",r"Since $D$ and $E$ are midpoints, triangle $BDE$ is similar to $BAC$ with scale factor $\frac12$, so $[BDE]=\frac14[ABC]$. Therefore $[AEDC]=\frac34[ABC]=\frac34\cdot18=13.5$."),("Conclude",r"The answer is $\boxed{13.5}$."),],
17:[("Count exchanges",r"Let $x$ be the number of red-token exchanges and $y$ the number of blue-token exchanges. Then the final red count is $75-2x+y$, and the final blue count is $75+x-3y$."),("Use the stopping condition",r"When no exchange is possible, the final red count is less than $2$ and the final blue count is less than $3$. Solving these integer conditions gives two algebraic candidates: $(R,B,x,y)=(1,2,59,44)$ or $(0,0,60,45)$."),("Remove the unreachable candidate",r"The state $(0,0)$ cannot be reached by a final legal move: the previous state would have to be $(2,-1)$ or $(-1,3)$, both impossible. Thus the reachable terminal state is $(1,2)$."),("Count silver tokens",r"In that state, the number of silver tokens is $x+y=59+44=103$."),("Conclude",r"The answer is $\boxed{103}$."),],
18:[("Separate by thousands digit",r"A number between $1000$ and $2013$ has thousands digit $1$ or $2$. Write it as $abcd$, where the condition is $d=a+b+c$."),("Count numbers starting with 1",r"If $a=1$, then $d=1+b+c$ must be a digit, so $b+c\le8$. The number of nonnegative pairs $(b,c)$ with sum at most $8$ is $\binom{10}{2}=45$."),("Count numbers starting with 2",r"If $a=2$ and the number is less than $2013$, then only $2002$ works. The next possible case $2013$ is not less than $2013$."),("Add",r"The total is $45+1=46$. The answer is $\boxed{46}$."),],
19:[("Use the arithmetic sequence",r"Since $c,b,a$ form an arithmetic sequence, write $a=b+d$ and $c=b-d$, where $d\ge0$."),("Use the one-root condition",r"A quadratic has exactly one real root when its discriminant is zero, so $b^2-4ac=0$."),("Substitute",r"This gives $b^2=4(b+d)(b-d)=4(b^2-d^2)$, so $3b^2=4d^2$. Hence $\frac db=\frac{\sqrt3}{2}$."),("Find the root",r"The repeated root is $x=-\frac{b}{2a}=-\frac{b}{2(b+d)}=-\frac{1}{2(1+d/b)}=-\frac{1}{2+\sqrt3}$."),("Simplify",r"Rationalizing gives $x=\sqrt3-2=-2+\sqrt3$. The answer is $\boxed{-2+\sqrt3}$."),],
20:[("Use the large prime",r"Since $2013=3\cdot11\cdot61$, any factorial expression must introduce the prime $61$ in the numerator. Thus $a_1\ge61$."),("Try to keep the largest denominator small",r"If $b_1\le58$, then the factor $59$ appearing in $61!$ could not be canceled, so $b_1$ must be at least $59$ when $a_1=61$."),("Construct with a1=61 and b1=59",r"There is a construction: \[2013=\frac{61!\,11!\,3!}{59!\,10!\,5!}.\] Indeed this equals $(60\cdot61)\cdot11\cdot6/120=61\cdot11\cdot3$."),("Show minimality",r"This has $a_1+b_1=61+59=120$. A smaller sum would require $a_1=61$ and $b_1\le58$, which cannot cancel the unwanted factor $59$, or would require $a_1<61$, impossible."),("Conclude",r"Therefore $|a_1-b_1|=|61-59|=2$. The answer is $\boxed{2}$."),],
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {16},
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












































