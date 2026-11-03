# دليل الادوية الاردني
# The Jordanian Drugs Directory

Version **0.13.0**, 3 November 2026. A mobile-first Arabic/English static directory for GitHub Pages. It is an independent directory using JFDA source data.

## Upload the update

Extract the modified-files ZIP and upload **all its contents** into the existing `dalil` publishing directory, replacing matching files. **Include the updated `app.js` and `search.js` together.** Keep the existing `catalogue.json`, `prices.json`, manifests and icons alongside `index.html`. The complete ZIP includes the full website and preserves pre-existing repository files.

No build, account, API key or server is required. Keep the files at the ZIP root rather than creating a second nested `dalil` folder. GitHub Pages should publish the same directory as before. The versioned service worker refreshes the app assets; reload after deployment if an older version remains visible.

## Recent prices and clearer kidney links in v0.13

- 32 packs of important medicines (Entresto, Kerendia, Eliquis, Pradaxa, Ozempic, Verquvo, Prograf, Advagraf, Valcyte, One-Alpha, Aranesp, Eprex, Prolia, Repatha, NovoRapid, Exforge and others) have a recent public price, looked up on 3 November 2026 on the Drug Center pharmacy website by the site editor and matched to each pack by hand (`scripts/import_pharmacy_prices_2026_11.py`, `docs/PRICE_CHECK_2026-11-03.json`). 29 of them had no price before. These are labelled "Recent price · 2026-11"; older ones keep "Historical price".
- Results show a **Kidney** badge when the medicine has a RenalRounds page, and the RenalRounds link now sits at the top of the details, under the name.
- A note beside the JFDA links explains that a sign-in page may appear: ignore it and click the link again.

## Voice search in v0.12

- A mic button in the search box listens in Arabic (ar-JO) or English, following the interface language. It appears only in browsers that offer speech recognition (Chrome on Android, recent Safari). Of the recognised alternatives, the first one that matches a product is used; otherwise the spelling suggestions and Arabic phonetic matching take over.
- Privacy: speech is processed by the browser's own speech-recognition service (in Chrome usually Google's servers), not by Dalil. Nothing starts until the mic is tapped, and the button says so.

## Barcode scanner and easier searching in v0.11

- **Scan the box.** The barcode button in the search box opens the phone camera (Android Chrome and other browsers with the Barcode Detection API). It reads EAN/UPC barcodes and the GS1 DataMatrix codes on newer packs, entirely on the phone — no image is sent. A recognised barcode opens that product. Browsers without camera barcode support (for example iPhone Safari) show a box for typing the number under the barcode. A barcode number typed in the main search box also finds the product.
- `barcodes.json` holds 3,807 barcodes for 3,857 packs. They come from the `DRG_BARCODE` column of the December 2020 JFDA price workbook, for packs already matched by `import_historical_prices.py`. Rebuild with `scripts/build_barcodes.py <workbook>`; it checks the workbook SHA-256. Packs without a barcode in that file are found by name. Each product's details show its barcode.
- **"Contains" search.** When no name starts with the typed text, Dalil shows names that contain it (for example `tamol` finds paracetamol) and says so.
- **Dosage-form groups.** The form filter now starts with 10 groups (tablets, capsules, injections, oral liquids, skin, eye & ear, suppositories, inhalers, nasal, powders) covering 98.8% of rows; the exact source forms remain below them.

## Newer prices in v0.10

- The JFDA reduced-price list («قائمة الأدوية المخفضة», 374 items; PDF dated 25 July 2023, shown on the JFDA website with a 2025 date) was imported with `scripts/import_reduced_prices_2023.py`. 328 items matched a catalogue pack exactly (313 automatically, 15 after manual review). Their "current price including tax" now replaces the 2020 price, and 129 packs that had no price before now have one. Each price shows its source period (2020-12 or 2023-07). Comparisons and lower-priced options only rank prices from the same source.
- Matching uses brand, every number in the product name, pack count and form. A match is accepted only when it is unique. The list's "previous price" agreed with the 2020 price for the same pack (median ratio 1.00), which confirms the matching. The 45 unmatched items (brands or packs not in the June 2026 catalogue, or ambiguous products) are listed in `docs/PRICE_LIST_2023-07.json` with a status.
- Run order: `import_historical_prices.py` (2020 workbook), then `import_reduced_prices_2023.py <list.pdf>`. The second script is idempotent and checks the PDF's SHA-256.
- About lists every price source; card labels show the actual price years.

