import csv, json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER = 119
CONTEST_DIR = "amc10"
ANSWER_KEY_URL = "https://artofproblemsolving.com/wiki/index.php/2020_AMC_10B_Answer_Key"
TARGET_NUMBERS = {11,12,13,15,16,17,18,19,20}
SKIPPED = ["2020 AMC 10B Problem 14 skipped: shaded region depends on the missing semicircle/hexagon figure."]
BATCH_LABEL = "2020 AMC 10B Problems 11-13,15-20"
NEXT_START = "2020 AMC 10B Problem 21"

ANS={11:("D",r"\frac{25}{63}"),12:("D","26"),13:("B",r"(-1030,-990)"),15:("D","11"),16:("A","Bela will always win."),17:("C","13"),18:("B",r"\frac15"),19:("A","2"),20:("B","19")}

OV={
11:(r"Harold and Betty each selected a different set of $5$ books from a set of $10$ books. What is the probability that their selections have exactly $2$ books in common?",[("A",r"$\frac19$"),("B",r"$\frac16$"),("C",r"$\frac29$"),("D",r"$\frac{25}{63}$"),("E",r"$\frac12$")]),
12:(r"What is the number of zeros following the decimal point before the first nonzero digit in the decimal representation of \[\frac{1}{20^{20}}?\]",[("A","20"),("B","24"),("C","25"),("D","26"),("E","30")]),
13:(r"Andy the Ant lives on a coordinate plane and is currently at $(-20,20)$ facing east. Andy moves $1$ unit and then turns $90^\circ$ left. Andy then moves $2$ units and turns $90^\circ$ left, then moves $3$ units and turns $90^\circ$ left, and so on. What are the coordinates of Andy's location immediately after his $2020$th left turn?",[("A",r"$(-1030,-994)$"),("B",r"$(-1030,-990)$"),("C",r"$(-1026,-994)$"),("D",r"$(-1026,-990)$"),("E",r"$(-1022,-994)$")]),
15:(r"The digits $1,2,3,4,5$ are written repeatedly from left to right to form a list of $10000$ digits, beginning $123451234512345\cdots$. Then every third digit in the list is crossed out. Of the remaining digits, every fourth digit is crossed out. Of the remaining digits, every fifth digit is crossed out. What is the sum of the digits in the positions $2019,2020,2021$ of the remaining list?",[("A","8"),("B","9"),("C","10"),("D","11"),("E","12")]),
16:(r"A game is played on the interval $[0,n]$, where $n$ is an integer greater than $4$. Two players, Bela and Jenn, take turns choosing real numbers in the interval. Bela goes first. A number may not be chosen if it is within $1$ unit of any previously chosen number. The player who cannot choose a number loses. Which player has a winning strategy?",[("A","Bela will always win."),("B","Jenn will always win."),("C","Bela wins if and only if $n$ is odd."),("D","Bela wins if and only if $n$ is even."),("E","Bela wins if and only if $n$ is prime.")]),
17:(r"Ten people are sitting around a circular table. Each person knows the two people sitting next to them and the person sitting directly across from them. How many ways are there to split the $10$ people into $5$ pairs so that the two people in each pair know each other?",[("A","11"),("B","12"),("C","13"),("D","14"),("E","15")]),
18:(r"An urn contains one red ball and one blue ball. Each minute, a ball is chosen uniformly at random from the urn and then replaced, along with another ball of the same color. After $4$ minutes, what is the probability that the urn contains $3$ red balls and $3$ blue balls?",[("A",r"$\frac16$"),("B",r"$\frac15$"),("C",r"$\frac14$"),("D",r"$\frac13$"),("E",r"$\frac12$")]),
19:(r"How many $10$-element subsets are there of a $52$-element set? The number is written in the form $158A00A4AA0$, where $A$ represents a digit. What is $A$?",[("A","2"),("B","3"),("C","4"),("D","5"),("E","6")]),
20:(r"A box has dimensions $1\times3\times4$. For a real number $r>0$, let $S(r)$ be the set of points that are within distance $r$ of the box. The volume of $S(r)$ can be written as $ar^3+br^2+cr+d$, where $a,b,c,d$ are constants. What is $\frac{bc}{ad}$?",[("A","16"),("B","19"),("C","22"),("D","24"),("E","26")]),
}

