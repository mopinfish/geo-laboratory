# FOSS4G 2026 Hiroshima 口頭発表 内容契約 — 北木島丁場跡水域

本書は、2026年9月2日 13:30–14:00（Himawari、Regular Talk）で発表する英語スライドの**投影文字列と主張境界の正本**である。数値・主張は下記の権威資料に従い、逸脱する記述を投影面に置かない。スライド生成スクリプト・PPTX・スピーカーノートは本書と同期させる。

- 設計規約: `experiments-local-llm/docs/presentations/DESIGN_GUIDE.md`、`CONVENTIONS.md` に準拠
- 発表形式: Regular Talk 30分枠（**発表20分・質疑5分・入替5分**）／使用言語 英語
- 発話合計の目標: **17:30**（20分枠に対しバッファ 2:30。実際の英語通し読みが最終ゲート）

## 本発表の性格（設計意図）

**手法の新規性を主張しない。** 適用したのは水域指数による標準的な検出手順であり、貢献は「一般的な手法を、記録が整っていない産業遺産の島に適用し、島全体の候補リストを作って公開した」ことにある。

**物語の骨格は三つの縮尺**である。徒歩＝質感、上空＝境界、衛星＝分布。同じ島を見る縮尺を上げていくと別のものが見える、という現地体験がそのまま構成になっている。

**OSM照合は参考値**として扱う。投影するのは「既に地図にある丁場跡は検出に含まれていた」という1行のみで、距離定義・感度・件数の内訳は投影しない（ノートと想定問答へ）。

**結論は前向きに閉じる。** 「まだ地図にない」という欠落の指摘で終わらせず、**衛星で候補を絞る → 現地で目で確かめる → OpenStreetMap に還す**というループの提案で閉じる。

## 権威資料（数値・主張の正本）

| 資料 | 役割 |
|---|---|
| `docs/reports/exp002_kitagi_quarry_water_detection_report.md` | 数値・考察・限界の一次情報 |
| `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md` | Codex承認済みの主張境界・確定値 |
| `docs/posters/exp002_kitagi_foss4g2026_proposal.md` | 採択アブストラクト（聴衆への約束） |
| `docs/articles/2026_chiri-koryu-10/draft.md` | 現地訪問記（三スケールの枠組み・現地写真） |
| `docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson` | 公開済み検出ポリゴン145件 |
| `docs/results/exp002/exp002_osm_comparison.md` | OSM照合記録（参考値。投影面には出さない詳細を含む） |

## 中心メッセージ（聴衆が1つだけ持ち帰るもの）

> Standard open satellite processing turned a heritage island's quarry ponds into a finite list of candidates — a list that can be checked in the field, confirmed, and put on the public map.

## 採択プロポーザルとの対応（約束の履行台帳）

| プロポーザルの約束 | 着地スライド |
|---|---|
| 島の歴史（17世紀初頭〜、1957年ピーク127丁場・人口1万2千人） | 2 |
| 2019年 日本遺産認定、島全体のインベントリが未整備 | 2 |
| Sentinel-2 L2A を Microsoft Planetary Computer STAC API 経由で取得 | 5 |
| NDWI・MNDWI による水域検出、NDVI マスク | 5 |
| 10 m でのスペクトル混合対策としての負の閾値（−0.2 / −0.1 / 0.3） | 5 |
| 春季（2025-03-23、雲量0.0%）・夏季（2025-08-02、雲量0.7%）の比較 | 6 |
| 春季113件（最大1.28 ha） | 6 |
| 夏季145件・4集中地帯・歴史記録と整合 | 6 |
| NDVIマスクの除外は9ピクセルのみ | 6（ノート）／10 |
| GeoJSON・GeoTIFF 出力、現地調査と遺産記録の基礎データ | 11 |
| OSS のみ（rasterio, numpy, shapely, pystac-client, planetary-computer, folium） | 11 |
| 瀬戸内の他の採石島への展開可能性 | 11 |
| テーマ: Humanitarian, ethical, and peacebuilding | 2, 12 |

