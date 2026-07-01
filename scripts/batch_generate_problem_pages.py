from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 37
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2007_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21, 22, 23, 24, 25}
SKIPPED = []
BATCH_LABEL = "2007 AMC 10B Problems 21-25"
NEXT_START = "2008 AMC 10A Problem 1"

ANS = {
    21: ("B", r"\frac{60}{37}"),
    22: ("B", r"-\frac{1}{16}"),
    23: ("E", r"4+2\sqrt2"),
    24: ("C", "4944"),
    25: ("A", "4"),
}


OV = {
    21: (r"Right $\triangle ABC$ has $AB=3$, $BC=4$, and $AC=5$. Square $XYZW$ is inscribed in $\triangle ABC$ with $X$ and $Y$ on $AC$, $W$ on $AB$, and $Z$ on $BC$. What is the side length of the square?", [("A", r"$\frac32$"), ("B", r"$\frac{60}{37}$"), ("C", r"$\frac{12}{7}$"), ("D", r"$\frac{23}{13}$"), ("E", "$2$")]),
    22: (r"A player chooses one of the numbers $1$ through $4$. After the choice has been made, two regular four-sided tetrahedral dice are rolled, with the sides numbered $1$ through $4$. If the number chosen appears on the bottom of exactly one die, the player wins $\$1$. If it appears on the bottom of both dice, the player wins $\$2$. If it does not appear on the bottom of either die, the player loses $\$1$. What is the expected return to the player, in dollars, for one roll of the dice?", [("A", r"$-\frac18$"), ("B", r"$-\frac1{16}$"), ("C", "$0$"), ("D", r"$\frac1{16}$"), ("E", r"$\frac18$")]),
    23: (r"A pyramid with a square base is cut by a plane that is parallel to its base and is $2$ units from the base. The surface area of the smaller pyramid that is cut from the top is half the surface area of the original pyramid. What is the altitude of the original pyramid?", [("A", "$2$"), ("B", r"$2+\sqrt2$"), ("C", r"$1+2\sqrt2$"), ("D", "$4$"), ("E", r"$4+2\sqrt2$")]),
    24: (r"Let $n$ denote the smallest positive integer that is divisible by both $4$ and $9$, and whose base-$10$ representation consists only of $4$'s and $9$'s, with at least one of each. What are the last four digits of $n$?", [("A", "$4444$"), ("B", "$4494$"), ("C", "$4944$"), ("D", "$9444$"), ("E", "$9944$")]),
    25: (r"How many pairs of positive integers $(a,b)$ are there such that $\gcd(a,b)=1$ and $\frac{a}{b}+\frac{14b}{9a}$ is an integer?", [("A", "$4$"), ("B", "$6$"), ("C", "$9$"), ("D", "$12$"), ("E", "infinitely many")]),
}


KEY_OVERRIDES = {
    21: "Use similar triangles: the width parallel to the hypotenuse decreases linearly with distance from the hypotenuse.",
    22: "Compute expected value by separating exactly-one, both, and neither outcomes.",
    23: "Surface areas of similar pyramids scale as the square of the linear scale factor.",
    24: "Use divisibility by 4 and 9 together with smallest-number digit placement.",
    25: "Use coprimality to force divisibility conditions on a and b, then check the finite candidates.",
}


