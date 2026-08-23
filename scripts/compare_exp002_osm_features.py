"""公開済みの検出ポリゴンと OpenStreetMap の水域・採石場地物を照合する。

exp002（北木島丁場水域検出）で公開した夏季145ポリゴン
（docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson）と、
OSM に登録済みの水域・採石場地物を突き合わせ、次を記録する。

- OSM 地物のうち、検出ポリゴンが近傍にあるものの数（= 既知の水域をどれだけ再発見できたか）
- 検出ポリゴンのうち、OSM に対応地物がないものの数（= まだ地図にない候補）
- 名前付き OSM 地物（丁場跡・採石場）と最近傍検出ポリゴンの距離

これは精度検証ではない。OSM はコミュニティ寄稿データであり、正解データではないため、
一致は独立した傍証、不一致は「未登録」か「誤検出」のどちらかを意味する。

OSM は生きたデータベースなので、取得結果を
docs/results/exp002/exp002_osm_water_features.json へ取得日つきで保存し、
既定ではその保存済み応答を使う（--refresh で再取得）。

実行方法:
    uv run python scripts/compare_exp002_osm_features.py            # 保存済み応答を使う
    uv run python scripts/compare_exp002_osm_features.py --refresh  # Overpass から再取得
"""

from __future__ import annotations

import argparse
import json
import math
import urllib.request
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "docs" / "results" / "exp002"
GEOJSON_PATH = RESULTS_DIR / "exp002_kitagi_summer_water_polygons_2025-08-02.geojson"
OSM_ARCHIVE = RESULTS_DIR / "exp002_osm_water_features.json"
REPORT_PATH = RESULTS_DIR / "exp002_osm_comparison.md"

# 解析と同一のバウンディングボックス [west, south, east, north]
KITAGI_BBOX = [133.515, 34.350, 133.570, 34.400]
KITAGI_CENTER_LAT = 34.374

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_QUERY = f"""[out:json][timeout:90];
(
  nwr["natural"="water"]({KITAGI_BBOX[1]},{KITAGI_BBOX[0]},{KITAGI_BBOX[3]},{KITAGI_BBOX[2]});
  nwr["landuse"="quarry"]({KITAGI_BBOX[1]},{KITAGI_BBOX[0]},{KITAGI_BBOX[3]},{KITAGI_BBOX[2]});
  nwr["water"]({KITAGI_BBOX[1]},{KITAGI_BBOX[0]},{KITAGI_BBOX[3]},{KITAGI_BBOX[2]});
);
out tags center;
"""

MATCH_THRESHOLDS_M = (50, 100, 200)


def fetch_osm() -> dict:
    """Overpass API から取得し、取得日つきで保存する。"""
    req = urllib.request.Request(
        OVERPASS_URL,
        data=OVERPASS_QUERY.encode("utf-8"),
        headers={"User-Agent": "geo-laboratory exp002 OSM cross-check"},
    )
    with urllib.request.urlopen(req, timeout=120) as res:
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


def metres(a: tuple[float, float], b: tuple[float, float]) -> float:
    """経緯度差から概算距離（m）。北木島の緯度で経度を補正する。"""
    cos_lat = math.cos(math.radians(KITAGI_CENTER_LAT))
    return math.hypot((a[0] - b[0]) * 111_000 * cos_lat, (a[1] - b[1]) * 111_000)


