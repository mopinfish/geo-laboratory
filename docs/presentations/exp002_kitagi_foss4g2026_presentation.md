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
| 8 | 訪問5〜6か所と検出145件の規模の対比 | 1:30 |
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
- **Projected body**: `March 2026 — a drone mapping party on the island`; `Vertical granite walls, cut not weathered`; `Water in an unusual green; reported depths of a few metres to about twenty`; `A wooden stage on the water, with stone blocks arranged as seats`; `Five or six sites during the event.`
- **Visual**: 現地写真2枚を同寸で並置（`fig01_lake_stage.jpg`、`choba_lake_1.jpg`）。**固定寸法スロット**。
  （Fix round 3: `choba_lake_2.jpg` は水面（緑がかった池）がほぼ写らず投影文と
  対応しないため、垂直な花崗岩壁が緑がかった水面へ直接落ち込む `choba_lake_1.jpg`
  に差し替え。`choba_lake_3.jpg` はS1表紙・S7パネル(a)で採用済みのため使わない。）
- **Notes-only boundary**: 水深は報告書由来の記述であり、著者の計測値ではない。
- **Claim type**: Field observation（定性・質感）。
- **Duration**: 1:30
- **Evidence**: 訪問記 Ⅰ章、報告書 1.1（水深）、写真は著者撮影。参加イベント: 「北木島ドローン・マッピングパーティ 2026」2026年3月20〜21日。

## Slide 4 — From the air: the quarry boundaries are the landform

- **Central claim**: 上空の縮尺で分かるのは境界の在り方である。採石権を持つ企業同士の境目が、細い岩壁として残されている。
- **Projected body**: `Drone flown from the stage on the water`; `Grey rectangles cut into the green canopy`; `Between two quarries, a thin wall left standing`; `A property line, standing as terrain`; `The same event added features to OpenStreetMap.`
- **Visual**: 丁場池の上空写真（`aerial_quarry_pond.jpg`）と湖上ステージのドローン
  （`drone_lake_stage.jpg`）を**縦長スロット2枚**として同寸で並置し、本文列を左に置く。
  （2026-08-24 の調整: 印刷用にグレースケール化された記事図版
  `fig06_aerial_quarries.jpg` / `fig05_drone_takeoff.jpg` から、発表者提供の色付き原本
  `docs/results/exp002/photos/01.jpg` / `02.jpg` に差し替えた。2枚はいずれも縦位置
  （縦横比 0.75〜0.88）で 16:9 スロットでは各フレームの58%を捨てることになり、
  S4 の主張（境界が地形として読める）に必要な縦方向の広がりが失われるため、
  スロットを縦長に変更した。実測: スロット 3.87 × 4.40 in ×2 ＋ 間隔 0.20 in = 7.93 in、
  本文列 4.00 in で図版帯 12.23 × 4.80 in に重なりなく収まる。写真は引き伸ばさず
  スロット比へのクロップのみで配置する。`01.jpg` は画面を撮影した写真で macOS の Dock と
  「Pages」ツールチップが写り込んでいるため、`images/` へのコピー時点で y=1230 で
  切り落としてある。S3・S9 の 16:9 固定スロットは変更していない。詳細は照合記録 2.5 節）
- **Notes-only boundary**: 境界が地形になっているという観察は現地での定性的観察であり、本研究の測定結果ではない。イベントではドローンで湖の測量も行った。
- **Claim type**: Field observation（定性・境界）。
- **Duration**: 1:30
- **Evidence**: 訪問記 Ⅱ章、写真は著者撮影。
- **物語上の役割**: ここで OSM への地物追加に触れ、S12 の「地図に還す」で回収する。イベントで追加したのは現地で観察した地物であり、徒歩到達範囲を網羅的に地図化したとは述べない。

## Slide 5 — On the train home: one satellite scene covers the whole island

