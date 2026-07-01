from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 46
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2009_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21, 22, 23, 24, 25}
SKIPPED = []
BATCH_LABEL = "2009 AMC 10A Problems 21-25"
NEXT_START = "2009 AMC 10B Problem 1"

ANS={21:("C",r"4(3-2\sqrt2)"),22:("D",r"\frac{2}{11}"),23:("E","6"),24:("C",r"\frac{4}{7}"),25:("B","7")}

OV={
21:(r"Many Gothic cathedrals have windows with portions containing a ring of congruent circles that are circumscribed by a larger circle. In the figure shown, the number of smaller circles is four. What is the ratio of the sum of the areas of the four smaller circles to the area of the larger circle?",[("A",r"$3-2\sqrt2$"),("B",r"$2-\sqrt2$"),("C",r"$4(3-2\sqrt2)$"),("D",r"$\frac12(3-\sqrt2)$"),("E",r"$2\sqrt2-2$")]),
22:(r"Two cubical dice each have removable numbers $1$ through $6$. The twelve numbers on the two dice are removed, put into a bag, then drawn one at a time and randomly reattached to the faces of the cubes, one number to each face. The dice are then rolled and the numbers on the two top faces are added. What is the probability that the sum is $7$?",[("A",r"$\frac19$"),("B",r"$\frac18$"),("C",r"$\frac16$"),("D",r"$\frac{2}{11}$"),("E",r"$\frac15$")]),
23:(r"Convex quadrilateral $ABCD$ has $AB=9$ and $CD=12$. Diagonals $AC$ and $BD$ intersect at $E$, $AC=14$, and $\triangle AED$ and $\triangle BEC$ have equal areas. What is $AE$?",[("A",r"$\frac92$"),("B",r"$\frac{50}{11}$"),("C",r"$\frac{21}{4}$"),("D",r"$\frac{17}{3}$"),("E","$6$")]),
24:(r"Three distinct vertices of a cube are chosen at random. What is the probability that the plane determined by these three vertices contains points inside the cube?",[("A",r"$\frac14$"),("B",r"$\frac38$"),("C",r"$\frac47$"),("D",r"$\frac57$"),("E",r"$\frac34$")]),
25:(r"For $k>0$, let $I_k=10\ldots064$, where there are $k$ zeros between the $1$ and the $6$. Let $N(k)$ be the number of factors of $2$ in the prime factorization of $I_k$. What is the maximum value of $N(k)$?",[("A","$6$"),("B","$7$"),("C","$8$"),("D","$9$"),("E","$10$")]),
}

KEY_OVERRIDES={21:"Relate the small circle radius to the large circle radius using the square formed by the four centers.",22:"Treat the two top faces as two drawn number labels from the twelve labels without replacement.",23:"Use equal areas to get a ratio on one diagonal, then compare similar scale factors from AB and CD.",24:"Count triples of cube vertices, excluding triples that lie on a face plane.",25:"Use 2-adic valuation of 10^(k+2)+64 and check the special case when powers of 2 match."}

SOL={
21:[("Name the radii",r"Let each small circle have radius $r$, and let the large circle have radius $R$."),("Use the four-circle geometry",r"The centers of the four small circles form a square. Adjacent small circles are tangent, so the side length of this square is $2r$. The distance from the center of the large circle to a small-circle center is half the diagonal, or $r\sqrt2$."),("Find the large radius",r"The large radius reaches from the center of the large circle to a small-circle center, then one more small radius to the outer tangency point. Thus $R=r\sqrt2+r=r(1+\sqrt2)$."),("Compare areas",r"The sum of the four small areas is $4\pi r^2$, and the large area is $\pi R^2=\pi r^2(1+\sqrt2)^2$. The ratio is $\frac{4}{(1+\sqrt2)^2}$."),("Simplify",r"Since $(1+\sqrt2)^2=3+2\sqrt2$, the ratio is $\frac{4}{3+2\sqrt2}=4(3-2\sqrt2)$."),("Answer",r"The ratio is $\boxed{4(3-2\sqrt2)}$.")],
22:[("Model the top labels",r"After the labels are randomly attached, the two top faces are like two labels chosen from the twelve labels without replacement, one from each die after labeling."),("Count all ordered possibilities",r"There are $12$ choices for the first top label and $11$ remaining choices for the second, so $132$ ordered label choices."),("Count sums of 7",r"The ordered value pairs that sum to $7$ are $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$. For each ordered value pair, there are $2$ copies of the first value and $2$ copies of the second, giving $4$ label choices."),("Compute favorable choices",r"There are $6\cdot4=24$ favorable ordered choices."),("Find the probability",r"The probability is $\frac{24}{132}=\frac{2}{11}$."),("Answer",r"The answer is $\boxed{\frac{2}{11}}$.")],
23:[("Use the equal-area condition",r"Triangles $AED$ and $BEC$ share the vertical angle at $E$. Their areas are proportional to $AE\cdot DE$ and $BE\cdot CE$. Equal areas give $AE\cdot DE=BE\cdot CE$."),("Turn that into a ratio",r"So $\frac{DE}{BE}=\frac{CE}{AE}$. This means the scale from triangle $ABE$ to triangle $CDE$ is reciprocal along both diagonals."),("Compare AB and CD",r"Using the law of cosines with the same included angle at $E$, this ratio implies $\frac{AE}{CE}=\frac{AB}{CD}=\frac{9}{12}=\frac34$."),("Use AC=14",r"Let $AE=x$, so $CE=14-x$. Then $\frac{x}{14-x}=\frac34$."),("Solve",r"We get $4x=3(14-x)$, so $7x=42$ and $x=6$."),("Answer",r"Therefore $AE=\boxed{6}$.")],
24:[("Count all triples",r"There are $\binom83=56$ ways to choose three distinct vertices of a cube."),("Identify the bad triples",r"A plane through three vertices fails to contain interior points of the cube exactly when those three vertices lie on one face of the cube. Then the plane is just a face plane."),("Count face triples",r"Each of the $6$ faces has $4$ vertices, and choosing any $3$ of them gives $\binom43=4$ triples. A three-vertex set lies on only one face, so there are $6\cdot4=24$ bad triples."),("Subtract",r"The favorable triples are $56-24=32$."),("Compute the probability",r"The probability is $\frac{32}{56}=\frac47$."),("Answer",r"The answer is $\boxed{\frac47}$.")],
25:[("Write the number algebraically",r"The number $I_k$ has digits $1$, then $k$ zeros, then $64$, so $I_k=10^{k+2}+64$."),("Factor powers of 2",r"This is $2^{k+2}5^{k+2}+2^6$. The number of factors of $2$ depends on which of $k+2$ and $6$ is smaller, except when they are equal."),("Handle k less than 4",r"If $k<4$, then $k+2<6$, and factoring out $2^{k+2}$ leaves an odd number. So $N(k)=k+2\le5$."),("Handle k greater than 4",r"If $k>4$, factoring out $2^6$ leaves an odd number, so $N(k)=6$."),("Check the special case",r"When $k=4$, the two terms have the same power $2^6$: $I_4=2^6(5^6+1)$. Since $5^6+1=15626$ is divisible by $2$ but not by $4$, this gives $N(4)=7$."),("Answer",r"The maximum value is $\boxed{7}$.")],
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
        if r["year"] == "2009" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {21},
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
        + "- Answer verification source: AoPS 2009 AMC 10A Answer Key\n\n"
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








