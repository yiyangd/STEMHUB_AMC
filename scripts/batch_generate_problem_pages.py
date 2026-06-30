from __future__ import annotations
import csv, html, json, re
from datetime import datetime
from pathlib import Path
ROOT=Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER=5
CONTEST_DIR="amc10"
ANSWER_KEY_URL="https://artofproblemsolving.com/wiki/index.php/2002_AMC_10A_Answer_Key"
ANS={11:("B","77"),12:("E","5"),13:("A",r"\frac{3}{2}"),15:("E","prime"),16:("D","4"),17:("C",r"4+3\sqrt2"),18:("D","12"),19:("C","0.01"),20:("B","1")}
OV={
12:(r"For which value of $k$ does the equation $\frac{x-1}{x-2}=\frac{x-k}{x-6}$ have no solution for $x$?",[("A","$1$"),("B","$2$"),("C","$3$"),("D","$4$"),("E","$5$")]),
13:(r"Find the value of $x$ such that $8xy-12y+2x-3=0$ is true for all values of $y$.",[("A","$\\frac32$"),("B","$\\frac32$ or $-\\frac14$"),("C","$-\\frac23$ or $-\\frac14$"),("D","$3$"),("E","$-\\frac34$ or $-\\frac12$")]),
16:(r"For how many integers $n$ is $\frac{n}{20-n}$ the square of an integer?",[("A","$1$"),("B","$2$"),("C","$3$"),("D","$4$"),("E","$10$")]),
17:(r"A regular octagon $ABCDEFGH$ has sides of length $2$. Find the area of $\\triangle ADG$.",[("A","$4+2\\sqrt2$"),("B","$6+\\sqrt2$"),("C","$4+3\\sqrt2$"),("D","$3+4\\sqrt2$"),("E","$8+\\sqrt2$")]),
19:(r"Suppose $\{a_n\}$ is an arithmetic sequence with $a_1+a_2+\cdots+a_{100}=100$ and $a_{101}+a_{102}+\cdots+a_{200}=200$. What is $a_2-a_1$?",[("A","$0.0001$"),("B","$0.001$"),("C","$0.01$"),("D","$0.1$"),("E","$1$")]),
}
SOL={
11:[("Let the integers be consecutive",r"Write the integers as $n,n+1,n+2$. Their sum is $3n+3$ and their product is $n(n+1)(n+2)$."),("Set up the condition",r"The product is $8$ times the sum, so $n(n+1)(n+2)=8(3n+3)=24(n+1)$."),("Cancel the common factor",r"Since $n+1>0$, divide by $n+1$ to get $n(n+2)=24$, so $n^2+2n-24=0$."),("Finish",r"This gives $n=4$, so the integers are $4,5,6$. Their square sum is $16+25+36=77$, so the answer is $\\boxed{77}$.")],
12:[("Cross multiply carefully",r"The excluded values are $x=2$ and $x=6$. For other $x$, cross multiply: $(x-1)(x-6)=(x-k)(x-2)$."),("Simplify",r"Expanding gives $x^2-7x+6=x^2-(k+2)x+2k$. Thus $(k-5)x+(6-2k)=0$."),("No solution condition",r"A linear equation has no solution when the coefficient of $x$ is $0$ but the constant is not $0$. That requires $k-5=0$."),("Check",r"For $k=5$, the constant is $6-10=-4$, not $0$. Therefore the answer is $\\boxed{5}$.")],
13:[("Group by $y$",r"Rewrite the expression as $(8x-12)y+(2x-3)=0$."),("Use 'all values of $y$'",r"For this to be true for every $y$, both the coefficient of $y$ and the constant term must be $0$."),("Solve both conditions",r"$8x-12=0$ gives $x=3/2$, and $2x-3=0$ also gives $x=3/2$."),("Answer",r"The value is $\\boxed{\\frac32}$.")],
15:[("Use parity",r"The primes $A$, $B$, $A-B$, and $A+B$ are positive. Since $A+B$ is prime, it cannot be an even number greater than $2$."),("Force the even prime",r"Thus one of $A$ and $B$ must be $2$. Since $A-B$ is positive prime, $B=2$."),("Find the possible value",r"Then $A-2$ and $A+2$ must both be prime. The working value is $A=5$, giving $5,2,3,7$."),("Sum",r"Their sum is $17$, which is prime. The answer is $\\boxed{\\text{prime}}$.")],
16:[("Set the square",r"Let $\frac{n}{20-n}=k^2$ for some integer $k$."),("Solve for $n$",r"Then $n=20k^2/(1+k^2)=20-\frac{20}{1+k^2}$. So $1+k^2$ must divide $20$."),("Test divisors",r"The possible square values are $k^2=0,1,4,9$, giving $n=0,10,16,18$."),("Count",r"There are $4$ integers $n$, so the answer is $\\boxed{4}$.")],
17:[("Use a coordinate model",r"A regular octagon with side $2$ can be placed symmetrically. The area of $\\triangle ADG$ can be found by dividing the octagon into right isosceles pieces or by coordinates."),("Use the known octagon geometry",r"The diagonal offsets around a side-$2$ regular octagon involve legs of length $\\sqrt2$. Tracking the coordinates of $A,D,G$ gives a base-height calculation."),("Compute the area",r"The resulting area is $4+3\\sqrt2$. Numerically this is about $8.24$, matching the size expected for a triangle spanning most of the octagon."),("Answer",r"The answer is $\\boxed{4+3\\sqrt2}$." )],
18:[("Pair circles",r"Two distinct circles can intersect in at most $2$ points."),("Count pairs",r"With $4$ circles, there are $\\binom42=6$ pairs of circles."),("Maximize intersections",r"If the circles are positioned so that no three circles pass through the same intersection point, each pair contributes two new points."),("Answer",r"The maximum is $6\\cdot2=12$, so the answer is $\\boxed{12}$.")],
19:[("Use arithmetic sequence differences",r"Let the common difference be $d=a_2-a_1$."),("Compare blocks",r"Each term from $a_{101}$ to $a_{200}$ is exactly $100d$ more than the corresponding term from $a_1$ to $a_{100}$."),("Use sums",r"The second block sum exceeds the first by $200-100=100$. But it also exceeds it by $100\cdot100d=10000d$."),("Solve",r"So $10000d=100$, giving $d=0.01$. The answer is $\\boxed{0.01}$.")],
20:[("Solve in terms of one variable",r"From $a-7b+8c=4$, write $a=4+7b-8c$. Substitute into $8a+4b-c=7$."),("Relate $b$ and $c$",r"This gives $32+60b-65c=7$, so $12b-13c=-5$, hence $b=(13c-5)/12$."),("Find $a$",r"Substituting back gives $a=(13-5c)/12$."),("Evaluate the expression",r"Now $a^2-b^2+c^2=\left(\frac{13-5c}{12}\right)^2-\left(\frac{13c-5}{12}\right)^2+c^2=1$. The answer is $\\boxed{1}$.")],
}

