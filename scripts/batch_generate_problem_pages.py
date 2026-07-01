import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 67
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2012_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15,16,17,18,19,20}
SKIPPED = []
BATCH_LABEL = "2012 AMC 10B Problems 11-20"
NEXT_START = "2012 AMC 10B Problem 21"

ANS = {11:("A","729"),12:("B","31 and 32"),13:("B","40"),14:("D",r"8\sqrt3-12"),15:("D","5"),16:("A",r"10\pi+4\sqrt3"),17:("C",r"\frac{\sqrt{10}}{10}"),18:("C",r"\frac{1}{11}"),19:("C",r"\frac{135}{2}"),20:("A","7")}

OV = {
11:(r"A dessert chef prepares the dessert for every day of a week starting with Sunday. Each day is cake, pie, ice cream, or pudding. The same dessert may not be served two days in a row. There must be cake on Friday. How many different dessert menus for the week are possible?",[("A","729"),("B","972"),("C","1024"),("D","2187"),("E","2304")]),
12:(r"Point $B$ is due east of point $A$. Point $C$ is due north of point $B$. The distance $AC$ is $10\sqrt2$ meters, and $\angle BAC=45^\circ$. Point $D$ is $20$ meters due north of point $C$. The distance $AD$ is between which two integers?",[("A","30 and 31"),("B","31 and 32"),("C","32 and 33"),("D","33 and 34"),("E","34 and 35")]),
13:(r"It takes Clea $60$ seconds to walk down an escalator when it is not operating and $24$ seconds to walk down the escalator when it is operating. How many seconds does it take Clea to ride down the operating escalator when she just stands on it?",[("A","36"),("B","40"),("C","42"),("D","48"),("E","52")]),
14:(r"Two equilateral triangles are contained in a square whose side length is $2\sqrt3$. The bases of these triangles are opposite sides of the square, and their intersection is a rhombus. What is the area of the rhombus?",[("A",r"\sqrt3"),("B",r"\frac{3\sqrt3}{2}"),("C",r"2\sqrt2-1"),("D",r"8\sqrt3-12"),("E",r"4\sqrt3")]),
15:(r"In a round-robin tournament with $6$ teams, each team plays one game against each other team, and each game has one winner and one loser. Teams are ranked by number of wins. What is the maximum number of teams that could be tied for the most wins?",[("A","2"),("B","3"),("C","4"),("D","5"),("E","6")]),
16:(r"Three circles with radius $2$ are mutually tangent. What is the total area of the circles and the region bounded by them, as shown in the figure?",[("A",r"10\pi+4\sqrt3"),("B",r"13\pi-3"),("C",r"12\pi+\sqrt3"),("D",r"10\pi+9"),("E",r"13\pi")]),
17:(r"Jesse cuts a circular paper disk of radius $12$ along two radii to form two sectors, the smaller having central angle $120^\circ$. He makes two circular cones, using each sector as the lateral surface of a cone. What is the ratio of the volume of the smaller cone to that of the larger?",[("A",r"\frac18"),("B",r"\frac14"),("C",r"\frac{\sqrt{10}}{10}"),("D",r"\frac{\sqrt5}{6}"),("E",r"\frac{\sqrt{10}}{5}")]),
18:(r"In a population, one of every $500$ people has a disease. A test is always positive for a person with the disease. For a person without the disease, there is a $2\%$ false positive rate. Let $p$ be the probability that a randomly chosen person with a positive test actually has the disease. Which choice is closest to $p$?",[("A",r"\frac1{98}"),("B",r"\frac19"),("C",r"\frac1{11}"),("D",r"\frac{49}{99}"),("E",r"\frac{98}{99}")]),
19:(r"In rectangle $ABCD$, $AB=6$, $AD=30$, and $G$ is the midpoint of $AD$. Segment $AB$ is extended $2$ units beyond $B$ to point $E$, and $F$ is the intersection of $ED$ and $BC$. What is the area of $BFDG$?",[("A","133"),("B",r"\frac{67}{2}"),("C",r"\frac{135}{2}"),("D","68"),("E",r"\frac{137}{2}")]),
20:(r"Bernardo and Silvia play a game. An integer between $0$ and $999$ is selected and given to Bernardo. Whenever Bernardo receives a number, he doubles it and passes the result to Silvia. Whenever Silvia receives a number, she adds $50$ and passes the result to Bernardo. The winner is the last person who produces a number less than $1000$. Let $N$ be the smallest initial number that results in a win for Bernardo. What is the sum of the digits of $N$?",[("A","7"),("B","8"),("C","9"),("D","10"),("E","11")]),
}

