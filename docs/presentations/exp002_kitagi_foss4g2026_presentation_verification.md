# FOSS4G 2026 Hiroshima 口頭発表 照合記録 — 北木島丁場跡水域

本書は、口頭発表（`exp002_kitagi_foss4g2026_presentation.pptx` / `..._no_revisit.pptx`）で投影・発話する全数値と、`images/` 配下の全画像について、出典（権威資料の節番号）とコピー元・SHA256を記録するものである。内容契約（`exp002_kitagi_foss4g2026_presentation.md`）が「何を投影するか」の正本であるのに対し、本書は「その数値・画像がどこから来たか」の正本である。

- 検査対象: `docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py` の `check_verification_record()`
- SHA256 は本書執筆時にディスク上のファイルから直接計算した（`shasum -a 256`／`hashlib.sha256`）。過去のレポート・チャットに記載された値はコピーしていない
- 権威資料: `docs/reports/exp002_kitagi_quarry_water_detection_report.md`（数値・限界の一次情報）、`docs/posters/exp002_kitagi_foss4g2026_proposal.md`（採択アブストラクトの約束）、`docs/presentations/exp002_kitagi_foss4g2026_presentation.md`（投影文字列の正本）、`docs/results/exp002/exp002_osm_comparison.md`（OSM照合。参考値）、`docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson`（公開ポリゴン）

## 1. 数値照合表

「投影」列は当該スライドの投影本文（テキストフレーム）に文字列として現れることを指す。図版内の注記や口頭のみの言及は「発話のみ」と明記する。数値は内容契約（`exp002_kitagi_foss4g2026_presentation.md`）の `Projected body` と生成スクリプト（`exp002_kitagi_foss4g2026_presentation.py`）の投影文字列リテラルを照合して確認した。