- **Central claim**: 島全体を一度に覆えるのは衛星である。使ったのは水域指数による標準的な手順で、新しい手法ではない。
- **Projected body**: `Sentinel-2 L2A via the Microsoft Planetary Computer STAC API`; `Summer 2025-08-02 · 0.7% cloud · 10 m analysis grid`; `Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)`; `Thresholds below zero: at 10 m a narrow pond is part water, part granite, part shadow`; `A standard water-index workflow — nothing new in the method`; `Minimum reported polygon area: 100 m²`.
- **Visual**: 4パネル（NDWI / MNDWI / NDVI / 最終マスク、**新規図版 P5**
  `p05_index_panels.png`）。式は図中に置く。ポスター図版 `poster_f4_index_panels.png`
  は native 18pt・実寸 8.82 × 8.50 in で、16:9スライドのどの配置でも図中文字が
  実効15ptに届かない（15ptには配置高さ7.09inが必要で、スライド全高は7.5in）。
  同図のパネル画像を切り出して英語ラベルとカラーバーを大きく描き直したものを使う
  （ラスタは無加工。ネットワーク非依存）。
- **Notes-only boundary**: 閾値はヒストグラムの谷から決めた値で、最適化・感度分析・現地検証はしていない。B11 は 20 m から 10 m へリサンプリングしている。
- **Claim type**: Method（標準手順の適用）。
- **Duration**: 1:50
- **Evidence**: 報告書 3.2、3.3、3.4、4.2（図4-2）、ポスター §3・§4。

## Slide 6 — The scan found 145 water polygons across the island

- **Central claim**: 夏季シーンから島内145件の水域ポリゴンを検出し、その分布は採石の歴史的中心と整合した。
- **Projected body**: 大きな数値 `145`; `intra-island water polygons ≥ 100 m², summer 2025-08-02`; `Clustered in the north, south-east, centre and west — consistent with historical quarrying records`; `145 detections vs 127 recorded quarry sites — a comparison of scale, not a one-to-one match`; 小タイル `Spring 2025-03-23 — 113 polygons reported`; `These are detected water polygons, not individually field-confirmed quarry ponds.`; `Contains modified Copernicus Sentinel data [2025].`
- **Visual**: 検出分布図（4集中地帯を注記した**新規図版 P6**）。春季113は小さな数値タイルで併記。
  検出ポリゴンの下に**追跡済みの背景地図**（CARTO Positron ラベルなし `light_nolabels` z17、`basemap_kitagi_carto_positron.png`）を減光して敷き、海岸線との関係で位置が読めるようにする。**航空写真は使わない**（実写の池の上に検出結果を載せると ground truth と読まれるため。照合記録 2.4 節）。
  地図の描画範囲は **P6・S7パネル(c)・P8 で共通**（`133.5135/34.3645/133.5630/34.4045`。島の陸域の実測 bbox に約 230 m の余白）で、3枚のスライドで島の輪郭が同じ形に見えるようにする。
  `Basemap: © OpenStreetMap contributors, © CARTO` は**地図枠の下**に1行のキャプションとして焼き込む（地図面には重ねない）。
