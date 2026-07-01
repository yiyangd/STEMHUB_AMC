import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 87
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2015_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2015 AMC 10A Problems 21-25"
NEXT_START = "2015 AMC 10B Problem 1"

ANS={21:("C",r"\frac{24}{5}"),22:("A",r"\frac{47}{256}"),23:("C","16"),24:("B","31"),25:("A","59")}

OV={
21:(r"Tetrahedron $ABCD$ has $AB=5$, $AC=3$, $BC=4$, $BD=4$, $AD=3$, and $CD=\frac{12\sqrt2}{5}$. What is the volume of the tetrahedron?",[("A",r"3\sqrt2"),("B",r"2\sqrt5"),("C",r"\frac{24}{5}"),("D",r"3\sqrt3"),("E",r"\frac{24\sqrt2}{5}")]),
22:(r"Eight people are sitting around a circular table, each holding a fair coin. All eight people flip their coins, and those who flip heads stand while those who flip tails remain seated. What is the probability that no two adjacent people will stand?",[("A",r"\frac{47}{256}"),("B",r"\frac3{16}"),("C",r"\frac{49}{256}"),("D",r"\frac{25}{128}"),("E",r"\frac{51}{256}")]),
23:(r"The zeroes of the function $f(x)=x^2-ax+2a$ are integers. What is the sum of all possible values of $a$?",[("A","7"),("B","8"),("C","16"),("D","17"),("E","18")]),
24:(r"For some positive integers $p$, there is a quadrilateral $ABCD$ with positive integer side lengths, perimeter $p$, right angles at $B$ and $C$, $AB=2$, and $CD=AD$. How many different values of $p<2015$ are possible?",[("A","30"),("B","31"),("C","61"),("D","62"),("E","63")]),
25:(r"Let $S$ be a square of side length $1$. Two points are chosen independently at random on the sides of $S$. The probability that the straight-line distance between the points is at least $\frac12$ is $\frac{a-b\pi}{c}$, where $a$, $b$, and $c$ are positive integers and $\gcd(a,b,c)=1$. What is $a+b+c$?",[("A","59"),("B","60"),("C","61"),("D","62"),("E","63")]),
}

KEY_OVERRIDES={21:"Use coordinates for the two 3-4-5 faces and compute height.",22:"Count binary circular strings of length 8 with no adjacent heads.",23:"Use Vieta's formulas and factor a shifted product.",24:"Parameterize the right-angle quadrilateral to get a square condition.",25:"Break the boundary choices into same, adjacent, and opposite side cases."}

SOL={
21:[("Place one face in the xy-plane",r"Let $A=(0,0,0)$ and $B=(5,0,0)$. Since $AC=3$ and $BC=4$, we can put $C=\left(\frac95,\frac{12}{5},0\right)$."),("Use the equal distances to A and B",r"Because $AD=3$ and $BD=4$, point $D$ has the same $x$-coordinate as $C$, namely $\frac95$. Write $D=\left(\frac95,y,z\right)$."),("Use AD and CD",r"From $AD=3$, we get $y^2+z^2=\left(\frac{12}{5}\right)^2$. From $CD=\frac{12\sqrt2}{5}$, we get \[(y-\frac{12}{5})^2+z^2=\frac{288}{25}.\]"),("Solve for the height",r"Subtracting the equations gives $y=0$, so $z=\frac{12}{5}$. This $z$-value is the height above the plane of $\triangle ABC$."),("Compute volume",r"The area of $\triangle ABC$ is $\frac12\cdot3\cdot4=6$. Thus the tetrahedron volume is \[\frac13\cdot6\cdot\frac{12}{5}=\frac{24}{5}.\]"),("Conclude",r"The answer is $\boxed{\frac{24}{5}}$."),],
22:[("Model heads and tails as binary strings",r"Each coin flip outcome is a circular string of length $8$, where heads means a person stands. There are $2^8=256$ total outcomes."),("Count by number of standing people",r"With no adjacent standing people on a circle of $8$, there can be $0$, $1$, $2$, $3$, or $4$ people standing."),("Use circular spacing counts",r"The counts are $1$ for zero heads, $8$ for one head, $20$ for two heads, $16$ for three heads, and $2$ for four heads."),("Add favorable outcomes",r"The total favorable count is $1+8+20+16+2=47$."),("Compute probability",r"The probability is $\frac{47}{256}$."),("Conclude",r"The answer is $\boxed{\frac{47}{256}}$."),],
23:[("Use Vieta's formulas",r"Let the integer zeroes be $r$ and $s$. Then $r+s=a$ and $rs=2a$."),("Eliminate a",r"Substitute $a=r+s$ into $rs=2a$ to get \[rs=2r+2s.\]"),("Factor by shifting",r"Rearrange as \[rs-2r-2s=0,\] then add $4$ to get \[(r-2)(s-2)=4.\]"),("List integer factor pairs",r"The factor pairs for $4$ are $(1,4),(2,2),(4,1),(-1,-4),(-2,-2),(-4,-1)$. These give possible $a=r+s$ values $9,8,9,-1,0,-1$."),("Add distinct a values",r"The possible values of $a$ are $-1,0,8,9$. Their sum is $16$."),("Conclude",r"The answer is $\boxed{16}$."),],
24:[("Set coordinates",r"Let $B=(0,0)$ and $C=(x,0)$, where $BC=x$ is a positive integer. Since $AB=2$ and the angle at $B$ is right, put $A=(0,2)$."),("Use CD equal to AD",r"Let $CD=h$, so $D=(x,h)$ and $AD=h$. The equation $AD^2=h^2$ gives \[x^2+(h-2)^2=h^2.\]"),("Simplify to a square condition",r"This becomes $x^2=4h-4=4(h-1)$. Hence $x$ must be even; write $x=2k$. Then $h=k^2+1$."),("Write the perimeter",r"The perimeter is \[p=AB+BC+CD+AD=2+2k+2(k^2+1)=2k^2+2k+4.\]"),("Count possible k",r"We need $2k^2+2k+4<2015$. This holds for $k=1,2,\ldots,31$ and fails for $k=32$."),("Conclude",r"There are $\boxed{31}$ possible perimeters."),],
25:[("Separate side relationships",r"Choose the side of the first point. The second point is on the same side with probability $\frac14$, on an adjacent side with probability $\frac12$, and on the opposite side with probability $\frac14$."),("Same side",r"If both points are on the same side, their positions are two independent numbers in $[0,1]$. The probability their distance is at least $\frac12$ is the area where $|x-y|\ge\frac12$, which is $\frac14$."),("Adjacent sides",r"If the points are on adjacent sides meeting at a corner, their distance is $\sqrt{x^2+y^2}$. The bad region for distance less than $\frac12$ is a quarter circle of radius $\frac12$, with area $\frac{\pi}{16}$, so the good probability is $1-\frac{\pi}{16}$."),("Opposite sides",r"If the points are on opposite sides, their distance is always at least $1$, so it is certainly at least $\frac12$."),("Combine cases",r"The total probability is \[\frac14\cdot\frac14+\frac12\left(1-\frac{\pi}{16}\right)+\frac14=\frac{26-\pi}{32}.\]"),("Conclude",r"Thus $(a,b,c)=(26,1,32)$, so $a+b+c=\boxed{59}$."),],
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
    if n == 25:
        notes = "This page uses the corrected distance threshold $1/2$; the CSV OCR text omitted the denominator."
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in set() else notes
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
                "needs_review": int(r["problem_no"]) in {25},
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












































