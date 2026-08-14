# FOSS4G Hiroshima 2026 Kitagi Island Poster Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create, review, print, and display an English A0 portrait poster for the accepted FOSS4G Hiroshima 2026 presentation about detecting quarry pond remnants on Kitagi Island.

**Architecture:** Treat the existing exp002 report and generated figures as the numerical and evidence source of truth. Create a dedicated poster source in an editable vector-first format, export a print-ready A0 PDF and a review PNG, then pass the artifact through a Codex content/print review before Claude revisions and Visipri submission.

**Tech Stack:** SVG or the Visipri A0 template (editable poster source), PDF export tool selected during Task 1, existing PNG/JPEG figures under `docs/results/exp002/`, Python/uv only when a figure or validation script must be regenerated, Visipri for printing.

## Global Constraints

- Poster language is English only.
- Poster size is A0 portrait: 841 × 1189 mm.
- The submitted PDF is the print source of truth; the editable source must remain in the repository.
- The final artwork must accommodate Visipri's confirmed production requirements: A0 finished size 841 × 1189 mm, 3 mm bleed when artwork reaches the edge, CMYK output if required by the selected product, PDF input, and embedded or outlined fonts.
- Numerical claims must agree with `docs/reports/exp002_kitagi_quarry_water_detection_report.md` and the accepted proposal.
- Do not claim that all detected polygons are confirmed quarry ponds; label them as detected water polygons or candidate remnants where appropriate.
- State the Sentinel-2 10 m spatial-resolution limitation and the need for field validation.
- Include CC BY 4.0 and data/software attribution on the poster.
- Use only figures with known provenance; do not use untracked `tmp/` files directly in the final poster.
- Follow the official poster requirements: Sakura Lounge, September 1–3, core time September 2 13:00–15:00, self-mount after September 1 09:00, pins only, removal by September 3 18:30.
- The poster must fit the accepted proposal rather than becoming a general report or a second presentation deck.

## Repository Context and Source of Truth

Existing material to read before editing:

- `docs/plans/exp002_kitagi_quarry_water_detection.md` — original research plan and intended workflow.
- `notebooks/exp002_kitagi_quarry_water_detection.ipynb` — executable analysis and data processing history.
- `docs/experiments/exp002_kitagi_quarry_water_detection.md` — notebook-aligned processing description.
- `docs/reports/exp002_kitagi_quarry_water_detection_report.md` — final interpretation, limitations, and references.
- `docs/results/exp002/` — tracked figures and field photographs.
- `docs/posters/exp002_kitagi_foss4g2026_proposal.md` — proposal text and metadata supplied for poster planning.
- `scripts/generate_exp002_presentation.py` — existing presentation wording and figure usage.
- `https://2026.foss4g.org/ja/program-schedule/poster-session/` — official poster size, display, and mounting rules.
- `https://talks.osgeo.org/foss4g-2026/schedule/nojs` — official session date, time, and room.

Claims to lock before design:

- Spring imagery: 113 intra-island water polygons of at least 100 m².
- Summer imagery: 145 intra-island water polygons of at least 100 m².
- Composite condition: `NDWI > -0.2 OR MNDWI > -0.1`, excluding `NDVI > 0.3` vegetation pixels.
- The 145 detected polygons are spatially concentrated in four island regions and are consistent in distribution with historical quarrying records; individual pond-to-quarry identity is not yet field-validated.
- The vegetation mask excluded only 9 pixels in the reported summer analysis.
- Outputs include GeoJSON and GeoTIFF for future fieldwork and heritage documentation.
- Historical context: 127 active quarry sites were recorded at the 1957 peak; this is contextual evidence, not a one-to-one validation of the 145 detected polygons.
- Imagery dates: spring 2025-03-23 and summer 2025-08-02.
- Data access: Microsoft Planetary Computer STAC API.
- Software stack: rasterio, numpy, shapely, pystac-client, planetary-computer, and folium.
- Transferability: the workflow may be extended to other quarried islands in the Seto Inland Sea.

## Deliverables and File Boundaries

