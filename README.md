# دليل — Dalil v0.3.0 — GitHub Pages edition

An independent medicine catalogue with 10,628 JFDA source product rows. This package is a complete static website. No server, build, package installation, database account or ChatGPT sign-in is required by the application.

## Publish on GitHub Pages

1. Extract this ZIP on your computer. Upload the extracted files and the docs folder to a new GitHub repository. The repository can be named `dalil`, or another name you choose.
2. Confirm `index.html`, `app.js`, `styles.css`, `catalogue.json`, `sw.js`, the manifest and icons are directly at the repository root. Do not upload the ZIP itself or place these files inside an extra wrapper folder.
3. Open repository Settings → Pages. Under Build and deployment, select Deploy from a branch, choose the main branch and /(root), then Save.
4. Wait for the Pages deployment to succeed. Use the exact published address GitHub displays in Settings → Pages. Open that address, rather than an individual file on github.com.

The same files work at a domain root or a repository subfolder. All application assets use relative paths. The empty .nojekyll file is included for static hosting.

## Use on a phone

Open the published HTTPS address in the phone browser. Search is near the top. The four navigation buttons remain at the bottom. Product records display as cards with 44-pixel save and comparison buttons. The comparison table scrolls within its dialog. English and Arabic interfaces, theme and text-size controls are included.

You may use the browser's Add to Home Screen or Install option where supported. Open the application online once to load the catalogue and allow offline caching. Browsers can evict stored data, and installation/offline behaviour still needs verification on an actual device. This release was checked in narrow browser frames rather than on physical phones.

## What's included

- All 10,628 nonempty product rows from one official JFDA registered-medicines workbook.
- Brand/scientific-name/manufacturer/agent search, country and dosage-form filters.
- Saved medicines stored on the device, four-product field comparison and CSV export.
- Source worksheet row numbers, original concentration values and data coverage notes.
- Responsive layout checked at 320, 375 and 430 pixel iframe widths in English and Arabic, with no horizontal page overflow. Search and comparison were also checked on the narrowest frame with enlarged text.
- Offline cache keys scoped to this repository's URL, to avoid mixing caches between applications on the same GitHub Pages domain.

## Data limits

The source file is labelled 9 June 2026 and was retrieved on 31 October 2026. JFDA's listing displays 2026/11/06, an inconsistent date. The date in the filename is an edition label, not a verified current-registration date. All records are from that one source, not a verified complete current-market inventory.

This release contains no current prices, pharmacy stock, barcodes, clinical monographs or renal/dialysis dosing. Those fields are explicitly marked unavailable. 302 scientific labels, 303 concentrations and one dosage form are blank in the source. Drug names remain in the source language; the bilingual interface does not imply verified Arabic brand aliases.

Concentrations originally stored as numeric percentages are converted without rounding, and original values/formats remain inspectable. Source fields have not undergone clinical standardisation. Comparison and exact-scientific-label related records do not establish interchangeability.

The app's update control checks for application releases. It does not synchronise with JFDA. Prices require a verified new source and exact product/pack matching.

JFDA source page:
https://www.jfda.jo/AR/List/%D9%82%D9%88%D8%A7%D8%A6%D9%85

A detailed source audit, including its URL, hash, row counts and missing-field counts, is in docs/SOURCE_AUDIT.json. JFDA is the source, not the publisher of this independent app.

## Files

- index.html: application page.
- app.js and styles.css: original interface, search and local features.
- catalogue.json: imported source records and provenance metadata.
- manifest.webmanifest, sw.js and icons: installation and offline-cache support.
- docs/SOURCE_AUDIT.json: source and import audit.

Keep these files together. An index.html opened directly from a local file manager cannot fetch catalogue.json normally. Use a web server or GitHub Pages.

## Updates

Replace changed website files in the same repository. Keep all referenced assets together, preserve source dates and missing values, and increment the service-worker cache version with a new release. Catalogue content and clinical information require separate source review before publishing changes.

GitHub's publishing-source instructions:
https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## v0.3 update

The app name, browser title, home-screen name and icons are now دليل. New visits default to Arabic, with English available from the top control; existing language preferences are kept. Catalogue records are unchanged. A visible loading/error panel with a Retry button replaces silent data-load failure, and requests time out after 20 seconds. Application asset URLs and the offline cache are versioned to help browsers obtain the new interface. Existing saved items and preferences retain their original local-storage keys.

The live site https://izzatahmed.github.io/dalil/ was checked on 31 October 2026: all 10,628 records loaded and Jardiance returned the 10 mg and 25 mg records. The reported blank page was not reproduced; its cause is unconfirmed. The new files must be uploaded before the live site shows the new branding.

If a browser still shows a blank or old page after the deployment succeeds, first reopen the published website (not the GitHub repository). On desktop, try Ctrl+Shift+R. A private browsing window can help distinguish a cached copy from a failed deployment without removing saved medicines or preferences.