手法と結果の説明は S5・S6 の合計 4:20（26%）である。プロポーザルは手法の新規性を主張しておらず、約束13項目はすべて着地するため、強調点を物語側に置く配分とした。

## 主張境界（全スライド共通・ポスター内容契約から継承）

- 検出結果は water polygons / candidates と呼ぶ。`confirmed quarry ponds` を否定形以外で使わない
- 145件と127丁場の比較は**規模の比較**であり、1対1対応ではない
- 精度指標（適合率・再現率）は算出していない
- 春季113件は当時の報告値。実行設定が保存されておらず、**差の原因は特定できていない**。季節を原因として断定しない
- OSM は参考値であり正解データではない。「対応」「一致」を検証結果として述べない
- 8月31日の写真は illustrative field photographs であり validation ではない
- OSM への還元は**今後の計画**として述べる。すでに還元したとは述べない
- `Contains modified Copernicus Sentinel data [2025].` と CC BY 4.0 をクロージングに明示
- 投影面で `poster` を使わない（採択形式は口頭発表）

## タイミング

| スライド | 物語上の役割 | 時間 |
|---|---|---:|
| 1 | 表紙（岩壁） | 0:35 |
| 2 | 島と遺産、そして残された池 | 1:40 |
| 3–4 | 徒歩スケール・上空スケール | 3:00 |
| 5 | 衛星スケール（手法） | 1:50 |
| 6 | 主結果（145件・分布・季節差） | 2:30 |
| 7 | 三つの縮尺が示すもの | 1:10 |
| 8 | 見ていない95% | 1:30 |
| 9 | 再訪（現地確認の開始） | 1:50 |
| 10 | 限界と次の一手 | 1:20 |
| 11–12 | オープンデータと地図への還元 | 2:05 |
| **発話合計** | | **17:30** |

内訳（秒）: S1 35 / S2 100 / S3 90 / S4 90 / S5 110 / S6 150 / S7 70 / S8 90 / S9 110 / S10 80 / S11 70 / S12 55 = **1,050 秒**。

## Slide 1 — Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools

- **Central claim**: 採択タイトルの提示。
- **Projected body**: `Noboru Otsuka — Geolonia Inc.`; `FOSS4G 2026 Hiroshima`; `2026-09-02 13:30 · Himawari`.
- **Visual**: 丁場池の写真（`choba_lake_3.jpg`、色付き）を大きく配置。タイトルは左揃え。
  （Fix round 2: 印刷用にグレースケール化された記事図版 `fig03_keirin_cliff.jpg`
  から、緑がかった水面が見える色付き写真に差し替え。S7パネル(a)でも同一写真を
  再利用する。）
- **Notes-only boundary**: 冒頭の一言は「この崖は自然のものではない」。写真は現地撮影であり検出結果の図ではない。
- **Claim type**: Exact proposal title.
- **Duration**: 0:35
- **Evidence**: プロポーザル／Pretalx 掲載（`schedule.json` v0.27）。

## Slide 2 — A quarrying island, and the ponds it left behind

- **Central claim**: 島は400年の採石地で、産業の衰退後に無数の水没した採石跡が残った。その島全体の記録は見つからなかった。
- **Projected body**: `Kitagi Island · Kasaoka City, Okayama · Seto Inland Sea`; `Granite quarried since the early 17th century`; `127 active quarry sites at the 1957 peak · up to 12,000 residents`; `Today: two working quarries · about 600–700 residents`; `Abandoned pits filled with rain and groundwater`; `National heritage since 2019 — "Stone Islands of Setouchi"`; `I found no island-wide record of the ponds themselves.`
- **Visual**: 位置図（`poster_f1_study_area.png`、英語ラベル）。
- **Notes-only boundary**: 「見つからなかった」は探索範囲の限定であり、存在しないという断定ではない。オープンデータには部分的な記録がある（S8で参考として触れる）。
- **Claim type**: Historical context ＋探索範囲を限定した gap statement。
- **Duration**: 1:40
- **Evidence**: 報告書 1.1、3.1／プロポーザル Description ¶1／訪問記 Ⅰ-1。

