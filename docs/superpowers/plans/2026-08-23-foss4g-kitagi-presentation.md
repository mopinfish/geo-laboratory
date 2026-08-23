# FOSS4G 2026 北木島 口頭発表スライド 実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 内容契約に定義された12枚の英語スライドを、python-pptx で決定論的に生成し、英日併記スピーカーノート・照合記録・機械検査を揃える。

**Architecture:** 生成スクリプト（`_presentation.py`）を正本とし、PPTX は生成物として手編集しない。図版は別スクリプト（`_figures.py`）で `images/` へ出力する。スピーカーノートは Markdown を正本とし、同内容を PPTX のノートペインへ書き込む。検証は本リポジトリの既存イディオムに従い、pytest ではなく**単一の validator スクリプト**（assert して `OK: N checks passed` を出力）で行う。

**Tech Stack:** Python 3.11 / uv、python-pptx 1.0.2、matplotlib、Pillow、shapely、pyproj、rasterio（既存の図版スクリプトから流用）

**Spec:** `docs/presentations/exp002_kitagi_foss4g2026_presentation.md`（内容契約・正本。Codex 第4回レビューで実装着手承認済み: #issuecomment-5386129829）

## Global Constraints

- スライドは **16:9**（`Emu(12192000) × Emu(6858000)`）、**12枚**（再訪なし版は11枚）
- 投影文字列は**英語のみ**。日本語はスピーカーノートの非発話部分にのみ置く
- 文字サイズ: タイトル 27 pt 以上、本文 17 pt 目安、注記 14 pt、**本文は 15 pt 未満にしない**。ページ番号等は 10〜12 pt を許容
- 主要色は背景・文字色を除き **2色以内**。影・立体・グラデーション・SmartArt を使わない
- 図形は種類を混在させない。矢印は細く無彩色
- 発話合計 **17:30（1,050秒）**、**S6 単体 2:30 以内**。時間計測は英語部分のみ
- 数値の正本は `docs/reports/exp002_kitagi_quarry_water_detection_report.md`。投影・発話する値は内容契約の記述と一致させる
- 禁止表現: `confirmed quarry ponds`（直接否定構文以外）、`poster`、`145 quarry ponds`、精度主張（`high accuracy` 等）
- S6 の **required spoken content 6行**を英語ノート本文に必ず含める
- 生成物に実行日時を埋め込まない（再実行でバイト一致させる）
- `PPTX` は `.py` の実行成果物。手編集しない

---

## ファイル構成

| ファイル | 責務 |
|---|---|
| `docs/presentations/exp002_kitagi_foss4g2026_figures.py` | 新規図版 P6・P8・P12 を `images/` へ生成 |
| `docs/presentations/images/` | スライド用画像（新規図版＋既存図版・写真のコピー） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.py` | PPTX 生成（正本）。`--no-revisit` で11枚版 |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation.pptx` | 生成物 |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation_speaker_notes.md` | 英日併記ノート（正本） |
| `docs/presentations/exp002_kitagi_foss4g2026_presentation_verification.md` | 照合記録 |
| `docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py` | 機械検査（全成果物） |

---

### Task 0: 8月31日の撮影対象リスト生成（**最優先。渡航前に必要**）

内容契約「8月31日の撮影に向けた事前準備」に対応する。他タスクと独立しており、**8月31日より前に完了させる**。

**Files:**
- Create: `scripts/build_exp002_field_shot_list.py`
- Create: `docs/results/exp002/exp002_field_shot_list_2026-08-31.md`

**Interfaces:**
- Consumes: `docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson`、`docs/results/exp002/exp002_osm_water_features.json`
- Produces: 撮影対象リスト（ポリゴンID・重心座標・面積・OSM近傍地物の有無と名称・徒歩起点からの概算距離）

- [ ] **Step 1: 検査を先に書く**

スクリプト末尾に自己検査を実装する（本リポジトリのイディオム）。

```python
assert len(rows) >= 12, f"候補が少なすぎる: {len(rows)}"
assert any(r["class"] == "largest" for r in rows), "最大ポリゴンが含まれていない"
assert any(r["class"] == "unmapped" for r in rows), "OSM近傍地物なしの候補が含まれていない"
assert any(r["class"] == "confounder" for r in rows), "交絡例が含まれていない"
assert all(133.515 <= r["lon"] <= 133.570 for r in rows), "島の範囲外の座標がある"
print(f"OK: {len(rows)} 地点（largest / unmapped / confounder の3クラス）")
```

- [ ] **Step 2: 検査が失敗することを確認**

Run: `uv run python scripts/build_exp002_field_shot_list.py`
Expected: FAIL（スクリプト未実装）

- [ ] **Step 3: 実装**

3クラスを抽出する。**安全・立入許可・到達可能性を面積順位より優先**する旨をリストの冒頭に明記する。

- `largest`: 検出最大ポリゴン（7,826 m²、北部）。OSM の「今岡石材丁場跡（北木の桂林）」と重なる位置。GPS・撮影方向・撮影時刻を記録する対象
- `unmapped`: OSM 地物が 100 m 以内にない80件のうち、面積上位10件。訪問4地点（Task 1 の `VISIT_ANCHORS`）からの概算距離を併記して到達しやすい順に並べる
- `confounder`: `water=reservoir` の OSM 地物（北木北ポンプ室）から 100 m 以内の検出ポリゴン

出力 Markdown には、各地点の「ポリゴンID・緯度経度（度小数6桁）・面積・OSM近傍地物・クラス・撮影メモ欄（空欄）」の表と、地理院地図・OSM へのリンク（`https://www.openstreetmap.org/?mlat=<lat>&mlon=<lon>#map=18/<lat>/<lon>`）を含める。

