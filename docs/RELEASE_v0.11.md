# v0.11.0 — 1 November 2026

- Barcode scanner (camera, on-device; EAN/UPC and GS1 DataMatrix) with manual entry; barcode numbers also work in the main search. `barcodes.json`: 3,807 barcodes → 3,857 packs from the JFDA December 2020 workbook (`scripts/build_barcodes.py`).
- Barcode shown in product details.
- "Contains" fallback search when no name starts with the typed text.
- Dosage-form groups in the form filter (98.8% of rows grouped), with exact source forms kept.
- Includes all v0.9 (RenalRounds links) and v0.10 (2023 prices) changes.
