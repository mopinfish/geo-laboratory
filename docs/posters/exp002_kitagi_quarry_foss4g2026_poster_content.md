# FOSS4G Hiroshima 2026 Poster Content Contract

## Artifact

- **Title:** Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools
- **Author:** Noboru Otsuka
- **Affiliation:** Geolonia Inc.
- **Event:** FOSS4G Hiroshima 2026
- **Accepted listing:** September 2, 2026, 13:30–14:00, Himawari; Pretalx record: https://talks.osgeo.org/foss4g-2026/talk/GC3KYK/
- **Poster format:** English only, A0 portrait, finished size 841 × 1189 mm.
- **License:** CC BY 4.0.

This file is the content and evidence contract for the poster. Claude may edit wording for visual fit, but must not change a locked value, method, date, scope statement, or limitation without a new Codex review.

## One-sentence takeaway

Open-source Sentinel-2 processing revealed 113 spring and 145 summer intra-island water polygons on Kitagi Island; their distribution is consistent with historical quarrying patterns, while individual quarry-pond identities still require field validation.

## Required poster sections and copy

### 1. Background

Kitagi Island (Kitagi-shima), in Kasaoka City, Okayama Prefecture, is a granite-quarrying island in Japan's Seto Inland Sea. Quarrying has a history extending to the early seventeenth century. At its 1957 peak, historical records report 127 active quarry sites, called *dojo*. After quarrying declined, many abandoned excavations filled with rainwater or groundwater, forming isolated ponds enclosed by steep granite walls. The island's stone culture became part of Japan's national heritage in 2019 under the “Stone Islands of Setouchi” program.

### 2. Research question

Can open satellite imagery and reproducible open-source tools map water bodies associated with former quarry sites, and do their spatial patterns correspond to the island's quarrying history?

### 3. Data and study area

- Study area: Kitagi Island, Kasaoka City, Okayama Prefecture, Japan.
- Imagery: Sentinel-2 L2A, accessed through the Microsoft Planetary Computer STAC API.
- Spring scene date: 2025-03-23; reported cloud cover: 0.0%.
- Summer scene date: 2025-08-02; reported cloud cover: 0.7%.
- Spatial resolution: 10 m for the principal visible and near-infrared bands; mixed pixels limit detection of very small water bodies.
- Minimum reported polygon area: 100 m².

### 4. Method

Use a compact four-step diagram:

`Sentinel-2 L2A → STAC search and band access → NDWI + MNDWI union → NDVI mask and polygon extraction`

Indices:

```text
NDWI  = (Green − NIR)  / (Green + NIR)
MNDWI = (Green − SWIR) / (Green + SWIR)
NDVI  = (NIR − Red)    / (NIR + Red)
```

Composite water condition:

```text
(NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)
```

Explain in one sentence: the union condition favors sensitivity to small water bodies affected by spectral mixing, while the NDVI mask excludes vegetation-like pixels.

### 5. Results

Make the seasonal comparison the dominant quantitative element:

| Scene | Date | Intra-island water polygons ≥100 m² |
|---|---:|---:|
| Spring | 2025-03-23 | **113** |
| Summer | 2025-08-02 | **145** |

Required result wording:

“Summer imagery detected 145 intra-island water polygons. The detections were concentrated in northern, southeastern, central, and western parts of the island, a pattern consistent with historical quarrying records.”

Required caution directly beside the result:

“These are detected water polygons, not individually field-confirmed quarry ponds. Natural ponds, reservoirs, shadows, and other false positives may remain.”

Additional locked result:

“The summer NDVI mask excluded only 9 pixels, indicating limited overlap between the detected water candidates and vegetation zones in this granite-dominated landscape.”

### 6. Interpretation and limitations

- The number and spatial distribution of detected water polygons are consistent with the historical quarrying context, but the 145-to-127 comparison is a scale comparison, not an individual one-to-one match.
- Sentinel-2's 10 m resolution creates spectral mixing for narrow or small ponds.
- Negative index thresholds improve sensitivity but can increase false detections from dark rock, shadows, or other surfaces.
- Individual quarry-pond identity and accuracy metrics require field validation against known quarry locations.
- Seasonal imagery changes which water bodies are most detectable; spring and summer results should not be treated as interchangeable observations.

### 7. Reproducibility and reuse

Results are exported as GeoJSON and GeoTIFF for future fieldwork and heritage documentation. The workflow uses open-source Python libraries: rasterio, numpy, shapely, pystac-client, planetary-computer, and folium. The approach could be extended to other quarried islands in the Seto Inland Sea.

### 8. Closing statement

“A lightweight, reproducible workflow can provide a first spatial inventory of quarry-pond candidates and a practical base layer for field validation and heritage documentation.”

## Figure inventory and placement contract

All figures must be regenerated or exported at sufficient resolution before final layout. Do not enlarge the existing low-resolution files as the final production method.

