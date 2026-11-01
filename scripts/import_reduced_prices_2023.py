"""Add JFDA "قائمة الأدوية المخفضة" (reduced-price list, PDF dated 25 July 2023) to prices.json.
Run after import_historical_prices.py. Usage: python3 scripts/import_reduced_prices_2023.py /path/to/list.pdf
Each list item is matched to catalogue rows by brand, every number in its name (strength), pack count and form.
Only a single, unambiguous match is used; MANUAL lists items resolved by hand. Unmatched items are kept in
docs/PRICE_LIST_2023-07.json with status "unmatched". 2020 entries are kept; the 2023 entry follows them and is shown."""
import collections, hashlib, json, pathlib, re, sys
import pdfplumber
ROOT = pathlib.Path(__file__).resolve().parents[1]; PDF = pathlib.Path(sys.argv[1])
SID = 'jfda-2023-07-reduced'
SHA = hashlib.sha256(PDF.read_bytes()).hexdigest()
assert SHA == '7a5c3e90d8f1aa89caef9095b091b5175d992ab441d0b9330c65fd7d964f33f9', 'Different PDF; review before import.'
# 1. extract: table rows grouped by blank separator rows; each item has one number and one price row
rows = []
with pdfplumber.open(PDF) as pdf:
    for i, p in enumerate(pdf.pages):
        for t in p.extract_tables():
            rows += [[i + 1] + [(c or '').replace('\n', ' ').strip() for c in r] for r in t]
groups, cur = [], []
for r in rows:
    if not any(r[1:]):
        if cur: groups.append(cur); cur = []
    else: cur.append(r)
if cur: groups.append(cur)
items = []
for g in groups:
    num = [r[1] for r in g if re.fullmatch(r'\d+', r[1])]; pr = [r for r in g if re.search(r'\d', r[11]) and re.search(r'\d', r[14])]
    if len(num) == 1 and len(pr) == 1:
        p = pr[0]; items.append(dict(n=int(num[0]), name=' '.join(r[5] for r in g if r[5]).strip(), pack=p[8], old=p[11], new=p[14], pct=p[17], page=g[0][0]))
# two items share one separator group on the last page (verified against the PDF)
items += [dict(n=370, name='Zoledronic Acid Hikma 4mg Lyophilized Powder for Solution for I.V Infusion', pack='1 vial', old='160.56', new='143.45', pct='11%', page=18),
          dict(n=371, name='Zonic 4mg/5ml Solution for I.V Infusion', pack='1 vial', old='162.13', new='143.45', pct='12%', page=18)]
items.sort(key=lambda x: x['n']); assert [i['n'] for i in items] == list(range(1, 375)), 'Expected items 1-374'
for i in items:
    i['oldFils'] = round(float(i.pop('old').replace(',', '')) * 1000); i['fils'] = round(float(i.pop('new').replace(',', '')) * 1000)
    assert abs(round(100 * (1 - i['fils'] / i['oldFils'])) - int(i['pct'].rstrip('%'))) <= 1, i
# 2. match
cat = json.loads((ROOT/'catalogue.json').read_text()); prices = json.loads((ROOT/'prices.json').read_text())
assert cat['meta']['sha256'] == prices['meta'].get('catalogueSha256', cat['meta']['sha256'])
byid = {r['id']: r for r in cat['records']}
old2020 = {p['recordId']: p['fils'] for p in prices['entries'] if p['sourceId'] == 'jfda-2020-12'}
def words(s): return re.findall(r'[a-z]+', str(s or '').lower())
def nums(s): return {float(x.replace(',', '')) for x in re.findall(r'\d+(?:[.,]\d+)?', str(s or ''))}
def packn(s): return [int(x) for x in re.findall(r'\d+', str(s or ''))]
FORMW = {'tab': 'tab', 'tabs': 'tab', 'tablet': 'tab', 'tablets': 'tab', 'fc': 'tab', 'caplet': 'tab', 'cap': 'cap', 'caps': 'cap', 'capsule': 'cap', 'capsules': 'cap',
         'vial': 'inj', 'vials': 'inj', 'inj': 'inj', 'injection': 'inj', 'pfs': 'inj', 'pfp': 'inj', 'pen': 'inj', 'amp': 'inj', 'ampoule': 'inj', 'infusion': 'inj',
         'syrup': 'liq', 'susp': 'liq', 'suspension': 'liq', 'solution': 'liq', 'drops': 'drop', 'spray': 'spray', 'cream': 'top', 'gel': 'top', 'ointment': 'top',
         'supp': 'supp', 'suppository': 'supp', 'sachet': 'sach', 'sachets': 'sach', 'granules': 'sach', 'inhaler': 'inh', 'e': 'drop'}
