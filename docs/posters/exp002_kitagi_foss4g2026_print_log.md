# Visipri Print Log — FOSS4G Hiroshima 2026 Kitagi Island Poster

## Preliminary production baseline

- Product: A0 academic poster, portrait.
- Finished size: 841 × 1189 mm.
- Artwork: English, one-page PDF.
- Preliminary bleed: 3 mm on each side when artwork reaches the trim edge.
- Preliminary color requirement: CMYK preferred/required depending on the selected product; confirm at order time.
- Preliminary resolution guidance: 300 dpi recommended by the public PDF guide; poster raster assets target at least 150 effective dpi and preferably 200 dpi or higher at final placement size.
- Font handling: embed fonts or outline text in the final PDF.

## Sources checked

- A0 product page: https://visipri.com/gakkai/gakkai_poster_a0.php
- PDF data guide: https://visipri.com/dataguide/pdf/
- Academic poster data guide: https://visipri.com/gakkai/info-2-nyukou.php
- FOSS4G poster requirements: https://2026.foss4g.org/ja/program-schedule/poster-session/

## Task 3 制作記録（初稿、2026-08-14）

### 成果物

- 編集可能ソース: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg`（`scripts/build_exp002_poster_svg.py` が決定的に生成）
- 印刷用PDF: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf`
- レビュー用PNG: `docs/posters/exp002_kitagi_quarry_foss4g2026_poster_preview.png`（2,830 × 4,000 px）
- 図版: `docs/posters/figures/exp002/`（`scripts/generate_exp002_poster_figures.py` が生成）

### 生成コマンド

```bash
uv run python scripts/generate_exp002_poster_figures.py   # 図版（Sentinel-2再取得+検証つき）
uv run python scripts/build_exp002_poster_svg.py          # SVG組版
rsvg-convert -f pdf -o docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf \
    docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg
rsvg-convert -f png -h 4000 -o docs/posters/exp002_kitagi_quarry_foss4g2026_poster_preview.png \
    docs/posters/exp002_kitagi_quarry_foss4g2026_poster.svg
uv run python docs/posters/validate_exp002_kitagi_quarry_foss4g2026_poster.py  # 検証
```

### ツールバージョン

- rsvg-convert 2.61.1（librsvg / cairo, Homebrew）
- poppler 25.08.0（pdfinfo / pdffonts）
- uv 0.5.21, Python 3.11.11
- matplotlib 3.10.8, rasterio 1.4.4, numpy 2.4.3, shapely 2.1.2, contextily 1.7.0, pyproj 3.7.2, Pillow 12.1.1

### PDF 技術情報

- ページ: 1ページ、841 × 1189 mm（2383.94 × 3370.39 pt、pdfinfo で A0 と判定）、PDF 1.7
- フォント: Helvetica Neue（macOS システム TTC）。cairo により TrueType / CID TrueType サブセットとして全埋め込み。一部の記号グリフ（≥・−・• 等）は cairo が生成する Type 3 フォントとして埋め込み（表示は正常。PDF/X が必要になった場合は要変換 — 発注時に確認）
- カラーモード: RGB（rsvg-convert は CMYK 出力非対応）。ビジプリの製品別要件で CMYK 必須の場合は発注前に変換方法を確定する（未解決事項として Issue #6 に記載）
- 塗り足し: なし。端まで届くアートワークを使わない設計とし、本文・図版はトリム端から 15 mm 以上内側に配置（余白 18 mm）
- 検証: `validate_exp002_kitagi_quarry_foss4g2026_poster.py` 全チェック合格（必須文字列・参照画像・ページサイズ・フォント埋め込み・プレビュー寸法）。macOS Quartz（sips）でも開けることを確認

### 図版の配置時実効解像度（列幅 260 mm 配置時）

| 図版 | ピクセル | 実効解像度 |
|---|---|---|
| poster_f1_study_area.png | 2259 × 1348 | 220 dpi |
| poster_f3_summer_map.png | 2677 × 2729 | 261 dpi |
| poster_f4_index_panels.png | 2654 × 2543 | 259 dpi |
| poster_f5_truecolor_water.png | 3207 × 1749 | 313 dpi |
| poster_f6_field_photos.jpg | 3010 × 1990 | 294 dpi |
| poster_qr_repo.png (42 mm) | 444 × 444 | 269 dpi |

全図版が最低 150 dpi・目標 200 dpi を満たす。衛星画像パネルの原データ解像度は Sentinel-2 の 10 m（ポスター上に限界として明記）。

## Order-specific confirmation — complete before design export

- [ ] Selected Visipri product and paper/finish:
- [ ] Exact accepted file format and PDF/PDF-X version:
- [ ] Finished size and bleed/trim-mark requirement:
- [ ] CMYK/RGB policy:
- [ ] Maximum file size:
- [ ] Font embedding/outline requirement:
- [ ] Image-resolution requirement:
- [ ] Proofing option:
- [ ] Confirmation date and source URL:

## Order and inspection

- [ ] Order date:
- [ ] Order number:
- [ ] Quantity:
- [ ] Delivery address:
- [ ] Expected delivery date:
- [ ] Actual delivery date:
- [ ] Physical inspection result:
- [ ] Defects or corrective action:
