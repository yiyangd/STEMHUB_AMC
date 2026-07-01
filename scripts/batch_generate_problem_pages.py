import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 105
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2018_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2018 AMC 10A Problems 21-25"
NEXT_START = "2018 AMC 10B Problem 1"

ANS={21:("E",r"a>\frac12"),22:("D","13"),23:("D",r"\frac{145}{147}"),24:("D","75"),25:("D","18")}

OV={
21:(r"Which of the following describes the set of values of $a$ for which the curves $x^2+y^2=a^2$ and $y=x^2-a$ in the real $xy$-plane intersect at exactly $3$ points?",[("A",r"$a=\frac14$"),("B",r"$\frac14<a<\frac12$"),("C",r"$a>\frac14$"),("D",r"$a=\frac12$"),("E",r"$a>\frac12$")]),
22:(r"Let $a,b,c,d$ be positive integers such that $\gcd(a,b)=24$, $\gcd(b,c)=36$, $\gcd(c,d)=54$, and $70<\gcd(d,a)<100$. Which of the following must be a divisor of $a$?",[("A","5"),("B","7"),("C","11"),("D","13"),("E","17")]),
23:(r"Farmer Pythagoras has a field in the shape of a right triangle whose legs have lengths $3$ and $4$. In the right-angle corner, he leaves a small unplanted square $S$ so that it looks like the right angle symbol. The rest of the field is planted. The shortest distance from $S$ to the hypotenuse is $2$ units. What fraction of the field is planted?",[("A",r"$\frac{17}{18}$"),("B",r"$\frac{35}{36}$"),("C",r"$\frac{143}{144}$"),("D",r"$\frac{145}{147}$"),("E",r"$\frac{26}{27}$")]),
24:(r"Triangle $ABC$ with $AB=50$ and $AC=10$ has area $120$. Let $D$ be the midpoint of $AB$, and let $E$ be the midpoint of $AC$. The angle bisector of $\angle BAC$ intersects $DE$ and $BC$ at $F$ and $G$, respectively. What is the area of quadrilateral $FDBG$?",[("A","60"),("B","65"),("C","70"),("D","75"),("E","80")]),
25:(r"For a positive integer $n$ and nonzero digits $a,b,c$, let $A_n$ be the $n$-digit integer each of whose digits is $a$, let $B_n$ be the $n$-digit integer each of whose digits is $b$, and let $C_n$ be the $2n$-digit integer each of whose digits is $c$. What is the greatest possible value of $a+b+c$ for which there are at least two values of $n$ such that $C_n-B_n=A_n^2$?",[("A","12"),("B","14"),("C","16"),("D","18"),("E","20")]),
}

KEY_OVERRIDES={21:"Substitute the parabola into the circle and count real x-values.",22:"Track forced prime factors through the gcd conditions.",23:"Use distance from a square corner to the hypotenuse.",24:"Use the angle bisector theorem and midpoint similarity to get an area ratio.",25:"Express repdigits using $R_n=(10^n-1)/9$ and compare coefficients."}

