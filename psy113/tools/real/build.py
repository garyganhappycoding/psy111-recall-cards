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
# Lecture 14 articles (from the PSY 113 lecture PDFs)
import sys; sys.path.insert(0, str(ROOT / "lec")); from split import load
L = ROOT / "lec"
tri = json.loads((L / "trifiro.items.json").read_text()); secs = load(L / "trifiro.txt")
ids = {f"{i}.{j}" for i, s in enumerate(secs) for j in range(len(s["s"]))}
for it in tri["items"]:
    if it["kind"] == "sentence": assert not [x for x in it["ans"] + it.get("ok", []) if x not in ids], it["key"]
    if it["kind"] == "choice": assert it["ans"] in it["options"], it["key"]
arts.append({"id": "l14-trifiro", "v": 1, "real": True, "lec": 14, "level": tri["level"], "title": "Active Instagram Use and Its Association With Self-Esteem and Well-Being",
    "short": tri["short"], "authors": "Trifiro, B. M.; Prena, K.", "year": 2021, "journal": "Technology, Mind, and Behavior", "doi": "10.1037/tmb0000043",
    "url": "https://doi.org/10.1037/tmb0000043", "design": tri["design"],
    "citation": "Trifiro, B. M., & Prena, K. (2021). Active Instagram use and its association with self-esteem and well-being. Technology, Mind, and Behavior, 2(3), 266–270. https://doi.org/10.1037/tmb0000043",
    "licNote": "Licence: CC BY-NC-ND 4.0 (https://creativecommons.org/licenses/by-nc-nd/4.0/). Text reproduced unchanged for non-commercial study, with attribution; tables, figures, footnotes and references omitted.",
    "text": secs, "items": tri["items"]})
sri = json.loads((L / "srivastava.items.json").read_text())
for it in sri["items"]: assert it["kind"] != "sentence" and (it["kind"] != "choice" or it["ans"] in it["options"]), it["key"]
arts.append({"id": "l14-srivastava", "v": 1, "real": True, "lec": 14, "noText": True, "level": sri["level"], "title": "Relationship between Life Satisfaction and Depression among Working and Non-working Married Women",
    "short": sri["short"], "authors": "Srivastava, A.", "year": 2016, "journal": "International Journal of Education and Psychological Research", "design": sri["design"],
    "citation": "Srivastava, A. (2016). Relationship between life satisfaction and depression among working and non-working married women. International Journal of Education and Psychological Research, 5(3), 1–7.",
    "licNote": "Text not reproduced (no open licence found). Use the PDF from Lecture 14.",
    "text": [{"h": "Where's the text?", "s": sri["note"]}], "items": sri["items"]})
print("lec14:", len(tri["items"]), len(sri["items"]), "tasks")
arts.sort(key=lambda x: (0 if x.get("lec") else 1, x["level"], x["year"]))
OUT.write_text(json.dumps(arts, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", OUT, len(arts))