- [ ] **Step 4: 検査が通ることを確認**

Run: `uv run python scripts/build_exp002_field_shot_list.py`
Expected: `OK: N 地点（largest / unmapped / confounder の3クラス）`

- [ ] **Step 5: コミット**

```bash
git add scripts/build_exp002_field_shot_list.py \
        docs/results/exp002/exp002_field_shot_list_2026-08-31.md
git commit -m "feat: 8月31日の現地確認用 撮影対象リストを生成"
```

---

### Task 1: 新規図版 P6・P8・P12 の生成

**Files:**
- Create: `docs/presentations/exp002_kitagi_foss4g2026_figures.py`
- Create: `docs/presentations/images/`（出力先）

**Interfaces:**
- Consumes: `docs/results/exp002/exp002_kitagi_summer_water_polygons_2025-08-02.geojson`、`docs/posters/figures/exp002/poster_f3_summer_map.png`（配色の参照）
- Produces: `images/p06_clusters_map.png`、`images/p08_visit_anchors_map.png`、`images/p12_loop_diagram.png`。各画像は幅 2,400 px 以上、16:9 スライドの配置幅 220 mm で 200 dpi 以上

- [ ] **Step 1: 検査を先に書く**

`docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py` を新規作成し、図版の検査のみを実装する。

```python
#!/usr/bin/env python3
"""FOSS4G 2026 北木島 口頭発表の成果物を検査する。

使い方: uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parent
IMAGES = BASE / "images"

# 配置幅 220 mm で 200 dpi を満たす最小ピクセル幅
MIN_WIDTH_PX = int(220 / 25.4 * 200)  # 1732

FIGURES = ("p06_clusters_map.png", "p08_visit_anchors_map.png", "p12_loop_diagram.png")

errors: list[str] = []
checks = 0


def check(cond: bool, msg: str) -> None:
    global checks
    checks += 1
    if not cond:
        errors.append(msg)


for name in FIGURES:
    path = IMAGES / name
    check(path.is_file(), f"図版が存在しない: {name}")
    if path.is_file():
        width, height = Image.open(path).size
        check(width >= MIN_WIDTH_PX, f"{name}: 幅 {width}px が下限 {MIN_WIDTH_PX}px 未満")
        check(height > 0, f"{name}: 高さが不正")

if errors:
    print(f"FAIL ({len(errors)} / {checks} checks failed)")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"OK: {checks} checks passed")
```

- [ ] **Step 2: 検査が失敗することを確認**

Run: `uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py`
Expected: FAIL（`図版が存在しない: p06_clusters_map.png` 等 3件）

- [ ] **Step 3: 図版生成スクリプトを実装**