- Create: `docs/superpowers/plans/2026-08-14-foss4g-kitagi-poster.md` — this implementation plan.
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg` — editable A0 portrait vector source, generated or maintained by Claude. If CMYK or bleed handling is not reliable in SVG, use the Visipri A0 Illustrator/PowerPoint template and retain the editable source instead.
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf` — print-ready A0 PDF exported from the source.
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_preview.png` — reduced review preview; not used for printing.
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md` — English poster copy, source references, and claim-to-evidence mapping.
- Create: `docs/posters/validate_exp002_kitagi_quarry_foss4g2026_poster.py` — deterministic checks for page size, required text, output existence, and referenced assets, if the selected export workflow supports reliable validation.
- Create: `docs/posters/exp002_kitagi_foss4g2026_print_log.md` — confirmed Visipri settings, order, delivery, and physical inspection record.
- Modify only if required: `scripts/` for reproducible figure regeneration; do not modify the exp002 analysis unless a numerical discrepancy is found and explicitly recorded.

## Role Gates

1. **Codex planning/design gate:** Codex fixes the content contract, evidence map, layout, typography scale, figure inventory, and acceptance checks.
2. **Claude production gate:** Claude creates the source, figures as needed, PDF, preview, and production notes from the approved design.
3. **Codex review gate:** Codex checks scientific accuracy, English copy, visual hierarchy, A0 readability, PDF technical properties, and print readiness.
4. **Claude revision gate:** Claude resolves every blocking review item and regenerates all derived artifacts.
5. **Codex final gate:** Codex re-runs validation and gives explicit approval before Visipri ordering.
6. **Human print/venue gate:** The user confirms Visipri options, places the order, carries the poster, mounts it, attends core time, and removes it.

## Plan

### Task 1: Freeze requirements and choose the production workflow

**Files:**
- Read: `docs/reports/exp002_kitagi_quarry_water_detection_report.md`
- Read: `docs/results/exp002/`
- Read: official FOSS4G poster requirements
- Read: `docs/posters/exp002_kitagi_foss4g2026_proposal.md`
- Create or update: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md`
- Create: `docs/posters/exp002_kitagi_foss4g2026_print_log.md`

**Owner:** Codex

- [ ] Extract every poster claim into a claim table with source path, source section, exact value, and permitted wording.
- [ ] Copy the exact proposal title, abstract, author, affiliation, license, and open-source stack into the claim table; affiliation is verified against the public Pretalx speaker record.
- [ ] Mark proposal requirements separately from analysis results so the poster does not introduce unsupported claims.
- [ ] Confirm the Visipri product-specific requirements before design: finished size, 3 mm bleed, trim marks, CMYK/RGB policy, accepted PDF version/PDF-X profile, file-size limit, font handling, and image-resolution guidance. Record the URL and confirmation date in `exp002_kitagi_foss4g2026_print_log.md`.
- [ ] Use the current public Visipri guidance as the initial baseline: A0 841 × 1189 mm, PDF input, CMYK preferred/required depending on product, 3 mm bleed for edge-to-edge artwork, and 300 dpi recommended. Treat the order-specific instructions as authoritative if they differ.
- [ ] Confirm the production workflow supports the required page size, bleed, color mode, and embedded fonts or outlined text in the final PDF.
- [ ] Confirm the chosen workflow can export a reduced PNG preview and preserve source/editability.
- [ ] Record the final workflow and required local commands in the content file.
- [ ] Use a standard Copernicus attribution such as `Contains modified Copernicus Sentinel data [2025]` or the exact wording required by the selected data/product guidance, and record the final wording in the content file.
- [x] Confirm the official listing: the 9/2 13:30–14:00 Himawari entry is the accepted poster session listing, not a separate talk. Confirm with the organizer only whether presenters are expected to be physically at Himawari during that slot in addition to the 13:00–15:00 poster core time. Session record: https://talks.osgeo.org/foss4g-2026/talk/GC3KYK/

**Exit check:** The content file contains no unresolved numeric claims, no unspecified figure source, and one selected source/export workflow.

### Task 2: Approve the poster information architecture and visual design

**Files:**
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md`

**Owner:** Codex

Recommended single-page structure:

- Header: title, subtitle, author, affiliation, FOSS4G Hiroshima 2026, and a one-sentence takeaway.
- Left column: heritage context, research question, study area map, and data source.
- Center column: Sentinel-2 workflow diagram, NDWI/MNDWI/NDVI formulas or concise definitions, and seasonal comparison.
- Right column: main results map, 113 vs 145 comparison, historical-quarry correspondence, limitations, and future work.
- Footer: conclusion, references, open-source stack, data/software attribution, CC BY 4.0, and QR/link to the repository or report.

