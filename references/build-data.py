#!/usr/bin/env python3
"""
Enkoder danych dla meta-ads-checklist-by-mta-hubert-rado.
Wejście: CSV-e z pull (3 okna atrybucji + breakdowny) o nagłówkach jak niżej.
Wyjście: /tmp/DATA.json, /tmp/BRK.json — wstrzykiwane w markery skeletonu:
   const DATA=/*__INJECT_DATA__*/{...};  ->  const DATA=<DATA.json>;
   const BRK=/*__INJECT_BRK__*/{...};    ->  const BRK=<BRK.json>;
Uruchom z katalogu z CSV-ami (MTA_SRV_FBA/raw/<YYYY-MM>/) albo popraw ścieżki.

RAW CSV (per okno) — dokładnie te kolumny (18), kolejność dowolna (po nagłówku):
 Date, Campaign name, AdSet name, Ad name, Year-Month, Year-Week (Starting on Monday),
 Total Cost, Reach, Impressions, Link clicks, Outbound clicks, Landing page views,
 Website content views, Website adds to cart, Website checkouts initiated,
 Website purchases, Website purchases conversion value, Website adds of payment info
BREAKDOWN CSV (placement/age) — Date, <segment>, cost, impr, reach, clicks, pur, roas (val=cost*roas)
"""
import csv, json, os
WIN_FILES={'1dc':['meta-adlevel-1dc.csv'],'7dc':['meta-adlevel-7dc.csv'],'7dc1dv':['meta-adlevel-7dc1dv.csv','meta-3windows-7dc1dv.csv']}
BRK_FILES={'placement':('meta-breakdown-placement-daily.csv','placement'),
           'age':('meta-breakdown-age-daily.csv','age')}
# miesiące TM/LM wyliczane automatycznie z danych (dwa ostatnie obecne) — nie hardkoduj okresu
def num(x):
    try: return float(str(x).replace(',','').replace('PLN','').strip())
    except: return 0.0