`docs/presentations/exp002_kitagi_foss4g2026_figures.py` を作成する。3つの図を出力する。

- **P6**: 公開GeoJSONの145ポリゴンを塗り、4集中地帯（north / south-east / centre / west）を英語ラベルで注記。背景は陸域シルエット（`scripts/generate_exp002_poster_figures.py` の `make_f3_summer_map` と同じ配色・同じ手法を流用し、ラベルだけ追加）
- **P8**: P6 と同じ地図に、座標を確認できた訪問4地点のみを重ねる。**候補ポリゴンとは異なる記号**（黒い三角＋白縁）と凡例（`Georeferenced visit anchors` / `Detected water polygons`）を付ける。4地点は次の通り

```python
VISIT_ANCHORS = [
    ("Toyoura Port", 133.5369, 34.3956),
    ("Toyoura hall", 133.5364, 34.3943),
    ("Lake stage (Keirin)", 133.5329, 34.3912),
    ("Sen-no-hama", 133.5309, 34.3930),
]
```

- **P12**: 3ステップの横並びフロー。同一寸法の角丸なし矩形3つ（`Satellite scan` / `Field visit` / `OpenStreetMap`）を細い無彩色の矢印で結ぶ。各矩形の下に1行の説明（`a finite candidate list` / `see it with your own eyes` / `put what you confirmed on the public map`）

いずれも `dpi=200`、`facecolor="white"`、`bbox_inches="tight"` で保存し、実行日時は埋め込まない。

- [ ] **Step 4: 検査が通ることを確認**

Run: `uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py`
Run: `uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py`
Expected: `OK: 9 checks passed`

- [ ] **Step 5: 決定性を確認**

Run: `md5 docs/presentations/images/*.png`、スクリプト再実行、再度 `md5`
Expected: 3ファイルすべて同一ハッシュ

- [ ] **Step 6: コミット**

```bash
git add docs/presentations/exp002_kitagi_foss4g2026_figures.py \
        docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py \
        docs/presentations/images/
git commit -m "feat: 口頭発表用の新規図版 P6/P8/P12 を生成"
```

---

### Task 2: PPTX 生成スクリプトの骨格（12枚・タイトルのみ）

**Files:**
- Create: `docs/presentations/exp002_kitagi_foss4g2026_presentation.py`
- Modify: `docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py`

**Interfaces:**
- Consumes: Task 1 の `images/`
- Produces: `exp002_kitagi_foss4g2026_presentation.pptx`。ヘルパ関数 `add_title(slide, text)`、`add_body(slide, lines, size_pt)`、`add_footer(slide, text)`、`add_slide_number(slide, n)`、`build(revisit: bool) -> Presentation`

- [ ] **Step 1: タイトル検査を追加**

validator に次を追記する。`TITLES` は内容契約の `## Slide N — ` 見出しから転記した完全一致文字列。

```python
from pptx import Presentation
from pptx.util import Pt

PPTX = BASE / "exp002_kitagi_foss4g2026_presentation.pptx"

TITLES = [
    "Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools",
    "A quarrying island, and the ponds it left behind",
    "On foot: I could stand in front of five or six of them",
    "From the air: the quarry boundaries are the landform",
    "On the train home: one satellite scene covers the whole island",
    "The scan found 145 water polygons across the island",
    "Each scale shows what the others cannot",
    "Five or six sites visited — the scan produced 145 candidates",
    "Two days ago I went back — a first look, not validation",
    "What this can and cannot tell you",
    "The 145 polygons are open data now",
    "Check them on the ground, then put them on the map",
]

check(PPTX.is_file(), "PPTX が存在しない")
if PPTX.is_file():
    prs = Presentation(PPTX)
    check(len(prs.slides) == 12, f"スライド数が 12 でない: {len(prs.slides)}")
    texts = []
    for slide in prs.slides:
        texts.append("\n".join(
            sh.text_frame.text for sh in slide.shapes if sh.has_text_frame
        ))
    for i, title in enumerate(TITLES):
        check(i < len(texts) and title in texts[i],
              f"S{i+1}: タイトルが一致しない — 期待 '{title[:40]}...'")
        check(not (i < len(texts) and texts[i].lstrip().startswith(str(i + 1) + title[:6])),
              f"S{i+1}: タイトル先頭に番号が混入している")
```

