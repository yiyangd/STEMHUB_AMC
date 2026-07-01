import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 60
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2011_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,13,14,15}
SKIPPED = []
BATCH_LABEL = "2011 AMC 10B Problems 11-15"
NEXT_START = "2011 AMC 10B Problem 16"

ANS = {
    11: ("D", "5"),
    12: ("A", r"\frac{\pi}{3}"),
    13: ("D", r"\frac{5}{9}"),
    14: ("C", "62"),
    15: ("E", "II and III only"),
}

OV = {
    11: (r"There are $52$ people in a room. What is the largest value of $n$ such that the statement 'At least $n$ people in this room have birthdays falling in the same month' is always true?", [("A","2"),("B","3"),("C","4"),("D","5"),("E","12")]),
    12: (r"Keiko walks once around a track at exactly the same constant speed every day. The sides of the track are straight, and the ends are semicircles. The track has width $6$ meters, and it takes her $36$ seconds longer to walk around the outside edge of the track than around the inside edge. What is Keiko's speed in meters per second?", [("A",r"\frac{\pi}{3}"),("B",r"\frac{2\pi}{3}"),("C",r"\pi"),("D",r"\frac{4\pi}{3}"),("E",r"\frac{5\pi}{3}")]),
    13: (r"Two real numbers are selected independently at random from the interval $[-20,10]$. What is the probability that the product of those numbers is greater than zero?", [("A",r"\frac19"),("B",r"\frac13"),("C",r"\frac49"),("D",r"\frac59"),("E",r"\frac23")]),
    14: (r"A rectangular parking lot has a diagonal of $25$ meters and an area of $168$ square meters. In meters, what is the perimeter of the parking lot?", [("A","52"),("B","58"),("C","62"),("D","68"),("E","70")]),
    15: (r"Let $@$ denote the 'averaged with' operation: $a@b=\frac{a+b}{2}$. Which of the following distributive laws hold for all numbers $x,y,z$? I. $x@(y+z)=(x@y)+(x@z)$ II. $x+(y@z)=(x+y)@(x+z)$ III. $x@(y@z)=(x@y)@(x@z)$", [("A","I only"),("B","II only"),("C","III only"),("D","I and III only"),("E","II and III only")]),
}

KEY_OVERRIDES = {
    11: "Use the pigeonhole principle with 52 people and 12 months.",
    12: "The outside track is longer only because the two semicircular ends have larger radius.",
    13: "The product is positive when both selected numbers have the same sign.",
    14: "Use side product and diagonal information to find the sum of side lengths.",
    15: "Expand the averaging operation algebraically and compare both sides of each identity.",
}

SOL = {
    11: [
        ("Use the pigeonhole principle", r"Birth months are the boxes, and the $52$ people are the objects being placed into those boxes. There are $12$ months."),
        ("Find the forced minimum", r"If we tried to keep every month at $4$ or fewer birthdays, we could place at most $12\cdot4=48$ people. But there are $52$ people."),
        ("Increase the guarantee", r"Since $48$ is not enough, at least one month must contain at least $5$ people."),
        ("Check that 6 is not guaranteed", r"It is possible to distribute $52$ people as four months with $5$ birthdays and eight months with $4$ birthdays. Then no month has $6$ people, so $6$ is not guaranteed."),
        ("Conclude", r"The largest guaranteed value of $n$ is $\boxed{5}$."),
    ],
    12: [
        ("Compare inside and outside tracks", r"The straight parts of the inside and outside paths have the same lengths in pairs; the extra distance comes from the rounded ends."),
        ("Use the semicircles", r"Two semicircles make one full circle. The outside rounded path has radius $6$ meters more than the inside rounded path, so the difference in curved length is the difference of two circumferences: $2\pi\cdot6=12\pi$."),
        ("Use time equals distance over speed", r"Keiko takes $36$ seconds longer to walk the extra $12\pi$ meters. Since her speed is constant, \[\text{speed}=\frac{12\pi}{36}=\frac{\pi}{3}.\]"),
        ("Conclude", r"Her speed is $\boxed{\frac{\pi}{3}}$ meters per second."),
    ],
    13: [
        ("Identify when the product is positive", r"A product of two real numbers is positive when both numbers are positive or both numbers are negative. The probability of selecting exactly zero is $0$, so it does not affect the answer."),
        ("Find the interval lengths", r"The full interval $[-20,10]$ has length $30$. The negative part has length $20$, and the positive part has length $10$."),
        ("Compute same-sign probability", r"The probability both numbers are negative is $\left(\frac{20}{30}\right)^2=\frac49$. The probability both are positive is $\left(\frac{10}{30}\right)^2=\frac19$."),
        ("Add the cases", r"The total probability is $\frac49+\frac19=\frac59$. The answer is $\boxed{\frac59}$."),
    ],
    14: [
        ("Name the side lengths", r"Let the rectangle have side lengths $x$ and $y$. The area gives $xy=168$, and the diagonal gives $x^2+y^2=25^2=625$."),
        ("Look for the perimeter", r"The perimeter is $2(x+y)$, so we do not need $x$ and $y$ separately. We only need $x+y$."),
        ("Use the identity", r"Since $(x+y)^2=x^2+y^2+2xy$, we get \[(x+y)^2=625+2\cdot168=625+336=961.\]"),
        ("Finish", r"Thus $x+y=31$, and the perimeter is $2\cdot31=62$. The answer is $\boxed{62}$."),
    ],
    15: [
        ("Translate the operation", r"The operation $a@b$ means $\frac{a+b}{2}$. The safest way to test these laws is to expand both sides."),
        ("Test statement I", r"The left side is $x@(y+z)=\frac{x+y+z}{2}$. The right side is $(x@y)+(x@z)=\frac{x+y}{2}+\frac{x+z}{2}=x+\frac{y+z}{2}$. These are not always equal, so I is false."),
        ("Test statement II", r"The left side is $x+(y@z)=x+\frac{y+z}{2}$. The right side is $(x+y)@(x+z)=\frac{x+y+x+z}{2}=x+\frac{y+z}{2}$. These match, so II is true."),
        ("Test statement III", r"The left side is $x@(y@z)=\frac{x+\frac{y+z}{2}}{2}=\frac{x}{2}+\frac{y}{4}+\frac{z}{4}$. The right side is $(x@y)@(x@z)=\frac{\frac{x+y}{2}+\frac{x+z}{2}}{2}=\frac{x}{2}+\frac{y}{4}+\frac{z}{4}$. These match, so III is true."),
        ("Conclude", r"Exactly statements II and III hold. The answer is $\boxed{\text{II and III only}}$."),
    ],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {9}) else notes
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
        if r["year"] == "2011" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2011 AMC 10B Answer Key\n\n"
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



























