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
| **9 px**（NDVIマスクによる除外画素数） | 発話のみ: S6 required spoken content（"The NDVI vegetation mask removed only nine pixels"）、S10 EN本文（"The mask changed only nine pixels in this run"）。投影本文には数値を置かない | 報告書 表4-2「植生マスクにより除外 9 px」（§4.2）。仮説3の検証根拠。精度への効果は未評価（§5.1） |
| **100 m²**（最小報告ポリゴン面積） | 投影: S5（"Minimum reported polygon area: 100 m²"）・S6（"intra-island water polygons ≥ 100 m²"） | 報告書 §3.4「水域ポリゴンは100m²以上のもののみを抽出した」 |
| **10 m**（解析グリッド／Sentinel-2の分解能） | 投影: S5（"10 m analysis grid"、"at 10 m a narrow pond is..."）・S10（"10 m resolution — ponds narrower than about 10 m are unreliable"） | 報告書 §3.2（B02/B03/B04/B08の分解能10m）・§3.4（10mグリッドでの複合判定） |
| **20 m**（B11短波長赤外バンドの元解像度） | 発話のみ: S5 EN本文（"The short-wave band arrives at twenty metres, so I resampled it to ten"）。投影本文には置かない | 報告書 §3.2「B11（20m分解能）はバイリニア補間により10m分解能にリサンプリングした」 |
| **1.28 ha**（春季・島内最大水域面積） | 発話のみ: S6 required spoken content（"The largest was one point two eight hectares"） | 報告書 表4-1「島内最大水域面積 1.28 ha」（§4.1） |
| **7,826 m²**（夏季・島内最大水域面積） | 発話のみ: S6 required spoken content（"largest was seven thousand eight hundred and twenty-six square metres"） | 報告書 表4-2「島内最大水域面積 7,826 m²」（§4.2）。公開GeoJSONの `area_m2` 実測値は最大 7825.5（本書執筆時に算出、2章参照）で、報告書の 7,826 は四捨五入値。両者が同一ポリゴンであることは、面積の近さだけでなく重心座標の一致によって直接確認した（1.2節参照） |
| **2025-03-23**（春季シーン撮影日） | 投影: S6（小タイル "Spring 2025-03-23 — 113 polygons reported"）。発話: S6 required spoken content（"the twenty-third of March 2025"） | 報告書 §3.2 表「春季画像 撮影日 2025-03-23」（シーンID `S2C_MSIL2A_20250323T014711`） |
| **2025-08-02**（夏季シーン撮影日） | 投影: S5（"Summer 2025-08-02"）・S6（"summer 2025-08-02"）。発話: S6 required spoken content | 報告書 §3.2 表「夏季画像 撮影日 2025-08-02」（シーンID `S2A_MSIL2A_20250802T015121`）。公開GeoJSONのファイル名にも同日付 |
| **0.0%**（春季シーン雲量） | 発話のみ: S6 required spoken content（"Its reported cloud cover was zero point zero percent"） | 報告書 §3.2 表「春季画像 雲量 0.0%」 |
| **0.7%**（夏季シーン雲量） | 投影: S5（"0.7% cloud"）。発話: S6 required spoken content | 報告書 §3.2 表「夏季画像 雲量 0.7%」 |
| **−0.2**（NDWI閾値） | 投影: S5（合成条件 "Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)"） | 報告書 §3.4「水域マスク = (NDWI > -0.2 OR MNDWI > -0.1) AND NOT (NDVI > 0.3)」 |
| **−0.1**（MNDWI閾値） | 投影: S5（同上の合成条件） | 報告書 §3.4（同上） |
| **NDVI > 0.3**（NDVI植生マスク閾値） | 投影: S5（同上の合成条件） | 報告書 §3.4（同上）・図4-2のヒストグラム（谷の位置） |

### 1.1 式についての注記（ルーリング）

