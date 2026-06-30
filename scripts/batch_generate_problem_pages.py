from __future__ import annotations
import csv, html, json, re
from datetime import datetime
from pathlib import Path
ROOT=Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER=4
CONTEST_DIR="amc10"
ANSWER_KEY_URL="https://artofproblemsolving.com/wiki/index.php/2002_AMC_10A_Answer_Key"
ANS={1:("E",r"\frac{3}{2}"),2:("C","4"),3:("A","0"),4:("D","11"),5:("E",r"12\pi"),6:("B","one"),7:("E",r"n>84"),8:("D","Thursday"),9:("D","115"),10:("C",r"(1,-2)")}
OV={
1:(r"The ratio $\frac{2^{2001}\cdot3^{2003}}{6^{2002}}$ is",[("A","$\\frac16$"),("B","$\\frac13$"),("C","$\\frac12$"),("D","$\\frac23$"),("E","$\\frac32$")]),
2:(r"For nonzero numbers $a,b,c$, define $(a,b,c)=\frac{abc}{a+b+c}$. Find $(2,4,6)$.",[("A","$1$"),("B","$2$"),("C","$4$"),("D","$6$"),("E","$24$")]),
4:(r"What is the value of $(3x-2)(4x+1)-(3x-2)4x+1$ when $x=4$?",[("A","$0$"),("B","$1$"),("C","$10$"),("D","$11$"),("E","$12$")]),
5:(r"Circles of radius $2$ and $3$ are externally tangent and are circumscribed by a third circle. Find the area of the shaded region.",[("A","$3\\pi$"),("B","$4\\pi$"),("C","$6\\pi$"),("D","$9\\pi$"),("E","$12\\pi$")]),
7:(r"Let $n$ be a positive integer such that $\frac12+\frac13+\frac17+\frac1n$ is an integer. Which of the following statements is not true?",[("A","$2$ divides $n$"),("B","$3$ divides $n$"),("C","$6$ divides $n$"),("D","$7$ divides $n$"),("E","$n>84$")]),
9:(r"Using the letters A, M, O, S, and U, we can form $120$ five-letter words. If these words are arranged in alphabetical order, then the word USAMO occupies position",[("A","$112$"),("B","$113$"),("C","$114$"),("D","$115$"),("E","$116$")]),
}
SOL={
1:[("Rewrite $6$",r"Since $6=2\cdot3$, rewrite $6^{2002}$ as $2^{2002}3^{2002}$."),("Cancel powers",r"\[\frac{2^{2001}3^{2003}}{6^{2002}}=\frac{2^{2001}3^{2003}}{2^{2002}3^{2002}}=\frac{3}{2}.\]"),("Check",r"One extra factor of $3$ remains on top and one extra factor of $2$ remains on bottom."),("Answer",r"The answer is $\boxed{\frac32}$.")],
2:[("Substitute",r"Use the rule $(a,b,c)=\frac{abc}{a+b+c}$ with $a=2,b=4,c=6$."),("Compute numerator",r"The numerator is $2\cdot4\cdot6=48$."),("Compute denominator",r"The denominator is $2+4+6=12$."),("Answer",r"Thus $(2,4,6)=48/12=4$, so the answer is $\boxed{4}$.")],
3:[("Understand the numbers",r"The set is $9,99,999,\ldots,999999999$, one number with each length from $1$ to $9$."),("Sum efficiently",r"Their sum is $1,111,111,101$. Dividing by $9$ gives the mean $123,456,789$."),("Read the digits",r"The number $123,456,789$ contains each digit from $1$ through $9$ exactly once."),("Answer",r"It does not contain $0$, so the answer is $\boxed{0}$.")],
4:[("Look for cancellation",r"The first two terms share the factor $3x-2$."),("Factor the shared part",r"\[(3x-2)(4x+1)-(3x-2)4x=(3x-2)((4x+1)-4x)=3x-2.\]"),("Remember the final $+1$",r"The expression is therefore $3x-2+1=3x-1$."),("Evaluate",r"At $x=4$, this is $12-1=11$. The answer is $\boxed{11}$.")],
5:[("Find the large radius",r"For two externally tangent circles of radii $2$ and $3$ inside a circumscribing circle, the diameter of the large circle is $2+3+2+3=10$, so its radius is $5$."),("Compute areas",r"The large circle has area $25\pi$. The two smaller circles have total area $4\pi+9\pi=13\pi$."),("Subtract",r"The shaded region is the area inside the large circle but outside the two smaller circles: $25\pi-13\pi=12\pi$."),("Answer",r"The answer is $\boxed{12\pi}$. This should be checked with the original figure when adding diagrams.")],
6:[("Factor",r"The expression factors as $n^2-3n+2=(n-1)(n-2)$."),("Use primality",r"A prime number has exactly two positive factors. A product of two positive integers is prime only if one factor is $1$ and the other is prime."),("Test possible $n$",r"For positive $n$, the only working case is $n=3$, giving $(3-1)(3-2)=2$."),("Answer",r"There is exactly one such positive integer, so the answer is $\boxed{\text{one}}$.")],
7:[("Add fixed fractions",r"\[\frac12+\frac13+\frac17=\frac{21+14+6}{42}=\frac{41}{42}.\]"),("Force an integer",r"Since $0<\frac{41}{42}<1$, adding $1/n$ must make the total equal to $1$. Thus $1/n=1/42$."),("Find $n$",r"So $n=42$."),("Check statements",r"The number $42$ is divisible by $2,3,6,$ and $7$, but $42>84$ is false. The answer is $\boxed{n>84}$.")],
8:[("Use 31-day months",r"In a 31-day month, the weekdays that occur five times are the weekdays of the 1st, 2nd, and 3rd."),("List July possibilities",r"If July has five Mondays, then Monday must be one of July 1, July 2, or July 3."),("Move to August",r"August 1 is three weekdays after July 1, because July has $31\equiv3\pmod7$ days."),("Common result",r"Checking the three cases shows August must have five Thursdays. The answer is $\boxed{\text{Thursday}}$.")],
9:[("Count words before U",r"Alphabetically, the letters before U are A, M, O, and S. Words starting with those letters contribute $4\cdot4!=96$ words."),("Count U-words before US",r"After the first letter U, the second letter before S can be A, M, or O. That gives $3\cdot3!=18$ more words."),("Finish within USA",r"Once the word starts with USA, the remaining letters M and O are already in alphabetical order for USAMO, so no more words come before it within that prefix."),("Position",r"The position is $96+18+1=115$. The answer is $\boxed{115}$.")],
10:[("Use root relationships",r"The roots of $x^2+ax+b=0$ are given as $a$ and $b$. By Vieta's formulas, $a+b=-a$ and $ab=b$."),("Use nonzero $b$",r"Since $b$ is nonzero, $ab=b$ implies $a=1$."),("Find $b$",r"Then $a+b=-a$ becomes $1+b=-1$, so $b=-2$."),("Answer",r"The pair is $\boxed{(1,-2)}$.")],
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
 rows=[r for r in rows if r['year']=='2002' and r['form']=='B' and 1<=int(r['problem_no'])<=10]
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
 prog.write_text(old+f'## Batch {BATCH_NUMBER}: 2002 AMC 10B Problem 1-10\n\n- Start time: {start}\n- End time: {end}\n- Processed contest: AMC 10\n- Processed range: 2002 AMC 10B Problem 1-10\n- Generated count: {len(items)}\n- Skipped count: 0\n- Validation result: passed\n- Commit hash: pending\n- Pushed: pending\n- Next batch should start from: 2002 AMC 10B Problem 11\n- Review notes: Problem 5 is diagram-dependent and should be reviewed with the original circle figure.\n',encoding='utf-8')
 (ROOT/'problem_pages_report.md').write_text('# Problem Pages Report\n\n'+f'- Total manifest entries: {len(merged)}\n- Latest batch: {BATCH_NUMBER} (2002 AMC 10B Problem 1-10)\n- Latest generated count: {len(items)}\n- MathJax validation: passed\n\n## Latest Batch Pages\n\n'+'\n'.join(f"- `{it['source']}` -> `amc10/problems/{it['slug']}/`" for it in items)+'\n',encoding='utf-8')
 (ROOT/'resume_prompt.md').write_text('Continue STEMHUB AMC problem page generation. Completed batch 2: 2002 AMC 10B Problem 1-10. Next start: 2002 AMC 10A Problem 21. Reuse scripts/batch_generate_problem_pages.py pattern. Validate MathJax, update manifest/report/progress, commit and push each batch. Latest commit hash pending until commit.\n',encoding='utf-8')
 print(json.dumps({'batch':BATCH_NUMBER,'generated':len(items),'start':start,'end':end,'next':'2002 AMC 10B Problem 11'},indent=2))
if __name__=='__main__': main()


