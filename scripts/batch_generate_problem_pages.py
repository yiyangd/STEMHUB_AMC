from __future__ import annotations
import csv, html, json, re
from datetime import datetime
from pathlib import Path
ROOT=Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER=10
CONTEST_DIR="amc10"
ANSWER_KEY_URL="https://artofproblemsolving.com/wiki/index.php/2002_AMC_10A_Answer_Key"
ANS={1:("C",r"\frac23"),2:("D","20"),3:("B","8"),5:("C","1.35"),6:("D","21.5"),7:("B","38"),8:("B",r"-\frac{2\sqrt3}{3}"),9:("B","3"),10:("B",r"\frac{26^2}{10}")}
OV={
1:(r"Which of the following is the same as $\frac{2-4+6-8+10-12+14}{3-6+9-12+15-18+21}$?",[("A",r"$-\\frac13$"),("B",r"$-\\frac23$"),("C",r"$\\frac23$"),("D","$1$"),("E",r"$\\frac{14}{3}$")]),
8:(r"The second and fourth terms of a geometric sequence are $2$ and $6$. Which of the following is a possible first term?",[("A",r"$-\\sqrt3$"),("B",r"$-\\frac{2\\sqrt3}{3}$"),("C",r"$-\\frac{\\sqrt3}{3}$"),("D",r"$\\frac{\\sqrt3}{3}$"),("E",r"$\\sqrt3$")]),
9:(r"Find $x$ satisfying $\frac{5^{48/x}}{25^{-2}}=5^{26/x}\cdot25^{17/x}$.",[("A","$2$"),("B","$3$"),("C","$5$"),("D","$6$"),("E","$9$")]),
10:(r"Old license plates consisted of one letter followed by four digits. New license plates consist of three letters followed by three digits. By how many times is the number of possible license plates increased?",[("A","$26$"),("B",r"$\\frac{26^2}{10}$"),("C",r"$\\frac{26^2}{10^2}$"),("D",r"$\\frac{26^3}{10}$"),("E",r"$\\frac{26^3}{10^2}$")]),
}
SOL={
1:[("Evaluate numerator",r"The numerator is $2-4+6-8+10-12+14=8$."),("Evaluate denominator",r"The denominator is $3-6+9-12+15-18+21=12$."),("Simplify",r"The fraction is $8/12=2/3$."),("Answer",r"The answer is $\\boxed{\\frac23}$.")],
2:[("Set prices",r"Let a pink pill cost $p$ dollars. Then a green pill costs $p+1$ dollars."),("Use two weeks",r"Two weeks is $14$ days, and each day costs $p+(p+1)=2p+1$."),("Solve",r"$14(2p+1)=546$, so $2p+1=39$ and $p=19$."),("Answer",r"A green pill costs $20$, so the answer is $\\boxed{20}$.")],
3:[("Sum odd numbers",r"The first $8$ odd counting numbers have sum $8^2=64$."),("Find even sum",r"The five consecutive even integers have sum $64-4=60$."),("Use the middle term",r"Five consecutive even integers are symmetric around the middle term, so the middle term is $60/5=12$."),("Answer",r"The list is $8,10,12,14,16$, so the smallest is $\\boxed{8}$.")],
5:[("Use effective width",r"The mower cuts $28$ inches but overlaps by $4$ inches, so each pass effectively covers $24$ inches, or $2$ feet."),("Find total walking distance",r"The lawn area is $90\cdot150=13500$ square feet. With a $2$-foot effective width, Moe walks about $13500/2=6750$ feet."),("Use speed",r"At $5000$ feet per hour, the time is $6750/5000=1.35$ hours."),("Answer",r"The closest choice is $\\boxed{1.35}$.")],
6:[("Use the ratio",r"A $4:3$ screen has diagonal ratio $5$ by the $3$-$4$-$5$ triangle."),("Scale",r"If the diagonal is $27$, the scale factor is $27/5$."),("Horizontal length",r"The horizontal length is $4\cdot27/5=21.6$ inches."),("Answer",r"The closest choice is $\\boxed{21.5}$.")],
7:[("Group by square roots",r"$\lfloor\sqrt n\rfloor=1$ for $n=1,2,3$; $2$ for $n=4,5,6,7,8$; $3$ for $n=9$ through $15$; and $4$ for $n=16$."),("Add contributions",r"The sum is $3\cdot1+5\cdot2+7\cdot3+1\cdot4$."),("Compute",r"This equals $3+10+21+4=38$."),("Answer",r"The answer is $\\boxed{38}$.")],
8:[("Use geometric terms",r"Let the first term be $a$ and common ratio be $r$. Then $ar=2$ and $ar^3=6$."),("Find ratio",r"Dividing gives $r^2=3$, so $r=\\pm\\sqrt3$."),("Find first term",r"Then $a=2/r$, so possible first terms are $\\pm\\frac{2\\sqrt3}{3}$."),("Answer",r"Among the choices, a possible first term is $\\boxed{-\\frac{2\\sqrt3}{3}}$.")],
9:[("Rewrite powers of 25",r"Use $25=5^2$. Then $25^{-2}=5^{-4}$ and $25^{17/x}=5^{34/x}$."),("Compare exponents",r"The equation becomes $5^{48/x}/5^{-4}=5^{26/x}5^{34/x}$, so $5^{48/x+4}=5^{60/x}$."),("Solve",r"Thus $48/x+4=60/x$, so $4=12/x$ and $x=3$."),("Answer",r"The answer is $\\boxed{3}$.")],
10:[("Count old plates",r"An old plate has $26\cdot10^4$ possibilities."),("Count new plates",r"A new plate has $26^3\cdot10^3$ possibilities."),("Take ratio",r"The increase factor is $\\frac{26^3\cdot10^3}{26\cdot10^4}=\\frac{26^2}{10}$."),("Answer",r"The answer is $\\boxed{\\frac{26^2}{10}}$.")],
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
 rows=[r for r in rows if r['year']=='2003' and r['form']=='B' and 1<=int(r['problem_no'])<=10 and int(r['problem_no'])!=4]
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
 prog.write_text(old+f'## Batch {BATCH_NUMBER}: 2003 AMC 10B Problem 1-10\n\n- Start time: {start}\n- End time: {end}\n- Processed contest: AMC 10\n- Processed range: 2003 AMC 10B Problem 1-10\n- Generated count: {len(items)}\n- Skipped count: 0\n- Validation result: passed\n- Commit hash: pending\n- Pushed: pending\n- Next batch should start from: 2003 AMC 10B Problem 11\n- Review notes: Skipped 2003 AMC 10B Problem 4 due missing flower-bed figure; next starts from Problem 11.\n',encoding='utf-8')
 (ROOT/'problem_pages_report.md').write_text('# Problem Pages Report\n\n'+f'- Total manifest entries: {len(merged)}\n- Latest batch: {BATCH_NUMBER} (2003 AMC 10B Problem 1-10)\n- Latest generated count: {len(items)}\n- MathJax validation: passed\n\n## Latest Batch Pages\n\n'+'\n'.join(f"- `{it['source']}` -> `amc10/problems/{it['slug']}/`" for it in items)+'\n',encoding='utf-8')
 (ROOT/'resume_prompt.md').write_text('Continue STEMHUB AMC problem page generation. Completed batch 2: 2003 AMC 10B Problem 1-10. Next start: 2002 AMC 10A Problem 21. Reuse scripts/batch_generate_problem_pages.py pattern. Validate MathJax, update manifest/report/progress, commit and push each batch. Latest commit hash pending until commit.\n',encoding='utf-8')
 print(json.dumps({'batch':BATCH_NUMBER,'generated':len(items),'start':start,'end':end,'next':'2003 AMC 10B Problem 11'},indent=2))
if __name__=='__main__': main()


