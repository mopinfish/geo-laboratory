#!/usr/bin/env python3
"""FOSS4G 2026 北木島 口頭発表（英語・12枚、または再訪なし版11枚）の PPTX を生成する。

各スライドにタイトル・本文（必要に応じて callout・footer）・図版/写真・スライド
番号を配置する。図版・写真は `docs/presentations/images/` から読み込む
（外部ソースからのコピー元と SHA256 は Task 6 の照合記録に記載）。

タイトル文字列・投影本文は内容契約（docs/presentations/exp002_kitagi_foss4g2026_presentation.md）
の `## Slide N — ` 見出しと `Projected body` から転記した完全一致文字列。

`--no-revisit` を指定すると S9（8/31 再訪スライド）を除いた11枚を
`exp002_kitagi_foss4g2026_presentation_no_revisit.pptx` として出力する
（現地訪問が未実施の場合の切替。`build(revisit=False)` が11枚を返す）。

スピーカーノートは本スクリプトでは扱わない
（`exp002_kitagi_foss4g2026_presentation_speaker_notes.md` を正本とし、別タスクで
ノートペインへ反映する）。

決定性（determinism）: 生成される .pptx はコミット対象であり、再生成しても
バイト単位で同一になる必要がある。python-pptx が自動的にスタンプしうる
docProps/core.xml のプロパティ（created / modified / last_modified_by /
revision / author / title）はすべて固定リテラル値で明示的に上書きする。

使い方:
    uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py
    uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py --no-revisit
"""

from __future__ import annotations

import argparse
import datetime as dt
import io
import zipfile
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

BASE = Path(__file__).resolve().parent
IMAGES = BASE / "images"
OUTPUT = BASE / "exp002_kitagi_foss4g2026_presentation.pptx"
NO_REVISIT_OUTPUT = BASE / "exp002_kitagi_foss4g2026_presentation_no_revisit.pptx"

# --- 16:9 スライドサイズ ---
SLIDE_W = Emu(12192000)
SLIDE_H = Emu(6858000)

# --- レイアウト定数 ---
MARGIN = Inches(0.55)
TITLE_TOP = Inches(0.4)
TITLE_HEIGHT = Inches(1.8)
NUM_W = Inches(0.8)
NUM_H = Inches(0.35)

# --- タイプスケール ---
SZ_TITLE = 28
SZ_BODY = 17
SZ_CALLOUT = 66  # evidence 階層の主結果（S6 の 145 等）60〜72pt の中央値
SZ_NOTE = 14
SZ_FOOTER = 11  # 帰属・ライセンス・ライブラリ名（11〜12pt）
SZ_NUM = 11
BODY_MIN_PT = 15  # 本文はこの下限を下回ってはならない

# --- 配色 ---
COL_TEXT = RGBColor(0x2B, 0x2B, 0x2B)
COL_ACCENT = RGBColor(0x0D, 0x47, 0xA1)
COL_MUTED = RGBColor(0x5A, 0x56, 0x4E)

# --- 図版・写真配置の共通ジオメトリ ---
# タイトル直下からフッター/スライド番号の手前までの領域（画像・本文を配置する帯）。
GRAPHIC_TOP = TITLE_TOP + TITLE_HEIGHT
GRAPHIC_BOTTOM = SLIDE_H - Inches(0.5)
GRAPHIC_HEIGHT = GRAPHIC_BOTTOM - GRAPHIC_TOP
USABLE_LEFT = MARGIN
USABLE_WIDTH = SLIDE_W - 2 * MARGIN
IMAGE_TEXT_GAP = Inches(0.3)

# 写真スロット（S3・S4・S9）: 固定寸法、16:9、中央クロップして配置する。
# 差し替え（例: 8/31 撮影分の投入）で生成スクリプトを変更しなくてよいよう、
# 位置決めのロジックはこの2定数だけに依存させる。
PHOTO_SLOT_W_IN = Inches(5.6)
PHOTO_SLOT_H_IN = Inches(3.15)
PHOTO_ROW_GAP = Inches(0.2)
PHOTO_ROW_TOP = GRAPHIC_BOTTOM - PHOTO_SLOT_H_IN
PHOTO_ROW_LEFT = USABLE_LEFT + (USABLE_WIDTH - 2 * PHOTO_SLOT_W_IN - PHOTO_ROW_GAP) // 2
# 写真スロットの上に置く本文（S3・S4・S9 共通）の高さ。
PHOTO_TEXT_HEIGHT = PHOTO_ROW_TOP - GRAPHIC_TOP - Inches(0.15)


