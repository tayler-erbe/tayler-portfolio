"""Merge the authored answer cards into assets/chat/kb.json and bump the chat's data version.

    python3 tools/chat_cards/merge.py                 # write assets/chat/kb.json and bump DATA_VERSION in chat.js
    python3 tools/chat_cards/merge.py --out /tmp/kb.json   # write somewhere else (for testing); chat.js untouched

Sources, all in this folder:
  work_examples.py      "show me an example of..." and "have you used X?" cards, plus PATCHES to existing cards
  interview_*.json      interview answer cards, one file per role family:
                        {"cards": [...], "add_questions": {"existing-id": [...]}, "replace_answers": {"iv-id": {...}}, "tests": [...]}

Base: kb_base.json, the curated kb.json before any authored cards. Output = base + authored cards + patches, so re-running is safe.
Note: kb_emb.bin (meaning-based search) is built separately from this; new cards are found by wording until it is rebuilt.
"""
import argparse, datetime, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KB = os.path.join(ROOT, "assets", "chat", "kb.json")
BASE = os.path.join(HERE, "kb_base.json")   # the curated kb.json before any authored cards; replace it when the main build changes
JS = os.path.join(ROOT, "assets", "chat", "chat.js")
sys.path.insert(0, HERE)
import work_examples as w  # noqa: E402

CARD_KEYS = ("id", "section", "section_label", "title", "questions", "tags", "links", "state", "answer", "prior", "parent", "nocanon")
DASH = re.compile(r"—|–|\s--\s|\s-\s")


