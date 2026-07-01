from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 29
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2006_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 5, 9, 10}
SKIPPED = [
    "2006 AMC 10B Problem 6 skipped: statement depends on a diagram and OCR text is incomplete.",
    "2006 AMC 10B Problem 7 skipped: OCR text for the expression is unreliable.",
    "2006 AMC 10B Problem 8 skipped: statement depends on a diagram.",
]
BATCH_LABEL = "2006 AMC 10B Problems 1-5, 9-10"
NEXT_START = "2006 AMC 10B Problem 11"

ANS = {
    1: ("C", "0"),
    2: ("A", "-72"),
    3: ("A", "10"),
    4: ("D", "8"),
    5: ("B", "25"),
    9: ("B", "137"),
    10: ("A", "43"),
}


OV = {
    1: (
        r"What is $(-1)^1+(-1)^2+\cdots+(-1)^{2006}$?",
        [("A", "$-2006$"), ("B", "$-1$"), ("C", "$0$"), ("D", "$1$"), ("E", "$2006$")],
    ),
    2: (
        r"For real numbers $x$ and $y$, define $x\spadesuit y=(x+y)(x-y)$. What is $3\spadesuit(4\spadesuit5)$?",
        [("A", "$-72$"), ("B", "$-27$"), ("C", "$-24$"), ("D", "$24$"), ("E", "$72$")],
    ),
    3: (
        r"A football game was played between two teams, the Cougars and the Panthers. The two teams scored a total of $34$ points, and the Cougars won by a margin of $14$ points. How many points did the Panthers score?",
        [("A", "$10$"), ("B", "$14$"), ("C", "$17$"), ("D", "$20$"), ("E", "$24$")],
    ),
    4: (
        r"Circles of diameter $1$ inch and $3$ inches have the same center. The smaller circle is painted red, and the portion outside the smaller circle and inside the larger circle is painted blue. What is the ratio of the blue-painted area to the red-painted area?",
        [("A", "$2$"), ("B", "$3$"), ("C", "$6$"), ("D", "$8$"), ("E", "$9$")],
    ),
    5: (
        r"A $2\times3$ rectangle and a $3\times4$ rectangle are contained within a square without overlapping at any interior point, and the sides of the square are parallel to the sides of the two given rectangles. What is the smallest possible area of the square?",
        [("A", "$16$"), ("B", "$25$"), ("C", "$36$"), ("D", "$49$"), ("E", "$64$")],
    ),
    9: (
        r"Francesca uses $100$ grams of lemon juice, $100$ grams of sugar, and $400$ grams of water to make lemonade. There are $25$ calories in $100$ grams of lemon juice and $386$ calories in $100$ grams of sugar. Water contains no calories. How many calories are in $200$ grams of her lemonade?",
        [("A", "$129$"), ("B", "$137$"), ("C", "$174$"), ("D", "$223$"), ("E", "$411$")],
    ),
    10: (
        r"In a triangle with integer side lengths, one side is three times as long as a second side, and the length of the third side is $15$. What is the greatest possible perimeter of the triangle?",
        [("A", "$43$"), ("B", "$44$"), ("C", "$45$"), ("D", "$46$"), ("E", "$47$")],
    ),
}


KEY_OVERRIDES = {
    1: "Pair alternating powers of -1 so that each pair cancels to zero.",
    2: "Evaluate the custom operation from the inside outward, keeping track of signs.",
    3: "Use the sum and difference of two scores to solve a simple system.",
    4: "Compare annulus area to inner circle area using radii from the given diameters.",
    5: "Find the smallest square side length that can contain both rectangles without overlap.",
    9: "Use proportional reasoning: compute total calories first, then scale to 200 grams.",
    10: "Use the triangle inequality to maximize the integer side length while keeping a triangle possible.",
}


