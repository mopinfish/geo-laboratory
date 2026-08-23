# Accepted Proposal: FOSS4G Hiroshima 2026

## Submission metadata

- **Title:** Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools
- **Author:** Noboru Otsuka
- **Affiliation:** Geolonia Inc.
- **Presentation listing:** 2026-09-02 13:30–14:00, Himawari
- **Registered session type (official schedule):** `General session talk`, 30 minutes — **not** the poster listing
- **Contribution license:** CC BY 4.0

## 発表形式の未確定事項（2026-08-23 追記）

公式スケジュール（Pretalx schedule.json、version 0.27、`https://talks.osgeo.org/foss4g-2026/schedule/export/schedule.json`、確認日 2026-08-23）を確認した結果、**本採択が口頭発表かポスター発表かが未確定である**。

確認できた事実:

1. 本発表（`GC3KYK`）の登録は **`type = "General session talk"`、9月2日 13:30–14:00、会場 Himawari、30分**
2. **9月2日の Himawari は通常のトーク部屋**として運用されている。13:30 Otsuka → 14:00 Andal → 16:00 Nishio → 16:30 Matsumura → 17:00 Annoura → 17:30 Woodcock と、すべて30分の `General session talk` が連続する。本発表はこの列の中にある
3. スケジュールには **`type = "Poster"` が別に存在するが該当は2件のみ**で、いずれも個別発表ではない
   - Sakura、9月2日 13:00 から **2時間**、`Poster and Demonstration Presentations`（発表者名なし）
   - Phoenix Hall Lobby、9月2日 15:30、高校生ポスター発表
   - **個別のポスターは Pretalx に掲載されていない**
4. 公式ポスターセッション案内（`https://2026.foss4g.org/ja/program-schedule/poster-session/`）は、掲出 Sakura Lounge・9/1〜9/3、コアタイム 9/2 13:00–15:00、コアタイム中はポスター前に在席と記載。Himawari への言及はなく、ライトニングトーク等の記載もない

したがって、Issue #6 の Task 1 で記録した「Himawari 13:30–14:00 はポスターセッションの掲載枠であり別トークではない」という結論は**誤りである**。

未確定である点:

- 本採択が30分の口頭発表なのか、ポスター発表なのか、両方なのか
- 両方の場合、ポスターのコアタイム（13:00–15:00）と口頭発表（13:30–14:00）が重複するため、コアタイム中の30分不在の扱い

なお本アブストラクトの本文は "This poster presents the methodology..." とポスター前提で書かれている一方、プログラム上の登録種別は `General session talk` である。この食い違いは公開情報では解消できないため、主催者への確認が必要。

**確認が取れるまで、ビジプリへのポスター印刷発注は保留する。**

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
