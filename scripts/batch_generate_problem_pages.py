from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 43
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2008_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21, 22, 23, 24, 25}
SKIPPED = []
BATCH_LABEL = "2008 AMC 10B Problems 21-25"
NEXT_START = "2009 AMC 10A Problem 1"

ANS = {21: ("C", "480"), 22: ("C", r"\frac{1}{6}"), 23: ("B", "2"), 24: ("C", "85"), 25: ("B", "5")}

OV = {
    21: (r"Ten chairs are evenly spaced around a round table and numbered clockwise from $1$ through $10$. Five married couples are to sit in the chairs with men and women alternating, and no one is to sit either next to or directly across from his or her spouse. How many seating arrangements are possible?", [("A", "$240$"), ("B", "$360$"), ("C", "$480$"), ("D", "$540$"), ("E", "$720$")]),
    22: (r"Three red beads, two white beads, and one blue bead are placed in a line in random order. What is the probability that no two neighboring beads are the same color?", [("A", r"$\frac{1}{12}$"), ("B", r"$\frac{1}{10}$"), ("C", r"$\frac{1}{6}$"), ("D", r"$\frac{1}{3}$"), ("E", r"$\frac{1}{2}$")]),
    23: (r"A rectangular floor measures $a$ by $b$ feet, where $a$ and $b$ are positive integers with $b>a$. An artist paints a rectangle on the floor with the sides of the rectangle parallel to the sides of the floor. The unpainted part of the floor forms a border of width $1$ foot around the painted rectangle and occupies half of the area of the entire floor. How many possibilities are there for the ordered pair $(a,b)$?", [("A", "$1$"), ("B", "$2$"), ("C", "$3$"), ("D", "$4$"), ("E", "$5$")]),
    24: (r"Quadrilateral $ABCD$ has $AB=BC=CD$, $\angle ABC=70^\circ$, and $\angle BCD=170^\circ$. What is the degree measure of $\angle BAD$?", [("A", "$75$"), ("B", "$80$"), ("C", "$85$"), ("D", "$90$"), ("E", "$95$")]),
    25: (r"Michael walks at the rate of $5$ feet per second on a long straight path. Trash pails are located every $200$ feet along the path. A garbage truck travels at $10$ feet per second in the same direction as Michael and stops for $30$ seconds at each pail. As Michael passes a pail, he notices the truck ahead of him just leaving the next pail. How many times will Michael and the truck meet?", [("A", "$4$"), ("B", "$5$"), ("C", "$6$"), ("D", "$7$"), ("E", "$8$")]),
}

KEY_OVERRIDES = {
    21: "Seat genders first, then count the two valid wife placements for each fixed seating of the men.",
    22: "Count all bead arrangements and favorable arrangements with no adjacent equal colors.",
    23: "Translate the border area condition into a factor equation.",
    24: "Use isosceles triangle angles and a sine-law check in the second triangle.",
    25: "Track the truck's 20-second driving intervals and 30-second stops against Michael's constant walking.",
}

