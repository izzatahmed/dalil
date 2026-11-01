"""Build barcodes.json: GTIN barcodes for catalogue rows, taken from the JFDA December 2020 price workbook
(column DRG_BARCODE) for the rows already matched to the catalogue by import_historical_prices.py (prices.json sourceRows).
Usage: python3 scripts/build_barcodes.py /path/to/12-drug2020-.xls"""
import collections, hashlib, io, json, pathlib, re, sys
import openpyxl
ROOT = pathlib.Path(__file__).resolve().parents[1]; SRC = pathlib.Path(sys.argv[1])
SHA = hashlib.sha256(SRC.read_bytes()).hexdigest()
prices = json.loads((ROOT/'prices.json').read_text()); cat = json.loads((ROOT/'catalogue.json').read_text())
src = next(s for s in prices['meta']['sources'] if s['id'] == 'jfda-2020-12'); assert SHA == src['sha256'], 'Different workbook; review first.'
sheet = openpyxl.load_workbook(io.BytesIO(SRC.read_bytes()), read_only=True, data_only=True).active
rows = list(sheet.iter_rows(values_only=True)); assert rows[0][0] == 'DRG_BARCODE'
def gtin(v):
    s = re.sub(r'\D', '', str(v or '').split('.')[0] if isinstance(v, float) else str(v or ''))
    if len(s) not in (8, 12, 13, 14): return None
    s = s.lstrip('0') if len(s) == 14 and s.startswith('0') else s
    return s if len(s) >= 8 else None
ids = {r['id'] for r in cat['records']}
codes = collections.defaultdict(set)
for e in prices['entries']:
    if e['sourceId'] != 'jfda-2020-12' or e['recordId'] not in ids: continue
    for row in e['sourceRows']:
        c = gtin(rows[row - 1][0])
        if c: codes[c].add(e['recordId'])
out = dict(meta=dict(source=src['labelEn'], sourceSha256=SHA, catalogueSha256=cat['meta']['sha256'], column='DRG_BARCODE', codes=len(codes), records=len({i for v in codes.values() for i in v}),
    note='Barcodes from the December 2020 JFDA price workbook for matched packs. A pack may have more than one barcode; a barcode linked to several rows lists them all.'),
    codes={k: sorted(v) for k, v in sorted(codes.items())})
(ROOT/'barcodes.json').write_text(json.dumps(out, separators=(',', ':')))
print(json.dumps(out['meta']))
