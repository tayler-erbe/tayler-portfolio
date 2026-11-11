# Authored answer cards for "Ask about Tayler"

`assets/chat/kb.json` = `kb_base.json` (the curated chat as of 10 Nov 2026) + the cards in this folder.

| File | What it holds |
|---|---|
| `work_examples.py` | "Show me an example of..." (`ex-`) and "have you used X?" (`tech-`) cards, `PATCHES` to existing cards, routing phrasings, and the `FALLBACK` (no-answer) message |
| `interview_<family>.json` | Technical interview answers per role: `aie-` applied AI engineering, `ads-` applied data science, `ade-` AI data engineering, `fde-` forward-deployed engineering, `arc-` AI solutions architecture, `con-` AI consulting. Each card lists its `sources` (work_history.md lines, pages); each file carries held-out `tests` and `gaps` |
| `synonyms_extra.json` | Extra alias groups (the keyword net); each was kept only because the tests did not get worse |
| `tests/` | Blind interview questions, questions the chat should decline, and example-question sets |

Every answer was written from Tayler's sources with her permission (11 Nov 2026) and then fact-checked line by line against them.

## Change something

1. Edit a card (or add one) in the files above.
2. Build: `python3 tools/chat_cards/merge.py --strict` (writes `kb.json`, bumps `DATA_VERSION` in `chat.js`).
3. Rebuild the meaning-search file (needs network access to huggingface.co):
   `NODE_USE_ENV_PROXY=1 python3 ../jobhunter/chatbot/emb/build_emb.py --kb assets/chat/kb.json --out assets/chat/kb_emb.bin`
4. Test: `node tools/chat_cards/test_cards.js tools/chat_cards/interview_*.json tools/chat_cards/tests/examples_*.json`
   (add `--emb assets/chat/kb_emb.bin` for the hybrid search the browser uses; `--show` to print every route).

If the main pipeline (`jobhunter/chatbot/build_kb.py`) produces a new kb.json, copy it over `kb_base.json` first, then run step 2.
Diff it against `kb_base.json` before replacing: a few cards were edited directly on the site after that pipeline's last build.
