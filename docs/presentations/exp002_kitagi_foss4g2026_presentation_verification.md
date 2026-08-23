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
| **7,826 m²**（夏季・島内最大水域面積） | 発話のみ: S6 required spoken content（"largest was seven thousand eight hundred and twenty-six square metres"） | 報告書 表4-2「島内最大水域面積 7,826 m²」（§4.2）。公開GeoJSONの `area_m2` 実測値は最大 7825.5（本書執筆時に算出、2章参照）で、報告書の 7,826 は四捨五入値。両者が同一ポリゴンであることは、面積の近さだけでなく重心座標の一致によって直接確認した（1.2節参照） |
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

### 1.2 最大水域ポリゴンの同一性検証（座標による、Task 7で追加）

1.1節では報告書の 7,826 m² と公開GeoJSONの 7825.5 m² を「四捨五入差であり矛盾しない」としていたが、これは面積の近さのみに基づく弱い根拠だった。本節では、同一ポリゴンであることを重心座標の一致によって直接確認する。

本書執筆時に、公開GeoJSON（`exp002_kitagi_summer_water_polygons_2025-08-02.geojson`）を `shapely` で読み込み、`area_m2` 降順で上位2件を抽出し、各ポリゴンの重心座標（EPSG:32653へ投影して重心を求め、EPSG:4326へ逆投影した値。経緯度座標のままシェイプの重心を求めた場合でも同じ4桁に一致することを確認済み）を算出した。

| 順位 | GeoJSONの `id` | `area_m2` | 算出した重心座標 | 報告書 表4-3（§4.3）の対応行 |
|---|---|---|---|---|
| 1 | 1 | 7825.5 | 34.3911°N, 133.5333°E | 「1 \| 7,826 m² \| 34.3911°N \| 133.5333°E \| 北部」 |
| 2 | 2 | 6521.3 | 34.3780°N, 133.5422°E | 「2 \| 6,521 m² \| 34.3781°N \| 133.5421°E \| 南東部」 |

id=1（7825.5 m²）の重心座標は、経度・緯度ともに報告書 表4-3 第1行（7,826 m²、北部）の座標と小数第4位まで完全一致する（34.3911°N, 133.5333°E）。これは四捨五入された面積の近さではなく、同一の地物であることの直接証拠である。

id=2（6521.3 m²）の重心座標は報告書 表4-3 第2行（6,521 m²、南東部）の座標と小数第3位までおおむね一致し（緯度・経度ともに約0.0001°＝約10mの差。ポリゴン単純化の前後や重心計算手法の違いによる差と考えられ、同一地物であることを否定するものではない）、かつ報告書 §4.3・§5.3 が述べる南東部の集中地帯の範囲（34.376〜378°N, 133.542°E）内にある。これは1.1節の「同一ポリゴンを指す」という主張を、7,826 m² だけでなく2番目に大きい6,521 m²についても座標で補強する。

なお、この座標一致確認により、報告書 §5.3 が「検出最大水域が『北木の桂林』の有力な現地確認候補」とする根拠（OSM地物「今岡石材丁場跡（北木の桂林）」との重なり距離0m）が、GeoJSON上のどの `id` を指しているか（id=1）も特定できた。

検証コマンド（`uv run python` 経由、`shapely`・`pyproj` を使用。再現性確認のみで生成物には影響しない）:

```python
import json
from pathlib import Path
from shapely.geometry import shape

data = json.loads(Path("docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson").read_text(encoding="utf-8"))
by_id = {f["properties"]["id"]: f for f in data["features"]}
for fid in (1, 2):
    f = by_id[fid]
    c = shape(f["geometry"]).centroid
    print(fid, f["properties"]["area_m2"], round(c.y, 4), round(c.x, 4))
```

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

## 6. 最終ゲート（Task 7: 通し読み・目視・機械検査の結果）

本章は Task 7 で実施した4つの最終ゲートの結果を記録する。実施日時（本書執筆時）に PDF化・グレースケール化・機械検査を再実行し、以下の結果を得た。

