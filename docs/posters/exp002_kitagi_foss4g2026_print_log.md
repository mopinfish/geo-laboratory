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

> **注記（2026-08-23）**: 上表は Task 3 時点の値であり、**Task 5 で図版を再生成したため現行値ではない**。現行の実測値は下記「図版の配置時実効解像度（2026-08-23 実測）」を参照（230〜294 dpi）。

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

## Order-specific confirmation — 公開ページ再確認（2026-08-23、Claude）

- [x] **Selected Visipri product and paper/finish**: A0学会ポスター（仕上がり 841 × 1189 mm）。用紙は半光沢紙（半光沢フォト紙）を基本とし、フォト光沢紙・厚手マット紙・布（防炎クロス）・バックライトフィルム・透明フィルム・トレーシングペーパーも選択可。**用紙の最終選択はユーザー判断**（掲示はピン留めのため半光沢紙で問題なし）
- [x] **Exact accepted file format**: PDF可（PowerPoint作成時は必ずPDF保存して入稿）。**PDFバージョン・PDF/X の指定は公開ページに記載なし → 発注時に直接確認が必要**
- [x] **Finished size and bleed/trim-mark requirement**: 841 × 1189 mm。塗り足しは「背景や画像が紙端まであるデザイン」の場合に上下左右3 mm（学会ポスター入稿ガイドは3〜5 mm）。本ポスターは外周余白18 mmで紙端に何も配置しないため**該当せず**。トンボは「トンボ付きPDFの場合」のみ言及 → **付けない**
- [x] **CMYK/RGB policy**: PDFデータガイド「可能であればCMYK、もしくはK(黒)1色で作成してください」／学会ポスター入稿ガイド「RGBではなくCMYKカラーモードで作成する必要があります」 → **CMYK版 `exp002_kitagi_quarry_foss4g2026_poster_cmyk.pdf` を入稿**
- [x] **Maximum file size**: **一次基準は 50 MB**（厳しい方を採用）。公開ページ間で不一致があるため両方を記録する。
  - データガイド https://visipri.com/dataguide/ 見出し「50MB以上の印刷データにつきまして」: 「データ容量が50MBまでの場合はご入稿データのファイルを直接ご入稿頂けます」／「データ容量が50MB以上の場合はファイアストレージやギガファイル便などのサービスをご利用ください」（確認日 2026-08-23）
  - トップページ https://visipri.com/ 見出し「データをご入稿ください」: 「データ容量が200MB以下の場合 入稿フォームから、印刷データを直接アップロードしてください」／「データ容量が200MBを超える場合 firestorageやギガファイル便などの外部ストレージサービスをご利用ください」（確認日 2026-08-23）
  - **不一致の扱い**: 厳しい方の 50 MB を運用基準とする。本PDFは CMYK版 9.7 MB / RGB版 17.3 MB で**両基準を満たす**ため発注可否への影響なし
- [x] **Font embedding/outline requirement**: 「フォント埋め込み済みのPDFで保存してください」（PDFガイド）／「必ずアウトライン化するか、データに埋め込む」（学会ガイド）→ **全フォント埋め込み済み**
- [x] **Image-resolution requirement**: 300 dpi以上を目安（PDFガイド）／150〜300 dpi推奨（学会ガイド）→ **現行の全図版 230〜294 dpi で適合**（2026-08-23 実測。下表参照。CMYK版PDF内の画像も同範囲）
- [x] **Proofing option**: **色校正は可能で、申込手順も公開されている**（https://visipri.com/faq/faq051.php 、確認日 2026-08-23）。同一機材・同一データで出力する方式で、手順は (1) A4等の小サイズで希望商品を注文して色校正に使う、(2) 注文時に連絡事項欄へ【色校正希望】と明記、(3) 本注文時に注文番号と【色校正済み】を明記。色味の調整やカラー指定は受け付けておらず、印刷予定データの縮小版を入稿する運用。**費用と本番納期への影響は記載なし → 実施する場合は発注時に確認**
  - **今回の判断: 色校正は省略する**（Codex判定 #issuecomment-5385023161）。理由は、色校正は公開仕様上の必須条件ではなく品質上の推奨であり、実施すると本注文前に校正物の受領・確認期間が必要になるため。08-25発注 / 08-29納品検収 / 09-01掲出のスケジュールを優先し、CMYK版PDFのプレビュー目視確認をもって代替する
