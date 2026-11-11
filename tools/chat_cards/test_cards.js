// Route test questions through the real chat engine (assets/chat/chat.js) and report misses.
//   node tools/chat_cards/test_cards.js [--kb path/to/kb.json] [--prefix fde-] [tests files...]
// A tests file is either an interview_*.json (its "tests" key) or a JSON list of [question, "id|other-id"].
// With --prefix, also checks that every question variant of the matching cards routes to its own card.
// --show prints every routed question, not just misses.
// --emb path/to/kb_emb.bin  also runs the meaning-based (hybrid) search the browser uses once its model loads. Needs
//   @huggingface/transformers (TRANSFORMERS_DIR, default /home/user/jobhunter/chatbot/emb/node_modules) and network access
//   to huggingface.co (in Node 22: NODE_USE_ENV_PROXY=1 behind a proxy).
const fs = require("fs"), path = require("path");
const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); if (i < 0) return null; const v = args[i + 1]; args.splice(i, 2); return v; };
const flag = (k) => { const i = args.indexOf(k); if (i < 0) return false; args.splice(i, 1); return true; };
const root = path.resolve(__dirname, "..", "..");
const kbPath = opt("--kb") || path.join(root, "assets", "chat", "kb.json");
const prefix = opt("--prefix"), show = flag("--show"), embPath = opt("--emb");
global.window = { matchMedia: () => ({ matches: false }), innerWidth: 1000, addEventListener() {} };
global.document = { readyState: "loading", addEventListener() {}, documentElement: {}, querySelector() { return null; },
  currentScript: { src: "x/chat.js" }, getElementsByTagName() { return []; },
  createElement() { return { setAttribute() {}, appendChild() {}, addEventListener() {}, style: {} }; }, head: { appendChild() {} }, body: { appendChild() {} } };
eval(fs.readFileSync(path.join(root, "assets", "chat", "chat.js"), "utf8"));
const kb = JSON.parse(fs.readFileSync(kbPath, "utf8"));
const eng = new window.AskTayler.Engine(kb);
let qv = new Map();
const route = (q) => { const r = eng.search(q, qv.get(q)); return r.confident && r.best ? r.best.card.id : "(no answer)"; };
(async () => {
const files = args.map((f) => [f, (() => { const d = JSON.parse(fs.readFileSync(f, "utf8")); return Array.isArray(d) ? d : (d.tests || []); })()]);
if (embPath) {
  const buf = fs.readFileSync(embPath); const head = eng.setEmbeddings(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.length));
  const dir = process.env.TRANSFORMERS_DIR || "/home/user/jobhunter/chatbot/emb/node_modules";
  const lib = await import(path.join(dir, "@huggingface/transformers/dist/transformers.mjs"));
  lib.env.allowLocalModels = false;
  const fe = await lib.pipeline("feature-extraction", head.model, { revision: head.revision, dtype: head.dtype || "q8" });
  const qs = new Set(); for (const [, t] of files) for (const [q] of t) qs.add(q);
  if (prefix) for (const c of kb.cards) if (c.id.startsWith(prefix)) for (const q of c.questions) qs.add(q);
  const list = [...qs];
  for (let i = 0; i < list.length; i += 64) {
    const r = await fe(list.slice(i, i + 64), { pooling: "mean", normalize: true }); const d = r.dims[1];
    for (let j = 0; j < r.dims[0]; j++) qv.set(list[i + j], new Float32Array(r.data.slice(j * d, (j + 1) * d)));
  }
  console.log(`hybrid search on: ${head.model}, ${list.length} questions embedded`);
}
let total = 0, bad = 0;
if (prefix) {
  let n = 0, m = 0;
  for (const c of kb.cards) if (c.id.startsWith(prefix)) for (const q of c.questions) { n++; const g = route(q); if (g !== c.id) { m++; console.log("OWN  ", JSON.stringify(q), "->", g, " want", c.id); } }
  console.log(`own phrasings: ${n - m}/${n}`);
}
for (const [f, tests] of files) {
  let ok = 0;
  for (const [q, want] of tests) {
    const w = String(want).split("|"), g = route(q); total++;
    if (w.includes(g)) { ok++; if (show) console.log("ok   ", JSON.stringify(q), "->", g); }
    else { bad++; console.log("MISS ", JSON.stringify(q), "->", g, " want", w.join("|")); }
  }
  console.log(`${path.basename(f)}: ${ok}/${tests.length} held-out questions routed correctly`);
}
process.exitCode = bad ? 1 : 0;
})();
