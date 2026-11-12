# Adds Exam mode (50 MCQ + 2 essays) and Essay practice to the PSY 111 page (index.html).
import sys
p='index.html';s=open(p).read()
def rep(a,b,n=1):
    global s
    c=s.count(a);assert c==n,(a[:80],c);s=s.replace(a,b)
# ---- tabs + views
rep('<button role="tab" id="tab-spin" aria-selected="false">Spin wheel</button>','<button role="tab" id="tab-spin" aria-selected="false">Spin wheel</button>\n    <button role="tab" id="tab-xexam" aria-selected="false">Exam mode</button>\n    <button role="tab" id="tab-essays" aria-selected="false">Essay practice</button>')
rep('''  <section id="view-spin" hidden>''','''  <section id="view-xexam" hidden>
    <div class="exambox">
      <div><h2 class="xh">Exam mode</h2><p class="note">Practise under exam conditions: Section A has 50 scenario-based MCQs from every chapter, and Section B has 2 essay questions. You get no feedback until you submit. Then you see your MCQ score, why each answer is right, and the model answers with a checklist to mark your essays.</p></div>
      <div class="field"><span class="label">Paper</span><div class="seg" role="group" aria-label="Paper" id="xx-fmt"><button data-f="full">Full exam (50 MCQ + 2 essays)</button><button data-f="mcq">MCQs only</button><button data-f="essay">Essays only</button></div></div>
      <div class="field"><span class="label">Timer</span><div class="seg" role="group" aria-label="Timer" id="xx-time"><button data-t="0">No timer</button><button data-t="60">60 min</button><button data-t="90">90 min</button><button data-t="120">2 hours</button><button data-t="150">2.5 hours</button></div></div>
      <div><button class="btn primary" id="xx-go">Start exam</button> <span class="hint" id="xx-bank"></span></div>
      <div class="field" id="xx-histbox" hidden><span class="label">Your past exams</span><ol class="exhist" id="xx-hist"></ol></div>
    </div>
  </section>

  <section id="view-essays" hidden>
    <p class="note">Every essay question, for practice. Each one is a scenario worth 20 marks: write your answer, then reveal the model answer and tick the checklist to mark yourself.</p>
    <div class="toolbar" id="es-filter"></div>
    <div class="artgrid" id="es-grid"></div>
  </section>

  <section id="view-spin" hidden>''')
