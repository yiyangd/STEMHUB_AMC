import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 91
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2016_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2016 AMC 10A Problems 1-10"
NEXT_START = "2016 AMC 10A Problem 11"

ANS={1:("B","100"),2:("C","3"),3:("C","$87.50"),4:("B",r"-\frac1{40}"),5:("D","96"),6:("D","103"),7:("D","90"),8:("C","35"),9:("D","9"),10:("B","2")}

OV={
1:(r"What is the value of $\frac{11!-10!}{9!}$?",[("A","99"),("B","100"),("C","110"),("D","121"),("E","132")]),
2:(r"For what value of $x$ does $10^x\cdot100^{2x}=1000^5$?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
3:(r"For every dollar Ben spent on bagels, David spent $25$ cents less. Ben paid $\$12.50$ more than David. How much did they spend in the bagel store together?",[("A","$37.50"),("B","$50.00"),("C","$87.50"),("D","$90.00"),("E","$92.50")]),
4:(r"The remainder can be defined for all real numbers $x$ and $y$ with $y\ne0$ by $\operatorname{rem}(x,y)=x-y\left\lfloor\frac{x}{y}\right\rfloor$. What is $\operatorname{rem}\left(\frac38,-\frac25\right)$?",[("A",r"-\frac38"),("B",r"-\frac1{40}"),("C","0"),("D",r"\frac38"),("E",r"\frac{31}{40}")]),
5:(r"A rectangular box has integer side lengths in the ratio $1:3:4$. Which of the following could be the volume of the box?",[("A","48"),("B","56"),("C","64"),("D","96"),("E","144")]),
6:(r"Ximena lists the whole numbers $1$ through $30$ once. Emilio copies Ximena's numbers, replacing each occurrence of the digit $2$ by the digit $1$. Ximena adds her numbers and Emilio adds his numbers. How much larger is Ximena's sum than Emilio's?",[("A","13"),("B","26"),("C","102"),("D","103"),("E","110")]),
7:(r"The mean, median, and mode of the $7$ data values $60,100,x,40,50,200,90$ are all equal to $x$. What is the value of $x$?",[("A","50"),("B","60"),("C","75"),("D","90"),("E","100")]),
8:(r"Trickster Rabbit agrees with Foolish Fox to double Fox's money every time Fox crosses the bridge by Rabbit's house, as long as Fox pays $40$ coins in toll to Rabbit after each crossing. The payment is made after the doubling. Fox discovers that all his money is gone after crossing the bridge three times. How many coins did Fox have at the beginning?",[("A","20"),("B","30"),("C","35"),("D","40"),("E","45")]),
9:(r"A triangular array of $2016$ coins has $1$ coin in the first row, $2$ coins in the second row, $3$ coins in the third row, and so on up to $N$ coins in the $N$th row. What is the sum of the digits of $N$?",[("A","6"),("B","7"),("C","8"),("D","9"),("E","10")]),
10:(r"A rug is made with three different colors. The areas of the three differently colored rectangular regions form an arithmetic progression. The inner rectangle is $1$ foot wide, and each of the two surrounding shaded regions is $1$ foot wide on all four sides. What is the length in feet of the inner rectangle?",[("A","1"),("B","2"),("C","4"),("D","6"),("E","8")]),
}

KEY_OVERRIDES={1:"Factor common factorial terms.",2:"Rewrite all bases as powers of 10.",3:"Use the per-dollar difference to scale the total.",4:"Apply the floor-based remainder definition carefully for a negative divisor.",5:"Use the side-length ratio to express volume.",6:"Count digit replacements by place value.",7:"Use the mean equation, then verify median and mode.",8:"Work backward through the repeated doubling-and-toll operation.",9:"Solve a triangular-number equation.",10:"Write the three rectangular region areas in terms of the inner length."}

SOL={
1:[("Factor out 9 factorial",r"Both $11!$ and $10!$ contain a factor of $9!$. So \[\frac{11!-10!}{9!}=\frac{9!(11\cdot10)-9!(10)}{9!}.\]"),("Simplify",r"Cancel $9!$ to get $110-10=100$."),("Check the scale",r"The expression compares two large factorials, but dividing by $9!$ leaves only the next multiplication factors. A two- or three-digit answer is therefore reasonable."),("Conclude",r"The answer is $\boxed{100}$."),],
2:[("Rewrite bases",r"Use $100=10^2$ and $1000=10^3$. Then \[10^x\cdot100^{2x}=10^x\cdot(10^2)^{2x}=10^{5x}.\]"),("Rewrite the right side",r"$1000^5=(10^3)^5=10^{15}$."),("Compare exponents",r"Thus $5x=15$, so $x=3$."),("Conclude",r"The answer is $\boxed{3}$."),],
3:[("Understand the per-dollar comparison",r"For every dollar Ben spent, David spent $25$ cents less, or $\$0.75$. So David spent $75\%$ as much as Ben."),("Use the difference",r"The difference between their spending is $25\%$ of Ben's spending. This difference is $\$12.50$."),("Find Ben and David's amounts",r"Ben spent $\$12.50/0.25=\$50.00$. David spent $\$37.50$."),("Add",r"Together they spent $\$50.00+\$37.50=\$87.50$."),("Conclude",r"The answer is $\boxed{\$87.50}$."),],
4:[("Apply the definition",r"Here $x=\frac38$ and $y=-\frac25$. First compute \[\frac{x}{y}=\frac{3/8}{-2/5}=-\frac{15}{16}.\]"),("Take the floor",r"The greatest integer less than or equal to $-\frac{15}{16}$ is $-1$."),("Substitute",r"\[\operatorname{rem}\left(\frac38,-\frac25\right)=\frac38-\left(-\frac25\right)(-1)=\frac38-\frac25.\]"),("Simplify",r"\[\frac38-\frac25=\frac{15-16}{40}=-\frac1{40}.\]"),("Conclude",r"The answer is $\boxed{-\frac1{40}}$."),],
5:[("Use the ratio",r"Let the integer side lengths be $s$, $3s$, and $4s$."),("Find the volume form",r"The volume is $s\cdot3s\cdot4s=12s^3$."),("Test the choices",r"We need a choice of the form $12s^3$. When $s=2$, the volume is $12\cdot8=96$."),("Conclude",r"The possible volume is $\boxed{96}$."),],
6:[("Separate units and tens changes",r"Changing a digit $2$ to $1$ lowers a number by $1$ if the digit is in the units place, and by $10$ if the digit is in the tens place."),("Count units-place changes",r"The units digit is $2$ in $2,12,22$, giving a total decrease of $3$."),("Count tens-place changes",r"The tens digit is $2$ in $20,21,\ldots,29$, giving a total decrease of $10\cdot10=100$."),("Add the decreases",r"Emilio's sum is $3+100=103$ less than Ximena's sum."),("Conclude",r"Ximena's sum is $\boxed{103}$ larger."),],
7:[("Use the mean condition",r"The sum of the seven values is $60+100+x+40+50+200+90=540+x$."),("Set mean equal to x",r"\[\frac{540+x}{7}=x.\] Thus $540+x=7x$, so $x=90$."),("Verify median and mode",r"With $x=90$, the ordered list is $40,50,60,90,90,100,200$. The median is $90$, and the mode is also $90$."),("Conclude",r"The answer is $\boxed{90}$."),],
8:[("Work backward",r"After each crossing, Fox's money is doubled and then $40$ coins are paid. After the third crossing he has $0$."),("Before the third crossing",r"If he had $M$ before the third crossing, then $2M-40=0$, so $M=20$."),("Before the second and first crossings",r"Before the second crossing, $2M-40=20$, so $M=30$. Before the first crossing, $2M-40=30$, so $M=35$."),("Conclude",r"Fox began with $\boxed{35}$ coins."),],
9:[("Use the triangular number formula",r"The total number of coins is \[1+2+\cdots+N=\frac{N(N+1)}2.\]"),("Set equal to 2016",r"We need $\frac{N(N+1)}2=2016$, or $N(N+1)=4032$."),("Find N",r"Since $63\cdot64=4032$, we have $N=63$."),("Sum digits",r"The sum of the digits of $63$ is $6+3=9$."),("Conclude",r"The answer is $\boxed{9}$."),],
10:[("Name the inner length",r"Let the inner rectangle have length $x$ and width $1$, so its area is $x$."),("Compute the middle region",r"The first surrounding strip makes dimensions $(x+2)$ by $3$. Its area alone is $3(x+2)-x=2x+6$."),("Compute the outer region",r"The second surrounding strip makes dimensions $(x+4)$ by $5$. Its area alone is $5(x+4)-3(x+2)=2x+14$."),("Use arithmetic progression",r"The three areas $x$, $2x+6$, and $2x+14$ form an arithmetic progression, so \[(2x+6)-x=(2x+14)-(2x+6).\]"),("Solve",r"This gives $x+6=8$, so $x=2$."),("Conclude",r"The inner rectangle has length $\boxed{2}$ feet."),],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in {10} else notes
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
        if r["year"] == "2016" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2016 AMC 10A Answer Key\n\n"
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












































