#!/usr/bin/env python3
"""FOSS4G 2026 北木島 口頭発表用の新規図版（P6・P8・P12）を生成する。

公開済みの追跡データ（`docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson`）
のみを入力とし、`tmp/`（Git管理外のキャッシュ）やネットワークアクセスには依存しない。
配色は `scripts/generate_exp002_poster_figures.py` のポスター配色定数
（COL_TEXT / COL_WATER / COL_VEG / COL_STONE）を流用し、ポスターと発表資料の
見た目を揃える。ただし背景の陸域シルエットは衛星バンドから再導出せず、
中性色の背景＋スケールバーのみとする（Task 1 の判断: tmp/ 依存の回避）。

出力先: docs/presentations/images/
    p06_clusters_map.png         — 検出145ポリゴン + 4地区（英語ラベル、報告書§4.3準拠）
    p07_three_scales.png         — 三スケール合成図（英語ラベルのみ。Task 4 レビュー
                                    指摘の修正: 日本語記事と共有される
                                    `fig09_multiscale.png` の英語投影面への流用を解消）
    p08_visit_anchors_map.png    — 同じ地図 + 座標確認済み訪問4地点（凡例つき）
    p12_loop_diagram.png         — 「衛星 → 現地 → 地図」の3ステップフロー図

実行方法:
    uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py

再実行時にバイト一致するよう、実行日時・乱数・辞書順序等は一切使用しない。

フォントサイズの検査:
    各図版を保存した直後に、実測ピクセル幅から「配置幅220mmのスライド上で
    何ptに見えるか」を計算し、15pt未満であれば AssertionError で止める
    （`audit_slide_font_sizes` を参照。床の15ptはDESIGN_GUIDEの16:9スライド
    本文フォントの下限）。
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

# 4地区の緯度・経度範囲。
# 出典: docs/reports/exp002_kitagi_quarry_water_detection_report.md §4.3「島内水域の空間分布」
#   1. 島北部　　（34.391〜393°N, 133.533〜538°E）
#   2. 島南東部　（34.376〜378°N, 133.542°E。経度は中心値に±0.001の許容幅を設定）
#   3. 島中央部　（34.387〜390°N, 133.531〜533°E）
#   4. 島西部　　（34.386〜391°N, 133.522〜528°E）
# これは統計的クラスタリングの結果ではなく、報告書が定義した4地区の範囲そのもの。
# ラベルは各地区内に重心を持つ最大ポリゴンの重心に置く（ゾーン平均やバウンディング
# ボックス中心ではない）。地区の範囲に入らないポリゴンも描画するが、ラベルは付けない。
ZONE_EXTENTS: dict[str, tuple[float, float, float, float]] = {
    # zone_name: (lat_min, lat_max, lon_min, lon_max)
    "north": (34.391, 34.393, 133.533, 133.538),
    "south-east": (34.376, 34.378, 133.541, 133.543),
    "centre": (34.387, 34.390, 133.531, 133.533),
    "west": (34.386, 34.391, 133.522, 133.528),
}

# スライド上の実効フォントサイズ検査に使う定数
SLIDE_PLACEMENT_MM = 220.0  # スライド上での図版の配置幅
SAVE_DPI = 200
SLIDE_PT_FLOOR = 15.0  # DESIGN_GUIDE の16:9スライド本文フォント床

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


def polygon_true_centroid_lonlat(feature: dict) -> tuple[float, float]:
    """ポリゴンの面積重心（経度・緯度）を返す。外環頂点の単純平均ではなく、shapelyによる実際の重心。"""
    poly = shapely_shape(feature["geometry"])
    centroid = poly.centroid
    return centroid.x, centroid.y


def polygon_area_m2(feature: dict) -> float:
    """ポリゴンの面積(m^2)をWebメルカトル(EPSG:3857)投影後に計算する。"""
    poly = shapely_shape(feature["geometry"])
    poly_3857 = shapely_transform(_to_3857, poly)
    return poly_3857.area


def find_zone_label_anchor(features: list[dict], zone_name: str) -> tuple[float, float] | None:
    """指定した地区の範囲内に重心を持つポリゴンのうち、最大面積のものの重心を返す。

    ゾーン平均やバウンディングボックス中心ではなく、実際に存在する最大ポリゴンの
    重心にラベルを置くことで、ラベルが実在する検出物を指すようにする。
    範囲内に該当ポリゴンが無い場合は None を返す（強制的な割り当ては行わない）。
    """
    lat_min, lat_max, lon_min, lon_max = ZONE_EXTENTS[zone_name]
    best_area = -1.0
    best_point: tuple[float, float] | None = None
    for feature in features:
        lon, lat = polygon_true_centroid_lonlat(feature)
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            area = polygon_area_m2(feature)
            if area > best_area:
                best_area = area
                best_point = (lon, lat)
    return best_point


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


def add_scalebar(ax, lat: float = MAP_CENTER_LAT, km: float = 1.0, fontsize: float = 20.0):
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


def report_size(path: Path) -> int:
    with Image.open(path) as img:
        w, h = img.size
    print(f"saved: {path.relative_to(PROJECT_ROOT)} ({w} x {h} px)")
    return w


def audit_slide_font_sizes(
    figure_name: str, image_width_px: int, elements: list[tuple[str, float]]
) -> None:
    """220mm配置時のスライド上フォントサイズ(pt)を計算し、15pt未満なら止める。

    slide_pt = native_pt * (dpi/72) / image_width_px * (placement_mm/25.4) * 72

    native_pt はfigure内で指定したフォントサイズ、image_width_px は実際に保存された
    PNGのピクセル幅。dpi・配置幅は本スクリプトの保存設定（200dpi・220mm）と一致させる。
    """
    print(f"\n[{figure_name}] image width = {image_width_px}px, "
          f"placement = {SLIDE_PLACEMENT_MM:g}mm, dpi = {SAVE_DPI}")
    print(f"  {'element':<30s}{'native_pt':>12s}{'slide_pt':>12s}")
    for element, native_pt in elements:
        slide_pt = (
            native_pt
            * (SAVE_DPI / 72)
            / image_width_px
            * (SLIDE_PLACEMENT_MM / 25.4)
            * 72
        )
        print(f"  {element:<30s}{native_pt:>12.1f}{slide_pt:>12.2f}")
        assert slide_pt >= SLIDE_PT_FLOOR, (
            f"{figure_name}: '{element}' の実効サイズ {slide_pt:.2f}pt が "
            f"下限 {SLIDE_PT_FLOOR:g}pt を下回る（native {native_pt}pt）"
        )


# ---------------------------------------------------------------- P6: 検出分布図 + 4地区ラベル
def make_p06_clusters_map(features: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(11.0, 9.4), dpi=SAVE_DPI)
    setup_map_axes(ax)
    draw_water_polygons(ax, features)

    font_elements: list[tuple[str, float]] = []
    zone_label_fontsize = 20.0

    # ラベルのオフセット（地区内最大ポリゴンの重心から見やすい方向へずらす。
    # 単位: メートル、3857座標系）。地図範囲(MAP_BBOX)の外に出ないことを確認済み。
    label_offsets_m = {
        "north": (0, 300),
        "south-east": (230, -220),
        "west": (-260, 60),
        "centre": (-90, -300),
    }
    for zone_name, (dx, dy) in label_offsets_m.items():
        anchor = find_zone_label_anchor(features, zone_name)
        if anchor is None:
            continue  # 地区内に該当ポリゴンが無ければラベルを描かない（強制割当はしない）
        lon, lat = anchor
        cx, cy = _to_3857(lon, lat)
        ax.annotate(
            zone_name,
            xy=(cx, cy),
            xytext=(cx + dx, cy + dy),
            fontsize=zone_label_fontsize,
            weight="bold",
            ha="center",
            va="center",
            color=COL_TEXT,
            zorder=15,
            arrowprops=dict(arrowstyle="-", color=COL_TEXT, linewidth=1.0),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COL_TEXT, alpha=0.92),
        )
        font_elements.append((f"zone label ({zone_name})", zone_label_fontsize))

    title_fontsize = 20.0
    ax.set_title(
        f"Detected water polygons and the four documented quarrying zones "
        f"— {len(features)} polygons",
        fontsize=title_fontsize,
    )
    font_elements.append(("title", title_fontsize))

    scalebar_fontsize = 20.0
    add_scalebar(ax, fontsize=scalebar_fontsize)
    font_elements.append(("scale bar label", scalebar_fontsize))

    plt.tight_layout()
    out = OUT_DIR / "p06_clusters_map.png"
    plt.savefig(out, dpi=SAVE_DPI, bbox_inches="tight", facecolor="white")
    plt.close()
    width_px = report_size(out)
    audit_slide_font_sizes("P6", width_px, font_elements)


# ---------------------------------------------------------------- P8: 検出分布図 + 訪問4地点
def make_p08_visit_anchors_map(features: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(11.0, 9.4), dpi=SAVE_DPI)
    setup_map_axes(ax)
    draw_water_polygons(ax, features)

    font_elements: list[tuple[str, float]] = []
    label_fontsize = 20.0

    # 訪問4地点: 検出ポリゴンとは明確に異なる記号（黒い三角＋白縁）で重ねる。
    # これらは行程上の訪問地点であり、確認済みの丁場池ではない（凡例で明示する）。
    # 4地点は互いに150〜470mしか離れていないため、ラベルは重心から放射状に
    # オフセットし、リーダー線（細線）でマーカーと結んで重なりを避ける。
    label_offsets_m = {
        "Toyoura Port": (480, 380),
        "Toyoura hall": (830, -110),
        "Lake stage (Keirin)": (95, -540),
        "Sen-no-hama": (-830, 95),
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
            fontsize=label_fontsize,
            ha="center",
            va="center",
            color=COL_TEXT,
            zorder=22,
            arrowprops=dict(arrowstyle="-", color=COL_TEXT, linewidth=0.9),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=COL_TEXT, alpha=0.92),
        )
        font_elements.append((f"visit label ({name})", label_fontsize))

    title_fontsize = 20.0
    ax.set_title(
        f"Visit anchors are route points, not confirmed ponds — {len(features)} detected polygons",
        fontsize=title_fontsize,
    )
    font_elements.append(("title", title_fontsize))

    scalebar_fontsize = 20.0
    add_scalebar(ax, fontsize=scalebar_fontsize)
    font_elements.append(("scale bar label", scalebar_fontsize))

    legend_fontsize = 20.0
    legend_handles = [
        Line2D(
            [], [], marker="^", color="black", markeredgecolor="white",
            markeredgewidth=1.4, linestyle="None", markersize=14,
            label="Georeferenced visit anchors",
        ),
        Rectangle(
            (0, 0), 1, 1, facecolor=COL_WATER, edgecolor=COL_WATER_EDGE,
            label="Detected water polygons",
        ),
    ]
    # 凡例フォントを18pt以上に拡大すると地図内(lower right)には収まらないため、
    # 地図の外（下側）に配置する。
    legend = ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.02),
        ncol=2,
        fontsize=legend_fontsize,
        framealpha=0.92,
        edgecolor=COL_TEXT,
    )
    font_elements.append(("legend", legend_fontsize))

    plt.tight_layout()
    out = OUT_DIR / "p08_visit_anchors_map.png"
    plt.savefig(
        out, dpi=SAVE_DPI, bbox_inches="tight", facecolor="white",
        bbox_extra_artists=[legend],
    )
    plt.close()
    width_px = report_size(out)
    audit_slide_font_sizes("P8", width_px, font_elements)


# ---------------------------------------------------------------- P7: 三スケール合成図（英語ラベルのみ）
# S4（`exp002_kitagi_foss4g2026_presentation.py` の `s04()`）で採用した写真スロットの
# アスペクト比（`PHOTO_SLOT_W_IN` / `PHOTO_SLOT_H_IN`）と同じ値をここで再現する。
# 値そのものを import するのではなく定数として複製するのは、本スクリプトが
# tmp/・ネットワークだけでなく presentation.py の実行順序にも依存しない
# （どちらを先に実行しても成立する）ようにするため。
P07_PHOTO_SLOT_AR = 5.6 / 3.15  # 16:9。PHOTO_SLOT_W_IN / PHOTO_SLOT_H_IN と同一
P07_FIG06_VBIAS = 0.2768  # S4 の s04() で fig06_aerial_quarries.jpg に使った値をそのまま再利用


def _load_photo(path: Path) -> Image.Image:
    with Image.open(path) as im:
        return im.convert("RGB").copy()


def _crop_top_bottom_to_aspect(img: Image.Image, target_ar: float, vbias: float) -> Image.Image:
    """画像の上下だけをクロップして目的のアスペクト比 `target_ar` に合わせる。

    `add_picture_cover()`（`exp002_kitagi_foss4g2026_presentation.py`）の
    「必要クロップ量はアスペクト比の差分から一意に決まり、`vbias` が上下の配分を
    決める」という式をここで再現する。本関数は「画像が目的より縦長
    （`img_ar < target_ar`）で上下だけをクロップする」場合のみを扱う
    （fig06_aerial_quarries.jpg はこのケースに該当する）。
    """
    iw, ih = img.size
    img_ar = iw / ih
    assert img_ar < target_ar, "この関数は img_ar < target_ar の場合のみ対応する"
    visible = img_ar / target_ar
    total = 1 - visible
    top_px = round(total * vbias * ih)
    bottom_px = ih - round(total * (1 - vbias) * ih)
    return img.crop((0, top_px, iw, bottom_px))


def make_p07_three_scales(features: list[dict]) -> None:
    """三スケール合成図（英語ラベルのみ）を生成する。

    Task 4 レビュー指摘への対応: S7 に配置していた `fig09_multiscale.png` は
    日本語記事（`docs/articles/2026_chiri-koryu-10/`）と共有される図版で、
    パネル注記が日本語で焼き込まれている上、(b) パネルには動画再生UIの写り込みが
    残っている。英語のみの投影面という契約に抵触するため、発表専用の図版を
    ここで新規に生成する（日本語記事側の図版・生成スクリプトは変更しない）。

    パネル:
        (a) On foot — texture         : choba_lake_3.jpg（S1表紙と同一写真、クロップなし。
                                         Fix round 2 でグレースケールの fig03_keirin_cliff.jpg
                                         から色付きに差し替え）
        (b) From the air — boundaries : fig06_aerial_quarries.jpg を S4 と同じ縦クロップ
                                         （`P07_FIG06_VBIAS`）で動画UIの写り込みを除去
        (c) From orbit — distribution : 検出145ポリゴンの分布（p06/p08と同じ配色・
                                         地図範囲。ゾーンラベル・訪問地点は描かない）

    3パネルは高さを揃えて横並びにする（各パネルの実アスペクト比を列幅の比に使うため、
    letterbox＝余白がほぼ生じない）。
    """
    photo_a = _load_photo(OUT_DIR / "choba_lake_3.jpg")
    ar_a = photo_a.size[0] / photo_a.size[1]

    photo_b = _crop_top_bottom_to_aspect(
        _load_photo(OUT_DIR / "fig06_aerial_quarries.jpg"),
        P07_PHOTO_SLOT_AR, P07_FIG06_VBIAS,
    )
    ar_b = photo_b.size[0] / photo_b.size[1]

    west, south, east, north = MAP_BBOX
    xmin, ymin = _to_3857(west, south)
    xmax, ymax = _to_3857(east, north)
    ar_c = (xmax - xmin) / (ymax - ymin)

    # 3パネルの合計アスペクト比（約3.66）から逆算した高さ。(a) 列は縦長写真
    # （アスペクト比0.75）のため他列より狭く、キャプションを1行で置くと隣の列に
    # 溢れる（実測で確認済み）。P12（Task 4 fix round 1）と同じ「フォントを縮めず
    # 2行に折り返す」方針をここでも採用する。
    panel_height_in = 3.2
    caption_fontsize = 21.0

    fig, (ax_a, ax_b, ax_c) = plt.subplots(
        1, 3, figsize=(panel_height_in * (ar_a + ar_b + ar_c), panel_height_in),
        dpi=SAVE_DPI, gridspec_kw={"width_ratios": [ar_a, ar_b, ar_c], "wspace": 0.05},
    )

    font_elements: list[tuple[str, float]] = []
    title_texts = []
    panels = (
        (ax_a, photo_a, "(a) On foot —\ntexture"),
        (ax_b, photo_b, "(b) From the air —\nboundaries"),
    )
    for ax, photo, label in panels:
        ax.imshow(photo)
        ax.axis("off")
        title_texts.append(ax.set_title(label, fontsize=caption_fontsize, color=COL_TEXT, pad=10))
        font_elements.append((label.replace("\n", " "), caption_fontsize))

    setup_map_axes(ax_c, MAP_BBOX)
    draw_water_polygons(ax_c, features)
    add_scalebar(ax_c, fontsize=caption_fontsize)
    font_elements.append(("scale bar label", caption_fontsize))
    label_c = "(c) From orbit —\ndistribution"
    title_texts.append(ax_c.set_title(label_c, fontsize=caption_fontsize, color=COL_TEXT, pad=10))
    font_elements.append((label_c.replace("\n", " "), caption_fontsize))

    # 各キャプションが自列（ax の描画領域）の幅を超えて隣の列に溢れないことを検査する
    # （(a) 列が縦長写真で狭いため、1行キャプションで実際に衝突する回帰が試作時に
    # 発生した。P12 の caption-vs-box 検査と同じ発想の再発防止）。
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for ax, title_text in zip((ax_a, ax_b, ax_c), title_texts):
        col_width_px = ax.get_window_extent(renderer=renderer).width
        title_width_px = title_text.get_window_extent(renderer=renderer).width
        assert title_width_px <= col_width_px * 1.05, (
            f"P7: キャプション '{title_text.get_text()!r}' の表示幅 {title_width_px:.1f}px が "
            f"自列幅 {col_width_px:.1f}px の105%を超えている（隣列と衝突する可能性）"
        )

    out = OUT_DIR / "p07_three_scales.png"
    plt.savefig(out, dpi=SAVE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    width_px = report_size(out)
    audit_slide_font_sizes("P7", width_px, font_elements)


# ---------------------------------------------------------------- P12: 3ステップフロー図
def make_p12_loop_diagram() -> None:
    # キャプションは24pt(P12の床は19pt native)。24pt・1行のままでは各キャプションの幅が
    # 自ボックス幅を大きく超え、隣接キャプションと衝突して1行に見えてしまう回帰が
    # fix round 1で発生したため、フォントは縮めず、各キャプションを2行に折り返して
    # 自ボックスの幅に収める（Finding 2: フォントを縮めるのではなく表示方法を変える方針）。
    steps = [
        ("Satellite scan", ("a finite", "candidate list")),
        ("Field visit", ("see it with", "your own eyes")),
        ("OpenStreetMap", ("publish what", "you confirmed")),
    ]

    title_fontsize = 24.0
    caption_fontsize = 24.0

    box_w, box_h = 3.6, 1.5
    gap = 1.4  # キャプションの折り返しに加え、ボックス間隔にも余裕を持たせる
    n = len(steps)
    total_w = n * box_w + (n - 1) * gap
    fig, ax = plt.subplots(figsize=(12.5, 4.6), dpi=SAVE_DPI)
    ax.set_xlim(0, total_w)
    ax.set_ylim(0.1, 2.9)  # 2行キャプション分の縦の余白を確保
    ax.axis("off")

    font_elements: list[tuple[str, float]] = []
    centers = []
    box_spans_data: list[tuple[float, float]] = []
    caption_texts = []
    for i, (title, caption_lines) in enumerate(steps):
        x0 = i * (box_w + gap)
        y0 = 1.3
        rect = Rectangle(
            (x0, y0), box_w, box_h,
            facecolor="white", edgecolor=COL_TEXT, linewidth=1.6,
            joinstyle="miter", zorder=5,
        )
        ax.add_patch(rect)
        cx, cy = x0 + box_w / 2, y0 + box_h / 2
        centers.append((x0, x0 + box_w, cy))
        box_spans_data.append((x0, x0 + box_w))
        ax.text(
            cx, cy, title, ha="center", va="center",
            fontsize=title_fontsize, weight="bold", color=COL_TEXT, zorder=6,
        )
        font_elements.append((f"box title ({title})", title_fontsize))
        caption_text = ax.text(
            cx, y0 - 0.15, "\n".join(caption_lines), ha="center", va="top",
            fontsize=caption_fontsize, color=COL_TEXT, style="italic",
            linespacing=1.3, zorder=6,
        )
        caption_texts.append(caption_text)
        font_elements.append((f"caption ({title})", caption_fontsize))

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

    # キャプションが自ボックスの幅を大きく超えて隣接キャプションと衝突しないことを検査する
    # （fix round 1で24pt化した際に発生した回帰の再発防止）。
    # レンダラで実測した各キャプションの表示幅が、自ボックス幅の110%以内であることを確認する。
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    caption_bboxes = [t.get_window_extent(renderer=renderer) for t in caption_texts]
    caption_margin_frac = 0.10
    for i, (bbox, (bx0, bx1)) in enumerate(zip(caption_bboxes, box_spans_data)):
        box_disp0 = ax.transData.transform((bx0, 0.0))[0]
        box_disp1 = ax.transData.transform((bx1, 0.0))[0]
        box_width_px = box_disp1 - box_disp0
        max_allowed_px = box_width_px * (1.0 + caption_margin_frac)
        assert bbox.width <= max_allowed_px, (
            f"P12: caption {i} の表示幅 {bbox.width:.1f}px が自ボックス幅 "
            f"{box_width_px:.1f}px の110%（{max_allowed_px:.1f}px）を超えている"
        )
    min_caption_gap_px = min(
        caption_bboxes[i + 1].x0 - caption_bboxes[i].x1 for i in range(len(caption_bboxes) - 1)
    )
    print(f"[P12] caption-to-caption gap (min): {min_caption_gap_px:.1f}px")
    assert min_caption_gap_px >= 60.0, (
        f"P12: キャプション同士の間隔が {min_caption_gap_px:.1f}px しかなく、"
        "1本の文章に見えてしまう可能性がある（下限60px）"
    )

    plt.tight_layout()
    out = OUT_DIR / "p12_loop_diagram.png"
    plt.savefig(out, dpi=SAVE_DPI, bbox_inches="tight", facecolor="white")
    plt.close()
    width_px = report_size(out)
    audit_slide_font_sizes("P12", width_px, font_elements)


# ---------------------------------------------------------------- main
def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    features = load_polygons()
    print(f"loaded {len(features)} polygons from {GEOJSON_PATH.relative_to(PROJECT_ROOT)}")

    make_p06_clusters_map(features)
    make_p07_three_scales(features)
    make_p08_visit_anchors_map(features)
    make_p12_loop_diagram()
    print("\nAll presentation figures generated.")


if __name__ == "__main__":
    main()
