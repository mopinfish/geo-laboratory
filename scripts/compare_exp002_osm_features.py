"""公開済みの検出ポリゴンと OpenStreetMap の水域・採石場地物を照合する。

exp002（北木島丁場水域検出）で公開した夏季145ポリゴン
（docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson）と、
OSM に登録済みの水域・採石場地物を突き合わせ、次を記録する。

- OSM 地物と検出ポリゴンが重なる件数（主指標）および 50/100/200 m の感度
- 検出ポリゴンのうち OSM に近傍地物がないものの数（状態未決着の候補）
- 名前付き地物（特に landuse=quarry）と検出ポリゴンの位置関係
- OSM 地物の最終編集日（コミュニティのマッピング活動の文脈）

距離の定義: Overpass の `out geom` で地物形状を取得し、EPSG:32653（UTM 53N）へ
投影して**形状間距離**を計算する。重なっている場合は 0 m になる。中心点や重心を
用いた近似は距離を過大評価するため使わない。

これは精度検証ではない。OSM はコミュニティ寄稿データであり正解データではないため、
重なりは独立した傍証、近傍地物の不在は「OSM 未登録」か「誤検出」のいずれかを意味する
（状態は未決着）。適合率・再現率は算出していない。

OSM は生きたデータベースなので、取得結果を
docs/results/exp002/exp002_osm_water_features.json へ取得日つきで保存し、
既定ではその保存済み応答を使う（--refresh で再取得）。

実行方法:
    uv run python scripts/compare_exp002_osm_features.py            # 保存済み応答を使う
    uv run python scripts/compare_exp002_osm_features.py --refresh  # Overpass から再取得
"""

from __future__ import annotations

import argparse
import collections
import json
import urllib.request
from datetime import date
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import LineString, Point, Polygon, shape
from shapely.ops import transform as shapely_transform

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "docs" / "results" / "exp002"
GEOJSON_PATH = RESULTS_DIR / "exp002_kitagi_summer_water_polygons_2025-08-02.geojson"
OSM_ARCHIVE = RESULTS_DIR / "exp002_osm_water_features.json"
REPORT_PATH = RESULTS_DIR / "exp002_osm_comparison.md"

# 解析と同一のバウンディングボックス [west, south, east, north]
KITAGI_BBOX = [133.515, 34.350, 133.570, 34.400]
UTM_CRS = "EPSG:32653"  # 解析と同じ UTM Zone 53N

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_QUERY = f"""[out:json][timeout:120];
(
  nwr["natural"="water"]({KITAGI_BBOX[1]},{KITAGI_BBOX[0]},{KITAGI_BBOX[3]},{KITAGI_BBOX[2]});
  nwr["landuse"="quarry"]({KITAGI_BBOX[1]},{KITAGI_BBOX[0]},{KITAGI_BBOX[3]},{KITAGI_BBOX[2]});
  nwr["water"]({KITAGI_BBOX[1]},{KITAGI_BBOX[0]},{KITAGI_BBOX[3]},{KITAGI_BBOX[2]});
);
out geom meta;
"""

THRESHOLDS_M = (50, 100, 200)
PRIMARY_THRESHOLD_M = 100