### 6.1 PDF化による目視確認

```bash
soffice --headless --convert-to pdf --outdir /tmp/t7 \
  docs/presentations/exp002_kitagi_foss4g2026_presentation.pptx \
  docs/presentations/exp002_kitagi_foss4g2026_presentation_no_revisit.pptx
pdfinfo /tmp/t7/exp002_kitagi_foss4g2026_presentation.pdf | grep -E "Pages|Page size"
pdfinfo /tmp/t7/exp002_kitagi_foss4g2026_presentation_no_revisit.pdf | grep -E "Pages|Page size"
pdftoppm -r 100 -png /tmp/t7/exp002_kitagi_foss4g2026_presentation.pdf /tmp/t7/a
pdftoppm -r 100 -png /tmp/t7/exp002_kitagi_foss4g2026_presentation_no_revisit.pdf /tmp/t7/b
```

結果: 12枚版は `Pages: 12`、再訪なし版は `Pages: 11`、両方とも `Page size: 960.009 x 540 pts`（13.33in × 7.5in、16:9）を確認した。全ページを画像として目視し、以下の所見を得た（「問題なし」は文字切れ・重なり・スライド外への図形逸脱がないことを指す）。

**12枚版（`exp002_kitagi_foss4g2026_presentation.pptx`）**

| S | 内容 | 所見 |
|---|---|---|
| 1 | 表紙 | 問題なし。左のタイトル・発表者情報と右の縦長写真が重ならず収まっている |
| 2 | 島と遺産 | 問題なし。本文6行と2枚の地図（(a)(b)）がスライド内に収まり、地図同士も重ならない |
| 3 | 徒歩スケール | 問題なし。左右2枚の写真が等幅で並び、下端・右端ともにスライド内 |
| 4 | 上空スケール | 問題なし。左右2枚のグレースケール写真がスライド内に収まる |
| 5 | 衛星スケール（手法） | 問題なし。右側2×2パネル（NDWI/MNDWI/NDVI/Final mask）とカラーバーが重ならず、本文と干渉しない |
| 6 | 主結果（145） | 問題なし。左の "145" コールアウトと本文、右の分布図・4地区ラベル（north/west/centre/south-east）がいずれもスライド内。図の脚注（Copernicusクレジット）も左下に収まる |
| 7 | 三スケール合成 | 問題なし。(a)(b)(c) 3パネルと "1 km" スケールバーがスライド内、パネル同士の重なりなし |
| 8 | 見ていない95% | 問題なし。左の "5–6" "145" コールアウト、右の訪問地点地図（4ラベル＋凡例2種）がスライド内。凡例（▲ Georeferenced visit anchors / ■ Detected water polygons）がグラフ下端に収まる |
| 9 | 再訪（プレースホルダー） | 問題なし。2枚の "Placeholder — 2026-08-31 photograph" 枠が左右対称にスライド内。プレースホルダーであることが明示されている |
| 10 | 限界と次の一手 | 問題なし。本文4行のみ、テキストがスライド幅に収まる |
| 11 | オープンデータ | 問題なし。本文4行とQRコードが重ならず、下部の使用ライブラリ・データクレジット行もスライド内 |
| 12 | ループ図 | 問題なし。本文6行と3ボックスのループ図（Satellite scan → Field visit → OpenStreetMap）がスライド内、矢印もボックス間に収まる |

**再訪なし版（`exp002_kitagi_foss4g2026_presentation_no_revisit.pptx`、11枚）**

S1–S8 は `shasum -a 256` で12枚版のS1–S8とSHA256が完全一致し、バイト単位で同一の描画であることを確認した。S9（旧S10「限界と次の一手」）・S10（旧S11「オープンデータ」）・S11（旧S12「ループ図」）は、SHA256はページ番号の描画差分により完全一致しないが、目視で本文・図が12枚版の対応スライド（旧S10・S11・S12）と同一であり、ページ番号のみが繰り上がっていることを確認した（元のS9「再訪」が削除され後続が1つ前にずれている）。両版とも文字切れ・重なり・スライド外への逸脱は見つからなかった。

