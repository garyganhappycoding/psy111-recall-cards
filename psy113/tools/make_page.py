import re,sys
src=open('index.html').read();s=src
def rep(a,b,n=1):
    global s
    c=s.count(a)
    assert c==n,(a[:80],c);s=s.replace(a,b)
# ---------- branding ----------
rep('<meta name="description" content="Tap-to-reveal recall cards and paraphrase tables for PSY 111.">','<meta name="description" content="Concept cards, a 50-question MCQ exam and journal-article practice for PSY 113 Scientific Thinking and Academic Writing.">')
rep('<title>PSY 111 Recall Cards</title>','<title>PSY 113 Trainer</title>')
rep('<div class="eyebrow" id="eyebrow">PSY 111</div>','<div class="eyebrow" id="eyebrow">PSY 113</div>')
rep('<h1>PSY 111 <em>recall</em> cards</h1>','<h1>PSY 113 <em>scientific thinking</em> trainer</h1>')
rep('<p class="sub">Pick a topic and a mode. Learn a card first or test yourself straight away, then mark each card as Understand, Not sure or Totally forgot so you can revise the weak ones.</p>',
    '<p class="sub">Learn the concepts lecture by lecture, sit a 50-question MCQ exam drawn from every lecture, then practise reading real journal articles to find the research question, hypothesis, variables and more.</p>')
rep('$("#eyebrow").textContent=`PSY 111 · ${deck}`;','$("#eyebrow").textContent=`PSY 113 · ${deck}`;')
# ---------- separate local storage (login token stays shared with PSY 111) ----------
for k in ["pr-deck","pr-mode","pr-qplan","pr-qrot","pr-quizlast","pr-spin-norep","pr-spun","pr-done2","pr-drafts2","pr-local-deck2","pr-status2","pr-attempts2"]:
    s=s.replace(f'"{k}"',f'"p113-{k[3:]}"')
# ---------- account storage: PSY 113 has its own table ----------
rep('const {error}=await sb.rpc("recall_save_state_v3",{p_token:token,p_done:[...done],p_drafts:drafts,p_cards:customCards?C:null,p_status:status,p_attempts:attempts});',
    'const {error}=await sb.rpc("p113_save_state",{p_token:token,p_done:[...done],p_drafts:drafts,p_cards:customCards?C:null,p_status:status,p_attempts:attempts,p_articles:artState,p_exams:exams});')
rep('const {data,error}=await sb.rpc("recall_get_state",{p_token:token});','const {data,error}=await sb.rpc("p113_get_state",{p_token:token});')
rep('  if(data.cards){C=withNewTopics(data.cards);customCards=true}','''  {const sa=data.articles||{};Object.keys(sa).forEach(k=>{const a=artState[k],b=sa[k];if(!a||(b.at||"")>(a.at||""))artState[k]={...b,best:Math.max(b.best||0,(a&&a.best)||0)};else artState[k]={...a,best:Math.max(a.best||0,b.best||0)}});store.set("p113-articles",artState);}
  {const seen=new Set(exams.map(x=>x.at));(data.exams||[]).forEach(x=>{if(!seen.has(x.at))exams.push(x)});exams.sort((a,b)=>a.at<b.at?1:-1);exams=exams.slice(0,30);store.set("p113-exams",exams);}
  if(data.cards){C=withNewTopics(data.cards);customCards=true}''')
rep('user=null;token=null;customCards=false;done=new Set();drafts={};status={};attempts={};C=defaults;','user=null;token=null;customCards=false;done=new Set();drafts={};status={};attempts={};artState={};exams=[];C=defaults;')
rep('["pr-token","p113-done2","p113-drafts2","p113-local-deck2","p113-status2","p113-attempts2"].forEach(','["pr-token","p113-done2","p113-drafts2","p113-local-deck2","p113-status2","p113-attempts2","p113-articles","p113-exams"].forEach(')
# ---------- no slide pictures for PSY 113: show "Lecture N · slides" as a line under the answer ----------
rep('function renderSrc(el,c){\n  const s=cardSrc(c);el.innerHTML="";','function renderSrc(el,c){\n  el.innerHTML="";el.hidden=true;return;\n  const s=cardSrc(c);')
rep('<div class="answer hidden" id="s-answer" aria-live="polite"></div>','<div class="answer hidden" id="s-answer" aria-live="polite"></div><div class="srcline" id="s-srcline2" hidden></div>')
rep('<div class="answer" id="s-learn-ans"></div>','<div class="answer" id="s-learn-ans"></div><div class="srcline" id="s-srcline1"></div>')
rep('$("#s-name").textContent=questionOf(c);','$("#s-name").textContent=questionOf(c);{const t=lecRef(c);$("#s-srcline1").textContent=t;$("#s-srcline2").textContent=t;$("#s-srcline1").hidden=!t;}')
rep('  if(!h){markDone(cur);$("#s-rate").hidden=false;','  $("#s-srcline2").hidden=h||!lecRef(byId(cur));\n  if(!h){markDone(cur);$("#s-rate").hidden=false;')
open('psy113/index.html','w').write(s)
print("base ok")

