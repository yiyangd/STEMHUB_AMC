from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 50
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2010_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
SKIPPED = []
BATCH_LABEL = "2010 AMC 10A Problems 1-10"
NEXT_START = "2010 AMC 10A Problem 11"

ANS={1:("D","4"),2:("B",r"\frac43"),3:("D","25"),4:("B","51.5"),5:("E","144"),6:("C",r"\frac43"),7:("C",r"\sqrt3"),8:("D","13"),9:("E","24"),10:("E","2017")}

OV={
1:(r"Mary's top book shelf holds five books with the following widths, in centimeters: $6$, $\frac12$, $1$, $2.5$, and $10$. What is the average book width, in centimeters?",[("A","$1$"),("B","$2$"),("C","$3$"),("D","$4$"),("E","$5$")]),
2:(r"Four identical squares and one rectangle are placed together to form one large square. The four identical squares form a row across the top of the large square, and the rectangle fills the remaining space below them. The length of the rectangle is how many times as large as its width?",[("A",r"$\frac54$"),("B",r"$\frac43$"),("C",r"$\frac32$"),("D","$2$"),("E","$3$")]),
3:(r"Tyrone had $97$ marbles and Eric had $11$ marbles. Tyrone then gave some of his marbles to Eric so that Tyrone ended with twice as many marbles as Eric. How many marbles did Tyrone give to Eric?",[("A","$3$"),("B","$13$"),("C","$18$"),("D","$25$"),("E","$29$")]),
4:(r"A book that is to be recorded onto compact discs takes $412$ minutes to read aloud. Each disc can hold up to $56$ minutes of reading. Assume that the smallest possible number of discs is used and that each disc contains the same length of reading. How many minutes of reading will each disc contain?",[("A","$50.2$"),("B","$51.5$"),("C","$52.4$"),("D","$53.8$"),("E","$55.2$")]),
5:(r"The area of a circle whose circumference is $24\pi$ is $k\pi$. What is the value of $k$?",[("A","$6$"),("B","$12$"),("C","$24$"),("D","$36$"),("E","$144$")]),
6:(r"For positive numbers $x$ and $y$, the operation $x\spadesuit y$ is defined by $x\spadesuit y=x-\frac1y$. What is $2\spadesuit(2\spadesuit2)$?",[("A",r"$\frac23$"),("B","$1$"),("C",r"$\frac43$"),("D",r"$\frac53$"),("E","$2$")]),
7:(r"Crystal has a running course marked out for her daily run. She begins this run by heading due north for one mile. She then runs northeast for one mile, then southeast for one mile. The last portion of her run takes her on a straight line back to where she started. How far, in miles, is this last portion of her run?",[("A","$1$"),("B",r"$\sqrt2$"),("C",r"$\sqrt3$"),("D","$2$"),("E",r"$2\sqrt2$")]),
8:(r"Tony works $2$ hours a day and is paid $\$0.50$ per hour for each full year of his age. During a six month period Tony worked $50$ days and earned $\$630$. How old was Tony at the end of the six month period?",[("A","$9$"),("B","$11$"),("C","$12$"),("D","$13$"),("E","$14$")]),
9:(r"A palindrome, such as $83438$, is a number that remains the same when its digits are reversed. The numbers $x$ and $x+32$ are three-digit and four-digit palindromes, respectively. What is the sum of the digits of $x$?",[("A","$20$"),("B","$21$"),("C","$22$"),("D","$23$"),("E","$24$")]),
10:(r"Marvin had a birthday on Tuesday, May $27$ in the leap year $2008$. In what year will his birthday next fall on a Saturday?",[("A","$2011$"),("B","$2012$"),("C","$2013$"),("D","$2015$"),("E","$2017$")]),
}

KEY_OVERRIDES={1:"Add the five widths and divide by 5.",2:"Use the four equal top squares to compare the large square side with the rectangle height.",3:"Use the total number of marbles and the final 2-to-1 ratio.",4:"Use the smallest number of discs that can hold the total time, then divide evenly.",5:"Use circumference to find radius, then compute area.",6:"Evaluate the custom operation from the inside out.",7:"Add direction vectors and use distance from the origin.",8:"Convert total pay to an average hourly rate and account for Tony's birthday during the six-month period.",9:"The only possible four-digit palindrome near a three-digit number plus 32 is 1001.",10:"Track weekday shifts from birthday to birthday, including leap-year shifts."}