KEY_OVERRIDES={11:"Count Betty's choices after fixing Harold's selection.",12:"Rewrite the fraction with denominator a power of 10.",13:"Group the ant's motion into four-step cycles.",15:"Trace final positions backward through the deletion rounds.",16:"Use a mirror strategy about the midpoint of the interval.",17:"Count perfect matchings using the allowed neighbor and opposite edges.",18:"Use the symmetry of Polya's urn counts.",19:"Compute the binomial coefficient and match the digit pattern.",20:"Use the volume formula for a rounded rectangular box."}

SOL={
11:[("Fix one person's selection",r"To avoid double-counting, first pretend Harold's $5$ books are already fixed. Then Betty is choosing $5$ books from the same $10$ books."),("Choose the common books",r"For exactly $2$ books to be common, Betty must choose $2$ of Harold's $5$ books. This can be done in \[\binom52\] ways."),("Choose the non-common books",r"Betty's other $3$ books must come from the $5$ books Harold did not choose. This gives \[\binom53\] choices."),("Divide by all possible selections",r"Betty has \[\binom{10}{5}\] total possible selections, so the probability is \[\frac{\binom52\binom53}{\binom{10}{5}}=\frac{10\cdot10}{252}=\frac{25}{63}.\]"),("Conclude",r"The answer is $\boxed{\frac{25}{63}}$."),],
12:[("Turn the denominator into a power of ten",r"A decimal is easiest to read when the denominator is a power of $10$. Since $20=2\cdot10$, \[20^{20}=2^{20}\cdot10^{20}.\]"),("Clear the extra factor of 2",r"Multiplying numerator and denominator by $5^{20}$ gives \[\frac{1}{20^{20}}=\frac{5^{20}}{10^{40}}.\]"),("Count digits in the numerator",r"The number $5^{20}=95,367,431,640,625$ has $14$ digits. Dividing by $10^{40}$ moves the decimal point $40$ places left."),("Find the zeros before the first nonzero digit",r"If a $14$-digit integer is placed after $40$ decimal places, then the first nonzero digit appears after \[40-14=26\] zeros."),("Conclude",r"The answer is $\boxed{26}$."),],
13:[("Look for a repeating direction pattern",r"The directions repeat every $4$ moves: east, north, west, south. Because the lengths increase by $1$ each time, it is natural to group the motion into blocks of $4$ moves."),("Find one four-move displacement",r"A typical block with lengths $k,k+1,k+2,k+3$ changes the position by \[k-(k+2)=-2\] horizontally and \[(k+1)-(k+3)=-2\] vertically. So each full block moves Andy by $(-2,-2)$."),("Count complete blocks",r"The $2020$th left turn comes after $2020$ moves, and \[2020=4\cdot505.\] Thus Andy completes $505$ four-move blocks."),("Apply the displacement",r"Starting from $(-20,20)$, the total displacement is \[505(-2,-2)=(-1010,-1010).\] Therefore the location is \[(-20,20)+(-1010,-1010)=(-1030,-990).\]"),("Conclude",r"The answer is $\boxed{(-1030,-990)}$."),],
15:[("Think backward from the final positions",r"Forward deletion is messy because positions keep changing. A cleaner approach is to trace positions $2019,2020,2021$ backward through the three deletion rounds."),("Undo one deletion rule",r"If every $m$th remaining item was deleted, then the original position of the $j$th survivor is \[j+\left\lfloor\frac{j-1}{m-1}\right\rfloor.\] This counts how many deleted positions occurred before that survivor."),("Trace the three positions backward",r"Undoing the deletions by $5$, then $4$, then $3$, the final positions $2019,2020,2021$ correspond to original positions \[5044,\quad5047,\quad5050.\]"),("Read the repeated digit pattern",r"The original digit string repeats $1,2,3,4,5$. So a position's digit is determined by its remainder modulo $5$. The digits at positions $5044,5047,5050$ are respectively $4,2,5$."),("Add and conclude",r"The required sum is \[4+2+5=11.\] The answer is $\boxed{11}$."),],
16:[("Notice the symmetry of the interval",r"The game is about keeping legal space available. Since the interval $[0,n]$ is symmetric around its midpoint, Bela should try to use that symmetry from the first move."),("Choose the midpoint first",r"Bela begins by choosing \[\frac n2.\] This splits the interval into two mirror-image halves."),("Mirror every move",r"Whenever Jenn chooses a legal number $x$, Bela chooses the reflected number $n-x$. Distances are preserved by reflection, so if Jenn's choice is more than $1$ unit from all previous choices, its mirror is also more than $1$ unit from all mirrored previous choices."),("Explain why the mirror point is available",r"The only point fixed by the reflection is the midpoint, and Bela already chose it. Therefore Jenn can never choose a point whose mirror is itself and unoccupied."),("Conclude",r"Bela can always respond to Jenn's legal move. Since Jenn is the first player who can run out of moves, Bela will always win. The answer is $\boxed{\text{Bela will always win}}$."),],
17:[("Model the friendships as allowed edges",r"Label the people $0,1,\ldots,9$ around the table. A valid pair is either a neighboring pair or an opposite pair, so we are counting perfect matchings using those allowed edges."),("Start with person 0",r"Person $0$ can be paired only with $1$, $9$, or $5$. These three cases cover every valid pairing exactly once."),("Count the cases",r"If $0$ is paired with $1$, the remaining people can be paired in $4$ ways. By symmetry, pairing $0$ with $9$ also gives $4$ ways. If $0$ is paired with $5$, the remaining people can be paired in $5$ ways."),("Add the cases",r"The total number of valid splits is \[4+4+5=13.\] This case method is helpful because it prevents us from accidentally counting the same set of pairs twice."),("Conclude",r"The answer is $\boxed{13}$."),],
18:[("Identify the desired final composition",r"The urn starts with $1$ red and $1$ blue ball. After $4$ additions, having $3$ red and $3$ blue means exactly $2$ red additions and $2$ blue additions occurred."),("Use the Polya urn symmetry",r"In this urn process, every possible final number of red additions from $0$ through $4$ is equally likely. This happens because drawing a color makes that color more likely later, balancing the different orders in a symmetric way."),("Check with the formula",r"The probability of getting exactly $r$ red additions in $4$ draws is \[\frac{1}{5}\] for each $r=0,1,2,3,4$."),("Choose the needed count",r"We need $r=2$, so the probability is simply \[\frac15.\]"),("Conclude",r"The answer is $\boxed{\frac15}$."),],
19:[("Recognize the counting expression",r"The number of $10$-element subsets of a $52$-element set is the binomial coefficient \[\binom{52}{10}.\]"),("Compute in a controlled way",r"Using \[\binom{52}{10}=\frac{52\cdot51\cdot50\cdots43}{10!},\] careful arithmetic gives \[\binom{52}{10}=15,820,024,220.\]"),("Match the given digit pattern",r"The problem writes the number as $158A00A4AA0$. Comparing with \[15820024220,\] every $A$ must be the digit $2$."),("Check consistency",r"The positions of $A$ all agree with the same digit, so there is no contradiction in the pattern."),("Conclude",r"The answer is $\boxed{2}$."),],
20:[("Interpret the volume expansion",r"The set $S(r)$ is the original box thickened by distance $r$ in every direction. Its volume can be decomposed into the box, face prisms, edge quarter-cylinders, and corner octants."),("Find d and c",r"The constant term is the box volume, so \[d=1\cdot3\cdot4=12.\] The coefficient of $r$ is the surface area of the box: \[c=2(1\cdot3+1\cdot4+3\cdot4)=38.\]"),("Find b from the edges",r"The total edge length is \[4(1+3+4)=32.\] Around each edge is a quarter-cylinder, so \[b=\frac{\pi}{4}\cdot32=8\pi.\]"),("Find a from the corners",r"The $8$ rounded corners combine to one full sphere of radius $r$, so \[a=\frac{4\pi}{3}.\]"),("Compute the requested ratio",r"Now \[\frac{bc}{ad}=\frac{(8\pi)(38)}{\left(\frac{4\pi}{3}\right)(12)}=\frac{304\pi}{16\pi}=19.\]"),("Conclude",r"The answer is $\boxed{19}$."),],
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












