def _image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def add_picture_contain(slide, path: Path, left, top, max_width, max_height, name: str):
    """画像をアスペクト比を保ったまま矩形内に収めて中央配置する（クロップしない）。

    地図・グラフ・QRコードなど情報を伝える図版はラベル欠落を避けるためクロップせず、
    矩形内で均一スケールし中央に置く。
    """
    iw, ih = _image_size(path)
    scale = min(max_width / iw, max_height / ih)
    width = int(iw * scale)
    height = int(ih * scale)
    pic_left = int(left + (max_width - width) / 2)
    pic_top = int(top + (max_height - height) / 2)
    pic = slide.shapes.add_picture(str(path), pic_left, pic_top, width=width, height=height)
    pic.name = name
    return pic


def add_picture_cover(slide, path: Path, left, top, width, height, name: str, *, vbias: float = 0.5):
    """画像を矩形いっぱいにクロップで配置する（縦横比は変形させない）。

    写真スロット（S1 表紙・S3・S4・S9）で使用する。矩形とのアスペクト比の差分だけを
    長辺方向からクロップし、残った部分を矩形にそのまま引き伸ばす（この時点で
    残存部分のアスペクト比は矩形と一致しているため、実際には変形しない）。

    縦方向のクロップ（画像が縦長でクロップ対象が上下になる場合）が必要なとき、
    `vbias`（0〜1、既定 0.5 で中央対称）は必要クロップ量のうち上側から取る割合を
    表す。`vbias` を大きくすると上側をより多くクロップして構図が下寄りに動き
    （例: 水面を残す）、小さくすると下側をより多くクロップして構図が上寄りに動く
    （例: 写り込んだ機材・UIを画面下端から外す）。個体差のある画像アスペクト比
    でも必要クロップ量から比率で再計算するため、複数画像へ同じ `vbias` を安全に
    使い回せる。
    """
    iw, ih = _image_size(path)
    img_ar = iw / ih
    target_ar = width / height
    pic = slide.shapes.add_picture(str(path), left, top, width=width, height=height)
    pic.name = name
    if img_ar > target_ar:
        visible = target_ar / img_ar
        crop = (1 - visible) / 2
        pic.crop_left = crop
        pic.crop_right = crop
    elif img_ar < target_ar:
        visible = img_ar / target_ar
        total = 1 - visible
        pic.crop_top = total * vbias
        pic.crop_bottom = total * (1 - vbias)
    return pic


def add_photo_pair(
    slide, path1: Path, path2: Path, name1: str = "Picture1", name2: str = "Picture2",
    *, vbias1: float = 0.5, vbias2: float = 0.5,
):
    """写真スロット2枚を同寸で並置する（S3・S4・S9 共通）。

    `vbias1`/`vbias2` は各写真のクロップ位置（`add_picture_cover` の `vbias`）を
    個別に指定する場合に使う（既定は中央対称クロップ）。
    """
    add_picture_cover(
        slide, path1, PHOTO_ROW_LEFT, PHOTO_ROW_TOP, PHOTO_SLOT_W_IN, PHOTO_SLOT_H_IN, name1,
        vbias=vbias1,
    )
    add_picture_cover(
        slide, path2,
        PHOTO_ROW_LEFT + PHOTO_SLOT_W_IN + PHOTO_ROW_GAP,
        PHOTO_ROW_TOP, PHOTO_SLOT_W_IN, PHOTO_SLOT_H_IN, name2,
        vbias=vbias2,
    )


