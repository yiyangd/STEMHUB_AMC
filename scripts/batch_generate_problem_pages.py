import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 93
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2016_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2016 AMC 10A Problems 21-25"
NEXT_START = "2016 AMC 10B Problem 1"

ANS={21:("D",r"\sqrt6-\sqrt2"),22:("D","325"),23:("A","109"),24:("E","500"),25:("A","15")}

OV={
21:(r"Circles with centers $P$, $Q$, and $R$, having radii $1$, $2$, and $3$, respectively, lie on the same side of line $\ell$ and are tangent to $\ell$ at $P'$, $Q'$, and $R'$, respectively, with $Q'$ between $P'$ and $R'$. The circle with center $Q$ is externally tangent to each of the other two circles. What is the area of triangle $PQR$?",[("A","0"),("B","2"),("C","1"),("D",r"$\sqrt6-\sqrt2$"),("E",r"$\frac{3\sqrt3}{2}$")]),
22:(r"For some positive integer $n$, the number $110n^3$ has $110$ positive integer divisors, including $1$ and the number $110n^3$. How many positive integer divisors does the number $81n^4$ have?",[("A","110"),("B","191"),("C","261"),("D","325"),("E","425")]),
23:(r"A binary operation $\diamond$ has the properties that $a\diamond(b\diamond c)=(a\diamond b)\cdot c$ and that $a\diamond a=1$ for all nonzero real numbers $a$, $b$, and $c$. The solution to the equation $2016\diamond(6\diamond x)=100$ can be written as $\frac pq$, where $p$ and $q$ are relatively prime positive integers. What is $p+q$?",[("A","109"),("B","201"),("C","301"),("D","3049"),("E","33,601")]),
24:(r"A quadrilateral is inscribed in a circle of radius $200\sqrt2$. Three of the sides of this quadrilateral have length $200$. What is the length of the fourth side?",[("A","200"),("B",r"$200\sqrt2$"),("C",r"$200\sqrt3$"),("D",r"$300\sqrt2$"),("E","500")]),
25:(r"How many ordered triples $(x,y,z)$ of positive integers satisfy $\operatorname{lcm}(x,y)=72$, $\operatorname{lcm}(x,z)=600$, and $\operatorname{lcm}(y,z)=900$?",[("A","15"),("B","16"),("C","24"),("D","27"),("E","64")]),
}

KEY_OVERRIDES={21:"Use coordinates for tangent circles and compute area from center distances.",22:"Translate divisor counts into prime-exponent factors.",23:"Derive the operation from its identities before solving the equation.",24:"Use chord length and central angle relationships.",25:"Count prime exponent choices independently for each prime."}

