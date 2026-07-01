from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 35
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2007_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 5, 6, 7, 8, 9, 10}
SKIPPED = [
    "2007 AMC 10B Problem 4 skipped: statement references a circle diagram.",
]
BATCH_LABEL = "2007 AMC 10B Problems 1-3, 5-10"
NEXT_START = "2007 AMC 10B Problem 11"

ANS = {
    1: ("E", "876"),
    2: ("E", "16"),
    3: ("B", "24"),
    5: ("D", "All Crups are Arogs and are Brafs."),
    6: ("D", "16"),
    7: ("E", "150"),
    8: ("D", "20"),
    9: ("D", "s"),
    10: ("A", "two parallel lines"),
}


OV = {
    1: (r"Isabella's house has $3$ bedrooms. Each bedroom is $12$ feet long, $10$ feet wide, and $8$ feet high. Isabella must paint the walls of all the bedrooms. Doorways and windows, which will not be painted, occupy $60$ square feet in each bedroom. How many square feet of walls must be painted?", [("A", "$678$"), ("B", "$768$"), ("C", "$786$"), ("D", "$867$"), ("E", "$876$")]),
    2: (r"Define the operation $\star$ by $a\star b=(a+b)b$. What is $(3\star5)-(5\star3)$?", [("A", "$-16$"), ("B", "$-8$"), ("C", "$0$"), ("D", "$8$"), ("E", "$16$")]),
    3: (r"A college student drove his compact car $120$ miles home for the weekend and averaged $30$ miles per gallon. On the return trip the student drove his parents' SUV and averaged only $20$ miles per gallon. What was the average gas mileage, in miles per gallon, for the round trip?", [("A", "$22$"), ("B", "$24$"), ("C", "$25$"), ("D", "$26$"), ("E", "$28$")]),
    5: (r"In a certain land, all Arogs are Brafs, all Crups are Brafs, all Dramps are Arogs, and all Crups are Dramps. Which of the following statements is implied by these facts?", [("A", "All Dramps are Brafs and are Crups."), ("B", "All Brafs are Crups and are Dramps."), ("C", "All Arogs are Crups and are Dramps."), ("D", "All Crups are Arogs and are Brafs."), ("E", "All Arogs are Dramps and some Arogs may not be Crups.")]),
    6: (r"The 2007 AMC 10 will be scored by awarding $6$ points for each correct response, $0$ points for each incorrect response, and $1.5$ points for each problem left unanswered. After looking over the $25$ problems, Sarah has decided to attempt the first $22$ and leave only the last $3$ unanswered. How many of the first $22$ problems must she solve correctly in order to score at least $100$ points?", [("A", "$13$"), ("B", "$14$"), ("C", "$15$"), ("D", "$16$"), ("E", "$17$")]),
    7: (r"All sides of the convex pentagon $ABCDE$ are of equal length, and $\angle A=\angle B=90^\circ$. What is the degree measure of $\angle E$?", [("A", "$90$"), ("B", "$108$"), ("C", "$120$"), ("D", "$144$"), ("E", "$150$")]),
    8: (r"On the trip home from the meeting where this AMC 10 was constructed, the Contest Chair noted that his airport parking receipt had digits of the form $bbcac$, where $0\le a<b<c\le9$, and $b$ was the average of $a$ and $c$. How many different five-digit numbers satisfy all these properties?", [("A", "$12$"), ("B", "$16$"), ("C", "$18$"), ("D", "$20$"), ("E", "$24$")]),
    9: (r"A cryptographic code is designed as follows. The first time a letter appears in a given message it is replaced by the letter that is $1$ place to its right in the alphabet. The second time this same letter appears, it is replaced by the letter that is $1+2$ places to the right, the third time by $1+2+3$ places to the right, and so on. For example, with this code the word \"banana\" becomes \"cbodqg\". What letter will replace the last letter $s$ in the message \"Lee's sis is a Mississippi miss, Chriss!\"?", [("A", "g"), ("B", "h"), ("C", "o"), ("D", "s"), ("E", "t")]),
    10: (r"Two points $B$ and $C$ are in a plane. Let $S$ be the set of all points $A$ in the plane for which $\triangle ABC$ has area $1$. Which of the following describes $S$?", [("A", "two parallel lines"), ("B", "a parabola"), ("C", "a circle"), ("D", "a line segment"), ("E", "two points")]),
}


