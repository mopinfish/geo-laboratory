"""地理交流広場第10号 北木島訪問記の新規図版（図2・図4・図8・図9）を生成する。

実行方法:
    uv run python scripts/build_chiri_koryu_figures.py

生成される図版:
    docs/articles/2026_chiri-koryu-10/figures/fig02_location_map.png
    docs/articles/2026_chiri-koryu-10/figures/fig04_walking_route.png
    docs/articles/2026_chiri-koryu-10/figures/fig08_water_distribution.png
    docs/articles/2026_chiri-koryu-10/figures/fig09_multiscale.png

注: 図1（湖上ステージ）・図3（桂林岩壁）・図5（ドローン離陸）・図6（上空からの丁場群）
   はユーザ撮影写真。図7 は exp002 の既存図版（コピー済）。
   背景地図は地理院淡色タイル（淡色地図）を使用。出典は記事の注に記載。
"""

from __future__ import annotations

import json
from pathlib import Path

import contextily as cx
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import shape
from shapely.ops import transform as shapely_transform
import pyproj

# プロジェクトパス
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = PROJECT_ROOT / "docs" / "articles" / "2026_chiri-koryu-10"
FIGURES = ARTICLE_DIR / "figures"
TMP = PROJECT_ROOT / "tmp"
RESULTS = PROJECT_ROOT / "docs" / "results" / "exp002"

# 北木島の中心と範囲（exp002 の設定と同じ）
KITAGI_CENTER = (133.543, 34.374)  # (lon, lat)
KITAGI_BBOX = (133.515, 34.350, 133.570, 34.400)  # (W, S, E, N)

# 地理院淡色タイル（XYZ 形式）— モノクロ印刷耐性が高い
GSI_PALE = "https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png"
GSI_ATTR = "地理院タイル（淡色地図）"

# 投影変換用ヘルパ（lat/lon → Web Mercator EPSG:3857）
_to_3857 = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True).transform


def lonlat_to_3857(lon: float, lat: float) -> tuple[float, float]:
    return _to_3857(lon, lat)


# matplotlib の日本語フォント設定（macOS）
plt.rcParams["font.family"] = [
    "Hiragino Sans",
    "Yu Gothic",
    "Meiryo",
    "Noto Sans CJK JP",
    "sans-serif",
]
plt.rcParams["axes.unicode_minus"] = False


def _add_gsi_basemap(ax, zoom: int = 11) -> None:
    """地理院淡色タイルを背景地図として追加する。"""
    cx.add_basemap(ax, source=GSI_PALE, zoom=zoom, attribution=False)


def _setup_map_axes(ax, west: float, south: float, east: float, north: float) -> None:
    """地図軸の見た目を整える。X/Y 軸ラベル・目盛りを非表示にする。"""
    xmin, ymin = lonlat_to_3857(west, south)
    xmax, ymax = lonlat_to_3857(east, north)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(0.6)


def _save_as_grayscale(out_path: Path) -> None:
    """カラーで保存された PNG を L (グレースケール) モードに変換して上書き保存。

    モノクロ印刷時の可読性を確保するため、地図系の図に適用する。
    """
    img = Image.open(out_path).convert("L")
    img.save(out_path, "PNG", optimize=True)


