#!/usr/bin/env python3
"""FOSS4G 2026 北木島 口頭発表用の新規図版（P5・P6・P7・P8・P12）を生成する。

公開済みの追跡データ（`docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson`）
と、既にリポジトリへ取り込まれている画像（背景地図ラスタを含む）のみを入力とし、
`tmp/`（Git管理外のキャッシュ）やネットワークアクセスには依存しない。

背景地図（CARTO Positron のラベルなしタイル）だけは一度ネットワークから取得する必要があるが、その取得は
`--fetch-basemap` という専用の入口に分離してあり、図版生成の通常経路（引数なしの実行）は
追跡済みラスタ `images/basemap_kitagi_carto_positron.png` を読むだけである。
取得系のモジュール（`mercantile` / `urllib`）も `fetch_basemap()` の内側でのみ import する。
ラスタが存在しない場合は `load_basemap()` が明示的に失敗し、取得手順の再実行を促す
（背景地図なしの図版を黙って出力しない）。
配色は `scripts/generate_exp002_poster_figures.py` のポスター配色定数
（COL_TEXT / COL_WATER / COL_STONE）を流用し、ポスターと発表資料の
見た目を揃える。ただし背景の陸域シルエットは衛星バンドから再導出せず、
中性色の背景＋スケールバーのみとする（Task 1 の判断: tmp/ 依存の回避）。

出力先: docs/presentations/images/
    p05_index_panels.png         — 指数4パネル（ポスター F4 のパネル画像を切り出し、
                                    英語ラベルとカラーバーを大きく再描画したもの）
    p06_clusters_map.png         — 検出145ポリゴン + 4地区（英語ラベル、報告書§4.3準拠。
                                    減光したラベルなし背景地図つき）
    p07_three_scales.png         — 三スケール合成図（英語ラベルのみ。Task 4 レビュー
                                    指摘の修正: 日本語記事と共有される
                                    `fig09_multiscale.png` の英語投影面への流用を解消）
    p08_visit_anchors_map.png    — 同じ地図 + 座標確認済み訪問4地点（凡例つき、背景地図つき）
    p12_loop_diagram.png         — 「衛星 → 現地 → 地図」の3ステップフロー図

実行方法:
    # 背景地図の取得（一度だけ。ネットワークを使う唯一の経路）
    uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py --fetch-basemap
    # 図版生成（ネットワーク非依存）
    uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py

再実行時にバイト一致するよう、実行日時・乱数・辞書順序等は一切使用しない。

フォントサイズの検査:
    本スクリプトは図版内に焼き込んだ文字の native フォントサイズを
    `NATIVE_FONT_SIZES`（キー = images/ 内のファイル名）として**宣言**し、
    各図版の生成関数が「実際に使ったサイズが宣言と一致すること」を
    `declare_font_sizes()` で自己検査する（宣言の陳腐化を防ぐ）。

    「スライド上で何ptに見えるか」という実効サイズの下限（15pt）は本スクリプトでは
    判定しない。実効サイズは配置幅に依存し、配置幅を決めるのは
    `exp002_kitagi_foss4g2026_presentation.py` のレイアウトであって本スクリプトでは
    ないためである（以前ここにあった `audit_slide_font_sizes` は「配置幅220mm」という
    デッキが実際には使っていない値を測っていた）。実効サイズの検査は
    `validate_exp002_kitagi_foss4g2026_presentation.py` の
    `check_placed_font_sizes()` が、生成済みPPTXの `shape.width` と画像実寸
    （px ÷ dpi）から配置倍率を復元して行う。
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pyproj
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
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
COL_STONE = "#b0a999"

# 中性色の背景（陸域シルエットは描かず、COL_STONE を薄めた中性トーンのみ使用）
COL_BG_NEUTRAL = "#f4f2ee"
COL_WATER_EDGE = "#062a52"

# 地図の描画範囲。**P6・P7パネル(c)・P8 の3図版すべてがこの1つの範囲を使う**ので、
# 聴衆は3枚のスライドで同じ島の輪郭を見る（DESIGN_GUIDE §4.3「並置する図版は表示寸法・
# 表現を揃える」）。
#
# 導出: 北木島の陸域の実測バウンディングボックスに、およそ 230〜260 m の余白を付けた。
# 陸域の bbox は CARTO Positron の z14 タイル（陸 = 輝度 241、海 = 輝度 216）を
# 二値化し、島内の点 (133.5369, 34.3900) を含む連結成分の範囲として実測した:
#     133.51616 〜 133.56019 °E, 34.36661 〜 34.40224 °N
# 以前の範囲 [133.514, 34.367, 133.562, 34.402] は、この実測 bbox と 20〜40 m しか
# 違わない**余白ゼロ**の枠だった。そのため島の海岸線が四辺すべてで枠に接し、
# 図版ごとに島が切れて別の形に見えるという指摘を受けた（余白を付けて解消した）。
# 解析側の `KITAGI_BBOX = [133.515, 34.350, 133.570, 34.400]` は採らない。
# 南に約 1.8 km の空虚な海が入り、かつ北端（34.40224）を依然として切り落とすためである。
MAP_BBOX = [133.5135, 34.3645, 133.5630, 34.4045]  # [west, south, east, north]
MAP_CENTER_LAT = 34.3845  # 描画範囲の中央緯度（スケールバーのメルカトル補正に使う）
# 実測した陸域 bbox（上記の導出。`assert_map_bbox_frames_island()` が余白を機械検査する）
ISLAND_BBOX_MEASURED = [133.51616, 34.36661, 133.56019, 34.40224]
# 陸域 bbox の各辺に確保する最小余白（度）。経度 0.002° ≒ 184 m、緯度 0.0018° ≒ 200 m。
ISLAND_MARGIN_MIN_DEG = 0.0018

# ---------------------------------------------------------------- 背景地図（CARTO Positron）
# 検出ポリゴンが「島のどこにあるのか」が分かるよう、検出地図（P6・P8・P7 パネル(c)）の
# 下に文字を含まない淡色の**地図**を敷く。
#
# タイルの選定（検討した候補と却下理由）:
#   (1) 地理院タイル英語版（`xyz/english/`）は **ズーム 5〜11 しか存在しない**
#       （z12 以上は 404。実測で確認）。z11 の地上分解能は約 76 m/px で、地図範囲
#       (MAP_BBOX) の幅 5,510 m はわずか 72 px にしかならない。出力図版の地図軸は
#       約 1,850 px 幅であり、「出力1pxあたり2px以上」（＝3,700 px 以上）に対して
#       1/50 以下で、拡大すれば著しくぼやける。使えない。
#   (2) 地理院タイルの淡色地図・標準地図（z18まで）・白地図（z14まで）は
#       **日本語地名が焼き込まれている**。投影面は英語のみという制約に反するため使わない。
#   (3) 陰影起伏図（z16まで）・色別標高図（z15まで）は文字を含まないが解像度が足りない。
#   (4) 全国最新写真（`seamlessphoto`）は文字が無く z18 まであるが、**航空写真は使わない**。
#       理由は2つある。第一に、S7 は「歩いて／上空から／衛星から」の三スケール合成図で、
#       パネル(c)（衛星・分布）の下に航空写真を敷くとパネル(b)（上空）と見分けが付かなくなり、
#       このスライドの主旨が壊れる。第二に、実際の丁場池が写った航空写真の上に検出結果を
#       載せると「目視で検証済み」と読まれてしまう。本発表の主張境界は「検出は候補であり、
#       ground truth も精度指標も持たない」ことなので、これは許容できない
#       （「池が見えるなら指数は要らないのでは」という誤解も招く）。
#   (5) **採用: CARTO Positron（`light_nolabels`、z20まで）**。ラベルを一切含まないため
#       投影面が英語のみという要件を満たし、z17 で 4,614 px（出力1pxあたり2.5px）と
#       解像度も満たす。海岸線と道路が読めるので発表者の依頼（島のどこにあるか）に直接応え、
#       ベクタ由来のフラットなラスタなので実写と違い PNG が十分に圧縮される。
#       出典表示は `© OpenStreetMap contributors, © CARTO`（下記 BASEMAP_CREDIT）。
BASEMAP_PATH = OUT_DIR / "basemap_kitagi_carto_positron.png"
# `{s}`（サブドメイン）・`{r}`（Retina）のプレースホルダは使わない。取得コードは
# z/x/y だけを差し込むため、サブドメインは固定し、Retina 版（@2x）も使わない
# （contextily の `cx.providers.CartoDB.PositronNoLabels` と同じタイル。
#  URL テンプレートは `https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png`）。
BASEMAP_TILE_URL = "https://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"
BASEMAP_ZOOM = 17
# 背景地図の範囲は地図軸の範囲（MAP_BBOX）と厳密に一致させる。タイルモザイクを
# 合成したあと、この範囲に対応する画素窓へ切り出して保存するため、描画時の
# `imshow(extent=...)` は軸の範囲そのものになり、位置合わせの誤差が生じない。
BASEMAP_BBOX = MAP_BBOX  # [west, south, east, north] = 取得・保存した範囲
BASEMAP_RETRIEVED = "2026-08-24"  # 取得日（この日に一度だけ取得し、リポジトリに追跡）
# 保存された背景地図の画素数。取得スクリプトが書き出した値であり、読み込み時に
# 検査することで「別の範囲・別のズームのラスタが置かれた」事故を検出する。
BASEMAP_EXPECTED_PX = (4614, 4518)
# 背景地図の減光率（DESIGN_GUIDE §7.3「背景地図を薄くし、主題データとの視覚的競合を
# 避ける」）。出力 = 255 - (255 - 入力) × KEEP。
# Positron は元から淡い（実測: 海 ≈ 輝度 219、陸 ≈ 250、道路・海岸線 ≈ 200 前後）ため、
# 写真基図に使っていた KEEP=0.30 をそのまま当てると海岸線と道路が消えてしまう
# （海陸差が約 31 階調 → 約 9 階調）。主題データ（COL_WATER のグレースケール輝度 64）
# との分離は素のままでも 130 階調以上あるので、減光は「わずかに掛ける」だけで足りる。
BASEMAP_LIGHTEN_KEEP = 0.80
# 背景地図の帰属表示。CARTO Positron は OpenStreetMap データを CARTO がレンダリングした
# タイルなので、両者を表示する（contextily のプロバイダ定義の attribution と同一内容）。
BASEMAP_CREDIT = "Basemap: © OpenStreetMap contributors, © CARTO"
# 帰属表示の native フォントサイズ。デッキのフッター階層（実効 11〜12pt）に合わせる。
#   P6: 実寸 8.21 in、S6 の配置倍率 0.516 → 22pt × 0.516 = 11.4pt
#   P8: 実寸 8.26 in、S8 の配置倍率 0.504 → 22pt × 0.504 = 11.1pt
#   P7: 実寸 8.97 in、S7 の配置倍率 0.977 → 11.5pt × 0.977 = 11.2pt
# 帰属表示は本文でも図中の主題ラベルでもないため、15pt 下限（`NATIVE_FONT_SIZES` の
# 検査対象）には含めない。この扱いは内容契約の「実装時のハードゲート」に明記してある
# （S11 フッターが基図の帰属表示を 11pt で置いている前例に合わせる）。
BASEMAP_CREDIT_PT_MAP = 22.0
P07_BASEMAP_CREDIT_PT = 11.5

# 訪問4地点（Task 0 の踏査地点と同一の座標。scripts/build_chiri_koryu_figures.py の
# waypoints と一致させること。Task 1 の preflight ruling により verbatim で固定）
VISIT_ANCHORS = [
    ("Toyoura Port", 133.5369, 34.3956),
    ("Toyoura hall", 133.5364, 34.3943),
    ("Lake stage (Keirin)", 133.5329, 34.3912),
    ("Sen-no-hama", 133.5309, 34.3930),
]
# 訪問4地点の通し番号（北→南の緯度順）。地図面には番号だけを置き、地名は地図の下の
# 対応表（key）に出す。理由: 4地点は互いに 145〜470 m しか離れていないのに対し、
# 32pt のラベル箱は地図の縮尺で 1.2〜2.3 km に相当する。地名を地点の近くに置くことは
# 幾何学的に不可能で、以前は島の東側の海域に4枚を縦積みしてリーダー線を地図の上に
# 長く走らせていた（発表者からの指摘）。番号なら箱が小さく、各地点のすぐ隣に短い
# リーダー線で置ける。
VISIT_ANCHOR_NUMBERS = {
    "Toyoura Port": "1",
    "Toyoura hall": "2",
    "Sen-no-hama": "3",
    "Lake stage (Keirin)": "4",
}
# 地図の下に置く対応表の並び（行 → 列）。番号順に左上→右上→左下→右下と読む。
VISIT_KEY_ROWS = [
    ("1  Toyoura Port", "2  Toyoura hall"),
    ("3  Sen-no-hama", "4  Lake stage (Keirin)"),
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

SAVE_DPI = 200
SLIDE_PT_FLOOR = 15.0  # DESIGN_GUIDE の16:9スライド本文フォント床（検査は validator 側）

# 図版に焼き込まれた文字の native フォントサイズ（pt）。キーは `images/` 内のファイル名、
# 値は「要素グループ名 → pt」。
#
# この宣言は validator（`validate_exp002_kitagi_foss4g2026_presentation.py` の
# `check_placed_font_sizes()`）が読み、生成済みPPTX内の各PICTUREの `shape.width` と
# 画像実寸（px ÷ dpi）から復元した配置倍率を掛けて「スライド上の実効pt」を求め、
# 15pt下限を検査する。validator 側に数表を複製せず、ここを唯一の正本にする。
#
# 自前生成の図版（p05〜p12）は、各生成関数が `declare_font_sizes()` で
# 「実際に使ったサイズ = 宣言」を自己検査するため、宣言が実装から乖離できない。
# ポスター流用図版（poster_f1_study_area.png）は本スクリプトが生成しないため、
# 生成元スクリプトの該当行を出典として明記した手書きの宣言である。
NATIVE_FONT_SIZES: dict[str, dict[str, float]] = {
    "p05_index_panels.png": {
        "panel title": 18.0,
        "colorbar tick label": 18.0,
    },
    "p06_clusters_map.png": {
        "zone label": 32.0,
        "title": 32.0,
        "scale bar label": 32.0,
    },
    "p07_three_scales.png": {
        "panel caption": 21.0,
        "scale bar label": 21.0,
    },
    "p08_visit_anchors_map.png": {
        "visit number": 32.0,
        "anchor key": 32.0,
        "title": 32.0,
        "scale bar label": 32.0,
        "legend": 32.0,
    },
    "p12_loop_diagram.png": {
        "box title": 27.0,
        "caption": 27.0,
    },
    # 出典: `scripts/generate_exp002_poster_figures.py` の `make_f1_study_area()`。
    #   ax1/ax2 の set_title = 16pt（L417・L443）、"Kitagi Island" 注記 = 16pt（L408）、
    #   パネル(b)の島名ラベル = 16pt（Kitagi）/ 15pt（その他）（L436）。
    # この図版は GSI タイルをネットワーク取得して描くため再生成しない（配置倍率で
    # 実効ptを満たす。`exp002_kitagi_foss4g2026_presentation.py` の `s02()` を参照）。
    "poster_f1_study_area.png": {
        "panel title": 16.0,
        "Kitagi Island label": 16.0,
        "other island label": 15.0,
    },
}

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


def assert_labels_inside_and_disjoint(
    fig, ax, annotations: list, figure_label: str, *, gap_px: float = 6.0
) -> None:
    """地図注記が (1) 軸の内側に収まり (2) 互いに重ならないことを実測で検査する。

    図版内の文字を投影時 15pt 相当まで拡大すると注記の箱が大きくなり、
    地図外への逸脱・注記同士の衝突が起きやすくなる（Final review の Critical 指摘を
    受けた 20pt → 32pt の引き上げで実際に起きた）。オフセットの手調整が将来の編集で
    崩れても検出できるよう、レンダラで実測した箱で機械検査する。
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax_bb = ax.get_window_extent(renderer=renderer)

    boxes: list[tuple[str, object]] = []
    for ann in annotations:
        patch = ann.get_bbox_patch()
        bb = (
            patch.get_window_extent(renderer=renderer)
            if patch is not None
            else ann.get_window_extent(renderer=renderer)
        )
        boxes.append((ann.get_text().replace("\n", " "), bb))

    for text, bb in boxes:
        assert (
            bb.x0 >= ax_bb.x0 - 1 and bb.x1 <= ax_bb.x1 + 1
            and bb.y0 >= ax_bb.y0 - 1 and bb.y1 <= ax_bb.y1 + 1
        ), (
            f"{figure_label}: 注記 '{text}' の箱 "
            f"({bb.x0:.0f},{bb.y0:.0f})-({bb.x1:.0f},{bb.y1:.0f}) が軸の範囲 "
            f"({ax_bb.x0:.0f},{ax_bb.y0:.0f})-({ax_bb.x1:.0f},{ax_bb.y1:.0f}) を出ている"
        )

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            (t1, b1), (t2, b2) = boxes[i], boxes[j]
            overlap_x = min(b1.x1, b2.x1) - max(b1.x0, b2.x0)
            overlap_y = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
            assert not (overlap_x > -gap_px and overlap_y > -gap_px), (
                f"{figure_label}: 注記 '{t1}' と '{t2}' が重なっている"
                f"（余白 x={-overlap_x:.1f}px, y={-overlap_y:.1f}px、"
                f"下限 {gap_px:g}px）"
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


def _bbox_3857(bbox=MAP_BBOX) -> tuple[float, float, float, float]:
    """[west, south, east, north] を Web Mercator の (xmin, xmax, ymin, ymax) に変換する。"""
    west, south, east, north = bbox
    xmin, ymin = _to_3857(west, south)
    xmax, ymax = _to_3857(east, north)
    return xmin, xmax, ymin, ymax


def map_axes_ar() -> float:
    """共有する地図描画範囲（MAP_BBOX）の縦横比。P7 の3パネル共通比と P8 の軸寸法に使う。"""
    xmin, xmax, ymin, ymax = _bbox_3857(MAP_BBOX)
    return (xmax - xmin) / (ymax - ymin)


def fetch_basemap() -> None:
    """CARTO Positron タイルを**一度だけ**取得して `BASEMAP_PATH` に保存する（ネットワーク使用）。

    通常の図版生成（`main()`）はこの関数を呼ばない。図版生成をネットワークから完全に
    独立させるため、取得は `--fetch-basemap` という専用の入口に分離してある。
    タイル取得に使うモジュール（`mercantile` / `urllib`）もこの関数の内側でだけ
    import し、モジュール先頭には取得系の import を置かない。

    CARTO Positron は全球を覆うので欠測タイルは存在しない。404 が返るのは URL や
    ズームの指定を誤った場合であり、その場合は**黙って埋めずに失敗させる**
    （欠測を海として塗り潰していた写真基図向けの処理は廃止した）。
    合成後、`BASEMAP_BBOX` に対応する画素窓へ切り出して保存するので、
    保存されたラスタの地理的範囲は地図軸の範囲と厳密に一致する。
    """
    import io  # noqa: PLC0415 — 取得専用の入口だけで使う
    import urllib.error  # noqa: PLC0415
    import urllib.request  # noqa: PLC0415

    import mercantile  # noqa: PLC0415

    west, south, east, north = BASEMAP_BBOX
    tiles = list(mercantile.tiles(west, south, east, north, BASEMAP_ZOOM))
    xs = sorted({t.x for t in tiles})
    ys = sorted({t.y for t in tiles})
    print(
        f"fetching {len(tiles)} tiles (z{BASEMAP_ZOOM}, "
        f"x {xs[0]}–{xs[-1]}, y {ys[0]}–{ys[-1]}) from {BASEMAP_TILE_URL}"
    )
    mosaic = Image.new("RGB", (256 * len(xs), 256 * len(ys)), (255, 255, 255))
    for tile in tiles:
        url = BASEMAP_TILE_URL.format(z=tile.z, x=tile.x, y=tile.y)
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                payload = response.read()
        except urllib.error.HTTPError as exc:
            # Positron は全球を覆うため 404 は「URL・ズームの指定ミス」を意味する。
            # 欠測として埋めず、ここで失敗させる。
            raise RuntimeError(f"タイル取得に失敗しました（{exc.code}）: {url}") from exc
        with Image.open(io.BytesIO(payload)) as tile_img:
            mosaic.paste(
                tile_img.convert("RGB"),
                (256 * (tile.x - xs[0]), 256 * (tile.y - ys[0])),
            )
    print(f"  fetched {len(tiles)} tiles (no missing tiles expected: global coverage)")

    # モザイク全体の 3857 範囲（タイル境界にスナップした値）から、BASEMAP_BBOX に
    # 対応する画素窓を切り出す。
    upper_left = mercantile.xy_bounds(mercantile.Tile(xs[0], ys[0], BASEMAP_ZOOM))
    lower_right = mercantile.xy_bounds(mercantile.Tile(xs[-1], ys[-1], BASEMAP_ZOOM))
    mx0, my1 = upper_left.left, upper_left.top
    mx1, my0 = lower_right.right, lower_right.bottom
    px_per_m_x = mosaic.size[0] / (mx1 - mx0)
    px_per_m_y = mosaic.size[1] / (my1 - my0)
    xmin, xmax, ymin, ymax = _bbox_3857(BASEMAP_BBOX)
    left = round((xmin - mx0) * px_per_m_x)
    right = round((xmax - mx0) * px_per_m_x)
    top = round((my1 - ymax) * px_per_m_y)
    bottom = round((my1 - ymin) * px_per_m_y)
    cropped = mosaic.crop((left, top, right, bottom))

    assert cropped.size == BASEMAP_EXPECTED_PX, (
        f"切り出した背景地図の画素数 {cropped.size} が BASEMAP_EXPECTED_PX "
        f"{BASEMAP_EXPECTED_PX} と一致しない（定数を更新すること）"
    )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cropped.save(BASEMAP_PATH, format="PNG", optimize=True)
    print(
        f"saved: {BASEMAP_PATH.relative_to(PROJECT_ROOT)} "
        f"({cropped.size[0]} x {cropped.size[1]} px, "
        f"{BASEMAP_PATH.stat().st_size / 1e6:.1f} MB)\n"
        f"  extent (west, south, east, north) = {BASEMAP_BBOX}\n"
        f"  zoom = {BASEMAP_ZOOM}, tile url = {BASEMAP_TILE_URL}, "
        f"retrieved = {BASEMAP_RETRIEVED}"
    )


_BASEMAP_CACHE: dict[str, np.ndarray] = {}


def load_basemap() -> np.ndarray:
    """追跡済みの背景地図ラスタを読み、減光した uint8 配列を返す（ネットワーク非使用）。

    ファイルが無い場合は**明示的に失敗させる**。背景地図を黙って省いた図版を
    出力すると、検出ポリゴンの位置が分からない元の状態へ静かに戻ってしまう。
    """
    if "img" in _BASEMAP_CACHE:
        return _BASEMAP_CACHE["img"]
    if not BASEMAP_PATH.is_file():
        raise FileNotFoundError(
            f"背景地図が見つかりません: {BASEMAP_PATH}\n"
            "  この図版は追跡済みの背景地図ラスタを読み込みます（生成時にネットワークへは"
            "アクセスしません）。\n"
            "  取得手順を再実行してください:\n"
            "    uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py "
            "--fetch-basemap"
        )
    with Image.open(BASEMAP_PATH) as img:
        assert img.size == BASEMAP_EXPECTED_PX, (
            f"{BASEMAP_PATH.name}: 画素数 {img.size} が BASEMAP_EXPECTED_PX "
            f"{BASEMAP_EXPECTED_PX} と一致しない（取得範囲・ズームが異なるラスタの可能性）"
        )
        arr = np.asarray(img.convert("RGB"), dtype=np.uint16)
    # 減光: 出力 = 255 - (255 - 入力) × KEEP。整数演算のみで丸めるため、実行ごとに
    # 完全に同じ値になる（バイト一致の要件）。
    keep_num = round(BASEMAP_LIGHTEN_KEEP * 100)
    lightened = (255 - ((255 - arr) * keep_num + 50) // 100).astype(np.uint8)
    _BASEMAP_CACHE["img"] = lightened
    return lightened


def draw_basemap(ax, bbox=MAP_BBOX) -> None:
    """地図軸の最下層に減光した背景地図を敷く（主題データは zorder 5 以上で上に載る）。"""
    xmin, xmax, ymin, ymax = _bbox_3857(bbox)
    ax.imshow(
        load_basemap(),
        extent=(xmin, xmax, ymin, ymax),
        interpolation="antialiased",
        zorder=0,
    )


def add_basemap_credit(ax, fontsize: float, *, text: str = BASEMAP_CREDIT):
    """背景地図の帰属表示を地図軸の**下端の外側**に1行のキャプションとして置き、その Text を返す。

    以前は軸の内側・左上（地図範囲の北西隅）に白枠付きの2行の箱として焼き込んでいたが、
    32pt 級の図版内では箱が大きく、島の北西部を覆って地図の内容を隠していた
    （発表者からの指摘）。地図の下に置く一般的な出典表記に改め、地図面には一切
    重ねない。文言（`BASEMAP_CREDIT`）は変更していない。1行に戻せるのは、軸幅
    いっぱいを使えるようになり折り返しが不要になったためである。

    軸の外側に置いても図中文字の実効ptは目減りしない。図版の実寸高さは figsize の
    高さで決まっており（`bbox_inches="tight"` は figsize より小さく刈り込むだけ）、
    `tight_layout()` が帰属表示ぶんだけ地図軸を縮めて吸収するからである
    （実効ptは validator が生成済みPPTXの `shape.width` から実測検査する）。
    フォントサイズはデッキのフッター階層（実効 11〜12pt）に合わせる。内容契約の
    「実装時のハードゲート」に、帰属表示行はフッター階層に従うことを明記してある。
    """
    return ax.text(
        0.0, -0.012, text,
        transform=ax.transAxes, ha="left", va="top",
        fontsize=fontsize, color=COL_TEXT, zorder=30,
    )


def assert_credit_outside_map(fig, ax, credit, others: list, figure_label: str) -> None:
    """帰属表示が (1) 地図軸の下側の外にあり (2) 他の注記と重ならないことを実測で検査する。

    `assert_labels_inside_and_disjoint()` の逆向きの検査である。帰属表示を軸の内側から
    外へ移した意図（地図面を覆わない）が、将来の編集で静かに戻らないようにする。
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax_bb = ax.get_window_extent(renderer=renderer)
    bb = credit.get_window_extent(renderer=renderer)
    assert bb.y1 <= ax_bb.y0 + 1, (
        f"{figure_label}: 帰属表示の箱 y1={bb.y1:.0f} が地図軸の下端 "
        f"y0={ax_bb.y0:.0f} より上にある（地図面に重なっている）"
    )
    assert bb.x0 >= ax_bb.x0 - 1, (
        f"{figure_label}: 帰属表示の左端 x0={bb.x0:.0f} が地図軸の左端 "
        f"x0={ax_bb.x0:.0f} より外に出ている"
    )
    for other in others:
        ob = other.get_window_extent(renderer=renderer)
        overlap_x = min(bb.x1, ob.x1) - max(bb.x0, ob.x0)
        overlap_y = min(bb.y1, ob.y1) - max(bb.y0, ob.y0)
        assert not (overlap_x > 0 and overlap_y > 0), (
            f"{figure_label}: 帰属表示が他の注記と重なっている"
            f"（重なり x={overlap_x:.1f}px, y={overlap_y:.1f}px）"
        )


def assert_labels_clear_of_polygons(
    fig, ax, annotations: list, features: list[dict], figure_label: str
) -> None:
    """注記の箱が検出ポリゴンを覆っていないことを実測で検査する。

    注記が主題データ（検出した水域）を隠してしまうと、図版が示すはずのものが見えなくなる。
    ポリゴンは外接矩形（display座標）で近似する（矩形は実形状を含むので、この検査は
    安全側に働く）。
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    poly_boxes = []
    for feature in features:
        poly = shapely_transform(_to_3857, shapely_shape(feature["geometry"]))
        x0, y0, x1, y1 = poly.bounds
        (dx0, dy0), (dx1, dy1) = ax.transData.transform([(x0, y0), (x1, y1)])
        poly_boxes.append((dx0, dy0, dx1, dy1))
    for ann in annotations:
        patch = ann.get_bbox_patch()
        bb = (
            patch.get_window_extent(renderer=renderer)
            if patch is not None
            else ann.get_window_extent(renderer=renderer)
        )
        for dx0, dy0, dx1, dy1 in poly_boxes:
            overlap_x = min(bb.x1, dx1) - max(bb.x0, dx0)
            overlap_y = min(bb.y1, dy1) - max(bb.y0, dy0)
            assert not (overlap_x > 0 and overlap_y > 0), (
                f"{figure_label}: 注記 '{ann.get_text()}' の箱が検出ポリゴンを覆っている"
                f"（重なり x={overlap_x:.1f}px, y={overlap_y:.1f}px）"
            )


def assert_key_below_map(fig, ax, key_texts: list, others: list, figure_label: str) -> None:
    """番号と地名の対応表が (1) 地図軸の下側の外にあり (2) 互いにも他の注記にも
    重ならないことを実測で検査する。

    対応表は地図面を覆ってはならず（番号を地図に置いた理由が失われる）、行間・列間が
    足りずに1文に見えてもいけない。列位置はレンダラ計測から決めているが、
    フォントの差異でその計算が崩れても検出できるよう機械検査する。
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax_bb = ax.get_window_extent(renderer=renderer)
    boxes = [(t.get_text(), t.get_window_extent(renderer=renderer)) for t in key_texts]
    for text, bb in boxes:
        assert bb.y1 <= ax_bb.y0 + 1, (
            f"{figure_label}: 対応表 '{text}' の箱 y1={bb.y1:.0f} が地図軸の下端 "
            f"y0={ax_bb.y0:.0f} より上にある（地図面に重なっている）"
        )
    other_boxes = [
        (
            getattr(o, "get_text", lambda: "legend")(),
            o.get_window_extent(renderer=renderer),
        )
        for o in others
    ]
    for i, (t1, b1) in enumerate(boxes):
        for t2, b2 in boxes[i + 1:] + other_boxes:
            overlap_x = min(b1.x1, b2.x1) - max(b1.x0, b2.x0)
            overlap_y = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
            assert not (overlap_x > -8.0 and overlap_y > -4.0), (
                f"{figure_label}: 対応表 '{t1}' と '{t2}' の間隔が足りない"
                f"（余白 x={-overlap_x:.1f}px, y={-overlap_y:.1f}px）"
            )


def assert_map_bbox_frames_island() -> None:
    """地図の描画範囲が、実測した陸域 bbox を最小余白つきで完全に含むことを検査する。

    3図版が共有する `MAP_BBOX` を将来縮めてしまうと、島の海岸線が枠に接して
    「図版ごとに島の形が違う」という指摘が再発する。実測値との差を機械検査する。
    """
    west, south, east, north = MAP_BBOX
    i_west, i_south, i_east, i_north = ISLAND_BBOX_MEASURED
    for name, margin in (
        ("west", i_west - west), ("south", i_south - south),
        ("east", east - i_east), ("north", north - i_north),
    ):
        assert margin >= ISLAND_MARGIN_MIN_DEG, (
            f"MAP_BBOX の{name}側の余白が {margin:.5f}° しかない"
            f"（下限 {ISLAND_MARGIN_MIN_DEG:.4f}°）。島の海岸線が枠に接してしまう"
        )


def report_size(path: Path) -> int:
    with Image.open(path) as img:
        w, h = img.size
    print(f"saved: {path.relative_to(PROJECT_ROOT)} ({w} x {h} px)")
    return w


def declare_font_sizes(figure_file: str, used: dict[str, float], dpi: int) -> None:
    """図版が実際に使った native フォントサイズが `NATIVE_FONT_SIZES` の宣言と
    一致することを検査し、native 実寸（px ÷ dpi）を表示する。

    ここでは「スライド上の実効pt」を判定しない（配置幅はこのスクリプトの管轄外）。
    実効ptの15pt下限は validator が生成済みPPTXから配置倍率を復元して検査する。
    本関数の役割は、validator が読む宣言が実装から乖離しないよう固定することである。
    """
    declared = NATIVE_FONT_SIZES.get(figure_file)
    assert declared is not None, f"{figure_file}: NATIVE_FONT_SIZES に宣言が無い"
    assert used == declared, (
        f"{figure_file}: 実際に使った native フォントサイズ {used} が "
        f"宣言 {declared} と一致しない（NATIVE_FONT_SIZES を更新すること）"
    )
    path = OUT_DIR / figure_file
    with Image.open(path) as img:
        px_w, px_h = img.size
    print(
        f"  native size = {px_w / dpi:.2f} x {px_h / dpi:.2f} in "
        f"({px_w} x {px_h} px @ {dpi} dpi), native fonts = "
        + ", ".join(f"{k} {v:g}pt" for k, v in sorted(declared.items()))
    )


# ---------------------------------------------------------------- P5: 指数4パネル図
# ポスター図版 `poster_f4_index_panels.png` は native 18pt・実寸 8.82 x 8.50 in で、
# S5 の配置（帯高 4.8in）では実効 10.2pt しか出ない。実効ptは「文字の物理サイズ ÷
# 配置寸法」で決まり、18pt が 15pt に見えるには配置高さ 7.09in が必要で、
# タイトル帯を含む16:9スライドには収まらない（スライド全高 7.5in）。
# つまり**配置拡大では下限を満たせない**（統制者の裁定
# 「配置拡大で要件を満たせるなら再生成は不要」の前提が成立しない）。
#
# 一方、この図版の元データ（Sentinel-2 バンド）はリポジトリに無く、
# `scripts/generate_exp002_poster_figures.py` の `make_f4_index_panels(res)` は
# ネットワーク取得したラスタを必要とするため、そのままの再生成もできない。
#
# そこで、既にリポジトリへ取り込まれている PNG から**パネルのラスタ部分のみを切り出し**、
# 英語ラベルとカラーバーを matplotlib で大きく描き直す。ラスタは一切加工しない
# （切り出しと表示時の縮小のみ）ので、描かれているデータはポスターと同一である。
# ネットワーク・tmp/ への依存はない。同種の手法は `make_p07_three_scales()`
# （fig06 のクロップ＋英語ラベル再描画）で既に採用している。
F4_SOURCE_NAME = "poster_f4_index_panels.png"
# 切り出し座標が別のファイルに対して使われないよう、入力PNGをハッシュで固定する。
F4_SOURCE_SHA256 = "81b9b5dc9f1dffc38369606f3e2a5c91d21e75c63839972be577f761d57fc16a"

# パネルのラスタ部分の切り出し箱（ソースPNGのピクセル座標 left, top, right, bottom）。
# 「非白画素の割合が50%を超える連続した行・列」として実測した領域で、4枚とも
# 1008 x 1101〜1102 px。タイトル文字・カラーバー・目盛りラベルは含まない
# （それらは本関数が大きく描き直す）。
F4_PANEL_BOXES: dict[str, tuple[int, int, int, int]] = {
    "ndwi": (30, 110, 1038, 1212),
    "mndwi": (1400, 110, 2408, 1212),
    "ndvi": (30, 1378, 1038, 2479),
    "mask": (1357, 1378, 2365, 2479),
}

# パネルのタイトルとカラーバー設定。
# タイトル文字列・カラーマップ・値域・目盛りはポスター側 `make_f4_index_panels()` と
# 同一（閾値は `scripts/generate_exp002_poster_figures.py` の
# NDWI_THRESHOLD=-0.2 / MNDWI_THRESHOLD=-0.1 / NDVI_VEG_THRESHOLD=0.3 を
# f-string で埋めた結果と同じ表記）。最終マスクにカラーバーが無いのも同じ。
F4_PANEL_SPECS: list[tuple[str, str, str | None]] = [
    ("ndwi", "NDWI  (> -0.2)", "RdYlBu"),
    ("mndwi", "MNDWI  (> -0.1)", "RdYlBu"),
    ("ndvi", "NDVI  (mask > 0.3)", "RdYlGn"),
    ("mask", "Final mask", None),
]

# 図版全体の実寸。S5 の配置箱（幅5.4in・高さ4.8in）で配置倍率が 0.87 前後になり、
# native 18pt が実効 15.5pt 以上になるよう選んだ（実効値は validator が実測検査する）。
P05_FIGSIZE = (6.2, 5.5)
P05_DPI = 400  # 実寸が小さいので、配置幅あたりの精細さを保つため dpi を上げる


def make_p05_index_panels() -> None:
    """ポスター F4 のパネル画像を切り出し、英語ラベルを大きく描き直して P5 を作る。"""
    source = OUT_DIR / F4_SOURCE_NAME
    actual_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    assert actual_sha == F4_SOURCE_SHA256, (
        f"{F4_SOURCE_NAME} のSHA256が {actual_sha} で、切り出し座標を実測した版 "
        f"{F4_SOURCE_SHA256} と異なる（F4_PANEL_BOXES を再実測すること）"
    )

    with Image.open(source) as im:
        src = im.convert("RGB").copy()

    crops: dict[str, Image.Image] = {}
    for key, box in F4_PANEL_BOXES.items():
        crop = src.crop(box)
        # 切り出し箱がラスタの内側であること（縁に白い帯が入っていないこと）を確認する
        arr = np.asarray(crop).astype(int).sum(axis=2)
        for edge_name, edge in (
            ("top", arr[0, :]), ("bottom", arr[-1, :]),
            ("left", arr[:, 0]), ("right", arr[:, -1]),
        ):
            assert (edge < 730).mean() > 0.9, (
                f"P5: パネル '{key}' の切り出し箱の{edge_name}端に白い帯が含まれている"
                f"（非白率 {(edge < 730).mean():.2f}）— F4_PANEL_BOXES を再実測すること"
            )
        crops[key] = crop

    title_fontsize = 18.0
    tick_fontsize = 18.0

    fig, axes = plt.subplots(2, 2, figsize=P05_FIGSIZE, dpi=P05_DPI)
    for ax, (key, title, cmap) in zip(axes.flat, F4_PANEL_SPECS):
        ax.imshow(crops[key], interpolation="antialiased")
        ax.set_title(title, fontsize=title_fontsize)
        ax.axis("off")
        if cmap is None:
            continue
        cbar = fig.colorbar(
            ScalarMappable(norm=Normalize(vmin=-1, vmax=1), cmap=cmap),
            ax=ax, fraction=0.046, pad=0.04, ticks=[-1, 0, 1],
        )
        cbar.ax.tick_params(labelsize=tick_fontsize, colors=COL_TEXT)

    plt.tight_layout()
    out = OUT_DIR / "p05_index_panels.png"
    plt.savefig(out, dpi=P05_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    report_size(out)
    declare_font_sizes(
        "p05_index_panels.png",
        {"panel title": title_fontsize, "colorbar tick label": tick_fontsize},
        P05_DPI,
    )


# ---------------------------------------------------------------- P6: 検出分布図 + 4地区ラベル
def make_p06_clusters_map(features: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(11.0, 9.4), dpi=SAVE_DPI)
    setup_map_axes(ax)
    # 追跡済みの背景地図（CARTO Positron・ラベルなし）を最下層に敷く。検出ポリゴンが島のどこに
    # あるのかを海岸線との関係で読めるようにするため（DESIGN_GUIDE §7.3 に従い減光）。
    draw_basemap(ax)
    draw_water_polygons(ax, features)

    # native フォントは 20pt から 32pt へ引き上げた（Final review の Critical 指摘）。
    # S6 の配置幅では 20pt は実効 9.5pt しかなく、投影時に読めない。実効ptは
    # 「文字の物理サイズ ÷ 配置寸法」で決まるため、下限を満たすには図版内の文字を
    # 地図に対して相対的に大きくするしかない（配置側の拡大は S6 の帯高 4.8in が
    # 上限で、それだけでは 15pt に届かない）。
    zone_label_fontsize = 32.0

    # ラベルのオフセット（地区内最大ポリゴンの重心から見やすい方向へずらす。
    # 単位: メートル、3857座標系）。地図範囲(MAP_BBOX)の外に出ないことを確認済み。
    # 32pt 化でラベル箱が約1.6倍に広がったため、隣接する centre / west の衝突を
    # 避けるようオフセットを引き直した（実効値は保存後の目視とレンダリングで確認）。
    label_offsets_m = {
        "north": (250, 620),
        "south-east": (-150, -640),
        "west": (-620, 480),
        "centre": (240, -560),
    }
    zone_annotations = []
    for zone_name, (dx, dy) in label_offsets_m.items():
        anchor = find_zone_label_anchor(features, zone_name)
        if anchor is None:
            continue  # 地区内に該当ポリゴンが無ければラベルを描かない（強制割当はしない）
        lon, lat = anchor
        cx, cy = _to_3857(lon, lat)
        zone_annotations.append(ax.annotate(
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
        ))

    title_fontsize = 32.0
    # 32pt では元の1行タイトルは図の幅を大きく超えるため2行に折り返す
    # （フォントを縮めるのではなく表示方法を変える方針。P7・P12 と同じ）。
    # 末尾の「— 145 polygons」は外した。2行目が図の右端まで達して窮屈に見えるうえ、
    # 件数はスライド側のタイトルと 66pt コールアウトが既に述べており重複である。
    ax.set_title(
        "Detected water polygons and the four\ndocumented quarrying zones",
        fontsize=title_fontsize,
    )

    scalebar_fontsize = 32.0
    add_scalebar(ax, fontsize=scalebar_fontsize)

    # 帰属表示は地図軸の下（外側）に置く。地図面に重ならないことと、ゾーンラベルとの
    # 非重複を実測で検査する（将来の編集で軸内へ戻ってしまう回帰の防止）。
    credit = add_basemap_credit(ax, BASEMAP_CREDIT_PT_MAP)

    plt.tight_layout()
    assert_labels_inside_and_disjoint(fig, ax, zone_annotations, "P6")
    assert_credit_outside_map(fig, ax, credit, zone_annotations, "P6")
    out = OUT_DIR / "p06_clusters_map.png"
    plt.savefig(out, dpi=SAVE_DPI, bbox_inches="tight", facecolor="white")
    plt.close()
    report_size(out)
    declare_font_sizes(
        "p06_clusters_map.png",
        {
            "zone label": zone_label_fontsize,
            "title": title_fontsize,
            "scale bar label": scalebar_fontsize,
        },
        SAVE_DPI,
    )


# ---------------------------------------------------------------- P8: 検出分布図 + 訪問4地点
# P8 は地図の下に「帰属表示 1行 → 番号と地名の対応表 2行 → 凡例 2行」を積むため、
# 軸の位置を `tight_layout()` に任せず**明示的に確保**する（tight_layout は軸の外に
# 手で置いたテキストや凡例を知らないので、放っておくと図版の下辺が伸びて配置倍率＝
# 図中文字の実効ptが落ちる）。数値はすべて 32pt / 22pt の実測行高から積算した inch。
P08_MAP_H_IN = 5.30  # 地図軸の高さ（下の注記帯と 15pt 下限が許す最大値）
P08_TITLE_RESERVE_IN = 1.25  # 2行タイトル（32pt）
P08_CREDIT_RESERVE_IN = 0.52  # 帰属表示1行（22pt）
P08_KEY_RESERVE_IN = 1.10  # 対応表2行（32pt）
P08_LEGEND_RESERVE_IN = 1.55  # 凡例2行（32pt、枠つき）
P08_BOTTOM_MARGIN_IN = 0.10
P08_LEFT_IN = 0.45  # タイトルが地図軸より横に広いため左に余白を取る
P08_BELOW_MAP_IN = (
    P08_CREDIT_RESERVE_IN + P08_KEY_RESERVE_IN
    + P08_LEGEND_RESERVE_IN + P08_BOTTOM_MARGIN_IN
)
P08_FIG_H_IN = P08_MAP_H_IN + P08_BELOW_MAP_IN + P08_TITLE_RESERVE_IN
P08_FIG_W_IN = 8.5
# 図版の実寸高さの上限。S8 の配置箱は 4.6 x 4.8 in で高さ拘束なので、
# 配置倍率 = 4.8 / 実寸高さ。32pt の主題文字が 16pt 以上に見える上限を機械検査する。
P08_MAX_H_IN = 4.8 / (16.0 / 32.0)
# 番号の置き位置（単位: メートル、3857座標系。地点からのオフセット）。
# 互いに 145 m しか離れていない Toyoura Port / Toyoura hall は反対方向へ振り分ける。
# 値は「軸の内側」「番号どうしが重ならない」「検出ポリゴンを覆わない」の3条件を
# 満たす候補を機械探索して決めた（3条件はいずれも生成時に assert で検査する）。
P08_NUMBER_OFFSETS_M = {
    "Toyoura Port": (-190, 329),
    "Toyoura hall": (520, 0),
    "Sen-no-hama": (-116, 435),
    "Lake stage (Keirin)": (-520, 0),
}


def make_p08_visit_anchors_map(features: list[dict]) -> None:
    fig = plt.figure(figsize=(P08_FIG_W_IN, P08_FIG_H_IN), dpi=SAVE_DPI)
    map_h = P08_MAP_H_IN
    map_w = map_h * map_axes_ar()
    ax = fig.add_axes([
        P08_LEFT_IN / P08_FIG_W_IN,
        P08_BELOW_MAP_IN / P08_FIG_H_IN,
        map_w / P08_FIG_W_IN,
        map_h / P08_FIG_H_IN,
    ])
    setup_map_axes(ax)
    draw_basemap(ax)  # P6 と同じ背景地図（減光済み）
    draw_water_polygons(ax, features)

    # native フォントは 20pt から 32pt へ引き上げた（Final review の Critical 指摘。
    # S8 の配置幅では 20pt は実効 9.2pt しかなく、投影時に読めない）。
    label_fontsize = 32.0

    # 訪問4地点: 検出ポリゴンとは明確に異なる記号（黒い三角＋白縁）で重ねる。
    # これらは行程上の訪問地点であり、確認済みの丁場池ではない（凡例で明示する）。
    # 地図面に置くのは**通し番号だけ**で、地名は地図の下の対応表に出す
    # （理由は `VISIT_ANCHOR_NUMBERS` のコメント）。番号の箱は 32pt でも
    # 地図の縮尺で約 300 m 相当なので、各地点のすぐ隣に短いリーダー線で置ける。
    label_texts = dict(VISIT_ANCHOR_NUMBERS)
    label_offsets_m = P08_NUMBER_OFFSETS_M
    # マーカーを先に全て描き、ラベル（リーダー線付き）は後で重ねる。
    marker_xy = {}
    for name, lon, lat in VISIT_ANCHORS:
        x, y = _to_3857(lon, lat)
        marker_xy[name] = (x, y)
        ax.plot(
            x, y, marker="^", color="black", markersize=14,
            markeredgecolor="white", markeredgewidth=1.4, zorder=21,
        )
    visit_annotations = []
    for name, lon, lat in VISIT_ANCHORS:
        x, y = marker_xy[name]
        dx, dy = label_offsets_m[name]
        visit_annotations.append(ax.annotate(
            label_texts[name],
            xy=(x, y),
            xytext=(x + dx, y + dy),
            fontsize=label_fontsize,
            ha="center",
            va="center",
            color=COL_TEXT,
            zorder=22,
            arrowprops=dict(arrowstyle="-", color=COL_TEXT, linewidth=0.9),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=COL_TEXT, alpha=0.92),
        ))

    title_fontsize = 32.0
    # 32pt では元の1行タイトルは図の幅を大きく超えるため、2行に折り返し、
    # 検出件数（スライド側の 60〜72pt コールアウトと本文が既に述べている）を外した。
    # 主張境界の一文（route points であって confirmed ponds ではない）は残す。
    ax.set_title(
        "Visit anchors are route points,\nnot confirmed ponds",
        fontsize=title_fontsize,
    )

    scalebar_fontsize = 32.0
    add_scalebar(ax, fontsize=scalebar_fontsize)

    # 地図の下に積む注記（帰属表示 → 番号の対応表 → 凡例）の縦位置は、軸の実寸から
    # 算出する。軸位置は add_axes で固定してあるので実行ごとに同じ値になる（バイト一致の要件）。
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax_bb = ax.get_window_extent(renderer=renderer)
    ax_h_in = ax_bb.height / fig.dpi
    ax_w_in = ax_bb.width / fig.dpi

    credit = add_basemap_credit(ax, BASEMAP_CREDIT_PT_MAP)
    credit_h_frac = (BASEMAP_CREDIT_PT_MAP * 1.7) / 72.0 / ax_h_in

    # 番号と地名の対応表。2行 × 2列に置く。1列（4行）にすると縦に 2.6 in 使い、
    # 地図軸をその分だけ縮めることになるため、横に2列へ畳んだ。
    key_fontsize = 32.0
    key_row_h_frac = (key_fontsize * 1.45) / 72.0 / ax_h_in
    key_top = -0.012 - credit_h_frac
    key_texts = []
    for row_index, (left_entry, _) in enumerate(VISIT_KEY_ROWS):
        key_texts.append(ax.text(
            0.0, key_top - row_index * key_row_h_frac, left_entry,
            transform=ax.transAxes, ha="left", va="top",
            fontsize=key_fontsize, color=COL_TEXT,
        ))
    # 2列目の x は、1列目の実測幅（レンダラ計測）に一定の間隔を足して決める。
    fig.canvas.draw()
    col1_right_px = max(t.get_window_extent(renderer=renderer).x1 for t in key_texts)
    col2_x_frac = (col1_right_px - ax_bb.x0) / ax_bb.width + 0.45 / ax_w_in
    for row_index, (_, right_entry) in enumerate(VISIT_KEY_ROWS):
        key_texts.append(ax.text(
            col2_x_frac, key_top - row_index * key_row_h_frac, right_entry,
            transform=ax.transAxes, ha="left", va="top",
            fontsize=key_fontsize, color=COL_TEXT,
        ))

    legend_fontsize = 32.0
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
    # 地図の外（下側）に配置する。32pt では2列に並べると図の幅を超えて図版全体が
    # 横に伸び、配置倍率（＝実効pt）が下がるため、1列2行に積む。
    # 対応表の下に来るよう、その行数ぶん下げる。
    legend = ax.legend(
        handles=legend_handles,
        loc="upper left",
        bbox_to_anchor=(0.0, key_top - len(VISIT_KEY_ROWS) * key_row_h_frac + 0.06),
        ncol=1,
        fontsize=legend_fontsize,
        framealpha=0.92,
        edgecolor=COL_TEXT,
    )

    assert_labels_inside_and_disjoint(fig, ax, visit_annotations, "P8")
    assert_labels_clear_of_polygons(fig, ax, visit_annotations, features, "P8")
    assert_credit_outside_map(fig, ax, credit, visit_annotations, "P8")
    assert_key_below_map(fig, ax, key_texts, [credit, legend], "P8")
    out = OUT_DIR / "p08_visit_anchors_map.png"
    plt.savefig(
        out, dpi=SAVE_DPI, bbox_inches="tight", facecolor="white",
        bbox_extra_artists=[legend, *key_texts],
    )
    plt.close()
    with Image.open(out) as img:
        out_h_in = img.size[1] / SAVE_DPI
    assert out_h_in <= P08_MAX_H_IN, (
        f"P8: 図版の実寸高さ {out_h_in:.2f} in が上限 {P08_MAX_H_IN:.2f} in を超えている"
        f"（S8 は高さ拘束のため 32pt の主題文字が実効16pt を割る）"
    )
    report_size(out)
    declare_font_sizes(
        "p08_visit_anchors_map.png",
        {
            "visit number": label_fontsize,
            "anchor key": key_fontsize,
            "title": title_fontsize,
            "scale bar label": scalebar_fontsize,
            "legend": legend_fontsize,
        },
        SAVE_DPI,
    )


# ---------------------------------------------------------------- P7: 三スケール合成図（英語ラベルのみ）
# 3パネルは**表示寸法を完全に揃える**（DESIGN_GUIDE §4.3「並置する図版は表示寸法を
# 揃える」）。以前は各ソースの実比をそのまま列幅に使っていたため、(a) 縦長写真 =
# 狭い / (b) 16:9 = 広い / (c) 地図 = 中間 と3枚の幅が大きく違っていた（発表者からの指摘）。
#
# 共通のパネル比は**パネル(c) の地図範囲（MAP_BBOX）の比**とする。地図の比は島の形と
# 共有描画範囲（P6・P8 と同一）で決まっており縮めようがないのに対し、写真は上下を
# 切ればどの比にも合わせられるためである。引き伸ばしは一切しない（クロップのみ）。
# P7 は S7 でほぼ実寸（倍率≈1.03）で置かれるため、SAVE_DPI(200) のままでは配置後の
# 実効解像度が 195dpi となり下限 200dpi をわずかに割る。dpi は figure の実寸
# （インチ）とレイアウトを変えず画素数だけを増やすので、この図版だけ引き上げる。
P07_DPI = 240
# パネル(a)(b) の縦クロップ位置（上から取る割合）。共通比（約1.02）は縦長写真より
# 横長なので、2枚とも上下を切る。
#   (a) `choba_lake_3.jpg`（1500 x 1999 px、比 0.75）: 縦 531 px を落とす。
#       0.10 / 0.25 / 0.40 / 0.55 を並べて目視比較し、切削面の頂部と水面がともに残る
#       0.40（画像の 212〜1680 行）を選んだ。0.10 では水面が切れ、0.55 では岩壁の
#       上端（空との境）が失われる。
#   (b) `aerial_quarry_pond.jpg`（1080 x 1230 px、比 0.878）: 縦 172 px を落とす。
#       16:9 時代の 0.25 をそのまま用いる（クロップ量が 622 → 172 px に減ったため、
#       丁場池の水面と左右の切削面はいずれも余裕をもって残る）。
# 元画像は macOS の Dock と「Pages」ツールチップを切り落としたあとのものなので、
# どの vbias を選んでも UI は写らない（追跡ファイル自体が除去済み）。
P07_PANEL_A_VBIAS = 0.40
P07_PANEL_B_VBIAS = 0.25


def _load_photo(path: Path) -> Image.Image:
    with Image.open(path) as im:
        return im.convert("RGB").copy()


def _crop_top_bottom_to_aspect(img: Image.Image, target_ar: float, vbias: float) -> Image.Image:
    """画像の上下だけをクロップして目的のアスペクト比 `target_ar` に合わせる。

    `add_picture_cover()`（`exp002_kitagi_foss4g2026_presentation.py`）の
    「必要クロップ量はアスペクト比の差分から一意に決まり、`vbias` が上下の配分を
    決める」という式をここで再現する。本関数は「画像が目的より縦長
    （`img_ar < target_ar`）で上下だけをクロップする」場合のみを扱う
    （P7 の共通比 ≈ 1.02 に対し、パネル(a)(b) の写真はいずれも縦長でこのケースに該当する）。
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
        (a) On foot — texture         : choba_lake_3.jpg（S1表紙と同一写真。共通比へ
                                         縦クロップ `P07_PANEL_A_VBIAS`。Fix round 2 で
                                         グレースケールの fig03_keirin_cliff.jpg から
                                         色付きに差し替え）
        (b) From the air — boundaries : aerial_quarry_pond.jpg（S4左と同じ色付き原本。
                                         macOS の Dock とツールチップは追跡ファイルの
                                         時点で除去済み）を共通比へ縦クロップ
                                         （`P07_PANEL_B_VBIAS`）
        (c) From orbit — distribution : 検出145ポリゴンの分布（p06/p08と同じ配色・
                                         地図範囲。ゾーンラベル・訪問地点は描かない）

    3パネルは**表示寸法を完全に揃える**（共通比 = パネル(c) の地図範囲の比。
    写真は上下クロップのみで合わせ、引き伸ばしはしない）。
    """
    panel_ar = map_axes_ar()
    photo_a = _crop_top_bottom_to_aspect(
        _load_photo(OUT_DIR / "choba_lake_3.jpg"), panel_ar, P07_PANEL_A_VBIAS,
    )
    photo_b = _crop_top_bottom_to_aspect(
        _load_photo(OUT_DIR / "aerial_quarry_pond.jpg"), panel_ar, P07_PANEL_B_VBIAS,
    )

    # 3列すべて同じ比・同じ幅。キャプションは2行に折り返す（フォントを縮めず表示方法を
    # 変える方針。P12 と同じ）。
    panel_height_in = 3.2
    caption_fontsize = 21.0

    fig, (ax_a, ax_b, ax_c) = plt.subplots(
        1, 3, figsize=(panel_height_in * 3 * panel_ar, panel_height_in),
        dpi=P07_DPI, gridspec_kw={"width_ratios": [1, 1, 1], "wspace": 0.05},
    )

    title_texts = []
    panels = (
        (ax_a, photo_a, "(a) On foot —\ntexture"),
        (ax_b, photo_b, "(b) From the air —\nboundaries"),
    )
    for ax, photo, label in panels:
        ax.imshow(photo)
        ax.axis("off")
        title_texts.append(ax.set_title(label, fontsize=caption_fontsize, color=COL_TEXT, pad=10))

    setup_map_axes(ax_c, MAP_BBOX)
    draw_basemap(ax_c)  # P6・P8 と同じ背景地図（減光済み）
    draw_water_polygons(ax_c, features)
    add_scalebar(ax_c, fontsize=caption_fontsize)
    credit = add_basemap_credit(ax_c, P07_BASEMAP_CREDIT_PT)
    label_c = "(c) From orbit —\ndistribution"
    title_texts.append(ax_c.set_title(label_c, fontsize=caption_fontsize, color=COL_TEXT, pad=10))

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

    # 3パネルの**表示寸法が同一**であることを実測で検査する（DESIGN_GUIDE §4.3）。
    boxes = [ax.get_window_extent(renderer=renderer) for ax in (ax_a, ax_b, ax_c)]
    for i, bb in enumerate(boxes[1:], start=1):
        assert abs(bb.width - boxes[0].width) <= 1.0 and abs(bb.height - boxes[0].height) <= 1.0, (
            f"P7: パネル {i} の表示寸法 {bb.width:.1f}x{bb.height:.1f}px が "
            f"パネル 0 の {boxes[0].width:.1f}x{boxes[0].height:.1f}px と一致しない"
        )
    # 帰属表示はパネル(c) の地図の下（軸の外）に置く。地図面に重ならないことを検査する。
    assert_credit_outside_map(fig, ax_c, credit, [], "P7 panel (c)")

    out = OUT_DIR / "p07_three_scales.png"
    plt.savefig(out, dpi=P07_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    report_size(out)
    # P7 は S7 でほぼ実寸配置（倍率≈1.03）のため、native 21pt で実効21pt を超える。
    declare_font_sizes(
        "p07_three_scales.png",
        {"panel caption": caption_fontsize, "scale bar label": caption_fontsize},
        P07_DPI,
    )


# ---------------------------------------------------------------- P12: 3ステップフロー図
def make_p12_loop_diagram() -> None:
    # キャプションは27pt。24pt・1行のままでは各キャプションの幅が
    # 自ボックス幅を大きく超え、隣接キャプションと衝突して1行に見えてしまう回帰が
    # fix round 1で発生したため、フォントは縮めず、各キャプションを2行に折り返して
    # 自ボックスの幅に収める（Finding 2: フォントを縮めるのではなく表示方法を変える方針）。
    # 24pt → 27pt は Final review の Critical 指摘への対応。S12 の実配置（幅7.58in、
    # 高さ拘束）では 24pt は実効 14.7pt で 15pt 下限をわずかに割っていた。
    steps = [
        ("Satellite scan", ("a finite", "candidate list")),
        ("Field visit", ("see it with", "your own eyes")),
        ("OpenStreetMap", ("publish what", "you confirmed")),
    ]

    title_fontsize = 27.0
    caption_fontsize = 27.0

    box_w, box_h = 3.6, 1.5
    gap = 1.4  # キャプションの折り返しに加え、ボックス間隔にも余裕を持たせる
    n = len(steps)
    total_w = n * box_w + (n - 1) * gap
    fig, ax = plt.subplots(figsize=(12.5, 4.6), dpi=SAVE_DPI)
    ax.set_xlim(0, total_w)
    ax.set_ylim(0.1, 2.9)  # 2行キャプション分の縦の余白を確保
    ax.axis("off")

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
        caption_text = ax.text(
            cx, y0 - 0.15, "\n".join(caption_lines), ha="center", va="top",
            fontsize=caption_fontsize, color=COL_TEXT, style="italic",
            linespacing=1.3, zorder=6,
        )
        caption_texts.append(caption_text)

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
    report_size(out)
    declare_font_sizes(
        "p12_loop_diagram.png",
        {"box title": title_fontsize, "caption": caption_fontsize},
        SAVE_DPI,
    )


# ---------------------------------------------------------------- main
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fetch-basemap",
        action="store_true",
        help=(
            "背景地図タイルを取得してラスタを保存する（ネットワークを使う唯一の経路。"
            "図版は生成しない）"
        ),
    )
    args = parser.parse_args()
    if args.fetch_basemap:
        fetch_basemap()
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    assert_map_bbox_frames_island()
    features = load_polygons()
    print(f"loaded {len(features)} polygons from {GEOJSON_PATH.relative_to(PROJECT_ROOT)}")

    make_p05_index_panels()
    make_p06_clusters_map(features)
    make_p07_three_scales(features)
    make_p08_visit_anchors_map(features)
    make_p12_loop_diagram()
    print("\nAll presentation figures generated.")


if __name__ == "__main__":
    main()