- **投影されるのは合成条件（閾値付きの規則）である。** `"Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)"` は S5 の投影本文のテキストフレームに文字列として置かれている（生成スクリプト `exp002_kitagi_foss4g2026_presentation.py` の `s05()`、508行目付近）。
- **投影されないのは各指数の個別定義式である。** `NDWI = (Green − NIR) / (Green + NIR)` 等（報告書 §3.3）は、投影本文には置かず、図版 `p05_index_panels.png`（ポスター図版 `poster_f4_index_panels.png` のパネル画像から再構成）のパネル内注記としてのみ存在する。この切り分けは検査済み（`validate_..._presentation.py` の `check_evidence_hierarchy()` が `"(Green − NIR)"` 等が投影本文に無いことを確認する）。個別定義式は S5 の発話本文で「NDWI is built from the green band and the near-infrared band」のように言葉で説明する（内容契約 Slide 5・スピーカーノート S5参照）。

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
| `aerial_quarry_pond.jpg` | コピー元: `docs/results/exp002/photos/01.jpg`（著者提供の色付き原本、1080 x 1440 px）。**macOS の Dock（上端 y=1319）と「Pages」ツールチップ（上端 y=1244）を投影面に出さないため、上から 1230 行だけを切り出したもの**（1080 x 1230 px、下記2.5参照） | `5262eff47363798e4aff1bd3cf0c450a50bff8cb2d9176d391d517bdcdd49467` | S4（左、クロップなし）・S7パネル(b)の原画像（16:9へ `vbias=0.25` で縦クロップ） |
| `basemap_kitagi_carto_positron.png` | 取得元: CARTO Positron ラベルなし `https://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png`（contextily の `cx.providers.CartoDB.PositronNoLabels` と同一タイル、ズーム17、範囲 west 133.514 / south 34.367 / east 133.562 / north 34.402、取得日 2026-08-24）。取得は `exp002_kitagi_foss4g2026_figures.py --fetch-basemap` で一度だけ行い、以後はこの追跡ファイルを読むのみ（下記2.4参照） | `ecefa612a4f3b2449b08d7488ad0e09776b41e63421b94cd8dc5f5d89b291811` | （直接配置せず）P6・P7パネル(c)・P8 の背景地図 |
| `choba_lake_1.jpg` | コピー元: `docs/results/exp002/photos/choba_lake_1.jpg`（著者撮影、バイト一致確認済み） | `df0c227a8100895ac850978393c94ef960e662bc18f8694feda1462ad22a5d3a` | S3（右） |
| `choba_lake_3.jpg` | コピー元: `docs/results/exp002/photos/choba_lake_3.jpg`（著者撮影、バイト一致確認済み） | `fc76d7fa21c77ed0b4ecff470860b8f767fd1a7e0a0844e79338ffa47afffb8e` | S1（表紙）・S7パネル(a)の原画像 |
| `drone_lake_stage.jpg` | コピー元: `docs/results/exp002/photos/02.jpg`（著者提供の色付き原本、1080 x 1440 px、無加工のコピー） | `a458369e6601199c6e95819733f36dfa6fc3848826bbf5ceb0361c60294df94f` | S4（右、`vbias=0.0` で下側を縦クロップ） |
| `fig01_lake_stage.jpg` | コピー元: `docs/articles/2026_chiri-koryu-10/figures/fig01_lake_stage.jpg`（著者撮影・記事図版と共有、バイト一致確認済み） | `02da83402c64be3ed06acfefdb5f324c204428350e82b9534bfe4ad4303761ae` | S3（左） |
| `p05_index_panels.png` | 生成元: `docs/presentations/exp002_kitagi_foss4g2026_figures.py` の `make_p05_index_panels()`（入力: `poster_f4_index_panels.png` のパネル画像4枚の切り出し。ラスタは無加工で、英語ラベルとカラーバーのみ大きく再描画。下記2.3参照） | `0baee6fe35ec978d91567fe8688d43272ded0304400c8713addff3469faab4c7` | S5 |
| `p06_clusters_map.png` | 生成元: `docs/presentations/exp002_kitagi_foss4g2026_figures.py` の `make_p06_clusters_map()`（入力: 公開GeoJSON（SHA256は下記2.1参照）＋ `basemap_kitagi_carto_positron.png`） | `4265014970f552cf00cb21077693c84b61242fbc0bb3391a87072a0f75302f27` | S6 |
| `p07_three_scales.png` | 生成元: 同スクリプトの `make_p07_three_scales()`（入力: `choba_lake_3.jpg`・`aerial_quarry_pond.jpg`・公開GeoJSON＋`basemap_kitagi_carto_positron.png`。英語ラベルのみの発表専用合成図） | `1ccef8ea68c72069132da7dc3294cfcb87224c667ce15d3fce3328349752c9fe` | S7 |
| `p08_visit_anchors_map.png` | 生成元: 同スクリプトの `make_p08_visit_anchors_map()`（入力: 公開GeoJSON＋訪問記図4の座標確認済み4地点＋`basemap_kitagi_carto_positron.png`） | `87c186fed32ee4ebec8516438b33dfec3a0472129ecc7d82e77179a5d44f14c0` | S8 |
| `p12_loop_diagram.png` | 生成元: 同スクリプトの `make_p12_loop_diagram()`（新規作図、外部入力なし） | `d7d389b2fdc97829f427cdd29b25339ab16c9bf2113dce8cf9c7da9ad21ea45e` | S12 |
| `placeholder_revisit_1.png` | 生成元: 記録なし（一回性の生成物。生成スクリプトは保存されていない）。8/31撮影分の実写に差し替えるまでの仮画像 | `f9a9175dd22b98cb607f5f67e1f0d1c84aa77b675aea26e96e35d6bccdd4ea33` | S9（左、実写未着手のため使用中） |
| `placeholder_revisit_2.png` | 生成元: 同上。`placeholder_revisit_1.png` とバイト単位で同一（同一手順で生成された仮画像） | `f9a9175dd22b98cb607f5f67e1f0d1c84aa77b675aea26e96e35d6bccdd4ea33` | S9（右、実写未着手のため使用中） |
| `poster_f1_study_area.png` | コピー元: `docs/posters/figures/exp002/poster_f1_study_area.png`（バイト一致確認済み） | `05880cde6a1cf2362a36d266d1fa8af0942fb0e92c269cb33fa50a2dab29230e` | S2 |
| `poster_f4_index_panels.png` | コピー元: `docs/posters/figures/exp002/poster_f4_index_panels.png`（バイト一致確認済み） | `81b9b5dc9f1dffc38369606f3e2a5c91d21e75c63839972be577f761d57fc16a` | （直接配置せず）`p05_index_panels.png` の入力 |
| `poster_qr_repo.png` | コピー元: `docs/posters/figures/exp002/poster_qr_repo.png`（バイト一致確認済み） | `ff635ba17127bfca3ca228350a3b4b15b28c1925c1d640891aee1595b75880ee` | S11 |

### 2.1 P6・P7・P8・P12 の入力データ

新規図版5点（P5・P6・P7・P8・P12）は `docs/presentations/exp002_kitagi_foss4g2026_figures.py` が公開GeoJSON（および P7 は既にリポジトリにある写真2点）を入力として生成する（`tmp/`・ネットワークアクセスに依存しない）。

- 入力: `docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson`
- SHA256: `c0b63dbdff47377731ef1fa9103e31df0414692c87aec73a9779c9dfd2121de8`
- 本書執筆時に実測: `features` 数 145、`area_m2` 最大値 7825.5（1.1節の 7,826 m² との差の注記を参照）

### 2.2 記録から意図的に除外した画像（削除済み・不採用）

以下は現在 `images/` に存在しないが、設計レビュー・是正での不採用の経緯を記録として残す（ブリーフが名前での言及を要求している）。

- **`fig03_keirin_cliff.jpg`**（日本語記事用にグレースケール化された図版）: S1表紙・S7パネル(a)の初期案として使われていたが、色付きの現地写真であるべきという判断（本書「4. 意図的に境界を引いた主張」参照）により `choba_lake_3.jpg`（色付き）へ差し替え、参照が無くなったコピーを `images/` から削除した（コミット `031cfef`「fix: S1表紙・S3写真をグレースケール記事図版から色付き原本に差し替え」）。記事側の原本（`docs/articles/2026_chiri-koryu-10/figures/fig03_keirin_cliff.jpg`）は無変更で存在する
- **`fig09_multiscale.png`**（日本語記事と共有される三スケール合成図。日本語キャプション焼き込み・動画UI写り込みあり）: S7の英語専用面という契約に抵触するため不採用とし、発表専用の `p07_three_scales.png`（英語ラベルのみ）に差し替え、参照が無くなったコピーを削除した（コミット `2fe3ba0`「fix: S7の英語のみ違反を解消（fig09_multiscale→p07_three_scales差し替え）」）

