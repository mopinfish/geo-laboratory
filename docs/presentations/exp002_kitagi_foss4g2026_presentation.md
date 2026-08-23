# FOSS4G 2026 Hiroshima 口頭発表 内容契約 — 北木島丁場跡水域

本書は、2026年9月2日 13:30–14:00（Himawari、Regular Talk）で発表する英語スライドの**投影文字列と主張境界の正本**である。数値・主張は下記の権威資料に従い、逸脱する記述を投影面に置かない。スライド生成スクリプト・PPTX・スピーカーノートは本書と同期させる。

- 設計規約: `experiments-local-llm/docs/presentations/DESIGN_GUIDE.md`、`CONVENTIONS.md` に準拠
- 発表形式: Regular Talk 30分枠（**発表20分・質疑5分・入替5分**）／使用言語 英語
- 発話合計の目標: **19:30**（許容 18:30–20:00。実際の英語通し読みが最終ゲート）

## 権威資料（数値・主張の正本）

| 資料 | 役割 |
|---|---|
| `docs/reports/exp002_kitagi_quarry_water_detection_report.md` | 数値・考察・限界の一次情報 |
| `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md` | Codex承認済みの主張境界・確定値 |
| `docs/posters/exp002_kitagi_foss4g2026_proposal.md` | 採択アブストラクト（聴衆への約束） |
| `docs/results/exp002/exp002_osm_comparison.md` | OSM照合記録（取得日 2026-08-23） |
| `docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson` | 公開済み検出ポリゴン145件 |
| `docs/articles/2026_chiri-koryu-10/draft.md` | 現地訪問記（三スケールの枠組み・現地写真） |

## 中心メッセージ（聴衆が1つだけ持ち帰るもの）

> Open satellite data and open-source tools can give a heritage landscape its first island-wide inventory of quarry-pond candidates — and most of those candidates are not yet on any public map.

## 採択プロポーザルとの対応（約束の履行台帳）

| プロポーザルの約束 | 着地スライド |
|---|---|
| 島の歴史（17世紀初頭〜、1957年ピーク127丁場・人口1万2千人） | 2 |
| 2019年 日本遺産認定、島全体のインベントリが未整備 | 2 |
| Sentinel-2 L2A を Microsoft Planetary Computer STAC API 経由で取得 | 4 |
| NDWI・MNDWI による水域検出、NDVI マスク | 5 |
| 10 m でのスペクトル混合対策としての負の閾値（−0.2 / −0.1 / 0.3） | 5 |
| 春季（2025-03-23、雲量0.0%）・夏季（2025-08-02、雲量0.7%）の比較 | 10 |
| 春季113件（最大1.28 ha） | 10 |
| 夏季145件・4集中地帯・歴史記録と整合 | 6, 7 |
| NDVIマスクの除外は9ピクセルのみ | 10 |
| GeoJSON・GeoTIFF 出力、現地調査と遺産記録の基礎データ | 14 |
| OSS のみ（rasterio, numpy, shapely, pystac-client, planetary-computer, folium） | 14 |
| 瀬戸内の他の採石島への展開可能性 | 14 |
| テーマ: Humanitarian, ethical, and peacebuilding | 2, 9, 14 |

プロポーザルにない追加要素は3点のみで、いずれも独立した「結果」として提示しない。

1. 徒歩・上空で見えたもの（スライド3、11）— **なぜ衛星が必要か**の動機、および10 m解像度の限界を説明する枠組み
2. OSM照合（スライド8、9）— プロポーザルが約束した「歴史記録との対応」を、数の一致から**名前付き地点の対応**へ具体化する材料。精度検証としては提示しない
3. 8月31日の再訪写真（スライド12）— **現地検証が未実施であること**の次の一手。検証結果としては提示しない

## 主張境界（全スライド共通・ポスター内容契約から継承）

- 検出結果は water polygons / candidates と呼ぶ。`confirmed quarry ponds` を否定形以外で使わない
- 145件と127丁場の比較は**規模の比較**であり、1対1対応ではない
- 精度指標（適合率・再現率）は算出していない
- 春季113件は当時の報告値。実行設定が保存されておらず、差の原因は特定できていない
- OSM は正解データではない。一致は独立した傍証、不一致は「未登録」か「誤検出」
- 8月31日の写真は illustrative field photographs であり validation ではない
- `Contains modified Copernicus Sentinel data [2025].` と CC BY 4.0 をクロージングに明示

## タイミング

| スライド | 物語上の役割 | 時間 |
|---|---|---:|
| 1 | 表紙 | 0:40 |
| 2–3 | 課題と動機（島・遺産・現地で見えたもの） | 2:40 |
| 4–5 | 手法（データ・指数） | 3:10 |
| 6–7 | 主結果（145件・分布） | 3:20 |
| 8–9 | OSM照合（既知との一致・未登録の91件） | 2:40 |
| 10 | 季節差 | 1:30 |
| 11–12 | 三スケールの論旨・再訪 | 2:40 |
| 13–14 | 限界と次の一手・オープンデータと結び | 2:50 |
| **発話合計** | | **19:30** |

内訳（秒）: S1 40 / S2 80 / S3 80 / S4 80 / S5 110 / S6 110 / S7 90 / S8 80 / S9 80 / S10 90 / S11 80 / S12 80 / S13 90 / S14 80 = **1,170 秒**。

## Slide 1 — 1Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools

- **Central claim**: 採択タイトルの提示。
- **Projected body**: `Noboru Otsuka — Geolonia Inc.`; `FOSS4G 2026 Hiroshima`; `2026-09-02 13:30 · Himawari`.
- **Visual**: 桂林の岩壁写真（`fig03_keirin_cliff.jpg`）を右半分に配置。タイトルは左揃え。
- **Notes-only boundary**: 写真は現地で撮影した丁場跡であり、検出結果の図ではないと述べる。
- **Claim type**: Exact proposal title.
- **Duration**: 0:40
- **Evidence**: プロポーザル／Pretalx 掲載（`schedule.json` v0.27）。

## Slide 2 — 2A heritage island has no island-wide map of its own quarry ponds

- **Central claim**: 島の採石史と遺産認定に対して、丁場跡水域の島全体の記録が整備されていない。
- **Projected body**: `Kitagi Island · Kasaoka City, Okayama · Seto Inland Sea`; `Granite quarried since the early 17th century`; `127 active quarry sites at the 1957 peak · up to 12,000 residents`; `Abandoned pits filled with rain and groundwater`; `National heritage since 2019 — "Stone Islands of Setouchi"`; `As far as I could find, no island-wide inventory of these ponds has been published.`
- **Visual**: 位置図（`poster_f1_study_area.png`、英語ラベル）。
- **Notes-only boundary**: OSM には部分的な記録（37件）があることをノートで述べ、投影面では「島全体のインベントリがない」に限定する。
- **Claim type**: Historical context（文献・遺産記録）＋探索範囲を限定した gap statement。
- **Duration**: 1:20
- **Evidence**: 報告書 1.1、3.1／プロポーザル Description ¶1。
- **注記**: プロポーザル原文は "no systematic spatial inventory ... has been published" だが、網羅的探索の記録がないため投影面では "As far as I could find" を付す。

## Slide 3 — 3On the ground I could see fewer than ten of them

- **Central claim**: 徒歩と上空からの観察では島の一部しか捉えられない。だから島全体を一度に覆う手段が必要になる。
- **Projected body**: `March 2026 — I visited the island for a drone mapping party`; `On foot: five or six quarry sites`; `From the air: quarry-to-quarry boundaries left standing as thin rock walls`; `Neither view covers the whole island.`
- **Visual**: 写真2枚を同寸で並置 — 徒歩（`fig03_keirin_cliff.jpg`）、上空（`fig06_aerial_quarries.jpg`）。**固定寸法スロット**とし、差し替え可能にする。
- **Notes-only boundary**: 事業者間の境界が地形になっているという観察は現地での定性的観察であり、本研究の測定結果ではない。
- **Claim type**: Field observation（定性・動機づけ）。
- **Duration**: 1:20
- **Evidence**: `docs/articles/2026_chiri-koryu-10/draft.md` Ⅰ・Ⅱ章、写真は著者撮影。

## Slide 4 — 4One open satellite scene covers the whole island

