"""Add JFDA public prices and barcodes collected from the JFDA public drug search on 17 Nov 2026
(JFDA_audited_records.json from JFDA_Audited_Data_2026-11-17.zip; 18,154 records, 676 queries; completeness not verified by JFDA).
Usage: python3 scripts/import_jfda_2026_11_17.py /path/to/JFDA_audited_records.json
Matching is exact: normalised trade name + strength + pack + manufacturer, or, when that finds nothing, trade name + strength + pack,
and only when exactly one catalogue row fits. Only positive public prices (including tax) are used; listed zeros and missing prices are
ignored. Only barcodes whose check digit is valid are used; a barcode shared by several records maps to all the matched rows.
Run after import_drugcenter_prices_2026_11_15.py so the JFDA price is the one shown. Idempotent."""
import collections, hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]; SRC = pathlib.Path(sys.argv[1]); SID = 'jfda-search-2026-11-17'
SHA = hashlib.sha256(SRC.read_bytes()).hexdigest()
assert SHA == 'd1dd5b4a8fb3652bea1cab5c77fbfe0a144ac246c5255bb6aece6b2f4c75086f', 'Different audited file; review before import.'
data = json.loads(SRC.read_text()); recs = data['records']
cat = json.loads((ROOT/'catalogue.json').read_text())['records']
n = lambda s: re.sub(r'[^0-9a-z]', '', str(s or '').lower())
idx4, idx3 = collections.defaultdict(list), collections.defaultdict(list)
for r in cat:
    idx4[(n(r['brand']), n(r['strength']), n(r['pack']), n(r['manufacturer']))].append(r['id'])
    idx3[(n(r['brand']), n(r['strength']), n(r['pack']))].append(r['id'])
stat = collections.Counter(); hits = collections.defaultdict(list)
for j in recs:
    a = idx4.get((n(j['trade_name']), n(j['strength']), n(j['pack_details']), n(j['manufacturer'])), [])
    how = 'name+strength+pack+manufacturer'
    if len(a) != 1:
        b = idx3.get((n(j['trade_name']), n(j['strength']), n(j['pack_details'])), [])
        if len(a) == 0 and len(b) == 1: a, how = b, 'name+strength+pack'
        else: stat['not matched' if not a and not b else 'several catalogue rows fit'] += 1; continue
    stat['matched: ' + how] += 1; hits[a[0]].append(j)
COLLECTED = '2026-11-17'
entries, codes, conflicts = [], collections.defaultdict(set), []
for rid, js in hits.items():
    priced = [j for j in js if j['public_price_status'] == 'positive' and j['public_price_including_tax_jod']]
    fils = {round(j['public_price_including_tax_jod'] * 1000) for j in priced}
    if len(fils) > 1: conflicts.append(rid); stat['pack with conflicting JFDA prices (skipped)'] += 1
    elif fils:
        j = priced[0]; eff = j.get('price_effective_date_amman')
        e = dict(recordId=rid, fils=fils.pop(), sourceId=SID, sourceItem=j['jfda_internal_record_number'], sourceBrand=j['trade_name'])
        if eff and j.get('price_effective_date_status') == 'source_date_semantics_unverified' and eff[:10] <= COLLECTED: e['effectiveDate'] = eff[:10]
        entries.append(e)
    for j in js:
        bc = re.sub(r'\D', '', str(j.get('barcode') or ''))
        if j.get('barcode_check') == 'valid_check_digit_only' and 8 <= len(bc) <= 14:
            codes[bc.lstrip('0') if len(bc) == 14 and bc.startswith('0') else bc].add(rid)
prices = json.loads((ROOT/'prices.json').read_text())
prices['entries'] = [p for p in prices['entries'] if p['sourceId'] != SID] + sorted(entries, key=lambda e: e['recordId'])
prices['meta']['sources'] = [s for s in prices['meta']['sources'] if s['id'] != SID] + [dict(
    id=SID, labelAr='المؤسسة العامة للغذاء والدواء — بحث الأسعار العام، جُمع في 17 تشرين الثاني 2026', labelEn='JFDA public price search — collected 17 November 2026', period='2026-11', recent=True, official=True,
    dateBasis='Public price including tax shown by the JFDA public drug search, collected 17 November 2026 by 676 searches. Listed zero and missing prices are not used. The collection was not verified as the complete JFDA catalogue. Where JFDA gives a price-active date on or before the collection date it is kept as effectiveDate.',
    pageUrl='https://drugapplication.jfda.jo/PRep/publicDrugSearch', sha256=SHA, records=len(recs), matchedRows=len(hits), pricedRows=len(entries))]
prices['meta'].update(entryCount=len(prices['entries']), pricedRecords=len({p['recordId'] for p in prices['entries']}), latestPeriod='2026-11')
(ROOT/'prices.json').write_text(json.dumps(prices, ensure_ascii=False, separators=(',', ':')))
bcf = json.loads((ROOT/'barcodes.json').read_text())
for code, rid in bcf['meta'].get('jfda20261117', []):  # undo an earlier run
    ids = [i for i in bcf['codes'].get(code, []) if i != rid]
    if ids: bcf['codes'][code] = ids
    else: bcf['codes'].pop(code, None)
added = []
for code, ids in codes.items():
    have = set(bcf['codes'].get(code, []))
    for rid in sorted(ids - have): added.append([code, rid])
    bcf['codes'][code] = sorted(have | ids)
bcf['codes'] = dict(sorted(bcf['codes'].items()))
bcf['meta'].update(codes=len(bcf['codes']), records=len({i for v in bcf['codes'].values() for i in v}), jfda20261117=sorted(added),
    note='Barcodes from the December 2020 JFDA price workbook, one scanned by the site editor, and valid-check-digit barcodes from the JFDA public search collected 17 November 2026, for matched catalogue rows. A barcode linked to several rows lists them all.')
(ROOT/'barcodes.json').write_text(json.dumps(bcf, separators=(',', ':')))
(ROOT/'docs'/'JFDA_SEARCH_2026-11-17.json').write_text(json.dumps(dict(source=prices['meta']['sources'][-1], summary=dict(stat), conflicts=conflicts,
    matches=sorted([[rid, js[0]['jfda_internal_record_number']] for rid, js in hits.items()])), ensure_ascii=False, separators=(',', ':')))
print(json.dumps(dict(stat=dict(stat), priced=len(entries), barcodeCodes=bcf['meta']['codes'], barcodeRecords=bcf['meta']['records'], pricedRecords=prices['meta']['pricedRecords'])))
