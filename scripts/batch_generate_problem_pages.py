import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 111
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2019_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2019 AMC 10A Problems 21-25"
NEXT_START = "2019 AMC 10B Problem 1"

ANS={21:("D",r"2\sqrt5"),22:("B",r"\frac7{16}"),23:("C","5979"),24:("B","244"),25:("D","34")}

OV={
21:(r"A sphere with center $O$ has radius $6$. A triangle with side lengths $15,15,$ and $24$ is situated in space so that each of its sides is tangent to the sphere. What is the distance between $O$ and the plane determined by the triangle?",[("A",r"$2\sqrt3$"),("B","4"),("C",r"$3\sqrt2$"),("D",r"$2\sqrt5$"),("E","5")]),
22:(r"Real numbers between $0$ and $1$, inclusive, are chosen in the following manner. A fair coin is flipped. If it lands heads, then it is flipped again and the chosen number is $0$ if the second flip is heads and $1$ if the second flip is tails. If the first coin flip is tails, then the number is chosen uniformly at random from $[0,1]$. Two random numbers $x$ and $y$ are chosen independently in this manner. What is the probability that $|x-y|>\frac12$?",[("A",r"$\frac13$"),("B",r"$\frac7{16}$"),("C",r"$\frac12$"),("D",r"$\frac9{16}$"),("E",r"$\frac23$")]),
23:(r"Travis has to babysit the Thompson triplets. First Tadd says the number $1$, then Todd says the next two numbers, then Tucker says the next three numbers, then Tadd says the next four numbers, and the process continues to rotate through the three children in order, each saying one more number than the previous child did, until $10000$ is reached. What is the $2019$th number said by Tadd?",[("A","5743"),("B","5885"),("C","5979"),("D","6001"),("E","6011")]),
24:(r"Let $p,q,$ and $r$ be the distinct roots of $x^3-22x^2+80x-67$. It is given that there exist real numbers $A,B,$ and $C$ such that \[\frac1{s^3-22s^2+80s-67}=\frac{A}{s-p}+\frac{B}{s-q}+\frac{C}{s-r}\] for all $s\notin\{p,q,r\}$. What is $\frac1A+\frac1B+\frac1C$?",[("A","243"),("B","244"),("C","245"),("D","246"),("E","247")]),
25:(r"For how many integers $n$ between $1$ and $50$, inclusive, is \[\frac{(n^2-1)!}{(n!)^n}\] an integer? Recall that $0!=1$.",[("A","31"),("B","32"),("C","33"),("D","34"),("E","35")]),
}

KEY_OVERRIDES={21:"Project the sphere center onto the triangle plane and use the triangle's inradius.",22:"Split the mixed distribution into discrete and continuous cases.",23:"Group the counting game into rotating blocks.",24:"Use partial fractions and Vieta's formulas.",25:"Reduce factorial divisibility to whether $n$ divides $(n-1)!$."}

