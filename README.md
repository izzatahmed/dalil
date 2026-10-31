# دليل الادوية الاردني
# The Jordanian Drugs Directory

Version 0.5.0 — 31 October 2026. A static Arabic/English medicine directory for GitHub Pages.

## Upload the update

Extract the modified-files ZIP and upload **all its contents** into the existing `dalil` publishing location, replacing older files. Include the new **prices.json** and **manifest.en.webmanifest**, along with app.js, core.js, styles.css, index.html and sw.js. Keep catalogue.json in the same directory. The complete ZIP contains all website files, including the catalogue and pre-existing repository files.

No build, server, database account or ChatGPT sign-in is required. Open the GitHub Pages website after deployment, not a GitHub file preview. Refresh to obtain the versioned v0.5 assets.

## Interface changes

- The site name is exactly **دليل الادوية الاردني** in Arabic and **The Jordanian Drugs Directory** in English, including the browser title and language-specific app manifests.
- Text-size and night-mode controls are directly on the top strip. The language button shows the target language's initial: **E** for English and **ع** for العربية. Full language names remain available to screen readers and in tooltips.
- The home page shows search guidance and coverage counts. It does **not** show an alphabetical drug list. Results start after typing or explicitly choosing a filter. Saved medicines remain available from their own tab.
- Search responds as you type. Filters include dosage form, manufacturer country, concentration, pack contents and presence/absence of a historical price. Numeric concentration filtering matches complete numeric tokens: 10 does not match 100. Pack-count filtering can recognise bare tablet/capsule counts where the form supplies the unit.
- Repeated pack rows are grouped into 8,525 presentations. All 10,628 original JFDA catalogue rows are preserved. All displayed medicine/ingredient names retain the original source spelling; common Arabic search aliases are lookup aids.

## Historical prices now included

**5,046 catalogue packs have an imported historical price in JD (ISO currency JOD).** These are tax-inclusive public/citizen pack prices from the government resource labelled **12-Drug2020**, interpreted as a December 2020 file label.

They are **historical references, not current prices**. The workbook properties show creation on 23 September 2020 and last save on 19 April 2021. Individual effective dates are not supplied or independently verified. The portal's July 2025 page-update date is not used as a price date. A record without a matched price is left unpriced, not shown as zero or free.

The historical file has 15,445 data rows, including non-drug/unpriced entries. 6,283 rows have usable positive public prices with valid fils precision. Exact conservative matching against the current catalogue, including local agent, accepted 5,046 pack records. The hospital-price column was not used.

Source page:
https://opendata.gov.jo/en/dataset/drug-prices-838-2021

Source resource:
https://opendata.gov.jo/dataset/MIGRATED-838-2021/resource/b3c4be77-c54b-40a3-b048-17f4a4cad431/download/12-drug2020-.xls?increment=true

Despite its `.xls` URL, the downloaded file contains an XLSX workbook. The source page identifies JFDA as the organisation and the Jordanian open-data licence. Per-entry source row numbers, original price-source brand, pack, concentration and agent are preserved in prices.json. The source file hash, column names, dates, inclusion criteria and counts are in docs/PRICE_IMPORT_AUDIT.json.

## Matching method

Price joins require matching brand name, concentration, pack and English local-agent label, after limited case/spacing/punctuation and explicit pack-unit normalisation. There is no fuzzy brand matching, clinical ingredient inference, conversion between dose units or assumption that similarly named products share a price. A price mapping to multiple current product identities, or conflicting source prices for one key, is rejected. No conflicting/ambiguous mappings were accepted in this release. Missing fields and nonpositive prices were excluded.

The catalogue has no stable JFDA registration identifier to join on, so these are documented source-field matches rather than identifier-verified registration links. Local record IDs are content hashes. The old source's prices and each current catalogue record's regulatory/availability status have not been independently reconfirmed.

## Automatic comparison and entered prices

1. Search for a medicine and open **Alternatives & prices**.
2. Choose exact packs, then open the comparison.
3. **Published historical prices** loads matched prices automatically and displays the source period beside each one.
4. **Enter your prices** remains available for prices you obtain from a pharmacy or receipt. Those amounts stay in this browser and are clearly labelled as your inputs.

Automatic ranking uses only prices from the same historical source snapshot, with matching source scientific/concentration/form fields. Different strengths or release forms are not ranked as equivalents. Identical source pack labels can be compared by pack price. Different pack sizes need readable, consistent tablet/capsule counts for per-unit calculations. Ambiguous packs and differing units do not get a calculated ranking. A price missing for any selected pack leaves available prices visible without a ranking or difference.

The comparison identifies the lowest **within the chosen historical source**, not today's cheapest medicine in Jordan. Differences use the first selected pack as the reference. Unit prices may contain fractions of a fils and are displayed with up to six decimal places in JD. Pack prices are stored as integer fils and displayed with three decimals.

User-entered quotes need positive amounts, valid non-future dates and matching dates before ranking. Editing quotes hides the previous calculation until recalculation. Unsubmitted edits survive language/view changes within the current session. Quotes and preferences are stored locally; there are no patient fields or analytics.

Matching source fields does not establish originator/generic classification, bioequivalence or clinical interchangeability. Confirm strength, route and release properties before substituting a product. Clinical, renal and dialysis guidance remains a separate content task.

## Catalogue source and coverage

The unchanged 10,628-row catalogue comes from the JFDA registered-medicines workbook named 9 June 2026, retrieved on 31 October 2026. Its listing displays 2026/11/06, an inconsistent date. Neither current registration nor pharmacy stock is established by the snapshot. The source has 302 missing scientific labels, 303 missing concentrations and one missing dosage form; none were inferred.

Source page:
https://www.jfda.jo/AR/List/%D9%82%D9%88%D8%A7%D8%A6%D9%85

The app is independent. JFDA is a data source, not the app publisher. catalogue.json bytes are unchanged from the uploaded v0.4 repository. Pre-existing unrelated repository files are retained in the complete ZIP and are not newly integrated into the medicine interface.

## Reproduce the price import

Python with openpyxl is needed only for data maintenance, not for the website. Download the exact historical workbook and verify its SHA-256 against the audit, then run:

```bash
python scripts/import_historical_prices.py /path/to/source.xlsx --retrieved-on 2026-10-31
```

The importer asserts the expected columns and produces prices.json and its audit. It does not modify catalogue.json. This release's output was regenerated and compared for equality. A different file or date needs a reviewed release and updated source-period labels; there is no live price synchronisation.

## Validation

All imported price links and positive integer fils values checked, with real-source spot checks for Glucophage, Diaphage and Metforal. Checked pack and per-unit arithmetic, source-snapshot guards, missing prices, concentration differences and quoted-price safeguards. Verified all original catalogue bytes remain unchanged. Browser checks covered the search-only home, full names and E/ع controls, direct text/night controls, concentration/pack/price filters, actual imported-price cards and automatic historical comparison at 320/390px frame widths. No page overflow was found in those checks. Physical-phone installation and disconnected offline behaviour still need device verification.

App assets, the catalogue and historical prices are cached after a successful online visit where supported. Keep all files together under the same GitHub Pages publishing folder.
