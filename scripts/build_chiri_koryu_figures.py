"""地理交流広場第10号 北木島訪問記の新規図版（図1・図4・図8・図9）を生成する。

実行方法:
    uv run python scripts/build_chiri_koryu_figures.py

生成される図版:
    docs/articles/2026_chiri-koryu-10/figures/fig01_location_map.png
    docs/articles/2026_chiri-koryu-10/figures/fig04_walking_route.png
    docs/articles/2026_chiri-koryu-10/figures/fig08_water_distribution.png
    docs/articles/2026_chiri-koryu-10/figures/fig09_multiscale.png

注: 図2・3・5・6 はユーザ撮影写真、図7 は exp002 の既存図版（コピー済）。
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import shape

# プロジェクトパス
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = PROJECT_ROOT / "docs" / "articles" / "2026_chiri-koryu-10"
FIGURES = ARTICLE_DIR / "figures"
TMP = PROJECT_ROOT / "tmp"
RESULTS = PROJECT_ROOT / "docs" / "results" / "exp002"

# 北木島の中心と範囲（exp002 の設定と同じ）
KITAGI_CENTER = (133.543, 34.374)  # (lon, lat)
KITAGI_BBOX = (133.515, 34.350, 133.570, 34.400)  # (W, S, E, N)

# matplotlib の日本語フォント設定（macOS）
plt.rcParams["font.family"] = [
    "Hiragino Sans",
    "Yu Gothic",
    "Meiryo",
    "Noto Sans CJK JP",
    "sans-serif",
]
plt.rcParams["axes.unicode_minus"] = False


def make_fig01_location() -> None:
    """図1: 北木島の位置図（西日本俯瞰 + 笠岡諸島拡大の2パネル）。"""
    fig, axes = plt.subplots(1, 2, figsize=(8, 4), gridspec_kw={"width_ratios": [1, 1.2]})

    # 左パネル: 西日本俯瞰
    ax1 = axes[0]
    cities = {
        "大阪": (135.50, 34.70),
        "岡山": (133.93, 34.66),
        "広島": (132.46, 34.39),
        "高松": (134.04, 34.34),
        "松山": (132.77, 33.84),
    }
    for name, (lon, lat) in cities.items():
        ax1.plot(lon, lat, "o", color="dimgray", markersize=4)
        ax1.text(lon + 0.10, lat, name, fontsize=8, va="center")

    ax1.plot(*KITAGI_CENTER, "*", color="red", markersize=14, zorder=5)
    ax1.text(
        KITAGI_CENTER[0] + 0.15,
        KITAGI_CENTER[1] - 0.10,
        "北木島",
        fontsize=10,
        color="red",
        va="top",
        weight="bold",
    )

    ax1.set_xlim(131.5, 137.0)
    ax1.set_ylim(33.4, 35.6)
    ax1.set_aspect("equal")
    ax1.grid(True, alpha=0.3, linestyle="--")
    ax1.set_xlabel("経度", fontsize=9)
    ax1.set_ylabel("緯度", fontsize=9)
    ax1.set_title("(a) 西日本における位置", fontsize=10)

    # 右パネル: 笠岡諸島
    ax2 = axes[1]
    ports_islands = {
        "笠岡港 (伏越港)": (133.498, 34.500, "s", "black", 7),
        "高島": (133.513, 34.470, "o", "gray", 5),
        "白石島": (133.515, 34.430, "o", "gray", 5),
        "北木島": (133.543, 34.374, "*", "red", 14),
        "真鍋島": (133.560, 34.330, "o", "gray", 5),
    }
    for name, (lon, lat, marker, color, size) in ports_islands.items():
        ax2.plot(lon, lat, marker, color=color, markersize=size, zorder=5)
        weight = "bold" if name == "北木島" else "normal"
        ax2.text(
            lon + 0.005,
            lat,
            name,
            fontsize=9 if name == "北木島" else 8,
            color=color if name == "北木島" else "dimgray",
            va="center",
            weight=weight,
        )

    ax2.set_xlim(133.46, 133.62)
    ax2.set_ylim(34.30, 34.52)
    ax2.set_aspect("equal")
    ax2.grid(True, alpha=0.3, linestyle="--")
    ax2.set_xlabel("経度", fontsize=9)
    ax2.set_ylabel("緯度", fontsize=9)
    ax2.set_title("(b) 笠岡諸島", fontsize=10)

    plt.tight_layout()
    out = FIGURES / "fig01_location_map.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"saved: {out}")


def make_fig04_walking_route() -> None:
    """図4: 当日の主な訪問地と移動順序（簡易版）。"""
    fig, ax = plt.subplots(1, 1, figsize=(7, 6))

    # 主要訪問地（座標は推定値、実際の YAMAP ルートを反映する場合は GPX 取得が望ましい）
    waypoints = [
        ("北木大浦港", 133.520, 34.358),
        ("島内集会所", 133.528, 34.366),
        ("湖上ステージ\n(桂林)", 133.5421, 34.3781),
        ("地ノ浜", 133.555, 34.385),
    ]

    # 移動経路を線で結ぶ
    xs = [w[1] for w in waypoints]
    ys = [w[2] for w in waypoints]
    ax.plot(xs, ys, "-", color="black", linewidth=2, alpha=0.6, zorder=1)

    # 各地点をマーカーで描画
    for name, lon, lat in waypoints:
        if "桂林" in name:
            ax.plot(lon, lat, "*", color="red", markersize=14, zorder=2)
            ax.annotate(
                name,
                xy=(lon, lat),
                xytext=(10, 10),
                textcoords="offset points",
                fontsize=10,
                color="red",
                weight="bold",
            )
        else:
            ax.plot(lon, lat, "o", color="black", markersize=8, zorder=2)
            ax.annotate(
                name,
                xy=(lon, lat),
                xytext=(10, 10),
                textcoords="offset points",
                fontsize=9,
            )

    ax.set_xlim(KITAGI_BBOX[0], KITAGI_BBOX[2])
    ax.set_ylim(KITAGI_BBOX[1], KITAGI_BBOX[3])
    ax.set_aspect("equal")
    ax.ticklabel_format(useOffset=False, style="plain")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_xlabel("経度", fontsize=9)
    ax.set_ylabel("緯度", fontsize=9)
    ax.set_title("当日の主な訪問地と移動順序", fontsize=11)

    plt.tight_layout()
    out = FIGURES / "fig04_walking_route.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"saved: {out}")


def make_fig08_water_distribution() -> None:
    """図8: 145件の水域分布図（exp002 の geojson から描画）。"""
    geojson_path = TMP / "exp002_kitagi_water_bodies.geojson"
    if not geojson_path.exists():
        print(f"WARN: {geojson_path} が見つかりません。図8はスキップ。")
        return

    with open(geojson_path) as f:
        gj = json.load(f)

    fig, ax = plt.subplots(1, 1, figsize=(8, 7))

    # 島内のポリゴンのみフィルタ（海域は面積で除外。島面積≒7.5km²、最大丁場≒8000m²）
    SEA_AREA_THRESHOLD_M2 = 100_000
    polygons_island = []
    for feat in gj["features"]:
        geom = shape(feat["geometry"])
        cx, cy = geom.centroid.x, geom.centroid.y
        area_m2 = feat["properties"].get("area_m2", 0)
        in_bbox = (
            KITAGI_BBOX[0] <= cx <= KITAGI_BBOX[2]
            and KITAGI_BBOX[1] <= cy <= KITAGI_BBOX[3]
        )
        if in_bbox and area_m2 < SEA_AREA_THRESHOLD_M2:
            polygons_island.append(geom)

    # 描画
    for poly in polygons_island:
        if poly.geom_type == "Polygon":
            xs, ys = poly.exterior.xy
            ax.fill(xs, ys, color="black", alpha=0.85)
        elif poly.geom_type == "MultiPolygon":
            for p in poly.geoms:
                xs, ys = p.exterior.xy
                ax.fill(xs, ys, color="black", alpha=0.85)

    # 桂林の位置（南東部の主要丁場跡水域に相当）
    keirin_pos = (133.5421, 34.3781)
    ax.plot(*keirin_pos, "*", color="red", markersize=16, zorder=5)
    ax.annotate(
        "桂林",
        xy=keirin_pos,
        xytext=(12, 8),
        textcoords="offset points",
        fontsize=10,
        color="red",
        weight="bold",
    )

    ax.set_xlim(KITAGI_BBOX[0], KITAGI_BBOX[2])
    ax.set_ylim(KITAGI_BBOX[1], KITAGI_BBOX[3])
    ax.set_aspect("equal")
    ax.ticklabel_format(useOffset=False, style="plain")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_xlabel("経度", fontsize=9)
    ax.set_ylabel("緯度", fontsize=9)
    ax.set_title(
        f"検出された島内水域 ({len(polygons_island)}件、面積100m²以上)", fontsize=11
    )

    plt.tight_layout()
    out = FIGURES / "fig08_water_distribution.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"saved: {out} ({len(polygons_island)} polygons)")


def make_fig09_multiscale() -> None:
    """図9: 同一場所を徒歩・ドローン・衛星の三スケールで並べた合成図。"""
    img_walk = Image.open(FIGURES / "fig02_keirin_cliff.jpg").convert("RGB")
    img_drone = Image.open(FIGURES / "fig06_aerial_quarries.jpg").convert("RGB")
    img_satellite = Image.open(RESULTS / "exp002_geotiff_preview.png").convert("RGB")

    # 横幅を揃える
    target_w = 1000

    def resize(img: Image.Image, w: int) -> Image.Image:
        ratio = w / img.width
        h = int(img.height * ratio)
        return img.resize((w, h), Image.LANCZOS)

    img_walk = resize(img_walk, target_w)
    img_drone = resize(img_drone, target_w)
    img_satellite = resize(img_satellite, target_w)

    # ラベル領域の高さ
    label_h = 40
    composite_h = img_walk.height + img_drone.height + img_satellite.height + label_h * 3
    composite = Image.new("RGB", (target_w, composite_h), "white")

    # フォント
    try:
        font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 22)
    except OSError:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(composite)

    panels = [
        ("(a) 徒歩スケール — 桂林の岩壁前", img_walk),
        ("(b) ドローンスケール — 上空からの丁場群", img_drone),
        ("(c) 衛星スケール — Sentinel-2 トゥルーカラー合成", img_satellite),
    ]

    y = 0
    for label, img in panels:
        draw.text((20, y + 8), label, fill="black", font=font)
        y += label_h
        composite.paste(img, (0, y))
        y += img.height

    out = FIGURES / "fig09_multiscale.png"
    composite.save(out, "PNG", optimize=True)
    print(f"saved: {out} ({composite.size})")


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    make_fig01_location()
    make_fig04_walking_route()
    make_fig08_water_distribution()
    make_fig09_multiscale()
    print("All figures generated.")


if __name__ == "__main__":
    main()
