import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 65
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2012_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2012 AMC 10A Problems 21-25"
NEXT_START = "2012 AMC 10B Problem 1"

ANS = {
    21: ("C", r"\frac{3\sqrt5}{4}"),
    22: ("A", "255"),
    23: ("B", "170"),
    24: ("E", "253"),
    25: ("D", "10"),
}

OV = {
    21: (r"Let points $A=(0,0,0)$, $B=(1,0,0)$, $C=(0,2,0)$, and $D=(0,0,3)$. Points $E,F,G,H$ are midpoints of $BD,AB,AC,DC$, respectively. What is the area of $EFGH$?", [("A",r"\sqrt2"),("B",r"\frac{2\sqrt5}{3}"),("C",r"\frac{3\sqrt5}{4}"),("D",r"\sqrt3"),("E",r"\frac{2\sqrt7}{3}")]),
    22: (r"The sum of the first $m$ positive odd integers is $212$ more than the sum of the first $n$ positive even integers. What is the sum of all possible values of $n$?", [("A","255"),("B","256"),("C","257"),("D","258"),("E","259")]),
    23: (r"Adam, Benin, Chiang, Deshawn, Esther, and Fiona have internet accounts. Some, but not all, of them are internet friends with each other, and none has a friend outside this group. Each has the same number of internet friends. In how many different ways can this happen?", [("A","60"),("B","170"),("C","290"),("D","320"),("E","660")]),
    24: (r"Let $a,b,c$ be positive integers with $a\ge b\ge c$ such that $a^2-b^2-c^2+ab=2011$ and $a^2+3b^2+3c^2-3ab-2ac-2bc=-1997$. What is $a$?", [("A","249"),("B","250"),("C","251"),("D","252"),("E","253")]),
    25: (r"Real numbers $x,y,z$ are chosen independently and at random from $[0,n]$ for some positive integer $n$. The probability that no two of $x,y,z$ are within $1$ unit of each other is greater than $\frac12$. What is the smallest possible value of $n$?", [("A","7"),("B","8"),("C","9"),("D","10"),("E","11")]),
}

KEY_OVERRIDES = {
    21: "Use midpoint coordinates to identify a rectangle and compute its side lengths.",
    22: "Convert sums to formulas and factor a difference of squares.",
    23: "Count labeled regular graphs on six vertices by possible degree.",
    24: "Add the equations to force the small differences among $a,b,c$.",
    25: "Order the three random numbers and use a volume ratio.",
}

SOL = {
    21: [
        ("Compute the midpoints", r"The midpoints are $E=(\frac12,0,\frac32)$, $F=(\frac12,0,0)$, $G=(0,1,0)$, and $H=(0,1,\frac32)$. Coordinates let us avoid guessing the shape."),
        ("Find side lengths", r"The vector $\overrightarrow{EF}=(0,0,-\frac32)$, so $EF=\frac32$. Also $\overrightarrow{FG}=(-\frac12,1,0)$, so $FG=\sqrt{\frac14+1}=\frac{\sqrt5}{2}$."),
        ("Check the angle", r"The dot product of $\overrightarrow{EF}$ and $\overrightarrow{FG}$ is $0$, so the adjacent sides are perpendicular. Thus $EFGH$ is a rectangle."),
        ("Compute the area", r"The area is $EF\cdot FG=\frac32\cdot\frac{\sqrt5}{2}=\frac{3\sqrt5}{4}$. The answer is $\boxed{\frac{3\sqrt5}{4}}$."),
    ],
    22: [
        ("Use sum formulas", r"The first $m$ odd integers sum to $m^2$, and the first $n$ positive even integers sum to $2(1+2+\cdots+n)=n(n+1)$. So $m^2=n(n+1)+212$."),
        ("Complete the square", r"Multiply by $4$: $4m^2=4n^2+4n+848=(2n+1)^2+847$. Hence \[(2m-(2n+1))(2m+(2n+1))=847.\]"),
        ("Use factor pairs", r"The positive factor pairs of $847=7\cdot11^2$ are $(1,847)$, $(7,121)$, and $(11,77)$. For each pair, $2n+1$ is half the difference of the two factors."),
        ("Find n values", r"These give $2n+1=423,57,33$, so $n=211,28,16$. Their sum is $211+28+16=255$. The answer is $\boxed{255}$."),
    ],
    23: [
        ("Translate to graphs", r"Represent each person as a vertex and each friendship as an edge. The condition says the graph on $6$ labeled vertices is regular, but not empty and not complete."),
        ("List possible degrees", r"The common degree can be $1,2,3,$ or $4$. Degree $0$ would be no friendships, and degree $5$ would be all possible friendships."),
        ("Count degrees 1 and 4", r"A $1$-regular graph is a perfect matching: $5\cdot3\cdot1=15$ ways. A $4$-regular graph is the complement of a $1$-regular graph, so it also gives $15$ ways."),
        ("Count degrees 2 and 3", r"A $2$-regular graph is either one $6$-cycle or two $3$-cycles. There are $\frac{5!}{2}=60$ labeled $6$-cycles and $\frac{\binom63}{2}=10$ pairs of triangles, for $70$ total. Complements give $70$ graphs of degree $3$."),
        ("Add", r"The total is $15+15+70+70=170$. The answer is $\boxed{170}$."),
    ],
    24: [
        ("Add the equations", r"Adding the two equations gives \[2a^2+2b^2+2c^2-2ab-2ac-2bc=14.\] This is useful because it becomes a sum of squared differences."),
        ("Rewrite as squares", r"The left side is $(a-b)^2+(a-c)^2+(b-c)^2$, so \[(a-b)^2+(a-c)^2+(b-c)^2=14.\]"),
        ("Find the differences", r"Since $a\ge b\ge c$, the largest difference is $a-c$. The only possible square decomposition is $14=9+4+1$, so $a-c=3$ and the adjacent gaps are $1$ and $2$ in some order."),
        ("Test the two cases", r"Either $(a,b,c)=(a,a-1,a-3)$ or $(a,a-2,a-3)$. Substituting into $a^2-b^2-c^2+ab=2011$, the first case gives $7a=2021$, not integral; the second gives $8a=2024$."),
        ("Conclude", r"Thus $a=253$. The answer is $\boxed{253}$."),
    ],
    25: [
        ("Order the three numbers", r"There are $6$ possible orders for $x,y,z$, all equally likely except on boundary cases of probability zero. Work with one order, say $0\le z\le y\le x\le n$, and multiply is unnecessary because the ratio is the same in every order."),
        ("Find the total ordered volume", r"The region $0\le z\le y\le x\le n$ is one sixth of the cube $[0,n]^3$, so its volume is $\frac{n^3}{6}$."),
        ("Impose the spacing", r"In this order, no two numbers are within $1$ unit means $y-z>1$ and $x-y>1$. Shift by setting $z'=z$, $y'=y-1$, and $x'=x-2$. Then $0\le z'\le y'\le x'\le n-2$."),
        ("Compute the favorable ratio", r"The favorable ordered volume is $\frac{(n-2)^3}{6}$. Therefore the probability is \[\frac{(n-2)^3}{n^3}.\]"),
        ("Test the threshold", r"For $n=9$, this is $\frac{7^3}{9^3}=\frac{343}{729}<\frac12$. For $n=10$, it is $\frac{8^3}{10^3}=\frac{512}{1000}>\frac12$. So the smallest possible $n$ is $\boxed{10}$."),
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {16,17}) else notes
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
        if r["year"] == "2012" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2012 AMC 10A Answer Key\n\n"
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

































