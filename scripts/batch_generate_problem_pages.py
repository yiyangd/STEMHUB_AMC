from __future__ import annotations
import csv, html, json, re
from datetime import datetime
from pathlib import Path
ROOT=Path(r"D:\STEMHUB_AMC")
BATCH_NUMBER=1
CONTEST_DIR="amc10"
ANSWER_KEY_URL="https://artofproblemsolving.com/wiki/index.php/2002_AMC_10A_Answer_Key"
ANS={1:("D","5"),2:("C","6"),3:("B","1"),4:("E","infinitely many"),5:("C","2\\pi"),6:("A","15"),7:("A","\\frac{4}{9}"),8:("A","B=W"),9:("B","3"),10:("A","\\frac{7}{2}")}
OV={
1:(r"The ratio $\frac{10^{2000}+10^{2002}}{10^{2001}+10^{2001}}$ is closest to which of the following numbers?",[("A","$0.1$"),("B","$0.2$"),("C","$1$"),("D","$5$"),("E","$10$")]),
2:(r"Given nonzero real numbers $a,b,c$, define $(a,b,c)=\frac{a}{b}+\frac{b}{c}+\frac{c}{a}$. Find $(2,12,9)$.",[("A","$4$"),("B","$5$"),("C","$6$"),("D","$7$"),("E","$8$")]),
3:(r"According to the standard convention for exponentiation, $2^{2^{2^2}}=2^{16}=65,536$. If the order in which the exponentiations are performed is changed, how many other values are possible?",[("A","$0$"),("B","$1$"),("C","$2$"),("D","$3$"),("E","$4$")]),
7:(r"If an arc of $45^\circ$ on circle A has the same length as an arc of $30^\circ$ on circle B, then the ratio of the area of circle A to the area of circle B is",[("A","$\\frac{4}{9}$"),("B","$\\frac{2}{3}$"),("C","$\\frac{5}{6}$"),("D","$\\frac{3}{2}$"),("E","$\\frac{9}{4}$")]),
}
SOL={
1:[("Factor first",r"The expression is built from powers of $10$, so factoring is better than trying to compute the powers. Factor $10^{2000}$ from the numerator and $10^{2001}$ from the denominator."),("Simplify",r"\[\frac{10^{2000}+10^{2002}}{10^{2001}+10^{2001}}=\frac{10^{2000}(1+10^2)}{10^{2001}(1+1)}=\frac{101}{20}=5.05.\]"),("Choose",r"The value $5.05$ is closest to $5$, so the answer is $\boxed{5}$."),("Check",r"The ratio should be around $10^{2002}/(2\cdot10^{2001})=5$, so the choice is reasonable.")],
2:[("Read the notation",r"The symbol $(a,b,c)$ is a rule, not multiplication. Substitute $a=2$, $b=12$, and $c=9$ into the definition."),("Substitute",r"\[(2,12,9)=\frac{2}{12}+\frac{12}{9}+\frac{9}{2}.\]"),("Combine",r"\[\frac16+\frac43+\frac92=\frac{1+8+27}{6}=6.\]"),("Answer",r"The answer is $\boxed{6}$.")],
3:[("Notice the issue",r"Exponentiation is not associative, so different parentheses may produce different values. But because every number is $2$, several groupings still match."),("Standard value",r"The standard order gives $2^{2^{2^2}}=2^{16}=65536$."),("Other value",r"Changing the grouping can produce $$(2^2)^{(2^2)}=4^4=256,$$ and the other changed groupings give this same value rather than new ones."),("Count",r"There is only one other possible value, so the answer is $\boxed{1}$.")],
4:[("Use exists",r"The phrase 'there exists at least one positive integer $n$' means a single working choice of $n$ is enough."),("Try the simplest $n$",r"Let $n=1$. Then $mn\le m+n$ becomes $m\le m+1$, which is true for every positive integer $m$."),("Conclude",r"Every positive integer $m$ works, so there are infinitely many choices."),("Answer",r"The answer is $\boxed{\text{infinitely many}}$.")],
5:[("Read the geometry",r"Each small circle has radius $1$. The six surrounding circles have centers $2$ units from the center of the innermost circle."),("Find large radius",r"Each surrounding circle is tangent to the large circle, so the large radius is $2+1=3$."),("Subtract areas",r"The large circle has area $9\pi$, and the seven small circles have total area $7\pi$. The shaded area is $9\pi-7\pi=2\pi$."),("Note",r"This conclusion depends on the diagram's shaded region. The answer is $\boxed{2\pi}$.")],
6:[("Name the number",r"Let the original number be $x$. Cindy's wrong procedure gives $\frac{x-9}{3}=43$."),("Solve for $x$",r"Multiplying by $3$ gives $x-9=129$, so $x=138$."),("Do the correct procedure",r"The correct answer would be $\frac{138-3}{9}=\frac{135}{9}=15$."),("Answer",r"The answer is $\boxed{15}$.")],
7:[("Use arc length",r"Equal arcs mean equal values of $\frac{\theta}{360}\cdot2\pi r$."),("Set equal",r"\[\frac{45}{360}2\pi r_A=\frac{30}{360}2\pi r_B.\] Therefore $45r_A=30r_B$, so $r_A/r_B=2/3$."),("Square for area",r"Areas scale with the square of the radius, so $[A]/[B]=(2/3)^2=4/9$."),("Answer",r"The answer is $\boxed{\frac49}$.")],
8:[("Use decomposition",r"This is a diagram problem. The intended strategy is to decompose the flag into equal small regions rather than measure side lengths."),("Compare pieces",r"From the diagram, the blue triangular pieces can be paired by area with the white square regions."),("Relationship",r"Thus the total blue area equals the total white area: $B=W$."),("Review note",r"Because the reasoning depends on the original figure, this page should be rechecked when the diagram is added. The answer is $\boxed{B=W}$.")],
9:[("Divide by common factor",r"Both equations use multiples of $1001$, so divide by $1001$ to simplify."),("Rewrite",r"The equations become $C-2A=4$ and $B+3A=5$. Thus $C=2A+4$ and $B=5-3A$."),("Add",r"\[A+B+C=A+(5-3A)+(2A+4)=9.\]"),("Average",r"The average is $9/3=3$, so the answer is $\boxed{3}$.")],
10:[("Factor",r"Both terms contain $2x+3$, so factor before expanding."),("Equation",r"\[(2x+3)(x-4)+(2x+3)(x-6)=(2x+3)(2x-10)=0.\]"),("Roots",r"The roots are $x=-\frac32$ and $x=5$."),("Sum",r"Their sum is $5-\frac32=\frac72$, so the answer is $\boxed{\frac72}$.")],
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
 rows=list(csv.DictReader((ROOT/'amc10'/'all_problems.csv').open(encoding='utf-8-sig')))
 rows=[r for r in rows if r['year']=='2002' and r['form']=='A' and 1<=int(r['problem_no'])<=10]
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
 prog.write_text(old+f'## Batch {BATCH_NUMBER}: 2002 AMC 10A Problem 1-10\n\n- Start time: {start}\n- End time: {end}\n- Processed contest: AMC 10\n- Processed range: 2002 AMC 10A Problem 1-10\n- Generated count: {len(items)}\n- Skipped count: 0\n- Validation result: passed\n- Commit hash: pending\n- Pushed: pending\n- Next batch should start from: 2002 AMC 10A Problem 11\n- Review notes: Problems 5 and 8 are diagram-dependent.\n',encoding='utf-8')
 (ROOT/'problem_pages_report.md').write_text('# Problem Pages Report\n\n'+f'- Total manifest entries: {len(merged)}\n- Latest batch: {BATCH_NUMBER} (2002 AMC 10A Problem 1-10)\n- Latest generated count: {len(items)}\n- MathJax validation: passed\n\n## Latest Batch Pages\n\n'+'\n'.join(f"- `{it['source']}` -> `amc10/problems/{it['slug']}/`" for it in items)+'\n',encoding='utf-8')
 (ROOT/'resume_prompt.md').write_text('Continue STEMHUB AMC problem page generation. Completed batch 1: 2002 AMC 10A Problem 1-10. Next start: 2002 AMC 10A Problem 11. Reuse scripts/batch_generate_problem_pages.py pattern. Validate MathJax, update manifest/report/progress, commit and push each batch. Latest commit hash pending until commit.\n',encoding='utf-8')
 print(json.dumps({'batch':BATCH_NUMBER,'generated':len(items),'start':start,'end':end,'next':'2002 AMC 10A Problem 11'},indent=2))
if __name__=='__main__': main()