SOL = {
    21: [("Separate the gender pattern", r"Because the chairs are numbered, rotations are not being identified. Men and women must alternate, so there are $2$ possible gender patterns around the table."), ("Seat the men", r"Once a gender pattern is chosen, the five men can be placed in the five male-position chairs in $5!$ ways."), ("Study the wife positions for one fixed male seating", r"The five remaining chairs form five female positions around the circle. For each wife, the forbidden positions are the two chairs next to her husband and the chair directly across from him."), ("Count the valid wife placements", r"After labeling the female positions cyclically relative to the husbands, each wife has only two allowed positions. A short cycle check shows that all wives must shift the same way around the table, giving exactly $2$ valid placements of the wives."), ("Multiply", r"The total number of arrangements is $2\cdot5!\cdot2=480$."), ("Answer", r"The answer is $\boxed{480}$.")],
    22: [("Count all arrangements first", r"There are $6$ beads with repetitions: $3$ red, $2$ white, and $1$ blue. The total number of distinct orders is $\frac{6!}{3!2!}=60$."), ("Place the red beads without touching", r"The three red beads must occupy non-adjacent positions. The possible red position sets are $\{1,3,5\}$, $\{1,3,6\}$, $\{1,4,6\}$, and $\{2,4,6\}$."), ("Place the white beads", r"For red positions $\{1,3,5\}$ or $\{2,4,6\}$, the remaining three spots are non-adjacent, so the two white beads can be placed in $3$ ways. For each of the other two red patterns, one adjacent pair remains, so only $2$ white placements work."), ("Count favorable arrangements", r"Thus there are $3+2+2+3=10$ favorable arrangements."), ("Convert to probability", r"The probability is $\frac{10}{60}=\frac16$."), ("Answer", r"The probability is $\boxed{\frac16}$.")],
    23: [("Write the painted dimensions", r"A border of width $1$ foot on all sides means the painted rectangle has dimensions $(a-2)$ by $(b-2)$."), ("Use the area condition", r"The unpainted border occupies half the whole floor, so the painted area is also half the whole floor: $(a-2)(b-2)=\frac12ab$."), ("Turn it into a factor equation", r"Multiplying by $2$ and simplifying gives $2ab-4a-4b+8=ab$, so $ab-4a-4b=-8$. Add $16$ to both sides: $(a-4)(b-4)=8$."), ("Count integer pairs", r"Since $b>a$ and the dimensions must be positive, the positive factor pairs of $8$ give $(a-4,b-4)=(1,8)$ or $(2,4)$. These produce $(a,b)=(5,12)$ and $(6,8)$."), ("Answer", r"There are $\boxed{2}$ ordered pairs." )],
    24: [("Use the first isosceles triangle", r"Since $AB=BC$ and $\angle ABC=70^\circ$, triangle $ABC$ is isosceles. The base angles are $\frac{180^\circ-70^\circ}{2}=55^\circ$, so $\angle BAC=\angle ACB=55^\circ$."), ("Find the angle at C in triangle ACD", r"At $C$, the whole angle $\angle BCD$ is $170^\circ$. Since $\angle ACB=55^\circ$, the angle $\angle ACD$ is $170^\circ-55^\circ=115^\circ$."), ("Relate the side AC", r"Let the common side length $AB=BC=CD$ be $1$. In triangle $ABC$, the base $AC=2\sin35^\circ$."), ("Find angle CAD", r"In triangle $ACD$, the angles other than $115^\circ$ sum to $65^\circ$. Checking $\angle CAD=30^\circ$ gives $\angle ADC=35^\circ$, and the sine law gives $\frac{CD}{\sin30^\circ}=\frac{AC}{\sin35^\circ}=2$, which matches $CD=1$ and $AC=2\sin35^\circ$."), ("Add the angle at A", r"Therefore $\angle BAD=\angle BAC+\angle CAD=55^\circ+30^\circ=85^\circ$."), ("Answer", r"The angle measure is $\boxed{85^\circ}$.")],
    25: [("Set up the timeline", r"Let $t=0$ be the moment Michael passes a pail at position $0$ while the truck leaves the next pail at position $200$. The truck drives $200$ feet in $20$ seconds, then stops for $30$ seconds, so each pail cycle lasts $50$ seconds."), ("Track until the first meeting", r"At $t=170$ the truck reaches position $1000$ and stops until $t=200$. Michael reaches position $1000$ at $t=200$, so they meet once just as the truck leaves."), ("Continue through the close interval", r"After that, Michael and the truck are close enough to meet several times while the truck alternates between stopping and moving. They meet at $t=240$ at position $1200$, at $t=260$ while the truck is moving, at $t=280$ at position $1400$, and at $t=320$ at position $1600$."), ("Explain why there are no more", r"After $t=320$, Michael gets far enough ahead during the truck's stop that the truck can no longer catch him before reaching and stopping at the next pail. The gap pattern then grows rather than creating another meeting."), ("Count", r"The meeting times are $200,240,260,280,$ and $320$, for a total of $5$ meetings."), ("Answer", r"They meet $\boxed{5}$ times." )],
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
        if r["year"] == "2008" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2008 AMC 10B Answer Key\n\n"
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





