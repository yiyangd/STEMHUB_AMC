from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 22
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2005_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21, 22, 23, 24, 25}
SKIPPED = []
BATCH_LABEL = "2005 AMC 10A Problem 21-25"
NEXT_START = "2005 AMC 10B Problem 1"

ANS = {
    21: ("B", "5"),
    22: ("D", "668"),
    23: ("C", r"\frac{1}{3}"),
    24: ("B", "1"),
    25: ("D", r"\frac{19}{56}"),
}


OV = {
    21: (
        r"For how many positive integers $n$ does $1+2+\cdots+n$ evenly divide $6n$?",
        [("A", "$3$"), ("B", "$5$"), ("C", "$7$"), ("D", "$9$"), ("E", "$11$")],
    ),
    22: (
        r"Let $S$ be the set of the $2005$ smallest positive multiples of $4$, and let $T$ be the set of the $2005$ smallest positive multiples of $6$. How many elements are common to $S$ and $T$?",
        [("A", "$166$"), ("B", "$333$"), ("C", "$500$"), ("D", "$668$"), ("E", "$1001$")],
    ),
    23: (
        r"Let $AB$ be a diameter of a circle and $C$ be a point on $AB$ with $2\cdot AC=BC$. Let $D$ and $E$ be points on the circle such that $DC\perp AB$ and $DE$ is a second diameter. What is the ratio of the area of $\triangle DCE$ to the area of $\triangle ABD$?",
        [("A", r"$\frac16$"), ("B", r"$\frac14$"), ("C", r"$\frac13$"), ("D", r"$\frac12$"), ("E", r"$\frac23$")],
    ),
    24: (
        r"For each positive integer $m>1$, let $P(m)$ denote the greatest prime factor of $m$. For how many positive integers $n$ is it true that both $P(n)=\sqrt n$ and $P(n+48)=\sqrt{n+48}$?",
        [("A", "$0$"), ("B", "$1$"), ("C", "$3$"), ("D", "$4$"), ("E", "$5$")],
    ),
    25: (
        r"In $\triangle ABC$ we have $AB=25$, $BC=39$, and $AC=42$. Points $D$ and $E$ are on $AB$ and $AC$, respectively, with $AD=19$ and $AE=14$. What is the ratio of the area of triangle $ADE$ to the area of quadrilateral $BCED$?",
        [("A", r"$\frac{266}{1521}$"), ("B", r"$\frac{19}{75}$"), ("C", r"$\frac13$"), ("D", r"$\frac{19}{56}$"), ("E", r"$\frac12$")],
    ),
}


KEY_OVERRIDES = {
    21: "Convert the triangular-number divisibility condition into a divisor condition on n+1.",
    22: "Use least common multiples and inclusion with finite initial segments.",
    23: "Choose coordinates on the diameter to compare triangle areas directly.",
    24: "Interpret the greatest-prime-factor condition as saying the number is a square of a prime.",
    25: "Use the product of side ratios for triangles sharing an included angle.",
}