## Slide 3 — On foot: I could stand in front of five or six of them

- **Central claim**: 徒歩の縮尺で分かるのは質感である。切削面、緑の水面、深さ。だが島全体は見えない。
- **Projected body**: `March 2026 — a drone mapping party on the island`; `Vertical granite walls, cut not weathered`; `Water in an unusual green; reported depths of a few metres to about twenty`; `A stage on the water, built from leftover stone`; `Five or six sites during the event.`
- **Visual**: 現地写真2枚を同寸で並置（`fig01_lake_stage.jpg`、`choba_lake_2.jpg`）。**固定寸法スロット**。
  （Fix round 2: `choba_lake_3.jpg` はS1表紙に採用されたため、表紙を繰り返さない
  方針で `choba_lake_2.jpg` に差し替え。）
- **Notes-only boundary**: 水深は報告書由来の記述であり、著者の計測値ではない。
- **Claim type**: Field observation（定性・質感）。
- **Duration**: 1:30
- **Evidence**: 訪問記 Ⅰ章、報告書 1.1（水深）、写真は著者撮影。参加イベント: 「北木島ドローン・マッピングパーティ 2026」2026年3月20〜21日。

## Slide 4 — From the air: the quarry boundaries are the landform

- **Central claim**: 上空の縮尺で分かるのは境界の在り方である。採石権を持つ企業同士の境目が、細い岩壁として残されている。
- **Projected body**: `Drone flown from the stage on the water`; `Grey rectangles cut into the green canopy`; `Between two quarries, a thin wall left standing`; `A property line, standing as terrain`; `The same event added features to OpenStreetMap.`
- **Visual**: 上空写真（`fig06_aerial_quarries.jpg`）とドローン離陸（`fig05_drone_takeoff.jpg`）。
- **Notes-only boundary**: 境界が地形になっているという観察は現地での定性的観察であり、本研究の測定結果ではない。イベントではドローンで湖の測量も行った。
- **Claim type**: Field observation（定性・境界）。
- **Duration**: 1:30
- **Evidence**: 訪問記 Ⅱ章、写真は著者撮影。
- **物語上の役割**: ここで OSM への地物追加に触れ、S12 の「地図に還す」で回収する。イベントで追加したのは現地で観察した地物であり、徒歩到達範囲を網羅的に地図化したとは述べない。

## Slide 5 — On the train home: one satellite scene covers the whole island

- **Central claim**: 島全体を一度に覆えるのは衛星である。使ったのは水域指数による標準的な手順で、新しい手法ではない。
- **Projected body**: `Sentinel-2 L2A via the Microsoft Planetary Computer STAC API`; `Summer 2025-08-02 · 0.7% cloud · 10 m analysis grid`; `Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)`; `Thresholds below zero: at 10 m a narrow pond is part water, part granite, part shadow`; `A standard water-index workflow — nothing new in the method`; `Minimum reported polygon area: 100 m²`.
- **Visual**: 4パネル（NDWI / MNDWI / NDVI / 最終マスク、`poster_f4_index_panels.png`）。式は図中に置く。
- **Notes-only boundary**: 閾値はヒストグラムの谷から決めた値で、最適化・感度分析・現地検証はしていない。B11 は 20 m から 10 m へリサンプリングしている。
- **Claim type**: Method（標準手順の適用）。
- **Duration**: 1:50
- **Evidence**: 報告書 3.2、3.3、3.4、4.2（図4-2）、ポスター §3・§4。

## Slide 6 — The scan found 145 water polygons across the island