# =================== additions: MCQ exam + article trainer ===================
s=open('psy113/index.html').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    assert c==n,(a[:80],c);s=s.replace(a,b)
# ---- tabs + sections
rep('<button role="tab" id="tab-spin" aria-selected="false">Spin wheel</button>','<button role="tab" id="tab-spin" aria-selected="false">Spin wheel</button>\n    <button role="tab" id="tab-exam" aria-selected="false">MCQ exam</button>\n    <button role="tab" id="tab-art" aria-selected="false">Article practice</button>')
rep('''  <section id="view-spin" hidden>''','''  <section id="view-exam" hidden>
    <div class="exambox">
      <div><h2 class="xh">MCQ exam</h2><p class="note">Random questions drawn from every lecture, like the real paper. You see the right answer and why after each one.</p></div>
      <div class="field"><span class="label">How many questions</span><div class="seg" role="group" aria-label="Number of questions" id="ex-n"><button data-n="10">10</button><button data-n="25">25</button><button data-n="50">50</button></div></div>
      <div class="field"><span class="label">Lectures</span><div class="lecpick" id="ex-lecs"></div><span class="hint" id="ex-pool"></span></div>
      <div><button class="btn primary" id="ex-go">Start exam</button></div>
      <div class="field" id="ex-histbox" hidden><span class="label">Your past exams</span><ol class="exhist" id="ex-hist"></ol></div>
    </div>
  </section>

  <section id="view-art" hidden>
    <p class="note">Read a real psychology journal article and find its parts: the research question, hypothesis, variables, design and more. Tap sentences in the article or type your answer, then check. The articles go from easy to harder.</p>
    <div class="artgrid" id="artgrid"></div>
  </section>

  <section id="view-spin" hidden>''')
# ---- article sheet markup (before the lightbox)
rep('<div class="scrim" id="lbox" hidden>','''<div class="scrim" id="ascrim" hidden>
  <div class="sheet" id="asheet" role="dialog" aria-modal="true" aria-labelledby="a-title" tabindex="-1">
    <div class="sheet-in">
      <div class="a-head"><div class="tag" id="a-tag"></div><h3 id="a-title"></h3><div class="a-cite" id="a-cite"></div>
        <div class="seg a-tabs" role="group" aria-label="Show"><button data-t="read" aria-pressed="true">Article</button><button data-t="tasks" aria-pressed="false">Tasks <span id="a-tcount"></span></button></div></div>
      <div class="a-pick" id="a-pick" hidden><span id="a-picktext"></span><button class="btn" id="a-pickdone">Done</button></div>
      <div class="a-body" id="a-body"><div class="a-text" id="a-text"></div><div class="a-tasks" id="a-tasks"></div></div>
      <div class="sheet-foot a-foot"><button class="btn primary" id="a-check">Check my answers</button><button class="btn" id="a-reset">Start again</button><span class="spacer"></span><span class="count" id="a-score"></span><button class="btn" id="a-close">Close</button></div>
    </div>
  </div>
</div>

<div class="scrim" id="lbox" hidden>''')
# ---- CSS
rep('@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}','''.srcline{font-family:var(--mono);font-size:11px;letter-spacing:.04em;color:var(--muted);margin-top:2px}
/* exam setup */
.exambox{display:flex;flex-direction:column;gap:18px;max-width:760px;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:22px}
.xh{font-family:var(--display);font-weight:400;font-size:32px;margin:0 0 4px}
.lecpick{display:flex;flex-wrap:wrap;gap:8px}
.lecpick label{display:flex;align-items:center;gap:6px;font-size:13px;padding:6px 10px;border:1px solid var(--line);border-radius:999px;cursor:pointer;background:var(--bg)}
.lecpick input{accent-color:var(--accent)}
.exhist{margin:0;padding-left:20px;font-size:14px;display:flex;flex-direction:column;gap:4px}
.exhist .sc{font-weight:600}
/* article list */
.artgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.artcard{all:unset;cursor:pointer;display:flex;flex-direction:column;gap:8px;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:16px;border-top:4px solid var(--lv)}
.artcard:hover{border-color:var(--lv)}.artcard:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.artcard h4{font-family:var(--display);font-weight:400;font-size:21px;line-height:1.2;margin:0}
.artcard .meta{font-size:12px;color:var(--muted)}
.lvl{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--lv)}
.best{font-size:13px;font-weight:600}
/* article trainer: full screen */
#ascrim{padding:0}
#asheet{width:100%;height:100dvh;max-height:none;border-radius:0;display:flex;flex-direction:column;overflow:hidden}
#asheet>.sheet-in{flex:1;min-height:0;display:flex;flex-direction:column;gap:12px;width:min(1400px,100%);margin:0 auto;padding:18px 24px calc(12px + env(safe-area-inset-bottom))}
#asheet:focus{outline:none}
.a-head{flex-shrink:0;display:flex;flex-direction:column;gap:4px}
#asheet h3{font-size:clamp(22px,2.6vw,32px)}
.a-cite{font-size:12px;color:var(--muted)}.a-cite a{color:var(--accent)}
.a-tabs{display:none;align-self:flex-start;margin-top:6px}
.a-body{flex:1;min-height:0;display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:20px}
.a-text,.a-tasks{min-height:0;overflow:auto;overscroll-behavior:contain}
.a-text{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:18px 22px;font-size:16px;line-height:1.7}
.a-text h5{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:18px 0 6px}
.a-text h5:first-child{margin-top:0}
.a-text p{margin:0 0 10px}
.sent{border-radius:4px;padding:1px 0;box-decoration-break:clone;-webkit-box-decoration-break:clone;transition:background .15s}
.picking .sent{cursor:pointer}
.picking .sent:hover{background:color-mix(in srgb,var(--pc) 18%,transparent)}
.sent.sel{background:color-mix(in srgb,var(--sc) 28%,transparent);box-shadow:inset 0 -2px 0 var(--sc)}
.sent .stag{font-family:var(--mono);font-size:10px;font-weight:600;letter-spacing:.04em;color:var(--paper);background:var(--sc);border-radius:4px;padding:0 4px;margin-left:3px;vertical-align:1px}
.sent.key{outline:2px dashed var(--ok);outline-offset:1px}
.a-pick{flex-shrink:0;display:flex;align-items:center;gap:10px;justify-content:space-between;background:color-mix(in srgb,var(--pc) 14%,var(--paper));border:1px solid var(--pc);border-radius:10px;padding:8px 12px;font-size:14px}
.a-tasks{display:flex;flex-direction:column;gap:10px}
.task{background:var(--paper);border:1px solid var(--line);border-left:5px solid var(--tc);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:8px}
.task.on{box-shadow:0 0 0 2px var(--tc)}
.task-h{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.task-h b{font-size:15px}
.task-h .kind{font-size:12px;color:var(--muted)}
.task input[type=text]{font:inherit;font-size:15px;padding:9px 11px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);width:100%;box-sizing:border-box}
.task .picks{font-size:13px;color:var(--muted)}
.task .picks q{color:var(--ink);quotes:"“" "”"}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips button{all:unset;cursor:pointer;font-size:13px;padding:6px 11px;border:1.5px solid var(--line);border-radius:999px;background:var(--bg)}
.chips button[aria-pressed=true]{border-color:var(--tc);background:color-mix(in srgb,var(--tc) 16%,var(--paper));font-weight:600}
.chips button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.task .res{font-size:14px;border-top:1px dashed var(--line);padding-top:8px;display:flex;flex-direction:column;gap:4px}
.task .res .v{font-weight:600}.task .res .v.ok{color:var(--ok)}.task .res .v.part{color:var(--warn)}.task .res .v.bad{color:var(--bad)}
.task .res .model b{font-weight:600}
.task .res .why{color:var(--muted);font-size:13px}
.task .res .link{align-self:flex-start}
.a-foot{flex-shrink:0;padding-top:10px;border-top:1px solid var(--line)}
@media (max-width:900px),(orientation:portrait) and (max-width:1100px){
  .a-tabs{display:inline-flex}
  .a-body{grid-template-columns:minmax(0,1fr)}
  .a-body[data-show=read] .a-tasks,.a-body[data-show=tasks] .a-text{display:none}
}
@media (max-width:699px){
  #asheet>.sheet-in{padding:12px 14px calc(10px + env(safe-area-inset-bottom));gap:8px}
  .a-text{padding:14px;font-size:15px}
  .a-foot{flex-wrap:nowrap;gap:6px}.a-foot .btn{padding:9px 11px;white-space:nowrap}.a-foot .spacer{display:none}.a-foot #a-check{flex:1}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}''')
