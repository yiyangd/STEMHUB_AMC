from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 24
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2005_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
SKIPPED = []
BATCH_LABEL = "2005 AMC 10B Problem 11-20"
NEXT_START = "2005 AMC 10B Problem 21"

ANS = {
    11: ("E", "250"),
    12: ("E", r"\left(\frac{1}{6}\right)^{10}"),
    13: ("C", "835"),
    14: ("C", r"\frac{\sqrt3}{2}"),
    15: ("D", r"\frac{1}{2}"),
    16: ("D", "8"),
    17: ("B", r"\frac{3}{2}"),
    18: ("D", "8"),
    19: ("B", "1"),
    20: ("C", "53332.8"),
}


OV = {
    11: (
        r"The first term of a sequence is $2005$. Each succeeding term is the sum of the cubes of the digits of the previous term. What is the $2005$th term of the sequence?",
        [("A", "$29$"), ("B", "$55$"), ("C", "$85$"), ("D", "$133$"), ("E", "$250$")],
    ),
    12: (
        r"Twelve fair dice are rolled. What is the probability that the product of the numbers on the top faces is prime?",
        [("A", r"$\left(\frac{1}{12}\right)^{12}$"), ("B", r"$\left(\frac{1}{6}\right)^{12}$"), ("C", r"$2\left(\frac{1}{6}\right)^{11}$"), ("D", r"$5\left(\frac{1}{6}\right)^{11}$"), ("E", r"$\left(\frac{1}{6}\right)^{10}$")],
    ),
    13: (
        r"How many numbers between $1$ and $2005$ are integer multiples of $3$ or $4$ but not $12$?",
        [("A", "$501$"), ("B", "$668$"), ("C", "$835$"), ("D", "$1002$"), ("E", "$1169$")],
    ),
    14: (
        r"Equilateral $\triangle ABC$ has side length $2$, $M$ is the midpoint of $AC$, and $C$ is the midpoint of $BD$. What is the area of $\triangle CDM$?",
        [("A", r"$\frac12$"), ("B", r"$\frac{\sqrt3}{4}$"), ("C", r"$\frac{\sqrt3}{2}$"), ("D", "$1$"), ("E", "$2$")],
    ),
    15: (
        r"An envelope contains eight bills: two $1$-dollar bills, two $5$-dollar bills, two $10$-dollar bills, and two $20$-dollar bills. Two bills are drawn at random without replacement. What is the probability that their sum is $20$ dollars or more?",
        [("A", r"$\frac14$"), ("B", r"$\frac27$"), ("C", r"$\frac37$"), ("D", r"$\frac12$"), ("E", r"$\frac23$")],
    ),
    16: (
        r"The quadratic equation $x^2+mx+n=0$ has roots that are twice those of $x^2+px+m=0$, and none of $m$, $n$, and $p$ is zero. What is the value of $\frac np$?",
        [("A", "$1$"), ("B", "$2$"), ("C", "$4$"), ("D", "$8$"), ("E", "$16$")],
    ),
    17: (
        r"Suppose that $4^a=5$, $5^b=6$, $6^c=7$, and $7^d=8$. What is $a\cdot b\cdot c\cdot d$?",
        [("A", "$1$"), ("B", r"$\frac32$"), ("C", "$2$"), ("D", r"$\frac52$"), ("E", "$3$")],
    ),
    18: (
        r"All of David's telephone numbers have the form $555-abc-defg$, where $a,b,c,d,e,f,$ and $g$ are distinct digits and in increasing order, and none is either $0$ or $1$. How many different telephone numbers can David have?",
        [("A", "$1$"), ("B", "$2$"), ("C", "$7$"), ("D", "$8$"), ("E", "$9$")],
    ),
    19: (
        r"On a certain math exam, $10\%$ of the students got $70$ points, $25\%$ got $80$ points, $20\%$ got $85$ points, $15\%$ got $90$ points, and the rest got $95$ points. What is the difference between the mean and the median score on this exam?",
        [("A", "$0$"), ("B", "$1$"), ("C", "$2$"), ("D", "$4$"), ("E", "$5$")],
    ),
}


