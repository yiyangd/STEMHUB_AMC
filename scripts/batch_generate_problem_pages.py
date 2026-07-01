from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 26
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2006_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 5, 6, 8, 9, 10}
SKIPPED = ["2006 AMC 10A Problem 7: rectangle-to-hexagon dissection depends on the original diagram."]
BATCH_LABEL = "2006 AMC 10A Problem 1-10"
NEXT_START = "2006 AMC 10A Problem 11"

ANS = {
    1: ("A", "31"),
    2: ("C", "h"),
    3: ("B", "18"),
    4: ("E", "23"),
    5: ("D", "4"),
    6: ("B", r"\frac{2}{7}"),
    8: ("E", "11"),
    9: ("C", "3"),
    10: ("E", "11"),
}


OV = {
    1: (
        r"Sandwiches at Joe's Fast Food cost $3$ dollars each and sodas cost $2$ dollars each. How many dollars will it cost to purchase $5$ sandwiches and $8$ sodas?",
        [("A", "$31$"), ("B", "$32$"), ("C", "$33$"), ("D", "$34$"), ("E", "$35$")],
    ),
    2: (
        r"Define $x\otimes y=x^3-y$. What is $h\otimes(h\otimes h)$?",
        [("A", "$-h$"), ("B", "$0$"), ("C", "$h$"), ("D", "$2h$"), ("E", "$h^3$")],
    ),
    3: (
        r"The ratio of Mary's age to Alice's age is $3:5$. Alice is $30$ years old. How old is Mary?",
        [("A", "$15$"), ("B", "$18$"), ("C", "$20$"), ("D", "$24$"), ("E", "$50$")],
    ),
    4: (
        r"A digital watch displays hours and minutes with AM and PM. What is the largest possible sum of the digits in the display?",
        [("A", "$17$"), ("B", "$19$"), ("C", "$21$"), ("D", "$22$"), ("E", "$23$")],
    ),
    6: (
        r"What non-zero real value for $x$ satisfies $(7x)^{14}=(14x)^7$?",
        [("A", r"$\frac17$"), ("B", r"$\frac27$"), ("C", "$1$"), ("D", "$7$"), ("E", "$14$")],
    ),
    10: (
        r"For how many positive integer values of $x$ is $\sqrt{120-x}$ an integer?",
        [("A", "$3$"), ("B", "$6$"), ("C", "$9$"), ("D", "$10$"), ("E", "$11$")],
    ),
}


KEY_OVERRIDES = {
    1: "Multiply each item cost by the quantity and add.",
    2: "Evaluate the custom operation from the inside out.",
    3: "Use a ratio to scale Mary's age from Alice's age.",
    4: "Maximize the digit sum of a valid 12-hour digital time.",
    5: "Split the pizza cost according to which slices were eaten.",
    6: "Use exponent rules and the nonzero condition to solve for x.",
    8: "Use symmetry of equal y-values on a parabola.",
    9: "List possible lengths of consecutive positive integer sums.",
    10: "Count square values that keep x positive.",
}


SOL = {
    1: [
        ("Compute sandwich cost", r"Each sandwich costs $3$ dollars, so $5$ sandwiches cost $5\cdot3=15$ dollars."),
        ("Compute soda cost", r"Each soda costs $2$ dollars, so $8$ sodas cost $8\cdot2=16$ dollars."),
        ("Add the costs", r"The total cost is $15+16=31$ dollars."),
        ("Answer", r"The answer is $\boxed{31}$."),
    ],
    2: [
        ("Start inside", r"The expression is nested, so first compute $h\otimes h$. By definition, $h\otimes h=h^3-h$."),
        ("Substitute into the outside operation", r"Now $h\otimes(h\otimes h)=h\otimes(h^3-h)$."),
        ("Apply the definition again", r"Using $x\otimes y=x^3-y$, this becomes $h^3-(h^3-h)$."),
        ("Simplify", r"The $h^3$ terms cancel, leaving $h$."),
        ("Answer", r"The value is $\boxed{h}$."),
    ],
    3: [
        ("Use the ratio", r"Mary's age to Alice's age is $3:5$, so Mary is $3/5$ as old as Alice."),
        ("Substitute Alice's age", r"Alice is $30$, so Mary's age is $\frac35\cdot30=18$."),
        ("Check", r"The ratio $18:30$ simplifies to $3:5$, matching the problem."),
        ("Answer", r"Mary is $\boxed{18}$ years old."),
    ],
    4: [
        ("Think about valid times", r"The watch uses a $12$-hour display, so the hour can be from $1$ to $12$ and the minutes from $00$ to $59$."),
        ("Maximize the minute digits", r"The largest possible minute digit sum is from $59$, which gives $5+9=14$."),
        ("Maximize the hour digit with that", r"The hour with the largest digit sum is $9$, giving digit sum $9$. Times like $19:59$ are not valid on a $12$-hour watch."),
        ("Add", r"At $9:59$, the digit sum is $9+5+9=23$."),
        ("Answer", r"The largest possible sum is $\boxed{23}$."),
    ],
    5: [
        ("Find the total pizza cost", r"The plain pizza costs $8$, and anchovies on half add $2$, so the whole pizza costs $10$."),
        ("Separate plain and anchovy halves", r"The plain half costs $4$. The anchovy half costs the other $4$ of plain pizza plus the $2$ topping charge, so it costs $6$."),
        ("Assign Dave's cost", r"Dave ate all $4$ anchovy slices, worth $6$, and one plain slice. Since the plain half has $4$ slices costing $4$, one plain slice costs $1$. Dave pays $7$."),
        ("Assign Doug's cost", r"Doug ate the remaining $3$ plain slices, worth $3$."),
        ("Answer", r"Dave paid $7-3=\boxed{4}$ dollars more than Doug."),
    ],
    6: [
        ("Use the nonzero condition", r"Because $x\ne0$, we can divide by powers of $x$ without losing a solution."),
        ("Expand the powers", r"The equation is $7^{14}x^{14}=14^7x^7$. Dividing by $x^7$ gives $7^{14}x^7=14^7$."),
        ("Solve for x to the seventh", r"Since $14^7=(2\cdot7)^7=2^7\cdot7^7$, we get \[x^7=\frac{2^7\cdot7^7}{7^{14}}=\left(\frac27\right)^7.\]"),
        ("Take the seventh root", r"The seventh root preserves the real value, so $x=\frac27$."),
        ("Answer", r"The answer is $\boxed{\frac27}$."),
    ],
    8: [
        ("Use the equal y-values", r"The points $(2,3)$ and $(4,3)$ have the same $y$-value on the parabola. For a parabola, equal heights occur at points symmetric about the axis of symmetry."),
        ("Find the axis", r"The midpoint of $x=2$ and $x=4$ is $x=3$, so the axis of symmetry is $x=3$."),
        ("Relate this to b", r"For $y=x^2+bx+c$, the axis is $x=-b/2$. Thus $-b/2=3$, so $b=-6$."),
        ("Solve for c", r"Use point $(2,3)$: $3=2^2-6(2)+c=4-12+c$, so $c=11$."),
        ("Answer", r"The answer is $\boxed{11}$."),
    ],
    9: [
        ("List by length", r"We need sums of two or more consecutive positive integers that equal $15$. Checking by length is organized and avoids missing cases."),
        ("Find the examples", r"With length $2$, $7+8=15$. With length $3$, $4+5+6=15$. With length $5$, $1+2+3+4+5=15$."),
        ("Rule out other lengths", r"Length $4$ would have average $15/4$, not halfway between two middle integers. Lengths $6$ or more already exceed $15$ if they start at $1$."),
        ("Count", r"There are $3$ valid sets."),
        ("Answer", r"The answer is $\boxed{3}$."),
    ],
    10: [
        ("Translate the square-root condition", r"For $\sqrt{120-x}$ to be an integer, the quantity $120-x$ must be a perfect square."),
        ("Use positivity of x", r"Because $x$ is a positive integer, we need $120-x\ge0$, so the square can be $0^2,1^2,2^2,\ldots,10^2$."),
        ("Count the squares", r"The next square, $11^2=121$, would make $x=120-121=-1$, which is not positive. So there are $11$ possible squares, from $0^2$ through $10^2$."),
        ("Get x values", r"Each square gives exactly one value $x=120-k^2$."),
        ("Answer", r"There are $\boxed{11}$ possible positive integer values of $x$."),
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
        + "本批完成 2006 AMC 10A Problems 1-6 和 8-10；Problem 7 因图形依赖跳过。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
