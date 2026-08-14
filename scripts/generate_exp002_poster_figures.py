"""FOSS4G Hiroshima 2026 北木島ポスター用の高解像度図版を生成する。

exp002（北木島丁場水域検出）の夏季シーン（2025-08-02）の解析を Sentinel-2
L2A（Microsoft Planetary Computer STAC API）から再取得して再計算し、
ポスター（docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg）に
配置する図版を約300dpi相当で出力する。

解析ロジック（バンド読込・指数計算・マスク・再投影・ポリゴン抽出）は
notebooks/exp002_kitagi_quarry_water_detection.ipynb と同一。再計算した
夏季の島内ポリゴン数がレポート確定値（145）と一致しない場合は例外で
停止する（ポスターの数値を勝手に更新しない）。

検証記録（2026-08-14 実施）:
- 夏季 S2A_MSIL2A_20250802T015121_R017_T53SLU_20250802T044417 の再計算は
  レポート確定値と完全一致（総146・島内145・植生マスク除外9px）。NDWI は
  tmp/exp002_kitagi_ndwi.tif（2026-03-21 のノートブック実行の生成物）と
  ビット一致。
- 春季 S2C_MSIL2A_20250323T014711_R017_T53SLU_20250323T051113 は指数統計
  （NDWI最大1.000・MNDWI最大0.615）はレポートと一致するが、現行ノート
  ブックのパイプラインでの再計算では島内180ポリゴンとなり、レポート確定値
  113 を再現できない（春季解析の実行時設定はリポジトリに未保存）。この
  ため春季の図化は行わず、ポスターにはレポート確定値のみを記載する。

実行方法:
    uv run python scripts/generate_exp002_poster_figures.py

出力先: docs/posters/figures/exp002/
    poster_f1_study_area.png      — 位置図（瀬戸内海広域 + 笠岡諸島）
    poster_f3_summer_map.png      — 夏季の検出水域ポリゴン分布図（主要図版）
    poster_f4_index_panels.png    — 夏季の NDWI/MNDWI/NDVI/最終マスク 2x2 パネル
    poster_f5_truecolor_water.png — 夏季トゥルーカラー + 水域強調画像
    poster_f6_field_photos.jpg    — 現地写真2枚の横並び合成

バンドデータは tmp/poster_cache_<season>.npz にキャッシュし、再実行時は
ネットワークアクセスを省略する。背景地図は F1 のみ地理院英語版タイルを使用
（クレジットはポスター側キャプションに記載）。F3 はタイルを使わず、
シーン由来の陸域シルエットを背景とする（英語のみ要件のため）。
"""

from __future__ import annotations

from pathlib import Path

import contextily as cx
import matplotlib.pyplot as plt
import numpy as np
import pyproj
import rasterio
import rasterio.transform
from affine import Affine
from PIL import Image
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rasterio.features import shapes as rasterio_shapes
from rasterio.transform import from_bounds as transform_from_bounds
from rasterio.warp import calculate_default_transform, reproject, transform_bounds
from rasterio.windows import from_bounds
from shapely.geometry import shape as shapely_shape
from shapely.ops import transform as shapely_transform

# ---------------------------------------------------------------- 定数
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "docs" / "posters" / "figures" / "exp002"
PHOTO_DIR = PROJECT_ROOT / "docs" / "results" / "exp002" / "photos"
CACHE_DIR = PROJECT_ROOT / "tmp"

# 北木島の中心座標と範囲（exp002 ノートブックと同一）
KITAGI_CENTER = (133.543, 34.374)  # (lon, lat)
KITAGI_BBOX = [133.515, 34.350, 133.570, 34.400]  # [west, south, east, north]

# 水域判定閾値（exp002 ノートブックと同一）
NDWI_THRESHOLD = -0.2
MNDWI_THRESHOLD = -0.1
NDVI_VEG_THRESHOLD = 0.3
MIN_AREA_M2 = 100

# 海域除外の面積閾値（島内最大水域は 1.28ha なので十分に安全）
SEA_AREA_THRESHOLD_M2 = 100_000

# 図化対象シーン（夏季）とレポート確定値
SUMMER_DATE = "2025-08-02"
EXPECTED_SUMMER_ISLAND = 145
EXPECTED_SUMMER_VEG_EXCL = 9

# 地理院タイル（背景地図）。F1 のみ英語版（z5-11提供）を使用。
# 淡色・白地図タイルは日本語地名を含むため F3 では使用しない。
GSI_ENGLISH = "https://cyberjapandata.gsi.go.jp/xyz/english/{z}/{x}/{y}.png"

