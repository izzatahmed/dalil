# دليل — Dalil v0.4.0

A static, mobile-friendly Arabic/English medicine directory for GitHub Pages. All 10,628 JFDA catalogue rows remain unchanged. The interface groups them into 8,525 product presentations so repeated pack rows do not crowd the results.

## Install this update

Extract the modified-files ZIP and upload **all its contents** into the same `dalil` publishing folder, replacing existing files. Include the new **core.js** file. Keep `catalogue.json` alongside index.html. The complete ZIP also includes the catalogue for a fresh installation.

No build step, server, database account or ChatGPT sign-in is needed. Files work under a repository subpath such as `/dalil/`. After the GitHub Pages deployment succeeds, reopen the published address and refresh. The service-worker cache and script/style URLs are versioned for v0.4.0.

## What changed

- Results show the trade name, source scientific label, form and pack summary. Manufacturer, agent and provenance details are inside the medicine page.
- Pack rows with the same brand, scientific label, concentration, form, manufacturer, manufacturer country, agent and marketing company are grouped. Every original row remains inspectable and exportable.
- Search responds on the next animation frame as you type. It works without pressing Enter or a Search button. Filters are collapsed until requested. Arabic and English searches normalise case, spacing and Arabic-Indic digits.
- A prominent language button switches the interface and direction. There are 32 common Arabic generic/brand search aliases. These are search aids, not official Arabic registration labels; displayed names remain in the source language. Common forms and manufacturer countries have interface translations; unlisted source terms remain verbatim.
- Medicine details include matching alternatives and all listed packs. A four-pack comparison is available from the bottom navigation.
- Theme, larger text and export controls move into Settings.
- Existing local favourites, comparison selections and language/theme preferences keep their original storage keys.

## Price comparisons: what works now

**Current official JFDA prices are not included.** The app does not invent prices or claim that a product is available in a pharmacy. The live JFDA price service returned an error during preparation. A downloadable JFDA price-reduction PDF displayed with a 2025 listing date has creation metadata from July 2023; it was not imported as current pricing.

To compare real prices you have obtained:

1. Open a medicine and choose **Alternatives & prices**.
2. Select two to four exact packs, then open the comparison.
3. Enter each pack's price **including tax, in JOD**, its date and optionally a source such as a pharmacy or receipt. Do not enter patient information.
4. Calculate. The app labels all amounts **Prices you entered**. They stay in this browser and are saved only after valid calculation.

Prices support up to three decimal places (fils), including Arabic-Indic digit input. Zero, negative and invalid prices are rejected. Dates must be valid and not in the future. Quotes with different dates are displayed without a price ranking or savings calculation.

For matching formulation fields and the same source pack label, pack prices can be compared. For different pack sizes, per-tablet or per-capsule comparison requires a conservative unit count readable from the source pack, such as `50 Tab`, `120` with tablet form, or `30 TAB /1 BOX`. A count whose stated unit contradicts the source form is rejected. Composite or ambiguous packs are not expanded. Unit costs can show fractions of a fils (up to six decimal places in JOD); pack prices show three decimals.

Any ranking says **Lowest of the entered prices**, not the cheapest product in Jordan. Differences are relative to the first selected pack. Editing a quote hides the old calculation until recalculation. Unsubmitted edits are retained while switching language or views in the current session.

## Alternative matching

Candidates require the source scientific label, concentration and dosage form, with only case/spacing and explicit per-tablet/capsule notation normalised (`10 mg` and `10 MG/1 TAB` in tablet records). Salts, release formulations, routes, different strengths, different units and ingredient combinations are not treated as interchangeable. Incomplete records have no matching-formulation key. Different source spellings can leave out genuine alternatives.

Originator/generic status, bioequivalence, clinical substitution and current registration status are not established by this data. The comparison does not recommend treatment changes. Clinical, renal and dialysis dosing remain a separate pending content task.

## Data source and limits

The original JFDA workbook is named 9 June 2026 and was retrieved on 31 October 2026. The source listing shows 2026/11/06, a conflicting date. This is a dated snapshot, not a verified current register or complete current-market inventory.

302 scientific labels, 303 concentrations and one form are missing in the source. Missing data remain explicit. No barcode or live pharmacy-stock data are supplied. The `catalogue.json` bytes are unchanged from the uploaded v0.3 repository.

Source page:
https://www.jfda.jo/AR/List/%D9%82%D9%88%D8%A7%D8%A6%D9%85

The app is independent; JFDA is the source, not the publisher. Source URL, worksheet rows, original numeric percentage values and their Excel formats remain available in the catalogue. Detailed metadata are in `docs/SOURCE_AUDIT.json`.

## Files

Keep index.html, styles.css, app.js, **core.js**, catalogue.json, sw.js, manifest.webmanifest and the icons together. Do not open index.html directly as a local file; serve it or use the GitHub Pages address.

Offline support depends on the browser retaining its cache; open the site online once first. This release was tested in desktop and narrow browser views, not on a physical phone with networking disabled.

## Validation

All source rows preserved and all grouped rows reconciled. Checks covered integer monetary parsing, Arabic digits, per-unit matching, different strengths/releases, missing prices, mismatched dates, ambiguous packs and unit-price calculations. Browser checks covered input-driven search, Arabic aliases, English/Arabic switching, grouped results, source-matched alternatives, entering two pack prices, recalculation, language-switch draft retention, date guards and overflow at 320/390px frame widths. A desktop view was also checked. QA prices were test inputs in a separate preview browser; no example or invented prices are shipped in the catalogue.

To enable automatic official-price comparisons later, obtain an authorised current source with product identifiers, formulation, pack, price type/currency and effective dates, then review exact joins. A search result or similar brand spelling alone is not a sufficient price join.
