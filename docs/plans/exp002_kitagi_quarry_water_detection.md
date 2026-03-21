# 実験計画: 北木島丁場水域検出

## 実験ID

exp002

## 目的

岡山県笠岡市・北木島に分布する丁場（石切場跡）の位置を、衛星画像から水域を検出することで把握する。丁場跡には雨水が溜まり池状の水域を形成しているため、水域指数（NDWI）により検出が可能である。検出結果をインタラクティブ地図およびGeoTIFFとして出力し、現地調査や後続分析の基礎資料とする。

## 背景

北木島は笠岡諸島最大の島で、花崗岩（北木石）の産地として知られる。明治期以降、島内各所で採石が行われ、多数の丁場が開設された。現在は多くの丁場が閉鎖されており、切り立った岩壁の底部に雨水が溜まった水域が形成されている。これらの丁場跡は北木島の景観・歴史を特徴づける地形であるが、その全容を網羅的に把握した資料は限られている。

衛星リモートセンシングによる水域検出は、広域を一括して調査でき、アクセス困難な場所も含めて丁場跡の分布を把握する有効な手法である。

## 手法

### データソース

- **衛星画像**: Sentinel-2 L2A（欧州宇宙機関ESA）
  - 空間分解能: 10m（可視・近赤外バンド）
  - 取得方法: Microsoft Planetary Computer STAC API（無料・認証不要）
- **使用バンド**:
  - Band 2 (Blue, 490nm) — トゥルーカラー合成用
  - Band 3 (Green, 560nm) — NDWI計算・トゥルーカラー合成用
  - Band 4 (Red, 665nm) — トゥルーカラー合成用
  - Band 8 (NIR, 842nm) — NDWI計算用

### 水域指数

NDWI（Normalized Difference Water Index; McFeeters, 1996）を使用する。

```
NDWI = (Green − NIR) / (Green + NIR)
```

- 水域: NDWI > 0（開水面では通常 > 0.3）
- 植生・土壌: NDWI < 0

### 対象地域

| 項目 | 値 |
|------|-----|
| 島名 | 北木島（きたぎしま） |
| 所在 | 岡山県笠岡市 |
| 中心座標 | 34.374°N, 133.543°E |
| バウンディングボックス | W=133.515, S=34.350, E=133.570, N=34.400 |

### 画像選択基準

- 検索期間: 2023-01-01 〜 2025-12-31
- 最大雲量: 10%
- 雲量の最も少ない画像を自動選択

### 分析パラメータ

| パラメータ | 値 | 説明 |
|-----------|-----|------|
| `NDWI_WATER_THRESHOLD` | 0.0 | 水域判定閾値 |
| `MIN_AREA_M2` | 500 | 水域ポリゴン最小面積（m²） |

## 分析フロー

1. Sentinel-2画像の検索・選択（STAC API）
2. Green (B03)・NIR (B08) バンドの読み込み（AOI範囲でウィンドウ読み込み）
3. NDWI計算
4. 静的可視化（バンド画像・NDWI画像・ヒストグラム）
5. GeoTIFF出力（NDWIラスタ + 水域強調トゥルーカラー画像）
6. インタラクティブ地図作成（Folium）
   - OpenStreetMap / Esri衛星画像 / 地理院地図（ベースレイヤー）
   - NDWIラスタオーバーレイ
   - 水域ポリゴン（面積ツールチップ付き）
7. HTML・GeoJSON出力

## 仮説

1. **丁場跡の水域はNDWI > 0で検出可能である** — 花崗岩切り出し後の凹地に溜まった水域は、周囲の植生・岩肌と明確にNDWI値が異なるはずである
2. **島内部に複数の独立した水域が検出される** — 北木島には複数の丁場跡が存在し、それぞれ独立した水域として検出されるはずである
3. **Sentinel-2の10m分解能で主要な丁場跡は検出可能である** — 丁場跡の水域は一般に数十m〜数百m規模であり、10m分解能で捉えられる

## 成果物

| ファイル | パス | 内容 |
|---------|------|------|
| 実験計画書 | `docs/plans/exp002_kitagi_quarry_water_detection.md` | 本ドキュメント |
| ノートブック | `notebooks/exp002_kitagi_quarry_water_detection.ipynb` | 分析ノートブック |
| 実験ドキュメント | `docs/experiments/exp002_kitagi_quarry_water_detection.md` | ノートブック対応ドキュメント |
| インタラクティブ地図 | `tmp/exp002_kitagi_water_map.html` | Foliumインタラクティブ地図 |
| 水域ポリゴン | `tmp/exp002_kitagi_water_bodies.geojson` | 水域GeoJSON |
| NDWI GeoTIFF | `tmp/exp002_kitagi_ndwi.tif` | NDWI値ラスタ |
| 水域強調画像 | `tmp/exp002_kitagi_water_highlighted.tif` | 水域を青色で強調した衛星画像 |
| 静的画像 | `tmp/exp002_ndwi_static.png` | バンド画像・NDWI画像 |
| ヒストグラム | `tmp/exp002_ndwi_histogram.png` | NDWI分布ヒストグラム |

## 依存パッケージ

```
pystac-client, planetary-computer, rasterio, numpy,
folium, matplotlib, Pillow, shapely
```

パッケージ管理は `uv` を使用し、`pyproject.toml` で依存関係を管理する。

## 検証方法

1. ノートブックを上から順に実行し、全セルがエラーなく完了すること
2. Sentinel-2画像が正常に検索・取得されること
3. NDWI値が理論的な範囲 [-1, 1] 内に収まること
4. 島内部に水域ポリゴンが検出されること
5. GeoTIFFがQGIS等のGISソフトで正常に開けること
6. インタラクティブ地図がブラウザで正常に表示され、レイヤー切替が動作すること

## 今後の発展

- MNDWI（Modified NDWI = (Green − SWIR) / (Green + SWIR)）による検出精度の比較
- 複数時期の画像による季節変動・経年変化の分析
- 検出水域と既知の丁場位置情報との照合・精度評価
- 水域の色調解析による水質・深度の推定
- 北木島以外の採石島（白石島、犬島等）への適用

## 参考文献

- McFeeters, S. K. (1996) The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features. *International Journal of Remote Sensing*, **17**(7), 1425-1432. — NDWI の提唱論文
- Xu, H. (2006) Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery. *International Journal of Remote Sensing*, **27**(14), 3025-3033. — MNDWI の提唱論文（今後の発展で参照）