- **Central claim**: 無償のSentinel-2 1シーンで島全体を10 mグリッドで覆える。
- **Projected body**: `Sentinel-2 L2A via the Microsoft Planetary Computer STAC API`; `Summer scene 2025-08-02 · 0.7% cloud`; `Spring scene 2025-03-23 · 0.0% cloud`; `10 m analysis grid — B02/B03/B04/B08 native; B11 (SWIR) resampled from 20 m`; `Minimum reported polygon area: 100 m²`; `No data purchase · no local archive`.
- **Visual**: 夏季トゥルーカラーと水域強調の並置（`poster_f5_truecolor_water.png`）。
- **Notes-only boundary**: 10 m は検出限界そのものであり、幅10 m未満の池は捉えられない（スライド13で再掲）。
- **Claim type**: Method（データ取得）。
- **Duration**: 1:20
- **Evidence**: 報告書 3.2、ポスター §3。

## Slide 5 — 5Water indices, with thresholds set low on purpose

- **Central claim**: 水域指数の和集合と負の閾値によって、スペクトル混合で値が下がる小規模水域を拾う。
- **Projected body**: `NDWI = (Green − NIR) / (Green + NIR)`; `MNDWI = (Green − SWIR) / (Green + SWIR)`; `NDVI = (NIR − Red) / (NIR + Red)`; `Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)`; `At 10 m a narrow pond is part water, part granite, part shadow — a textbook threshold of zero misses it.`
- **Visual**: 4パネル（NDWI / MNDWI / NDVI / 最終マスク、`poster_f4_index_panels.png`）。
- **Notes-only boundary**: 閾値はヒストグラムの谷から決めた値であり、最適化・感度分析・現地検証はしていない。MNDWI −0.1 には独立した文書化根拠がない。
- **Claim type**: Method（判定条件）。
- **Duration**: 1:50
- **Evidence**: 報告書 3.3、3.4、4.2（図4-2 ヒストグラム）、ポスター §4。

## Slide 6 — 6Summer imagery detected 145 intra-island water polygons

- **Central claim**: 夏季シーンから島内145件の水域ポリゴン（100 m²以上）を検出した。
- **Projected body**: 大きな数値 `145`; `intra-island water polygons ≥ 100 m², summer 2025-08-02`; `These are detected water polygons, not individually field-confirmed quarry ponds.`; `Natural ponds, reservoirs and shadows may remain.`; `Contains modified Copernicus Sentinel data [2025].`
- **Visual**: 検出分布図（`poster_f3_summer_map.png`）。
- **Notes-only boundary**: 145は検出数であり丁場数ではない。
- **Claim type**: Direct result。
- **Duration**: 1:50
- **Evidence**: 報告書 4.2（表4-2）、ポスター §5。

## Slide 7 — 7The detections cluster where the island was quarried

- **Central claim**: 検出は北部・南東部・中央部・西部の4か所に集中し、採石の歴史的中心と整合する。
- **Projected body**: `North · South-east · Centre · West`; `Largest detection 7,826 m² (north)`; `A pattern consistent with historical quarrying records`; `145 detections vs 127 recorded quarry sites — a comparison of scale, not a one-to-one match.`
- **Visual**: 4集中地帯を注記した検出分布図（**新規図版**: F3 に集中地帯のラベルを追加）。
- **Notes-only boundary**: 個別のポリゴンを特定の丁場に結びつけてはいない（スライド8で名前付き地点の対応を扱う）。
- **Claim type**: Direct result（分布）＋ contextual comparison（127）。
- **Duration**: 1:30
- **Evidence**: 報告書 4.3、5.1（仮説2は部分的支持）、ポスター §6。

## Slide 8 — 8Named quarry sites in OpenStreetMap sit within 3 to 39 m of a detection

- **Central claim**: OSM に登録済みの名前付き丁場跡・採石場は、いずれも検出ポリゴンの近傍にある。
- **Projected body**: `OpenStreetMap · retrieved 2026-08-23`; 表 `Hanamoto quarry 3 m`, `Tsuruta quarry 6 m`, `Murakami quarry 9 m`, `Imaoka quarry — "Kitagi no Keirin" 37 m`; `Eight named quarry sites, all within 3–39 m of a detection`; `30 of 37 OSM water/quarry features have a detection within 100 m.`; `OSM is community-contributed data, not ground truth.`
- **表記の注意**: 投影する社名のローマ字は読みが確定できるものに限る（今岡=Imaoka、鶴田=Tsuruta、村上=Murakami、花本=Hanamoto）。読みが一意でない「馬越」「竹本」は社名を出さず件数で述べる。8月31日の再訪で地元の方に読みを確認できれば追加する。
- **Visual**: 検出ポリゴン（青）と OSM 地物（黒の点）を重ねた地図（**新規図版**）。
- **Notes-only boundary**: 一致は独立した傍証であり精度検証ではない。適合率・再現率は未算出。桂林の同定は現地GPS確認待ち。
- **Claim type**: Cross-check against an open dataset。
- **Duration**: 1:20
- **Evidence**: `docs/results/exp002/exp002_osm_comparison.md`、報告書 5.3。

## Slide 9 — 9Ninety-one of the 145 are not yet on the map

- **Central claim**: 検出のうち大半は既存のオープンデータに対応地物がなく、それが次に確かめるべき候補集合になる。
- **Projected body**: 大きな数値 `91 / 145`; `no OpenStreetMap water or quarry feature within 100 m`; `Either not yet mapped, or a false positive — fieldwork decides which.`; `This is the candidate list, not a discovery claim.`
- **Visual**: スライド8と同じ地図で、対応地物のない91件を強調（**新規図版**、同一の視覚言語）。
- **Notes-only boundary**: 「未登録」と「誤検出」を切り分ける手段は現地検証のみ。数値は2026-08-23時点のOSM状態に依存する。
- **Claim type**: Cross-check result（候補集合の提示）。
- **Duration**: 1:20
- **Evidence**: `exp002_osm_comparison.md`。

## Slide 10 — 10Season changes which ponds are detectable

- **Central claim**: 2時期の比較では、春季は大型水域、夏季は小規模水域の検出に強い。両者は入れ替え可能な観測ではない。
- **Projected body**: `Spring 2025-03-23 — 113 polygons · largest 1.28 ha`; `Summer 2025-08-02 — 145 polygons · largest 7,826 m²`; `Spring count: 113 reported polygons; the exact historical run configuration is not preserved, and the source of the difference has not been isolated.`; `The summer NDVI mask excluded only 9 pixels.`
- **Visual**: 数値タイル2枚（113 / 145）。ポスターと同じ視覚言語。
- **Notes-only boundary**: 現行パイプラインでの春季再計算は180。夏季145と9pxは完全再現可能。NDVIマスクが効かなかったのは仮説の棄却であり失敗ではない。
- **Claim type**: Direct result（季節差）＋ reproducibility limitation。
- **Duration**: 1:30
- **Evidence**: 報告書 4.1（再現性追記）、4.4（表4-4）、5.1（仮説3は棄却）、ポスター §5・§6。

## Slide 11 — 11Each scale shows what the others cannot — and I have stood at fewer than five percent of them

- **Central claim**: 徒歩は質感、上空は境界、衛星は分布を可視化する。衛星が示した145件のうち、著者が現地で確かめたのは5%未満である。
- **Projected body**: `On foot — texture: the cut face, the water, the depth`; `From the air — boundaries: property lines standing as rock walls`; `From orbit — distribution: 145 candidates across the island`; `I have stood beside fewer than 5% of them.`
- **Visual**: 三スケール合成図（`fig09_multiscale.png`）。
- **Notes-only boundary**: 5%未満は徒歩で訪れた5〜6か所を145で割った概算であり、精度指標ではない。
- **Claim type**: Framing（論旨）＋ acknowledged gap。
- **Duration**: 1:20
- **Evidence**: 訪問記 Ⅲ-3、`fig09_multiscale.png`。

## Slide 12 — 12Two days ago I went back to the island

- **Central claim**: 衛星が指し示した地点へ実際に戻った。これは検証の第一歩であって検証結果ではない。
- **Projected body**: `2026-08-31 — return visit`; `Photographed candidate ponds selected from the published GeoJSON`; `Illustrative field photographs — not accuracy validation`; `Next: match each polygon against a known quarry location and compute precision and recall.`
- **Visual**: 8月31日の写真 2〜3枚（**固定寸法スロット**。撮影後に画像を差し替えるだけで完成する構造）。撮影対象は公開GeoJSONから事前に選定した候補地点。
- **Notes-only boundary**: 写真は候補地点の存在を示すのみ。丁場跡であることの同定や精度評価は行っていない。
- **Claim type**: Field photographs（illustrative）。
- **Duration**: 1:20
- **Evidence**: 撮影記録（撮影後に `_verification.md` へ座標・撮影時刻を記載）。

## Slide 13 — 13What these polygons can and cannot support

- **Central claim**: 10 m解像度・負の閾値・海域分離・精度指標の不在という限界の内側でのみ使える。
- **Projected body**: `10 m resolution — ponds narrower than about 10 m are unreliable`; `Negative thresholds add false positives from dark rock and shadow`; `No strict coastline mask — shoreline polygons may include seawater`; `No precision or recall — field validation not done`; 実例 `A 100 m² detection sits 18 m from a mapped water reservoir.`; `Next: land mask · field campaign · higher-resolution imagery`.
- **Visual**: テキスト中心。誤検出例の位置を示す小さな地図片（**新規図版・任意**）。
- **Notes-only boundary**: ため池の例はOSM照合で見つかったもので、誤検出と断定はしていない。
- **Claim type**: Limitations。
- **Duration**: 1:30
- **Evidence**: 報告書 5.4、6.3、`exp002_osm_comparison.md`、ポスター §6。
- **注記**: プロポーザルは "This poster presents..." と書かれているが、採択形式は口頭発表である。投影面で "poster" を使わない。

## Slide 14 — 14The polygons are now open data

- **Central claim**: 145件を公開データとして出したので、他の島でも同じ手順を再実行できる。産業が作った景観をオープンデータ上で見えるようにする、その一歩である。
- **Projected body**: `145 detected polygons published as GeoJSON · EPSG:4326`; `GeoJSON and GeoTIFF exported for fieldwork and heritage documentation`; `rasterio · numpy · shapely · pystac-client · planetary-computer · folium`; `The same workflow could be extended to other quarried islands in the Seto Inland Sea.`; `Contains modified Copernicus Sentinel data [2025]. Basemaps: GSI Tiles, Geospatial Information Authority of Japan. CC BY 4.0.`; `github.com/mopinfish/geo-laboratory` + QR; `Thank you · Q&A`.
- **Visual**: QRコード（`poster_qr_repo.png`）と最小限のテキスト。
- **Notes-only boundary**: GeoTIFF はパイプラインの出力仕様で、公開しているのはGeoJSON。閾値は他島へそのまま持ち込めない。
- **Claim type**: Reuse and transferability（提案）。
- **Duration**: 1:20
- **Evidence**: 報告書 3.5、6.2、6.3、公開GeoJSONとREADME、ポスター §7・フッター。

## 新規に必要な図版

| ID | 内容 | 生成元 |
|---|---|---|
| P7 | 4集中地帯を注記した検出分布図 | `scripts/generate_exp002_poster_figures.py` の F3 に注記を追加した派生 |
| P8 | 検出ポリゴン + OSM地物の重畳図 | 公開GeoJSON + `exp002_osm_water_features.json` |
| P9 | P8 と同一視覚言語で、OSM対応のない91件を強調 | 同上 |
| P13 | 誤検出例（貯水槽近傍）の拡大片（任意） | 同上 |
| S3・S12 | 写真スロット（固定寸法） | 訪問記の写真、8月31日撮影分 |

## 8月31日の撮影に向けた事前準備

公開GeoJSONから撮影対象リスト（座標・面積・島内位置・OSM対応の有無）を生成し、渡航前に渡す。優先度は次の順とする。

1. 検出最大ポリゴン（7,826 m²、北部）— OSM の「北木の桂林」との同定をGPSで確認する
2. OSM に対応地物のない91件のうち、面積上位で北部の徒歩到達可能なもの
3. 貯水槽近傍の100 m²検出 — 誤検出例の裏取り

## 成果物

| ファイル | 役割 |
|---|---|
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.md` | 本書（内容契約・正本） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.py` | python-pptx 生成スクリプト（正本） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.pptx` | 生成物（手編集しない） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation_speaker_notes.md` | スピーカーノート（英日併記、pptxのノートペインにも書き込む） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation_verification.md` | 照合記録（数値・出典・写真の座標） |
| `docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py` | 機械検査（投影文字列・数値・禁止表現・スライド数） |
| `docs/presentations/images/` | スライド用画像 |
