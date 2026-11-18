"""Quiz mode: exam-style scenario MCQs (quiz-mcq.json, one per card) replace auto-generated questions."""
import pathlib
P = pathlib.Path(__file__).resolve().parent.parent / "index.html"
s = P.read_text()

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

rep('.qfeed{font-weight:600;font-size:15px}',
    '.qfeed{font-weight:600;font-size:15px}\n.qwhy{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px 12px;font-size:15px;line-height:1.5}')
rep('''        <div class="qfeed" id="q-feed" aria-live="polite"></div>''',
    '''        <div class="qfeed" id="q-feed" aria-live="polite"></div>
        <div class="qwhy" id="q-why" hidden></div>''')

# question bank + type
rep('''const QT=["describe","fact","compare"],QTLABEL={describe:"Choose the best answer",fact:"Pick the true statement",compare:"Compare similar concepts"};''',
    '''const QT=["describe","fact","compare"],QTLABEL={scenario:"Apply it to the scenario",describe:"Choose the best answer",fact:"Pick the true statement",compare:"Compare similar concepts"};
let QMCQ={};  // exam-style scenario question for each card id (quiz-mcq.json)''')
rep('''function buildQuestion(item){
  const c=byId(item.id);if(!c)return null;''',
'''function buildQuestion(item){
  const c=byId(item.id);if(!c)return null;
  const sq=QMCQ[c.id];
  if(sq&&item.type!=="compare"){const right=sq.opts[sq.a];return {type:"scenario",id:c.id,stem:sq.q,why:sq.why,opts:shuffleArr(sq.opts.slice()),right}}''')

# plans: one scenario question per card
rep('''function planItems(plan,cards){
  if(plan==="quick")return shuffleArr(cards).slice(0,10).map(c=>({id:c.id,type:nextType(c.id)}));
  if(plan==="full")return shuffleArr(cards.map(c=>({id:c.id,type:nextType(c.id)})));
  if(plan==="compare")return shuffleArr(cards.map(c=>({id:c.id,type:"compare"})));
  return shuffleArr(cards.flatMap(c=>QT.map(t=>({id:c.id,type:t}))));  // "all": every type for every card
}
const PLANS=[["full","Full quiz","One question per card, mixed types. Each new quiz asks each card a different way."],
  ["quick","Quick 10","10 random cards, mixed types."],
  ["compare","Compare similar concepts","Tell apart look-alikes, e.g. Id vs Ego, James-Lange vs Cannon-Bard."],
  ["all","Ultimate","All 3 question types for every card."]];''',
'''function planItems(plan,cards){
  const it=c=>({id:c.id,type:QMCQ[c.id]?"scenario":nextType(c.id)});
  if(plan==="quick")return shuffleArr(cards).slice(0,10).map(it);
  if(plan==="quick20")return shuffleArr(cards).slice(0,20).map(it);
  if(plan==="weak"){const w=cards.filter(c=>status[c.id]==="forgot"||status[c.id]==="unsure"||!status[c.id]);return shuffleArr(w.length?w:cards).map(it)}
  return shuffleArr(cards.map(it));
}
const PLANS=[["full","Full quiz","One exam-style scenario question for every card in this view."],
  ["quick","Quick 10","10 random cards."],
  ["quick20","Quick 20","20 random cards."],
  ["weak","Weak spots","Only cards you marked Not sure or Totally forgot, or haven't rated yet."]];''')
rep('''    const cnt={full:n,quick:Math.min(10,n),compare:n,all:n*QT.length}[v];''',
    '''    const weak=cards.filter(c=>status[c.id]==="forgot"||status[c.id]==="unsure"||!status[c.id]).length||n;
    const cnt={full:n,quick:Math.min(10,n),quick20:Math.min(20,n),weak}[v];''')
rep('''  const last=store.get("pr-qplan","full");''', '''  let last=store.get("pr-qplan","full");if(!PLANS.some(p=>p[0]===last))last="full";''')
rep('''Every question has 4 options. Pick a quiz:''', '''Every question is an exam-style scenario with 4 options. Pick a quiz:''')

# render
rep('''  if(q.type==="name"){''', '''  if(q.type==="scenario"){stem.append(q.stem)}
  else if(q.type==="name"){''')
rep('''  $("#q-after").hidden=true;$("#q-next").hidden=true;''', '''  $("#q-after").hidden=true;$("#q-next").hidden=true;$("#q-why").hidden=true;''')
rep('''  const cmp=$("#q-cmp");
  if(q.type==="compare"){''',
'''  const cmp=$("#q-cmp"),wy=$("#q-why");wy.hidden=!q.why;if(q.why){wy.textContent=q.why}
  if(q.type==="scenario"){$("#q-anslabel").textContent=`The concept: ${c.name}`;$("#q-ans").hidden=false;points($("#q-ans"),c.ans);cmp.hidden=true}
  else if(q.type==="compare"){''')
rep('''$("#q-retry").onclick=()=>startQuiz(shuffleArr(quiz.missed.map(id=>({id,type:nextType(id)}))),quiz.label+" · missed",quiz.plan);''',
    '''$("#q-retry").onclick=()=>startQuiz(shuffleArr(quiz.missed.map(id=>({id,type:QMCQ[id]?"scenario":nextType(id)}))),quiz.label+" · missed",quiz.plan);''')

# load bank
rep('''if(r.ok)XMCQ=await r.json()}catch(e){}mbTab();''',
    '''if(r.ok)XMCQ=await r.json()}catch(e){}mbTab();
  try{const r=await fetch("quiz-mcq.json",{cache:"no-store"});if(r.ok)QMCQ=await r.json()}catch(e){}''')
P.write_text(s)
print("ok")
