"""8月31日の北木島現地確認に向けた撮影対象リストを生成する。

exp002（北木島丁場水域検出）で公開した夏季145ポリゴン
（docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson）と、
OSM の水域・採石場地物の保存済み照合結果（docs/results/exp002/exp002_osm_water_features.json）
を突き合わせ、2026年8月31日の再訪で現地確認すべき候補を3クラスに分けて抽出する。

- largest: 検出最大ポリゴン（7,826 m²、北部）。OSM の「今岡石材丁場跡（北木の桂林）」と
  重なる位置にある。GPS・撮影方向・撮影時刻を記録する最優先対象
- unmapped: OSM 地物が100 m以内にない検出ポリゴンのうち、面積上位10件。
  2026年3月の訪問で使った4地点（豊浦港・豊浦公会堂・湖上ステージ(桂林)・千ノ浜）からの
  概算距離を併記し、到達しやすい順（最寄り地点までの距離が短い順）に並べる
- confounder: `water=reservoir` の OSM 地物（北木北ポンプ室）から100 m以内にある検出ポリゴン。
  人工ため池・貯水施設との誤検出の可能性を現地で確認する対象

距離の定義: scripts/compare_exp002_osm_features.py と同一。地物形状を EPSG:32653
（UTM 53N）へ投影した**形状間距離**を用いる（重なっている場合は0 m）。中心点・重心に
よる近似は距離を過大評価するため使わない。ただし表に記載する緯度経度は現地で目印にする
ための検出ポリゴンの重心（WGS84、度小数6桁）である。

これは精度検証ではない。OSM はコミュニティ寄稿データであり正解データではないため、
近傍地物の有無は「OSM未登録」か「誤検出」のいずれかを意味し、状態は未決着である。
本リストは探索的な現地確認のための候補選定であり、サンプリングに基づく精度検証ではない。
現地では安全・立入許可・到達可能性を面積順位よりも優先すること。

実行方法:
    uv run python scripts/build_exp002_field_shot_list.py
"""

from __future__ import annotations

import json
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import Point, shape
from shapely.ops import transform as shapely_transform

# compare_exp002_osm_features.py の element_geometry() をそのまま再利用する
from compare_exp002_osm_features import element_geometry

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "docs" / "results" / "exp002"
GEOJSON_PATH = RESULTS_DIR / "exp002_kitagi_summer_water_polygons_2025-08-02.geojson"
OSM_ARCHIVE = RESULTS_DIR / "exp002_osm_water_features.json"
OUTPUT_PATH = RESULTS_DIR / "exp002_field_shot_list_2026-08-31.md"

UTM_CRS = "EPSG:32653"  # 解析・照合スクリプトと同じ UTM Zone 53N
PRIMARY_THRESHOLD_M = 100
UNMAPPED_TOP_N = 10
PUMP_ROOM_NAME = "北木北ポンプ室"
KEIRIN_NAME = "今岡石材丁場跡（北木の桂林）"

# Task 1 の VISIT_ANCHORS が未実装のため、2026年3月訪問時の徒歩起点4地点を
# scripts/build_chiri_koryu_figures.py と同じ座標（lon, lat）で固定値として使う。
VISIT_ANCHORS = [
    ("豊浦港", 133.5369, 34.3956),
    ("豊浦公会堂", 133.5364, 34.3943),
    ("湖上ステージ(桂林)", 133.5329, 34.3912),
    ("千ノ浜", 133.5309, 34.3930),
]


def load_detections(to_utm) -> list[dict]:
    """検出ポリゴンを読み込み、WGS84の重心とUTM形状を付与する。"""
    data = json.loads(GEOJSON_PATH.read_text(encoding="utf-8"))
    detections = []
    for feature in data["features"]:
        geom_wgs84 = shape(feature["geometry"])
        centroid = geom_wgs84.centroid
        detections.append({
            "id": feature["properties"]["id"],
            "area_m2": feature["properties"]["area_m2"],
            "lon": round(centroid.x, 6),
            "lat": round(centroid.y, 6),
            "geom_utm": shapely_transform(to_utm, geom_wgs84),
        })
    # ID で安定ソート（決定的な順序を保証する）
    detections.sort(key=lambda d: d["id"])
    return detections


def load_osm(to_utm) -> list[dict]:
    """OSM保存応答を読み込み、UTM形状を付与する（ネットワークアクセスなし）。"""
    archive = json.loads(OSM_ARCHIVE.read_text(encoding="utf-8"))
    osm = []
    for element in archive["elements"]:
        geom = element_geometry(element)
        if geom is None:
            continue
        osm.append({
            "tags": element.get("tags", {}),
            "geom_utm": shapely_transform(to_utm, geom),
        })
    return osm