- [ ] Set a clear visual priority: the result map and 113/145 seasonal result are dominant; formulas and implementation details are secondary.
- [ ] Limit body copy to short English paragraphs and bullets readable at poster viewing distance.
- [ ] Use a consistent legend for water polygons, land, vegetation, and historical quarry context.
- [ ] Define color and grayscale-safe variants before production.
- [ ] Specify exact figure placements, captions, required source credits, and approximate physical sizes in millimeters.
- [ ] Set typography thresholds: title at least 72 pt, body text at least 24 pt, and captions/credits at least 18 pt unless a Codex review explicitly approves an exception.
- [ ] Specify the final title and takeaway wording without overclaiming quarry identification.
- [ ] Record the Task 1–2 design approval or rejection in an Issue #6 comment before Claude starts Task 3.

**Exit check:** Claude can produce the poster without deciding the research story, numerical values, or figure order.

### Task 3: Produce the first poster draft

**Files:**
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg`
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf`
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_preview.png`
- Modify if needed: `scripts/` figure-generation scripts only

**Owner:** Claude

- [ ] Implement the approved A0 portrait layout in the selected vector-first workflow.
- [ ] Regenerate the three main raster figures at sufficient source resolution before layout. At their final physical display size, require at least 150 effective dpi and target 200 dpi or higher; use approximately 300 dpi source output where practical. Existing low-resolution files must not be enlarged without regeneration.
- [ ] Use tracked figures from `docs/results/exp002/` or regenerate them reproducibly into that directory.
- [ ] Add English captions and source credits for every map, image, and chart.
- [ ] Add the accepted title and author information exactly as submitted.
- [ ] Export the PDF at A0 portrait dimensions and generate the review PNG.
- [ ] Record the generation command, tool versions, fonts, and any manual steps in a production note or the content file.
- [ ] Generate the review PNG with a long edge of approximately 4,000 px so that text and clipping remain reviewable.

**Exit check:** The source, PDF, and preview exist, are mutually consistent, and the PDF opens without missing fonts or linked assets.

### Task 4: Run first Codex content and scientific review

**Files:**
- Review: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md`
- Review: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg`
- Review: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf`

**Owner:** Codex

- [ ] Compare title, abstract claims, methods, thresholds, dates, polygon counts, area threshold, and limitations against the report and proposal.
- [ ] Check that “quarry pond remnants” is not presented as individually verified for all 145 polygons.
- [ ] Check NDWI/MNDWI/NDVI terminology, formulas, units, dates, and Sentinel-2 resolution.
- [ ] Check the 2025-03-23 and 2025-08-02 imagery dates, the contextual 127 quarry sites, Microsoft Planetary Computer STAC API, the complete named software stack, and the Seto Inland Sea transferability statement.
- [ ] Check that all citations and data/software attributions are present and readable.
- [ ] Check the visual narrative at full size and at a reduced viewing scale.
- [ ] Record findings as blocking, major, or minor review comments in Issue #6.

**Exit check:** Every blocking or major finding has a precise file/location and an unambiguous correction.

### Task 5: Revise and technically validate the poster

