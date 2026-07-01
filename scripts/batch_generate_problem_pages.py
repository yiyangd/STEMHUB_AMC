import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 55
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2010_AMC_10B_Answer_Key"
TARGET_NUMBERS = {21,22,23,24,25}
SKIPPED = []
BATCH_LABEL = "2010 AMC 10B Problems 21-25"
NEXT_START = "2011 AMC 10A Problem 1"

ANS = {
    21: ("E", r"\frac{1}{5}"),
    22: ("C", "1932"),
    23: ("D", "42"),
    24: ("E", "34"),
    25: ("B", "315"),
}

OV = {
    21: r"A palindrome between $1000$ and $10{,}000$ is chosen at random. What is the probability that it is divisible by $7$?",
    22: r"Seven distinct pieces of candy are to be distributed among three bags. The red bag and the blue bag must each receive at least one piece of candy; the white bag may remain empty. How many arrangements are possible?",
    23: r"The entries in a $3\times3$ array include all the digits from $1$ through $9$, arranged so that the entries in every row and every column are in increasing order. How many such arrays are there?",
    24: r"A high school basketball game between the Raiders and Wildcats was tied at the end of the first quarter. The number of points scored by the Raiders in each of the four quarters formed an increasing geometric sequence, and the number of points scored by the Wildcats in each of the four quarters formed an increasing arithmetic sequence. At the end of the fourth quarter, the Raiders had won by one point. Neither team scored more than $100$ points. What was the total number of points scored by the two teams in the first half?",
    25: r"Let $a>0$, and let $P(x)$ be a polynomial with integer coefficients such that $P(1)=P(3)=P(5)=P(7)=a$, and $P(2)=P(4)=P(6)=P(8)=-a$. What is the smallest possible value of $a$?",
}
OV = {k: (v, None) for k, v in OV.items()}

KEY_OVERRIDES = {
    21: "Write a four-digit palindrome algebraically and test divisibility by 7.",
    22: "Use complementary counting to enforce nonempty red and blue bags.",
    23: "Recognize the row-and-column increasing array as a standard Young tableau and use hook lengths.",
    24: "Model the two teams' quarter scores with sequences and use the one-point final difference.",
    25: "Use divisibility properties of integer-coefficient polynomials to force a lower bound, then construct it.",
}

