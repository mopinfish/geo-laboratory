# FOSS4G 2026 Hiroshima 口頭発表 内容契約 — 北木島丁場跡水域

本書は、2026年9月2日 13:30–14:00（Himawari、Regular Talk）で発表する英語スライドの**投影文字列と主張境界の正本**である。数値・主張は下記の権威資料に従い、逸脱する記述を投影面に置かない。スライド生成スクリプト・PPTX・スピーカーノートは本書と同期させる。

- 設計規約: `experiments-local-llm/docs/presentations/DESIGN_GUIDE.md`、`CONVENTIONS.md` に準拠
- 発表形式: Regular Talk 30分枠（**発表20分・質疑5分・入替5分**）／使用言語 英語
- 発話合計の目標: **17:30**（20分枠に対し 2:30 のバッファ。実際の英語通し読みが最終ゲート）

## 権威資料（数値・主張の正本）

| 資料 | 役割 |
|---|---|
| `docs/reports/exp002_kitagi_quarry_water_detection_report.md` | 数値・考察・限界の一次情報 |
| `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md` | Codex承認済みの主張境界・確定値 |
| `docs/posters/exp002_kitagi_foss4g2026_proposal.md` | 採択アブストラクト（聴衆への約束） |
| `docs/results/exp002/exp002_osm_comparison.md` | OSM照合記録（取得日 2026-08-23、形状間距離） |
| `docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson` | 公開済み検出ポリゴン145件 |
| `docs/articles/2026_chiri-koryu-10/draft.md` | 現地訪問記（現地写真・上空観察） |

## 中心メッセージ（聴衆が1つだけ持ち帰るもの）

> Open satellite data and open-source tools can give a heritage landscape its first island-wide list of quarry-pond candidates — and for most of those candidates, no public map yet says what they are.

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
| GeoJSON・GeoTIFF 出力、現地調査と遺産記録の基礎データ | 13 |
| OSS のみ（rasterio, numpy, shapely, pystac-client, planetary-computer, folium） | 13 |
| 瀬戸内の他の採石島への展開可能性 | 13 |
| テーマ: Humanitarian, ethical, and peacebuilding | 2, 9, 13 |

プロポーザルにない追加要素は3点のみで、いずれも独立した「結果」として提示しない。合計の発話時間は 2:15（全体の13%）に抑える。

1. 現地で見えたもの（スライド3、**1:00**）— **なぜ衛星が必要か**の動機
2. OSM照合（スライド8・9）— プロポーザルが約束した「歴史記録との対応」を、数の一致から**名前付き地点の重なり**へ具体化する補助照合。精度検証としては提示しない
3. 8月31日の再訪（スライド11、**1:15**）— **現地検証が未実施であること**の次の一手。検証結果としては提示しない

## 主張境界（全スライド共通・ポスター内容契約から継承）

- 検出結果は water polygons / candidates と呼ぶ。`confirmed quarry ponds` を否定形以外で使わない
- 145件と127丁場の比較は**規模の比較**であり、1対1対応ではない
- 精度指標（適合率・再現率）は算出していない
- 春季113件は当時の報告値。実行設定が保存されておらず、**差の原因は特定できていない**。季節を原因として断定しない
- OSM は正解データではない。重なりは独立した傍証、近傍地物の不在は「未登録」か「誤検出」で**状態は未決着**
- OSM 上の名称との重なりは「有力な現地確認候補」までとし、同定・確認済みと述べない
- 8月31日の写真は illustrative field photographs であり validation ではない
- `Contains modified Copernicus Sentinel data [2025].` と CC BY 4.0 をクロージングに明示
- 投影面で `poster` を使わない（採択形式は口頭発表）

## タイミング

| スライド | 物語上の役割 | 時間 |
|---|---|---:|
| 1 | 表紙 | 0:35 |
| 2–3 | 課題と動機 | 2:20 |
| 4–5 | 手法（データ・指数） | 3:05 |
| 6–7 | 主結果（145件・分布） | 3:30 |
| 8–9 | OSM照合（重なり・未決着の80件） | 2:30 |
| 10 | 二季節の観測差 | 1:20 |
| 11 | 再訪（現地確認の開始） | 1:15 |
| 12–13 | 限界と次の一手・オープンデータと結び | 2:55 |
| **発話合計** | | **17:30** |

内訳（秒）: S1 35 / S2 80 / S3 60 / S4 75 / S5 110 / S6 120 / S7 90 / S8 75 / S9 75 / S10 80 / S11 75 / S12 100 / S13 75 = **1,050 秒**。

