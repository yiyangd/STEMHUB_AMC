import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 73
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2013_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2013 AMC 10A Problems 21-25"
NEXT_START = "2013 AMC 10B Problem 1"

ANS = {21:("D","1925"),22:("B",r"\frac32"),23:("D","61"),24:("E","900"),25:("A","49")}

OV = {
21:(r"A group of $12$ pirates divide a chest of gold coins as follows. The $k$th pirate to take a share takes $\frac{k}{12}$ of the coins that remain in the chest. The initial number of coins is the smallest number for which every pirate receives a positive whole number of coins. How many coins does the $12$th pirate receive?",[("A","720"),("B","1296"),("C","1728"),("D","1925"),("E","3850")]),
22:(r"Six spheres of radius $1$ have centers at the vertices of a regular hexagon of side length $2$. The six spheres are internally tangent to a larger sphere whose center is the center of the hexagon. An eighth sphere is externally tangent to the six smaller spheres and internally tangent to the larger sphere. What is the radius of this eighth sphere?",[("A",r"\sqrt2"),("B",r"\frac32"),("C",r"\sqrt5"),("D",r"\sqrt3"),("E",r"\frac23")]),
23:(r"In $\triangle ABC$, $AB=86$ and $AC=97$. A circle with center $A$ and radius $AB$ intersects $BC$ at points $B$ and $X$. Moreover $BX$ and $CX$ have integer lengths. What is $BC$?",[("A","11"),("B","28"),("C","33"),("D","61"),("E","72")]),
24:(r"Central High School plays Northern High School in a backgammon match. Each school has three players, and each player plays two games against each player from the other school. The match has six rounds, with three games played simultaneously in each round. In how many different ways can the match be scheduled?",[("A","540"),("B","600"),("C","720"),("D","810"),("E","900")]),
25:(r"All diagonals are drawn in a regular octagon. At how many distinct points in the interior of the octagon, not on the boundary, do two or more diagonals intersect?",[("A","49"),("B","65"),("C","70"),("D","96"),("E","128")]),
}

KEY_OVERRIDES={21:"Work backward through the divisibility conditions on the remaining coins.",22:"Use symmetry and the Pythagorean theorem for the eighth sphere center.",23:"Use equal radii to create a chord and factor the difference of squares.",24:"View each round as a perfect matching between the two teams.",25:"Start with $\binom84$ intersections and correct for special concurrences in a regular octagon."}

SOL={
21:[("Track the remaining coins",r"Let $R_k$ be the number of coins left after the $k$th pirate takes a share. Pirate $k$ takes $\frac{k}{12}$ of $R_{k-1}$, so $R_k=\frac{12-k}{12}R_{k-1}$."),("Work backward",r"The $12$th pirate receives all of $R_{11}$. We want the smallest positive $R_{11}$ that makes every earlier remaining amount and every share an integer."),("Use the backward relation",r"For $k=11,10,\ldots,1$, the reverse formula is $R_{k-1}=\frac{12}{12-k}R_k$. Applying these divisibility requirements successively gives the smallest possible $R_{11}=1925$."),("Check the meaning",r"Since the $12$th pirate takes all coins remaining after the $11$th pirate, the $12$th pirate receives $R_{11}$."),("Conclude",r"The answer is $\boxed{1925}$."),],
22:[("Find the large sphere radius",r"The centers of the six small spheres are distance $2$ from the hexagon center. Since each small sphere has radius $1$ and is internally tangent to the large sphere, the large sphere has radius $3$."),("Place the eighth sphere by symmetry",r"The eighth sphere must lie on the line through the hexagon center perpendicular to the plane of the six centers. Let its radius be $r$ and its center be height $h$ above the hexagon plane."),("Write the tangency equations",r"Internal tangency to the large sphere gives $h+r=3$. External tangency to each small sphere gives $h^2+2^2=(r+1)^2$."),("Solve",r"Substitute $h=3-r$: $(3-r)^2+4=(r+1)^2$. This simplifies to $13-6r=r^2+2r+1-r^2$, so $12=8r$ and $r=\frac32$."),("Conclude",r"The radius is $\boxed{\frac32}$."),],
23:[("Use the equal radii",r"Since $B$ and $X$ lie on the circle centered at $A$, we have $AB=AX=86$. Thus $BX$ is a chord of that circle lying on line $BC$."),("Name the integer pieces",r"Let $BX=x$ and $CX=m$, where both are positive integers. Then $BC=x+m$."),("Compare right triangles",r"Drop the perpendicular from $A$ to line $BC$. It bisects chord $BX$, so the horizontal distances to $B$ and $X$ are both $x/2$. Comparing $AC^2$ and $AB^2$ gives \[(m+x/2)^2-(x/2)^2=97^2-86^2.\]"),("Factor",r"The left side is $m(m+x)$, and the right side is $2013=3\cdot11\cdot61$. Thus $m$ and $m+x=BC$ are factor pairs of $2013$."),("Use triangle inequality",r"The possible larger factors are $2013,671,183,61$. Since $BC<AB+AC=183$, only $61$ can work. The answer is $\boxed{61}$."),],
24:[("Model a round",r"In each round, the three games form a perfect matching between the three Central players and the three Northern players. There are $3!=6$ possible matchings for one round."),("Use the all-matchings schedule",r"If each of the $6$ possible matchings is used exactly once, then every cross-school pair occurs exactly twice. These schedules can be ordered in $6!=720$ ways."),("Find the other possible pattern",r"There are also two sets of three matchings that already cover every cross-school pair exactly once. Using each matching in one of these sets twice gives another valid schedule."),("Count those schedules",r"For each of the two such sets, the six-round order has three matchings repeated twice, so it can be arranged in $\frac{6!}{2!2!2!}=90$ ways. This contributes $2\cdot90=180$ schedules."),("Add",r"The total number of schedules is $720+180=900$. The answer is $\boxed{900}$."),],
25:[("Start with the general-position count",r"In a convex octagon with no three diagonals concurrent, each interior intersection comes from choosing $4$ vertices, so there would be $\binom84=70$ intersection points."),("Correct the center",r"In a regular octagon, the $4$ long diagonals connecting opposite vertices all meet at the center. The general count treats this as $\binom42=6$ intersections, but it is only one point, so subtract $5$."),("Correct the other triple intersections",r"Regular-octagon symmetry also creates $8$ other interior points where $3$ diagonals meet. Each such point is counted as $\binom32=3$ intersections in the general count but should be counted once, so each requires subtracting $2$."),("Compute",r"The corrected number is $70-5-8\cdot2=70-5-16=49$."),("Conclude",r"The answer is $\boxed{49}$."),],
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
        if r["year"] == "2013" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2013 AMC 10A Answer Key\n\n"
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









































