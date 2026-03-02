"""道路ネットワーク分析の可視化モジュール

地図描画、レーダーチャート、棒グラフ等の可視化関数を提供する。
"""

import folium
import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
import pandas as pd


def plot_network_on_map(G, title="", metrics=None, color="blue", weight=1):
    """道路ネットワークをfolium地図上に描画する

    Parameters
    ----------
    G : networkx.MultiDiGraph
        OSMnxで取得した道路ネットワークグラフ
    title : str
        地図のタイトル
    metrics : dict, optional
        表示する指標値の辞書
    color : str
        エッジの描画色
    weight : float
        エッジの描画太さ

    Returns
    -------
    folium.Map
    """
    nodes = ox.graph_to_gdfs(G, edges=False)
    center_lat = nodes.geometry.y.mean()
    center_lon = nodes.geometry.x.mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    # タイトル表示
    if title:
        title_html = f'<h3 style="position:fixed;z-index:100000;top:10px;left:50%;transform:translateX(-50%);background:white;padding:5px 15px;border-radius:5px;box-shadow:0 2px 6px rgba(0,0,0,0.3);">{title}</h3>'
        m.get_root().html.add_child(folium.Element(title_html))

    # エッジの描画
    _, edges = ox.graph_to_gdfs(G)
    for _, row in edges.iterrows():
        if row.geometry is not None:
            coords = [(y, x) for x, y in row.geometry.coords]
            folium.PolyLine(
                coords, color=color, weight=weight, opacity=0.7
            ).add_to(m)

    # 指標情報をポップアップで表示
    if metrics:
        info_text = "<br>".join(
            [f"<b>{k}</b>: {v:.4f}" for k, v in metrics.items()]
        )
        folium.Marker(
            location=[center_lat, center_lon],
            popup=folium.Popup(info_text, max_width=300),
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

    return m


def plot_radar_chart(city_metrics_dict, indicators=None, title=""):
    """3都市の指標をレーダーチャートで比較する

    Parameters
    ----------
    city_metrics_dict : dict
        {都市名: {指標名: 値}} の辞書
    indicators : list, optional
        表示する指標名リスト。Noneの場合は全指標
    title : str
        チャートのタイトル

    Returns
    -------
    matplotlib.figure.Figure
    """
    from src.network_metrics import NetworkMetricsCalculator

    if indicators is None:
        indicators = NetworkMetricsCalculator.FEATURE_COLUMNS

    cities = list(city_metrics_dict.keys())

    # 正規化（0-1スケール）
    df = pd.DataFrame(city_metrics_dict).T
    df = df[indicators]
    df_norm = (df - df.min()) / (df.max() - df.min() + 1e-10)

    num_vars = len(indicators)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    for i, city in enumerate(cities):
        values = df_norm.loc[city].tolist()
        values += values[:1]
        ax.fill(angles, values, alpha=0.15, color=colors[i % len(colors)])
        ax.plot(
            angles, values, "o-",
            linewidth=2, color=colors[i % len(colors)], label=city
        )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(indicators, fontsize=8)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.yaxis.grid(True, linestyle="--", alpha=0.7)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    if title:
        ax.set_title(title, y=1.08, fontweight="bold", fontsize=14)

    plt.tight_layout()
    return fig


def plot_comparison_bars(city_metrics_dict, indicator_groups=None, title=""):
    """回遊性/アクセス性/迂回性グループ別の棒グラフ比較

    Parameters
    ----------
    city_metrics_dict : dict
        {都市名: {指標名: 値}} の辞書
    indicator_groups : dict, optional
        {グループ名: [指標名リスト]} の辞書
    title : str
        チャートのタイトル

    Returns
    -------
    matplotlib.figure.Figure
    """
    from src.network_metrics import NetworkMetricsCalculator

    if indicator_groups is None:
        indicator_groups = {
            "回遊性": NetworkMetricsCalculator.CIRCULATION_INDICATORS,
            "アクセス性": NetworkMetricsCalculator.ACCESSIBILITY_INDICATORS,
            "迂回性": NetworkMetricsCalculator.CIRCUITY_INDICATORS,
        }

    cities = list(city_metrics_dict.keys())
    n_groups = len(indicator_groups)

    fig, axes = plt.subplots(1, n_groups, figsize=(6 * n_groups, 5))
    if n_groups == 1:
        axes = [axes]

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

    for ax, (group_name, indicators) in zip(axes, indicator_groups.items()):
        x = np.arange(len(indicators))
        width = 0.8 / len(cities)

        for i, city in enumerate(cities):
            values = [city_metrics_dict[city].get(ind, 0) for ind in indicators]
            ax.bar(
                x + i * width, values, width,
                label=city, color=colors[i % len(colors)]
            )

        ax.set_xlabel("指標")
        ax.set_ylabel("値")
        ax.set_title(group_name, fontweight="bold")
        ax.set_xticks(x + width * (len(cities) - 1) / 2)
        ax.set_xticklabels(indicators, rotation=45, ha="right", fontsize=7)
        ax.legend(fontsize=8)

    if title:
        fig.suptitle(title, fontsize=14, fontweight="bold")

    plt.tight_layout()
    return fig


def plot_subarea_comparison(subarea_metrics, area_type="coastal", title=""):
    """沿岸部vs内陸部、駅周辺の比較チャート

    Parameters
    ----------
    subarea_metrics : dict
        {都市名: {"沿岸部": {指標dict}, "内陸部": {指標dict}}} 等
    area_type : str
        "coastal"（沿岸部vs内陸部）または "station"（駅周辺）
    title : str
        チャートのタイトル

    Returns
    -------
    matplotlib.figure.Figure
    """
    from src.network_metrics import NetworkMetricsCalculator

    indicators = NetworkMetricsCalculator.FEATURE_COLUMNS
    cities = list(subarea_metrics.keys())
    subareas = list(next(iter(subarea_metrics.values())).keys())

    fig, axes = plt.subplots(
        len(cities), 1, figsize=(12, 4 * len(cities)), squeeze=False
    )

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

    for row, city in enumerate(cities):
        ax = axes[row, 0]
        x = np.arange(len(indicators))
        width = 0.8 / len(subareas)

        for i, subarea in enumerate(subareas):
            values = [
                subarea_metrics[city].get(subarea, {}).get(ind, 0)
                for ind in indicators
            ]
            ax.bar(
                x + i * width, values, width,
                label=subarea, color=colors[i % len(colors)]
            )

        ax.set_title(city, fontweight="bold")
        ax.set_xticks(x + width * (len(subareas) - 1) / 2)
        ax.set_xticklabels(indicators, rotation=45, ha="right", fontsize=7)
        ax.legend(fontsize=8)

    if title:
        fig.suptitle(title, fontsize=14, fontweight="bold")

    plt.tight_layout()
    return fig


def plot_liu_typology_comparison(city_metrics, liu_type_profiles, title=""):
    """劉（2016）の4類型プロファイルと本分析結果の対照レーダーチャート

    Parameters
    ----------
    city_metrics : dict
        {都市名: {指標名: 値}} の辞書
    liu_type_profiles : dict
        {類型名: {指標名: 正規化された値}} の辞書
    title : str
        チャートのタイトル

    Returns
    -------
    matplotlib.figure.Figure
    """
    from src.network_metrics import NetworkMetricsCalculator

    indicators = NetworkMetricsCalculator.FEATURE_COLUMNS

    # 全データを結合して正規化
    all_data = {}
    all_data.update(city_metrics)
    all_data.update(liu_type_profiles)

    df = pd.DataFrame(all_data).T
    available = [col for col in indicators if col in df.columns]
    df = df[available].fillna(0)
    df_norm = (df - df.min()) / (df.max() - df.min() + 1e-10)

    num_vars = len(available)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    # 都市データ（実線）
    city_colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for i, city in enumerate(city_metrics.keys()):
        if city in df_norm.index:
            values = df_norm.loc[city].tolist()
            values += values[:1]
            ax.plot(
                angles, values, "o-",
                linewidth=2, color=city_colors[i % len(city_colors)], label=city
            )
            ax.fill(angles, values, alpha=0.1, color=city_colors[i % len(city_colors)])

    # 類型データ（点線）
    type_colors = ["#aec7e8", "#ffbb78", "#98df8a", "#ff9896"]
    for i, type_name in enumerate(liu_type_profiles.keys()):
        if type_name in df_norm.index:
            values = df_norm.loc[type_name].tolist()
            values += values[:1]
            ax.plot(
                angles, values, "--",
                linewidth=1.5, color=type_colors[i % len(type_colors)],
                label=type_name, alpha=0.7
            )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(available, fontsize=8)
    ax.set_ylim(0, 1)
    ax.legend(loc="upper right", bbox_to_anchor=(1.4, 1.1), fontsize=9)

    if title:
        ax.set_title(title, y=1.08, fontweight="bold", fontsize=14)

    plt.tight_layout()
    return fig
