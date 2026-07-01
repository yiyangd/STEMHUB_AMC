import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 90
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2015_AMC_10B_Answer_Key"
TARGET_NUMBERS = {18,20,21,23,24,25}
SKIPPED = ["2015 AMC 10B Problem 17 skipped: prism dimensions depend on missing diagram", "2015 AMC 10B Problem 19 skipped: circle condition for constructed squares depends on diagram", "2015 AMC 10B Problem 22 skipped: pentagon segment labels depend on missing diagram"]
BATCH_LABEL = "2015 AMC 10B Problems 18,20,21,23,24,25"
NEXT_START = "2016 AMC 10A Problem 1"

ANS={18:("D","56"),20:("A","6"),21:("D","13"),23:("B","8"),24:("D","(13,-22)"),25:("B","10")}

OV={
18:(r"Johann has $64$ fair coins. He flips all the coins. Any coin that lands on tails is tossed again. Coins that land on tails on the second toss are tossed a third time. What is the expected number of coins that are now heads?",[("A","32"),("B","40"),("C","48"),("D","56"),("E","64")]),
20:(r"Erin the ant starts at a given corner of a cube and crawls along exactly $7$ edges in such a way that she visits every corner exactly once and then finds that she is unable to return along an edge to her starting point. How many paths are there meeting these conditions?",[("A","6"),("B","9"),("C","12"),("D","18"),("E","24")]),
21:(r"Cozy the Cat and Dash the Dog are going up a staircase with a certain number of steps. Cozy goes two steps up with each jump, except possibly the last jump. Dash goes five steps up with each jump, except possibly the last jump. Dash takes $19$ fewer jumps than Cozy. Let $s$ denote the sum of all possible numbers of steps this staircase can have. What is the sum of the digits of $s$?",[("A","9"),("B","11"),("C","12"),("D","13"),("E","15")]),
23:(r"Let $n$ be a positive integer greater than $4$ such that the decimal representation of $n!$ ends in $k$ zeros and the decimal representation of $(2n)!$ ends in $3k$ zeros. Let $s$ denote the sum of the four least possible values of $n$. What is the sum of the digits of $s$?",[("A","7"),("B","8"),("C","9"),("D","10"),("E","11")]),
24:(r"Aaron the ant walks on the coordinate plane according to the following rules. He starts at the origin $p_0=(0,0)$ facing east and walks one unit, arriving at $p_1=(1,0)$. For $n=1,2,3,\ldots$, right after arriving at $p_n$, if Aaron can turn $90^\circ$ left and walk one unit to an unvisited point, he does that; otherwise, he walks one unit straight ahead to reach $p_{n+1}$. The points continue in a counterclockwise spiral pattern. What is $p_{2015}$?",[("A","(-22,-13)"),("B","(-13,-22)"),("C","(-13,22)"),("D","(13,-22)"),("E","(22,-13)")]),
25:(r"A rectangular box measures $a\times b\times c$, where $a$, $b$, and $c$ are integers and $1\le a\le b\le c$. The volume and surface area of the box are numerically equal. How many ordered triples $(a,b,c)$ are possible?",[("A","4"),("B","10"),("C","12"),("D","21"),("E","26")]),
}

KEY_OVERRIDES={18:"Use linearity of expectation for each coin.",20:"Count Hamiltonian paths on the cube ending at the opposite vertex.",21:"Solve an equation involving ceiling functions.",23:"Count trailing zeros with factors of 5.",24:"Recognize square spiral layers and locate the index.",25:"Transform the volume-surface equation and enumerate bounded integer cases."}

