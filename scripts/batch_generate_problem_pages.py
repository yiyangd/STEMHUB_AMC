import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 82
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2014_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,14,15,16,17,18,19,20}
SKIPPED = ["2014 AMC 10B Problem 13 skipped: labels A, B, C depend on missing hexagon diagram"]
BATCH_LABEL = "2014 AMC 10B Problems 11-20 excluding 13"
NEXT_START = "2014 AMC 10B Problem 21"

ANS={11:("C","29"),12:("C","251750000"),14:("D","37"),15:("A",r"\frac{\sqrt3}{6}"),16:("B",r"\frac7{72}"),17:("D",r"2^{1005}"),18:("E","35"),19:("D",r"\frac13"),20:("C","12")}

OV={
11:(r"For the consumer, a single discount of $n\%$ is more advantageous than any of the following discounts: two successive $15\%$ discounts; three successive $10\%$ discounts; and a $25\%$ discount followed by a $5\%$ discount. What is the smallest possible positive integer value of $n$?",[("A","27"),("B","28"),("C","29"),("D","31"),("E","33")]),
12:(r"The largest divisor of $2014000000$ is itself. What is its fifth largest divisor?",[("A","125875000"),("B","201400000"),("C","251750000"),("D","402800000"),("E","503500000")]),
14:(r"Danica drove her new car on a trip for a whole number of hours, averaging $55$ miles per hour. At the beginning of the trip, $abc$ miles were displayed on the odometer, where $abc$ is a three-digit number with $a\ge1$ and $a+b+c\le7$. At the end of the trip, the odometer showed $cba$ miles. What is $a^2+b^2+c^2$?",[("A","26"),("B","27"),("C","36"),("D","37"),("E","41")]),
15:(r"In rectangle $ABCD$, $DC=2CB$ and points $E$ and $F$ lie on $AB$ so that $ED$ and $FD$ trisect $\angle ADC$. What is the ratio of the area of $\triangle DEF$ to the area of rectangle $ABCD$?",[("A",r"\frac{\sqrt3}{6}"),("B",r"\frac{\sqrt6}{8}"),("C",r"\frac{3\sqrt3}{16}"),("D",r"\frac13"),("E",r"\frac{\sqrt6}{4}")]),
16:(r"Four fair six-sided dice are rolled. What is the probability that at least three of the four dice show the same value?",[("A",r"\frac1{36}"),("B",r"\frac7{72}"),("C",r"\frac19"),("D",r"\frac5{36}"),("E",r"\frac16")]),
17:(r"What is the greatest power of $2$ that is a factor of $10^{1002}-4^{501}$?",[("A",r"2^{1002}"),("B",r"2^{1003}"),("C",r"2^{1004}"),("D",r"2^{1005}"),("E",r"2^{1006}")]),
18:(r"A list of $11$ positive integers has a mean of $10$, a median of $9$, and a unique mode of $8$. What is the largest possible value of an integer in the list?",[("A","24"),("B","30"),("C","31"),("D","33"),("E","35")]),
19:(r"Two concentric circles have radii $1$ and $2$. Two points on the outer circle are chosen independently and uniformly at random. What is the probability that the chord joining the two points intersects the inner circle?",[("A",r"\frac16"),("B",r"\frac14"),("C",r"\frac{2-\sqrt2}{2}"),("D",r"\frac13"),("E",r"\frac12")]),
20:(r"For how many integers $x$ is the number $x^4-51x^2+50$ negative?",[("A","8"),("B","10"),("C","12"),("D","14"),("E","16")]),
}

KEY_OVERRIDES={11:"Convert successive discounts into remaining-price multipliers.",12:"Match largest divisors with smallest divisors.",14:"Use the odometer reversal to get a divisibility condition.",15:"Model the trisected right angle with 30-60-90 slopes.",16:"Count exactly three-of-a-kind and four-of-a-kind outcomes.",17:"Factor out the obvious power of 2 and use the exponent of 5^n-1.",18:"Minimize the first ten entries while preserving median and unique mode.",19:"Parameterize the chord by the central angle between the two random points.",20:"Factor the polynomial in x^2 and count integer values in the interval."}