| 値 | 使用スライド | 出典（節番号） |
|---|---|---|
| **145**（夏季・島内検出ポリゴン数） | 投影: S6（callout 66pt）・S7・S8・S11。発話: S6–S12全体 | 報告書 表4-2「島内水域ポリゴン数（海域除外）145」（§4.2）。公開GeoJSON（`exp002_kitagi_summer_water_polygons_2025-08-02.geojson`）を本書執筆時に実測し、`features` 数が145件であることを確認済み（2章の生成コマンドと同じ環境で `len(features) == 145`） |
| **113**（春季・島内報告ポリゴン数） | 投影: S6（小タイル "Spring 2025-03-23 — 113 polygons reported"）。発話: S6 required spoken content | 報告書 表4-1「島内水域ポリゴン数（海域除外）113」（§4.1）。同節の再現性追記: 当該実行の設定は保存されておらず、現行パイプラインで同一シーンを再計算すると180件になり113は未再現（原因未特定のまま S6 で扱う） |
| **127**（1957年ピークの丁場数） | 投影: S2（"127 active quarry sites at the 1957 peak"）・S6（"145 detections vs 127 recorded quarry sites"） | 報告書 §1.1「昭和32年（1957年）には島内に大小127か所の丁場が稼働」。プロポーザル Abstract ¶2 に同値 |
| **9 px**（NDVIマスクによる除外画素数） | 発話のみ: S6 required spoken content（"The NDVI vegetation mask removed only nine pixels"）、S10 EN本文（"The vegetation mask removed only nine pixels"）。投影本文には数値を置かない | 報告書 表4-2「植生マスクにより除外 9 px」（§4.2）。仮説3の棄却根拠（§5.1） |
| **100 m²**（最小報告ポリゴン面積） | 投影: S5（"Minimum reported polygon area: 100 m²"）・S6（"intra-island water polygons ≥ 100 m²"） | 報告書 §3.4「水域ポリゴンは100m²以上のもののみを抽出した」 |
| **10 m**（解析グリッド／Sentinel-2の分解能） | 投影: S5（"10 m analysis grid"、"at 10 m a narrow pond is..."）・S10（"10 m resolution — ponds narrower than about 10 m are unreliable"） | 報告書 §3.2（B02/B03/B04/B08の分解能10m）・§3.4（10mグリッドでの複合判定） |
| **20 m**（B11短波長赤外バンドの元解像度） | 発話のみ: S5 EN本文（"The short-wave band arrives at twenty metres, so I resampled it to ten"）。投影本文には置かない | 報告書 §3.2「B11（20m分解能）はバイリニア補間により10m分解能にリサンプリングした」 |
| **1.28 ha**（春季・島内最大水域面積） | 発話のみ: S6 required spoken content（"largest of them was one point two eight hectares"） | 報告書 表4-1「島内最大水域面積 1.28 ha」（§4.1） |
| **7,826 m²**（夏季・島内最大水域面積） | 発話のみ: S6 required spoken content（"largest was seven thousand eight hundred and twenty-six square metres"） | 報告書 表4-2「島内最大水域面積 7,826 m²」（§4.2）。公開GeoJSONの `area_m2` 実測値は最大 7825.5（本書執筆時に算出、2章参照）で、報告書の 7,826 は四捨五入値。両者は同一ポリゴンを指し矛盾しない |
| **2025-03-23**（春季シーン撮影日） | 投影: S6（小タイル "Spring 2025-03-23 — 113 polygons reported"）。発話: S6 required spoken content（"the twenty-third of March 2025"） | 報告書 §3.2 表「春季画像 撮影日 2025-03-23」（シーンID `S2C_MSIL2A_20250323T014711`） |
| **2025-08-02**（夏季シーン撮影日） | 投影: S5（"Summer 2025-08-02"）・S6（"summer 2025-08-02"）。発話: S6 required spoken content | 報告書 §3.2 表「夏季画像 撮影日 2025-08-02」（シーンID `S2A_MSIL2A_20250802T015121`）。公開GeoJSONのファイル名にも同日付 |
| **0.0%**（春季シーン雲量） | 発話のみ: S6 required spoken content（"the scene had no cloud at all"） | 報告書 §3.2 表「春季画像 雲量 0.0%」 |
| **0.7%**（夏季シーン雲量） | 投影: S5（"0.7% cloud"）。発話: S6 required spoken content | 報告書 §3.2 表「夏季画像 雲量 0.7%」 |
| **−0.2**（NDWI閾値） | 投影: S5（合成条件 "Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)"） | 報告書 §3.4「水域マスク = (NDWI > -0.2 OR MNDWI > -0.1) AND NOT (NDVI > 0.3)」 |
| **−0.1**（MNDWI閾値） | 投影: S5（同上の合成条件） | 報告書 §3.4（同上） |
| **NDVI > 0.3**（NDVI植生マスク閾値） | 投影: S5（同上の合成条件） | 報告書 §3.4（同上）・図4-2のヒストグラム（谷の位置） |

### 1.1 式についての注記（ルーリング）

- **投影されるのは合成条件（閾値付きの規則）である。** `"Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)"` は S5 の投影本文のテキストフレームに文字列として置かれている（生成スクリプト `exp002_kitagi_foss4g2026_presentation.py` の `s05()`、508行目付近）。
- **投影されないのは各指数の個別定義式である。** `NDWI = (Green − NIR) / (Green + NIR)` 等（報告書 §3.3）は、投影本文には置かず、図版 `poster_f4_index_panels.png` のパネル内注記としてのみ存在する。この切り分けは検査済み（`validate_..._presentation.py` の `check_evidence_hierarchy()` が `"(Green − NIR)"` 等が投影本文に無いことを確認する）。個別定義式は S5 の発話本文で「NDWI is built from the green band and the near-infrared band」のように言葉で説明する（内容契約 Slide 5・スピーカーノート S5参照）。

## 2. 画像照合表（SHA256）

SHA256 は `docs/presentations/images/` 内のファイルから本書執筆時に直接計算した値である（コマンド: `shasum -a 256 <file>`。検査スクリプトは `hashlib.sha256` で独立に再計算し照合する）。

