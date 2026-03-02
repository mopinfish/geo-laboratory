# exp001_shizuoka_road_network.ipynb - 静岡県3都市の道路ネットワーク比較分析

## 概要

本ノートブックは、静岡県の3都市（焼津市・静岡市・浜松市）の道路ネットワークをOSMnxで取得し、8指標を用いて定量的に比較する。劉（2016）の道路ネットワーク解析手法に基づき、回遊性・アクセス性・迂回性の3観点から構造化して分析する。

分析は以下の3段階で構成される:

1. **市全域分析**: 各市の行政区域全体の道路ネットワーク（drive）から8指標を算出
2. **防災分析**: 海岸線からの距離で沿岸部（2km以内）と内陸部に分割し、避難路ネットワーク特性を比較
3. **観光分析**: 各市の主要駅周辺800mの歩行者ネットワーク（walk）の回遊性を比較。drive との差分で細街路効果を分析

## 重要な設定定数

```python
# 対象都市
cities = {
    "焼津市": "焼津市, 静岡県, Japan",
    "静岡市": "静岡市, 静岡県, Japan",
    "浜松市": "浜松市, 静岡県, Japan",
}

# 対象駅（緯度, 経度）
stations = {
    "焼津駅": (34.8671, 138.3225),
    "静岡駅": (34.9717, 138.3891),
    "浜松駅": (34.7038, 137.7350),
}

COASTAL_THRESHOLD_M = 2000  # 沿岸部の閾値距離（メートル）
STATION_RADIUS = 800        # 駅周辺の分析半径（メートル）
```

## 使用指標（8指標）

劉（2016）の3観点に対応付けた8指標を使用する。

| 観点 | 指標 | 計算方法 |
|------|------|----------|
| 回遊性 | `alpha_index` | (e - n + p) / (2n - 5) |
| 回遊性 | `degree_centrality_mean` | `nx.degree_centrality()` の平均 |
| 回遊性 | `basic_streets_per_node_avg` | `ox.stats.basic_stats()` |
| 回遊性 | `basic_self_loop_proportion` | `ox.stats.basic_stats()` |
| アクセス性 | `closeness_centrality_mean` | 500ノードサンプリングによる`nx.single_source_dijkstra_path_length()` ベースの近似平均 |
| アクセス性 | `basic_clean_intersection_density_km` | `ox.stats.basic_stats(clean_int_tol=15)` |
| 迂回性 | `avg_circuity_A` | 500ノードサンプリングによるdijkstra距離/ユークリッド距離の平均 |
| 迂回性 | `basic_circuity_avg` | `ox.stats.basic_stats()` |

## 主要クラス・関数

### NetworkMetricsCalculator (`src/network_metrics.py`)

8指標を一括算出するクラス。

| メソッド | 機能 |
|---------|------|
| `calculate_all(G, area_m2)` | 8指標を一括算出しdictで返す |
| `calculate_all_as_series(G, area_m2)` | 8指標をpd.Seriesで返す |
| `_calculate_centrality(G)` | degree_centrality_mean, closeness_centrality_mean |
| `_calculate_topology(G)` | alpha_index |
| `_calculate_circuity(G)` | avg_circuity_A（500ノードサンプリング） |
| `_calculate_osmnx_stats(G, area_m2)` | basic_self_loop_proportion, basic_circuity_avg, basic_streets_per_node_avg, basic_clean_intersection_density_km |

### 可視化関数 (`src/visualization.py`)

| 関数 | 機能 |
|------|------|
| `plot_network_on_map(G, title, metrics)` | folium地図上にネットワーク描画 |
| `plot_radar_chart(city_metrics_dict, indicators)` | 都市間比較レーダーチャート（正規化済み） |
| `plot_comparison_bars(city_metrics_dict, indicator_groups)` | 回遊性/アクセス性/迂回性グループ別棒グラフ |
| `plot_subarea_comparison(subarea_metrics, area_type)` | 沿岸部vs内陸部、駅周辺の比較チャート |
| `plot_liu_typology_comparison(city_metrics, liu_type_profiles)` | 劉の4類型プロファイルとの対照レーダーチャート |

### ヘルパー関数（ノートブック内定義）

| 関数 | 機能 |
|------|------|
| `get_coastline_for_city(city_name, boundary_gdf)` | OSMから海岸線を取得（取得失敗時はwater境界で代替） |
| `split_graph_by_coastline(G_proj, coastline_gdf, threshold_m)` | グラフを海岸線距離で沿岸部/内陸部に分割 |

## 処理フロー

```
Section 1: 環境セットアップ
├── パッケージインストール（osmnx, networkx, folium等）
├── Google Driveマウント & パス設定
└── ライブラリ・srcモジュールのインポート
      ↓
Section 2: データ取得
├── 3都市の道路ネットワーク取得（drive）
│     └── ox.graph_from_place() → ox.project_graph()
├── サブエリア抽出（沿岸部2km / 内陸部）
│     ├── ox.features_from_place(tags={'natural': 'coastline'})
│     └── ノードの海岸線距離を計算 → 2km閾値で分割
├── 駅周辺800mネットワーク取得（walk + drive の2パターン）
│     └── ox.graph_from_point(dist=800)
└── 基本統計量の確認
      ↓
Section 3: 市全域の指標算出
├── 各市の8指標を算出（NetworkMetricsCalculator）
├── 劉の3観点でグルーピングして表示
├── 3観点別グループ棒グラフ
└── レーダーチャート
      ↓
Section 4: 防災分析（沿岸部 vs 内陸部）
├── 沿岸部・内陸部の8指標を算出
├── 回遊性指標の比較
├── 迂回性指標の比較
├── 沿岸部ネットワークの地図可視化（folium）
└── 棒グラフによる比較
      ↓
Section 5: 観光分析（駅周辺の回遊性）
├── 駅周辺800mの8指標を算出（walk + drive）
├── 細街路効果の分析（walk - drive の差分）
├── アクセス性指標の比較
├── 駅周辺ネットワークの地図可視化（folium）
└── 劉の4類型との対照レーダーチャート
      ↓
Section 6: 総合比較
├── 全分析結果の統合テーブル
├── ヒートマップ（指標×都市×エリア）
├── 劉の類型化との対照まとめ
└── 主要な知見のまとめ（4仮説の検証）
      ↓
Section 7: 結果保存
├── 指標データをCSV保存（data/）
├── 地図をHTML保存（docs/results/）
└── グラフ画像をPNG保存（docs/results/）
```

## 計算時間の目安

`closeness_centrality` および `avg_circuity_A` は500ノードサンプリングで近似計算する。

| 都市 | ノード数 | エッジ数 | 推定時間（Section 3） |
|------|---------|---------|-------------------|
| 焼津市 | 8,195 | 24,635 | ~1分 |
| 静岡市 | 30,160 | 82,938 | ~1〜2分 |
| 浜松市 | 47,162 | 138,120 | ~2〜3分 |

Section 3の合計で約5分程度。ノートブック全体で約10〜15分。

## 出力ファイル

| ファイル | 内容 |
|---------|------|
| `data/exp001_all_metrics.csv` | 全分析結果の統合テーブル（都市×エリア×タイプ） |
| `data/exp001_city_metrics.csv` | 市全域の8指標 |
| `data/exp001_fine_street_effect.csv` | 細街路効果（walk - drive差分） |
| `docs/results/exp001_city_radar_chart.png` | 市全域レーダーチャート |
| `docs/results/exp001_city_comparison_bars.png` | 3観点別棒グラフ |
| `docs/results/exp001_liu_typology_comparison.png` | 市全域 vs 劉の4類型 |
| `docs/results/exp001_station_liu_comparison.png` | 駅周辺 vs 劉の4類型 |
| `docs/results/exp001_{駅名}_walk_network.html` | 駅周辺歩行者ネットワーク地図 |
| `docs/results/exp001_{都市名}_coastal_network.html` | 沿岸部ネットワーク地図 |

## 結果例

[実験実施後に記載]

## 次のステップ

- 実験結果に基づき `docs/reports/exp001_shizuoka_road_network_report.md` のプレースホルダを埋める
- `docs/presentations/exp001_shizuoka_road_network_presentation.pptx` の作成