def make_fig02_location() -> None:
    """図2: 北木島の位置図（西日本俯瞰 + 笠岡諸島拡大の2パネル、地理院タイル背景）。"""
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2), gridspec_kw={"width_ratios": [1, 1]})

    # 左パネル: 西日本俯瞰
    ax1 = axes[0]
    west, south, east, north = 131.5, 33.4, 137.0, 35.6
    _setup_map_axes(ax1, west, south, east, north)
    _add_gsi_basemap(ax1, zoom=7)

    cities = {
        "大阪": (135.50, 34.70),
        "岡山": (133.93, 34.66),
        "広島": (132.46, 34.39),
        "高松": (134.04, 34.34),
        "松山": (132.77, 33.84),
    }
    for name, (lon, lat) in cities.items():
        x, y = lonlat_to_3857(lon, lat)
        ax1.plot(x, y, "o", color="dimgray", markersize=4, zorder=5)
        ax1.text(x + 8000, y, name, fontsize=8, va="center", zorder=6)

    kx, ky = lonlat_to_3857(*KITAGI_CENTER)
    ax1.plot(kx, ky, "*", color="black", markersize=18, markeredgecolor="white",
             markeredgewidth=1.0, zorder=10)
    ax1.text(kx + 12000, ky - 8000, "北木島", fontsize=10, color="black", va="top", weight="bold", zorder=10)

    ax1.set_title("(a) 西日本における位置", fontsize=10)

    # 右パネル: 笠岡諸島
    ax2 = axes[1]
    west2, south2, east2, north2 = 133.45, 34.30, 133.62, 34.52
    _setup_map_axes(ax2, west2, south2, east2, north2)
    _add_gsi_basemap(ax2, zoom=12)

    ports_islands = {
        "笠岡港 (伏越港)": (133.498, 34.500, "s", "black", 7),
        "高島": (133.513, 34.470, "o", "gray", 5),
        "白石島": (133.515, 34.430, "o", "gray", 5),
        "北木島": (133.543, 34.374, "*", "black", 18),
        "真鍋島": (133.560, 34.330, "o", "gray", 5),
    }
    for name, (lon, lat, marker, color, size) in ports_islands.items():
        x, y = lonlat_to_3857(lon, lat)
        edge = dict(markeredgecolor="white", markeredgewidth=1.0) if name == "北木島" else {}
        ax2.plot(x, y, marker, color=color, markersize=size, zorder=10, **edge)
        weight = "bold" if name == "北木島" else "normal"
        ax2.text(x + 400, y, name, fontsize=9 if name == "北木島" else 8,
                 color="black", va="center", weight=weight, zorder=10)

    ax2.set_title("(b) 笠岡諸島", fontsize=10)

    plt.tight_layout()
    out = FIGURES / "fig02_location_map.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    _save_as_grayscale(out)
    print(f"saved (grayscale): {out}")


def make_fig04_walking_route() -> None:
    """図4: 当日の主な訪問地と移動順序（地理院タイル背景）。

    全ての訪問地が島の北部に集中するため、北部のみを拡大して描画する。
    """
    fig, ax = plt.subplots(1, 1, figsize=(7, 6))

    # 北部に拡大（全ウェイポイントは lon 133.530-133.537, lat 34.391-34.396 の範囲）
    west, south, east, north = 133.525, 34.387, 133.545, 34.400
    _setup_map_axes(ax, west, south, east, north)
    _add_gsi_basemap(ax, zoom=15)

    # 主要訪問地（OSM／ユーザ提示の度分秒に基づく実座標）
    waypoints = [
        ("豊浦港", 133.5369, 34.3956),         # OSM ferry_terminal「北木島 豊浦」
        ("豊浦公会堂", 133.5364, 34.3943),     # OSM 北木島郵便局近傍に推定
        ("湖上ステージ\n(桂林)", 133.5329, 34.3912),  # OSM「今岡石材丁場跡（北木の桂林）」
        ("千ノ浜", 133.5309, 34.3930),         # ユーザ提示 34°23'34.8"N 133°31'51.3"E
    ]

    # 移動経路を線で結ぶ（Web Mercator 座標で、モノクロ対応で黒線・破線）
    pts = [(lonlat_to_3857(lon, lat), name) for name, lon, lat in waypoints]
    xs = [p[0][0] for p in pts]
    ys = [p[0][1] for p in pts]
    ax.plot(xs, ys, "-", color="black", linewidth=2.5, alpha=0.95, zorder=4)

    for (x, y), name in pts:
        if "桂林" in name:
            ax.plot(x, y, "*", color="black", markersize=20, markeredgecolor="white",
                    markeredgewidth=1.5, zorder=10)
            ax.annotate(name, xy=(x, y), xytext=(14, 12), textcoords="offset points",
                        fontsize=10, color="black", weight="bold", zorder=10,
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.9))
        else:
            ax.plot(x, y, "o", color="black", markersize=10, markeredgecolor="white",
                    markeredgewidth=1.0, zorder=10)
            ax.annotate(name, xy=(x, y), xytext=(12, 10), textcoords="offset points",
                        fontsize=9, color="black", zorder=10,
                        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="black", alpha=0.9))

    ax.set_title("当日の主な訪問地と移動順序", fontsize=11)

    plt.tight_layout()
    out = FIGURES / "fig04_walking_route.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    _save_as_grayscale(out)
    print(f"saved (grayscale): {out}")