# ---- views
rep('function view(v){["cards","table","spin"].forEach(k=>{$("#view-"+k).hidden=k!==v;$("#tab-"+k).setAttribute("aria-selected",k===v)});render()}',
    'let curView="cards";\nfunction view(v){curView=v;["cards","table","spin","exam","art"].forEach(k=>{$("#view-"+k).hidden=k!==v;$("#tab-"+k).setAttribute("aria-selected",k===v)});$("#topics").hidden=v==="exam"||v==="art";render();if(v==="exam")renderExam();if(v==="art")renderArts()}')
rep('$("#tab-spin").onclick=()=>view("spin");','$("#tab-spin").onclick=()=>view("spin");$("#tab-exam").onclick=()=>view("exam");$("#tab-art").onclick=()=>view("art");')
# ---- MCQ inside the quiz engine
rep('function buildQuestion(item){\n  const c=byId(item.id);if(!c)return null;','''function buildQuestion(item){
  if(item.type==="mcq"){const m=MCQ[item.id];if(!m)return null;return {type:"mcq",id:m.id,stem:m.q,opts:shuffleArr(m.opts.slice()),right:m.opts[m.a],why:m.why,lec:m.lec}}
  const c=byId(item.id);if(!c)return null;''')
rep('  const c=byId(q.id);quiz.q=q;quiz.answered=false;\n  $("#q-tag").textContent=`Quiz · ${quiz.label}`;','  const c=byId(q.id);quiz.q=q;quiz.answered=false;\n  $("#q-tag").textContent=quiz.plan==="exam"?`MCQ exam · ${quiz.label}`:`Quiz · ${quiz.label}`;')
rep('  $("#q-type").textContent=QTLABEL[q.type];\n  const stem=$("#q-stem");stem.innerHTML="";','  $("#q-type").textContent=q.type==="mcq"?`Lecture ${q.lec}`:QTLABEL[q.type];\n  const stem=$("#q-stem");stem.innerHTML="";\n  if(q.type==="mcq")stem.append(q.stem);else')
rep('''  const q=quiz.q,c=byId(q.id),ok=btn.dataset.v===q.right;''','''  const q=quiz.q,ok=btn.dataset.v===q.right;
  if(q.type==="mcq"){
    document.querySelectorAll("#q-opts .qopt").forEach(b=>{b.disabled=true;if(b.dataset.v===q.right)b.classList.add("right")});
    if(!ok)btn.classList.add("wrong");if(ok)quiz.score++;else if(!quiz.missed.includes(q.id))quiz.missed.push(q.id);
    const fb=$("#q-feed");fb.className="qfeed "+(ok?"ok":"bad");fb.textContent=ok?"✓ Correct!":"✗ Not quite. The right answer is highlighted in green.";
    $("#q-anslabel").textContent=`Why · Lecture ${q.lec}`;$("#q-ans").hidden=false;$("#q-ans").textContent=q.why;$("#q-cmp").hidden=true;$("#q-src").hidden=true;
    $("#q-prog").textContent=`Question ${quiz.i+1} of ${quiz.items.length} · Score ${quiz.score}`;
    $("#q-after").hidden=false;$("#q-next").hidden=false;
    requestAnimationFrame(()=>{const bd=$("#q-play .q-body"),af=$("#q-after");if(getComputedStyle(bd).gridTemplateColumns.split(" ").length===1){bd.scrollTo({top:af.offsetTop-bd.offsetTop-8,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"})}});
    $("#q-next").textContent=quiz.i+1<quiz.items.length?"Next question →":"See my score →";$("#q-next").focus({preventScroll:true});return}
  const c=byId(q.id);''')
