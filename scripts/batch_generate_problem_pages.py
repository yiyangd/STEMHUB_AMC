from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 36
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2007_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11, 12, 13, 14, 15, 16, 17, 20}
SKIPPED = [
    "2007 AMC 10B Problem 18 skipped: statement depends on a diagram.",
    "2007 AMC 10B Problem 19 skipped: statement depends on a spinner/checkerboard diagram.",
]
BATCH_LABEL = "2007 AMC 10B Problems 11-17, 20"
NEXT_START = "2007 AMC 10B Problem 21"

ANS = {
    11: ("C", r"\frac{81\pi}{32}"),
    12: ("D", "5"),
    13: ("D", r"2(\pi-2)"),
    14: ("C", "8"),
    15: ("D", "173"),
    16: ("C", "93"),
    17: ("D", r"4\sqrt3"),
    20: ("C", "600"),
}


OV = {
    11: (r"A circle passes through the three vertices of an isosceles triangle that has two sides of length $3$ and a base of length $2$. What is the area of this circle?", [("A", r"$2\pi$"), ("B", r"$\frac{5\pi}{2}$"), ("C", r"$\frac{81\pi}{32}$"), ("D", r"$3\pi$"), ("E", r"$\frac{7\pi}{2}$")]),
    12: (r"Tom's age is $T$ years, which is also the sum of the ages of his three children. His age $N$ years ago was twice the sum of their ages then. What is $\frac{T}{N}$?", [("A", "$2$"), ("B", "$3$"), ("C", "$4$"), ("D", "$5$"), ("E", "$6$")]),
    13: (r"Two circles of radius $2$ are centered at $(2,0)$ and at $(0,2)$. What is the area of the intersection of the interiors of the two circles?", [("A", r"$\pi-2$"), ("B", r"$\pi$"), ("C", r"$\frac{3\pi}{2}$"), ("D", r"$2(\pi-2)$"), ("E", r"$2\pi$")]),
    14: (r"Some boys and girls are having a car wash to raise money for a class trip to China. Initially $40\%$ of the group are girls. Shortly thereafter two girls leave and two boys arrive, and then $30\%$ of the group are girls. How many girls were initially in the group?", [("A", "$4$"), ("B", "$6$"), ("C", "$8$"), ("D", "$10$"), ("E", "$12$")]),
    15: (r"The angles of quadrilateral $ABCD$ satisfy $\angle A=2\angle B=3\angle C=4\angle D$. What is the degree measure of $\angle A$, rounded to the nearest whole number?", [("A", "$125$"), ("B", "$144$"), ("C", "$153$"), ("D", "$173$"), ("E", "$180$")]),
    16: (r"A teacher gave a test to a class in which $10\%$ of the students are juniors and $90\%$ are seniors. The average score on the test was $84$. The juniors all received the same score, and the average score of the seniors was $83$. What score did each of the juniors receive on the test?", [("A", "$85$"), ("B", "$88$"), ("C", "$93$"), ("D", "$94$"), ("E", "$98$")]),
    17: (r"Point $P$ is inside equilateral $\triangle ABC$. Points $Q,R,$ and $S$ are the feet of the perpendiculars from $P$ to $AB,BC,$ and $CA$, respectively. Given that $PQ=1$, $PR=2$, and $PS=3$, what is $AB$?", [("A", "$4$"), ("B", r"$3\sqrt3$"), ("C", "$6$"), ("D", r"$4\sqrt3$"), ("E", "$9$")]),
    20: (r"A set of $25$ square blocks is arranged into a $5\times5$ square. How many different combinations of $3$ blocks can be selected from that set so that no two are in the same row or column?", [("A", "$100$"), ("B", "$125$"), ("C", "$600$"), ("D", "$2300$"), ("E", "$3600$")]),
}


KEY_OVERRIDES = {
    11: "Find the circumradius of the isosceles triangle using area and side lengths.",
    12: "Compare current and past total ages, remembering that all three children age by N years.",
    13: "Compute the overlap of two equal circles using sectors minus triangles.",
    14: "Use the unchanged group size and percentage change to solve for the initial total.",
    15: "Express all angles in terms of angle A and use the quadrilateral angle sum.",
    16: "Use a weighted average to isolate the juniors' score.",
    17: "Apply Viviani's theorem: distances to the sides of an equilateral triangle sum to the altitude.",
    20: "Choose rows, choose columns, then match them with a permutation.",
}


