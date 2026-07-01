import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 100
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2017_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2017 AMC 10B Problems 1-10"
NEXT_START = "2017 AMC 10B Problem 11"

ANS={1:("B","12"),2:("C","7 minutes and 5 seconds"),3:("E",r"y+z"),4:("D","2"),5:("D","40"),6:("B","4"),7:("C","2.8"),8:("C","(-4,9)"),9:("D",r"\frac7{27}"),10:("E","13")}

OV={
1:(r"Mary thought of a positive two-digit number. She multiplied it by $3$ and added $11$. Then she switched the digits of the result, obtaining a number between $71$ and $75$, inclusive. What was Mary's number?",[("A","11"),("B","12"),("C","13"),("D","14"),("E","15")]),
2:(r"Sofia ran $5$ laps around the $400$-meter track at her school. For each lap, she ran the first $100$ meters at an average speed of $4$ meters per second and the remaining $300$ meters at an average speed of $5$ meters per second. How much time did Sofia take running the $5$ laps?",[("A","5 minutes and 35 seconds"),("B","6 minutes and 40 seconds"),("C","7 minutes and 5 seconds"),("D","7 minutes and 25 seconds"),("E","8 minutes and 10 seconds")]),
3:(r"Real numbers $x$, $y$, and $z$ satisfy $0<x<1$, $-1<y<0$, and $1<z<2$. Which of the following numbers is necessarily positive?",[("A",r"$y+x^2$"),("B",r"$y+xz$"),("C",r"$y+y^2$"),("D",r"$y+2y^2$"),("E",r"$y+z$")]),
4:(r"Suppose that $x$ and $y$ are nonzero real numbers such that $\frac{3x+y}{x-3y}=-2$. What is the value of $\frac{x+3y}{3x-y}$?",[("A","-3"),("B","-1"),("C","1"),("D","2"),("E","3")]),
5:(r"Camilla had twice as many blueberry jelly beans as cherry jelly beans. After eating $10$ pieces of each kind, she now has three times as many blueberry jelly beans as cherry jelly beans. How many blueberry jelly beans did she originally have?",[("A","10"),("B","20"),("C","30"),("D","40"),("E","50")]),
6:(r"What is the largest number of solid $2$-in by $2$-in by $1$-in blocks that can fit in a $3$-in by $2$-in by $3$-in box?",[("A","3"),("B","4"),("C","5"),("D","6"),("E","7")]),
7:(r"Samia set off on her bicycle to visit her friend, traveling at an average speed of $17$ kilometers per hour. When she had gone half the distance to her friend's house, a tire went flat, and she walked the rest of the way at $5$ kilometers per hour. In all it took her $44$ minutes to reach her friend's house. In kilometers rounded to the nearest tenth, how far did Samia walk?",[("A","2.0"),("B","2.2"),("C","2.8"),("D","3.4"),("E","4.4")]),
8:(r"Points $A(11,9)$ and $B(2,-3)$ are vertices of $\triangle ABC$ with $AB=AC$. The altitude from $A$ meets the opposite side at $D(-1,3)$. What are the coordinates of point $C$?",[("A","(-8,9)"),("B","(-4,8)"),("C","(-4,9)"),("D","(-2,3)"),("E","(-1,0)")]),
9:(r"A radio program has a quiz consisting of $3$ multiple-choice questions, each with $3$ choices. A contestant wins if he or she gets $2$ or more of the questions right. The contestant answers randomly to each question. What is the probability of winning?",[("A",r"$\frac1{27}$"),("B",r"$\frac19$"),("C",r"$\frac29$"),("D",r"$\frac7{27}$"),("E",r"$\frac12$")]),
10:(r"The lines with equations $ax-2y=c$ and $2x+by=-c$ are perpendicular and intersect at $(1,-5)$. What is $c$?",[("A","-13"),("B","-8"),("C","2"),("D","8"),("E","13")]),
}

KEY_OVERRIDES={1:"Reverse the digit switch and arithmetic operations.",2:"Add times, not speeds, across each lap.",3:"Use interval bounds to determine guaranteed signs.",4:"Solve the given rational equation for the ratio x:y.",5:"Set up a linear equation from before-and-after ratios.",6:"Use volume as an upper bound, then show the packing is possible.",7:"Use distance over speed on two equal halves.",8:"Use the fact that the altitude in an isosceles triangle is also a median.",9:"Use binomial counting for exactly two or three correct answers.",10:"Use perpendicular slopes and the given intersection point."}

