import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 54
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2010_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16,17,18,19,20}
SKIPPED = []
BATCH_LABEL = "2010 AMC 10B Problems 11-20"
NEXT_START = "2010 AMC 10B Problem 21"

ANS = {
    11: ("A", "50"),
    12: ("D", "60"),
    13: ("C", "92"),
    14: ("B", r"\frac{50}{101}"),
    15: ("C", "29"),
    16: ("B", r"\frac{2\pi}{9}-\frac{\sqrt{3}}{3}"),
    17: ("B", "23"),
    18: ("E", r"\frac{13}{27}"),
    19: ("B", "6"),
    20: ("D", "81"),
}

OV = {
    11: r"A shopper plans to purchase an item with listed price greater than $\$100$ and may use one coupon. Coupon A gives $15\%$ off the listed price, Coupon B gives $\$30$ off the listed price, and Coupon C gives $25\%$ off the amount by which the listed price exceeds $\$100$. Let $x$ and $y$ be the smallest and largest prices for which Coupon A saves at least as many dollars as Coupon B or Coupon C. What is $y-x$?",
    12: r"At the beginning of the school year, $50\%$ of the students in Mr. Well's class answered \"Yes\" to \"Do you love math?\" and $50\%$ answered \"No.\" At the end of the year, $70\%$ answered \"Yes\" and $30\%$ answered \"No.\" Altogether, $x\%$ of the students gave a different answer at the beginning and end. What is the difference between the maximum and minimum possible values of $x$?",
    13: r"What is the sum of all solutions of $x=\left|2x-|60-2x|\right|$?",
    14: r"The average of the numbers $1,2,3,\ldots,98,99,$ and $x$ is $100x$. What is $x$?",
    15: r"On a $50$-question multiple choice math contest, students receive $4$ points for a correct answer, $0$ points for a blank answer, and $-1$ point for an incorrect answer. Jesse's total score was $99$. What is the maximum number of questions that Jesse could have answered correctly?",
    16: r"A square of side length $1$ and a circle of radius $\frac{\sqrt{3}}{3}$ share the same center. What is the area inside the circle, but outside the square?",
    17: r"Every high school in the city of Euclid sent a team of $3$ students to a math contest. Each participant received a different score. Andrea's score was the median among all students, and hers was the highest score on her team. Andrea's teammates Beth and Carla placed $37^{\text{th}}$ and $64^{\text{th}}$, respectively. How many schools are in the city?",
    18: r"Positive integers $a,b,c$ are randomly and independently selected with replacement from the set $\{1,2,3,\ldots,2010\}$. What is the probability that $abc+ab+a$ is divisible by $3$?",
    19: r"A circle with center $O$ has area $156\pi$. Triangle $ABC$ is equilateral, $BC$ is a chord of the circle, $OA=4\sqrt{3}$, and point $O$ is outside $\triangle ABC$. What is the side length of $\triangle ABC$?",
    20: r"Two circles lie outside regular hexagon $ABCDEF$. The first is tangent to $\overline{AB}$, and the second is tangent to $\overline{DE}$. Both are tangent to lines $BC$ and $FA$. What is the ratio of the area of the second circle to that of the first circle?",
}

OV = {k: (v, None) for k, v in OV.items()}

KEY_OVERRIDES = {
    11: "Translate coupon savings into inequalities and find the interval of listed prices.",
    12: "Compare two yes/no distributions by matching as many students as possible, then as few as possible.",
    13: "Break an absolute value equation at the points where the inside expressions change sign.",
    14: "Turn the average statement into an equation using the sum of an arithmetic sequence.",
    15: "Use variables and an inequality to maximize correct answers under the scoring rule.",
    16: "Find one repeated circular segment using symmetry, then multiply by four.",
    17: "Use Andrea's median rank and teammate ranks to pin down the total number of students.",
    18: "Work modulo $3$ and count residue classes instead of individual integers.",
    19: "Relate the chord length, circle radius, and equilateral-triangle height with the Pythagorean theorem.",
    20: "View the tangent circles as incircles in the same $60^\circ$ angle and compare their radii.",
}