def resolve_revisit_photo(n: int) -> Path:
    """8/31 再訪の撮影写真を解決する（撮影後の差し替えを生成スクリプト変更なしで行う）。

    `images/revisit_{n}.jpg`（`.jpeg` / `.png` も許容）が存在すればそれを使う。
    撮影がまだの間は `images/placeholder_revisit_{n}.png`
    （`Placeholder — 2026-08-31 photograph` と描いた無地画像）を使う。
    """
    for ext in ("jpg", "jpeg", "png"):
        candidate = IMAGES / f"revisit_{n}.{ext}"
        if candidate.is_file():
            return candidate
    return IMAGES / f"placeholder_revisit_{n}.png"


# 内容契約の `## Slide N — ` 見出しから転記した、各スライドのタイトル完全一致文字列。
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

# --- 決定性のための固定リテラル値 ---
FIXED_DATETIME = dt.datetime(2026, 1, 1, 0, 0, 0)
FIXED_AUTHOR = "geo-laboratory exp002"
FIXED_LAST_MODIFIED_BY = "exp002_kitagi_foss4g2026_presentation.py"
FIXED_REVISION = 1
FIXED_ZIP_DATETIME = (2026, 1, 1, 0, 0, 0)


def _normalize_zip_timestamps(path: Path) -> None:
    """保存済み .pptx（zip）内の各エントリの mtime を固定値で揃え直す。

    python-pptx（zipfile.ZipFile.writestr）は各エントリのタイムスタンプを
    実行時刻で書き込むため、docProps/core.xml の日時を固定しても
    zip 全体のバイト列は実行するたびに変わってしまう。保存後にこの関数で
    全エントリの date_time を固定し、内容（バイト列・圧縮方式・並び順）は
    保ったまま再書き込みすることで、再生成時の md5 一致（決定性）を保証する。
    """
    with zipfile.ZipFile(path, "r") as zin:
        infos = zin.infolist()
        contents = [zin.read(info.filename) for info in infos]

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for info, data in zip(infos, contents):
            fixed_info = zipfile.ZipInfo(info.filename, date_time=FIXED_ZIP_DATETIME)
            fixed_info.compress_type = info.compress_type
            fixed_info.external_attr = info.external_attr
            zout.writestr(fixed_info, data)

    path.write_bytes(buf.getvalue())


def add_title(slide, text: str):
    """タイトル用テキストボックスを配置する。

    検査（validate_exp002_kitagi_foss4g2026_presentation.py）が図形を確実に
    識別できるよう、シェイプ名を "Title" に固定する。
    """
    box = slide.shapes.add_textbox(
        MARGIN, TITLE_TOP, SLIDE_W - 2 * MARGIN, TITLE_HEIGHT
    )
    box.name = "Title"
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.LEFT
    run = p.runs[0]
    run.font.size = Pt(SZ_TITLE)
    run.font.bold = True
    run.font.color.rgb = COL_TEXT
    return box


def add_body(
    slide,
    lines: list[str | tuple[str, int]],
    size_pt: int = SZ_BODY,
    *,
    top=None,
    left=None,
    width=None,
    height=None,
    align=PP_ALIGN.LEFT,
    color: RGBColor = COL_TEXT,
    bold: bool = False,
    name: str = "Body",
):
    """本文用テキストボックスを配置する（Task 2 で用意、Task 3 で使用）。

    `lines` の各要素は `str`（`size_pt` を使用）または `(text, size_pt)` の2要素
    タプル（行ごとに個別のフォントサイズを指定。evidence 階層で補足値を主結果より
    小さく見せる場合に使う）。いずれの `size_pt` も BODY_MIN_PT（15pt）を
    下回ってはならない。

    位置・寸法（`top`/`left`/`width`/`height`）を省略した場合は Task 2 の既定位置
    （タイトル直下から footer 手前まで）を使う。大きな数値（S6 の `145` 等）を
    60〜72pt の callout として個別のテキストボックスに置く場合は、これらの
    キーワード引数で位置を指定して呼び出す。シェイプ名は既定で "Body"（Task 2 の
    命名規約を維持する）。
    """
    resolved: list[tuple[str, int]] = [
        (line, size_pt) if isinstance(line, str) else line for line in lines
    ]
    for _, pt in resolved:
        if pt < BODY_MIN_PT:
            raise ValueError(f"body size_pt={pt} は下限 {BODY_MIN_PT}pt を下回っている")

    box = slide.shapes.add_textbox(
        left if left is not None else MARGIN,
        top if top is not None else TITLE_TOP + TITLE_HEIGHT,
        width if width is not None else SLIDE_W - 2 * MARGIN,
        height if height is not None else SLIDE_H - TITLE_TOP - TITLE_HEIGHT - Inches(0.5),
    )
    box.name = name
    tf = box.text_frame
    tf.word_wrap = True
    for i, (line, pt) in enumerate(resolved):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        run = p.runs[0]
        run.font.size = Pt(pt)
        run.font.bold = bold
        run.font.color.rgb = color
    return box