SOL={
11:[("Convert discounts to remaining price",r"A discount is easier to compare by asking what fraction of the price remains. Two $15\%$ discounts leave $0.85^2=0.7225$ of the price."),("Compute the effective discounts",r"Two $15\%$ discounts give a $27.75\%$ discount. Three $10\%$ discounts leave $0.9^3=0.729$, so they give a $27.1\%$ discount."),("Check the third option",r"A $25\%$ discount followed by a $5\%$ discount leaves $0.75\cdot0.95=0.7125$ of the price, so it gives a $28.75\%$ discount."),("Choose the smallest integer",r"A single $n\%$ discount must be greater than all three, so it must be greater than $28.75\%$. The smallest positive integer that works is $29$."),("Conclude",r"The answer is $\boxed{29}$."),],
12:[("Use divisor pairs",r"The largest divisors correspond to the smallest divisors. Specifically, if $d$ is a small divisor of $N$, then $N/d$ is a large divisor."),("Factor enough of the number",r"$2014000000=2014\cdot10^6=2^7\cdot5^6\cdot19\cdot53$."),("List the smallest divisors",r"The first five positive divisors in increasing order are $1,2,4,5,8$."),("Convert to the fifth largest divisor",r"Therefore the fifth largest divisor is \[\frac{2014000000}{8}=251750000.\]"),("Conclude",r"The answer is $\boxed{251750000}$."),],
14:[("Use the odometer reversal",r"The starting reading is $100a+10b+c$, and the ending reading is $100c+10b+a$. The distance traveled is their difference, $99(c-a)$."),("Use the whole number of hours",r"Danica drove at $55$ miles per hour for a whole number of hours, so $99(c-a)$ must be divisible by $55$."),("Find the digit difference",r"Since $99(c-a)=55h$, we need $9(c-a)=5h$, so $c-a$ must be a multiple of $5$. The ending reading is larger, so $c-a=5$."),("Use the digit-sum condition",r"Now $c=a+5$, and $a+b+c\le7$ gives $2a+b+5\le7$. Since $a\ge1$, the only possibility is $a=1$, $b=0$, and $c=6$."),("Conclude",r"Thus $a^2+b^2+c^2=1^2+0^2+6^2=37$, so the answer is $\boxed{37}$."),],
15:[("Choose convenient dimensions",r"Let $CB=1$ and $DC=2$, so the rectangle has area $2$. Place $D$ at the origin, $DC$ along the positive $x$-axis, and $DA$ vertical."),("Use trisected angles",r"The angle $\angle ADC$ is $90^\circ$, so the trisecting rays make angles $30^\circ$ and $60^\circ$ with $DC$."),("Find where the rays hit AB",r"The top side $AB$ has height $1$. A ray at $30^\circ$ reaches $y=1$ when $x=\sqrt3$, and a ray at $60^\circ$ reaches $y=1$ when $x=\frac1{\sqrt3}$."),("Compute triangle area",r"Thus $EF=\sqrt3-\frac1{\sqrt3}=\frac2{\sqrt3}$. The height from $D$ to $EF$ is $1$, so \[[DEF]=\frac12\cdot\frac2{\sqrt3}\cdot1=\frac1{\sqrt3}.\]"),("Find the ratio",r"The rectangle area is $2$, so the ratio is $\frac{1/\sqrt3}{2}=\frac1{2\sqrt3}=\frac{\sqrt3}{6}$."),("Conclude",r"The answer is $\boxed{\frac{\sqrt3}{6}}$."),],
16:[("Count all outcomes",r"Four dice have $6^4=1296$ ordered outcomes."),("Count exactly three equal dice",r"Choose the repeated value in $6$ ways, choose which one of the four dice is different in $4$ ways, and choose the different value in $5$ ways. This gives $6\cdot4\cdot5=120$ outcomes."),("Count four equal dice",r"There are $6$ outcomes where all four dice show the same value."),("Compute the probability",r"The favorable count is $120+6=126$, so the probability is \[\frac{126}{1296}=\frac7{72}.\]"),("Conclude",r"The answer is $\boxed{\frac7{72}}$."),],
17:[("Factor out the obvious power of 2",r"We have $10^{1002}=2^{1002}5^{1002}$ and $4^{501}=2^{1002}$. Therefore \[10^{1002}-4^{501}=2^{1002}(5^{1002}-1).\]"),("Find the extra factors of 2",r"We need the power of $2$ dividing $5^{1002}-1$. Since the exponent is even, the standard factor rule gives \[v_2(5^n-1)=v_2(5-1)+v_2(5+1)+v_2(n)-1.\]"),("Apply the rule",r"For $n=1002$, this is $2+1+1-1=3$, because $1002$ has one factor of $2$."),("Add exponents",r"The total power of $2$ is $1002+3=1005$."),("Conclude",r"The greatest power is $\boxed{2^{1005}}$."),],
18:[("Use the total sum",r"The mean is $10$ for $11$ numbers, so the total sum is $110$."),("Understand what to minimize",r"To make the largest entry as large as possible, we want the other ten entries as small as possible while keeping median $9$ and unique mode $8$."),("Construct a minimal first ten",r"One minimal arrangement is \[1,1,8,8,8,9,9,10,10,11.\] Here the sixth number is $9$, and $8$ is the unique mode."),("Compute the remaining value",r"The sum of these ten numbers is $75$, so the eleventh number can be $110-75=35$."),("Check uniqueness",r"Adding $35$ does not create another value appearing three times, so $8$ remains the unique mode."),("Conclude",r"The largest possible value is $\boxed{35}$."),],
19:[("Fix one point",r"Because of rotational symmetry, fix one point on the outer circle and let the other point vary uniformly around the circle."),("Relate chord distance to central angle",r"Let $\theta$ be the smaller central angle between the two points. The distance from the center to the chord is $2\cos(\theta/2)$."),("Require intersection with the inner circle",r"The chord intersects the inner circle of radius $1$ exactly when $2\cos(\theta/2)\le1$. This means $\theta/2\ge60^\circ$, so $\theta\ge120^\circ$."),("Count the arc",r"The second point must lie on the opposite arc from $120^\circ$ to $240^\circ$, which has measure $120^\circ$ out of $360^\circ$."),("Conclude",r"The probability is $\frac{120}{360}=\boxed{\frac13}$."),],
20:[("Factor using x squared",r"Let $u=x^2$. Then \[x^4-51x^2+50=u^2-51u+50=(u-1)(u-50).\]"),("Find when the product is negative",r"The product $(u-1)(u-50)$ is negative when $1<u<50$."),("Return to x",r"Thus $1<x^2<50$. For integer $x$, this means $|x|=2,3,4,5,6,7$."),("Count both signs",r"There are $6$ positive values and $6$ negative values."),("Conclude",r"The total number of integers is $\boxed{12}$."),],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in {15} else notes
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
        if r["year"] == "2014" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {15},
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
        + "- Answer verification source: AoPS 2014 AMC 10B Answer Key\n\n"
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












































