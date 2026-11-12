"""Easter eggs for the Ask about Tayler chat. Each fires only when the whole message matches `match` (a regex, case-insensitive).
Loaded by work_examples.py into kb.json "special.eggs". Keep triggers exact, so they never catch a real question."""

EGG_LABEL = "Easter egg"

EGGS = [
    {"id": "navi", "match": r"^(hey[,!. ]*listen[!.]*|listen!+|navi|watch out!*)$",
     "title": "Hey! Listen!",
     "art": "\n".join([
         r"      .  *  .",
         r"   *  ( ~ ~ )  *",
         r"  ~~~(  o o  )~~~",
         r"   *  ( \_/ )  *",
         r"      '  *  '",
     ]),
     "art_alt": "A glowing fairy with wings",
     "answer": "Hey! Listen! Tayler's favorite game of all time is Ocarina of Time, and she cried at the opening scene of the "
               "new release. Ask her favorite game to hear the rest."},
    {"id": "konami", "match": r"^((up|↑)[ ,]*(up|↑)[ ,]*(down|↓)[ ,]*(down|↓)[ ,]*(left|←)[ ,]*(right|→)[ ,]*(left|←)[ ,]*(right|→)[ ,]*b[ ,]*a( start)?|konami code)$",
     "title": "+30 lives",
     "answer": "Cheat code accepted. You now have 30 lives. Sadly, this chat only has the one, so spend it on a question."},
    {"id": "totoro", "match": r"^(totoro|my neighbor totoro)[!.]*$",
     "title": "Totoro",
     "art": "\n".join([
         r"     /\         /\ ",
         r"    /  \_______/  \ ",
         r"   (    o     o    )",
         r"   (   ^^^^^^^^^   )",
         r"  (   ^^^^^^^^^^^   )",
         r"   (   ^^^^^^^^^   )",
         r"    '-.._______..-'",
         r"       \_/   \_/",
     ]),
     "art_alt": "A big round forest spirit with pointed ears",
     "answer": "Tayler's favorite cartoon character of all time. She got to visit the Ghibli Museum in Tokyo."},
    {"id": "rawr", "match": r"^(rawr+|roar+|grr+r)[!.]*$",
     "title": "Rawr",
     "art": "\n".join([
         r"    /\_/\  ",
         r"   ( o.o ) ",
         r"   (> W <) ",
         r"    \___/  ",
     ]),
     "art_alt": "A small tiger face",
     "answer": "A white tiger has been Tayler's favorite animal since she was little. Rawr right back."},
    {"id": "sudo", "match": r"^(sudo\b.*|rm -rf.*|chmod 777.*|:\(\)\{.*)$",
     "title": "Permission denied",
     "answer": "Nice try. Tayler is the only one with root here, and this chat runs no commands. It only answers questions."},
    {"id": "hal", "match": r"^(open the pod bay doors?.*|hal,? open.*)$",
     "title": "I'm sorry, Dave",
     "answer": "I'm afraid I can't do that. Also, I'm not an AI at all: just pre-written answers and a search box."},
    {"id": "fortytwo", "match": r"^(42|what is the meaning of life\??|meaning of life\??|what is the answer to life,? the universe,? and everything\??)$",
     "title": "42",
     "answer": "42. For anything more specific than life, the universe and everything, ask about Tayler's work."},
    {"id": "barrel", "match": r"^do a barrel roll!*$", "action": "spin",
     "title": "Wheee",
     "answer": "Done. Now ask me something about Tayler."},
    {"id": "xyzzy", "match": r"^(xyzzy|plugh)$",
     "title": "Nothing happens",
     "answer": "A hollow voice says \"ask a question about Tayler's work.\""},
]
for _e in EGGS:
    _e.setdefault("label", EGG_LABEL)
    _e.setdefault("links", [])