SOL = {
    11: [("Find the triangle's height", r"The isosceles triangle has equal sides $3$ and base $2$. Dropping an altitude to the base splits the base into two segments of length $1$. The height is $\sqrt{3^2-1^2}=\sqrt8=2\sqrt2$."), ("Find the triangle area", r"The area is $K=\frac12\cdot2\cdot2\sqrt2=2\sqrt2$."), ("Use the circumradius formula", r"For a triangle with side lengths $a,b,c$ and area $K$, the circumradius is $R=\frac{abc}{4K}$. Here $a,b,c=3,3,2$, so $R=\frac{18}{4(2\sqrt2)}=\frac{9}{4\sqrt2}$."), ("Compute the circle area", r"Thus $R^2=\frac{81}{32}$, and the circle's area is $\pi R^2=\frac{81\pi}{32}$."), ("Answer", r"The answer is $\boxed{\frac{81\pi}{32}}$." )],
    12: [("Use current ages", r"Tom's current age is $T$, and the sum of his three children's current ages is also $T$."), ("Move N years back", r"$N$ years ago, Tom's age was $T-N$. Each of the three children was $N$ years younger, so the sum of their ages then was $T-3N$."), ("Translate the condition", r"The problem says $T-N=2(T-3N)$."), ("Solve for the ratio", r"Expanding gives $T-N=2T-6N$, so $T=5N$. Therefore $\frac{T}{N}=5$."), ("Answer", r"The answer is $\boxed{5}$." )],
    13: [("Find the distance between centers", r"The centers are $(2,0)$ and $(0,2)$, so their distance is $\sqrt{(2-0)^2+(0-2)^2}=2\sqrt2$."), ("Understand the overlap", r"Each circle has radius $2$. In each circle, the chord of intersection subtends a $90^\circ$ central angle because $\cos\theta=\frac{d}{2r}=\frac{2\sqrt2}{4}=\frac{\sqrt2}{2}$."), ("Compute one circular segment", r"One segment is a $90^\circ$ sector of radius $2$ minus an isosceles right triangle with legs $2$. The sector area is $\frac14\pi(2^2)=\pi$, and the triangle area is $2$."), ("Double the segment", r"The overlap consists of two such segments, so its area is $2(\pi-2)$."), ("Answer", r"The answer is $\boxed{2(\pi-2)}$." )],
    14: [("Let the group size be N", r"The total number of people does not change, because two girls leave and two boys arrive. Let the total be $N$."), ("Write the initial number of girls", r"Initially $40\%$ are girls, so the number of girls is $0.4N$."), ("Write the later number of girls", r"After two girls leave, the number of girls is $0.4N-2$. This is $30\%$ of the same total, so $0.4N-2=0.3N$."), ("Solve", r"Then $0.1N=2$, so $N=20$. The initial number of girls is $0.4\cdot20=8$."), ("Answer", r"The answer is $\boxed{8}$." )],
    15: [("Use one variable", r"Let $\angle A=x$. Since $x=2\angle B=3\angle C=4\angle D$, we have $\angle B=\frac{x}{2}$, $\angle C=\frac{x}{3}$, and $\angle D=\frac{x}{4}$."), ("Use the quadrilateral angle sum", r"The angles of a quadrilateral add to $360^\circ$, so $x+\frac{x}{2}+\frac{x}{3}+\frac{x}{4}=360$."), ("Combine fractions", r"The coefficient is $1+\frac12+\frac13+\frac14=\frac{25}{12}$, so $\frac{25}{12}x=360$."), ("Solve and round", r"Thus $x=360\cdot\frac{12}{25}=172.8$, which rounds to $173$."), ("Answer", r"The answer is $\boxed{173}$." )],
    16: [("Use a weighted average", r"Juniors make up $10\%$ of the class and seniors make up $90\%$. Let the junior score be $j$."), ("Set up the average", r"The class average is $84$, so $0.10j+0.90(83)=84$."), ("Solve", r"Since $0.90\cdot83=74.7$, we get $0.10j+74.7=84$, so $0.10j=9.3$ and $j=93$."), ("Check", r"A small group of juniors must score above $84$ to pull the senior average of $83$ up to $84$, so $93$ is reasonable."), ("Answer", r"The juniors each scored $\boxed{93}$." )],
    17: [("Recall the key property", r"In an equilateral triangle, the sum of the perpendicular distances from any interior point to the three sides equals the triangle's altitude. This is Viviani's theorem."), ("Find the altitude", r"Here the three distances are $1$, $2$, and $3$, so the altitude is $1+2+3=6$."), ("Relate altitude to side length", r"For an equilateral triangle with side length $s$, the altitude is $\frac{\sqrt3}{2}s$. Therefore $\frac{\sqrt3}{2}s=6$."), ("Solve", r"So $s=\frac{12}{\sqrt3}=4\sqrt3$."), ("Answer", r"The answer is $\boxed{4\sqrt3}$." )],
    20: [("Choose the rows", r"No two selected blocks can be in the same row, so first choose which $3$ of the $5$ rows will contain selected blocks. This can be done in $\binom53$ ways."), ("Choose the columns", r"Similarly, choose which $3$ of the $5$ columns will contain selected blocks. This can also be done in $\binom53$ ways."), ("Match rows to columns", r"Once the rows and columns are chosen, each selected row must be paired with a different selected column. There are $3!$ such matchings."), ("Compute", r"The number of combinations is $\binom53\binom53\cdot3!=10\cdot10\cdot6=600$."), ("Answer", r"The answer is $\boxed{600}$." )],
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
        + "- Review notes: Skipped Problems 18 and 19 because they require diagrams.\n",
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
        + "本批跳过 2007 AMC 10B Problems 18, 19：题面依赖图形。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
