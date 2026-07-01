from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 33
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2007_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11, 12, 13, 14, 16, 17, 20}
SKIPPED = [
    "2007 AMC 10A Problem 15 skipped: statement depends on a diagram.",
    "2007 AMC 10A Problem 18 skipped: statement depends on a diagram.",
    "2007 AMC 10A Problem 19 skipped: statement depends on a diagram.",
]
BATCH_LABEL = "2007 AMC 10A Problems 11-14, 16, 17, 20"
NEXT_START = "2007 AMC 10A Problem 21"

ANS = {
    11: ("C", "18"),
    12: ("D", "62"),
    13: ("B", r"\frac{3}{4}"),
    14: ("A", "8.64"),
    16: ("E", r"\frac{5}{8}"),
    17: ("D", "60"),
    20: ("D", "194"),
}


OV = {
    11: (r"The numbers from $1$ to $8$ are placed at the vertices of a cube in such a manner that the sum of the four numbers on each face is the same. What is this common sum?", [("A", "$14$"), ("B", "$16$"), ("C", "$18$"), ("D", "$20$"), ("E", "$24$")]),
    12: (r"Two tour guides are leading six tourists. The guides decide to split up. Each tourist must choose one of the guides, but with the stipulation that each guide must take at least one tourist. How many different groupings of guides and tourists are possible?", [("A", "$56$"), ("B", "$58$"), ("C", "$60$"), ("D", "$62$"), ("E", "$64$")]),
    13: (r"Yan is somewhere between his home and the stadium. To get to the stadium he can walk directly to the stadium, or else he can walk home and then ride his bicycle to the stadium. He rides $7$ times as fast as he walks, and both choices require the same amount of time. What is the ratio of Yan's distance from his home to his distance from the stadium?", [("A", r"$\frac23$"), ("B", r"$\frac34$"), ("C", r"$\frac45$"), ("D", r"$\frac56$"), ("E", r"$\frac67$")]),
    14: (r"A triangle with side lengths in the ratio $3:4:5$ is inscribed in a circle of radius $3$. What is the area of the triangle?", [("A", "$8.64$"), ("B", "$12$"), ("C", r"$5\pi$"), ("D", "$17.28$"), ("E", "$18$")]),
    16: (r"Integers $a,b,c,$ and $d$, not necessarily distinct, are chosen independently and at random from $0$ to $2007$, inclusive. What is the probability that $ad-bc$ is even?", [("A", r"$\frac38$"), ("B", r"$\frac7{16}$"), ("C", r"$\frac12$"), ("D", r"$\frac9{16}$"), ("E", r"$\frac58$")]),
    17: (r"Suppose that $m$ and $n$ are positive integers such that $75m=n^3$. What is the minimum possible value of $m+n$?", [("A", "$15$"), ("B", "$30$"), ("C", "$50$"), ("D", "$60$"), ("E", "$5700$")]),
    20: (r"Suppose that the number $a$ satisfies the equation $4=a+a^{-1}$. What is the value of $a^4+a^{-4}$?", [("A", "$164$"), ("B", "$172$"), ("C", "$192$"), ("D", "$194$"), ("E", "$212$")]),
}


KEY_OVERRIDES = {
    11: "Double-count face sums on a cube: each vertex belongs to exactly three faces.",
    12: "Count all assignments to two guides, then subtract the two invalid all-one-guide cases.",
    13: "Translate equal travel times into an equation using distance and speed.",
    14: "Recognize the 3-4-5 triangle as right and use the circumradius as half the hypotenuse.",
    16: "Use parity: a product is odd exactly when both factors are odd.",
    17: "Use prime exponents to make 75m a perfect cube with minimum n.",
    20: "Use repeated squaring on a+a^{-1} to get a^4+a^{-4} without solving for a.",
}