def polygon_centroid(coords: list) -> tuple[float, float]:
    ring = coords[0]
    return sum(p[0] for p in ring) / len(ring), sum(p[1] for p in ring) / len(ring)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Overpass から再取得する")
    args = parser.parse_args()

    archive = load_osm(args.refresh)
    osm = [
        (e["center"]["lon"], e["center"]["lat"], e.get("tags", {}), e["type"], e["id"])
        for e in archive["elements"]
        if "center" in e
    ]
    features = json.loads(GEOJSON_PATH.read_text(encoding="utf-8"))["features"]
    detections = [
        (polygon_centroid(f["geometry"]["coordinates"]), f["properties"]["area_m2"])
        for f in features
    ]

    lines: list[str] = []
    out = lines.append
    out("# 検出ポリゴンと OpenStreetMap 地物の照合記録（exp002 / 北木島）")
    out("")
    out(f"- OSM 取得日: **{archive['retrieved']}**（Overpass API、保存応答: `{OSM_ARCHIVE.name}`）")
    out(f"- 検出ポリゴン: `{GEOJSON_PATH.name}`（{len(detections)} 件、夏季 2025-08-02）")
    out(f"- 照合範囲: バウンディングボックス {KITAGI_BBOX}")
    out(f"- 距離は OSM 地物の center と検出ポリゴンの重心の概算距離")
    out("")
    out("**これは精度検証ではない。** OSM はコミュニティ寄稿データであり正解データではない。"
        "一致は独立した傍証であり、不一致は「OSM に未登録」か「誤検出」のいずれかを意味する。"
        "適合率・再現率は算出していない。")
    out("")

    named = [(x, y, t) for x, y, t, _, _ in osm if t.get("name")]
    out("## 集計")
    out("")
    out("| 指標 | 値 |")
    out("|---|---:|")
    out(f"| OSM 地物数（water / quarry タグ） | {len(osm)} |")
    out(f"| うち名前付き | {len(named)} |")
    for thr in MATCH_THRESHOLDS_M:
        n = sum(
            1 for x, y, _, _, _ in osm
            if min(metres((x, y), c) for c, _ in detections) <= thr
        )
        out(f"| OSM 地物のうち検出ポリゴンが {thr} m 以内にあるもの | {n} / {len(osm)} |")
    for thr in (50, 100):
        n = sum(
            1 for c, _ in detections
            if min(metres(c, (x, y)) for x, y, _, _, _ in osm) <= thr
        )
        out(f"| 検出ポリゴンのうち OSM 地物が {thr} m 以内にあるもの | {n} / {len(detections)} |")
    unmapped = sum(
        1 for c, _ in detections
        if min(metres(c, (x, y)) for x, y, _, _, _ in osm) > 100
    )
    out(f"| **OSM に対応地物のない検出ポリゴン（100 m 超）** | **{unmapped} / {len(detections)}** |")
    out("")

    out("## 名前付き OSM 地物と最近傍の検出ポリゴン")
    out("")
    out("| OSM 地物 | 座標 | 主なタグ | 最近傍検出との距離 | 該当ポリゴンの面積 |")
    out("|---|---|---|---:|---:|")
    for x, y, t in sorted(named, key=lambda n: n[2].get("name", "")):
        dist, area = min((metres((x, y), c), a) for c, a in detections)
        tags = " ".join(
            f"`{k}={t[k]}`" for k in ("natural", "landuse", "water") if k in t
        )
        out(f"| {t['name']} | {y:.4f}N, {x:.4f}E | {tags} | {dist:.0f} m | {area:,.0f} m² |")
    out("")

    out("## 検出上位5件と最近傍 OSM 地物")
    out("")
    out("| 面積 | 座標 | 最近傍 OSM 地物 | 距離 |")
    out("|---:|---|---|---:|")
    for c, a in sorted(detections, key=lambda d: -d[1])[:5]:
        dist, name = min(
            (metres(c, (x, y)), t.get("name") or "(名前なし)")
            for x, y, t, _, _ in osm
        )
        out(f"| {a:,.0f} m² | {c[1]:.4f}N, {c[0]:.4f}E | {name} | {dist:.0f} m |")
    out("")

    out("## 「北木の桂林」の位置")
    out("")
    keirin = next(
        ((x, y, t) for x, y, t, _, _ in osm if "桂林" in (t.get("name") or "")), None
    )
    if keirin:
        x, y, t = keirin
        dist, area = min((metres((x, y), c), a) for c, a in detections)
        out(f"OSM の「{t['name']}」は **{y:.4f}N, {x:.4f}E（島北部）** にあり、"
            f"最近傍の検出ポリゴン（面積 {area:,.0f} m²）まで **{dist:.0f} m** である。")
        out("")
        out("レポート 5.3 は当初、南東部の 6,521 m² ポリゴンが「北木の桂林」に相当する可能性を"
            "述べていたが、OSM の位置情報はこれと整合しない。南東部のポリゴンには対応する"
            "OSM 地物がない。なお OSM のタグ付けもコミュニティ寄稿であり、確定には現地での"
            "位置確認が必要である。")
    else:
        out("OSM 応答に「桂林」を含む地物が見つからなかった。")
    out("")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OSM 地物: {len(osm)} 件（名前付き {len(named)} 件） / 検出: {len(detections)} 件")
    print(f"OSM に対応地物のない検出: {unmapped} 件")
    print(f"記録: {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"保存応答: {OSM_ARCHIVE.relative_to(PROJECT_ROOT)}（取得日 {archive['retrieved']}）")


if __name__ == "__main__":
    main()
