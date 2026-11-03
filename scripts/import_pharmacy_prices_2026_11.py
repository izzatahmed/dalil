"""Add public prices looked up on 3 Nov 2026 on the Drug Center pharmacy website (drugcenterjo.net) by the site editor,
recorded in Top50_prices_to_filled.xlsx. Each list row was matched to one catalogue pack by hand (MAP below).
Run after import_reduced_prices_2023.py. Usage: python3 scripts/import_pharmacy_prices_2026_11.py /path/to/Top50_prices_to_filled.xlsx"""
import json, pathlib, sys, hashlib
from openpyxl import load_workbook
ROOT = pathlib.Path(__file__).resolve().parents[1]; SRC = pathlib.Path(sys.argv[1]); SID = 'drugcenter-2026-11-03'
# list row number (or 'exforge' for the added last row) -> catalogue record id
MAP = {1: '0ac410c0114aea625e-1', 2: '732ed37228fde84580-1', 3: 'c2749618ff7372b71b-1', 4: '0b0446e37eb8dbf315-1', 5: '0feec8cccd15264577-1',
       6: 'b240cb2d9d9cc6f12f-1', 7: '1258b07bbe08e9bee6-1', 8: 'fc0de2aeb9c6d3e1d8-1', 9: '46721bf13f4ec64bfb-1', 10: 'baf8aaa8cc02080c83-1',
       11: '66d6622071c789c726-1', 12: 'a954e25afc64d3d1d5-1', 13: '435b27916a66740523-1', 21: '2244388d1b16b52c24-1', 22: 'c97cee92368c10a150-1',
       23: 'abd67260da5d4d7eb3-1', 24: '6b1a8cbb41c5528fdd-1', 25: '07760fa7135f4edfb2-1', 26: '2595cc1b932de8c9ea-1', 27: '85e967ebadf7912a55-1',
       30: '1e4190c5422c0d2344-1', 32: 'f5db631f0a1ff2fe75-1', 37: '6f7d4980353933a420-1', 38: 'e370839c0710903e61-1', 40: '6cd387de0e14aa52ea-1',
       41: 'f590bc5b5dc3f643ab-1', 42: '79391123777fac2fba-1', 44: 'f0a0f2ffa80ca3f643-1', 48: 'c05bd07ceb3da62673-1', 49: 'a5408c8b37397dc259-1',
       50: '3148c92cf5d6d9e697-1', 'exforge': '58bcb3796466417b6f-1'}
BARCODES = {'6251605002546': 11}  # scanned barcode -> list row (Ozempic 0.25 mg); row 10's barcode awaits confirmation of strength
ws = load_workbook(SRC, data_only=True).active
rows = {}
for r in ws.iter_rows(min_row=4, values_only=True):
    n, g, b, s, pack, price = r[:6]
    if price in (None, ''): continue
    key = n if n is not None else ('exforge' if str(b).lower().startswith('exforge') else None)
    rows[key] = dict(item=key, brand=b, strength=s, pack=str(pack or '').strip(), price=float(price))
assert set(rows) == set(MAP), sorted(set(rows) ^ set(MAP), key=str)
cat = {r['id']: r for r in json.loads((ROOT/'catalogue.json').read_text())['records']}
prices = json.loads((ROOT/'prices.json').read_text())
prices['entries'] = [p for p in prices['entries'] if p['sourceId'] != SID] + [
    dict(recordId=MAP[k], fils=round(v['price'] * 1000), sourceId=SID, sourceBrand=f"{v['brand']} {v['strength']}", sourcePack=v['pack'])
    for k, v in sorted(rows.items(), key=lambda kv: str(kv[0]).zfill(3)) if MAP[k] in cat]
prices['meta']['sources'] = [s for s in prices['meta']['sources'] if s['id'] != SID] + [dict(
    id=SID, labelAr='موقع صيدلية دراغ سنتر — تاريخ الاطلاع 3 تشرين الثاني 2026', labelEn='Drug Center pharmacy website — checked 3 November 2026', period='2026-11', recent=True,
    dateBasis='Public price shown on drugcenterjo.net, looked up by the site editor on 3 November 2026 and matched to the pack by hand.', pageUrl='https://drugcenterjo.net/',
    sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(), items=len(rows))]
prices['meta'].update(entryCount=len(prices['entries']), pricedRecords=len({p['recordId'] for p in prices['entries']}), latestPeriod='2026-11')
(ROOT/'prices.json').write_text(json.dumps(prices, ensure_ascii=False, separators=(',', ':')))
bc = json.loads((ROOT/'barcodes.json').read_text())
for code, item in BARCODES.items(): bc['codes'][code] = sorted(set(bc['codes'].get(code, [])) | {MAP[item]})
bc['meta'].update(codes=len(bc['codes']), records=len({i for v in bc['codes'].values() for i in v}), manual=dict(source=SID, codes=len(BARCODES)))
(ROOT/'barcodes.json').write_text(json.dumps(bc, separators=(',', ':')))
(ROOT/'docs'/'PRICE_CHECK_2026-11-03.json').write_text(json.dumps(dict(source=prices['meta']['sources'][-1], items=[dict(v, recordId=MAP[k], catalogueBrand=cat[MAP[k]]['brand'], cataloguePack=cat[MAP[k]]['pack']) for k, v in rows.items()]), ensure_ascii=False, indent=1))
print(json.dumps(dict(prices=len(rows), pricedRecords=prices['meta']['pricedRecords'], barcodes=bc['meta']['codes'])))
