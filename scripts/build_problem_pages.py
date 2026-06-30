from __future__ import annotations

import csv
import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(r"D:\STEMHUB_AMC")

ANSWER_KEYS = {
    "2024 AMC 10B Problem 1": ("B", "2022"),
    "2024 AMC 10B Problem 2": ("B", "0"),
    "2024 AMC 10B Problem 3": ("E", "21"),
    "2024 AMC 10B Problem 4": ("D", "D"),
    "2024 AMC 10B Problem 5": ("B", "15"),
    "2024 AMC 12B Problem 1": ("B", "2022"),
    "2024 AMC 12B Problem 2": ("B", "0"),
    "2024 AMC 12B Problem 3": ("E", "21"),
    "2024 AMC 12B Problem 4": ("D", "D"),
    "2024 AMC 12B Problem 5": ("B", "15"),
}

# AoPS answer-key pages used only to verify final answer letters.
AOPS_ANSWER_KEY_URLS = {
    "AMC 10": "https://artofproblemsolving.com/wiki/index.php/2024_AMC_10B_Answer_Key",
    "AMC 12": "https://artofproblemsolving.com/wiki/index.php/2024_AMC_12B_Answer_Key",
}

SAMPLES = [
    "2024 AMC 10B Problem 1",
    "2024 AMC 10B Problem 2",
    "2024 AMC 10B Problem 3",
    "2024 AMC 10B Problem 4",
    "2024 AMC 10B Problem 5",
    "2024 AMC 12B Problem 1",
    "2024 AMC 12B Problem 2",
    "2024 AMC 12B Problem 3",
    "2024 AMC 12B Problem 4",
    "2024 AMC 12B Problem 5",
]

CANONICAL_STATEMENTS = {
    "2024 AMC 10B Problem 1": "In a long line of people, the 1013th person from the left is also the 1010th person from the right. How many people are in the line?",
    "2024 AMC 10B Problem 2": "What is $10! - 7! \\cdot 6!$?",
    "2024 AMC 10B Problem 3": "For how many integer values of $x$ is $|2x| \\le 7\\pi$?",
    "2024 AMC 10B Problem 4": "Balls numbered $1,2,3,\\ldots$ are deposited in $5$ bins, labeled A, B, C, D, and E, using blocks of sizes $1,2,3,4,\\ldots$ cyclically through the bins. In which bin is ball $2024$ deposited?",
    "2024 AMC 10B Problem 5": "In the expression $1+3+5+\\cdots+97+99$, Melanie changes some plus signs to minus signs. The new expression is negative. What is the least number of plus signs she could have changed?",
    "2024 AMC 12B Problem 1": "In a long line of people, the 1013th person from the left is also the 1010th person from the right. How many people are in the line?",
    "2024 AMC 12B Problem 2": "What is $10! - 7! \\cdot 6!$?",
    "2024 AMC 12B Problem 3": "For how many integer values of $x$ is $|2x| \\le 7\\pi$?",
    "2024 AMC 12B Problem 4": "Balls numbered $1,2,3,\\ldots$ are deposited in $5$ bins, labeled A, B, C, D, and E, using blocks of sizes $1,2,3,4,\\ldots$ cyclically through the bins. In which bin is ball $2024$ deposited?",
    "2024 AMC 12B Problem 5": "In $1+3+5+\\cdots+97+99$, Melanie changes some plus signs to minus signs. The new expression is negative. What is the least number of plus signs changed?",
}

