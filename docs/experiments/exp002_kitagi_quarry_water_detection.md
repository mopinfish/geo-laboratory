# exp002_kitagi_quarry_water_detection.ipynb — 北木島丁場水域検出

## 概要

岡山県笠岡市・北木島の丁場（石切場跡）に溜まった水域を、Sentinel-2衛星画像のNDWI（正規化水域指数）で検出し、Foliumによるインタラクティブ地図で可視化する。

## 重要な設定定数

```python
# 北木島の中心座標と範囲
KITAGI_CENTER = [34.374, 133.543]           # [lat, lon]
KITAGI_BBOX = [133.515, 34.350, 133.570, 34.400]  # [west, south, east, north]

# NDWI水域判定閾値
NDWI_WATER_THRESHOLD = 0.0  # NDWI > 0 で水域と判定

# 検索パラメータ
SEARCH_DATETIME = "2023-01-01/2025-12-31"
MAX_CLOUD_COVER = 10        # 最大雲量 (%)
MIN_AREA_PIXELS = 5         # 水域ポリゴン最小面積（ピクセル数）
```

## 主要クラス・関数

| 名前 | 種別 | 説明 |
|------|------|------|
| `read_band_aoi()` | 関数 | Sentinel-2バンドをAOI範囲で読み込み、座標情報とともに返す |
| `ndwi_to_rgba()` | 関数 | NDWI配列をRGBA画像に変換（水域を青で強調、非水域は透明） |
| `normalize_band()` | 関数 | バンドデータをパーセンタイルストレッチで0-255に正規化 |
| `pystac_client.Client` | 外部クラス | STAC APIカタログへの接続 |
| `planetary_computer.sign_inplace` | 外部関数 | Planetary ComputerのURLに認証署名を付与 |
| `rasterio.open()` | 外部関数 | Cloud-Optimized GeoTIFFのリモート読み込み |
| `rasterio.features.shapes()` | 外部関数 | ラスタデータからベクタポリゴンを抽出 |
| `folium.Map` | 外部クラス | Leaflet.jsベースのインタラクティブ地図 |
| `folium.raster_layers.ImageOverlay` | 外部クラス | ラスタ画像を地図上に重ね合わせ |

## 処理フロー

```
パッケージインストール・インポート
  ↓
対象地域（AOI）の定義
  ↓
Sentinel-2画像の検索（STAC API）
  → 雲量の少ない画像を自動選択
  ↓
バンドデータの読み込み
  → Green (B03) + NIR (B08) をAOI範囲でウィンドウ読み込み
  ↓
NDWI計算
  → NDWI = (Green - NIR) / (Green + NIR)
  ↓
静的可視化（matplotlib）
  → バンド画像、NDWI画像、ヒストグラム
  ↓
GeoTIFF出力
  → NDWI値ラスタ（float32、1バンド）
  → Red (B04) + Blue (B02) を追加読み込み
  → トゥルーカラー合成 + 水域を青色で強調（RGBA、4バンド）
  ↓
インタラクティブ地図作成（Folium）
  → NDWIラスタオーバーレイ
  → 水域ポリゴン抽出・重ね合わせ
  → レイヤー切替・面積表示
  ↓
HTML・GeoJSON出力
```

## 出力ファイル

| ファイル | 説明 |
|---------|------|
| `tmp/exp002_kitagi_water_map.html` | インタラクティブ地図（ブラウザで開く） |
| `tmp/exp002_kitagi_water_bodies.geojson` | 水域ポリゴン（GISソフトで利用可能） |
| `tmp/exp002_kitagi_ndwi.tif` | NDWI GeoTIFF（float32、1バンド） |
| `tmp/exp002_kitagi_water_highlighted.tif` | 水域強調衛星画像 GeoTIFF（RGBA、4バンド） |
| `tmp/exp002_ndwi_static.png` | バンド画像・NDWI静的画像 |
| `tmp/exp002_ndwi_histogram.png` | NDWIヒストグラム |

## 結果例

実験実施後に記載。

## 次のステップ

- MNDWI（Modified NDWI = (Green - SWIR) / (Green + SWIR)）による水域検出精度の比較
- 複数時期の画像による季節変動の確認
- 検出された水域と既知の丁場位置の照合
- 水域面積・深度の推定