rep('''  const pname=(PLANS.find(p=>p[0]===quiz.plan)||[,"Quiz"])[1];''','''  const pname=quiz.plan==="exam"?"MCQ exam":(PLANS.find(p=>p[0]===quiz.plan)||[,"Quiz"])[1];''')
rep('''  quiz.missed.forEach(id=>{const c=byId(id);if(c){const sp=document.createElement("span");sp.textContent=c.name;mb.appendChild(sp)}});''','''  quiz.missed.forEach(id=>{const c=byId(id),m=MCQ[id];if(c||m){const sp=document.createElement("span");sp.textContent=c?c.name:(m.q.length>90?m.q.slice(0,88)+"…":m.q);mb.appendChild(sp)}});''')
rep('''  $("#q-markmiss").disabled=false;''','''  if(quiz.plan==="exam")$("#q-markmiss").hidden=true;
  if(quiz.plan==="exam"&&total&&!/missed$/.test(quiz.label)){exams.unshift({at:new Date().toISOString(),score:quiz.score,total,of:quiz.items.length});exams=exams.slice(0,30);store.set("p113-exams",exams);queueSync()}
  $("#q-markmiss").disabled=false;''')
rep('''$("#q-retry").onclick=()=>startQuiz(shuffleArr(quiz.missed.map(id=>({id,type:nextType(id)}))),quiz.label+" · missed",quiz.plan);''','''$("#q-retry").onclick=()=>startQuiz(shuffleArr(quiz.missed.map(id=>MCQ[id]?{id,type:"mcq"}:{id,type:nextType(id)})),quiz.label+" · missed",quiz.plan);''')
rep('function closeQuiz(){$("#qscrim").hidden=true;quiz=null;render()}','function closeQuiz(){const ex=quiz&&quiz.plan==="exam";$("#qscrim").hidden=true;quiz=null;render();if(ex)renderExam()}')
# ---- exam + article code, data loading
rep('''(async function boot(){
  try{const r=await fetch("cards.json",{cache:"no-store"});if(!r.ok)throw 0;defaults=await r.json()}catch(e){defaults=[];setStatus("Couldn't load the card deck.")}''','''/* ===== PSY 113: lecture references, MCQ exam, article practice ===== */
let MCQ={},ARTS=[],artState=store.get("p113-articles",{}),exams=store.get("p113-exams",[]);
function lecRef(c){const s=c&&c.src;if(!s||!s.lec)return "";const p=s.p||[];return `From Lecture ${s.lec}`+(p.length?` · slide${p.length>1?"s":""} ${p.join(", ")}`:"")}
let exN=store.get("p113-exn",50),exLecs=null;
function lecturesInBank(){return [...new Set(Object.values(MCQ).map(m=>m.lec))].sort((a,b)=>a-b)}
function renderExam(){
  const lecs=lecturesInBank();if(!exLecs)exLecs=new Set(store.get("p113-exlecs",lecs));
  document.querySelectorAll("#ex-n button").forEach(b=>{b.setAttribute("aria-pressed",+b.dataset.n===exN);b.onclick=()=>{exN=+b.dataset.n;store.set("p113-exn",exN);renderExam()}});
  const box=$("#ex-lecs");box.innerHTML="";
  lecs.forEach(l=>{const lab=document.createElement("label");const cb=document.createElement("input");cb.type="checkbox";cb.checked=exLecs.has(l);
    cb.onchange=()=>{cb.checked?exLecs.add(l):exLecs.delete(l);store.set("p113-exlecs",[...exLecs]);renderExam()};
    const n=Object.values(MCQ).filter(m=>m.lec===l).length;lab.append(cb,`Lecture ${l} (${n})`);box.appendChild(lab)});
  const pool=Object.values(MCQ).filter(m=>exLecs.has(m.lec));
  $("#ex-pool").textContent=pool.length?`${pool.length} questions in the bank for these lectures. Each exam picks ${Math.min(exN,pool.length)} at random, spread across the lectures.`:"Pick at least one lecture.";
  $("#ex-go").disabled=!pool.length;
  const h=$("#ex-hist");h.innerHTML="";$("#ex-histbox").hidden=!exams.length;
  exams.slice(0,8).forEach(x=>{const li=document.createElement("li");const sc=document.createElement("span");sc.className="sc";sc.textContent=`${x.score}/${x.total} (${Math.round(x.score/x.total*100)}%)`;li.append(sc,` · ${fmtWhen(x.at)}`+(x.total<x.of?` · stopped at ${x.total} of ${x.of}`:""));h.appendChild(li)});
}
function pickExam(n){
  // spread questions across lectures: round-robin over shuffled per-lecture pools
  const by={};Object.values(MCQ).filter(m=>exLecs.has(m.lec)).forEach(m=>(by[m.lec]=by[m.lec]||[]).push(m));
  Object.keys(by).forEach(k=>by[k]=shuffleArr(by[k]));const keys=shuffleArr(Object.keys(by));const out=[];
  while(out.length<n&&keys.some(k=>by[k].length)){for(const k of keys){if(out.length>=n)break;const m=by[k].pop();if(m)out.push(m)}}
  return shuffleArr(out).map(m=>({id:m.id,type:"mcq"}));
}
$("#ex-go").onclick=()=>{const items=pickExam(exN);if(items.length)startQuiz(items,`${items.length} questions`,"exam")};

/* article practice */
const TASKCOL=["#2f6f9f","#b2531f","#4b7d3a","#7a4fa3","#a3366a","#1f7f7a","#8a6d1f","#5a5f9e","#9c4a3c","#3f6e55"];
let art=null; // {a, sel:{key:Set|string}, picking:key|null, checked:bool, over:{key:true}}
function levelInfo(l){return [["Easy","var(--ok)"],["Easy","var(--ok)"],["Medium","var(--warn)"],["Harder","var(--bad)"]][Math.min(l,3)]||["",""]}
function renderArts(){
  const g=$("#artgrid");g.innerHTML="";
  ARTS.forEach((a,i)=>{const b=document.createElement("button");b.className="artcard";const [lv,col]=levelInfo(a.level);b.style.setProperty("--lv",col);
    const st=artState[a.id];
    b.innerHTML=`<span class="lvl"></span><h4></h4><span class="meta"></span><span class="best"></span>`;
    b.querySelector(".lvl").textContent=`Article ${i+1} · ${lv}`;b.querySelector("h4").textContent=a.short||a.title;
    b.querySelector(".meta").textContent=`${a.design} · ${a.items.length} things to find`;
    b.querySelector(".best").textContent=st&&st.best!=null?`Best score: ${st.best}%`:"Not tried yet";
    b.onclick=()=>openArticle(a.id);g.appendChild(b)});
}
function sentId(si,j){return si+"."+j}
function openArticle(id){
  const a=ARTS.find(x=>x.id===id);if(!a)return;
  const st=artState[id];const sel={};
  a.items.forEach(it=>{const v=st&&st.answers?st.answers[it.key]:null;sel[it.key]=it.kind==="sentence"?new Set(v||[]):(v||"")});
  art={a,sel,picking:null,checked:false,over:{}};
  const [lv]=levelInfo(a.level);$("#a-tag").textContent=`Article practice · ${lv}`;$("#a-title").textContent=a.title;
  const cite=$("#a-cite");cite.textContent=`${a.authors} (${a.year}). ${a.journal}. ${a.license}. `;
  if(a.url){const l=document.createElement("a");l.href=a.url;l.target="_blank";l.rel="noopener";l.textContent="Open the full article";cite.appendChild(l)}
  const tx=$("#a-text");tx.innerHTML="";
  a.text.forEach((sec,si)=>{const h=document.createElement("h5");h.textContent=sec.h;tx.appendChild(h);const p=document.createElement("p");
    sec.s.forEach((t,j)=>{const sp=document.createElement("span");sp.className="sent";sp.dataset.id=sentId(si,j);sp.textContent=t;sp.onclick=()=>pickSentence(sp.dataset.id);p.append(sp," ")});tx.appendChild(p)});
  $("#a-tcount").textContent=`(${a.items.length})`;
  setArtTab(matchMedia("(max-width:900px),(orientation:portrait) and (max-width:1100px)").matches?"tasks":"read");
  $("#ascrim").hidden=false;renderTasks();paintSentences();$("#a-score").textContent=st&&st.best!=null?`Best ${st.best}%`:"";
  $("#a-text").scrollTop=0;$("#a-tasks").scrollTop=0;$("#asheet").focus({preventScroll:true});
}
function setArtTab(t){$("#a-body").dataset.show=t;document.querySelectorAll(".a-tabs button").forEach(b=>b.setAttribute("aria-pressed",b.dataset.t===t))}
document.querySelectorAll(".a-tabs button").forEach(b=>b.onclick=()=>setArtTab(b.dataset.t));
function itemColor(k){const i=art.a.items.findIndex(x=>x.key===k);return TASKCOL[i%TASKCOL.length]}
function paintSentences(){
  const owners={};art.a.items.forEach(it=>{if(it.kind==="sentence")art.sel[it.key].forEach(id=>(owners[id]=owners[id]||[]).push(it))});
  const keys=new Set();if(art.checked)art.a.items.forEach(it=>{if(it.kind==="sentence")(it.ans||[]).forEach(id=>keys.add(id))});
  document.querySelectorAll("#a-text .sent").forEach(sp=>{
    sp.querySelectorAll(".stag").forEach(t=>t.remove());const o=owners[sp.dataset.id]||[];
    sp.classList.toggle("sel",!!o.length);if(o.length)sp.style.setProperty("--sc",itemColor(o[0].key));
    o.forEach(it=>{const t=document.createElement("span");t.className="stag";t.style.background=itemColor(it.key);t.textContent=it.tag||it.label;sp.appendChild(t)});
    sp.classList.toggle("key",keys.has(sp.dataset.id));
  });
  $("#a-text").classList.toggle("picking",!!art.picking);
  if(art.picking)$("#a-text").style.setProperty("--pc",itemColor(art.picking));
}
function pickSentence(id){
  if(!art||!art.picking)return;const s=art.sel[art.picking];s.has(id)?s.delete(id):s.add(id);art.checked=false;paintSentences();renderTasks();saveArtDraft();
}
function startPicking(k){
  art.picking=art.picking===k?null:k;
  const it=art.a.items.find(x=>x.key===k);
  $("#a-pick").hidden=!art.picking;if(art.picking){$("#a-pick").style.setProperty("--pc",itemColor(k));$("#a-picktext").textContent=`Tap the sentence(s) that give the ${it.label.toLowerCase()}. Tap again to unselect.`;
    if($("#a-body").dataset.show==="tasks"&&getComputedStyle($(".a-tabs")).display!=="none")setArtTab("read")}
  paintSentences();renderTasks();
}
$("#a-pickdone").onclick=()=>{const k=art.picking;art.picking=null;$("#a-pick").hidden=true;paintSentences();renderTasks();if(getComputedStyle($(".a-tabs")).display!=="none")setArtTab("tasks");const el=document.querySelector(`.task[data-k="${k}"]`);if(el)el.scrollIntoView({block:"nearest"})};
function normTxt(t){return (" "+t.toLowerCase().replace(/[^a-z0-9%]+/g," ")+" ")}
function markItem(it){
  const v=art.sel[it.key];
  if(art.over[it.key])return 1;
  if(it.kind==="sentence"){
    if(!v.size)return 0;const ans=new Set(it.ans||[]),ok=new Set([...(it.ans||[]),...(it.ok||[])]);
    const hit=[...v].some(id=>ans.has(id)),extra=[...v].filter(id=>!ok.has(id)).length;
    return hit?(extra?.5:1):0;
  }
  if(it.kind==="choice")return v===it.ans?1:0;
  const t=normTxt(v||"");if(t.trim().length<2)return 0;
  return (it.accept||[]).some(group=>group.every(w=>w.split("|").some(alt=>t.includes(" "+alt.toLowerCase()))))?1:0;
}
function renderTasks(){
  const box=$("#a-tasks");box.innerHTML="";
  art.a.items.forEach((it,i)=>{
    const d=document.createElement("div");d.className="task"+(art.picking===it.key?" on":"");d.dataset.k=it.key;d.style.setProperty("--tc",itemColor(it.key));
    const h=document.createElement("div");h.className="task-h";const b=document.createElement("b");b.textContent=`${i+1}. ${it.label}`;
    const kd=document.createElement("span");kd.className="kind";kd.textContent=it.kind==="sentence"?"Find it in the article":it.kind==="choice"?"Choose one":"Type your answer";
    h.append(b,kd);d.appendChild(h);
    if(it.prompt){const p=document.createElement("div");p.className="kind";p.style.fontSize="13px";p.style.color="var(--muted)";p.textContent=it.prompt;d.appendChild(p)}
    if(it.kind==="sentence"){
      const btn=document.createElement("button");btn.className="btn";btn.textContent=art.picking===it.key?"Done selecting":(art.sel[it.key].size?"Change selection":"Select in article");btn.onclick=()=>art.picking===it.key?$("#a-pickdone").click():startPicking(it.key);
      const pk=document.createElement("div");pk.className="picks";
      if(art.sel[it.key].size){[...art.sel[it.key]].forEach(id=>{const [si,j]=id.split(".").map(Number);const t=(art.a.text[si]||{s:[]}).s[j]||"";const q=document.createElement("q");q.textContent=t.length>110?t.slice(0,108)+"…":t;pk.append(q," ")})}else pk.textContent="Nothing selected yet.";
      d.append(btn,pk);
    }else if(it.kind==="choice"){
      const ch=document.createElement("div");ch.className="chips";
      it.options.forEach(o=>{const bt=document.createElement("button");bt.textContent=o;bt.setAttribute("aria-pressed",art.sel[it.key]===o);bt.onclick=()=>{art.sel[it.key]=o;art.checked=false;art.over[it.key]=false;renderTasks();paintSentences();saveArtDraft()};ch.appendChild(bt)});
      d.appendChild(ch);
    }else{
      const inp=document.createElement("input");inp.type="text";inp.value=art.sel[it.key];inp.placeholder=it.placeholder||"Type it in your own words…";
      inp.oninput=()=>{art.sel[it.key]=inp.value;art.over[it.key]=false;if(art.checked){art.checked=false;renderTasks();paintSentences();const n=document.querySelector(`.task[data-k="${it.key}"] input`);n.focus();n.setSelectionRange(n.value.length,n.value.length)}saveArtDraft()};
      inp.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();$("#a-check").click()}};
      d.appendChild(inp);
    }
    if(art.checked){
      const m=markItem(it),r=document.createElement("div");r.className="res";
      const v=document.createElement("span");v.className="v "+(m===1?"ok":m?"part":"bad");
      v.textContent=m===1?(art.over[it.key]?"✓ Marked correct by you":"✓ Correct"):m?"◐ Partly right: you picked the right sentence plus extra ones":(it.kind==="sentence"&&!art.sel[it.key].size?"✗ Not answered":"✗ Not quite");
      const mo=document.createElement("div");mo.className="model";const mb=document.createElement("b");mb.textContent="Answer: ";mo.append(mb,it.model);
      r.append(v,mo);
      if(it.why){const w=document.createElement("div");w.className="why";w.textContent=it.why;r.appendChild(w)}
      if(it.kind==="sentence"&&(it.ans||[]).length){const sh=document.createElement("button");sh.className="link";sh.textContent="Show it in the article";sh.onclick=()=>{setArtTab("read");const el=document.querySelector(`.sent[data-id="${it.ans[0]}"]`);if(el)el.scrollIntoView({block:"center",behavior:"smooth"})};r.appendChild(sh)}
      if(m<1&&it.kind==="text"&&(art.sel[it.key]||"").trim()){const ov=document.createElement("button");ov.className="link";ov.textContent="My answer means the same → mark it correct";ov.onclick=()=>{art.over[it.key]=true;scoreArt();renderTasks()};r.appendChild(ov)}
      d.appendChild(r);
    }
    box.appendChild(d);
  });
}
function saveArtDraft(){const id=art.a.id,prev=artState[id]||{};const answers={};art.a.items.forEach(it=>{const v=art.sel[it.key];answers[it.key]=v instanceof Set?[...v]:v});artState[id]={...prev,answers,at:new Date().toISOString()};store.set("p113-articles",artState);queueSync()}
function scoreArt(){
  const tot=art.a.items.length,got=art.a.items.reduce((s,it)=>s+markItem(it),0),pct=Math.round(got/tot*100);
  const id=art.a.id,prev=artState[id]||{};saveArtDraft();artState[id]={...artState[id],last:pct,best:Math.max(prev.best||0,pct)};store.set("p113-articles",artState);queueSync();
  $("#a-score").textContent=`Score ${pct}% · Best ${artState[id].best}%`;return pct;
}
$("#a-check").onclick=()=>{if(!art)return;art.picking=null;$("#a-pick").hidden=true;art.checked=true;scoreArt();renderTasks();paintSentences();if(getComputedStyle($(".a-tabs")).display!=="none")setArtTab("tasks");$("#a-tasks").scrollTop=0};
$("#a-reset").onclick=()=>{if(!art)return;art.a.items.forEach(it=>{art.sel[it.key]=it.kind==="sentence"?new Set():""});art.over={};art.checked=false;art.picking=null;$("#a-pick").hidden=true;saveArtDraft();renderTasks();paintSentences()};
function closeArticle(){$("#ascrim").hidden=true;art=null;renderArts()}
$("#a-close").onclick=closeArticle;
document.addEventListener("keydown",e=>{if($("#ascrim").hidden)return;if(e.key==="Escape"){if(art&&art.picking)$("#a-pickdone").click();else closeArticle()}},true);

(async function boot(){
  try{const r=await fetch("cards.json",{cache:"no-store"});if(!r.ok)throw 0;defaults=await r.json()}catch(e){defaults=[];setStatus("Couldn't load the card deck.")}
  try{const r=await fetch("mcq.json",{cache:"no-store"});if(r.ok){(await r.json()).forEach(m=>MCQ[m.id]=m)}}catch(e){}
  try{const r=await fetch("articles.json",{cache:"no-store"});if(r.ok)ARTS=await r.json()}catch(e){}''')
