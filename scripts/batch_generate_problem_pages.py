import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 103
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2018_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,10}
SKIPPED = ["2018 AMC 10A Problem 9 skipped: similar-triangle area question depends on the missing diagram subdivision."]
BATCH_LABEL = "2018 AMC 10A Problems 1-8, 10"
NEXT_START = "2018 AMC 10A Problem 11"

ANS={1:("B",r"\frac{11}{7}"),2:("A","Liliane has 20% more soda than Alice."),3:("E","February 12"),4:("E","24"),5:("D","(5,6)"),6:("B","300"),7:("E","9"),8:("C","2"),10:("A","8")}

OV={
1:(r"What is the value of $\left(\left((2+1)^{-1}+1\right)^{-1}+1\right)^{-1}+1$?",[("A",r"$\frac58$"),("B",r"$\frac{11}{7}$"),("C",r"$\frac85$"),("D",r"$\frac{18}{11}$"),("E",r"$\frac{15}{8}$")]),
2:(r"Liliane has $50\%$ more soda than Jacqueline, and Alice has $25\%$ more soda than Jacqueline. What is the relationship between the amounts of soda that Liliane and Alice have?",[("A","Liliane has 20% more soda than Alice."),("B","Liliane has 25% more soda than Alice."),("C","Liliane has 45% more soda than Alice."),("D","Liliane has 75% more soda than Alice."),("E","Liliane has 100% more soda than Alice.")]),
3:(r"A unit of blood expires after $10!=10\cdot9\cdot8\cdots1$ seconds. Yasin donates a unit of blood at noon on January $1$. On what day does his unit of blood expire?",[("A","January 2"),("B","January 12"),("C","January 22"),("D","February 11"),("E","February 12")]),
4:(r"How many ways can a student schedule $3$ mathematics courses, algebra, geometry, and number theory, in a $6$-period day if no two mathematics courses can be taken in consecutive periods?",[("A","3"),("B","6"),("C","12"),("D","18"),("E","24")]),
5:(r"Alice, Bob, and Charlie were on a hike and were wondering how far away the nearest town was. Alice said, 'We are at least $6$ miles away.' Bob replied, 'We are at most $5$ miles away.' Charlie remarked, 'The nearest town is at most $4$ miles away.' It turned out that none of the three statements was true. Let $d$ be the distance in miles to the nearest town. Which interval is the set of all possible values of $d$?",[("A","(0,4)"),("B","(4,5)"),("C","(4,6)"),("D","(5,6)"),("E",r"$(5,\infty)$")]),
6:(r"Sangho uploaded a video to a website where viewers can vote that they like or dislike a video. Each video begins with score $0$, and the score increases by $1$ for each like vote and decreases by $1$ for each dislike vote. At one point his video had score $90$, and $65\%$ of the votes were like votes. How many votes had been cast?",[("A","200"),("B","300"),("C","400"),("D","500"),("E","600")]),
7:(r"For how many not necessarily positive integer values of $n$ is $4000\left(\frac25\right)^n$ an integer?",[("A","3"),("B","4"),("C","6"),("D","8"),("E","9")]),
8:(r"Joe has a collection of $23$ coins, consisting of $5$-cent coins, $10$-cent coins, and $25$-cent coins. He has $3$ more $10$-cent coins than $5$-cent coins, and the total value is $320$ cents. How many more $25$-cent coins does Joe have than $5$-cent coins?",[("A","0"),("B","1"),("C","2"),("D","3"),("E","4")]),
10:(r"Suppose that real number $x$ satisfies $\sqrt{49-x^2}-\sqrt{25-x^2}=3$. What is the value of $\sqrt{49-x^2}+\sqrt{25-x^2}$?",[("A","8"),("B",r"$\sqrt{33}+8$"),("C","9"),("D",r"$2\sqrt{10}+4$"),("E","12")]),
}

KEY_OVERRIDES={1:"Work from the innermost reciprocal outward.",2:"Compare both amounts to the same baseline.",3:"Convert factorial seconds into days.",4:"Choose nonconsecutive periods, then arrange the courses.",5:"Negate each statement and intersect the resulting inequalities.",6:"Convert like and dislike percentages into net score percentage.",7:"Use prime exponents in $4000(2/5)^n$.",8:"Set variables for coin counts and use total number and value.",10:"Use conjugates: product of sum and difference of radicals."}

SOL={
1:[("Start inside",r"The expression is built from repeated operations of taking a reciprocal and adding $1$. First, $2+1=3$."),("First reciprocal layer",r"\[(2+1)^{-1}+1=\frac13+1=\frac43.\]"),("Second reciprocal layer",r"\[\left(\frac43\right)^{-1}+1=\frac34+1=\frac74.\]"),("Third reciprocal layer",r"\[\left(\frac74\right)^{-1}+1=\frac47+1=\frac{11}{7}.\]"),("Conclude",r"The value is $\boxed{\frac{11}{7}}$."),],
2:[("Use Jacqueline as the baseline",r"Let Jacqueline have $J$ units of soda. Then Liliane has $1.50J$ and Alice has $1.25J$."),("Compare Liliane to Alice",r"The ratio is \[\frac{1.50J}{1.25J}=\frac{1.50}{1.25}=1.2.\]"),("Interpret the ratio",r"A ratio of $1.2$ means Liliane has $20\%$ more soda than Alice."),("Conclude",r"The answer is $\boxed{\text{Liliane has 20% more soda than Alice.}}$."),],
3:[("Convert seconds to days",r"There are $60\cdot60\cdot24=86400$ seconds in a day. We need \[\frac{10!}{86400}\] days."),("Simplify",r"Since $10!=3,628,800$, \[\frac{3,628,800}{86,400}=42.\] So the blood expires after $42$ days."),("Count from January 1 noon",r"After $31$ days it is noon on February $1$. There are $42-31=11$ more days."),("Find the date",r"Eleven days after February $1$ is February $12$."),("Conclude",r"The answer is $\boxed{\text{February 12}}$."),],
4:[("Choose the periods first",r"We need choose $3$ periods from $1$ through $6$ with no two consecutive. The possible sets are \[(1,3,5),(1,3,6),(1,4,6),(2,4,6).\]"),("Arrange the courses",r"For each valid set of periods, the three courses algebra, geometry, and number theory can be arranged in $3!=6$ orders."),("Multiply",r"There are $4$ valid period sets and $6$ course orders for each, giving \[4\cdot6=24.\]"),("Conclude",r"The answer is $\boxed{24}$."),],
5:[("Negate Alice's statement",r"Alice said $d\ge6$. Since her statement was false, we must have $d<6$."),("Negate Bob's statement",r"Bob said $d\le5$. Since that was false, we must have $d>5$."),("Negate Charlie's statement",r"Charlie said $d\le4$. Since that was false, we must have $d>4$, which is already implied by $d>5$."),("Combine",r"The possible distances satisfy \[5<d<6.\]"),("Conclude",r"The interval is $\boxed{(5,6)}$."),],
6:[("Let total votes be V",r"If $65\%$ of the votes were likes, then $35\%$ were dislikes."),("Convert to score",r"Each like contributes $+1$ and each dislike contributes $-1$, so the score is \[(0.65-0.35)V=0.30V.\]"),("Use the score 90",r"We are told $0.30V=90$, so \[V=\frac{90}{0.30}=300.\]"),("Conclude",r"There had been $\boxed{300}$ votes."),],
7:[("Factor the expression",r"Write \[4000=2^5\cdot5^3.\] Then \[4000\left(\frac25\right)^n=2^{5+n}5^{3-n}.\]"),("Require nonnegative exponents",r"For this to be an integer, both exponents must be nonnegative: \[5+n\ge0,\quad 3-n\ge0.\]"),("Solve the range",r"Thus \[-5\le n\le3.\]"),("Count integers",r"The integers from $-5$ through $3$ inclusive are $9$ values."),("Conclude",r"The answer is $\boxed{9}$."),],
8:[("Set variables",r"Let $x$ be the number of $5$-cent coins. Then the number of $10$-cent coins is $x+3$."),("Use the total number of coins",r"The number of $25$-cent coins is \[23-x-(x+3)=20-2x.\]"),("Use the total value",r"The total value is \[5x+10(x+3)+25(20-2x)=320.\]"),("Solve",r"Simplifying gives \[530-35x=320,\] so $x=6$."),("Answer the comparison",r"The number of $25$-cent coins is $20-2(6)=8$, which is $2$ more than the $6$ five-cent coins."),("Conclude",r"The answer is $\boxed{2}$."),],
10:[("Name the radicals",r"Let \[A=\sqrt{49-x^2},\quad B=\sqrt{25-x^2}.\] The problem tells us $A-B=3$."),("Use conjugates",r"We want $A+B$. The product \[(A-B)(A+B)=A^2-B^2\] removes the square roots."),("Compute the difference of squares",r"\[A^2-B^2=(49-x^2)-(25-x^2)=24.\]"),("Solve for the sum",r"Since $A-B=3$, \[3(A+B)=24,\] so $A+B=8$."),("Conclude",r"The answer is $\boxed{8}$."),],
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
        if r["year"] == "2018" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2018 AMC 10A Answer Key\n\n"
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












