- [ ] **Step 2: 検査が失敗することを確認**

Run: `uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py`
Expected: FAIL（`PPTX が存在しない`）

- [ ] **Step 3: 生成スクリプトを実装**

`scripts/generate_exp002_presentation.py` のヘルパ構造（`Presentation()`、`slide_layouts[6]`、`add_textbox`）を踏襲する。16:9 を明示し、12枚のタイトルのみを配置する。

```python
SLIDE_W, SLIDE_H = Emu(12192000), Emu(6858000)
MARGIN = Inches(0.55)
SZ_TITLE, SZ_BODY, SZ_NOTE, SZ_NUM = 28, 17, 14, 11
COL_TEXT, COL_ACCENT, COL_MUTED = RGBColor(0x2B, 0x2B, 0x2B), RGBColor(0x0D, 0x47, 0xA1), RGBColor(0x5A, 0x56, 0x4E)


def build(revisit: bool = True) -> Presentation:
    prs = Presentation()
    prs.slide_width, prs.slide_height = SLIDE_W, SLIDE_H
    slides = [s01, s02, s03, s04, s05, s06, s07, s08]
    if revisit:
        slides.append(s09)
    slides += [s10, s11, s12]
    for n, fn in enumerate(slides, start=1):
        fn(prs.slides.add_slide(prs.slide_layouts[6]), n)
    return prs
```

各 `sNN(slide, n)` はこの Task ではタイトルとスライド番号のみを置く。

- [ ] **Step 4: 検査が通ることを確認**

Run: `uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py`
Run: `uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py`
Expected: `OK: 34 checks passed`

- [ ] **Step 5: コミット**

```bash
git add docs/presentations/exp002_kitagi_foss4g2026_presentation.py \
        docs/presentations/exp002_kitagi_foss4g2026_presentation.pptx \
        docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py
git commit -m "feat: 口頭発表 PPTX 生成スクリプトの骨格（12枚・タイトル）"
```

---

### Task 3: 投影本文の実装と禁止表現の検査

**Files:**
- Modify: `docs/presentations/exp002_kitagi_foss4g2026_presentation.py`
- Modify: `docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py`

**Interfaces:**
- Consumes: Task 2 の `add_body`、`add_footer`
- Produces: 全12枚の投影文字列。validator の `REQUIRED_STRINGS`（スライド別必須文字列）と `FORBIDDEN`

- [ ] **Step 1: 必須文字列と禁止表現の検査を追加**

内容契約の `Projected body` から転記する。抜粋（全12枚分を同形式で列挙する）。

```python
REQUIRED_STRINGS = {
    1: ["Noboru Otsuka", "Geolonia", "FOSS4G 2026 Hiroshima", "2026-09-02 13:30", "Himawari"],
    2: ["127 active quarry sites at the 1957 peak", "National heritage since 2019",
        "I found no island-wide record of the ponds themselves"],
    3: ["Five or six sites during the event"],
    4: ["A property line, standing as terrain"],
    5: ["Microsoft Planetary Computer STAC API", "NDWI", "MNDWI", "NDVI",
        "A standard water-index workflow", "100 m"],
    6: ["145", "2025-08-02", "113", "a comparison of scale, not a one-to-one match",
        "not individually field-confirmed quarry ponds",
        "Contains modified Copernicus Sentinel data [2025]"],
    7: ["Not better or worse"],
    8: ["Five or six quarry sites visited during the event",
        "145 water polygons detected from one scene",
        "no precision or recall yet",
        "Every quarry feature already mapped in OpenStreetMap overlaps one of the detections",
        "for reference", "finite field-check list"],
    9: ["2026-08-31", "Illustrative field photographs — not accuracy validation"],
    10: ["10 m resolution", "No precision or recall", "field validation not done"],
    11: ["Published — 145 detected polygons as GeoJSON", "Pipeline outputs",
         "Open-source Python pipeline", "Seto Inland Sea", "CC BY 4.0"],
    12: ["Satellite scan", "Field visit", "OpenStreetMap",
         "I plan to contribute the ponds I can confirm",
         "The March mapping party added features observed on the ground"],
}

FORBIDDEN = [
    (r"confirmed quarry pond", r"not\s+(?:individually\s+)?(?:field[-\s])?confirmed quarry pond",
     "現地確認済みと読める表現"),
    (r"\b145 quarry ponds?\b", None, "検出を丁場池と同一視"),
    (r"high accuracy|accuracy is high", None, "精度主張"),
    (r"\bposter\b", None, "採択形式は口頭発表"),
    (r"one-to-one match", r"not\s+(?:a\s+)?one-to-one match", "1対1対応と読める表現"),
]
```

