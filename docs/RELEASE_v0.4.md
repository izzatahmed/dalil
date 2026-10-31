# Release v0.4.0 — 31 October 2026

- Input source: public izzatahmed/dalil repository commit f8b37a0d55669041e93b29d3c209696ccadb3d47.
- Original catalogue: 10,628 rows; bytes unchanged in this release.
- Display groups: 8,525; grouping is a view, not a data deletion or a count of unique active ingredients.
- New matching/monetary helpers: core.js.
- Arabic search aids: 32 aliases plus Arabic-Indic digit normalisation. Displayed medicine/ingredient labels remain original source values.
- Current official price records imported: zero.
- User-entered price comparison: positive JOD amounts stored as integer fils, date/source metadata, same-formulation checks and conservative pack-unit arithmetic. This is not a clinical substitution engine.
- Price source assessed: https://www.jfda.jo/ebv4.0/root_storage/ar/eb_list_page/%D8%A7%D9%84%D8%A3%D8%AF%D9%88%D9%8A%D8%A9_%D8%A7%D9%84%D8%AA%D9%8A_%D8%AA%D9%85_%D8%AA%D8%AE%D9%81%D9%8A%D8%B6_%D8%A3%D8%B3%D8%B9%D8%A7%D8%B1%D9%87%D8%A7-4.pdf
- The assessed PDF has 18 pages and 374 numbered entries; its CreationDate/ModDate metadata are 2023-07-25. The listing displays 2025/01/01. That does not establish current effective prices, so no rows from it were merged into the app.
- The live price enquiry endpoint returned HTTP 503 in this environment during this update. Browser/search failures do not establish that the service is unavailable to all users.
- Source clinical values are not independently clinically validated or harmonised. Routes/release properties may be incomplete or inconsistently represented; matching source labels alone cannot establish interchangeability.
