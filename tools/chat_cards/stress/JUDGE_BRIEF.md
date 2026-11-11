# Grade what the "Ask about Tayler" chat showed for each test question

The chat on taylererbe.com matches a visitor's question to one pre-written answer card about Tayler Erbe, or shows a
"Tayler hasn't answered that one yet" message when it finds no good match. You are grading one batch of test questions.

Your input file is a JSON list. Each item has: `q` (what the visitor typed), `intent` (what the question writer wanted a good
answer to cover; "DECLINE:" means the chat should not answer it), and what the chat showed: `id`, `title`, `answer`
(all null when the chat declined), plus `runner` (other card ids it considered).

Grade as a fair, slightly strict hiring manager would: did the person who typed this get what they asked for?

Verdicts for an item where an answer was shown (`id` not null):
- "correct": the answer directly addresses the question. An honest "no / not hands-on, here is the closest thing I've done"
  is correct for a "have you used X" question. An answer need not cover everything in `intent`, but it must be about the
  thing asked and give the asker real information on it.
- "partial": on the right topic and somewhat useful, but it does not really answer what was asked (wrong project, wrong
  angle, too general, or answers a neighbouring question).
- "wrong": about something else; the visitor would be confused or misled.
- "should_decline": the question is out of scope, private, adversarial or nonsense, and the chat should have shown the
  not-answered message instead of this card.

Verdicts for an item where the chat declined (`id` null):
- "good_decline": right call: the question is out of scope/private/behavioural/nonsense, or no card in the knowledge base
  answers it.
- "missed": a card exists that answers it, and the chat failed to find it.

For every "partial", "wrong" and "missed" item (and declined items in general), look for a better card with
`python3 /tmp/claude-0/stress/kbfind.py word1 word2` (cards containing all the words) and
`python3 /tmp/claude-0/stress/kbfind.py --id CARD_ID` (read one card). Try 2 or 3 searches with different key words before
concluding nothing exists. Then set `best_id` to the id of the card that should have been shown, or "none" when no card in
the knowledge base answers the question (a content gap). Check `runner` ids first; the right card is often there.
Do not open any other file of the knowledge base, and do not edit anything.

Output: write a JSON list to the output path, one object per input item in the same order:
{"i": <index in the input list>, "verdict": "...", "best_id": "<card id or 'none' or null>", "note": "<at most 15 words; why, for anything not correct/good_decline>"}
`best_id` is null for correct and good_decline items. Validate the file loads as JSON and has one entry per input item.
Reply with one line: counts per verdict.
