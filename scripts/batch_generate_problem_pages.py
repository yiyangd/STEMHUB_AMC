import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 77
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2013_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2013 AMC 10B Problems 21-25"
NEXT_START = "2014 AMC 10A Problem 1"

ANS={21:("C","104"),22:("C","1152"),23:("B","21"),24:("A","1"),25:("E","25")}

OV={
21:(r"Two non-decreasing sequences of nonnegative integers have different first terms. Each sequence has the property that each term beginning with the third is the sum of the previous two terms, and the seventh term of each sequence is $N$. What is the smallest possible value of $N$?",[("A","55"),("B","89"),("C","104"),("D","144"),("E","273")]),
22:(r"A regular octagon $ABCDEFGH$ has center $J$. Each of the vertices and the center is to be associated with one of the digits $1$ through $9$, with each digit used once, in such a way that the sums of the numbers on the lines $AJE$, $BJF$, $CJG$, and $DJH$ are equal. In how many ways can this be done?",[("A","384"),("B","576"),("C","1152"),("D","1680"),("E","3546")]),
23:(r"In triangle $ABC$, $AB=13$, $BC=14$, and $CA=15$. Distinct points $D$, $E$, and $F$ lie on segments $BC$, $CA$, and $DE$, respectively, such that $AD\perp BC$, $DE\perp AC$, and $AF\perp BF$. The length of segment $DF$ can be written as $\frac{m}{n}$, where $m$ and $n$ are relatively prime positive integers. What is $m+n$?",[("A","18"),("B","21"),("C","24"),("D","27"),("E","30")]),
24:(r"A positive integer $n$ is nice if there is a positive integer $m$ with exactly four positive divisors, including $1$ and $m$, such that the sum of the four divisors is equal to $n$. How many numbers in the set $\{2010,2011,2012,\ldots,2019\}$ are nice?",[("A","1"),("B","2"),("C","3"),("D","4"),("E","5")]),
25:(r"Bernardo chooses a three-digit positive integer $N$ and writes both its base-$5$ and base-$6$ representations on a blackboard. Later LeRoy sees the two numbers Bernardo has written. Treating the two numbers as base-$10$ integers, he adds them to obtain an integer $S$. For example, if $N=749$, Bernardo writes the numbers $10444$ and $3245$, and LeRoy obtains $S=13689$. For how many choices of $N$ are the two rightmost digits of $S$, in order, the same as those of $2N$?",[("A","5"),("B","10"),("C","15"),("D","20"),("E","25")]),
}

KEY_OVERRIDES={21:"Represent the seventh term as a linear expression in the first two terms.",22:"Use the common line sum to force opposite vertex pairs to have equal sums.",23:"Place the triangle in coordinates, then use projection and a right-angle circle condition.",24:"Classify integers with exactly four divisors as either p^3 or pq.",25:"Track only the last two displayed digits using modular arithmetic."}

