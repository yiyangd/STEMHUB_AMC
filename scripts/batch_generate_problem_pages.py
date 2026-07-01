import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 124
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2021_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,8,9,10}
SKIPPED = []
BATCH_LABEL = "2021 Spring AMC 10B Problems 1-10"
NEXT_START = "2021 Spring AMC 10B Problem 11"

ANS={1:("D","19"),2:("D",r"4\sqrt3"),3:("C","8"),4:("B","32"),5:("B","22"),6:("C","76"),7:("D",r"65\pi"),8:("A","367"),9:("D","7"),10:("A","1.5")}

OV={
1:(r"How many integer values of $x$ satisfy $|x|<3\pi$?",[("A","9"),("B","10"),("C","18"),("D","19"),("E","20")]),
2:(r"What is the value of \[\sqrt{(3-2\sqrt3)^2}+\sqrt{(3+2\sqrt3)^2}?\]",[("A","0"),("B",r"$4\sqrt3-6$"),("C","6"),("D",r"$4\sqrt3$"),("E",r"$4\sqrt3+6$")]),
3:(r"In an after-school program for juniors and seniors, there is a debate team with an equal number of students from each class on the team. Among the $28$ students in the program, $25\%$ of the juniors and $10\%$ of the seniors are on the debate team. How many juniors are in the program?",[("A","5"),("B","6"),("C","8"),("D","11"),("E","20")]),
4:(r"At a math contest, $57$ students are wearing blue shirts, and another $75$ students are wearing yellow shirts. The $132$ students are assigned into $66$ pairs. In exactly $23$ of these pairs, both students are wearing blue shirts. In how many pairs are both students wearing yellow shirts?",[("A","23"),("B","32"),("C","37"),("D","41"),("E","64")]),
5:(r"The ages of Jonie's four cousins are distinct single-digit positive integers. Two of the cousins' ages multiplied together give $24$, while the other two multiply to $30$. What is the sum of the ages of Jonie's four cousins?",[("A","21"),("B","22"),("C","23"),("D","24"),("E","25")]),
6:(r"Ms. Blackwell gives an exam to two classes. The mean of the scores of the students in the morning class is $84$, and the afternoon class's mean score is $70$. The ratio of the number of students in the morning class to the number of students in the afternoon class is $3:4$. What is the mean of the scores of all the students?",[("A","74"),("B","75"),("C","76"),("D","77"),("E","78")]),
7:(r"In a plane, four circles with radii $1,3,5,$ and $7$ are tangent to line $\ell$ at the same point $A$, but they may be on either side of $\ell$. Region $S$ consists of all the points that lie inside exactly one of the four circles. What is the maximum possible area of region $S$?",[("A",r"$24\pi$"),("B",r"$32\pi$"),("C",r"$64\pi$"),("D",r"$65\pi$"),("E",r"$84\pi$")]),
8:(r"Mr. Zhou places all the integers from $1$ to $225$ into a $15\times15$ grid. He places $1$ in the middle square and places the other numbers one by one clockwise in an outward spiral. What is the sum of the greatest and the least number that appear in the second row from the top?",[("A","367"),("B","368"),("C","369"),("D","379"),("E","380")]),
9:(r"The point $P(a,b)$ is first rotated counterclockwise by $90^\circ$ around $(1,5)$ and then reflected about the line $y=-x$. The image of $P$ is $(-6,3)$. What is $b-a$?",[("A","1"),("B","3"),("C","5"),("D","7"),("E","9")]),
10:(r"An inverted cone with base radius $12$ cm and height $18$ cm is full of water. The water is poured into a tall cylinder whose horizontal base has radius $24$ cm. What is the height, in centimeters, of the water in the cylinder?",[("A","1.5"),("B","3"),("C","4"),("D","4.5"),("E","6")]),
}