SOL = {
    11: [
        ("Represent the price clearly", r"Let the listed price be $P$. The problem is not asking for the best coupon for one fixed price; it asks for all prices where Coupon A saves at least as much as each of the other two coupons. So we should write the three savings as expressions in $P$."),
        ("Write the three savings", r"Coupon A saves $0.15P$. Coupon B saves $30$. Coupon C saves $25\%$ of the amount above $100$, so it saves $0.25(P-100)$. Coupon A must be at least as good as both, so it must satisfy two inequalities."),
        ("Compare A with B", r"From $0.15P\ge 30$, multiply by $100$ or divide by $0.15$ to get $P\ge 200$. This gives the left endpoint: below $200$, a flat $30$ discount beats Coupon A."),
        ("Compare A with C", r"Now compare Coupon A with Coupon C: $0.15P\ge 0.25(P-100)$. This becomes $0.15P\ge 0.25P-25$, so $25\ge 0.10P$ and therefore $P\le 250$. This gives the right endpoint."),
        ("Find the requested difference", r"The valid prices run from $x=200$ to $y=250$. Therefore $y-x=250-200=50$, so the answer is $\boxed{50}$."),
    ],
    12: [
        ("Convert the percentages into groups", r"Think of $100$ students, since all percentages then become counts. At the beginning there are $50$ Yes and $50$ No. At the end there are $70$ Yes and $30$ No."),
        ("Find the minimum number who changed", r"To make as few students change as possible, keep all $50$ original Yes students as Yes. The class still needs $20$ more Yes answers at the end, so $20$ No students must change to Yes. Thus the minimum possible value of $x$ is $20$."),
        ("Find the maximum number who changed", r"To make as many students change as possible, change all $50$ original Yes students to No if possible. But the end has only $30$ No answers, so only $30$ of them can switch to No. Also all $50$ original No students can switch to Yes, giving $30+50=80$ students who changed."),
        ("Compare the extremes", r"The maximum possible value of $x$ is $80$, and the minimum possible value is $20$. The requested difference is $80-20=60$, so the answer is $\boxed{60}$."),
    ],
    13: [
        ("Locate where the absolute values change", r"The expression has two absolute values. The inner one, $|60-2x|$, changes form at $x=30$. After that, another absolute value may change depending on the simplified expression, so a case approach is the cleanest way to avoid guessing."),
        ("Case 1: $x<30$", r"If $x<30$, then $|60-2x|=60-2x$. The equation becomes $x=|2x-(60-2x)|=|4x-60|$. This new absolute value changes at $x=15$."),
        ("Solve the subcases below $30$", r"For $15\le x<30$, we have $|4x-60|=4x-60$, so $x=4x-60$ and $x=20$. For $x<15$, we have $|4x-60|=60-4x$, so $x=60-4x$ and $x=12$. Both values fit their subcases."),
        ("Case 2: $x\ge 30$", r"If $x\ge 30$, then $|60-2x|=2x-60$. The equation becomes $x=|2x-(2x-60)|=|60|=60$. This solution fits $x\ge 30$."),
        ("Add the solutions", r"The solutions are $12$, $20$, and $60$. Their sum is $12+20+60=92$, so the answer is $\boxed{92}$."),
    ],
    14: [
        ("Translate average into total sum", r"An average is total divided by number of terms. Here there are the $99$ numbers from $1$ to $99$, plus the extra number $x$, so there are $100$ terms altogether."),
        ("Sum the known numbers", r"The sum $1+2+\cdots+99$ is $\frac{99\cdot100}{2}=99\cdot50$. Therefore the total sum of all $100$ terms is $99\cdot50+x$."),
        ("Set up the average equation", r"Since the average is $100x$, we write \[\frac{99\cdot50+x}{100}=100x.\] Multiplying by $100$ gives $99\cdot50+x=10000x$."),
        ("Solve for $x$ cleanly", r"Move the $x$ term to the right: $99\cdot50=9999x$. Since $9999=99\cdot101$, we get \[x=\frac{99\cdot50}{99\cdot101}=\frac{50}{101}.\]"),
        ("Check the size", r"The value is about $0.495$, which is plausible because the average $100x$ is about $49.5$, near the average of $1$ through $99$. The answer is $\boxed{\frac{50}{101}}$."),
    ],
    15: [
        ("Name the quantities", r"Let $c$ be the number correct, $w$ the number wrong, and $b$ the number blank. Then $c+w+b=50$. The score equation is $4c-w=99$."),
        ("Focus on maximizing correct answers", r"Blank answers do not change the score, so to make $c$ large we mainly need to know whether there are enough remaining questions to absorb the necessary wrong answers. From $4c-w=99$, we get $w=4c-99$."),
        ("Use the total number of questions", r"The number answered either correctly or incorrectly is $c+w$, and this cannot exceed $50$. Substitute $w=4c-99$: \[c+(4c-99)\le 50.\] This gives $5c\le149$, so $c\le29.8$."),
        ("Use integrality", r"Because $c$ is an integer, the largest possible value is $c=29$. This is actually possible because then $w=4(29)-99=17$ and $b=50-29-17=4$."),
        ("Conclude", r"So Jesse could have answered at most $29$ questions correctly. The answer is $\boxed{29}$."),
    ],
    16: [
        ("Understand the overlap", r"The circle and square have the same center. The radius is $\frac{\sqrt3}{3}$, while half the square's side is $\frac12$. The circle crosses each side of the square, so the desired region consists of four identical circular segments outside the square."),
        ("Study one side of the square", r"Look at the top side of the square. From the center to that side is distance $\frac12$. If half the chord cut by the circle on that side is $a$, then \[a^2+\left(\frac12\right)^2=\left(\frac{\sqrt3}{3}\right)^2.\] Thus $a^2=\frac13-rac14=\frac1{12}$, so $a=\frac{\sqrt3}{6}$."),
        ("Identify the central angle", r"The full chord length is $2a=\frac{\sqrt3}{3}$, which equals the radius. A chord equal to the radius subtends a $60^\circ$ central angle. That tells us the outside piece above one side is one $60^\circ$ sector minus an equilateral triangle."),
        ("Compute one segment", r"The sector area is \[\frac{60}{360}\pi\left(\frac{\sqrt3}{3}\right)^2=\frac{\pi}{18}.\] The equilateral triangle has side $\frac{\sqrt3}{3}$, so its area is \[\frac{\sqrt3}{4}\left(\frac{\sqrt3}{3}\right)^2=\frac{\sqrt3}{12}.\]"),
        ("Multiply by four", r"There are four identical segments, one on each side of the square. The total area is $4\left(\frac{\pi}{18}-\frac{\sqrt3}{12}\right)=\frac{2\pi}{9}-\frac{\sqrt3}{3}$. The answer is $\boxed{\frac{2\pi}{9}-\frac{\sqrt3}{3}}$."),
    ],
    17: [
        ("Translate schools into students", r"Let there be $n$ schools. Since each school sends $3$ students, there are $3n$ contestants. Because all scores are different, the median is a single middle rank, so $3n$ must be odd and the median rank is $\frac{3n+1}{2}$."),
        ("Use Andrea's team condition", r"Andrea has the highest score on her own team, while Beth and Carla placed $37$th and $64$th. Therefore Andrea's rank is better than both teammates, so her rank is less than $37$."),
        ("Use the existence of the 64th-place teammate", r"There must be at least $64$ contestants, so $3n\ge64$. This gives $n\ge22$. Since $3n$ must be odd, $n$ must be odd, so possible nearby values begin with $23,25,\ldots$."),
        ("Test the median rank", r"If $n=23$, then there are $69$ students and the median rank is $35$, which is less than $37$. That works with Andrea being ahead of Beth and Carla. If $n=25$, the median rank is $38$, which is not better than Beth's $37$th place, so it fails."),
        ("Conclude", r"The only possible number of schools is $23$. Therefore the answer is $\boxed{23}$."),
    ],
    18: [
        ("Reduce the expression modulo 3", r"We only care whether $abc+ab+a$ is divisible by $3$. Factor the expression as \[abc+ab+a=a(bc+b+1)=a\bigl(b(c+1)+1\bigr).\] A product is $0$ modulo $3$ if at least one factor is $0$ modulo $3$."),
        ("Use uniform residues", r"The set $\{1,2,\ldots,2010\}$ has the same number of integers in each residue class modulo $3$, because $2010$ is divisible by $3$. So $a,b,c$ are each equally likely to be $0,1,$ or $2$ modulo $3$."),
        ("Count when the first factor works", r"If $a\equiv0\pmod3$, the expression is automatically divisible by $3$. This happens with probability $\frac13$."),
        ("Count when the second factor works", r"If $a\not\equiv0\pmod3$, we need $b(c+1)+1\equiv0\pmod3$. Among the $9$ possible residue pairs $(b,c)$, this happens for $(b,c)=(1,1)$ and $(2,0)$, so the probability is $\frac29$."),
        ("Combine the cases", r"The cases are disjoint by whether $a$ is $0$ modulo $3$. Thus the probability is \[\frac13+\frac23\cdot\frac29=\frac13+\frac4{27}=\frac{13}{27}.\] The answer is $\boxed{\frac{13}{27}}$."),
    ],
    19: [
        ("Turn the area into a radius", r"The circle has area $156\pi$, so its radius $R$ satisfies $\pi R^2=156\pi$. Thus $R^2=156$. We will use $R^2$ directly instead of simplifying the radical."),
        ("Let the triangle side be $s$", r"Since $ABC$ is equilateral, the altitude from $A$ to $BC$ is $\frac{s\sqrt3}{2}$. The chord $BC$ has length $s$, so if the distance from $O$ to chord $BC$ is $d$, then the right triangle from the circle center to the midpoint of the chord gives \[\left(\frac{s}{2}\right)^2+d^2=156.\]"),
        ("Use the position of $O$", r"Point $O$ is outside the equilateral triangle, and $OA=4\sqrt3$. In this configuration the center lies beyond side $BC$ from vertex $A$, so the distance from $O$ to $BC$ is the triangle altitude plus $OA$: \[d=\frac{s\sqrt3}{2}+4\sqrt3.\]"),
        ("Solve the equation", r"Substitute this into the chord equation: \[\frac{s^2}{4}+\left(\frac{s\sqrt3}{2}+4\sqrt3\right)^2=156.\] This simplifies to $s^2+12s+48=156$, so $s^2+12s-108=0$."),
        ("Choose the positive root", r"Factoring gives $(s-6)(s+18)=0$. A side length must be positive, so $s=6$. The answer is $\boxed{6}$."),
    ],
    20: [
        ("Use a convenient scale", r"The ratio of areas will not depend on the size of the regular hexagon, so let the side length be $1$. The lines $BC$ and $FA$ meet at a $60^\circ$ angle outside the hexagon."),
        ("Find the small circle radius", r"The first circle is tangent to lines $BC$ and $FA$ and also to side $AB$. In the $60^\circ$ angle, its center lies on the angle bisector. The distance from the angle vertex to line $AB$ is the altitude of an equilateral triangle of side $1$, namely $\frac{\sqrt3}{2}$. For a circle inside this small triangular region, that distance equals $3r_1$, so $r_1=\frac{\sqrt3}{6}$."),
        ("Find the large circle radius", r"The second circle is tangent to the same two lines but to the opposite side $DE$. The distance from the angle vertex down to line $DE$ is three times as large, $\frac{3\sqrt3}{2}$. Since this circle lies on the far side of $DE$, the distance to its center is $2r_2$, and the last radius reaches back to $DE$, so $2r_2=\frac{3\sqrt3}{2}+r_2$. Thus $r_2=\frac{3\sqrt3}{2}$."),
        ("Compare radii", r"The ratio of the radii is \[\frac{r_2}{r_1}=\frac{\frac{3\sqrt3}{2}}{\frac{\sqrt3}{6}}=9.\] Since circle areas scale with the square of the radius, the area ratio is $9^2=81$."),
        ("Conclude", r"Therefore the ratio of the area of the second circle to that of the first circle is $\boxed{81}$."),
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
        if r["year"] == "2010" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2010 AMC 10B Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批无跳过题。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()



