def add_footer(slide, text: str | list[str], size_pt: int = SZ_FOOTER):
    """フッター用テキストボックスを配置する（Task 2 で用意、Task 3 で使用）。

    `text` は単一行の `str`、または複数行を表す `list[str]`（帰属・ライセンス表記と
    ライブラリ名を別行にする場合等）。`size_pt` は 11〜12pt を想定する。
    """
    lines = [text] if isinstance(text, str) else list(text)
    extra = Inches(0.22) * (len(lines) - 1)
    box = slide.shapes.add_textbox(
        MARGIN, SLIDE_H - Inches(0.4) - extra,
        SLIDE_W - 2 * MARGIN - NUM_W - Inches(0.1),
        Inches(0.3) + extra,
    )
    box.name = "Footer"
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = PP_ALIGN.LEFT
        run = p.runs[0]
        run.font.size = Pt(size_pt)
        run.font.color.rgb = COL_MUTED
    return box


def add_slide_number(slide, n: int):
    """スライド番号を右下に配置する。"""
    box = slide.shapes.add_textbox(
        SLIDE_W - MARGIN - NUM_W, SLIDE_H - Inches(0.4), NUM_W, NUM_H
    )
    box.name = "SlideNumber"
    tf = box.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = str(n)
    p.alignment = PP_ALIGN.RIGHT
    run = p.runs[0]
    run.font.size = Pt(SZ_NUM)
    run.font.color.rgb = COL_MUTED
    return box


def s01(slide, n: int) -> None:
    """表紙。演者・カンファレンス・日時（内容契約 Slide 1 Projected body）。

    視覚: 丁場池の写真（`choba_lake_3.jpg`）を右側に大きく配置し、タイトル・
    演者情報は左揃えで残す。

    Fix round 2（レビュー指摘）: 元は `fig03_keirin_cliff.jpg`（日本語記事用に
    グレースケール化された図版）を使っていたが、島の特徴である「緑がかった水」を
    表紙で見せられないのは事故的な欠落であるとのレビュー指摘を受け、色付きの
    `choba_lake_3.jpg`（垂直な花崗岩壁＋緑がかった水面＋青空）に差し替えた
    （担当者ルーリング）。S7 パネル(a)でも同じ写真を再利用する（再認識が目的）。
    """
    add_title(slide, TITLES[0])
    cover_path = IMAGES / "choba_lake_3.jpg"
    photo_h = GRAPHIC_HEIGHT
    cover_iw, cover_ih = _image_size(cover_path)
    photo_w = int(photo_h * cover_iw / cover_ih)  # 元写真のアスペクト比に合わせ、クロップなしで大きく配置
    photo_left = SLIDE_W - MARGIN - photo_w
    add_picture_cover(slide, cover_path, photo_left, GRAPHIC_TOP, photo_w, photo_h, "Picture1")
    text_width = photo_left - MARGIN - IMAGE_TEXT_GAP
    add_body(
        slide,
        [
            "Noboru Otsuka — Geolonia Inc.",
            "FOSS4G 2026 Hiroshima",
            "2026-09-02 13:30 · Himawari",
        ],
        top=GRAPHIC_TOP, width=text_width, height=GRAPHIC_HEIGHT,
    )
    add_slide_number(slide, n)


