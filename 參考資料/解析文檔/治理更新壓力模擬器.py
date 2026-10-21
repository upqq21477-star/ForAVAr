#!/usr/bin/env python3
"""Synthetic governance stress model. Standard library only; not a live runtime test."""
import json, random
from collections import Counter
from statistics import mean

LIMIT=7200
TYPES=("novel","duplicate","refinement","conflict","unverified","incident","routine")
MIX=(22,25,18,10,10,8,7)
# name, preflight, dedup recall, false merge, conflict recall, unsupported recall,
# dual check, fail closed, tx failure, rollback success, split content/logs,
# trace chars, source chars, exception chars, index chars
POL=[
("V0_append",0,0,0,0,0,False,False,.022,0,False,False,250,0,0,0),
("V1_partial",.60,.88,.025,.68,.56,False,False,.015,.10,True,True,170,90,330,55),
("V2_preflight",.98,.94,.020,.96,.96,False,False,.006,.95,True,True,115,95,300,48),
("V3_iterative",.995,.985,.003,.995,.998,False,False,.003,.995,True,True,80,90,210,42),
("V4_patched",.999,.992,.0005,.999,.999,False,False,.003,.999,True,True,70,80,180,38),
("V5_failclosed_dual",.999,.992,.0005,.999,.999,True,True,.003,.9999,True,True,70,80,180,38),
]
def events(seed,n):
    r=random.Random(seed); pool=[f"S{i:04d}" for i in range(600)]; nov=0; out=[]
    for i in range(n):
        typ=r.choices(TYPES,weights=MIX,k=1)[0]; topic=f"T{r.randrange(120):03d}"
        if typ=="novel":
            key=f"N{seed}_{nov}";nov+=1;pool.append(key)
        elif typ in ("duplicate","refinement","conflict") and r.random()<.90: key=r.choice(pool)
        elif typ in ("unverified","incident","routine") and r.random()<.75: key=r.choice(pool)
        else:
            key=f"S{r.randrange(600):04d}"
            if key not in pool: pool.append(key)
        out.append((typ,topic,key,r.randint(180,330)))
    return out
def add(parts,size,split):
    if split:
        if parts[-1]+size>LIMIT: parts.append(0)
    parts[-1]+=size
def run(pol,ev,seed):
    (name,pf,dedup,merge,conf,unsup,dual,closed,tx,rb,split,splitlog,
     trace,source,exc,index)=pol
    r=random.Random(seed); docs={f"T{i:03d}":[4000] for i in range(120)}
    m=Counter(); logs=[0]; src=[0]; cases=[0]
    for typ,topic,key,size in ev:
        gate=r.random()<pf; m["gate"]+=int(gate)
        if not gate and closed:
            m["blocked"]+=1;add(logs,trace,splitlog);add(src,source,splitlog);continue
        action=None
        if typ=="novel": action=("novel",size)
        elif typ=="duplicate":
            if gate and r.random()<dedup:m["dup_link"]+=1
            else:action=("dup",size)
        elif typ=="refinement":
            if gate and r.random()<merge:m["mismerge"]+=1
            else:action=("refine",size)
        elif typ=="conflict":
            found=gate and r.random()<conf
            if gate and dual:found=found or r.random()<conf
            if found:m["conflict_quarantine"]+=1
            else:action=("conflict",size)
        elif typ=="unverified":
            found=gate and r.random()<unsup
            if gate and dual:found=found or r.random()<unsup
            if found:m["unsup_quarantine"]+=1
            else:action=("unsup",size)
        elif typ=="incident":m["incident"]+=1
        else:m["routine"]+=1
        commit=bool(action)
        if action and r.random()<tx:
            m["tx_fail"]+=1
            if not split:m["partial"]+=1
            elif r.random()<rb:m["rollback"]+=1;commit=False
            else:m["partial"]+=1
        if commit and action:
            kind,amount=action; dest=docs[topic]
            if split and dest[-1]+amount>LIMIT:dest.append(450);m["shards"]+=1
            dest[-1]+=amount;m[kind]+=1
        add(logs,trace,splitlog)
        if source:add(src,source,splitlog)
        if exc and typ in ("conflict","unverified","incident"):add(cases,exc,splitlog)
    lengths=[x for vv in docs.values() for x in vv]; ncontent=len(lengths)
    nindex=(ncontent+len(logs)+len(src)+len(cases))*index
    ix=[0]
    while nindex:
        take=min(LIMIT-ix[-1],nindex);ix[-1]+=take;nindex-=take
        if nindex:ix.append(0)
    files=ncontent+len(logs)+(len(src) if source else 0)+(len(cases) if exc else 0)+(len(ix) if index else 0)
    all_lengths=lengths+logs+(src if source else [])+(cases if exc else [])+(ix if index else [])
    audit=sum(logs)+(sum(src) if source else 0)+(sum(cases) if exc else 0)+sum(ix)
    return {"name":name,"preflight_pct":100*m["gate"]/len(ev],"blocked":m["blocked"],
        "duplicates":m["dup"],"conflicts":m["conflict"],"unsupported":m["unverified"],
        "refinement_mismerge":m["mismerge"],"partial":m["partial"],"rollback":m["rollback"],
        "files":files,"oversized":sum(x>8000 for x in all_lengths),"maxfile":max(all_lengths),
        "chars":sum(lengths)+audit,"active_chars":sum(lengths),"audit_chars":audit}
def main():
    rows=[]
    for seed in range(20261021,20261026):
        ev=events(seed,10_000)
        for i,p in enumerate(POL):rows.append(run(p,ev,(seed%1000)+i*151))
    summary=[]
    for p in POL:
        g=[x for x in rows if x["name"]==p[0]]
        obj={"scenario":p[0],"workloads":5,"updates_each":10000}
        for k in ("preflight_pct","blocked","duplicates","conflicts","unsupported",
                  "refinement_mismerge","partial","files","oversized","maxfile","chars"):
            v=[x[k] for x in g];obj[k+"_mean"]=round(mean(v),2)
            if k in ("files","oversized","maxfile","chars"):obj[k+"_min"]=min(v);obj[k+"_max"]=max(v)
        summary.append(obj)
    scale=run(POL[-1],events(20261099,100_000),599)
    print(json.dumps({"notice":"Synthetic workload; no model weights or live GitHub runtime were run.",
        "event_mix_percent":dict(zip(TYPES,MIX)),"10k_runs":summary,
        "100k_scale_check":{k:scale[k] for k in ("files","maxfile","chars","active_chars","audit_chars","oversized","blocked","partial")}},
        ensure_ascii=False,indent=2))
if __name__=="__main__":main()
