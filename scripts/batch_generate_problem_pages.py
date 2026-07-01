import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 88
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2015_AMC_10B_Answer_Key"
TARGET_NUMBERS = {1,2,3,4,5,6,7,10}
SKIPPED = ["2015 AMC 10B Problem 8 skipped: answer choices are images of a transformed letter", "2015 AMC 10B Problem 9 skipped: shaded falcata region depends on diagram interpretation"]
BATCH_LABEL = "2015 AMC 10B Problems 1-10 excluding 8 and 9"
NEXT_START = "2015 AMC 10B Problem 11"

ANS={1:("C",r"\frac74"),2:("B","3:30 PM"),3:("A","8"),4:("C","Beth, Cyril, Dan, Alex"),5:("B","Hikmet"),6:("E","Saturday"),7:("A",r"-\frac7{30}"),10:("C","negative and ending with 5")}

OV={
1:(r"What is the value of $2-(-2)^{-2}$?",[("A","-2"),("B",r"\frac1{16}"),("C",r"\frac74"),("D",r"\frac94"),("E","6")]),
2:(r"Marie does three equally time-consuming tasks in a row without taking breaks. She begins the first task at 1:00 PM and finishes the second task at 2:40 PM. When does she finish the third task?",[("A","3:10 PM"),("B","3:30 PM"),("C","4:00 PM"),("D","4:10 PM"),("E","4:30 PM")]),
3:(r"Isaac has written down one integer two times and another integer three times. The sum of the five numbers is $100$, and one of the numbers is $28$. What is the other number?",[("A","8"),("B","11"),("C","14"),("D","15"),("E","18")]),
4:(r"Four siblings ordered an extra large pizza. Alex ate $\frac15$, Beth ate $\frac13$, and Cyril ate $\frac14$ of the pizza. Dan got the leftovers. What is the sequence of the siblings in decreasing order of the part of pizza they consumed?",[("A","Alex, Beth, Cyril, Dan"),("B","Beth, Cyril, Alex, Dan"),("C","Beth, Cyril, Dan, Alex"),("D","Beth, Dan, Cyril, Alex"),("E","Dan, Beth, Cyril, Alex")]),
5:(r"David, Hikmet, Jack, Marta, Rand, and Todd were in a $12$-person race with $6$ other people. Rand finished $6$ places ahead of Hikmet. Marta finished $1$ place behind Jack. David finished $2$ places behind Hikmet. Jack finished $2$ places behind Todd. Todd finished $1$ place behind Rand. Marta finished in $6$th place. Who finished in $8$th place?",[("A","David"),("B","Hikmet"),("C","Jack"),("D","Rand"),("E","Todd")]),
6:(r"Marley practices exactly one sport each day of the week. She runs three days a week but never on two consecutive days. On Monday she plays basketball and two days later golf. She swims and plays tennis, but she never plays tennis the day after running or swimming. Which day of the week does Marley swim?",[("A","Sunday"),("B","Tuesday"),("C","Thursday"),("D","Friday"),("E","Saturday")]),
7:(r"Consider the operation 'minus the reciprocal of,' defined by $a\diamond b=a-\frac1b$. What is $((1\diamond2)\diamond3)-(1\diamond(2\diamond3))$?",[("A",r"-\frac7{30}"),("B",r"-\frac16"),("C","0"),("D",r"\frac16"),("E",r"\frac7{30}")]),
10:(r"What are the sign and units digit of the product of all the odd negative integers strictly greater than $-2015$?",[("A","It is a negative number ending with a 1."),("B","It is a positive number ending with a 1."),("C","It is a negative number ending with a 5."),("D","It is a positive number ending with a 5."),("E","It is a negative number ending with a 0.")]),
}

KEY_OVERRIDES={1:"Handle the negative exponent before subtracting.",2:"Use equal task durations.",3:"Test which repeated count can contain the given number.",4:"Compute Dan's leftover fraction and compare.",5:"Work backward through the race-position clues.",6:"Use the weekly schedule constraints systematically.",7:"Evaluate the custom operation in the correct grouping.",10:"Count factors for the sign and use the units digit cycle."}