**Files:**
- Modify: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg`
- Regenerate: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf`
- Regenerate: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_preview.png`
- Create if needed: `docs/posters/validate_exp002_kitagi_quarry_foss4g2026_poster.py`

**Owner:** Claude, then Codex

- [ ] Apply all blocking and major review corrections.
- [ ] Validate exact PDF page size: 841 × 1189 mm, portrait, one page.
- [ ] Validate required text: exact title, author, affiliation, Sentinel-2, Microsoft Planetary Computer STAC API, NDWI, MNDWI, NDVI, 113, 145, 127, GeoJSON, GeoTIFF, rasterio, numpy, shapely, pystac-client, planetary-computer, folium, Seto Inland Sea, and CC BY 4.0.
- [ ] Validate that all raster assets meet at least 150 effective dpi at their physical display size, target 200 dpi or higher, and document any approved exception.
- [ ] Validate no text, legend, QR code, caption, or figure is clipped at the page edge.
- [ ] Validate fonts, special characters, color profile/export settings, and PDF opening in at least two viewers if available.
- [ ] Have Codex re-review the regenerated PDF and mark the artifact approved or return one final correction round.
- [ ] Record the final PDF approval, or the exact remaining blockers, in an Issue #6 comment before Task 6 begins.

**Exit check:** Codex explicitly approves the exact PDF that will be submitted to Visipri.

### Task 6: Confirm Visipri order and production logistics

**Files:**
- Update: `docs/posters/exp002_kitagi_foss4g2026_print_log.md`

**Owner:** User, with Codex support

- [ ] Confirm Visipri A0 portrait product, paper type, finish, color mode, bleed/margin requirements, and delivery estimate.
- [ ] Treat the requirements already confirmed in Task 1 as the design baseline; only resolve order-specific differences here.
- [ ] Select a delivery date that leaves time for inspection before September 1, 09:00.
- [ ] Confirm shipping address, quantity, cost, and whether proofing is available.
- [ ] Upload only the Codex-approved PDF.
- [ ] Record order number, selected specifications, expected delivery date, and inspection result without recording payment secrets.

**Exit check:** The physical poster is delivered and matches the approved PDF; any print defect is recorded and escalated before the conference.

### Task 7: Mount, present, and remove the poster

**Files:**
- Update: `docs/posters/exp002_kitagi_foss4g2026_print_log.md`
- Update: Issue #6 checklist and final comment

**Owner:** User

- [ ] Carry the poster and mounting pins to the venue.
- [ ] Mount it in the Sakura Lounge after September 1, 09:00.
- [ ] Be present during September 2, 13:00–15:00 core time.
- [ ] Confirm the organizer's attendance expectation for the Himawari 13:30–14:00 poster listing. If physical attendance there is required in addition to poster core time, record the practical coverage arrangement in Issue #6.
- [ ] Prepare a short spoken explanation and answers for method, thresholds, seasonal difference, false positives, and field validation.
- [ ] Remove the poster by September 3, 18:30.
- [ ] Attach a completion note and close Issue #6 after all physical tasks are complete.

**Exit check:** Poster displayed, core-time interaction completed, poster removed on time, and the final state is documented in Issue #6.

## Review Checklist

- [ ] Proposal title and accepted scope are preserved.
- [ ] A0 portrait dimensions are exact.
- [ ] English-only copy is clear and concise.
- [ ] Main result is immediately visible from a distance.
- [ ] 113 spring and 145 summer polygons are not confused with confirmed quarry counts.
- [ ] Thresholds and imagery dates match the evidence source.
- [ ] Limitations include 10 m resolution, spectral mixing, and missing individual field validation.
- [ ] Sources, licenses, CC BY 4.0, and software names are legible.
- [ ] PDF is one page, fonts are safe, figures are sharp, and no content is clipped.
- [ ] Visipri order is based on the approved PDF.
- [ ] Display, core time, and removal logistics are recorded.

## Execution Handoff

After Codex approves Tasks 1–2, Claude should execute Task 3. Codex then performs Task 4 before any printing decision. Claude performs Task 5 revisions, and Codex gives the final PDF approval before Task 6. No print order should be placed before that approval.

## Target Schedule

These are internal target dates, not organizer deadlines. They leave time for one correction cycle and physical inspection before mounting.

- **2026-08-15:** Task 1 requirements, proposal record, print baseline, and Himawari/core-time clarification request complete.
- **2026-08-16:** Task 2 content contract and layout design approved by Codex; Claude handoff ready.
- **2026-08-20:** Task 3 first draft SVG/PDF/PNG complete.
- **2026-08-21:** Task 4 first Codex review complete and findings recorded in Issue #6.
- **2026-08-23:** Task 5 corrected PDF regenerated.
- **2026-08-24:** Codex final PDF approval complete.
- **2026-08-25:** Visipri order placed using the approved PDF.
- **2026-08-29:** Printed poster delivered, inspected, and any defect escalated.
- **2026-09-01 09:00 onward:** Poster mounted at Sakura Lounge.
- **2026-09-02 13:00–15:00:** Poster core time, subject to resolution of the Himawari overlap.
- **2026-09-03 18:30:** Poster removed.