- **Notes-only boundary**: 145は検出数であって丁場数ではない。春季113は当時の報告値で、実行設定が保存されておらず差の原因は特定できていない（現行パイプラインの再計算は180）。夏季のNDVIマスクで除外されたのは9ピクセルのみで、候補マスクへの追加効果は限定的だった。精度への効果は未評価である。
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
  焼き込み・動画UI写り込みのため不採用。ソース: (a) `choba_lake_3.jpg`（S1表紙と同一の
  色付き写真。Fix round 2 でグレースケールの記事図版 `fig03_keirin_cliff.jpg` から
  差し替えた際に本行の更新が漏れていた。成果物・S1の注記・照合記録はいずれも
  `choba_lake_3.jpg` である）、
  (b) `aerial_quarry_pond.jpg`（S4左と同じ色付き原本。画面UIは追跡ファイルの時点で除去済み）、
  (c) 検出145ポリゴンの分布（`exp002_kitagi_summer_water_polygons_2025-08-02.geojson`、
  ゾーンラベル・訪問地点なし。P6・P8 と同じ背景地図・同じ描画範囲。帰属表示は地図枠の下。
  文言・行数は変えず、**パネル (c) の右端に右揃え**で置く——パネル (c) の実効幅は
  2.45 in で、1行の帰属表示は 3.79 in あり、左揃えでは右へ 1.34 in はみ出すため。
  折り返して収める手（3行で 2.27 in）は採らない。P7 は S7 で高さ拘束のため、図版が
  縦に伸びると3パネルの表示寸法がそのまま約13%縮み、このスライドの主題である三スケール
  比較の絵を損なう。右揃えなら1行の高さのままはみ出しが消える。右端はパネル (c)、
  左端は隣のパネル (a) を境界として assert で検査する）。
  **3パネルは表示寸法を完全に同一**にする（共通の縦横比 = パネル(c) の地図範囲の比 ≈ 1.02。
  写真は上下クロップのみで合わせ、引き伸ばしはしない。`vbias` は (a) 0.40 / (b) 0.25）。
  生成: `exp002_kitagi_foss4g2026_figures.py` の `make_p07_three_scales()`）。
- **Notes-only boundary**: なし（解釈の提示）。
- **Claim type**: Framing（論旨）。
- **Duration**: 1:10
- **Evidence**: 訪問記 Ⅲ-3、`p07_three_scales.png`。

## Slide 8 — Five or six sites visited — the scan produced 145 candidates

