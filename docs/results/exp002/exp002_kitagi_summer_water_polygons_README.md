# 夏季検出水域ポリゴン GeoJSON（exp002 / 北木島）

`exp002_kitagi_summer_water_polygons_2025-08-02.geojson`

Sentinel-2 L2A の夏季シーン（2025-08-02）から検出した北木島の島内水域ポリゴン145件。FOSS4G Hiroshima 2026 ポスター発表の成果データとして公開する（ポスターのQRコードからの導線）。

## 内容

| 項目 | 値 |
|---|---|
| 形式 | GeoJSON FeatureCollection（RFC 7946） |
| 座標系 | EPSG:4326 / CRS84（**経度・緯度順**、小数6桁に丸め） |
| ジオメトリ | Polygon のみ |
| feature 数 | **145**（レポート表4-2の島内水域ポリゴン数と一致） |
| 属性 | `id`（面積降順の1〜145）、`area_m2` |
| 面積範囲 | 最大 7,825.5 m²（レポート記載 7,826 m²）／最小 100.3 m² |
| 1,000 m² 超 | 14件（レポート表4-2と一致） |
| 経度範囲 | 133.518388 – 133.558317 |
| 緯度範囲 | 34.370659 – 34.399861 |
| ファイルサイズ | 86,615 bytes |

`metadata` メンバー（RFC 7946 の foreign member）にシーンID・判定条件・帰属表示・ライセンス・注意書きを埋め込んでいる。

## 生成方法

```bash
uv run python scripts/generate_exp002_poster_figures.py
```

- 生成コミット: **3fc6581**（`feature/foss4g-kitagi-talk-materials`）
- 生成元スクリプト: `scripts/generate_exp002_poster_figures.py` の `export_summer_geojson()`
- 解析ロジックは `notebooks/exp002_kitagi_quarry_water_detection.ipynb` と同一。スクリプトは島内ポリゴン数145・植生マスク除外9pxがレポート確定値と一致しない場合に例外で停止する
- 実行日時・コミットハッシュはファイルに埋め込まない（再実行でバイト一致させるため）。生成コミットは本ファイルに記録する

## 判定条件

```text
(NDWI > −0.2  OR  MNDWI > −0.1)  AND NOT  (NDVI > 0.3)
```

10 m 解析グリッド、最小ポリゴン面積 100 m²。シーンID `S2A_MSIL2A_20250802T015121_R017_T53SLU_20250802T044417`（雲量 0.7%）。

## 利用上の注意

1. **検出水域であり、個別に現地確認された丁場池ではない。** 自然の池沼、農業用ため池、影、暗い岩肌による誤検出が含まれる可能性がある
2. **厳密な海岸線マスクを適用していない。** 海岸線付近のポリゴンには海水が含まれる可能性がある（海域そのものは面積閾値と重心のバウンディングボックス判定で除外している）
3. **精度指標（適合率・再現率）は未算出。** 現地検証が未実施のため
4. Sentinel-2 の10 m分解能により、幅10 m未満の水域や100 m²未満の水域は捕捉されていない
5. 単一時期の観測であり、水位の季節変動・経年変化は反映していない

詳細は `docs/reports/exp002_kitagi_quarry_water_detection_report.md` の 5.4「分析の限界」を参照。

## 帰属表示・ライセンス

- Contains modified Copernicus Sentinel data [2025].
- Sentinel-2 L2A data accessed through Microsoft Planetary Computer STAC API.
- 本データ: CC BY 4.0 / Noboru Otsuka (Geolonia Inc.)