def s02(slide, n: int) -> None:
    """島と遺産、そして残された池（内容契約 Slide 2 Projected body）。

    視覚: 位置図（`poster_f1_study_area.png`）を右側に配置。
    """
    add_title(slide, TITLES[1])
    img_max_w = Inches(6.0)
    img = add_picture_contain(
        slide, IMAGES / "poster_f1_study_area.png",
        SLIDE_W - MARGIN - img_max_w, GRAPHIC_TOP, img_max_w, GRAPHIC_HEIGHT, "Picture1",
    )
    text_width = img.left - MARGIN - IMAGE_TEXT_GAP
    add_body(
        slide,
        [
            "Kitagi Island · Kasaoka City, Okayama · Seto Inland Sea",
            "Granite quarried since the early 17th century",
            "127 active quarry sites at the 1957 peak · up to 12,000 residents",
            "Today: two working quarries · about 600–700 residents",
            "Abandoned pits filled with rain and groundwater",
            'National heritage since 2019 — "Stone Islands of Setouchi"',
            "I found no island-wide record of the ponds themselves.",
        ],
        top=GRAPHIC_TOP, width=text_width, height=GRAPHIC_HEIGHT,
    )
    add_slide_number(slide, n)


def s03(slide, n: int) -> None:
    """徒歩スケール：質感（内容契約 Slide 3 Projected body）。

    視覚: 現地写真2枚を同寸で並置。`fig01_lake_stage.jpg` と `choba_lake_1.jpg` を使う。

    Fix round 3（レビュー指摘）: `choba_lake_2.jpg`（丁場の谷を見下ろして遠景の海まで
    写した構図。水面がほぼ写っていない上、クレーンアーム・小屋が写り込む）は投影文
    `Vertical granite walls, cut not weathered` / `Water in an unusual green` を
    支持しないため不採用とし、`choba_lake_1.jpg`（垂直な花崗岩の切削面が緑がかった
    水面へ直接落ち込む構図）に差し替えた。`choba_lake_3.jpg`（表紙・S7パネル(a)で
    採用済み）とは画角が異なるため、表紙の反復にもならない。
    """
    add_title(slide, TITLES[2])
    add_body(
        slide,
        [
            "March 2026 — a drone mapping party on the island",
            "Vertical granite walls, cut not weathered",
            "Water in an unusual green; reported depths of a few metres to about twenty",
            "A stage on the water, built from leftover stone",
            "Five or six sites during the event.",
        ],
        top=GRAPHIC_TOP, height=PHOTO_TEXT_HEIGHT,
    )
    # fig01: 縦長写真をそのまま中央対称クロップすると、水面が写る下部が失われ岩壁のみに
    # なる（元画像は上2/3が岩壁・下1/3が水面のため）。水面・ステージが見える構図を
    # 残すよう上側を多くクロップする（vbias1=0.75、Task 4 から変更なし）。
    # choba_lake_1: 上部は空・稜線の樹木、中央から下は垂直な花崗岩壁、最下部が緑がかった
    # 水面（元画像1500x1999で水面は下から約22%）。中央対称クロップでは空・樹木が残って
    # しまうため、上側を大きくクロップして水面を残す（vbias2=0.85。0.70〜1.00で試作
    # クロップを目視確認し、空・稜線の崩石が完全に外れ、垂直な壁面と水面がともに
    # 十分な面積で残る構図として選定）。
    add_photo_pair(
        slide, IMAGES / "fig01_lake_stage.jpg", IMAGES / "choba_lake_1.jpg",
        vbias1=0.75, vbias2=0.85,
    )
    add_slide_number(slide, n)


def s04(slide, n: int) -> None:
    """上空スケール：境界（内容契約 Slide 4 Projected body）。

    視覚: 上空写真（`fig06_aerial_quarries.jpg`）とドローン離陸（`fig05_drone_takeoff.jpg`）。
    """
    add_title(slide, TITLES[3])
    add_body(
        slide,
        [
            "Drone flown from the stage on the water",
            "Grey rectangles cut into the green canopy",
            "Between two quarries, a thin wall left standing",
            "A property line, standing as terrain",
            "The same event added features to OpenStreetMap.",
        ],
        top=GRAPHIC_TOP, height=PHOTO_TEXT_HEIGHT,
    )
    # fig06 は再生中の動画をキャプチャした写真で、中央対称クロップだと再生バーや
    # Dockが画面に残ってしまう。採石地の水面・崖が収まり、それらが外れる範囲へ
    # 下側を多くクロップする（vbias<0.5）。fig05 は中央対称のままで問題ない。
    add_photo_pair(
        slide, IMAGES / "fig06_aerial_quarries.jpg", IMAGES / "fig05_drone_takeoff.jpg",
        vbias1=0.2768,
    )
    add_slide_number(slide, n)


