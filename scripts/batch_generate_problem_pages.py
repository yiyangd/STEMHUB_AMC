import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 114
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2019_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2019 AMC 10B Problems 21-25"
NEXT_START = "2020 AMC 10A Problem 1"

ANS={21:("B",r"\frac1{24}"),22:("B",r"\frac14"),23:("C",r"\frac{85\pi}{8}"),24:("C","[81,242]"),25:("C","65")}

OV={
21:(r"Debra flips a fair coin repeatedly, keeping track of how many heads and tails she has seen in total, until she gets either two heads in a row or two tails in a row, at which point she stops. What is the probability that she gets two heads in a row but she sees a second tail before she sees a second head?",[("A",r"$\frac1{36}$"),("B",r"$\frac1{24}$"),("C",r"$\frac1{18}$"),("D",r"$\frac1{12}$"),("E",r"$\frac16$")]),
22:(r"Raashan, Sylvia, and Ted play a game. Each starts with $1$. Every round, each player who currently has money independently chooses one of the other two players at random and gives $1$ to that player. What is the probability that after the bell has rung $2019$ times, each player will have $1$?",[("A",r"$\frac17$"),("B",r"$\frac14$"),("C",r"$\frac13$"),("D",r"$\frac12$"),("E",r"$\frac23$")]),
23:(r"Points $A(6,13)$ and $B(12,11)$ lie on circle $\omega$. Suppose that the tangent lines to $\omega$ at $A$ and $B$ intersect at a point on the $x$-axis. What is the area of $\omega$?",[("A",r"$\frac{83\pi}{8}$"),("B",r"$\frac{21\pi}{2}$"),("C",r"$\frac{85\pi}{8}$"),("D",r"$\frac{43\pi}{4}$"),("E",r"$\frac{87\pi}{8}$")]),
24:(r"Define a sequence recursively by $x_0=5$ and \[x_{n+1}=\frac{x_n^2+5x_n+4}{x_n+6}\] for all nonnegative integers $n$. Let $m$ be the least positive integer such that \[x_m\le4+\frac1{2^{20}}.\] In which interval does $m$ lie?",[("A","[9,26]"),("B","[27,80]"),("C","[81,242]"),("D","[243,728]"),("E","[729,∞]")]),
25:(r"How many sequences of $0$s and $1$s of length $19$ begin with a $0$, end with a $0$, contain no two consecutive $0$s, and contain no three consecutive $1$s?",[("A","55"),("B","60"),("C","65"),("D","70"),("E","75")]),
}

KEY_OVERRIDES={21:"List the alternating prefixes that allow HH to stop after the second tail comes first.",22:"Use a two-state Markov description of money distributions.",23:"Use equal tangent lengths and perpendicular radii.",24:"Shift by 4 and bound the recurrence geometrically.",25:"Represent the sequence as gaps of one or two 1s between zeros."}

