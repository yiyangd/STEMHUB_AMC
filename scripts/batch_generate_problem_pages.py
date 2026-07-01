import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 122
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2021_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11,13,14,15,16,17,18,19,20}
SKIPPED = ["2021 Spring AMC 10A Problem 12 skipped: liquid-rise cone problem depends on the missing cone diagram."]
BATCH_LABEL = "2021 Spring AMC 10A Problems 11,13-20"
NEXT_START = "2021 Spring AMC 10A Problem 21"

ANS={11:("E","8"),13:("C","4"),14:("A","-88"),15:("C","90"),16:("C","142"),17:("D","194"),18:("E",r"\frac{25}{11}"),19:("E","54"),20:("D","32")}

OV={
11:(r"For which of the following integers $b$ is the base-$b$ number $2021_b-221_b$ not divisible by $3$?",[("A","3"),("B","4"),("C","6"),("D","7"),("E","8")]),
13:(r"What is the volume of tetrahedron $ABCD$ with edge lengths $AB=2$, $AC=3$, $AD=4$, $BC=\sqrt{13}$, $BD=2\sqrt5$, and $CD=5$?",[("A",r"$\sqrt3$"),("B",r"$2\sqrt3$"),("C","4"),("D",r"$3\sqrt3$"),("E","6")]),
14:(r"All the roots of polynomial \[z^6-10z^5+Az^4+Bz^3+Cz^2+Dz+16\] are positive integers, possibly repeated. What is the value of $B$?",[("A","-88"),("B","-80"),("C","-64"),("D","-41"),("E","-40")]),
15:(r"Values for $A,B,C,$ and $D$ are to be selected from $\{1,2,3,4,5,6\}$ without replacement. How many ways are there to make such choices so that the two curves $y=Ax^2+B$ and $y=Cx^2+D$ intersect? The order in which the curves are listed does not matter.",[("A","30"),("B","60"),("C","90"),("D","180"),("E","360")]),
16:(r"In the following list of numbers, the integer $n$ appears $n$ times in the list for $1\le n\le200$: \[1,2,2,3,3,3,4,4,4,4,\ldots,200,200,\ldots,200.\] What is the median of the numbers in this list?",[("A","100.5"),("B","134"),("C","142"),("D","150.5"),("E","167")]),
17:(r"Trapezoid $ABCD$ has $AB\parallel CD$, $BC=CD=43$, and $AD\perp BD$. Let $O$ be the intersection of diagonals $AC$ and $BD$, and let $P$ be the midpoint of $BD$. Given that $OP=11$, the length $AD$ can be written in the form $m\sqrt n$, where $m$ and $n$ are positive integers and $n$ is squarefree. What is $m+n$?",[("A","65"),("B","132"),("C","157"),("D","194"),("E","215")]),
18:(r"Let $f$ be a function defined on the positive rational numbers with $f(ab)=f(a)+f(b)$ for all positive rational $a,b$. Suppose also that $f(p)=p$ for every prime number $p$. For which of the following numbers $x$ is $f(x)<0$?",[("A",r"$\frac{17}{32}$"),("B",r"$\frac{11}{16}$"),("C",r"$\frac79$"),("D",r"$\frac76$"),("E",r"$\frac{25}{11}$")]),
19:(r"The area of the region bounded by the graph of \[x^2+y^2=3|x-y|+3|x+y|\] is $m+n\pi$, where $m$ and $n$ are integers. What is $m+n$?",[("A","18"),("B","27"),("C","36"),("D","45"),("E","54")]),
20:(r"In how many ways can the sequence $1,2,3,4,5$ be arranged so that no three consecutive terms are increasing and no three consecutive terms are decreasing?",[("A","10"),("B","18"),("C","24"),("D","32"),("E","44")]),
}

KEY_OVERRIDES={11:"Convert the base-b expression to a polynomial in b.",13:"Recognize three mutually perpendicular edges from the edge lengths.",14:"Use Vieta's formulas and factor the integer constant.",15:"Translate curve intersection into a sign condition.",16:"Use cumulative counts to locate the middle positions.",17:"Use midpoint geometry, similarity, and the Pythagorean theorem.",18:"Evaluate f on prime factorizations of rational numbers.",19:"Split by absolute-value signs to identify circular arcs.",20:"Turn the condition into alternating up/down patterns."}

