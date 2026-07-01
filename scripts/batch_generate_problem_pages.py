import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 117
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2020_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2020 AMC 10A Problems 21-25"
NEXT_START = "2020 AMC 10B Problem 1"

ANS={21:("C","137"),22:("A","22"),23:("A","12"),24:("C","18"),25:("A",r"\frac7{36}")}

OV={
21:(r"There exists a unique strictly increasing sequence of nonnegative integers $a_1<a_2<\cdots<a_k$ such that \[\frac{2^{289}+1}{2^{17}+1}=2^{a_1}+2^{a_2}+\cdots+2^{a_k}.\] What is $k$?",[("A","117"),("B","136"),("C","137"),("D","273"),("E","306")]),
22:(r"For how many positive integers $n\le1000$ is \[\left\lfloor\frac{998}{n}\right\rfloor+\left\lfloor\frac{999}{n}\right\rfloor+\left\lfloor\frac{1000}{n}\right\rfloor\] not divisible by $3$?",[("A","22"),("B","23"),("C","24"),("D","25"),("E","26")]),
23:(r"Let $T$ be the triangle with vertices $(0,0),(4,0),(0,3)$. Consider five isometries: rotations of $90^\circ,180^\circ,270^\circ$ counterclockwise around the origin, reflection across the $x$-axis, and reflection across the $y$-axis. How many of the $125$ sequences of three of these transformations return $T$ to its original position?",[("A","12"),("B","15"),("C","17"),("D","20"),("E","25")]),
24:(r"Let $n$ be the least positive integer greater than $1000$ for which \[\gcd(63,n+120)=21\] and \[\gcd(n+63,120)=60.\] What is the sum of the digits of $n$?",[("A","12"),("B","15"),("C","18"),("D","21"),("E","24")]),
25:(r"Jason rolls three fair standard six-sided dice. Then he chooses a subset of the dice to reroll. After rerolling, he wins if and only if the sum is exactly $7$. Jason always plays to optimize his chances of winning. What is the probability that he chooses to reroll exactly two of the dice?",[("A",r"$\frac7{36}$"),("B",r"$\frac5{24}$"),("C",r"$\frac29$"),("D",r"$\frac{17}{72}$"),("E",r"$\frac14$")]),
}

KEY_OVERRIDES={21:"Use the finite geometric factorization and count binary 1-blocks.",22:"Compare the three floor terms to $3\lfloor999/n\rfloor$.",23:"Count first-two transformation products whose inverse is in the allowed set.",24:"Translate gcd conditions into congruences.",25:"Classify initial dice rolls by which reroll subset gives the best probability."}