| ファイル名 | コピー元 / 生成元 | SHA256 | 使用スライド |
|---|---|---|---|
| `choba_lake_1.jpg` | コピー元: `docs/results/exp002/photos/choba_lake_1.jpg`（著者撮影、バイト一致確認済み） | `df0c227a8100895ac850978393c94ef960e662bc18f8694feda1462ad22a5d3a` | S3（右） |
| `choba_lake_3.jpg` | コピー元: `docs/results/exp002/photos/choba_lake_3.jpg`（著者撮影、バイト一致確認済み） | `fc76d7fa21c77ed0b4ecff470860b8f767fd1a7e0a0844e79338ffa47afffb8e` | S1（表紙）・S7パネル(a)の原画像 |
| `fig01_lake_stage.jpg` | コピー元: `docs/articles/2026_chiri-koryu-10/figures/fig01_lake_stage.jpg`（著者撮影・記事図版と共有、バイト一致確認済み） | `02da83402c64be3ed06acfefdb5f324c204428350e82b9534bfe4ad4303761ae` | S3（左） |
| `fig05_drone_takeoff.jpg` | コピー元: `docs/articles/2026_chiri-koryu-10/figures/fig05_drone_takeoff.jpg`（著者撮影・記事図版と共有、バイト一致確認済み） | `f4ec2d10e0729a867af58f5cad32040a40f9be56eb24c6432e90ada6573353a3` | S4（右） |
| `fig06_aerial_quarries.jpg` | コピー元: `docs/articles/2026_chiri-koryu-10/figures/fig06_aerial_quarries.jpg`（著者撮影・記事図版と共有、バイト一致確認済み） | `086a3714fee9792edbf29e60057fff10452028a584338f65bf0784582c4e29b2` | S4（左）・S7パネル(b)の原画像（`vbias=0.2768` で上寄りクロップ） |
| `p06_clusters_map.png` | 生成元: `docs/presentations/exp002_kitagi_foss4g2026_figures.py` の `make_p06_clusters_map()`（入力: 公開GeoJSON、SHA256は下記2.1参照） | `48c608006ac2e041e3dbdbbd5683cf6e95398aedc514c068f4be086e281a4baf` | S6 |
| `p07_three_scales.png` | 生成元: 同スクリプトの `make_p07_three_scales()`（入力: `choba_lake_3.jpg`・`fig06_aerial_quarries.jpg`・公開GeoJSON。英語ラベルのみの発表専用合成図） | `9f174e3f0712f76b872d56d83528439ffaa193582db555e011231032bbcc8ac3` | S7 |
| `p08_visit_anchors_map.png` | 生成元: 同スクリプトの `make_p08_visit_anchors_map()`（入力: 公開GeoJSON＋訪問記図4の座標確認済み4地点） | `ce87b9685c60555ba4ec4ffb0dfb6ba56356462ff7276a59e57d69750b775cf7` | S8 |
| `p12_loop_diagram.png` | 生成元: 同スクリプトの `make_p12_loop_diagram()`（新規作図、外部入力なし） | `eb389c37cbe8252eef7b6171144a62756a7b548e8f1614fefc353084c150d5ba` | S12 |
| `placeholder_revisit_1.png` | 生成元: 記録なし（一回性の生成物。生成スクリプトは保存されていない）。8/31撮影分の実写に差し替えるまでの仮画像 | `f9a9175dd22b98cb607f5f67e1f0d1c84aa77b675aea26e96e35d6bccdd4ea33` | S9（左、実写未着手のため使用中） |
| `placeholder_revisit_2.png` | 生成元: 同上。`placeholder_revisit_1.png` とバイト単位で同一（同一手順で生成された仮画像） | `f9a9175dd22b98cb607f5f67e1f0d1c84aa77b675aea26e96e35d6bccdd4ea33` | S9（右、実写未着手のため使用中） |
| `poster_f1_study_area.png` | コピー元: `docs/posters/figures/exp002/poster_f1_study_area.png`（バイト一致確認済み） | `05880cde6a1cf2362a36d266d1fa8af0942fb0e92c269cb33fa50a2dab29230e` | S2 |
| `poster_f4_index_panels.png` | コピー元: `docs/posters/figures/exp002/poster_f4_index_panels.png`（バイト一致確認済み） | `81b9b5dc9f1dffc38369606f3e2a5c91d21e75c63839972be577f761d57fc16a` | S5 |
| `poster_qr_repo.png` | コピー元: `docs/posters/figures/exp002/poster_qr_repo.png`（バイト一致確認済み） | `ff635ba17127bfca3ca228350a3b4b15b28c1925c1d640891aee1595b75880ee` | S11 |

