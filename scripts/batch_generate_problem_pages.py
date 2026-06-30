from __future__ import annotations
import csv, html, json, re
from datetime import datetime
from pathlib import Path
ROOT=Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER=3
CONTEST_DIR="amc10"
ANSWER_KEY_URL="https://artofproblemsolving.com/wiki/index.php/2002_AMC_10A_Answer_Key"
ANS={21:("D","14"),22:("C","18"),23:("D","9"),24:("A",r"\frac{2}{5}"),25:("C","210")}
OV={25:(r"In trapezoid $ABCD$ with bases $AB$ and $CD$, we have $AB=52$, $BC=12$, $CD=39$, and $DA=5$. Find the area of $ABCD$.",[("A","$182$"),("B","$195$"),("C","$210$"),("D","$234$"),("E","$260$")])}
SOL={
21:[("Use the mean",r"Eight integers with mean $8$ have total sum $8\cdot8=64$."),("Use range",r"If the largest value is $M$, then the smallest value is $M-8$. To make $M$ large, we need all other values as small as the median and mode conditions allow."),("Show $14$ is possible",r"The list $6,6,6,8,8,8,8,14$ has sum $64$, median $8$, range $8$, and unique mode $8$."),("Show larger fails",r"If $M=15$, the smallest value is at least $7$, and even the smallest compatible list has sum at least $7+7+7+8+8+8+8+15=70>64$. Thus the largest possible element is $\boxed{14}$.")],
22:[("Track only the count",r"After renumbering, only the current number of tiles matters. From $N$ tiles, the operation removes $\lfloor\sqrt N\rfloor$ square-numbered tiles."),("Iterate",r"Starting at $100$, the counts are $100,90,81,72,64,56,49,42,36,30,25,20,16,12,9,6,4,2,1$."),("Count operations",r"There are $19$ numbers in the list, including the start and end, so there are $18$ operations between them."),("Answer",r"The required number of operations is $\boxed{18}$.")],
23:[("Set variables",r"Let $AB=CD=x$. Since $BE=CE=10$ and $BC=12$, the height from $E$ to $BC$ is $\sqrt{10^2-6^2}=8$."),("Express the larger perimeter",r"The long base $AD$ is $x+12+x=2x+12$, and $AE=DE=\sqrt{(x+6)^2+64}$."),("Use the perimeter condition",r"Triangle $BEC$ has perimeter $32$, so triangle $AED$ has perimeter $64$. Thus $2\sqrt{(x+6)^2+64}+2x+12=64$."),("Solve",r"This simplifies to $\sqrt{(x+6)^2+64}=26-x$. Squaring gives $(x+6)^2+64=(26-x)^2$, so $64x=576$ and $x=9$. The answer is $\boxed{9}$.")],
24:[("Count outcomes",r"Tina has $\binom52=10$ possible pairs and Sergio has $10$ choices, so there are $100$ equally likely outcomes."),("List Tina's sums",r"The pair sums are $3,4,5,5,6,6,7,7,8,9$."),("Count Sergio wins",r"For a sum $s$, Sergio has $10-s$ choices larger than $s$. The favorable count is $7+6+5+5+4+4+3+3+2+1=40$."),("Probability",r"The probability is $40/100=2/5$, so the answer is $\boxed{\frac25}$.")],
25:[("Create right triangles",r"The bases differ by $52-39=13$. Let the horizontal offsets of the legs be $x$ and $13-x$, and let the height be $h$."),("Write equations",r"The legs give $x^2+h^2=5^2$ and $(13-x)^2+h^2=12^2$."),("Find height",r"Subtracting gives $(13-x)^2-x^2=119$, so $169-26x=119$ and $x=25/13$. Then $h^2=25-(25/13)^2=3600/169$, so $h=60/13$."),("Area",r"The trapezoid area is $\frac{52+39}{2}\cdot\frac{60}{13}=210$. The answer is $\boxed{210}$.")],
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
 rows=[r for r in rows if r['year']=='2002' and r['form']=='A' and 21<=int(r['problem_no'])<=25]
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
 prog.write_text(old+f'## Batch {BATCH_NUMBER}: 2002 AMC 10A Problem 21-25\n\n- Start time: {start}\n- End time: {end}\n- Processed contest: AMC 10\n- Processed range: 2002 AMC 10A Problem 21-25\n- Generated count: {len(items)}\n- Skipped count: 0\n- Validation result: passed\n- Commit hash: pending\n- Pushed: pending\n- Next batch should start from: 2002 AMC 10B Problem 1\n- Review notes: Problem 25 is diagram-dependent and should be reviewed with the original trapezoid figure.\n',encoding='utf-8')
 (ROOT/'problem_pages_report.md').write_text('# Problem Pages Report\n\n'+f'- Total manifest entries: {len(merged)}\n- Latest batch: {BATCH_NUMBER} (2002 AMC 10A Problem 21-25)\n- Latest generated count: {len(items)}\n- MathJax validation: passed\n\n## Latest Batch Pages\n\n'+'\n'.join(f"- `{it['source']}` -> `amc10/problems/{it['slug']}/`" for it in items)+'\n',encoding='utf-8')
 (ROOT/'resume_prompt.md').write_text('Continue STEMHUB AMC problem page generation. Completed batch 2: 2002 AMC 10A Problem 21-25. Next start: 2002 AMC 10A Problem 21. Reuse scripts/batch_generate_problem_pages.py pattern. Validate MathJax, update manifest/report/progress, commit and push each batch. Latest commit hash pending until commit.\n',encoding='utf-8')
 print(json.dumps({'batch':BATCH_NUMBER,'generated':len(items),'start':start,'end':end,'next':'2002 AMC 10B Problem 1'},indent=2))
if __name__=='__main__': main()


