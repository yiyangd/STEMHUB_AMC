from __future__ import annotations
import csv, html, json, re
from datetime import datetime
from pathlib import Path
ROOT=Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER=2
CONTEST_DIR="amc10"
ANSWER_KEY_URL="https://artofproblemsolving.com/wiki/index.php/2002_AMC_10A_Answer_Key"
ANS={11:("B","13"),12:("B","48"),13:("B","12"),14:("B","1"),15:("E","190"),16:("B",r"-\\frac{10}{3}"),17:("D",r"\\frac{2}{5}"),18:("D","90"),19:("E",r"3\\pi"),20:("D",r"\\frac{5}{3}")}
OV={}
SOL={
11:[("Understand the packing limits",r"A disk holds $1.44$ MB. A $0.8$ MB file cannot be paired with a $0.7$ MB file, since $0.8+0.7=1.5>1.44$."),("Pack the largest files efficiently",r"Pair each of the three $0.8$ MB files with one $0.4$ MB file. That uses $3$ disks."),("Pack the medium files",r"The twelve $0.7$ MB files can be paired two per disk, since $0.7+0.7=1.4$. That uses $6$ more disks."),("Finish the count",r"There are $12$ files of size $0.4$ MB left, and at most three fit per disk. They require $4$ disks, for a total of $3+6+4=13$. The answer is $\boxed{13}$.")],
12:[("Turn minutes into hours",r"Three minutes is $0.05$ hours. Let the on-time travel time be $t$ hours and the distance be $d$ miles."),("Write both time equations",r"At $40$ mph, $d/40=t+0.05$. At $60$ mph, $d/60=t-0.05$."),("Eliminate $t$",r"Subtracting gives $d/40-d/60=0.10$. Since $1/40-1/60=1/120$, we get $d=12$."),("Find the needed speed",r"The on-time travel time is $12/40-0.05=0.25$ hours. The needed speed is $12/0.25=48$, so the answer is $\boxed{48}$.")],
13:[("Recognize the right triangle",r"The sides $15,20,25$ form a right triangle because $15^2+20^2=25^2$."),("Compute the area",r"Using the legs, the area is $\frac12\cdot15\cdot20=150$."),("Shortest altitude uses longest base",r"For a fixed area, altitude equals $2A/\text{base}$. The shortest altitude is to the longest side, $25$."),("Calculate",r"$h=2\cdot150/25=12$. The answer is $\boxed{12}$.")],
14:[("Use Vieta",r"If the prime roots are $p$ and $q$, then $p+q=63$ and $pq=k$."),("Use parity",r"The sum $63$ is odd. Two odd primes have an even sum, so one root must be the only even prime, $2$."),("Determine the roots",r"The other root is $63-2=61$, which is prime."),("Count $k$",r"Then $k=2\cdot61=122$. There is exactly one possible value, so the answer is $\boxed{1}$.")],
15:[("Focus on units digits",r"A two-digit prime cannot end in an even digit or $5$. Therefore the units digits must be $1,3,7,9$."),("Identify tens digits",r"The remaining digits $2,4,5,6$ must be tens digits."),("Use place value",r"The sum is $10(2+4+5+6)+(1+3+7+9)=170+20=190$."),("Answer",r"The exact pairing is not needed for the sum. The answer is $\boxed{190}$.")],
16:[("Name the common value",r"Let the common value be $t$. Then $a=t-1$, $b=t-2$, $c=t-3$, and $d=t-4$."),("Sum variables",r"Thus $a+b+c+d=4t-10$."),("Use the last equality",r"Also $t=a+b+c+d+5=4t-5$, so $3t=5$ and $t=5/3$."),("Compute the sum",r"$a+b+c+d=4(5/3)-10=-10/3$. The answer is $\boxed{-\frac{10}{3}}$.")],
17:[("Track amounts",r"Start with $4$ ounces coffee in cup 1 and $4$ ounces cream in cup 2."),("First transfer",r"Half the coffee is $2$ ounces, so cup 2 has $2$ ounces coffee and $4$ ounces cream, $6$ ounces total."),("Mixture transfer back",r"Cup 2 is $1/3$ coffee and $2/3$ cream. Half of it is $3$ ounces, containing $1$ ounce coffee and $2$ ounces cream."),("Final fraction",r"Cup 1 has $3$ ounces coffee and $2$ ounces cream, $5$ ounces total. The cream fraction is $\boxed{\frac25}$.")],
18:[("Classify visible dice",r"Corners show $3$ faces, edge-center dice show $2$ faces, and face-center dice show $1$ face."),("Minimize each type",r"On a standard die, opposite faces sum to $7$. The least visible sums are $1+2+3=6$ for a corner, $1+2=3$ for an edge-center die, and $1$ for a face-center die."),("Count positions",r"There are $8$ corners, $12$ edge-center dice, and $6$ face-center dice."),("Add",r"The minimum total is $8\cdot6+12\cdot3+6\cdot1=90$. The answer is $\boxed{90}$.")],
19:[("Use sectors",r"The reachable region outside the regular hexagon is made of circular sectors as the rope wraps around vertices."),("Main sector",r"At the tethered vertex, the outside angle is $240^\circ$. With radius $2$, the sector area is $\frac{240}{360}\pi(2)^2=\frac{8\pi}{3}$."),("Adjacent sectors",r"After wrapping around an adjacent vertex, $1$ yard of rope remains. The two adjacent contributions are $60^\circ$ sectors of radius $1$, total area $2\cdot\frac{60}{360}\pi=\frac{\pi}{3}$."),("Total",r"The reachable area is $\frac{8\pi}{3}+\frac{\pi}{3}=3\pi$. The answer is $\boxed{3\pi}$.")],
20:[("Choose coordinates",r"Place $A,B,C,D,E,F$ at $0,1,2,3,4,5$ on the $x$-axis and take $AG$ vertical. This preserves the needed ratio."),("Find $HC$",r"On line $GD$, the height decreases linearly from $G$ at $x=0$ to $D$ at $x=3$. At $C$, where $x=2$, the remaining fraction is $1/3$, so $HC=AG/3$."),("Find $JE$",r"On line $GF$, at $E$ where $x=4$ out of $5$, the remaining fraction is $1/5$, so $JE=AG/5$."),("Ratio",r"Therefore $HC/JE=(AG/3)/(AG/5)=5/3$. The answer is $\boxed{\frac53}$.")],
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
 rows=[r for r in rows if r['year']=='2002' and r['form']=='A' and 11<=int(r['problem_no'])<=20]
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
 prog.write_text(old+f'## Batch {BATCH_NUMBER}: 2002 AMC 10A Problem 11-20\n\n- Start time: {start}\n- End time: {end}\n- Processed contest: AMC 10\n- Processed range: 2002 AMC 10A Problem 11-20\n- Generated count: {len(items)}\n- Skipped count: 0\n- Validation result: passed\n- Commit hash: pending\n- Pushed: pending\n- Next batch should start from: 2002 AMC 10A Problem 21\n- Review notes: Problems 19 and 20 are geometry/diagram-dependent and should be reviewed with the original figures.\n',encoding='utf-8')
 (ROOT/'problem_pages_report.md').write_text('# Problem Pages Report\n\n'+f'- Total manifest entries: {len(merged)}\n- Latest batch: {BATCH_NUMBER} (2002 AMC 10A Problem 11-20)\n- Latest generated count: {len(items)}\n- MathJax validation: passed\n\n## Latest Batch Pages\n\n'+'\n'.join(f"- `{it['source']}` -> `amc10/problems/{it['slug']}/`" for it in items)+'\n',encoding='utf-8')
 (ROOT/'resume_prompt.md').write_text('Continue STEMHUB AMC problem page generation. Completed batch 2: 2002 AMC 10A Problem 11-20. Next start: 2002 AMC 10A Problem 21. Reuse scripts/batch_generate_problem_pages.py pattern. Validate MathJax, update manifest/report/progress, commit and push each batch. Latest commit hash pending until commit.\n',encoding='utf-8')
 print(json.dumps({'batch':BATCH_NUMBER,'generated':len(items),'start':start,'end':end,'next':'2002 AMC 10A Problem 21'},indent=2))
if __name__=='__main__': main()