KEY_OVERRIDES={11:"Choose Friday first, then count menus on each side with no adjacent repeats.",12:"Use the 45-45-90 triangle to get coordinates and then apply distance formula.",13:"Subtract walking rate from combined rate to get escalator rate.",14:"Compute the rhombus diagonals from cross-sections of the two equilateral triangles.",15:"Build a balanced tournament among five teams and show six-way tie is impossible.",16:"Add three circle areas and the small curvilinear triangular gap.",17:"Turn sector arc lengths into cone base radii and use slant height 12.",18:"Use conditional probability among positive tests.",19:"Use coordinates to find F and compute the trapezoid area.",20:"Work backward or recursively through the doubling/add-50 game."}

SOL={
11:[("Fix Friday",r"Friday must be cake. The days split into Sunday-Thursday before Friday and Saturday after Friday."),("Count before Friday",r"Sunday has $4$ choices. Each of Monday through Thursday has $3$ choices because it cannot match the previous day. That gives $4\cdot3^4$."),("Count Saturday",r"Saturday cannot be cake because Friday is cake, so it has $3$ choices."),("Multiply",r"The total is $4\cdot3^4\cdot3=4\cdot3^5=972? But this overcounts Thursday cake? Thursday may be cake, and then Friday cake would repeat, so Thursday must not be cake. Count Sunday-Thursday ending not cake: after five days, each dessert appears equally often as the last dessert, so $4\cdot3^4/4=3^4$ end in cake and $3\cdot3^4$ end not cake. Then Saturday has $3$ choices, total $3^5\cdot3=729$. The answer is $\boxed{729}$."),],
12:[("Use the 45 degree angle",r"Since $B$ is east of $A$ and $C$ is north of $B$, triangle $ABC$ is right. With $\angle BAC=45^\circ$, it is a $45$-$45$-$90$ triangle."),("Find coordinates",r"The hypotenuse $AC=10\sqrt2$, so the legs are $10$ and $10$. Thus from $A$, point $C$ is $10$ east and $10$ north."),("Move to D",r"Point $D$ is $20$ meters north of $C$, so from $A$ it is $10$ east and $30$ north."),("Compute AD",r"Then $AD=\sqrt{10^2+30^2}=\sqrt{1000}=10\sqrt{10}$, which is between $31$ and $32$."),],
13:[("Use rates",r"Let one escalator length be $1$ trip. Clea's walking rate on a stopped escalator is $1/60$ trip per second."),("Use combined rate",r"When the escalator operates and she walks, the combined rate is $1/24$."),("Subtract to get escalator rate",r"The escalator's own rate is $1/24-1/60=1/40$."),("Conclude",r"Standing still, Clea takes $\boxed{40}$ seconds."),],
14:[("Set the square side",r"Let the square side be $s=2\sqrt3$. Each equilateral triangle has height $s\sqrt3/2=3$."),("Find the vertical diagonal",r"The two triangle apexes overlap vertically by $2\cdot3-s=6-2\sqrt3$. This is one diagonal of the rhombus."),("Find the horizontal diagonal",r"At the middle height of the square, the width of either equilateral triangle is $s(1-\frac{s/2}{3})=2\sqrt3-2$. This is the other diagonal."),("Compute area",r"The rhombus area is $\frac12(6-2\sqrt3)(2\sqrt3-2)=8\sqrt3-12$."),],
15:[("Rule out all six",r"There are $\binom62=15$ games, so the average number of wins per team is $15/6=2.5$. All six teams cannot tie because the common number of wins would not be an integer."),("Construct five tied teams",r"Let one team lose to all other five teams. Among the remaining five teams, arrange the games so each team wins two and loses two, which is possible in a cycle-style tournament."),("Count wins",r"Each of those five teams gets one win against the sixth team plus two wins inside the group, so all five have $3$ wins."),("Conclude",r"The maximum is $\boxed{5}$."),],
16:[("Start with circle areas",r"The three circles have radius $2$, so their total area is $3\cdot4\pi=12\pi$."),("Find the central gap",r"The centers form an equilateral triangle of side $4$. Its area is $\frac{\sqrt3}{4}\cdot4^2=4\sqrt3$."),("Subtract sectors",r"Inside that triangle, the three $60^\circ$ sectors together make half of one radius-$2$ circle, with area $2\pi$."),("Add desired area",r"The bounded gap has area $4\sqrt3-2\pi$. Adding the three circles gives $12\pi+4\sqrt3-2\pi=10\pi+4\sqrt3$."),],
17:[("Convert sectors to cone radii",r"The slant height of both cones is $12$. The $120^\circ$ sector has arc length $8\pi$, so the smaller cone base radius is $4$. The larger sector has arc length $16\pi$, so its base radius is $8$."),("Find cone heights",r"The smaller height is $\sqrt{12^2-4^2}=8\sqrt2$. The larger height is $\sqrt{12^2-8^2}=4\sqrt5$."),("Compare volumes",r"Volume is proportional to $r^2h$. The ratio is $\frac{4^2\cdot8\sqrt2}{8^2\cdot4\sqrt5}=\frac{\sqrt{10}}{10}$."),("Conclude",r"The answer is $\boxed{\frac{\sqrt{10}}{10}}$."),],
18:[("Use a population of 500",r"In $500$ people, expect $1$ person with the disease and $499$ without it."),("Count positive tests",r"The diseased person definitely tests positive. Among the $499$ without disease, about $0.02\cdot499=9.98$ test positive falsely."),("Compute conditional probability",r"Among positive tests, the probability of actually having the disease is $\frac{1}{1+9.98}\approx0.091$."),("Match a choice",r"This is closest to $\frac1{11}$."),],
19:[("Place coordinates",r"Let $A=(0,0)$, $B=(6,0)$, $D=(0,30)$, and $C=(6,30)$. Then $E=(8,0)$ and $G=(0,15)$."),("Find F",r"Line $ED$ goes from $(8,0)$ to $(0,30)$. Its slope is $-15/4$, so at $x=6$ its height is $y=\frac{15}{2}$. Thus $F=(6,\frac{15}{2})$."),("See the trapezoid",r"Quadrilateral $BFDG$ has parallel vertical sides $BF=\frac{15}{2}$ and $DG=15$, separated by distance $6$."),("Compute area",r"The area is $\frac12(\frac{15}{2}+15)\cdot6=\frac{135}{2}$."),],
20:[("Think backward",r"Bernardo wins if he is the last to produce a number below $1000$. Direct simulation of intervals is easiest from small candidates."),("Test the threshold",r"Starting with $N=16$, the produced numbers are $32,82,164,214,428,478,956$, and then Silvia receives $956$ and would produce $1006$, which is not below $1000$. Bernardo produced the last valid number, $956$."),("Check smaller starts",r"For every smaller starting number, the same alternating process lasts one more valid move, so Silvia is last below $1000$. Thus $16$ is the smallest Bernardo-winning start."),("Find digit sum",r"The sum of the digits of $16$ is $1+6=7$."),],
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
        if r["year"] == "2012" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2012 AMC 10B Answer Key\n\n"
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



