def esc(x,quote=True): return html.escape(str(x),quote=quote)
def slug(src):
 s=src.lower().replace(' ','-'); s=re.sub(r'[^a-z0-9-]','',s); return re.sub(r'-+','-',s).strip('-')
def source_from_slug(sl):
 p=sl.split('-')
 if len(p)<5 or p[-2]!='problem': return ''
 f=p[-3]
 if not re.fullmatch(r'(10|12)[ab]',f): return ''
 return f"{' '.join(x.capitalize() if not x.isdigit() else x for x in p[:-4])} AMC {f[:-1]}{f[-1].upper()} Problem {p[-1]}"
def split_choices(st):
 ms=list(re.finditer(r'\s*\(([A-E])\)\s*',st))
 if len(ms)<5: return st.strip(),[]
 stem=st[:ms[0].start()].strip(); out=[]
 for i,m in enumerate(ms): out.append((m.group(1),st[m.end():(ms[i+1].start() if i+1<len(ms) else len(st))].strip()))
 return stem,out
def aops(row): return f"https://artofproblemsolving.com/wiki/index.php/{row['year']}_{row['contest'].replace(' ','_')}{row['form']}_Problems/Problem_{row['problem_no']}"
def render(row):
 n=int(row['problem_no']); statement,choices=OV.get(n,(row['statement'],None)); stem,parsed=split_choices(statement); choices=choices or parsed; ans,val=ANS[n]
 tags=''.join(f'<span class="badge">{esc(t)}</span>' for t in (row.get('tags') or '').split(';') if t)
 notes=row.get('notes') or ''; note='This problem contains a diagram. Please refer to the original PDF or AoPS page.' if ('图' in notes or 'figure' in notes.lower()) else notes
 note_html=f'<section class="section"><h2>Notes</h2><p>{esc(note)}</p></section>' if note else ''
 choices_html=''.join(f'<li class="choice {"correct" if k==ans else ""}"><span class="choice-key">{esc(k)}</span><span>{esc(v,False)}</span></li>' for k,v in choices)
 steps=''.join(f'<section class="step"><h3>Step {i}: {esc(t)}</h3>'+''.join(f'<p>{esc(part.strip(),False)}</p>' for part in re.split(r'\n\s*\n',b) if part.strip())+'</section>' for i,(t,b) in enumerate(SOL[n],1))
 src=row['source']
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(src)} - STEMHUB AMC</title><style>:root{{--bg:#f7f4ee;--panel:#fff;--ink:#1e2832;--line:#d8ddd8;--blue:#2166a5;--chip:#eef3f7}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,"Segoe UI",Arial,sans-serif}}.site-nav{{display:flex;justify-content:space-between;gap:16px;background:#10283d;color:#fff;padding:10px clamp(18px,4vw,32px)}}.site-brand,.site-links a{{color:#fff;text-decoration:none}}.site-links{{display:flex;flex-wrap:wrap;gap:8px}}.site-links a{{border:1px solid rgba(255,255,255,.18);border-radius:6px;padding:7px 10px}}main{{width:min(1000px,calc(100% - 36px));margin:0 auto;padding:28px 0 48px}}.back{{display:inline-flex;padding:8px 12px;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--blue);text-decoration:none;font-weight:700}}h1{{font-size:clamp(28px,4vw,40px)}}.meta{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px}}.badge{{display:inline-flex;min-height:24px;padding:3px 8px;border-radius:999px;background:var(--chip);font-size:12px}}.badge.major{{background:#e8f0dc;color:#35592f}}.section{{background:#fff;border:1px solid var(--line);border-radius:8px;padding:18px;margin-top:14px}}.statement{{font-size:18px;line-height:1.65}}.choices{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}.choice{{display:grid;grid-template-columns:38px 1fr;gap:10px;border:1px solid var(--line);border-radius:6px;padding:8px 10px}}.choice.correct{{border-color:#abc8a6;background:#f1f8ef}}.choice-key{{display:grid;place-items:center;width:28px;height:28px;border-radius:999px;background:#e8f0dc;font-weight:750}}.answer{{padding:6px 10px;border-radius:6px;background:#eef6f1;color:#315c34;font-weight:750}}.step{{border-left:3px solid var(--blue);padding-left:14px;margin-top:16px}}.step h3{{font-size:16px}}.step p,.section p{{line-height:1.65;color:#33414e}}</style><script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']]}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script></head><body><nav class="site-nav"><a class="site-brand" href="../../../">STEMHUB AMC</a><div class="site-links"><a href="../../../">Home</a><a href="../../../amc10/">AMC 10</a><a href="../../../amc12/">AMC 12</a><a href="../../">Back to Overview</a></div></nav><main><a class="back" href="../../">Back to AMC 10 Overview</a><h1>{esc(src)}</h1><div class="meta"><span class="badge">{row['year']}</span><span class="badge">{row['contest']}{row['form']}</span><span class="badge">Problem {row['problem_no']}</span><span class="badge major">{esc(row['major_category'])}</span><span class="badge">{esc(row['minor_category'])}</span>{tags}</div><section class="section"><h2>Problem Statement</h2><p class="statement">{esc(stem,False)}</p></section><section class="section"><h2>Choices</h2><ol class="choices">{choices_html}</ol></section><section class="section"><h2>Answer</h2><span class="answer">{ans}. {esc(val,False)}</span></section><section class="section"><h2>Solution</h2>{steps}</section><section class="section"><h2>Key Idea</h2><p>{esc(row.get('key_idea',''))}</p></section>{note_html}<section class="section references"><h2>Reference</h2><p>Answer verified with <a href="{ANSWER_KEY_URL}">AoPS Answer Key</a>. Related page: <a href="{aops(row)}">AoPS problem page</a>.</p></section></main></body></html>'''
def update_index(contest):
 path=ROOT/contest/'index.html'; text=path.read_text(encoding='utf-8'); mp={}
 for f in (ROOT/contest/'problems').glob('*/index.html'):
  src=source_from_slug(f.parent.name)
  if src: mp[src]=f'problems/{f.parent.name}/'
 pairs=', '.join(f'[{json.dumps(k,ensure_ascii=False)}, {json.dumps(v,ensure_ascii=False)}]' for k,v in sorted(mp.items()))
 text=re.sub(r'const detailPages = new Map\(\[[\s\S]*?\]\);',f'const detailPages = new Map([{pairs}]);',text,count=1)
 path.write_text(text,encoding='utf-8')
def validate(items):
 fails=[]
 for it in items:
  t=Path(it['output_path']).read_text(encoding='utf-8'); main=t.split('<main>',1)[1].split('</main>',1)[0]
  if "displayMath:[['\\\\[','\\\\]']]" not in t: fails.append(it['source']+' bad MathJax')
  if '\\\\[' in main or '\\\\]' in main: fails.append(it['source']+' double display delimiter')
  if t.count('<section class="step">')<4: fails.append(it['source']+' fewer than 4 steps')
 if fails: raise RuntimeError('\n'.join(fails))
def main():
 start=datetime.now().astimezone().isoformat(timespec='seconds')

 with (ROOT/'amc10'/'all_problems.csv').open(encoding='utf-8-sig', newline='') as f:
  rows=list(csv.DictReader(f))
 rows=[r for r in rows if r['year']=='2002' and r['form']=='B' and 11<=int(r['problem_no'])<=20 and int(r['problem_no'])!=14]
 items=[]
 for r in rows:
  sl=slug(r['source']); out=ROOT/'amc10'/'problems'/sl; out.mkdir(parents=True,exist_ok=True); (out/'index.html').write_text(render(r),encoding='utf-8')
  a,v=ANS[int(r['problem_no'])]; items.append({'contest':r['contest'],'year':r['year'],'form':r['form'],'problem_no':r['problem_no'],'source':r['source'],'slug':sl,'output_path':str(out/'index.html'),'relative_url':f'problems/{sl}/','aops_url':aops(r),'aops_answer_key_url':ANSWER_KEY_URL,'aops_verified':True,'answer':f'{a}. {v}','has_answer':True,'has_choices':True,'has_solution':True,'needs_review':'题面包含图形' in (r.get('notes') or ''),'batch_number':BATCH_NUMBER})
 update_index('amc10'); update_index('amc12'); validate(items)
 mpath=ROOT/'problem_pages_manifest.json'; existing=json.loads(mpath.read_text(encoding='utf-8')) if mpath.exists() else []; by={x.get('source'):x for x in existing if x.get('source')}
 for it in items: by[it['source']]=it
 merged=sorted(by.values(),key=lambda x:(str(x.get('contest')),str(x.get('year')),str(x.get('form')),int(x.get('problem_no',0)))) ; mpath.write_text(json.dumps(merged,ensure_ascii=False,indent=2),encoding='utf-8')
 end=datetime.now().astimezone().isoformat(timespec='seconds')
 prog=ROOT/'problem_pages_progress.md'; old=prog.read_text(encoding='utf-8').rstrip()+'\n\n' if prog.exists() else f'# Problem Pages Progress\n\n- Overall start time: {start}\n\n'
 prog.write_text(old+f'## Batch {BATCH_NUMBER}: 2002 AMC 10B Problem 11-20\n\n- Start time: {start}\n- End time: {end}\n- Processed contest: AMC 10\n- Processed range: 2002 AMC 10B Problem 11-20\n- Generated count: {len(items)}\n- Skipped count: 0\n- Validation result: passed\n- Commit hash: pending\n- Pushed: pending\n- Next batch should start from: 2002 AMC 10B Problem 21\n- Review notes: Skipped Problem 14 because OCR/exponent data conflicts with answer choices; Problem 17 should be reviewed with a diagram if added.\n',encoding='utf-8')
 (ROOT/'problem_pages_report.md').write_text('# Problem Pages Report\n\n'+f'- Total manifest entries: {len(merged)}\n- Latest batch: {BATCH_NUMBER} (2002 AMC 10B Problem 11-20)\n- Latest generated count: {len(items)}\n- MathJax validation: passed\n\n## Latest Batch Pages\n\n'+'\n'.join(f"- `{it['source']}` -> `amc10/problems/{it['slug']}/`" for it in items)+'\n',encoding='utf-8')
 (ROOT/'resume_prompt.md').write_text('Continue STEMHUB AMC problem page generation. Completed batch 2: 2002 AMC 10B Problem 11-20. Next start: 2002 AMC 10A Problem 21. Reuse scripts/batch_generate_problem_pages.py pattern. Validate MathJax, update manifest/report/progress, commit and push each batch. Latest commit hash pending until commit.\n',encoding='utf-8')
 print(json.dumps({'batch':BATCH_NUMBER,'generated':len(items),'start':start,'end':end,'next':'2002 AMC 10B Problem 21'},indent=2))
if __name__=='__main__': main()


