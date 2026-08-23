#!/usr/bin/env python3
"""口頭説明スクリプト・想定問答集の整合性チェック。

検証内容:
1. 両ファイルの存在
2. Tier 1（ポスター掲載値）の必須出現と、Tier 定義の明文化
3. 禁止表現（過大主張）の不在
   - 除外は「§0-3 NG例表の ✗ セル」のみ。他の表は除外しない
   - 否定は対象句を直接否定する構文のみ許容（行中の任意の not では免除しない）
4. Tier 2（報告書由来の補足値）の出現位置制約
   - 口頭スクリプトの 30秒版 / 2〜3分版には出現しない
   - それ以外では [report] / [報告書] の出典マーカーと同一行に置く
   - 丁場跡の水深（報告書由来）は出典マーカー必須
5. 想定問答の英日併記・根拠欄の構造
6. 想定問答の必須カバー範囲
7. 禁止表現チェッカ自体の回帰テスト（悪性例が落ち、正しい否定例が通ること）

使い方: uv run python docs/posters/validate_exp002_kitagi_foss4g2026_talk_materials.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
TALK = BASE / "exp002_kitagi_foss4g2026_talk_script.md"
QA = BASE / "exp002_kitagi_foss4g2026_qa.md"

# --- Tier 1: ポスター掲載値（主要な抜粋。網羅列挙ではない）---
TIER1 = ["113", "145", "127", "9 px", "100 m²", "10 m", "2025-03-23", "2025-08-02", "−0.2", "−0.1", "0.3"]

# --- Tier 2: ポスターに無く報告書のみに基づく補足値 ---
TIER2 = ["180", "7,826", "72,636", "215,984", "212,80", "0.210", "1.000",
         "S2C_MSIL2A", "S2A_MSIL2A", "T53SLU", "EPSG:32653"]
MARKER = ("[report", "[報告書")

# --- 禁止表現（過大主張）。allow は対象句を直接否定する構文のみ ---
FORBIDDEN = [
    (r"confirmed quarry pond",
     r"not\s+(?:individually\s+)?(?:field[-\s])?confirmed quarry pond",
     "「現地確認済みの丁場池」は直接否定する構文以外で使用しない"),
    (r"\b145 quarry ponds?\b", None, "検出ポリゴンを丁場池と同一視している"),
    (r"high accuracy|accuracy is high", None, "精度指標は未算出のため精度主張は不可"),
    (r"one-to-one match", r"not\s+(?:a\s+)?one-to-one match",
     "145対127を1対1対応と読める表現"),
]

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


def scannable_spans(text: str) -> list[tuple[int, str]]:
    """禁止表現の走査対象。§0-3 の NG例表だけ ✗ セル（1列目）を除外する。"""
    out: list[tuple[int, str]] = []
    in_ng_table = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("###") or line.startswith("##"):
            in_ng_table = line.startswith("### 0-3.")
        if in_ng_table and line.lstrip().startswith("|"):
            cells = line.split("|")
            out.append((i, "|".join(cells[2:])))  # ✓ 列以降のみ走査
        else:
            out.append((i, line))
    return out


def forbidden_hits(text: str) -> list[tuple[int, str, str]]:
    hits = []
    for lineno, line in scannable_spans(text):
        for pattern, allow, why in FORBIDDEN:
            for m in re.finditer(pattern, line, re.IGNORECASE):
                if allow and any(
                    a.start() <= m.start() and m.end() <= a.end()
                    for a in re.finditer(allow, line, re.IGNORECASE)
                ):
                    continue
                hits.append((lineno, m.group(0), why))
    return hits


def section(text: str, start: str, end: str | None) -> str:
    i = text.index(start)
    j = text.index(end) if end else len(text)
    return text[i:j]


# 0. 回帰テスト（チェッカ自体の健全性）
MALICIOUS = [
    "We detected 145 quarry ponds, though they are not field-validated.",
    "There is a notable one-to-one match with the historical records.",
    "| context | These are confirmed quarry ponds |",
    "The accuracy is high for this workflow.",
    "not really confirmed quarry ponds in any sense",  # 直接否定でない
]
BENIGN = [
    "These are detected water polygons, not individually field-confirmed quarry ponds.",
    "It is a scale comparison, not a one-to-one match.",
    "We detected 145 water polygons — quarry pond candidates.",
]
for case in MALICIOUS:
    check(bool(forbidden_hits(case)), f"回帰テスト失敗（検出されるべき）: {case}")
for case in BENIGN:
    check(not forbidden_hits(case), f"回帰テスト失敗（通るべき）: {case}")

# 1. ファイル存在
for path in (TALK, QA):
    check(path.is_file(), f"ファイルが存在しない: {path.name}")
if errors:
    print("\n".join(f"FAIL: {e}" for e in errors))
    sys.exit(1)

talk = TALK.read_text(encoding="utf-8")
qa = QA.read_text(encoding="utf-8")

# 2. Tier 1 の必須出現と Tier 定義の明文化
for value in TIER1:
    check(value in talk, f"口頭スクリプトに Tier 1 値が無い: {value}")
    check(value in qa, f"想定問答に Tier 1 値が無い: {value}")
tier_table = section(talk, "### 0-2.", "### 0-3.")
for value in ("0.0% / 0.7%", "20 m"):
    check(value in tier_table, f"口頭スクリプトの Tier 1 表にポスター掲載値が無い: {value}")
check("Tier 1 の定義" in tier_table and "網羅列挙ではない" in tier_table,
      "Tier 1 の定義（ポスター掲載値すべて／表は抜粋）が明文化されていない")
check("網羅列挙ではない" in qa, "想定問答の Tier 1 定義が口頭スクリプトと一致していない")

# 3. 禁止表現
for label, text in (("口頭スクリプト", talk), ("想定問答", qa)):
    for lineno, hit, why in forbidden_hits(text):
        check(False, f"{label} L{lineno}: 禁止表現 '{hit}' — {why}")

# 4a. 要約版（30秒版・2〜3分版）に Tier 2 が混入していないか
summary = section(talk, "## 1. 30秒版", "## 3. 5分版")
for value in TIER2:
    check(value not in summary, f"30秒版/2〜3分版に Tier 2 値が混入: {value}")

# 4b. Tier 2 は出典マーカーと同一行（両ファイル）
for label, text in (("口頭スクリプト", talk), ("想定問答", qa)):
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("| **") or line.lstrip().startswith("- 根拠:"):
            continue  # Tier 表・根拠欄は出典そのもの
        hits = [v for v in TIER2 if v in line]
        if hits and not any(mk in line for mk in MARKER):
            check(False, f"{label} L{lineno}: Tier 2 値 {hits} に出典マーカーが無い")

# 4c. 丁場跡の水深（報告書由来）は出典マーカー必須
for label, text in (("口頭スクリプト", talk), ("想定問答", qa)):
    for lineno, line in enumerate(text.splitlines(), 1):
        if re.search(r"reported depths|深さは数m", line) and not any(mk in line for mk in MARKER):
            check(False, f"{label} L{lineno}: 水深の記述に出典マーカーが無い")

# 5. 想定問答の構造（英日併記・根拠欄）
blocks = re.split(r"^### ", qa, flags=re.MULTILINE)[1:]
qblocks = [b for b in blocks if b.startswith("Q")]
check(len(qblocks) >= 30, f"想定問答の項目数が不足: {len(qblocks)}")
for b in qblocks:
    qid = b.split(".")[0]
    for field in ("- **JP:**", "- **A (EN):**", "- **A (JP):**", "- 根拠:"):
        check(field in b, f"想定問答 {qid}: 必須欄が無い {field}")

# 6. 想定問答のカバー範囲
for topic, keys in REQUIRED_QA_TOPICS.items():
    for key in keys:
        check(key in qa, f"想定問答の必須カバー範囲が欠落: {topic} — '{key}'")

# 7. 口頭スクリプトの構成
for heading in ("### 0-1. 1画面カード", "## 1. 30秒版", "## 2. 2〜3分版", "## 3. 5分版"):
    check(heading in talk, f"口頭スクリプトに節が無い: {heading}")
card = section(talk, "### 0-1.", "### 0-2.")
check("|" not in card, "1画面カードに表が含まれている（1画面に収まらない）")
check(len(card.splitlines()) <= 16, f"1画面カードが長すぎる: {len(card.splitlines())} 行")
# 現行前提（口頭発表）の記載
check("Regular Talk" in talk, "口頭スクリプトに採択形式（Regular Talk）の記載が無い")
check("13:30–14:00" in talk, "口頭スクリプトに登壇時刻の記載が無い")
check("Himawari" in talk, "口頭スクリプトに登壇会場の記載が無い")
check("前提訂正（2026-08-23）" in talk, "冒頭の前提訂正の告知が無い")

# 旧ポスター前提の断定が残っていないこと（廃止記述としての言及は許容）
STALE = [
    (r"本ポスターの掲載枠", "Himawari 枠をポスター掲載枠とする旧前提"),
    (r"別会場でのトークがある", "在席要否が未確認という旧前提"),
    (r"(?<!旧版は)コアタイムは \*\*9月2日", "ポスターコアタイムを基準とする旧運用"),
]
for lineno, line in enumerate(talk.splitlines(), 1):
    if "廃止" in line or "旧版" in line:
        continue  # 廃止済みとして言及している行は対象外
    for pattern, why in STALE:
        if re.search(pattern, line):
            check(False, f"口頭スクリプト L{lineno}: 旧ポスター前提が残っている — {why}")

if errors:
    print(f"FAIL ({len(errors)} / {checks} checks failed)")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"OK: {checks} checks passed")
print(f"  talk script: {len(talk):,} chars")
print(f"  Q&A: {len(qa):,} chars, {len(qblocks)} questions")