SOL = {
    21: [("Use the hypotenuse as the base", r"The square has one side $XY$ on the hypotenuse $AC$, so it is natural to view the triangle with base $AC=5$. The altitude from the right angle to the hypotenuse is $\frac{3\cdot4}{5}=\frac{12}{5}$."), ("Let the square side be s", r"The side $WZ$ of the square is parallel to $AC$ and lies $s$ units away from $AC$. A cross-section parallel to the hypotenuse shrinks linearly as we move toward vertex $B$."), ("Set up similarity", r"At distance $s$ from the hypotenuse, the available width is $5\left(1-\frac{s}{12/5}\right)$. This width must equal the square side length $s$."), ("Solve", r"So $s=5\left(1-\frac{5s}{12}\right)=5-\frac{25s}{12}$. Thus $\frac{37s}{12}=5$, and $s=\frac{60}{37}$."), ("Answer", r"The side length is $\boxed{\frac{60}{37}}$." )],
    22: [("Focus on the chosen number", r"The player chooses a number first, but by symmetry every chosen number has the same probabilities. For each die, the chance that the chosen number appears on the bottom is $\frac14$."), ("Compute exactly one match", r"Exactly one die shows the chosen number with probability $2\cdot\frac14\cdot\frac34=\frac38$. This pays $1$ dollar."), ("Compute two matches", r"Both dice show the chosen number with probability $\frac14\cdot\frac14=\frac1{16}$. This pays $2$ dollars."), ("Compute no matches", r"Neither die shows the chosen number with probability $\frac34\cdot\frac34=\frac9{16}$. This loses $1$ dollar."), ("Find expected value", r"The expected return is $1\cdot\frac38+2\cdot\frac1{16}-1\cdot\frac9{16}=\frac6{16}+\frac2{16}-\frac9{16}=-\frac1{16}$."), ("Answer", r"The expected return is $\boxed{-\frac1{16}}$ dollars." )],
    23: [("Use similarity", r"The cutting plane is parallel to the base, so the small top pyramid is similar to the original pyramid."), ("Convert surface-area ratio to length ratio", r"The smaller pyramid has half the surface area of the original. Surface area scales as the square of the linear scale factor, so the linear scale factor is $\frac{1}{\sqrt2}$."), ("Relate altitudes", r"Let the original altitude be $H$. Since the plane is $2$ units above the base, the smaller top pyramid has altitude $H-2$. Therefore $\frac{H-2}{H}=\frac1{\sqrt2}$."), ("Solve for H", r"We have $H-2=\frac{H}{\sqrt2}$, so $H\left(1-\frac1{\sqrt2}\right)=2$. Hence $H=\frac{2}{1-1/\sqrt2}=4+2\sqrt2$."), ("Answer", r"The altitude is $\boxed{4+2\sqrt2}$." )],
    24: [("Use divisibility by 4", r"A number is divisible by $4$ if its last two digits form a number divisible by $4$. With digits only $4$ and $9$, the possible endings are $44,49,94,99$, and only $44$ is divisible by $4$."), ("Use divisibility by 9", r"A number is divisible by $9$ when its digit sum is divisible by $9$. If the number has $t$ digits equal to $4$ and the rest equal to $9$, its digit sum is congruent to $4t$ modulo $9$. Thus $t$ must be a multiple of $9$."), ("Make the number as short as possible", r"The number must contain at least one $9$, so it cannot have exactly nine digits all equal to $4$. The shortest possibility has ten digits: nine $4$'s and one $9$."), ("Make the number as small as possible", r"To make the ten-digit number as small as possible, put the single $9$ as far to the right as possible, but the last two digits must be $44$. So the ending is $4944$."), ("Answer", r"The last four digits are $\boxed{4944}$." )],
    25: [("Start from the integer condition", r"We need $\frac{a}{b}+\frac{14b}{9a}$ to be an integer, with $\gcd(a,b)=1$. Combining fractions gives $\frac{9a^2+14b^2}{9ab}$."), ("Use divisibility by b", r"For this fraction to be an integer, $b$ must divide the numerator. Modulo $b$, the numerator is congruent to $9a^2$. Since $\gcd(a,b)=1$, this forces $b\mid9$."), ("Use divisibility by a", r"Similarly, modulo $a$, the numerator is congruent to $14b^2$. Since $\gcd(a,b)=1$, this forces $a\mid14$."), ("Check finite candidates", r"Thus $a\in\{1,2,7,14\}$ and $b\in\{1,3,9\}$, with $\gcd(a,b)=1$. Checking these finite possibilities in the original expression leaves four pairs: $(1,9),(2,9),(7,1),(14,1)$."), ("Answer", r"There are $\boxed{4}$ pairs." )],
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
        if r["year"] == "2007" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Review notes: Problem 25 statement corrected from OCR using AoPS reference.\n",
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
        + "- Answer verification source: AoPS 2007 AMC 10B Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批无跳过题；Problem 25 已根据 AoPS 修正 OCR 漏掉的分数线。\n"
        + "2007 AMC 10B 已完成可可靠生成部分。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
