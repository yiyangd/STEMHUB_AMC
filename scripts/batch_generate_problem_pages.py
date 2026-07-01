import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 81
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2014_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,6,7,8,9,10}
SKIPPED = ["2014 AMC 10B Problem 5 skipped: pane layout depends on missing diagram"]
BATCH_LABEL = "2014 AMC 10B Problems 1-10 excluding 5"
NEXT_START = "2014 AMC 10B Problem 11"

ANS={1:("C","37"),2:("E","64"),3:("E",r"\frac{300}{7}"),4:("B",r"\frac53"),6:("C","36"),7:("A",r"100\left(\frac{A-B}{B}\right)"),8:("E",r"\frac{10b}{t}"),9:("A","-2014"),10:("C","7")}

OV={
1:(r"Leah has $13$ coins, all of which are pennies and nickels. If she had one more nickel than she has now, then she would have the same number of pennies and nickels. In cents, how much are Leah's coins worth?",[("A","33"),("B","35"),("C","37"),("D","39"),("E","41")]),
2:(r"What is $\frac{2^3+2^3}{2^{-3}+2^{-3}}$?",[("A","16"),("B","24"),("C","32"),("D","48"),("E","64")]),
3:(r"Randy drove the first third of his trip on a gravel road, the next $20$ miles on pavement, and the remaining one-fifth on a dirt road. In miles, how long was Randy's trip?",[("A","30"),("B",r"\frac{400}{11}"),("C",r"\frac{75}{2}"),("D","40"),("E",r"\frac{300}{7}")]),
4:(r"Susie pays for $4$ muffins and $3$ bananas. Calvin spends twice as much paying for $2$ muffins and $16$ bananas. A muffin is how many times as expensive as a banana?",[("A","3"),("B",r"\frac53"),("C",r"\frac74"),("D","2"),("E",r"\frac{13}{4}")]),
6:(r"Orvin went to the store with just enough money to buy $30$ balloons. When he arrived, he discovered that the store had a special sale on balloons: buy $1$ balloon at the regular price and get a second at $\frac13$ off the regular price. What is the greatest number of balloons Orvin could buy?",[("A","33"),("B","34"),("C","36"),("D","38"),("E","39")]),
7:(r"Suppose $A>B>0$ and $A$ is $x\%$ greater than $B$. What is $x$?",[("A",r"100\left(\frac{A-B}{B}\right)"),("B",r"100\left(\frac{A+B}{B}\right)"),("C",r"100\left(\frac{A+B}{A}\right)"),("D",r"100\left(\frac{A-B}{A}\right)"),("E",r"100\left(\frac{A}{B}\right)")]),
8:(r"A truck travels $\frac{b}{6}$ feet every $t$ seconds. There are $3$ feet in a yard. How many yards does the truck travel in $3$ minutes?",[("A",r"\frac{b}{1080t}"),("B",r"\frac{30t}{b}"),("C",r"\frac{30b}{t}"),("D",r"\frac{10t}{b}"),("E",r"\frac{10b}{t}")]),
9:(r"For real numbers $w$ and $z$, \[\frac{\frac1w+\frac1z}{\frac1w-\frac1z}=2014.\] What is $\frac{w+z}{w-z}$?",[("A","-2014"),("B",r"-\frac1{2014}"),("C",r"\frac1{2014}"),("D","1"),("E","2014")]),
10:(r"In the addition shown below, $A$, $B$, $C$, and $D$ are distinct digits: \[ABBCB+BCADA=DBDDD.\] How many different values are possible for $D$?",[("A","2"),("B","4"),("C","7"),("D","8"),("E","9")]),
}

KEY_OVERRIDES={1:"Translate the coin condition into two equations.",2:"Simplify powers carefully, especially negative exponents.",3:"Use fractions of the total trip to identify the 20-mile middle part.",4:"Set up prices for muffins and bananas and solve for the ratio.",6:"Group balloons into sale pairs and compare their cost to regular price.",7:"Use the definition of percent increase from the original amount.",8:"Convert feet to yards and minutes to seconds before multiplying by rate.",9:"Clear the complex fraction and watch the sign change.",10:"Analyze column carries in a digit addition puzzle."}