### 6.2 グレースケール確認

`pdftoppm` で生成した12枚版のPNG（100dpi）を Pillow の `Image.convert("L")` でグレースケール化し、各スライドを目視した。水域／陸域、訪問地点／検出、コールアウト／本文の区別ができるかを重点的に確認した。

```python
# グレースケール変換（Pillow）
from PIL import Image
import glob, os
for path in sorted(glob.glob("/tmp/t7/a-*.png")):
    Image.open(path).convert("L").save(f"/tmp/t7/gray/{os.path.basename(path)}")
```

| 確認対象 | スライド | 結果 |
|---|---|---|
| 水域（海）と陸域の区別 | S5 右下パネル "Final mask" | 海（元は青、RGB≈(13,70,160)）はグレー値63、陸（元は緑、RGB≈(73,124,68)）はグレー値102。差約39段階で区別可能 |
| 検出ポリゴンと背景の区別 | S6・S7(c)・S8 の分布図 | 検出ポリゴン（青）はグレー値64〜66、背景（ベージュまたは白）はグレー値241〜255。差150段階以上で明確に区別可能 |
| 訪問地点マーカーと検出ポリゴンの区別 | S8 | 訪問地点の三角マーカー（黒、グレー値53）と検出ポリゴン（青、グレー値64）はグレー値の差が約11段階と小さいが、マーカーの形状（塗りの三角形＋ラベルへのリーダー線）と検出ポリゴン（小さな不定形の点群）が視覚的に異なり、凡例のテキスト（"Georeferenced visit anchors" / "Detected water polygons"）でも区別できる。色のみに依存した区別ではないことを付記する |
| コールアウトと本文の区別 | S6・S8 | "145"・"5–6" のコールアウトは色を落としても本文よりはるかに大きく太いフォントのため、グレースケールでも本文との区別は明確 |
| 水面と岩壁の区別（現地写真） | S3 | 右写真: 水面グレー値30・岩壁グレー値98（差68）。左写真: 水面グレー値113・岩壁グレー値83（差30、写真ごとに明暗の向きは異なるが質感の違いで区別可能） |

S1・S2・S4・S9〜S12 は上記のような色分けされた対比要素を持たない（文字・写実的な写真・線図のみ）ため、グレースケール化による情報欠落はない。全12枚を通じて、区別が失われたスライドは無かった。ただし S8 の訪問地点マーカーと検出ポリゴンの区別は、グレー値の差だけでは弱く、形状と凡例テキストに依存している点を記録として残す。

### 6.3 英語通し読み時間 — 算出値であり実測ではない

**この節の秒数は、EN ノート本文の語数を145 wpmで換算した算出値である。人間が声に出して読み上げた実測ではない。** 実測は登壇前に発表者自身が行う必要があり、本書はそのためのチェックリストを6.3.2に示す。

#### 6.3.1 語数と算出秒数（145 wpm換算）

検査スクリプト `validate_exp002_kitagi_foss4g2026_presentation.py` の `count_en_words()`（アルファベットで始まる語のみを数え、`145`のような数字のみのトークンは数えない）と同じロジックで、スピーカーノートMarkdown（`exp002_kitagi_foss4g2026_presentation_speaker_notes.md`）のEN本文を数えた。

