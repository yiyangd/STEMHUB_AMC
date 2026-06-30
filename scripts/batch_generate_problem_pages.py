from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 13
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2004_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 6, 7, 8, 9, 10}
SKIPPED = ["2004 AMC 10A Problem 5: probability question depends on the original grid diagram."]
BATCH_LABEL = "2004 AMC 10A Problem 1-10"
NEXT_START = "2004 AMC 10A Problem 11"

ANS = {
    1: ("A", "250"),
    2: ("B", r"-\frac{1}{4}"),
    3: ("E", "29"),
    4: ("D", r"\frac{3}{2}"),
    6: ("E", "26"),
    7: ("C", "100"),
    8: ("B", "37"),
    9: ("B", "4"),
    10: ("D", r"\frac{35}{128}"),
}


OV = {
    1: (
        r"You and five friends need to raise $\$1500$ in donations for a charity, dividing the fundraising equally. How many dollars will each of you need to raise?",
        [("A", "$250$"), ("B", "$300$"), ("C", "$1500$"), ("D", "$7500$"), ("E", "$9000$")],
    ),
    2: (
        r"For any three real numbers $a$, $b$, and $c$, with $b\ne c$, the operation $\otimes$ is defined by $\otimes(a,b,c)=\frac{a}{b-c}$. What is $\otimes(\otimes(1,2,3),\otimes(2,3,1),\otimes(3,1,2))$?",
        [("A", r"$-\frac12$"), ("B", r"$-\frac14$"), ("C", "$0$"), ("D", r"$\frac14$"), ("E", r"$\frac12$")],
    ),
    3: (
        r"Alicia earns $\$20$ per hour, of which $1.45\%$ is deducted to pay local taxes. How many cents per hour of Alicia's wages are used to pay local taxes?",
        [("A", "$0.0029$"), ("B", "$0.029$"), ("C", "$0.29$"), ("D", "$2.9$"), ("E", "$29$")],
    ),
    4: (
        r"What is the value of $x$ if $|x-1|=|x-2|$?",
        [("A", r"$-\frac12$"), ("B", r"$\frac12$"), ("C", "$1$"), ("D", r"$\frac32$"), ("E", "$2$")],
    ),
    7: (
        r"A grocer stacks oranges in a pyramid-like stack whose rectangular base is $5$ oranges by $8$ oranges. Each orange above the first level rests in a pocket formed by four oranges in the level below. The stack is completed by a single row of oranges. How many oranges are in the stack?",
        [("A", "$96$"), ("B", "$98$"), ("C", "$100$"), ("D", "$101$"), ("E", "$134$")],
    ),
    9: (
        r"In the figure, $\angle EAB$ and $\angle ABC$ are right angles. Also $AB=4$, $BC=6$, $AE=8$, and $AC$ and $BE$ intersect at $D$. What is the difference between the areas of $\triangle ADE$ and $\triangle BDC$?",
        [("A", "$2$"), ("B", "$4$"), ("C", "$5$"), ("D", "$8$"), ("E", "$9$")],
    ),
    10: (
        r"Coin A is flipped three times and coin B is flipped four times. What is the probability that the number of heads obtained from flipping the two fair coins is the same?",
        [("A", r"$\frac{19}{128}$"), ("B", r"$\frac{23}{128}$"), ("C", r"$\frac14$"), ("D", r"$\frac{35}{128}$"), ("E", r"$\frac12$")],
    ),
}


KEY_OVERRIDES = {
    1: "Divide the total fundraising goal equally among all six people.",
    2: "Evaluate the custom operation inside-out, keeping the order of the three inputs clear.",
    3: "Convert a percent of dollars into cents carefully.",
    4: "Use the meaning of equal distances on a number line.",
    6: "Set up a simple count of daughters and granddaughters.",
    7: "Add the rectangular layers of the orange stack as each layer shrinks by one in each direction.",
    8: "Find the repeating three-round cycle in the token counts.",
    9: "Use coordinates to compute the two triangle areas from the intersection point.",
    10: "Sum the probabilities that both coins produce the same number of heads.",
}


