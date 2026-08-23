#!/usr/bin/env python3
"""FOSS4G 2026 北木島 口頭発表用の新規図版（P6・P8・P12）を生成する。

公開済みの追跡データ（`docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson`）
のみを入力とし、`tmp/`（Git管理外のキャッシュ）やネットワークアクセスには依存しない。
配色は `scripts/generate_exp002_poster_figures.py` のポスター配色定数
（COL_TEXT / COL_WATER / COL_VEG / COL_STONE）を流用し、ポスターと発表資料の
見た目を揃える。ただし背景の陸域シルエットは衛星バンドから再導出せず、
中性色の背景＋スケールバーのみとする（Task 1 の判断: tmp/ 依存の回避）。

出力先: docs/presentations/images/
    p06_clusters_map.png         — 検出145ポリゴン + 4集中地帯（英語ラベル）
    p08_visit_anchors_map.png    — 同じ地図 + 座標確認済み訪問4地点（凡例つき）
    p12_loop_diagram.png         — 「衛星 → 現地 → 地図」の3ステップフロー図

実行方法:
    uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py

再実行時にバイト一致するよう、実行日時・乱数・辞書順序等は一切使用しない。
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pyproj
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle
from PIL import Image
from shapely.geometry import shape as shapely_shape
from shapely.ops import transform as shapely_transform

# ---------------------------------------------------------------- 定数
PROJECT_ROOT = Path(__file__).resolve().parents[2]
GEOJSON_PATH = (
    PROJECT_ROOT
    / "docs"
    / "results"
    / "exp002"
    / "exp002_kitagi_summer_water_polygons_2025-08-02.geojson"
)
OUT_DIR = Path(__file__).resolve().parent / "images"

# ポスターの配色（scripts/generate_exp002_poster_figures.py と同一。見た目を揃える）
COL_TEXT = "#2b2b2b"
COL_WATER = "#0d47a1"
COL_VEG = "#4a7c46"  # 本図版では直接使用しないが、配色定数として保持（同一ファミリー）
COL_STONE = "#b0a999"

# 中性色の背景（陸域シルエットは描かず、COL_STONE を薄めた中性トーンのみ使用）
COL_BG_NEUTRAL = "#f4f2ee"
COL_WATER_EDGE = "#062a52"

# 地図の描画範囲（検出ポリゴン145件の実際の分布に、訪問4地点を含む余白を付けた範囲）
MAP_BBOX = [133.514, 34.367, 133.562, 34.402]  # [west, south, east, north]
MAP_CENTER_LAT = 34.384

# 訪問4地点（Task 0 の踏査地点と同一の座標。scripts/build_chiri_koryu_figures.py の
# waypoints と一致させること。Task 1 の preflight ruling により verbatim で固定）
VISIT_ANCHORS = [
    ("Toyoura Port", 133.5369, 34.3956),
    ("Toyoura hall", 133.5364, 34.3943),
    ("Lake stage (Keirin)", 133.5329, 34.3912),
    ("Sen-no-hama", 133.5309, 34.3930),
]

_to_3857 = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True).transform

plt.rcParams["font.family"] = ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.color"] = COL_TEXT
plt.rcParams["axes.edgecolor"] = COL_TEXT


# ---------------------------------------------------------------- データ読込
def load_polygons() -> list[dict]:
    """公開GeoJSON（145件）を読み込み、面積降順のまま返す。"""
    geojson = json.loads(GEOJSON_PATH.read_text(encoding="utf-8"))
    return geojson["features"]


def polygon_centroid_lonlat(feature: dict) -> tuple[float, float]:
    """ポリゴンの外環頂点の単純平均から代表点（経度・緯度）を求める。"""
    coords = feature["geometry"]["coordinates"][0]
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    return sum(lons) / len(lons), sum(lats) / len(lats)


def classify_zone(lon: float, lat: float) -> str:
    """ポリゴン代表点を4つの地理的ゾーン（north/south-east/west/centre）に振り分ける。

    北木島全体の緯度・経度分布を目視で確認した上で決めた単純な閾値ルールであり、
    統計的クラスタリング（k-means等）ではない。既存資料（proposal / qa / talk_script）
    が述べる「north・south-east・centre・west に集中」という記述と対応させるための
    説明的な区分であり、境界線自体をスライド上で主張するものではない。
    """
    if lat < 34.383:
        return "south-east"
    if lon < 133.531:
        return "west"
    if lat >= 34.389:
        return "north"
    return "centre"


# ---------------------------------------------------------------- 地図描画の共通部分
def setup_map_axes(ax, bbox=MAP_BBOX):
    west, south, east, north = bbox
    xmin, ymin = _to_3857(west, south)
    xmax, ymax = _to_3857(east, north)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor(COL_BG_NEUTRAL)
    for spine in ax.spines.values():
        spine.set_edgecolor(COL_TEXT)
        spine.set_linewidth(0.8)


def add_scalebar(ax, lat: float = MAP_CENTER_LAT, km: float = 1.0, fontsize: int = 13):
    """左下に簡易スケールバーを描く（Web Mercator の緯度補正込み。ポスター図版と同一手法）。"""
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    length = km * 1000.0 / np.cos(np.radians(lat))
    x0 = xmin + (xmax - xmin) * 0.05
    y0 = ymin + (ymax - ymin) * 0.05
    ax.plot(
        [x0, x0 + length], [y0, y0],
        color=COL_TEXT, linewidth=3, solid_capstyle="butt", zorder=20,
    )
    ax.text(
        x0 + length / 2,
        y0 + (ymax - ymin) * 0.015,
        f"{km:g} km",
        ha="center",
        va="bottom",
        fontsize=fontsize,
        color=COL_TEXT,
        zorder=20,
    )


def draw_water_polygons(ax, features: list[dict]) -> None:
    """検出水域ポリゴンを塗る（配色はポスターF3と同一）。"""
    for feature in features:
        poly = shapely_shape(feature["geometry"])
        poly_3857 = shapely_transform(_to_3857, poly)
        polys = [poly_3857] if poly_3857.geom_type == "Polygon" else list(poly_3857.geoms)
        for p in polys:
            xs, ys = p.exterior.xy
            ax.fill(
                xs, ys, color=COL_WATER, alpha=0.95, edgecolor=COL_WATER_EDGE,
                linewidth=0.4, zorder=5,
            )


def report_size(path: Path) -> None:
    with Image.open(path) as img:
        w, h = img.size
    print(f"saved: {path.relative_to(PROJECT_ROOT)} ({w} x {h} px)")


# ---------------------------------------------------------------- P6: 検出分布図 + 4集中地帯
def make_p06_clusters_map(features: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(11.0, 9.4), dpi=200)
    setup_map_axes(ax)
    draw_water_polygons(ax, features)

    # ゾーンごとの代表点（各ゾーンの重心）を求め、ラベルを注記する
    zone_points: dict[str, list[tuple[float, float]]] = {
        "north": [], "south-east": [], "west": [], "centre": [],
    }
    for feature in features:
        lon, lat = polygon_centroid_lonlat(feature)
        zone_points[classify_zone(lon, lat)].append((lon, lat))

    # ラベルテキストとオフセット（重心から見やすい方向へずらす。単位: メートル、3857座標系）
    label_config = {
        "north": {"dx": 0, "dy": 220},
        "south-east": {"dx": 260, "dy": -60},
        "west": {"dx": -260, "dy": 40},
        "centre": {"dx": -40, "dy": -220},
    }
    for zone_name, points in zone_points.items():
        lons = [p[0] for p in points]
        lats = [p[1] for p in points]
        centroid_lon = sum(lons) / len(lons)
        centroid_lat = sum(lats) / len(lats)
        cx, cy = _to_3857(centroid_lon, centroid_lat)
        dx = label_config[zone_name]["dx"] * 1.0
        dy = label_config[zone_name]["dy"] * 1.0
        ax.annotate(
            zone_name,
            xy=(cx, cy),
            xytext=(cx + dx, cy + dy),
            fontsize=17,
            weight="bold",
            ha="center",
            va="center",
            color=COL_TEXT,
            zorder=15,
            arrowprops=dict(arrowstyle="-", color=COL_TEXT, linewidth=1.0),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COL_TEXT, alpha=0.92),
        )

    ax.set_title(
        f"Detected water polygons cluster in four zones — Summer 2025-08-02 · {len(features)} polygons",
        fontsize=18,
    )
    add_scalebar(ax)

    plt.tight_layout()
    out = OUT_DIR / "p06_clusters_map.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    report_size(out)


# ---------------------------------------------------------------- P8: 検出分布図 + 訪問4地点
def make_p08_visit_anchors_map(features: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(11.0, 9.4), dpi=200)
    setup_map_axes(ax)
    draw_water_polygons(ax, features)

    # 訪問4地点: 検出ポリゴンとは明確に異なる記号（黒い三角＋白縁）で重ねる。
    # これらは行程上の訪問地点であり、確認済みの丁場池ではない（凡例で明示する）。
    # 4地点は互いに300m前後しか離れていないため、ラベルは重心から放射状に
    # オフセットし、リーダー線（細線）でマーカーと結んで重なりを避ける。
    label_offsets_m = {
        "Toyoura Port": (300, 240),
        "Toyoura hall": (520, -70),
        "Lake stage (Keirin)": (60, -340),
        "Sen-no-hama": (-520, 60),
    }
    # マーカーを先に全て描き、ラベル（リーダー線付き）は後で重ねる。
    marker_xy = {}
    for name, lon, lat in VISIT_ANCHORS:
        x, y = _to_3857(lon, lat)
        marker_xy[name] = (x, y)
        ax.plot(
            x, y, marker="^", color="black", markersize=14,
            markeredgecolor="white", markeredgewidth=1.4, zorder=21,
        )
    for name, lon, lat in VISIT_ANCHORS:
        x, y = marker_xy[name]
        dx, dy = label_offsets_m[name]
        ax.annotate(
            name,
            xy=(x, y),
            xytext=(x + dx, y + dy),
            fontsize=12,
            ha="center",
            va="center",
            color=COL_TEXT,
            zorder=22,
            arrowprops=dict(arrowstyle="-", color=COL_TEXT, linewidth=0.9),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=COL_TEXT, alpha=0.92),
        )

    ax.set_title(
        f"Visit anchors are route points, not confirmed ponds — {len(features)} detected polygons",
        fontsize=17,
    )
    add_scalebar(ax)

    legend_handles = [
        Line2D(
            [], [], marker="^", color="black", markeredgecolor="white",
            markeredgewidth=1.4, linestyle="None", markersize=12,
            label="Georeferenced visit anchors",
        ),
        Rectangle(
            (0, 0), 1, 1, facecolor=COL_WATER, edgecolor=COL_WATER_EDGE,
            label="Detected water polygons",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower right",
        fontsize=12,
        framealpha=0.92,
        edgecolor=COL_TEXT,
    )

    plt.tight_layout()
    out = OUT_DIR / "p08_visit_anchors_map.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    report_size(out)


# ---------------------------------------------------------------- P12: 3ステップフロー図
def make_p12_loop_diagram() -> None:
    steps = [
        ("Satellite scan", "a finite candidate list"),
        ("Field visit", "see it with your own eyes"),
        ("OpenStreetMap", "put what you confirmed on the public map"),
    ]

    box_w, box_h = 3.0, 1.4
    gap = 1.4
    n = len(steps)
    total_w = n * box_w + (n - 1) * gap
    fig, ax = plt.subplots(figsize=(11.0, 4.2), dpi=200)
    ax.set_xlim(0, total_w)
    ax.set_ylim(0, 3.2)
    ax.axis("off")

    centers = []
    for i, (title, caption) in enumerate(steps):
        x0 = i * (box_w + gap)
        y0 = 1.1
        rect = Rectangle(
            (x0, y0), box_w, box_h,
            facecolor="white", edgecolor=COL_TEXT, linewidth=1.6,
            joinstyle="miter", zorder=5,
        )
        ax.add_patch(rect)
        cx, cy = x0 + box_w / 2, y0 + box_h / 2
        centers.append((x0, x0 + box_w, cy))
        ax.text(
            cx, cy, title, ha="center", va="center",
            fontsize=17, weight="bold", color=COL_TEXT, zorder=6,
        )
        ax.text(
            cx, y0 - 0.22, caption, ha="center", va="top",
            fontsize=13, color=COL_TEXT, style="italic", zorder=6,
        )

    # 細い無彩色の矢印で3つの矩形を接続する
    arrow_color = "#7a7a7a"
    for i in range(n - 1):
        _, x_end, y_mid_a = centers[i]
        x_start, _, y_mid_b = centers[i + 1]
        arrow = FancyArrowPatch(
            (x_end + 0.06, y_mid_a), (x_start - 0.06, y_mid_b),
            arrowstyle="-|>", mutation_scale=16,
            color=arrow_color, linewidth=1.4, zorder=4,
        )
        ax.add_patch(arrow)

    plt.tight_layout()
    out = OUT_DIR / "p12_loop_diagram.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    report_size(out)


# ---------------------------------------------------------------- main
def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    features = load_polygons()
    print(f"loaded {len(features)} polygons from {GEOJSON_PATH.relative_to(PROJECT_ROOT)}")

    make_p06_clusters_map(features)
    make_p08_visit_anchors_map(features)
    make_p12_loop_diagram()
    print("All presentation figures generated.")


if __name__ == "__main__":
    main()