SOL={
21:[("Place the line on an axis",r"Let the tangent line be horizontal. Since the radii are $1$, $2$, and $3$, the centers $P$, $Q$, and $R$ have heights $1$, $2$, and $3$ above the line."),("Use tangency to find horizontal distances",r"The circles centered at $P$ and $Q$ are externally tangent, so $PQ=1+2=3$. Their vertical separation is $1$, so their horizontal separation is \[\sqrt{3^2-1^2}=2\sqrt2.\] Similarly, $QR=2+3=5$, and the horizontal separation between $Q$ and $R$ is \[\sqrt{5^2-1^2}=2\sqrt6.\]"),("Choose coordinates",r"Because $Q'$ is between $P'$ and $R'$, the centers occur in that horizontal order. We may take \[P=(0,1),\quad Q=(2\sqrt2,2),\quad R=(2\sqrt2+2\sqrt6,3).\]"),("Compute the area",r"Use vectors from $P$: \[\overrightarrow{PQ}=(2\sqrt2,1),\quad \overrightarrow{PR}=(2\sqrt2+2\sqrt6,2).\] The triangle area is half the absolute determinant: \[\frac12\left|(2\sqrt2)(2)-1(2\sqrt2+2\sqrt6)\right|=\sqrt6-\sqrt2.\]"),("Conclude",r"The area of triangle $PQR$ is $\boxed{\sqrt6-\sqrt2}$."),],
22:[("Translate divisor count to exponents",r"Write $n=2^a3^b5^c11^d m$, where $m$ is relatively prime to $2\cdot3\cdot5\cdot11$. In $110n^3$, the primes $2$, $5$, and $11$ have exponents $3a+1$, $3c+1$, and $3d+1$, so their divisor-count factors are $3a+2$, $3c+2$, and $3d+2$."),("Use the factorization of 110",r"The total divisor count is $110=2\cdot5\cdot11$. The three factors $3a+2$, $3c+2$, and $3d+2$ are all congruent to $2$ modulo $3$, so they must be $2$, $5$, and $11$ in some order. This gives exponents $a,c,d$ equal to $0$, $1$, and $3$ in some order."),("Check the prime 3 and other primes",r"The factor from prime $3$ is $3b+1$, which is congruent to $1$ modulo $3$. There is no room in the product $110$ for an extra factor of this type except $1$, so $b=0$. Similarly, no other prime can occur in $m$."),("Count divisors of 81 n fourth",r"In $81n^4$, the prime $3$ has exponent $4$, contributing $5$ divisors. The exponents $0$, $1$, and $3$ for the primes $2$, $5$, and $11$ become $0$, $4$, and $12$, contributing factors $1$, $5$, and $13$."),("Multiply",r"The number of positive divisors is \[5\cdot1\cdot5\cdot13=325.\]"),("Conclude",r"The answer is $\boxed{325}$."),],
23:[("Find what the operation must be",r"The condition $a\diamond a=1$ suggests division. We can prove it from the given identity instead of guessing."),("Use b diamond b",r"Put $c=b$ in the identity: \[a\diamond(b\diamond b)=(a\diamond b)\cdot b.\] Since $b\diamond b=1$, this becomes \[a\diamond1=(a\diamond b)b.\]"),("Determine a diamond 1",r"Now set $b=a$ in the last equation. Since $a\diamond a=1$, we get \[a\diamond1=a.\] Therefore $a=(a\diamond b)b$, so \[a\diamond b=\frac ab.\]"),("Solve the equation",r"Then $6\diamond x=\frac6x$, and \[2016\diamond(6\diamond x)=2016\div\frac6x=336x.\] The equation becomes $336x=100$."),("Finish",r"Thus \[x=\frac{100}{336}=\frac{25}{84}.\] Hence $p+q=25+84=109$."),("Conclude",r"The answer is $\boxed{109}$."),],
24:[("Convert side lengths to central angles",r"For a chord of length $200$ in a circle of radius $200\sqrt2$, let half of its central angle be $\phi$. Then \[200=2(200\sqrt2)\sin\phi,\] so \[\sin\phi=\frac{1}{2\sqrt2}.\]"),("Understand the remaining side",r"The three equal sides use three equal central angles, each equal to $2\phi$. The fourth side corresponds to the remaining central angle $2\pi-6\phi$."),("Use the half-angle of the remaining chord",r"The fourth chord length is \[2(200\sqrt2)\sin(\pi-3\phi)=400\sqrt2\sin(3\phi).\]"),("Compute sin three phi",r"Using $\sin(3\phi)=3\sin\phi-4\sin^3\phi$ and $\sin\phi=\frac1{2\sqrt2}$, we get \[\sin(3\phi)=\frac{3}{2\sqrt2}-\frac{4}{16\sqrt2}=\frac5{4\sqrt2}.\]"),("Find the length",r"Therefore the fourth side is \[400\sqrt2\cdot\frac5{4\sqrt2}=500.\]"),("Conclude",r"The answer is $\boxed{500}$."),],
25:[("Work prime by prime",r"LCM conditions are easiest when we compare prime exponents. Factor the three given LCMs: \[72=2^3\cdot3^2,\quad 600=2^3\cdot3\cdot5^2,\quad 900=2^2\cdot3^2\cdot5^2.\]"),("Count choices for the exponent of 2",r"Let the exponents of $2$ in $x,y,z$ be $a,b,c$. We need \[\max(a,b)=3,\quad \max(a,c)=3,\quad \max(b,c)=2.\] The last condition gives $b,c\le2$ and at least one of them is $2$. Then $a=3$. There are $3\cdot3-2\cdot2=5$ choices for $(b,c)$."),("Count choices for the exponent of 3",r"For prime $3$, the conditions are \[\max(a,b)=2,\quad \max(a,c)=1,\quad \max(b,c)=2.\] Thus $b=2$, while $a,c\le1$ and at least one of $a,c$ equals $1$. This gives $2\cdot2-1=3$ choices."),("Count choices for the exponent of 5",r"For prime $5$, the conditions are \[\max(a,b)=0,\quad \max(a,c)=2,\quad \max(b,c)=2.\] So $a=b=0$ and $c=2$, giving $1$ choice."),("Multiply independent choices",r"The choices for different primes are independent, so the total number of triples is \[5\cdot3\cdot1=15.\]"),("Conclude",r"The answer is $\boxed{15}$."),],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in {10} else notes
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
        if r["year"] == "2016" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2016 AMC 10A Answer Key\n\n"
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












