rep('  if(location.hash==="#table")view("table");else render();','  if(location.hash==="#table")view("table");else if(location.hash==="#exam")view("exam");else if(location.hash==="#articles")view("art");else render();')
open('psy113/index.html','w').write(s)
print("full ok")

# ---- topics in lecture order
s=open('psy113/index.html').read()
rep('function decks(){const seen=[...new Set(C.map(c=>c.deck))];return [...DECK_ORDER.filter(d=>seen.includes(d)),...seen.filter(d=>!DECK_ORDER.includes(d))]}',
    'function decks(){const seen=[...new Set(C.map(c=>c.deck))];const n=d=>{const c=C.find(x=>x.deck===d);const m=/^L(\\d+)/.exec(d);return c&&c.src&&c.src.lec||(m?+m[1]:999)};return seen.sort((a,b)=>n(a)-n(b))}')
open('psy113/index.html','w').write(s)
print("order ok")

s=open('psy113/index.html').read()
rep('.lecpick{display:flex;flex-wrap:wrap;gap:8px}','.lecpick{display:flex;flex-wrap:wrap;gap:8px}\n#ex-n{align-self:flex-start}\n.ascore{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:15px}\n.ascore b{font-size:20px}')
rep('.a-foot{flex-wrap:nowrap;gap:6px}.a-foot .btn{padding:9px 11px;white-space:nowrap}.a-foot .spacer{display:none}.a-foot #a-check{flex:1}','.a-foot{flex-wrap:nowrap;gap:6px}.a-foot .btn{padding:9px 11px;white-space:nowrap}.a-foot .spacer,.a-foot .count{display:none}.a-foot #a-check{flex:1}')
rep('''function renderTasks(){
  const box=$("#a-tasks");box.innerHTML="";''','''function renderTasks(){
  const box=$("#a-tasks");box.innerHTML="";
  if(art.checked){const tot=art.a.items.length,got=art.a.items.reduce((s,it)=>s+markItem(it),0);const d=document.createElement("div");d.className="ascore";const b=document.createElement("b");b.textContent=`${Math.round(got/tot*100)}%`;d.append(b,` · ${got} of ${tot} correct. Read the answers below, then try the ones you missed again.`);box.appendChild(d)}''')
