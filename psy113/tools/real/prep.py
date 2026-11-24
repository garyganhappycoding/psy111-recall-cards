import json,re,sys
import pathlib as _p
_D=_p.Path(__file__).resolve().parent
A={a['pmcid']:a for a in json.load(open(_D/'source.json'))}
for _l in (_D/'authors.txt').read_text().splitlines():
    _k,_v=_l.split('|');A[_k]['authors']=_v.split('; ')
DROP=re.compile(r'^(Author Contributions|Conflict|Acknowledg|Funding|Data Availab|Associated Data|Supplementary|Publisher|.*Reporting summary|.*Conflict of)',re.I)
def clean(a):
    secs=[s for s in a['text'] if not DROP.match(s['h']) and not DROP.match(s['h'].split(' – ')[-1])]
    for s in secs: s['s']=[x.strip() for x in s['s'] if x.strip()]
    return secs
if __name__=='__main__':
    a=A[sys.argv[1]];secs=clean(a)
    lo,hi=(int(sys.argv[2]),int(sys.argv[3])) if len(sys.argv)>3 else (0,999)
    for i,s in enumerate(secs):
        if lo<=i<=hi:
            print(f'== [{i}] {s["h"]}')
            for j,t in enumerate(s['s']): print(f'{i}.{j} {t}')