def make_fig08_water_distribution() -> None:
    """図8: 145件の水域分布図（exp002 の geojson から描画、地理院タイル背景）。"""
    geojson_path = TMP / "exp002_kitagi_water_bodies.geojson"
    if not geojson_path.exists():
        print(f"WARN: {geojson_path} が見つかりません。図8はスキップ。")
        return

    with open(geojson_path) as f:
        gj = json.load(f)

    fig, ax = plt.subplots(1, 1, figsize=(8, 7))
    west, south, east, north = KITAGI_BBOX
    _setup_map_axes(ax, west, south, east, north)
    _add_gsi_basemap(ax, zoom=14)

    # 島内のポリゴンのみフィルタ（海域は面積で除外。島面積≒7.5km²、最大丁場≒8000m²）
    SEA_AREA_THRESHOLD_M2 = 100_000
    polygons_island = []
    for feat in gj["features"]:
        geom = shape(feat["geometry"])
        cx_lon, cy_lat = geom.centroid.x, geom.centroid.y
        area_m2 = feat["properties"].get("area_m2", 0)
        in_bbox = (
            KITAGI_BBOX[0] <= cx_lon <= KITAGI_BBOX[2]
            and KITAGI_BBOX[1] <= cy_lat <= KITAGI_BBOX[3]
        )
        if in_bbox and area_m2 < SEA_AREA_THRESHOLD_M2:
            polygons_island.append(geom)

    # 各ポリゴンを Web Mercator に変換して描画（モノクロ対応で黒塗り）
    project = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True).transform
    for poly in polygons_island:
        poly_3857 = shapely_transform(project, poly)
        if poly_3857.geom_type == "Polygon":
            xs, ys = poly_3857.exterior.xy
            ax.fill(xs, ys, color="black", alpha=0.85, edgecolor="black", linewidth=0.5, zorder=5)
        elif poly_3857.geom_type == "MultiPolygon":
            for p in poly_3857.geoms:
                xs, ys = p.exterior.xy
                ax.fill(xs, ys, color="black", alpha=0.85, edgecolor="black", linewidth=0.5, zorder=5)

    # 桂林の位置（OSM「今岡石材丁場跡（北木の桂林）」 ノードに基づく、島北部）
    keirin_x, keirin_y = lonlat_to_3857(133.5329, 34.3912)
    ax.plot(keirin_x, keirin_y, "*", color="black", markersize=20, markeredgecolor="white",
            markeredgewidth=1.5, zorder=15)
    ax.annotate("桂林", xy=(keirin_x, keirin_y), xytext=(14, 10),
                textcoords="offset points", fontsize=10, color="black", weight="bold", zorder=15,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.9))

    ax.set_title(
        f"検出された島内水域 ({len(polygons_island)}件、面積100m²以上)", fontsize=11
    )

    plt.tight_layout()
    out = FIGURES / "fig08_water_distribution.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    _save_as_grayscale(out)
    print(f"saved (grayscale): {out} ({len(polygons_island)} polygons)")