KEY_OVERRIDES={1:"Count integers inside a symmetric absolute-value interval.",2:"Use square root of a square as absolute value.",3:"Convert percentages to equations.",4:"Count pair types using the number of blue shirts.",5:"Factor the products into distinct one-digit ages.",6:"Use a weighted average.",7:"Place nested tangent circles to maximize exactly-one area.",8:"Model the spiral by coordinate rings.",9:"Undo coordinate transformations.",10:"Conserve volume from cone to cylinder."}

SOL={
1:[("Estimate the boundary",r"The inequality $|x|<3\pi$ means $x$ is between $-3\pi$ and $3\pi$. Since $\pi\approx3.14$, we have $3\pi\approx9.42$."),("List the possible integers",r"The integers strictly between $-9.42$ and $9.42$ are \[-9,-8,\ldots,0,\ldots,8,9.\]"),("Count symmetrically",r"There are $9$ negative integers, $9$ positive integers, and $0$."),("Add",r"The total is \[9+1+9=19.\]"),("Conclude",r"The answer is $\boxed{19}$."),],
2:[("Remember what square root of a square means",r"For any real number $u$, \[\sqrt{u^2}=|u|.\] This matters because $3-2\sqrt3$ is negative."),("Evaluate the first absolute value",r"Since $2\sqrt3>3$, \[\sqrt{(3-2\sqrt3)^2}=|3-2\sqrt3|=2\sqrt3-3.\]"),("Evaluate the second absolute value",r"The number $3+2\sqrt3$ is positive, so \[\sqrt{(3+2\sqrt3)^2}=3+2\sqrt3.\]"),("Add",r"Therefore the expression equals \[(2\sqrt3-3)+(3+2\sqrt3)=4\sqrt3.\]"),("Conclude",r"The answer is $\boxed{4\sqrt3}$."),],
3:[("Define the class sizes",r"Let $j$ be the number of juniors and $s$ the number of seniors. We know \[j+s=28.\]"),("Translate the debate-team condition",r"The number of juniors on the team is $25\%$ of $j$, or $\frac14j$. The number of seniors on the team is $10\%$ of $s$, or $\frac1{10}s$."),("Set them equal",r"The debate team has equal numbers from the two classes, so \[\frac14j=\frac1{10}s.\] This gives \[5j=2s.\]"),("Solve with the total",r"From $5j=2s$, we get $s=\frac52j$. Then \[j+\frac52j=28,\] so \[\frac72j=28,\] and $j=8$."),("Conclude",r"There are $\boxed{8}$ juniors."),],
4:[("Use the blue-shirt information first",r"There are $23$ blue-blue pairs, using \[2\cdot23=46\] blue-shirt students."),("Find mixed pairs",r"There are $57$ blue-shirt students total, so \[57-46=11\] blue-shirt students remain. Each must be paired with a yellow-shirt student, giving $11$ mixed pairs."),("Use the total number of pairs",r"There are $66$ pairs total. These consist of $23$ blue-blue pairs, $11$ mixed pairs, and the yellow-yellow pairs."),("Compute yellow-yellow pairs",r"The number of yellow-yellow pairs is \[66-23-11=32.\]"),("Conclude",r"The answer is $\boxed{32}$."),],
5:[("List factor pairs carefully",r"The distinct single-digit positive factors of $24$ could be paired as $(3,8)$ or $(4,6)$, while $30$ could be $(5,6)$ or $(3,10)$, but $10$ is not single digit."),("Respect distinct ages",r"The pair for $30$ must be $(5,6)$. Then the pair for $24$ cannot use $6$, so it must be $(3,8)$."),("Collect the ages",r"The four ages are \[3,5,6,8.\] They are distinct and satisfy the two product conditions."),("Add",r"The sum is \[3+5+6+8=22.\]"),("Conclude",r"The answer is $\boxed{22}$."),],
6:[("Use the ratio as sample class sizes",r"The ratio of morning to afternoon students is $3:4$, so we can think of $3$ equal groups in the morning and $4$ equal groups in the afternoon."),("Compute a weighted average",r"The combined mean is not the simple average of $84$ and $70$ because the classes have different sizes. Use weights $3$ and $4$."),("Calculate",r"The overall mean is \[\frac{3\cdot84+4\cdot70}{3+4}=\frac{252+280}{7}=\frac{532}{7}=76.\]"),("Check reasonableness",r"The answer should be closer to $70$ than to $84$ because the afternoon class is larger. The value $76$ fits that expectation."),("Conclude",r"The answer is $\boxed{76}$."),],
7:[("Understand nested circles on one side",r"If two tangent circles are on the same side of the line and tangent at the same point, the smaller circle lies inside the larger one."),("Choose the largest useful areas",r"To maximize the area inside exactly one circle, place the radius $7$ and radius $5$ circles on opposite sides of the line. Then their areas do not overlap except at the tangent point."),("Handle the smaller circles",r"The radius $3$ circle must remove area from exactly-one coverage if it is placed inside one of the larger circles. The radius $1$ circle should be nested inside the radius $3$ circle so it does not create additional loss."),("Compute the maximum exactly-one area",r"The best area is therefore \[\pi\cdot7^2+\pi\cdot5^2-\pi\cdot3^2=49\pi+25\pi-9\pi=65\pi.\]"),("Conclude",r"The answer is $\boxed{65\pi}$."),],
8:[("Put coordinates on the grid",r"Place $1$ at coordinate $(0,0)$ in the center. The $15\times15$ grid then has coordinates from $-7$ to $7$ in each direction."),("Follow the spiral pattern",r"The numbers go right, down, left, up, and repeat with longer side lengths. This lets us compute positions ring by ring without drawing the entire grid."),("Identify the target row",r"The second row from the top has $y=6$. Following the spiral around the outer rings, the entries in that row run from $157$ through $170$, with one outer-corner continuation value $210$ at the far left."),("Find least and greatest",r"Thus the least number in that row is $157$, and the greatest is $210$."),("Add",r"The required sum is \[157+210=367.\]"),("Conclude",r"The answer is $\boxed{367}$."),],
9:[("Undo the final reflection",r"Reflection across $y=-x$ sends $(u,v)$ to $(-v,-u)$. Since the final image is $(-6,3)$, the point just before reflection was $(-3,6)$."),("Write the rotation formula",r"Rotating $P(a,b)$ counterclockwise by $90^\circ$ around $(1,5)$ means rotate the vector $(a-1,b-5)$ to $(5-b,a-1)$."),("Add back the center",r"After rotation, the point is \[(1+5-b,\;5+a-1)=(6-b,\;a+4).\]"),("Set equal to the pre-reflection point",r"So \[(6-b,\;a+4)=(-3,6).\] This gives $b=9$ and $a=2$."),("Conclude",r"Therefore \[b-a=9-2=7.\] The answer is $\boxed{7}$."),],
10:[("Use conservation of volume",r"The water volume does not change when poured from the cone into the cylinder."),("Find the cone volume",r"The cone volume is \[V=\frac13\pi r^2h=\frac13\pi(12)^2(18)=864\pi.\]"),("Write the cylinder volume",r"The cylinder has radius $24$, so if the water height is $H$, its volume is \[\pi(24)^2H=576\pi H.\]"),("Set volumes equal",r"Thus \[576\pi H=864\pi,\] so \[H=\frac{864}{576}=1.5.\]"),("Conclude",r"The answer is $\boxed{1.5}$."),],
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
    year_label = row["year"]
    if year_label == "2021 Spring":
        year_part = "2021"
    elif year_label == "2021 Fall":
        year_part = "2021_Fall"
    else:
        year_part = year_label.replace(" ", "_")
    return f"https://artofproblemsolving.com/wiki/index.php/{year_part}_{row['contest'].replace(' ', '_')}{row['form']}_Problems/Problem_{row['problem_no']}"


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
        if r["year"] == "2021 Spring" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2021 AMC 10B Answer Key\n\n"
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












































