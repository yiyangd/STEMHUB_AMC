import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 128
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2022_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16,17,18,19,20}
SKIPPED = []
BATCH_LABEL = "2022 AMC 10A Problems 11-20"
NEXT_START = "2022 AMC 10A Problem 21"

ANS={11:("C","7"),12:("A","7"),13:("C","10"),14:("E","144"),15:("D","1565"),16:("D","30"),17:("D","13"),18:("A","359"),19:("C","5"),20:("E","206")}

OV={
11:(r"Ted mistakenly wrote $2^m\cdot\sqrt{\frac{1}{4096}}$ as $2\cdot\sqrt[m]{\frac{1}{4096}}$. What is the sum of all real numbers $m$ for which these two expressions have the same value?",[("A","5"),("B","6"),("C","7"),("D","8"),("E","9")]),
12:(r"On Halloween, $31$ children walked into the principal's office asking for candy. They can be classified into three types: some always lie, some always tell the truth, and some alternately lie and tell the truth. The alternaters arbitrarily choose their first response, either a lie or the truth, but each subsequent statement has the opposite truth value from its predecessor. The principal asked everyone the same three questions in this order. First: \"Are you a truth-teller?\" The principal gave candy to each of the $22$ children who answered yes. Second: \"Are you an alternater?\" The principal gave candy to each of the $15$ children who answered yes. Third: \"Are you a liar?\" The principal gave candy to each of the $9$ children who answered yes. How many pieces of candy in all did the principal give to the children who always tell the truth?",[("A","7"),("B","12"),("C","21"),("D","27"),("E","31")]),
13:(r"Let $\triangle ABC$ be a scalene triangle. Point $P$ lies on $\overline{BC}$ so that $\overline{AP}$ bisects $\angle BAC$. The line through $B$ perpendicular to $\overline{AP}$ intersects the line through $A$ parallel to $\overline{BC}$ at point $D$. Suppose $BP=2$ and $PC=3$. What is $AD$?",[("A","8"),("B","9"),("C","10"),("D","11"),("E","12")]),
14:(r"How many ways are there to split the integers $1$ through $14$ into $7$ pairs such that in each pair, the greater number is at least $2$ times the smaller number?",[("A","108"),("B","120"),("C","126"),("D","132"),("E","144")]),
15:(r"Quadrilateral $ABCD$ with side lengths $AB=7$, $BC=24$, $CD=20$, and $DA=15$ is inscribed in a circle. The area interior to the circle but exterior to the quadrilateral can be written in the form $\frac{a\pi-b}{c}$, where $a,b,$ and $c$ are positive integers such that $a$ and $c$ have no common prime factor. What is $a+b+c$?",[("A","260"),("B","855"),("C","1235"),("D","1565"),("E","1997")]),
16:(r"The roots of the polynomial $10x^3-39x^2+29x-6$ are the height, length, and width of a rectangular box. A new rectangular box is formed by lengthening each edge of the original box by $2$ units. What is the volume of the new box?",[("A",r"$\frac{24}{5}$"),("B",r"$\frac{42}{5}$"),("C",r"$\frac{81}{5}$"),("D","30"),("E","48")]),
17:(r"How many three-digit positive integers $\overline{abc}$ are there whose nonzero digits $a,b,$ and $c$ satisfy \[0.\overline{abc}=\frac13(0.\overline{a}+0.\overline{b}+0.\overline{c})?\] The bar indicates repetition.",[("A","9"),("B","10"),("C","11"),("D","13"),("E","14")]),
18:(r"Let $T_k$ be the transformation of the coordinate plane that first rotates the plane $k$ degrees counterclockwise around the origin and then reflects the plane across the $y$-axis. What is the least positive integer $n$ such that performing the sequence of transformations $T_1,T_2,T_3,\ldots,T_n$ returns the point $(1,0)$ back to itself?",[("A","359"),("B","360"),("C","719"),("D","720"),("E","721")]),
19:(r"Define $L_n$ as the least common multiple of all the integers from $1$ to $n$ inclusive. There is a unique integer $h$ such that \[\frac11+\frac12+\frac13+\cdots+\frac1{17}=\frac{h}{L_{17}}.\] What is the remainder when $h$ is divided by $17$?",[("A","1"),("B","3"),("C","5"),("D","7"),("E","9")]),
20:(r"A four-term sequence is formed by adding each term of a four-term arithmetic sequence of positive integers to the corresponding term of a four-term geometric sequence of positive integers. The first three terms of the resulting four-term sequence are $57$, $60$, and $91$. What is the fourth term of this sequence?",[("A","190"),("B","194"),("C","198"),("D","202"),("E","206")]),
}

