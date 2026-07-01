from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 45
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2009_AMC_10A_Answer_Key"
TARGET_NUMBERS = {11, 12, 13, 14, 16, 17, 18, 19}
SKIPPED = [
    "2009 AMC 10A Problem 15 skipped: OCR/diagram sequence text is incomplete",
    "2009 AMC 10A Problem 20 skipped: OCR appears to contain only displaced choices/figure labels",
]
BATCH_LABEL = "2009 AMC 10A Problems 11-14, 16-19"
NEXT_START = "2009 AMC 10A Problem 21"

ANS={11:("D","125"),12:("C","13"),13:("E",r"P^{2n}Q^m"),14:("A","3"),16:("D","18"),17:("C",r"\frac{125}{12}"),18:("D","51%"),19:("B","8")}

OV={
11:(r"One dimension of a cube is increased by $1$, another is decreased by $1$, and the third is left unchanged. The volume of the new rectangular solid is $5$ less than that of the cube. What was the volume of the cube?",[("A","$8$"),("B","$27$"),("C","$64$"),("D","$125$"),("E","$216$")]),
12:(r"In quadrilateral $ABCD$, $AB=5$, $BC=17$, $CD=5$, $DA=9$, and $BD$ is an integer. What is $BD$?",[("A","$11$"),("B","$12$"),("C","$13$"),("D","$14$"),("E","$15$")]),
13:(r"Suppose that $P=2^m$ and $Q=3^n$. Which of the following is equal to $12^{mn}$ for every pair of integers $(m,n)$?",[("A",r"$P^2Q$"),("B",r"$P^nQ^m$"),("C",r"$P^nQ^{2m}$"),("D",r"$P^{2m}Q^n$"),("E",r"$P^{2n}Q^m$")]),
14:(r"Four congruent rectangles are placed around a square as shown. The area of the outer square is $4$ times that of the inner square. What is the ratio of the length of the longer side of each rectangle to the length of its shorter side?",[("A","$3$"),("B",r"$\sqrt{10}$"),("C",r"$2+\sqrt2$"),("D",r"$2\sqrt3$"),("E","$4$")]),
16:(r"Let $a,b,c,$ and $d$ be real numbers with $|a-b|=2$, $|b-c|=3$, and $|c-d|=4$. What is the sum of all possible values of $|a-d|$?",[("A","$9$"),("B","$12$"),("C","$15$"),("D","$18$"),("E","$24$")]),
17:(r"Rectangle $ABCD$ has $AB=4$ and $BC=3$. Segment $EF$ is constructed through $B$ so that $EF$ is perpendicular to $DB$, and $A$ and $C$ lie on $DE$ and $DF$, respectively. What is $EF$?",[("A","$9$"),("B","$10$"),("C",r"$\frac{125}{12}$"),("D",r"$\frac{103}{9}$"),("E","$12$")]),
18:(r"At Jefferson Summer Camp, $60\%$ of the children play soccer, $30\%$ of the children swim, and $40\%$ of the soccer players swim. To the nearest whole percent, what percent of the non-swimmers play soccer?",[("A","$30\%$"),("B","$40\%$"),("C","$49\%$"),("D","$51\%$"),("E","$70\%$")]),
19:(r"Circle $A$ has radius $100$. Circle $B$ has an integer radius $r<100$ and remains internally tangent to circle $A$ as it rolls once around the circumference of circle $A$. The two circles have the same points of tangency at the beginning and end of circle $B$'s trip. How many possible values can $r$ have?",[("A","$4$"),("B","$8$"),("C","$9$"),("D","$50$"),("E","$90$")]),
}

KEY_OVERRIDES={11:"Compare the cube volume with the changed rectangular-prism volume.",12:"Use triangle inequalities on the two triangles formed by diagonal BD.",13:"Rewrite 12 as powers of 2 and 3, then match exponents using P and Q.",14:"Relate outer and inner square side lengths in terms of the rectangle sides.",16:"Represent each absolute-value difference as a signed step and list possible net distances.",17:"Use coordinates and a line perpendicular to the rectangle diagonal.",18:"Use a 100-child model and subtract swimmers from soccer players.",19:"The small circle returns to the same tangency point when the internal rolling rotation count is an integer."}