あわせて**evidence 階層**を検査する。中心メッセージ（タイトル）より補足値が大きくならないこと、S5 の式は投影本文のテキストフレームに置かず図版内にあることを確認する。

```python
# S5: 式は図版内に置く（投影本文のテキストとして存在しない）
s5_text = texts[4]
for formula in ("(Green − NIR)", "(Green + NIR)", "(Green − SWIR)"):
    check(formula not in s5_text, f"S5: 式 '{formula}' が投影本文にある（図版内へ置く）")

# S6: 春季タイル・雲量は主結果 145 より小さい文字サイズ
def max_font_pt(slide, needle: str) -> float:
    sizes = [run.font.size.pt for sh in slide.shapes if sh.has_text_frame
             for para in sh.text_frame.paragraphs for run in para.runs
             if needle in run.text and run.font.size is not None]
    return max(sizes) if sizes else 0.0

s6 = prs.slides[5]
check(max_font_pt(s6, "145") > max_font_pt(s6, "113"),
      "S6: 春季113が主結果145以上の大きさになっている")
```

あわせて**文字サイズ下限**を検査する。

```python
for i, slide in enumerate(prs.slides, start=1):
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                if run.font.size is None or not run.text.strip():
                    continue
                pt = run.font.size.pt
                is_number_or_footer = run.text.strip().isdigit() or pt <= 12
                check(pt >= 15 or is_number_or_footer,
                      f"S{i}: 本文 {pt}pt が 15pt 未満 — '{run.text[:30]}'")
```

- [ ] **Step 2: 検査が失敗することを確認**

Expected: FAIL（各スライドの必須文字列が未実装のため多数）

- [ ] **Step 3: 投影本文を実装**

内容契約の `Projected body` を、スライドごとに `add_body` で配置する。大きな数値（S6 の `145`、S8 の対比）は `callout` として 60〜72 pt で置き、説明文は 17 pt。帰属・ライセンス・ライブラリ名は `add_footer`（11〜12 pt）へ。

- [ ] **Step 4: 検査が通ることを確認**

Run: 生成 → validator
Expected: `OK: 100+ checks passed`（必須文字列・禁止表現・文字サイズを含む）

- [ ] **Step 5: コミット**

```bash
git add docs/presentations/exp002_kitagi_foss4g2026_presentation.{py,pptx} \
        docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py
git commit -m "feat: 投影本文を実装し必須文字列・禁止表現・15pt下限を検査"
```

---

### Task 4: 図版・写真の配置と再訪なし版の切替

**Files:**
- Modify: `docs/presentations/exp002_kitagi_foss4g2026_presentation.py`
- Modify: `docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py`
- Create: `docs/presentations/images/`（既存写真のコピー）

**Interfaces:**
- Consumes: Task 1 の P6/P8/P12、`docs/articles/2026_chiri-koryu-10/figures/`、`docs/posters/figures/exp002/`
- Produces: `--no-revisit` オプション、写真スロット定数 `PHOTO_SLOT_W_IN`、`PHOTO_SLOT_H_IN`

- [ ] **Step 1: 画像配置と版切替の検査を追加**

```python
EXPECTED_IMAGES = {
    1: 1,   # 岩壁写真
    2: 1,   # 位置図
    3: 2,   # 徒歩写真2枚
    4: 2,   # 上空写真2枚
    5: 1,   # 指数4パネル
    6: 1,   # P6 集中地帯地図
    7: 1,   # 三スケール合成図
    8: 1,   # P8 訪問地点地図
    9: 2,   # 8/31 写真（暫定プレースホルダ2枚）
    11: 1,  # QR
    12: 1,  # P12 ループ図
}
for i, slide in enumerate(prs.slides, start=1):
    n_pic = sum(1 for sh in slide.shapes if sh.shape_type == 13)  # PICTURE
    expected = EXPECTED_IMAGES.get(i, 0)
    check(n_pic == expected, f"S{i}: 画像数 {n_pic} が期待値 {expected} と不一致")
```

