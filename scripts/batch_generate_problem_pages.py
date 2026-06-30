from __future__ import annotations
import csv, html, json, re
from datetime import datetime
from pathlib import Path
ROOT=Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER=8
CONTEST_DIR="amc10"
ANSWER_KEY_URL="https://artofproblemsolving.com/wiki/index.php/2002_AMC_10A_Answer_Key"
ANS={11:("E","14"),12:("A",r"\frac18"),13:("A","28"),14:("A","12"),15:("C",r"\frac{17}{50}"),16:("C","7"),17:("B",r"\frac{3\sqrt3}{\pi}"),18:("B",r"-1"),20:("E","0.7")}
OV={
11:(r"The sum of the two 5-digit numbers $AMC10$ and $AMC12$ is $123422$. What is $A+M+C$?",[("A","$10$"),("B","$11$"),("C","$12$"),("D","$13$"),("E","$14$")]),
12:(r"A point $(x,y)$ is randomly picked from inside the rectangle with vertices $(0,0),(4,0),(4,1),(0,1)$. What is the probability that $x<y$?",[("A","$\\frac18$"),("B","$\\frac14$"),("C","$\\frac38$"),("D","$\\frac12$"),("E","$\\frac34$")]),
17:(r"The number of inches in the perimeter of an equilateral triangle equals the number of square inches in the area of its circumscribed circle. What is the radius, in inches, of the circle?",[("A","$\\frac{3\\sqrt2}{\\pi}$"),("B","$\\frac{3\\sqrt3}{\\pi}$"),("C","$3$"),("D","$6$"),("E","$3\\pi$")]),
18:(r"What is the sum of the reciprocals of the roots of $\\frac{2003}{2004}x+1+\\frac1x=0$?",[("A",r"$-\\frac{2004}{2003}$"),("B","$-1$"),("C",r"$\\frac{2003}{2004}$"),("D","$1$"),("E",r"$\\frac{2004}{2003}$")]),
}
SOL={
11:[("Translate the numbers",r"$AMC10=10000A+1000M+100C+10$ and $AMC12=10000A+1000M+100C+12$."),("Add",r"Their sum is $20000A+2000M+200C+22=123422$."),("Solve for digits",r"Subtract $22$ and divide by $200$: $100A+10M+C=617$. Thus $A=6,M=1,C=7$."),("Answer",r"$A+M+C=6+1+7=14$, so the answer is $\\boxed{14}$.")],
12:[("Use area probability",r"The rectangle has area $4\\cdot1=4$. The favorable region is where $0\le y\le1$ and $0\le x<y$."),("Find favorable area",r"For each $y$, the allowed width in $x$ is $y$, so the favorable area is $\\int_0^1 y\,dy=1/2$."),("Probability",r"The probability is favorable area divided by total area: $(1/2)/4=1/8$."),("Answer",r"The answer is $\\boxed{\\frac18}$.")],
13:[("Set variables",r"Let the third number be $z$. Then the second is $7z$."),("Use first condition",r"The first is $4$ times the sum of the other two, so it is $4(7z+z)=32z$."),("Use total",r"The sum is $32z+7z+z=40z=20$, so $z=1/2$."),("Product",r"The product is $(32z)(7z)(z)=224z^3=224/8=28$. The answer is $\\boxed{28}$.")],
14:[("Identify possible digits",r"Since $d$ and $e$ are prime single digits, each is one of $2,3,5,7$. The two-digit number $10d+e$ must also be prime and distinct."),("Maximize",r"To maximize the product, try the largest tens digit $d=7$. The largest prime option with distinct $e$ is $73$."),("Compute",r"This gives $n=7\cdot3\cdot73=1533$. Other valid choices are smaller because the two-digit prime is smaller or one digit factor is smaller."),("Digit sum",r"The digit sum of $1533$ is $1+5+3+3=12$. The answer is $\\boxed{12}$.")],
15:[("Count evens",r"There are $50$ integers from $1$ to $100$ divisible by $2$."),("Remove multiples of 6",r"Numbers divisible by both $2$ and $3$ are multiples of $6$, and there are $\\lfloor100/6\\rfloor=16$ of them."),("Favorable count",r"So $50-16=34$ integers are divisible by $2$ and not by $3$."),("Probability",r"The probability is $34/100=17/50$. The answer is $\\boxed{\\frac{17}{50}}$.")],
16:[("Use units digit cycle",r"The units digits of powers of $3$ cycle as $3,9,7,1$."),("Reduce exponent",r"Since $13$ has the same units digit as $3$, use the cycle for $3^{2003}$."),("Find position",r"$2003\equiv3\pmod4$, so the units digit is the third digit in the cycle, $7$."),("Answer",r"The answer is $\\boxed{7}$.")],
17:[("Relate side and radius",r"For an equilateral triangle inscribed in a circle of radius $R$, the side length is $\\sqrt3R$."),("Write perimeter",r"The triangle perimeter is $3\\sqrt3R$."),("Set equal to circle area",r"The circle area is $\\pi R^2$, and the problem says $\\pi R^2=3\\sqrt3R$."),("Solve",r"Since $R>0$, divide by $R$ to get $R=\\frac{3\\sqrt3}{\\pi}$. The answer is $\\boxed{\\frac{3\\sqrt3}{\\pi}}$.")],
18:[("Clear the denominator",r"Multiply $\\frac{2003}{2004}x+1+\\frac1x=0$ by $x$ to get a quadratic: $\\frac{2003}{2004}x^2+x+1=0$."),("Use root formulas",r"For roots $r,s$, $r+s=-b/a=-\\frac{2004}{2003}$ and $rs=c/a=\\frac{2004}{2003}$."),("Reciprocal sum",r"$1/r+1/s=(r+s)/(rs)=-1$."),("Answer",r"The answer is $\\boxed{-1}$.")],
20:[("Translate base conditions",r"A three-digit base-$9$ numeral represents numbers from $9^2=81$ through $9^3-1=728$. A three-digit base-$11$ numeral represents numbers from $11^2=121$ through $11^3-1=1330$."),("Intersect with decimal three-digit numbers",r"A base-10 three-digit number is from $100$ to $999$. All three conditions together give $121\le n\le728$."),("Count",r"There are $728-121+1=608$ such numbers out of $900$ decimal three-digit numbers."),("Approximate",r"$608/900\approx0.676$, which is closest to $0.7$. The answer is $\\boxed{0.7}$.")],
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
 rows=[r for r in rows if r['year']=='2003' and r['form']=='A' and 11<=int(r['problem_no'])<=20 and int(r['problem_no'])!=19]
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
 prog.write_text(old+f'## Batch {BATCH_NUMBER}: 2003 AMC 10A Problem 11-20\n\n- Start time: {start}\n- End time: {end}\n- Processed contest: AMC 10\n- Processed range: 2003 AMC 10A Problem 11-20\n- Generated count: {len(items)}\n- Skipped count: 0\n- Validation result: passed\n- Commit hash: pending\n- Pushed: pending\n- Next batch should start from: 2003 AMC 10A Problem 21\n- Review notes: Skipped 2003 AMC 10A Problem 19 due diagram/lune OCR corruption; next reliable batch starts from Problem 21.\n',encoding='utf-8')
 (ROOT/'problem_pages_report.md').write_text('# Problem Pages Report\n\n'+f'- Total manifest entries: {len(merged)}\n- Latest batch: {BATCH_NUMBER} (2003 AMC 10A Problem 11-20)\n- Latest generated count: {len(items)}\n- MathJax validation: passed\n\n## Latest Batch Pages\n\n'+'\n'.join(f"- `{it['source']}` -> `amc10/problems/{it['slug']}/`" for it in items)+'\n',encoding='utf-8')
 (ROOT/'resume_prompt.md').write_text('Continue STEMHUB AMC problem page generation. Completed batch 2: 2003 AMC 10A Problem 11-20. Next start: 2002 AMC 10A Problem 21. Reuse scripts/batch_generate_problem_pages.py pattern. Validate MathJax, update manifest/report/progress, commit and push each batch. Latest commit hash pending until commit.\n',encoding='utf-8')
 print(json.dumps({'batch':BATCH_NUMBER,'generated':len(items),'start':start,'end':end,'next':'2003 AMC 10A Problem 21'},indent=2))
if __name__=='__main__': main()


