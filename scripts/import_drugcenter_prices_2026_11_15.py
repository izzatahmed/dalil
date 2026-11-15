"""Add Drug Center pharmacy website listed prices (export dated 15 Nov 2026, 3,390 products) to prices.json.
Run after import_pharmacy_prices_2026_11.py. Usage: python3 scripts/import_drugcenter_prices_2026_11_15.py /path/to/DrugCenter_Drug_Prices_2026-11-15.csv
A product is matched to a catalogue pack only when one pack fits its brand, every strength number in its name, its pack count
(or volume) and its form. Products whose brand is not a registered medicine in the catalogue (cosmetics, devices, supplements)
match nothing and are ignored. A match is held back for review when the price differs from the pack's earlier price by more than
3 times, when the pack size could not be confirmed and the price is not within 25 percent of the earlier price, or when two different
products fall on one pack. Every product's outcome is written to docs/PRICES_DRUGCENTER_2026-11-15.json."""
import csv, json, re, html, collections, sys, hashlib, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; SRC = pathlib.Path(sys.argv[1]); SID = 'drugcenter-2026-11-15'
SHA = hashlib.sha256(SRC.read_bytes()).hexdigest()
assert SHA == '60879c1cbb5577446a9a982f7bb6fb9b58091c736d7b63f27c0012053aad4891', 'Different export; review before import.'
rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
cat = json.loads((ROOT/'catalogue.json').read_text())['records']
prices = json.loads((ROOT/'prices.json').read_text())
prev = {}
for e in prices['entries']:
    if e['sourceId'] != SID: prev[e['recordId']] = e
def clean(n):
    n=html.unescape(n); n=re.sub(r'^\s*N\.\d\.A\s*\d{1,2}/\d{1,2}/\d{4}\s*','',n); return re.sub(r'\s+',' ',n).strip()
def words(s): return re.findall(r'[a-z]+',str(s or '').lower())
def nums(s): return {float(x) for x in re.findall(r'\d+(?:\.\d+)?',str(s or '').replace(',','.'))}
UNIT=r'(?:tab|tabs|tablet|tablets|cap|caps|capsule|capsules|sach|sachet|sachets|amp|amps|ampoule|vial|vials|supp|pcs|doses|dose|ovules|pen|pens|pfs|syringe|syringes|patch|patches|lozenges|bags|bag|sheets)'
def packcount(n):
    m=re.findall(r'(\d+)\s*(?:v/)?\s*'+UNIT+r'\b',n.lower()); return {int(x) for x in m}
def vol(n):
    return {float(x) for x in re.findall(r'(\d+(?:\.\d+)?)\s*(?:ml|g|gm)\b',n.lower())}
FK={'tab':'tab','tabs':'tab','tablet':'tab','tablets':'tab','caplet':'tab','fc':'tab','cap':'cap','caps':'cap','capsule':'cap','capsules':'cap','sach':'sach','sachet':'sach','sachets':'sach','granules':'sach','powder':'sach',
'amp':'inj','ampoule':'inj','vial':'inj','vials':'inj','inj':'inj','injection':'inj','pen':'inj','pfs':'inj','syringe':'inj','infusion':'inj','syrup':'liq','susp':'liq','suspension':'liq','solution':'liq','drops':'drop','e':'drop','d':'drop','cream':'top','gel':'top','ointment':'top','lotion':'top','oint':'top','supp':'supp','suppositories':'supp','ovules':'supp','spray':'spray','inhaler':'inh','diskus':'inh','evohaler':'inh','turbuhaler':'inh','patch':'patch'}
def fk(s): return {FK[w] for w in words(s) if w in FK}
by1=collections.defaultdict(list)
for r in cat:
    w=words(r['brand'])
    if w: by1[w[0]].append(r)
