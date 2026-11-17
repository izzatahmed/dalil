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
# Strength text differs in style between the two (JFDA often adds the ingredient name: "Apixaban 5 MG" vs "5MG"), so a third
# pass compares the strength's numbers only, with the same trade name and pack, among rows not matched by the first two passes.
sn = lambda s: tuple(sorted(float(x) for x in re.findall(r'\d+(?:\.\d+)?', str(s or ''))))
idxN = collections.defaultdict(list)
for r in cat: idxN[(n(r['brand']), sn(r['strength']), n(r['pack']))].append(r['id'])
stat = collections.Counter(); hits = collections.defaultdict(list); later = []
for j in recs:
    a = idx4.get((n(j['trade_name']), n(j['strength']), n(j['pack_details']), n(j['manufacturer'])), [])
    how = 'name+strength+pack+manufacturer'
    if len(a) != 1:
        b = idx3.get((n(j['trade_name']), n(j['strength']), n(j['pack_details'])), [])
        if len(a) == 0 and len(b) == 1: a, how = b, 'name+strength+pack'
        elif not a and not b: later.append(j); continue
        else: stat['several catalogue rows fit'] += 1; continue
    stat['matched: ' + how] += 1; hits[a[0]].append(j)
for j in later:
    c = [i for i in idxN.get((n(j['trade_name']), sn(j['strength']), n(j['pack_details'])), []) if i not in hits]
    if len(c) == 1 and sn(j['strength']): stat['matched: name+strength numbers+pack'] += 1; hits[c[0]].append(j)
    else: stat['not matched' if not c else 'several catalogue rows fit'] += 1
# New catalogue rows: JFDA records with a positive public price that match no catalogue row and do not duplicate one
# (same trade name, strength numbers and pack numbers), and that carry an ATC code or listed ingredients.
pn = lambda s: tuple(sorted(float(x) for x in re.findall(r'\d+(?:\.\d+)?', str(s or ''))))
byBrand = collections.defaultdict(list)
for r in cat: byBrand[n(r['brand'])].append(r)
agentMap, countryOK = collections.defaultdict(collections.Counter), {r['country'] for r in cat}
C = {r['id']: r for r in cat}
for rid, js in hits.items():
    for j in js: agentMap[(j['agent'] or '').strip()][C[rid]['agent']] += 1
FORMS = [('Eye drops', 'eye|ophth'), ('Ear drops', '\\bear\\b|otic'), ('Nasal spray', 'nasal'), ('Inhalation powder', 'inhal|dispens|\\bcnt\\b|diskus|rotacap'), ('Prolonged release tablet', '\\b(xr|sr|pr|er|cr|mr|xl)\\b.*\\btab|prolonged|extended release.*tab|modified release'), ('Film-coated tablet', 'film[- ]?coated|f\\.?c\\.?\\s*tab'), ('Orodispersible tablet', 'orodispersible|oral dispersible|odt\\b'), ('Effervescent tablet', 'efferves'), ('Chewable tablet', 'chewable'), ('Tablet', '\\btab|tablet|caplet'), ('Capsules', '\\bcap|capsul|softgel'), ('Solution for injection in pre-filled syringe', 'pre-?filled syringe|\\bpfs\\b'), ('Solution for injection in pre-filled pen', 'pre-?filled pen|\\bpfp\\b|\\bpen\\b'), ('Powder for solution for injection', 'powder for (solution|concentrate).*inj|lyophili'), ('Solution for injection', 'inject|\\bamp|ampoule|\\bvial|\\bvil\\b|infusion|\\bi\\.?v\\b'), ('Cream', 'cream'), ('Ointment', 'ointment|\\boint\\b'), ('Gel', '\\bgel\\b'), ('Suppository', 'suppos'), ('Vaginal tablet', 'vaginal'), ('Oral suspension', 'suspension|\\bsusp\\b'), ('Syrup', 'syrup'), ('Oral drops', '\\bdrops\\b'), ('Sachet', 'sachet|\\bsac\\b|granule'), ('Cutaneous solution', 'topical|scalp|cutaneous'), ('Medicated chewing gum', '\\bgum\\b'), ('Oral solution', 'oral solution'), ('Solution', 'solution|\\bml\\b')]
def form_of(j):
    t = ' '.join(str(j.get(k) or '') for k in ('trade_name', 'pack_details', 'strength')).lower()
    return next((f for f, rx in FORMS if re.search(rx, t)), '')