## Slide 1 — Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools

- **Central claim**: 採択タイトルの提示。
- **Projected body**: `Noboru Otsuka — Geolonia Inc.`; `FOSS4G 2026 Hiroshima`; `2026-09-02 13:30 · Himawari`.
- **Visual**: 桂林の岩壁写真（`fig03_keirin_cliff.jpg`）を右半分に配置。タイトルは左揃え。
- **Notes-only boundary**: 写真は現地で撮影した丁場跡であり、検出結果の図ではない。
- **Claim type**: Exact proposal title.
- **Duration**: 0:35
- **Evidence**: プロポーザル／Pretalx 掲載（`schedule.json` v0.27）。

## Slide 2 — I found no published island-wide inventory of these quarry ponds

- **Central claim**: 島の採石史と遺産認定に対して、丁場跡水域を島全体で記録したものが見つからなかった。
- **Projected body**: `Kitagi Island · Kasaoka City, Okayama · Seto Inland Sea`; `Granite quarried since the early 17th century`; `127 active quarry sites at the 1957 peak · up to 12,000 residents`; `Abandoned pits filled with rain and groundwater`; `National heritage since 2019 — "Stone Islands of Setouchi"`; `Partial records exist in open data; I found no island-wide inventory.`
- **Visual**: 位置図（`poster_f1_study_area.png`、英語ラベル）。
- **Notes-only boundary**: OSM に37件の部分的な記録があることをノートで述べる。「存在しない」ではなく「探した範囲で見つからなかった」であることを口頭でも保つ。
- **Claim type**: Historical context（文献・遺産記録）＋探索範囲を限定した gap statement。
- **Duration**: 1:20
- **Evidence**: 報告書 1.1、3.1／プロポーザル Description ¶1。
- **注記**: プロポーザル原文は "no systematic spatial inventory ... has been published" だが、網羅的探索の記録がないため主張を探索範囲に限定する。

## Slide 3 — On the ground I could reach only a handful of them

- **Central claim**: 徒歩と上空からの観察では島の一部しか捉えられない。島全体を一度に覆う手段が必要になる。
- **Projected body**: `March 2026 — a drone mapping party on the island`; `On foot: five or six quarry sites`; `From the air: quarry boundaries left standing as thin rock walls`; `On foot, texture. From the air, boundaries. Neither covers the island.`
- **Visual**: 写真2枚を同寸で並置 — 徒歩（`fig03_keirin_cliff.jpg`）、上空（`fig06_aerial_quarries.jpg`）。**固定寸法スロット**。
- **Notes-only boundary**: 境界が地形になっているという観察は現地での定性的観察であり、本研究の測定結果ではない。ノートで述べる補足: 湖上のステージは余った採石で作られており、そこからドローンを上げて湖の測量も行った。岸壁は採石権を持つ企業同士の境目にあたる。
- **Claim type**: Field observation（定性・動機づけ）。
- **Duration**: 1:00
- **Evidence**: `docs/articles/2026_chiri-koryu-10/draft.md` Ⅰ・Ⅱ章、写真は著者撮影。参加イベント: 「北木島ドローン・マッピングパーティ 2026」2026年3月20〜21日（岡山県笠岡市北木島）— 著者のYAMAP活動記録 `https://yamap.com/activities/46866739`、告知 `https://kryptokyoto.com/openmatomeview/?q=17724374938884`。

## Slide 4 — One open satellite scene covers the whole island

- **Central claim**: 無償のSentinel-2 1シーンで島全体を10 mグリッドで覆える。
- **Projected body**: `Sentinel-2 L2A via the Microsoft Planetary Computer STAC API`; `Summer scene 2025-08-02 · 0.7% cloud`; `Spring scene 2025-03-23 · 0.0% cloud`; `10 m analysis grid — B02/B03/B04/B08 native; B11 (SWIR) resampled from 20 m`; `Minimum reported polygon area: 100 m²`; `No data purchase · no local archive`.
- **Visual**: 夏季トゥルーカラーと水域強調の並置（`poster_f5_truecolor_water.png`）。
- **Notes-only boundary**: 10 m は検出限界そのものであり、幅10 m未満の池は捉えられない（スライド12で再掲）。
- **Claim type**: Method（データ取得）。
- **Duration**: 1:15
- **Evidence**: 報告書 3.2、ポスター §3。

## Slide 5 — Water indices, with thresholds set below zero on purpose

