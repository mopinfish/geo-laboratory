#!/usr/bin/env python3
"""口頭説明スクリプト・想定問答集の整合性チェック。

検証内容:
1. 両ファイルの存在
2. Tier 1（ポスター掲載の確定値）の必須出現
3. 禁止表現（過大主張）の不在 — NG例を列挙した表の行は対象外
4. Tier 2（報告書由来の補足値）の出現位置制約
   - 口頭スクリプトの 30秒版 / 2〜3分版には出現しない
   - 想定問答では [report] / [報告書] の出典マーカーと同一行に置く
5. 想定問答の英日併記・根拠欄の構造
6. 想定問答の必須カバー範囲

使い方: uv run python docs/posters/validate_exp002_kitagi_foss4g2026_talk_materials.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
TALK = BASE / "exp002_kitagi_foss4g2026_talk_script.md"
QA = BASE / "exp002_kitagi_foss4g2026_qa.md"

# --- Tier 1: ポスターに掲載された確定値 ---
TIER1 = ["113", "145", "127", "9 px", "100 m²", "10 m", "2025-03-23", "2025-08-02", "−0.2", "−0.1", "0.3"]

# --- Tier 2: 報告書由来の補足値（出典マーカー必須・要約版では禁止） ---
TIER2 = ["180", "7,826", "1.28", "399", "72,636", "215,984", "212,80", "0.210", "1.000",
         "S2C_MSIL2A", "S2A_MSIL2A", "T53SLU", "EPSG:32653"]

# --- 禁止表現（過大主張）---
FORBIDDEN = [
    (r"confirmed quarry pond", "「現地確認済みの丁場池」は否定形以外で使用しない"),
    (r"\b145 quarry ponds?\b", "検出ポリゴンを丁場池と同一視している"),
    (r"high accuracy|accuracy is high", "精度指標は未算出のため精度主張は不可"),
    (r"one-to-one match", "145対127を1対1対応と読める表現"),
]
# 上記のうち、同一行に否定語があれば許容するもの
NEGATABLE = {"confirmed quarry pond": ("not", "never", "✗", "n't", "使わない", "言わない"),
             "one-to-one match": ("not",)}

REQUIRED_QA_TOPICS = {
    "手法（指数の選択理由）": ["NDWI", "MNDWI"],
    "閾値の根拠": ["threshold", "histogram"],
    "季節差": ["seasonal", "spring"],
    "偽陽性": ["false positive", "shadow"],
    "現地検証": ["precision and recall", "field"],
    "春季再現性": ["not preserved", "180"],
    "解像度の限界": ["spectral mixing", "one Sentinel-2 pixel"],
    "127丁場との対応": ["scale, not a one-to-one", "127"],
    "瀬戸内展開": ["Seto Inland Sea"],
    "データ入手": ["GeoJSON", "GeoTIFF", "github.com/mopinfish/geo-laboratory"],
    "ライセンス": ["CC BY 4.0", "Copernicus"],
}

errors: list[str] = []
checks = 0


def check(cond: bool, msg: str) -> None:
    global checks
    checks += 1
    if not cond:
        errors.append(msg)


def prose_lines(text: str) -> list[tuple[int, str]]:
    """表の行（NG例の列挙を含む）を除いた本文行。"""
    return [(i, ln) for i, ln in enumerate(text.splitlines(), 1) if not ln.lstrip().startswith("|")]


def section(text: str, start: str, end: str | None) -> str:
    i = text.index(start)
    j = text.index(end) if end else len(text)
    return text[i:j]


# 1. ファイル存在
for path in (TALK, QA):
    check(path.is_file(), f"ファイルが存在しない: {path.name}")
if errors:
    print("\n".join(f"FAIL: {e}" for e in errors))
    sys.exit(1)

talk = TALK.read_text(encoding="utf-8")
qa = QA.read_text(encoding="utf-8")

# 2. Tier 1 の必須出現
for value in TIER1:
    check(value in talk, f"口頭スクリプトに Tier 1 値が無い: {value}")
    check(value in qa, f"想定問答に Tier 1 値が無い: {value}")

# 3. 禁止表現
for label, text in (("口頭スクリプト", talk), ("想定問答", qa)):
    for pattern, why in FORBIDDEN:
        for lineno, line in prose_lines(text):
            m = re.search(pattern, line, re.IGNORECASE)
            if not m:
                continue
            allowed = NEGATABLE.get(m.group(0).lower(), ())
            if allowed and any(tok in line.lower() for tok in allowed):
                continue
            check(False, f"{label} L{lineno}: 禁止表現 '{m.group(0)}' — {why}")

# 4a. 要約版に Tier 2 が混入していないか
summary = section(talk, "## 1. 30秒版", "## 3. 5分版")
for value in TIER2:
    check(value not in summary, f"30秒版/2〜3分版に Tier 2 値が混入: {value}")

# 4b. 想定問答の Tier 2 は出典マーカーと同一行
for lineno, line in prose_lines(qa):
    hits = [v for v in TIER2 if v in line]
    if not hits:
        continue
    check("[report" in line or "[報告書" in line or "根拠:" in line.strip()[:4] or line.lstrip().startswith("- 根拠:"),
          f"想定問答 L{lineno}: Tier 2 値 {hits} に出典マーカー([report]/[報告書])が無い")

# 5. 想定問答の構造（英日併記・根拠欄）
blocks = re.split(r"^### ", qa, flags=re.MULTILINE)[1:]
qblocks = [b for b in blocks if b.startswith("Q")]
check(len(qblocks) >= 20, f"想定問答の項目数が不足: {len(qblocks)}")
for b in qblocks:
    qid = b.split(".")[0]
    for field in ("- **JP:**", "- **A (EN):**", "- **A (JP):**", "- 根拠:"):
        check(field in b, f"想定問答 {qid}: 必須欄が無い {field}")

# 6. 想定問答のカバー範囲
for topic, keys in REQUIRED_QA_TOPICS.items():
    for key in keys:
        check(key in qa, f"想定問答の必須カバー範囲が欠落: {topic} — '{key}'")

# 7. 口頭スクリプトの3段構え
for heading in ("## 1. 30秒版", "## 2. 2〜3分版", "## 3. 5分版"):
    check(heading in talk, f"口頭スクリプトに節が無い: {heading}")
check("Sakura Lounge" in talk, "口頭スクリプトにコアタイム会場の記載が無い")
check("13:00–15:00" in talk, "口頭スクリプトにコアタイムの記載が無い")

if errors:
    print(f"FAIL ({len(errors)} / {checks} checks failed)")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"OK: {checks} checks passed")
print(f"  talk script: {len(talk):,} chars")
print(f"  Q&A: {len(qa):,} chars, {len(qblocks)} questions")