- [x] **Confirmation date and source URL**: 2026-08-23 / https://visipri.com/ 、https://visipri.com/gakkai/gakkai_poster_a0.php 、https://visipri.com/dataguide/ 、https://visipri.com/dataguide/pdf/ 、https://visipri.com/gakkai/info-2-nyukou.php 、https://visipri.com/intro06_faq.php

### 納期プランと価格（A0学会ポスター、2026-08-23 確認）

| プラン | 発送 | 価格（税抜 / 税込） |
|---|---|---|
| 激安便 | 入稿・校了から3日後発送 | 2,420円 / 2,662円 |
| 通常便 | 16時までの入稿・校了で当日発送 | 4,200円 / 4,620円 |
| 特急便 | 最短3時間 | 8,400円 / 9,240円 |

掲出は9月1日09:00以降、内部目標は08-29までの納品検収。08-25発注なら激安便でも間に合う。

### PDFデータガイドの「してはいけないこと」への適合確認（2026-08-23 実測）

| 禁止事項 | 本ポスターの状態 | 確認方法 |
|---|---|---|
| サイズが異なる作成 | 841 × 1189 mm（2383.94 × 3370.39 pt）で一致 | `pdfinfo` |
| 線幅0.5 mm未満の使用 | **最小 0.6 mm**（見出し罫線）— 適合 | SVG の `stroke-width` 全値: 0.6 / 0.8 / 0.9 / 1.0 / 1.2 mm |
| フォント6 pt未満の使用 | **最小 6.526 mm ≒ 18.5 pt** — 適合（ポスター要件の18 pt下限と整合） | SVG の `font-size` 最小値 × 2.835 |
| 塗り足しなしでの提出 | 紙端まで届くデザインではないため塗り足し不要 | 外周余白18 mm |
| 不要な注釈・コメント・ハイライト・フォーム情報の残置 | **0件** — 下記「注釈の構造的検証」を参照 | pypdf によるPDFオブジェクト構造解析（主）＋ `pdfinfo` の `Form: none`（補強）＋バイト走査（補助） |
| 英語以外のファイル名 | ASCII のみ | ファイル名検査 |

### 図版の配置時実効解像度（2026-08-23 実測）

`scripts/build_exp002_poster_svg.py` の出力と、SVG の `<image width>`（mm）と PNG のピクセル幅からの独立計算が一致した値。

| 図版 | ピクセル幅 | 配置幅 | 実効解像度 |
|---|---:|---:|---:|
| poster_f1_study_area.png | 2355 px | 260.33 mm | **230 dpi** |
| poster_f3_summer_map.png | 3006 px | 260.33 mm | 293 dpi |
| poster_f4_index_panels.png | 2645 px | 260.33 mm | 258 dpi |
| poster_f5_truecolor_water.png | 2817 px | 260.33 mm | 275 dpi |
| poster_f6_field_photos.jpg | 3010 px | 260.33 mm | **294 dpi** |
| poster_qr_repo.png | 444 px | 42.0 mm | 269 dpi |

現行の範囲は **230〜294 dpi**。Task 3 の表（220〜313 dpi）および Task 5 記録の「230〜313 dpi」は、いずれも Task 5 の図版再生成前後の値が混在しており現行値ではない。全図版が最低150 dpi・目標200 dpi を満たす。

### 注釈の構造的検証（2026-08-23）

バイト列検索は PDF 1.6 のオブジェクトストリームに圧縮された辞書を検出できないため（同じ理由で CMYK 版の Type 3 を見落とした）、PDFオブジェクトを展開して構造的に検査した。