def s05(slide, n: int) -> None:
    """衛星スケール：手法（内容契約 Slide 5 Projected body）。

    ルーリング（NDWI・MNDWI・NDVI の式定義そのものはノートと図版内へ）に従い、
    投影本文には合成条件（`Water if ...`）のみを置き、`(Green − NIR)` 等の個別式は
    ここに書かない（図版 P5/F4 のパネル内に別途配置される）。
    """
    add_title(slide, TITLES[4])
    img_max_w = Inches(5.4)
    img = add_picture_contain(
        slide, IMAGES / "poster_f4_index_panels.png",
        SLIDE_W - MARGIN - img_max_w, GRAPHIC_TOP, img_max_w, GRAPHIC_HEIGHT, "Picture1",
    )
    text_width = img.left - MARGIN - IMAGE_TEXT_GAP
    add_body(
        slide,
        [
            "Sentinel-2 L2A via the Microsoft Planetary Computer STAC API",
            "Summer 2025-08-02 · 0.7% cloud · 10 m analysis grid",
            "Water if (NDWI > −0.2 OR MNDWI > −0.1) AND NOT (NDVI > 0.3)",
            "Thresholds below zero: at 10 m a narrow pond is part water, part granite, part shadow",
            "A standard water-index workflow — nothing new in the method",
            "Minimum reported polygon area: 100 m²",
        ],
        top=GRAPHIC_TOP, width=text_width, height=GRAPHIC_HEIGHT,
    )
    add_slide_number(slide, n)


def s06(slide, n: int) -> None:
    """主結果：145件（内容契約 Slide 6 Projected body）。

    evidence 階層: 主結果 `145` を callout（60〜72pt、ここでは SZ_CALLOUT=66pt）、
    春季の補足値 `113` は小タイルとして本文の下限 15pt に留め、主結果より明確に
    小さくする（validator の `check_evidence_hierarchy` が検査する）。
    """
    add_title(slide, TITLES[5])
    img_max_w = Inches(5.2)
    img_height = Inches(4.4)
    img = add_picture_contain(
        slide, IMAGES / "p06_clusters_map.png",
        SLIDE_W - MARGIN - img_max_w, GRAPHIC_TOP, img_max_w, img_height, "Picture1",
    )
    text_width = img.left - MARGIN - IMAGE_TEXT_GAP
    add_body(
        slide, ["145"], SZ_CALLOUT,
        top=TITLE_TOP + TITLE_HEIGHT, left=MARGIN,
        width=Inches(3.2), height=Inches(1.3),
        bold=True, color=COL_ACCENT,
    )
    add_body(
        slide,
        [
            "intra-island water polygons ≥ 100 m², summer 2025-08-02",
            "Clustered in the north, south-east, centre and west — consistent with historical quarrying records",
            "145 detections vs 127 recorded quarry sites — a comparison of scale, not a one-to-one match",
            ("Spring 2025-03-23 — 113 polygons reported", BODY_MIN_PT),
            "These are detected water polygons, not individually field-confirmed quarry ponds.",
        ],
        top=TITLE_TOP + TITLE_HEIGHT + Inches(1.4),
        width=text_width,
        height=Inches(3.0),
    )
    add_footer(slide, "Contains modified Copernicus Sentinel data [2025].")
    add_slide_number(slide, n)