SOL={
1:[("Reverse the digit switch",r"After Mary switched the digits, the result was between $71$ and $75$. Before switching, the number must have been one of $17,27,37,47,57$."),("Undo the addition",r"Before adding $11$, the number was one of \[6,16,26,36,46.\]"),("Undo the multiplication by 3",r"This number must be divisible by $3$, because it came from multiplying Mary's original number by $3$. The only value in the list divisible by $3$ is $36$."),("Find Mary's number",r"Thus Mary's original number was \[36\div3=12.\]"),("Conclude",r"The answer is $\boxed{12}$."),],
2:[("Compute one lap carefully",r"For each lap, Sofia runs $100$ meters at $4$ m/s, which takes $25$ seconds. Then she runs $300$ meters at $5$ m/s, which takes $60$ seconds."),("Add time per lap",r"One lap takes \[25+60=85\] seconds."),("Multiply by 5 laps",r"Five laps take \[5\cdot85=425\] seconds."),("Convert to minutes",r"Since $420$ seconds is $7$ minutes, $425$ seconds is $7$ minutes and $5$ seconds."),("Conclude",r"The answer is $\boxed{\text{7 minutes and 5 seconds}}$."),],
3:[("Use the guaranteed intervals",r"We know $y$ is negative and between $-1$ and $0$, while $z$ is greater than $1$."),("Test the likely positive expression",r"For choice E, \[y+z> -1+1=0.\] Since both inequalities are strict, $y+z$ is necessarily positive."),("See why the others can fail",r"The other choices involve adding $y$ to quantities that can be very small. For example, $x^2$, $xz$, $y^2$, and $2y^2$ can all be too small to overcome a negative $y$."),("Conclude",r"The only necessarily positive expression is $\boxed{y+z}$."),],
4:[("Clear the fraction",r"The equation is \[\frac{3x+y}{x-3y}=-2.\] Multiply both sides by $x-3y$ to get \[3x+y=-2x+6y.\]"),("Solve for the ratio",r"Rearranging gives \[5x=5y,\] so $x=y$."),("Substitute into the target",r"Then \[\frac{x+3y}{3x-y}=\frac{x+3x}{3x-x}=\frac{4x}{2x}=2.\]"),("Check nonzero condition",r"Because $x$ and $y$ are nonzero, dividing by $x$ is valid."),("Conclude",r"The answer is $\boxed{2}$."),],
5:[("Set up original amounts",r"Let Camilla originally have $c$ cherry jelly beans. Then she originally had $2c$ blueberry jelly beans."),("Translate the after-eating condition",r"After eating $10$ of each kind, she has $2c-10$ blueberry and $c-10$ cherry jelly beans. The new ratio is $3:1$, so \[2c-10=3(c-10).\]"),("Solve",r"This gives $2c-10=3c-30$, so $c=20$."),("Answer the requested amount",r"She originally had $2c=40$ blueberry jelly beans."),("Conclude",r"The answer is $\boxed{40}$."),],
6:[("Use volume as an upper bound",r"The box has volume $3\cdot2\cdot3=18$ cubic inches. Each block has volume $2\cdot2\cdot1=4$ cubic inches. So at most $\lfloor18/4\rfloor=4$ blocks can fit."),("Show that 4 is possible",r"Orient each block so its $2$-inch thickness matches the box's $2$-inch dimension. Then each block has a $2$ by $1$ footprint in the $3$ by $3$ base."),("Pack the base",r"A $3$ by $3$ rectangle can hold four $2$ by $1$ footprints, leaving one $1$ by $1$ square unused."),("Conclude",r"The largest possible number is $\boxed{4}$."),],
7:[("Let the walking distance be d",r"Samia biked half the distance and walked the other half. Let the walking distance be $d$ kilometers. Then she also biked $d$ kilometers."),("Write the total time",r"Her biking time was $\frac{d}{17}$ hours and her walking time was $\frac{d}{5}$ hours. The total was $44$ minutes, or $\frac{11}{15}$ hours."),("Solve for d",r"\[\frac{d}{17}+\frac{d}{5}=\frac{11}{15}.\] The left side is $d\cdot\frac{22}{85}$, so \[d=\frac{11}{15}\cdot\frac{85}{22}=\frac{17}{6}\approx2.833.\]"),("Round",r"Rounded to the nearest tenth, this is $2.8$ kilometers."),("Conclude",r"The answer is $\boxed{2.8}$."),],
8:[("Use the isosceles triangle property",r"Since $AB=AC$, point $A$ is the apex of an isosceles triangle. The altitude from $A$ to $BC$ is also the median of $BC$."),("Use D as the midpoint",r"Therefore $D(-1,3)$ is the midpoint of segment $BC$."),("Solve for C",r"If $B=(2,-3)$ and $C=(u,v)$, then \[\left(\frac{2+u}{2},\frac{-3+v}{2}\right)=(-1,3).\]"),("Compute coordinates",r"From $\frac{2+u}{2}=-1$, we get $u=-4$. From $\frac{-3+v}{2}=3$, we get $v=9$."),("Conclude",r"Point $C$ is $\boxed{(-4,9)}$."),],
9:[("Identify success cases",r"The contestant wins by getting exactly $2$ questions right or exactly $3$ questions right."),("Find single-question probabilities",r"Each question has probability $\frac13$ of being correct and $\frac23$ of being wrong."),("Count exactly two correct",r"There are $\binom32=3$ ways to choose which two questions are correct, so the probability is \[3\left(\frac13\right)^2\left(\frac23\right)=\frac{6}{27}.\]"),("Count exactly three correct",r"The probability of all three correct is \[\left(\frac13\right)^3=\frac1{27}.\]"),("Add",r"The winning probability is \[\frac6{27}+\frac1{27}=\frac7{27}.\]"),("Conclude",r"The answer is $\boxed{\frac7{27}}$."),],
10:[("Use perpendicular slopes",r"The line $ax-2y=c$ has slope $\frac a2$. The line $2x+by=-c$ has slope $-\frac2b$."),("Set product of slopes",r"Perpendicular lines have slopes with product $-1$, so \[\frac a2\cdot\left(-\frac2b\right)=-1.\] This gives $a=b$."),("Use the intersection point in both equations",r"Plug $(1,-5)$ into the first equation: \[a+10=c.\] Plug it into the second equation: \[2-5a=-c.\]"),("Solve",r"Using $c=a+10$ in the second equation gives \[2-5a=-(a+10),\] so $a=3$."),("Find c",r"Then $c=a+10=13$."),("Conclude",r"The answer is $\boxed{13}$."),],
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
        if r["year"] == "2017" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2017 AMC 10B Answer Key\n\n"
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












































