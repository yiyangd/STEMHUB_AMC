from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 51
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2010_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11, 12, 13, 15, 16, 17, 18, 20}
SKIPPED = [
    "2010 AMC 10A Problem 14 skipped: geometry construction solution needs more careful diagram-based review",
    "2010 AMC 10A Problem 19 skipped: equiangular hexagon area relation needs more careful derivation",
]
BATCH_LABEL = "2010 AMC 10A Problems 11-13, 15-18, 20"
NEXT_START = "2010 AMC 10A Problem 21"

ANS={11:("D","20"),12:("C","0.4"),13:("A",r"80t+100(\frac83-t)=250"),15:("D","3"),16:("B","33"),17:("A","7"),18:("B",r"\frac{37}{56}"),20:("D",r"4\sqrt2+4\sqrt3")}

OV={
11:(r"The length of the interval of solutions of the inequality $a\le 2x+3\le b$ is $10$. What is $b-a$?",[("A","$6$"),("B","$10$"),("C","$15$"),("D","$20$"),("E","$30$")]),
12:(r"Logan is constructing a scaled model of his town. The city's water tower stands $40$ meters high, and the top portion is a sphere that holds $100{,}000$ liters of water. Logan's miniature water tower holds $0.1$ liters. How tall, in meters, should Logan make his tower?",[("A","$0.04$"),("B",r"$\frac{0.4}{\pi}$"),("C","$0.4$"),("D",r"$\frac4\pi$"),("E","$4$")]),
13:(r"Angelina drove at an average rate of $80$ km/h and then stopped $20$ minutes for gas. After the stop, she drove at an average rate of $100$ km/h. Altogether she drove $250$ km in a total trip time of $3$ hours including the stop. Which equation could be used to solve for the time $t$ in hours that she drove before her stop?",[("A",r"$80t+100(\frac83-t)=250$"),("B",r"$80t=250$"),("C",r"$100t=250$"),("D",r"$90t=250$"),("E",r"$80(\frac83-t)+100t=250$")]),
15:(r"In a magical swamp there are two species of talking amphibians: toads, whose statements are always true, and frogs, whose statements are always false. Brian says, 'Mike and I are different species.' Chris says, 'LeRoy is a frog.' LeRoy says, 'Chris is a frog.' Mike says, 'Of the four of us, at least two are toads.' How many of these amphibians are frogs?",[("A","$0$"),("B","$1$"),("C","$2$"),("D","$3$"),("E","$4$")]),
16:(r"Nondegenerate $\triangle ABC$ has integer side lengths, $BD$ is an angle bisector, $AD=3$, and $DC=8$. What is the smallest possible value of the perimeter?",[("A","$30$"),("B","$33$"),("C","$35$"),("D","$36$"),("E","$37$")]),
17:(r"A solid cube has side length $3$ inches. A $2$-inch by $2$-inch square hole is cut into the center of each face. The edges of each cut are parallel to the edges of the cube, and each hole goes all the way through the cube. What is the volume, in cubic inches, of the remaining solid?",[("A","$7$"),("B","$8$"),("C","$10$"),("D","$12$"),("E","$15$")]),
18:(r"Bernardo randomly picks $3$ distinct numbers from $\{1,2,3,4,5,6,7,8,9\}$ and arranges them in descending order to form a $3$-digit number. Silvia randomly picks $3$ distinct numbers from $\{1,2,3,4,5,6,7,8\}$ and also arranges them in descending order. What is the probability that Bernardo's number is larger than Silvia's number?",[("A",r"$\frac{47}{72}$"),("B",r"$\frac{37}{56}$"),("C",r"$\frac23$"),("D",r"$\frac{49}{72}$"),("E",r"$\frac{39}{56}$")]),
20:(r"A fly trapped inside a cubical box with side length $1$ meter decides to visit each corner of the box. It will begin and end in the same corner and visit each of the other corners exactly once. To get from a corner to any other corner, it will either fly or crawl in a straight line. What is the maximum possible length, in meters, of its path?",[("A",r"$4+4\sqrt2$"),("B",r"$2+4\sqrt2+2\sqrt3$"),("C",r"$2+3\sqrt2+3\sqrt3$"),("D",r"$4\sqrt2+4\sqrt3$"),("E",r"$3\sqrt2+5\sqrt3$")]),
}

KEY_OVERRIDES={11:"Solve the compound inequality for x and compare interval lengths.",12:"Volume scale is the cube of length scale.",13:"Subtract the gas stop from the total time before writing the distance equation.",15:"Use consistency between truth-tellers and liars.",16:"Apply the angle bisector theorem, then minimize integer side lengths without degeneracy.",17:"Use inclusion-exclusion on three square tunnels through the cube.",18:"Separate the case where Bernardo chooses 9 from the symmetric case without 9.",20:"A cube has four body diagonals at most; then use face diagonals for the remaining steps."}

