import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BATCH_LABEL = "High-risk reviewed problem pages batch 1"
BATCH_NUMBER = 285


PROBLEMS = {
    "2010 AMC 10A Problem 24": {
        "contest_dir": "amc10",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2010_AMC_10A_Answer_Key",
        "answer": ("A", "12"),
        "statement": "The number obtained from the last two nonzero digits of $90!$ is equal to $n$. What is $n$?",
        "choices": [("A", "12"), ("B", "32"), ("C", "48"), ("D", "52"), ("E", "68")],
        "key_idea": "Remove the factors of 10, keep the remaining unit part modulo 100, and then restore the extra powers of 2.",
        "solution": [
            ("Separate trailing zeros from the meaningful last digits",
             "Trailing zeros in $90!$ come from pairs of factors $2\\cdot5$. Since there are far more factors of $2$ than factors of $5$, every factor of $5$ pairs with a factor of $2$ to make a zero.\n\nSo the last two nonzero digits come from removing all factors of $5$, removing the same number of factors of $2$, and then computing the remaining product modulo $100$."),
            ("Count the leftover powers of 2",
             "The number of factors of $5$ in $90!$ is\n\n\\[\\left\\lfloor\\frac{90}{5}\\right\\rfloor+\\left\\lfloor\\frac{90}{25}\\right\\rfloor=18+3=21.\\]\n\nThe number of factors of $2$ is\n\n\\[45+22+11+5+2+1=86.\\]\n\nAfter making the trailing zeros, there are $86-21=65$ extra factors of $2$."),
            ("Compute the odd-and-non-5 part modulo 100",
             "For each factor from $1$ to $90$, remove all factors of $2$ and $5$, then multiply the remaining parts modulo $100$. A controlled block table for $1$-$10$, $11$-$20$, and so on gives block products\n\n\\[67,63,1,61,39,61,9,51,1.\\]\n\nTheir product is\n\n\\[67\\cdot63\\cdot1\\cdot61\\cdot39\\cdot61\\cdot9\\cdot51\\cdot1\\equiv41\\pmod{100}.\\]"),
            ("Restore the leftover powers of 2",
             "The extra factor is $2^{65}$. Powers of $2$ modulo $100$ repeat, and\n\n\\[2^{65}\\equiv32\\pmod{100}.\\]\n\nThus the last two nonzero digits are\n\n\\[41\\cdot32\\equiv12\\pmod{100}.\\]"),
            ("Check the interpretation of the result",
             "The result $12$ already has two digits and is not divisible by $10$, so it is exactly the number formed by the last two nonzero digits. Therefore $n=12$."),
        ],
    },
    "2015 AMC 12B Problem 20": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2015_AMC_12B_Answer_Key",
        "answer": ("B", "1"),
        "statement": "For every positive integer $n$, let $\\operatorname{mod}_5(n)$ be the remainder when $n$ is divided by $5$. Define $f:\\{0,1,2,3,\\ldots\\}\\times\\{0,1,2,3,4\\}\\to\\{0,1,2,3,4\\}$ recursively by\n\n\\[f(0,j)=\\operatorname{mod}_5(j+1),\\]\n\n\\[f(i,0)=f(i-1,1)\\quad\\text{for }i\\ge1,\\]\n\nand\n\n\\[f(i,j)=f(i-1,f(i,j-1))\\quad\\text{for }i\\ge1,\\ 1\\le j\\le4.\\]\n\nWhat is $f(2015,2)$?",
        "choices": [("A", "0"), ("B", "1"), ("C", "2"), ("D", "3"), ("E", "4")],
        "key_idea": "Compute the five-entry row for small values of i until the recursive table stabilizes.",
        "solution": [
            ("Think of each i as a row of five values",
             "For a fixed $i$, define the row\n\n\\[R_i=(f(i,0),f(i,1),f(i,2),f(i,3),f(i,4)).\\]\n\nThe recursion tells us how to build $R_i$ from the previous row $R_{i-1}$. This is much easier than trying to evaluate $f(2015,2)$ directly."),
            ("Start with the row i = 0",
             "The first rule says $f(0,j)$ is the remainder of $j+1$ modulo $5$. Therefore\n\n\\[R_0=(1,2,3,4,0).\\]\n\nThis gives the initial row for the recursion."),
            ("Build the next few rows",
             "Using the recursive rules carefully gives\n\n\\[R_1=(2,3,4,0,1),\\]\n\\[R_2=(3,0,2,4,1),\\]\n\\[R_3=(0,3,4,1,0),\\]\n\\[R_4=(3,1,3,1,3),\\]\n\\[R_5=(1,1,1,1,1).\\]\n\nThe important observation is that we do not need all $2015$ rows if the table stabilizes."),
            ("Notice the stable row",
             "If $R_i=(1,1,1,1,1)$, then the recursion keeps every entry equal to $1$ in the next row. So\n\n\\[R_5=R_6=R_7=\\cdots=(1,1,1,1,1).\\]\n\nSince $2015\\ge5$, the row $R_{2015}$ is also all ones."),
            ("Read the requested entry",
             "The requested value is the third entry of $R_{2015}$, because $j=2$. Hence\n\n\\[f(2015,2)=1.\\]\n\nSo the answer is $1$."),
        ],
    },
    "2020 AMC 12A Problem 19": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2020_AMC_12A_Answer_Key",
        "answer": ("C", "137"),
        "statement": "There exists a unique strictly increasing sequence of nonnegative integers $a_1<a_2<\\cdots<a_k$ such that\n\n\\[\\frac{2^{289}+1}{2^{17}+1}=2^{a_1}+2^{a_2}+\\cdots+2^{a_k}.\\]\n\nWhat is $k$?",
        "choices": [("A", "117"), ("B", "136"), ("C", "137"), ("D", "273"), ("E", "306")],
        "key_idea": "Use the factorization of an odd power sum and then count the ones in the binary representation.",
        "solution": [
            ("Recognize that this is asking for binary ones",
             "Writing a number as\n\n\\[2^{a_1}+2^{a_2}+\\cdots+2^{a_k}\\]\n\nwith strictly increasing exponents is exactly its binary expansion. So $k$ is the number of $1$'s in the binary representation of the fraction."),
            ("Use the odd power factorization",
             "Let $y=2^{17}$. Then $2^{289}=y^{17}$, and\n\n\\[\\frac{2^{289}+1}{2^{17}+1}=\\frac{y^{17}+1}{y+1}.\\]\n\nBecause $17$ is odd,\n\n\\[\\frac{y^{17}+1}{y+1}=y^{16}-y^{15}+y^{14}-\\cdots-y+1.\\]"),
            ("Pair the negative terms with the following positive terms",
             "Rewrite the alternating sum as\n\n\\[1+(y^2-y)+(y^4-y^3)+\\cdots+(y^{16}-y^{15}).\\]\n\nEach paired difference is\n\n\\[y^{2r}-y^{2r-1}=y^{2r-1}(y-1).\\]"),
            ("Interpret each block in binary",
             "Since $y=2^{17}$, we have\n\n\\[y-1=2^{17}-1,\\]\n\nwhich is a block of $17$ ones in binary. Multiplying by $y^{2r-1}=2^{17(2r-1)}$ shifts that block without changing the number of ones."),
            ("Count the non-overlapping blocks",
             "There are $8$ paired differences, and each contributes a block of $17$ ones. These blocks do not overlap because each shift is by multiples of $34$ positions.\n\nThe initial $1$ contributes one more binary one. Therefore\n\n\\[k=8\\cdot17+1=137.\\]"),
        ],
    },
    "2021 Spring AMC 12A Problem 18": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12A_Answer_Key",
        "answer": ("E", r"$\frac{25}{11}$"),
        "statement": "Let $f$ be a function defined on the set of positive rational numbers with the property that $f(a\\cdot b)=f(a)+f(b)$ for all positive rational numbers $a$ and $b$. Suppose also that $f(p)=p$ for every prime number $p$. For which of the following numbers $x$ is $f(x)<0$?",
        "choices": [("A", r"$\frac{17}{32}$"), ("B", r"$\frac{11}{16}$"), ("C", r"$\frac79$"), ("D", r"$\frac76$"), ("E", r"$\frac{25}{11}$")],
        "key_idea": "Use the multiplicative-to-additive rule to evaluate f from prime factorizations.",
        "solution": [
            ("Find what f does to 1 and reciprocals",
             "Using the rule with $a=1$ gives\n\n\\[f(1\\cdot b)=f(1)+f(b).\\]\n\nSo $f(1)=0$. Then for any positive rational $q$,\n\n\\[f(q)+f(1/q)=f(1)=0,\\]\n\nwhich means $f(1/q)=-f(q)$."),
            ("Extend the rule to prime powers",
             "If $p$ is prime, then $f(p)=p$. Repeated multiplication gives\n\n\\[f(p^e)=ef(p)=ep.\\]\n\nFor a rational number, prime factors in the numerator contribute positively, and prime factors in the denominator contribute negatively."),
            ("Evaluate the first four answer choices",
             "Now compute:\n\n\\[f\\left(\\frac{17}{32}\\right)=17-5\\cdot2=7,\\]\n\\[f\\left(\\frac{11}{16}\\right)=11-4\\cdot2=3,\\]\n\\[f\\left(\\frac79\\right)=7-2\\cdot3=1,\\]\n\\[f\\left(\\frac76\\right)=7-2-3=2.\\]\n\nAll four are positive."),
            ("Evaluate the remaining choice",
             "For the last choice,\n\n\\[\\frac{25}{11}=\\frac{5^2}{11}.\\]\n\nTherefore\n\n\\[f\\left(\\frac{25}{11}\\right)=2\\cdot5-11=-1.\\]"),
            ("Choose the only negative value",
             "The only answer choice for which $f(x)<0$ is\n\n\\[x=\\frac{25}{11}.\\]\n\nSo the answer is $\\frac{25}{11}$."),
        ],
    },
    "2021 Spring AMC 12A Problem 19": {
        "contest_dir": "amc12",
        "answer_key_url": "https://artofproblemsolving.com/wiki/index.php/2021_AMC_12A_Answer_Key",
        "answer": ("C", "2"),
        "statement": "How many solutions does the equation\n\n\\[\\sin\\left(\\frac{\\pi}{2}\\cos x\\right)=\\cos\\left(\\frac{\\pi}{2}\\sin x\\right)\\]\n\nhave in the closed interval $[0,\\pi]$?",
        "choices": [("A", "0"), ("B", "1"), ("C", "2"), ("D", "3"), ("E", "4")],
        "key_idea": "Rewrite the cosine as a sine and solve the resulting sine equality in the restricted interval.",
        "solution": [
            ("Convert the right side to a sine",
             "Use $\\cos u=\\sin(\\frac\\pi2-u)$. The equation becomes\n\n\\[\\sin\\left(\\frac\\pi2\\cos x\\right)=\\sin\\left(\\frac\\pi2-\\frac\\pi2\\sin x\\right).\\]\n\nThis puts both sides into the same trig function."),
            ("Use the sine equality cases",
             "If $\\sin A=\\sin B$, then either\n\n\\[A=B+2k\\pi\\]\n\nor\n\n\\[A=\\pi-B+2k\\pi\\]\n\nfor some integer $k$. Here the angles involved are small enough that only the basic cases can occur on $0\\le x\\le\\pi$."),
            ("Solve the first case",
             "The case $A=B$ gives\n\n\\[\\frac\\pi2\\cos x=\\frac\\pi2-\\frac\\pi2\\sin x,\\]\n\nso\n\n\\[\\sin x+\cos x=1.\\]\n\nOn $[0,\\pi]$, this has solutions $x=0$ and $x=\\frac\\pi2$."),
            ("Solve the second case",
             "The case $A=\\pi-B$ gives\n\n\\[\\frac\\pi2\\cos x=\\frac\\pi2+\frac\\pi2\\sin x,\\]\n\nso\n\n\\[\\cos x-\sin x=1.\\]\n\nOn $[0,\\pi]$, this gives only $x=0$, which has already been counted."),
            ("Count distinct solutions",
             "The distinct solutions are\n\n\\[x=0\\quad\\text{and}\\quad x=\\frac\\pi2.\\]\n\nTherefore the equation has $2$ solutions in the interval."),
        ],
    },
}


