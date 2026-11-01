# v0.7.0 — 1 November 2026

Based on uploaded v0.6, public GitHub commit `491d353`.

The previous suggestion index used scientific labels including concentration and formulation. Selecting a complete label could narrow a generic search to one source presentation. Ingredient suggestions now open a browsing family rather than one dose/form.

- Selecting the spelling suggestion for `amoxocillin` opens Amoxicillin: 108 presentations, 144 pack records, 10 forms, 40 distinct source concentration strings and 21 source manufacturer labels.
- Double-clicking a medicine name copies the exact brand name into the search box and opens its ingredient family. Single tap/click on result names provides the same action. Details remains a separate button. Names in Details and comparisons are browsable too.
- Selecting `Amoclan 600 vials` opens Amoxicillin + Clavulanic Acid: 67 presentations, 83 packs, 8 forms, 24 source concentration strings and 17 manufacturers.
- Family selection clears narrow filters. Source manufacturers are visible on cards and available in a manufacturer filter. Single-ingredient and combination browsing are distinct; combination cards are labelled. Manual typing exits family mode and preserves precise strength searching.
- Family scope and manufacturer filters are preserved in hash links and browser history. The initial family result limit is 200; all 108 Amoxicillin presentations are shown immediately.

Family parsing is for discovery only and does not alter scientific fields, strengths, salts, source rows or clinical/price matching. Price equivalence remains strict. Missing ingredients are not invented. Catalogue and price files are byte-for-byte unchanged from v0.6; 5,046 historical prices remain included.

Validation: syntax; regression checks with real source rows; original data byte comparison; translation parity and unique HTML IDs; browser checks at 320/390 pixels; misspelling selection; double-click with active IV/concentration/manufacturer filters; visible companies and combination labels; manual precision after family browsing; exact medicine/family deep links and Back to results. Physical-device installation and offline behavior were not independently retested.

Upload all extracted update ZIP files into the existing dalil publishing directory, replacing matching files. Include app.js, search.js, styles.css, index.html, sw.js and both manifests together. Keep the existing core.js, catalogue.json and prices.json alongside them. The full ZIP includes all existing source data and preserves pre-existing repository files.

Family result ordering places tablets, capsules and suspensions before vials/injectable forms, while retaining every matching source presentation.