KEY_OVERRIDES = {
    1: "Compute wall area from room perimeter times height, then subtract unpainted area.",
    2: "Evaluate the custom operation in each order; the operation is not symmetric.",
    3: "Average miles per gallon means total miles divided by total gallons, not the average of the two rates.",
    5: "Use subset logic to follow the implications from Crups to Dramps to Arogs to Brafs.",
    6: "Set up a score inequality including unanswered points.",
    7: "Use an equal-side construction to determine the remaining angle in the pentagon.",
    8: "Count arithmetic triples of digits a,b,c with b as the midpoint.",
    9: "Count occurrences of the letter s and reduce the triangular-number shift modulo 26.",
    10: "For a fixed base, constant triangle area means constant perpendicular distance from the base line.",
}


SOL = {
    1: [("Find the wall area of one bedroom", r"A rectangular room has two walls measuring $12\times8$ and two walls measuring $10\times8$. So the wall area before subtracting openings is $2(12\cdot8)+2(10\cdot8)=192+160=352$ square feet."), ("Subtract unpainted openings", r"Doorways and windows occupy $60$ square feet in each bedroom, so one bedroom needs $352-60=292$ square feet painted."), ("Multiply by the number of bedrooms", r"There are $3$ identical bedrooms, so the total painted wall area is $3\cdot292=876$ square feet."), ("Check the setup", r"We do not paint floors or ceilings, only walls, so using perimeter times height was the right model."), ("Answer", r"The answer is $\boxed{876}$." )],
    2: [("Apply the operation carefully", r"The rule is $a\star b=(a+b)b$. The value depends on which number is second, because the sum is multiplied by $b$."), ("Compute the first term", r"$3\star5=(3+5)5=8\cdot5=40$."), ("Compute the second term", r"$5\star3=(5+3)3=8\cdot3=24$."), ("Subtract", r"Thus $(3\star5)-(5\star3)=40-24=16$."), ("Answer", r"The answer is $\boxed{16}$." )],
    3: [("Avoid averaging the rates", r"Average gas mileage is total distance divided by total gallons. Since the two cars use different amounts of gas, we should not average $30$ and $20$ directly."), ("Compute gallons used going home", r"The compact car travels $120$ miles at $30$ miles per gallon, so it uses $120/30=4$ gallons."), ("Compute gallons used returning", r"The SUV travels $120$ miles at $20$ miles per gallon, so it uses $120/20=6$ gallons."), ("Compute the overall mileage", r"The round trip is $240$ miles and uses $4+6=10$ gallons. Therefore the average mileage is $240/10=24$ miles per gallon."), ("Answer", r"The answer is $\boxed{24}$." )],
    5: [("Translate each statement", r"The facts say $\text{Dramps}\subseteq\text{Arogs}$ and $\text{Arogs}\subseteq\text{Brafs}$. They also say $\text{Crups}\subseteq\text{Dramps}$."), ("Follow the chain from Crups", r"If something is a Crup, then it is a Dramp. Since every Dramp is an Arog, that Crup is also an Arog."), ("Continue to Brafs", r"Since every Arog is a Braf, every Crup is also a Braf."), ("Choose the implied statement", r"Therefore all Crups are Arogs and are Brafs. The other choices reverse implications or add information not guaranteed."), ("Answer", r"The answer is $\boxed{\text{D}}$." )],
    6: [("Account for unanswered problems", r"Sarah leaves $3$ problems unanswered, and each is worth $1.5$ points. That contributes $3\cdot1.5=4.5$ points."), ("Let x be correct answers", r"Among the first $22$ problems, suppose she solves $x$ correctly. Incorrect responses get $0$, so her score is $6x+4.5$."), ("Set the target inequality", r"She needs at least $100$ points, so $6x+4.5\ge100$."), ("Solve", r"This gives $6x\ge95.5$, so $x\ge15.916\ldots$. Since $x$ must be an integer, she needs at least $16$ correct answers."), ("Answer", r"The answer is $\boxed{16}$." )],
    7: [("Build a helpful picture mentally", r"Let the common side length be $1$. Since $\angle A=90^\circ$ and $\angle B=90^\circ$, we can place consecutive equal sides so that $E$ and $C$ lie one unit above $A$ and $B$, respectively."), ("Locate the remaining vertex", r"Then $CE$ also has length $1$. Since $CD=DE=1$, triangle $CDE$ is equilateral with side length $1$, sitting on segment $CE$."), ("Find the angle at E", r"At $E$, side $EA$ points straight downward, while side $ED$ makes a $60^\circ$ angle above the horizontal segment $EC$. The angle between downward vertical and $ED$ is $150^\circ$."), ("Check convexity", r"The convex pentagon uses the outside angle at $E$, so $150^\circ$ is the interior angle, not $30^\circ$."), ("Answer", r"The answer is $\boxed{150^\circ}$." )],
    8: [("Translate the average condition", r"The condition that $b$ is the average of $a$ and $c$ means $a+c=2b$. Thus $a,b,c$ form an arithmetic progression of digits."), ("Use a step size", r"Let $d=b-a=c-b$. Then $d$ is a positive integer, $a=b-d\ge0$, and $c=b+d\le9$."), ("Count choices for each b", r"For a fixed $b$, the number of possible $d$ values is $\min(b,9-b)$. For $b=1,2,3,4,5,6,7,8$, these counts are $1,2,3,4,4,3,2,1$."), ("Add", r"The total number is $1+2+3+4+4+3+2+1=20$."), ("Answer", r"The answer is $\boxed{20}$." )],
    9: [("Focus only on the letter s", r"The replacement for a letter depends on how many times that same letter has appeared before. So for the last $s$, we only need to count how many $s$'s have appeared in the message."), ("Count occurrences", r"In \"Lee's sis is a Mississippi miss, Chriss!\", the letter $s$ appears $12$ times in total, counting the final $s$ in \"Chriss\"."), ("Find the shift", r"The $12$th occurrence is shifted by $1+2+\cdots+12=\frac{12\cdot13}{2}=78$ places."), ("Reduce modulo the alphabet", r"Since the alphabet has $26$ letters and $78=3\cdot26$, shifting $78$ places returns to the same letter."), ("Answer", r"The last $s$ is replaced by $\boxed{s}$." )],
    10: [("Use the area formula", r"For triangle $ABC$, take $BC$ as the base. The area is $\frac12\cdot BC\cdot h$, where $h$ is the perpendicular distance from $A$ to the line through $B$ and $C$."), ("Keep the area fixed", r"Since $B$ and $C$ are fixed and the area must be $1$, the height $h$ must be a fixed positive distance."), ("Describe all possible A", r"All points at a fixed distance from a line form two lines parallel to the original line, one on each side."), ("Exclude the base line", r"The distance cannot be $0$, because the area is $1$, so the set is not the line $BC$ itself."), ("Answer", r"The set $S$ is $\boxed{\text{two parallel lines}}$." )],
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
        if r["year"] == "2007" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Review notes: Skipped Problem 4 because it references a diagram.\n",
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
        + "- Answer verification source: AoPS 2007 AMC 10B Answer Key\n\n"
        + "## Latest Batch Pages\n\n"
        + latest
        + ("\n\n## Skipped in latest batch\n\n" + "\n".join(f"- {s}" for s in SKIPPED) + "\n" if SKIPPED else ""),
        encoding="utf-8",
    )

    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 批量生成任务。\n\n"
        + f"当前状态：Batch {BATCH_NUMBER} 已生成/更新并通过本地脚本验证；最新范围为 {BATCH_LABEL}。\n"
        + "本批跳过 2007 AMC 10B Problem 4：题面引用图形。\n"
        + f"下一批从 {NEXT_START} 开始。\n\n"
        + "继续策略：每批生成 5-10 道可靠题；遇到图形缺失或 OCR 不可靠就记录并跳过；验证 MathJax、详情链接和 teaching steps 后 commit/push。\n",
        encoding="utf-8",
    )

    print(json.dumps({"batch": BATCH_NUMBER, "new": new_count, "updated": updated_count, "skipped": len(SKIPPED), "start": start, "end": end, "next": NEXT_START}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