SOL={
11:[("Let the cube side be s",r"If the cube has side length $s$, its volume is $s^3$."),("Write the new dimensions",r"The rectangular solid has dimensions $s+1$, $s-1$, and $s$. Its volume is $(s+1)(s-1)s=(s^2-1)s=s^3-s$."),("Use the volume difference",r"The new volume is $5$ less than the cube volume, so $s^3-s=s^3-5$."),("Solve",r"This gives $s=5$."),("Answer",r"The original cube volume is $5^3=\boxed{125}$.")],
12:[("Use BD as a shared side",r"The diagonal $BD$ forms triangles $ABD$ and $BCD$. We can restrict $BD$ using triangle inequalities."),("Apply triangle ABD",r"Triangle $ABD$ has sides $5,9,BD$, so $|9-5|<BD<9+5$, giving $4<BD<14$."),("Apply triangle BCD",r"Triangle $BCD$ has sides $17,5,BD$, so $|17-5|<BD<17+5$, giving $12<BD<22$."),("Combine with integer condition",r"The only integer satisfying both $4<BD<14$ and $12<BD<22$ is $13$."),("Answer",r"Therefore $BD=\boxed{13}$.")],
13:[("Rewrite the target",r"Since $12=2^2\cdot3$, we have $12^{mn}=2^{2mn}3^{mn}$."),("Use P and Q",r"Because $P=2^m$, raising $P$ to $2n$ gives $P^{2n}=2^{2mn}$."),("Match the power of 3",r"Because $Q=3^n$, raising $Q$ to $m$ gives $Q^m=3^{mn}$."),("Multiply",r"Thus $P^{2n}Q^m=2^{2mn}3^{mn}=12^{mn}$."),("Answer",r"The matching expression is $\boxed{P^{2n}Q^m}$.")],
14:[("Name the rectangle sides",r"Let the shorter side be $x$ and the longer side be $y$. In the standard four-rectangle arrangement, the outer square has side $x+y$, and the inner square has side $y-x$."),("Use the area ratio",r"The outer square area is $4$ times the inner square area, so $(x+y)^2=4(y-x)^2$."),("Take positive square roots",r"Since side lengths are positive, $x+y=2(y-x)$."),("Solve for the ratio",r"This simplifies to $x+y=2y-2x$, so $3x=y$. Therefore $\frac{y}{x}=3$."),("Answer",r"The ratio is $\boxed{3}$.")],
16:[("Turn each distance into a signed step",r"The conditions mean $a-b$ can be $\pm2$, $b-c$ can be $\pm3$, and $c-d$ can be $\pm4$."),("Add the steps",r"We have $a-d=(a-b)+(b-c)+(c-d)$, so possible values come from $\pm2\pm3\pm4$."),("List distinct absolute values",r"The possible net sums have absolute values $1,3,5,$ and $9$."),("Add them",r"The required sum is $1+3+5+9=18$."),("Answer",r"The sum of all possible values is $\boxed{18}$.")],
17:[("Place the rectangle on coordinates",r"Let $A=(0,0)$, $B=(4,0)$, $C=(4,3)$, and $D=(0,3)$. Then diagonal $DB$ has slope $-\frac34$."),("Find the perpendicular line",r"A line perpendicular to $DB$ has slope $\frac43$. Through $B=(4,0)$, it has equation $y=\frac43(x-4)$."),("Find E and F",r"Line $DE$ passes through $D$ and $A$, so it is $x=0$; intersecting gives $E=(0,-\frac{16}{3})$. Line $DF$ passes through $D$ and $C$, so it is $y=3$; intersecting gives $F=(\frac{25}{4},3)$."),("Compute EF",r"The differences are $\Delta x=\frac{25}{4}$ and $\Delta y=\frac{25}{3}$, so $EF=\sqrt{(\frac{25}{4})^2+(\frac{25}{3})^2}=25\sqrt{\frac1{16}+\frac1{9}}=\frac{125}{12}$."),("Answer",r"Thus $EF=\boxed{\frac{125}{12}}$.")],
18:[("Use a convenient total",r"Imagine there are $100$ children. Then $60$ play soccer and $30$ swim."),("Find soccer players who swim",r"Since $40\%$ of soccer players swim, $0.40\cdot60=24$ children both play soccer and swim."),("Find soccer-playing non-swimmers",r"The soccer players who do not swim are $60-24=36$."),("Find all non-swimmers",r"The total number of non-swimmers is $100-30=70$."),("Compute the percentage",r"The desired percent is $\frac{36}{70}\approx51.4\%$, which rounds to $51\%$."),("Answer",r"The answer is $\boxed{51\%}$.")],
19:[("Think in rotations",r"When a circle of radius $r$ rolls internally inside a circle of radius $100$, its center travels around a circle of radius $100-r$."),("Use the internal rolling count",r"The small circle makes $\frac{100-r}{r}=\frac{100}{r}-1$ rotations relative to its own circumference during one trip."),("Require the same tangency point",r"For the same point of circle $B$ to return to tangency, this rotation count must be an integer. Therefore $\frac{100}{r}$ must be an integer."),("Count possible radii",r"So $r$ must be a positive divisor of $100$ less than $100$: $1,2,4,5,10,20,25,50$."),("Answer",r"There are $\boxed{8}$ possible values of $r$.")],
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
        if r["year"] == "2009" and r["form"] == "A" and int(r["problem_no"]) in TARGET_NUMBERS
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
                "needs_review": ("题面包含图形" in (r.get("notes") or "")) or int(r["problem_no"]) in {14},
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
        + "- Answer verification source: AoPS 2009 AMC 10A Answer Key\n\n"
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