def fetch_osm() -> dict:
    """Overpass API から地物形状つきで取得し、取得日を添えて保存する。"""
    req = urllib.request.Request(
        OVERPASS_URL,
        data=OVERPASS_QUERY.encode("utf-8"),
        headers={"User-Agent": "geo-laboratory exp002 OSM cross-check"},
    )
    with urllib.request.urlopen(req, timeout=180) as res:
        payload = json.loads(res.read().decode("utf-8"))
    archive = {
        "retrieved": date.today().isoformat(),
        "endpoint": OVERPASS_URL,
        "query": OVERPASS_QUERY,
        "bbox": KITAGI_BBOX,
        "elements": payload.get("elements", []),
    }
    OSM_ARCHIVE.write_text(
        json.dumps(archive, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    return archive


def load_osm(refresh: bool) -> dict:
    if refresh or not OSM_ARCHIVE.exists():
        return fetch_osm()
    return json.loads(OSM_ARCHIVE.read_text(encoding="utf-8"))


def element_geometry(element: dict):
    """Overpass 要素を shapely ジオメトリへ変換する（緯度経度）。"""
    if element["type"] == "node" and "lat" in element:
        return Point(element["lon"], element["lat"])
    coords = [(p["lon"], p["lat"]) for p in element.get("geometry", []) if "lon" in p]
    if len(coords) >= 4 and coords[0] == coords[-1]:
        poly = Polygon(coords)
        return poly if poly.is_valid else poly.buffer(0)
    if len(coords) >= 2:
        return LineString(coords)
    if coords:
        return Point(coords[0])
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Overpass から再取得する")
    args = parser.parse_args()

    archive = load_osm(args.refresh)
    to_utm = Transformer.from_crs("EPSG:4326", UTM_CRS, always_xy=True).transform

    osm = []
    for element in archive["elements"]:
        geom = element_geometry(element)
        if geom is None:
            continue
        osm.append({
            "geom": shapely_transform(to_utm, geom),
            "tags": element.get("tags", {}),
            "timestamp": element.get("timestamp", ""),
        })
    detections = [
        {"geom": shapely_transform(to_utm, shape(f["geometry"])),
         "area_m2": f["properties"]["area_m2"]}
        for f in json.loads(GEOJSON_PATH.read_text(encoding="utf-8"))["features"]
    ]

    def nearest_detection(o) -> tuple[float, float]:
        return min((o["geom"].distance(d["geom"]), d["area_m2"]) for d in detections)

    def nearest_osm(d) -> float:
        return min(d["geom"].distance(o["geom"]) for o in osm)

    named = [o for o in osm if o["tags"].get("name")]
    quarry_named = [o for o in named if o["tags"].get("landuse") == "quarry"]
    other_named = [o for o in named if o not in quarry_named]

    lines: list[str] = []
    out = lines.append
    out("# 検出ポリゴンと OpenStreetMap 地物の照合記録（exp002 / 北木島）")
    out("")
    out(f"- OSM 取得日: **{archive['retrieved']}**（Overpass API `out geom meta`、保存応答: `{OSM_ARCHIVE.name}`）")
    out(f"- 検出ポリゴン: `{GEOJSON_PATH.name}`（{len(detections)} 件、夏季 2025-08-02）")
    out(f"- 照合範囲: バウンディングボックス {KITAGI_BBOX}")
    out(f"- **距離の定義**: 地物形状を {UTM_CRS}（UTM 53N）へ投影した**形状間距離**。"
        "重なっている場合は 0 m。中心点・重心による近似は距離を過大評価するため使わない")
    out("")
    out("**これは精度検証ではない。** OSM はコミュニティ寄稿データであり正解データではない。"
        "重なりは独立した傍証であり、近傍地物の不在は「OSM 未登録」か「誤検出」のいずれかで、"
        "状態は未決着である。適合率・再現率は算出していない。")
    out("")

    geom_kinds = collections.Counter(o["geom"].geom_type for o in osm)
    overlap_osm = sum(1 for o in osm if nearest_detection(o)[0] == 0)
    out("## 集計")
    out("")
    out("| 指標 | 値 |")
    out("|---|---:|")
    out(f"| OSM 地物数（water / quarry タグ） | {len(osm)} |")
    out(f"| 形状の種類 | {', '.join(f'{k} {v}' for k, v in sorted(geom_kinds.items()))} |")
    out(f"| うち名前付き | {len(named)} |")
    out(f"| うち名前付きで `landuse=quarry` | **{len(quarry_named)}** |")
    out(f"| **OSM 地物が検出ポリゴンと重なる（0 m）** | **{overlap_osm} / {len(osm)}** |")
    for thr in THRESHOLDS_M:
        n = sum(1 for o in osm if nearest_detection(o)[0] <= thr)
        out(f"| OSM 地物に検出ポリゴンが {thr} m 以内 | {n} / {len(osm)} |")
    for thr in THRESHOLDS_M:
        n = sum(1 for d in detections if nearest_osm(d) <= thr)
        out(f"| 検出ポリゴンに OSM 地物が {thr} m 以内 | {n} / {len(detections)} |")
    unresolved = sum(1 for d in detections if nearest_osm(d) > PRIMARY_THRESHOLD_M)
    out(f"| **OSM に近傍地物のない検出（{PRIMARY_THRESHOLD_M} m 超）** | **{unresolved} / {len(detections)}** |")
    out("")
    out(f"主指標は「重なり（0 m）」とする。{PRIMARY_THRESHOLD_M} m は探索的な近傍判定の閾値であり、"
        "10 m グリッドの位置精度と OSM の描画精度の双方に幅があることを踏まえた便宜的な値である。"
        "上の感度表のとおり、閾値を変えると件数は変わる。")
    out("")

    out("## 名前付きの採石場・丁場跡地物（`landuse=quarry`）")
    out("")
    out("| OSM 地物 | 最近傍検出との距離 | 重なった検出の面積 | 最終編集日 |")
    out("|---|---:|---:|---|")
    for o in sorted(quarry_named, key=lambda o: o["tags"]["name"]):
        dist, area = nearest_detection(o)
        out(f"| {o['tags']['name']} | {dist:.1f} m | {area:,.0f} m² | {o['timestamp'][:10]} |")
    out("")
    n_overlap_q = sum(1 for o in quarry_named if nearest_detection(o)[0] == 0)
    out(f"名前付きの `landuse=quarry` 地物 {len(quarry_named)} 件のうち **{n_overlap_q} 件**が"
        "検出ポリゴンと重なっている。")
    out("")

    out("## その他の名前付き地物")
    out("")
    out("| OSM 地物 | 主なタグ | 最近傍検出との距離 | 面積 |")
    out("|---|---|---:|---:|")
    for o in sorted(other_named, key=lambda o: o["tags"]["name"]):
        dist, area = nearest_detection(o)
        tags = " ".join(f"`{k}={o['tags'][k]}`" for k in ("natural", "water", "landuse") if k in o["tags"])
        out(f"| {o['tags']['name']} | {tags} | {dist:.1f} m | {area:,.0f} m² |")
    out("")
    out("`water=reservoir` の地物が検出ポリゴンの近傍にあることは、報告書 5.4 が挙げる"
        "「人工ため池・貯水施設の誤検出」の交絡例にあたる。誤検出と断定はしていない。")
    out("")

    out("## OSM 地物の最終編集日")
    out("")
    out("| 最終編集日 | 件数 |")
    out("|---|---:|")
    edits = collections.Counter(o["timestamp"][:10] for o in osm)
    for day, n in sorted(edits.items()):
        out(f"| {day} | {n} |")
    out("")
    out("2025-02-28〜03-02 に編集された地物が集中しており、2025年3月1〜2日に島で開催された"
        "コミュニティのマッピングイベントの時期と一致する。2026-03-20 の編集は、著者が参加した"
        "「北木島ドローン・マッピングパーティ 2026」（2026年3月20〜21日）当日にあたる。"
        "編集者名は記載しない。")
    out("")

    out("## 「北木の桂林」の位置")
    out("")
    keirin = next((o for o in osm if "桂林" in (o["tags"].get("name") or "")), None)
    if keirin:
        dist, area = nearest_detection(keirin)
        rel = "重なっている" if dist == 0 else f"{dist:.1f} m 離れている"
        out(f"OSM の「{keirin['tags']['name']}」は島北部にあり、面積 {area:,.0f} m² の検出ポリゴン"
            f"（本解析の最大水域）と{rel}。")
        out("")
        out("レポート 5.3 は当初、南東部の 6,521 m² ポリゴンが「北木の桂林」に相当する可能性を"
            "述べていたが、OSM の位置情報はこれと整合しない。南東部のポリゴン近傍には OSM 地物が"
            "ない。ただし OSM の名称・位置もコミュニティ寄稿であり、現地での位置確認（GPS・撮影"
            "方向・撮影時刻の記録）までは**有力な現地確認候補**と述べるにとどめる。")
    out("")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OSM 地物 {len(osm)} 件（名前付き {len(named)}、うち quarry {len(quarry_named)}）")
    print(f"重なり: {overlap_osm}/{len(osm)}  近傍地物なし（{PRIMARY_THRESHOLD_M}m超）: {unresolved}/{len(detections)}")
    print(f"名前付き quarry の重なり: {n_overlap_q}/{len(quarry_named)}")
    print(f"記録: {REPORT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