SOL={
21:[("Describe a sequence by its first two terms",r"Let the first two terms be $a$ and $b$. Because the sequence is non-decreasing and uses nonnegative integers, we need $0\le a\le b$."),("Write the seventh term",r"The recurrence gives $a,b,a+b,a+2b,2a+3b,3a+5b,5a+8b$. Therefore the seventh term is $N=5a+8b$."),("Ask when two different first terms are possible",r"For a fixed $N$, the value of $a$ must satisfy $5a\equiv N\pmod 8$, so possible values of $a$ differ by $8$. To have two sequences with different first terms, we need at least two allowed values of $a$."),("Use the non-decreasing condition",r"The condition $a\le b$ means $a\le\frac{N-5a}{8}$, so $13a\le N$. If two possible $a$ values differ by $8$, the smallest pair is $a=0$ and $a=8$, which requires $N\ge13\cdot8=104$."),("Check that the lower bound works",r"When $N=104$, the pairs $(a,b)=(0,13)$ and $(8,8)$ both work. They give non-decreasing sequences and have different first terms."),("Conclude",r"The smallest possible value is $\boxed{104}$."),],
22:[("Focus on opposite pairs",r"The equal line sums are $A+J+E$, $B+J+F$, $C+J+G$, and $D+J+H$. Since the same center digit $J$ appears in every sum, the four opposite vertex pairs must all have the same sum."),("Choose the center digit",r"The digits $1$ through $9$ have total sum $45$. If the center digit is $c$ and each opposite pair has sum $s$, then $4s=45-c$. Thus $45-c$ must be divisible by $4$, so $c$ can be $1$, $5$, or $9$."),("Verify the pairings",r"For $c=1$, the remaining digits pair to sum $11$: $(2,9),(3,8),(4,7),(5,6)$. For $c=5$, they pair to sum $10$: $(1,9),(2,8),(3,7),(4,6)$. For $c=9$, they pair to sum $9$: $(1,8),(2,7),(3,6),(4,5)$."),("Count arrangements for each center",r"Once the four pairs are determined, assign them to the four opposite lines in $4!$ ways. Then each pair can be reversed between its two endpoints, giving $2^4$ choices."),("Multiply",r"For each of the $3$ possible center digits, there are $4!\cdot2^4=384$ arrangements. The total is $3\cdot384=1152$."),("Conclude",r"The answer is $\boxed{1152}$."),],
23:[("Set up coordinates",r"A $13$-$14$-$15$ triangle is friendly for coordinates. Put $B=(0,0)$ and $C=(14,0)$. Solving $AB=13$ and $AC=15$ gives $A=(5,12)$, so the altitude foot is $D=(5,0)$."),("Find point E by projecting to AC",r"The vector from $A$ to $C$ is $(9,-12)$, with unit direction $(3/5,-4/5)$. Projecting $D-A=(0,-12)$ onto this direction gives distance $48/5$, so $E=A+\frac{48}{5}(3/5,-4/5)=\left(\frac{269}{25},\frac{108}{25}\right)$."),("Parametrize F on DE",r"Let $F=D+t(E-D)$, where $0\le t\le1$. Since $E-D=\left(\frac{144}{25},\frac{108}{25}\right)$, we have $F=\left(5+\frac{144t}{25},\frac{108t}{25}\right)$."),("Use the right-angle condition",r"The condition $AF\perp BF$ means $(F-A)\cdot(F-B)=0$. Substituting the coordinates gives \[\frac{t}{25}(-576+1296t)=0.\] The nonzero solution is $t=\frac49$."),("Convert the parameter to DF",r"The length $DE$ is $\sqrt{(144/25)^2+(108/25)^2}=\frac{36}{5}$. Therefore $DF=\frac49\cdot\frac{36}{5}=\frac{16}{5}$."),("Conclude",r"Thus $m+n=16+5=\boxed{21}$."),],
24:[("Classify four-divisor numbers",r"A positive integer with exactly four positive divisors is either $p^3$ for a prime $p$, or $pq$ for two distinct primes $p$ and $q$. This classification keeps the search small."),("Handle the p cubed case",r"If $m=p^3$, the divisor sum is $1+p+p^2+p^3$. Near $2010$, $p=11$ gives $1464$ and $p=13$ gives $2380$, so no number from $2010$ to $2019$ comes from this case."),("Handle the pq case",r"If $m=pq$, then the four divisors are $1,p,q,pq$, and their sum is $(1+p)(1+q)$. Therefore we need one of $2010,2011,\ldots,2019$ to factor as a product of two numbers that are each one more than a prime."),("Check the short interval efficiently",r"Factoring the ten candidates, only $2016$ works. For example, $2016=4\cdot504$, and $4-1=3$, $504-1=503$ are both prime, so $m=3\cdot503$ has divisor sum $2016$."),("Count nice numbers",r"The other numbers in the interval do not have such a factorization, and none came from the $p^3$ case. Therefore exactly one number is nice."),("Conclude",r"The answer is $\boxed{1}$."),],
25:[("Only the last two displayed digits matter",r"The question asks about the two rightmost digits of $S$, so we can work modulo $100$. If the last two base-$5$ digits of $N$ are $a,b$, then the last two displayed decimal digits of the base-$5$ representation are $10a+b$."),("Write formulas for the two bases",r"Let $N=100h+t$, where $h=1,2,\ldots,9$ and $0\le t\le99$. The base-$5$ last two digits depend on $t\bmod25$, while the base-$6$ last two digits depend on $N\bmod36$, which is $28h+t\bmod36$."),("Turn this into a small table",r"For each hundreds digit $h$, compute \[A(t)=10\left\lfloor\frac{t\bmod25}{5}\right\rfloor+(t\bmod5)\] and \[B_h(t)=10\left\lfloor\frac{(28h+t)\bmod36}{6}\right\rfloor+((28h+t)\bmod6).\] We need $A(t)+B_h(t)\equiv2t\pmod{100}$."),("List the successful endings",r"Checking the nine possible values of $h$ gives successful endings only in these groups: for $h=3$, $t=60,61,62,63,64,90,91,92,93,94$; for $h=7$, $t=20,21,22,23,24$; for $h=9$, $t=0,1,2,3,4,30,31,32,33,34$."),("Count the choices",r"These groups contain $10+5+10=25$ possible values of $N$. The table is small because each entry uses only remainders, not full base conversions."),("Conclude",r"The number of choices is $\boxed{25}$."),],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {22}) else notes
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
        if r["year"] == "2013" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {22},
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
        + "- Answer verification source: AoPS 2013 AMC 10B Answer Key\n\n"
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












































