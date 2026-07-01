import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 58
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2011_AMC_10A_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2011 AMC 10A Problems 21-25"
NEXT_START = "2011 AMC 10B Problem 1"

ANS = {
    21: ("D", r"\frac{15}{19}"),
    22: ("C", "3120"),
    23: ("C", "365"),
    24: ("D", r"\frac{1}{6}"),
    25: ("C", "2320"),
}

OV = {
    21: (r"Two counterfeit coins of equal weight are mixed with $8$ identical genuine coins. The weight of each counterfeit coin is different from the weight of each genuine coin. A pair of coins is selected at random without replacement from the $10$ coins. A second pair is selected at random without replacement from the remaining $8$ coins. The combined weight of the first pair is equal to the combined weight of the second pair. What is the probability that all $4$ selected coins are genuine?", [("A",r"\frac{7}{11}"),("B",r"\frac{9}{13}"),("C",r"\frac{11}{15}"),("D",r"\frac{15}{19}"),("E",r"\frac{15}{16}")]),
    22: (r"Each vertex of convex pentagon $ABCDE$ is to be assigned a color. There are $6$ colors to choose from, and the ends of each diagonal must have different colors. How many different colorings are possible?", [("A","2520"),("B","2880"),("C","3120"),("D","3250"),("E","3750")]),
    23: (r"Seven students count from $1$ to $1000$ as follows. Alice says all the numbers except the middle number in each consecutive group of three numbers. Barbara says all of the numbers Alice does not say, except she also skips the middle number in each consecutive group of three numbers. Candice, Debbie, Eliza, and Fatima continue the same process in alphabetical order. Finally, George says the only number that no one else says. What number does George say?", [("A","37"),("B","242"),("C","365"),("D","728"),("E","998")]),
    24: (r"Two distinct regular tetrahedra have all their vertices among the vertices of the same unit cube. What is the volume of the region formed by the intersection of the tetrahedra?", [("A",r"\frac{1}{12}"),("B",r"\frac{\sqrt2}{12}"),("C",r"\frac{\sqrt3}{12}"),("D",r"\frac{1}{6}"),("E",r"\frac{\sqrt2}{6}")]),
    25: (r"Let $R$ be a square region and $n\ge4$ an integer. A point $X$ in the interior of $R$ is called $n$-ray partitional if there are $n$ rays emanating from $X$ that divide $R$ into $n$ triangles of equal area. How many points are $100$-ray partitional but not $60$-ray partitional?", [("A","1500"),("B","1560"),("C","2320"),("D","2480"),("E","2500")]),
}

KEY_OVERRIDES = {
    21: "Condition on equal pair weights and count the possible type patterns of the two pairs.",
    22: "The diagonal constraints form a 5-cycle coloring problem.",
    23: "Repeatedly keeping the middle number in each group of three creates a base-3 recurrence.",
    24: "The intersection of the two cube tetrahedra is the octahedron with vertices at the face centers.",
    25: "Translate equal-area ray partitions into integer conditions on the distances from the point to the square's sides.",
}

SOL = {
    21: [
        ("Focus on the condition", r"We are told that the two pair weights are equal. Since both counterfeit coins have the same weight and all genuine coins have the same weight, a pair's weight depends only on how many counterfeit coins it contains."),
        ("List possible equal-weight cases", r"The two pairs can have equal weight in two useful ways: both pairs are genuine-genuine, or both pairs are mixed with one genuine and one counterfeit. A pair of two counterfeit coins cannot be matched by another such pair because there are only two counterfeit coins total."),
        ("Count all-genuine equal cases", r"For ordered first and second pairs, the all-genuine case has $\binom82\binom62=28\cdot15=420$ possibilities."),
        ("Count mixed equal cases", r"For the first pair to be mixed, choose $1$ of the $2$ counterfeit coins and $1$ of the $8$ genuine coins, giving $16$ choices. The second pair must use the remaining counterfeit coin and one of the remaining $7$ genuine coins, giving $7$ choices. That makes $112$ mixed cases."),
        ("Compute the conditional probability", r"Given equal weights, there are $420+112=532$ possible cases, and $420$ of them have all four coins genuine. Thus the probability is $\frac{420}{532}=\frac{15}{19}$. The answer is $\boxed{\frac{15}{19}}$."),
    ],
    22: [
        ("Understand the graph of restrictions", r"In a pentagon, the diagonals connect vertices that are not adjacent. The rule says the two endpoints of every diagonal must have different colors."),
        ("Notice the diagonal graph", r"The five diagonals themselves form another $5$-cycle on the same vertices. So the problem is equivalent to properly coloring a cycle of length $5$ using $6$ colors."),
        ("Use the cycle coloring formula", r"The number of proper colorings of a cycle of length $n$ with $k$ colors is $(k-1)^n+(-1)^n(k-1)$. Here $n=5$ and $k=6$."),
        ("Calculate", r"This gives $5^5-5=3125-5=3120$."),
        ("Conclude", r"There are $\boxed{3120}$ valid colorings."),
    ],
    23: [
        ("See what each student leaves behind", r"Each student says all available numbers except the middle number in each consecutive group of three. So after a student is done, the numbers left are exactly the $2$nd, $5$th, $8$th, and so on in that student's current list."),
        ("Track positions, not all numbers", r"If a number is the $k$th number in the next remaining list, then before that round it was in position $3k-1$. This gives a simple reverse recurrence: go backward by replacing $k$ with $3k-1$."),
        ("Count the rounds", r"Alice, Barbara, Candice, Debbie, Eliza, and Fatima each perform this skipping process. George receives the one number left after six such rounds."),
        ("Work backward from the final number", r"Start with final position $1$ and apply $k\mapsto3k-1$ six times: \[1\to2\to5\to14\to41\to122\to365.\]"),
        ("Conclude", r"So George says the number $\boxed{365}$."),
    ],
    24: [
        ("Visualize the two tetrahedra", r"A unit cube has two regular tetrahedra formed by choosing alternating vertices. These two tetrahedra are distinct and symmetric inside the cube."),
        ("Identify the intersection", r"Their intersection is the octahedron whose vertices are the centers of the six faces of the cube. This is a common and useful way to see the central overlap of the two alternating tetrahedra."),
        ("Split the octahedron", r"That octahedron can be split into two congruent square pyramids. The shared square is the middle cross-section of the cube, and its side length is $\frac{\sqrt2}{2}$, so its area is $\left(\frac{\sqrt2}{2}\right)^2=\frac12$."),
        ("Compute the volume", r"Each pyramid has height $\frac12$. So the total octahedron volume is \[2\cdot\frac13\cdot\frac12\cdot\frac12=\frac16.\]"),
        ("Conclude", r"The intersection volume is $\boxed{\frac16}$."),
    ],
    25: [
        ("Turn the square into coordinates", r"Let the square have side length $1$, and let point $X$ have distances $x$, $1-x$, $y$, and $1-y$ from the four sides. We only need distances to the sides because each small triangle has base on a side of the square and height equal to the distance from $X$ to that side."),
        ("Find the condition for one side", r"If the square is divided into $n$ equal-area triangles, each triangle has area $\frac1n$. Along a side at distance $h$ from $X$, a triangle with base length $b$ has area $\frac12bh$, so $b=\frac{2}{nh}$. Since the side length is $1$, the number of such equal triangles along that side is $\frac{1}{b}=\frac{nh}{2}$."),
        ("Convert to integer conditions", r"Therefore $X$ is $n$-ray partitional exactly when $\frac{nx}{2}$, $\frac{n(1-x)}{2}$, $\frac{ny}{2}$, and $\frac{n(1-y)}{2}$ are integers. For even $n$, this is equivalent to requiring $\frac{nx}{2}$ and $\frac{ny}{2}$ to be integers."),
        ("Count 100-ray points", r"For $n=100$, we need $50x$ and $50y$ to be integers. Since $X$ is inside the square, each coordinate can be $\frac1{50},\frac2{50},\ldots,\frac{49}{50}$, giving $49^2=2401$ points."),
        ("Subtract the 60-ray points", r"For $n=60$, we need $30x$ and $30y$ to be integers. A point counted by both conditions must have both $50x$ and $30x$ integers, so $10x$ is an integer; similarly $10y$ is an integer. That gives $9^2=81$ points counted by both."),
        ("Finish", r"The number that are $100$-ray partitional but not $60$-ray partitional is $2401-81=2320$. The answer is $\boxed{2320}$."),
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {18}) else notes
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
        if r["year"] == "2011" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2011 AMC 10A Answer Key\n\n"
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
























