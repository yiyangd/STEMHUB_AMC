from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 11
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2003_AMC_10B_Answer_Key"
TARGET_NUMBERS = {10, 11, 12, 13, 14, 15, 16, 17, 18, 20}
SKIPPED = ["2003 AMC 10B Problem 19: semicircle shaded-region problem depends on the original diagram and OCR-corrupted choices."]
BATCH_LABEL = "2003 AMC 10B Problem 11-20"
NEXT_START = "2003 AMC 10B Problem 21"

ANS = {
    10: ("C", r"\frac{26^2}{10}"),
    11: ("A", "2"),
    12: ("C", "400"),
    13: ("E", "10"),
    14: ("D", "407"),
    15: ("E", "divisible by 11"),
    16: ("E", "8"),
    17: ("B", "3:1"),
    18: ("D", "15"),
    20: ("D", r"\frac{25}{2}"),
}

OV = {
    10: (
        "Nebraska changed its license plate scheme. Each old license plate consisted of a letter followed by four digits. Each new license plate consists of three letters followed by three digits. By how many times has the number of possible license plates increased?",
        [("A", r"$\frac{26}{10}$"), ("B", r"$\frac{26^2}{10^2}$"), ("C", r"$\frac{26^2}{10}$"), ("D", r"$\frac{26^3}{10^3}$"), ("E", r"$\frac{26^3}{10^2}$")],
    ),
    11: (
        r"A line with slope $3$ intersects a line with slope $5$ at the point $(10,15)$. What is the distance between the $x$-intercepts of these two lines?",
        [("A", "$2$"), ("B", "$5$"), ("C", "$7$"), ("D", "$12$"), ("E", "$20$")],
    ),
    12: (
        r"Al, Betty, and Clare split $\$1000$ among them to be invested in different ways. Each begins with a different amount. At the end of one year they have a total of $\$1500$. Betty and Clare have both doubled their money, whereas Al has managed to lose $\$100$. What was Al's original portion?",
        [("A", r"$\$250$"), ("B", r"$\$350$"), ("C", r"$\$400$"), ("D", r"$\$450$"), ("E", r"$\$500$")],
    ),
    14: (
        r"Given that $3^8\cdot 5^2=a^b$, where both $a$ and $b$ are positive integers, find the smallest possible value for $a+b$.",
        [("A", "$25$"), ("B", "$34$"), ("C", "$351$"), ("D", "$407$"), ("E", "$900$")],
    ),
    18: (
        r"What is the largest integer that is a divisor of $(n+1)(n+3)(n+5)(n+7)(n+9)$ for all positive even integers $n$?",
        [("A", "$3$"), ("B", "$5$"), ("C", "$11$"), ("D", "$15$"), ("E", "$165$")],
    ),
    20: (
        r"In rectangle $ABCD$, $AB=5$ and $BC=3$. Points $F$ and $G$ are on $\overline{CD}$ so that $DF=1$ and $GC=2$. Lines $AF$ and $BG$ intersect at $E$. Find the area of $\triangle AEB$.",
        [("A", "$10$"), ("B", r"$\frac{21}{2}$"), ("C", "$12$"), ("D", r"$\frac{25}{2}$"), ("E", "$15$")],
    ),
}

KEY_OVERRIDES = {
    10: "Count old and new plate formats separately, then divide to get the increase factor.",
    11: "Use the point-slope form of each line and set y=0 to find the x-intercepts.",
    12: "Let Al's initial amount be the unknown and express the final total in terms of it.",
    13: "Reduce the condition to possible digit sums, then count two-digit numbers with those sums.",
    14: "Use prime exponents to decide the largest possible exponent b, which minimizes a+b.",
    15: "In a single-elimination tournament, every match eliminates exactly one player.",
    16: "Translate the menu choices into a product and compare with the number of nights in 2003.",
    17: "Compare the melted sphere volume with the cone volume using the shared radius.",
    18: "Look for factors guaranteed among any five consecutive odd numbers produced by even n.",
    20: "Use similar triangles above and below the top side of the rectangle to find the height of E above AB.",
}

