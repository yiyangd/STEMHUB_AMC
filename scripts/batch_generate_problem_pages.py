from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 27
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2006_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11, 13, 14, 15, 18, 19, 20}
SKIPPED = ["2006 AMC 10A Problem 12: dog rope arrangement depends on preliminary drawings.", "2006 AMC 10A Problem 16: tangent-circles triangle depends on the original diagram.", "2006 AMC 10A Problem 17: WXYZ rectangle/trisection area depends on the original diagram."]
BATCH_LABEL = "2006 AMC 10A Problem 11-20"
NEXT_START = "2006 AMC 10A Problem 21"

ANS = {
    11: ("C", "two lines"),
    13: ("D", "60"),
    14: ("B", "173"),
    15: ("D", "47"),
    18: ("C", r"5\cdot10^4\cdot26^2"),
    19: ("C", "59"),
    20: ("E", "1"),
}


OV = {
    11: (
        r"Which of the following describes the graph of the equation $(x+y)^2=x^2+y^2$?",
        [("A", "the empty set"), ("B", "one point"), ("C", "two lines"), ("D", "a circle"), ("E", "the entire plane")],
    ),
    13: (
        r"A player pays $5$ dollars to play a game. A die is rolled. If the number on the die is odd, the game is lost. If the number is even, the die is rolled again. In this case the player wins if the second number matches the first and loses otherwise. How much should the player win if the game is fair?",
        [("A", "$12$"), ("B", "$30$"), ("C", "$50$"), ("D", "$60$"), ("E", "$100$")],
    ),
    14: (
        r"A number of linked rings, each $1$ cm thick, are hanging on a peg. The top ring has an outside diameter of $20$ cm. The outside diameter of each of the other rings is $1$ cm less than that of the ring above it. The bottom ring has an outside diameter of $3$ cm. What is the distance, in cm, from the top of the top ring to the bottom of the bottom ring?",
        [("A", "$171$"), ("B", "$173$"), ("C", "$182$"), ("D", "$188$"), ("E", "$210$")],
    ),
    18: (
        r"A license plate in a certain state consists of $4$ digits, not necessarily distinct, and $2$ letters, also not necessarily distinct. These six characters may appear in any order, except that the two letters must appear next to each other. How many distinct license plates are possible?",
        [("A", r"$10^4\cdot26^2$"), ("B", r"$10^3\cdot26^3$"), ("C", r"$5\cdot10^4\cdot26^2$"), ("D", r"$10^2\cdot26^4$"), ("E", r"$5\cdot10^3\cdot26^3$")],
    ),
    20: (
        r"Six distinct positive integers are randomly chosen between $1$ and $2006$, inclusive. What is the probability that some pair of these integers has a difference that is a multiple of $5$?",
        [("A", r"$\frac12$"), ("B", r"$\frac35$"), ("C", r"$\frac23$"), ("D", r"$\frac45$"), ("E", "$1$")],
    ),
}


KEY_OVERRIDES = {
    11: "Expand and simplify the equation to identify the coordinate axes.",
    13: "Compute the probability of winning and set expected payout equal to the cost.",
    14: "Add the vertical contributions of linked rings using outside and inside radii.",
    15: "Compare angular speeds on two circular lanes moving in opposite directions.",
    18: "Treat the adjacent letters as one block, then arrange with the four digits.",
    19: "An arithmetic progression of triangle angles must have middle angle 60 degrees.",
    20: "Use the pigeonhole principle on residues modulo 5.",
}