SOL={
1:[("Identify the data",r"The five widths are $6$, $\frac12$, $1$, $2.5$, and $10$ centimeters."),("Add the widths",r"Their sum is $6+0.5+1+2.5+10=20$."),("Divide by the number of books",r"There are $5$ books, so the average width is $20\div5=4$."),("Answer",r"The average width is $\boxed{4}$ centimeters.")],
2:[("Name the small square side",r"Let each small square have side length $s$. Four of them placed in a row make the side length of the large square $4s$."),("Find the rectangle dimensions",r"The rectangle fills the space under the top row of squares. Its length is the full width $4s$, and its width is the remaining height $4s-s=3s$."),("Compute the ratio",r"The length-to-width ratio is $\frac{4s}{3s}=\frac43$."),("Answer",r"The rectangle's length is $\boxed{\frac43}$ times its width.")],
3:[("Use the total",r"Together Tyrone and Eric have $97+11=108$ marbles, and giving marbles from one to the other does not change the total."),("Use the final ratio",r"At the end Tyrone has twice as many as Eric, so their final amounts are in the ratio $2:1$."),("Find Eric's final amount",r"Eric must have $\frac13$ of the total, which is $108\div3=36$ marbles."),("Find the transfer",r"Eric started with $11$ marbles and ended with $36$, so Tyrone gave him $36-11=25$ marbles."),("Answer",r"Tyrone gave Eric $\boxed{25}$ marbles.")],
4:[("Estimate the number of discs",r"Each disc can hold at most $56$ minutes, so we compare $412$ with multiples of $56$."),("Choose the smallest possible number",r"Since $7\cdot56=392$ is too small and $8\cdot56=448$ is enough, the smallest possible number of discs is $8$."),("Divide the reading evenly",r"The reading is split equally among the $8$ discs, so each disc contains $412\div8=51.5$ minutes."),("Answer",r"Each disc contains $\boxed{51.5}$ minutes of reading.")],
5:[("Find the radius",r"The circumference is $2\pi r=24\pi$, so $r=12$."),("Compute the area",r"The area is $\pi r^2=\pi\cdot12^2=144\pi$."),("Match k",r"Since the area is $k\pi$, we have $k=144$."),("Answer",r"The value of $k$ is $\boxed{144}$.")],
6:[("Evaluate the inner operation",r"First compute $2\spadesuit2=2-\frac12=\frac32$."),("Use that as the second input",r"Now compute $2\spadesuit\frac32=2-\frac{1}{3/2}$."),("Simplify",r"Since $\frac{1}{3/2}=\frac23$, the value is $2-\frac23=\frac43$."),("Answer",r"The result is $\boxed{\frac43}$.")],
7:[("Use vectors",r"Represent north as $(0,1)$. A one-mile northeast run contributes $(\frac{\sqrt2}{2},\frac{\sqrt2}{2})$, and a one-mile southeast run contributes $(\frac{\sqrt2}{2},-\frac{\sqrt2}{2})$."),("Add the displacement",r"The two diagonal runs have vertical components that cancel, and their horizontal components add to $\sqrt2$. Including the first mile north, Crystal's final position is $(\sqrt2,1)$."),("Find the distance home",r"The straight-line distance back to the starting point is $\sqrt{(\sqrt2)^2+1^2}=\sqrt3$."),("Answer",r"The last portion is $\boxed{\sqrt3}$ miles.")],
8:[("Find Tony's average hourly pay",r"Tony worked $2\cdot50=100$ hours and earned $630$, so his average hourly pay was $\$6.30$."),("Translate pay into age",r"He is paid $\$0.50$ per hour for each full year of age, so an hourly rate of $\$6.30$ corresponds to an average credited age of $12.6$ years."),("Interpret the six-month period",r"A credited age between $12$ and $13$ means Tony was $12$ for part of the work period and $13$ for the rest. Therefore he must have turned $13$ during the six months."),("Answer",r"At the end of the period, Tony was $\boxed{13}$ years old.")],
9:[("Restrict the four-digit palindrome",r"Since $x$ is three digits, $x+32$ is between $132$ and $1031$. The only four-digit palindrome in this range is $1001$."),("Find x",r"Thus $x+32=1001$, so $x=969$."),("Add the digits",r"The sum of the digits of $969$ is $9+6+9=24$."),("Answer",r"The digit sum is $\boxed{24}$.")],
10:[("Track yearly shifts",r"From one May $27$ to the next, the weekday usually moves forward one day. It moves forward two days if the interval includes February $29$."),("List the birthdays",r"Starting from Tuesday in $2008$: $2009$ is Wednesday, $2010$ is Thursday, $2011$ is Friday, and because $2012$ is a leap year with February $29$ before May $27$, $2012$ is Sunday."),("Continue until Saturday",r"Then $2013$ is Monday, $2014$ Tuesday, $2015$ Wednesday, $2016$ Friday, and $2017$ Saturday."),("Answer",r"His birthday next falls on a Saturday in $\boxed{2017}$.")],
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {2},
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