SOL={
1:[("Name the coins",r"Let $p$ be the number of pennies and $n$ be the number of nickels. The total number of coins gives $p+n=13$."),("Translate the extra nickel condition",r"If Leah had one more nickel, she would have $n+1$ nickels. That would equal the number of pennies, so $p=n+1$."),("Solve the system",r"Substitute $p=n+1$ into $p+n=13$: \[(n+1)+n=13.\] Thus $2n=12$, so $n=6$ and $p=7$."),("Compute the value",r"The pennies are worth $7$ cents, and the nickels are worth $6\cdot5=30$ cents. The total is $37$ cents."),("Conclude",r"The answer is $\boxed{37}$."),],
2:[("Simplify the numerator",r"The numerator is $2^3+2^3=8+8=16$."),("Simplify the denominator",r"A negative exponent means reciprocal: $2^{-3}=\frac18$. So the denominator is $\frac18+\frac18=\frac14$."),("Divide by the denominator",r"The expression is \[\frac{16}{1/4}=16\cdot4=64.\]"),("Check the size",r"The denominator is less than $1$, so dividing by it should make the numerator larger. Getting $64$ is reasonable."),("Conclude",r"The answer is $\boxed{64}$."),],
3:[("Represent the whole trip",r"Let the total trip length be $T$ miles. The first part is $\frac13T$, and the last part is $\frac15T$."),("Identify the paved part",r"The paved part is what remains after the first and last parts: \[1-\frac13-\frac15=\frac7{15}\] of the trip."),("Use the 20-mile information",r"The paved part is $20$ miles, so \[\frac7{15}T=20.\]"),("Solve",r"Multiplying by $\frac{15}{7}$ gives $T=20\cdot\frac{15}{7}=\frac{300}{7}$."),("Conclude",r"The answer is $\boxed{\frac{300}{7}}$."),],
4:[("Assign prices",r"Let a muffin cost $m$ dollars and a banana cost $b$ dollars. Susie pays $4m+3b$."),("Translate Calvin's cost",r"Calvin pays for $2$ muffins and $16$ bananas, so his cost is $2m+16b$. The problem says this is twice Susie's cost."),("Set up the equation",r"\[2m+16b=2(4m+3b).\] Expanding gives $2m+16b=8m+6b$."),("Solve for the ratio",r"Move terms to get $10b=6m$, so $\frac{m}{b}=\frac{10}{6}=\frac53$."),("Conclude",r"A muffin is $\boxed{\frac53}$ times as expensive as a banana."),],
6:[("Measure money in regular balloon prices",r"Let one regular-price balloon cost $p$. Orvin has $30p$ dollars."),("Find the cost of a sale pair",r"Under the sale, two balloons cost $p+\frac23p=\frac53p$, because the second balloon is $\frac13$ off."),("Count full sale pairs",r"With $30p$ dollars, Orvin can buy \[\frac{30p}{(5/3)p}=18\] sale pairs."),("Convert pairs to balloons",r"Each pair contains $2$ balloons, so $18$ pairs give $36$ balloons. This uses all of his money exactly."),("Conclude",r"The answer is $\boxed{36}$."),],
7:[("Recall the definition",r"Saying $A$ is $x\%$ greater than $B$ means the increase from $B$ to $A$ is $x\%$ of $B$."),("Write the increase",r"The increase is $A-B$. Therefore \[\frac{x}{100}\cdot B=A-B.\]"),("Solve for x",r"Divide by $B$ and multiply by $100$: \[x=100\left(\frac{A-B}{B}\right).\]"),("Check the denominator",r"The denominator must be the original amount, which is $B$, not the final amount $A$."),("Conclude",r"The answer is $\boxed{100\left(\frac{A-B}{B}\right)}$."),],
8:[("Convert the distance unit",r"The truck travels $\frac{b}{6}$ feet every $t$ seconds. Since $3$ feet make $1$ yard, this is $\frac{b}{18}$ yards every $t$ seconds."),("Convert the time",r"Three minutes is $180$ seconds. That contains $\frac{180}{t}$ intervals of length $t$ seconds."),("Multiply rate by number of intervals",r"The total distance in yards is \[\frac{b}{18}\cdot\frac{180}{t}=\frac{10b}{t}.\]"),("Check the units",r"The feet-to-yards conversion divides by $3$, and the minutes-to-seconds conversion multiplies by $180$. Both conversions are accounted for."),("Conclude",r"The answer is $\boxed{\frac{10b}{t}}$."),],
9:[("Clear the complex fraction",r"Multiply the numerator and denominator by $wz$. Then \[\frac{\frac1w+\frac1z}{\frac1w-\frac1z}=\frac{z+w}{z-w}.\]"),("Use the given value",r"The equation tells us \[\frac{w+z}{z-w}=2014,\] since $z+w=w+z$."),("Compare with the requested expression",r"The denominator in the requested expression is $w-z$, which is the negative of $z-w$."),("Change the sign",r"Therefore \[\frac{w+z}{w-z}=-\frac{w+z}{z-w}=-2014.\]"),("Conclude",r"The answer is $\boxed{-2014}$."),],
10:[("Look at the leftmost column",r"The sum has only five digits, so there is no carry into a sixth digit. Thus the leftmost column gives $A+B=D$."),("Use the ones column",r"The ones column is also $B+A$, so it gives the same digit $D$ and has no carry."),("Use the tens column",r"With no carry from the ones column, the tens column gives $C+D=D$. Hence $C=0$."),("Determine possible D values",r"Since $A$ and $B$ are distinct nonzero digits and $D=A+B$, the smallest possible $D$ is $1+2=3$. Any value from $3$ through $9$ can be made by choosing distinct positive digits with that sum."),("Count",r"The possible values are $3,4,5,6,7,8,9$, which gives $7$ values."),("Conclude",r"The answer is $\boxed{7}$."),],
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
        if r["year"] == "2014" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2014 AMC 10B Answer Key\n\n"
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












