| ID | Figure | Source | Placement | Required caption/credit |
|---|---|---|---|---|
| F1 | Kitagi Island location/study-area map | New English map generated from the existing Kitagi extent constants and map-generation logic in `scripts/build_chiri_koryu_figures.py` | Left column, 210 × 150 mm target | “Study area: Kitagi Island, Kasaoka City, Okayama Prefecture.” Credit basemap/data sources used. |
| F2 | Processing workflow | New vector diagram | Center column, 250 × 115 mm target | No external image credit; label Sentinel-2, STAC, indices, mask, polygons. |
| F3 | Seasonal result comparison | Regenerated chart/map using report values | Right/center dominant panel, 300 × 220 mm target | “Detected intra-island water polygons ≥100 m²: 113 in spring, 145 in summer.” |
| F4 | Summer index/mask panels | `docs/results/exp002/exp002_ndwi_static.png`, regenerated at print resolution | Center column, 250 × 220 mm target | Identify NDWI, MNDWI, NDVI, and final water mask; cite Sentinel-2 date. |
| F5 | Water-highlighted context image | `docs/results/exp002/exp002_geotiff_preview.png`, regenerated at print resolution | Right column, 300 × 150 mm target | “Detected water candidates highlighted in blue; not individual quarry validation.” |
| F6 | Field photograph | `docs/results/exp002/photos/choba_lake_*.jpg` | Left column, optional 210 × 120 mm | Credit: Noboru Otsuka, if used; use only photographs with known permission/provenance. |

F1/F3/F5 may be consolidated if the regenerated figures provide a clearer result story. The result map and 113/145 comparison must remain visually dominant.

## Selected production workflow

- Claude edits the poster as an editable, one-page SVG in A0 portrait dimensions, using this content contract as the copy and layout authority.
- Claude regenerates raster figures from repository scripts or source data at the required effective resolution; existing low-resolution previews are not enlarged for final output.
- Export the SVG to a one-page PDF while preserving the 841 × 1189 mm page size, the agreed 3 mm bleed treatment, and embedded or outlined fonts. Export the review PNG from the same SVG/PDF source with a long edge of approximately 4,000 px.
- Before final PDF approval, record the actual export tool, command, PDF version/profile, color mode, font handling, and output dimensions in Issue #6 and the print log. Order-specific Visipri instructions override this baseline if they differ.

## Layout and typography contract

### Canvas

- Finished page: 841 × 1189 mm, portrait.
- If edge-to-edge artwork is used, add 3 mm bleed on all sides according to the preliminary Visipri guide; keep all essential content at least 15 mm inside the trim edge until product-specific instructions are confirmed.
- Use a three-column grid with 18 mm outer margins and 12 mm gutters. Approximate usable width: 785 mm; column widths: 245 / 245 / 245 mm.
- Reserve the bottom 95 mm for references, attribution, license, QR code, and contact information.

### Type scale

- Title: 72–96 pt.
- Section headings: 36–44 pt.
- Body text and bullets: 24–28 pt.
- Figure captions and credits: 18–20 pt.
- Do not reduce below 18 pt without an explicit Codex review exception.

### Visual language

- Use a restrained granite/sea palette: charcoal text, warm stone neutrals, deep blue water, and one vegetation green.
- Ensure water, vegetation, and land remain distinguishable in grayscale or low-saturation printing.
- Use large numeric callouts for **113**, **145**, **10 m**, and **127 historical quarry sites**.
- Do not use decorative satellite imagery that competes with the result map.

## Attribution and references

Required footer text or equivalent:

“Contains modified Copernicus Sentinel data [2025]. Sentinel-2 L2A data accessed through Microsoft Planetary Computer STAC API. Analysis uses rasterio, numpy, shapely, pystac-client, planetary-computer, and folium. Conference contribution licensed CC BY 4.0.”

References to include in compact form:

- McFeeters, S. K. (1996). The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features. *International Journal of Remote Sensing*, 17(7), 1425–1432.
- Xu, H. (2006). Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery. *International Journal of Remote Sensing*, 27(14), 3025–3033.
- Du, Y. et al. (2016). Water bodies' mapping from Sentinel-2 imagery with Modified Normalized Difference Water Index at 10-m spatial resolution. *Remote Sensing*, 8(4), 354.
- Japan Heritage Story: “Islands of stone,” https://stone-islands.jp/en/story/

## Acceptance checks for Claude's first draft

- [ ] Exact title, author, and affiliation are present.
- [ ] All locked values appear with the approved meaning: 113, 145, 127, 9 pixels, 100 m², 10 m, 2025-03-23, 2025-08-02, −0.2, −0.1, and 0.3.
- [ ] The method names and all required software/data names are present.
- [ ] The poster explicitly distinguishes detected water polygons from field-confirmed quarry ponds.
- [ ] The poster includes GeoJSON, GeoTIFF, CC BY 4.0, Copernicus/Sentinel attribution, and the three references.
- [ ] Main result figures are not sourced from untracked `tmp/` files.
- [ ] Layout follows A0 portrait, three-column grid, 72/36/24/18 pt type thresholds, and the reserved footer area.
- [ ] Claude records the source format, export commands, font handling, figure dimensions, and any deviations in Issue #6.
