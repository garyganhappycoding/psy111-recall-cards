import re, sys, json, pathlib
def load(p):
    secs=[]
    for line in pathlib.Path(p).read_text().splitlines():
        if line.startswith("## "): secs.append({"h":line[3:],"s":[]}); continue
        if not line.strip(): continue
        t=re.sub(r"\b(et al|e\.g|i\.e|vs|Vol|No)\.\s", lambda m:m.group(1).replace(".","§")+"§ ", line)
        parts=re.split(r"(?:(?<=[.!?])|(?<=[.!?]”))\s+(?=[A-Z“])", t)
        secs[-1]["s"]+= [x.replace("§",".") for x in parts]
    return secs
if __name__=="__main__":
    s=load(sys.argv[1])
    for i,sec in enumerate(s):
        print("##",i,sec["h"])
        for j,x in enumerate(sec["s"]): print(f"{i}.{j}",x[:150])
