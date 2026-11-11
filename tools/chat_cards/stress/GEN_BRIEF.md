# Write blind test questions for the "Ask about Tayler" chat

taylererbe.com has a chat panel where visitors type questions about Tayler Erbe (a data scientist / applied AI engineer at the
University of Illinois System who is job hunting for forward-deployed engineering, AI consulting, applied AI engineering, applied
AI data science, AI data engineering and AI solutions architecture roles). The chat matches each question to one of about 1,100
pre-written answers. You are writing realistic questions to stress-test it.

RULES
- Do NOT open or read anything under /home/user/tayler-portfolio/assets/chat/ or /home/user/tayler-portfolio/tools/ or
  /home/user/jobhunter/chatbot/. The test must be blind to how the answers are stored.
- You MAY read the public site pages as plain text to learn what her work is: /tmp/claude-0/-home-user-research-proposal-processing/f1061a4e-d852-5fbc-9167-05222635bed5/scratchpad/txt/*.txt
  (index.txt is the home page; one file per case study).
- Write exactly 200 questions, all different in substance or wording, the way real people type into a chat box. Mix the styles:
  about 35% full natural questions, 30% short casual ones ("ever used docker?"), 15% keyword-only ("rag experience"),
  10% third person ("has she worked with oracle", "what did tayler build for hr"), 5% with realistic typos or sloppy
  grammar, 5% long multi-part questions. Vary the vocabulary; do not reuse the site's exact headings as questions.
- Include questions whose honest answer is "no / not really" (tools or experience she probably lacks), because people ask those.
- Output: a JSON file, a list of 200 objects: {"q": "the question", "intent": "8 to 15 words on what a good answer must cover"}.
  Validate it with python3 -c "import json;print(len(json.load(open(PATH))))" and make sure it prints 200.
- Reply with one line: the path and the count.