- **Central claim**: 現地で訪れたのは5〜6か所、衛星が返したのは145件の候補である。両者は規模が違う。候補は有限の現地確認リストになる。
- **Projected body**: `Five or six quarry sites visited during the event`; `145 water polygons detected from one scene`; `Individual ponds are not field-confirmed — no precision or recall yet`; `Every quarry feature already mapped in OpenStreetMap overlaps one of the detections (retrieved 2026-08-23, for reference)`; `The candidates form a finite field-check list.`
- **Visual**: 検出分布図の上に、**座標を確認できた訪問地点のみ**を控えめに重ねる（**新規図版 P8**）。訪問記の図4で座標が特定できているのは4地点（豊浦港・豊浦公会堂・湖上ステージ〔桂林〕・千ノ浜）であり、この4地点だけを表示する。
  背景地図・描画範囲・帰属表示の置き方は P6 と同一（CARTO Positron ラベルなし `light_nolabels` z17、減光、帰属表示は地図枠の下）。
  4地点は**地図面に通し番号 1〜4**（北→南）を短いリーダー線で置き、**番号と地名の対応表を地図の下に2行×2列**で示す。32 pt のラベル箱は地図の縮尺で 1.2〜2.3 km に相当し、互いに 145〜470 m しか離れていない4地点の近くに地名を並べることは幾何学的に不可能なため（照合記録 4 章の裁定）。
  **凡例（`Visit anchors` / `Detected water`）は地図軸の内側**に置く。地図の下に積むと 32 pt × 2行＋枠で 1.55 in を占め、高さ拘束の S8 ではその分だけ地図が小さくなる（「島のどこに位置しているのか分かりにくい」という指摘の主因）。置き位置は「軸の内側に収まる・番号1〜4とスケールバーに重ならない・検出ポリゴンを1つも覆わない」の3条件を満たす候補の機械探索で決め、定数として固定したうえで生成時に assert で検査する。陸地の無地部分に重なることは許容する（S6 がゾーン名を地図内に置いているのと同じ扱い）。
  **図タイトルは1行**（`Route points, not confirmed ponds`）とする。2行から詰めて 0.62 in を地図に回した。主張境界（訪問地点は route points であって confirmed ponds ではない）はこの1行が保つ。
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
- **Projected body**: `Published — 145 detected polygons as GeoJSON · EPSG:4326`; `Pipeline outputs — GeoJSON and GeoTIFF for fieldwork and heritage documentation`; `Open-source Python pipeline · no licence fee, no imagery purchase`; `The same workflow could be extended to other quarried islands in the Seto Inland Sea.`; footer に `rasterio · numpy · shapely · pystac-client · planetary-computer · folium`、`Contains modified Copernicus Sentinel data [2025]. CC BY 4.0.`、`Basemaps: GSI Tiles, Geospatial Information Authority of Japan; © OpenStreetMap contributors, © CARTO.`（デッキが実際に使う2種類の基図。S2 の位置図が GSI Tiles、S6・S7パネル(c)・S8 の検出地図が CARTO/OSM）
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
| P5 | 指数4パネル（NDWI / MNDWI / NDVI / 最終マスク） | `docs/presentations/exp002_kitagi_foss4g2026_figures.py` の `make_p05_index_panels()`（`poster_f4_index_panels.png` のパネル画像を切り出し、英語ラベルとカラーバーを再描画） |
| P6 | 4集中地帯を注記した検出分布図（減光したラベルなし淡色地図の背景つき） | `docs/presentations/exp002_kitagi_foss4g2026_figures.py` の `make_p06_clusters_map()`（公開GeoJSON + `basemap_kitagi_carto_positron.png`） |
| P7 | 三スケール合成図（徒歩・上空・衛星の英語ラベルのみ） | 同スクリプトの `make_p07_three_scales()`（`choba_lake_3.jpg` + `aerial_quarry_pond.jpg` + 公開GeoJSON + `basemap_kitagi_carto_positron.png`） |
| P8 | 検出分布図に、座標を確認できた訪問地点4点のみを重ねた図（背景地図は P6 と同一） | 公開GeoJSON + 訪問記 図4 の4地点（豊浦港・豊浦公会堂・湖上ステージ〔桂林〕・千ノ浜） + `basemap_kitagi_carto_positron.png` |
| P12 | 「衛星 → 現地 → 地図」の3ステップフロー | 新規作図（図形3つ・細い矢印） |
| S3・S9 | 写真スロット（16:9固定寸法） | 訪問記の写真、8月31日撮影分 |
| S4 | 写真スロット（縦長・固定寸法。縦横比 0.878） | 発表者提供の色付き原本 `docs/results/exp002/photos/01.jpg`（画面UIを除去して `aerial_quarry_pond.jpg`）・`02.jpg`（`drone_lake_stage.jpg`） |
| BM | 背景地図ラスタ（CARTO Positron ラベルなし `light_nolabels` z17、範囲 133.5135/34.3645/133.5630/34.4045、取得日 2026-08-24、1.00 MB） | `exp002_kitagi_foss4g2026_figures.py --fetch-basemap`（ネットワークを使う唯一の経路。取得後は追跡ファイルを読むのみ） |

## 8月31日の撮影に向けた事前準備

公開GeoJSONから撮影対象リスト（座標・面積）を生成し、渡航前に渡す。**安全・立入許可・到達可能性を面積順位より優先**する。

1. 検出最大ポリゴン（7,826 m²、北部）— OSM 上で「北木の桂林」として登録されている地物と重なる位置。GPS・撮影方向・撮影時刻を記録する
2. 徒歩到達可能で面積の大きい候補（S9 の写真に使う）
3. 現地で確認できた地物は、後日 OSM への追加候補として記録する（S12 の計画の実行）

これは標本設計された accuracy validation ではなく、探索的な現地確認である。

## 実装時のハードゲート

