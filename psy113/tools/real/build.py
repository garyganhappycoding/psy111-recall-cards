"""Build psy113/articles.json from real open-access (CC BY) articles.
source.json: full text pulled from Europe PMC (fullTextXML) in the browser, split into sentences.
items/<PMCID>.json: tasks; sentence answers refer to "section.sentence" ids AFTER back-matter is removed (see prep.clean)."""
import json, pathlib
from prep import A, clean
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent.parent / "articles.json"
VERSION = 3
def apa(a):
    au = a["authors"]
    names = ", ".join(au[:-1]) + (", & " + au[-1] if len(au) > 1 else au[0]) if len(au) <= 20 else ", ".join(au[:19]) + ", … " + au[-1]
    vol = a["volume"]; loc = a["eloc"] or (a["fpage"] + ("–" + a["lpage"] if a["lpage"] else ""))
    iss = f"({a['issue']})" if a.get("issue") else ""
    art = f", {loc}" if a["lpage"] else (f", Article {loc}" if loc else "")
    return f"{names} ({a['year']}). {a['title']}. {a['journal']}, {vol}{iss}{art}. https://doi.org/{a['doi']}"
arts = []
for f in sorted((ROOT / "items").glob("*.json")):
    meta = json.loads(f.read_text()); a = A[f.stem]; secs = clean(a)
    ids = {f"{i}.{j}" for i, s in enumerate(secs) for j in range(len(s["s"]))}
    for it in meta["items"]:
        if it["kind"] == "sentence":
            bad = [x for x in it["ans"] + it.get("ok", []) if x not in ids]
            assert not bad, (f.stem, it["key"], bad)
        if it["kind"] == "choice": assert it["ans"] in it["options"], (f.stem, it["key"])
    lic = "CC BY" if "creativecommons.org/licenses/by" in a["license"] or "(CC BY)" in a["license"] or "Creative Commons Attribution License" in a["license"] else None
    assert lic, (f.stem, a["license"][:80])
    arts.append({"id": "r-" + f.stem, "v": VERSION, "real": True, "level": meta["level"], "title": a["title"], "short": meta["short"],
        "authors": "; ".join(a["authors"]), "year": int(a["year"]), "journal": a["journal"], "doi": a["doi"], "url": "https://doi.org/" + a["doi"],
        "license": "CC BY (Creative Commons Attribution). " + a["license"][:400], "design": meta["design"], "citation": apa(a),
        "source": f"Full text from Europe PMC ({f.stem}); figures, tables, references and back matter omitted.",
        "text": secs, "items": meta["items"]})
    print(f"{f.stem} L{meta['level']} {sum(len(' '.join(s['s']).split()) for s in secs):5d} words {len(meta['items']):2d} tasks  {meta['short']}")
arts.sort(key=lambda x: (x["level"], x["year"]))
OUT.write_text(json.dumps(arts, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", OUT, len(arts))
