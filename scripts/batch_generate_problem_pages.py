from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 32
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2007_AMC_10A_Answer_Key"
TARGET_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
SKIPPED = []
BATCH_LABEL = "2007 AMC 10A Problems 1-10"
NEXT_START = "2007 AMC 10A Problem 11"

ANS = {
    1: ("C", "10"),
    2: ("A", r"-\frac{1}{2}"),
    3: ("D", "2"),
    4: ("A", "4"),
    5: ("B", "$5.84"),
    6: ("A", "2002 and 2003"),
    7: ("D", "37,500"),
    8: ("D", "50"),
    9: ("E", "60"),
    10: ("E", "6"),
}


OV = {
    1: (r"One ticket to a show costs $\$20$ at full price. Susan buys $4$ tickets using a coupon that gives her a $25\%$ discount. Pam buys $5$ tickets using a coupon that gives her a $30\%$ discount. How many more dollars does Pam pay than Susan?", [("A", "$2$"), ("B", "$5$"), ("C", "$10$"), ("D", "$15$"), ("E", "$20$")]),
    2: (r"Define $a@b=ab-b^2$ and $a\#b=a+b-ab^2$. What is $\frac{6@2}{6\#2}$?", [("A", r"$-\frac12$"), ("B", r"$-\frac14$"), ("C", r"$\frac18$"), ("D", r"$\frac14$"), ("E", r"$\frac12$")]),
    3: (r"An aquarium has a rectangular base that measures $100$ cm by $40$ cm and has height $50$ cm. It is filled with water to a height of $40$ cm. A brick with a rectangular base that measures $40$ cm by $20$ cm and height $10$ cm is placed in the aquarium. By how many centimeters does the water rise?", [("A", "$0.5$"), ("B", "$1$"), ("C", "$1.5$"), ("D", "$2$"), ("E", "$2.5$")]),
    4: (r"The larger of two consecutive odd integers is three times the smaller. What is their sum?", [("A", "$4$"), ("B", "$8$"), ("C", "$12$"), ("D", "$16$"), ("E", "$20$")]),
    5: (r"A school store sells $7$ pencils and $8$ notebooks for $\$4.15$. It also sells $5$ pencils and $3$ notebooks for $\$1.77$. How much do $16$ pencils and $10$ notebooks cost?", [("A", "$1.76"), ("B", "$5.84"), ("C", "$6.00"), ("D", "$6.16"), ("E", "$6.32")]),
    6: (r"At Euclid High School, the number of students taking the AMC 10 was $60$ in $2002$, $66$ in $2003$, $70$ in $2004$, $76$ in $2005$, $78$ in $2006$, and $85$ in $2007$. Between what two consecutive years was there the largest percentage increase?", [("A", "2002 and 2003"), ("B", "2003 and 2004"), ("C", "2004 and 2005"), ("D", "2005 and 2006"), ("E", "2006 and 2007")]),
    7: (r"Last year Mr. John Q. Public received an inheritance. He paid $20\%$ in federal taxes on the inheritance, and paid $10\%$ of what he had left in state taxes. He paid a total of $\$10,500$ for both taxes. How many dollars was the inheritance?", [("A", "$30,000"), ("B", "$32,500"), ("C", "$35,000"), ("D", "$37,500"), ("E", "$40,000")]),
    8: (r"Triangles $ABC$ and $ADC$ are isosceles with $AB=BC$ and $AD=DC$. Point $D$ is inside $\triangle ABC$. Angle $ABC=40^\circ$, and angle $ADC=140^\circ$. What is the degree measure of $\angle BAD$?", [("A", "$20$"), ("B", "$30$"), ("C", "$40$"), ("D", "$50$"), ("E", "$60$")]),
    9: (r"Real numbers $a$ and $b$ satisfy the equations $3^a=81^{b+2}$ and $125^b=5^{a-3}$. What is $ab$?", [("A", "$-60$"), ("B", "$-17$"), ("C", "$9$"), ("D", "$12$"), ("E", "$60$")]),
    10: (r"The Dunbar family consists of a mother, a father, and some children. The average age of the members of the family is $20$, the father is $48$ years old, and the average age of the mother and children is $16$. How many children are in the family?", [("A", "$2$"), ("B", "$3$"), ("C", "$4$"), ("D", "$5$"), ("E", "$6$")]),
}