SOL={
1:[("Evaluate the negative exponent",r"First compute $(-2)^{-2}=\frac{1}{(-2)^2}=\frac14$."),("Subtract",r"The expression is $2-\frac14=\frac84-\frac14=\frac74$."),("Check the sign",r"The subtracted amount is small and positive, so the answer should be slightly less than $2$."),("Conclude",r"The answer is $\boxed{\frac74}$."),],
2:[("Find the time for two tasks",r"From 1:00 PM to 2:40 PM is $100$ minutes. That covers the first two equally long tasks."),("Find one task length",r"Each task takes $100/2=50$ minutes."),("Add the third task",r"Starting from 2:40 PM, another $50$ minutes brings Marie to 3:30 PM."),("Conclude",r"The answer is $\boxed{\text{3:30 PM}}$."),],
3:[("Set up the two possibilities",r"One integer is written twice and the other is written three times. One of the two integers is $28$."),("Test if 28 is written twice",r"If $28$ were written twice, it would contribute $56$, leaving $44$ for three equal integers, which is impossible."),("Use the other case",r"Therefore $28$ is written three times, contributing $84$. The two copies of the other integer sum to $100-84=16$."),("Solve",r"The other integer is $16/2=8$."),("Conclude",r"The answer is $\boxed{8}$."),],
4:[("Compare the known fractions",r"Beth ate $\frac13$, Cyril ate $\frac14$, and Alex ate $\frac15$, so among those three the order is Beth, Cyril, Alex."),("Compute Dan's share",r"Dan ate the leftover amount: \[1-\frac13-\frac14-\frac15=\frac{60-20-15-12}{60}=\frac{13}{60}.\]"),("Place Dan in the order",r"We compare $\frac{13}{60}$ with $\frac14=\frac{15}{60}$ and $\frac15=\frac{12}{60}$. Dan ate less than Cyril but more than Alex."),("Conclude",r"The decreasing order is $\boxed{\text{Beth, Cyril, Dan, Alex}}$."),],
5:[("Start from the fixed position",r"Marta finished in $6$th place. Since Marta was $1$ place behind Jack, Jack finished $5$th."),("Work backward through the clues",r"Jack was $2$ places behind Todd, so Todd finished $3$rd. Todd was $1$ place behind Rand, so Rand finished $2$nd."),("Find Hikmet",r"Rand finished $6$ places ahead of Hikmet, so Hikmet finished $2+6=8$th."),("Conclude",r"The person in $8$th place was $\boxed{\text{Hikmet}}$."),],
6:[("Fill the fixed sports",r"Monday is basketball, and two days later means Wednesday is golf. The remaining five days are Tuesday, Thursday, Friday, Saturday, and Sunday."),("Place the three running days",r"Marley runs on three nonconsecutive days. Among the remaining days, the only workable running pattern is Tuesday, Friday, and Sunday."),("Use the tennis restriction",r"The remaining days are Thursday and Saturday. Tennis cannot be the day after running or swimming. Thursday can be tennis because Wednesday is golf."),("Identify swimming",r"That leaves Saturday for swimming. This also avoids putting tennis immediately after swimming."),("Conclude",r"Marley swims on $\boxed{\text{Saturday}}$."),],
7:[("Evaluate the left grouping",r"First, $1\diamond2=1-\frac12=\frac12$. Then \[(1\diamond2)\diamond3=\frac12-\frac13=\frac16.\]"),("Evaluate the right grouping",r"Next, $2\diamond3=2-\frac13=\frac53$. Then \[1\diamond(2\diamond3)=1-\frac{1}{5/3}=1-\frac35=\frac25.\]"),("Subtract the two results",r"\[\frac16-\frac25=\frac5{30}-\frac{12}{30}=-\frac7{30}.\]"),("Conclude",r"The answer is $\boxed{-\frac7{30}}$."),],
10:[("Count the factors",r"The odd negative integers strictly greater than $-2015$ are $-2013,-2011,\ldots,-1$. There are $1007$ such numbers."),("Determine the sign",r"An odd number of negative factors gives a negative product, so the product is negative."),("Find the units digit",r"The absolute values include every odd number from $1$ to $2013$. Since one factor is $5$ and all factors are odd, the product's units digit is $5$."),("Conclude",r"The product is $\boxed{\text{negative and ending with 5}}$."),],
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
    if n in {10,17} and notes == "题面包含图形":
        notes = ""
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if n in set() else notes
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
        if r["year"] == "2015" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": int(r["problem_no"]) in set(),
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
        + "- Answer verification source: AoPS 2015 AMC 10B Answer Key\n\n"
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












































