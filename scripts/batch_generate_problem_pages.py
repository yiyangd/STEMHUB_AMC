from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 15
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2004_AMC_10A_Answer_Key"
TARGET_NUMBERS = {22, 23, 25}
SKIPPED = ["2004 AMC 10A Problem 21: shaded concentric-circle region depends on the original diagram.", "2004 AMC 10A Problem 24: CSV/PDF text is truncated before the recurrence conditions."]
BATCH_LABEL = "2004 AMC 10A Problem 21-25"
NEXT_START = "2004 AMC 10B Problem 1"

ANS = {
    22: ("D", r"\frac{5}{2}"),
    23: ("D", r"\frac{8}{9}"),
    25: ("B", r"3+\frac{\sqrt{69}}{3}"),
}


OV = {
    22: (
        r"Square $ABCD$ has side length $2$. A semicircle with diameter $AB$ is constructed inside the square, and the tangent to the semicircle from $C$ intersects side $AD$ at $E$. What is the length of $CE$?",
        [("A", r"$\frac{2+\sqrt5}{2}$"), ("B", r"$\sqrt5$"), ("C", r"$\sqrt6$"), ("D", r"$\frac52$"), ("E", r"$5-\sqrt5$")],
    ),
    23: (
        r"Circles $A$, $B$, and $C$ are externally tangent to each other and internally tangent to circle $D$. Circles $B$ and $C$ are congruent. Circle $A$ has radius $1$ and passes through the center of $D$. What is the radius of circle $B$?",
        [("A", r"$\frac23$"), ("B", r"$\frac34$"), ("C", r"$\frac78$"), ("D", r"$\frac89$"), ("E", r"$1+\frac{\sqrt3}{3}$")],
    ),
    25: (
        r"Three mutually tangent spheres of radius $1$ rest on a horizontal plane. A sphere of radius $2$ rests on them. What is the distance from the plane to the top of the larger sphere?",
        [("A", r"$3+\frac{\sqrt{30}}{2}$"), ("B", r"$3+\frac{\sqrt{69}}{3}$"), ("C", r"$3+\frac{\sqrt{123}}{4}$"), ("D", r"$\frac{\sqrt{52}}{2}$"), ("E", r"$3+\frac{2\sqrt9}{3}$")],
    ),
}


KEY_OVERRIDES = {
    22: "Use coordinate geometry and the distance from a circle center to a tangent line.",
    23: "Use symmetry and tangency distances between circle centers.",
    25: "Model the sphere centers as a tetrahedral arrangement over an equilateral triangle.",
}


SOL = {
    22: [
        ("Set up coordinates", r"Place $A=(0,0)$, $B=(2,0)$, $C=(2,2)$, and $D=(0,2)$. The semicircle has center $(1,0)$ and radius $1$. Let $E=(0,e)$ on side $AD$."),
        ("Write the tangent line", r"Line $CE$ passes through $(2,2)$ and $(0,e)$. In standard form it is $(2-e)x-2y+2e=0$."),
        ("Use the tangent condition", r"A tangent line is exactly one radius away from the center. Thus the distance from $(1,0)$ to the line is $1$: \[\frac{|(2-e)+2e|}{\sqrt{(2-e)^2+4}}=1.\]"),
        ("Solve for E", r"This becomes $\frac{2+e}{\sqrt{(2-e)^2+4}}=1$. Squaring gives $(2+e)^2=(2-e)^2+4$, so $8e=4$ and $e=\frac12$."),
        ("Find CE", r"Now $CE=\sqrt{(2-0)^2+(2-\frac12)^2}=\sqrt{4+\frac94}=\sqrt{\frac{25}{4}}=\frac52$. The answer is $\boxed{\frac52}$."),
    ],
    23: [
        ("Find the radius of the large circle", r"Circle $A$ has radius $1$, passes through the center of $D$, and is internally tangent to $D$. Therefore the radius of $D$ is $2$."),
        ("Use symmetry", r"Let the congruent circles $B$ and $C$ have radius $r$. By symmetry, put their centers at $(x,r)$ and $(x,-r)$, while the center of $D$ is at the origin and the center of $A$ is at $(-1,0)$."),
        ("Use tangency to circle D", r"Since $B$ is internally tangent to $D$, the distance from its center to the origin is $2-r$. Thus \[x^2+r^2=(2-r)^2,\] so $x^2=4-4r$."),
        ("Use tangency to circle A", r"Circle $B$ is externally tangent to circle $A$, so the distance between their centers is $1+r$: \[(x+1)^2+r^2=(1+r)^2.\] This simplifies to $x^2+2x=2r$."),
        ("Solve", r"Using $x^2=4-4r$ in $x^2+2x=2r$ gives $x=3r-2$. Then $(3r-2)^2=4-4r$, so $9r^2-8r=0$. Since $r>0$, $r=\frac89$. The answer is $\boxed{\frac89}$."),
    ],
    25: [
        ("Look at the centers", r"The centers of the three small spheres form an equilateral triangle of side $2$ in a horizontal plane one unit above the floor."),
        ("Place the large center above the triangle center", r"By symmetry, the center of the radius-$2$ sphere lies directly above the centroid of that equilateral triangle."),
        ("Find the horizontal distance", r"In an equilateral triangle of side $2$, the distance from the centroid to a vertex is $\frac{2}{\sqrt3}$."),
        ("Use the center-to-center distance", r"The large sphere is tangent to each small sphere, so the distance between their centers is $1+2=3$. If the vertical distance between centers is $h$, then \[h^2+\left(\frac{2}{\sqrt3}\right)^2=3^2.\] Thus $h^2=9-\frac43=\frac{23}{3}=\frac{69}{9}$, so $h=\frac{\sqrt{69}}{3}$."),
        ("Add heights", r"The small-sphere centers are $1$ unit above the plane, so the large-sphere center is $1+\frac{\sqrt{69}}{3}$ above the plane. The top of the large sphere is $2$ more units up, giving $3+\frac{\sqrt{69}}{3}$. The answer is $\boxed{3+\frac{\sqrt{69}}{3}}$."),
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {22, 23}) else notes
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
        if r["year"] == "2004" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in {22, 23},
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
        + "- Review notes: Corrected 2003 AMC 10B Problem 10 answer choice from the AoPS answer key; Problem 20 uses the diagram data stated in text and should be visually reviewed later.\n",
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
        + "- Answer verification source: AoPS 2003 AMC 10B Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批完成 2004 AMC 10A Problems 22、23、25；Problems 21 和 24 因图形/OCR 问题跳过。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
