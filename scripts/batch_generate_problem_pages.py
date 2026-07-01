import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 80
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2014_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,24,25}
SKIPPED = ["2014 AMC 10A Problem 23 skipped: folding line and overlap depend on missing diagram"]
BATCH_LABEL = "2014 AMC 10A Problems 21,22,24,25"
NEXT_START = "2014 AMC 10B Problem 1"

ANS={21:("E",r"-8"),22:("E","20"),24:("A","996506"),25:("B","279")}

OV={
21:(r"Positive integers $a$ and $b$ are such that the graphs of $y=ax+5$ and $y=3x+b$ intersect the $x$-axis at the same point. What is the sum of all possible $x$-coordinates of these points of intersection?",[("A",r"-20"),("B",r"-18"),("C",r"-15"),("D",r"-12"),("E",r"-8")]),
22:(r"In rectangle $ABCD$, $AB=20$ and $BC=10$. Let $E$ be a point on $CD$ such that $\angle CBE=15^\circ$. What is $AE$?",[("A",r"\frac{20}{\sqrt3}"),("B",r"10\sqrt3"),("C","18"),("D",r"11\sqrt3"),("E","20")]),
24:(r"A sequence of natural numbers is constructed by listing the first $4$, then skipping one, listing the next $5$, skipping $2$, listing $6$, skipping $3$, and, on the $n$th iteration, listing $n+3$ and skipping $n$. The sequence begins $1,2,3,4,6,7,8,9,10,13$. What is the $500000$th number in the sequence?",[("A","996506"),("B","996507"),("C","996508"),("D","996509"),("E","996510")]),
25:(r"The number $5^{867}$ is between $2^{2013}$ and $2^{2014}$. How many pairs of integers $(m,n)$ are there such that $1\le m\le2012$ and $5^n<2^m<2^{m+2}<5^{n+1}$?",[("A","278"),("B","279"),("C","280"),("D","281"),("E","282")]),
}

KEY_OVERRIDES={21:"Convert the shared x-intercept into a divisor equation.",22:"Use the 15-degree angle to locate E, then apply the distance formula.",24:"Use cumulative listed counts to locate the correct iteration.",25:"Convert the exponential inequalities into fractional-part counting with logarithms."}

SOL={
21:[("Use the shared x-intercept",r"The line $y=ax+5$ meets the $x$-axis when $0=ax+5$, so $x=-\frac5a$. The line $y=3x+b$ meets the $x$-axis when $x=-\frac b3$."),("Set the intercepts equal",r"Since the two $x$-intercepts are the same, \[-\frac5a=-\frac b3.\] Thus $ab=15$."),("List positive factor pairs",r"Because $a$ and $b$ are positive integers, the possible values of $a$ are $1,3,5,15$."),("Find and add the x-coordinates",r"The corresponding intercepts are $-5$, $-\frac53$, $-1$, and $-\frac13$. Their sum is \[-5-\frac53-1-\frac13=-8.\]"),("Conclude",r"The answer is $\boxed{-8}$."),],
22:[("Place the rectangle",r"Let $A=(0,0)$, $B=(20,0)$, $C=(20,10)$, and $D=(0,10)$. Point $E$ lies on the top side $CD$."),("Use the 15-degree angle",r"From $B$, segment $BC$ is vertical and has length $10$. Since $\angle CBE=15^\circ$, the horizontal distance from $C$ to $E$ is $10\tan15^\circ$."),("Use the special tangent value",r"\[\tan15^\circ=2-\sqrt3.\] Therefore $E$ has $x$-coordinate $20-10(2-\sqrt3)=10\sqrt3$, and $y$-coordinate $10$."),("Compute AE",r"Now \[AE=\sqrt{(10\sqrt3)^2+10^2}=\sqrt{300+100}=20.\]"),("Conclude",r"The answer is $\boxed{20}$."),],
24:[("Count listed terms by iteration",r"On iteration $n$, the sequence lists $n+3$ numbers. After $k$ iterations, the number of listed terms is \[\sum_{n=1}^k(n+3)=\frac{k(k+7)}2.\]"),("Locate the 500000th listed term",r"For $k=996$, this count is $\frac{996\cdot1003}{2}=499494$. For $k=997$, it is $\frac{997\cdot1004}{2}=500494$. So the $500000$th term occurs during iteration $997$."),("Find the actual numbers reached before that iteration",r"Each iteration $n$ lists $n+3$ numbers and then skips $n$, so it passes over $2n+3$ natural numbers. After $996$ iterations, the last passed number is \[\sum_{n=1}^{996}(2n+3)=996^2+4\cdot996=996000.\]"),("Move to the desired position",r"The $500000$th listed term is $500000-499494=506$ terms into iteration $997$. That iteration starts at $996001$, so the desired number is $996001+505=996506$."),("Conclude",r"The answer is $\boxed{996506}$."),],
25:[("Translate with logarithms",r"Let $\alpha=\log_2 5$. The inequality $5^n<2^m<2^{m+2}<5^{n+1}$ becomes \[n\alpha<m<m+2<(n+1)\alpha.\]"),("Understand how many m values are possible",r"Since $\alpha$ is a little more than $2$, the possible integer $m$ for a fixed $n$ can only be the first integer greater than $n\alpha$. Such an $m$ works exactly when the fractional part of $n\alpha$ is greater than $3-\alpha$."),("Remove the integer part of alpha",r"Write $\alpha=2+\beta$, where $\beta=\log_2(5/4)$. The condition becomes $\{n\beta\}>1-\beta$, which is equivalent to $\lfloor(n+1)\beta\rfloor=\lfloor n\beta\rfloor+1$."),("Count the jumps",r"For $1\le m\le2012$, the relevant values are $n=1$ through $866$. The number of jumps is \[\lfloor867\beta\rfloor.\]"),("Use the given estimate",r"The given fact says $2^{2013}<5^{867}<2^{2014}$, so $2013<867\alpha<2014$. Subtracting $2\cdot867=1734$ gives $279<867\beta<280$."),("Conclude",r"Therefore $\lfloor867\beta\rfloor=279$, so the answer is $\boxed{279}$."),],
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
    if n == 17 and notes == "题面包含图形":
        notes = ""
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in {12,13} else notes
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
        if r["year"] == "2014" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {12,13},
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
        + "- Answer verification source: AoPS 2014 AMC 10A Answer Key\n\n"
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












