matchedIds = {j['jfda_internal_record_number'] for js in hits.values() for j in js}
additions = []; seenNew = set()
for j in recs:
    if j['jfda_internal_record_number'] in matchedIds or j['public_price_status'] != 'positive' or not j['public_price_including_tax_jod']: continue
    if not ((j.get('atc_code') and j['atc_code'] != 'N/A') or j.get('ingredients')): continue
    if any(pn(c['strength']) == pn(j['strength']) and pn(c['pack']) == pn(j['pack_details']) for c in byBrand.get(n(j['trade_name']), [])): stat['new: skipped as likely duplicate of a catalogue row'] += 1; continue
    dkey = (n(j['trade_name']), n(j['strength']), n(j['pack_details']), round(j['public_price_including_tax_jod'] * 1000))
    if dkey in seenNew: stat['new: duplicate JFDA record skipped'] += 1; continue
    seenNew.add(dkey)
    ag = (j['agent'] or '').strip(); agent = agentMap[ag].most_common(1)[0][0] if agentMap.get(ag) else ag
    additions.append(dict(brand=(j['trade_name'] or '').strip(), pack=(j['pack_details'] or '').strip(), form=form_of(j), strength=(j['strength'] or '').strip(), agent=agent,
        scientific=(j['ingredients'] or '').strip(), manufacturer=(j['manufacturer'] or '').strip(), country=(j['manufacturer_country'] or '').strip(),
        marketing=(j.get('marketing_authorisation_holder') or j['manufacturer'] or '').strip(), marketingCountry=(j.get('marketing_holder_country') or j['manufacturer_country'] or '').strip(),
        id='jfda-' + str(j['jfda_internal_record_number']), row=None, rawStrength=(j['strength'] or '').strip(), strengthFormat='General', atc=j.get('atc_code'),
        jfdaRecord=str(j['jfda_internal_record_number']), addedFrom=SID))
    hits[additions[-1]['id']].append(j)
additions.sort(key=lambda r: (r['brand'].lower(), r['id']))
stat['new catalogue rows added'] = len(additions)
(ROOT/'catalogue_additions.json').write_text(json.dumps(dict(meta=dict(source=SID, title='Products found in the JFDA public price search (17 Nov 2026) that are not in the June 2026 JFDA workbook',
    sourceSha256=SHA, baseCatalogueSha256=json.loads((ROOT/'catalogue.json').read_text())['meta']['sha256'], recordCount=len(additions),
    note='Each has a positive JFDA public price. The dosage form is inferred from the name and pack text (blank when unclear); the agent is shown in English where the same agent appears in the workbook.'),
    records=additions), ensure_ascii=False, separators=(',', ':')))
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
LEAF = {}
for rid, js in hits.items():
    files = sorted({f for j in js for f in (j.get('leaflet_file_names') or []) if re.fullmatch(r'[A-Za-z0-9_\-]+\.pdf', f)})
    if files: LEAF[rid] = files
(ROOT/'leaflets.json').write_text(json.dumps(dict(meta=dict(source=SID, base='https://drugapplication.jfda.jo/PRep/DisplayF?fil=', records=len(LEAF),
    note='JFDA-approved leaflet PDFs named in the JFDA public search for matched catalogue rows and additions (17 November 2026). Link pattern confirmed by the site editor with Empaxa (4257495.pdf).'),
    records=dict(sorted(LEAF.items()))), separators=(',', ':')))
stat['rows with a leaflet PDF'] = len(LEAF)
(ROOT/'docs'/'JFDA_SEARCH_2026-11-17.json').write_text(json.dumps(dict(source=prices['meta']['sources'][-1], summary=dict(stat), conflicts=conflicts,
    matches=sorted([[rid, js[0]['jfda_internal_record_number']] for rid, js in hits.items() if not rid.startswith('jfda-')])), ensure_ascii=False, separators=(',', ':')))
print(json.dumps(dict(stat=dict(stat), priced=len(entries), barcodeCodes=bcf['meta']['codes'], barcodeRecords=bcf['meta']['records'], pricedRecords=prices['meta']['pricedRecords'])))
