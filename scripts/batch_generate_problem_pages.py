from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 18
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2004_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21, 22, 23, 24}
SKIPPED = ["2004 AMC 10B Problem 25: shaded two-circle/lens region requires the original figure and choices are missing from OCR."]
BATCH_LABEL = "2004 AMC 10B Problem 21-25"
NEXT_START = "2005 AMC 10A Problem 1"

ANS = {
    21: ("A", "3722"),
    22: ("D", r"\frac{\sqrt{65}}{2}"),
    23: ("B", r"\frac{5}{16}"),
    24: ("B", r"\frac{5}{3}"),
}


OV = {
    21: (
        r"Let $1,4,\ldots$ and $9,16,\ldots$ be two arithmetic progressions. The set $S$ is the union of the first $2004$ terms of each sequence. How many distinct numbers are in $S$?",
        [("A", "$3722$"), ("B", "$3732$"), ("C", "$3914$"), ("D", "$3924$"), ("E", "$4007$")],
    ),
    22: (
        r"A triangle with sides $5$, $12$, and $13$ has both an inscribed and a circumscribed circle. What is the distance between the centers of those circles?",
        [("A", r"$\frac{3\sqrt5}{2}$"), ("B", r"$\frac72$"), ("C", r"$\frac{\sqrt{15}}{2}$"), ("D", r"$\frac{\sqrt{65}}{2}$"), ("E", r"$\frac92$")],
    ),
    23: (
        r"Each face of a cube is painted either red or blue, each with probability $1/2$. The color of each face is determined independently. What is the probability that the painted cube can be placed on a horizontal surface so that the four vertical faces are all the same color?",
        [("A", r"$\frac14$"), ("B", r"$\frac5{16}$"), ("C", r"$\frac38$"), ("D", r"$\frac7{16}$"), ("E", r"$\frac12$")],
    ),
    24: (
        r"In $\triangle ABC$ we have $AB=7$, $AC=8$, and $BC=9$. Point $D$ is on the circumscribed circle of the triangle so that $AD$ bisects $\angle BAC$. What is the value of $AD/CD$?",
        [("A", r"$\frac98$"), ("B", r"$\frac53$"), ("C", "$2$"), ("D", r"$\frac{17}{7}$"), ("E", r"$\frac52$")],
    ),
}


KEY_OVERRIDES = {
    21: "Use inclusion-exclusion on two finite arithmetic progressions.",
    22: "Place the right triangle on coordinates and locate the incenter and circumcenter.",
    23: "Count colorings where one pair of opposite faces can be top and bottom.",
    24: "Use the angle-bisector theorem, power of a point, and Ptolemy's theorem.",
}


SOL = {
    21: [
        ("Describe the two progressions", r"The first progression is $1,4,7,\ldots$, so its terms are $1+3k$ for $0\le k\le2003$. The second is $9,16,23,\ldots$, so its terms are $9+7j$ for $0\le j\le2003$."),
        ("Use inclusion-exclusion", r"If there were no overlap, the union would have $2004+2004=4008$ numbers. We need to subtract the common terms."),
        ("Solve for overlaps", r"A common term satisfies $1+3k=9+7j$, so $3k-7j=8$. Modulo $7$, this gives $3k\equiv1\pmod7$, so $k\equiv5\pmod7$."),
        ("Count valid k values", r"Thus $k=5+7t$. The condition $k\le2003$ gives $5+7t\le2003$, so $t=0,1,\ldots,285$. That gives $286$ overlaps; the corresponding $j=1+3t$ values are also within range."),
        ("Compute the union size", r"Therefore $|S|=4008-286=\boxed{3722}$."),
    ],
    22: [
        ("Recognize the right triangle", r"A $5$-$12$-$13$ triangle is right. Put the right angle at the origin, with legs along the axes."),
        ("Locate the circumcenter", r"For a right triangle, the circumcenter is the midpoint of the hypotenuse. With legs $5$ and $12$, this point is $(5/2,6)$."),
        ("Locate the incenter", r"The inradius of a right triangle is $r=\frac{5+12-13}{2}=2$. With the right angle at the origin, the incenter is $(2,2)$."),
        ("Find the distance", r"The distance between $(5/2,6)$ and $(2,2)$ is \[\sqrt{\left(\frac12\right)^2+4^2}=\sqrt{\frac14+16}=\frac{\sqrt{65}}{2}.\]"),
        ("Answer", r"The distance is $\boxed{\frac{\sqrt{65}}{2}}$."),
    ],
    23: [
        ("Rephrase the placement condition", r"Choosing how to place the cube means choosing one pair of opposite faces to be top and bottom. The other four faces must all have the same color."),
        ("Count one axis", r"For a fixed opposite pair chosen as top and bottom, the four remaining faces can all be red or all be blue: $2$ choices. The top and bottom faces are arbitrary: $2^2=4$ choices. So one axis gives $8$ colorings."),
        ("Use inclusion-exclusion over three axes", r"There are $3$ opposite-face pairs, so the first count is $3\cdot8=24$. If two axes both work, then all six faces must be the same color, giving $2$ colorings. There are $3$ pairwise intersections, and the triple intersection is also those same $2$ colorings."),
        ("Count favorable colorings", r"By inclusion-exclusion, the number of favorable colorings is $24-3\cdot2+2=20$."),
        ("Divide by all colorings", r"There are $2^6=64$ total colorings, so the probability is $20/64=\boxed{\frac5{16}}$."),
    ],
    24: [
        ("Use the angle bisector point on BC", r"Let the angle bisector from $A$ meet $BC$ at $E$. By the angle-bisector theorem, $BE:EC=AB:AC=7:8$. Since $BC=9$, we get $BE=21/5$ and $EC=24/5$."),
        ("Find AE", r"The angle-bisector length formula gives \[AE^2=AB\cdot AC\left(1-\frac{BC^2}{(AB+AC)^2}\right)=56\left(1-\frac{81}{225}\right)=\frac{896}{25}.\] Thus $AE=\frac{8\sqrt{14}}5$."),
        ("Use power of a point", r"Since chords $AD$ and $BC$ intersect at $E$, we have $EA\cdot ED=EB\cdot EC$. Therefore \[ED=\frac{(21/5)(24/5)}{8\sqrt{14}/5}=\frac{9\sqrt{14}}{10}.\]"),
        ("Find AD", r"Then $AD=AE+ED=\frac{8\sqrt{14}}5+\frac{9\sqrt{14}}{10}=\frac{5\sqrt{14}}2$."),
        ("Use Ptolemy", r"Because $AD$ bisects $\angle BAC$, arcs $BD$ and $DC$ are equal, so chords $BD$ and $CD$ are equal. Let each be $x$. Ptolemy on cyclic quadrilateral $ABDC$ gives $AC\cdot BD+AB\cdot CD=AD\cdot BC$, so $8x+7x=9AD$. Hence $x=3AD/5$, and $AD/CD=AD/x=\boxed{\frac53}$."),
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
        if r["year"] == "2004" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "本批完成 2004 AMC 10B Problems 21-24；Problem 25 因图形/OCR 缺失跳过。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题，遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
