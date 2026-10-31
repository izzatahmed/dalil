import pathlib,re,unicodedata,json,decimal,collections,hashlib,io
import openpyxl
import argparse
parser=argparse.ArgumentParser(description='Rebuild dated prices from the exact historical government workbook.');parser.add_argument('source_file');parser.add_argument('--retrieved-on',default='2026-10-31');args=parser.parse_args()
ROOT=pathlib.Path(__file__).resolve().parents[1];source=pathlib.Path(args.source_file)
def compact(v):
 s=unicodedata.normalize('NFKC',str(v or '')).lower().replace('µ','mc').replace('μ','mc')
 return re.sub(r'[^a-z0-9\u0621-\u064a.%/+]','',s)
def unit_form(form):
 f=str(form).lower()
 return 'tab' if 'tablet' in f or 'caplet' in f else 'cap' if 'capsule' in f else None
def pack_key(pack,form):
 s=compact(pack)
 for a,b in [('tablets','tab'),('tablet','tab'),('tabs','tab'),('capsules','cap'),('capsule','cap'),('caps','cap'),('vials','vial'),('ampoules','amp'),('ampoule','amp')]:s=s.replace(a,b)
 u=unit_form(form)
 m=re.fullmatch(r'(\d+)(tab|cap)?(?:/1box)?',s)
 if m and u and (not m[2] or m[2]==u):return m[1]+u
 return s
def strength_key(v,form):
 s=compact(v);u=unit_form(form)
 if u:s=re.sub(r'/1'+('(?:tabs?|tablets?)' if u=='tab' else '(?:caps?|capsules?)')+r'(?=[,+]|$)','',s)
 return s
def fils(v):
 if not isinstance(v,(float,int)) or v<=0:return None
 n=decimal.Decimal(str(v))*1000;q=n.to_integral_value(rounding=decimal.ROUND_HALF_UP)
 return int(q) if abs(n-q)<=decimal.Decimal('0.00001') else None
cat=json.loads((ROOT/'catalogue.json').read_text());records=cat['records'];workbook=openpyxl.load_workbook(io.BytesIO(source.read_bytes()),read_only=True,data_only=True);sheet=workbook.active
assert next(sheet.iter_rows(values_only=True))==('DRG_BARCODE','DRG_DESC_L','DRG_FILLING','DRG_CONCENTRATE','DRG_TAXED_JORD_CITIZEN_PRICE','DRG_TAXED_HOSP_PRICE','STORES_DESC_A','STORES_DESC_L'),'Unexpected workbook headers; review before import.'
raw=[]
for row,cells in enumerate(sheet.iter_rows(min_row=2,values_only=True),2):
 f=fils(cells[4])
 if f is not None:raw.append({'row':row,'barcode':str(cells[0] or ''),'brand':str(cells[1] or ''),'pack':str(cells[2] or ''),'strength':str(cells[3] or ''),'fils':f,'agent':str(cells[7] or '')})
# An exact brand+pack+concentration key is built in the target form context.
bybrand=collections.defaultdict(list)
for old in raw:bybrand[compact(old['brand'])].append(old)
candidates=[];conflicts=[];no_agent=0
for r in records:
 if not r['strength'] or not r['form']:continue
 options=[old for old in bybrand[compact(r['brand'])] if pack_key(old['pack'],r['form'])==pack_key(r['pack'],r['form']) and strength_key(old['strength'],r['form'])==strength_key(r['strength'],r['form'])]
 if not options:continue
 no_agent+=1
 options=[old for old in options if compact(old['agent'])==compact(r['agent'])]
 if not options:continue
 amounts=set(o['fils'] for o in options)
 if len(amounts)!=1:conflicts.append({'recordId':r['id'],'sourceRows':[o['row'] for o in options],'reason':'conflicting public prices'});continue
 candidates.append((r,options))
# Reject keys mapping to more than one current product identity, even with the same price.
index=collections.defaultdict(list)
for r,opts in candidates:
 for o in opts:index[o['row']].append(r['id'])
entries=[]
for r,options in candidates:
 if any(len(set(index[o['row']]))>1 for o in options):conflicts.append({'recordId':r['id'],'sourceRows':[o['row'] for o in options],'reason':'ambiguous current-product identity'});continue
 entries.append({'recordId':r['id'],'fils':options[0]['fils'],'sourceId':'jfda-2020-12','sourceRows':[o['row'] for o in options],'sourceBrand':options[0]['brand'],'sourcePack':options[0]['pack'],'sourceStrength':options[0]['strength'],'sourceAgent':options[0]['agent']})
meta={'currency':'JOD','displayCurrency':'JD','priceType':'tax-inclusive public/citizen pack price','historical':True,'importedOn':args.retrieved_on,'entryCount':len(entries),'sources':[{'id':'jfda-2020-12','labelAr':'ملف ديسمبر 2020','labelEn':'December 2020 file','period':'2020-12','dateBasis':'filename label; effective dates not independently verified','url':'https://opendata.gov.jo/dataset/MIGRATED-838-2021/resource/b3c4be77-c54b-40a3-b048-17f4a4cad431/download/12-drug2020-.xls?increment=true','pageUrl':'https://opendata.gov.jo/en/dataset/drug-prices-838-2021','sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'workbookCreated':workbook.properties.created.date().isoformat(),'workbookModified':workbook.properties.modified.date().isoformat(),'sheet':sheet.title,'sourceRows':sheet.max_row-1,'priceColumn':'DRG_TAXED_JORD_CITIZEN_PRICE','concentrationColumn':'DRG_CONCENTRATE','packColumn':'DRG_FILLING','agentColumn':'STORES_DESC_L'}]}
(ROOT/'prices.json').write_text(json.dumps({'meta':meta,'entries':entries},ensure_ascii=False,separators=(',',':')))
(ROOT/'docs/PRICE_IMPORT_AUDIT.json').write_text(json.dumps({'metadata':meta,'validPositivePublicPriceRows':len(raw),'targetCandidatesBeforeAgentCheck':no_agent,'acceptedRows':len(entries),'rejectedAmbiguousOrConflicting':conflicts,'method':'Exact conservative brand, pack, source concentration and English agent comparison. No fuzzy name matching. Missing or nonpositive prices excluded. Hospital price column not imported. Matches ambiguous across current product identities rejected.'},ensure_ascii=False,indent=2))
print(json.dumps({'sourceRows':sheet.max_row-1,'positivePublicPrices':len(raw),'beforeAgent':no_agent,'accepted':len(entries),'conflicts':len(conflicts)},indent=2))