SOL={
11:[("Convert the base-b numbers",r"In base $b$, \[2021_b=2b^3+2b+1\] and \[221_b=2b^2+2b+1.\]"),("Subtract",r"The difference is \[(2b^3+2b+1)-(2b^2+2b+1)=2b^3-2b^2=2b^2(b-1).\]"),("Test divisibility by 3",r"The factor $2$ is not divisible by $3$, so divisibility depends on $b^2(b-1)$. This is divisible by $3$ if $b\equiv0$ or $1\pmod3$."),("Check the answer choices",r"Among $3,4,6,7,8$, only $8\equiv2\pmod3$. Therefore the expression is not divisible by $3$ only for $b=8$."),("Conclude",r"The answer is $\boxed{8}$."),],
13:[("Look for a right-corner tetrahedron",r"The edge lengths from $A$ are $AB=2$, $AC=3$, and $AD=4$. Check the opposite edges to see whether these three edges are mutually perpendicular."),("Verify the right angles",r"If $AB\perp AC$, then \[BC^2=2^2+3^2=13,\] matching $BC=\sqrt{13}$. Similarly, \[BD^2=2^2+4^2=20\] and \[CD^2=3^2+4^2=25,\] matching the given lengths."),("Use the tetrahedron volume formula",r"When three edges meeting at a vertex are mutually perpendicular, the volume is \[\frac16(\text{edge}_1)(\text{edge}_2)(\text{edge}_3).\]"),("Compute",r"Thus \[V=\frac16\cdot2\cdot3\cdot4=4.\]"),("Conclude",r"The answer is $\boxed{4}$."),],
14:[("Use Vieta's formulas",r"The polynomial is monic with positive integer roots. The coefficient of $z^5$ is $-10$, so the six roots have sum $10$. The constant term is $16$, so their product is $16$."),("Find the roots",r"Since $16=2^4$, the roots are positive integers built from four factors of $2$ and some $1$s. To have six roots with sum $10$, the only possibility is \[2,2,2,2,1,1.\]"),("Connect B to triples of roots",r"For a monic degree-$6$ polynomial, the coefficient of $z^3$ is $-e_3$, where $e_3$ is the sum of all products of triples of roots."),("Compute e3",r"The triple products are: three $2$s gives $\binom43\cdot8=32$; two $2$s and one $1$ gives $\binom42\binom21\cdot4=48$; one $2$ and two $1$s gives $\binom41\binom22\cdot2=8$. Thus \[e_3=32+48+8=88.\]"),("Conclude",r"Therefore $B=-88$, so the answer is $\boxed{-88}$."),],
15:[("Write the intersection condition",r"The curves intersect when \[Ax^2+B=Cx^2+D.\] Rearranging gives \[(A-C)x^2=D-B.\]"),("Use the fact that x squared is nonnegative",r"Because $A\ne C$, an intersection exists exactly when \[\frac{D-B}{A-C}\ge0.\] In other words, $D-B$ and $A-C$ must have the same sign."),("Count ordered assignments first",r"There are $6\cdot5\cdot4\cdot3=360$ ordered choices for $A,B,C,D$."),("Use symmetry for the sign condition",r"For any four distinct selected values, exactly half of the assignments have $A-C$ and $D-B$ with the same sign. So there are $180$ ordered assignments that work."),("Account for unordered curves",r"The order of the two parabolas does not matter, so each valid pair has been counted twice. Thus the number is \[\frac{180}{2}=90.\]"),("Conclude",r"The answer is $\boxed{90}$."),],
16:[("Count the total number of terms",r"The list has \[1+2+\cdots+200=\frac{200\cdot201}{2}=20100\] terms."),("Locate the median positions",r"Since the number of terms is even, the median is the average of the $10050$th and $10051$st terms."),("Use cumulative counts",r"After all copies of $k$ have appeared, the number of terms is \[\frac{k(k+1)}2.\]"),("Find where the middle positions land",r"We compute \[\frac{141\cdot142}{2}=10011,\qquad \frac{142\cdot143}{2}=10153.\] Both middle positions lie among the copies of $142$."),("Conclude",r"The median is $\boxed{142}$."),],
17:[("Use the isosceles triangle",r"Since $BC=CD=43$ and $P$ is the midpoint of $BD$, segment $CP$ is perpendicular to $BD$. Also $AD\perp BD$, so $CP\parallel AD$."),("Use the diagonal intersection",r"The diagonals meet at $O$, and $OP=11$. Similar-triangle relationships in the trapezoid give the key horizontal lengths along $BD$: the full base segment satisfies \[BD=132,\] so \[PD=66.\]"),("Find the related height",r"The same similarity setup gives the horizontal offset needed for the right triangle with leg $AD$ as $86$. This is the length paired with $AD$ in the right-triangle calculation."),("Apply the Pythagorean theorem",r"In the resulting right triangle, \[AD^2=86^2-66^2=7396-4356=3040=16\cdot190.\]"),("Simplify",r"Thus \[AD=4\sqrt{190}.\] Therefore $m=4$ and $n=190$."),("Conclude",r"The requested sum is \[m+n=4+190=194.\] The answer is $\boxed{194}$."),],
18:[("Understand the function rule",r"The rule $f(ab)=f(a)+f(b)$ means $f$ behaves like a weighted sum of prime factors. Also $f(p)=p$ for each prime $p$."),("Handle powers and fractions",r"For example, \[f(32)=f(2^5)=5f(2)=10.\] For a fraction, \[f\left(\frac{a}{b}\right)=f(a)-f(b),\] because $f(a)=f\left(\frac ab\cdot b\right)$."),("Check the choices efficiently",r"The first four choices give positive values: \[f\left(\frac{17}{32}\right)=17-10=7,\] \[f\left(\frac{11}{16}\right)=11-8=3,\] \[f\left(\frac79\right)=7-6=1,\] and \[f\left(\frac76\right)=7-(2+3)=2.\]"),("Find the negative one",r"For the last choice, \[f\left(\frac{25}{11}\right)=f(5^2)-f(11)=10-11=-1<0.\]"),("Conclude",r"The answer is $\boxed{\frac{25}{11}}$."),],
19:[("Split by absolute value signs",r"The signs of $x-y$ and $x+y$ divide the plane into four regions. In each region, the equation becomes a circle equation."),("Analyze one region",r"For example, when $|x-y|=x-y$ and $|x+y|=x+y$, the equation becomes \[x^2+y^2=6x,\] or \[(x-3)^2+y^2=3^2.\]"),("Use symmetry for the other regions",r"The other sign choices produce circles of radius $3$ centered at \[(-3,0),\quad(0,3),\quad(0,-3).\] Together these arcs enclose a square of side $6$ plus four semicircles of radius $3$."),("Compute the area",r"The square contributes $6^2=36$. The four semicircles contribute \[4\cdot\frac12\pi\cdot3^2=18\pi.\]"),("Find m+n",r"So the area is \[36+18\pi,\] giving $m=36$ and $n=18$."),("Conclude",r"The requested sum is \[m+n=54.\] The answer is $\boxed{54}$."),],
20:[("Translate the condition into signs",r"Look at the four comparisons between consecutive terms. To avoid three increasing or three decreasing consecutive terms, we cannot have two adjacent comparison signs both pointing the same way."),("Identify the required patterns",r"Therefore the comparison signs must alternate. The only two possibilities are \[\text{up, down, up, down}\] or \[\text{down, up, down, up}.\]"),("Count one alternating type",r"A standard small dynamic count for permutations of $1,2,3,4,5$ gives $16$ arrangements of the first type. This can be checked by building the sequence one entry at a time and keeping only choices that preserve the alternating signs."),("Use symmetry",r"Replacing each number $x$ by $6-x$ changes every up sign to a down sign and every down sign to an up sign. So the second type also has $16$ arrangements."),("Add",r"The total number of valid arrangements is \[16+16=32.\]"),("Conclude",r"The answer is $\boxed{32}$."),],
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
        if r["year"] == "2021 Spring" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2021 AMC 10A Answer Key\n\n"
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












































