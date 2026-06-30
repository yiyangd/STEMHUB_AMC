from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 14
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2004_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
SKIPPED = []
BATCH_LABEL = "2004 AMC 10A Problem 11-20"
NEXT_START = "2004 AMC 10A Problem 21"

ANS = {
    11: ("C", "36"),
    12: ("C", "768"),
    13: ("D", "18"),
    14: ("A", "0"),
    15: ("D", r"\frac{1}{2}"),
    16: ("D", "19"),
    17: ("C", "350"),
    18: ("A", "1"),
    19: ("C", "240"),
    20: ("D", "2"),
}


OV = {
    11: (
        r"A company sells peanut butter in cylindrical jars. Marketing research suggests that using wider jars will increase sales. If the diameter of the jars is increased by $25\%$ without altering the volume, by what percent must the height be decreased?",
        [("A", "$10$"), ("B", "$25$"), ("C", "$36$"), ("D", "$50$"), ("E", "$60$")],
    ),
    12: (
        r"Henry's Hamburger Heaven orders its hamburgers with the following condiments: ketchup, mustard, mayonnaise, tomato, lettuce, pickles, cheese, and onions. A customer can choose one, two, or three meat patties, and any collection of condiments. How many different kinds of hamburgers can be ordered?",
        [("A", "$24$"), ("B", "$256$"), ("C", "$768$"), ("D", "$40,320$"), ("E", "$120,960$")],
    ),
    15: (
        r"Given that $-4\le x\le -2$ and $2\le y\le4$, what is the largest possible value of $\frac{x+y}{x}$?",
        [("A", "$-1$"), ("B", r"$-\frac12$"), ("C", "$0$"), ("D", r"$\frac12$"), ("E", "$1$")],
    ),
    16: (
        r"The $5\times5$ grid shown contains a collection of squares with sizes from $1\times1$ to $5\times5$. How many of these squares contain the black center square?",
        [("A", "$12$"), ("B", "$15$"), ("C", "$17$"), ("D", "$19$"), ("E", "$20$")],
    ),
    19: (
        r"A white cylindrical silo has diameter $30$ feet and height $80$ feet. A red stripe with a horizontal width of $3$ feet is painted on the silo, making two complete revolutions around it. What is the area of the stripe in square feet?",
        [("A", "$120$"), ("B", "$180$"), ("C", "$240$"), ("D", "$360$"), ("E", "$480$")],
    ),
    20: (
        r"Points $E$ and $F$ are located on square $ABCD$ so that $\triangle BEF$ is equilateral. What is the ratio of the area of $\triangle DEF$ to that of $\triangle ABE$?",
        [("A", r"$\frac43$"), ("B", r"$\frac32$"), ("C", r"$\sqrt3$"), ("D", "$2$"), ("E", r"$1+\sqrt3$")],
    ),
}


KEY_OVERRIDES = {
    11: "Keep cylinder volume constant while the radius is scaled.",
    12: "Use independent choices: meat patty count times include-or-exclude condiment choices.",
    13: "Count dance pairings in two ways.",
    14: "Use the average formula before and after adding one quarter.",
    15: "Rewrite the expression and use endpoint reasoning with a negative denominator.",
    16: "Count axis-aligned grid squares of each size that contain the central cell.",
    17: "Use constant speed ratios between the first and second meetings on a circular track.",
    18: "Turn arithmetic progression and geometric progression conditions into one quadratic.",
    19: "Unroll the cylinder and shear the diagonal stripe into a rectangle with the same area.",
    20: "Relate the square and equilateral triangle with right triangles and equal side lengths.",
}


SOL = {
    11: [
        ("Focus on volume", r"The jar is a cylinder, so its volume is $V=\pi r^2h$. The volume stays the same, so any increase in $r^2$ must be balanced by a decrease in $h$."),
        ("Convert the diameter change", r"If the diameter increases by $25\%$, then the radius also increases by $25\%$. The new radius is $1.25r=\frac54r$."),
        ("Find the area factor", r"The circular base area is multiplied by $(\frac54)^2=\frac{25}{16}$."),
        ("Keep volume constant", r"To keep $\pi r^2h$ unchanged, the height must be multiplied by the reciprocal, $\frac{16}{25}$."),
        ("Convert to a percent decrease", r"The new height is $64\%$ of the old height, so the decrease is $100\%-64\%=36\%$. The answer is $\boxed{36}$."),
    ],
    12: [
        ("Separate the independent choices", r"The customer chooses the number of patties and then chooses condiments. These choices are independent, so we multiply the counts."),
        ("Count patty choices", r"There are $3$ choices for meat patties: one, two, or three."),
        ("Count condiment choices", r"There are $8$ condiments. Each condiment is either included or not included, so there are $2^8=256$ possible condiment collections."),
        ("Multiply", r"The total number of hamburgers is $3\cdot256=768$."),
        ("Answer", r"The answer is $\boxed{768}$."),
    ],
    13: [
        ("Count the same thing two ways", r"The useful object to count is a dance pairing between one man and one woman."),
        ("Count from the men's side", r"There are $12$ men, and each danced with exactly $3$ women. That gives $12\cdot3=36$ dance pairings."),
        ("Count from the women's side", r"If there are $w$ women, and each danced with exactly $2$ men, then the same number of pairings is $2w$."),
        ("Solve", r"Thus $2w=36$, so $w=18$."),
        ("Answer", r"There were $\boxed{18}$ women at the party."),
    ],
    14: [
        ("Set up the original average", r"Let $n$ be the number of coins. Since the average value is $20$ cents, the total value is $20n$ cents."),
        ("Use the new average", r"After adding one quarter, there are $n+1$ coins and the total value is $20n+25$ cents. The new average is $21$ cents, so \[\frac{20n+25}{n+1}=21.\]"),
        ("Solve for the number of coins", r"This gives $20n+25=21n+21$, so $n=4$. The original total value was $80$ cents."),
        ("Determine the coins", r"With four coins totaling $80$ cents, the only way using pennies, nickels, dimes, and quarters is three quarters and one nickel. That uses no dimes."),
        ("Answer", r"Paula has $\boxed{0}$ dimes."),
    ],
    15: [
        ("Rewrite the expression", r"We have $\frac{x+y}{x}=1+\frac{y}{x}$. Since $x$ is negative and $y$ is positive, the fraction $\frac{y}{x}$ is negative."),
        ("Make the negative part as small as possible", r"To maximize the whole expression, we want $\frac{y}{x}$ to be as close to $0$ as possible. That means choose the smallest $y$ and the negative $x$ with largest absolute value."),
        ("Use the endpoints", r"The best choices are $y=2$ and $x=-4$. Then \[\frac{x+y}{x}=\frac{-4+2}{-4}=\frac{-2}{-4}=\frac12.\]"),
        ("Answer", r"The largest possible value is $\boxed{\frac12}$."),
    ],
    16: [
        ("Count by square size", r"The black square is the center cell of a $5\times5$ grid. Count how many axis-aligned squares of each size contain that center cell."),
        ("Small sizes", r"For $1\times1$ squares, only the center square works: $1$. For $2\times2$ squares, the center cell can be in any of four positions inside the square, so there are $4$."),
        ("Middle and large sizes", r"For $3\times3$ squares, there are $3$ possible row positions and $3$ possible column positions, giving $9$. For $4\times4$ squares, there are $2\cdot2=4$. For the $5\times5$ square, there is $1$."),
        ("Add", r"The total is $1+4+9+4+1=19$."),
        ("Answer", r"The answer is $\boxed{19}$."),
    ],
    17: [
        ("Introduce the track length", r"Let the track length be $L$. Since the runners start at opposite points, they are initially $L/2$ meters apart along either direction."),
        ("Use the first meeting", r"At the first meeting, Brenda has run $100$ meters, so Sally has run $L/2-100$ meters. Their speed ratio is therefore $\frac{100}{L/2-100}$."),
        ("Use the second meeting", r"Between consecutive meetings while running in opposite directions, together they cover one full lap. From the first to the next meeting, Sally runs $150$ meters, so Brenda runs $L-150$ meters."),
        ("Set equal speed ratios", r"The speed ratio is constant, so \[\frac{100}{L/2-100}=\frac{L-150}{150}.\] Solving gives $15000=(L-150)(L/2-100)$, which simplifies to $L=350$."),
        ("Answer", r"The track length is $\boxed{350}$ meters."),
    ],
    18: [
        ("Write the arithmetic progression", r"Let the common difference be $d$. The three original terms are $9$, $9+d$, and $9+2d$."),
        ("Apply the changes", r"After adding $2$ to the second term and $20$ to the third term, the new terms are $9$, $11+d$, and $29+2d$."),
        ("Use the geometric progression condition", r"For three terms in a geometric progression, the middle squared equals the product of the first and third: \[(11+d)^2=9(29+2d).\]"),
        ("Solve for d", r"Expanding gives $d^2+22d+121=261+18d$, so $d^2+4d-140=0$. Thus $d=10$ or $d=-14$."),
        ("Find the smallest third term", r"The third term of the geometric progression is $29+2d$. The two possibilities are $49$ and $1$, so the smallest possible value is $\boxed{1}$."),
    ],
    19: [
        ("Unroll the cylinder", r"Imagine cutting the silo vertically and unrolling it into a rectangle. The red stripe becomes a diagonal band crossing the rectangle while wrapping twice around the cylinder."),
        ("Use the given horizontal width", r"The stripe has horizontal width $3$ feet. In the unrolled rectangle, a diagonal band of constant horizontal width can be sheared into a vertical rectangle without changing area."),
        ("Identify the rectangle dimensions", r"After this shear, the equivalent rectangle has width $3$ feet and height equal to the silo height, $80$ feet. The number of revolutions changes the slant, but not this area calculation when the horizontal width is fixed."),
        ("Compute the area", r"The area is $3\cdot80=240$ square feet."),
        ("Answer", r"The stripe area is $\boxed{240}$."),
    ],
    20: [
        ("Use a convenient scale", r"Let the side length of the square be $1$. From the diagram, $E$ lies on $AD$ and $F$ lies on $DC$, with $\triangle BEF$ equilateral."),
        ("Set a helpful variable", r"Let $DE=DF=x$. Then $AE=1-x$. Triangle $DEF$ is a right isosceles triangle, so $EF^2=x^2+x^2=2x^2$."),
        ("Use the equilateral condition", r"Because $\triangle BEF$ is equilateral, $BE=EF$. Also triangle $ABE$ is right, so $BE^2=AB^2+AE^2=1+(1-x)^2$."),
        ("Relate x to the square", r"Set $BE^2=EF^2$: \[1+(1-x)^2=2x^2.\] This simplifies to $x^2=2(1-x)$."),
        ("Compare areas", r"Now $[DEF]=\frac{x^2}{2}$ and $[ABE]=\frac{1-x}{2}$. Their ratio is \[\frac{[DEF]}{[ABE]}=\frac{x^2}{1-x}=2.\] The answer is $\boxed{2}$."),
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {16, 19, 20}) else notes
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
                "needs_review": int(r["problem_no"]) in {16, 19, 20},
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
        + "本批完成 2004 AMC 10A Problems 11-20；Problems 16、19、20 标记为图形复核。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
