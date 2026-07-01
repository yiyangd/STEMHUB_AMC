import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 85
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2015_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16}
SKIPPED = []
BATCH_LABEL = "2015 AMC 10A Problems 11-16"
NEXT_START = "2015 AMC 10A Problem 17"

ANS={11:("C",r"\frac{12}{25}"),12:("C","2"),13:("C","5"),14:("C","4 o'clock"),15:("B","1"),16:("B","15")}

OV={
11:(r"The ratio of the length to the width of a rectangle is $4:3$. If the rectangle has diagonal of length $d$, then the area may be expressed as $kd^2$ for some constant $k$. What is $k$?",[("A",r"\frac27"),("B",r"\frac37"),("C",r"\frac{12}{25}"),("D",r"\frac{16}{25}"),("E",r"\frac34")]),
12:(r"Points $(\sqrt{\pi},a)$ and $(\sqrt{\pi},b)$ are distinct points on the graph of $y^2+x^4=2x^2y+1$. What is $|a-b|$?",[("A","1"),("B",r"\sqrt{\pi}"),("C","2"),("D",r"1+\pi"),("E",r"1+\pi^2")]),
13:(r"Claudia has $12$ coins, each of which is a $5$-cent coin or a $10$-cent coin. There are exactly $17$ different values that can be obtained as combinations of one or more of her coins. How many $10$-cent coins does Claudia have?",[("A","3"),("B","4"),("C","5"),("D","6"),("E","7")]),
14:(r"The circular face of a clock has radius $20$ cm, and a circular disk with radius $10$ cm is externally tangent to the clock face at $12$ o'clock. The disk has an arrow painted on it, initially pointing upward. The disk rolls clockwise around the clock face. At what point on the clock face will the disk be tangent when the arrow is next pointing upward?",[("A","2 o'clock"),("B","3 o'clock"),("C","4 o'clock"),("D","6 o'clock"),("E","8 o'clock")]),
15:(r"Consider the set of all fractions $\frac{x}{y}$, where $x$ and $y$ are relatively prime positive integers. How many of these fractions have the property that if both numerator and denominator are increased by $1$, the value of the fraction is increased by $10\%$?",[("A","0"),("B","1"),("C","2"),("D","3"),("E","infinitely many")]),
16:(r"If $y+4=(x-2)^2$, $x+4=(y-2)^2$, and $x\ne y$, what is the value of $x^2+y^2$?",[("A","10"),("B","15"),("C","20"),("D","25"),("E","30")]),
}

KEY_OVERRIDES={11:"Use a 3-4-5 rectangle scale factor.",12:"Substitute the fixed x-value and complete the square in y.",13:"Convert nickel/dime values to sums using ones and twos.",14:"Use the rolling circle rotation factor for external rolling.",15:"Turn the fraction condition into a factor equation.",16:"Subtract the symmetric equations and use x+y."}

SOL={
11:[("Use the ratio as side lengths",r"Let the rectangle have length $4s$ and width $3s$. This is the natural way to use the $4:3$ ratio."),("Find the diagonal",r"By the Pythagorean Theorem, the diagonal is $5s$, so $d=5s$ and $s=\frac d5$."),("Compute the area",r"The area is $(4s)(3s)=12s^2=12\left(\frac d5\right)^2=\frac{12}{25}d^2$."),("Conclude",r"Thus $k=\boxed{\frac{12}{25}}$."),],
12:[("Substitute the fixed x-value",r"With $x=\sqrt{\pi}$, we have $x^2=\pi$ and $x^4=\pi^2$. The equation becomes \[y^2+\pi^2=2\pi y+1.\]"),("Complete the square",r"Move terms to get \[y^2-2\pi y+\pi^2=1,\] so \[(y-\pi)^2=1.\]"),("Find the two y-values",r"The two solutions are $y=\pi+1$ and $y=\pi-1$."),("Compute the distance",r"Therefore $|a-b|=(\pi+1)-(\pi-1)=2$."),("Conclude",r"The answer is $\boxed{2}$."),],
13:[("Scale values by 5 cents",r"A $5$-cent coin contributes $1$ unit and a $10$-cent coin contributes $2$ units. If Claudia has $t$ ten-cent coins, then she has $12-t$ five-cent coins."),("Count possible unit sums",r"With at least one five-cent coin, the possible positive unit sums run consecutively from $1$ up to $(12-t)+2t=12+t$."),("Use the given number of values",r"The number of different positive values is therefore $12+t$. The problem says this number is $17$."),("Solve",r"$12+t=17$, so $t=5$."),("Conclude",r"Claudia has $\boxed{5}$ ten-cent coins."),],
14:[("Understand the rolling factor",r"When a circle of radius $r$ rolls externally around a fixed circle of radius $R$, it rotates through angle $\frac{R+r}{r}\theta$ while its center sweeps angle $\theta$ around the fixed circle."),("Apply the radii",r"Here $R=20$ and $r=10$, so the rotation factor is $\frac{20+10}{10}=3$."),("Find the first upright arrow",r"The arrow is next upright after the disk has rotated $2\pi$ radians. Thus $3\theta=2\pi$, so $\theta=\frac{2\pi}{3}$."),("Convert to clock position",r"A clockwise sweep of $\frac{2\pi}{3}=120^\circ$ from $12$ o'clock lands at $4$ o'clock."),("Conclude",r"The answer is $\boxed{\text{4 o'clock}}$."),],
15:[("Translate the 10 percent increase",r"The new fraction is $\frac{x+1}{y+1}$, and it is $10\%$ larger than $\frac xy$. Thus \[\frac{x+1}{y+1}=\frac{11x}{10y}.\]"),("Clear denominators",r"Cross-multiplying gives $10y(x+1)=11x(y+1)$."),("Rearrange into a factor equation",r"This simplifies to $xy+11x-10y=0$, or \[(x-10)(y+11)=-110.\]"),("Check positive coprime possibilities",r"Since $x,y>0$, we need $x<10$. Testing positive divisors of $110$ gives only one relatively prime solution: $x=5$, $y=11$."),("Conclude",r"There is exactly $\boxed{1}$ such fraction."),],
16:[("Rewrite both equations",r"From $y+4=(x-2)^2$, we get $y=x^2-4x$. From $x+4=(y-2)^2$, we get $x=y^2-4y$."),("Subtract the equations",r"Subtracting gives \[y-x=(x^2-y^2)-4(x-y).\] Since $x\ne y$, divide by $x-y$ carefully to get $x+y=3$."),("Find xy without solving both values",r"Substitute $y=3-x$ into $y=x^2-4x$: \[3-x=x^2-4x,\] so $x^2-3x-3=0$. This implies $x(3-x)=-3$, so $xy=-3$."),("Compute x squared plus y squared",r"Use \[x^2+y^2=(x+y)^2-2xy=3^2-2(-3)=15.\]"),("Conclude",r"The answer is $\boxed{15}$."),],
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
    if n in {10,17} and notes == "题面包含图形":
        notes = ""
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in {14} else notes
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
        if r["year"] == "2015" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {14},
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
        + "- Review notes: none.\n",
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
        + "- Answer verification source: AoPS 2015 AMC 10A Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + ("本批无跳过题。\n" if not SKIPPED else "本批跳过题：\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n")
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()












