## Linked with RenalRounds in v0.9

- Product details now show **Kidney dosing · RenalRounds** (جرعات مرضى الكلى) links for 6,811 of the 10,628 JFDA rows. Each link opens the matching adult renal-dosing entry at izzatahmed.github.io/drugs, matched by active ingredient and route: tablets and syrups link to the oral entry, vials and ampoules to the IV entry, and creams, eye or nasal products only to a topical entry (for example, Protopic ointment is not linked to systemic tacrolimus). Combination products link to each ingredient and to the combination entry when RenalRounds has one.
- The links come from `renalrounds.json`, which RenalRounds' `build_dalil_links.py` generates from this catalogue. It records the catalogue SHA-256 and must be regenerated whenever `catalogue.json` changes. The site still works if the file is missing; the links are simply hidden.
- About links to RenalRounds. RenalRounds links back: each medicine there shows "Products in Jordan" with a button that opens this directory filtered by scientific name.
- Upload every file in the update ZIP together (it includes all v0.9 and v0.10 changes).

## Arabic search and night appearance in v0.8

- `فاموتيدين` and `Famotidine` return the same 17 presentations / 35 source packs. `فامودار`, `فامو دار` and `Famodar` return the same 4 presentations / 9 source packs. Selecting a name still opens the broader ingredient family.
- Arabic matching normalises vowel marks, tatweel, Arabic/Persian digit scripts and common letter variants. Explicit brand/ingredient aliases are checked against source labels. Queries such as `فامودار٢٠ملغ` preserve the requested concentration.
- Unlisted Arabic spellings can use conservative phonetic matching against source brand/ingredient words. These are search candidates, not verified Arabic registration names; a note asks users to check the displayed English name and strength. Complete long names require complete phonetic-word matches; only short typed prefixes use prefix matching. The original names remain visible.
- English matching uses word prefixes, avoiding accidental matches inside a different ingredient name, such as Citalopram inside Escitalopram. Neither browsing nor phonetic matching modifies clinical/price equivalence.
- During a newly typed search, if an old field mode or previous filters hide every match but the catalogue contains matches, the app switches to All and clears those previous filters with a visible message. Filters deliberately changed after typing are respected, even when they produce no results. Invalid or unavailable strengths are not silently removed.
- A unified night palette covers the root viewport, body, cards, search controls, filters, dialogs, comparison/saved panels, navigation and empty home. The body fills the viewport. Stored night preferences are applied before the stylesheet renders to avoid a light-page flash.
- The top appearance button has a 44 px minimum width and 48 px minimum height on phones, a clear moon/sun icon, and a visible Night/Day or ليلي/نهاري label. Its action, pressed state and browser theme colour update together.

### Retained browsing features


- Exact Arabic/English names and the direct text-size, night and E/ع controls are retained.
- The home page stays search-only. The 10,628 original source rows remain searchable.
- Ingredient suggestions use browsing families instead of complete strength-specific source labels. For example, the spelling suggestion for `amoxocillin` is **Amoxicillin**, covering 108 presentations / 144 source pack rows / 10 forms / 21 source manufacturers.
- Double-click a medicine name to place its exact brand name in the search box and browse its active-ingredient family. A single tap on a result name provides the same action on mobile. Separate Details buttons still open the selected presentation.
- A family selection clears form, country, manufacturer, concentration, pack and historical-price filters so a previous IV/strength filter cannot hide the other presentations. The family scope is shown above results. Manual typing leaves family browsing and returns to precise text/numeric search.
- `Amoclan 600 vials` expands to the amoxicillin + clavulanic acid family: 67 presentations / 83 source pack rows / 8 forms / 17 source manufacturers, including oral preparations and other brands. A single-ingredient Amoxicillin family includes labelled combination products; an explicitly selected combination keeps its complete ingredient set.
- Every result shows the raw source scientific name and manufacturer. Combination products have a separate label. A manufacturer filter is now available.
- Up to 200 presentations are shown immediately in family browsing; larger result sets retain Show more. All 108 amoxicillin presentations fit in the initial family result set.
- Choosing a suggestion labelled **All forms, strengths & companies** explicitly broadens the search. Typing a concentration manually still matches complete numeric tokens, and fuzzy spelling suggestions still retain typed numbers before selection.
- Arabic search aliases cover common ingredient and brand spellings. Official product names retain the source language. Aliases do not establish approved Arabic names, indications or clinical equivalence.
- Concentration queries match complete numeric tokens: `10` does not match `100`. Existing form, country, manufacturer, concentration, pack and historical-price filters are retained. Active filters appear as removable chips; Clear all removes filters while preserving the query.
- The result action opens **Lower-priced options**. Choose a reference pack; matching pack sizes appear first. Other readable tablet/capsule pack sizes show explicit per-unit prices. A lower unit price can accompany a larger pack with a higher total pack price.
- Historical and entered-price comparisons use readable cards. Different source fields are highlighted. Ranking remains conditional on valid, compatible data.
- Medicine and exact-pack links use URL hashes, so GitHub Pages does not need server routing. Copy link includes language and search filters. Direct links, reload, browser back and Back to results are supported. Returning restores the query, filter state, result limit and scroll position.

