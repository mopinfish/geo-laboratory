#!/usr/bin/env python3
"""FOSS4G 2026 北木島 口頭発表の成果物を検査する。

図版（P6・P8・P12）と PPTX 本体（スライド数・タイトル）の検査を実装する。後続タスク
（スピーカーノート・数値照合等）はこのファイルに追記していく前提の構造とする。

使い方: uv run python docs/presentations/validate_exp002_kitagi_foss4g2026_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation

BASE = Path(__file__).resolve().parent
IMAGES = BASE / "images"
PPTX = BASE / "exp002_kitagi_foss4g2026_presentation.pptx"

# 配置幅 220 mm で 200 dpi を満たす最小ピクセル幅
MIN_WIDTH_PX = int(220 / 25.4 * 200)  # 1732

FIGURES = ("p06_clusters_map.png", "p08_visit_anchors_map.png", "p12_loop_diagram.png")

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


def main() -> None:
    check_figures()
    check_pptx_titles()

    if errors:
        print(f"FAIL ({len(errors)} / {checks} checks failed)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"OK: {checks} checks passed")


if __name__ == "__main__":
    main()
