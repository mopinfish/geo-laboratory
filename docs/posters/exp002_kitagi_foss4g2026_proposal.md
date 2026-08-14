# Accepted Proposal: FOSS4G Hiroshima 2026

## Submission metadata

- **Title:** Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools
- **Author:** Noboru Otsuka
- **Affiliation:** Geolonia Inc.
- **Presentation listing:** 2026-09-02 13:30–14:00, Himawari
- **Contribution license:** CC BY 4.0

## Abstract

This study applies Sentinel-2 satellite imagery and open-source Python tools
to detect and map quarry pond remnants on Kitagi Island, a designated heritage
site in Japan's Seto Inland Sea, revealing spatial distributions consistent with
the island's historical quarrying records.

Kitagi Island (Kitagi-shima), located in Kasaoka City, Okayama Prefecture,
Japan, has been a center of granite quarrying since the early 17th century.
At its peak in 1957, the island hosted 127 active quarry sites (called "dojo")
with a population of up to 12,000 people. As the quarrying industry declined,
the abandoned sites filled with rainwater and groundwater, forming isolated
ponds enclosed by steep granite walls. In 2019, the island's stone culture was
designated as part of Japan's national heritage under the "Stone Islands of
Setouchi" program. Despite their heritage significance, no systematic spatial
inventory of these quarry pond remnants has been published.

This study applies Sentinel-2 L2A satellite imagery—retrieved via the
Microsoft Planetary Computer STAC API—to detect and map water bodies on
Kitagi Island using NDWI (Normalized Difference Water Index) and MNDWI
(Modified NDWI). To improve detection of small water bodies subject to
spectral mixing at 10 m resolution, we used a composite union condition
(NDWI > −0.2 OR MNDWI > −0.1) combined with an NDVI-based vegetation mask.
We compared spring imagery (March 2025, 0.0% cloud cover) and summer imagery
(August 2025, 0.7% cloud cover) to characterize seasonal detection differences.

Spring imagery detected 113 intra-island water polygons (≥100 m²) with a
maximum area of 1.28 ha. Summer imagery detected 145 polygons, with spatial
concentrations in the northern, southeastern, central, and western parts of
the island—a distribution consistent with historical records of quarry
locations. The NDVI vegetation mask contributed minimally to exclusion
(9 pixels), suggesting that quarry ponds and vegetation zones do not
substantially overlap in this granite-dominated landscape.

Results are exported as GeoJSON and GeoTIFF for use as base data in future
fieldwork and heritage documentation. The analysis pipeline uses exclusively
open-source Python libraries: rasterio, numpy, shapely, pystac-client,
planetary-computer, and folium.

This poster presents the methodology, detection results, and their
correspondence with the island's quarrying history, and discusses the
potential for extending the approach to other quarried islands in the
Seto Inland Sea.

## Reference material specified by the proposal

- Japan Heritage Story: [Islands of stone](https://stone-islands.jp/en/story/)
- Open-source projects/data: Sentinel-2 (ESA Copernicus), Microsoft Planetary Computer STAC API, rasterio, numpy, shapely, pystac-client, folium, and GeoJSON.
- License statement: The conference contribution (abstract, proceedings text, presentation materials, video recording, and live transmission) is available under CC BY 4.0.

## Verification note

This file records the proposal text supplied by the presenter for poster planning. The author affiliation was verified against the public Pretalx speaker record.