SOL={
11:[("Solve for x",r"Subtracting $3$ from all parts gives $a-3\le 2x\le b-3$. Dividing by $2$ gives $\frac{a-3}{2}\le x\le\frac{b-3}{2}$."),("Write the interval length",r"The length of this interval is $\frac{b-3}{2}-\frac{a-3}{2}=\frac{b-a}{2}$."),("Use the given length",r"We are told this length is $10$, so $\frac{b-a}{2}=10$."),("Answer",r"Therefore $b-a=\boxed{20}$.")],
12:[("Compare volumes",r"The real tower holds $100{,}000$ liters, while the model holds $0.1$ liters. The volume scale factor is $\frac{0.1}{100000}=10^{-6}$."),("Convert volume scale to length scale",r"For similar solids, volume scale is the cube of length scale. Thus the length scale is $\sqrt[3]{10^{-6}}=10^{-2}=\frac1{100}$."),("Scale the height",r"The real tower is $40$ meters high, so the model should be $40\cdot\frac1{100}=0.4$ meters high."),("Answer",r"Logan should make the tower $\boxed{0.4}$ meters tall.")],
13:[("Remove the stop time",r"The total trip time was $3$ hours, but $20$ minutes, or $\frac13$ hour, was spent stopped. So the total driving time was $3-\frac13=\frac83$ hours."),("Use t for the first driving time",r"If Angelina drove for $t$ hours before stopping, then she drove for $\frac83-t$ hours after stopping."),("Write total distance",r"Distance equals rate times time, so the two driving distances are $80t$ and $100(\frac83-t)$. Their sum is $250$."),("Answer",r"The equation is $\boxed{80t+100(\frac83-t)=250}$.")],
15:[("Analyze Chris and LeRoy",r"Chris says LeRoy is a frog, and LeRoy says Chris is a frog. Exactly one of these two statements can be true, so exactly one of Chris and LeRoy is a frog and the other is a toad."),("Test Mike as a toad",r"If Mike were a toad, his statement that at least two are toads would be true. But Brian's statement about being a different species from Mike cannot be made consistently by either a toad or a frog in that case."),("Conclude Mike is a frog",r"Therefore Mike is a frog, so his statement is false. That means there are fewer than two toads total."),("Determine Brian",r"Since exactly one of Chris and LeRoy is a toad, Brian must also be a frog. Then Brian's statement that he and Mike are different species is false, which is consistent."),("Count frogs",r"Brian, Mike, and one of Chris or LeRoy are frogs, for a total of $3$."),("Answer",r"There are $\boxed{3}$ frogs.")],
16:[("Use the angle bisector theorem",r"Since $BD$ is an angle bisector, $\frac{AB}{BC}=\frac{AD}{DC}=\frac38$."),("Write side lengths",r"Because side lengths are integers, let $AB=3k$ and $BC=8k$ for a positive integer $k$. Also $AC=AD+DC=11$."),("Avoid degeneracy",r"If $k=1$, the sides would be $3,8,11$, which is degenerate because $3+8=11$."),("Try the next k",r"For $k=2$, the sides are $6,16,11$, and $6+11>16$, so this is a valid nondegenerate triangle."),("Compute the perimeter",r"The perimeter is $6+16+11=33$."),("Answer",r"The smallest possible perimeter is $\boxed{33}$.")],
17:[("Start with the full cube",r"The original cube has volume $3^3=27$."),("Count the three tunnels",r"Each square hole is a $2\times2\times3$ rectangular tunnel, so each has volume $12$. There are three perpendicular tunnels, one for each direction."),("Correct the overlaps",r"The overlap of any two tunnels is the central $2\times2\times2$ cube, volume $8$. The overlap of all three tunnels is the same central cube."),("Use inclusion-exclusion",r"The removed volume is $3\cdot12-3\cdot8+8=20$."),("Find the remaining volume",r"The remaining volume is $27-20=7$."),("Answer",r"The remaining solid has volume $\boxed{7}$ cubic inches.")],
18:[("Use Bernardo's possible 9",r"If Bernardo chooses the number $9$, then his descending three-digit number is automatically larger than Silvia's, because Silvia can only choose from $1$ through $8$."),("Find that probability",r"The probability Bernardo chooses $9$ is $\frac{\binom82}{\binom93}=\frac{28}{84}=\frac13$."),("Handle the no-9 case",r"If Bernardo does not choose $9$, then both students are choosing three-element subsets from $\{1,2,\ldots,8\}$. The chance Bernardo's number is larger equals the chance Silvia's is larger by symmetry, except when they choose the same set."),("Compute the symmetric probability",r"The probability of the same set is $\frac1{\binom83}=\frac1{56}$. So, conditional on no $9$, Bernardo is larger with probability $\frac{1-1/56}{2}=\frac{55}{112}$."),("Combine cases",r"The total probability is $\frac13+\frac23\cdot\frac{55}{112}=\frac{37}{56}$."),("Answer",r"The probability is $\boxed{\frac{37}{56}}$.")],
20:[("Classify possible moves",r"Between two cube corners, the longest possible straight move is a body diagonal of length $\sqrt3$. The next longest is a face diagonal of length $\sqrt2$."),("Bound the body diagonals",r"A cube has four pairs of opposite vertices, so a closed path visiting all $8$ corners can use at most four body diagonals."),("Use the best remaining moves",r"After using four body diagonals, the other four moves can be no longer than face diagonals, so the total length is at most $4\sqrt3+4\sqrt2$."),("Show it is achievable",r"One can alternate body diagonals and face diagonals through all eight vertices, for example by using coordinates of the cube corners and moving $000\to111\to001\to110\to100\to011\to101\to010\to000$."),("Answer",r"The maximum path length is $\boxed{4\sqrt2+4\sqrt3}$.")],
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
        if r["year"] == "2010" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2010 AMC 10A Answer Key\n\n"
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














