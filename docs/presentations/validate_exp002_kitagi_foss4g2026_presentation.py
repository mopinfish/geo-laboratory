#!/usr/bin/env python3
"""FOSS4G 2026 北木島 口頭発表の成果物を検査する。

図版（P6・P8・P12）、PPTX 本体（スライド数・タイトル・画像数・callout の文字サイズ）、
再訪なし版（`--no-revisit` で生成される11枚版）を検査する。後続タスク
（スピーカーノート・数値照合等）はこのファイルに追記していく前提の構造とする。

使い方: uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

BASE = Path(__file__).resolve().parent
IMAGES = BASE / "images"
PPTX = BASE / "exp002_kitagi_foss4g2026_presentation.pptx"
NO_REVISIT_PPTX = BASE / "exp002_kitagi_foss4g2026_presentation_no_revisit.pptx"

# 配置幅 220 mm で 200 dpi を満たす最小ピクセル幅
MIN_WIDTH_PX = int(220 / 25.4 * 200)  # 1732

FIGURES = ("p06_clusters_map.png", "p08_visit_anchors_map.png", "p12_loop_diagram.png")

# 各スライドの画像（PICTURE シェイプ）の期待枚数。S9 は8/31撮影分（未着の間はプレースホルダ）
# 2枚、S10 はテキスト中心のため意図的に0枚。
EXPECTED_IMAGES: dict[int, int] = {
    1: 1, 2: 1, 3: 2, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1, 9: 2, 11: 1, 12: 1,
}

# callout（S6 の `145`、S8 の `5–6`・`145`）が満たすべき文字サイズの範囲（pt）。
CALLOUT_MIN_PT = 60.0
CALLOUT_MAX_PT = 72.0
CALLOUT_TARGETS: dict[int, list[str]] = {6: ["145"], 8: ["5–6", "145"]}

# 内容契約（docs/presentations/exp002_kitagi_foss4g2026_presentation.md）の
# `## Slide N — ` 見出しから転記した、各スライドのタイトル完全一致文字列。
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

# 内容契約の `Projected body` から転記した、スライド別の必須文字列（機械検査対象の部分集合）。
REQUIRED_STRINGS: dict[int, list[str]] = {
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

# (禁止パターン, 許容される否定形パターン（None なら常に禁止）, 説明)。
# 否定形にマッチする範囲に完全に包含される禁止パターンの一致は許容する
# （例: "not individually field-confirmed quarry ponds" は許容し、
#  裸の "confirmed quarry ponds" は禁止する）。
FORBIDDEN: list[tuple[str, str | None, str]] = [
    (r"confirmed quarry pond", r"not\s+(?:individually\s+)?(?:field[-\s])?confirmed quarry pond",
     "現地確認済みと読める表現"),
    (r"\b145 quarry ponds?\b", None, "検出を丁場池と同一視"),
    (r"high accuracy|accuracy is high", None, "精度主張"),
    (r"\bposter\b", None, "採択形式は口頭発表"),
    (r"one-to-one match", r"not\s+(?:a\s+)?one-to-one match", "1対1対応と読める表現"),
]

BODY_MIN_PT = 15  # 生成スクリプト側の下限（exp002_kitagi_foss4g2026_presentation.py と同値）

errors: list[str] = []
checks = 0


def check(cond: bool, msg: str) -> None:
    global checks
    checks += 1
    if not cond:
        errors.append(msg)


def check_figures() -> None:
    """P6・P8・P12 の図版が存在し、配置幅220mm・200dpiの下限を満たすことを確認する。"""
    for name in FIGURES:
        path = IMAGES / name
        check(path.is_file(), f"図版が存在しない: {name}")
        if path.is_file():
            width, height = Image.open(path).size
            check(width >= MIN_WIDTH_PX, f"{name}: 幅 {width}px が下限 {MIN_WIDTH_PX}px 未満")
            check(height > 0, f"{name}: 高さが不正")


def check_pptx_titles() -> None:
    """PPTX が12枚のスライドを持ち、各スライドのタイトル用シェイプ（name="Title"）が
    内容契約のタイトル文字列と完全一致し、数字で始まっていないことを確認する。

    ブリーフの原案（`title in texts[i]` による部分一致＋番号プレフィックスの雑な検出）は
    誤検出・見逃しの両方向で信頼できないため採用しない。代わりにタイトル用シェイプを
    name="Title" で明示的に識別し、テキストの完全一致と先頭文字が数字でないことを
    それぞれ独立に検査する。
    """
    check(PPTX.is_file(), "PPTX が存在しない")
    if not PPTX.is_file():
        return

    prs = Presentation(PPTX)
    check(len(prs.slides) == 12, f"スライド数が12でない: {len(prs.slides)}")

    slides = list(prs.slides)
    for i, expected in enumerate(TITLES):
        label = f"S{i + 1}"
        if i >= len(slides):
            check(False, f"{label}: スライドが存在しない")
            continue
        title_shapes = [
            sh for sh in slides[i].shapes
            if sh.has_text_frame and sh.name == "Title"
        ]
        check(
            len(title_shapes) == 1,
            f"{label}: タイトル用シェイプ(name='Title')が1つでない: {len(title_shapes)}個",
        )
        text = title_shapes[0].text_frame.text if len(title_shapes) == 1 else ""
        check(text == expected, f"{label}: タイトルが完全一致しない — 期待 '{expected[:40]}...'")
        check(not text[:1].isdigit(), f"{label}: タイトル先頭が数字で始まっている")


def _slide_text(slide) -> str:
    """スライド内の全テキストフレームの文字列を改行区切りで連結する。"""
    return "\n".join(
        sh.text_frame.text for sh in slide.shapes if sh.has_text_frame
    )


def check_required_strings(prs: Presentation) -> None:
    """各スライドの投影文字列が、内容契約の `Projected body` から転記した
    `REQUIRED_STRINGS` の全文字列を部分文字列として含むことを確認する。
    """
    slides = list(prs.slides)
    for i, needles in REQUIRED_STRINGS.items():
        label = f"S{i}"
        if i > len(slides):
            for needle in needles:
                check(False, f"{label}: スライドが存在しない（必須文字列 '{needle}' を検査不可）")
            continue
        text = _slide_text(slides[i - 1])
        for needle in needles:
            check(needle in text, f"{label}: 必須文字列が見つからない — '{needle}'")


def check_forbidden(prs: Presentation) -> None:
    """`FORBIDDEN` の禁止表現が、許容される否定形（例: 'not ... confirmed quarry
    ponds'）の範囲外で裸に使われていないことを確認する。

    否定形パターンが与えられている場合、禁止パターンの一致区間が否定形の
    一致区間に完全に包含されていれば許容する（例が S6 に実在する
    'not individually field-confirmed quarry ponds'）。それ以外の一致は禁止表現の
    使用として検査失敗にする。
    """
    for i, slide in enumerate(prs.slides, start=1):
        text = _slide_text(slide)
        for positive, allowed, desc in FORBIDDEN:
            allowed_spans = [m.span() for m in re.finditer(allowed, text)] if allowed else []
            bad = [
                m for m in re.finditer(positive, text)
                if not any(a0 <= m.start() and m.end() <= a1 for a0, a1 in allowed_spans)
            ]
            check(
                not bad,
                f"S{i}: 禁止表現 '{bad[0].group(0) if bad else ''}' — {desc}",
            )


def check_evidence_hierarchy(prs: Presentation) -> None:
    """evidence 階層を検査する。

    - S5: 式（`(Green − NIR)` 等）は投影本文のテキストフレームに置かず、図版内に
      置く（この検査は投影本文に存在しないことのみを確認する）。
    - S6: 春季タイル（`113`）は主結果（`145`）より小さい文字サイズであることを
      確認する。
    """
    slides = list(prs.slides)
    if len(slides) >= 5:
        s5_text = _slide_text(slides[4])
        for formula in ("(Green − NIR)", "(Green + NIR)", "(Green − SWIR)"):
            check(formula not in s5_text, f"S5: 式 '{formula}' が投影本文にある（図版内へ置く）")

    def max_font_pt(slide, needle: str) -> float:
        sizes = [
            run.font.size.pt
            for sh in slide.shapes if sh.has_text_frame
            for para in sh.text_frame.paragraphs for run in para.runs
            if needle in run.text and run.font.size is not None
        ]
        return max(sizes) if sizes else 0.0

    if len(slides) >= 6:
        s6 = slides[5]
        check(
            max_font_pt(s6, "145") > max_font_pt(s6, "113"),
            "S6: 春季113が主結果145以上の大きさになっている",
        )


def check_image_counts(prs: Presentation) -> None:
    """各スライドの画像（PICTURE シェイプ）数が `EXPECTED_IMAGES` と一致することを確認する。

    未記載のスライド（S10）は期待値0（意図的にテキストのみ・余白を広く取る）。
    """
    for i, slide in enumerate(prs.slides, start=1):
        n_pic = sum(1 for sh in slide.shapes if sh.shape_type == MSO_SHAPE_TYPE.PICTURE)
        expected = EXPECTED_IMAGES.get(i, 0)
        check(n_pic == expected, f"S{i}: 画像数 {n_pic} が期待値 {expected} と不一致")


def check_callout_range(prs: Presentation) -> None:
    """S6 の `145`、S8 の `5–6`・`145` の callout が 60〜72pt の範囲にあることを確認する。

    Task 3 レビューの Minor 指摘: この範囲を固定する検査がなく、将来の編集で
    callout が意図せず縮小・拡大されても検査が通り続けてしまう問題への対処。
    """
    slides = list(prs.slides)
    for idx, needles in CALLOUT_TARGETS.items():
        label = f"S{idx}"
        if idx > len(slides):
            for needle in needles:
                check(False, f"{label}: callout '{needle}' を検査不可（スライドが存在しない）")
            continue
        slide = slides[idx - 1]
        for needle in needles:
            sizes = [
                run.font.size.pt
                for sh in slide.shapes if sh.has_text_frame
                for para in sh.text_frame.paragraphs for run in para.runs
                if run.text.strip() == needle and run.font.size is not None
            ]
            check(bool(sizes), f"{label}: callout '{needle}' の文字サイズが見つからない")
            for pt in sizes:
                check(
                    CALLOUT_MIN_PT <= pt <= CALLOUT_MAX_PT,
                    f"{label}: callout '{needle}' が {pt}pt — {CALLOUT_MIN_PT:.0f}〜{CALLOUT_MAX_PT:.0f}pt の範囲外",
                )


def check_no_revisit_variant() -> None:
    """`--no-revisit` で生成される11枚版が存在し、S9 が除外されていることを確認する。"""
    if not NO_REVISIT_PPTX.is_file():
        check(False, "再訪なし版のPPTXが存在しない")
        return
    prs2 = Presentation(NO_REVISIT_PPTX)
    check(len(prs2.slides) == 11, f"再訪なし版のスライド数が11でない: {len(prs2.slides)}")
    t2 = "\n".join(sh.text_frame.text for s in prs2.slides for sh in s.shapes if sh.has_text_frame)
    check("2026-08-31" not in t2, "再訪なし版に再訪スライドが残っている")


def check_font_floor(prs: Presentation) -> None:
    """本文の文字サイズが15pt未満に自動縮小されていないことを確認する。

    数字のみのラン（スライド番号や callout の裸の数値）と 12pt 以下のラン
    （footer・スライド番号として意図されたもの）は例外として許容する。
    """
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
                    check(
                        pt >= BODY_MIN_PT or is_number_or_footer,
                        f"S{i}: 本文 {pt}pt が {BODY_MIN_PT}pt 未満 — '{run.text[:30]}'",
                    )


def main() -> None:
    check_figures()
    check_pptx_titles()

    if PPTX.is_file():
        prs = Presentation(PPTX)
        check_required_strings(prs)
        check_forbidden(prs)
        check_evidence_hierarchy(prs)
        check_font_floor(prs)
        check_image_counts(prs)
        check_callout_range(prs)

    check_no_revisit_variant()

    if errors:
        print(f"FAIL ({len(errors)} / {checks} checks failed)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"OK: {checks} checks passed")


if __name__ == "__main__":
    main()