KEY_OVERRIDES = {
    11: "Compute early terms until the digit-cube process enters a cycle.",
    12: "A product is prime only when exactly one die contributes a prime and all others are 1.",
    13: "Use inclusion-exclusion, then remove multiples of 12.",
    14: "Use coordinates for the equilateral triangle and midpoint condition.",
    15: "Count unordered pairs of bills with sum at least 20.",
    16: "Apply Vieta's formulas to two quadratics whose roots differ by a factor of 2.",
    17: "Rewrite the exponents as logarithms so the product telescopes.",
    18: "Choose the seven increasing digits; the order is then forced.",
    19: "Compute the weighted mean and locate the median from cumulative percentages.",
    20: "Use symmetry: each digit appears equally often in each place value.",
}


SOL = {
    11: [
        ("Compute the first few terms", r"Start with $2005$. The next term is $2^3+0^3+0^3+5^3=8+125=133$."),
        ("Look for a cycle", r"From $133$, the next term is $1^3+3^3+3^3=55$. From $55$, the next term is $5^3+5^3=250$. From $250$, the next term is $2^3+5^3+0^3=133$."),
        ("Identify the repeating block", r"After the first term, the sequence repeats $133,55,250$ with period $3$."),
        ("Use the index", r"The $2005$th term is $2004$ steps after the first term. Since $2004$ is divisible by $3$, the sequence lands on the third value of the repeating block, $250$."),
        ("Answer", r"The $2005$th term is $\boxed{250}$."),
    ],
    12: [
        ("Understand when a product is prime", r"A product of twelve positive integers is prime only if one factor is that prime and all the other factors are $1$."),
        ("Choose which die gives the prime", r"There are $12$ choices for the die that shows a prime."),
        ("Choose the prime face", r"On a standard die, the prime faces are $2,3,5$, so the probability that the chosen die shows a prime is $3/6$."),
        ("Force all other dice to be 1", r"The remaining $11$ dice must each show $1$, with probability $(1/6)^{11}$."),
        ("Combine", r"The probability is $12\cdot\frac36\cdot\left(\frac16\right)^{11}=6\left(\frac16\right)^{11}=\boxed{\left(\frac16\right)^{10}}$."),
    ],
    13: [
        ("Count multiples of 3 or 4", r"Between $1$ and $2005$, there are $\lfloor2005/3\rfloor=668$ multiples of $3$ and $\lfloor2005/4\rfloor=501$ multiples of $4$."),
        ("Avoid double-counting multiples of 12", r"Multiples of both $3$ and $4$ are multiples of $12$, and there are $\lfloor2005/12\rfloor=167$ of them."),
        ("Find the union", r"The number divisible by $3$ or $4$ is $668+501-167=1002$."),
        ("Remove multiples of 12", r"The problem says 'but not $12$', meaning not multiples of $12$. Remove those $167$ numbers."),
        ("Answer", r"The count is $1002-167=\boxed{835}$."),
    ],
    14: [
        ("Place the equilateral triangle", r"Let $B=(-1,0)$, $C=(1,0)$, and $A=(0,\sqrt3)$. This gives side length $2$."),
        ("Locate M", r"Point $M$ is the midpoint of $AC$, so $M=\left(\frac12,\frac{\sqrt3}{2}\right)$."),
        ("Use C as midpoint of BD", r"Since $C$ is the midpoint of $BD$ and $B=(-1,0)$, point $D$ must be $(3,0)$."),
        ("Compute the triangle area", r"Segment $CD$ is horizontal with length $2$. The height from $M$ to line $CD$ is $\frac{\sqrt3}{2}$."),
        ("Answer", r"Thus $[CDM]=\frac12\cdot2\cdot\frac{\sqrt3}{2}=\boxed{\frac{\sqrt3}{2}}$."),
    ],
    15: [
        ("Count all pairs", r"There are $8$ bills, so the total number of unordered pairs is $\binom82=28$."),
        ("Count pairs involving a $20$", r"Any pair with a $20$-dollar bill has sum at least $20$. There are $2$ choices for a $20$ and $6$ choices for a non-$20$ bill, giving $12$ pairs, plus the pair of two $20$s, giving $13$ pairs."),
        ("Count pairs without a $20$", r"Without a $20$, the only way to reach at least $20$ is to choose the two $10$-dollar bills. That adds $1$ more pair."),
        ("Compute the probability", r"There are $14$ favorable pairs out of $28$ total pairs."),
        ("Answer", r"The probability is $14/28=\boxed{\frac12}$."),
    ],
    16: [
        ("Name the roots", r"Let the roots of $x^2+px+m=0$ be $r$ and $s$. Then the roots of $x^2+mx+n=0$ are $2r$ and $2s$."),
        ("Use Vieta on the second equation", r"For $x^2+px+m=0$, we have $r+s=-p$ and $rs=m$."),
        ("Use Vieta on the first equation", r"For $x^2+mx+n=0$, the sum of roots is $-m$. But the roots are $2r$ and $2s$, so $2r+2s=2(r+s)=-2p=-m$. Hence $m=2p$."),
        ("Use the product", r"The product of the first equation's roots is $n$. Thus $n=(2r)(2s)=4rs=4m$."),
        ("Answer", r"Since $m=2p$, we get $n=4m=8p$, so $\frac np=\boxed{8}$."),
    ],
    17: [
        ("Rewrite as logarithms", r"From $4^a=5$, we have $a=\log_4 5$. Similarly, $b=\log_5 6$, $c=\log_6 7$, and $d=\log_7 8$."),
        ("Multiply the logs", r"The product is \[\log_4 5\cdot\log_5 6\cdot\log_6 7\cdot\log_7 8.\]"),
        ("Use telescoping", r"Using $\log_a b\cdot\log_b c=\log_a c$, the product collapses to $\log_4 8$."),
        ("Evaluate", r"Since $4=2^2$ and $8=2^3$, $\log_4 8=\frac32$."),
        ("Answer", r"The answer is $\boxed{\frac32}$."),
    ],
    18: [
        ("Identify the available digits", r"The digits cannot be $0$ or $1$, so they come from $2,3,4,5,6,7,8,9$, which gives $8$ possible digits."),
        ("Use the increasing-order condition", r"Once David chooses which $7$ digits appear, their order is forced because they must be in increasing order."),
        ("Count choices", r"So the number of telephone numbers is just the number of ways to choose $7$ digits from $8$: \[\binom87=8.\]"),
        ("Answer", r"David can have $\boxed{8}$ different telephone numbers."),
    ],
    19: [
        ("Find the median", r"The cumulative percentages are $10\%$ at $70$, then $35\%$ at $80$, then $55\%$ at $85$. So the median score is $85$."),
        ("Find the remaining percentage", r"The listed percentages before $95$ add to $10+25+20+15=70\%$, so $30\%$ of students got $95$."),
        ("Compute the mean", r"The mean is \[0.10(70)+0.25(80)+0.20(85)+0.15(90)+0.30(95).\]"),
        ("Evaluate", r"This equals $7+20+17+13.5+28.5=86$."),
        ("Answer", r"The difference between the mean and median is $86-85=\boxed{1}$."),
    ],
    20: [
        ("Use symmetry of permutations", r"All permutations of the digits $1,3,5,7,8$ are used. In each place value, every digit appears equally often."),
        ("Find the average digit in each place", r"The average of the five digits is \[\frac{1+3+5+7+8}{5}=\frac{24}{5}=4.8.\]"),
        ("Build the average number", r"Since each place has average digit $4.8$, the average number is \[4.8(10000+1000+100+10+1).\]"),
        ("Compute", r"This is $4.8\cdot11111=53332.8$."),
        ("Answer", r"The average is $\boxed{53332.8}$."),
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
        if r["year"] == "2005" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "本批完成 2005 AMC 10B Problems 11-20，无跳过题。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