SOL={
21:[("Substitute the parabola into the circle",r"Using $y=x^2-a$ in $x^2+y^2=a^2$ gives \[x^2+(x^2-a)^2=a^2.\]"),("Simplify",r"Expanding and canceling $a^2$ gives \[x^2+x^4-2ax^2=0,\] or \[x^2(x^2+1-2a)=0.\]"),("Count solutions for x",r"The factor $x^2=0$ always gives $x=0$, which gives one intersection point. The other factor gives \[x^2=2a-1.\]"),("Require two more points",r"To have exactly three intersection points, we need two additional real nonzero $x$-values, so $2a-1>0$."),("Conclude",r"Thus $a>\frac12$, so the answer is $\boxed{a>\frac12}$."),],
22:[("Factor the given gcds",r"\[\gcd(a,b)=24=2^3\cdot3,\quad \gcd(b,c)=36=2^2\cdot3^2,\quad \gcd(c,d)=54=2\cdot3^3.\]"),("Track what a cannot have",r"Because $\gcd(a,b)$ has only one factor of $3$ while $\gcd(b,c)$ has $3^2$, the number $a$ is not forced to have $3^2$. Also $a$ is divisible by $2^3\cdot3$."),("Track d",r"Because $\gcd(c,d)=54$, the number $d$ is divisible by $2\cdot3^3$, but not forced to have $2^2$."),("Use gcd d a",r"The common part of $d$ and $a$ must include $2\cdot3=6$, and the condition says \[70<\gcd(d,a)<100.\] Thus \[\gcd(d,a)=6q\] with $12<q<17$."),("Find q",r"The integer $q$ cannot have extra factors $2$ or $3$, and the only possibility from $13,14,15,16$ is $13$."),("Conclude",r"Therefore $13$ must divide $a$, so the answer is $\boxed{13}$."),],
23:[("Set up the right triangle",r"Place the right angle at the origin, with the legs along the axes. The hypotenuse of the $3$-$4$-$5$ triangle has equation \[4X+3Y=12.\]"),("Let the square side be s",r"The unplanted square in the right-angle corner has farthest corner $(s,s)$. That corner is closest to the hypotenuse."),("Use the distance to the hypotenuse",r"The distance from $(s,s)$ to line $4X+3Y=12$ is \[\frac{12-7s}{5}.\] This is given as $2$, so \[\frac{12-7s}{5}=2.\]"),("Solve for s",r"This gives $12-7s=10$, so $s=\frac27$."),("Find the planted fraction",r"The field area is $\frac12\cdot3\cdot4=6$. The unplanted square area is $\frac4{49}$. The planted fraction is \[\frac{6-\frac4{49}}{6}=\frac{145}{147}.\]"),("Conclude",r"The answer is $\boxed{\frac{145}{147}}$."),],
24:[("Use area coordinates",r"Use $A$ as the origin and think of $B$ and $C$ as basis vectors. In these coordinates, $D=(\frac12,0)$ and $E=(0,\frac12)$."),("Locate G by the angle bisector theorem",r"The angle bisector meets $BC$ at $G$ with \[BG:GC=AB:AC=50:10=5:1.\] Thus \[G=\left(\frac16,\frac56\right)\] in the $(B,C)$ coordinate system."),("Locate F by midpoint similarity",r"Segment $DE$ is the image of $BC$ under dilation centered at $A$ with scale factor $\frac12$. Therefore the angle bisector meets $DE$ at \[F=\frac12G=\left(\frac1{12},\frac5{12}\right).\]"),("Find the area ratio",r"Using the shoelace formula on $F,D,B,G$ in these coordinates gives area $\frac{5}{16}$ of the parallelogram spanned by $B$ and $C$. Since $\triangle ABC$ is half that parallelogram, \[[FDBG]=\frac58[ABC].\]"),("Compute",r"The area is \[\frac58\cdot120=75.\]"),("Conclude",r"The answer is $\boxed{75}$."),],
25:[("Write repdigits algebraically",r"Let \[R_n=\frac{10^n-1}{9}.\] Then $A_n=aR_n$, $B_n=bR_n$, and $C_n=cR_{2n}=cR_n(10^n+1)$."),("Use the equation",r"The equation $C_n-B_n=A_n^2$ becomes \[cR_n(10^n+1)-bR_n=a^2R_n^2.\] Divide by $R_n$ to get \[c(10^n+1)-b=a^2\frac{10^n-1}{9}.\]"),("Compare as a function of 10 to the n",r"Multiplying by $9$ gives \[(9c-a^2)10^n+(9c-9b+a^2)=0.\] This must hold for at least two different values of $n$, so both coefficients must be $0$."),("Solve digit conditions",r"Thus \[a^2=9c,\quad 9c-9b+a^2=0.\] Using $a^2=9c$, the second equation gives $b=2c$."),("Maximize digit sum",r"The digit possibilities with $a^2=9c$ are $(a,c)=(3,1)$ and $(6,4)$, while $(9,9)$ would make $b=18$, not a digit. The best is $a=6$, $c=4$, $b=8$, giving $a+b+c=18$."),("Conclude",r"The greatest possible value is $\boxed{18}$."),],
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
        if r["year"] == "2018" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2018 AMC 10A Answer Key\n\n"
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












































