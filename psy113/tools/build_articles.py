"""Build psy113/articles.json from tools/articles/*.txt.

File format:
  key: value            header lines (id, level, title, short, design, based_on, url, doi)
  == Section heading    starts a section
  one sentence per line; tags at the start mark answers for items:
      [rq] sentence       -> this sentence is a correct answer for item 'rq'
      [rq~] sentence      -> also acceptable (partial / alternative) for 'rq'
      several tags allowed: [tf][gap~] sentence
  --- items             then one JSON object per line (sentence items get 'ans'/'ok' filled from tags)
"""
import json, re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "articles.json"
VERSION = 2
TAG = re.compile(r"^\[([a-z0-9_]+)(~?)\]\s*")

def parse(path):
    head, text, items = {}, [], []
    mode = "head"
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line == "--- items":
            mode = "items"; continue
        if mode == "items":
            items.append(json.loads(line)); continue
        if line.startswith("== "):
            mode = "text"; text.append({"h": line[3:].strip(), "s": [], "_tags": []}); continue
        if mode == "head":
            k, v = line.split(":", 1); head[k.strip()] = v.strip(); continue
        tags = []
        while True:
            m = TAG.match(line)
            if not m: break
            tags.append((m.group(1), m.group(2) == "~")); line = line[m.end():]
        sec = text[-1]
        sec["s"].append(line); sec["_tags"].append(tags)
    ans, ok = {}, {}
    for si, sec in enumerate(text):
        for j, tags in enumerate(sec.pop("_tags")):
            for k, alt in tags:
                (ok if alt else ans).setdefault(k, []).append(f"{si}.{j}")
    keys = {it["key"] for it in items}
    for it in items:
        if it["kind"] == "sentence":
            assert it["key"] in ans, f"{path.name}: no sentence tagged for {it['key']}"
            it["ans"] = ans[it["key"]]
            if it["key"] in ok: it["ok"] = ok[it["key"]]
        elif it["kind"] == "choice":
            assert it["ans"] in it["options"], f"{path.name}: bad choice answer {it['key']}"
        elif it["kind"] == "text":
            assert it.get("accept"), f"{path.name}: text item {it['key']} needs accept"
    unknown = (set(ans) | set(ok)) - keys
    if unknown: print(f"  note {path.name}: unused tags {sorted(unknown)}")
    a = {"id": head["id"], "v": VERSION, "level": int(head["level"]), "title": head["title"], "short": head["short"],
         "authors": "Practice article", "year": 2026, "journal": "PSY113 Practice", "doi": head.get("doi", ""),
         "url": head.get("url", ""), "license": "Written for practice; details simplified", "design": head["design"],
         "based_on": head.get("based_on", ""), "text": text, "items": items}
    words = sum(len(s.split()) for sec in text for s in sec["s"])
    return a, words

def main():
    arts = []
    for p in sorted((ROOT / "articles").glob("a*.txt"), key=lambda p: int(p.stem[1:])):
        a, w = parse(p); arts.append(a)
        print(f"{a['id']:>4} L{a['level']} {w:5d} words {len(a['items']):3d} tasks  {a['short']}")
    if "--check" not in sys.argv:
        OUT.write_text(json.dumps(arts, ensure_ascii=False, indent=1), encoding="utf-8")
        print("wrote", OUT)

main()