SOL={
21:[("Describe possible stopping strings",r"Before the stopping flip, the sequence cannot contain two equal consecutive flips. Therefore it must alternate. To stop with two heads in a row, the sequence must end in $HH$."),("Impose the second-tail condition",r"Debra must see her second tail before her second head. The shortest successful sequence is \[THTHH.\] The second tail occurs on flip $3$, while the second head occurs on flip $4$."),("List all successful patterns",r"After $THT$, Debra may continue alternating with pairs $HT$ any number of times, and then finish with $HH$. Thus the successful sequences are \[THTHH,\ THTHTHH,\ THTHTHTHH,\ldots\]"),("Sum the probabilities",r"The probabilities are \[\frac1{2^5}+\frac1{2^7}+\frac1{2^9}+\cdots.\] This is a geometric series with first term $\frac1{32}$ and ratio $\frac14$."),("Compute",r"\[\frac{1/32}{1-1/4}=\frac{1}{32}\cdot\frac43=\frac1{24}.\]"),("Conclude",r"The answer is $\boxed{\frac1{24}}$."),],
22:[("Reduce to two money states",r"Up to player names, the only possible money distributions after a round are balanced $(1,1,1)$ and unbalanced $(2,1,0)$. The game starts balanced."),("From the balanced state",r"If all three players have $1$, there are $2^3=8$ equally likely ways to choose recipients. Exactly two directed cycles keep everyone at $1$, so the probability of returning to balanced is \[\frac28=\frac14.\]"),("From the unbalanced state",r"In a state like $(2,1,0)$, only two players give money, so there are $2^2=4$ equally likely choices. Exactly one of these choices returns the distribution to $(1,1,1)$."),("Notice the invariant probability",r"From either possible state, the probability that the next state is balanced is always $\frac14$."),("Apply to 2019 rounds",r"Therefore after any positive number of rounds, including $2019$, the probability of being balanced is $\frac14$."),("Conclude",r"The answer is $\boxed{\frac14}$."),],
23:[("Find the tangent intersection point",r"Let the tangent lines meet at $P=(t,0)$. Tangent segments from the same external point have equal lengths, so \[PA=PB.\]"),("Solve for t",r"Using $A(6,13)$ and $B(12,11)$, \[(t-6)^2+13^2=(t-12)^2+11^2.\] This gives $t=5$, so $P=(5,0)$."),("Use perpendicular radii",r"The radius to a tangent point is perpendicular to the tangent line. The slope of $PA$ is $13$, so the radius through $A$ has slope $-\frac1{13}$. The slope of $PB$ is $\frac{11}{7}$, so the radius through $B$ has slope $-\frac7{11}$."),("Find the center",r"Intersecting the two radius lines gives the center \[O=\left(\frac{37}{4},\frac{51}{4}\right).\]"),("Find radius squared",r"Using point $A$, \[r^2=\left(\frac{37}{4}-6\right)^2+\left(\frac{51}{4}-13\right)^2=\frac{85}{8}.\]"),("Conclude",r"The area is \[\pi r^2=\boxed{\frac{85\pi}{8}}.\]"),],
24:[("Shift the sequence toward its limit",r"The expression suggests that $4$ is the limiting value. Define \[y_n=x_n-4.\] Then \[y_{n+1}=y_n\cdot\frac{y_n+9}{y_n+10}.\]"),("Bound the ratio",r"Since $x_0=5$, we have $y_0=1$, and the sequence stays positive and decreasing. For $0<y_n\le1$, \[\frac9{10}<\frac{y_n+9}{y_n+10}<\frac{10}{11}.\]"),("Get upper and lower bounds",r"Therefore \[\left(\frac9{10}\right)^n<y_n<\left(\frac{10}{11}\right)^n.\] We need $y_m\le2^{-20}$."),("Show m is not too small",r"At $n=80$, \[\left(\frac9{10}\right)^{80}>2^{-20},\] so $m>80$."),("Show m is not too large",r"At $n=242$, \[\left(\frac{10}{11}\right)^{242}<2^{-20},\] so $m\le242$."),("Conclude",r"Together, \[81\le m\le242,\] so the correct interval is $\boxed{[81,242]}$."),],
25:[("Translate the restrictions into gaps",r"The sequence begins and ends with $0$, and no two zeros are consecutive. Therefore between consecutive zeros there must be a block of $1$s."),("Use the no-three-ones condition",r"Because no three consecutive $1$s are allowed, each block between zeros has length either $1$ or $2$."),("Set up variables",r"Suppose there are $k$ gaps between zeros. Then there are $k+1$ zeros. If $t$ of the gaps have length $2$ and the rest have length $1$, the total length is \[(k+1)+(k+t)=2k+t+1.\]"),("Use length 19",r"We need \[2k+t+1=19,\] so \[t=18-2k.\] Also $0\le t\le k$."),("Count possibilities",r"The possible values are $k=6,7,8,9$, giving \[\binom66+\binom74+\binom82+\binom90=1+35+28+1=65.\]"),("Conclude",r"The answer is $\boxed{65}$."),],
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
        if r["year"] == "2019" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2019 AMC 10B Answer Key\n\n"
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












