SOL = {
    10: [
        ("Read the format as a counting problem", r"The old format has one letter and four digits, while the new format has three letters and three digits. Since each position can be chosen independently, multiplication is the natural counting tool."),
        ("Count the old plates", r"There are $26$ choices for the letter and $10$ choices for each digit. Therefore the number of old plates is $26\cdot 10^4$."),
        ("Count the new plates", r"The new format has $26^3$ choices for the three letters and $10^3$ choices for the three digits. So the number of new plates is $26^3\cdot 10^3$."),
        ("Compare by division", r"The question asks how many times larger the new count is, so divide new by old: \[\frac{26^3\cdot 10^3}{26\cdot 10^4}=\frac{26^2}{10}.\]"),
        ("Choose the matching option", r"The increase factor is $\frac{26^2}{10}$, which is choice $\boxed{\text{C}}$.")
    ],
    11: [
        ("Focus on what an x-intercept means", r"An $x$-intercept is where a line crosses the $x$-axis, so its $y$-coordinate is $0$. The slopes and the common point give us enough information to write each line."),
        ("Write the line with slope 3", r"Using point-slope form through $(10,15)$, the first line is $y-15=3(x-10)$. Set $y=0$ because we want the $x$-intercept: $-15=3(x-10)$, so $x=5$."),
        ("Write the line with slope 5", r"For the second line, $y-15=5(x-10)$. Again set $y=0$: $-15=5(x-10)$, so $x=7$."),
        ("Take the distance on the x-axis", r"The two intercepts are at $x=5$ and $x=7$. Their distance is $|7-5|=2$."),
        ("Check the answer", r"The steeper line reaches the $x$-axis over a shorter horizontal distance, which matches the intercept $7$ being closer to $10$ than $5$ is. The answer is $\boxed{2}$.")
    ],
    12: [
        ("Choose one unknown", r"Let Al's original portion be $a$. Then Betty and Clare together originally had $1000-a$, which keeps the setup simple."),
        ("Translate the final amounts", r"Al loses $100$, so he ends with $a-100$. Betty and Clare both double their money, so together they end with $2(1000-a)$."),
        ("Use the final total", r"The final total is $1500$, so \[(a-100)+2(1000-a)=1500.\] Simplifying gives $1900-a=1500$, hence $a=400$."),
        ("Check reasonableness", r"If Al started with $400$, Betty and Clare together started with $600$ and ended with $1200$, while Al ended with $300$. The total is $1500$, so the answer is $\boxed{400}$."),
    ],
    13: [
        ("Name the digit sum", r"For a two-digit number $x$, the value $\clubsuit(x)$ is the sum of its digits. This sum can range from $1$ to $18$."),
        ("Find which digit sums work", r"We need $\clubsuit(\clubsuit(x))=3$. Between $1$ and $18$, the numbers whose digit sum is $3$ are $3$ and $12$. So $\clubsuit(x)$ must be either $3$ or $12$."),
        ("Count two-digit numbers with digit sum 3", r"The tens digit cannot be $0$. The pairs are $(1,2),(2,1),(3,0)$, giving $3$ numbers."),
        ("Count two-digit numbers with digit sum 12", r"The possible tens digits are $3,4,5,6,7,8,9$, with the ones digit determined each time. That gives $7$ numbers."),
        ("Combine the cases", r"The total is $3+7=10$, so the answer is $\boxed{10}$."),
    ],
    14: [
        ("Interpret the expression as a perfect power", r"The right side is $a^b$, so the left side must be written as a power with integer exponent $b$. Prime exponents tell us which exponents are possible."),
        ("Look at the prime factorization", r"The expression is already factored: $3^8\cdot 5^2$. If it equals $a^b$, then $b$ must divide both exponents $8$ and $2$."),
        ("Choose the exponent that can make a small base", r"The common divisors of $8$ and $2$ are $1$ and $2$. Using $b=2$ makes the base much smaller than using $b=1$, so it is the only serious candidate for minimizing $a+b$."),
        ("Compute the base", r"With $b=2$, we have \[a=3^{8/2}\cdot 5^{2/2}=3^4\cdot 5=81\cdot 5=405.\] Thus $a+b=405+2=407$."),
        ("Check the other exponent", r"If $b=1$, then $a=3^8\cdot 5^2$, which is far larger. Therefore the smallest possible value is $\boxed{407}$."),
    ],
    15: [
        ("Recognize the key tournament fact", r"In a single-elimination tournament, each match eliminates exactly one player. To end with one unbeaten player from $100$ players, exactly $99$ players must be eliminated."),
        ("Avoid unnecessary round counting", r"The byes affect when players enter, but they do not change the number of eliminations needed. Every eliminated player corresponds to one match."),
        ("Find the total number of matches", r"Therefore the tournament has $100-1=99$ matches."),
        ("Match the divisibility choice", r"The number $99$ is divisible by $11$ because $99=9\cdot 11$. It is not prime, not divisible by $2$, $5$, or $7$. The answer is $\boxed{\text{divisible by }11}$."),
    ],
    16: [
        ("Turn menu choices into multiplication", r"Let the number of main courses be $m$. Then there are $2m$ appetizers and $3$ desserts. A dinner is formed by choosing one item from each category."),
        ("Write the number of possible dinners", r"The number of different dinners is $(2m)(m)(3)=6m^2$."),
        ("Use the year correctly", r"The phrase 'each night in the year 2003' means each night of that calendar year, not $2003$ dinners. Since 2003 was not a leap year, there are $365$ nights."),
        ("Find the least possible m", r"We need $6m^2\ge 365$. Since $m=7$ gives $294$ and $m=8$ gives $384$, the least possible value is $m=8$."),
        ("Answer", r"The restaurant should offer $\boxed{8}$ main courses."),
    ],
    17: [
        ("Represent both volumes with the same radius", r"The cone and sphere have the same diameter, so they also have the same radius $r$. This makes the volume comparison clean."),
        ("Find the melted ice cream volume", r"The frozen sphere has volume $\frac{4}{3}\pi r^3$. The melted ice cream occupies $75\%$ of that volume, so its volume is \[\frac34\cdot\frac43\pi r^3=\pi r^3.\]"),
        ("Set it equal to the cone volume", r"The melted ice cream exactly fills the cone. The cone volume is $\frac13\pi r^2h$, so \[\frac13\pi r^2h=\pi r^3.\]"),
        ("Solve for the height", r"Cancel $\pi r^2$ from both sides to get $h/3=r$, so $h=3r$."),
        ("Interpret the ratio", r"The ratio of the cone's height to its radius is $h:r=3r:r=\boxed{3:1}$."),
    ],
    18: [
        ("Understand the sequence", r"Because $n$ is even, the five factors $n+1,n+3,n+5,n+7,n+9$ are five consecutive odd integers."),
        ("Find a guaranteed factor of 5", r"Among any five consecutive odd integers, the residues modulo $10$ run through the five odd residue classes. One of them must be divisible by $5$."),
        ("Find a guaranteed factor of 3", r"The terms differ by $2$. Modulo $3$, adding $2$ cycles through all residue classes, so within five terms at least one factor is divisible by $3$."),
        ("Combine the guaranteed factors", r"Since $3$ and $5$ are relatively prime, the product is always divisible by $15$."),
        ("Check that a larger listed factor is not guaranteed", r"The tempting larger option is $165=3\cdot5\cdot11$. But if $n=12$, the factors are $13,15,17,19,21$, and none is divisible by $11$. So $11$ is not guaranteed, and the largest listed divisor that always works is $\boxed{15}$."),
    ],
    20: [
        ("Use the diagram information without needing to draw", r"Place the rectangle so $AB$ is the bottom side of length $5$ and $CD$ is the top side. Since $DF=1$ and $GC=2$, the top segment $FG$ has length $5-1-2=2$."),
        ("Notice the similar triangles", r"Segment $FG$ is parallel to $AB$, so $\triangle EFG$ is similar to $\triangle EAB$. Their corresponding bases are $FG=2$ and $AB=5$."),
        ("Relate the heights", r"Let $h$ be the height of $E$ above $AB$. The distance from $E$ down to $FG$ is $h-3$, because the rectangle has height $3$. Similarity gives \[\frac{h-3}{h}=\frac{FG}{AB}=\frac25.\]"),
        ("Solve for the height", r"From $5(h-3)=2h$, we get $5h-15=2h$, so $3h=15$ and $h=5$."),
        ("Compute the area", r"Triangle $AEB$ has base $AB=5$ and height $5$. Therefore \[[AEB]=\frac12\cdot5\cdot5=\frac{25}{2}.\] The answer is $\boxed{\frac{25}{2}}$."),
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n == 20) else notes
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
        if r["year"] == "2003" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) == 20,
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
        + f"- Skipped reasons: {skipped_text}\n"
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
        + "\n\n## Skipped in latest batch\n\n"
        + "\n".join(f"- {s}" for s in SKIPPED)
        + "\n",
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批新增 2003 AMC 10B Problems 11-18 和 20，并修正了 Problem 10 的答案选项；Problem 19 因图形/OCR 问题跳过。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