SOL={
21:[("Project the center onto the triangle's plane",r"Let $P$ be the perpendicular projection of the sphere center $O$ onto the plane of the triangle, and let $h=OP$. Each side of the triangle is tangent to the sphere, so the distance from $O$ to each side is $6$."),("Relate this to in-plane distance",r"If the distance from $P$ to a side of the triangle is $r$, then the right triangle formed by $O$, $P$, and the closest point on that side gives \[r^2+h^2=6^2.\] Because this is true for all three sides, $P$ is the incenter of the triangle and $r$ is its inradius."),("Find the triangle's inradius",r"The triangle has sides $15,15,24$. Its altitude to the side $24$ is \[\sqrt{15^2-12^2}=9,\] so its area is \[\frac12\cdot24\cdot9=108.\] The semiperimeter is \[\frac{15+15+24}{2}=27,\] so the inradius is \[r=\frac{108}{27}=4.\]"),("Solve for h",r"Now \[4^2+h^2=6^2,\] so \[h^2=36-16=20.\]"),("Conclude",r"The distance from $O$ to the plane is \[h=\sqrt{20}=\boxed{2\sqrt5}.\]"),],
22:[("Understand the distribution",r"One chosen number is $0$ with probability $\frac14$, is $1$ with probability $\frac14$, and is uniformly distributed on $[0,1]$ with probability $\frac12$."),("Both numbers are endpoint values",r"If both numbers come from the endpoint process, then $|x-y|>\frac12$ exactly when the pair is $(0,1)$ or $(1,0)$. This contributes \[2\cdot\frac14\cdot\frac14=\frac18.\]"),("One endpoint and one uniform",r"If one number is an endpoint and the other is uniform, the uniform number must lie in the opposite half of the interval. For each order, the probability is \[\frac12\cdot\frac12\cdot\frac12=\frac18,\] so the two orders contribute $\frac14$ total."),("Both uniform",r"If both are uniform, the region $|x-y|>\frac12$ consists of two right triangles in the unit square with total area $\frac14$. Since both numbers are uniform with probability $\frac12\cdot\frac12=\frac14$, this contributes \[\frac14\cdot\frac14=\frac1{16}.\]"),("Add the cases",r"The total probability is \[\frac18+\frac14+\frac1{16}=\frac7{16}.\]"),("Conclude",r"The answer is $\boxed{\frac7{16}}$."),],
23:[("Group the game into blocks",r"The block lengths are $1,2,3,\ldots$, and the children repeat in the order Tadd, Todd, Tucker. Tadd receives blocks numbered $1,4,7,\ldots$."),("Count Tadd's blocks",r"Tadd's block lengths are \[1,4,7,\ldots,\] so the first $m$ Tadd blocks contain \[1+4+\cdots+(3m-2)=\frac{m(3m-1)}2\] numbers."),("Locate the 2019th Tadd number",r"For $m=36$, this total is \[\frac{36\cdot107}{2}=1926.\] For $m=37$, it is \[\frac{37\cdot110}{2}=2035.\] So the $2019$th Tadd number is in Tadd's $37$th block."),("Find where that block starts",r"Tadd's $37$th block is overall block $109$. The total number said before block $109$ is \[1+2+\cdots+108=\frac{108\cdot109}{2}=5886,\] so the block starts at $5887$."),("Find the offset",r"The desired number is the \[2019-1926=93\]rd number in that block. Therefore it is \[5887+92=5979.\]"),("Conclude",r"The answer is $\boxed{5979}$."),],
24:[("Use the factorization concept",r"Since $p,q,r$ are the roots, \[s^3-22s^2+80s-67=(s-p)(s-q)(s-r).\] The given equation is a partial fraction decomposition."),("Clear denominators",r"Multiplying by $(s-p)(s-q)(s-r)$ gives the identity \[1=A(s-q)(s-r)+B(s-p)(s-r)+C(s-p)(s-q).\]"),("Extract A, B, and C",r"Substitute $s=p$ into the identity. The $B$ and $C$ terms vanish, so \[1=A(p-q)(p-r),\] hence \[\frac1A=(p-q)(p-r).\] Similarly, \[\frac1B=(q-p)(q-r),\qquad \frac1C=(r-p)(r-q).\]"),("Simplify the sum",r"Adding these three expressions gives \[\frac1A+\frac1B+\frac1C=p^2+q^2+r^2-pq-pr-qr.\]"),("Use Vieta's formulas",r"From the polynomial, \[p+q+r=22,\qquad pq+pr+qr=80.\] Therefore \[p^2+q^2+r^2=(p+q+r)^2-2(pq+pr+qr)=22^2-160=324.\]"),("Conclude",r"The desired sum is \[324-80=244.\] The answer is $\boxed{244}$."),],
25:[("Rewrite using a known integer",r"The multinomial number \[\frac{(n^2)!}{(n!)^{n+1}}\] is an integer because it counts ways to split $n^2$ objects into $n$ unlabeled groups of size $n$."),("Relate it to the target expression",r"Now write \[\frac{(n^2-1)!}{(n!)^n}=\frac{(n^2)!}{(n!)^{n+1}}\cdot\frac{n!}{n^2}.\] The first factor is always an integer, so every $n$ with $n^2\mid n!$ definitely works."),("Identify the working composite numbers",r"For composite $n\ne4$, the factorial $n!$ contains enough factors to make $n^2$. If $n=ab$ with $1<a<b<n$, then both $a$ and $b$ appear below $n$; if $n=a^2$ with $a\ge3$, then $a$ and $2a$ both appear below $n$ and supply two factors of $a$."),("Find the failures",r"If $n$ is prime, the numerator $(n^2-1)!$ contains only $n-1$ multiples of $n$, while the denominator $(n!)^n$ contains $n$ factors of $n$, so the expression is not an integer. Also $n=4$ fails because there are not enough factors of $2$."),("Count failures",r"Between $1$ and $50$, there are $15$ primes. Together with $n=4$, that gives $16$ failures."),("Conclude",r"Thus the number of successful integers is \[50-16=\boxed{34}.\]"),],
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
        if r["year"] == "2019" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2019 AMC 10A Answer Key\n\n"
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












































