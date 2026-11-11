"""Merge the cards in work_examples.py into assets/chat/kb.json and bump the chat's data version.

    python3 tools/chat_cards/merge.py

Safe to re-run: new cards replace any card with the same id, and patches are idempotent.
Note: kb_emb.bin (meaning-based search) is built separately; new cards are found by wording until it is rebuilt.
"""
import datetime, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KB = os.path.join(ROOT, "assets", "chat", "kb.json")
JS = os.path.join(ROOT, "assets", "chat", "chat.js")
sys.path.insert(0, HERE)
import work_examples as w  # noqa: E402

kb = json.load(open(KB, encoding="utf-8"))
new_ids = {c["id"] for c in w.CARDS}
kb["cards"] = [c for c in kb["cards"] if c["id"] not in new_ids]
by_id = {c["id"]: c for c in kb["cards"]}

for cid, p in w.PATCHES.items():
    c = by_id[cid]
    if "answer" in p:
        c["answer"] = p["answer"]
    rm = set(p.get("remove_questions", []))
    c["questions"] = [q for q in c["questions"] if q not in rm]
    for q in p.get("add_questions", []):
        if q not in c["questions"]:
            c["questions"].append(q)
    for link in p.get("add_links", []):
        if link["url"] not in [l["url"] for l in c["links"]]:
            c["links"].append(link)

# keep the new cards together, after the core "About" cards
pos = max(i for i, c in enumerate(kb["cards"]) if c["section"] == "core") + 1
kb["cards"][pos:pos] = w.CARDS
kb["built"] = datetime.date.today().isoformat()

with open(KB, "w", encoding="utf-8") as f:
    json.dump(kb, f, ensure_ascii=False, separators=(",", ":"))

js = open(JS, encoding="utf-8").read()
m = re.search(r'var DATA_VERSION = "(\d+)"', js)
stamp = datetime.date.today().strftime("%Y%m%d")
old = m.group(1)
nv = str(int(old) + 1) if old.startswith(stamp) else stamp + "01"
open(JS, "w", encoding="utf-8").write(js.replace(m.group(0), 'var DATA_VERSION = "%s"' % nv))
print("cards: %d total, %d new/updated, %d patched; DATA_VERSION %s -> %s" % (len(kb["cards"]), len(w.CARDS), len(w.PATCHES), old, nv))