SOL={
18:[("Use one coin first",r"A single coin is tossed until it lands heads or until it has been tossed three times. It is still not heads only if it lands tails three times."),("Find the probability a coin is heads",r"The probability of three tails is $\left(\frac12\right)^3=\frac18$, so the probability the coin is heads at the end is $1-\frac18=\frac78$."),("Use linearity of expectation",r"Expected values add even when outcomes are not listed one by one. For $64$ coins, the expected number of heads is $64\cdot\frac78=56$."),("Conclude",r"The answer is $\boxed{56}$."),],
20:[("Translate to cube vertices",r"Visiting every corner exactly once along $7$ edges is a Hamiltonian path on the cube graph starting from a fixed vertex."),("Use the final condition",r"After $7$ edge moves, the endpoint has odd parity relative to the start. Among odd-parity vertices, the only one not adjacent to the start is the opposite vertex."),("Count paths to the opposite vertex",r"From a fixed start to the opposite vertex, a direct case check on the first two moves shows there are $6$ Hamiltonian paths. Equivalently, they correspond to the $3!$ orders in which the three coordinate directions are first introduced."),("Check the condition",r"Each such path ends at the opposite corner, which is not connected to the starting corner by an edge, so Erin cannot return directly."),("Conclude",r"There are $\boxed{6}$ paths."),],
21:[("Write jumps with ceiling functions",r"If the staircase has $n$ steps, Cozy takes $\lceil n/2\rceil$ jumps and Dash takes $\lceil n/5\rceil$ jumps."),("Set up the difference",r"The condition is \[\left\lceil\frac n2\right\rceil-\left\lceil\frac n5\right\rceil=19.\]"),("Check the narrow range",r"Since the difference is roughly $\frac{3n}{10}$, $n$ should be near $63$. Testing the few possible values gives $n=63,64,66$."),("Sum possible stair counts",r"The sum is $s=63+64+66=193$."),("Sum digits",r"The digit sum of $193$ is $1+9+3=13$."),("Conclude",r"The answer is $\boxed{13}$."),],
23:[("Count trailing zeros",r"The number of trailing zeros in $n!$ is \[z(n)=\left\lfloor\frac n5\right\rfloor+\left\lfloor\frac n{25}\right\rfloor+\cdots.\]"),("Search the first values carefully",r"We need $z(2n)=3z(n)$. For small $n>4$, this can be checked by tracking multiples of $5$."),("Find the four least n",r"The first four values that work are $n=8,9,13,14$. For example, $z(8)=1$ and $z(16)=3$, while $z(13)=2$ and $z(26)=6$."),("Compute s",r"Their sum is $s=8+9+13+14=44$."),("Sum digits",r"The digit sum of $44$ is $8$."),("Conclude",r"The answer is $\boxed{8}$."),],
24:[("Recognize the spiral layers",r"The path forms a square spiral. The corners of the layers occur at nearby perfect squares, which makes it useful to locate $2015$ between squares."),("Locate the layer",r"We have $44^2=1936$ and $45^2=2025$. Thus $p_{2015}$ is on the layer ending near the square of side length $45$."),("Move back from a known corner",r"In this spiral, $p_{2025}$ is at $(22,-22)$. Moving back $10$ steps along the bottom side gives $p_{2015}=(13,-22)$."),("Conclude",r"The answer is $\boxed{(13,-22)}$."),],
25:[("Write the equation",r"The volume is $abc$, and the surface area is $2(ab+ac+bc)$. The condition is \[abc=2(ab+ac+bc).\]"),("Solve for c",r"Rearrange as \[c(ab-2a-2b)=2ab,\] so \[c=\frac{2ab}{ab-2a-2b}.\] This gives a finite check because the denominator must be positive."),("Bound a and b",r"Since $a\le b\le c$, testing possible small $a$ values is enough. The denominator becomes positive only after $a$ and $b$ are large enough, but if $a\ge7$ the fraction is already too small to keep $c\ge b$."),("List the valid triples",r"The valid triples are $(3,7,42),(3,8,24),(3,9,18),(3,10,15),(3,12,12),(4,5,20),(4,6,12),(4,8,8),(5,5,10),(6,6,6)$."),("Count",r"There are $10$ triples."),("Conclude",r"The answer is $\boxed{10}$."),],
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
        if r["year"] == "2015" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2015 AMC 10B Answer Key\n\n"
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












































