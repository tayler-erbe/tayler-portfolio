#!/usr/bin/env python3
"""python3 analyze.py [routed.json] [grades prefix] -> results.json + printed diagnosis.
Cause of each failure:
  gap            no card answers it (best_id none)                      -> write a new answer
  ranking        right card was in the engine's top 4 but not first      -> phrasings/priors
  vocabulary     right card exists but was nowhere near the top          -> phrasings/tags/aliases
  over_decline   right card exists, chat declined                        -> phrasings or threshold
  over_answer    should have declined, answered anyway                   -> threshold / decoy
  weak_answer    judged partial and the shown card IS the best card      -> improve that answer
"""
import json,sys,collections
D='/tmp/claude-0/stress/'
routed=json.load(open(sys.argv[1] if len(sys.argv)>1 else D+'routed.json'))
pre=sys.argv[2] if len(sys.argv)>2 else D+'grades_'
kbids={c['id'] for c in json.load(open('/home/user/tayler-portfolio/assets/chat/kb.json'))['cards']}
rows=[]
for b in range(5):
    g={x['i']:x for x in json.load(open(f'{pre}{b}.json'))}
    for i in range(200):
        r=dict(routed[b*200+i]); x=g.get(i,{'verdict':'ungraded','best_id':None,'note':''})
        v,best=x['verdict'],x.get('best_id')
        if best not in kbids and best not in (None,'none'): best='none?'+str(best)
        if v in('correct','good_decline'): cause='ok'
        elif v=='should_decline': cause='over_answer'
        elif best in(None,'none') or str(best).startswith('none?'): cause='gap'
        elif v=='missed': cause='over_decline'
        elif best==r['id']: cause='weak_answer'
        elif best in r['runner'] or best in r.get('related',[]): cause='ranking'
        else: cause='vocabulary'
        r.update(verdict=v,best_id=best,note=x.get('note',''),cause=cause); r.pop('answer',None); rows.append(r)
json.dump(rows,open(D+'results.json','w'),indent=1)
def table(key,rs):
    t=collections.defaultdict(collections.Counter)
    for r in rs: t[key(r)][r['cause']]+=1
    cs=['ok','gap','ranking','vocabulary','over_decline','over_answer','weak_answer']
    print(f"{'':32s}"+''.join(f'{c[:9]:>10s}' for c in cs)+'   ok%')
    for k,c in sorted(t.items(),key=lambda kv:-sum(kv[1].values())):
        n=sum(c.values()); print(f'{str(k)[:31]:32s}'+''.join(f'{c[x]:10d}' for x in cs)+f'  {100*c["ok"]/n:4.0f}%  (n={n})')
for sp in('all','dev','test'):
    rs=[r for r in rows if sp=='all' or r['split']==sp]
    print(f'\n== {sp}: {sum(r["cause"]=="ok" for r in rs)}/{len(rs)} ok');
    if sp=='all':
        print(collections.Counter(r['verdict'] for r in rs)); table(lambda r:r['slice'],rs); print(); table(lambda r:r['style'].split('+')[0],rs)
