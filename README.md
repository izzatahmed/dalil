# دليل الادوية الاردني
# The Jordanian Drugs Directory

Version **0.6.0**, 1 November 2026. A mobile-first Arabic/English static directory for GitHub Pages. It is an independent directory using JFDA source data.

## Upload the update

Extract the modified-files ZIP and upload **all its contents** into the existing `dalil` publishing directory, replacing matching files. **Include the new `search.js`.** Keep the existing `catalogue.json`, `prices.json`, manifests and icons alongside `index.html`. The complete ZIP includes the full website and preserves pre-existing repository files.

No build, account, API key or server is required. Keep the files at the ZIP root rather than creating a second nested `dalil` folder. GitHub Pages should publish the same directory as before. The versioned service worker refreshes the app assets; reload after deployment if an older version remains visible.

## What changed in v0.6

- Exact Arabic/English names and the direct text-size, night and E/ع controls are retained.
- The home page stays search-only. The 10,628 original source rows remain searchable.
- Brand and ingredient suggestions appear while typing. Conservative spelling suggestions require user selection and retain numeric strength tokens. Suggestions are navigation aids, not replacements for an entered medicine.
- Arabic search aliases cover common ingredient and brand spellings. Official product names retain the source language. Aliases do not establish approved Arabic names, indications or clinical equivalence.
- Concentration queries match complete numeric tokens: `10` does not match `100`. Existing form, country, concentration, pack and historical-price filters are retained. Active filters appear as removable chips; Clear all removes filters while preserving the query.
- The result action opens **Lower-priced options**. Choose a reference pack; matching pack sizes appear first. Other readable tablet/capsule pack sizes show explicit per-unit prices. A lower unit price can accompany a larger pack with a higher total pack price.
- Historical and entered-price comparisons use readable cards. Different source fields are highlighted. Ranking remains conditional on valid, compatible data.
- Medicine and exact-pack links use URL hashes, so GitHub Pages does not need server routing. Copy link includes language and search filters. Direct links, reload, browser back and Back to results are supported. Returning restores the query, filter state, result limit and scroll position.

## Historical prices and limits

**5,046 catalogue packs have a matched historical tax-inclusive public/citizen price in JD (ISO JOD).** `prices.json` and `catalogue.json` are byte-for-byte unchanged from v0.5.

The price source is the official government resource labelled `12-Drug2020`, interpreted as a December 2020 filename label. Workbook creation is 23 September 2020; last save is 19 April 2021. Individual price effective dates are not supplied or independently verified. The portal's July 2025 update is not treated as a price date. These prices are historical references, not today's prices. Missing prices are not shown as zero or free.

The original import retains source row references and raw fields, using conservative brand, pack, concentration and English-agent matching. It excludes missing/nonpositive amounts and ambiguous/conflicting joins, and uses the public/citizen column rather than the hospital column. Values are stored as integer fils.

Additional official reduction lists were researched for v0.6. A 2025-labelled page and older PDF creation metadata do not establish current price effective dates. No further prices passed release verification in this iteration. The research outcome is recorded in `docs/PRICE_RESEARCH_v0.6.json`.

Official source: https://opendata.gov.jo/en/dataset/drug-prices-838-2021

## Comparison safeguards

Lower-price ranking requires matching ingredient, source concentration and dosage form fields, plus agreement of explicit route/release labels detected in the brand/form. This is intentionally conservative. Plain, prolonged-release and other formulations are not merged by fuzzy matching. Source-field agreement does not prove interchangeability or suitability for substitution. Confirm route and release characteristics with a pharmacist.

Automatic comparison also requires positive prices from the same source snapshot. Different source periods, missing prices or incompatible products are shown without ranking or savings. Pack-price comparison requires matching pack labels; different packs need a reliable, consistent tablet/capsule count for per-unit calculations. The first selected pack is the reference. Displayed unit prices can contain fractions of a fils; pack prices have three decimal places.

Entered prices stay on the device and are separately labelled. Their comparison requires matching valid dates, positive values with up to three decimals, and compatible product/pack fields. Edits hide stale results until Calculate is pressed again.

The catalogue groups 10,628 original product/pack rows into presentations without deleting rows. The original registered-medicines filename is dated 9 June 2026, retrieved 31 October 2026; the source webpage has a conflicting date. The effective registry date has not been verified. Inclusion does not establish current registration or pharmacy stock. The source has 302 missing scientific labels, 303 missing strengths and one missing form; these fields are not guessed. Verified originator/generic classification, barcodes, live stock and clinical/renal dosing are not supplied.

## Files and validation

Runtime: `index.html`, `app.js`, `core.js`, `search.js`, `styles.css`, `catalogue.json`, `prices.json`, both manifests, `sw.js`, and icons. Source audits and release notes are under `docs/`. Pre-existing unrelated repository files are preserved in the complete package and are not used by this app.

Checks:

```sh
node --input-type=module --check < app.js
node --input-type=module --check < core.js
node --input-type=module --check < search.js
node --check sw.js
node tests/release.cjs
```

The regression check uses the actual catalogue/prices for guarded comparisons, exact pack-size priority, release/route exclusions, typo/strength safeguards, Arabic aliases, complete row retention and translation-key parity. Browser review covered 320 px and 390 px layouts, direct top controls, recorded and entered-price cards, stale-result hiding, filter chips, shared-link reload, multi-pack links and return-position restoration. Physical-device installation and offline behavior were not independently retested for this release.

To rebuild the original price import with Python and openpyxl:

```sh
python scripts/import_historical_prices.py /path/to/source.xlsx --retrieved-on 2026-10-31
```

Local preferences, saved products, comparison choices and entered prices remain in the existing `jma-*` browser storage. There is no account, telemetry, patient database or analytics. Source dates, source links and limitations are available in About.