再訪なし版の検査も追加する。

```python
NO_REVISIT_PPTX = BASE / "exp002_kitagi_foss4g2026_presentation_no_revisit.pptx"
if NO_REVISIT_PPTX.is_file():
    prs2 = Presentation(NO_REVISIT_PPTX)
    check(len(prs2.slides) == 11, f"再訪なし版のスライド数が 11 でない: {len(prs2.slides)}")
    t2 = "\n".join(sh.text_frame.text for s in prs2.slides for sh in s.shapes if sh.has_text_frame)
    check("2026-08-31" not in t2, "再訪なし版に再訪スライドが残っている")
```

- [ ] **Step 2: 検査が失敗することを確認**

Expected: FAIL（画像が0枚、再訪なし版が存在しない）

- [ ] **Step 3: 画像配置と版切替を実装**

- 既存画像を `images/` へコピーする（`fig01_lake_stage.jpg`、`fig03_keirin_cliff.jpg`、`fig05_drone_takeoff.jpg`、`fig06_aerial_quarries.jpg`、`fig09_multiscale.png`、`poster_f1_study_area.png`、`poster_f4_index_panels.png`、`poster_qr_repo.png`）。コピー元と SHA256 を Task 6 の照合記録へ記載する
- S3・S4・S9 の写真は**固定寸法スロット**（幅 5.6 in × 高さ 3.15 in、16:9）に中央クロップして配置する。S9 は 8/31 撮影分が未着のため、`images/placeholder_revisit_1.png`（`Placeholder — 2026-08-31 photograph` と描いた無地画像）を置く
- `--no-revisit` で S9 を除外して `_no_revisit.pptx` を出力する

- [ ] **Step 4: 検査が通ることを確認**

Run: `uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py`
Run: `uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py --no-revisit`
Run: validator
Expected: `OK`（画像数・再訪なし版を含む）

- [ ] **Step 5: コミット**

```bash
git add docs/presentations/
git commit -m "feat: 図版と写真スロットを配置し再訪なし版の切替を実装"
```

---

### Task 5: 英日併記スピーカーノートと PPTX ノートペイン

**Files:**
- Create: `docs/presentations/exp002_kitagi_foss4g2026_presentation_speaker_notes.md`
- Modify: `docs/presentations/exp002_kitagi_foss4g2026_presentation.py`
- Modify: `docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py`

**Interfaces:**
- Consumes: 内容契約の Central claim / Notes-only boundary / Required spoken content
- Produces: ノート Markdown の構造（スライド毎に `### Slide N — <title>` → `**EN (spoken)**` → `**JA (not spoken)**`）。生成スクリプトは EN 部分のみを PPTX ノートペインの先頭に、JA を続けて書き込む

- [ ] **Step 1: ノートの検査を追加**