- **Central claim**: 夏季シーンから島内145件の水域ポリゴンを検出し、その分布は採石の歴史的中心と整合した。
- **Projected body**: 大きな数値 `145`; `intra-island water polygons ≥ 100 m², summer 2025-08-02`; `Clustered in the north, south-east, centre and west — consistent with historical quarrying records`; `145 detections vs 127 recorded quarry sites — a comparison of scale, not a one-to-one match`; 小タイル `Spring 2025-03-23 — 113 polygons reported`; `These are detected water polygons, not individually field-confirmed quarry ponds.`; `Contains modified Copernicus Sentinel data [2025].`
- **Visual**: 検出分布図（4集中地帯を注記した**新規図版 P6**）。春季113は小さな数値タイルで併記。
- **Notes-only boundary**: 145は検出数であって丁場数ではない。春季113は当時の報告値で、実行設定が保存されておらず差の原因は特定できていない（現行パイプラインの再計算は180）。夏季のNDVIマスクで除外されたのは9ピクセルのみで、これは仮説の棄却である。
- **Required spoken content（英語ノートで必須。投影面に全て載せる必要はない）**:
  - `Spring: 2025-03-23, 0.0% cloud — 113 reported polygons, largest 1.28 hectares`
  - `Summer: 2025-08-02, 0.7% cloud — 145 polygons, largest 7,826 square metres`
  - `The two reported scenes differed, but we have not isolated the cause`
  - `The spring figure is what we reported; that run's configuration is not preserved`
  - `The NDVI vegetation mask removed only nine pixels`
  - `These are detected water polygons, not individually field-confirmed quarry ponds`
  これらは内部注記ではなく**英語の発話本文**に置く。S6 で時間を詰める場合も、この6行と候補／非検証の留保は削らない。
- **Claim type**: Direct result。
- **Duration**: 2:30（S6 単体で 2:30 以内に収めることを通し読みのハードゲートとする）
- **Evidence**: 報告書 4.1（再現性追記）、4.2、4.3、4.4、5.1、ポスター §5・§6。

## Slide 7 — Each scale shows what the others cannot

- **Central claim**: 徒歩は質感を、上空は境界を、衛星は分布を可視化する。三つは代替ではなく別のものを見せる。
- **Projected body**: `On foot — texture: the cut face, the water, the depth`; `From the air — boundaries: property lines standing as rock walls`; `From orbit — distribution: 145 candidates across the island`; `Not better or worse. Different things become visible.`
- **Visual**: 三スケール合成図（`p07_three_scales.png`、英語ラベルのみ。
  発表専用に生成。日本語記事と共有される `fig09_multiscale.png` は日本語キャプション
  焼き込み・動画UI写り込みのため不採用。ソース: (a) `fig03_keirin_cliff.jpg`、
  (b) `fig06_aerial_quarries.jpg`（S4と同じ縦クロップでUI除去）、
  (c) 検出145ポリゴンの分布（`exp002_kitagi_summer_water_polygons_2025-08-02.geojson`、
  ゾーンラベル・訪問地点なし）。生成: `exp002_kitagi_foss4g2026_figures.py` の
  `make_p07_three_scales()`）。
- **Notes-only boundary**: なし（解釈の提示）。
- **Claim type**: Framing（論旨）。
- **Duration**: 1:10
- **Evidence**: 訪問記 Ⅲ-3、`p07_three_scales.png`。

## Slide 8 — Five or six sites visited — the scan produced 145 candidates

- **Central claim**: 現地で訪れたのは5〜6か所、衛星が返したのは145件の候補である。両者は規模が違う。候補は有限の現地確認リストになる。
- **Projected body**: `Five or six quarry sites visited during the event`; `145 water polygons detected from one scene`; `Individual ponds are not field-confirmed — no precision or recall yet`; `Every quarry feature already mapped in OpenStreetMap overlaps one of the detections (retrieved 2026-08-23, for reference)`; `The candidates form a finite field-check list.`
- **Visual**: 検出分布図の上に、**座標を確認できた訪問地点のみ**を控えめに重ねる（**新規図版 P8**）。訪問記の図4で座標が特定できているのは4地点（豊浦港・豊浦公会堂・湖上ステージ〔桂林〕・千ノ浜）であり、この4地点だけを表示する。
- **Notes-only boundary**: 訪問した5〜6か所を145ポリゴンの個別IDへ照合した記録はない。ここで述べているのは**規模の対比**であり、訪問地点が検出集合の部分集合であるという主張ではない。到達可能性は安全・立入許可に依存し、すべてが徒歩で到達できるとは限らない。OSM は参考値であって正解データではなく、重なりは同一地物の同定や精度を意味しない。件数の内訳・距離の定義は投影しない。
- **Claim type**: Scale contrast ＋ acknowledged gap ＋ OSM を参考値として1行。
- **Duration**: 1:30
- **Evidence**: 訪問記 Ⅲ-3（訪問数）、報告書 4.2（145件）、5.4、6.3、`exp002_osm_comparison.md`（参考）。

## Slide 9 — Two days ago I went back — a first look, not validation

- **Central claim**: 衛星が指し示した候補地点へ実際に戻った。これは現地確認の開始であって精度検証ではない。
- **Projected body**: `2026-08-31 — return visit`; `Candidates selected from the published GeoJSON`; `Illustrative field photographs — not accuracy validation`; `What the scan pointed at, seen from the ground.`
- **Visual**: 8月31日の写真 2〜3枚（**固定寸法スロット**。撮影後に画像を差し替えるだけで完成する構造）。
- **Notes-only boundary**: 写真は候補地点の存在を示すのみ。丁場跡であることの同定や精度評価は行っていない。
- **Claim type**: Field photographs（illustrative）。
- **Duration**: 1:50
- **Evidence**: 撮影記録（撮影後に `_verification.md` へ座標・撮影時刻・撮影方向を記載）。
- **撮影できなかった場合**: 本スライドを**削除**し、S8 から S10 へ直接接続する。既存写真での代替は `Two days ago` の記述と矛盾するため行わない。生成スクリプトは「再訪あり版」「なし版」を切り替え可能にする。

## Slide 10 — What this can and cannot tell you

- **Central claim**: 10 m解像度・負の閾値・精度指標の不在という限界の内側でのみ使える。
- **Projected body**: `10 m resolution — ponds narrower than about 10 m are unreliable`; `Thresholds below zero admit dark rock and shadow`; `No precision or recall — field validation not done`; `Next: walk the candidates · a land mask for the shoreline · higher-resolution imagery`.
- **Visual**: テキスト中心。余白を広く取る。
- **Notes-only boundary**: 自然の池・農業用ため池・貯水施設が含まれ得る。海岸線付近のポリゴンには海水が含まれる可能性がある。
- **Claim type**: Limitations。
- **Duration**: 1:20
- **Evidence**: 報告書 5.4、6.3、ポスター §6。

## Slide 11 — The 145 polygons are open data now

- **Central claim**: 検出結果を公開したので、誰でも同じ手順を再実行し、候補を確かめられる。
- **Projected body**: `Published — 145 detected polygons as GeoJSON · EPSG:4326`; `Pipeline outputs — GeoJSON and GeoTIFF for fieldwork and heritage documentation`; `Open-source Python pipeline · no licence fee, no imagery purchase`; `The same workflow could be extended to other quarried islands in the Seto Inland Sea.`; footer に `rasterio · numpy · shapely · pystac-client · planetary-computer · folium`、`Contains modified Copernicus Sentinel data [2025]. Basemaps: GSI Tiles, Geospatial Information Authority of Japan. CC BY 4.0.`
- **Visual**: QRコード（`poster_qr_repo.png`）と最小限のテキスト。
- **Notes-only boundary**: 公開しているのはGeoJSON。GeoTIFF はパイプラインの出力仕様であって公開物ではない。閾値は他島へそのまま持ち込めない。
- **Claim type**: Reuse and transferability。
- **Duration**: 1:10
- **Evidence**: 報告書 3.5、6.2、6.3、公開GeoJSONとREADME、ポスター §7・フッター。

## Slide 12 — Check them on the ground, then put them on the map

- **Central claim**: 衛星で候補を絞り、現地で目で確かめ、確かめたものを OpenStreetMap に還す。この一巡が、記録の整っていない産業遺産の景観を公共の地図に載せていく道筋である。
- **Projected body**: `Satellite scan → a finite candidate list`; `Field visit → see it with your own eyes`; `OpenStreetMap → put what you confirmed on the public map`; `I plan to contribute the ponds I can confirm.`; `The March mapping party added features observed on the ground. The scan suggests where to look next.`; `Thank you · Q&A`.
- **Visual**: 3ステップの横並びフロー（**新規図版 P12**、同じ寸法の図形3つ・矢印は細い無彩色）。
- **Notes-only boundary**: OSM への還元は**今後の計画**であり、まだ行っていない。地物の追加は現地確認できたものに限る。
- **Claim type**: Proposal（今後の計画）。
- **Duration**: 0:55
- **Evidence**: 訪問記 Ⅱ-1（マッピングパーティ）、Ⅲ-3、〔結〕。

## 新規に必要な図版

| ID | 内容 | 生成元 |
|---|---|---|
| P6 | 4集中地帯を注記した検出分布図 | `scripts/generate_exp002_poster_figures.py` の F3 派生 |
| P8 | 検出分布図に、座標を確認できた訪問地点4点のみを重ねた図 | 公開GeoJSON + 訪問記 図4 の4地点（豊浦港・豊浦公会堂・湖上ステージ〔桂林〕・千ノ浜） |
| P12 | 「衛星 → 現地 → 地図」の3ステップフロー | 新規作図（図形3つ・細い矢印） |
| S3・S4・S9 | 写真スロット（固定寸法） | 訪問記の写真、8月31日撮影分 |

## 8月31日の撮影に向けた事前準備

公開GeoJSONから撮影対象リスト（座標・面積）を生成し、渡航前に渡す。**安全・立入許可・到達可能性を面積順位より優先**する。

1. 検出最大ポリゴン（7,826 m²、北部）— OSM 上で「北木の桂林」として登録されている地物と重なる位置。GPS・撮影方向・撮影時刻を記録する
2. 徒歩到達可能で面積の大きい候補（S9 の写真に使う）
3. 現地で確認できた地物は、後日 OSM への追加候補として記録する（S12 の計画の実行）

これは標本設計された accuracy validation ではなく、探索的な現地確認である。

## 実装時のハードゲート

- 本文を **15 pt 未満へ自動縮小しない**。収まらない場合は footer またはスピーカーノートへ送る（投影文字列が多い S2・S5・S6・S11 で特に注意）
- S5 の式、S6 の補足値（春季タイル・雲量）は、中心メッセージより**小さい evidence 階層**に置く
- 英語の通し読みで **S6 単体 2:30 以内・本編 17:30 前後**に収まることを確認する。語数計測は英語部分のみを対象とする
- S6 の required spoken content と、各スライドのヘッジは英語の発話本文に置く（内部注記に留めない）

## 成果物