KEY_OVERRIDES = {
    1: "Compute each discounted ticket total, then compare.",
    2: "Evaluate each custom operation exactly as defined before forming the fraction.",
    3: "Use displaced volume divided by aquarium base area to find the rise in water height.",
    4: "Represent consecutive odd integers algebraically and solve the relation.",
    5: "Solve a two-variable linear pricing system and compute the requested combination.",
    6: "Compare percentage increases, not raw increases.",
    7: "Model sequential percentage taxes as fractions of the original inheritance.",
    8: "Use base angles in two isosceles triangles to subtract angles at A.",
    9: "Rewrite powers using common bases and solve the resulting linear system.",
    10: "Use weighted averages to compare total family age in two ways.",
}


SOL = {
    1: [("Find Susan's cost", r"A $25\%$ discount means Susan pays $75\%$ of full price. Four tickets at $\$20$ each would cost $\$80$, so Susan pays $0.75\cdot80=60$ dollars."), ("Find Pam's cost", r"A $30\%$ discount means Pam pays $70\%$ of full price. Five tickets at $\$20$ each would cost $\$100$, so Pam pays $0.70\cdot100=70$ dollars."), ("Compare", r"Pam pays $70-60=10$ more dollars than Susan."), ("Check the scale", r"Pam buys one more ticket, but also has a larger discount. A difference of $10$ dollars is reasonable."), ("Answer", r"The answer is $\boxed{10}$." )],
    2: [("Evaluate the numerator", r"Use $a@b=ab-b^2$. With $a=6$ and $b=2$, we get $6@2=6\cdot2-2^2=12-4=8$."), ("Evaluate the denominator", r"Use $a\#b=a+b-ab^2$. Thus $6\#2=6+2-6\cdot2^2=8-24=-16$."), ("Form the fraction", r"The requested value is $\frac{6@2}{6\#2}=\frac{8}{-16}=-\frac12$."), ("Watch the sign", r"The denominator is negative, so the final answer must be negative. That eliminates all positive choices."), ("Answer", r"The answer is $\boxed{-\frac12}$." )],
    3: [("Find the brick's volume", r"The brick displaces water equal to its volume, assuming it is fully submerged. Its volume is $40\cdot20\cdot10=8000$ cubic centimeters."), ("Find the aquarium base area", r"The base of the aquarium has area $100\cdot40=4000$ square centimeters."), ("Convert volume to height", r"A rise of $h$ centimeters over that base has volume $4000h$. So $4000h=8000$, giving $h=2$."), ("Check for overflow", r"The water starts at height $40$ cm and rises $2$ cm, reaching $42$ cm, below the aquarium height $50$ cm. So no overflow changes the answer."), ("Answer", r"The water rises $\boxed{2}$ centimeters." )],
    4: [("Set up the consecutive odd integers", r"Let the smaller odd integer be $x$. Then the next consecutive odd integer is $x+2$."), ("Use the given relationship", r"The larger is three times the smaller, so $x+2=3x$."), ("Solve", r"This gives $2=2x$, so $x=1$. The larger integer is $3$."), ("Find the sum", r"Their sum is $1+3=4$."), ("Answer", r"The answer is $\boxed{4}$." )],
    5: [("Name the prices", r"Let $p$ be the price of one pencil in cents and $n$ be the price of one notebook in cents. Then $7p+8n=415$ and $5p+3n=177$."), ("Solve the system", r"From $5p+3n=177$, $p=\frac{177-3n}{5}$. Substitute into the first equation: $7\left(\frac{177-3n}{5}\right)+8n=415$."), ("Find each price", r"Multiplying by $5$ gives $1239-21n+40n=2075$, so $19n=836$ and $n=44$. Then $5p+3\cdot44=177$, so $p=9$."), ("Compute the requested cost", r"The cost of $16$ pencils and $10$ notebooks is $16\cdot9+10\cdot44=144+440=584$ cents."), ("Answer", r"The answer is $\boxed{\$5.84}$." )],
    6: [("Use percentages", r"The problem asks for percentage increase, so we compare increase divided by the previous year's number, not just the raw increase."), ("Compute the main candidates", r"From $2002$ to $2003$, the increase is $6$ out of $60$, which is $10\%$. From $2004$ to $2005$, the increase is $6$ out of $70$, which is less than $10\%$. From $2006$ to $2007$, the increase is $7$ out of $78$, also less than $10\%$."), ("Check the smaller increases", r"The other increases are $4$ out of $66$ and $2$ out of $76$, both clearly smaller percentages."), ("Choose the largest", r"The largest percentage increase is therefore from $2002$ to $2003$."), ("Answer", r"The answer is $\boxed{\text{2002 and 2003}}$." )],
    7: [("Let the inheritance be $x$", r"The federal tax is $20\%$ of $x$, or $0.20x$. After that tax, he has $0.80x$ left."), ("Compute the state tax", r"The state tax is $10\%$ of what remains, so it is $0.10\cdot0.80x=0.08x$."), ("Use the total tax", r"The total tax is $0.20x+0.08x=0.28x$. We are told this equals $10,500$."), ("Solve", r"Thus $0.28x=10500$, so $x=10500/0.28=37500$."), ("Answer", r"The inheritance was $\boxed{37,500}$ dollars." )],
    8: [("Use triangle $ABC$", r"Since $AB=BC$, triangle $ABC$ is isosceles with vertex angle $\angle ABC=40^\circ$. Therefore the base angles at $A$ and $C$ are each $\frac{180-40}{2}=70^\circ$."), ("Use triangle $ADC$", r"Since $AD=DC$, triangle $ADC$ is also isosceles, with vertex angle $\angle ADC=140^\circ$. Its base angles at $A$ and $C$ are each $\frac{180-140}{2}=20^\circ$."), ("Relate the angles at $A$", r"Point $D$ is inside $\triangle ABC$, so ray $AD$ splits angle $BAC$. We know $\angle BAC=70^\circ$ and $\angle DAC=20^\circ$."), ("Subtract", r"Therefore $\angle BAD=70^\circ-20^\circ=50^\circ$."), ("Answer", r"The answer is $\boxed{50^\circ}$." )],
    9: [("Rewrite using common bases", r"Since $81=3^4$, the first equation becomes $3^a=(3^4)^{b+2}=3^{4b+8}$, so $a=4b+8$."), ("Rewrite the second equation", r"Since $125=5^3$, the second equation becomes $(5^3)^b=5^{a-3}$, so $3b=a-3$, or $a=3b+3$."), ("Solve the linear system", r"Set the two expressions for $a$ equal: $4b+8=3b+3$. Hence $b=-5$. Then $a=3(-5)+3=-12$."), ("Compute $ab$", r"Now $ab=(-12)(-5)=60$."), ("Answer", r"The answer is $\boxed{60}$." )],
    10: [("Let the number of children be $n$", r"Then the family has $n+2$ members: the children, the mother, and the father."), ("Use the whole-family average", r"The total age of the whole family is $20(n+2)$."), ("Use the mother-and-children average", r"The mother and children together have $n+1$ people with average age $16$, so their total age is $16(n+1)$. Adding the father's age gives total family age $16(n+1)+48$."), ("Set the totals equal", r"So $20(n+2)=16(n+1)+48$. This simplifies to $20n+40=16n+64$, hence $4n=24$ and $n=6$."), ("Answer", r"There are $\boxed{6}$ children." )],
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
        if r["year"] == "2007" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2007 AMC 10A Answer Key\n\n"
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