CHOICES = {
    "2024 AMC 10B Problem 1": [("A", "2021"), ("B", "2022"), ("C", "2023"), ("D", "2024"), ("E", "2025")],
    "2024 AMC 10B Problem 2": [("A", "$-120$"), ("B", "$0$"), ("C", "$120$"), ("D", "$600$"), ("E", "$720$")],
    "2024 AMC 10B Problem 3": [("A", "16"), ("B", "17"), ("C", "19"), ("D", "20"), ("E", "21")],
    "2024 AMC 10B Problem 4": [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"), ("E", "E")],
    "2024 AMC 10B Problem 5": [("A", "14"), ("B", "15"), ("C", "16"), ("D", "17"), ("E", "18")],
}
for n in range(1, 6):
    CHOICES[f"2024 AMC 12B Problem {n}"] = CHOICES[f"2024 AMC 10B Problem {n}"]

SOLUTIONS = {
    "2024 AMC 10B Problem 1": [
        (
            "Read the position information carefully",
            r"""The sentence gives the same person's position from both ends of the line. From the left, this person is number $1013$; from the right, this person is number $1010$. A common mistake is to add these two numbers directly, but that counts the person twice.""",
        ),
        (
            "Translate positions into people on each side",
            r"""If someone is the $1013$th person from the left, then there are $1013-1=1012$ people before them. If the same person is the $1010$th person from the right, then there are $1010-1=1009$ people after them. This turns the wording into a simple picture: left side, the person, right side.""",
        ),
        (
            "Count the whole line once",
            r"""Now count each part exactly once. The total number of people is $1012$ on the left, plus the chosen person, plus $1009$ on the right. Therefore
\[
1012+1+1009=2022.
\]""",
        ),
        (
            "Check why the answer is reasonable",
            r"""The answer should be a little more than $2000$, because the two given positions are about $1000$ from each side. The value $2022$ matches that expectation and avoids double-counting the middle person. Thus the answer is $\boxed{2022}$.""",
        ),
    ],
    "2024 AMC 10B Problem 2": [
        (
            "Notice the shared factorial structure",
            r"""The expression $10!-7!\cdot 6!$ looks large, but AMC problems often become simple after factoring. Since one term already contains $7!$, it is natural to rewrite $10!$ in terms of $7!$ instead of evaluating both factorials fully.""",
        ),
        (
            "Rewrite $10!$ using $7!$",
            r"""Break off the factors above $7$:
\[
10! = 10\cdot 9\cdot 8\cdot 7!.
\]
This is useful because the second term is also built from $7!$.""",
        ),
        (
            "Recognize the remaining product",
            r"""The product $10\cdot 9\cdot 8$ equals $720$, and $6!=720$. So we can rewrite
\[
10! = 6!\cdot 7!.
\]
At this point the two terms are actually identical.""",
        ),
        (
            "Subtract identical quantities",
            r"""Now the expression becomes
\[
10!-7!\cdot 6! = 6!\cdot 7!-7!\cdot 6! = 0.
\]
The important idea is not big computation; it is choosing the right factorization.""",
        ),
        (
            "Confirm the answer choice",
            r"""Since the expression is exactly zero, not just approximately small, the correct answer is $\boxed{0}$.""",
        ),
    ],
    "2024 AMC 10B Problem 3": [
        (
            "Identify what is being counted",
            r"""The problem asks for the number of integer values of $x$, not for a range length. So after solving the inequality, we must count integers carefully, including both negative and positive values.""",
        ),
        (
            "Isolate $x$ inside the absolute value inequality",
            r"""The inequality is
\[
|2x|\le 7\pi.
\]
Because $|2x|=2|x|$, divide both sides by $2$ to get
\[
|x|\le \frac{7\pi}{2}.
\]
This means $x$ must lie between $-\frac{7\pi}{2}$ and $\frac{7\pi}{2}$.""",
        ),
        (
            "Estimate the boundary without overdoing decimals",
            r"""We only need to know which integers fit. Since $\pi$ is a little more than $3$, $\frac{7\pi}{2}$ is a little more than $\frac{21}{2}=10.5$. Since $\pi<\frac{22}{7}$, we also have $\frac{7\pi}{2}<11$. So the cutoff is between $10.5$ and $11$.""",
        ),
        (
            "List the possible integers in a structured way",
            r"""Because the cutoff is greater than $10$ but less than $11$, the allowed integers are
\[
-10,-9,\ldots,-1,0,1,\ldots,9,10.
\]
That is $10$ negative integers, $0$, and $10$ positive integers.""",
        ),
        (
            "Count and check the endpoints",
            r"""The total number of integers is $10+1+10=21$. The endpoint $11$ is not allowed because the cutoff is less than $11$, while $10$ is allowed because the cutoff is greater than $10$. Therefore the answer is $\boxed{21}$.""",
        ),
    ],
    "2024 AMC 10B Problem 4": [
        (
            "Understand the deposit pattern",
            r"""The balls are not placed one at a time into consecutive bins. Instead, the process uses blocks: first $1$ ball, then $2$ balls, then $3$ balls, and so on. The bins cycle by block, not by individual ball, so the main task is to find which block contains ball $2024$.""",
        ),
        (
            "Use triangular numbers to locate the block",
            r"""After block $n$, the total number of deposited balls is
\[
1+2+\cdots+n=\frac{n(n+1)}{2}.
\]
This formula helps us avoid listing hundreds of blocks.""",
        ),
        (
            "Find the block containing ball $2024$",
            r"""Compute nearby triangular numbers:
\[
T_{63}=\frac{63\cdot64}{2}=2016, \qquad T_{64}=\frac{64\cdot65}{2}=2080.
\]
Since $2016<2024\le 2080$, ball $2024$ is placed during block $64$.""",
        ),
        (
            "Convert the block number into a bin",
            r"""The bins repeat in the order A, B, C, D, E. Block $1$ goes to A, block $2$ to B, and so on. Since the pattern has length $5$, reduce the block number modulo $5$:
\[
64\equiv 4\pmod 5.
\]
The fourth bin in the cycle is D.""",
        ),
        (
            "Check that the reasoning matches the process",
            r"""We found the block first and only then chose the bin, which is important because every ball in block $64$ goes into the same bin. Therefore ball $2024$ is deposited in bin $\boxed{D}$.""",
        ),
    ],
    "2024 AMC 10B Problem 5": [
        (
            "Start with the original sum",
            r"""The expression adds all positive odd numbers from $1$ to $99$. There are $50$ such numbers, and the sum of the first $50$ positive odd numbers is
\[
1+3+5+\cdots+99=50^2=2500.
\]
So before any signs are changed, the expression is quite positive.""",
        ),
        (
            "Understand what changing one sign does",
            r"""If a term $k$ changes from $+k$ to $-k$, the value of the expression decreases by $2k$, not just by $k$. For example, changing $+99$ to $-99$ changes the total by $198$. To make the total negative using as few sign changes as possible, we should change the largest odd numbers first.""",
        ),
        (
            "Set up the target decrease",
            r"""To make the new expression negative, the total decrease must be more than $2500$. If the changed odd numbers have sum $S$, then the decrease is $2S$. Therefore we need
\[
2S>2500, \qquad \text{so} \qquad S>1250.
\]
Now the problem becomes: how few of the largest odd numbers can have sum greater than $1250$?""",
        ),
        (
            "Test the largest possible groups",
            r"""The largest $14$ odd numbers are $73,75,\ldots,99$. Their average is $\frac{73+99}{2}=86$, so their sum is $14\cdot86=1204$. This is not enough, because $1204<1250$.""",
        ),
        (
            "Add one more term and finish",
            r"""If we also include the next largest odd number, $71$, the sum becomes
\[
1204+71=1275>1250.
\]
So $15$ sign changes are enough, while $14$ are not enough even in the best possible case. Therefore the least number of plus signs changed is $\boxed{15}$.""",
        ),
    ],
}
for n in range(1, 6):
    SOLUTIONS[f"2024 AMC 12B Problem {n}"] = SOLUTIONS[f"2024 AMC 10B Problem {n}"]

KEY_IDEA_EN = {
    "2024 AMC 10B Problem 1": "Use position counting and subtract the person counted from both sides once.",
    "2024 AMC 10B Problem 2": "Factor factorials so both terms have the same product.",
    "2024 AMC 10B Problem 3": "Convert the absolute value inequality into an interval for integer values.",
    "2024 AMC 10B Problem 4": "Use triangular numbers to locate the block containing the target ball, then reduce the block number modulo $5$.",
    "2024 AMC 10B Problem 5": "Use the sum of odd numbers and choose the largest terms greedily to minimize the number of sign changes.",
}
for n in range(1, 6):
    KEY_IDEA_EN[f"2024 AMC 12B Problem {n}"] = KEY_IDEA_EN[f"2024 AMC 10B Problem {n}"]


def slugify_source(source: str) -> str:
    s = source.lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def aops_problem_url(row: dict[str, str]) -> str:
    year = row["year"]
    contest = row["contest"].replace(" ", "_")
    form = row["form"]
    no = row["problem_no"]
    if "Spring" in year:
        year_part = year.replace(" ", "_")
    elif "Fall" in year:
        year_part = year.replace(" ", "_")
    else:
        year_part = year
    return f"https://artofproblemsolving.com/wiki/index.php/{year_part}_{contest}{form}_Problems/Problem_{no}"


def read_rows(contest_dir: str) -> list[dict[str, str]]:
    path = ROOT / contest_dir / "all_problems.csv"
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_samples() -> list[dict[str, str]]:
    by_source: dict[str, dict[str, str]] = {}
    for contest_dir in ("amc10", "amc12"):
        for row in read_rows(contest_dir):
            row["contest_dir"] = contest_dir
            by_source[row["source"]] = row
    return [by_source[source] for source in SAMPLES]


def split_choices_from_statement(statement: str):
    pattern = re.compile(r"\s*\(([A-E])\)\s*")
    matches = list(pattern.finditer(statement))
    if len(matches) < 5:
        return statement.strip(), []
    stem = statement[: matches[0].start()].strip()
    choices = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(statement)
        choices.append((m.group(1), statement[start:end].strip()))
    return stem, choices


def normalize_notes(notes: str) -> str:
    if not notes:
        return ""
    if "图" in notes or "figure" in notes.lower() or "diagram" in notes.lower():
        return "This problem contains a diagram. Please refer to the original PDF or AoPS page."
    return notes


def html_text(value: str) -> str:
    return html.escape(value, quote=True)


def render_math_text(value: str) -> str:
    # Keep curated LaTeX intact. Escape HTML only.
    return html.escape(value, quote=False)


def render_detail_page(row: dict[str, str]) -> str:
    source = row["source"]
    contest_dir = row["contest_dir"]
    contest_label = "AMC 10" if contest_dir == "amc10" else "AMC 12"
    answer_letter, answer_value = ANSWER_KEYS[source]
    statement = CANONICAL_STATEMENTS.get(source, row["statement"])
    stem, parsed_choices = split_choices_from_statement(statement)
    choices = CHOICES.get(source) or parsed_choices
    answer_display = f"{answer_letter}. {answer_value}"
    tags = [t for t in row.get("tags", "").split(";") if t]
    notes = normalize_notes(row.get("notes", ""))
    aops_url = aops_problem_url(row)
    answer_key_url = AOPS_ANSWER_KEY_URLS[row["contest"]]
    key_idea = KEY_IDEA_EN.get(source, row.get("key_idea", ""))
    solution_steps = SOLUTIONS[source]

    choices_html = "\n".join(
        f'<li class="choice {"correct" if key == answer_letter else ""}"><span class="choice-key">{html_text(key)}</span><span>{render_math_text(text)}</span></li>'
        for key, text in choices
    ) or '<li class="choice"><span>Choices to be organized.</span></li>'
    tags_html = "".join(f'<span class="badge">{html_text(t)}</span>' for t in tags)
    notes_html = f'<section class="section"><h2>Notes</h2><p>{html_text(notes)}</p></section>' if notes else ""
    def render_step(i: int, step) -> str:
        if isinstance(step, dict):
            title = str(step.get("title", "")).strip()
            body = str(step.get("body", "")).strip()
        elif isinstance(step, (list, tuple)) and len(step) == 2:
            title = str(step[0]).strip()
            body = str(step[1]).strip()
        else:
            title = ""
            body = str(step).strip()
        heading = f"Step {i}: {title}" if title else f"Step {i}"
        paragraphs = "".join(
            f"<p>{render_math_text(part.strip())}</p>"
            for part in re.split(r"\n\s*\n", body)
            if part.strip()
        )
        return f'<section class="step"><h3>{html_text(heading)}</h3>{paragraphs}</section>'

    steps_html = "\n".join(render_step(i, step) for i, step in enumerate(solution_steps, 1))

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html_text(source)} - STEMHUB AMC</title>
  <style>
    :root {{ --bg:#f7f4ee; --panel:#fff; --ink:#1e2832; --muted:#66727f; --line:#d8ddd8; --blue:#2166a5; --green:#4f7d48; --chip:#eef3f7; --navy:#17324a; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:Inter,"Segoe UI",Arial,sans-serif; }}
    .site-nav {{ display:flex; justify-content:space-between; align-items:center; gap:16px; background:#10283d; color:#fff; padding:10px clamp(18px,4vw,32px); border-bottom:1px solid rgba(255,255,255,.12); }}
    .site-brand {{ font-weight:800; color:#fff; text-decoration:none; white-space:nowrap; }}
    .site-links {{ display:flex; flex-wrap:wrap; gap:8px; }}
    .site-links a {{ color:#d7e4ef; text-decoration:none; border:1px solid rgba(255,255,255,.18); border-radius:6px; padding:7px 10px; min-height:34px; display:inline-flex; align-items:center; }}
    main {{ width:min(1000px, calc(100% - 36px)); margin:0 auto; padding:28px 0 48px; }}
    .back {{ display:inline-flex; align-items:center; min-height:38px; padding:8px 12px; border:1px solid var(--line); border-radius:6px; background:#fff; color:var(--blue); text-decoration:none; font-weight:700; }}
    h1 {{ margin:22px 0 12px; font-size:clamp(28px,4vw,40px); line-height:1.2; letter-spacing:0; }}
    .meta {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:18px; }}
    .badge {{ display:inline-flex; min-height:24px; padding:3px 8px; border-radius:999px; background:var(--chip); font-size:12px; }}
    .badge.major {{ background:#e8f0dc; color:#35592f; }}
    .section {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:18px; margin-top:14px; }}
    .section h2 {{ margin:0 0 12px; font-size:19px; line-height:1.25; }}
    .statement {{ font-size:18px; line-height:1.65; margin:0; }}
    .choices {{ list-style:none; margin:0; padding:0; display:grid; gap:8px; }}
    .choice {{ display:grid; grid-template-columns:38px minmax(0,1fr); gap:10px; align-items:center; min-height:42px; border:1px solid var(--line); border-radius:6px; padding:8px 10px; background:#fbfcfb; }}
    .choice.correct {{ border-color:#abc8a6; background:#f1f8ef; }}
    .choice-key {{ display:inline-grid; place-items:center; width:28px; height:28px; border-radius:999px; background:#e8f0dc; color:#35592f; font-weight:750; }}
    .answer {{ display:inline-flex; min-height:34px; align-items:center; padding:6px 10px; border-radius:6px; background:#eef6f1; color:#315c34; font-weight:750; }}
    .step {{ border-left:3px solid var(--blue); padding:0 0 0 14px; margin-top:16px; }}
    .step:first-child {{ margin-top:0; }}
    .step h3 {{ margin:0 0 6px; font-size:16px; }}
    .step p,.section p {{ margin:0; color:#33414e; line-height:1.65; }}
    .references a {{ color:var(--blue); font-weight:700; }}
    @media (max-width:700px) {{ .site-nav {{ align-items:flex-start; flex-direction:column; }} .site-links {{ width:100%; }} .site-links a {{ flex:1 1 auto; justify-content:center; }} main {{ width:min(100% - 28px, 980px); padding-top:18px; }} .statement {{ font-size:16px; }} }}
  </style>
  <script>
    window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']] }} }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <nav class="site-nav" aria-label="Site navigation">
    <a class="site-brand" href="../../../">STEMHUB AMC</a>
    <div class="site-links">
      <a href="../../../">Home</a>
      <a href="../../../amc10/">AMC 10</a>
      <a href="../../../amc12/">AMC 12</a>
      <a href="../../">Back to Overview</a>
    </div>
  </nav>
  <main>
    <a class="back" href="../../">Back to {contest_label} Overview</a>
    <h1>{html_text(source)}</h1>
    <div class="meta" aria-label="Problem metadata">
      <span class="badge">{html_text(row['year'])}</span>
      <span class="badge">{html_text(row['contest'])}{html_text(row['form'])}</span>
      <span class="badge">Problem {html_text(row['problem_no'])}</span>
      <span class="badge major">{html_text(row['major_category'])}</span>
      <span class="badge">{html_text(row['minor_category'])}</span>
      {tags_html}
    </div>

    <section class="section">
      <h2>Problem Statement</h2>
      <p class="statement">{render_math_text(stem)}</p>
    </section>

    <section class="section">
      <h2>Choices</h2>
      <ol class="choices">
        {choices_html}
      </ol>
    </section>

    <section class="section">
      <h2>Answer</h2>
      <span class="answer">{html_text(answer_display)}</span>
    </section>

    <section class="section">
      <h2>Solution</h2>
      {steps_html}
    </section>

    <section class="section">
      <h2>Key Idea</h2>
      <p>{render_math_text(key_idea)}</p>
    </section>

    {notes_html}

    <section class="section references">
      <h2>Reference</h2>
      <p>Answer verified with <a href="{html_text(answer_key_url)}">AoPS Answer Key</a>. Related page: <a href="{html_text(aops_url)}">AoPS problem page</a>.</p>
    </section>
  </main>
</body>
</html>
'''


def write_pages(samples: list[dict[str, str]]) -> list[dict[str, object]]:
    manifest = []
    for row in samples:
        source = row["source"]
        slug = slugify_source(source)
        out_dir = ROOT / row["contest_dir"] / "problems" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(render_detail_page(row), encoding="utf-8")
        letter, value = ANSWER_KEYS[source]
        manifest.append({
            "contest": row["contest"],
            "year": row["year"],
            "form": row["form"],
            "problem_no": row["problem_no"],
            "source": source,
            "slug": slug,
            "output_path": str(out_dir / "index.html"),
            "relative_url": f"problems/{slug}/",
            "aops_url": aops_problem_url(row),
            "aops_answer_key_url": AOPS_ANSWER_KEY_URLS[row["contest"]],
            "aops_verified": True,
            "answer": f"{letter}. {value}",
            "has_answer": True,
            "has_choices": bool(CHOICES.get(source)),
            "has_solution": True,
            "needs_review": False,
            "sample_round": True,
        })
    return manifest


def source_from_slug(slug: str) -> str:
    parts = slug.split("-")
    if len(parts) < 5 or parts[-2] != "problem":
        return ""
    no = parts[-1]
    form_token = parts[-3]
    if not re.fullmatch(r"(10|12)[ab]", form_token):
        return ""
    contest_no = form_token[:-1]
    form = form_token[-1].upper()
    year_parts = parts[:-4]
    year = " ".join(part.capitalize() if not part.isdigit() else part for part in year_parts)
    return f"{year} AMC {contest_no}{form} Problem {no}"


def update_index(contest_dir: str, manifest: list[dict[str, object]]) -> None:
    path = ROOT / contest_dir / "index.html"
    text = path.read_text(encoding="utf-8")
    contest_name = "AMC 10" if contest_dir == "amc10" else "AMC 12"

    entry_map: dict[str, str] = {}
    problems_dir = ROOT / contest_dir / "problems"
    if problems_dir.exists():
        for child in sorted(problems_dir.iterdir()):
            if child.is_dir() and (child / "index.html").exists():
                source = source_from_slug(child.name)
                if source:
                    entry_map[source] = f"problems/{child.name}/"

    for m in manifest:
        if m["contest"] == contest_name:
            entry_map[str(m["source"])] = str(m["relative_url"])

    pairs = ", ".join(
        f"[{json.dumps(source, ensure_ascii=False)}, {json.dumps(url, ensure_ascii=False)}]"
        for source, url in sorted(entry_map.items())
    )
    map_code = f"const detailPages = new Map([{pairs}]);"
    if "const detailPages = new Map" in text:
        text = re.sub(r"const detailPages = new Map\(\[[\s\S]*?\]\);", map_code, text, count=1)
    else:
        text = text.replace('    const yearOrder = ', f'    {map_code}\n    const yearOrder = ', 1)

    if "function detailHref" not in text:
        text = text.replace(
            "    function fill(select, values, current = select.value) {",
            "    function detailHref(p) {\n      return detailPages.get(p.source) || \"\";\n    }\n    function fill(select, values, current = select.value) {",
            1,
        )

    render_block = '''cards.innerHTML = shown.map(p => {
        const href = detailHref(p);
        const cardBody = `
          <div class="top">
            <div class="source">${esc(p.source)}</div>
            <span class="badge">${esc(p.year)}</span>
            <span class="badge">${esc(p.form)}卷</span>
            <span class="badge major">${esc(p.major_category)}</span>
            <span class="badge">${esc(p.minor_category)}</span>
          </div>
          <div class="statement">${esc(p.statement)}</div>
          <div class="idea">${esc(p.key_idea)}${p.notes ? `<br><strong>备注：</strong>${esc(p.notes)}` : ""}</div>
          <div>${String(p.tags).split(";").map(t => `<span class="badge">${esc(t)}</span>`).join(" ")}</div>
        `;
        return href
          ? `<a class="card problem-link" href="${esc(href)}" aria-label="View details for ${esc(p.source)}">${cardBody}<div class="detail-cta">View details</div></a>`
          : `<article class="card">${cardBody}</article>`;
      }).join("");'''
    text = re.sub(r"cards\.innerHTML = shown\.map\(p => \{[\s\S]*?\n      \}\)\.join\(\"\"\);", render_block, text, count=1)

    if ".problem-link" not in text:
        text = text.replace(
            "    .card { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:15px; display:grid; gap:10px; }",
            "    .card { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:15px; display:grid; gap:10px; }\n    .problem-link { color:inherit; text-decoration:none; transition:border-color .15s ease, box-shadow .15s ease, transform .15s ease; }\n    .problem-link:hover { border-color:var(--blue); box-shadow:0 8px 20px rgba(23,50,74,.12); transform:translateY(-1px); }\n    .detail-cta { color:var(--blue); font-weight:750; font-size:13px; }",
            1,
        )

    path.write_text(text, encoding="utf-8")

def validate_generated_mathjax(manifest: list[dict[str, object]]) -> None:
    failures: list[str] = []
    for item in manifest:
        page = Path(str(item["output_path"]))
        text = page.read_text(encoding="utf-8")
        main = text.split("<main>", 1)[1].split("</main>", 1)[0] if "<main>" in text else text
        if "displayMath: [['\\\\[', '\\\\]']]" not in text:
            failures.append(f"{page}: MathJax displayMath config is not escaped for JavaScript strings")
        if "\\\\[" in main or "\\\\]" in main:
            failures.append(f"{page}: body contains double-escaped display math delimiters")
        if "\\[" in main and "\\]" not in main:
            failures.append(f"{page}: body has unmatched display math opening delimiter")
        if "\\]" in main and "\\[" not in main:
            failures.append(f"{page}: body has unmatched display math closing delimiter")
        if "\\frac" in main and "\\boxed" not in main:
            failures.append(f"{page}: expected boxed answer marker is missing")
    if failures:
        raise RuntimeError("Generated MathJax validation failed:\n" + "\n".join(failures))

def write_reports(manifest: list[dict[str, object]]) -> None:
    (ROOT / "problem_pages_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Problem Pages Report",
        "",
        "First sample round: 10 per-problem detail pages with expanded English teaching solutions and LaTeX.",
        "",
        f"- Total sample pages: {len(manifest)}",
        f"- AMC 10 sample pages: {sum(1 for m in manifest if m['contest'] == 'AMC 10')}",
        f"- AMC 12 sample pages: {sum(1 for m in manifest if m['contest'] == 'AMC 12')}",
        f"- AoPS answer-key verified: {sum(1 for m in manifest if m['aops_verified'])}",
        f"- Pages with choices: {sum(1 for m in manifest if m['has_choices'])}",
        f"- Pages with expanded teaching solutions: {sum(1 for m in manifest if m['has_solution'])}",
        "",
        "## Sample Pages",
        "",
    ]
    for m in manifest:
        lines.append(f"- `{m['source']}` -> `{m['contest'].lower().replace(' ', '')}/problems/{m['slug']}/` | answer `{m['answer']}` | AoPS: {m['aops_url']}")
    lines += [
        "",
        "## Notes",
        "",
        "Solutions are rewritten in original English instructional language with step titles, reasoning cues, and checks. AoPS is used as an answer verification/reference source only.",
        "This is a sample round; bulk generation for all problems should run after the page structure and solution style are approved.",
    ]
    (ROOT / "problem_pages_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    samples = load_samples()
    manifest = write_pages(samples)
    update_index("amc10", manifest)
    update_index("amc12", manifest)
    validate_generated_mathjax(manifest)
    write_reports(manifest)
    print(json.dumps({"generated": len(manifest), "sources": [m["source"] for m in manifest]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()