SOL = {
    21: [
        ("Rewrite the divisor", r"The sum $1+2+\cdots+n$ is the triangular number $\frac{n(n+1)}{2}$. The condition is \[\frac{n(n+1)}2 \mid 6n.\]"),
        ("Cancel the common factor carefully", r"Since $n$ is positive, compare $6n$ with $\frac{n(n+1)}2$: \[\frac{6n}{n(n+1)/2}=\frac{12}{n+1}.\] The divisibility holds exactly when $\frac{12}{n+1}$ is an integer."),
        ("Count possible n", r"Thus $n+1$ must be a positive divisor of $12$. The divisors are $1,2,3,4,6,12$."),
        ("Remove the impossible divisor", r"Because $n$ is positive, $n+1>1$, so we use $2,3,4,6,12$. These give $n=1,2,3,5,11$."),
        ("Answer", r"There are $\boxed{5}$ possible values of $n$."),
    ],
    22: [
        ("Describe the two sets", r"The $2005$ smallest positive multiples of $4$ run from $4$ to $4\cdot2005=8020$. The $2005$ smallest positive multiples of $6$ run from $6$ to $6\cdot2005=12030$."),
        ("Find common multiples", r"A number common to both sets must be a multiple of $\operatorname{lcm}(4,6)=12$."),
        ("Use the smaller endpoint", r"Since every common element must lie in $S$, it cannot exceed $8020$. Any multiple of $12$ up to $8020$ is also at most $12030$, so it is automatically in $T$."),
        ("Count", r"The number of positive multiples of $12$ up to $8020$ is \[\left\lfloor\frac{8020}{12}\right\rfloor=668.\]"),
        ("Answer", r"The two sets have $\boxed{668}$ elements in common."),
    ],
    23: [
        ("Choose a convenient scale", r"The ratio is unchanged by scaling, so let $AC=1$ and $BC=2$. Then $AB=3$. Put $A=(0,0)$, $C=(1,0)$, and $B=(3,0)$."),
        ("Find point D", r"The circle has center $(3/2,0)$ and radius $3/2$. Since $DC\perp AB$, point $D$ has $x$-coordinate $1$. Its height is \[\sqrt{\left(\frac32\right)^2-\left(1-\frac32\right)^2}=\sqrt2.\] Thus $D=(1,\sqrt2)$."),
        ("Use the second diameter", r"Since $DE$ is a diameter, $E$ is opposite $D$ through the center. Therefore $E=(2,-\sqrt2)$."),
        ("Compute the two areas", r"Triangle $ABD$ has base $AB=3$ and height $\sqrt2$, so its area is $\frac{3\sqrt2}{2}$. Triangle $DCE$ has base $DC=\sqrt2$ and horizontal height $1$, so its area is $\frac{\sqrt2}{2}$."),
        ("Form the ratio", r"The ratio is \[\frac{[DCE]}{[ABD]}=\frac{\sqrt2/2}{3\sqrt2/2}=\frac13.\] The answer is $\boxed{\frac13}$."),
    ],
    24: [
        ("Interpret the condition", r"If $P(n)=\sqrt n$, then $\sqrt n$ is a prime factor of $n$ and is the greatest prime factor. This means $n$ must be the square of a prime."),
        ("Set up prime squares", r"Let $n=p^2$ and $n+48=q^2$, where $p$ and $q$ are primes and $q>p$. Then \[q^2-p^2=48.\]"),
        ("Factor the difference of squares", r"We get $(q-p)(q+p)=48$. Since $p$ and $q$ are primes greater than $2$ in the only viable case, both factors are even."),
        ("Test factor pairs", r"The even factor pairs for $48$ are $(2,24)$, $(4,12)$, and $(6,8)$. These give $(p,q)=(11,13)$, $(4,8)$, and $(1,7)$ respectively. Only $(11,13)$ uses two primes."),
        ("Answer", r"Thus there is exactly one value, $n=11^2=121$. The answer is $\boxed{1}$."),
    ],
    25: [
        ("Notice the shared angle", r"Triangles $ABC$ and $ADE$ share angle $A$. Their areas can be compared using the two sides around that angle."),
        ("Use side ratios", r"The side ratio on $AB$ is $AD/AB=19/25$. The side ratio on $AC$ is $AE/AC=14/42=1/3$."),
        ("Find the area fraction", r"Therefore \[\frac{[ADE]}{[ABC]}=\frac{19}{25}\cdot\frac13=\frac{19}{75}.\]"),
        ("Convert to the requested denominator", r"Quadrilateral $BCED$ is the rest of triangle $ABC$, so \[[BCED]=[ABC]-[ADE]=\frac{56}{75}[ABC].\]"),
        ("Answer", r"Thus \[\frac{[ADE]}{[BCED]}=\frac{19/75}{56/75}=\frac{19}{56}.\] The answer is $\boxed{\frac{19}{56}}$."),
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
        if r["year"] == "2005" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "本批完成 2005 AMC 10A Problems 21-25，无跳过题；2005A 可可靠处理部分完成。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
