import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 106
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2018_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2018 AMC 10B Problems 1-10"
NEXT_START = "2018 AMC 10B Problem 11"

ANS={1:("A","90"),2:("D","67"),3:("B","3"),4:("B","22"),5:("D","240"),6:("D",r"\frac15"),7:("D","19"),8:("C","12"),9:("D","39"),10:("E","2")}

OV={
1:(r"Kate bakes a $20$-inch by $18$-inch pan of cornbread. The cornbread is cut into pieces that measure $2$ inches by $2$ inches. How many pieces of cornbread does the pan contain?",[("A","90"),("B","100"),("C","180"),("D","200"),("E","360")]),
2:(r"Sam drove $96$ miles in $90$ minutes. His average speed during the first $30$ minutes was $60$ mph, and his average speed during the second $30$ minutes was $65$ mph. What was his average speed, in mph, during the last $30$ minutes?",[("A","64"),("B","65"),("C","66"),("D","67"),("E","68")]),
3:(r"In the expression $(\square\times\square)+(\square\times\square)$, each blank is filled with one of the digits $1,2,3,4$, each used once. How many different values can be obtained?",[("A","2"),("B","3"),("C","4"),("D","6"),("E","24")]),
4:(r"A three-dimensional rectangular box with dimensions $X$, $Y$, and $Z$ has face areas $24,24,48,48,72,72$. What is $X+Y+Z$?",[("A","18"),("B","22"),("C","24"),("D","30"),("E","36")]),
5:(r"How many subsets of $\{2,3,4,5,6,7,8,9\}$ contain at least one prime number?",[("A","128"),("B","192"),("C","224"),("D","240"),("E","256")]),
6:(r"A box contains $5$ chips, numbered $1,2,3,4,5$. Chips are drawn randomly one at a time without replacement until the sum of the values drawn exceeds $4$. What is the probability that $3$ draws are required?",[("A",r"$\frac1{15}$"),("B",r"$\frac1{10}$"),("C",r"$\frac16$"),("D",r"$\frac15$"),("E",r"$\frac14$")]),
7:(r"$N$ congruent semicircles lie on the diameter of a large semicircle, with their diameters covering the diameter of the large semicircle with no overlap. Let $A$ be the combined area of the small semicircles and $B$ be the area inside the large semicircle but outside the small semicircles. The ratio $A:B$ is $1:18$. What is $N$?",[("A","16"),("B","17"),("C","18"),("D","19"),("E","36")]),
8:(r"Sara makes a staircase out of toothpicks. A $3$-step staircase uses $18$ toothpicks. How many steps would be in a staircase that used $180$ toothpicks?",[("A","10"),("B","11"),("C","12"),("D","24"),("E","30")]),
9:(r"The faces of each of $7$ standard dice are labeled with the integers from $1$ to $6$. Let $p$ be the probability that when all $7$ dice are rolled, the sum of the top faces is $10$. What other sum occurs with the same probability as $p$?",[("A","13"),("B","26"),("C","32"),("D","39"),("E","42")]),
10:(r"In a rectangular parallelepiped, $AB=3$, $BC=1$, and $CG=2$. Point $M$ is the midpoint of $FG$. What is the volume of the rectangular pyramid with base $BCHE$ and apex $M$?",[("A",r"$\frac12$"),("B","1"),("C",r"$\frac32$"),("D",r"$\sqrt2$"),("E","2")]),
}

KEY_OVERRIDES={1:"Divide each dimension by the side length of each square piece.",2:"Use distance equals rate times time for each half-hour segment.",3:"Pair the digits into two products and list possible pairings.",4:"Use pairwise products $XY$, $YZ$, and $XZ$.",5:"Count all subsets minus subsets with no primes.",6:"Three draws are required exactly when the first two chip values sum to at most 4.",7:"Compare semicircle areas by square of scale factor.",8:"Use the toothpick count formula for an n-step staircase.",9:"Use the dice symmetry $k$ maps to $7-k$.",10:"Use coordinates for the slanted rectangular base and height."}