SOL = {
    21: [
        ("Describe the palindromes", r"A palindrome between $1000$ and $10{,}000$ has four digits, so it has the form $abba$. Algebraically this is $1000a+100b+10b+a=1001a+110b$, where $a$ can be $1$ through $9$ and $b$ can be $0$ through $9$."),
        ("Count the total possibilities", r"There are $9$ choices for $a$ and $10$ choices for $b$, so there are $90$ palindromes total. Now we only need to count which of these are divisible by $7$."),
        ("Use modular arithmetic", r"Since $1001=7\cdot143$, the term $1001a$ is always divisible by $7$. Therefore divisibility by $7$ depends only on $110b$. Because $110\equiv5\pmod7$, we need $5b\equiv0\pmod7$, so $b\equiv0\pmod7$."),
        ("Count favorable palindromes", r"The digit $b$ can be $0$ or $7$. For each of those $2$ choices, $a$ can still be any of $9$ nonzero digits. Thus there are $18$ favorable palindromes."),
        ("Compute the probability", r"The probability is $\frac{18}{90}=\frac15$. The answer is $\boxed{\frac15}$."),
    ],
    22: [
        ("Start with all distributions", r"Each of the $7$ distinct candies can independently go into the red, blue, or white bag. Without restrictions, that gives $3^7$ possible distributions."),
        ("Subtract distributions with an empty required bag", r"The red bag is not allowed to be empty. If it is empty, each candy has only two choices, blue or white, giving $2^7$ bad distributions. Similarly, there are $2^7$ distributions where the blue bag is empty."),
        ("Correct for double subtraction", r"If both the red and blue bags are empty, then all candies are in the white bag. That one distribution was subtracted twice, so we add it back once."),
        ("Calculate", r"The number of valid distributions is \[3^7-2^7-2^7+1=2187-128-128+1=1932.\]"),
        ("Conclude", r"Therefore there are $\boxed{1932}$ arrangements."),
    ],
    23: [
        ("Recognize the structure", r"The entries must increase left to right in every row and top to bottom in every column. This is exactly the same structure as filling a $3\times3$ Young diagram with $1$ through $9$ so that rows and columns increase."),
        ("Use the hook-length idea", r"For this kind of increasing array, the number of fillings is \[\frac{9!}{\text{product of all hook lengths}}.\] A hook length counts the cell itself, the cells to its right, and the cells below it."),
        ("List the hook lengths", r"For a $3\times3$ square, the hook lengths are \[\begin{matrix}5&4&3\\4&3&2\\3&2&1\end{matrix}.\] Their product is $5\cdot4\cdot3\cdot4\cdot3\cdot2\cdot3\cdot2\cdot1=8640$."),
        ("Divide", r"Since $9!=362880$, the number of valid arrays is \[\frac{362880}{8640}=42.\]"),
        ("Conclude", r"So the number of arrays is $\boxed{42}$."),
    ],
    24: [
        ("Set up the two score sequences", r"Let the Raiders' first-quarter score be $a$. Since the game was tied after the first quarter, the Wildcats also scored $a$ in the first quarter. Suppose the Raiders' geometric sequence has integer ratio $r>1$, so their scores are $a,ar,ar^2,ar^3$. The Wildcats' arithmetic sequence is $a,a+d,a+2d,a+3d$."),
        ("Use the final one-point margin", r"The Raiders won by one point, so \[a(1+r+r^2+r^3)-\bigl(4a+6d\bigr)=1.\] This simplifies to \[a(r+r^2+r^3-3)-6d=1.\]"),
        ("Limit the possible ratio", r"The Raiders scored fewer than $100$ total points, so $a(1+r+r^2+r^3)<100$. Testing integer ratios, $r=2$ is the only small ratio that can satisfy the congruence cleanly. With $r=2$, the equation becomes $11a-6d=1$."),
        ("Solve the score pattern", r"From $11a-6d=1$, we get $11a\equiv1\pmod6$, so $5a\equiv1\pmod6$ and $a\equiv5\pmod6$. Also $15a<100$, so $a=5$. Then $55-6d=1$, giving $d=9$."),
        ("Compute the first-half total", r"The Raiders scored $5+10=15$ in the first half. The Wildcats scored $5+14=19$ in the first half. Together they scored $15+19=34$, so the answer is $\boxed{34}$."),
    ],
    25: [
        ("Use roots at the odd inputs", r"The condition $P(1)=P(3)=P(5)=P(7)=a$ means the polynomial $P(x)-a$ has roots $1,3,5,7$. Because these factors are monic with integer roots, we can write \[P(x)-a=(x-1)(x-3)(x-5)(x-7)Q(x)\] for some polynomial $Q(x)$ with integer coefficients."),
        ("Plug in the even inputs", r"At $x=2,4,6,8$, we have $P(x)=-a$, so $P(x)-a=-2a$. The factor $(x-1)(x-3)(x-5)(x-7)$ takes the values $-15,9,-15,105$ at $x=2,4,6,8$."),
        ("Get a divisibility condition", r"Because $Q$ has integer coefficients, $Q(2),Q(4),Q(6),Q(8)$ are integers. Therefore each of $15,9,15,105$ must divide $2a$. Their least common multiple is $315$, so $315$ divides $2a$. Since $315$ is odd, $315$ must divide $a$."),
        ("Show the lower bound is attainable", r"It remains to know that $a=315$ is possible. One working choice is \[Q(x)=-8x^3+124x^2-576x+762.\] Then $Q(2)=42$, $Q(4)=-70$, $Q(6)=42$, and $Q(8)=-6$, exactly giving $P(x)-a=-630$ at the even inputs when $a=315$."),
        ("Conclude", r"Thus $a$ must be a multiple of $315$, and $315$ can actually occur. The smallest possible value is $\boxed{315}$."),
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
        if r["year"] == "2010" and r["form"] == "B" and int(r["problem_no"]) in TARGET_NUMBERS
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
        + "- Answer verification source: AoPS 2010 AMC 10B Answer Key\n\n"
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




















