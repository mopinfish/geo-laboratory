#!/usr/bin/env python3
"""FOSS4G 2026 北木島 口頭発表の成果物を検査する。

図版（P6・P8・P12）、PPTX 本体（スライド数・タイトル・画像数・callout の文字サイズ）、
再訪なし版（`--no-revisit` で生成される11枚版）、スピーカーノート Markdown
（構造・英語語数・S6 の required spoken content）と PPTX ノートペインとの同期を検査する。
後続タスク（数値照合等）はこのファイルに追記していく前提の構造とする。

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
NOTES_MD = BASE / "exp002_kitagi_foss4g2026_presentation_speaker_notes.md"

# スピーカーノートの英語発話量の判定基準。内容契約「タイミング」節の秒数（合計1,050秒）を
# 145 wpm で語数へ換算し、±25% の幅で判定する。
WPM = 145
DURATIONS_S = [35, 100, 90, 90, 110, 150, 70, 90, 110, 80, 70, 55]
WORD_TOLERANCE = 0.25

# ノート Markdown 内の構造マーカー。英語（発話対象）と日本語（非発話）の境界。
EN_MARKER = "**EN (spoken)**"
JA_MARKER = "**JA (not spoken)**"

# 内容契約 Slide 6 の `Required spoken content`。内部注記ではなく英語の発話本文に
# 置くことが契約上の要件であるため、S6 の EN 部分に対する部分文字列一致で検査する。
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

# 再訪なし版（11枚）の各スライド位置に対応する内容契約のスライド番号。
# S9（再訪）が抜けるため、位置9以降は内容契約の番号とずれる。
NO_REVISIT_CONTRACT_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]

# 配置幅 220 mm で 200 dpi を満たす最小ピクセル幅
MIN_WIDTH_PX = int(220 / 25.4 * 200)  # 1732

FIGURES = (
    "p06_clusters_map.png", "p07_three_scales.png", "p08_visit_anchors_map.png",
    "p12_loop_diagram.png",
)

# バイト単位で固定する写真・図版のソース。キーはスライド番号、値はそのスライドの
# PICTURE シェイプの挿入順で期待するファイル名（`docs/presentations/images/`）。
# S1・S3 は色付きの現地写真を意図しており、日本語記事用にグレースケール化された
# `fig03_keirin_cliff.jpg` へ将来の編集で意図せず戻ってしまう回帰を防ぐ
# （Fix round 2 のレビュー指摘）。S7 は英語ラベルのみの三スケール合成図
# `p07_three_scales.png` が、日本語キャプション付きの `fig09_multiscale.png` に
# 戻ってしまう回帰を防ぐ（Fix round 1 のレビュー指摘）。
PINNED_PHOTO_SOURCES: dict[int, tuple[str, ...]] = {
    1: ("choba_lake_3.jpg",),
    3: ("fig01_lake_stage.jpg", "choba_lake_1.jpg"),
    7: ("p07_three_scales.png",),
}

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


def check_pinned_photo_sources(prs: Presentation) -> None:
    """`PINNED_PHOTO_SOURCES` に列挙したスライドの PICTURE シェイプが、意図した
    ファイルとバイト単位で一致することを確認する。

    シェイプ名やファイル名の一致だけでは、グレースケールの記事図版
    （`fig03_keirin_cliff.jpg` 等、日本語記事用に変換されたもの）や日本語キャプション
    付き図版（`fig09_multiscale.png`）への意図しないフォールバック・混入を検出
    できない（Fix round 1・Fix round 2 のレビュー指摘の再発防止）。
    """
    slides = list(prs.slides)
    for idx, expected_names in PINNED_PHOTO_SOURCES.items():
        label = f"S{idx}"
        if idx > len(slides):
            for name in expected_names:
                check(False, f"{label}: スライドが存在しない（画像 '{name}' を検査不可）")
            continue
        pics = [sh for sh in slides[idx - 1].shapes if sh.shape_type == MSO_SHAPE_TYPE.PICTURE]
        check(
            len(pics) == len(expected_names),
            f"{label}: PICTUREシェイプが{len(expected_names)}個でない: {len(pics)}個",
        )
        if len(pics) != len(expected_names):
            continue
        for pic, name in zip(pics, expected_names):
            expected_path = IMAGES / name
            check(expected_path.is_file(), f"{name} が存在しない")
            if not expected_path.is_file():
                continue
            check(
                pic.image.blob == expected_path.read_bytes(),
                f"{label}: 画像が {name} と一致しない（バイト比較。意図しない差し替え・"
                "フォールバックの可能性）",
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


def parse_notes(md: str) -> dict[int, dict[str, str]]:
    """スピーカーノート Markdown を `### Slide N — <title>` 単位に分解する。

    返り値は内容契約のスライド番号をキーとし、`title`（見出しのタイトル文字列）、
    `en`（英語の発話本文。`**EN (spoken)**` から `**JA (not spoken)**` の直前まで）、
    `ja`（`**JA (not spoken)**` の行から節末まで。節区切りの水平線 `---` は除く）を
    持つ辞書。

    生成スクリプト側にも同等の分解処理があるが、検査側は独立実装で持つ
    （生成スクリプトの読み取り結果をそのまま信じると、PPTX ノートペインとの
    同期検査が「自分が書いたものを読み直した」だけの検査になってしまう）。
    """
    parts = re.split(r"(?m)^### Slide (\d+) — (.*)$", md)[1:]
    sections: dict[int, dict[str, str]] = {}
    for i in range(0, len(parts), 3):
        number = int(parts[i])
        title = parts[i + 1].strip()
        body = parts[i + 2]
        en, ja = "", ""
        if EN_MARKER in body and JA_MARKER in body:
            after_en = body.split(EN_MARKER, 1)[1]
            en = after_en.split(JA_MARKER, 1)[0].strip()
            ja = re.sub(
                r"\n+-{3,}\s*$",
                "",
                (JA_MARKER + after_en.split(JA_MARKER, 1)[1]).strip(),
            ).strip()
        sections[number] = {"title": title, "en": en, "ja": ja}
    return sections


def notes_pane_text(section: dict[str, str]) -> str:
    """ノート Markdown の1節から、PPTX ノートペインに入るべき文字列を組み立てる。

    英語の発話本文を先頭に置き、空行を挟んで日本語（非発話）の塊を続ける
    （生成スクリプトの `build_notes_text()` と同一の正規形）。
    """
    return f"{section['en']}\n\n{section['ja']}"


def count_en_words(en: str) -> int:
    """英語発話本文の語数を数える。

    数字のみのトークン（`145` 等）は語として数えない。初出を綴り字
    （`one hundred and forty-five`）にする方針と整合させるため、綴られた語のみを
    通し読み時間の見積り対象とする。
    """
    return len(re.findall(r"[A-Za-z][A-Za-z'’-]*", en))


def check_speaker_notes() -> dict[int, dict[str, str]]:
    """スピーカーノート Markdown の構造・語数・S6 必須発話内容を検査する。"""
    if not NOTES_MD.is_file():
        check(False, "スピーカーノート Markdown が存在しない")
        return {}

    sections = parse_notes(NOTES_MD.read_text(encoding="utf-8"))
    check(len(sections) == 12, f"ノートのスライド数が12でない: {len(sections)}")

    for n, expected_title in enumerate(TITLES, start=1):
        label = f"S{n}"
        if n not in sections:
            check(False, f"{label}: ノートの節が存在しない")
            continue
        section = sections[n]
        check(
            section["title"] == expected_title,
            f"{label}: ノートの見出しタイトルが内容契約と完全一致しない",
        )
        check(bool(section["en"]), f"{label}: EN 発話本文が無い（{EN_MARKER}）")
        check(bool(section["ja"]), f"{label}: JA 非発話部分が無い（{JA_MARKER}）")
        check(
            EN_MARKER not in section["en"] and JA_MARKER not in section["en"],
            f"{label}: EN 部分に構造マーカーが混入している",
        )
        words = count_en_words(section["en"])
        budget = round(DURATIONS_S[n - 1] / 60 * WPM)
        check(
            abs(words - budget) <= budget * WORD_TOLERANCE,
            f"{label}: EN 語数 {words} が想定 {budget} 語から "
            f"{WORD_TOLERANCE:.0%} 超乖離",
        )

    en6 = sections.get(6, {}).get("en", "")
    for line in S6_REQUIRED:
        check(line in en6, f"S6: required spoken content が EN 本文に無い — '{line}'")

    return sections


def check_notes_sync(sections: dict[int, dict[str, str]]) -> None:
    """両版の PPTX ノートペインが、ノート Markdown の正規形と一致することを確認する。

    12枚版はスライド位置＝内容契約の番号だが、再訪なし版（11枚）は S9 が抜けるため
    `NO_REVISIT_CONTRACT_NUMBERS` で対応付ける（位置で素朴に添字を取ると、
    位置9以降に S10・S11・S12 ではなく1つ前のノートが載っていても検査が通ってしまう）。
    """
    if not sections:
        return
    decks = [
        ("12枚版", PPTX, list(range(1, 13))),
        ("再訪なし版", NO_REVISIT_PPTX, NO_REVISIT_CONTRACT_NUMBERS),
    ]
    for deck_label, path, contract_numbers in decks:
        if not path.is_file():
            check(False, f"{deck_label}: PPTX が存在しない（ノート同期を検査不可）")
            continue
        slides = list(Presentation(path).slides)
        check(
            len(slides) == len(contract_numbers),
            f"{deck_label}: スライド数 {len(slides)} が期待値 {len(contract_numbers)} と不一致",
        )
        for position, contract_n in enumerate(contract_numbers, start=1):
            label = f"{deck_label} 位置{position}（契約 S{contract_n}）"
            if position > len(slides):
                check(False, f"{label}: スライドが存在しない")
                continue
            slide = slides[position - 1]
            check(slide.has_notes_slide, f"{label}: ノートペインが無い")
            if not slide.has_notes_slide:
                continue
            actual = slide.notes_slide.notes_text_frame.text
            expected = notes_pane_text(sections[contract_n])
            check(
                actual == expected,
                f"{label}: PPTX ノートペインが Markdown と一致しない",
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
        check_pinned_photo_sources(prs)

    check_no_revisit_variant()

    sections = check_speaker_notes()
    check_notes_sync(sections)

    if errors:
        print(f"FAIL ({len(errors)} / {checks} checks failed)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"OK: {checks} checks passed")


if __name__ == "__main__":
    main()
