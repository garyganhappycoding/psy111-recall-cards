"""Add the Mistake book to PSY 111 Exam mode (save wrong MCQs, own notes, review, practise)."""
import pathlib
P = pathlib.Path(__file__).resolve().parent.parent / "index.html"
s = P.read_text()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

# ---------- CSS ----------
rep(".x-rev.ok{border-left-color:var(--ok)}",
""".x-rev.ok{border-left-color:var(--ok)}
.mbadd{all:unset;cursor:pointer;align-self:flex-start;font-size:13px;font-weight:600;padding:6px 12px;border-radius:999px;border:1px dashed var(--accent);color:var(--accent);margin-top:2px}
.mbadd[aria-pressed="true"]{border-style:solid;background:var(--accent);color:var(--paper)}
.mbadd:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.mbhead{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
.mbbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.mblist{display:flex;flex-direction:column;gap:14px;margin-top:12px}
.mbcard{background:var(--paper);border:1px solid var(--line);border-left:5px solid var(--bad);border-radius:14px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.mbcard.done{border-left-color:var(--ok);opacity:.85}
.mbcard .top{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;font-size:12px;color:var(--muted)}
.mbcard .top .deck{font-family:var(--mono);text-transform:uppercase;letter-spacing:.04em}
.mbcard .q{font-weight:600;font-size:16px;line-height:1.45}
.mbcard ol{margin:0;padding-left:22px;display:flex;flex-direction:column;gap:3px;font-size:15px}
.mbcard ol li.right{color:var(--ok);font-weight:600}.mbcard ol li.yours{color:var(--bad);text-decoration:line-through}
.mbcard .why{color:var(--muted);font-size:14px}
.mbcard .ans{display:flex;flex-direction:column;gap:4px;font-size:15px}
.mbcard .ans .yours{color:var(--bad)}.mbcard .ans .right{color:var(--ok);font-weight:600}
.mbcard label.nl{font-size:13px;font-weight:600;margin-top:4px}
.mbcard textarea{min-height:84px}
.mbcard .acts{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.mbcard .saved{font-size:12px;color:var(--muted)}
.mbempty{background:var(--paper);border:1px dashed var(--line);border-radius:14px;padding:22px;text-align:center;color:var(--muted);margin-top:12px}
#tab-mistakes .n{font-family:var(--mono);font-size:11px;margin-left:5px;padding:1px 6px;border-radius:999px;background:var(--bad);color:var(--paper)}""")

# ---------- tab + view ----------
rep('<button role="tab" id="tab-essays" aria-selected="false">Essay practice</button>',
    '<button role="tab" id="tab-essays" aria-selected="false">Essay practice</button>\n    <button role="tab" id="tab-mistakes" aria-selected="false">Mistake book</button>')
rep('''  <section id="view-spin" hidden>''',
'''  <section id="view-mistakes" hidden>
    <div class="mbhead"><p class="note" style="margin:0">MCQs you saved from Exam mode. Write your own notes on why the answer is right, then practise them again until you can mark them as mastered.</p></div>
    <div class="toolbar" id="mb-state"></div>
    <div class="toolbar sub2" id="mb-decks"></div>
    <div class="mbbar"><button class="btn primary" id="mb-practise">Practise these</button><label class="hint"><input type="checkbox" id="mb-hide"> Hide answers (test yourself first)</label></div>
    <div class="mblist" id="mb-list"></div>
  </section>

  <section id="view-spin" hidden>''')

rep('''function view(v){["cards","table","spin","xexam","essays"].forEach(k=>{$("#view-"+k).hidden=k!==v;$("#tab-"+k).setAttribute("aria-selected",k===v)});$("#topics").hidden=v==="xexam"||v==="essays";render();if(v==="xexam")renderXSetup();if(v==="essays")renderEssayList()}''',
'''function view(v){["cards","table","spin","xexam","essays","mistakes"].forEach(k=>{$("#view-"+k).hidden=k!==v;$("#tab-"+k).setAttribute("aria-selected",k===v)});$("#topics").hidden=v==="xexam"||v==="essays"||v==="mistakes";render();if(v==="xexam")renderXSetup();if(v==="essays")renderEssayList();if(v==="mistakes")renderMistakes()}''')
rep('''$("#tab-essays").onclick=()=>view("essays");''', '''$("#tab-essays").onclick=()=>view("essays");$("#tab-mistakes").onclick=()=>view("mistakes");''')