open('psy113/index.html','w').write(s)
print("polish ok")

s=open('psy113/index.html').read()
rep('  const g=$("#artgrid");g.innerHTML="";','  const g=$("#artgrid");g.innerHTML="";\n  if(!ARTS.length){const p=document.createElement("p");p.className="note";p.textContent="The practice articles are being added. Check back soon.";g.appendChild(p);return}')
open('psy113/index.html','w').write(s)
print("empty ok")

s=open('psy113/index.html').read()
rep('const cite=$("#a-cite");cite.textContent=`${a.authors} (${a.year}). ${a.journal}. ${a.license}. `;',
    'const cite=$("#a-cite");cite.textContent=a.based_on?`Practice article written for PSY 113 (details simplified). Adapted from: ${a.based_on} `:`${a.authors} (${a.year}). ${a.journal}. ${a.license}. `;')
rep('if(a.url){const l=document.createElement("a");l.href=a.url;l.target="_blank";l.rel="noopener";l.textContent="Open the full article";cite.appendChild(l)}',
    'if(a.url){const l=document.createElement("a");l.href=a.url;l.target="_blank";l.rel="noopener";l.textContent=a.based_on?"Original study":"Open the full article";cite.appendChild(l)}')
rep('b.querySelector(".meta").textContent=`${a.design} · ${a.items.length} things to find`;',
    'b.querySelector(".meta").textContent=`${a.design} · ${a.items.length} things to find`+(a.based_on?` · based on ${(a.based_on.match(/^[^(]*\\(\\d{4}\\)/)||[a.based_on])[0]}`:"");')
