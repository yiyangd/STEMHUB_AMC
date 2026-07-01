import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 120
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2020_AMC_10B_Answer_Key"
TARGET_NUMBERS = {22,23,24,25}
SKIPPED = ["2020 AMC 10B Problem 21 skipped: area question depends on the missing square diagram with points E,F,G,H,I,J."]
BATCH_LABEL = "2020 AMC 10B Problems 22-25"
NEXT_START = "2021 Spring AMC 10A Problem 1"

ANS={22:("D","201"),23:("C",r"2^{38}"),24:("C","6"),25:("A","112")}

OV={
22:(r"What is the remainder when $2^{202}+202$ is divided by $2^{101}+2^{51}+1$?",[("A","100"),("B","101"),("C","200"),("D","201"),("E","202")]),
23:(r"Square $ABCD$ in the coordinate plane has vertices at $A(1,1)$, $B(-1,1)$, $C(-1,-1)$, and $D(1,-1)$. Consider the transformations $L$ and $R$, rotations by $90^\circ$ counterclockwise and clockwise around the origin, and $H$ and $V$, reflections across the $x$-axis and $y$-axis. How many sequences of $20$ transformations chosen from $\{L,R,H,V\}$ send all labeled vertices back to their original positions?",[("A",r"$2^{37}$"),("B",r"$3\cdot2^{36}$"),("C",r"$2^{38}$"),("D",r"$3\cdot2^{37}$"),("E",r"$2^{39}$")]),
24:(r"How many positive integers $n$ satisfy \[\frac{n+1000}{70}=\lfloor\sqrt n\rfloor?\] Recall that $\lfloor x\rfloor$ is the greatest integer not exceeding $x$.",[("A","2"),("B","4"),("C","6"),("D","30"),("E","32")]),
25:(r"Let $D(n)$ denote the number of ways of writing the positive integer $n$ as a product \[n=f_1\cdot f_2\cdots f_k,\] where $k\ge1$, the $f_i$ are integers strictly greater than $1$, and the order of the factors matters. For example, $D(6)=3$ because $6$, $2\cdot3$, and $3\cdot2$ are counted. What is $D(96)$?",[("A","112"),("B","128"),("C","144"),("D","172"),("E","184")]),
}

KEY_OVERRIDES={22:"Rewrite the numerator as a multiple of the divisor plus a small remainder.",23:"Use the symmetry group structure and count one-step extensions.",24:"Replace the floor value by an integer parameter.",25:"Use a recurrence for ordered factorizations of $2^a3^b$."}

SOL={
22:[("Look for the divisor inside the numerator",r"The divisor is \[2^{101}+2^{51}+1.\] Since the numerator contains $2^{202}=(2^{101})^2$, we try to rewrite $2^{202}+202$ as a multiple of this divisor plus a small leftover."),("Use a difference of squares",r"Notice that \[(2^{101}-2^{51}+1)(2^{101}+2^{51}+1)=(2^{101}+1)^2-(2^{51})^2.\] The two middle terms cancel because $2\cdot2^{101}=2^{102}=(2^{51})^2$."),("Rewrite the numerator",r"Therefore \[(2^{101}-2^{51}+1)(2^{101}+2^{51}+1)=2^{202}+1,\] so \[2^{202}+202=(2^{101}-2^{51}+1)(2^{101}+2^{51}+1)+201.\]"),("Identify the remainder",r"The leftover is $201$, and $201$ is smaller than the divisor. Therefore it is the actual remainder."),("Conclude",r"The answer is $\boxed{201}$."),],
23:[("Think of configurations, not individual coordinates",r"Each transformation sends the labeled square to another labeled configuration of the same square. The question asks for sequences whose final configuration is the original one."),("Use the last move idea",r"A useful way to count is to choose the first $19$ transformations freely, then ask whether there is a final transformation that returns the square to its starting labeled position."),("Why the final move is unique",r"After an odd number of moves, the square is always one allowed move away from the original configuration. Among $L,R,H,V$, exactly one transformation sends that current configuration back to the original."),("Count prefixes",r"There are $4$ choices for each of the first $19$ transformations, and each such prefix has exactly one valid final choice. Thus the number of valid sequences is \[4^{19}=2^{38}.\]"),("Conclude",r"The answer is $\boxed{2^{38}}$."),],
24:[("Name the floor value",r"Let \[k=\lfloor\sqrt n\rfloor.\] The equation becomes \[\frac{n+1000}{70}=k,\] so \[n=70k-1000.\]"),("Translate the floor condition",r"The condition $k=\lfloor\sqrt n\rfloor$ means \[k^2\le n<(k+1)^2.\] Substitute $n=70k-1000$ into both inequalities."),("Use the left inequality",r"From $k^2\le70k-1000$, we get \[k^2-70k+1000\le0,\] or \[(k-20)(k-50)\le0.\] Thus $20\le k\le50$."),("Use the right inequality",r"From $70k-1000<(k+1)^2$, we get \[k^2-68k+1001>0.\] The roots are between $21$ and $22$, and between $46$ and $47$, so this holds for integer $k\le21$ or $k\ge47$."),("Count valid k values",r"Combining the ranges gives \[k=20,21,47,48,49,50,\] for $6$ values. Each gives one positive integer $n=70k-1000$."),("Conclude",r"The answer is $\boxed{6}$."),],
25:[("Factor the number first",r"The number is \[96=2^5\cdot3.\] Ordered factorizations can be counted by tracking how the powers of $2$ and the single power of $3$ are distributed among ordered factors."),("Set up a recurrence",r"Let $F(a,b)$ be the number of ordered factorizations of $2^a3^b$, with $F(0,0)=1$ representing the empty product used inside the recurrence. The first factor can take any nonzero part of the exponents, and the rest is counted recursively."),("Handle powers of two",r"For pure powers of two, \[F(a,0)=2^{a-1}\quad(a\ge1),\] and $F(0,0)=1$. So \[F(0,0),F(1,0),\ldots,F(5,0)=1,1,2,4,8,16.\]"),("Compute the values with one factor of 3",r"Let $G_a=F(a,1)$. Then \[G_a=\sum_{t=0}^{a-1}G_t+\sum_{t=0}^{a}F(t,0).\] Starting with $G_0=1$, this gives \[G_1=3,\quad G_2=8,\quad G_3=20,\quad G_4=48,\quad G_5=112.\]"),("Apply to 96",r"Because $96=2^5\cdot3$, we need $F(5,1)=G_5=112$."),("Conclude",r"The answer is $\boxed{112}$."),],
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
        if r["year"] == "2020" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2020 AMC 10B Answer Key\n\n"
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












