| S | 内容契約の時間割 | 割当語数（145wpm換算） | EN語数（算出） | 算出秒数（語数÷145×60） | 割当語数からの差 |
|---|---:|---:|---:|---:|---:|
| 1 | 0:35 | 85 | 90 | 37.2秒 | +5.9% |
| 2 | 1:40 | 242 | 234 | 96.8秒 | −3.3% |
| 3 | 1:30（3–4で3:00） | 218 | 240 | 99.3秒 | +10.1% |
| 4 | 1:30（3–4で3:00） | 218 | 230 | 95.2秒 | +5.5% |
| 5 | 1:50 | 266 | 306 | 126.6秒 | +15.0% |
| 6 | 2:30 | 362 | 358 | 148.1秒 | −1.1% |
| 7 | 1:10 | 169 | 165 | 68.3秒 | −2.4% |
| 8 | 1:30 | 218 | 248 | 102.6秒 | +13.8% |
| 9 | 1:50 | 266 | 277 | 114.6秒 | +4.1% |
| 10 | 1:20 | 193 | 185 | 76.6秒 | −4.1% |
| 11 | 1:10（11–12で2:05） | 169 | 146 | 60.4秒 | −13.6% |
| 12 | 0:55（11–12で2:05） | 133 | 129 | 53.4秒 | −3.0% |
| **合計** | **17:30（1,050秒）** | **2,539** | **2,608** | **1,079.2秒（17:59）** | **+2.7%** |

いずれのスライドも検査スクリプトの許容幅（割当語数の±25%）以内であり、`validate_...py` は「OK: 466 checks passed」で通過している（6.4節）。**S6単体は算出358語・148.1秒（2:28）で、ハードゲートの2:30（150秒）に対して1.9秒の余裕がある。** 全体の算出合計17:59は目標17:30に対して+29秒（+2.8%）で、20分枠（質疑5分・入替5分を除く発表20分）に対しては十分な余裕がある。

#### 6.3.2 発表者が声に出して計測するためのチェックリスト

以下は登壇前に発表者自身が実施するべき、実測のためのチェックリストである。本書のどの数値も実測を代替しない。

- [ ] 各スライドを声に出して読み、上表の「内容契約の時間割」列（秒）に対する実測秒数を記録する
- [ ] **S6単体を実測し、2:30（150秒）以内に収まることを確認する。** 超過した場合は、S6の情景描写（分布説明以外の部分）からEN本文の文を削る。投影文字列（スライド上のテキスト）は変更しない
- [ ] 本編合計を実測し、17:30前後（20分枠に対しバッファ2:30）に収まることを確認する
- [ ] 超過した場合は、投影文字列ではなくEN ノートの文を削ることを徹底する（削るスライドは合計への寄与が大きいスライド、特にS3・S4・S5・S8のように算出値が割当より10%以上大きいスライドを優先的に見直す）
- [ ] 実測結果を得たら、本節（6.3）に実測秒数を追記し、「算出値」ではなく「実測値」として記録し直す

### 6.4 全検査の再実行（機械検査）

```bash
uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py
uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py
uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py --no-revisit
uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py
```

結果: `OK: 466 checks passed`。上記4コマンドの実行後に `git status --short` を確認したところ、差分は無かった（生成物は実行時刻に依存せずバイト単位で再現される）。すなわち `docs/presentations/` 配下の全生成物（PPTX 2種・図版4点）は再実行前と再実行後でバイト単位で一致した。

### 6.5 登壇前に残っている作業

- **S9の2枚の写真は依然プレースホルダーである。** 差し替え手順は「8月31日以降の差し替え手順」節（ブリーフ）どおり: (1) 撮影した写真を `docs/presentations/images/revisit_1.jpg` / `revisit_2.jpg` として配置する（固定寸法スロットに合わせて中央クロップされる）、(2) `uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py` を再実行する、(3) 本書 3章の8/31撮影記録テーブル（座標・撮影時刻・撮影方向・対象ポリゴンID）を実測値で埋め、スピーカーノート・内容契約に残る `[UPDATE AFTER 2026-08-31]` の申し送りを除去する
- **現地確認（8月31日の再訪）が実施できなかった場合は、11枚版（`exp002_kitagi_foss4g2026_presentation_no_revisit.pptx`、S9を除く）を本番として使用する**
- **英語通し読みの時間は未実測である。** 6.3節の秒数はすべて145wpmからの算出値であり、発表者本人が声に出して計測するまでは実測値として扱わない
