#!/usr/bin/env python3
"""python3 kbfind.py word1 word2 ...   -> cards whose title/answer/questions contain ALL the words (id | title | first 160 chars)
   python3 kbfind.py --id CARD_ID      -> that card's title, full answer and question phrasings"""
import json,sys
kb=json.load(open('/home/user/tayler-portfolio/assets/chat/kb.json'))['cards']
a=sys.argv[1:]
if a and a[0]=='--id':
    for c in kb:
        if c['id']==a[1]: print(c['title'],'\n',c.get('answer',''),'\nQUESTIONS:',' | '.join(c['questions']))
else:
    w=[x.lower() for x in a];n=0
    for c in kb:
        t=(c['title']+' '+c.get('answer','')+' '+' '.join(c['questions'])+' '+' '.join(c.get('tags',[]))).lower()
        if all(x in t for x in w):
            n+=1
            if n<=25: print(c['id'],'|',c['title'],'|',c.get('answer','')[:160])
    print(n,'cards')
