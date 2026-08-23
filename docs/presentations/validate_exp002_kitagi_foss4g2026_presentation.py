#!/usr/bin/env python3
"""FOSS4G 2026 北木島 口頭発表の成果物を検査する。

現時点では図版（P6・P8・P12）の検査のみを実装する。後続タスク（PPTX本体・
スピーカーノート・数値照合等）はこのファイルに追記していく前提の構造とする。

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


def check_figures() -> None:
    """P6・P8・P12 の図版が存在し、配置幅220mm・200dpiの下限を満たすことを確認する。"""
    for name in FIGURES:
        path = IMAGES / name
        check(path.is_file(), f"図版が存在しない: {name}")
        if path.is_file():
            width, height = Image.open(path).size
            check(width >= MIN_WIDTH_PX, f"{name}: 幅 {width}px が下限 {MIN_WIDTH_PX}px 未満")
            check(height > 0, f"{name}: 高さが不正")


def main() -> None:
    check_figures()

    if errors:
        print(f"FAIL ({len(errors)} / {checks} checks failed)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"OK: {checks} checks passed")


if __name__ == "__main__":
    main()
