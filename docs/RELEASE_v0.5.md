# v0.5.0 — 31 October 2026

Names: دليل الادوية الاردني / The Jordanian Drugs Directory.

Base repository commit: c11aa92 (public izzatahmed/dalil repository, uploaded v0.4). Catalogue bytes unchanged.

New data: 5,046 dated public/citizen tax-inclusive pack-price matches, from the government resource labelled 12-Drug2020. Source workbook last save: 19 April 2021. Individual price effective dates remain unknown; the portal's 2025 update date is not a price date.

Import: 15,445 source rows; 6,283 usable positive public-price rows; 5,514 current-catalogue candidates before the exact agent-label check; 5,046 accepted unique pack links after agent and ambiguity checks. No fuzzy joins. Hospital prices not imported. Zero/missing/non-fils prices not interpreted as free medicines.

Price matching compares documented brand/concentration/pack/agent source fields because a shared registration identifier is absent from the catalogue. This does not independently verify a current regulatory registration or clinical interchangeability.

UI: direct text-size/night controls, E/ع language button, full language-specific names, no default alphabetical list, extra concentration/pack/historical-price filters. Historical and user-entered price comparisons are separate.

New runtime files: prices.json and manifest.en.webmanifest. Include both when updating.
