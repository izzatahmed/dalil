# v0.6.0 — 1 November 2026

Based on public GitHub commit `8f52fb7` (uploaded v0.5).

- Instant bilingual autocomplete and conservative spelling suggestions. Strength numbers remain in suggestions and complete numeric tokens are matched. Expanded Arabic search aliases are aids, not official registration names.
- Lower-priced matching packs open directly from results. Matching pack sizes appear first; other tablet/capsule pack sizes show per-unit prices. All ranking requires matching source ingredient, concentration, form, explicit release/route labels and price snapshot.
- Historical and entered-price results use responsive comparison cards. Different fields are highlighted. Missing prices and incompatible products are not ranked.
- Removable filter chips and Clear all preserve the query.
- Hash-based medicine and exact-pack links work on GitHub Pages. Copy medicine/pack link preserves language and search filters. Browser back and Back to results restore query, result limit and scroll position.
- Header name, E/ع controls, larger text, night appearance and the search-only home are retained.

`catalogue.json` and `prices.json` are unchanged. The 5,046 imported prices remain historical references from the December 2020-labelled file. Further official reduction lists were researched; no new prices passed the release verification in this iteration. See PRICE_RESEARCH_v0.6.json.

Validation: ES module syntax; tests/release.cjs; original data byte comparison; unique HTML IDs; Arabic/English translation key parity; phone review at 320 and 390 pixels; desktop shared-link reload; multi-pack copy/reopen; filter chip removal; search/scroll restoration; direct theme/text toggles; recorded comparison; entered-price calculation and stale-result hiding. Physical-device installation and offline behavior were not independently retested.

Upload the extracted update ZIP contents to the existing dalil publishing directory. Include the new search.js alongside all changed files. The complete ZIP preserves the repository's pre-existing files.