- **Central claim**: 水域指数の和集合と負の閾値によって、スペクトル混合で値が下がる小規模水域を拾う。
- **Projected body**: `Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)`; `At 10 m a narrow pond is part water, part granite, part shadow`; `Thresholds below zero are motivated by those mixed pixels`; `Set from the index histograms — not optimised, not sensitivity-tested`.
- **Visual**: 4パネル（NDWI / MNDWI / NDVI / 最終マスク、`poster_f4_index_panels.png`）。3つの式は**図中に配置**し、投影本文には置かない。
- **Notes-only boundary**: 閾値はヒストグラムの谷から決めた値であり、最適化・感度分析・現地検証はしていない。MNDWI −0.1 には独立した文書化根拠がない。
- **Claim type**: Method（判定条件）。
- **Duration**: 1:50
- **Evidence**: 報告書 3.3、3.4、4.2（図4-2 ヒストグラム）、ポスター §4。

## Slide 6 — Summer imagery detected 145 intra-island water polygons

- **Central claim**: 夏季シーンから島内145件の水域ポリゴン（100 m²以上）を検出した。
- **Projected body**: 大きな数値 `145`; `intra-island water polygons ≥ 100 m², summer 2025-08-02`; `These are detected water polygons, not individually field-confirmed quarry ponds.`; `Natural ponds, reservoirs and shadows may remain.`; `Contains modified Copernicus Sentinel data [2025].`
- **Visual**: 検出分布図（`poster_f3_summer_map.png`）。
- **Notes-only boundary**: 145は検出数であり丁場数ではない。
- **Claim type**: Direct result。
- **Duration**: 2:00
- **Evidence**: 報告書 4.2（表4-2）、ポスター §5。

## Slide 7 — The detections cluster where the island was quarried

- **Central claim**: 検出は北部・南東部・中央部・西部の4か所に集中し、採石の歴史的中心と整合する。
- **Projected body**: `North · South-east · Centre · West`; `Largest detection 7,826 m² (north)`; `A pattern consistent with historical quarrying records`; `145 detections vs 127 recorded quarry sites — a comparison of scale, not a one-to-one match.`
- **Visual**: 4集中地帯を注記した検出分布図（**新規図版 P7**）。
- **Notes-only boundary**: 個別のポリゴンを特定の丁場に結びつけてはいない（対応はスライド8）。
- **Claim type**: Direct result（分布）＋ contextual comparison（127）。
- **Duration**: 1:30
- **Evidence**: 報告書 4.3、5.1（仮説2は部分的支持）、ポスター §6。

## Slide 8 — Seven OSM-mapped quarry features overlap a detected water polygon

- **Central claim**: OSM に名前付きで登録された採石場・丁場跡の地物は、いずれも検出ポリゴンと重なる。
- **Projected body**: `OpenStreetMap · retrieved 2026-08-23 · feature shapes compared in EPSG:32653`; `Seven named quarry features — all seven overlap a detected polygon`; `21 of 37 OSM water or quarry features overlap a detection`; `Imaoka quarry — locally "Kitagi no Keirin" — overlaps the largest detection`; `OSM is community-contributed data, not ground truth.`
- **Visual**: 検出ポリゴン（青）と OSM 地物（黒の輪郭）を重ねた地図（**新規図版 P8**）。重なりが読める配色にする。
- **Notes-only boundary**: 重なりは独立した傍証であり精度検証ではない。適合率・再現率は未算出。桂林の同定は現地での位置確認待ちで、現時点では「有力な現地確認候補」。
- **Claim type**: Open-data cross-check（重なりの観測）。
- **Duration**: 1:15
- **Evidence**: `docs/results/exp002/exp002_osm_comparison.md`（形状間距離・感度表・最終編集日）、報告書 5.3。

## Slide 9 — For most detections, no public map yet says what they are

- **Central claim**: 検出の大半は既存のオープンデータに近傍地物がなく、未登録か誤検出かが未決着である。それが次に確かめるべき候補集合になる。
- **Projected body**: `OpenStreetMap has 37 water and quarry features here — most were edited during community mapping sessions in March 2025 and March 2026.`; 大きな数値 `80 / 145`; `no OSM water or quarry feature within 100 m`; `Not yet mapped, or a false positive — unresolved until fieldwork.`; `A candidate list, not a discovery claim.`
- **Visual**: スライド8と同一の視覚言語で、近傍地物のない80件を強調（**新規図版 P9**）。
- **Notes-only boundary**: 「未登録」と「誤検出」を切り分ける手段は現地検証のみ。件数は2026-08-23時点のOSMの状態と100 mという探索的閾値に依存する（50 m なら104件、200 m なら69件）。編集者名は述べない。
- **Claim type**: Open-data cross-check（未決着の候補集合）。
- **Duration**: 1:15
- **Evidence**: `exp002_osm_comparison.md`（感度表・最終編集日）。

## Slide 10 — The two reported scenes produced different detection patterns

- **Central claim**: 報告上、春季シーンでは大型水域、夏季シーンでは小規模水域が多く検出された。ただし差の原因は分離できていない。
- **Projected body**: `Spring 2025-03-23 — 113 polygons · largest 1.28 ha`; `Summer 2025-08-02 — 145 polygons · largest 7,826 m²`; `Spring count: 113 reported polygons; the exact historical run configuration is not preserved, and the source of the difference has not been isolated.`; `The summer NDVI mask excluded only 9 pixels.`
- **Visual**: 数値タイル2枚（113 / 145）。ポスターと同じ視覚言語。
- **Notes-only boundary**: 現行パイプラインでの春季再計算は180。夏季145と9pxは完全再現可能。季節・大気・海況・太陽高度は候補要因であって確定した原因ではない。NDVIマスクが効かなかったのは仮説の棄却であり失敗ではない。
- **Claim type**: Reported observation（因果を主張しない）＋ reproducibility limitation。
- **Duration**: 1:20
- **Evidence**: 報告書 4.1（再現性追記）、4.4（表4-4）、5.1（仮説3は棄却）、5.2、ポスター §5・§6。

## Slide 11 — A return visit begins field checking — it does not validate accuracy

- **Central claim**: 衛星が指し示した地点へ実際に戻った。これは現地確認の開始であって精度検証ではない。
- **Projected body**: `2026-08-31 — return visit`; `Candidate ponds selected from the published GeoJSON`; `Illustrative field photographs — not accuracy validation`; `I have stood beside fewer than 5% of the 145.`; `Next: match polygons to known quarry locations, then compute precision and recall.`
- **Visual**: 8月31日の写真 2〜3枚（**固定寸法スロット**。撮影後に画像を差し替えるだけで完成する構造）。
- **Notes-only boundary**: 写真は候補地点の存在を示すのみ。丁場跡であることの同定や精度評価は行っていない。「5%未満」は徒歩で訪れた5〜6か所を145で割った概算であり、精度指標ではない。
- **Claim type**: Field photographs（illustrative）＋ acknowledged gap。
- **Duration**: 1:15
- **Evidence**: 撮影記録（撮影後に `_verification.md` へ座標・撮影時刻・撮影方向を記載）。
- **撮影できなかった場合**: 本スライドを**削除**し、スライド10からスライド12へ直接接続する。既存写真での代替は `A return visit` の記述と矛盾し、スライド3とも重複するため行わない。生成スクリプトは「再訪あり版」「なし版」を切り替え可能にする。

## Slide 12 — What these polygons can and cannot support

- **Central claim**: 10 m解像度・負の閾値・海域分離・精度指標の不在という限界の内側でのみ使える。
- **Projected body**: `10 m resolution — ponds narrower than about 10 m are unreliable`; `Thresholds below zero admit dark rock and shadow`; `No strict coastline mask — shoreline polygons may include seawater`; `No precision or recall — field validation not done`; 実例 `A 100 m² detection lies 2.7 m from a mapped water reservoir.`; `Next: land mask · field campaign · higher-resolution imagery`.
- **Visual**: テキスト中心。交絡例の位置を示す小さな地図片（**新規図版 P12・任意**）。
- **Notes-only boundary**: ため池の例はOSM照合で見つかった交絡例であり、誤検出と断定はしていない。
- **Claim type**: Limitations。
- **Duration**: 1:40
- **Evidence**: 報告書 5.4、6.3、`exp002_osm_comparison.md`、ポスター §6。

## Slide 13 — The polygons are now open data

- **Central claim**: 145件を公開データとして出したので、他の島でも同じ手順を再実行できる。産業が作った景観をオープンデータ上で見えるようにする、その一歩である。
- **Projected body**: `Published — 145 detected polygons as GeoJSON · EPSG:4326`; `Pipeline outputs — GeoJSON and GeoTIFF for fieldwork and heritage documentation`; `Open-source Python pipeline · no licence fee, no imagery purchase`; `The same workflow could be extended to other quarried islands in the Seto Inland Sea.`; `github.com/mopinfish/geo-laboratory` + QR; `Thank you · Q&A`.
- **Visual**: QRコード（`poster_qr_repo.png`）と最小限のテキスト。ライブラリ名・帰属・ライセンスは小さな footer に置く（`rasterio · numpy · shapely · pystac-client · planetary-computer · folium`；`Contains modified Copernicus Sentinel data [2025]. Basemaps: GSI Tiles, Geospatial Information Authority of Japan. CC BY 4.0.`）。
- **Notes-only boundary**: 公開しているのはGeoJSON。GeoTIFF はパイプラインの出力仕様であって公開物ではない。閾値は他島へそのまま持ち込めない。
- **Claim type**: Reuse and transferability（提案）。
- **Duration**: 1:15
- **Evidence**: 報告書 3.5、6.2、6.3、公開GeoJSONとREADME、ポスター §7・フッター。