- 本文を **15 pt 未満へ自動縮小しない**。収まらない場合は footer またはスピーカーノートへ送る（投影文字列が多い S2・S5・S6・S11 で特に注意）
- S5 の式、S6 の補足値（春季タイル・雲量）は、中心メッセージより**小さい evidence 階層**に置く
- 図版内の**背景地図の帰属表示**（`Basemap: © OpenStreetMap contributors, © CARTO`）は**地図枠の下**に置き、地図面（島・検出ポリゴン・スケールバー・ラベル）には重ねない。本文でも主題ラベルでもないため、15 pt 下限ではなく**フッター階層（11〜12 pt）**に従う（S11 のフッターが基図の帰属表示を 11 pt で置いている前例に合わせる）。この行は図版生成スクリプトの`NATIVE_FONT_SIZES` に宣言せず、validator の 15 pt 検査の対象外とする（意図的な除外であることを本節で明記する）
- **図版内に焼き込んだ文字**も、スライド上の実効サイズで 15 pt を下回らない。実効サイズは
  `native_pt × (配置幅 ÷ 画像実寸幅)` であり、判定は生成済みPPTXの `shape.width` と
  画像実寸（px ÷ dpi）から復元して行う（`validate_..._presentation.py` の
  `check_placed_font_sizes()`）。図版生成側の「配置幅を仮定した自己申告」では判定しない
- 英語の通し読みで **S6 単体 2:30 以内・本編 17:30 前後**に収まることを確認する。語数計測は英語部分のみを対象とする
- S6 の required spoken content と、各スライドのヘッジは英語の発話本文に置く（内部注記に留めない）

## 成果物

| ファイル | 役割 |
|---|---|
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.md` | 本書（内容契約・正本） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.py` | python-pptx 生成スクリプト（正本） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.pptx` | 生成物（手編集しない） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation_speaker_notes.md` | スピーカーノート。スライド毎に3ブロック構成（`EN (spoken)` / `JA（訳・読み上げ可）` / `JA（補足・読み上げない）`）。**当日の登壇は英語のみ**（採択通知が英語での発表を前提としている）。日本語の訳はリハーサル・自己確認・非常時の備えとして読み上げ可能な散文で用意し、主張境界や伏線などの内部メモは第3ブロックに分離する。pptxのノートペインへ3ブロックを同順で書き込む |
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

### 2026-08-24 全体レビュー（1回の修正ウェーブ）の反映

| 指摘 | 対応 |
|---|---|
| Critical: 図版内文字の実効サイズ | 図版の自己検査が「配置幅220mm」というデッキが使っていない値を測っていた。実配置での実効サイズは 9.2〜14.7 pt で下限15pt未達。判定を validator へ移し（生成済みPPTXの `shape.width` と画像実寸から復元）、自前図版は native を引き上げ（P6・P8 20→32 pt、P12 24→27 pt）、S6・S8 の図版配置高さを 4.4/4.3 in → 4.8 in にした。実効は 16.0〜21.6 pt |
| Critical: 流用図版 F1（S2） | 地理院タイルをネットワーク取得して描くため再生成せず、**配置を実寸の1.04倍**に拡大して native 15pt を実効 15.6pt にした。本文列が約3.8inに狭まるため S2 本文のみ 16pt（下限15ptは維持） |
| Critical: 流用図版 F4（S5） | 配置拡大では下限を満たせない（実効15ptに配置高さ7.09inが必要でスライド全高7.5in）。同図のパネル画像を切り出し英語ラベルとカラーバーを大きく描き直した **P5** に差し替えた（ラスタは無加工・ネットワーク非依存） |
| Important: 11枚版の検査不足 | タイトル・必須文字列・禁止表現・15pt下限・画像数・callout・pin画像・実効フォントサイズの検査群を、12枚版と再訪なし版の**両方**に走らせるようパラメータ化した（466 → 949 checks） |
| Important: S7 Visual の不整合 | パネル(a)のソース名を成果物と一致させた（`fig03_keirin_cliff.jpg` → `choba_lake_3.jpg`）。新規図版一覧に P5・P7 を追加 |
| Minor: S8 の呼称 | タイミング表の「見ていない95%」を規模の対比の表現に改めた（採用タイトルは変更なし） |

### 2026-08-24 発表者からの調整依頼（背景地図の追加）

| 依頼 | 対応 |
|---|---|
| 検出ポリゴンが島のどこにあるか分からない（検出地図の背景が中性色で海岸線が無い） | 文字を含まない背景地図を**追跡ラスタ**として一度だけ取得し（`--fetch-basemap`）、P6・S7パネル(c)・P8 の最下層に減光して敷いた。図版生成は以後ネットワークに触れない（ラスタが無ければ明示的に失敗させる） |
| 背景地図は英語版タイルで | 英語版タイル（`xyz/english/`）は**z11 までしか存在せず**（実測）、島の縮尺では 70 px しか得られないため、解像度（出力1pxあたり2px以上）を満たせない。英語版を指定した理由（日本語地名を投影面に出さない）を満たすため、**ラベルを一切含まない**淡色地図 CARTO Positron（`light_nolabels` z17）を採用した。日本語地名を含む淡色地図・標準地図・白地図は使わない。詳細は照合記録 2.4 節 |
| 主題データとの視覚的競合を避ける | DESIGN_GUIDE §7.3 に従い整数演算で減光（`出力 = 255 - (255 - 入力) × 0.80`）。減光後の最小輝度 222 に対し検出ポリゴンのグレースケール輝度は 64 で、グレースケール化しても明確に分離することを目視確認した。Positron は元から淡いため、写真基図向けの `0.30` では海岸線が消える（照合記録 2.4 節） |
| 帰属表示 | 各図版内の左上に `Basemap: © OpenStreetMap contributors, © CARTO` を焼き込む（フッター階層 11〜12 pt。上記「実装時のハードゲート」参照）。図版の外側には置かない（図版実寸が伸びて配置倍率＝図中文字の実効ptが下がるため） |

### 2026-08-24 発表者からの調整依頼（写真の色付き原本への差し替え）

| 依頼 | 対応 |
|---|---|
| S4 の写真をグレースケール記事図版から色付き原本へ | `docs/results/exp002/photos/01.jpg`（丁場池の上空写真）・`02.jpg`（湖上ステージのドローン）を `images/` へ取り込み、`fig06_aerial_quarries.jpg` / `fig05_drone_takeoff.jpg` を置き換えた。参照が無くなった2点は `images/` から削除した（`docs/articles/` 側の原本は無変更） |
| `01.jpg` の画面UI（macOS Dock・「Pages」ツールチップ）を投影面に出さない | 行ごとの彩度プロファイルと拡大目視で位置を特定（ツールチップ上端 y≈1244、Dock 上端 y≈1319）し、**追跡ファイルへのコピー時点で y=1230 で切り落とした**。表示側のクロップをどう変えても UI が再出現しない構造にした。詳細は照合記録 2.5 節 |
| 縦長写真に合わせて S4 のレイアウトを変更 | 16:9 スロット2枚（横並び・本文は上）から、**縦長スロット2枚（横並び・本文は左）**へ変更。実測でスロット 3.87 × 4.40 in ×2 ＋ 間隔 0.20 in = 7.93 in、本文列 4.00 in となり図版帯（12.23 × 4.80 in）に重なりなく収まることを確認した。写真は引き伸ばさずクロップのみ。S3・S9 の 16:9 固定スロットは変更していない |
| S7 パネル(b) も色付き原本へ | P7 は3パネル同高さの横並びなのでパネル(b) は横長（16:9）のまま。丁場池の水面が中央に、左右の切削面がともに入る `vbias=0.25` を試作の目視比較で選んだ |

### 2026-08-24 是正（背景地図を航空写真からラベルなし淡色地図へ）

同日の第1波では背景地図に地理院タイルの全国最新写真（`seamlessphoto` z17）を採用したが、
これを撤回し **CARTO Positron のラベルなしタイル（`light_nolabels` z17）** に差し替えた。
背景地図を敷くこと自体・取得の一回性・ネットワーク非依存・減光・帰属表示の位置と階層は変えていない。