SOL = {
    1: [
        ("Notice the repeating pattern", r"The powers of $-1$ alternate: $(-1)^1=-1$, $(-1)^2=1$, then the same pattern repeats. When a long expression alternates like this, pairing neighboring terms is usually cleaner than adding one by one."),
        ("Pair the terms", r"Group the sum as $((-1)^1+(-1)^2)+((-1)^3+(-1)^4)+\cdots+((-1)^{2005}+(-1)^{2006})$. Each pair is $-1+1=0$."),
        ("Check that no term is left over", r"There are $2006$ terms, which is even, so the terms divide into $1003$ complete pairs. This matters because an odd number of terms would leave one extra $-1$."),
        ("Add the pairs", r"Since every pair contributes $0$, the whole sum is $0$."),
        ("Answer", r"Therefore the answer is $\boxed{0}$."),
    ],
    2: [
        ("Read the operation carefully", r"The symbol $\spadesuit$ is not a standard operation; the problem defines it for us. Whenever an AMC problem defines a new operation, we should substitute into the definition exactly as written."),
        ("Evaluate the inside first", r"The expression is $3\spadesuit(4\spadesuit5)$, so first compute $4\spadesuit5$: \[4\spadesuit5=(4+5)(4-5)=9(-1)=-9.\]"),
        ("Use the result as the second input", r"Now the original expression becomes $3\spadesuit(-9)$. Apply the same rule again, this time with $x=3$ and $y=-9$."),
        ("Compute the final value", r"We get \[3\spadesuit(-9)=(3+(-9))(3-(-9))=(-6)(12)=-72.\] The negative sign is reasonable because one factor is negative and one is positive."),
        ("Answer", r"Therefore the answer is $\boxed{-72}$."),
    ],
    3: [
        ("Assign variables to the scores", r"Let $p$ be the Panthers' score. Since the Cougars won by $14$, the Cougars scored $p+14$. This turns the wording into an equation."),
        ("Use the total points", r"The two teams scored $34$ points altogether, so \[p+(p+14)=34.\] This equation uses both pieces of information: total score and winning margin."),
        ("Solve for the Panthers' score", r"Simplifying gives $2p+14=34$, so $2p=20$, and therefore $p=10$."),
        ("Check the result", r"If the Panthers scored $10$, the Cougars scored $24$. The total is $34$ and the margin is $14$, so both conditions are satisfied."),
        ("Answer", r"The Panthers scored $\boxed{10}$ points."),
    ],
    4: [
        ("Convert diameters to radii", r"Area formulas use radius, not diameter. The red circle has radius $\frac12$, and the larger circle has radius $\frac32$."),
        ("Compute the red area", r"The red area is the area of the smaller circle: \[\pi\left(\frac12\right)^2=\frac{\pi}{4}.\]"),
        ("Compute the blue area as a difference", r"The blue region is the larger circle minus the smaller circle: \[\pi\left(\frac32\right)^2-\pi\left(\frac12\right)^2=\frac{9\pi}{4}-\frac{\pi}{4}=2\pi.\]"),
        ("Form the requested ratio", r"The ratio of blue area to red area is \[\frac{2\pi}{\pi/4}=8.\] The factor of $\pi$ cancels, as it often does in ratios of circular areas."),
        ("Answer", r"Therefore the answer is $\boxed{8}$."),
    ],
    5: [
        ("Think in terms of side length", r"The square must be large enough in both horizontal and vertical directions. Because the sides of all rectangles are parallel, we only need to reason about widths and heights."),
        ("Find a lower bound", r"The $3\times4$ rectangle already requires one side of the square to be at least $4$. But the total area of the two rectangles is $2\cdot3+3\cdot4=18$, so a $4\times4$ square of area $16$ is impossible."),
        ("Test the next possible answer size", r"The answer choices are square areas, so after $16$ the next candidate is $25$, which means a $5\times5$ square. We need to see whether the two rectangles can fit inside it."),
        ("Give a fitting arrangement", r"Place the $3\times4$ rectangle using width $3$ and height $4$. Place the $2\times3$ rectangle beside it using width $2$ and height $3$. Together they fit in a $5$-wide by $4$-high region, which is inside a $5\times5$ square."),
        ("Answer", r"So the smallest possible square area is $\boxed{25}$."),
    ],
    9: [
        ("Compute the total mass", r"The lemonade contains $100+100+400=600$ grams in all. The question asks about $200$ grams, which is one third of the total mixture."),
        ("Compute the total calories", r"The lemon juice contributes $25$ calories, the sugar contributes $386$ calories, and the water contributes $0$. So the full $600$ grams has $25+386=411$ calories."),
        ("Scale the calories", r"Since the ingredients are mixed evenly, a $200$-gram serving has the same fraction of the total calories as its fraction of the mass. That fraction is $\frac{200}{600}=\frac13$."),
        ("Calculate", r"Therefore the calories in $200$ grams are \[\frac13\cdot411=137.\]"),
        ("Answer", r"The answer is $\boxed{137}$."),
    ],
    10: [
        ("Name the related sides", r"Let the shorter of the two related sides be $x$. Then the side three times as long is $3x$, and the third side is $15$. The perimeter is $x+3x+15=4x+15$, so we want $x$ as large as possible."),
        ("Apply the key triangle inequality", r"For a triangle, the sum of the two shorter sides must be greater than the longest side. Since $3x$ is the potentially long side, we need $x+15>3x$."),
        ("Solve the inequality", r"The inequality gives $15>2x$, so $x<7.5$. Because the side lengths are integers, the largest possible value is $x=7$."),
        ("Check that it works", r"With $x=7$, the side lengths are $7$, $21$, and $15$. We have $7+15=22>21$, so the triangle is valid."),
        ("Answer", r"The greatest possible perimeter is $7+21+15=\boxed{43}$."),
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
        if r["year"] == "2006" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Review notes: Skipped Problems 6 and 8 because they require diagrams; skipped Problem 7 because OCR made the expression unreliable.\n",
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
        + "- Answer verification source: AoPS 2006 AMC 10B Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批跳过 2006 AMC 10B Problems 6, 7, 8：6 和 8 依赖图形，7 的公式 OCR 不可靠。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
