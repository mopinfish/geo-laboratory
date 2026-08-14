"""FOSS4G Hiroshima 2026 北木島ポスターの A0 SVG を生成する。

docs/posters/exp002_kitagi_quarry_foss4g2026_poster_content.md（内容契約）の
コピー・レイアウト仕様に従い、A0縦（841 × 1189 mm）の1ページ SVG を組む。
テキストの折返しは HelveticaNeue.ttc の実測字幅で計算する。

生成物（コミット対象の編集可能ソース）:
    docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg

エクスポート（このスクリプトでは行わない。コマンドは print で表示）:
    rsvg-convert -f pdf -o docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf \
        docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg
    rsvg-convert -f png -h 4000 -o docs/posters/exp002_kitagi_quarry_foss4g2026_poster_preview.png \
        docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg

実行方法:
    uv run python scripts/build_exp002_poster_svg.py
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSTER_DIR = PROJECT_ROOT / "docs" / "posters"
FIG_DIR = POSTER_DIR / "figures" / "exp002"
OUT_SVG = POSTER_DIR / "exp002_kitagi_quarry_foss4g2026_poster.svg"

# ---------------------------------------------------------------- ページ・グリッド（mm）
PAGE_W, PAGE_H = 841.0, 1189.0
MARGIN = 18.0
GUTTER = 12.0
COL_W = (PAGE_W - 2 * MARGIN - 2 * GUTTER) / 3  # 260.33 mm
COL_X = [MARGIN, MARGIN + COL_W + GUTTER, MARGIN + 2 * (COL_W + GUTTER)]
CONTENT_W = PAGE_W - 2 * MARGIN

FOOTER_RULE_Y = 1090.0  # 契約の「下部95mm予約」を満たす（1189-95=1094 より上）
CONTENT_BOTTOM = FOOTER_RULE_Y - 8.0

# ---------------------------------------------------------------- タイポグラフィ（mm; 1pt = 0.352778mm）
PT = 0.352778
SZ_TITLE = 74 * PT      # 26.1mm ≥72pt
SZ_EVENT = 26 * PT
SZ_AUTHOR = 32 * PT
SZ_TAKEAWAY = 27 * PT
SZ_HEADING = 38 * PT
SZ_BODY = 24.5 * PT     # ≥24pt
SZ_CAPTION = 18.5 * PT  # ≥18pt
SZ_FOOTER = 18.5 * PT
SZ_BIGNUM = 96 * PT
SZ_MIDNUM = 60 * PT

LH_TITLE = SZ_TITLE * 1.18
LH_BODY = SZ_BODY * 1.38
LH_CAPTION = SZ_CAPTION * 1.3
LH_FOOTER = SZ_FOOTER * 1.3

# ---------------------------------------------------------------- 配色（granite/sea パレット）
COL_TEXT = "#2b2b2b"
COL_BLUE = "#0d47a1"
COL_STONE_BG = "#f0ece3"
COL_STONE_LINE = "#8a8375"
COL_MUTED = "#5a564e"

FONT_FAMILY = "Helvetica Neue"
TTC = "/System/Library/Fonts/HelveticaNeue.ttc"
_MEASURE_SCALE = 10.0  # 1mm = 10px で実測
_FONTS = {
    "normal": ImageFont.truetype(TTC, 100, index=0),
    "bold": ImageFont.truetype(TTC, 100, index=1),
    "medium": ImageFont.truetype(TTC, 100, index=10),
}


def text_width_mm(text: str, size_mm: float, weight: str = "normal") -> float:
    """実フォントで文字列幅を測る（mm）。"""
    font = _FONTS[weight]
    return _FONTS[weight].getlength(text) / 100.0 * size_mm


def wrap_text(text: str, width_mm: float, size_mm: float, weight: str = "normal") -> list[str]:
    """幅に収まるよう単語単位で折り返す。ノーブレークスペース（U+00A0）では折り返さない。"""
    words = [w for w in text.split(" ") if w]
    lines: list[str] = []
    cur = ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if text_width_mm(cand, size_mm, weight) <= width_mm or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Svg:
    def __init__(self):
        self.parts: list[str] = []
        self.figures: list[tuple[str, float, int, int]] = []  # (name, w_mm, px_w, px_h)

    def add(self, s: str):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill, stroke=None, stroke_w=0.0, rx=0.0):
        s = f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}"'
        if rx:
            s += f' rx="{rx:.2f}"'
        if stroke:
            s += f' stroke="{stroke}" stroke-width="{stroke_w:.2f}"'
        self.add(s + "/>")

    def line(self, x1, y1, x2, y2, stroke, width):
        self.add(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{stroke}" stroke-width="{width:.2f}"/>'
        )

    def text(self, x, y, s, size, weight="normal", fill=COL_TEXT, anchor="start", spacing=None):
        w = {"normal": "400", "medium": "500", "bold": "700"}[weight]
        extra = f' letter-spacing="{spacing}"' if spacing else ""
        self.add(
            f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT_FAMILY}" '
            f'font-size="{size:.3f}" font-weight="{w}" fill="{fill}" '
            f'text-anchor="{anchor}"{extra}>{escape(s)}</text>'
        )

    def paragraph(self, x, y, text, width_mm, size, lh, weight="normal", fill=COL_TEXT) -> float:
        """折返し段落を描き、次のベースライン開始位置を返す。"""
        for line in wrap_text(text, width_mm, size, weight):
            self.text(x, y, line, size, weight, fill)
            y += lh
        return y

    def bullets(self, x, y, items, width_mm, size, lh, fill=COL_TEXT) -> float:
        indent = 7.0
        for item in items:
            lines = wrap_text(item, width_mm - indent, size)
            self.text(x, y, "•", size, "bold", COL_BLUE)
            for i, line in enumerate(lines):
                self.text(x + indent, y, line, size, "normal", fill)
                y += lh
            y += 1.5
        return y

    def image(self, path: Path, x, y, w_mm) -> float:
        """画像をアスペクト維持で配置し、下端 y を返す。"""
        with Image.open(path) as img:
            px_w, px_h = img.size
        h_mm = w_mm * px_h / px_w
        rel = path.relative_to(POSTER_DIR)
        self.add(
            f'<image x="{x:.2f}" y="{y:.2f}" width="{w_mm:.2f}" height="{h_mm:.2f}" '
            f'xlink:href="{rel.as_posix()}"/>'
        )
        self.figures.append((path.name, w_mm, px_w, px_h))
        return y + h_mm

    def caption(self, x, y, text, width_mm) -> float:
        return self.paragraph(x, y, text, width_mm, SZ_CAPTION, LH_CAPTION, fill=COL_MUTED)

    def heading(self, x, y, text) -> float:
        self.text(x, y, text, SZ_HEADING, "bold", COL_BLUE)
        self.line(x, y + 3.5, x + COL_W, y + 3.5, COL_STONE_LINE, 0.6)
        return y + SZ_HEADING * 0.9 + 6.0

    def callout(self, x, y, number, label, width_mm) -> float:
        """大きな数値 + ラベルのコールアウト。y はブロック上端。次のベースライン y を返す。"""
        num_w = text_width_mm(number, SZ_MIDNUM, "bold") + 7.0
        lh_label = SZ_BODY * 1.3
        lines = wrap_text(label, width_mm - num_w, SZ_BODY, "medium")
        num_base = y + SZ_MIDNUM * 0.75
        self.text(x, num_base, number, SZ_MIDNUM, "bold", COL_BLUE)
        # ラベルは数値の視覚中心に合わせて縦センタリング
        label_h = len(lines) * lh_label
        ly = num_base - SZ_MIDNUM * 0.34 - label_h / 2 + SZ_BODY * 0.85
        for line in lines:
            self.text(x + num_w, ly, line, SZ_BODY, "medium")
            ly += lh_label
        bottom = max(num_base + SZ_MIDNUM * 0.05, ly - lh_label + SZ_BODY * 0.35)
        return bottom + LH_BODY


def build() -> None:
    svg = Svg()
    svg.add(
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{PAGE_W:.0f}mm" height="{PAGE_H:.0f}mm" viewBox="0 0 {PAGE_W:.0f} {PAGE_H:.0f}">'
    )
    svg.rect(0, 0, PAGE_W, PAGE_H, "#ffffff")

    # ---------------------------------------------------------- ヘッダ
    y = 24.0
    svg.text(MARGIN, y, "FOSS4G Hiroshima 2026 — Poster Session", SZ_EVENT, "medium", COL_BLUE)
    svg.text(PAGE_W - MARGIN, y, "Sakura Lounge · September 1–3, 2026", SZ_EVENT, "normal", COL_MUTED, anchor="end")

    y = 46.0
    title = (
        "Detecting Quarry Pond Remnants on a Japanese Island Heritage Site "
        "Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools"
    )
    for line in wrap_text(title, CONTENT_W, SZ_TITLE, "bold"):
        svg.text(MARGIN, y, line, SZ_TITLE, "bold")
        y += LH_TITLE

    y += 2.0
    svg.text(MARGIN, y, "Noboru Otsuka — Geolonia Inc.", SZ_AUTHOR, "medium")
    y += SZ_AUTHOR * 0.6

    # テイクアウェイ帯
    band_y = y + 6.0
    takeaway = (
        "Open-source Sentinel-2 processing revealed 113 spring and 145 summer intra-island "
        "water polygons on Kitagi Island; their distribution is consistent with historical "
        "quarrying patterns, while individual quarry-pond identities still require field validation."
    )
    tw_lines = wrap_text(takeaway, CONTENT_W - 16, SZ_TAKEAWAY, "medium")
    band_h = len(tw_lines) * SZ_TAKEAWAY * 1.35 + 10.0
    svg.rect(MARGIN, band_y, CONTENT_W, band_h, COL_STONE_BG, rx=2.0)
    svg.rect(MARGIN, band_y, 3.0, band_h, COL_BLUE)
    ty = band_y + 8.0 + SZ_TAKEAWAY * 0.65
    for line in tw_lines:
        svg.text(MARGIN + 10, ty, line, SZ_TAKEAWAY, "medium")
        ty += SZ_TAKEAWAY * 1.35

    content_top = band_y + band_h + 14.0

    # ---------------------------------------------------------- 左カラム
    x = COL_X[0]
    y = content_top + SZ_HEADING * 0.8
    y = svg.heading(x, y, "1 · Background and heritage")
    y += SZ_BODY * 0.9
    y = svg.paragraph(
        x, y,
        "Kitagi Island (Kitagi-shima), in Kasaoka City, Okayama Prefecture, is a "
        "granite-quarrying island in Japan’s Seto Inland Sea. Quarrying here extends "
        "back to the early seventeenth century.",
        COL_W, SZ_BODY, LH_BODY,
    )
    # 127 コールアウト
    y += 2.0
    y = svg.callout(x, y, "127", "active quarry sites (dojo) recorded at the 1957 peak", COL_W)
    y = svg.paragraph(
        x, y,
        "As the industry declined, abandoned excavations filled with rainwater and "
        "groundwater, forming isolated ponds enclosed by steep granite walls. In 2019 "
        "the island’s stone culture became part of Japan’s national heritage under the "
        "“Stone Islands of Setouchi” program. No systematic spatial inventory of these "
        "quarry pond remnants has been published.",
        COL_W, SZ_BODY, LH_BODY,
    )

    y += 8.0 + SZ_HEADING * 0.8
    y = svg.heading(x, y, "2 · Research question")
    y += SZ_BODY * 0.9
    y = svg.paragraph(
        x, y,
        "Can open satellite imagery and reproducible open-source tools map water bodies "
        "associated with former quarry sites, and do their spatial patterns correspond "
        "to the island’s quarrying history?",
        COL_W, SZ_BODY, LH_BODY,
    )

    y += 4.0
    y = svg.image(FIG_DIR / "poster_f1_study_area.png", x, y, COL_W) + LH_CAPTION
    y = svg.caption(
        x, y,
        "Study area: Kitagi Island, Kasaoka City, Okayama Prefecture. "
        "Basemap: GSI Tiles (English), Geospatial Information Authority of Japan.",
        COL_W,
    )

    y += 6.0 + SZ_HEADING * 0.8
    y = svg.heading(x, y, "3 · Data and study area")
    y += SZ_BODY * 0.9
    y = svg.bullets(
        x, y,
        [
            "Sentinel-2 L2A imagery accessed through the Microsoft Planetary Computer STAC API",
            "Spring scene 2025-03-23 (cloud cover 0.0%); summer scene 2025-08-02 (cloud cover 0.7%)",
            "10 m analysis grid: B02/B03/B04/B08 are native 10 m; B11 (SWIR) is resampled from its "
            "native 20 m. Mixed pixels limit very small water bodies",
            "Minimum reported polygon area: 100 m²",
        ],
        COL_W, SZ_BODY, LH_BODY,
    )

    y += 4.0
    y = svg.image(FIG_DIR / "poster_f6_field_photos.jpg", x, y, COL_W) + LH_CAPTION
    y = svg.caption(
        x, y,
        "Water-filled quarry remnants (“Choba lake”) enclosed by granite walls, Kitagi Island. "
        "Photos: Noboru Otsuka.",
        COL_W,
    )
    left_bottom = y

    # ---------------------------------------------------------- 中央カラム
    x = COL_X[1]
    y = content_top + SZ_HEADING * 0.8
    y = svg.heading(x, y, "4 · Method — open-source pipeline")
    y += SZ_BODY * 0.9

    steps = [
        "Sentinel-2 L2A; 10 m analysis grid; B11 SWIR resampled from 20 m",
        "STAC search and band access — Microsoft Planetary Computer",
        "Water index union: NDWI + MNDWI",
        "NDVI vegetation mask, then water polygon extraction (≥100 m²)",
    ]
    box_w = COL_W
    for i, step in enumerate(steps):
        lines = wrap_text(step, box_w - 14, SZ_BODY, "medium")
        box_h = len(lines) * SZ_BODY * 1.3 + 7.5
        svg.rect(x, y, box_w, box_h, "#ffffff", stroke=COL_BLUE, stroke_w=0.9, rx=2.0)
        ly = y + 5.5 + SZ_BODY * 0.72
        for line in lines:
            svg.text(x + 7, ly, line, SZ_BODY, "medium")
            ly += SZ_BODY * 1.3
        y += box_h
        if i < len(steps) - 1:
            ax = x + box_w / 2
            svg.line(ax, y + 1.0, ax, y + 7.0, COL_BLUE, 1.2)
            svg.add(
                f'<path d="M {ax - 2.6:.2f} {y + 6.2:.2f} L {ax + 2.6:.2f} {y + 6.2:.2f} '
                f'L {ax:.2f} {y + 10.0:.2f} Z" fill="{COL_BLUE}"/>'
            )
            y += 11.0

    y += 14.0
    for formula in (
        "NDWI  = (Green − NIR) / (Green + NIR)",
        "MNDWI = (Green − SWIR) / (Green + SWIR)",
        "NDVI  = (NIR − Red) / (NIR + Red)",
    ):
        svg.text(x, y, formula, SZ_BODY, "normal")
        y += LH_BODY

    y += 3.0
    cond = "(NDWI > −0.2  OR  MNDWI > −0.1)  AND NOT  (NDVI > 0.3)"
    cond_h = SZ_BODY * 1.3 + 8.0
    svg.rect(x, y, COL_W, cond_h, COL_STONE_BG, stroke=COL_BLUE, stroke_w=1.0, rx=2.0)
    svg.text(x + COL_W / 2, y + cond_h / 2 + SZ_BODY * 0.36, cond, SZ_BODY, "bold", COL_BLUE, anchor="middle")
    y += cond_h + LH_BODY

    y = svg.paragraph(
        x, y,
        "The union condition favors sensitivity to small water bodies affected by spectral "
        "mixing at 10 m resolution, while the NDVI mask excludes vegetation-like pixels.",
        COL_W, SZ_BODY, LH_BODY,
    )

    y += 4.0
    y = svg.image(FIG_DIR / "poster_f4_index_panels.png", x, y, COL_W) + LH_CAPTION
    y = svg.caption(
        x, y,
        "NDWI, MNDWI, NDVI and the final mask (blue = water, green = vegetation, gray = other), "
        "Sentinel-2 L2A, 2025-08-02. B11 (SWIR, native 20 m) resampled to the 10 m grid. "
        "Contains modified Copernicus Sentinel data [2025].",
        COL_W,
    )

    y += 6.0
    # 10 m コールアウト + 9px の確定文
    y = svg.callout(x, y, "10 m", "Sentinel-2 spatial resolution — the key detection limit", COL_W)
    y = svg.paragraph(
        x, y,
        "The summer NDVI mask excluded only 9 pixels, indicating limited overlap between the "
        "detected water candidates and vegetation zones in this granite-dominated landscape.",
        COL_W, SZ_BODY, LH_BODY,
    )

    y += 4.0
    y = svg.image(FIG_DIR / "poster_f5_truecolor_water.png", x, y, COL_W) + LH_CAPTION
    y = svg.caption(
        x, y,
        "Detected water candidates highlighted in blue; not individual quarry validation. "
        "Contains modified Copernicus Sentinel data [2025].",
        COL_W,
    )
    center_bottom = y

    # ---------------------------------------------------------- 右カラム
    x = COL_X[2]
    y = content_top + SZ_HEADING * 0.8
    y = svg.heading(x, y, "5 · Results — seasonal detection")
    y += SZ_BODY * 0.9

    svg.text(x, y, "Detected intra-island water polygons ≥100 m²", SZ_BODY, "medium")
    y += SZ_BODY * 0.7

    tile_w = (COL_W - 8) / 2
    tile_h = SZ_BIGNUM * 1.05 + SZ_CAPTION * 2.9 + 8.0
    for i, (num, label1, label2) in enumerate(
        (("113", "Spring", "2025-03-23"), ("145", "Summer", "2025-08-02"))
    ):
        tx = x + i * (tile_w + 8)
        svg.rect(tx, y, tile_w, tile_h, COL_STONE_BG, rx=2.0)
        svg.text(tx + tile_w / 2, y + SZ_BIGNUM * 0.95, num, SZ_BIGNUM, "bold", COL_BLUE, anchor="middle")
        svg.text(tx + tile_w / 2, y + SZ_BIGNUM * 1.05 + SZ_CAPTION * 1.1, f"{label1} · {label2}",
                 SZ_CAPTION * 1.15, "medium", COL_TEXT, anchor="middle")
        svg.text(tx + tile_w / 2, y + SZ_BIGNUM * 1.05 + SZ_CAPTION * 2.5, "water polygons ≥100 m²",
                 SZ_CAPTION, "normal", COL_MUTED, anchor="middle")
    y += tile_h + LH_CAPTION
    # 春季113件のプロベナンス注記（Task 4 B1 対応: 確定値は維持しつつ再現状況を明示）
    y = svg.caption(
        x, y,
        "Spring count: 113 reported polygons; the exact historical run configuration "
        "is not preserved in the current repository.",
        COL_W,
    )
    y += 4.0

    y = svg.image(FIG_DIR / "poster_f3_summer_map.png", x, y, COL_W) + LH_CAPTION
    y = svg.caption(
        x, y,
        "Summer result: 145 detected intra-island water polygons (blue) on a land/sea outline "
        "derived from the same Sentinel-2 scene. Contains modified Copernicus Sentinel data [2025].",
        COL_W,
    )

    y += 5.0
    y = svg.paragraph(
        x, y,
        "Summer imagery detected 145 intra-island water polygons. The detections were "
        "concentrated in northern, southeastern, central, and western parts of the island, "
        "a pattern consistent with historical quarrying records.",
        COL_W, SZ_BODY, LH_BODY,
    )

    # 注意書きボックス（確定文言）
    y += 2.0
    caution = (
        "These are detected water polygons, not individually field-confirmed quarry ponds. "
        "Natural ponds, reservoirs, shadows, and other false positives may remain."
    )
    c_lines = wrap_text(caution, COL_W - 14, SZ_BODY, "medium")
    c_h = len(c_lines) * LH_BODY + 9.0
    svg.rect(x, y, COL_W, c_h, COL_STONE_BG, stroke=COL_STONE_LINE, stroke_w=0.9, rx=2.0)
    cy = y + 7.0 + SZ_BODY * 0.72
    for line in c_lines:
        svg.text(x + 7, cy, line, SZ_BODY, "medium")
        cy += LH_BODY
    y += c_h + 8.0

    y += 6.0 + SZ_HEADING * 0.8
    y = svg.heading(x, y, "6 · Interpretation and limitations")
    y += SZ_BODY * 0.9
    y = svg.bullets(
        x, y,
        [
            "The count and distribution of detected polygons are consistent with the historical "
            "quarrying context; the 145-to-127 comparison is a scale comparison, not a one-to-one match.",
            "Sentinel-2’s 10 m resolution causes spectral mixing for narrow or small ponds.",
            "Negative thresholds improve sensitivity but can add false positives from dark rock or shadows.",
            "Individual quarry-pond identity and accuracy metrics require field validation.",
            "Season changes which water bodies are most detectable; spring and summer results are "
            "not interchangeable observations.",
        ],
        COL_W, SZ_BODY, LH_BODY,
    )
    right_bottom = y

    # ---------------------------------------------------------- フッタ
    svg.line(MARGIN, FOOTER_RULE_Y, PAGE_W - MARGIN, FOOTER_RULE_Y, COL_STONE_LINE, 0.8)
    fy0 = FOOTER_RULE_Y + 10.0

    # ブロックA: 結論と再利用
    ax_, aw = MARGIN, 262.0
    yA = fy0
    svg.text(ax_, yA, "Conclusion and reuse", SZ_FOOTER * 1.15, "bold", COL_BLUE)
    yA += LH_FOOTER * 1.25
    yA = svg.paragraph(
        ax_, yA,
        "A lightweight, reproducible workflow can provide a first spatial inventory of "
        "quarry-pond candidates and a practical base layer for field validation and heritage "
        "documentation. Results are exported as GeoJSON and GeoTIFF. The workflow uses "
        "open-source Python libraries — rasterio, numpy, shapely, pystac-client, "
        "planetary-computer, and folium — and could be extended to other quarried islands "
        "in the Seto Inland Sea.",
        aw, SZ_FOOTER, LH_FOOTER,
    )

    # ブロックB: 参考文献
    bx, bw = MARGIN + 274.0, 278.0
    yB = fy0
    svg.text(bx, yB, "References", SZ_FOOTER * 1.15, "bold", COL_BLUE)
    yB += LH_FOOTER * 1.25
    refs = [
        "McFeeters, S. K. (1996) The use of the Normalized Difference Water Index (NDWI) in the "
        "delineation of open water features. Int. J. Remote Sensing, 17(7), 1425–1432.",
        "Xu, H. (2006) Modification of normalised difference water index (NDWI) to enhance open water "
        "features in remotely sensed imagery. Int. J. Remote Sensing, 27(14), 3025–3033.",
        "Du, Y. et al. (2016) Water bodies’ mapping from Sentinel-2 imagery with MNDWI at 10-m spatial "
        "resolution. Remote Sensing, 8(4), 354.",
        "Japan Heritage story “Islands of stone”: stone-islands.jp/en/story/",
    ]
    for ref in refs:
        yB = svg.paragraph(bx, yB, ref, bw, SZ_FOOTER, LH_FOOTER)
        yB += 1.0

    # ブロックC: 帰属表示・ライセンス・QR
    cx_, cw = MARGIN + 564.0, CONTENT_W - 564.0  # 241mm
    qr_w = 42.0
    yC = fy0
    svg.text(cx_, yC, "Attribution and license", SZ_FOOTER * 1.15, "bold", COL_BLUE)
    yC += LH_FOOTER * 1.25
    text_w = cw - qr_w - 10.0
    yC = svg.paragraph(
        cx_, yC,
        "Contains modified Copernicus Sentinel data [2025]. Sentinel-2 L2A data accessed through "
        "Microsoft Planetary Computer STAC API. Analysis uses rasterio, numpy, shapely, "
        "pystac-client, planetary-computer, and folium. Conference contribution licensed CC BY 4.0.",
        text_w, SZ_FOOTER, LH_FOOTER,
    )
    yC = svg.paragraph(
        cx_, yC,
        "Basemaps: GSI Tiles, Geospatial Information Authority of Japan.",
        text_w, SZ_FOOTER, LH_FOOTER, fill=COL_MUTED,
    )
    yC = svg.paragraph(
        cx_, yC,
        "Code and data: github.com/mopinfish/geo-laboratory",
        text_w, SZ_FOOTER, LH_FOOTER, fill=COL_MUTED,
    )
    svg.image(FIG_DIR / "poster_qr_repo.png", cx_ + cw - qr_w, fy0 - 3.0, qr_w)

    svg.add("</svg>")

    OUT_SVG.write_text("\n".join(svg.parts) + "\n", encoding="utf-8")
    print(f"written: {OUT_SVG.relative_to(PROJECT_ROOT)}")

    # ---------------------------------------------------------- 検証出力
    print("\n--- カラム下端（content bottom 上限 {:.0f}mm）---".format(CONTENT_BOTTOM))
    for name, bottom in (("left", left_bottom), ("center", center_bottom), ("right", right_bottom)):
        status = "OK" if bottom <= CONTENT_BOTTOM else "OVERFLOW!"
        print(f"  {name:6s}: {bottom:7.1f} mm  {status}")

    print("\n--- 図版の配置時実効解像度 ---")
    for name, w_mm, px_w, px_h in svg.figures:
        dpi = px_w / (w_mm / 25.4)
        flag = "OK" if dpi >= 150 else "LOW!"
        target = "" if dpi >= 200 else " (<200 target)"
        print(f"  {name:32s} {px_w}x{px_h}px @ {w_mm:.0f}mm → {dpi:5.0f} dpi {flag}{target}")

    print("\nエクスポートコマンド:")
    print("  rsvg-convert -f pdf -o docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf \\")
    print("      docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg")
    print("  rsvg-convert -f png -h 4000 -o docs/posters/exp002_kitagi_quarry_foss4g2026_poster_preview.png \\")
    print("      docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg")


if __name__ == "__main__":
    build()
