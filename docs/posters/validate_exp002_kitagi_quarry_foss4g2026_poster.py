"""FOSS4G Hiroshima 2026 北木島ポスターの決定的検証。

チェック内容:
1. SVG に必須文字列（タイトル・著者・所属・確定数値・手法名・ライブラリ・
   ライセンス・帰属表示）がすべて含まれる
2. SVG が参照する画像ファイルが存在する
3. PDF が1ページ・A0縦（841 × 1189 mm = 2383.94 × 3370.39 pt）である
4. PDF のフォントがすべて埋め込まれている（pdffonts）
5. プレビュー PNG の長辺が約4,000px である

実行方法:
    uv run python docs/posters/validate_exp002_kitagi_quarry_foss4g2026_poster.py

終了コード 0 = 全チェック合格。
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

POSTER_DIR = Path(__file__).resolve().parent
SVG = POSTER_DIR / "exp002_kitagi_quarry_foss4g2026_poster.svg"
PDF = POSTER_DIR / "exp002_kitagi_quarry_foss4g2026_poster.pdf"
PREVIEW = POSTER_DIR / "exp002_kitagi_quarry_foss4g2026_poster_preview.png"

REQUIRED_STRINGS = [
    # タイトル（3行に折り返されるため断片で確認）
    "Detecting Quarry Pond Remnants on a Japanese Island",
    "Sensing Tools",
    "Noboru Otsuka",
    "Geolonia Inc.",
    "FOSS4G Hiroshima 2026",
    # 確定数値・日付・閾値
    "113",
    "145",
    "127",
    "9 pixels",
    "100 m²",
    "10 m",
    "2025-03-23",
    "2025-08-02",
    "−0.2",
    "−0.1",
    "0.3",
    "1957",
    # 手法・データ・ライブラリ
    "Sentinel-2",
    "Microsoft Planetary Computer STAC API",
    "NDWI",
    "MNDWI",
    "NDVI",
    "GeoJSON",
    "GeoTIFF",
    "rasterio",
    "numpy",
    "shapely",
    "pystac-client",
    "planetary-computer",
    "folium",
    "Seto Inland Sea",
    # ライセンス・帰属表示
    "CC BY 4.0",
    "Contains modified Copernicus Sentinel data [2025]",
    "Geospatial Information Authority of Japan",
    # 過大主張の防止（注意書きの確定文言）
    "not individually",
    "field-confirmed quarry ponds",
    # Task 5 追加要件: B11 リサンプリング明記と春季プロベナンス注記
    "resampled from 20 m",
    "113 reported polygons",
]

failures: list[str] = []


def check(label: str, ok: bool, detail: str = ""):
    mark = "OK " if ok else "NG!"
    print(f"[{mark}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(label)


def main() -> int:
    # 1. 必須文字列（折返しで複数の text 要素に分かれるため、文書順に連結して検索）
    svg_text = SVG.read_text(encoding="utf-8")
    joined = " ".join(re.findall(r">([^<>]+)</text>", svg_text))
    for s in REQUIRED_STRINGS:
        check(f"SVG 必須文字列: {s!r}", s in svg_text or s in joined)

    # 2. 参照画像の存在
    hrefs = re.findall(r'xlink:href="([^"]+)"', svg_text)
    for href in hrefs:
        check(f"参照画像あり: {href}", (POSTER_DIR / href).exists())

    # 3. PDF ページ数・サイズ
    info = subprocess.run(["pdfinfo", str(PDF)], capture_output=True, text=True).stdout
    pages = re.search(r"Pages:\s+(\d+)", info)
    size = re.search(r"Page size:\s+([\d.]+) x ([\d.]+) pts", info)
    check("PDF が1ページ", bool(pages) and pages.group(1) == "1")
    if size:
        w, h = float(size.group(1)), float(size.group(2))
        check("PDF が A0縦 (2383.94 × 3370.39 pt)",
              abs(w - 2383.94) < 1.0 and abs(h - 3370.39) < 1.0, f"{w} x {h} pt")
    else:
        check("PDF ページサイズ取得", False)

    # 4. フォント埋め込み（pdffonts の末尾5列は emb sub uni object-ID gen）
    fonts = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True).stdout
    rows = [ln for ln in fonts.splitlines()[2:] if ln.strip()]
    for ln in rows:
        cols = ln.split()
        emb = cols[-5] if len(cols) >= 5 else "?"
        check(f"フォント埋め込み: {cols[0]}", emb == "yes", f"emb={emb}")
    # 予期しないフォールバックフォントの検出（Helvetica Neue 以外の名前付きフォント）
    named = [ln.split()[0] for ln in rows if not ln.startswith("[none]")]
    unexpected = [n for n in named if "HelveticaNeue" not in n]
    check("フォールバックフォントなし（Helvetica Neue のみ）", not unexpected, str(unexpected))

    # 5. プレビュー PNG 長辺
    from PIL import Image

    with Image.open(PREVIEW) as img:
        long_edge = max(img.size)
    check("プレビュー長辺 ≈ 4000px", 3800 <= long_edge <= 4200, f"{img.size}")

    print()
    if failures:
        print(f"NG: {len(failures)} 件のチェックに失敗")
        return 1
    print("全チェック合格")
    return 0


if __name__ == "__main__":
    sys.exit(main())