| 是正の理由・論点 | 対応 |
|---|---|
| 航空写真は S7 の物語と衝突する | S7 は「(a) 歩いて＝質感 / (b) 上空から＝境界 / (c) 衛星から＝分布」の三スケール合成図であり、パネル(c) の下に航空写真を敷くとパネル(b) と見分けが付かなくなる。ラベルなしの**地図**にしたことでパネル(b) と(c) が明確に別物として読める |
| 航空写真は ground truth と読まれる | 本発表の主張境界は「検出は候補であり、ground truth も精度指標も持たない」こと。実際の丁場池が写った写真の上に検出結果を載せると「目視で検証済み」と受け取られ、「池が見えるなら指数は不要では」という誤解も招く。写真ではない地図に替えて解消した |
| 投影面は英語のみ | Positron のラベルなしタイルは文字を一切含まないため、英語版タイルを指定した本来の理由をそのまま満たす（日本語地名を含む地理院の淡色地図・標準地図・白地図は引き続き使わない） |
| 解像度 | Positron は z20 まであり、z17 で 4,474 px（出力1pxあたり2.4px）を確保できる |
| 減光率の再調整 | Positron は元から淡いため（海 = 輝度 216、陸 = 241）、写真基図向けの `KEEP = 0.30` では全画素が 243 に潰れて海岸線が消える。`KEEP = 0.80` に緩め、検出ポリゴン（輝度 64）との差 158階調と海陸差 20階調を両立させた |
| 帰属表示 | 図版内の焼き込みを `Basemap: © OpenStreetMap contributors, © CARTO` に差し替えた。S11 フッターはデッキが実際に使う2種類の基図を挙げる（S2 の位置図 = GSI Tiles、S6・S7パネル(c)・S8 = CARTO/OSM） |
| 容量 | ベクタ由来のフラットなラスタは PNG が圧縮されるため、追跡ラスタ 18.3 MB → 0.95 MB、PPTX 各 13.0 MB → 8.9 MB に戻った |

### 2026-08-24 発表者からのレイアウト指摘（S6・S7・S8 の図版）

背景地図を敷いたあとのレンダリングを見た発表者から、図版の見えの不具合を4件指摘された。
**投影文字列・スピーカーノート・主張境界は変更していない**（図版の描き方だけを直した）。

| 指摘 | 対応 |
|---|---|
| 帰属表示の白い箱が地図の内側（左上）に置かれ、島の北西部を覆っていた | 地図枠の**下**に1行のキャプションとして出した。文言は変更なし。フッター階層（実効 11.1〜11.4 pt）と 15 pt 下限からの除外もそのまま。軸の内側へ戻る回帰は `assert_credit_outside_map()` が実測検査する |
| S8 の訪問地点ラベル4枚が地図の右端に縦積みされ、枠からはみ出し、`Sen-no-` / `hama` のように語中で折れていた | 地図面には**通し番号 1〜4**（北→南）だけを短いリーダー線で置き、番号と地名の対応表を地図の下に2行×2列で示す形に改めた。32 pt のラベル箱は地図の縮尺で 1.2〜2.3 km 相当で、互いに 145〜470 m しか離れていない4地点の近くに地名を置くことは幾何学的に不可能である（照合記録 4 章の裁定） |
| S6 と S7(c)・S8 で島の形が違って見え、島が枠で切れていた | 3図版が共有する描画範囲を**島の陸域の実測 bbox + 約 230 m の余白**へ広げた（`133.5135/34.3645/133.5630/34.4045`）。従来の範囲は実測 bbox との差が 20〜40 m しかない余白ゼロの枠で、海岸線が四辺すべてで枠に接していた。背景地図ラスタも同じ範囲で取り直した（`--fetch-basemap` は1回のみ、図版生成は従来どおりネットワーク非依存） |
| S7 の3パネルの幅が不揃い（(a) 狭い / (b) 広い / (c) 中間） | 共通の縦横比（= パネル(c) の地図範囲の比 ≈ 1.02）を決め、写真2枚を上下クロップだけで合わせた（引き伸ばしなし）。3パネルの表示寸法が同一であることを実測 assert で固定した |
| S6 の図版タイトルが2行目で図の右端に達していた | 末尾の `— 145 polygons` を外した（件数はスライドのタイトルと 66 pt コールアウトが既に述べており重複） |