def make_fig09_multiscale() -> None:
    """図9: 同一場所を徒歩・ドローン・衛星の三スケールで横並びに並べた合成図。

    縦に並べると合計が縦長すぎて B5 ページからはみ出るため、横3列の構成にする。
    各パネルは中央クロップで縦横比を揃え、ラベルは画像の上部に配置する。
    衛星パネルは exp002 の水域強調 GeoTIFF（RGBA）を rasterio で読んで RGB を取得する。
    """
    import rasterio  # ローカルインポート（重い依存のため）
    import numpy as np

    img_walk = Image.open(FIGURES / "fig03_keirin_cliff.jpg").convert("RGB")
    img_drone = Image.open(FIGURES / "fig06_aerial_quarries.jpg").convert("RGB")

    # 衛星画像は GeoTIFF から直接読む。RGBA の RGB チャネルを使用。
    sat_tif = PROJECT_ROOT / "tmp" / "exp002_kitagi_water_highlighted.tif"
    with rasterio.open(sat_tif) as src:
        data = src.read([1, 2, 3])  # RGB
    rgb_array = np.transpose(data, (1, 2, 0)).astype(np.uint8)
    img_satellite = Image.fromarray(rgb_array, mode="RGB")

    def square_crop(img: Image.Image) -> Image.Image:
        """中央正方形クロップ。"""
        w, h = img.size
        s = min(w, h)
        left = (w - s) // 2
        top = (h - s) // 2
        return img.crop((left, top, left + s, top + s))

    panel_size = 600  # 各パネルの一辺
    panels_imgs = [square_crop(im).resize((panel_size, panel_size), Image.LANCZOS)
                   for im in (img_walk, img_drone, img_satellite)]

    label_h = 40
    gap = 10
    composite_w = panel_size * 3 + gap * 2
    composite_h = panel_size + label_h
    composite = Image.new("RGB", (composite_w, composite_h), "white")

    try:
        font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 22)
    except OSError:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(composite)
    labels = [
        "(a) 徒歩 — 桂林の岩壁前",
        "(b) ドローン — 上空からの丁場群",
        "(c) 衛星 — Sentinel-2 トゥルーカラー",
    ]

    for i, (label, img) in enumerate(zip(labels, panels_imgs)):
        x = i * (panel_size + gap)
        draw.text((x + 10, 6), label, fill="black", font=font)
        composite.paste(img, (x, label_h))

    out = FIGURES / "fig09_multiscale.png"
    composite.save(out, "PNG", optimize=True)
    print(f"saved: {out} ({composite.size})")


COLOR_KEEP_FIGURES = ("fig01", "fig09")  # この接頭辞のファイルだけカラー維持
"""カラーで残す図の prefix。それ以外はグレースケール化される。

理由: 編集者からの「なるべくモノクロにして欲しい」というオーダーに対応。
- 図1: 冒頭の桂林の景観を強くインパクトで見せたいためカラー維持
- 図9: 三スケール比較の視認性を保つためカラー維持
"""


def _convert_remaining_to_grayscale() -> None:
    """カラー維持指定以外のすべての写真・画像をグレースケールに変換する。

    matplotlib で生成した地図系（fig02, fig04, fig08）は既にグレースケールだが、
    写真系（fig03, fig05, fig06）と exp002 由来の解析図（fig07）はカラーなので、
    ここで PIL で grayscale 変換して上書きする。
    """
    for path in sorted(FIGURES.iterdir()):
        if not path.is_file():
            continue
        if any(path.name.startswith(k) for k in COLOR_KEEP_FIGURES):
            continue
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            continue
        img = Image.open(path)
        if img.mode == "L":
            continue  # 既にグレースケール
        gray = img.convert("L")
        if path.suffix.lower() == ".png":
            gray.save(path, "PNG", optimize=True)
        else:
            gray.save(path, "JPEG", quality=92, optimize=True)
        print(f"grayscaled: {path.name}")


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    make_fig02_location()
    make_fig04_walking_route()
    make_fig08_water_distribution()
    make_fig09_multiscale()
    _convert_remaining_to_grayscale()
    print("All figures generated.")


if __name__ == "__main__":
    main()