def nearest_osm_feature(det_geom_utm, osm: list[dict]) -> tuple[float, dict | None]:
    """検出ポリゴンから最も近いOSM地物とその形状間距離を返す。"""
    best_dist = float("inf")
    best_o = None
    for o in osm:
        d = det_geom_utm.distance(o["geom_utm"])
        if d < best_dist:
            best_dist = d
            best_o = o
    return best_dist, best_o


def osm_label(o: dict | None) -> str:
    if o is None:
        return "（該当なし）"
    tags = o["tags"]
    name = tags.get("name")
    if name:
        return name
    kv = " ".join(f"{k}={tags[k]}" for k in ("natural", "water", "landuse") if k in tags)
    return kv or "（タグなし）"


def gsi_link(lat: float, lon: float) -> str:
    return f"https://maps.gsi.go.jp/#18/{lat}/{lon}"


def osm_link(lat: float, lon: float) -> str:
    return f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}"


def build_rows() -> list[dict]:
    to_utm = Transformer.from_crs("EPSG:4326", UTM_CRS, always_xy=True).transform

    detections = load_detections(to_utm)
    osm = load_osm(to_utm)

    pump_room = next((o for o in osm if o["tags"].get("name") == PUMP_ROOM_NAME), None)
    assert pump_room is not None, f"OSM地物『{PUMP_ROOM_NAME}』がアーカイブに見つからない"
    keirin = next((o for o in osm if o["tags"].get("name") == KEIRIN_NAME), None)
    assert keirin is not None, f"OSM地物『{KEIRIN_NAME}』がアーカイブに見つからない"

    anchor_points_utm = [
        (name, shapely_transform(to_utm, Point(lon, lat)))
        for name, lon, lat in VISIT_ANCHORS
    ]

    enriched = []
    for d in detections:
        dist, nearest = nearest_osm_feature(d["geom_utm"], osm)
        dist_pump = d["geom_utm"].distance(pump_room["geom_utm"])
        enriched.append({
            **d,
            "nearest_osm_dist_m": dist,
            "nearest_osm_label": osm_label(nearest),
            "dist_pump_room_m": dist_pump,
        })

    # largest: 検出最大ポリゴン（北部、今岡石材丁場跡（北木の桂林）と重なる）
    largest = max(enriched, key=lambda d: d["area_m2"])
    dist_keirin = largest["geom_utm"].distance(keirin["geom_utm"])
    assert dist_keirin == 0.0, (
        f"最大ポリゴン（id={largest['id']}）が『{KEIRIN_NAME}』と重なっていない"
        f"（距離 {dist_keirin:.1f} m）"
    )

    # confounder: water=reservoir（北木北ポンプ室）から100 m以内の検出ポリゴン
    confounders = [d for d in enriched if d["dist_pump_room_m"] <= PRIMARY_THRESHOLD_M]
    confounders.sort(key=lambda d: (d["dist_pump_room_m"], d["id"]))

    # unmapped: OSM地物が100 m以内にない検出ポリゴンのうち面積上位10件
    unmapped_pool = [d for d in enriched if d["nearest_osm_dist_m"] > PRIMARY_THRESHOLD_M]
    unmapped_pool.sort(key=lambda d: (-d["area_m2"], d["id"]))
    unmapped_top = unmapped_pool[:UNMAPPED_TOP_N]

    for d in unmapped_top:
        anchor_dists = [
            (name, round(d["geom_utm"].distance(pt), 1)) for name, pt in anchor_points_utm
        ]
        d["anchor_dists"] = anchor_dists
        d["min_anchor_dist_m"] = min(v for _, v in anchor_dists)

    # 到達しやすい順（最寄り徒歩起点までの距離が短い順）、同距離はIDで安定ソート
    unmapped_top.sort(key=lambda d: (d["min_anchor_dist_m"], d["id"]))

    rows: list[dict] = []

    rows.append({
        "class": "largest",
        "id": largest["id"],
        "lat": largest["lat"],
        "lon": largest["lon"],
        "area_m2": largest["area_m2"],
        "osm_label": largest["nearest_osm_label"],
        "osm_dist_m": largest["nearest_osm_dist_m"],
        "note": "",
        "anchor_note": "",
    })

    for d in unmapped_top:
        anchor_note = "; ".join(f"{name} {dist:.1f} m" for name, dist in d["anchor_dists"])
        rows.append({
            "class": "unmapped",
            "id": d["id"],
            "lat": d["lat"],
            "lon": d["lon"],
            "area_m2": d["area_m2"],
            "osm_label": d["nearest_osm_label"],
            "osm_dist_m": d["nearest_osm_dist_m"],
            "note": "",
            "anchor_note": anchor_note,
        })

    for d in confounders:
        rows.append({
            "class": "confounder",
            "id": d["id"],
            "lat": d["lat"],
            "lon": d["lon"],
            "area_m2": d["area_m2"],
            "osm_label": PUMP_ROOM_NAME,
            "osm_dist_m": d["dist_pump_room_m"],
            "note": "",
            "anchor_note": "",
        })

    return rows


def render_markdown(rows: list[dict], osm_retrieved: str) -> str:
    lines: list[str] = []
    out = lines.append

    out("# 8月31日 現地確認用 撮影対象リスト（exp002 / 北木島）")
    out("")
    out("**現地では安全・立入許可・到達可能性を面積順位よりも優先すること。**"
        "私有地・工事区域・崖地・水面への立入りが必要と判断される場合は、その地点の"
        "撮影を見送ってよい。")
    out("")
    out("**本リストは探索的な現地確認のための候補選定であり、サンプリングに基づく"
        "精度検証ではない。** OSM近傍地物の有無は「OSM未登録」か「誤検出」のいずれかを"
        "意味し、状態は未決着である。現地確認は不一致の解消（現物の有無・種別の確認）を"
        "目的とする。")
    out("")
    out(f"- 検出ポリゴン: `{GEOJSON_PATH.name}`（夏季 2025-08-02）")
    out(f"- OSM参照: `{OSM_ARCHIVE.name}`（取得日 {osm_retrieved}、Overpass `out geom meta` の保存応答。ネットワーク再取得なし）")
    out(f"- 距離の定義: 検出ポリゴンとOSM地物形状を EPSG:32653（UTM 53N）へ投影した"
        "**形状間距離**（重なっている場合は0 m）。徒歩起点からの距離も同様に形状間距離。")
    out(f"- 抽出クラス: `largest`（検出最大ポリゴン1件）／ `unmapped`"
        f"（OSM地物が{PRIMARY_THRESHOLD_M} m以内にない検出のうち面積上位{UNMAPPED_TOP_N}件）"
        f"／ `confounder`（`{PUMP_ROOM_NAME}` から{PRIMARY_THRESHOLD_M} m以内の検出）")
    out("")

    out("## 撮影対象リスト")
    out("")
    out("| # | クラス | ポリゴンID | 緯度 | 経度 | 面積(m²) | OSM近傍地物 | OSMとの距離 | 徒歩起点からの距離 | 地理院地図 | OSM | 撮影メモ |")
    out("|---:|---|---:|---:|---:|---:|---|---:|---|---|---|---|")
    for i, r in enumerate(rows, start=1):
        osm_dist = "0 m（重なり）" if r["osm_dist_m"] == 0 else f"{r['osm_dist_m']:.1f} m"
        anchor_note = r["anchor_note"] if r["anchor_note"] else "-"
        gsi = gsi_link(r["lat"], r["lon"])
        osmlink = osm_link(r["lat"], r["lon"])
        out(
            f"| {i} | {r['class']} | {r['id']} | {r['lat']:.6f} | {r['lon']:.6f} | "
            f"{r['area_m2']:,.1f} | {r['osm_label']} | {osm_dist} | {anchor_note} | "
            f"[地理院地図]({gsi}) | [OSM]({osmlink}) | {r['note']} |"
        )
    out("")

    out("## クラス別メモ")
    out("")
    out(f"- **largest**: 検出最大ポリゴン（面積上位1件、北部）。GPS・撮影方向・撮影時刻を記録する。")
    out(f"- **unmapped**: OSM地物が{PRIMARY_THRESHOLD_M} m以内にない検出のうち面積上位"
        f"{UNMAPPED_TOP_N}件。豊浦港・豊浦公会堂・湖上ステージ(桂林)・千ノ浜の4地点のうち"
        "最寄り地点までの概算距離が短い順（到達しやすい順）に並べた。")
    out(f"- **confounder**: `{PUMP_ROOM_NAME}`（`water=reservoir`）から{PRIMARY_THRESHOLD_M} m"
        "以内の検出。人工ため池・貯水施設との誤検出の可能性を現地で確認する。")
    out("")

    return "\n".join(lines) + "\n"


def main() -> None:
    rows = build_rows()
    archive = json.loads(OSM_ARCHIVE.read_text(encoding="utf-8"))
    markdown = render_markdown(rows, archive["retrieved"])
    OUTPUT_PATH.write_text(markdown, encoding="utf-8")

    # --- 自己検査（本リポジトリのイディオム） ---
    assert len(rows) >= 12, f"候補が少なすぎる: {len(rows)}"
    assert any(r["class"] == "largest" for r in rows), "最大ポリゴンが含まれていない"
    assert any(r["class"] == "unmapped" for r in rows), "OSM近傍地物なしの候補が含まれていない"
    assert any(r["class"] == "confounder" for r in rows), "交絡例が含まれていない"
    assert all(133.515 <= r["lon"] <= 133.570 for r in rows), "島の範囲外の座標がある"
    print(f"OK: {len(rows)} 地点（largest / unmapped / confounder の3クラス）")


if __name__ == "__main__":
    main()