def s07(slide, n: int) -> None:
    """三つの縮尺が示すもの（内容契約 Slide 7 Projected body）。

    視覚: 三スケール合成図（`p07_three_scales.png`、英語ラベルのみ）を本文の下に
    横断的に配置する。

    Task 4 レビュー指摘の修正: 元は `fig09_multiscale.png`（日本語記事
    `docs/articles/2026_chiri-koryu-10/` と共有される図版で、パネル注記が日本語で
    焼き込まれ、(b) パネルに動画UIの写り込みがある）を使っていたが、英語のみの
    投影面という契約に抵触するため、発表専用の英語版図版に差し替えた
    （`exp002_kitagi_foss4g2026_figures.py` の `make_p07_three_scales()` が生成。
    日本語記事側の図版・生成スクリプトは変更していない）。
    """
    add_title(slide, TITLES[6])
    text_h = Inches(1.3)
    add_body(
        slide,
        [
            "On foot — texture: the cut face, the water, the depth",
            "From the air — boundaries: property lines standing as rock walls",
            "From orbit — distribution: 145 candidates across the island",
            "Not better or worse. Different things become visible.",
        ],
        top=GRAPHIC_TOP, height=text_h,
    )
    img_top = GRAPHIC_TOP + text_h + Inches(0.15)
    img_height = GRAPHIC_BOTTOM - img_top
    add_picture_contain(
        slide, IMAGES / "p07_three_scales.png",
        USABLE_LEFT, img_top, USABLE_WIDTH, img_height, "Picture1",
    )
    add_slide_number(slide, n)


def s08(slide, n: int) -> None:
    """見ていない95%：規模の対比（内容契約 Slide 8 Projected body）。

    「5〜6か所訪問」対「145件検出」という規模の対比を、2つの callout（60〜72pt）
    として並置する。
    """
    add_title(slide, TITLES[7])
    img_max_w = Inches(4.6)
    img_height = Inches(4.3)
    img = add_picture_contain(
        slide, IMAGES / "p08_visit_anchors_map.png",
        SLIDE_W - MARGIN - img_max_w, GRAPHIC_TOP, img_max_w, img_height, "Picture1",
    )
    text_width = img.left - MARGIN - IMAGE_TEXT_GAP
    add_body(
        slide, ["5–6"], SZ_CALLOUT,
        top=TITLE_TOP + TITLE_HEIGHT, left=MARGIN,
        width=Inches(2.2), height=Inches(1.1),
        bold=True, color=COL_ACCENT,
    )
    add_body(
        slide, ["145"], SZ_CALLOUT,
        top=TITLE_TOP + TITLE_HEIGHT, left=MARGIN + Inches(2.4),
        width=Inches(2.2), height=Inches(1.1),
        bold=True, color=COL_ACCENT,
    )
    add_body(
        slide,
        [
            "Five or six quarry sites visited during the event",
            "145 water polygons detected from one scene",
            "Individual ponds are not field-confirmed — no precision or recall yet",
            "Every quarry feature already mapped in OpenStreetMap overlaps one of the detections (retrieved 2026-08-23, for reference)",
            "The candidates form a finite field-check list.",
        ],
        top=TITLE_TOP + TITLE_HEIGHT + Inches(1.3),
        width=text_width,
        height=Inches(3.0),
    )
    add_slide_number(slide, n)


def s09(slide, n: int) -> None:
    """再訪（内容契約 Slide 9 Projected body）。

    視覚: 8/31 撮影分の写真2枚（撮影前は `resolve_revisit_photo()` がプレースホルダを
    返す）。`--no-revisit` 指定時は `build()` がこのスライド自体を除外する。
    """
    add_title(slide, TITLES[8])
    add_body(
        slide,
        [
            "2026-08-31 — return visit",
            "Candidates selected from the published GeoJSON",
            "Illustrative field photographs — not accuracy validation",
            "What the scan pointed at, seen from the ground.",
        ],
        top=GRAPHIC_TOP, height=PHOTO_TEXT_HEIGHT,
    )
    add_photo_pair(slide, resolve_revisit_photo(1), resolve_revisit_photo(2))
    add_slide_number(slide, n)


def s10(slide, n: int) -> None:
    """限界と次の一手（内容契約 Slide 10 Projected body）。"""
    add_title(slide, TITLES[9])
    add_body(slide, [
        "10 m resolution — ponds narrower than about 10 m are unreliable",
        "Thresholds below zero admit dark rock and shadow",
        "No precision or recall — field validation not done",
        "Next: walk the candidates · a land mask for the shoreline · higher-resolution imagery",
    ])
    add_slide_number(slide, n)