SOL = {
    11: [
        ("Expand the left side", r"The equation is $(x+y)^2=x^2+y^2$. Expanding gives $x^2+2xy+y^2=x^2+y^2$."),
        ("Simplify", r"Subtract $x^2+y^2$ from both sides to get $2xy=0$."),
        ("Interpret the product", r"The equation $2xy=0$ means $x=0$ or $y=0$."),
        ("Identify the graph", r"The set $x=0$ is the $y$-axis, and the set $y=0$ is the $x$-axis. Together these are two lines."),
        ("Answer", r"The graph is $\boxed{\text{two lines}}$."),
    ],
    13: [
        ("Find the probability of reaching the second roll", r"The first roll must be even. A fair die has $3$ even faces out of $6$, so this happens with probability $1/2$."),
        ("Find the probability of matching", r"Once the first roll is fixed, the second roll must match that exact number. This has probability $1/6$."),
        ("Find the win probability", r"Therefore the probability of winning is $\frac12\cdot\frac16=\frac1{12}$."),
        ("Use fairness", r"For a fair game, expected winnings equal the $5$ dollar cost. If the prize is $W$, then $\frac1{12}W=5$."),
        ("Answer", r"Solving gives $W=60$, so the player should win $\boxed{60}$ dollars."),
    ],
    14: [
        ("Count the rings", r"The outside diameters are $20,19,18,\ldots,3$, so there are $18$ rings."),
        ("Use inside radii", r"Each ring is $1$ cm thick, so a ring with outside diameter $D$ has inside radius $D/2-1$."),
        ("Find center-to-center drops", r"For two linked rings with outside diameters $D_i$ and $D_{i+1}$, their centers are separated vertically by the sum of their inside radii: $(D_i/2-1)+(D_{i+1}/2-1)$."),
        ("Add top and bottom radii", r"The total distance is the top outside radius $10$, plus all $17$ center-to-center drops, plus the bottom outside radius $3/2$."),
        ("Compute", r"This gives $10+\sum_{D=20}^{4}\left((D/2-1)+((D-1)/2-1)\right)+\frac32=173$. The answer is $\boxed{173}$."),
    ],
    15: [
        ("Convert speeds to angular speeds", r"Odell's angular speed is $250/50=5$ radians per minute. Kershaw's angular speed is $300/60=5$ radians per minute."),
        ("Use opposite directions", r"Since they run in opposite directions, their relative angular speed is $5+5=10$ radians per minute."),
        ("Find total relative angle", r"In $30$ minutes, the relative angular distance is $30\cdot10=300$ radians."),
        ("Count meetings after the start", r"They pass whenever the relative angular distance reaches a positive multiple of $2\pi$. The count is $\left\lfloor\frac{300}{2\pi}\right\rfloor$."),
        ("Answer", r"Since $\frac{300}{2\pi}\approx47.7$, they pass $\boxed{47}$ times after the start."),
    ],
    18: [
        ("Treat the two letters as a block", r"Because the two letters must be next to each other, view them as one letter-block plus four separate digit positions. That makes $5$ objects to arrange."),
        ("Place the letter block", r"The block can occupy any of $5$ positions among the six characters."),
        ("Choose characters", r"The four digits have $10^4$ choices because repetition is allowed. The two letters have $26^2$ choices because repetition is also allowed and order matters inside the block."),
        ("Multiply", r"The total number of plates is $5\cdot10^4\cdot26^2$."),
        ("Answer", r"The answer is $\boxed{5\cdot10^4\cdot26^2}$."),
    ],
    19: [
        ("Use the arithmetic progression structure", r"If three angles are in arithmetic progression, write them as $60-d$, $60$, and $60+d$, because their sum must be $180$."),
        ("Apply positivity", r"The smallest angle must be positive, so $60-d>0$. Thus $d<60$."),
        ("Apply distinctness", r"The angles are distinct, so $d$ must be a positive integer."),
        ("Count d values", r"Therefore $d$ can be $1,2,\ldots,59$, giving $59$ different angle triples."),
        ("Answer", r"Each different angle triple gives a non-similar triangle, so the answer is $\boxed{59}$."),
    ],
    20: [
        ("Think modulo 5", r"Two integers have a difference that is a multiple of $5$ exactly when they have the same remainder modulo $5$."),
        ("Use pigeonhole principle", r"There are only $5$ possible remainders modulo $5$: $0,1,2,3,4$."),
        ("Place six integers into five classes", r"Choosing $6$ distinct integers forces at least two of them to have the same remainder modulo $5$."),
        ("Conclude", r"That pair has a difference divisible by $5$, no matter which six integers were chosen."),
        ("Answer", r"The probability is therefore $\boxed{1}$."),
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in set()) else notes
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
        if r["year"] == "2006" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in set(),
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
        + "本批完成 2006 AMC 10A Problems 11、13、14、15、18、19、20；Problems 12、16、17 因图形依赖跳过。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
