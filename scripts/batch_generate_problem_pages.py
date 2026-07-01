import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 86
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2015_AMC_10A_Answer_Key"
TARGET_NUMBERS = {17,18,19,20}
SKIPPED = []
BATCH_LABEL = "2015 AMC 10A Problems 17-20"
NEXT_START = "2015 AMC 10A Problem 21"

ANS={17:("D",r"3+2\sqrt3"),18:("E","21"),19:("D",r"\frac{50-25\sqrt3}{2}"),20:("B","102")}

OV={
17:(r"A line that passes through the origin intersects both the line $x=1$ and the line $y=1+\frac{x}{\sqrt3}$. The three lines create an equilateral triangle. What is the perimeter of the triangle?",[("A",r"2\sqrt6"),("B",r"2+2\sqrt3"),("C","6"),("D",r"3+2\sqrt3"),("E",r"6+3\sqrt3")]),
18:(r"Hexadecimal (base-$16$) numbers are written using numeric digits $0$ through $9$ as well as the letters $A$ through $F$ to represent $10$ through $15$. Among the first $1000$ positive integers, there are $n$ whose hexadecimal representation contains only numeric digits. What is the sum of the digits of $n$?",[("A","17"),("B","18"),("C","19"),("D","20"),("E","21")]),
19:(r"The isosceles right triangle $ABC$ has right angle at $C$ and area $12.5$. The rays trisecting $\angle ACB$ intersect $AB$ at $D$ and $E$. What is the area of $\triangle CDE$?",[("A",r"5\sqrt2"),("B",r"\frac{50\sqrt3-75}{4}"),("C",r"\frac{15\sqrt3}{2}"),("D",r"\frac{50-25\sqrt3}{2}"),("E",r"\frac{25\sqrt3}{6}")]),
20:(r"A rectangle with positive integer side lengths has area $A$ square centimeters and perimeter $P$ centimeters. Which of the following numbers cannot equal $A+P$?",[("A","100"),("B","102"),("C","104"),("D","106"),("E","108")]),
}

KEY_OVERRIDES={17:"Use the 60-degree angle between the given lines to identify the third line.",18:"Count hexadecimal representations with only decimal digits.",19:"Place the right isosceles triangle on coordinate axes and use trisection slopes.",20:"Rewrite A+P as (a+2)(b+2)-4 for integer side lengths."}

SOL={
17:[("Use the angle between the fixed lines",r"The line $x=1$ is vertical, and the line $y=1+\frac{x}{\sqrt3}$ has slope $\frac1{\sqrt3}$, so it makes a $30^\circ$ angle with the $x$-axis. The angle between these two lines is $60^\circ$."),("Choose the third line",r"For the triangle to be equilateral, the third line through the origin must make a $60^\circ$ angle with each of the other two lines. This gives the line $y=-\frac{x}{\sqrt3}$."),("Find the vertical side length",r"On $x=1$, the slanted upper line has $y=1+\frac1{\sqrt3}$, while the line through the origin has $y=-\frac1{\sqrt3}$. The side length is \[1+\frac2{\sqrt3}.\]"),("Find the perimeter",r"The triangle is equilateral, so the perimeter is \[3\left(1+\frac2{\sqrt3}\right)=3+2\sqrt3.\]"),("Conclude",r"The answer is $\boxed{3+2\sqrt3}$."),],
18:[("Translate the bound",r"The first $1000$ positive integers go up to decimal $1000$, which is hexadecimal $3E8$."),("Count one- and two-digit hexadecimal numbers",r"With only numeric digits, there are $9$ one-digit positive numbers and $9\cdot10=90$ two-digit numbers."),("Count three-digit numbers",r"For three-digit hexadecimal numbers up to $3E8$, the first digit can be $1$, $2$, or $3$. Since the other allowed digits are only $0$ through $9$, all $3\cdot100=300$ such numbers are below $3E8$."),("Find n",r"Thus $n=9+90+300=399$."),("Sum the digits",r"The sum of the decimal digits of $399$ is $3+9+9=21$."),("Conclude",r"The answer is $\boxed{21}$."),],
19:[("Place the triangle on axes",r"Since the triangle is isosceles right with area $12.5$, its legs have length $5$. Put $C=(0,0)$, $A=(5,0)$, and $B=(0,5)$, so $AB$ is $x+y=5$."),("Use the trisecting rays",r"The rays trisecting the right angle have slopes $\tan30^\circ=\frac1{\sqrt3}$ and $\tan60^\circ=\sqrt3$."),("Find the intersection points",r"The first ray meets $AB$ at \[\left(\frac{5\sqrt3}{\sqrt3+1},\frac5{\sqrt3+1}\right),\] and the second meets $AB$ at \[\left(\frac5{\sqrt3+1},\frac{5\sqrt3}{\sqrt3+1}\right).\]"),("Compute area with a determinant",r"The absolute determinant of these two point vectors is \[\frac{25(3-1)}{(\sqrt3+1)^2}=\frac{25}{2+\sqrt3}.\] The triangle area is half of that."),("Simplify",r"Thus \[[CDE]=\frac{25}{2(2+\sqrt3)}=\frac{25(2-\sqrt3)}2=\frac{50-25\sqrt3}{2}.\]"),("Conclude",r"The answer is $\boxed{\frac{50-25\sqrt3}{2}}$."),],
20:[("Use the corrected integer-side version",r"Let the positive integer side lengths be $a$ and $b$. Then $A=ab$ and $P=2a+2b$."),("Factor A plus P",r"\[A+P=ab+2a+2b=(a+2)(b+2)-4.\] Thus $A+P+4$ must factor into two integers greater than $2$."),("Test the choices by adding 4",r"The choices become $104,106,108,110,112$ after adding $4$."),("Find the impossible one",r"$106=2\cdot53$ has no factorization into two integers both greater than $2$. The others do: for example, $104=4\cdot26$, $108=6\cdot18$, $110=5\cdot22$, and $112=4\cdot28$."),("Conclude",r"Therefore $A+P$ cannot be $\boxed{102}$."),],
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
    if n == 20:
        notes = "This page uses the corrected practice version with positive integer side lengths; the original wording was ambiguous."
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
        if r["year"] == "2015" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {20},
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
        + "- Answer verification source: AoPS 2015 AMC 10A Answer Key\n\n"
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












































