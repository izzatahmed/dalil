# v0.8.0 — 1 November 2026

Based on uploaded v0.7, public GitHub commit `a14a281`.

## Problems fixed

The Arabic brand spelling Famodar was missing from the alias dictionary. Famotidine could also be hidden by a retained Brand field mode or incompatible prior filters. Dark variables were scoped to body while the root viewport background and inherited text colour remained light-theme values.

## Result

- Arabic and English Famotidine searches both return 17 presentations / 35 source pack rows; Arabic and English Famodar searches both return 4 / 9.
- Additional catalogue-backed spellings, diacritic/tatweel/letter/digit normalisation, numeric strength preservation and conservative phonetic discovery improve bilingual search. Unverified phonetic candidates retain source labels and are marked as search aids.
- New text searches can recover from a restrictive old field/filter state when catalogue matches exist. Deliberately chosen filters remain effective. Complete English words match prefixes rather than arbitrary internal substrings in another ingredient.
- Root and body now share a coherent night palette, fill the viewport, and cover all main surfaces. A stored dark preference is applied before styles render. The theme toggle has an explicit moon/sun icon and visible target-mode label, with a 44 x 48 px minimum phone target.
- Catalogue and historical prices remain byte-for-byte unchanged; matching/source/formulation/price guards remain in place.

## Validation

Syntax; complete regression checks with real catalogue rows; Arabic/English parity and number/diacritic/unit examples; near-name distinction tests; original data byte checks; unique HTML IDs and translation parity. Phone review at 320/390 px covers night home/results, root/body colour continuity, input/navigation/dialog surfaces, visible toggle sizing, night persistence, Arabic search in an English UI, old-mode/filter recovery and deliberate no-result filtering. Physical-device installation and offline behavior were not independently retested.

Upload all extracted update ZIP contents into the existing dalil publishing directory, replacing matching files. Include the updated core.js, search.js, app.js, styles.css, index.html, sw.js and both manifests together. Keep catalogue.json and prices.json alongside them.