- **`fig05_drone_takeoff.jpg` / `fig06_aerial_quarries.jpg`**（いずれも日本語記事用にグレースケール化された図版。mode L で無彩色）: S4（2枚）と S7パネル(b) に使っていたが、2026-08-24 に発表者から色付き原本（`docs/results/exp002/photos/01.jpg`・`02.jpg`）の提供を受けたため `aerial_quarry_pond.jpg` / `drone_lake_stage.jpg` へ差し替え、参照が無くなったコピーを `images/` から削除した。記事側の原本（`docs/articles/2026_chiri-koryu-10/figures/`）は無変更で存在し、`scripts/build_chiri_koryu_figures.py` は引き続きそちらを参照する

- **`basemap_kitagi_gsi_seamlessphoto.png`**（地理院タイル「全国最新写真」z17 のモザイク、18.3 MB）: 2026-08-24 の第1波で P6・S7パネル(c)・P8 の背景地図として採用したが、**同日中に撤回した**。理由は (1) S7 の三スケール合成図でパネル(b)「上空から」とパネル(c)「衛星から」の対比が壊れる、(2) 実際の丁場池が写った写真の上に検出結果を載せると ground truth と読まれ、精度指標を持たないという主張境界に反する——の2点である（付随的に、実写は PNG が圧縮されず容量も大きかった）。ラベルなしの淡色地図 `basemap_kitagi_carto_positron.png` へ差し替え、参照が無くなったラスタを `images/` から削除した（本書2.4節参照）

### 2.3 P5（指数4パネル）の由来と、ポスター図版を直接使わない理由

S5 の指数4パネルは、ポスター図版 `poster_f4_index_panels.png` を**そのまま配置していない**。

- 理由: この図版の図中フォントは native 18 pt、実寸 8.82 × 8.50 in である。図中文字が
  スライド上で15 pt に見えるには配置高さ 7.09 in が必要で、16:9スライドの全高 7.5 in から
  タイトル帯を引いた領域には収まらない。**配置をどう拡大しても下限を満たせない**
- 元データ（Sentinel-2 バンドのラスタ）はリポジトリに無く、生成元
  `scripts/generate_exp002_poster_figures.py` の `make_f4_index_panels(res)` は
  ネットワーク取得したラスタを必要とするため、より小さい実寸での再生成もできない
- そこで `make_p05_index_panels()` が、既にリポジトリにある PNG から4枚のパネルの
  **ラスタ部分のみを切り出し**、英語ラベル（文字列・カラーマップ・値域・目盛りは
  ポスター側と同一）とカラーバーを大きく描き直す。ラスタは切り出しと表示時の縮小のみで、
  描かれているデータはポスターと同一である
- 切り出し座標が別のファイルに適用されないよう、生成関数は入力PNGの SHA256
  （`81b9b5dc9f1dffc38369606f3e2a5c91d21e75c63839972be577f761d57fc16a`）を検査してから
  切り出す。切り出し箱の各辺が白い帯を含まないことも実測で検査する

### 2.4 背景地図（CARTO Positron）の出典・範囲・取得日と、他のタイルを使わなかった理由

検出地図（P6・S7パネル(c)・P8）は、検出ポリゴンが島のどこにあるのかを海岸線との関係で
読めるよう、**文字を一切含まない淡色の地図**を最下層に敷く。

| 項目 | 値 |
|---|---|
| タイルURL | `https://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png`（CARTO Positron ラベルなし。contextily の `cx.providers.CartoDB.PositronNoLabels` と同一タイル。`{s}` サブドメインは `a` に固定、Retina 版は使わない） |
| ズームレベル | 17（プロバイダの最大は 20） |
| 範囲（west, south, east, north） | 133.514, 34.367, 133.562, 34.402（EPSG:4326。図版の地図軸 `MAP_BBOX` と厳密に一致） |
| 保存画素数 | 4,474 × 3,953 px（地上分解能約 1.0 m/px。出力1pxあたり2.4px） |
| 取得日 | 2026-08-24 |
| 取得タイル数 | 304 枚（全球を覆うプロバイダのため欠測なし。404 は取得コードで即座に失敗させる） |
| 追跡ファイル | `docs/presentations/images/basemap_kitagi_carto_positron.png`（0.95 MB） |
| 帰属表示 | `Basemap: © OpenStreetMap contributors, © CARTO`（P6・P8 は native 22pt、P7パネル(c) は native 11pt で図版内左上に焼き込み。実効 11.3〜11.4pt でフッター階層と同じ） |

**他のタイルを使わなかった理由**

- 地理院タイル英語版 `xyz/english/`: **ズームレベル 5〜11 しか存在しない**（z12 以上は 404。
  2026-08-24 に実測して確認）。z11 の地上分解能は約 76 m/px で、地図範囲（幅 5,343 m）は
  わずか 70 px にしかならない。出力図版の地図軸は約 1,850 px 幅であり、「出力1pxあたり2px以上」
  （＝3,700 px 以上）に対して 1/50 以下で、拡大すれば著しくぼやける
- 淡色地図 `pale`・標準地図 `std`（z18まで）・白地図 `blank`（z14まで）: **日本語地名**
  （北木島・豊浦・大浦 等）が焼き込まれている。投影面は英語のみという制約に反する
- 陰影起伏図 `hillshademap`（z16まで）・色別標高図 `relief`（z15まで）: 文字は無いが解像度不足
  （2,237 px / 1,118 px）
- **全国最新写真 `seamlessphoto`（z18まで、航空写真）**: 文字が無く解像度も足りるため
  2026-08-24 の第1波でいったん採用したが、同日の是正で撤回した。理由は2つある。
  (1) **S7 の物語と衝突する。** S7 は「(a) 歩いて＝質感 / (b) 上空から＝境界 / (c) 衛星から＝分布」
  の三スケール合成図であり、パネル(c) の下に航空写真を敷くとパネル(b) と見分けが付かなくなって
  スライドの主旨が壊れる。(2) **ground truth と読まれる。** 本発表の主張境界は「検出は候補で
  あり、ground truth も精度指標も持たない」ことである。実際の丁場池が写った航空写真の上に
  検出結果を載せると「目視で検証済み」と受け取られ、「池が見えるなら指数は不要では」という
  誤解も招く。加えて実写は PNG が圧縮されず、追跡ラスタ 18.3 MB・PPTX 各 13.0 MB を招いていた
- **採用: CARTO Positron ラベルなし（`light_nolabels`）**。ラベルを一切含まないので
  「投影面は英語のみ」を（英語版タイルを指定した本来の理由と同じ根拠で）満たし、z20 まで
  あるので解像度も満たす。海岸線と道路が読めるため発表者の依頼（島のどこにあるか）に直接応え、
  ベクタ由来のフラットなラスタなので実写と違い PNG が十分に圧縮される（0.95 MB）。
  写真ではないので ground truth とは読まれない

**減光とグレースケール確認**

DESIGN_GUIDE §7.3（背景地図を薄くし、主題データとの視覚的競合を避ける）に従い、
`出力 = 255 - (255 - 入力) × KEEP` の整数演算で減光する（実行ごとに完全に同じ値になる）。
Positron は元から淡い（実測: 海 = 輝度 216 が全体の 51.9%、陸 = 241 が 37.8%、道路 = 250 前後）
ため、写真基図に使っていた `KEEP = 0.30` をそのまま当てると全画素が 243 に潰れ、
海陸差が約 25 階調から約 3 階調に落ちて**海岸線が消える**（実測）。そこで **`KEEP = 0.80`**
へ再調整した。減光後の最小輝度は 222（グレースケール変換後も 222）で、検出ポリゴンの色
`COL_WATER = #0d47a1`（グレースケール輝度 64、透過 0.95 で背景と合成しても約 71）とは
**158階調**離れている（写真基図のときは 115階調）。海陸差は約 20 階調残り、海岸線・道路が読める。
P6・P7・P8 の各図版を Pillow の `.convert("L")` でグレースケール化して目視し、水域ポリゴンが
最も目立つ要素であり、かつ島の海岸線が判別できることを確認した（本書6章に記録）。

**再生成時のネットワーク非依存**

図版生成（`exp002_kitagi_foss4g2026_figures.py` の通常実行）はこの追跡ラスタを読むだけで、
ネットワークへはアクセスしない。取得系のモジュール（`mercantile` / `urllib`）は
`fetch_basemap()` の内側でのみ import する。ラスタが無い場合は
`load_basemap()` が `FileNotFoundError` で明示的に失敗し、`--fetch-basemap` の再実行を促す
（黙って背景地図なしの図版を出力しない）。画素数が `BASEMAP_EXPECTED_PX` と異なる場合も
assert で失敗する。

### 2.5 S4・S7パネル(b) の色付き原本と、`01.jpg` から取り除いた画面UI

2026-08-24、発表者から S4 用の色付き原本2点の提供を受けた。従来使っていた記事図版
（`fig05_drone_takeoff.jpg`・`fig06_aerial_quarries.jpg`）は印刷用にグレースケール化された
ものだったため、これを置き換えた（本書4章「S1・S3は色付き原本、上空写真はグレースケール」の
裁定は、色付き原本が存在しないという前提が崩れたので更新した）。

| 原本 | 内容 | SHA256 | 画素数・モード |
|---|---|---|---|
| `docs/results/exp002/photos/01.jpg` | 丁場池を上空から見た構図（**パソコン画面を撮影した写真**） | `f2811e248d50e2529b0b31ef2a1261ded74b5854fd02e78633b93ca3344840e6` | 1080 x 1440、RGB |
| `docs/results/exp002/photos/02.jpg` | 湖上ステージ上のドローン2機 | `7cdf0340d1689232ea6636ad3555f217b72afc9be63dd28ec82f4cb68431d8fc` | 1080 x 1440、RGB |

**`01.jpg` から取り除いた画面UI**

`01.jpg` はパソコンの画面を撮影した写真であり、下端に macOS の Dock、その少し上に
「Pages」というツールチップが写り込んでいる。どちらも投影面に出してはならない。
行ごとの彩度プロファイル（Pillow で実測）と拡大目視により、以下の位置を特定した。

| 要素 | 画像内の位置（1440 行中） | 高さ比 |
|---|---|---|
| 「Pages」ツールチップ（吹き出しの上端〜先端） | y ≈ 1244〜1310 | 86.4%〜91.0% |
| macOS Dock（帯の上端。画面を斜めから撮っているため左 1319・右 1347 と傾く） | y ≈ 1319 以降 | 91.6% 以降 |

上端がより高い（＝より上にある）のはツールチップの y=1244 なので、**y=1230 で切り落とした**
（余裕 14 px）。追跡ファイル `docs/presentations/images/aerial_quarry_pond.jpg` は
この切り出し後の 1080 x 1230 px であり、UI は追跡ファイルの時点で存在しない。
表示側のクロップ（S4 のスロット比、S7 パネル(b) の 16:9）をどう変えても UI が
再出現しないのは、この「元ファイルの時点で除去する」設計によるものである。
切り出しコマンド（一回性。`images/` への他の画像のコピーと同じ扱い）:

```python
from PIL import Image
Image.open("docs/results/exp002/photos/01.jpg").crop((0, 0, 1080, 1230)).save(
    "docs/presentations/images/aerial_quarry_pond.jpg", quality=95, subsampling=0)
Image.open("docs/results/exp002/photos/02.jpg").save(
    "docs/presentations/images/drone_lake_stage.jpg", quality=95, subsampling=0)
```

**S4 のレイアウト変更（16:9横長スロット → 縦長スロット2枚）と実測**

新しい2枚はいずれも縦位置（`aerial_quarry_pond.jpg` は 1080/1230 = 0.878、
`drone_lake_stage.jpg` は 0.75）で、従来の 16:9 スロット（5.60 x 3.15 in）に収めると
各フレームの 58% を捨てることになる。S4 の主張は「上空から見ると採石権の境界が地形として
読める」であり、それには縦方向の広がりが必要なため、スロットを縦長にして本文列と左右に
並べるレイアウトへ変更した。実測値:

| 量 | 値 |
|---|---|
| 図版帯（タイトル下〜フッター手前） | 12.233 x 4.800 in |
| 縦長スロット（1枚） | 3.866 x 4.400 in（縦横比 0.878 = `aerial_quarry_pond.jpg` の実比） |
| 写真帯（2枚 + 間隔 0.200 in） | 7.933 in |
| 本文列 | 4.000 in（= 12.233 − 7.933 − 0.300 の画像・本文間隔） |
| 写真の上下位置 | 上 2.400 in / 下 6.800 in（図版帯 2.200〜7.000 in の内側） |

すなわち、縦長スロット2枚は本文と重ならず、スライド外にも出ない。写真は引き伸ばさず、
スロット比へのクロップのみで配置する（`add_picture_cover()`）。
左（`aerial_quarry_pond.jpg`）はスロット比が実比と一致するためクロップは生じない。
右（`drone_lake_stage.jpg`）は 14.6% を縦方向に落とす必要があり、被写体（岩壁・水面・機体2機）が
上 65% に収まっているため全量を下側から取る（`vbias=0.0`、板張りの床のみを落とす）。
S3・S9 の 16:9 固定スロット（`PHOTO_SLOT_W_IN` / `PHOTO_SLOT_H_IN`）は変更していない。

**S7 パネル(b) のクロップ**

P7 は3パネルを同じ高さで横並びにする図版なので、パネル(b) は横長のままである
（16:9、`P07_PANEL_B_AR`）。`aerial_quarry_pond.jpg`（1080 x 1230）を 16:9 にするには縦 622 px を
落とす必要があり、vbias 0.10 / 0.25 / 0.40 / 0.55 の試作を目視比較して、丁場池の水面が中央に、
左右の切削面（灰色の岩壁と傾いた花崗岩のスラブ）がともに入る **0.25**（画像の 156〜763 行）を
選んだ。

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
| 指数の合成条件は投影、個別定義式は発話・図版内 | S5投影本文には閾値付きの合成条件（`Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)`）を置くが、`NDWI = (Green − NIR) / (Green + NIR)` 等の個別定義式は投影本文に置かず、発話とfigure内注記（`p05_index_panels.png`）に限る | 本書1.1節、`exp002_kitagi_foss4g2026_presentation.py` の `s05()` コメント、validator `check_evidence_hierarchy()` |
| 投影する現地写真はすべて色付き原本 | S1表紙・S3・S4 の現地写真はすべて色付きの原本を使う。2026-08-23 時点では上空写真の色付き原本が存在しなかったため S4 のみグレースケールの記事図版（`fig05_drone_takeoff.jpg`・`fig06_aerial_quarries.jpg`、mode L）を使っていたが、2026-08-24 に発表者から色付き原本の提供を受けたので差し替え、参照の無くなったコピーを削除した。現在 `images/` にある投影用の現地写真はすべて mode RGB である | 内容契約 S1・S3・S4 の Visual 注記、本書2.5節、validator `PINNED_PHOTO_SOURCES` |
| 背景地図はラベルなしの淡色**地図**（写真は使わない） | 検出地図（P6・S7パネル(c)・P8）の背景地図は CARTO Positron のラベルなしタイル（`light_nolabels` z17）を使う。地理院タイル英語版は z11 までしか存在せず島の縮尺では著しくぼやけるため使えず、日本語地名を含む淡色地図・標準地図・白地図は投影面が英語のみという契約に抵触する。**航空写真（`seamlessphoto`）は 2026-08-24 の第1波で採用したが同日に撤回した**（S7 のパネル(b)「上空」とパネル(c)「衛星」の対比が壊れる／実写の池の上に検出結果を載せると ground truth と読まれ、精度指標を持たないという主張境界に反する）。以後、この図版群に写真基図は使わない | 本書2.4節、内容契約 S6・S7・S8 の Visual 注記 |
| 帰属表示はフッター階層 | 図版内の帰属表示（`Basemap: © OpenStreetMap contributors, © CARTO`）は本文でも主題ラベルでもないため、15pt下限ではなくフッター階層（実効11〜12pt）に従う。S11 フッターが基図の帰属表示を 11pt で置いている前例に合わせる | 内容契約「実装時のハードゲート」節、`exp002_kitagi_foss4g2026_figures.py` の `BASEMAP_CREDIT_PT_MAP` |
| 帰属表示は実際に使った基図に従う | 図版内・フッターの基図帰属は、デッキが実際に使っている基図だけを挙げる。S2 の位置図（`poster_f1_study_area.png`、`scripts/generate_exp002_poster_figures.py` が地理院タイル英語版 z8/z11 で描画）は GSI Tiles、S6・S7パネル(c)・S8 の検出地図は `© OpenStreetMap contributors, © CARTO`。S11 フッターはこの2つを挙げ、それ以外は挙げない | `exp002_kitagi_foss4g2026_presentation.py` の `s11()`、本書2.4節、内容契約 S11 Projected body |
| S7は英語専用の三スケール合成図 | S7には発表専用に新規生成した `p07_three_scales.png`（英語ラベルのみ）を使い、日本語記事と共有される `fig09_multiscale.png`（日本語キャプション焼き込み・動画UI写り込み）は使わない | 内容契約 S7 Visual 注記、本書2.2節 |
| 再訪は現地確認の開始であり検証ではない | 8月31日の再訪は"a first look, not validation"であり、サンプリング設計されたaccuracy validationではない。写真は候補地点の存在を示すのみで、正誤の集計や丁場の同定は行わない | 内容契約 S9 Notes-only boundary・「8月31日の撮影に向けた事前準備」節、本書3章 |
| OSMへの還元は今後の計画 | OpenStreetMapへの地物追加は今後の計画として述べ、既に還元したとは述べない。追加するのは現地で確認できたものに限る | 内容契約「主張境界」節・S12 Notes-only boundary、S12投影本文（"I plan to contribute the ponds I can confirm."） |

## 5. 生成コマンド

以下はすべて `uv run python` 経由で実行する（リポジトリ規約）。図版・PPTX・検査スクリプトはこの順に再実行すればバイト単位で再現される決定的な出力を生成する（各スクリプトのdocstringに再現性の明記あり）。