def esc(value, quote=True):
    return html.escape(str(value), quote=quote)


def slug(source):
    s = source.lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9-]", "", s)
    return re.sub(r"-+", "-", s).strip("-")


def source_from_slug(sl):
    p = sl.split("-")
    if len(p) < 5 or p[-2] != "problem":
        return ""
    form = p[-3]
    if not re.fullmatch(r"(10|12)[ab]", form):
        return ""
    year_words = " ".join(x.capitalize() if not x.isdigit() else x for x in p[:-4])
    return f"{year_words} AMC {form[:-1]}{form[-1].upper()} Problem {p[-1]}"


def aops_problem_url(row):
    year_label = row["year"]
    if year_label == "2021 Spring":
        year_part = "2021"
    elif year_label == "2021 Fall":
        year_part = "2021_Fall"
    else:
        year_part = year_label.replace(" ", "_")
    return f"https://artofproblemsolving.com/wiki/index.php/{year_part}_{row['contest'].replace(' ', '_')}{row['form']}_Problems/Problem_{row['problem_no']}"


def read_rows():
    rows = {}
    for contest_dir in ["amc10", "amc12"]:
        with (ROOT / contest_dir / "all_problems.csv").open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                rows[row["source"]] = row
    return rows


def render_page(row, spec):
    src = row["source"]
    answer_letter, answer_value = spec["answer"]
    tags = "".join(f'<span class="badge">{esc(t)}</span>' for t in (row.get("tags") or "").split(";") if t)
    choices_html = "".join(
        f'<li class="choice {"correct" if key == answer_letter else ""}"><span class="choice-key">{esc(key)}</span><span>{esc(value, False)}</span></li>'
        for key, value in spec["choices"]
    )
    steps = "".join(
        f'<section class="step"><h3>Step {i}: {esc(title)}</h3>'
        + "".join(f'<p>{esc(part.strip(), False)}</p>' for part in re.split(r"\n\s*\n", body) if part.strip())
        + "</section>"
        for i, (title, body) in enumerate(spec["solution"], 1)
    )
    overview_label = row["contest"]
    notes = row.get("notes") or ""
    note_html = f'<section class="section"><h2>Notes</h2><p>{esc(notes)}</p></section>' if notes else ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(src)} - STEMHUB AMC</title><style>:root{{--bg:#f7f4ee;--panel:#fff;--ink:#1e2832;--line:#d8ddd8;--blue:#2166a5;--chip:#eef3f7}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,"Segoe UI",Arial,sans-serif}}.site-nav{{display:flex;justify-content:space-between;gap:16px;background:#10283d;color:#fff;padding:10px clamp(18px,4vw,32px)}}.site-brand,.site-links a{{color:#fff;text-decoration:none}}.site-links{{display:flex;flex-wrap:wrap;gap:8px}}.site-links a{{border:1px solid rgba(255,255,255,.18);border-radius:6px;padding:7px 10px}}main{{width:min(1000px,calc(100% - 36px));margin:0 auto;padding:28px 0 48px}}.back{{display:inline-flex;padding:8px 12px;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--blue);text-decoration:none;font-weight:700}}h1{{font-size:clamp(28px,4vw,40px)}}.meta{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px}}.badge{{display:inline-flex;min-height:24px;padding:3px 8px;border-radius:999px;background:var(--chip);font-size:12px}}.badge.major{{background:#e8f0dc;color:#35592f}}.section{{background:#fff;border:1px solid var(--line);border-radius:8px;padding:18px;margin-top:14px}}.statement{{font-size:18px;line-height:1.65}}.choices{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}.choice{{display:grid;grid-template-columns:38px 1fr;gap:10px;border:1px solid var(--line);border-radius:6px;padding:8px 10px}}.choice.correct{{border-color:#abc8a6;background:#f1f8ef}}.choice-key{{display:grid;place-items:center;width:28px;height:28px;border-radius:999px;background:#e8f0dc;font-weight:750}}.answer{{padding:6px 10px;border-radius:6px;background:#eef6f1;color:#315c34;font-weight:750}}.step{{border-left:3px solid var(--blue);padding-left:14px;margin-top:16px}}.step h3{{font-size:16px}}.step p,.section p{{line-height:1.65;color:#33414e}}</style><!-- STEMHUB I18N ASSETS --><link rel="stylesheet" href="../../../assets/language-switcher.css?v=20260714" data-stemhub-i18n-assets><script defer src="../../../assets/i18n-dictionary.js?v=20260714" data-stemhub-i18n-assets></script><script defer src="../../../assets/language-switcher.js?v=20260714" data-stemhub-i18n-assets></script><!-- /STEMHUB I18N ASSETS --><script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\(','\\)']],displayMath:[['\\\\[','\\\\]']]}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script></head><body><nav class="site-nav"><a class="site-brand" href="../../../">STEMHUB AMC</a><div class="site-links"><a href="../../../">Home</a><a href="../../../amc10/">AMC 10</a><a href="../../../amc12/">AMC 12</a><a href="../../">Back to Overview</a></div></nav><main><a class="back" href="../../">Back to {overview_label} Overview</a><h1>{esc(src)}</h1><div class="meta"><span class="badge">{row['year']}</span><span class="badge">{row['contest']}{row['form']}</span><span class="badge">Problem {row['problem_no']}</span><span class="badge major">{esc(row['major_category'])}</span><span class="badge">{esc(row['minor_category'])}</span>{tags}</div><section class="section"><h2>Problem Statement</h2><p class="statement">{esc(spec['statement'], False)}</p></section><section class="section"><h2>Choices</h2><ol class="choices">{choices_html}</ol></section><section class="section"><h2>Answer</h2><span class="answer">{answer_letter}. {esc(answer_value, False)}</span></section><section class="section"><h2>Solution</h2>{steps}</section><section class="section"><h2>Key Idea</h2><p>{esc(spec['key_idea'])}</p></section>{note_html}<section class="section references"><h2>Reference</h2><p>Answer verified with <a href="{spec['answer_key_url']}">AoPS Answer Key</a>. Related page: <a href="{aops_problem_url(row)}">AoPS problem page</a>.</p></section></main></body></html>'''


def update_index(contest_dir):
    path = ROOT / contest_dir / "index.html"
    text = path.read_text(encoding="utf-8")
    mapping = {}
    for page in (ROOT / contest_dir / "problems").glob("*/index.html"):
        src = source_from_slug(page.parent.name)
        if src:
            mapping[src] = f"problems/{page.parent.name}/"
    pairs = ", ".join(
        f"[{json.dumps(k, ensure_ascii=False)}, {json.dumps(v, ensure_ascii=False)}]"
        for k, v in sorted(mapping.items())
    )
    text = re.sub(r"const detailPages = new Map\(\[[\s\S]*?\]\);", f"const detailPages = new Map([{pairs}]);", text, count=1)
    path.write_text(text, encoding="utf-8")


def validate(items):
    errors = []
    for item in items:
        page = Path(item["output_path"])
        if not page.exists():
            errors.append(f"missing page {page}")
            continue
        html_text = page.read_text(encoding="utf-8")
        main = html_text.split("<main>", 1)[1].split("</main>", 1)[0]
        if "displayMath:[['\\\\[','\\\\]']]" not in html_text:
            errors.append(f"{item['source']} bad MathJax config")
        if "\\\\[" in main or "\\\\]" in main:
            errors.append(f"{item['source']} double display delimiter in body")
        if html_text.count('<section class="step">') < 4:
            errors.append(f"{item['source']} fewer than 4 steps")
        if "AoPS Answer Key" not in html_text:
            errors.append(f"{item['source']} missing AoPS reference")
        idx = (ROOT / item["contest_dir"] / "index.html").read_text(encoding="utf-8")
        if item["source"] not in idx:
            errors.append(f"{item['source']} missing from overview detail map")
    if errors:
        raise RuntimeError("\n".join(errors))


def update_manifest(items):
    path = ROOT / "problem_pages_manifest.json"
    existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    by_source = {row["source"]: row for row in existing if row.get("source")}
    for item in items:
        by_source[item["source"]] = {k: v for k, v in item.items() if k != "contest_dir"}
    merged = sorted(by_source.values(), key=lambda row: row["source"])
    path.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(merged)


def update_progress_and_report(items, skipped):
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    pages = "\n".join(f"- `{item['source']}` -> `{item['contest_dir']}/problems/{item['slug']}/`" for item in items)
    progress = ROOT / "problem_pages_progress.md"
    old = progress.read_text(encoding="utf-8").rstrip() + "\n\n"
    progress.write_text(
        old
        + f"## {BATCH_LABEL}\n\n"
        + f"- Time: {now}\n"
        + f"- Generated count: {len(items)}\n"
        + f"- Skipped count: {len(skipped)}\n"
        + ("- Skipped reasons: " + "; ".join(skipped) + "\n" if skipped else "- Skipped reasons: none\n")
        + "- Validation result: passed\n"
        + "- Commit hash: pending\n"
        + "- Pushed: pending\n",
        encoding="utf-8",
    )
    (ROOT / "problem_pages_report.md").write_text(
        "# Problem Pages Report\n\n"
        + f"- Latest reviewed batch: {BATCH_LABEL}\n"
        + f"- Generated count: {len(items)}\n"
        + f"- Skipped count: {len(skipped)}\n"
        + "- MathJax validation: passed\n\n"
        + "## Latest Reviewed Pages\n\n"
        + pages
        + ("\n\n## Skipped\n\n" + "\n".join(f"- {s}" for s in skipped) if skipped else ""),
        encoding="utf-8",
    )
    (ROOT / "resume_prompt.md").write_text(
        "请继续 STEMHUB AMC problem teaching pages 补完阶段。\n\n"
        + f"当前状态：{BATCH_LABEL} 已生成并通过本地验证；已生成 {len(items)} 道 high-risk reviewed pages。\n"
        + "下一步：重新查看 `missing_problem_triage.md`，继续从 `solution_high_risk` 中挑 3-5 道非图形、非 OCR、答案可确认的题逐题精修。\n",
        encoding="utf-8",
    )


def main():
    rows = read_rows()
    items = []
    skipped = list(globals().get("REVIEW_SKIPPED", []))
    for source, spec in PROBLEMS.items():
        row = rows.get(source)
        if not row:
            skipped.append(f"{source}: missing from all_problems.csv")
            continue
        contest_dir = spec["contest_dir"]
        sl = slug(source)
        out_dir = ROOT / contest_dir / "problems" / sl
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(render_page(row, spec), encoding="utf-8")
        answer_letter, answer_value = spec["answer"]
        items.append({
            "contest": row["contest"],
            "year": row["year"],
            "form": row["form"],
            "problem_no": row["problem_no"],
            "source": source,
            "slug": sl,
            "output_path": str(out_dir / "index.html"),
            "relative_url": f"problems/{sl}/",
            "aops_url": aops_problem_url(row),
            "aops_answer_key_url": spec["answer_key_url"],
            "aops_verified": True,
            "answer": f"{answer_letter}. {answer_value}",
            "has_answer": True,
            "has_choices": True,
            "has_solution": True,
            "needs_review": True,
            "batch_number": BATCH_NUMBER,
            "review_batch": BATCH_LABEL,
            "contest_dir": contest_dir,
        })

    update_index("amc10")
    update_index("amc12")
    validate(items)
    manifest_count = update_manifest(items)
    update_progress_and_report(items, skipped)
    print(json.dumps({"generated": len(items), "skipped": skipped, "manifest_total": manifest_count}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