res=collections.Counter();out=[];review=[];status={}
for p in rows:
    name=clean(p['product_name']); w=words(name)
    if not w: res['noname']+=1; status[p['product_id']]='no name'; continue
    c=by1.get(w[0],[])
    if not c: res['brand not in catalogue']+=1; status[p['product_id']]='brand not in catalogue'; continue
    if len(w)>1 and w[1] not in FK and not re.match(r'^(mg|mcg|ml|g|iu|plus)$',w[1]):
        c2=[r for r in c if w[1] in words(r['brand'])]
        if c2: c=c2
    pk=packcount(name); vl=vol(name)
    n=nums(name)-{float(x) for x in pk}-vl-{0.0}
    if n: c=[r for r in c if n<=(nums(r['brand'])|nums(r['strength'])|nums(r.get('rawStrength'))|nums(r['scientific'])|nums(r['pack']))]
    if not c: res['strength mismatch']+=1; status[p['product_id']]='strength mismatch'; continue
    if pk:
        c3=[r for r in c if pk & {int(x) for x in nums(r['pack'])}]
        if not c3: res['pack not in catalogue']+=1; status[p['product_id']]='pack not in catalogue'; continue
        c=c3
    elif vl:
        c3=[r for r in c if vl & (nums(r['pack'])|nums(r['brand'])|nums(r['strength']))]
        if not c3: res['volume not in catalogue']+=1; status[p['product_id']]='volume not in catalogue'; continue
        c=c3
    f=fk(name)
    c4=[r for r in c if f & fk(r['form']+' '+r['brand']+' '+r['pack'])]
    if f and not c4 and all(fk(r['form']+' '+r['brand']+' '+r['pack']) for r in c): res['form mismatch']+=1; status[p['product_id']]='form mismatch'; continue
    if c4: c=c4
    if len(c)!=1:
        # identical strength+pack duplicates? keep ambiguous
        res['ambiguous']+=1; status[p['product_id']]='ambiguous'; continue
    r=c[0]; price=round(float(p['listed_price_jod'])*1000)
    old=prev.get(r['id']); ratio=old and price/old['fils']
    item=dict(product_id=p['product_id'],sku=p['product_code_sku'],name=name,fils=price,url=p['product_url'],recordId=r['id'],brand=r['brand'],pack=r['pack'],prev=old and old['fils'],prevSource=old and old['sourceId'],ratio=ratio,packConfirmed=bool(pk or vl))
    if ratio and not (0.3<=ratio<=3): item['status']='review: price differs >3x from earlier price'; review.append(item); res['price outlier vs previous']+=1; continue
    if not (pk or vl) and not (ratio and 0.75<=ratio<=1.33): item['status']='review: pack size not confirmed'; res['matched but pack unconfirmed']+=1; review.append(item); continue
    out.append(item); res['matched']+=1
norm = lambda n: re.sub(r'\bdiscont\w*\b', '', n.lower()).replace(' ', '')
grp = collections.defaultdict(list)
for i in out: grp[i['recordId']].append(i)
keep = []
for k, v in grp.items():
    names = {norm(x['name']) for x in v}
    if len({x['fils'] for x in v}) == 1 and (len(names) == 1 or (len(names) <= 2 and v[0]['packConfirmed'])): keep.append(v[0])
    else:
        for x in v: x['status'] = 'review: different products on one pack'; review.append(x)
        res['conflicting products for one pack'] += len(v); res['matched'] -= len(v)
out = keep
for i in out: i['status'] = 'matched'
prices['entries'] = [p for p in prices['entries'] if p['sourceId'] != SID] + [dict(recordId=i['recordId'], fils=i['fils'], sourceId=SID, sourceItem=i['product_id'], sourceBrand=i['name'], sourceUrl=i['url']) for i in sorted(out, key=lambda i: i['recordId'])]
prices['meta']['sources'] = [s for s in prices['meta']['sources'] if s['id'] != SID] + [dict(id=SID, labelAr='موقع صيدلية دراغ سنتر — قائمة 15 تشرين الثاني 2026', labelEn='Drug Center pharmacy website — list of 15 November 2026', period='2026-11', recent=True,
    dateBasis='Listed retail price on drugcenterjo.net, exported 15 November 2026 (retrieved_at_utc). The export states: retailer website listed price; not independently verified official JFDA price.', pageUrl='https://drugcenterjo.net/', sha256=SHA, items=len(rows), matchedItems=len(out))]
prices['meta'].update(entryCount=len(prices['entries']), pricedRecords=len({p['recordId'] for p in prices['entries']}), latestPeriod='2026-11')
(ROOT/'prices.json').write_text(json.dumps(prices, ensure_ascii=False, separators=(',', ':')))
byid = {**{i['product_id']: i for i in review}, **{i['product_id']: i for i in out}}
docs = [dict(product_id=p['product_id'], name=clean(p['product_name']), fils=round(float(p['listed_price_jod']) * 1000),
    **({k: byid[p['product_id']][k] for k in ('status', 'recordId', 'brand', 'pack', 'prev', 'prevSource')} if p['product_id'] in byid else dict(status=status.get(p['product_id'], 'not matched')))) for p in rows]
(ROOT/'docs'/'PRICES_DRUGCENTER_2026-11-15.json').write_text(json.dumps(dict(source=prices['meta']['sources'][-1], summary=dict(res), products=docs), ensure_ascii=False, separators=(',', ':')))
print(json.dumps(dict(res=dict(res), matched=len(out), newlyPriced=sum(1 for i in out if not i['prev']), pricedRecords=prices['meta']['pricedRecords'])))
