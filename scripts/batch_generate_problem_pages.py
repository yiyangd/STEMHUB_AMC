import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 72
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2013_AMC_10A_Answer_Key"
TARGET_NUMBERS = {16,17,18,19,20}
SKIPPED = []
BATCH_LABEL = "2013 AMC 10A Problems 16-20"
NEXT_START = "2013 AMC 10A Problem 21"

ANS = {16:("E",r"\frac{32}{3}"),17:("B","54"),18:("B","58"),19:("C","13"),20:("C",r"2-\sqrt2+\frac{\pi}{4}")}

OV = {
16:(r"A triangle with vertices $(6,5)$, $(8,-3)$, and $(9,1)$ is reflected about the line $x=8$ to create a second triangle. What is the area of the union of the two triangles?",[("A","9"),("B",r"\frac{28}{3}"),("C","10"),("D",r"\frac{31}{3}"),("E",r"\frac{32}{3}")]),
17:(r"Daphne is visited periodically by her three best friends. Alice visits every third day, Beatrix every fourth day, and Claire every fifth day. All three visited Daphne yesterday. How many days of the next $365$-day period will exactly two friends visit her?",[("A","48"),("B","54"),("C","60"),("D","66"),("E","72")]),
18:(r"Let $A=(0,0)$, $B=(1,2)$, $C=(3,3)$, and $D=(4,0)$. Quadrilateral $ABCD$ is cut into equal-area pieces by a line passing through $A$. This line intersects $CD$ at $(\frac pq,\frac rs)$, where the fractions are in lowest terms. What is $p+q+r+s$?",[("A","54"),("B","58"),("C","62"),("D","70"),("E","75")]),
19:(r"In base $10$, the number $2013$ ends in digit $3$. In base $9$, the same number is written as $(2676)_9$ and ends in digit $6$. For how many positive integers $b$ does the base-$b$ representation of $2013$ end in digit $3$?",[("A","6"),("B","9"),("C","13"),("D","16"),("E","18")]),
20:(r"A unit square is rotated $45^\circ$ about its center. What is the area of the region swept out by the interior of the square?",[("A",r"1-\frac{\sqrt2}{2}+\frac{\pi}{4}"),("B",r"1+\frac{\pi}{4}"),("C",r"2-\sqrt2+\frac{\pi}{4}"),("D",r"2+\frac{\pi}{4}"),("E",r"1+\frac{\sqrt2}{2}+\frac{\pi}{8}")]),
}

KEY_OVERRIDES={16:"Compute the two triangle areas and subtract their overlap after reflection.",17:"Use inclusion-exclusion on days divisible by pairs of 3, 4, and 5.",18:"Use coordinate area and a parameter on segment CD.",19:"The last digit in base $b$ is the remainder modulo $b$.",20:"Add the original square and four congruent swept corner regions."}

SOL={
16:[("Reflect the vertices",r"Reflecting across $x=8$ sends $(6,5)$ to $(10,5)$, keeps $(8,-3)$ fixed, and sends $(9,1)$ to $(7,1)$. So the two triangles are mirror images."),("Compute one triangle area",r"Using the shoelace formula on $(6,5),(8,-3),(9,1)$ gives area $8$. The two triangles together would have area $16$ before subtracting overlap."),("Find the overlap",r"The overlap is the quadrilateral with vertices $(8,\frac73)$, $(7,1)$, $(8,-3)$, and $(9,1)$. The shoelace formula gives its area $\frac{16}{3}$."),("Subtract the overlap",r"The union area is $8+8-\frac{16}{3}=\frac{32}{3}$."),("Conclude",r"The answer is $\boxed{\frac{32}{3}}$."),],
17:[("Translate visit days",r"Since all three visited yesterday, in the next period Alice visits on multiples of $3$, Beatrix on multiples of $4$, and Claire on multiples of $5$."),("Count pair meetings",r"Alice and Beatrix both visit on multiples of $12$, giving $\lfloor365/12\rfloor=30$ days. Alice and Claire both visit on multiples of $15$, giving $24$ days. Beatrix and Claire both visit on multiples of $20$, giving $18$ days."),("Remove triple visits",r"Days when all three visit are multiples of $60$, giving $\lfloor365/60\rfloor=6$ days. Each such day was counted in all three pair counts, but should count zero times for exactly two friends."),("Compute exactly two",r"The number is $30+24+18-3\cdot6=54$."),("Conclude",r"The answer is $\boxed{54}$."),],
18:[("Find the total area",r"Using the shoelace formula for $A(0,0),B(1,2),C(3,3),D(4,0)$, the area of quadrilateral $ABCD$ is $\frac{15}{2}$. Half of this is $\frac{15}{4}$."),("Parameterize point P",r"Let $P$ be on segment $CD$. Write $P=(4-t,3t)$, where $t=0$ gives $D$ and $t=1$ gives $C$."),("Use triangle ADP",r"The line $AP$ cuts off triangle $ADP$ along the bottom side. Since $AD=4$ and the height of $P$ above $AD$ is $3t$, the area of $\triangle ADP$ is $\frac12\cdot4\cdot3t=6t$."),("Set equal areas",r"We need $6t=\frac{15}{4}$, so $t=\frac58$. Then $P=(4-\frac58,3\cdot\frac58)=(\frac{27}{8},\frac{15}{8})$."),("Add the requested numbers",r"Thus $p+q+r+s=27+8+15+8=58$. The answer is $\boxed{58}$."),],
19:[("Interpret the last digit",r"In base $b$, the last digit of $2013$ is the remainder when $2013$ is divided by $b$. We want that remainder to be $3$."),("Set up divisibility",r"So $2013\equiv3\pmod b$, which means $b$ divides $2010$. Also $b>3$, because digit $3$ must be allowed in base $b$."),("Count divisors",r"The factorization is $2010=2\cdot3\cdot5\cdot67$, so it has $2^4=16$ positive divisors."),("Exclude small bases",r"The divisors $1,2,3$ do not give valid bases with final digit $3$. Therefore the number of valid bases is $16-3=13$."),("Conclude",r"The answer is $\boxed{13}$."),],
20:[("Start with the original square",r"The swept region contains the original unit square, whose area is $1$. As the square rotates, each corner creates one congruent extra curved region outside the original square."),("Compute one corner sector",r"Each vertex is distance $\frac{\sqrt2}{2}$ from the center and rotates through $45^\circ=\frac{\pi}{4}$ radians. The sector area traced by one vertex is $\frac12(\frac{\sqrt2}{2})^2\cdot\frac{\pi}{4}=\frac{\pi}{16}$."),("Subtract the part already inside",r"For each corner, the part of this sector already inside the original square is a small right triangle of area $\frac{\sqrt2-1}{4}$. Thus the new area contributed by one corner is $\frac{\pi}{16}-\frac{\sqrt2-1}{4}$."),("Add four corners",r"The swept area is \[1+4\left(\frac{\pi}{16}-\frac{\sqrt2-1}{4}\right)=1+\frac{\pi}{4}-(\sqrt2-1).\]"),("Simplify",r"This equals $2-\sqrt2+\frac{\pi}{4}$. The answer is $\boxed{2-\sqrt2+\frac{\pi}{4}}$."),],
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
    note = "This problem contains a diagram. Please refer to the original PDF or AoPS page." if ("图" in notes or "figure" in notes.lower() or n in {16,17}) else notes
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
        if r["year"] == "2013" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2013 AMC 10A Answer Key\n\n"
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








































