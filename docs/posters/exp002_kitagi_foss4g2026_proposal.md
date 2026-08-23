# Accepted Proposal: FOSS4G Hiroshima 2026

## Submission metadata

- **Title:** Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools
- **Author:** Noboru Otsuka
- **Affiliation:** Geolonia Inc.
- **Presentation listing:** 2026-09-02 13:30–14:00, Himawari
- **Registered session type (official schedule):** `General session talk`, 30 minutes — **not** the poster listing
- **Contribution license:** CC BY 4.0

## 発表形式（2026-08-23 確定）

**本採択は口頭発表（General Track）である。ポスター発表ではない。**

- **日時・会場: 2026-09-02 13:30–14:00、Himawari、30分**
- **使用言語: 英語**（採択通知に "presentations are expected to be delivered in English"）
- 登録種別（公式スケジュール `schedule.json` v0.27）: `General session talk`

### 根拠（主催者からのメール3通）

1. **採択通知**: "We are pleased to inform you that your proposal ... has been **accepted for the General Track** of FOSS4G 2026 general tracks."
   - "Your presentation has been selected based on the community vote and review by the Program Committee"
   - "To ensure smooth communication, presentations are expected to be delivered in **English**."
   - ポスターへの言及はない
2. **スケジュール通知（初回）**: 「あなたの**講演** ... は Conference Management **Room4** の 09/02, **11:00** で行われます」
3. **スケジュール通知（変更）**: 「あなたの**講演** ... は **Himawari** の 09/02, **13:30** に移動しました」

### 公式スケジュールで確認した事実（2026-08-23、`https://talks.osgeo.org/foss4g-2026/schedule/export/schedule.json` v0.27）

- 本発表（`GC3KYK`）は `type = "General session talk"`、9/2 13:30–14:00、Himawari、30分
- 9/2 の Himawari は30分の `General session talk` が連続する通常のトーク部屋（13:30 Otsuka → 14:00 Andal → 16:00 Nishio → 16:30 Matsumura → 17:00 Annoura → 17:30 Woodcock）
- `type = "Poster"` は2件のみで、いずれも個別発表ではない（Sakura 9/2 13:00 から2時間の `Poster and Demonstration Presentations`、および Phoenix Hall Lobby 15:30 の高校生ポスター）。**個別のポスターは Pretalx に掲載されていない**
- Pretalx の公開セッションページにはセッション種別の表示がない（表示は日時と会場のみ）

### 経緯の記録

投稿時のアブストラクト本文は "This poster presents the methodology..." とポスター前提で書かれており、Issue #6 の Task 1 では「Himawari 13:30–14:00 はポスターセッションの掲載枠であり別トークではない」と結論していた。**この結論は誤りであった。**

この誤認に基づき、A0ポスター（`exp002_kitagi_quarry_foss4g2026_poster.pdf` ほか）と当日資料（口頭スクリプト・想定問答集）を制作した。ポスターは採択形式ではないため掲出物としては使用しない。**ビジプリへの印刷発注は中止する。**

制作物のうち、口頭発表へ転用できるもの:

- `docs/reports/exp002_kitagi_quarry_water_detection_report.md` — 数値・考察の正本（変更なし）
- `docs/posters/figures/exp002/` — 300dpi相当の図版（スライドへ流用可）
- `docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson` — 公開済み成果データ（変更なし）
- `docs/posters/exp002_kitagi_foss4g2026_talk_script.md` — 30秒/2〜3分/5分版。30分版の骨格として再構成が必要
- `docs/posters/exp002_kitagi_foss4g2026_qa.md` — 33問。発表後の質疑にそのまま使用可
- `docs/presentations/exp002_kitagi_quarry_water_detection_presentation.pptx` — 既存の日本語13枚。英語化と30分尺への拡張が必要

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