SOL = {
    11: [("Count total vertex value", r"The numbers at the vertices are $1$ through $8$, whose sum is $36$."), ("Double-count face sums", r"There are $6$ faces, each with common sum $S$, so the total of all face sums is $6S$."), ("Notice how often each vertex is counted", r"Each vertex of a cube lies on exactly $3$ faces. Therefore, when all face sums are added, each vertex number is counted $3$ times."), ("Solve for the common sum", r"Thus $6S=3\cdot36=108$, so $S=18$."), ("Answer", r"The common face sum is $\boxed{18}$." )],
    12: [("Start with all choices", r"Each of the $6$ tourists has $2$ choices: guide 1 or guide 2. That gives $2^6=64$ assignments."), ("Remove invalid assignments", r"The only invalid cases are when all tourists choose the first guide or all tourists choose the second guide. In those cases, one guide has no tourists."), ("Subtract", r"So the number of valid groupings is $64-2=62$."), ("Check interpretation", r"The guides are distinct people, so assigning a particular tourist to guide 1 is different from assigning that tourist to guide 2."), ("Answer", r"The answer is $\boxed{62}$." )],
    13: [("Define the two distances", r"Let $x$ be Yan's distance from home, and let $y$ be his distance from the stadium. We want the ratio $x:y$."), ("Compare times", r"Walking directly to the stadium takes time proportional to $y$. Walking home takes time proportional to $x$, and then biking from home to the stadium, a distance $x+y$, takes time proportional to $\frac{x+y}{7}$."), ("Set the times equal", r"Since both choices take the same time, $y=x+\frac{x+y}{7}$. Multiplying by $7$ gives $7y=7x+x+y$."), ("Solve the ratio", r"So $6y=8x$, which gives $\frac{x}{y}=\frac{6}{8}=\frac34$."), ("Answer", r"The answer is $\boxed{\frac34}$." )],
    14: [("Recognize the triangle type", r"A triangle with side ratio $3:4:5$ is a right triangle, with the side corresponding to $5$ as the hypotenuse."), ("Use the circumradius", r"For a right triangle, the hypotenuse is the diameter of the circumcircle. The circle radius is $3$, so the diameter and hypotenuse are $6$."), ("Find the scale factor", r"If the hypotenuse is $5k=6$, then $k=\frac65$. The legs are $3k=\frac{18}{5}$ and $4k=\frac{24}{5}$."), ("Compute the area", r"The area is $\frac12\cdot\frac{18}{5}\cdot\frac{24}{5}=\frac{216}{25}=8.64$."), ("Answer", r"The answer is $\boxed{8.64}$." )],
    16: [("Reduce to parity", r"The expression $ad-bc$ is even exactly when $ad$ and $bc$ have the same parity."), ("Find product parity", r"From $0$ to $2007$ there are equally many even and odd integers: $1004$ each. A product is odd only if both factors are odd, so $P(ad\text{ odd})=\frac12\cdot\frac12=\frac14$. Thus $P(ad\text{ even})=\frac34$."), ("Match the two parities", r"The products $ad$ and $bc$ are independent and have the same parity distribution. The probability they match is $\left(\frac14\right)^2+\left(\frac34\right)^2$."), ("Compute", r"This is $\frac1{16}+\frac9{16}=\frac{10}{16}=\frac58$."), ("Answer", r"The answer is $\boxed{\frac58}$." )],
    17: [("Factor the condition", r"The equation $75m=n^3$ means $75m$ must be a perfect cube. Since $75=3\cdot5^2$, the prime exponents in $75m$ must all become multiples of $3$."), ("Choose the smallest possible $n$", r"For $n^3$ to be divisible by $75$, $n$ must contain at least one factor of $3$ and one factor of $5$. The smallest such $n$ is $15$."), ("Find the corresponding $m$", r"With $n=15$, we have $n^3=3375$. Then $m=\frac{3375}{75}=45$."), ("Compute the sum", r"So $m+n=45+15=60$."), ("Answer", r"The minimum possible value is $\boxed{60}$." )],
    20: [("Use the given symmetric expression", r"We are given $a+a^{-1}=4$. Expressions like $a^4+a^{-4}$ can be reached by squaring, without solving for $a$."), ("Square once", r"$(a+a^{-1})^2=a^2+2+a^{-2}=16$, so $a^2+a^{-2}=14$."), ("Square again", r"Now square $a^2+a^{-2}$: $(a^2+a^{-2})^2=a^4+2+a^{-4}=14^2=196$."), ("Subtract the middle term", r"Therefore $a^4+a^{-4}=196-2=194$."), ("Answer", r"The answer is $\boxed{194}$." )],
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
        if r["year"] == "2007" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Review notes: Skipped Problems 15, 18, and 19 because they require diagrams.\n",
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
        + "- Answer verification source: AoPS 2007 AMC 10A Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批跳过 2007 AMC 10A Problems 15, 18, 19：题面依赖图形。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