def fk(s): return {FORMW[w] for w in words(s) if w in FORMW}
SPEC = ['gel', 'cream', 'ointment', 'pfp', 'pfs', 'xl', 'xr', 'plus', 'kids', 'pediatric', 'forte', 'susp', 'syrup', 'e/d']
def spec(s): return {w for w in SPEC if re.search(r'\b' + re.escape(w) + r'\b', s.lower())}
def first(s): p = packn(s); return p[0] if p else None
by1 = collections.defaultdict(list)
for r in cat['records']:
    w = words(r['brand'])
    if w: by1[w[0]].append(r)
MANUAL = {42: 'de0f026fb3365e71bd-1', 94: 'bea8b71a681170e593-1', 108: '71bf24d8284aaefdfd-1', 117: 'd6042a2b4a1a01b7ec-1', 119: '621e06c522ee9106e1-1',
          128: '3125bf5bdf35c9bb55-1', 147: '529c1936a5cf771254-1', 157: 'd7702be31fec8dac10-1', 213: 'a0fdbb676367a63fa9-1', 227: 'efc9baae6f60bab496-1',
          350: '514ecf387df41b856e-1', 369: 'b9a1399544475170e5-1', 370: 'a8229b2a7c7ed1d4b6-1', 20: '0befb84754bf401061-1', 294: '1c726205043fc83bb5-1'}
SKIP = {21}  # duplicate line of item 20 (same product, same prices)
def match(it):
    w = words(it['name']); c = by1.get(w[0], [])
    if len(w) > 1 and w[1] not in FORMW and not w[1].startswith(('mg', 'mcg', 'ml')):
        c = [r for r in c if w[1] in words(r['brand'] + ' ' + (r['scientific'] or ''))] or c
    n = nums(it['name']) - {0.0}
    if n: c = [r for r in c if n <= (nums(r['brand']) | nums(r['strength']) | nums(r.get('rawStrength')) | nums(r['scientific']))]
    pk = packn(it['pack']); c3 = [r for r in c if pk and set(pk) <= set(packn(r['pack']))]; c = c3 or c
    f = fk(it['name'] + ' ' + it['pack']); c = [r for r in c if f & fk(r['form'] + ' ' + r['brand'] + ' ' + r['pack'])] or c
    if len(c) > 1: c = [r for r in c if first(r['pack']) == first(it['pack'])] or c
    if len(c) > 1: sp = spec(it['name'] + ' ' + it['pack']); c = [r for r in c if spec(r['brand'] + ' ' + r['pack'] + ' ' + r['form']) == sp] or c
    if len(c) != 1: return None, 'ambiguous' if c else 'not found'
    r = c[0]; ratio = r['id'] in old2020 and it['oldFils'] / old2020[r['id']]
    return (r['id'], 'matched') if c3 or (ratio and 0.65 < ratio < 1.5) else (None, 'pack not confirmed')
used = {}
for it in items:
    if it['n'] in SKIP: it.update(status='duplicate of item 20'); continue
    rid, st = (MANUAL[it['n']], 'matched (reviewed)') if it['n'] in MANUAL else match(it)
    if rid and rid in used: st, rid = 'conflict', None
    it.update(status=st if rid else 'unmatched: ' + st, recordId=rid)
    if rid: used[rid] = it['n']; it.update(brand=byid[rid]['brand'], catalogPack=byid[rid]['pack'])
# 3. write
prices['entries'] = [p for p in prices['entries'] if p['sourceId'] != SID] + [
    dict(recordId=i['recordId'], fils=i['fils'], sourceId=SID, previousFils=i['oldFils'], sourceItem=i['n'], sourceBrand=i['name'], sourcePack=i['pack'])
    for i in items if i.get('recordId')]
prices['meta']['sources'] = [s for s in prices['meta']['sources'] if s['id'] != SID] + [dict(
    id=SID, labelAr='قائمة الأدوية المخفضة – تموز 2023', labelEn='JFDA reduced-price list, July 2023', period='2023-07',
    dateBasis='PDF document date 25 July 2023 (file metadata); "current price including tax" column. Effective dates not independently verified.',
    pageUrl='https://www.jfda.jo/', sha256=SHA, items=len(items), matchedItems=len(used), priceColumn='السعر الحالي مع الضريبة', previousPriceColumn='السعر السابق مع الضريبة')]
prices['meta'].update(entryCount=len(prices['entries']), pricedRecords=len({p['recordId'] for p in prices['entries']}), latestPeriod='2023-07', catalogueSha256=cat['meta']['sha256'])
(ROOT/'prices.json').write_text(json.dumps(prices, ensure_ascii=False, separators=(',', ':')))
(ROOT/'docs'/'PRICE_LIST_2023-07.json').write_text(json.dumps(dict(source=prices['meta']['sources'][-1], items=items), ensure_ascii=False, indent=1))
st = collections.Counter(i['status'].split(':')[0] for i in items)
print(json.dumps(dict(items=len(items), matched=len(used), status=st, newRecords=sum(1 for r in used if r not in old2020), pricedRecords=prices['meta']['pricedRecords']), ensure_ascii=False))
