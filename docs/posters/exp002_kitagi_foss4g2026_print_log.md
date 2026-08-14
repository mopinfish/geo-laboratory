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

## Task 5 修正記録・ビジプリ入稿仕様確認（2026-08-14）

### ビジプリ公開ガイドの確認結果（確認日 2026-08-14）

| 項目 | 確認結果 | 出典 |
|---|---|---|
| RGB入稿の可否 | 可。ただし「印刷時にCMYKに変換される為、色味が変わる可能性」と明記。CMYK推奨 | PDFデータガイド |
| CMYK必須か | 学会ポスター入稿ガイドは「RGBではなくCMYKカラーモードで作成する必要」と記載（推奨〜必須の表現揺れあり）。**発注時に選択製品で最終確認** | 学会ポスター入稿ガイド |
| PDFバージョン | 記載なし（制限の明示なし。PDF 1.6/1.7 とも受領実績の範囲と判断、発注時に確認） | 両ガイド |
| PDF/X指定 | 記載なし | 両ガイド |
| Type 3フォントの可否 | 記載なし（禁止の明示なし。発注時に確認） | 両ガイド |
| フォント | 埋め込みまたはアウトライン化が必要 → **全フォント埋め込み済み** | 両ガイド |
| 塗り足し・トンボ | 塗り足し上下左右3mm（端まで届くアートワークの場合）。本ポスターは端に何も配置しない設計（外周余白18mm）のため該当せず。トンボは「トンボ付きPDFの場合」のみ言及 → 付けない | PDFデータガイド |
| ファイル容量上限 | 記載なし（発注時に確認） | 両ガイド |
| 推奨解像度 | 画像150〜300dpi目安、300dpi以上推奨 → **全図版 230〜313dpi で適合** | PDFデータガイド |
| 入稿形式 | PDF可（PowerPoint作成時もPDF化して入稿） | A0製品ページ |
| A0製品 | 841×1189mm。半光沢紙ほか。激安便3日/通常便当日/特急便3時間 | A0製品ページ |

確認URL: https://visipri.com/dataguide/pdf/ 、https://visipri.com/gakkai/info-2-nyukou.php 、https://visipri.com/gakkai/gakkai_poster_a0.php

### CMYK変換手順（再現可能・Codex再レビュー用）

RGB版 `exp002_kitagi_quarry_foss4g2026_poster.pdf` から Ghostscript 10.07.1 で CMYK 版を生成:

```bash
gs -o docs/posters/exp002_kitagi_quarry_foss4g2026_poster_cmyk.pdf \
   -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress \
   -sColorConversionStrategy=CMYK -dProcessColorModel=/DeviceCMYK \
   -dCompatibilityLevel=1.6 -dEmbedAllFonts=true \
   docs/posters/exp002_kitagi_quarry_foss4g2026_poster.pdf
```

- 変換後検証: 1ページ・A0（2383.94 × 3370.39 pt）維持、PDF 1.6、フォント全埋め込み維持、全画像 CMYK 化（`pdfimages -list` で確認、QRのみgray）、画像解像度 230〜294 ppi 維持、9.7 MB
- どちらのPDFを入稿するか（RGB版 or CMYK版）は、発注時の製品別確認と Codex 最終承認で決定する

### Task 5 修正サマリ

- B1: 春季113件のプロベナンス → レポート4.1に追記・5.4に限界追加、ポスター結果タイル直下に注記（113は維持）
- M1: F3 をタイル不使用のシーン由来陸域シルエット地図に変更（英語のみ）。F1 は目視検証の結果、英語版タイルで日本語ラベルなしを確認（パネル別クロップで確認済み）
- M2: 手法ボックスを「Sentinel-2 L2A; 10 m analysis grid; B11 SWIR resampled from 20 m」に変更、F4キャプションとデータ節にリサンプリングを明記
- M3: 図版内部文字を配置後18pt以上に調整（F1: 15–16pt×1.22、F3: 18pt×1.05、F4: 18pt×1.07、F5: 19pt×0.99。カラーバー目盛は −1/0/1 の3点に削減）
- M4: 上記の仕様確認とCMYK変換手順を記録

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
