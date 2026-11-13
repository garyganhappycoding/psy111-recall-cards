# Exam mode: keep every paper, review past exams, progress chart, chapter breakdown, redo wrong questions.
p='index.html';s=open(p).read()
def rep(a,b,n=1):
    global s
    c=s.count(a);assert c==n,(a[:80],c);s=s.replace(a,b)
# ---- markup: history panel replaces the short list
rep('''      <div class="field" id="xx-histbox" hidden><span class="label">Your past exams</span><ol class="exhist" id="xx-hist"></ol></div>''','''      <div class="xhist" id="xx-histbox" hidden>
        <div class="field"><span class="label">Your progress</span><div class="xstats" id="xx-stats"></div><div class="xchart" id="xx-chart"></div></div>
        <div class="field" id="xx-chapbox" hidden><span class="label">MCQ accuracy by chapter (all your exams)</span><span class="hint">Weakest first. Tap a chapter to revise its cards.</span><div class="xchaps" id="xx-chaps"></div></div>
        <div class="field"><span class="label">Past exams</span><div class="xpast" id="xx-hist"></div></div>
      </div>''')
# ---- CSS
rep('.exhist{margin:0;padding-left:20px;font-size:14px;display:flex;flex-direction:column;gap:4px}.exhist .sc{font-weight:600}','''.exhist{margin:0;padding-left:20px;font-size:14px;display:flex;flex-direction:column;gap:4px}.exhist .sc{font-weight:600}
.xhist{display:flex;flex-direction:column;gap:22px;border-top:1px solid var(--line);padding-top:18px}
.xstats{display:flex;flex-wrap:wrap;gap:10px}
.xstats div{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:120px}
.xstats b{display:block;font-family:var(--display);font-weight:400;font-size:26px;line-height:1.1}
.xstats span{font-size:12px;color:var(--muted)}
.xstats .up{color:var(--ok)}.xstats .down{color:var(--bad)}
.xchart svg{width:100%;height:auto;display:block}
.xchart .grid{stroke:var(--line);stroke-width:1}
.xchart .ax{fill:var(--muted);font-size:11px;font-family:var(--mono)}
.xchart .l-mcq{fill:none;stroke:var(--accent);stroke-width:2.5}
.xchart .l-ess{fill:none;stroke:var(--warn);stroke-width:2.5;stroke-dasharray:6 4}
.xchart .d-mcq{fill:var(--accent)}.xchart .d-ess{fill:var(--warn)}
.xchart .vl{font-size:11px;font-family:var(--mono);fill:var(--ink)}
.xlegend{display:flex;gap:16px;font-size:12px;color:var(--muted);margin-top:4px}
.xlegend i{display:inline-block;width:18px;height:3px;border-radius:2px;vertical-align:middle;margin-right:6px;background:var(--accent)}
.xlegend i.e{background:var(--warn)}
.xchaps{display:flex;flex-direction:column;gap:6px}
.xchap{all:unset;cursor:pointer;display:grid;grid-template-columns:minmax(110px,170px) 1fr 70px;gap:10px;align-items:center;font-size:13px;padding:3px 4px;border-radius:6px}
.xchap:hover{background:var(--bg)}.xchap:focus-visible{outline:2px solid var(--accent)}
.xchap .bar{height:10px;border-radius:5px;background:var(--line);overflow:hidden}
.xchap .bar i{display:block;height:100%;border-radius:5px}
.xchap .pc{font-family:var(--mono);font-size:12px;text-align:right;color:var(--muted)}
.xpast{display:flex;flex-direction:column;gap:8px}
.xrow{display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.xrow .n{font-family:var(--mono);font-size:12px;color:var(--muted);min-width:24px}
.xrow .what{flex:1;min-width:160px;display:flex;flex-direction:column;gap:2px}
.xrow .what b{font-size:15px}
.xrow .what span{font-size:12px;color:var(--muted)}
.xrow .acts{display:flex;gap:6px;flex-wrap:wrap}
.xrow .btn{padding:7px 11px;font-size:13px}''')
# ---- record the full paper on submit
rep('''  X.rec={at:new Date().toISOString(),mcq:X.mcqScore,mcqTotal:X.mcq.length,essay:X.ess.length?null:undefined,essayTotal:X.ess.reduce((s,e)=>s+XE(e.id).total,0)||undefined,mins:X.mins};''',
'''  X.rec={at:new Date().toISOString(),mcq:X.mcqScore,mcqTotal:X.mcq.length,essay:X.ess.length?null:undefined,essayTotal:X.ess.reduce((s,e)=>s+XE(e.id).total,0)||undefined,mins:X.mins,
    kind:X.redo?"redo":(X.mcq.length&&X.ess.length?"full":X.mcq.length?"mcq":"essay"),
    items:X.mcq.map(it=>({id:it.id,opts:it.opts,pick:it.pick})),ess:X.ess.map(e=>({id:e.id,ans:{...e.ans},ticks:{}}))};''')
rep('''  X.rec.essay=tot;store.set("pr-xexams",xExams);''','''  X.rec.essay=tot;if(X.rec.ess)X.rec.ess.forEach(r=>{r.ticks=X.ticks[r.id]||{}});store.set("pr-xexams",xExams);''')
rep('''  xExams.unshift(X.rec);xExams=xExams.slice(0,30);''','''  xExams.unshift(X.rec);xExams=xExams.slice(0,40);''')
# ---- results: redo wrong button
rep('''  if(X.ess.length)mk("Mark Essay 1 →",()=>{X.i=X.mcq.length;renderX()},"primary");''','''  if(X.ess.length)mk("Mark Essay 1 →",()=>{X.i=X.mcq.length;renderX()},"primary");
  {const wr=X.mcq.filter(it=>it.pick!==XM(it.id).opts[XM(it.id).a]);if(wr.length)mk(`Redo the ${wr.length} I got wrong`,()=>startRedo(wr.map(it=>it.id)),X.ess.length?"":"primary")}''')
rep('''  $("#x-title").textContent=X.auto?"Time's up! Your results":"Your results";''','''  $("#x-title").textContent=X.past?`Past exam · ${fmtWhen(X.rec.at)}`:X.auto?"Time's up! Your results":"Your results";''')
# ---- setup: new history panel
rep('''  const h=$("#xx-hist");h.innerHTML="";$("#xx-histbox").hidden=!xExams.length;
  xExams.slice(0,8).forEach(x=>{const li=document.createElement("li");const sc=document.createElement("span");sc.className="sc";
    const parts=[];if(x.mcqTotal)parts.push(`MCQ ${x.mcq}/${x.mcqTotal}`);if(x.essayTotal)parts.push(`Essays ${x.essay==null?"not marked":x.essay+"/"+x.essayTotal}`);
    sc.textContent=parts.join(" · ");li.append(sc,` · ${fmtWhen(x.at)}`+(x.mins?` · ${x.mins} min`:""));h.appendChild(li)});
}''','''  renderXHistory();
}
const pct=(a,b)=>b?Math.round(a/b*100):null;
function renderXHistory(){
  $("#xx-histbox").hidden=!xExams.length;if(!xExams.length)return;
  const chron=xExams.slice().reverse();                      // oldest → newest
  const mcqRuns=chron.filter(x=>x.mcqTotal&&x.kind!=="redo"),essRuns=chron.filter(x=>x.essayTotal&&x.essay!=null);
  // stats
  const st=$("#xx-stats");st.innerHTML="";
  const card=(big,small,cls)=>{const d=document.createElement("div");const b=document.createElement("b");b.textContent=big;if(cls)b.className=cls;const sp=document.createElement("span");sp.textContent=small;d.append(b,sp);st.appendChild(d)};
  card(String(xExams.length),xExams.length===1?"exam taken":"exams taken");
  if(mcqRuns.length){const last=mcqRuns[mcqRuns.length-1],lp=pct(last.mcq,last.mcqTotal);card(lp+"%","latest MCQ score");
    card(Math.max(...mcqRuns.map(x=>pct(x.mcq,x.mcqTotal)))+"%","best MCQ score");
    if(mcqRuns.length>1){const d=lp-pct(mcqRuns[0].mcq,mcqRuns[0].mcqTotal);card((d>0?"+":"")+d+"%","since your first exam",d>0?"up":d<0?"down":"")}}
  if(essRuns.length){const last=essRuns[essRuns.length-1];card(pct(last.essay,last.essayTotal)+"%","latest essay mark")}
  // chart
  const ch=$("#xx-chart");ch.innerHTML="";
  const pts=chron.map((x,i)=>({i,x,m:x.mcqTotal&&x.kind!=="redo"?pct(x.mcq,x.mcqTotal):null,e:x.essayTotal&&x.essay!=null?pct(x.essay,x.essayTotal):null})).filter(p=>p.m!=null||p.e!=null);
  if(pts.length){
    const W=640,H=220,L=40,R=16,T=16,B=34,n=pts.length,xs=k=>n===1?L+(W-L-R)/2:L+k*(W-L-R)/(n-1),ys=v=>T+(100-v)/100*(H-T-B);
    let svg=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Exam scores over time">`;
    [0,25,50,75,100].forEach(v=>{svg+=`<line class="grid" x1="${L}" x2="${W-R}" y1="${ys(v)}" y2="${ys(v)}"/><text class="ax" x="${L-8}" y="${ys(v)+4}" text-anchor="end">${v}%</text>`});
    pts.forEach((p,k)=>{if(n<=12||k%Math.ceil(n/12)===0||k===n-1)svg+=`<text class="ax" x="${xs(k)}" y="${H-12}" text-anchor="middle">${new Date(p.x.at).toLocaleDateString(undefined,{day:"numeric",month:"short"})}</text>`});
    const line=(key,cls)=>{const q=pts.map((p,k)=>p[key]==null?null:[xs(k),ys(p[key]),p[key]]).filter(Boolean);if(!q.length)return;
      if(q.length>1)svg+=`<polyline class="l-${cls}" points="${q.map(a=>a[0]+","+a[1]).join(" ")}"/>`;
      q.forEach(a=>{svg+=`<circle class="d-${cls}" cx="${a[0]}" cy="${a[1]}" r="4.5"/>`;if(n<=10)svg+=`<text class="vl" x="${a[0]}" y="${a[1]-10}" text-anchor="middle">${a[2]}%</text>`})};
    line("m","mcq");line("e","ess");svg+="</svg>";ch.innerHTML=svg;
    const lg=document.createElement("div");lg.className="xlegend";lg.innerHTML=`<span><i></i>MCQ %</span>`+(essRuns.length?`<span><i class="e"></i>Essay % (once marked)</span>`:"");ch.appendChild(lg);
  }
  // chapter accuracy over all saved papers
  const by={};xExams.forEach(x=>(x.items||[]).forEach(it=>{const m=XM(it.id);if(!m)return;const d=by[m.deck]=by[m.deck]||{ok:0,n:0};d.n++;if(it.pick===m.opts[m.a])d.ok++}));
  const chs=Object.entries(by).map(([deck,v])=>({deck,...v,p:Math.round(v.ok/v.n*100)})).sort((a,b)=>a.p-b.p||b.n-a.n);
  $("#xx-chapbox").hidden=!chs.length;const cb=$("#xx-chaps");cb.innerHTML="";
  chs.forEach(c=>{const b=document.createElement("button");b.className="xchap";b.title=`Revise ${c.deck}`;
    const nm=document.createElement("span");nm.textContent=c.deck;const bar=document.createElement("span");bar.className="bar";const fill=document.createElement("i");fill.style.width=c.p+"%";fill.style.background=c.p>=75?"var(--ok)":c.p>=50?"var(--warn)":"var(--bad)";bar.appendChild(fill);
    const pc=document.createElement("span");pc.className="pc";pc.textContent=`${c.p}% · ${c.ok}/${c.n}`;b.append(nm,bar,pc);
    b.onclick=()=>{if(decks().includes(c.deck)){deck=c.deck;store.set("pr-deck",deck)}view("cards");window.scrollTo({top:0,behavior:"smooth"})};cb.appendChild(b)});
  // list of every past exam
  const h=$("#xx-hist");h.innerHTML="";
  xExams.forEach((x,k)=>{const r=document.createElement("div");r.className="xrow";
    const n=document.createElement("span");n.className="n";n.textContent="#"+(xExams.length-k);
    const w=document.createElement("div");w.className="what";const b=document.createElement("b");const parts=[];
    if(x.mcqTotal)parts.push(`MCQ ${x.mcq}/${x.mcqTotal} (${pct(x.mcq,x.mcqTotal)}%)`);if(x.essayTotal)parts.push(`Essays ${x.essay==null?"not marked":x.essay+"/"+x.essayTotal}`);
    b.textContent=parts.join(" · ");const sp=document.createElement("span");
    sp.textContent=`${{full:"Full exam",mcq:"MCQs only",essay:"Essays only",redo:"Redo of wrong questions"}[x.kind]||"Exam"} · ${fmtWhen(x.at)}`+(x.mins?` · ${x.mins} min`:"");w.append(b,sp);
    const a=document.createElement("div");a.className="acts";
    if(x.items||x.ess){const rv=document.createElement("button");rv.className="btn";rv.textContent="Review";rv.onclick=()=>reviewExam(x);a.appendChild(rv);
      const wr=(x.items||[]).filter(it=>{const m=XM(it.id);return m&&it.pick!==m.opts[m.a]});
      if(wr.length){const rd=document.createElement("button");rd.className="btn";rd.textContent=`Redo ${wr.length} wrong`;rd.onclick=()=>startRedo(wr.map(it=>it.id));a.appendChild(rd)}}
    else{const sp2=document.createElement("span");sp2.className="hint";sp2.textContent="Details weren't saved for this older exam";a.appendChild(sp2)}
    r.append(n,w,a);h.appendChild(r)});
}
function reviewExam(rec){
  const items=(rec.items||[]).filter(it=>XM(it.id)),ess=(rec.ess||[]).filter(e=>XE(e.id));
  X={mcq:items.map(it=>({id:it.id,opts:it.opts,pick:it.pick,flag:false})),ess:ess.map(e=>({id:e.id,ans:{...e.ans}})),i:-1,started:0,limit:0,submitted:true,past:true,
     rec,ticks:Object.fromEntries(ess.map(e=>[e.id,JSON.parse(JSON.stringify(e.ticks||{}))])),mcqScore:rec.mcq,mins:rec.mins||0};
  $("#xscrim").hidden=false;$("#x-timer").hidden=true;clearInterval(xTick);renderX();$("#xsheet").focus({preventScroll:true});
}
function startRedo(ids){
  const mcq=shuffleArr(ids.filter(id=>XM(id)).map(id=>({id,opts:shuffleArr(XM(id).opts.slice()),pick:null,flag:false})));if(!mcq.length)return;
  X={mcq,ess:[],i:0,started:Date.now(),limit:0,submitted:false,confirm:false,ticks:{},redo:true};
  $("#xscrim").hidden=false;$("#x-timer").hidden=true;clearInterval(xTick);renderX();$("#xsheet").focus({preventScroll:true});
}''')
open(p,'w').write(s);print("history ok")

