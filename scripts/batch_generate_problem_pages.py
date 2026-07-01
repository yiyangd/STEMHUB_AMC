from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 49
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2009_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21, 22, 23, 24, 25}
SKIPPED = []
BATCH_LABEL = "2009 AMC 10B Problems 21-25"
NEXT_START = "2010 AMC 10A Problem 1"

ANS={21:("D","4"),22:("B",r"\frac{32}{5}"),23:("C",r"\frac{3}{16}"),24:("A","100"),25:("B",r"\frac{3}{16}")}

OV={
21:(r"What is the remainder when $3^0+3^1+3^2+\cdots+3^{2009}$ is divided by $8$?",[("A","$0$"),("B","$1$"),("C","$2$"),("D","$4$"),("E","$6$")]),
22:(r"A cubical cake with edge length $2$ inches is iced on the sides and the top. It is cut vertically into three pieces as shown in a top view, where $M$ is the midpoint of a top edge. The piece whose top is triangle $B$ contains $c$ cubic inches of cake and $s$ square inches of icing. What is $c+s$?",[("A",r"$\frac{24}{5}$"),("B",r"$\frac{32}{5}$"),("C",r"$8+\sqrt5$"),("D",r"$5+\frac{16\sqrt5}{5}$"),("E",r"$10+5\sqrt5$")]),
23:(r"Rachel and Robert run on a circular track. Rachel runs counterclockwise and completes a lap every $90$ seconds, and Robert runs clockwise and completes a lap every $80$ seconds. Both start from the starting line at the same time. At some random time between $10$ minutes and $11$ minutes after they begin to run, a photographer standing inside the track takes a picture that shows one-fourth of the track, centered on the starting line. What is the probability that both Rachel and Robert are in the picture?",[("A",r"$\frac{1}{16}$"),("B",r"$\frac18$"),("C",r"$\frac{3}{16}$"),("D",r"$\frac14$"),("E",r"$\frac{5}{16}$")]),
24:(r"The keystone arch is an ancient architectural feature. It is composed of congruent isosceles trapezoids fitted together along the non-parallel sides, as shown. The bottom sides of the two end trapezoids are horizontal. In an arch made with $9$ trapezoids, let $x$ be the angle measure in degrees of the larger interior angle of the trapezoid. What is $x$?",[("A","$100$"),("B","$102$"),("C","$104$"),("D","$106$"),("E","$108$")]),
25:(r"Each face of a cube is given a single narrow stripe painted from the center of one edge to the center of the opposite edge. The choice of the edge pairing is made at random and independently for each face. What is the probability that there is a continuous stripe encircling the cube?",[("A",r"$\frac18$"),("B",r"$\frac{3}{16}$"),("C",r"$\frac14$"),("D",r"$\frac38$"),("E",r"$\frac12$")]),
}

KEY_OVERRIDES={21:"Use the repeating pattern of powers of 3 modulo 8.",22:"Use the top-view triangle area for volume and count only the original iced surfaces on that piece.",23:"Convert each runner's visible interval into a time interval and intersect them.",24:"Nine congruent trapezoids split a 180-degree turn, so each trapezoid turns by 20 degrees.",25:"A continuous stripe can encircle the cube in one of three belt directions, each requiring four independent face choices."}

SOL={
21:[("Find the cycle modulo 8",r"Modulo $8$, powers of $3$ alternate: $3^0\equiv1$, $3^1\equiv3$, $3^2\equiv1$, $3^3\equiv3$, and so on."),("Pair the terms",r"Each pair $3^{2k}+3^{2k+1}$ is congruent to $1+3=4\pmod8$."),("Count the terms",r"From exponent $0$ through $2009$ there are $2010$ terms, or $1005$ pairs."),("Reduce the total",r"The sum is congruent to $1005\cdot4\equiv 4\pmod8$, because an odd multiple of $4$ leaves remainder $4$ when divided by $8$."),("Answer",r"The remainder is $\boxed{4}$.")],
22:[("Use the top-view geometry",r"In the top view, the square has side $2$. The triangular top of piece $B$ has the full right edge of length $2$ as a base, and its perpendicular distance to the opposite cut point is $\frac45$."),("Find the top area",r"So the top area of piece $B$ is $\frac12\cdot2\cdot\frac45=\frac45$ square inch."),("Find the cake volume",r"The cuts are vertical and the cake height is $2$, so the volume is $c=2\cdot\frac45=\frac85$."),("Find the icing area",r"The piece has icing on its top, area $\frac45$, and on the original right side of the cube, area $2\cdot2=4$. The new cut faces are not iced. Thus $s=4+\frac45=\frac{24}{5}$."),("Add",r"Therefore $c+s=\frac85+\frac{24}{5}=\frac{32}{5}$."),("Answer",r"The value is $\boxed{\frac{32}{5}}$.")],
23:[("Translate the picture into time intervals",r"A photo shows one-fourth of the track centered at the starting line, so each runner is visible when within one-eighth of a lap on either side of the starting line."),("Find Rachel's visible times",r"Rachel completes a lap every $90$ seconds, so she is visible for $\frac18\cdot90=11.25$ seconds before and after each multiple of $90$. Between $600$ and $660$ seconds, the relevant multiple is $630$, giving $[618.75,641.25]$."),("Find Robert's visible times",r"Robert completes a lap every $80$ seconds, so he is visible for $10$ seconds before and after each multiple of $80$. The relevant multiple is $640$, giving $[630,650]$."),("Intersect the intervals",r"Both runners are visible from $630$ to $641.25$, a length of $11.25$ seconds."),("Compute the probability",r"The random time is chosen from a $60$-second interval, so the probability is $\frac{11.25}{60}=\frac{45}{240}=\frac{3}{16}$."),("Answer",r"The probability is $\boxed{\frac{3}{16}}$.")],
24:[("Find the turn per trapezoid",r"The arch goes from one horizontal end to the other, making a total turn of $180^\circ$. With $9$ congruent trapezoids, each one accounts for $180^\circ/9=20^\circ$ of turning."),("Connect turn to trapezoid angles",r"In an isosceles trapezoid, the larger base angle exceeds $90^\circ$ by half of this turn angle."),("Compute the larger angle",r"So the larger interior angle is $90^\circ+\frac{20^\circ}{2}=100^\circ$."),("Answer",r"Thus $x=\boxed{100}$." )],
25:[("Identify possible belts",r"A continuous stripe can encircle the cube around one of three directions, corresponding to the three pairs of opposite faces of the cube."),("Find the probability for one belt",r"For a fixed belt direction, the four side faces around that belt must each choose the stripe orientation that continues the belt. Each face has probability $\frac12$ of choosing that orientation."),("Multiply for one belt",r"Thus one specified belt occurs with probability $(\frac12)^4=\frac1{16}$. The two end faces do not affect that belt."),("Use the three directions",r"There are $3$ possible belt directions. Two different belt directions cannot occur at the same time because a shared face would need two perpendicular stripe orientations."),("Add the disjoint cases",r"Therefore the total probability is $3\cdot\frac1{16}=\frac3{16}$."),("Answer",r"The probability is $\boxed{\frac{3}{16}}$.")],
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
        if r["year"] == "2009" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {22, 24},
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
        + "- Answer verification source: AoPS 2009 AMC 10B Answer Key\n\n"
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