KEY_OVERRIDES={11:"Convert radicals and roots to powers of 2, then compare exponents.",12:"Classify answer patterns by speaker type and subtract yes-count equations.",13:"Use angle-bisector ratio plus similar triangles from parallel lines.",14:"Pair large numbers with small numbers in a forced order.",15:"Recognize two right triangles sharing a diameter, then subtract areas.",16:"Use Vieta's formulas to compute the shifted volume without finding roots.",17:"Convert repeating decimals to fractions and count digit triples.",18:"Track the angle after pairs of transformations.",19:"Use modular arithmetic with the common denominator $L_{17}$.",20:"Model the two component sequences and use integer constraints."}

SOL={
11:[("Turn the strange expressions into powers",r"The main obstacle is notation, not computation. Since $4096=2^{12}$, both expressions can be written as powers of $2$."),("Rewrite the left side",r"The square root contributes an exponent of $\frac12$: \[\sqrt{\frac1{4096}}=(2^{-12})^{1/2}=2^{-6}.\] Thus the left expression is $2^m\cdot2^{-6}=2^{m-6}$."),("Rewrite the right side",r"The $m$th root means an exponent of $\frac1m$, so \[2\cdot\sqrt[m]{\frac1{4096}}=2\cdot(2^{-12})^{1/m}=2^{1-12/m}.\]"),("Compare exponents",r"Because the bases are the same and positive, the exponents must be equal: \[m-6=1-\frac{12}{m}.\] Multiplying by $m$ gives \[m^2-7m+12=0.\]"),("Use the requested sum",r"The roots are $m=3$ and $m=4$, so the sum of all possible values is $3+4=7$."),("Conclude",r"The answer is $\boxed{7}$."),],
12:[("Organize by response pattern",r"This is easier if we write what each type says to the three questions. Truth-tellers answer yes, no, no. Liars answer yes, yes, no."),("Separate the two kinds of alternaters",r"An alternater who lies first answers yes, yes, yes. An alternater who tells the truth first answers no, no, no. Let $A$ be the number of alternaters of the first kind."),("Translate the first two yes counts",r"The first question receives yes answers from truth-tellers, liars, and these $A$ alternaters. Thus \[T+L+A=22.\] The second question receives yes answers from liars and the same $A$ alternaters, so \[L+A=15.\]"),("Subtract to isolate truth-tellers",r"Subtracting the second equation from the first removes the types that are not truth-tellers: \[T=(T+L+A)-(L+A)=22-15=7.\]"),("Check what is being asked",r"The question asks for pieces of candy given to truth-tellers. A truth-teller says yes only to the first question, so each truth-teller receives exactly one piece."),("Conclude",r"There are $7$ such pieces of candy, so the answer is $\boxed{7}$."),],
13:[("Add helpful intersection points",r"Let the perpendicular line through $B$ meet $\overline{AP}$ at $X$ and meet $\overline{AC}$ at $Y$. This turns the configuration into right triangles and similar triangles."),("Use the angle bisector",r"Because $\overline{AP}$ bisects $\angle BAC$, the right triangles $\triangle ABX$ and $\triangle AYX$ have two equal angles and the shared side $AX$. Therefore they are congruent, so $AB=AY$."),("Apply the angle-bisector theorem",r"The angle-bisector theorem gives \[\frac{AB}{AC}=\frac{BP}{PC}=\frac23.\] Write $AB=AY=2x$ and $AC=3x$. Then \[YC=AC-AY=3x-2x=x.\]"),("Use the parallel line",r"Since $AD\parallel BC$, triangles $\triangle ADY$ and $\triangle CBY$ are similar. Their scale factor is \[\frac{AY}{CY}=\frac{2x}{x}=2.\]"),("Finish with the known base",r"Thus $AD=2\cdot CB$. Since $CB=BP+PC=2+3=5$, we get \[AD=2\cdot5=10.\]"),("Conclude",r"The answer is $\boxed{10}$."),],
14:[("Split small and large numbers",r"Numbers $8$ through $14$ cannot pair with each other, because then some small numbers would have to pair together and fail the condition. So each large number pairs with exactly one number from $1$ through $7$."),("Notice the forced pair",r"The number $7$ can pair only with $14$, because the partner must be at least $2\cdot7=14$. So $(7,14)$ is forced."),("Choose a partner for 6",r"Now $6$ can pair with $12$ or $13$, since $14$ is already used. That gives $2$ choices."),("Choose a partner for 5",r"After that, $5$ can pair with one of the remaining numbers among $10,11,12,13$. One of these may already have been used by $6$, leaving $3$ choices."),("Arrange the rest freely",r"The remaining small numbers $1,2,3,4$ can pair with the remaining four large numbers in any order, because each remaining large number is at least $8$."),("Multiply",r"The total number of pairings is \[2\cdot3\cdot4!=2\cdot3\cdot24=144.\] The answer is $\boxed{144}$."),],
15:[("Look for the intended right triangles",r"The side lengths $7,24$ and $15,20$ strongly suggest the Pythagorean triples $7$-$24$-$25$ and $15$-$20$-$25$. This suggests that diagonal $AC$ is the common hypotenuse of two right triangles."),("Find the circle radius",r"If $\triangle ABC$ and $\triangle ADC$ are right triangles with common hypotenuse $AC=25$, then $AC$ is a diameter of the circumcircle. Therefore the radius is \[r=\frac{25}{2}.\]"),("Compute the circle area",r"The area of the circle is \[\pi r^2=\pi\left(\frac{25}{2}\right)^2=\frac{625\pi}{4}.\]"),("Compute the quadrilateral area",r"The quadrilateral is the union of the two right triangles, so its area is \[\frac12(7)(24)+\frac12(15)(20)=84+150=234=\frac{936}{4}.\]"),("Subtract the areas",r"The region inside the circle but outside the quadrilateral has area \[\frac{625\pi}{4}-\frac{936}{4}=\frac{625\pi-936}{4}.\]"),("Conclude",r"Thus $a=625$, $b=936$, and $c=4$, so \[a+b+c=625+936+4=1565.\] The answer is $\boxed{1565}$."),],
16:[("Avoid finding the roots directly",r"The roots are the original dimensions. If they are $a,b,c$, the new volume is $(a+2)(b+2)(c+2)$."),("Expand in symmetric sums",r"Expanding keeps the expression in terms of sums of roots: \[(a+2)(b+2)(c+2)=abc+2(ab+ac+bc)+4(a+b+c)+8.\]"),("Use Vieta's formulas",r"For $10x^3-39x^2+29x-6$, Vieta's formulas give \[a+b+c=\frac{39}{10},\quad ab+ac+bc=\frac{29}{10},\quad abc=\frac{6}{10}.\]"),("Substitute",r"Now \[V=\frac{6}{10}+2\left(\frac{29}{10}\right)+4\left(\frac{39}{10}\right)+8.\]"),("Compute",r"This is \[\frac{6+58+156}{10}+8=22+8=30.\]"),("Conclude",r"The volume of the new box is $\boxed{30}$."),],
17:[("Translate repeating decimals",r"A repeating three-digit decimal is \[0.\overline{abc}=\frac{100a+10b+c}{999}.\] Also $0.\overline{a}=\frac a9$, and similarly for $b$ and $c$."),("Set up the digit equation",r"The condition becomes \[\frac{100a+10b+c}{999}=\frac13\left(\frac a9+\frac b9+\frac c9\right).\] Multiplying by $999$ gives \[100a+10b+c=37a+37b+37c,\] so \[7a=3b+4c.\]"),("Use modular arithmetic",r"Taking the equation modulo $7$ gives \[3b+4c\equiv 0\pmod7.\] Since $4\equiv-3\pmod7$, this means $3(b-c)\equiv0\pmod7$, so $b\equiv c\pmod7$."),("Count the equal-digit cases",r"If $b=c$, then $7a=7b$, so $a=b=c$. This gives $9$ solutions: $(1,1,1)$ through $(9,9,9)$."),("Count the digit pairs differing by 7",r"The other possibilities are $(b,c)=(1,8),(2,9),(8,1),(9,2)$. They give $(a,b,c)=(5,1,8),(6,2,9),(4,8,1),(5,9,2)$."),("Add",r"There are $9+4=13$ valid three-digit integers. The answer is $\boxed{13}$."),],
18:[("Track only the angle",r"Rotations and reflections keep the point on the unit circle, so we only need to track its angle. Start with $(1,0)$, which has angle $0^\circ$."),("Describe one transformation",r"After rotating by $k^\circ$, an angle $\theta$ becomes $\theta+k$. Reflecting across the $y$-axis sends an angle $\alpha$ to $180^\circ-\alpha$."),("Pair consecutive transformations",r"Applying $T_k$ and then $T_{k+1}$ sends an angle $\theta$ back to \[\theta-1^\circ.\] This is the key simplification: every two transformations rotate the point $1^\circ$ clockwise."),("Check the odd first step",r"After $T_1$, the point is at angle $179^\circ$. Then every two more transformations decrease this angle by $1^\circ$."),("Return to the starting point",r"We need to go from $179^\circ$ down to $0^\circ$, which takes $179$ two-step decreases after the first step. Therefore \[n=1+2\cdot179=359.\]"),("Conclude",r"The least positive value is $\boxed{359}$."),],
19:[("Focus on the numerator modulo 17",r"When the fractions are put over the common denominator $L_{17}$, the numerator is \[h=\sum_{k=1}^{17}\frac{L_{17}}{k}.\] We only need this modulo $17$."),("Notice which terms matter",r"For $k=1,2,\ldots,16$, the number $\frac{L_{17}}{k}$ is still divisible by $17$, because $k$ does not remove the factor $17$. So all those terms are $0\pmod{17}$."),("Reduce to one term",r"Only the term for $k=17$ may be nonzero modulo $17$. Therefore \[h\equiv \frac{L_{17}}{17}\pmod{17}.\]"),("Write the needed lcm",r"After removing the factor $17$, the remaining lcm is \[L_{16}=2^4\cdot3^2\cdot5\cdot7\cdot11\cdot13.\]"),("Compute modulo 17",r"Modulo $17$, this is \[16\cdot9\cdot5\cdot7\cdot11\cdot13\equiv (-1)\cdot9\cdot5\cdot7\cdot11\cdot13.\] Since $5\cdot7=35\equiv1$, this becomes \[-9\cdot11\cdot13\equiv -99\cdot13\equiv 3\cdot13=39\equiv5.\]"),("Conclude",r"The remainder is $\boxed{5}$."),],
20:[("Name the two hidden sequences",r"Let the arithmetic sequence be $a,a+d,a+2d,a+3d$ and the geometric sequence be $b,br,br^2,br^3$."),("Use the first three terms",r"The combined sequence gives \[a+b=57,\quad a+d+br=60,\quad a+2d+br^2=91.\]"),("Subtract to see the pattern",r"Subtract consecutive equations: \[d+b(r-1)=3,\quad d+br(r-1)=31.\] Subtracting these gives \[b(r-1)^2=28.\]"),("Use positive integer constraints",r"Because the geometric sequence has positive integer terms, $b$ and $r$ are positive integers. The useful possibilities for $(r-1)^2$ are $1$ or $4$."),("Reject the invalid case",r"If $(r-1)^2=1$, then $r=2$ and $b=28$. The first equation gives $a=29$, and then $d=-25$, so the arithmetic sequence is not positive throughout. This case is invalid."),("Use the valid case",r"If $(r-1)^2=4$, then $r=3$ and $b=7$. Then $a=50$ and $d=-11$, so the fourth term is \[a+3d+br^3=50-33+7\cdot27=17+189=206.\] The answer is $\boxed{206}$."),],
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
    year_label = row["year"]
    if year_label == "2021 Spring":
        year_part = "2021"
    elif year_label == "2021 Fall":
        year_part = "2021_Fall"
    else:
        year_part = year_label.replace(" ", "_")
    return f"https://artofproblemsolving.com/wiki/index.php/{year_part}_{row['contest'].replace(' ', '_')}{row['form']}_Problems/Problem_{row['problem_no']}"


def render(row):
    n = int(row["problem_no"])
    statement, choices = OV.get(n, (row["statement"], None))
    stem, parsed = split_choices(statement)
    choices = choices or parsed
    ans, val = ANS[n]
    tags = "".join(f'<span class="badge">{esc(t)}</span>' for t in (row.get("tags") or "").split(";") if t)
    notes = row.get("notes") or ""
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if notes == "题面包含图形" else notes
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
        if r["year"] == "2022" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {10},
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
        + "- Answer verification source: AoPS 2022 AMC 10A Answer Key\n\n"
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












