SOL={
1:[("Count pieces along each dimension",r"Along the $20$-inch side, pieces of width $2$ inches make $20/2=10$ pieces. Along the $18$-inch side, pieces of width $2$ inches make $18/2=9$ pieces."),("Multiply rows and columns",r"The pan is cut into a $10$ by $9$ grid."),("Compute",r"\[10\cdot9=90.\]"),("Conclude",r"The pan contains $\boxed{90}$ pieces."),],
2:[("Convert each 30 minutes to hours",r"Each $30$-minute part is $\frac12$ hour."),("Find distances in the first two parts",r"In the first half hour, Sam drove $60\cdot\frac12=30$ miles. In the second half hour, he drove $65\cdot\frac12=32.5$ miles."),("Find the remaining distance",r"He drove $96$ miles total, so the last half hour covered \[96-30-32.5=33.5\] miles."),("Compute speed",r"Speed is distance divided by time, so the last speed was \[\frac{33.5}{0.5}=67\text{ mph}.\]"),("Conclude",r"The answer is $\boxed{67}$."),],
3:[("Think in pairings",r"The expression pairs the four digits into two products. The order within a product and the order of the two products do not change the value."),("List the pairings",r"The possible pairings are \[(1,2),(3,4),\quad (1,3),(2,4),\quad (1,4),(2,3).\]"),("Compute values",r"These give \[1\cdot2+3\cdot4=14,\] \[1\cdot3+2\cdot4=11,\] and \[1\cdot4+2\cdot3=10.\]"),("Count",r"There are $3$ different values."),("Conclude",r"The answer is $\boxed{3}$."),],
4:[("Relate dimensions to face areas",r"The three distinct face areas are $XY$, $YZ$, and $XZ$, which are $24$, $48$, and $72$ in some order."),("Find the product XYZ",r"Multiplying the three face areas gives \[(XY)(YZ)(XZ)=(XYZ)^2=24\cdot48\cdot72.\]"),("Assign convenient values",r"Take $XY=24$, $YZ=48$, and $XZ=72$. Then \[X^2=\frac{(XY)(XZ)}{YZ}=\frac{24\cdot72}{48}=36,\] so $X=6$."),("Find Y and Z",r"Then $Y=24/6=4$ and $Z=72/6=12$."),("Add",r"\[X+Y+Z=6+4+12=22.\]"),("Conclude",r"The answer is $\boxed{22}$."),],
5:[("Count all subsets",r"The set has $8$ elements, so it has $2^8=256$ subsets total."),("Count subsets with no primes",r"The primes in the set are $2,3,5,7$. The nonprimes are $4,6,8,9$. A subset with no primes can use only these $4$ nonprimes, giving $2^4=16$ subsets."),("Subtract",r"Subsets with at least one prime: \[256-16=240.\]"),("Conclude",r"The answer is $\boxed{240}$."),],
6:[("Understand three draws required",r"Three draws are required exactly when after two draws the sum is still at most $4$. Since all chips are positive, the third draw will then make the sum exceed $4$."),("Count ordered first two draws",r"The ordered first two draws must be distinct numbers from $1,2,3,4,5$ with sum at most $4$. The possibilities are \[(1,2),(2,1),(1,3),(3,1).\]"),("Count all ordered first two draws",r"There are $5\cdot4=20$ possible ordered first two draws."),("Find probability",r"The probability is \[\frac4{20}=\frac15.\]"),("Conclude",r"The answer is $\boxed{\frac15}$."),],
7:[("Compare areas by scale",r"Let the large semicircle have radius $R$. Since the $N$ congruent small diameters exactly cover the large diameter, each small semicircle has radius $R/N$."),("Find combined small area",r"The large semicircle area is proportional to $R^2$. The combined small area is \[N\cdot\frac12\pi\left(\frac RN\right)^2=\frac1N\cdot\frac12\pi R^2.\] So $A$ is $\frac1N$ of the large semicircle area."),("Find the leftover area",r"The leftover area $B$ is \[1-\frac1N=\frac{N-1}{N}\] of the large semicircle area."),("Use the ratio",r"Thus \[A:B=1:(N-1).\] Since this ratio is $1:18$, we have $N-1=18$."),("Conclude",r"$N=\boxed{19}$."),],
8:[("Use the staircase count",r"For an $n$-step toothpick staircase, the count is \[n(n+3).\] This matches the given $3$-step example: $3(3+3)=18$."),("Set up the equation",r"We need \[n(n+3)=180.\]"),("Solve",r"\[n^2+3n-180=0=(n-12)(n+15).\] The positive solution is $n=12$."),("Conclude",r"The staircase has $\boxed{12}$ steps."),],
9:[("Use dice symmetry",r"For one die, replacing a roll $r$ by $7-r$ gives another equally likely roll."),("Apply to seven dice",r"If seven dice have sum $S$, then the transformed seven dice have sum \[7\cdot7-S=49-S.\]"),("Match sum 10",r"Therefore the sum with the same probability as $10$ is \[49-10=39.\]"),("Conclude",r"The answer is $\boxed{39}$."),],
10:[("Set coordinates for the box",r"Use coordinates $A=(0,0,0)$, $B=(3,0,0)$, $C=(3,1,0)$, $E=(0,0,2)$, $F=(3,0,2)$, $G=(3,1,2)$, and $H=(0,1,2)$."),("Locate M",r"Since $M$ is the midpoint of $FG$, \[M=\left(3,\frac12,2\right).\]"),("Find the base area",r"The base $BCHE$ is a rectangle with side vectors $\overrightarrow{BC}=(0,1,0)$ and $\overrightarrow{BE}=(-3,0,2)$. Its area is \[\left|\overrightarrow{BC}\times\overrightarrow{BE}\right|=\sqrt{13}.\]"),("Find the height",r"The distance from $M$ to the plane $BCHE$ is \[\frac{6}{\sqrt{13}}.\]"),("Compute pyramid volume",r"The volume is \[\frac13\cdot\sqrt{13}\cdot\frac6{\sqrt{13}}=2.\]"),("Conclude",r"The answer is $\boxed{2}$."),],
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
        if r["year"] == "2018" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2018 AMC 10B Answer Key\n\n"
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












