def s11(slide, n: int) -> None:
    """オープンデータ（内容契約 Slide 11 Projected body）。

    帰属・ライセンス・使用ライブラリ名は `add_footer` へ送る（11〜12pt）。
    """
    add_title(slide, TITLES[10])
    qr_size = Inches(2.6)
    img = add_picture_contain(
        slide, IMAGES / "poster_qr_repo.png",
        SLIDE_W - MARGIN - qr_size, GRAPHIC_TOP, qr_size, qr_size, "Picture1",
    )
    text_width = img.left - MARGIN - IMAGE_TEXT_GAP
    add_body(
        slide,
        [
            "Published — 145 detected polygons as GeoJSON · EPSG:4326",
            "Pipeline outputs — GeoJSON and GeoTIFF for fieldwork and heritage documentation",
            "Open-source Python pipeline · no licence fee, no imagery purchase",
            "The same workflow could be extended to other quarried islands in the Seto Inland Sea.",
        ],
        width=text_width,
        height=Inches(4.4),
    )
    add_footer(slide, [
        "rasterio · numpy · shapely · pystac-client · planetary-computer · folium",
        "Contains modified Copernicus Sentinel data [2025]. Basemaps: GSI Tiles, "
        "Geospatial Information Authority of Japan. CC BY 4.0.",
    ])
    add_slide_number(slide, n)


def s12(slide, n: int) -> None:
    """地図への還元（内容契約 Slide 12 Projected body）。

    視覚: 「衛星 → 現地 → 地図」の3ステップフロー（`p12_loop_diagram.png`）を
    本文の下に横断的に配置。
    """
    add_title(slide, TITLES[11])
    text_h = Inches(1.9)
    add_body(
        slide,
        [
            "Satellite scan → a finite candidate list",
            "Field visit → see it with your own eyes",
            "OpenStreetMap → put what you confirmed on the public map",
            "I plan to contribute the ponds I can confirm.",
            "The March mapping party added features observed on the ground. The scan suggests where to look next.",
            "Thank you · Q&A",
        ],
        top=GRAPHIC_TOP, height=text_h,
    )
    img_top = GRAPHIC_TOP + text_h + Inches(0.15)
    img_height = GRAPHIC_BOTTOM - img_top
    add_picture_contain(
        slide, IMAGES / "p12_loop_diagram.png",
        USABLE_LEFT, img_top, USABLE_WIDTH, img_height, "Picture1",
    )
    add_slide_number(slide, n)


def build(revisit: bool = True) -> Presentation:
    """12枚（`revisit=False` の場合は S9 を除いた11枚）の Presentation を組み立てる。

    `revisit` は CLI の `--no-revisit`（`main()` 参照）から渡される。
    """
    prs = Presentation()
    prs.slide_width, prs.slide_height = SLIDE_W, SLIDE_H

    slides = [s01, s02, s03, s04, s05, s06, s07, s08]
    if revisit:
        slides.append(s09)
    slides += [s10, s11, s12]

    for n, fn in enumerate(slides, start=1):
        fn(prs.slides.add_slide(prs.slide_layouts[6]), n)

    cp = prs.core_properties
    cp.created = FIXED_DATETIME
    cp.modified = FIXED_DATETIME
    cp.last_modified_by = FIXED_LAST_MODIFIED_BY
    cp.revision = FIXED_REVISION
    cp.author = FIXED_AUTHOR
    cp.title = TITLES[0]

    return prs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-revisit",
        action="store_true",
        help=(
            "S9（8/31 再訪スライド）を除いた11枚を "
            "exp002_kitagi_foss4g2026_presentation_no_revisit.pptx として出力する"
        ),
    )
    args = parser.parse_args()

    revisit = not args.no_revisit
    out = NO_REVISIT_OUTPUT if args.no_revisit else OUTPUT
    prs = build(revisit=revisit)
    prs.save(out)
    _normalize_zip_timestamps(out)
    print(f"saved: {out} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