```python
NOTES_MD = BASE / "exp002_kitagi_foss4g2026_presentation_speaker_notes.md"
WPM = 145
DURATIONS_S = [35, 100, 90, 90, 110, 150, 70, 90, 110, 80, 70, 55]
S6_REQUIRED = [
    "Spring: 2025-03-23, 0.0% cloud",
    "113 reported polygons",
    "largest 1.28 hectares",
    "Summer: 2025-08-02, 0.7% cloud",
    "145 polygons",
    "we have not isolated the cause",
    "that run's configuration is not preserved",
    "removed only nine pixels",
    "not individually field-confirmed quarry ponds",
]

md = NOTES_MD.read_text(encoding="utf-8")
blocks = re.split(r"(?m)^### Slide (\d+) — ", md)[1:]
pairs = {int(blocks[i]): blocks[i + 1] for i in range(0, len(blocks), 2)}
check(len(pairs) == 12, f"ノートのスライド数が 12 でない: {len(pairs)}")
for n, body in pairs.items():
    check("**EN (spoken)**" in body, f"S{n}: EN 発話本文が無い")
    check("**JA (not spoken)**" in body, f"S{n}: JA 非発話部分が無い")
    en = body.split("**JA (not spoken)**")[0]
    words = len(re.findall(r"[A-Za-z][A-Za-z'’-]*", en))
    budget = round(DURATIONS_S[n - 1] / 60 * WPM)
    check(abs(words - budget) <= budget * 0.25,
          f"S{n}: EN 語数 {words} が想定 {budget} 語から 25% 超乖離")
for line in S6_REQUIRED:
    en6 = pairs[6].split("**JA (not spoken)**")[0]
    check(line in en6, f"S6: required spoken content が EN 本文に無い — '{line}'")

# PPTX ノートペインと Markdown の同期
for i, slide in enumerate(prs.slides, start=1):
    note = slide.notes_slide.notes_text_frame.text
    en = pairs[i].split("**JA (not spoken)**")[0]
    first = next(l.strip() for l in en.splitlines() if l.strip() and not l.startswith("**"))
    check(first[:40] in note, f"S{i}: PPTX ノートに EN 本文が同期していない")
```

- [ ] **Step 2: 検査が失敗することを確認**

Expected: FAIL（ノート Markdown が存在しない）

- [ ] **Step 3: ノート Markdown を書く**

各スライドの語数目安（145 wpm 換算）:

| S | 秒 | EN 語数目安 |
|---:|---:|---:|
| 1 | 35 | 85 |
| 2 | 100 | 242 |
| 3 | 90 | 218 |
| 4 | 90 | 218 |
| 5 | 110 | 266 |
| 6 | 150 | 363 |
| 7 | 70 | 169 |
| 8 | 90 | 218 |
| 9 | 110 | 266 |
| 10 | 80 | 193 |
| 11 | 70 | 169 |
| 12 | 55 | 133 |

形式は次の通り。EN は**読み上げる文章そのもの**を書く（箇条書きにしない）。1文は短く保ち、非母語話者が読み上げやすい語彙にする。JA は訳と補足で、**読み上げない**ことを明記する。

```markdown
### Slide 6 — The scan found 145 water polygons across the island

**EN (spoken)**

The scan found one hundred and forty-five water polygons inside the island, each at
least one hundred square metres. Summer: 2025-08-02, 0.7% cloud — 145 polygons,
largest 7,826 square metres. ...

**JA (not spoken)** — 訳と補足。読み上げない。

- 145件は検出数であって丁場数ではない
- 春季113は当時の報告値。実行設定が保存されておらず、差の原因は特定できていない
```

- [ ] **Step 4: PPTX ノートペインへの書き込みを実装**

生成スクリプトでノート Markdown を読み、スライド番号ごとに EN → JA の順で `notes_text_frame.text` へ書き込む。

- [ ] **Step 5: 検査が通ることを確認**

Run: 生成 → validator
Expected: `OK`（語数・required spoken content・ノート同期を含む）

- [ ] **Step 6: コミット**

```bash
git add docs/presentations/
git commit -m "feat: 英日併記スピーカーノートを作成し PPTX ノートペインへ同期"
```

---

### Task 6: 照合記録

**Files:**
- Create: `docs/presentations/exp002_kitagi_foss4g2026_presentation_verification.md`
- Modify: `docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py`

**Interfaces:**
- Consumes: 全成果物
- Produces: 数値・出典の対応表、画像の SHA256 とコピー元、写真の座標欄

- [ ] **Step 1: 照合記録の検査を追加**

```python
VERIFICATION = BASE / "exp002_kitagi_foss4g2026_presentation_verification.md"
v = VERIFICATION.read_text(encoding="utf-8")
for value in ("145", "113", "127", "1.28", "7,826", "9", "100 m²", "10 m",
              "2025-03-23", "2025-08-02", "0.0%", "0.7%"):
    check(value in v, f"照合記録に値の出典が無い: {value}")
for name in FIGURES + ("fig03_keirin_cliff.jpg", "poster_f4_index_panels.png"):
    check(name in v, f"照合記録に画像の記載が無い: {name}")
check("SHA256" in v, "照合記録に SHA256 の記載が無い")
```