# ---- sheets (exam + single essay)
rep('<div class="scrim" id="lbox" hidden>','''<div class="scrim" id="xscrim" hidden>
  <div class="sheet xsheet" id="xsheet" role="dialog" aria-modal="true" aria-labelledby="x-title" tabindex="-1">
    <div class="sheet-in">
      <div class="x-head"><div><div class="tag" id="x-tag">PSY 111 exam</div><h3 id="x-title"></h3></div><div class="x-right"><span class="x-timer" id="x-timer" hidden></span><span class="count" id="x-prog"></span></div></div>
      <div class="x-nav" id="x-nav" aria-label="Question navigator"></div>
      <div class="x-body" id="x-body"></div>
      <div class="sheet-foot x-foot" id="x-foot"></div>
    </div>
  </div>
</div>

<div class="scrim" id="lbox" hidden>''')
# ---- CSS
rep('@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}','''/* exam setup + essay list (shared look) */
.exambox{display:flex;flex-direction:column;gap:18px;max-width:820px;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:22px}
.exambox .seg{align-self:flex-start;flex-wrap:wrap}
.xh{font-family:var(--display);font-weight:400;font-size:32px;margin:0 0 4px}
.exhist{margin:0;padding-left:20px;font-size:14px;display:flex;flex-direction:column;gap:4px}.exhist .sc{font-weight:600}
.artgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}
.artcard{all:unset;cursor:pointer;display:flex;flex-direction:column;gap:8px;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:16px;border-top:4px solid var(--lv)}
.artcard:hover{border-color:var(--lv)}.artcard:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.artcard h4{font-family:var(--display);font-weight:400;font-size:21px;line-height:1.2;margin:0}
.artcard .meta{font-size:12px;color:var(--muted)}.lvl{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--lv)}.best{font-size:13px;font-weight:600}
/* exam sheet: full screen */
#xscrim{padding:0}
.xsheet{width:100%;height:100dvh;max-height:none;border-radius:0;display:flex;flex-direction:column;overflow:hidden}
.xsheet:focus{outline:none}
.xsheet>.sheet-in{flex:1;min-height:0;display:flex;flex-direction:column;gap:12px;width:min(1200px,100%);margin:0 auto;padding:18px 24px calc(12px + env(safe-area-inset-bottom))}
.x-head{flex-shrink:0;display:flex;justify-content:space-between;align-items:flex-end;gap:12px}
.xsheet h3{font-size:clamp(22px,2.4vw,30px)}
.x-right{display:flex;flex-direction:column;align-items:flex-end;gap:4px}
.x-timer{font-family:var(--mono);font-size:18px;font-weight:600}.x-timer.low{color:var(--bad)}
.x-nav{flex-shrink:0;display:flex;flex-wrap:wrap;gap:4px;max-height:76px;overflow:auto}
.x-nav button{all:unset;cursor:pointer;min-width:26px;height:26px;padding:0 4px;box-sizing:border-box;text-align:center;font-family:var(--mono);font-size:11px;line-height:24px;border-radius:6px;border:1px solid var(--line);background:var(--paper);color:var(--muted)}
.x-nav button.ans{background:color-mix(in srgb,var(--accent) 16%,var(--paper));color:var(--ink);border-color:color-mix(in srgb,var(--accent) 40%,var(--line))}
.x-nav button.flag{box-shadow:inset 0 -3px 0 var(--warn)}
.x-nav button.cur{outline:2px solid var(--accent);outline-offset:1px;color:var(--ink)}
.x-nav button.ok{background:var(--ok-bg);border-color:var(--ok);color:var(--ok)}.x-nav button.no{background:var(--bad-bg);border-color:var(--bad);color:var(--bad)}
.x-nav button.ess{padding:0 8px}
.x-body{flex:1;min-height:0;overflow:auto;overscroll-behavior:contain;display:flex;flex-direction:column;gap:14px}
.x-q{font-size:clamp(17px,1.8vw,21px);font-weight:600;line-height:1.45}
.x-q .sub{display:block;font-size:12px;font-family:var(--mono);font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.x-opts{display:flex;flex-direction:column;gap:10px}
.x-opts .qopt[aria-pressed=true]{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 10%,var(--paper))}
.x-foot{flex-shrink:0;padding-top:12px;border-top:1px solid var(--line);flex-wrap:wrap}
.x-review{display:flex;flex-direction:column;gap:12px}
.x-rev{background:var(--paper);border:1px solid var(--line);border-left:5px solid var(--bad);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:6px;font-size:15px}
.x-rev.ok{border-left-color:var(--ok)}
.x-rev .yours{color:var(--bad)}.x-rev .right{color:var(--ok);font-weight:600}.x-rev .why{color:var(--muted);font-size:14px}
.x-score{display:flex;flex-wrap:wrap;gap:12px}
.x-score div{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:12px 16px;min-width:150px}
.x-score b{display:block;font-family:var(--display);font-weight:400;font-size:34px;line-height:1.1}
.x-score span{font-size:12px;color:var(--muted)}
/* essay component */
.es-scn{background:var(--paper);border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:12px;padding:14px 16px;font-size:16px;line-height:1.65;white-space:pre-line}
.es-part{display:flex;flex-direction:column;gap:8px}
.es-part .pq{font-weight:600;font-size:16px}
.es-part .pq small{font-family:var(--mono);font-weight:500;color:var(--muted);margin-left:6px}
.es-part textarea{font:inherit;font-size:15px;line-height:1.6;min-height:150px;resize:vertical;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink)}
.es-wc{font-size:12px;color:var(--muted);align-self:flex-end}
.es-mark{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px}
.es-mark>div{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:12px 14px;font-size:14px;line-height:1.6;white-space:pre-line}
.es-mark .lab{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:6px;white-space:normal}
.es-check{display:flex;flex-direction:column;gap:6px}
.es-check label{display:flex;gap:8px;align-items:flex-start;font-size:14px;cursor:pointer}
.es-check input{accent-color:var(--ok);margin-top:3px;width:16px;height:16px;flex-shrink:0}
.es-check .m{margin-left:auto;font-family:var(--mono);font-size:12px;color:var(--muted);white-space:nowrap}
.es-tot{font-weight:600}
.es-mist{font-size:14px;color:var(--muted)}.es-mist b{color:var(--ink)}
@media (max-width:820px){.es-mark{grid-template-columns:minmax(0,1fr)}}
@media (max-width:699px){
  .xsheet>.sheet-in{padding:12px 14px calc(10px + env(safe-area-inset-bottom));gap:8px}
  .x-nav{max-height:58px}
  .x-foot .btn{padding:9px 11px}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}''')
