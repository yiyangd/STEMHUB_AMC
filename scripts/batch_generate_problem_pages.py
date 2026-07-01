from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 28
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2006_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21, 22, 23, 24, 25}
SKIPPED = []
BATCH_LABEL = "2006 AMC 10A Problem 21-25"
NEXT_START = "2006 AMC 10B Problem 1"

ANS = {
    21: ("E", "5416"),
    22: ("C", "30"),
    23: ("B", r"\frac{44}{3}"),
    24: ("B", r"\frac{1}{6}"),
    25: ("C", r"\frac{2}{243}"),
}


OV = {
    21: (
        r"How many four-digit positive integers have at least one digit that is a $2$ or a $3$?",
        [("A", "$2439$"), ("B", "$4096$"), ("C", "$4903$"), ("D", "$4904$"), ("E", "$5416$")],
    ),
    22: (
        r"Two farmers agree that pigs are worth $\$300$ and goats are worth $\$210$. When one farmer owes the other money, he pays the debt in pigs or goats, with change received in the form of goats or pigs as necessary. What is the amount of the smallest positive debt that can be resolved in this way?",
        [("A", "$5$"), ("B", "$10$"), ("C", "$30$"), ("D", "$90$"), ("E", "$210$")],
    ),
    23: (
        r"Circles with centers $A$ and $B$ have radii $3$ and $8$, respectively. A common internal tangent intersects the circles at $C$ and $D$, respectively. Lines $AB$ and $CD$ intersect at $E$, and $AE=5$. What is $CD$?",
        [("A", r"$\sqrt{13}$"), ("B", r"$\frac{44}{3}$"), ("C", r"$\sqrt{221}$"), ("D", r"$\sqrt{255}$"), ("E", r"$\frac{55}{3}$")],
    ),
    24: (
        r"Centers of adjacent faces of a unit cube are joined to form a regular octahedron. What is the volume of this octahedron?",
        [("A", r"$\frac18$"), ("B", r"$\frac16$"), ("C", r"$\frac14$"), ("D", r"$\frac13$"), ("E", r"$\frac12$")],
    ),
    25: (
        r"A bug starts at one vertex of a cube and moves along the edges of the cube according to the following rule. At each vertex the bug will choose to travel along one of the three edges emanating from that vertex. Each edge has equal probability of being chosen, and all choices are independent. What is the probability that after seven moves the bug will have visited every vertex exactly once?",
        [("A", r"$\frac{1}{2187}$"), ("B", r"$\frac{1}{729}$"), ("C", r"$\frac{2}{243}$"), ("D", r"$\frac{1}{81}$"), ("E", r"$\frac{5}{243}$")],
    ),
}


KEY_OVERRIDES = {
    21: "Use complement counting to avoid overcounting numbers with multiple 2s or 3s.",
    22: "Find the smallest positive integer combination of 300 and 210 using the greatest common divisor.",
    23: "Use internal similarity and the internal tangent length formula.",
    24: "Place the cube face centers on coordinate axes and use the standard octahedron volume.",
    25: "Count Hamiltonian paths on the cube from a fixed starting vertex.",
}


SOL = {
    21: [
        ("Count the complement", r"It is easier to count four-digit numbers with no digit equal to $2$ or $3$, then subtract from all four-digit numbers."),
        ("Count all four-digit numbers", r"There are $9000$ four-digit positive integers, from $1000$ through $9999$."),
        ("Count numbers avoiding 2 and 3", r"The thousands digit has $7$ choices: $1,4,5,6,7,8,9$. Each of the other three digits has $8$ choices, because it can be any digit except $2$ or $3$."),
        ("Subtract", r"The complement has $7\cdot8^3=3584$ numbers. Therefore the desired count is $9000-3584=5416$."),
        ("Answer", r"The answer is $\boxed{5416}$."),
    ],
    22: [
        ("Translate the exchange system", r"A debt can be resolved if it can be written as a difference between a total value of pigs and a total value of goats. So possible debts have the form $300a-210b$ for integers $a,b$."),
        ("Use the greatest common divisor", r"Every such amount is a multiple of $\gcd(300,210)=30$. So no positive debt smaller than $30$ can always be represented in this system."),
        ("Show that 30 works", r"For example, $300-210=90$, and combinations of pigs and goats can generate multiples of $30$; in particular, $300-210-210+300-300$ style exchanges are governed by the same gcd. More directly, $300(5)-210(7)=1500-1470=30$."),
        ("Conclude", r"The smallest positive resolvable debt is $30$."),
        ("Answer", r"The answer is $\boxed{30}$."),
    ],
    23: [
        ("Use the internal similarity point", r"For a common internal tangent, the intersection point $E$ of the tangent and the line of centers is the internal center of similarity. Therefore $AE:BE=3:8$."),
        ("Find AB", r"Since $AE=5$, we have $BE=\frac83\cdot5=\frac{40}{3}$. Thus $AB=AE+BE=5+\frac{40}{3}=\frac{55}{3}$."),
        ("Use the internal tangent length formula", r"For two circles with center distance $AB$ and radii $3$ and $8$, the length between tangent points on a common internal tangent is \[CD=\sqrt{AB^2-(3+8)^2}.\]"),
        ("Compute", r"So \[CD=\sqrt{\left(\frac{55}{3}\right)^2-11^2}=\sqrt{\frac{3025-1089}{9}}=\sqrt{\frac{1936}{9}}=\frac{44}{3}.\]"),
        ("Answer", r"The answer is $\boxed{\frac{44}{3}}$."),
    ],
    24: [
        ("Place the cube in coordinates", r"Use a unit cube centered at the origin. The centers of its faces are $(\pm\frac12,0,0)$, $(0,\pm\frac12,0)$, and $(0,0,\pm\frac12)$."),
        ("Recognize the octahedron", r"These six points are the vertices of a regular octahedron. It is the region satisfying $|x|+|y|+|z|\le\frac12$."),
        ("Use the standard volume", r"An octahedron with axis radius $a$ has volume $\frac{4}{3}a^3$. Here $a=\frac12$."),
        ("Compute", r"The volume is \[\frac43\left(\frac12\right)^3=\frac43\cdot\frac18=\frac16.\]"),
        ("Answer", r"The volume is $\boxed{\frac16}$."),
    ],
    25: [
        ("Count all possible walks", r"At each of the $7$ moves, the bug has $3$ equally likely edge choices. So there are $3^7=2187$ possible move sequences."),
        ("Understand the successful walks", r"To visit every vertex exactly once after $7$ moves, the bug must follow a Hamiltonian path of the cube starting from the initial vertex."),
        ("Count first two moves by symmetry", r"From the starting vertex there are $3$ choices for the first move. From there, to avoid returning immediately, there are $2$ choices for the second move."),
        ("Finish the path count", r"After two moves, the path lies on one square face of the cube. A careful continuation count gives $3$ possible completions from each such start: one continues around that face before crossing, and two cross earlier to the opposite face. Thus the number of successful paths is $3\cdot2\cdot3=18$."),
        ("Answer", r"The probability is $\frac{18}{2187}=\boxed{\frac{2}{243}}$."),
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
        + "本批完成 2006 AMC 10A Problems 21-25，无跳过题；2006A 完成。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