- [ ] **Step 2: 検査が失敗することを確認**

Expected: FAIL（照合記録が存在しない）

- [ ] **Step 3: 照合記録を書く**

- 投影・発話する全数値について「値 / スライド / 出典（レポートの節番号）」の表
- `images/` の全画像について「ファイル名 / コピー元パス / SHA256 / 使用スライド」の表
- 8/31 写真は撮影後に「座標 / 撮影時刻 / 撮影方向 / 対象ポリゴンID」を追記する空欄を用意
- OSM 照合は参考値であり投影しない旨、および参照先（`exp002_osm_comparison.md`）

- [ ] **Step 4: 検査が通ることを確認 → コミット**

```bash
git add docs/presentations/
git commit -m "docs: 口頭発表の照合記録を作成"
```

---

### Task 7: 最終ゲート（通し読み・目視・報告）

**Files:**
- Modify: `docs/presentations/exp002_kitagi_foss4g2026_presentation_verification.md`

- [ ] **Step 1: PDF 化して目視確認**

```bash
soffice --headless --convert-to pdf --outdir tmp \
  docs/presentations/exp002_kitagi_foss4g2026_presentation.pptx
pdfinfo tmp/exp002_kitagi_foss4g2026_presentation.pdf | grep -E "Pages|Page size"
pdftoppm -r 80 -png tmp/exp002_kitagi_foss4g2026_presentation.pdf tmp/slide
```

12ページ・16:9 であることと、文字切れ・重なり・スライド外図形がないことを全ページで確認する。

- [ ] **Step 2: 英語通し読みの実測**

EN ノートを実際に音読し、**S6 単体 2:30 以内・本編 17:30 前後**を確認する。結果（各スライドの実測秒）を照合記録へ記載する。超過した場合は投影文字列ではなく EN ノートの文を削る。

- [ ] **Step 3: グレースケール確認**

`sips -s format png --matchTo '/System/Library/ColorSync/Profiles/Generic Gray Gamma 2.2 Profile.icc'` でグレースケール化し、水域・訪問地点・凡例が区別できることを確認する。

- [ ] **Step 4: 全検査を再実行してコミット**

```bash
uv run python docs/presentations/exp002_kitagi_foss4g2026_figures.py
uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py
uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py --no-revisit
uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py
git diff --check
git add docs/presentations/
git commit -m "docs: 通し読み時間と目視確認の結果を照合記録へ追記"
```

- [ ] **Step 5: Issue #6 へ報告**

作成ファイル、検査結果（`OK: N checks passed`）、通し読みの実測時間、PDF のページ数、8/31 写真の差し替え手順、Codex レビュー依頼の観点を投稿する。

---

## Review Checklist

- [ ] スライド12枚（再訪なし版11枚）、タイトルが内容契約と完全一致
- [ ] 投影文字列が英語のみ、本文 15 pt 以上
- [ ] 禁止表現なし（`confirmed quarry ponds` の直接否定以外、`poster`、精度主張）
- [ ] S6 の required spoken content 6行が EN ノート本文にある
- [ ] EN 語数が各スライドの想定秒数（145 wpm）から 25% 以内
- [ ] PPTX ノートペインと Markdown が同期
- [ ] P8 の訪問地点が候補ポリゴンと異なる記号・凡例で区別されている
- [ ] 画像の SHA256 とコピー元が照合記録にある
- [ ] 生成物に実行日時が埋め込まれていない（再実行でバイト一致）
- [ ] 英語通し読みで S6 単体 2:30 以内・本編 17:30 前後
- [ ] S5 の式が図版内にあり投影本文にない。S6 の春季タイルが主結果より小さい
- [ ] 8月31日の撮影対象リスト（Task 0）が渡航前に完成している

## 8月31日以降の差し替え手順

1. 撮影した写真を `images/revisit_1.jpg`、`images/revisit_2.jpg` として配置（固定寸法スロットに合わせて中央クロップされる）
2. 照合記録の 8/31 欄へ座標・撮影時刻・撮影方向・対象ポリゴンIDを記入
3. `uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py` を再実行
4. validator を再実行し、PDF 化して S9 を目視確認
5. 撮影できなかった場合は `--no-revisit` 版を本番として使う