# ---- views
rep('function view(v){["cards","table","spin"].forEach(k=>{$("#view-"+k).hidden=k!==v;$("#tab-"+k).setAttribute("aria-selected",k===v)});render()}',
    'function view(v){["cards","table","spin","xexam","essays"].forEach(k=>{$("#view-"+k).hidden=k!==v;$("#tab-"+k).setAttribute("aria-selected",k===v)});$("#topics").hidden=v==="xexam"||v==="essays";render();if(v==="xexam")renderXSetup();if(v==="essays")renderEssayList()}')
rep('$("#tab-spin").onclick=()=>view("spin");','$("#tab-spin").onclick=()=>view("spin");$("#tab-xexam").onclick=()=>view("xexam");$("#tab-essays").onclick=()=>view("essays");')
# ---- account sync: exams + essays
rep('const {error}=await sb.rpc("recall_save_state_v3",{p_token:token,p_done:[...done],p_drafts:drafts,p_cards:customCards?C:null,p_status:status,p_attempts:attempts});',
    'const {error}=await sb.rpc("recall_save_state_v4",{p_token:token,p_done:[...done],p_drafts:drafts,p_cards:customCards?C:null,p_status:status,p_attempts:attempts,p_exams:xExams,p_essays:esState});')
rep('const {data,error}=await sb.rpc("recall_get_state",{p_token:token});','const {data,error}=await sb.rpc("recall_get_state_v2",{p_token:token});')
rep('  if(data.cards){C=withNewTopics(data.cards);customCards=true}','''  {const seen=new Set(xExams.map(x=>x.at));(data.exams||[]).forEach(x=>{if(!seen.has(x.at))xExams.push(x)});xExams.sort((a,b)=>a.at<b.at?1:-1);xExams=xExams.slice(0,30);store.set("pr-xexams",xExams);}
  {const se=data.essays||{};Object.keys(se).forEach(k=>{const a=esState[k],b=se[k];const best=Math.max((a&&a.best)||0,(b&&b.best)||0);esState[k]=(!a||(b.at||"")>(a.at||""))?{...b,best}:{...a,best}});store.set("pr-essays",esState);}
  if(data.cards){C=withNewTopics(data.cards);customCards=true}''')
rep('user=null;token=null;customCards=false;done=new Set();drafts={};status={};attempts={};C=defaults;','user=null;token=null;customCards=false;done=new Set();drafts={};status={};attempts={};xExams=[];esState={};C=defaults;')
rep('["pr-token","pr-done2","pr-drafts2","pr-local-deck2","pr-status2","pr-attempts2"].forEach(','["pr-token","pr-done2","pr-drafts2","pr-local-deck2","pr-status2","pr-attempts2","pr-xexams","pr-essays"].forEach(')
# ---- JS: exam + essays
rep('''(async function boot(){''','''/* ===== Exam mode (Section A: 50 MCQ, Section B: 2 essays) + Essay practice ===== */
let XMCQ=[],ESSAYS=[],xExams=store.get("pr-xexams",[]),esState=store.get("pr-essays",{});
let xFmt=store.get("pr-xfmt","full"),xTime=store.get("pr-xtime",0),X=null,xTick=null;
const ETYPE={A:"Analyse the scenario",B:"Compare theories",C:"Design an intervention",D:"Cross-chapter case"};
function fmtDur(sec){sec=Math.max(0,Math.round(sec));const h=Math.floor(sec/3600),m=Math.floor(sec%3600/60),s2=sec%60;return (h?h+":"+String(m).padStart(2,"0"):m)+":"+String(s2).padStart(2,"0")}
function segSet(sel,attr,val,cb){document.querySelectorAll(sel+" button").forEach(b=>{b.setAttribute("aria-pressed",String(b.dataset[attr])===String(val));b.onclick=()=>cb(b.dataset[attr])})}
function renderXSetup(){
  segSet("#xx-fmt","f",xFmt,v=>{xFmt=v;store.set("pr-xfmt",v);renderXSetup()});
  segSet("#xx-time","t",xTime,v=>{xTime=+v;store.set("pr-xtime",xTime);renderXSetup()});
  $("#xx-bank").textContent=`${XMCQ.length} exam MCQs and ${ESSAYS.length} essay questions in the bank. Every attempt is a new random paper.`;
  const h=$("#xx-hist");h.innerHTML="";$("#xx-histbox").hidden=!xExams.length;
  xExams.slice(0,8).forEach(x=>{const li=document.createElement("li");const sc=document.createElement("span");sc.className="sc";
    const parts=[];if(x.mcqTotal)parts.push(`MCQ ${x.mcq}/${x.mcqTotal}`);if(x.essayTotal)parts.push(`Essays ${x.essay==null?"not marked":x.essay+"/"+x.essayTotal}`);
    sc.textContent=parts.join(" · ");li.append(sc,` · ${fmtWhen(x.at)}`+(x.mins?` · ${x.mins} min`:""));h.appendChild(li)});
}
function pickXMCQ(n){
  const by={};XMCQ.forEach(m=>(by[m.deck]=by[m.deck]||[]).push(m));Object.keys(by).forEach(k=>by[k]=shuffleArr(by[k]));
  const keys=shuffleArr(Object.keys(by)),out=[];while(out.length<n&&keys.some(k=>by[k].length)){for(const k of keys){if(out.length>=n)break;const m=by[k].pop();if(m)out.push(m)}}
  return shuffleArr(out).map(m=>({id:m.id,opts:shuffleArr(m.opts.slice()),pick:null,flag:false}));
}
function pickEssays(n){
  // two essays from different areas where possible, least-practised first
  const seen=new Set(),out=[];const pool=shuffleArr(ESSAYS.slice()).sort((a,b)=>((esState[a.id]||{}).best!=null)-((esState[b.id]||{}).best!=null));
  for(const e of pool){if(out.length>=n)break;if(e.decks.some(d=>seen.has(d)))continue;out.push(e);e.decks.forEach(d=>seen.add(d))}
  for(const e of pool){if(out.length>=n)break;if(!out.includes(e))out.push(e)}
  return out.map(e=>({id:e.id,ans:{}}));
}
const XM=id=>XMCQ.find(m=>m.id===id),XE=id=>ESSAYS.find(e=>e.id===id);
$("#xx-go").onclick=()=>{
  const mcq=xFmt==="essay"?[]:pickXMCQ(50),ess=xFmt==="mcq"?[]:pickEssays(2);
  if(!mcq.length&&!ess.length)return;
  X={mcq,ess,i:0,started:Date.now(),limit:xTime*60,submitted:false,confirm:false,ticks:{}};
  $("#xscrim").hidden=false;$("#x-timer").hidden=!xTime;clearInterval(xTick);if(xTime)xTick=setInterval(xTimer,1000);xTimer();renderX();$("#xsheet").focus({preventScroll:true});
};
function xTimer(){if(!X||X.submitted||!X.limit)return;const left=X.limit-(Date.now()-X.started)/1000;const t=$("#x-timer");t.textContent=`⏱ ${fmtDur(left)} left`;t.classList.toggle("low",left<300);if(left<=0){clearInterval(xTick);submitX(true)}}
function xSlots(){return [...X.mcq.map((m,i)=>({k:"m",i})),...X.ess.map((e,i)=>({k:"e",i}))]}
function renderX(){
  const slots=xSlots(),cur=slots[X.i];
  // navigator
  const nav=$("#x-nav");nav.innerHTML="";
  slots.forEach((sl,j)=>{const b=document.createElement("button");
    if(sl.k==="m"){const it=X.mcq[sl.i];b.textContent=sl.i+1;if(X.submitted){b.className=it.pick===XM(it.id).opts[XM(it.id).a]?"ok":"no"}else{if(it.pick!=null)b.classList.add("ans");if(it.flag)b.classList.add("flag")}}
    else{b.textContent=`Essay ${sl.i+1}`;b.classList.add("ess");const e=X.ess[sl.i];if(Object.values(e.ans).some(t=>t.trim()))b.classList.add("ans")}
    if(j===X.i)b.classList.add("cur");b.setAttribute("aria-label",sl.k==="m"?`Question ${sl.i+1}`:`Essay ${sl.i+1}`);b.onclick=()=>{X.i=j;X.confirm=false;renderX()};nav.appendChild(b)});
  const answered=X.mcq.filter(m=>m.pick!=null).length;
  $("#x-prog").textContent=X.submitted?"Submitted":`${answered}/${X.mcq.length} MCQs answered`+(X.ess.length?` · ${X.ess.filter(e=>Object.values(e.ans).some(t=>t.trim())).length}/${X.ess.length} essays started`:"");
  const body=$("#x-body");body.innerHTML="";body.scrollTop=0;const foot=$("#x-foot");foot.innerHTML="";
  if(X.submitted&&X.i===-1)return renderXResults();
  if(cur.k==="m"){
    const it=X.mcq[cur.i],m=XM(it.id);$("#x-title").textContent=`Section A · Question ${cur.i+1} of ${X.mcq.length}`;
    const q=document.createElement("div");q.className="x-q";const sub=document.createElement("span");sub.className="sub";sub.textContent=m.deck;q.append(sub,m.q);body.appendChild(q);
    const box=document.createElement("div");box.className="x-opts";
    it.opts.forEach((o,k)=>{const b=document.createElement("button");b.className="qopt";const key=document.createElement("span");key.className="key";key.textContent="ABCD"[k];const tx=document.createElement("span");tx.textContent=o;b.append(key,tx);
      b.setAttribute("aria-pressed",it.pick===o);
      if(X.submitted){b.disabled=true;if(o===m.opts[m.a])b.classList.add("right");else if(o===it.pick)b.classList.add("wrong")}
      else b.onclick=()=>{it.pick=o;X.confirm=false;renderX()};
      box.appendChild(b)});
    body.appendChild(box);
    if(X.submitted){const w=document.createElement("div");w.className="x-rev"+(it.pick===m.opts[m.a]?" ok":"");w.innerHTML='<span class="right"></span><span class="why"></span>';w.querySelector(".right").textContent=(it.pick===m.opts[m.a]?"✓ Correct: ":it.pick==null?"Not answered. Answer: ":"✗ Answer: ")+m.opts[m.a];w.querySelector(".why").textContent=m.why;body.appendChild(w)}
  }else{
    const e=X.ess[cur.i],es=XE(e.id);$("#x-title").textContent=`Section B · Essay ${cur.i+1} of ${X.ess.length} · ${es.total} marks`;
    renderEssayInto(body,es,e.ans,X.submitted?{mark:true,ticks:(X.ticks[e.id]=X.ticks[e.id]||{}),onTick:()=>{saveXMarks();renderXNavOnly()}}:{onInput:()=>{}});
  }
  // footer
  const mk=(t,c,fn,cls)=>{const b=document.createElement("button");b.className="btn"+(cls?" "+cls:"");b.textContent=t;b.onclick=fn;foot.appendChild(b);return b};
  mk("← Prev","",()=>{X.i=Math.max(0,X.i-1);X.confirm=false;renderX()}).disabled=X.i===0;
  mk("Next →","",()=>{X.i=Math.min(slots.length-1,X.i+1);X.confirm=false;renderX()}).disabled=X.i===slots.length-1;
  if(cur.k==="m"&&!X.submitted){const f=mk(X.mcq[cur.i].flag?"⚑ Flagged":"⚑ Flag for review","",()=>{X.mcq[cur.i].flag=!X.mcq[cur.i].flag;renderX()});f.setAttribute("aria-pressed",X.mcq[cur.i].flag)}
  const sp=document.createElement("span");sp.className="spacer";foot.appendChild(sp);
  if(!X.submitted){
    const left=X.mcq.length-answered;
    const sb=mk(X.confirm?(left?`Submit with ${left} unanswered?`:"Yes, submit"):"Submit exam","",()=>{if(!X.confirm){X.confirm=true;renderX();return}submitX(false)},"primary");
    mk("Quit","",()=>{if(confirmQuit()){closeX()}});
  }else{mk("See my results","",()=>{X.i=-1;renderX()},"primary");mk("Close","",closeX)}
}
function renderXNavOnly(){}
function confirmQuit(){if(X.quitArm){return true}X.quitArm=true;setTimeout(()=>{if(X)X.quitArm=false},3000);const b=[...$("#x-foot").querySelectorAll(".btn")].find(x=>x.textContent==="Quit");if(b)b.textContent="Tap again to quit (answers will be lost)";return false}
function submitX(auto){
  X.submitted=true;clearInterval(xTick);$("#x-timer").hidden=true;
  X.mcqScore=X.mcq.filter(it=>it.pick===XM(it.id).opts[XM(it.id).a]).length;
  X.mins=Math.round((Date.now()-X.started)/60000);
  X.rec={at:new Date().toISOString(),mcq:X.mcqScore,mcqTotal:X.mcq.length,essay:X.ess.length?null:undefined,essayTotal:X.ess.reduce((s,e)=>s+XE(e.id).total,0)||undefined,mins:X.mins};
  xExams.unshift(X.rec);xExams=xExams.slice(0,30);store.set("pr-xexams",xExams);queueSync();
  // essays written in the exam also count as essay-practice attempts
  X.ess.forEach(e=>{const prev=esState[e.id]||{};esState[e.id]={...prev,ans:{...e.ans},at:new Date().toISOString()}});store.set("pr-essays",esState);
  X.i=-1;X.auto=auto;renderX();
}
function essayScore(es,ticks){let t=0;es.parts.forEach((p,pi)=>{(ticks[pi]||[]).forEach(k=>{const pt=p.points[k];if(pt)t+=pt.m})});return t}
function saveXMarks(){
  if(!X||!X.rec)return;let tot=0;X.ess.forEach(e=>{const es=XE(e.id),tk=X.ticks[e.id]||{},sc=essayScore(es,tk);tot+=sc;
    const prev=esState[e.id]||{};esState[e.id]={...prev,ticks:tk,score:sc,best:Math.max(prev.best||0,sc),at:new Date().toISOString()}});
  X.rec.essay=tot;store.set("pr-xexams",xExams);store.set("pr-essays",esState);queueSync();
  const el=$("#x-esstot");if(el)el.textContent=`${tot}/${X.rec.essayTotal}`;
}
function renderXResults(){
  $("#x-title").textContent=X.auto?"Time's up! Your results":"Your results";
  const body=$("#x-body"),foot=$("#x-foot");
  const sc=document.createElement("div");sc.className="x-score";
  const box=(big,small,id)=>{const d=document.createElement("div");const b=document.createElement("b");b.textContent=big;if(id)b.id=id;const s2=document.createElement("span");s2.textContent=small;d.append(b,s2);sc.appendChild(d)};
  if(X.mcq.length)box(`${X.mcqScore}/${X.mcq.length}`,`Section A · ${Math.round(X.mcqScore/X.mcq.length*100)}%`);
  if(X.ess.length){X.ess.forEach(e=>{X.ticks[e.id]=X.ticks[e.id]||{}});box(`${X.rec.essay==null?0:X.rec.essay}/${X.rec.essayTotal}`,"Section B · tick the checklists to mark","x-esstot")}
  box(fmtDur(X.mins*60),"Time used");
  body.appendChild(sc);
  if(X.ess.length){const p=document.createElement("p");p.className="note";p.textContent="Mark your essays: open Essay 1 and Essay 2 in the bar above, compare with the model answer and tick each checklist point you really covered.";body.appendChild(p)}
  if(X.mcq.length){
    const wrong=X.mcq.map((it,i)=>({it,i,m:XM(it.id)})).filter(x=>x.it.pick!==x.m.opts[x.m.a]);
    const h=document.createElement("div");h.className="label";h.textContent=wrong.length?`Review the ${wrong.length} MCQs you missed`:"You got every MCQ right!";body.appendChild(h);
    const rv=document.createElement("div");rv.className="x-review";
    wrong.forEach(({it,i,m})=>{const d=document.createElement("div");d.className="x-rev";
      const q=document.createElement("div");q.textContent=`Q${i+1}. ${m.q}`;q.style.fontWeight="600";
      const y=document.createElement("span");y.className="yours";y.textContent=it.pick==null?"You didn't answer.":`Your answer: ${it.pick}`;
      const r=document.createElement("span");r.className="right";r.textContent=`Answer: ${m.opts[m.a]}`;
      const w=document.createElement("span");w.className="why";w.textContent=m.why;d.append(q,y,r,w);rv.appendChild(d)});
    body.appendChild(rv);
  }
  const mk=(t,fn,cls)=>{const b=document.createElement("button");b.className="btn"+(cls?" "+cls:"");b.textContent=t;b.onclick=fn;foot.appendChild(b)};
  if(X.ess.length)mk("Mark Essay 1 →",()=>{X.i=X.mcq.length;renderX()},"primary");
  const sp=document.createElement("span");sp.className="spacer";foot.appendChild(sp);mk("Close",closeX);
}
function closeX(){clearInterval(xTick);$("#xscrim").hidden=true;X=null;if(!$("#view-xexam").hidden)renderXSetup();if(!$("#view-essays").hidden)renderEssayList()}

/* shared essay renderer: write mode, or mark mode (model answer + checklist) */
function wc(t){return (t.trim().match(/\\S+/g)||[]).length}
function renderEssayInto(box,es,ans,opt){
  const h=document.createElement("div");h.className="lvl";h.style.setProperty("--lv","var(--accent)");h.textContent=`Type ${es.type} · ${ETYPE[es.type]||""} · ${es.decks.join(", ")}`;box.appendChild(h);
  const sc=document.createElement("div");sc.className="es-scn";sc.textContent=es.scenario;box.appendChild(sc);
  es.parts.forEach((p,pi)=>{
    const d=document.createElement("div");d.className="es-part";
    const q=document.createElement("div");q.className="pq";q.textContent=`${p.label} ${p.q}`;const mk=document.createElement("small");mk.textContent=`[${p.marks} marks]`;q.appendChild(mk);d.appendChild(q);
    if(!opt.mark){
      const ta=document.createElement("textarea");ta.value=ans[pi]||"";ta.placeholder="Write your answer…";ta.setAttribute("aria-label",`Answer to part ${p.label}`);
      const w=document.createElement("span");w.className="es-wc";w.textContent=`${wc(ta.value)} words`;
      ta.oninput=()=>{ans[pi]=ta.value;w.textContent=`${wc(ta.value)} words`;opt.onInput&&opt.onInput()};
      d.append(ta,w);
    }else{
      const g=document.createElement("div");g.className="es-mark";
      const yours=document.createElement("div");const l1=document.createElement("div");l1.className="lab";l1.textContent="Your answer";yours.append(l1,(ans[pi]||"").trim()||"(not answered)");
      const model=document.createElement("div");const l2=document.createElement("div");l2.className="lab";l2.textContent="Model answer";model.append(l2,p.model);
      g.append(yours,model);d.appendChild(g);
      const ck=document.createElement("div");ck.className="es-check";const l3=document.createElement("div");l3.className="label";l3.textContent="Tick what your answer really covered";ck.appendChild(l3);
      const tk=(opt.ticks[pi]=opt.ticks[pi]||[]);
      p.points.forEach((pt,k)=>{const lab=document.createElement("label");const cb=document.createElement("input");cb.type="checkbox";cb.checked=tk.includes(k);
        cb.onchange=()=>{const i2=tk.indexOf(k);if(cb.checked&&i2<0)tk.push(k);if(!cb.checked&&i2>=0)tk.splice(i2,1);partTot.textContent=`${p.points.reduce((s,x,j)=>s+(tk.includes(j)?x.m:0),0)}/${p.marks}`;opt.onTick&&opt.onTick()};
        const t=document.createElement("span");t.textContent=pt.t;const m=document.createElement("span");m.className="m";m.textContent=`+${pt.m}`;lab.append(cb,t,m);ck.appendChild(lab)});
      const partTot=document.createElement("span");partTot.className="es-tot";partTot.textContent=`${p.points.reduce((s,x,j)=>s+(tk.includes(j)?x.m:0),0)}/${p.marks}`;ck.appendChild(partTot);
      d.appendChild(ck);
    }
    box.appendChild(d);
  });
  if(opt.mark&&es.mistakes&&es.mistakes.length){const m=document.createElement("div");m.className="es-mist";const b=document.createElement("b");b.textContent="Common mistakes: ";m.append(b,es.mistakes.join(" · "));box.appendChild(m)}
}

/* essay practice page */
let esType="all";
function renderEssayList(){
  const f=$("#es-filter");f.innerHTML="";
  [["all","All types"],...Object.entries(ETYPE).map(([k,v])=>[k,`${k} · ${v}`])].forEach(([k,t])=>{const b=document.createElement("button");b.className="chip";b.textContent=t;b.setAttribute("aria-pressed",esType===k);b.onclick=()=>{esType=k;renderEssayList()};f.appendChild(b)});
  const g=$("#es-grid");g.innerHTML="";
  ESSAYS.filter(e=>esType==="all"||e.type===esType).forEach(e=>{const b=document.createElement("button");b.className="artcard";b.style.setProperty("--lv",{A:"var(--accent)",B:"var(--warn)",C:"var(--ok)",D:"var(--bad)"}[e.type]||"var(--accent)");
    const st=esState[e.id];b.innerHTML='<span class="lvl"></span><h4></h4><span class="meta"></span><span class="best"></span>';
    b.querySelector(".lvl").textContent=`Type ${e.type} · ${ETYPE[e.type]||""}`;b.querySelector("h4").textContent=e.title;b.querySelector(".meta").textContent=e.decks.join(" · ");
    b.querySelector(".best").textContent=st&&st.best!=null?`Best: ${st.best}/${e.total}`:(st&&st.ans&&Object.values(st.ans).some(t=>t&&t.trim())?"Draft saved":"Not tried yet");
    b.onclick=()=>openEssay(e.id);g.appendChild(b)});
}
let EP=null;
function openEssay(id){
  const es=XE(id);if(!es)return;const st=esState[id]||{};
  EP={es,ans:{...(st.ans||{})},ticks:{},marking:false};
  X=null;$("#xscrim").hidden=false;$("#x-timer").hidden=true;$("#x-nav").innerHTML="";renderEP();$("#xsheet").focus({preventScroll:true});
}
function saveEPDraft(){const id=EP.es.id,prev=esState[id]||{};esState[id]={...prev,ans:{...EP.ans},at:new Date().toISOString()};store.set("pr-essays",esState);queueSync()}
function renderEP(){
  $("#x-tag").textContent="Essay practice";$("#x-title").textContent=EP.es.title;
  const words=Object.values(EP.ans).reduce((s,t)=>s+wc(t||""),0);$("#x-prog").textContent=EP.marking?`Score ${essayScore(EP.es,EP.ticks)}/${EP.es.total}`:`${words} words · ${EP.es.total} marks`;
  const body=$("#x-body");body.innerHTML="";const foot=$("#x-foot");foot.innerHTML="";
  let t=null;renderEssayInto(body,EP.es,EP.ans,EP.marking?{mark:true,ticks:EP.ticks,onTick:()=>{const sc=essayScore(EP.es,EP.ticks),id=EP.es.id,prev=esState[id]||{};esState[id]={...prev,ans:{...EP.ans},ticks:EP.ticks,score:sc,best:Math.max(prev.best||0,sc),at:new Date().toISOString()};store.set("pr-essays",esState);queueSync();$("#x-prog").textContent=`Score ${sc}/${EP.es.total}`}}:{onInput:()=>{clearTimeout(t);t=setTimeout(saveEPDraft,600);const w=Object.values(EP.ans).reduce((s,x)=>s+wc(x||""),0);$("#x-prog").textContent=`${w} words · ${EP.es.total} marks`}});
  const mk=(tx,fn,cls)=>{const b=document.createElement("button");b.className="btn"+(cls?" "+cls:"");b.textContent=tx;b.onclick=fn;foot.appendChild(b)};
  if(!EP.marking)mk("Show model answer & mark →",()=>{saveEPDraft();EP.marking=true;renderEP();body.scrollTop=0},"primary");
  else mk("← Back to my answer",()=>{EP.marking=false;renderEP()});
  const sp=document.createElement("span");sp.className="spacer";foot.appendChild(sp);
  mk("Close",()=>{saveEPDraft();EP=null;$("#x-tag").textContent="PSY 111 exam";closeX()});
}
document.addEventListener("keydown",e=>{
  if($("#xscrim").hidden||!X||X.submitted&&X.i===-1)return;
  if(e.target.tagName==="TEXTAREA"||e.target.tagName==="INPUT")return;
  const slots=xSlots(),cur=slots[X.i];if(!cur)return;
  if(e.key==="ArrowRight"){X.i=Math.min(slots.length-1,X.i+1);renderX();e.preventDefault()}
  else if(e.key==="ArrowLeft"){X.i=Math.max(0,X.i-1);renderX();e.preventDefault()}
  else if(cur.k==="m"&&!X.submitted){const k="abcd".indexOf(e.key.toLowerCase())>=0?"abcd".indexOf(e.key.toLowerCase()):"1234".indexOf(e.key);if(k>=0){X.mcq[cur.i].pick=X.mcq[cur.i].opts[k];renderX()}}
},true);

(async function boot(){
  try{const r=await fetch("exam-mcq.json",{cache:"no-store"});if(r.ok)XMCQ=await r.json()}catch(e){}
  try{const r=await fetch("essays.json",{cache:"no-store"});if(r.ok)ESSAYS=await r.json()}catch(e){}''')
rep('  if(location.hash==="#table")view("table");else render();','  if(location.hash==="#table")view("table");else if(location.hash==="#exam")view("xexam");else if(location.hash==="#essays")view("essays");else render();')
open(p,'w').write(s);print("exam added")