## 新規に必要な図版

| ID | 内容 | 生成元 |
|---|---|---|
| P7 | 4集中地帯を注記した検出分布図 | `scripts/generate_exp002_poster_figures.py` の F3 に注記を追加した派生 |
| P8 | 検出ポリゴン + OSM地物の重畳図（重なりが読める配色） | 公開GeoJSON + `exp002_osm_water_features.json` |
| P9 | P8 と同一視覚言語で、近傍地物のない80件を強調 | 同上 |
| P12 | 交絡例（貯水槽近傍）の拡大片（任意） | 同上 |
| S3・S11 | 写真スロット（固定寸法） | 訪問記の写真、8月31日撮影分 |

## 8月31日の撮影に向けた事前準備

公開GeoJSONから撮影対象リスト（座標・面積・OSM対応の有無）を生成し、渡航前に渡す。**安全・立入許可・到達可能性を面積順位より優先**し、下記3クラスから最低1地点ずつ記録する。

1. 検出最大ポリゴン（7,826 m²、北部）— OSM の「北木の桂林」との同定を、GPS・撮影方向・撮影時刻の記録で裏付ける
2. OSM に近傍地物のない80件のうち、徒歩到達可能で面積の大きいもの
3. 貯水槽近傍の100 m²検出 — 交絡例の裏取り（スライド12で使用）

これは標本設計された accuracy validation ではなく、探索的な現地確認である。

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

## レビュー反映履歴

### 2026-08-23 設計レビュー（#issuecomment-5385367686）の反映

| 指摘 | 対応 |
|---|---|
| Major 1: OSM距離計算 | 形状間距離（EPSG:32653）へ変更。`out geom meta` で地物形状を取得。**重なり（0 m）を主指標**とし、50/100/200 m の感度を記録。Codex 提示値（32/37・89/145）は OSM 中心点→検出形状の定義によるもので、形状間距離では **34/37・80/145**（重なりは 21/37）。この差を照合記録に明示 |
| Major 2: 分類と主張の強さ | 名前付き `landuse=quarry` は **7件**（8件は誤り）。Slide 8 を「Seven OSM-mapped quarry features overlap a detected water polygon」、Slide 9 を「For most detections, no public map yet says what they are」へ変更。レポート5.3・Q7-2 を「有力な現地確認候補」まで弱め、「確認された」「相当すると考えられる」を削除 |
| Major 3: Slide 10 の因果表現 | タイトルを「The two reported scenes produced different detection patterns」へ変更。Central claim から「季節が変える」「強い」を削除 |
| Major 4: 時間設計 | 目標を **17:30**（バッファ 2:30）へ変更。旧 Slide 11（三スケール論旨）を削除し、要点1行を Slide 3 へ、「5%未満」を Slide 11（再訪）へ統合。**14枚 → 13枚**。Slide 3 を 1:00 に短縮。Slide 5 の3式は図中へ、Slide 13 のライブラリ列挙・ライセンスは footer へ移動 |
| Major 5: 旧ポスター運用の記述 | `docs/posters/exp002_kitagi_foss4g2026_talk_script.md` の運用メモを廃止済みとして明記し、validator に旧ポスター枠文言の禁止チェックを追加（別コミット） |
| Minor 1: Slide 2 タイトル | 「I found no published island-wide inventory of these quarry ponds」へ変更 |
| Minor 2: Slide 5・13 の境界 | Slide 5 を「Thresholds below zero are motivated by those mixed pixels」へ。Slide 13 は `Published` と `Pipeline outputs` を分離し `Open-source Python pipeline` を明示 |
| Minor 3: 見出しの番号二重化 | 修正済み（生成スクリプトが投影するタイトル文字列を一意にする） |
| Slide 11 の再訪なし版 | スライド削除で対応することを明記。生成スクリプトに版切り替えを実装 |
| スピーカーノート方針 | 発話対象は英語のみ、日本語は非発話として分離することを成果物表に明記 |