### 2.1 P6・P7・P8・P12 の入力データ

新規図版4点（P6・P7・P8・P12）は `docs/presentations/exp002_kitagi_foss4g2026_figures.py` が公開GeoJSONのみを入力として生成する（`tmp/`・ネットワークアクセスに依存しない）。

- 入力: `docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson`
- SHA256: `c0b63dbdff47377731ef1fa9103e31df0414692c87aec73a9779c9dfd2121de8`
- 本書執筆時に実測: `features` 数 145、`area_m2` 最大値 7825.5（1.1節の 7,826 m² との差の注記を参照）

### 2.2 記録から意図的に除外した画像（削除済み・不採用）

以下の2点は現在 `images/` に存在しないが、設計レビューでの不採用の経緯を記録として残す（ブリーフが名前での言及を要求している）。

- **`fig03_keirin_cliff.jpg`**（日本語記事用にグレースケール化された図版）: S1表紙・S7パネル(a)の初期案として使われていたが、色付きの現地写真であるべきという判断（本書「4. 意図的に境界を引いた主張」参照）により `choba_lake_3.jpg`（色付き）へ差し替え、参照が無くなったコピーを `images/` から削除した（コミット `031cfef`「fix: S1表紙・S3写真をグレースケール記事図版から色付き原本に差し替え」）。記事側の原本（`docs/articles/2026_chiri-koryu-10/figures/fig03_keirin_cliff.jpg`）は無変更で存在する
- **`fig09_multiscale.png`**（日本語記事と共有される三スケール合成図。日本語キャプション焼き込み・動画UI写り込みあり）: S7の英語専用面という契約に抵触するため不採用とし、発表専用の `p07_three_scales.png`（英語ラベルのみ）に差し替え、参照が無くなったコピーを削除した（コミット `2fe3ba0`「fix: S7の英語のみ違反を解消（fig09_multiscale→p07_three_scales差し替え）」）

## 3. 2026-08-31 撮影記録（現地確認後に追記）

S9（"Two days ago I went back — a first look, not validation"）の2枚の写真は、本書執筆時点では未撮影であり、`placeholder_revisit_1.png` / `placeholder_revisit_2.png` が仮画像として使われている（2章参照）。8月31日の再訪後、撮影した写真に差し替えたうえで、以下の空欄表を実測値で埋めること。

| # | 座標 | 撮影時刻 | 撮影方向 | 対象ポリゴンID |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

- 座標: GPS実測値（十進緯度経度、EPSG:4326）
- 撮影時刻: 現地時間（JST）
- 撮影方向: 磁北からの方位角、または「南東向き」等の記述
- 対象ポリゴンID: 公開GeoJSON（`exp002_kitagi_summer_water_polygons_2025-08-02.geojson`）の `id` プロパティ値。候補選定の優先順は内容契約「8月31日の撮影に向けた事前準備」節（検出最大ポリゴン7,826 m²を優先しつつ、安全・立入許可・到達可能性を面積順位より優先）による

撮影ができなかった場合は、内容契約 Slide 9 の記載どおり S9 を削除した11枚版（`exp002_kitagi_foss4g2026_presentation_no_revisit.pptx`）を使用し、この表は空欄のまま残す。

## 4. 意図的に境界を引いた主張（controller rulings）

以下は、投影・発話の内容を決める際に発表者・レビューが下した裁定であり、将来の読者が「なぜこの書き方なのか」を追跡できるようにするため、根拠となる記載箇所とともに明示する。

