#!/usr/bin/env python3
"""FOSS4G 2026 北木島 口頭発表（英語・12枚）の PPTX を生成する。

このタスク（骨格）では各スライドに「タイトル」と「スライド番号」のみを配置する。
本文・画像・フッター・スピーカーノートは後続タスク（Task 3〜5）で追記する。

タイトル文字列は内容契約（docs/presentations/exp002_kitagi_foss4g2026_presentation.md）
の `## Slide N — ` 見出しから転記した完全一致文字列。

決定性（determinism）: 生成される .pptx はコミット対象であり、再生成しても
バイト単位で同一になる必要がある。python-pptx が自動的にスタンプしうる
docProps/core.xml のプロパティ（created / modified / last_modified_by /
revision / author / title）はすべて固定リテラル値で明示的に上書きする。

使い方: uv run python docs/presentations/exp002_kitagi_foss4g2026_presentation.py
"""

from __future__ import annotations

import datetime as dt
import io
import zipfile
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / "exp002_kitagi_foss4g2026_presentation.pptx"

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
SZ_NOTE = 14
SZ_NUM = 11
BODY_MIN_PT = 15  # 本文はこの下限を下回ってはならない

# --- 配色 ---
COL_TEXT = RGBColor(0x2B, 0x2B, 0x2B)
COL_ACCENT = RGBColor(0x0D, 0x47, 0xA1)
COL_MUTED = RGBColor(0x5A, 0x56, 0x4E)

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


def add_body(slide, lines: list[str], size_pt: int = SZ_BODY):
    """本文用テキストボックスを配置する（Task 3 で使用予定。本タスクでは呼ばれない）。

    `size_pt` は BODY_MIN_PT（15pt）を下回ってはならない。
    """
    if size_pt < BODY_MIN_PT:
        raise ValueError(f"body size_pt={size_pt} は下限 {BODY_MIN_PT}pt を下回っている")
    box = slide.shapes.add_textbox(
        MARGIN, TITLE_TOP + TITLE_HEIGHT, SLIDE_W - 2 * MARGIN,
        SLIDE_H - TITLE_TOP - TITLE_HEIGHT - Inches(0.5),
    )
    box.name = "Body"
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = PP_ALIGN.LEFT
        run = p.runs[0]
        run.font.size = Pt(size_pt)
        run.font.color.rgb = COL_TEXT
    return box


def add_footer(slide, text: str):
    """フッター用テキストボックスを配置する（Task 5 で使用予定。本タスクでは呼ばれない）。"""
    box = slide.shapes.add_textbox(
        MARGIN, SLIDE_H - Inches(0.4), SLIDE_W - 2 * MARGIN - NUM_W - Inches(0.1),
        Inches(0.3),
    )
    box.name = "Footer"
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.LEFT
    run = p.runs[0]
    run.font.size = Pt(SZ_NOTE)
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


def _make_slide(index: int):
    """`index`（0始まり、TITLES のインデックス）に対応する `sNN(slide, n)` を返す。"""

    def _fn(slide, n: int) -> None:
        add_title(slide, TITLES[index])
        add_slide_number(slide, n)

    return _fn


s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12 = (
    _make_slide(i) for i in range(12)
)


def build(revisit: bool = True) -> Presentation:
    """12枚（`revisit=False` の場合は S9 を除いた11枚）の Presentation を組み立てる。

    `revisit` による S9 の除外オプションは Task 4 で CLI（`--no-revisit`）として
    公開される。本タスクではデフォルト（`revisit=True`）で常に12枚を生成する。
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
    prs = build()
    prs.save(OUTPUT)
    _normalize_zip_timestamps(OUTPUT)
    print(f"saved: {OUTPUT} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