s=open(p).read()
rep('.xchap{all:unset;cursor:pointer;display:grid;grid-template-columns:minmax(110px,170px) 1fr 70px;gap:10px;align-items:center;font-size:13px;padding:3px 4px;border-radius:6px}',
    '.xchap{all:unset;box-sizing:border-box;width:100%;cursor:pointer;display:grid;grid-template-columns:minmax(0,170px) minmax(60px,1fr) 96px;gap:12px;align-items:center;font-size:13px;padding:4px 6px;border-radius:6px}')
rep('const W=640,H=220,L=40,R=16,T=16,B=34,n=pts.length,xs=k=>n===1?L+(W-L-R)/2:L+k*(W-L-R)/(n-1)','const W=640,H=220,L=44,R=24,T=20,B=34,n=pts.length,xs=k=>n===1?L+(W-L-R)/2:L+18+k*(W-L-R-18)/(n-1)')
rep('''svg+=`<text class="ax" x="${xs(k)}" y="${H-12}" text-anchor="middle">${new Date(p.x.at).toLocaleDateString(undefined,{day:"numeric",month:"short"})}</text>`''',
    '''svg+=`<text class="ax" x="${xs(k)}" y="${H-12}" text-anchor="middle">#${xExams.length-xExams.indexOf(p.x)}</text>`''')
open(p,'w').write(s);print("fix ok")
