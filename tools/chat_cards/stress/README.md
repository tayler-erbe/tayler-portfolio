# 1,000-question stress test (11 Nov 2026)

`questions.json`: 1,000 blind questions (written without seeing the stored phrasings), each with an `intent`, a `slice`
(who would ask it), a `style`, and a `split`: `dev` (failures may be fixed) or `test` (never used for fixes; the honest score).

How a round runs: `route.js` sends every question through the real engine (hybrid search, as in the browser) and records
what a visitor would see. Graders (Sonnet, following `JUDGE_BRIEF.md`) mark each response correct / partial / wrong /
missed / good_decline / should_decline and name the card that should have won. `analyze.py` turns that into a cause per
failure: gap (no answer exists), ranking (right card was runner-up), vocabulary (right card nowhere near), over_decline,
over_answer. The scripts use absolute paths from the session they were written in; adjust before re-running.

| | fix half (dev, 500) | held-out half (test, 500) |
|---|---|---|
| Round 0, before fixes | 345 (69%) | 363 (73%) |
| Round 1, after 121 routing phrasings + 4 new cards | 464 (93%) | 363 (73%) |

Reading: adding the failed questions as phrasings fixes those questions and nothing else. On the held-out half, 87%
of responses were on-topic or better and 5% were plainly wrong. A sweep of 144 engine settings found none better than the
current ones. The remaining levers are content (34 gaps found) and a stronger matching method.

## Round 2 (same day): fresh 300 questions

After round 1 both halves of the 1,000 were used for routing fixes, so a fresh blind set of 300 was written and graded
(`fresh300_*`). On it: 226/300 (75%) before, 238/300 (79%) after adding 139 fact-checked deep-dive cards for six thinly
covered pages, broader decline cards and 18 fun placeholders. On-topic or better: 272 -> 277.

Tried and rejected, each measured on held-out questions: bulk phrasing expansion by a cheap model (15,000 phrasings;
top-1 fell from 282 to 240 of 428), the same phrasings in the meaning index only (312 -> 307), a larger embedding model
(bge-base: 209 vs 218 of 283), looser decline thresholds, and 144 engine setting combinations.