SOL={
21:[("Use the sum of powers identity",r"Let $x=2^{17}$. Since $289=17\cdot17$, \[\frac{2^{289}+1}{2^{17}+1}=\frac{x^{17}+1}{x+1}.\] For odd exponent $17$, \[\frac{x^{17}+1}{x+1}=x^{16}-x^{15}+x^{14}-\cdots-x+1.\]"),("Return to powers of two",r"This becomes \[2^{272}-2^{255}+2^{238}-2^{221}+\cdots-2^{17}+1.\]"),("Pair positive and negative terms",r"Each pair \[2^{17r}-2^{17(r-1)}\] equals \[2^{17(r-1)}(2^{17}-1),\] which is a block of $17$ consecutive $1$s in binary."),("Count the blocks",r"There are $8$ such positive-minus-negative pairs, giving \[8\cdot17=136\] ones in the binary expansion."),("Add the final term",r"The final $+1$ contributes one more $1$ in the binary expansion."),("Conclude",r"Thus $k=136+1=\boxed{137}$."),],
22:[("Compare to the middle term",r"Let \[q=\left\lfloor\frac{999}{n}\right\rfloor.\] The three floor terms are usually $q,q,q$, except when crossing a multiple of $n$ near $999$."),("Find when the first term drops",r"\[\left\lfloor\frac{998}{n}\right\rfloor=q-1\] exactly when $n$ divides $999$. Otherwise it equals $q$."),("Find when the last term rises",r"\[\left\lfloor\frac{1000}{n}\right\rfloor=q+1\] exactly when $n$ divides $1000$. Otherwise it equals $q$."),("Use divisibility by 3",r"The sum is \[3q-1,\quad 3q,\quad\text{or}\quad3q+1.\] It is not divisible by $3$ exactly when $n$ divides $999$ or $1000$, but not both."),("Count divisors",r"We have \[999=3^3\cdot37,\] which has $8$ divisors, and \[1000=2^3\cdot5^3,\] which has $16$ divisors. The only common divisor is $1$, and for $n=1$ the two changes cancel."),("Conclude",r"The count is \[8+16-2=22.\] The answer is $\boxed{22}$."),],
23:[("Represent the transformations",r"Let $R$ be rotation by $90^\circ$, and let $X$ and $Y$ be reflections across the $x$- and $y$-axes. The allowed set is \[\{R,R^2,R^3,X,Y\}.\]"),("Use the first two transformations",r"Once the first two transformations are chosen, the third transformation must be the inverse of their product in order for the total composition to be the identity."),("Count valid first-two products",r"Among the $25$ ordered choices for the first two transformations, the product is one of the allowed five transformations in exactly $12$ cases. This can be checked from the small dihedral group table: the allowed product counts are $2$ for $R$, $4$ for $R^2$, $2$ for $R^3$, $2$ for $X$, and $2$ for $Y$."),("Choose the third transformation",r"For each of these $12$ first-two choices, the required inverse is also in the allowed set and is uniquely determined."),("Conclude",r"Therefore $\boxed{12}$ sequences return the triangle to its original position."),],
24:[("Translate the first gcd condition",r"Since $63=3^2\cdot7$, the condition \[\gcd(63,n+120)=21\] means $n+120$ is divisible by $21$ but not by $9$. In particular, \[n\equiv -120\equiv6\pmod{21}.\]"),("Translate the second gcd condition",r"Since $120=2^3\cdot3\cdot5$, the condition \[\gcd(n+63,120)=60\] means $n+63$ is divisible by $60$ but not by $120$. Thus \[n\equiv57\pmod{60}\] and specifically \[n\equiv117\pmod{120}.\]"),("Solve the congruences",r"Solve \[n\equiv6\pmod{21},\qquad n\equiv117\pmod{120}.\] Checking values $117,237,357,\ldots$ modulo $21$, the solutions are \[n\equiv237\pmod{840}.\]"),("Find the least value over 1000",r"The least positive integer greater than $1000$ in this congruence class is \[237+2\cdot840=1917.\]"),("Check the excluded divisibility",r"This value satisfies the required non-divisibility by $9$ and by $120$, so both gcd conditions are exact."),("Conclude",r"The sum of the digits is \[1+9+1+7=\boxed{18}.\]"),],
25:[("Think in terms of the initial roll",r"Jason chooses the reroll subset after seeing the three dice. For each initial roll, compare the best winning probability from rerolling $0,1,2,$ or $3$ dice."),("Use a complete classification",r"For the $216$ equally likely initial rolls, the optimal choice is unique. A direct classification by kept sum shows: reroll $0$ dice for $15$ rolls, reroll $1$ die for $132$ rolls, reroll $2$ dice for $42$ rolls, and reroll all $3$ dice for $27$ rolls."),("Explain the two-dice class",r"Rerolling exactly two dice is best when keeping one die creates a target sum for two dice with higher probability than any one-die or three-dice option. For example, keeping a $1$ needs the two rerolled dice to sum to $6$, which has probability $\frac5{36}$."),("Count favorable initial rolls",r"The classification gives $42$ initial rolls for which the unique optimal strategy rerolls exactly two dice."),("Compute probability",r"Since all $216$ initial rolls are equally likely, the probability is \[\frac{42}{216}=\frac7{36}.\]"),("Conclude",r"The answer is $\boxed{\frac7{36}}$."),],
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
        if r["year"] == "2020" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2020 AMC 10A Answer Key\n\n"
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












