| 境界 | 内容 | 記載箇所 |
|---|---|---|
| 候補は現地確認済みではない | 検出145件は water polygons / candidates であり、`confirmed quarry ponds` は否定形以外で使わない | 内容契約「主張境界」節、S6・S8投影本文、validator `FORBIDDEN` |
| 145 vs 127 は規模の比較 | 145件と127丁場の近さは規模の比較であり1対1対応ではない。個別の検出を特定の丁場に照合した記録はない | 内容契約「主張境界」節、S6投影本文（"a comparison of scale, not a one-to-one match"）、報告書 §5.1（仮説2は部分的支持） |
| 精度指標は算出していない | 適合率・再現率は算出していない。「no precision or recall yet」を明言する | 内容契約「主張境界」節、S6・S8・S10投影本文、報告書 §5.4-6・§6.3 |
| 春季値は再現できない | 春季113件は当時の報告値であり、実行設定が保存されておらず現行パイプラインでは再現できない（再計算は180件）。差の原因は特定できていないため、季節を原因として断定しない | 内容契約 S6 required spoken content、報告書 §4.1 追記（2026-08-14）・§5.4-7 |
| OSMは参考値 | OpenStreetMap照合は参考値であり正解データではない。距離は地物形状をEPSG:32653へ投影した形状間距離（重なる場合は0m）。投影面には件数・距離・感度を出さず、S8の1行のみに集約する | 内容契約「本発表の性格」節・S8 Notes-only boundary、`exp002_osm_comparison.md`（距離定義・集計表・「これは精度検証ではない」の明記） |
| 指数の合成条件は投影、個別定義式は発話・図版内 | S5投影本文には閾値付きの合成条件（`Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)`）を置くが、`NDWI = (Green − NIR) / (Green + NIR)` 等の個別定義式は投影本文に置かず、発話とfigure内注記（`poster_f4_index_panels.png`）に限る | 本書1.1節、`exp002_kitagi_foss4g2026_presentation.py` の `s05()` コメント、validator `check_evidence_hierarchy()` |
| S1・S3は色付き原本、上空写真はグレースケール | S1表紙・S3の2枚の写真は色付きの現地写真原本を使う。上空写真（`fig05_drone_takeoff.jpg`・`fig06_aerial_quarries.jpg`）は日本語記事用に変換されたグレースケール版のままで、色付き原本が存在しないため差し替えていない（本書執筆時にPillowで画素サンプリングして確認: `choba_lake_1.jpg`/`choba_lake_3.jpg`/`fig01_lake_stage.jpg` は mode RGB でチャンネル間に差があり、`fig05_drone_takeoff.jpg`/`fig06_aerial_quarries.jpg` は mode L で無彩色） | 内容契約 S1・S3の Visual 注記（Fix round 2・3）、本書2章の画像表 |
| S7は英語専用の三スケール合成図 | S7には発表専用に新規生成した `p07_three_scales.png`（英語ラベルのみ）を使い、日本語記事と共有される `fig09_multiscale.png`（日本語キャプション焼き込み・動画UI写り込み）は使わない | 内容契約 S7 Visual 注記、本書2.2節 |
| 再訪は現地確認の開始であり検証ではない | 8月31日の再訪は"a first look, not validation"であり、サンプリング設計されたaccuracy validationではない。写真は候補地点の存在を示すのみで、正誤の集計や丁場の同定は行わない | 内容契約 S9 Notes-only boundary・「8月31日の撮影に向けた事前準備」節、本書3章 |
| OSMへの還元は今後の計画 | OpenStreetMapへの地物追加は今後の計画として述べ、既に還元したとは述べない。追加するのは現地で確認できたものに限る | 内容契約「主張境界」節・S12 Notes-only boundary、S12投影本文（"I plan to contribute the ponds I can confirm."） |

## 5. 生成コマンド

以下はすべて `uv run python` 経由で実行する（リポジトリ規約）。図版・PPTX・検査スクリプトはこの順に再実行すればバイト単位で再現される決定的な出力を生成する（各スクリプトのdocstringに再現性の明記あり）。

```bash
# 1. 新規図版（P6・P7・P8・P12）を images/ に生成
uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py

# 2. 口頭発表 PPTX を生成（12枚版）
uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py

# 3. 再訪なし版 PPTX を生成（11枚版、S9を除く）
uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py --no-revisit

# 4. 機械検査（投影文字列・数値・禁止表現・画像SHA256・8/31空欄表 等）
uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py
```

SHA256の再計算（本書の値を検証する場合）:

```bash
shasum -a 256 docs/presentations/images/*
shasum -a 256 docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson
```