# ポスターの配色（内容契約の granite/sea パレット）
COL_TEXT = "#2b2b2b"
COL_WATER = "#0d47a1"
COL_VEG = "#4a7c46"
COL_STONE = "#b0a999"

_to_3857 = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True).transform

plt.rcParams["font.family"] = ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.color"] = COL_TEXT
plt.rcParams["axes.edgecolor"] = COL_TEXT


# ---------------------------------------------------------------- データ取得
def read_band_aoi(asset_href, bbox, target_shape=None):
    """指定バウンディングボックス範囲のバンドデータを読み込む（ノートブックと同一）。"""
    with rasterio.open(asset_href) as src:
        bounds_native = transform_bounds("EPSG:4326", src.crs, *bbox)
        window = from_bounds(*bounds_native, src.transform)

        if target_shape is not None:
            data = src.read(
                1, window=window, out_shape=target_shape, resampling=Resampling.bilinear
            ).astype(np.float32)
        else:
            data = src.read(1, window=window).astype(np.float32)

        actual_bounds = rasterio.windows.bounds(window, src.transform)

        if target_shape is not None:
            win_transform = transform_from_bounds(
                *actual_bounds, target_shape[1], target_shape[0]
            )
        else:
            win_transform = src.window_transform(window)

        return data, win_transform, src.crs


def fetch_scene(season: str, date: str) -> dict:
    """シーンのバンドデータを取得する。tmp/ にキャッシュがあればそれを使う。"""
    cache_path = CACHE_DIR / f"poster_cache_{season}.npz"
    if cache_path.exists():
        z = np.load(cache_path, allow_pickle=False)
        print(f"[{season}] キャッシュ使用: {cache_path.name} (scene={z['scene_id']})")
        return {
            "scene_id": str(z["scene_id"]),
            "cloud_cover": float(z["cloud_cover"]),
            "bands": {k: z[k] for k in ("blue", "green", "red", "nir", "swir")},
            "transform": Affine(*z["transform"][:6]),
            "crs": CRS.from_wkt(str(z["crs_wkt"])),
        }

    import planetary_computer
    import pystac_client

    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=KITAGI_BBOX,
        datetime=f"{date}T00:00:00Z/{date}T23:59:59Z",
    )
    items = list(search.items())
    if not items:
        raise RuntimeError(f"[{season}] {date} のシーンが見つかりません")
    item = min(items, key=lambda it: it.properties["eo:cloud_cover"])
    print(f"[{season}] シーン取得: {item.id} (雲量 {item.properties['eo:cloud_cover']:.1f}%)")

    green, win_transform, crs = read_band_aoi(item.assets["B03"].href, KITAGI_BBOX)
    ref_shape = green.shape
    blue, _, _ = read_band_aoi(item.assets["B02"].href, KITAGI_BBOX)
    red, _, _ = read_band_aoi(item.assets["B04"].href, KITAGI_BBOX)
    nir, _, _ = read_band_aoi(item.assets["B08"].href, KITAGI_BBOX)
    swir, _, _ = read_band_aoi(item.assets["B11"].href, KITAGI_BBOX, target_shape=ref_shape)

    np.savez_compressed(
        cache_path,
        scene_id=item.id,
        cloud_cover=item.properties["eo:cloud_cover"],
        blue=blue,
        green=green,
        red=red,
        nir=nir,
        swir=swir,
        transform=np.array(
            [win_transform.a, win_transform.b, win_transform.c,
             win_transform.d, win_transform.e, win_transform.f]
        ),
        crs_wkt=crs.to_wkt(),
    )
    return {
        "scene_id": item.id,
        "cloud_cover": float(item.properties["eo:cloud_cover"]),
        "bands": {"blue": blue, "green": green, "red": red, "nir": nir, "swir": swir},
        "transform": win_transform,
        "crs": crs,
    }