```bash
uv run --with pypdf python  # ページの /Annots、Root の /AcroForm、
                            # xref 上の全間接オブジェクトを解決して注釈系辞書を走査
```

| 検査項目 | RGB版 | CMYK版 |
|---|---|---|
| ページ数 | 1 | 1 |
| ページの `/Annots` エントリ数 | **0** | **0** |
| Root の `/AcroForm` | なし | なし |
| Root の `/OCProperties`・`/Names` | なし | なし |
| 解決した間接オブジェクト数 | 230 | 143 |
| 注釈系辞書（`/Type /Annot`、`/Widget`・`/Popup`・`/Text`・`/Highlight`・`/FreeText`・`/Stamp` 等の `/Subtype`） | **0件** | **0件** |
| `pdfinfo` の `Form` | none | none |

pypdf はオブジェクトストリーム内のオブジェクトも解決するため、この走査は圧縮された注釈辞書も対象に含む。バイト走査（`/Annots`・`/AcroForm`・`/Widget`・`/Popup` の文字列不検出）は**補助確認**として位置づける。

### 未解決事項（公開ページに記載なし → 発注時に直接確認）

1. **PDFバージョン（1.6 / 1.7）および PDF/X の受入可否** — 全ガイド・FAQに記載なし
2. **Type 3 グリフの受入可否** — 記載なし。**CMYK版にも Type 3 フォントが残存している**（`pdffonts` で確認。PDF 1.6 のオブジェクトストリームに圧縮されるためバイト列検索では検出できない）。cairo が記号グリフ（−・≥ 等）に生成するもので表示は正常だが、禁止された場合は当該グリフのアウトライン化版を再出力する必要がある
3. **色校正の費用・納期・申込方法**

問い合わせ先: フリーコール 0800-91-91-910（24時間年中無休）／メール visipri@visia.co.jp／東京 03-3974-8220／大阪 06-6533-7188

### Type 3 への対処方針: 案1（直接確認）を採用

Codex 判定（#issuecomment-5385023161）により、記号グリフのアウトライン化（案2）は先行させず、まず直接確認する。公開要件は「アウトライン化**または**埋め込み」であり Type 3 禁止は公開されておらず、現行の Type 3 は埋め込み済みで表示・テキスト抽出・validator を通過しているため。

電話で確認する内容:

> 埋め込み済みの Type 3 フォントを含む PDF 1.6 を、A0学会ポスターとして受け付けられますか。また、文字をラスタライズせずに出力できますか。PDF/X での入稿が必須ですか。

回答（担当者名・日時・回答内容）を本ログに記録する。不可の場合のみ案2に移り、`scripts/build_exp002_poster_svg.py` 経由で記号グリフ限定の代替文字化またはアウトライン化版を再生成し、validator・`pdffonts`・目視を再実施する（**全テキストのアウトライン化は poster validator の必須文字列チェックを壊すため不可**）。

### 発注前に必須の確認項目（Codex 判定 #issuecomment-5385023161）

**発注前（少なくとも校了・印刷開始前）に必須:**

1. [ ] CMYK版 PDF 1.6 の受入可否（PDF/X 必須か否かも同じ問い合わせで確認）
2. [ ] 埋め込み Type 3 の受入可否と、文字を保持したまま出力されること
3. [ ] 最終用紙・配送先・送料を含む**到着予定日**の確定（「3日後発送」は到着日ではないため、08-29 納品を配送込みで確認）

**発注時の選択または任意:**

- 色校正 — 今回は省略と判断（上記 Proofing option 参照）
- ファイル容量 — 両PDFとも厳しい方の 50 MB 未満のため追加確認不要

## Order and inspection

- [ ] Order date:
- [ ] Order number:
- [ ] Quantity:
- [ ] Delivery address:
- [ ] Expected delivery date:
- [ ] Actual delivery date:
- [ ] Physical inspection result:
- [ ] Defects or corrective action:
