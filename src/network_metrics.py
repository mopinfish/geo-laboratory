"""道路ネットワークから8指標を算出するモジュール

劉（2016）の道路ネットワーク解析手法に基づき、回遊性・アクセス性・迂回性の
3観点から道路ネットワーク特性を定量評価する。

8指標:
  回遊性: alpha_index, degree_centrality_mean, basic_streets_per_node_avg,
           basic_self_loop_proportion
  アクセス性: closeness_centrality_mean, basic_clean_intersection_density_km
  迂回性: avg_circuity_A, basic_circuity_avg
"""

import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd


class NetworkMetricsCalculator:
    """道路ネットワークから8指標を算出するクラス

    SRPプロジェクトのNetworkMetricsCalculatorクラスを基に、
    劉（2016）の3観点で構造化した8指標に特化。

    Parameters
    ----------
    clean_int_tol : float
        交差点クリーニングの許容距離（メートル）。デフォルト15m。
    """

    FEATURE_COLUMNS = [
        'degree_centrality_mean', 'closeness_centrality_mean',
        'basic_self_loop_proportion', 'avg_circuity_A',
        'alpha_index', 'basic_circuity_avg',
        'basic_streets_per_node_avg', 'basic_clean_intersection_density_km'
    ]

    # 劉（2016）の3観点に基づく指標グループ
    CIRCULATION_INDICATORS = [
        'alpha_index', 'degree_centrality_mean',
        'basic_streets_per_node_avg', 'basic_self_loop_proportion'
    ]
    ACCESSIBILITY_INDICATORS = [
        'closeness_centrality_mean',
        'basic_clean_intersection_density_km'
    ]
    CIRCUITY_INDICATORS = [
        'avg_circuity_A', 'basic_circuity_avg'
    ]

    def __init__(self, clean_int_tol=15):
        self.clean_int_tol = clean_int_tol

    def calculate_all(self, G, area_m2=None):
        """8指標を一括算出する

        Parameters
        ----------
        G : networkx.MultiDiGraph
            OSMnxで取得した道路ネットワークグラフ
        area_m2 : float, optional
            分析対象エリアの面積（平方メートル）。
            Noneの場合はconvex hullから推定する。

        Returns
        -------
        dict
            8指標の辞書
        """
        # 投影座標系への変換（未投影の場合）
        if not ox.projection.is_projected(G.graph["crs"]):
            G = ox.project_graph(G)

        # 面積の推定
        if area_m2 is None:
            area_m2 = self._estimate_area(G)

        results = {}
        results.update(self._calculate_centrality(G))
        results.update(self._calculate_topology(G))
        results.update(self._calculate_circuity(G))
        results.update(self._calculate_osmnx_stats(G, area_m2))

        return results

    def calculate_all_as_series(self, G, area_m2=None):
        """8指標をpandas.Seriesとして返す

        Parameters
        ----------
        G : networkx.MultiDiGraph
            OSMnxで取得した道路ネットワークグラフ
        area_m2 : float, optional
            分析対象エリアの面積（平方メートル）

        Returns
        -------
        pd.Series
            FEATURE_COLUMNS順に並んだ指標値
        """
        metrics = self.calculate_all(G, area_m2)
        return pd.Series({col: metrics.get(col, np.nan) for col in self.FEATURE_COLUMNS})

    def _estimate_area(self, G):
        """グラフのノード座標からconvex hullの面積を推定する"""
        nodes = ox.graph_to_gdfs(G, edges=False)
        if len(nodes) < 3:
            return 0.0
        hull = nodes.unary_union.convex_hull
        return hull.area

    def _calculate_centrality(self, G):
        """degree_centrality_mean, closeness_centrality_meanを算出する

        closeness_centralityは大規模グラフでの計算コストが高いため、
        ノード数がmax_closeness_samplesを超える場合はサンプリングで近似する。
        """
        G_undir = G.to_undirected(reciprocal=False)

        try:
            deg_cent = pd.Series(nx.degree_centrality(G_undir))

            nodes = list(G_undir.nodes())
            max_samples = 100
            if len(nodes) > max_samples:
                rng = np.random.default_rng(42)
                sampled_nodes = rng.choice(
                    nodes, size=max_samples, replace=False
                ).tolist()
                clo_values = []
                for node in sampled_nodes:
                    sp = nx.single_source_dijkstra_path_length(
                        G_undir, node, weight="length"
                    )
                    reachable = {k: v for k, v in sp.items() if v > 0}
                    if reachable:
                        avg_dist = sum(reachable.values()) / len(reachable)
                        clo_values.append(1.0 / avg_dist)
                    else:
                        clo_values.append(0.0)
                clo_mean = sum(clo_values) / len(clo_values) if clo_values else 0.0
            else:
                clo_cent = pd.Series(
                    nx.closeness_centrality(G_undir, distance="length")
                )
                clo_mean = clo_cent.mean()

            return {
                "degree_centrality_mean": deg_cent.mean(),
                "closeness_centrality_mean": clo_mean,
            }
        except Exception:
            return {
                "degree_centrality_mean": 0.0,
                "closeness_centrality_mean": 0.0,
            }

    def _calculate_topology(self, G):
        """alpha_indexを算出する

        alpha = (e - n + p) / (2n - 5)
        e: エッジ数, n: ノード数, p: 連結成分数
        """
        G_undir = G.to_undirected(reciprocal=False)
        n = G_undir.number_of_nodes()
        e = G_undir.number_of_edges()
        p = nx.number_connected_components(G_undir)

        mu = e - n + p
        alpha = mu / (2 * n - 5) if n > 2 else 0.0

        return {"alpha_index": alpha}

    def _calculate_circuity(self, G):
        """avg_circuity_Aを算出する

        全ノードペア間のdijkstra最短経路距離とユークリッド距離の比率の平均。
        大規模グラフでは計算量が膨大になるため、サンプリングを行う。
        """
        G_undir = G.to_undirected(reciprocal=False)
        coords = {n: (d['x'], d['y']) for n, d in G_undir.nodes(data=True)}

        nodes = list(G_undir.nodes())
        max_samples = 100
        if len(nodes) > max_samples:
            rng = np.random.default_rng(42)
            sampled_nodes = rng.choice(nodes, size=max_samples, replace=False)
        else:
            sampled_nodes = nodes

        circuity_list = []
        for u in sampled_nodes:
            try:
                lengths = nx.single_source_dijkstra_path_length(
                    G_undir, u, weight="length"
                )
            except Exception:
                continue

            x1, y1 = coords[u]
            for v, d in lengths.items():
                if u == v or d == 0:
                    continue
                x2, y2 = coords[v]
                euclid = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                if euclid > 0:
                    circuity_list.append(d / euclid)

        avg_circuity = (
            sum(circuity_list) / len(circuity_list) if circuity_list else 0.0
        )
        return {"avg_circuity_A": avg_circuity}

    def _calculate_osmnx_stats(self, G, area_m2):
        """OSMnx基本統計量から指標を抽出する

        basic_self_loop_proportion, basic_circuity_avg,
        basic_streets_per_node_avg, basic_clean_intersection_density_km
        """
        try:
            stats = ox.stats.basic_stats(
                G, area=area_m2, clean_int_tol=self.clean_int_tol
            )
            return {
                "basic_self_loop_proportion": stats.get("self_loop_proportion", 0.0),
                "basic_circuity_avg": stats.get("circuity_avg", 0.0),
                "basic_streets_per_node_avg": stats.get("streets_per_node_avg", 0.0),
                "basic_clean_intersection_density_km": stats.get(
                    "clean_intersection_density_km", 0.0
                ),
            }
        except Exception:
            return {
                "basic_self_loop_proportion": 0.0,
                "basic_circuity_avg": 0.0,
                "basic_streets_per_node_avg": 0.0,
                "basic_clean_intersection_density_km": 0.0,
            }