```bash
# 0. 背景地図の取得（ネットワークを使う唯一の経路。取得済みなら再実行不要）
uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py --fetch-basemap

# 1. 新規図版（P5・P6・P7・P8・P12）を images/ に生成（ネットワーク非依存）
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
| 2 | 島と遺産 | 問題なし（2026-08-24 再確認）。位置図を実寸の1.04倍まで拡大したため本文列は約3.8in・16ptになったが、本文7行（折り返し後14行）は下端に余裕を残して収まり、地図の島名ラベルは投影サイズで判読できる。地図同士・本文との重なりなし |
| 3 | 徒歩スケール | 問題なし。左右2枚の写真が等幅で並び、下端・右端ともにスライド内 |
| 4 | 上空スケール | 問題なし。左右2枚のグレースケール写真がスライド内に収まる |
| 5 | 衛星スケール（手法） | 問題なし（2026-08-24 再確認）。図版を `p05_index_panels.png` に差し替え。右側2×2パネル（NDWI/MNDWI/NDVI/Final mask）のタイトルとカラーバー目盛りが投影サイズで判読でき、パネル同士・本文とも重ならない |
| 6 | 主結果（145） | 問題なし（2026-08-24 再確認）。図版配置高さを4.8inへ拡大し図中文字を32ptへ引き上げた。4地区ラベル（north/west/centre/south-east）は互いに重ならず軸内に収まり、投影サイズで判読できる。左の "145" コールアウト・本文・脚注（Copernicusクレジット）との干渉なし |
| 7 | 三スケール合成 | 問題なし。(a)(b)(c) 3パネルと "1 km" スケールバーがスライド内、パネル同士の重なりなし |
| 8 | 訪問5〜6か所と検出145件の規模の対比 | 問題なし（2026-08-24 再確認）。図中文字を32ptへ引き上げ、4地点のラベルは2行折り返しで島東側の海域に縦に積み、リーダー線で標定した（互いに重ならず軸内。交差もしない）。凡例は1列2行にしてグラフ下端に収まる。左の "5–6" "145" コールアウト・本文との干渉なし |
| 9 | 再訪（プレースホルダー） | 問題なし。2枚の "Placeholder — 2026-08-31 photograph" 枠が左右対称にスライド内。プレースホルダーであることが明示されている |
| 10 | 限界と次の一手 | 問題なし。本文4行のみ、テキストがスライド幅に収まる |
| 11 | オープンデータ | 問題なし。本文4行とQRコードが重ならず、下部の使用ライブラリ・データクレジット行もスライド内 |
| 12 | ループ図 | 問題なし（2026-08-24 再確認）。図中文字を27ptへ引き上げても、本文6行と3ボックスのループ図（Satellite scan → Field visit → OpenStreetMap）はスライド内、キャプション同士の間隔・矢印の収まりに変化なし |

**再訪なし版（`exp002_kitagi_foss4g2026_presentation_no_revisit.pptx`、11枚）**

S1–S8 は `shasum -a 256` で12枚版のS1–S8とSHA256が完全一致し、バイト単位で同一の描画であることを確認した（2026-08-24 の修正ウェーブ後に再確認済み。8ページすべて一致）。S9（旧S10「限界と次の一手」）・S10（旧S11「オープンデータ」）・S11（旧S12「ループ図」）は、SHA256はページ番号の描画差分により完全一致しないが、目視で本文・図が12枚版の対応スライド（旧S10・S11・S12）と同一であり、ページ番号のみが繰り上がっていることを確認した（元のS9「再訪」が削除され後続が1つ前にずれている）。両版とも文字切れ・重なり・スライド外への逸脱は見つからなかった。

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

**語数の算定方法**: 検査スクリプト `validate_exp002_kitagi_foss4g2026_presentation.py` の `count_en_words()` を用いた。これは正規表現 `[A-Za-z][A-Za-z'’-]*` による語トークナイザであり、アルファベットで始まる語のみを数え、`145` のような数字のみのトークンは数えない（数値の初出を綴り字で発話する方針と整合させるため）。本節の表・合計・秒数はすべてこの方法による値であり、検査スクリプトの語数ゲート（割当語数の±25%）が用いる数え方と同一である。

比較のため、同じEN本文を単純な空白分割（`str.split()`、数字トークンも1語として数える）で数えると合計 2,516 語（本節の 2,499 語より17語多い）になる。数え方によって合計は数十語ずれるため、本節はどの数え方によるかを明示している。以下は `count_en_words()` の値である。

| S | 内容契約の時間割 | 割当語数（145wpm換算） | EN語数（算出） | 算出秒数（語数÷145×60） | 割当語数からの差 |
|---|---:|---:|---:|---:|---:|
| 1 | 0:35 | 85 | 81 | 33.5秒 | −4.7% |
| 2 | 1:40 | 242 | 229 | 94.8秒 | −5.4% |
| 3 | 1:30（3–4で3:00） | 218 | 219 | 90.6秒 | +0.5% |
| 4 | 1:30（3–4で3:00） | 218 | 220 | 91.0秒 | +0.9% |
| 5 | 1:50 | 266 | 273 | 113.0秒 | +2.6% |
| 6 | 2:30 | 362 | 357 | 147.7秒 | −1.4% |
| 7 | 1:10 | 169 | 162 | 67.0秒 | −4.1% |
| 8 | 1:30 | 218 | 212 | 87.7秒 | −2.8% |
| 9 | 1:50 | 266 | 277 | 114.6秒 | +4.1% |
| 10 | 1:20 | 193 | 186 | 77.0秒 | −3.6% |
| 11 | 1:10（11–12で2:05） | 169 | 154 | 63.7秒 | −8.9% |
| 12 | 0:55（11–12で2:05） | 133 | 129 | 53.4秒 | −3.0% |
| **合計** | **17:30（1,050秒）** | **2,539** | **2,499** | **1,034.1秒（17:14）** | **−1.6%** |

いずれのスライドも検査スクリプトの許容幅（割当語数の±25%）以内であり、`validate_...py` は「OK: 949 checks passed」で通過している（6.4節）。S11 以外の11枚は割当語数の±5%以内に収まっている（S11 は −8.9%。口頭で挙げるライブラリ名を6つから3つへ削り、残りはフッターの投影に委ねた結果であり、投影面は変更していない。不足分は間として使える）。**S6単体は算出357語・147.7秒（2:28）で、ハードゲートの2:30（150秒）に対して2.3秒の余裕がある**（数値を1文1項目に分割したため、前回記録の354語・2:26より3語増えた。必須発話6項目は全て維持している）。全体の算出合計17:14は目標17:30に対して−16秒（−1.6%）で、20分枠（質疑5分・入替5分を除く発表20分）に対しては十分な余裕がある。**いずれの秒数も145 wpm換算の算出値であり、声に出して計測した実測値ではない。**

#### 6.3.2 発表者が声に出して計測するためのチェックリスト

以下は登壇前に発表者自身が実施するべき、実測のためのチェックリストである。本書のどの数値も実測を代替しない。

- [ ] 各スライドを声に出して読み、上表の「内容契約の時間割」列（秒）に対する実測秒数を記録する
- [ ] **S6単体を実測し、2:30（150秒）以内に収まることを確認する。** 超過した場合は、S6の情景描写（分布説明以外の部分）からEN本文の文を削る。投影文字列（スライド上のテキスト）は変更しない
- [ ] 本編合計を実測し、17:30前後（20分枠に対しバッファ2:30）に収まることを確認する
- [ ] 超過した場合は、投影文字列ではなくEN ノートの文を削ることを徹底する（削るスライドは合計への寄与が大きいスライド、特にS9のように算出値が割当を上回るスライドを優先的に見直す。2026-08-24 の第2次内容修正で S5・S8 は割当の±5%以内に収まっている）
- [ ] 実測結果を得たら、本節（6.3）に実測秒数を追記し、「算出値」ではなく「実測値」として記録し直す

### 6.4 全検査の再実行（機械検査）

```bash
uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py
uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py
uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py --no-revisit
uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py
```

結果: `OK: 949 checks passed`（2026-08-24 の修正ウェーブで検査群を両デッキへパラメータ化し、図中文字の実効サイズ検査を追加したため 466 → 949）。上記4コマンドの実行後に `git status --short` を確認したところ、差分は無かった（生成物は実行時刻に依存せずバイト単位で再現される）。すなわち `docs/presentations/` 配下の全生成物（PPTX 2種・図版5点）は再実行前と再実行後でバイト単位で一致した。

### 6.5 登壇前に残っている作業

- **S9の2枚の写真は依然プレースホルダーである。** 差し替え手順は「8月31日以降の差し替え手順」節（ブリーフ）どおり: (1) 撮影した写真を `docs/presentations/images/revisit_1.jpg` / `revisit_2.jpg` として配置する（固定寸法スロットに合わせて中央クロップされる）、(2) `uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py` を再実行する、(3) 本書 3章の8/31撮影記録テーブル（座標・撮影時刻・撮影方向・対象ポリゴンID）を実測値で埋め、スピーカーノート・内容契約に残る `[UPDATE AFTER 2026-08-31]` の申し送りを除去する
- **現地確認（8月31日の再訪）が実施できなかった場合は、11枚版（`exp002_kitagi_foss4g2026_presentation_no_revisit.pptx`、S9を除く）を本番として使用する**
- **英語通し読みの時間は未実測である。** 6.3節の秒数はすべて145wpmからの算出値であり、発表者本人が声に出して計測するまでは実測値として扱わない

## 7. 2026-08-24 修正ウェーブの検証（図中文字の実効サイズ）

全体レビューの Critical 指摘（図版の自己検査が実配置と異なる幅を測っていた）への対応として、
図中文字の**スライド上の実効サイズ**を生成済みPPTXから実測した。実効サイズ =
`native_pt × (配置幅 ÷ 画像実寸幅)`、実寸幅 = `ピクセル幅 ÷ 画像に記録された dpi`。

| 図版 / スライド | native pt | 修正前 配置倍率 | 修正前 実効pt | 修正後 配置倍率 | 修正後 実効pt |
|---|---:|---:|---:|---:|---:|
| `poster_f1_study_area.png` / S2 | 15（最小） | 0.764 | 11.46 | 1.040 | **15.60** |
| `poster_f4_index_panels.png` → `p05_index_panels.png` / S5 | 18 | 0.564 | 10.15 | 0.889 | **16.00** |
| `p06_clusters_map.png` / S6 | 20 → 32 | 0.473 | 9.46 | 0.516 | **16.52** |
| `p07_three_scales.png` / S7 | 21 | 1.026 | 21.55 | 1.026 | **21.55** |
| `p08_visit_anchors_map.png` / S8 | 20 → 32 | 0.461 | 9.22 | 0.518 | **16.57** |
| `p12_loop_diagram.png` / S12 | 24 → 27 | 0.612 | 14.69 | 0.612 | **16.51** |

検査の実効性（mutation test、いずれも確認後に復旧してバイト一致を再確認）:

- native を下げる経路: P6 の宣言と実装を 32pt → 24pt にすると
  `12枚版/再訪なし版 S6 ... 実効サイズ 12.41pt が 下限 15pt 未満（native 24pt × 配置倍率 0.517）` で失敗した
- 配置を縮める経路: native を触らず S6 の図版配置高さを 4.8in → 4.0in にすると
  `実効サイズ 13.77pt ...（native 32pt × 配置倍率 0.430）` で失敗した
  （4.4in では 15.2pt で合格する。設計に余裕を持たせているため）

## 8. 2026-08-24 調整ウェーブの検証（背景地図・色付き写真・S4レイアウト）

同日中に背景地図の出典を**航空写真から CARTO Positron のラベルなし地図へ是正**した（理由は2.4節）。
本章の数値はすべて是正後の成果物から測り直した値である。

### 8.1 図中文字の実効サイズ（生成済みPPTXの `shape.width` から復元）

配置倍率 = 配置幅 ÷ 画像実寸幅（実寸幅 = px ÷ 画像に記録された dpi）。実効pt = native pt × 配置倍率。
値は12枚版・再訪なし版で同一である（両デッキで同じ配置定数を使うため）。

| 図版 / スライド | 要素 | native pt | 実寸幅 (in) | 配置幅 (in) | 配置倍率 | 実効 pt | 実効 dpi |
|---|---|---:|---:|---:|---:|---:|---:|
| `poster_f1_study_area.png` / S2 | パネルタイトル・島名ラベル | 16 / 16 / 15 | 7.85 | 8.16 | 1.040 | 16.6 / 16.6 / **15.6** | 288 |
| `p05_index_panels.png` / S5 | パネルタイトル・カラーバー目盛 | 18 | 5.67 | 5.04 | 0.889 | **16.0** | 450 |
| `p06_clusters_map.png` / S6 | ゾーンラベル・タイトル・スケールバー | 32 | 9.49 | 4.90 | 0.516 | **16.5** | 387 |
| `p06_clusters_map.png` / S6 | 背景地図の帰属表示（フッター階層） | 22 | 9.49 | 4.90 | 0.516 | 11.4 | 387 |
| `p07_three_scales.png` / S7 | パネルキャプション・スケールバー | 21 | 9.28 | 9.54 | 1.028 | **21.6** | 233 |
| `p07_three_scales.png` / S7 | 背景地図の帰属表示（フッター階層） | 11 | 9.28 | 9.54 | 1.028 | 11.3 | 233 |
| `p08_visit_anchors_map.png` / S8 | 訪問ラベル・タイトル・凡例・スケールバー | 32 | 7.51 | 3.89 | 0.518 | **16.6** | 386 |
| `p08_visit_anchors_map.png` / S8 | 背景地図の帰属表示（フッター階層） | 22 | 7.51 | 3.89 | 0.518 | 11.4 | 386 |
| `p12_loop_diagram.png` / S12 | ボックスタイトル・キャプション | 27 | 12.35 | 7.55 | 0.612 | **16.5** | 327 |

太字は 15 pt 下限の検査対象（`NATIVE_FONT_SIZES` に宣言した主題ラベル）。すべて下限以上。
帰属表示はフッター階層（11〜12 pt）として意図的に検査対象外にしている
（内容契約「実装時のハードゲート」節、4章の裁定「帰属表示はフッター階層」を参照）。
背景地図の追加・出典の是正でも図版の画素数は変わらず（P6 1898×1859、P7 2226×782、P8 1502×1853）、
実効ptは調整前と同一である。P7 のみパネル(b) の写真差し替えで幅が 2224 → 2226 px に変わったが、
配置は高さ拘束のため倍率は 1.028 のままである。実効dpi はすべて下限 200 dpi 以上。

### 8.2 グレースケール確認（背景地図と主題データの分離）

`Pillow` の `.convert("L")` で P6・P7・P8 をグレースケール化し、目視で確認した。

| 図版 | グレースケール輝度の最小値 | 1パーセンタイル | 中央値 | 所見 |
|---|---:|---:|---:|---|
| `p06_clusters_map.png` | 39 | 43 | 243 | 検出ポリゴン（暗）と背景地図（明）が明確に分離。島の海岸線と道路が薄く読める |
| `p07_three_scales.png` | 0 | 43 | 210 | 最小値0はパネル(a)(b) の写真の暗部。パネル(c) の分離は P6 と同じ |
| `p08_visit_anchors_map.png` | 0 | 43 | 243 | 最小値0は訪問地点の黒い三角マーカー。ポリゴンと背景地図の分離は P6 と同じ |

減光後（`KEEP = 0.80`）の背景地図そのものの最小輝度は 222（ラスタ全体で実測）、検出ポリゴンの色
`COL_WATER = #0d47a1` のグレースケール輝度は 64（透過 0.95 で背景と合成しても約 71）である。
**158階調**の差があり、グレースケールでも水域ポリゴンが最も目立つ要素であることを確認した。
同時に海陸差は約 20 階調残っており、グレースケールでも島の海岸線が判別できる。
背景地図を薄くしたり主題データを濃くしたりする追加調整は不要だった
（逆に、写真基図向けの `KEEP = 0.30` では海岸線が消えるため 0.80 へ緩めた。2.4節参照）。

### 8.3 PDF化による全ページ目視（12枚版・再訪なし版）

```bash
soffice --headless --convert-to pdf --outdir /tmp/adjpdf \
  docs/presentations/exp002_kitagi_foss4g2026_presentation.pptx \
  docs/presentations/exp002_kitagi_foss4g2026_presentation_no_revisit.pptx
pdftoppm -r 110 -png /tmp/adjpdf/exp002_kitagi_foss4g2026_presentation.pdf /tmp/adjpdf/a
```

`Pages: 12` / `Pages: 11`、いずれも `Page size: 960.009 x 540 pts`（16:9）。全ページを画像として
目視し、文字切れ・重なり・スライド外への逸脱がないことを確認した。特に確認した点:

- **S4**: 縦長スロット2枚は表示寸法が同一（3.87 × 4.40 in）で、いずれも引き伸ばされていない。
  左は原本のクロップなし、右は下側のみクロップ。本文（8行に折り返し、17 pt）は左列 4.00 in に
  収まり、写真と重ならず、スライド下端にも達しない
- **macOS の Dock・「Pages」ツールチップ**: 12枚版・再訪なし版の全ページ（S4・S7 を含む）で
  一切写っていない。追跡ファイルの時点で切り落としているため構造的に出現しない
- **S6・S7(c)・S8**: 背景地図の上で検出ポリゴンが最も目立ち、島の海岸線が読める。背景は
  ラベルなしの淡色地図であって写真ではないため、検出結果が実写で裏付けられたようには読めない。
  S7 はパネル(b) の航空写真とパネル(c) の地図が明確に別物として読める。
  帰属表示（`Basemap: © OpenStreetMap contributors, © CARTO`）は地図軸の左上（北西の海域）に
  収まり、ゾーンラベル・訪問地点ラベル・スケールバーと重ならない
  （`assert_labels_inside_and_disjoint()` がレンダラ実測で機械検査）

### 8.4 決定性とネットワーク非依存

- 図版生成 → 両デッキ生成を2回連続で実行し、`git status` がクリーンであることを確認した
  （図版PNG・PPTX いずれもバイト一致）
- 図版生成をプロキシを無効アドレス（`127.0.0.1:9`）に向けた環境で実行し、正常に完走して
  同一バイトの図版が得られることを確認した。取得系のモジュールはモジュール先頭で import せず
  `fetch_basemap()` の内側だけで import している
- 3つの検査スクリプト（発表・口頭資料・ポスター）をすべて再実行して合格した