def load_families(strict):
    fams = []
    for p in sorted(glob.glob(os.path.join(HERE, "interview_*.json"))):
        try:
            fams.append((os.path.basename(p), json.load(open(p, encoding="utf-8"))))
        except Exception as e:  # a file another writer is still editing
            if strict:
                raise
            print("skipping %s: %s" % (os.path.basename(p), e))
    return fams


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--strict", action="store_true", help="fail on any unreadable or invalid file")
    a = ap.parse_args()
    kb = json.load(open(BASE, encoding="utf-8"))
    by_id = {c["id"]: c for c in kb["cards"]}

    new_cards, problems = list(w.CARDS), []
    patches = {k: dict(v) for k, v in w.PATCHES.items()}
    for name, fam in load_families(a.strict):
        for c in fam.get("cards", []):
            c = {k: v for k, v in c.items() if k in CARD_KEYS}
            c.setdefault("state", "CLEAN")
            if not c.get("answer") or DASH.search(c["answer"]):
                problems.append("%s %s: missing answer or contains a dash" % (name, c.get("id")))
                continue
            new_cards.append(c)
        for cid, qs in fam.get("add_questions", {}).items():
            patches.setdefault(cid, {}).setdefault("add_questions", [])
            patches[cid]["add_questions"] = patches[cid]["add_questions"] + qs
        for cid, r in fam.get("replace_answers", {}).items():
            if DASH.search(r.get("answer", "")):
                problems.append("%s replace %s: contains a dash" % (name, cid)); continue
            patches.setdefault(cid, {}).update({k: v for k, v in r.items() if k in ("answer", "title", "add_links", "add_questions", "remove_questions", "tags")})

    ids = [c["id"] for c in new_cards]
    dup = {i for i in ids if ids.count(i) > 1} | (set(ids) & set(by_id))
    if dup:
        problems.append("duplicate ids: %s" % sorted(dup))
        seen = set(); new_cards = [c for c in new_cards if not (c["id"] in seen or seen.add(c["id"]) or c["id"] in by_id)]

    by_id.update({c["id"]: c for c in new_cards})
    bulk = os.environ.get("BULK", os.path.join(HERE, "phrasings_bulk.json"))   # bulk phrasing expansion, {card id: [phrasings]}
    if bulk and os.path.exists(bulk):
        for cid, qs in json.load(open(bulk, encoding="utf-8")).items():
            if cid in by_id:
                patches.setdefault(cid, {}).setdefault("add_questions", [])
                patches[cid]["add_questions"] = patches[cid]["add_questions"] + qs   # patches may also target authored cards (e.g. extra phrasings for ex-*)
    for cid, p in patches.items():
        if cid not in by_id:
            problems.append("patch for unknown card %s" % cid); continue
        c = by_id[cid]
        if "answer" in p: c["answer"] = p["answer"]
        if "title" in p: c["title"] = p["title"]
        if "tags" in p: c["tags"] = c["tags"] + [t for t in p["tags"] if t not in c["tags"]]
        rm = set(p.get("remove_questions", []))
        c["questions"] = [q for q in c["questions"] if q not in rm]
        for q in p.get("add_questions", []):
            if q not in c["questions"]: c["questions"].append(q)
        for link in p.get("add_links", []):
            if link["url"] not in [l["url"] for l in c["links"]]: c["links"].append(link)

    for c in new_cards:                            # cards waiting for her answer carry no answer text
        if c.get("state") == "PENDING":
            c.pop("answer", None)
    pos = max(i for i, c in enumerate(kb["cards"]) if c["section"] == "core") + 1
    kb["cards"][pos:pos] = new_cards
    if getattr(w, "FALLBACK", None):
        kb["fallback"] = w.FALLBACK
    extra = os.path.join(HERE, "synonyms_extra.json")   # extra alias groups (the "keyword net"), each kept only if tests improve
    for g in (json.load(open(extra, encoding="utf-8")) if os.path.exists(extra) else []):
        if g not in kb["synonyms"]: kb["synonyms"].append(g)
    # every non-personal answer gets at least one place to go and see the work it talks about
    RULES = [(r"agent", [("Agent architecture", "agent-architecture.html")]), (r"skyrule", [("Skyrule", "skyrule.html")]),
             (r"legislat|\bbill", [("Legislative pipeline", "legislative-pipeline.html")]),
             (r"local model|open.weight|self.host|small model|open source", [("Choosing a local model (guide)", "choosing-local-models-guide.html")]),
             (r"procure|messy data", [("Procurement intelligence", "procurement-intelligence.html")]),
             (r"monitor|pipeline", [("Applied AI Lab", "https://tayler-erbe.github.io/document-intelligence-lab/")])]
    FUN = re.compile(r"^(personal-|answer-fun|answer-q6|persona-(dessert|drinks|movies|vibe))")
    for c in kb["cards"]:
        if c.get("links") or c.get("section") not in ("answers", "opinions") or FUN.match(c["id"]):
            continue
        text = (c["title"] + " " + c.get("answer", "")).lower()
        links = [l for pat, ls in RULES if re.search(pat, text) for l in ls][:2]
        links = links or [("My projects", "index.html#projects")]
        if c["section"] == "opinions" or re.match(r"^(persona-|answer-(op|li|q))", c["id"]):
            links.append(("My writing on Medium", "https://medium.com/@tayler.erbe"))
        c["links"] = [{"label": a, "url": b} for a, b in links[:3]]
    for c in kb["cards"]:                          # the Agent City section moved off the Skyrule page (12 Nov 2026)
        for l in c.get("links", []):
            if l["url"] == "skyrule.html#agent-city":
                l["url"] = "agent-city.html"
    kb["built"] = datetime.date.today().isoformat()
    out = a.out or KB
    with open(out, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, separators=(",", ":"))
    if not a.out:
        js = open(JS, encoding="utf-8").read()
        m = re.search(r'var DATA_VERSION = "(\d+)"', js)
        stamp = datetime.date.today().strftime("%Y%m%d"); old = m.group(1)
        nv = str(int(old) + 1) if old.startswith(stamp) else stamp + "01"
        open(JS, "w", encoding="utf-8").write(js.replace(m.group(0), 'var DATA_VERSION = "%s"' % nv))
        print("DATA_VERSION %s -> %s" % (old, nv))
    print("wrote %s: %d cards (%d authored, %d patched)" % (out, len(kb["cards"]), len(new_cards), len(patches)))
    for p in problems: print("PROBLEM:", p)
    return 1 if (problems and a.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