def iso(s):  # "May 1, 2026"/"2026-05-01" -> 2026-05-01 ; rok z daty (fallback: bieżący kontekst)
    import re;s=str(s)
    if len(s)>=10 and s[4]=='-': return s[:10]
    M={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    m=re.match(r'^([A-Z][a-z]{2})\w*\s+(\d{1,2})\D*(\d{4})?',s)
    if not m: return s
    yr=m.group(3) or '2026'  # gdy rok ucięty w źródle — popraw na właściwy
    return '%s-%s-%02d'%(yr,M[m.group(1)],int(m.group(2)))

def col(r,*names):
    for n in names:
        if n in r: return r[n]
    return ''

def build_window(path):
    rows=list(csv.DictReader(open(path)))
    yms,yws,dates,camps,adsets,ads=[],[],[],[],[],[]
    def idx(a,v):
        v=v or ''
        if v not in a:a.append(v)
        return a.index(v)
    craw=[]
    for r in rows:
        dt=iso(col(r,'Date'))[:10]
        ym=col(r,'Year-Month') or (dt[:4]+'|'+dt[5:7])
        yw=col(r,'Year-Week (Starting on Monday)','Year-Week') or ''
        craw.append([idx(yms,ym),idx(yws,yw),idx(dates,dt),
            idx(camps,col(r,'Campaign name')),idx(adsets,col(r,'AdSet name')),idx(ads,col(r,'Ad name')),
            round(num(col(r,'Total Cost')),2),int(num(col(r,'Reach'))),int(num(col(r,'Impressions'))),
            int(num(col(r,'Link clicks'))),int(num(col(r,'Outbound clicks'))),int(num(col(r,'Landing page views'))),
            int(num(col(r,'Website content views'))),int(num(col(r,'Website adds to cart'))),
            int(num(col(r,'Website checkouts initiated'))),int(num(col(r,'Website purchases'))),
            round(num(col(r,'Website purchases conversion value')),2),int(num(col(r,'Website adds of payment info')))])
    lut={'yms':yms,'yws':yws,'dates':dates,'camps':camps,'adsets':adsets,'ads':ads}
    F=['cost','reach','impr','clicks','oc','lpv','cv','atc','ic','pur','val','api']
    C={'cost':6,'reach':7,'impr':8,'clicks':9,'oc':10,'lpv':11,'cv':12,'atc':13,'ic':14,'pur':15,'val':16,'api':17}
    def deriv(o):
        o=dict(o)
        o['freq']=o['impr']/o['reach'] if o['reach'] else 0
        o['ctr']=o['oc']/o['impr'] if o['impr'] else 0
        o['cpm']=o['cost']/o['impr']*1000 if o['impr'] else 0
        o['roas']=o['val']/o['cost'] if o['cost'] else 0
        o['aov']=o['val']/o['pur'] if o['pur'] else 0
        o['cpp']=o['cost']/o['pur'] if o['pur'] else 0
        o['crpc']=o['pur']/o['ic'] if o['ic'] else 0
        o['crpa']=o['pur']/o['atc'] if o['atc'] else 0
        o['crpv']=o['pur']/o['cv'] if o['cv'] else 0
        o['crpl']=o['pur']/o['lpv'] if o['lpv'] else 0
        for k in ('cost','val','cpm','aov','cpp'):o[k]=round(o[k],2)
        for k in ('freq','ctr','roas','crpc','crpa','crpv','crpl'):o[k]=round(o[k],6)
        return o
    def agg(keyfn):
        m={}
        for c in craw:
            k=keyfn(c)
            if k not in m:m[k]={f:0 for f in F};m[k]['_yw']=set();m[k]['_ads']=set();m[k]['_sets']=set()
            for f in F:m[k][f]+=c[C[f]]
            m[k]['_yw'].add(c[1]);m[k]['_ads'].add(c[5]);m[k]['_sets'].add(c[4])
        return m
    total=sum(c[6] for c in craw) or 1
    mm=agg(lambda c:yms[c[0]]);month=[{**{k:deriv(mm[ym])[k] for k in deriv(mm[ym]) if not k.startswith('_')},'ym':ym} for ym in sorted(mm)]
    def byday(t):
        m={}
        for c in craw:
            if yms[c[0]]!=t:continue
            d=dates[c[2]]
            if d not in m:m[d]={f:0 for f in F}
            for f in F:m[d][f]+=c[C[f]]
        return [{**{k:deriv(m[d])[k] for k in deriv(m[d]) if not k.startswith('_')},'date':d} for d in sorted(m)]
    months=sorted({c0[0] for c0 in [[yms[c[0]]] for c in craw]});CUR=months[-1] if months else '';PREV=months[-2] if len(months)>1 else CUR
    tm=byday(CUR);lm=byday(PREV)
    def rollup(name_key):
        a=agg(lambda c:({'camp':camps[c[3]],'adset':adsets[c[4]]}[name_key]));out=[]
        for nm,raw in a.items():
            nw=len(raw['_yw']) or 1;o=deriv({f:raw[f] for f in F})
            o={k:o[k] for k in o if not k.startswith('_')};o[name_key]=nm
            o['nads']=len(raw['_ads']);o['spshare']=round(raw['cost']/total,6);o['purwk']=round(raw['pur']/nw,2)
            if name_key=='camp':o['nsets']=len(raw['_sets'])
            if name_key=='adset':
                fl=[]
                if o['purwk']<25:fl.append('<25/tydz')
                if o['nads']<4:fl.append('<4 kreacji')
                o['flag']=' · '.join(fl)
            out.append(o)
        return sorted(out,key=lambda x:-x['cost'])
    return {'craw':craw,'lut':lut,'month':month,'tm':tm,'lm':lm,'camp':rollup('camp'),'adset':rollup('adset')}

def build_brk(path,segcol):
    from collections import defaultdict
    rows=list(csv.DictReader(open(path)));daily=[]
    for r in rows:
        cost=num(col(r,'cost'));roas=num(col(r,'roas'))
        daily.append({'date':iso(col(r,'Date','date')),'seg':col(r,segcol,'segment'),
            'cost':round(cost,2),'impr':int(num(col(r,'impr'))),'reach':int(num(col(r,'reach'))),
            'clicks':int(num(col(r,'clicks'))),'pur':int(num(col(r,'pur'))),'val':round(cost*roas,2)})
    agg=defaultdict(lambda:{'cost':0,'impr':0,'reach':0,'clicks':0,'pur':0,'val':0})
    for d in daily:
        for k in ('cost','impr','reach','clicks','pur','val'):agg[d['seg']][k]+=d[k]
    roll=[]
    for seg,a in agg.items():
        cost=a['cost'];pur=a['pur'];val=a['val'];impr=a['impr']
        roll.append({'seg':seg,'reach':a['reach'],'impr':impr,'freq':None,'clicks':a['clicks'],'oc':None,
            'ctr':(a['clicks']/impr if impr else 0),'cpm':(cost/impr*1000 if impr else 0),'cost':round(cost,2),
            'lpv':None,'cv':None,'atc':None,'ic':None,'api':None,'pur':pur,'crpc':None,'crpa':None,'crpv':None,'crpl':None,
            'cpp':(cost/pur if pur else 0),'val':round(val,2),'roas':(val/cost if cost else 0),'aov':(val/pur if pur else 0)})
    roll.sort(key=lambda x:-x['cost'])
    return {'daily':daily,'roll':roll}

if __name__=='__main__':
    DATA={w:build_window(next(f for f in fs if os.path.exists(f))) for w,fs in WIN_FILES.items() if any(os.path.exists(f) for f in fs)}
    BRK={t:build_brk(f,sc) for t,(f,sc) in BRK_FILES.items() if os.path.exists(f)}
    open('/tmp/DATA.json','w').write(json.dumps(DATA,ensure_ascii=False,separators=(',',':')))
    open('/tmp/BRK.json','w').write(json.dumps(BRK,ensure_ascii=False,separators=(',',':')))
    for w in DATA:
        tc=sum(r['cost'] for r in DATA[w]['month']);tp=sum(r['pur'] for r in DATA[w]['month']);tv=sum(r['val'] for r in DATA[w]['month'])
        print(f"{w}: rows={len(DATA[w]['craw'])} cost={tc:.0f} pur={tp} roas={tv/tc:.2f}")
    print("DATA/BRK zapisane do /tmp/. Wstrzyknij w markery __INJECT_DATA__ / __INJECT_BRK__ skeletonu.")
