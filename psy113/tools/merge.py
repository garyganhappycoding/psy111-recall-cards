import json,glob,os,re,collections
D="/tmp/claude-0/-home-claude/b48e75fb-8c10-57b1-91de-6d42e84cac5b/scratchpad/p113"
out="/home/claude/psy111-recall-cards/psy113"
cards=[];mcq=[]
num=lambda f:int(re.search(r"L(\d+)",os.path.basename(f)).group(1))
for f in sorted(glob.glob(D+"/lec/L*-cards.json"),key=num):cards+=json.load(open(f))
for f in sorted(glob.glob(D+"/lec/L*-mcq.json"),key=num):mcq+=json.load(open(f))
ids=[c["id"] for c in cards];assert len(ids)==len(set(ids)),[i for i,n in collections.Counter(ids).items() if n>1]
mids=[m["id"] for m in mcq];assert len(mids)==len(set(mids))
for m in mcq:assert len(m["opts"])==4 and 0<=m["a"]<4,m["id"]
for c in cards:
    c["sim"]=[x for x in c.get("sim",[]) if x in set(ids) and x!=c["id"]]
    if not c["sim"]:c.pop("sim")
json.dump(cards,open(out+"/cards.json","w"),ensure_ascii=False,indent=1)
json.dump(mcq,open(out+"/mcq.json","w"),ensure_ascii=False,indent=1)
arts=[]
for f in ["set1","set2"]:
    p=f"{D}/art/{f}.json"
    if os.path.exists(p):arts+=json.load(open(p))
arts.sort(key=lambda a:int(a["id"][1:]))
json.dump(arts,open(out+"/articles.json","w"),ensure_ascii=False,indent=1)
print(len(cards),"cards",collections.Counter(c["deck"] for c in cards));print(len(mcq),"mcq",collections.Counter(m["lec"] for m in mcq));print(len(arts),"articles")