## Browsing families and source integrity

Family names remove explicit doses and selected salt/hydrate wording for discovery only. Parenthesised source descriptors are not used in these browsing labels. Source records, source strengths, clinical matching and price-comparison keys remain unchanged. Broad browsing across strengths, routes or release types does **not** establish interchangeability. Missing source ingredients are not inferred; those records fall back to their brand search.

Family scope, manufacturer filtering and the displayed query survive shared medicine links and reloads. Returning from Details restores the family result list and scroll position. Clearing the search returns to the search-only home.

## Historical prices and limits

**5,046 catalogue packs have a matched historical tax-inclusive public/citizen price in JD (ISO JOD).** `prices.json` and `catalogue.json` are byte-for-byte unchanged from v0.7 (and earlier price-bearing versions).

The price source is the official government resource labelled `12-Drug2020`, interpreted as a December 2020 filename label. Workbook creation is 23 September 2020; last save is 19 April 2021. Individual price effective dates are not supplied or independently verified. The portal's July 2025 update is not treated as a price date. These prices are historical references, not today's prices. Missing prices are not shown as zero or free.

The original import retains source row references and raw fields, using conservative brand, pack, concentration and English-agent matching. It excludes missing/nonpositive amounts and ambiguous/conflicting joins, and uses the public/citizen column rather than the hospital column. Values are stored as integer fils.

Additional official reduction lists were researched for v0.6; v0.7 and v0.8 change search behavior without adding prices. A 2025-labelled page and older PDF creation metadata do not establish current price effective dates. No further prices passed release verification in this iteration. The research outcome is recorded in `docs/PRICE_RESEARCH_v0.6.json`.

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

The regression check uses the actual catalogue/prices for guarded comparisons, exact pack-size priority, release/route exclusions, typo/strength safeguards, Arabic aliases, amoxicillin and combination-family coverage, complete row retention and translation-key parity. Browser review for v0.7 covered 320 px and 390 px layouts, the amoxocillin suggestion, all-form family results, exact-name double-click, narrow-filter clearing, manufacturer display, manual-search precision, and shared medicine/family link restoration. The v0.6 recorded/entered-price calculations and related guards remain covered by regression checks. Physical-device installation and offline behavior were not independently retested for this release.

To rebuild the original price import with Python and openpyxl:

```sh
python scripts/import_historical_prices.py /path/to/source.xlsx --retrieved-on 2026-10-31
```

Local preferences, saved products, comparison choices and entered prices remain in the existing `jma-*` browser storage. There is no account, telemetry, patient database or analytics. Source dates, source links and limitations are available in About.

Family result ordering places tablets, capsules and suspensions before vials/injectable forms, while retaining every matching source presentation.

Browser review for v0.8 additionally covers Arabic/English query parity, stale-mode and stale-filter recovery, deliberate filtering, night-mode persistence on reload, full-viewport dark backgrounds, dark details dialogs and header sizing at 320/390 px. Physical-device installation and offline behavior were not independently retested.