| ファイル | 役割 |
|---|---|
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.md` | 本書（内容契約・正本） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.py` | python-pptx 生成スクリプト（正本） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.pptx` | 生成物（手編集しない） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation_speaker_notes.md` | スピーカーノート（英日併記。**発話対象は英語のみ**、日本語は非発話の訳・補足として構造的に分離。pptxのノートペインへ同内容を書き込む） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation_verification.md` | 照合記録（数値・出典・写真の座標と撮影時刻） |
| `docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py` | 機械検査（投影文字列・数値・禁止表現・スライド数・EN/JA同期・15pt下限） |
| `docs/presentations/images/` | スライド用画像 |

## 設計の変更履歴

### 2026-08-23 設計レビュー（#issuecomment-5385367686）の反映

| 指摘 | 対応 |
|---|---|
| Major 1: OSM距離計算 | 形状間距離（EPSG:32653）へ変更し、`out geom meta` で地物形状を取得。ただし**本発表では OSM を参考値に格下げ**し、投影面には件数・距離・感度を出さない（S8 の1行のみ）。詳細は `exp002_osm_comparison.md` と想定問答へ |
| Major 2: 分類と主張の強さ | レポート5.3・Q7-2 を「有力な現地確認候補」まで弱め、「確認された」「相当すると考えられる」を削除。名前付き `landuse=quarry` は7件（8件は誤り） |
| Major 3: 季節の因果表現 | 季節を原因として断定しない。春季113は S6 の小タイル＋プロベナンス注記に統合し、独立スライドを廃止 |
| Major 4: 時間設計 | 目標を **17:30**（バッファ 2:30）に設定 |
| Major 5: 旧ポスター運用の記述 | 口頭スクリプトの運用メモを廃止済みとして書き換え、validator に旧前提の禁止チェックを追加（別コミット） |
| Minor 1: Slide 2 タイトル | 探索範囲を限定した表現へ（`I found no island-wide record of the ponds themselves.`） |
| Minor 2: 投影境界 | 閾値の説明を「mixed pixels によって動機づけられる」へ。公開物（GeoJSON）とパイプライン出力（GeoJSON/GeoTIFF）を分離 |
| Minor 3: 見出しの番号二重化 | 修正済み |

### 2026-08-23 設計レビュー第3回（#issuecomment-5386098831）の反映

| 指摘 | 対応 |
|---|---|
| integrity 1: S8 の集合包含 | タイトルを規模の対比（`Five or six sites visited — the scan produced 145 candidates`）へ変更。`The rest ... I can walk` を削除し `The candidates form a finite field-check list.` へ。訪問5〜6か所を145の部分集合として扱わない旨を境界に明記。P8 は座標を確認できた4地点のみ表示。中心メッセージの `can be walked` を `can be checked in the field` へ |
| integrity 2: 春季値・9px の発話保証 | S6 に **required spoken content**（英語6行）を新設。春季の雲量0.0%・113件・最大1.28 ha、夏季の雲量0.7%・145件、原因未分離、プロベナンス、NDVI 9px、候補である旨を英語の発話本文で必須化 |
| integrity 3: 出典が支えない一般化 | S3 を `Five or six sites during the event.` へ。S12 を `The March mapping party added features observed on the ground. The scan suggests where to look next.` へ限定 |
| story 1: S9 タイトル | `Two days ago I went back — a first look, not validation` へ変更（境界を述語に載せる） |
| DESIGN_GUIDE・タイミング判定 | 15pt下限、evidence階層、S6 2:30・本編17:30の通し読みゲートを「実装時のハードゲート」節に明記 |
| out-of-scope 2件 | 距離定義の最適化・感度分析・精度指標・新規手法は本発表の修正条件としない（後続の論文化向けに記録） |

### 2026-08-23 発表者による設計方針の確定

| 決定 | 内容 |
|---|---|
| 発表の性格 | 手法の新規性を主張しない旅行記的な talk とする。三つの縮尺を骨格にする |
| OSM の扱い | 参考値。専用スライド2枚を廃止し、S8 の1行に集約 |
| 季節差 | 独立スライドを廃止し S6 に統合 |
| 配分 | 物語（S3・S4・S7・S9）370秒（35%）、手法＋結果（S5・S6）260秒（26%） |
| 結論 | 「まだ地図にない」という欠落の指摘で終わらせない。**衛星で候補を絞る → 現地で確かめる → OSM に還す**というループの提案で閉じる（S12） |
