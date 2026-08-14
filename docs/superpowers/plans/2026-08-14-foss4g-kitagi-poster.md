# FOSS4G Hiroshima 2026 Kitagi Island Poster Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create, review, print, and display an English A0 portrait poster for the accepted FOSS4G Hiroshima 2026 presentation about detecting quarry pond remnants on Kitagi Island.

**Architecture:** Treat the existing exp002 report and generated figures as the numerical and evidence source of truth. Create a dedicated poster source in an editable vector-first format, export a print-ready A0 PDF and a review PNG, then pass the artifact through a Codex content/print review before Claude revisions and Visipri submission.

**Tech Stack:** SVG (editable poster source), PDF export tool selected during Task 1, existing PNG/JPEG figures under `docs/results/exp002/`, Python/uv only when a figure or validation script must be regenerated, Visipri for printing.

## Global Constraints

- Poster language is English only.
- Poster size is A0 portrait: 841 × 1189 mm.
- The submitted PDF is the print source of truth; the editable source must remain in the repository.
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

## Deliverables and File Boundaries

- Create: `docs/superpowers/plans/2026-08-14-foss4g-kitagi-poster.md` — this implementation plan.
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg` — editable A0 portrait vector source, generated or maintained by Claude.
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf` — print-ready A0 PDF exported from the source.
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_preview.png` — reduced review preview; not used for printing.
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md` — English poster copy, source references, and claim-to-evidence mapping.
- Create: `docs/posters/validate_exp002_kitagi_quarry_foss4g2026_poster.py` — deterministic checks for page size, required text, output existence, and referenced assets, if the selected export workflow supports reliable validation.
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
- Create or update: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md`

**Owner:** Codex

- [ ] Extract every poster claim into a claim table with source path, source section, exact value, and permitted wording.
- [ ] Mark proposal requirements separately from analysis results so the poster does not introduce unsupported claims.
- [ ] Confirm the production workflow supports an exact A0 portrait page and embedded fonts or outlined text in the final PDF.
- [ ] Confirm the chosen workflow can export a reduced PNG preview and preserve source/editability.
- [ ] Record the final workflow and required local commands in the content file.

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
- [ ] Specify the final title and takeaway wording without overclaiming quarry identification.

**Exit check:** Claude can produce the poster without deciding the research story, numerical values, or figure order.

### Task 3: Produce the first poster draft

**Files:**
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg`
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf`
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_preview.png`
- Modify if needed: `scripts/` figure-generation scripts only

**Owner:** Claude

- [ ] Implement the approved A0 portrait layout in the selected vector-first workflow.
- [ ] Use tracked figures from `docs/results/exp002/` or regenerate them reproducibly into that directory.
- [ ] Add English captions and source credits for every map, image, and chart.
- [ ] Add the accepted title and author information exactly as submitted.
- [ ] Export the PDF at A0 portrait dimensions and generate the review PNG.
- [ ] Record the generation command, tool versions, fonts, and any manual steps in a production note or the content file.

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
- [ ] Validate required text: title, author, Sentinel-2, NDWI, MNDWI, NDVI, 113, 145, GeoJSON, GeoTIFF, CC BY 4.0.
- [ ] Validate that all raster assets meet the effective print-resolution target at their physical display size.
- [ ] Validate no text, legend, QR code, caption, or figure is clipped at the page edge.
- [ ] Validate fonts, special characters, color profile/export settings, and PDF opening in at least two viewers if available.
- [ ] Have Codex re-review the regenerated PDF and mark the artifact approved or return one final correction round.

**Exit check:** Codex explicitly approves the exact PDF that will be submitted to Visipri.

### Task 6: Confirm Visipri order and production logistics

**Files:**
- Create: `docs/posters/exp002_kitagi_quarry_foss4g2026_print_log.md`

**Owner:** User, with Codex support

- [ ] Confirm Visipri A0 portrait product, paper type, finish, color mode, bleed/margin requirements, and delivery estimate.
- [ ] Select a delivery date that leaves time for inspection before September 1, 09:00.
- [ ] Confirm shipping address, quantity, cost, and whether proofing is available.
- [ ] Upload only the Codex-approved PDF.
- [ ] Record order number, selected specifications, expected delivery date, and inspection result without recording payment secrets.

**Exit check:** The physical poster is delivered and matches the approved PDF; any print defect is recorded and escalated before the conference.

### Task 7: Mount, present, and remove the poster

**Files:**
- Update: `docs/posters/exp002_kitagi_quarry_foss4g2026_print_log.md`
- Update: Issue #6 checklist and final comment

**Owner:** User

- [ ] Carry the poster and mounting pins to the venue.
- [ ] Mount it in the Sakura Lounge after September 1, 09:00.
- [ ] Be present during September 2, 13:00–15:00 core time.
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