open('psy113/index.html','w').write(s)
print("cite ok")

s=open('psy113/index.html').read()
rep('  const lecs=lecturesInBank();if(!exLecs)exLecs=new Set(store.get("p113-exlecs",lecs));','  const lecs=lecturesInBank();ensureLecs();')
rep('cb.onchange=()=>{cb.checked?exLecs.add(l):exLecs.delete(l);store.set("p113-exlecs",[...exLecs]);renderExam()};','cb.onchange=()=>{cb.checked?exLecs.add(l):exLecs.delete(l);store.set("p113-exoff",lecturesInBank().filter(x=>!exLecs.has(x)));renderExam()};')
rep('function pickExam(n){','function ensureLecs(){if(!exLecs){const off=new Set(store.get("p113-exoff",[]));exLecs=new Set(lecturesInBank().filter(l=>!off.has(l)))}}\nfunction pickExam(n){ensureLecs();')
open('psy113/index.html','w').write(s)
print("exam fix ok")

s=open('psy113/index.html').read()
rep('then practise reading real journal articles to find the research question, hypothesis, variables and more.','then practise reading journal-style articles based on real studies to find the research question, hypothesis, variables and more.')
rep('<p class="note">Read a real psychology journal article and find its parts: the research question, hypothesis, variables, design and more. Tap sentences in the article or type your answer, then check. The articles go from easy to harder.</p>',
    '<p class="note">Each practice article is a short, simplified version of a real published psychology study (the original is linked inside). Find its parts: the research question, hypothesis, variables, definitions, method, theoretical framework and more. Tap sentences in the article or type your answer, then check. Articles go from easy to harder.</p>')
open('psy113/index.html','w').write(s)
print("text ok")