SOL = {
    1: [
        ("Count the people sharing the goal", r"The phrase 'you and five friends' means there are $6$ people total, not $5$. The donations are divided equally among all $6$."),
        ("Divide the total", r"Each person must raise \[\frac{1500}{6}=250.\]"),
        ("Check the total", r"If each of the $6$ people raises $250$, the total is $6\cdot250=1500$."),
        ("Answer", r"Each person needs to raise $\boxed{250}$ dollars."),
    ],
    2: [
        ("Understand the operation", r"The operation takes three inputs and returns the first input divided by the difference of the second and third: $\otimes(a,b,c)=\frac{a}{b-c}$. Since the final expression uses nested operations, start inside."),
        ("Evaluate the three inner operations", r"We get $\otimes(1,2,3)=\frac{1}{2-3}=-1$, $\otimes(2,3,1)=\frac{2}{3-1}=1$, and $\otimes(3,1,2)=\frac{3}{1-2}=-3$."),
        ("Substitute into the outer operation", r"The expression becomes $\otimes(-1,1,-3)$. Use the same rule again: \[\otimes(-1,1,-3)=\frac{-1}{1-(-3)}.\]"),
        ("Finish the calculation", r"The denominator is $4$, so the value is $-\frac14$."),
        ("Answer", r"The answer is $\boxed{-\frac14}$."),
    ],
    3: [
        ("Translate the percent", r"The tax rate $1.45\%$ means $0.0145$ of her hourly wage. Percent problems become easier once the percent is written as a decimal."),
        ("Find the dollar amount", r"Alicia earns $20$ dollars per hour, so the tax is $20\cdot0.0145=0.29$ dollars per hour."),
        ("Convert dollars to cents", r"Since $1$ dollar is $100$ cents, $0.29$ dollars is $29$ cents."),
        ("Answer", r"The local tax is $\boxed{29}$ cents per hour."),
    ],
    4: [
        ("Interpret the absolute values", r"The equation $|x-1|=|x-2|$ says that $x$ is the same distance from $1$ and from $2$ on the number line."),
        ("Use symmetry", r"The point equally distant from $1$ and $2$ is their midpoint."),
        ("Compute the midpoint", r"The midpoint is \[\frac{1+2}{2}=\frac32.\]"),
        ("Answer", r"Therefore $x=\boxed{\frac32}$."),
    ],
    6: [
        ("Define the unknown", r"Bertha has $6$ daughters. Let $d$ be the number of those daughters who each have $6$ daughters."),
        ("Use the total family count", r"The number of granddaughters is $6d$. The total number of daughters and granddaughters is $6+6d=30$."),
        ("Solve for d", r"From $6+6d=30$, we get $6d=24$, so $d=4$. Thus $4$ of Bertha's daughters have daughters, and $2$ of her daughters have no daughters."),
        ("Count people with no daughters", r"All $24$ granddaughters have no daughters because there are no great-granddaughters. Adding the $2$ daughters with no daughters gives $24+2=26$."),
        ("Answer", r"The answer is $\boxed{26}$."),
    ],
    7: [
        ("Visualize the layers", r"The bottom layer is a $5$ by $8$ rectangle of oranges. Each higher layer sits in pockets, so both dimensions shrink by $1$ each time."),
        ("List the layer sizes", r"The layers are $5\times8$, $4\times7$, $3\times6$, $2\times5$, and $1\times4$. The process stops at the single row $1\times4$."),
        ("Add the layers", r"The total number of oranges is \[5\cdot8+4\cdot7+3\cdot6+2\cdot5+1\cdot4.\]"),
        ("Compute", r"This is $40+28+18+10+4=100$."),
        ("Answer", r"The stack contains $\boxed{100}$ oranges."),
    ],
    8: [
        ("Track the first few rounds", r"The player with the most tokens loses $3$ tokens total: one to each of the other two players and one to the discard pile. Each other player gains $1$."),
        ("Find the repeating pattern", r"Starting from $(15,14,13)$, after three rounds the counts become $(14,13,12)$. The same order has returned, but each player has one fewer token."),
        ("Use the cycle", r"Every $3$ rounds, all three players decrease by $1$. After $36$ rounds, which is $12$ cycles, the counts are $(3,2,1)$."),
        ("Finish one more round", r"At that point A has the most tokens. In round $37$, A gives away three tokens total, so A goes from $3$ to $0$, and the game ends."),
        ("Answer", r"There are $\boxed{37}$ rounds."),
    ],
    9: [
        ("Choose coordinates", r"Place $A=(0,0)$, $B=(4,0)$, $C=(4,6)$, and $E=(0,8)$. This matches the two right angles and the given side lengths."),
        ("Find the intersection D", r"Line $AC$ has slope $6/4=3/2$, so its equation is $y=\frac32x$. Line $BE$ through $(4,0)$ and $(0,8)$ has equation $y=-2x+8$."),
        ("Solve for D", r"Set the equations equal: $\frac32x=-2x+8$. Then $\frac72x=8$, so $x=\frac{16}{7}$ and $y=\frac{24}{7}$."),
        ("Compute the two areas", r"Triangle $ADE$ has base $AE=8$ and horizontal height $\frac{16}{7}$, so its area is $\frac12\cdot8\cdot\frac{16}{7}=\frac{64}{7}$. Triangle $BDC$ has base $BC=6$ and horizontal height $4-\frac{16}{7}=\frac{12}{7}$, so its area is $\frac12\cdot6\cdot\frac{12}{7}=\frac{36}{7}$."),
        ("Subtract", r"The difference is $\frac{64}{7}-\frac{36}{7}=\frac{28}{7}=4$. The answer is $\boxed{4}$."),
    ],
    10: [
        ("Organize by the number of heads", r"Coin A is flipped $3$ times, so it can have $0,1,2,$ or $3$ heads. Coin B is flipped $4$ times, and we need the same number of heads."),
        ("Count favorable outcomes", r"For each possible $k$, the number of ways is $\binom{3}{k}\binom{4}{k}$. Therefore the favorable count is \[\binom30\binom40+\binom31\binom41+\binom32\binom42+\binom33\binom43.\]"),
        ("Compute the sum", r"This equals $1\cdot1+3\cdot4+3\cdot6+1\cdot4=1+12+18+4=35$."),
        ("Count all outcomes", r"There are $2^3$ outcomes for coin A and $2^4$ outcomes for coin B, for a total of $2^7=128$ equally likely outcomes."),
        ("Answer", r"The probability is $\boxed{\frac{35}{128}}$."),
    ],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {7, 9}) else notes
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
        if r["year"] == "2004" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {7, 9},
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
        + "- Review notes: Corrected 2003 AMC 10B Problem 10 answer choice from the AoPS answer key; Problem 20 uses the diagram data stated in text and should be visually reviewed later.\n",
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
        + "- Answer verification source: AoPS 2003 AMC 10B Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批完成 2004 AMC 10A Problems 1-4 和 6-10；Problem 5 因网格图缺失跳过。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