# ---------------------------------------------------------------- 解析（ノートブックと同一）
def analyze_scene(scene: dict) -> dict:
    b = scene["bands"]
    green, red, nir, swir = b["green"], b["red"], b["nir"], b["swir"]

    ndwi = np.where((green + nir) > 0, (green - nir) / (green + nir), 0)
    mndwi = np.where((green + swir) > 0, (green - swir) / (green + swir), 0)
    ndvi = np.where((nir + red) > 0, (nir - red) / (nir + red), 0)
    veg_mask = ndvi > NDVI_VEG_THRESHOLD
    water_candidates = (ndwi > NDWI_THRESHOLD) | (mndwi > MNDWI_THRESHOLD)
    water_mask = water_candidates & ~veg_mask

    # UTM → EPSG:4326 再投影（ノートブックと同一手順）
    crs, win_transform = scene["crs"], scene["transform"]
    dst_crs = CRS.from_epsg(4326)
    src_bounds = rasterio.transform.array_bounds(
        water_mask.shape[0], water_mask.shape[1], win_transform
    )
    dst_transform_4326, dst_width, dst_height = calculate_default_transform(
        crs, dst_crs, water_mask.shape[1], water_mask.shape[0], *src_bounds
    )
    water_mask_4326 = np.zeros((dst_height, dst_width), dtype=np.uint8)
    reproject(
        source=water_mask.astype(np.uint8),
        destination=water_mask_4326,
        src_transform=win_transform,
        src_crs=crs,
        dst_transform=dst_transform_4326,
        dst_crs=dst_crs,
        resampling=Resampling.nearest,
    )
    water_mask_4326 = water_mask_4326.astype(bool)

    # 水域ポリゴン抽出（面積計算式もノートブックと同一）
    polygon_generator = rasterio_shapes(
        water_mask_4326.astype(np.uint8), mask=water_mask_4326, transform=dst_transform_4326
    )
    cos_lat = np.cos(np.radians(34.374))
    features = []
    for geom, _val in polygon_generator:
        poly = shapely_shape(geom)
        area_m2 = poly.area * (111_000**2) * cos_lat
        if area_m2 >= MIN_AREA_M2:
            features.append({"area_m2": area_m2, "shape": poly})

    # 陸域シルエット（F3 の背景用）: 水域マスクの補集合から抽出
    land_mask = ~water_mask_4326
    land_features = []
    for geom, _val in rasterio_shapes(
        land_mask.astype(np.uint8), mask=land_mask, transform=dst_transform_4326
    ):
        poly = shapely_shape(geom)
        area_m2 = poly.area * (111_000**2) * cos_lat
        if area_m2 >= 10_000:  # 微小なスペックルを除外
            land_features.append(poly)

    island = [
        f
        for f in features
        if f["area_m2"] < SEA_AREA_THRESHOLD_M2
        and KITAGI_BBOX[0] <= f["shape"].centroid.x <= KITAGI_BBOX[2]
        and KITAGI_BBOX[1] <= f["shape"].centroid.y <= KITAGI_BBOX[3]
    ]

    return {
        "ndwi": ndwi,
        "mndwi": mndwi,
        "ndvi": ndvi,
        "veg_mask": veg_mask,
        "water_candidates": water_candidates,
        "water_mask": water_mask,
        "features_all": features,
        "features_island": island,
        "land_features": land_features,
    }


# ---------------------------------------------------------------- 図版ヘルパ
def setup_map_axes(ax, west, south, east, north):
    xmin, ymin = _to_3857(west, south)
    xmax, ymax = _to_3857(east, north)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor(COL_TEXT)
        spine.set_linewidth(0.8)


def add_scalebar(ax, lat: float, km: float = 1.0, fontsize: int = 11):
    """左下に簡易スケールバーを描く（Web Mercator の緯度補正込み）。"""
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


def normalize_band(band, pct_low=2, pct_high=98):
    low = np.percentile(band, pct_low)
    high = np.percentile(band, pct_high)
    if high == low:
        return np.zeros_like(band, dtype=np.uint8)
    return np.clip((band - low) / (high - low) * 255, 0, 255).astype(np.uint8)


def report_size(path: Path):
    with Image.open(path) as img:
        w, h = img.size
    print(f"saved: {path.relative_to(PROJECT_ROOT)} ({w} x {h} px)")


# ---------------------------------------------------------------- F1 位置図
def make_f1_study_area():
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.6), dpi=300)

    ax1 = axes[0]
    setup_map_axes(ax1, 131.7, 33.3, 136.0, 35.4)
    # 英語版タイルには主要都市名が既に入っているため、追加ラベルは北木島のみ
    cx.add_basemap(ax1, source=GSI_ENGLISH, zoom=8, attribution=False)
    kx, ky = _to_3857(*KITAGI_CENTER)
    ax1.plot(kx, ky, "*", color=COL_WATER, markersize=24, markeredgecolor="white",
             markeredgewidth=1.2, zorder=10)
    ax1.annotate(
        "Kitagi Island",
        xy=(kx, ky),
        xytext=(kx - 65000, ky - 80000),
        fontsize=16,
        weight="bold",
        ha="center",
        va="top",
        zorder=10,
        color=COL_TEXT,
        arrowprops=dict(arrowstyle="-", color=COL_TEXT, linewidth=1.0),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COL_TEXT, alpha=0.9),
    )
    ax1.set_title("(a) Seto Inland Sea, western Japan", fontsize=16)

    ax2 = axes[1]
    setup_map_axes(ax2, 133.45, 34.30, 133.62, 34.52)
    cx.add_basemap(ax2, source=GSI_ENGLISH, zoom=11, attribution=False)
    places = {
        "Kasaoka Port": (133.498, 34.500, "s", "dimgray", 8, (800, -3300), "top"),
        "Shiraishi Island": (133.515, 34.430, "o", "dimgray", 6, (900, 0), "center"),
        "Kitagi Island": (133.543, 34.374, "*", COL_WATER, 24, (1100, 0), "center"),
        "Manabe Island": (133.560, 34.330, "o", "dimgray", 6, (900, 0), "center"),
    }
    for name, (lon, lat, marker, color, size, (dx, dy), va) in places.items():
        x, y = _to_3857(lon, lat)
        kwargs = {"markeredgecolor": "white", "markeredgewidth": 1.0} if "Kitagi" in name else {}
        ax2.plot(x, y, marker, color=color, markersize=size, zorder=10, **kwargs)
        ax2.text(
            x + dx,
            y + dy,
            name,
            fontsize=16 if "Kitagi" in name else 15,
            weight="bold" if "Kitagi" in name else "normal",
            va=va,
            zorder=10,
            color=COL_TEXT,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75),
        )
    ax2.set_title("(b) Kasaoka Islands, Okayama Pref.", fontsize=16)

    plt.tight_layout()
    out = OUT_DIR / "poster_f1_study_area.png"
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    report_size(out)


# ---------------------------------------------------------------- F3 夏季分布図（主要図版）
def make_f3_summer_map(res: dict):
    """タイル背景を使わず、Sentinel-2 由来の陸域シルエット + 検出ポリゴンを描画する。

    背景タイル（地理院淡色）には日本語地名が含まれ「英語のみ」要件に抵触する
    ため、シーン自身から導出した海岸線・島形状を背景とする（Task 4 M1 対応）。
    """
    fig, ax = plt.subplots(figsize=(9.8, 9.2), dpi=300)
    setup_map_axes(ax, *KITAGI_BBOX)
    ax.set_facecolor("#e9eff6")  # 海: ごく薄い青（グレースケール印刷でも陸と分離可能）

    # 陸域シルエット（10 m マスク由来。ピクセル境界のまま描画）
    for poly in res["land_features"]:
        poly_3857 = shapely_transform(_to_3857, poly)
        polys = [poly_3857] if poly_3857.geom_type == "Polygon" else list(poly_3857.geoms)
        for p in polys:
            xs, ys = p.exterior.xy
            ax.fill(xs, ys, color="#eae5d9", edgecolor="#8a8375", linewidth=0.5, zorder=3)

    # 検出水域ポリゴン
    for f in res["features_island"]:
        poly_3857 = shapely_transform(_to_3857, f["shape"])
        polys = [poly_3857] if poly_3857.geom_type == "Polygon" else list(poly_3857.geoms)
        for p in polys:
            xs, ys = p.exterior.xy
            ax.fill(xs, ys, color=COL_WATER, alpha=0.95, edgecolor="#062a52",
                    linewidth=0.4, zorder=5)

    # 島名ラベル（英語のみ、島の上に配置）
    lx, ly = _to_3857(133.5265, 34.3745)
    ax.text(lx, ly, "Kitagi Island", fontsize=18, style="italic", color="#6b665c",
            ha="center", zorder=10)

    count = len(res["features_island"])
    ax.set_title(
        f"Detected intra-island water polygons ≥100 m²  —  Summer {SUMMER_DATE}  ·  {count} polygons",
        fontsize=18,
    )
    add_scalebar(ax, KITAGI_CENTER[1], km=1.0, fontsize=18)

    plt.tight_layout()
    out = OUT_DIR / "poster_f3_summer_map.png"
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    report_size(out)


# ---------------------------------------------------------------- F4 指数パネル（夏季）
def make_f4_index_panels(res: dict):
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 8.6), dpi=300)

    panels = [
        (res["ndwi"], "RdYlBu", f"NDWI  (> {NDWI_THRESHOLD})"),
        (res["mndwi"], "RdYlBu", f"MNDWI  (> {MNDWI_THRESHOLD})"),
        (res["ndvi"], "RdYlGn", f"NDVI  (mask > {NDVI_VEG_THRESHOLD})"),
    ]
    for ax, (data, cmap, title) in zip(axes.flat[:3], panels):
        im = ax.imshow(data, cmap=cmap, vmin=-1, vmax=1, interpolation="nearest")
        ax.set_title(title, fontsize=18)
        ax.axis("off")
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, ticks=[-1, 0, 1])
        cbar.ax.tick_params(labelsize=18, colors=COL_TEXT)

    mask_rgb = np.zeros((*res["water_mask"].shape, 3), dtype=np.uint8)
    mask_rgb[~res["water_mask"] & ~res["veg_mask"]] = [176, 169, 153]  # COL_STONE
    mask_rgb[res["veg_mask"]] = [74, 124, 70]  # COL_VEG
    mask_rgb[res["water_mask"]] = [13, 71, 161]  # COL_WATER
    ax = axes.flat[3]
    ax.imshow(mask_rgb, interpolation="nearest")
    ax.set_title("Final mask", fontsize=18)
    ax.axis("off")

    plt.tight_layout()
    out = OUT_DIR / "poster_f4_index_panels.png"
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    report_size(out)


# ---------------------------------------------------------------- F5 トゥルーカラー + 水域強調（夏季）
def make_f5_truecolor_water(res: dict, scene: dict):
    b = scene["bands"]
    r = normalize_band(b["red"])
    g = normalize_band(b["green"])
    bl = normalize_band(b["blue"])
    water_mask = res["water_mask"]

    blend = 0.5
    r_hl, g_hl, b_hl = r.copy(), g.copy(), bl.copy()
    r_hl[water_mask] = (r[water_mask] * (1 - blend)).astype(np.uint8)
    g_hl[water_mask] = np.clip(g[water_mask] * (1 - blend) + 100 * blend, 0, 255).astype(np.uint8)
    b_hl[water_mask] = np.clip(bl[water_mask] * (1 - blend) + 255 * blend, 0, 255).astype(np.uint8)

    fig, axes = plt.subplots(1, 2, figsize=(10.3, 5.1), dpi=300)
    axes[0].imshow(np.stack([r, g, bl], axis=-1), interpolation="nearest")
    axes[0].set_title("True color (B04/B03/B02)", fontsize=19)
    axes[0].axis("off")
    axes[1].imshow(np.stack([r_hl, g_hl, b_hl], axis=-1), interpolation="nearest")
    axes[1].set_title("Detected water in blue", fontsize=19)
    axes[1].axis("off")
    plt.tight_layout()
    out = OUT_DIR / "poster_f5_truecolor_water.png"
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    report_size(out)


# ---------------------------------------------------------------- F6 現地写真合成
def make_f6_field_photos():
    img1 = Image.open(PHOTO_DIR / "choba_lake_1.jpg").convert("RGB")
    img2 = Image.open(PHOTO_DIR / "choba_lake_3.jpg").convert("RGB")

    target_h = 1990

    def resize_h(img):
        w, h = img.size
        return img.resize((round(w * target_h / h), target_h), Image.LANCZOS)

    img1, img2 = resize_h(img1), resize_h(img2)
    gap = 24
    composite = Image.new("RGB", (img1.width + gap + img2.width, target_h), "white")
    composite.paste(img1, (0, 0))
    composite.paste(img2, (img1.width + gap, 0))
    out = OUT_DIR / "poster_f6_field_photos.jpg"
    composite.save(out, "JPEG", quality=92, optimize=True)
    report_size(out)


# ---------------------------------------------------------------- main
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    scene = fetch_scene("summer", SUMMER_DATE)
    res = analyze_scene(scene)
    n_island = len(res["features_island"])
    n_veg_excl = int((res["water_candidates"] & res["veg_mask"]).sum())
    print(
        f"[summer] scene={scene['scene_id']} 雲量={scene['cloud_cover']:.1f}% "
        f"総ポリゴン={len(res['features_all'])} 島内={n_island} "
        f"(期待値 {EXPECTED_SUMMER_ISLAND}) 植生マスク除外={n_veg_excl} px"
    )
    if n_island != EXPECTED_SUMMER_ISLAND or n_veg_excl != EXPECTED_SUMMER_VEG_EXCL:
        raise RuntimeError(
            f"[summer] 再計算結果（島内={n_island}, 植生除外={n_veg_excl}px）が"
            f"レポート確定値（{EXPECTED_SUMMER_ISLAND}, {EXPECTED_SUMMER_VEG_EXCL}px）"
            "と一致しません。ポスター制作を中止します。"
        )

    make_f1_study_area()
    make_f3_summer_map(res)
    make_f4_index_panels(res)
    make_f5_truecolor_water(res, scene)
    make_f6_field_photos()
    print("All poster figures generated.")


if __name__ == "__main__":
    main()