# ---------- sync ----------
rep('''sb.rpc("recall_save_state_v4",{p_token:token,p_done:[...done],p_drafts:drafts,p_cards:customCards?C:null,p_status:status,p_attempts:attempts,p_exams:xExams,p_essays:esState});''',
    '''sb.rpc("recall_save_state_v5",{p_token:token,p_done:[...done],p_drafts:drafts,p_cards:customCards?C:null,p_status:status,p_attempts:attempts,p_exams:xExams,p_essays:esState,p_mistakes:mistakes});''')
rep('''sb.rpc("recall_get_state_v2",{p_token:token});''', '''sb.rpc("recall_get_state_v3",{p_token:token});''')
rep('''store.set("pr-essays",esState);}
  if(data.cards)''',
'''store.set("pr-essays",esState);}
  {const sm=data.mistakes||{};Object.keys(sm).forEach(k=>{const a=mistakes[k],b=sm[k];if(!a||(b.at||"")>(a.at||""))mistakes[k]=b});store.set("pr-mistakes",mistakes);mbTab();}
  if(data.cards)''')
rep('''xExams=[];esState={};C=defaults;''', '''xExams=[];esState={};mistakes={};C=defaults;''')
rep('''"pr-xexams","pr-essays"].forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
  render();renderAcct();''', '''"pr-xexams","pr-essays","pr-mistakes"].forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
  render();renderAcct();mbTab();''')

# ---------- state + helpers ----------
rep('''let XMCQ=[],ESSAYS=[],xExams=store.get("pr-xexams",[]),esState=store.get("pr-essays",{});''',
'''let XMCQ=[],ESSAYS=[],xExams=store.get("pr-xexams",[]),esState=store.get("pr-essays",{});
/* mistake book: {mcqId:{added,at,pick,note,wrong,right,mastered,removed}} — removed entries are kept as tombstones so removal syncs */
let mistakes=store.get("pr-mistakes",{}),mbState=store.get("pr-mbstate","learning"),mbDeck="all",mbHide=store.get("pr-mbhide",false);
const inMB=id=>!!(mistakes[id]&&!mistakes[id].removed);
function mbSave(){store.set("pr-mistakes",mistakes);queueSync();mbTab()}
function mbTab(){const t=$("#tab-mistakes");if(!t)return;const n=Object.keys(mistakes).filter(k=>inMB(k)&&!mistakes[k].mastered&&XM(k)).length;t.innerHTML="Mistake book"+(n?`<span class="n">${n}</span>`:"")}
function mbAdd(id,pick){const now=new Date().toISOString(),p=mistakes[id];
  mistakes[id]=p&&!p.removed?{...p,at:now}:{...(p||{}),added:now,at:now,pick:pick==null?null:pick,note:(p&&p.note)||"",wrong:Math.max(1,(p&&p.wrong)||0),right:(p&&p.right)||0,mastered:false,removed:false}}
function mbRemove(id){if(mistakes[id])mistakes[id]={...mistakes[id],removed:true,at:new Date().toISOString()}}
function mbBtn(id,pick){const b=document.createElement("button");b.className="mbadd";
  const paint=()=>{const on=inMB(id);b.setAttribute("aria-pressed",on);b.textContent=on?"✓ In your mistake book":"＋ Add to mistake book";b.title=on?"Tap to remove it from your mistake book":"Save this question so you can review it and write notes"};
  b.onclick=e=>{e.stopPropagation();if(inMB(id))mbRemove(id);else mbAdd(id,pick);mbSave();paint();document.querySelectorAll(".mbaddall").forEach(x=>x.dispatchEvent(new Event("repaint")))};paint();return b}''')

# ---------- per-question review inside an exam ----------
rep('''w.querySelector(".why").textContent=m.why;body.appendChild(w)}
  }else{''',
'''w.querySelector(".why").textContent=m.why;if(it.pick!==m.opts[m.a])w.appendChild(mbBtn(it.id,it.pick));body.appendChild(w)}
  }else{''')

# ---------- results list ----------
rep('''    const rv=document.createElement("div");rv.className="x-review";
    wrong.forEach(({it,i,m})=>{const d=document.createElement("div");d.className="x-rev";''',
'''    if(wrong.length){const all=document.createElement("button");all.className="btn mbaddall";all.style.alignSelf="flex-start";
      const paint=()=>{const left=wrong.filter(x=>!inMB(x.it.id)).length;all.textContent=left?`＋ Add ${left===wrong.length?"all "+left:"the other "+left} to my mistake book`:`✓ All ${wrong.length} are in your mistake book. Open it →`;all.classList.toggle("primary",!!left)};
      all.onclick=()=>{const left=wrong.filter(x=>!inMB(x.it.id));if(!left.length){closeX();view("mistakes");window.scrollTo({top:0,behavior:"smooth"});return}left.forEach(x=>mbAdd(x.it.id,x.it.pick));mbSave();renderX()};
      all.addEventListener("repaint",paint);paint();body.appendChild(all)}
    const rv=document.createElement("div");rv.className="x-review";
    wrong.forEach(({it,i,m})=>{const d=document.createElement("div");d.className="x-rev";''')
rep('''w.className="why";w.textContent=m.why;d.append(q,y,r,w);rv.appendChild(d)});''',
    '''w.className="why";w.textContent=m.why;d.append(q,y,r,w,mbBtn(it.id,it.pick));rv.appendChild(d)});''')

# ---------- track right/wrong for saved questions when an exam is submitted ----------
rep('''  xExams.unshift(X.rec);xExams=xExams.slice(0,40);''',
'''  {let ch=false;X.mcq.forEach(it=>{if(!inMB(it.id)||it.pick==null)return;const mm=mistakes[it.id],ok=it.pick===XM(it.id).opts[XM(it.id).a];
    mistakes[it.id]={...mm,at:new Date().toISOString(),...(ok?{right:(mm.right||0)+1}:{wrong:(mm.wrong||0)+1,pick:it.pick,mastered:false})};ch=true});if(ch)mbSave();}
  xExams.unshift(X.rec);xExams=xExams.slice(0,40);''')
rep('''function closeX(){clearInterval(xTick);$("#xscrim").hidden=true;X=null;if(!$("#view-xexam").hidden)renderXSetup();if(!$("#view-essays").hidden)renderEssayList()}''',
'''function closeX(){clearInterval(xTick);$("#xscrim").hidden=true;X=null;if(!$("#view-xexam").hidden)renderXSetup();if(!$("#view-essays").hidden)renderEssayList();if(!$("#view-mistakes").hidden)renderMistakes()}

/* ---------- Mistake book view ---------- */
function mbItems(){return Object.entries(mistakes).filter(([id,v])=>!v.removed&&XM(id)).map(([id,v])=>({id,v,m:XM(id)})).sort((a,b)=>(a.v.added<b.v.added?1:-1))}
function renderMistakes(){
  const all=mbItems(),learning=all.filter(x=>!x.v.mastered),mastered=all.filter(x=>x.v.mastered);
  const st=$("#mb-state");st.innerHTML="";
  [["learning","Still learning",learning.length],["mastered","Mastered",mastered.length],["all","All",all.length]].forEach(([k,t,n])=>{const b=document.createElement("button");b.className="chip";b.innerHTML=`<span></span><span class="n">${n}</span>`;b.firstChild.textContent=t;b.setAttribute("aria-pressed",mbState===k);b.onclick=()=>{mbState=k;store.set("pr-mbstate",k);renderMistakes()};st.appendChild(b)});
  const pool=mbState==="all"?all:mbState==="mastered"?mastered:learning;
  const decksIn=[...new Set(pool.map(x=>x.m.deck))];if(mbDeck!=="all"&&!decksIn.includes(mbDeck))mbDeck="all";
  const dk=$("#mb-decks");dk.innerHTML="";dk.hidden=decksIn.length<2;
  [["all","All chapters",pool.length],...decksIn.map(d=>[d,d,pool.filter(x=>x.m.deck===d).length])].forEach(([k,t,n])=>{const b=document.createElement("button");b.className="chip";b.innerHTML=`<span></span><span class="n">${n}</span>`;b.firstChild.textContent=t;b.setAttribute("aria-pressed",mbDeck===k);b.onclick=()=>{mbDeck=k;renderMistakes()};dk.appendChild(b)});
  const list=pool.filter(x=>mbDeck==="all"||x.m.deck===mbDeck);
  const pr=$("#mb-practise");pr.hidden=!list.length;pr.textContent=`Practise these ${list.length} as a quiz`;pr.onclick=()=>startRedo(shuffleArr(list.map(x=>x.id)));
  const hd=$("#mb-hide");hd.checked=mbHide;hd.onchange=()=>{mbHide=hd.checked;store.set("pr-mbhide",mbHide);renderMistakes()};hd.closest("label").hidden=!list.length;
  const L=$("#mb-list");L.innerHTML="";
  if(!list.length){const e=document.createElement("div");e.className="mbempty";
    e.textContent=!all.length?"Your mistake book is empty. After an exam, tap \\"＋ Add to mistake book\\" on any question you got wrong and it will be saved here.":mbState==="learning"?"Nothing left to learn here. Every saved question is marked as mastered.":"No questions here yet.";
    L.appendChild(e);if(!all.length){const b=document.createElement("button");b.className="btn primary";b.textContent="Go to Exam mode";b.style.marginTop="12px";b.onclick=()=>view("xexam");e.appendChild(document.createElement("br"));e.appendChild(b)}return}
  list.forEach(({id,v,m})=>{
    const c=document.createElement("article");c.className="mbcard"+(v.mastered?" done":"");
    const top=document.createElement("div");top.className="top";const dd=document.createElement("span");dd.className="deck";dd.textContent=m.deck;
    const meta=document.createElement("span");meta.textContent=`Saved ${fmtWhen(v.added)} · wrong ${v.wrong||1}×`+(v.right?` · right ${v.right}× since`:"")+(v.mastered?" · mastered ✓":"");top.append(dd,meta);
    const q=document.createElement("div");q.className="q";q.textContent=m.q;
    const ol=document.createElement("ol");ol.type="A";m.opts.forEach((o,k)=>{const li=document.createElement("li");li.textContent=o;if(!mbHide||c.dataset.shown){if(k===m.a)li.className="right";else if(o===v.pick)li.className="yours"}ol.appendChild(li)});
    const ans=document.createElement("div");ans.className="ans";
    const y=document.createElement("span");y.className="yours";y.textContent=v.pick==null?"You didn't answer it.":`Your answer: ${v.pick}`;
    const r=document.createElement("span");r.className="right";r.textContent=`Answer: ${m.opts[m.a]}`;
    const w=document.createElement("span");w.className="why";w.textContent=m.why;ans.append(y,r,w);
    const show=document.createElement("button");show.className="btn";show.textContent="Show answer";
    const reveal=()=>{ans.hidden=false;show.hidden=true;[...ol.children].forEach((li,k)=>{if(k===m.a)li.className="right";else if(m.opts[k]===v.pick)li.className="yours"})};
    show.onclick=reveal;ans.hidden=mbHide;show.hidden=!mbHide;
    const nl=document.createElement("label");nl.className="nl";nl.textContent="My notes: why is this the answer? What tricked me?";nl.htmlFor="mbn-"+id;
    const ta=document.createElement("textarea");ta.id="mbn-"+id;ta.placeholder="Write it in your own words, e.g. the key clue in the scenario, the concept it points to, and how it differs from the option I picked.";ta.value=v.note||"";
    const saved=document.createElement("span");saved.className="saved";saved.textContent=v.note?"Notes saved":"";
    let t=null;ta.oninput=()=>{saved.textContent="Saving…";clearTimeout(t);t=setTimeout(()=>{mistakes[id]={...mistakes[id],note:ta.value,at:new Date().toISOString()};mbSave();saved.textContent=user?"Notes saved to your account":"Notes saved on this device"},600)};
    const acts=document.createElement("div");acts.className="acts";
    const mk=(tx,fn,cls)=>{const b=document.createElement("button");b.className="btn"+(cls?" "+cls:"");b.textContent=tx;b.onclick=fn;acts.appendChild(b);return b};
    acts.appendChild(show);
    mk("Retry this one",()=>startRedo([id]));
    mk(v.mastered?"Move back to still learning":"✓ I've mastered this",()=>{mistakes[id]={...mistakes[id],mastered:!v.mastered,at:new Date().toISOString()};mbSave();renderMistakes()},v.mastered?"":"primary");
    const rm=mk("Remove",()=>{if(rm.dataset.arm){mbRemove(id);mbSave();renderMistakes()}else{rm.dataset.arm=1;rm.textContent="Tap again to remove";setTimeout(()=>{rm.textContent="Remove";delete rm.dataset.arm},3000)}});
    acts.appendChild(saved);
    c.append(top,q,ol,ans,nl,ta,acts);L.appendChild(c)});
}''')

# badge after the MCQ bank loads
rep('if(r.ok)XMCQ=await r.json()}catch(e){}','if(r.ok)XMCQ=await r.json()}catch(e){}mbTab();')
P.write_text(s)
print("ok")
