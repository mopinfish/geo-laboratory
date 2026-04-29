"""地理交流広場第10号 北木島訪問記の Word ファイル(.docx)を生成する。

テンプレート（コラム体裁）のセクションプロパティ・フォント設定をベースに、
draft.md の内容を python-docx で組み直す。

実行方法:
    uv run python scripts/build_chiri_koryu_docx.py

入力:
    docs/articles/2026_chiri-koryu-10/draft.md
    /Users/otsuka/Downloads/地理交流広場テンプレート（コラム体裁）_v3.docx

出力:
    docs/articles/2026_chiri-koryu-10/draft.docx (.gitignore で除外)

体裁:
    - B5 (182×257mm)
    - 余白: 上下25mm、左右18mm
    - 本文: UD デジタル 教科書体 N-R 9pt
    - 見出し: UD デジタル 教科書体 N-B
    - タイトル: UD デジタル 教科書体 N-B 12pt
"""

from __future__ import annotations

import re
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Iterator

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Mm, Pt
from docx.oxml import OxmlElement

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = PROJECT_ROOT / "docs" / "articles" / "2026_chiri-koryu-10"
DRAFT_MD = ARTICLE_DIR / "draft.md"
OUT_DOCX = ARTICLE_DIR / "draft.docx"
TEMPLATE = Path("/Users/otsuka/Downloads/地理交流広場テンプレート（コラム体裁）_v3.docx")

FONT_BOLD = "UD デジタル 教科書体 N-B"
FONT_REGULAR = "UD デジタル 教科書体 N-R"


def set_run_font(run, name: str, size_pt: float, bold: bool = False) -> None:
    """ランに UD デジタル教科書体 を直接指定する（ASCII・eastAsia 両方）。"""
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    # 既存の rFonts を削除して新しい設定を入れる
    for elem in rpr.findall(qn("w:rFonts")):
        rpr.remove(elem)
    rfonts = OxmlElement("w:rFonts")
    rfonts.set(qn("w:ascii"), name)
    rfonts.set(qn("w:eastAsia"), name)
    rfonts.set(qn("w:hAnsi"), name)
    rfonts.set(qn("w:cs"), name)
    rfonts.set(qn("w:hint"), "eastAsia")
    rpr.insert(0, rfonts)
    run.font.size = Pt(size_pt)
    if bold:
        run.bold = True


def add_paragraph(doc, text: str, *, font: str = FONT_REGULAR, size_pt: float = 9.0,
                  bold: bool = False, align: str | None = None,
                  space_before: float = 0.0, space_after: float = 0.0,
                  first_line_indent: bool = False,
                  clear_wrap: bool = False):
    """本文段落を追加する。インライン記法（**bold**, ^sup^）も簡易処理する。

    clear_wrap=True にすると、段落の先頭に clear="all" のテキスト改行を入れ、
    上にある回り込み画像の下から段落が始まるようにする（見出し等で使用）。
    """
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    if first_line_indent:
        pf.first_line_indent = Pt(size_pt)  # 1文字分の字下げ
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # 回り込み解除ブレーク（見出しなど、画像の隣に並びたくない段落用）
    if clear_wrap:
        clear_run = p.add_run()
        br = OxmlElement("w:br")
        br.set(qn("w:type"), "textWrapping")
        br.set(qn("w:clear"), "all")
        clear_run._element.append(br)

    # インライン記法を解釈してランを作る
    for piece, kind in _parse_inline(text):
        run = p.add_run(piece)
        is_bold = bold or kind == "bold"
        set_run_font(run, font, size_pt, bold=is_bold)
        if kind == "sup":
            run.font.superscript = True
    return p


def _parse_inline(text: str) -> Iterator[tuple[str, str]]:
    """**bold**, ^sup^ を解釈してテキスト断片を返す。"""
    # トークン化: 順番に **bold** / ^sup^ / 通常テキスト
    pattern = re.compile(r"(\*\*[^*]+\*\*|\^[^^]+\^)")
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            yield text[pos:m.start()], "normal"
        token = m.group(0)
        if token.startswith("**"):
            yield token[2:-2], "bold"
        elif token.startswith("^"):
            yield token[1:-1], "sup"
        pos = m.end()
    if pos < len(text):
        yield text[pos:], "normal"


def _convert_inline_to_anchor(picture_run, *, side: str = "right") -> None:
    """add_picture で挿入された inline 画像を anchor (wrapSquare) に変換する。

    本文が画像の左右に回り込むようにする。テンプレートの画像配置と整合させる。
    """
    drawing = picture_run.find(qn("w:drawing"))
    if drawing is None:
        return
    inline = drawing.find(qn("wp:inline"))
    if inline is None:
        return

    extent = inline.find(qn("wp:extent"))
    docPr = inline.find(qn("wp:docPr"))
    cNvGraphicFramePr = inline.find(qn("wp:cNvGraphicFramePr"))
    graphic = inline.find(qn("a:graphic"))

    anchor = OxmlElement("wp:anchor")
    for k, v in [
        ("distT", "0"), ("distB", "0"),
        ("distL", "114300"), ("distR", "114300"),
        ("simplePos", "0"), ("relativeHeight", "251660288"),
        ("behindDoc", "0"), ("locked", "0"),
        ("layoutInCell", "1"), ("allowOverlap", "1"),
    ]:
        anchor.set(k, v)

    simple_pos = OxmlElement("wp:simplePos")
    simple_pos.set("x", "0")
    simple_pos.set("y", "0")
    anchor.append(simple_pos)

    # 横位置: テンプレートと同じく margin 基準で右寄せ
    pos_h = OxmlElement("wp:positionH")
    pos_h.set("relativeFrom", "margin")
    align_h = OxmlElement("wp:align")
    align_h.text = side  # "right" or "left"
    pos_h.append(align_h)
    anchor.append(pos_h)

    # 縦位置: 段落の先頭を基準に top
    pos_v = OxmlElement("wp:positionV")
    pos_v.set("relativeFrom", "paragraph")
    align_v = OxmlElement("wp:align")
    align_v.text = "top"
    pos_v.append(align_v)
    anchor.append(pos_v)

    anchor.append(deepcopy(extent))

    effect_extent = OxmlElement("wp:effectExtent")
    for k, v in [("l", "0"), ("t", "0"), ("r", "0"), ("b", "0")]:
        effect_extent.set(k, v)
    anchor.append(effect_extent)

    # 文字回り込み: 両側
    wrap = OxmlElement("wp:wrapSquare")
    wrap.set("wrapText", "bothSides")
    anchor.append(wrap)

    if docPr is not None:
        anchor.append(deepcopy(docPr))
    if cNvGraphicFramePr is not None:
        anchor.append(deepcopy(cNvGraphicFramePr))
    if graphic is not None:
        anchor.append(deepcopy(graphic))

    drawing.remove(inline)
    drawing.append(anchor)


def add_image(doc, image_path: Path, caption: str) -> None:
    """文字回り込みで画像を貼り、下にキャプション。

    テンプレートに準拠: 画像は anchor wrapSquare で右寄せ、本文が左に回り込む。
    キャプションは画像直後の段落に右寄せで配置する。
    """
    # 画像を含む段落
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(2)
    run = p.add_run()
    # 画像幅 75mm（B5本文幅 148mm の約半分）— 文字回り込みのスペースを確保
    run.add_picture(str(image_path), width=Mm(75))
    # inline → anchor 変換
    _convert_inline_to_anchor(run._element, side="right")

    # キャプション（同じ段落の続きに右寄せで入れる）
    cap_run = p.add_run(caption)
    set_run_font(cap_run, FONT_REGULAR, 9.0)


def clear_body_keep_sectPr(doc) -> None:
    """body の中身を全て削除する（最後の sectPr は document 側で保持される）。"""
    body = doc.element.body
    # sectPr 以外の全要素を削除
    sectPr = body.find(qn("w:sectPr"))
    for child in list(body):
        if child.tag != qn("w:sectPr"):
            body.remove(child)
    # sectPr は最後に再追加される必要があるが、find で取得した要素はまだ body にある
    # （find は remove しないので、上記 list(body) で sectPr も含まれていた場合は除外済）
    # 念のため: sectPr が残っているか確認、なければ追加
    if sectPr is not None and body.find(qn("w:sectPr")) is None:
        body.append(sectPr)


def parse_markdown(md_text: str) -> list[dict]:
    """draft.md を簡易パースしてブロックリストに変換する。"""
    blocks: list[dict] = []
    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 空行はスキップ（次のループで判定）
        if stripped == "":
            i += 1
            continue

        # 区切り線
        if stripped == "---":
            blocks.append({"type": "hr"})
            i += 1
            continue

        # H1 タイトル
        if stripped.startswith("# "):
            blocks.append({"type": "h1", "text": stripped[2:]})
            i += 1
            continue

        # H2 章
        if stripped.startswith("## "):
            blocks.append({"type": "h2", "text": stripped[3:]})
            i += 1
            continue

        # H3 節
        if stripped.startswith("### "):
            blocks.append({"type": "h3", "text": stripped[4:]})
            i += 1
            continue

        # 画像 ![caption](path)
        m = re.match(r"!\[([^\]]+)\]\(([^)]+)\)", stripped)
        if m:
            blocks.append({"type": "image", "caption": m.group(1), "path": m.group(2)})
            i += 1
            continue

        # 文献リスト（- で始まる）
        if stripped.startswith("- "):
            blocks.append({"type": "list_item", "text": stripped[2:]})
            i += 1
            continue

        # 注（数字+）で始まる）
        m_note = re.match(r"^(\d+)\)\s+(.+)$", stripped)
        if m_note:
            blocks.append({"type": "note_item", "num": m_note.group(1), "text": m_note.group(2)})
            i += 1
            continue

        # 副題（―...―）
        if stripped.startswith("―") and stripped.endswith("―"):
            blocks.append({"type": "subtitle", "text": stripped})
            i += 1
            continue

        # それ以外は本文段落（連続する非空行を結合）
        para_lines = [stripped]
        j = i + 1
        while j < len(lines) and lines[j].strip() and not _is_block_start(lines[j].strip()):
            para_lines.append(lines[j].strip())
            j += 1
        blocks.append({"type": "para", "text": " ".join(para_lines)})
        i = j

    return blocks


def _is_block_start(line: str) -> bool:
    """この行が新しいブロックの開始か判定する。"""
    if line.startswith(("# ", "## ", "### ", "- ", "!")):
        return True
    if line == "---":
        return True
    if re.match(r"^\d+\)\s+", line):
        return True
    if line.startswith("―") and line.endswith("―"):
        return True
    return False


def is_author_line(text: str) -> bool:
    """著者行（短く、特定パターンに合う）を判定する。"""
    return text.strip() in ("Otsuka Noboru", "大塚　昇", "大塚 昇")


def render(blocks: list[dict], doc) -> None:
    """ブロックを Word ドキュメントに書き込む。"""
    # まず空のドキュメントから始まる前提。最初に表紙的に title/subtitle/author を扱う
    seen_h1 = False
    for blk in blocks:
        t = blk["type"]
        if t == "h1":
            # タイトル: UD N-B 12pt 中央揃え
            add_paragraph(doc, blk["text"], font=FONT_BOLD, size_pt=12.0,
                          align="center", space_before=0, space_after=4)
            seen_h1 = True
        elif t == "subtitle":
            # 副題: UD N-B 9pt 中央揃え
            add_paragraph(doc, blk["text"], font=FONT_BOLD, size_pt=9.0,
                          align="center", space_after=4)
        elif t == "para" and is_author_line(blk["text"]):
            # 著者行: 10.5pt 中央揃え
            add_paragraph(doc, blk["text"], font=FONT_REGULAR, size_pt=10.5,
                          align="center", space_after=12)
        elif t == "hr":
            # 区切り線は空段落として扱う（罫線は省略）
            continue
        elif t == "h2":
            # 章: UD N-B 11pt 太字、章前に間。フロート画像の下から開始させる
            add_paragraph(doc, blk["text"], font=FONT_BOLD, size_pt=11.0,
                          bold=True, space_before=10, space_after=4,
                          clear_wrap=True)
        elif t == "h3":
            # 節: UD N-B 9.5pt 太字。フロート画像の下から開始させる
            add_paragraph(doc, blk["text"], font=FONT_BOLD, size_pt=9.5,
                          bold=True, space_before=6, space_after=2,
                          clear_wrap=True)
        elif t == "image":
            img_path = ARTICLE_DIR / blk["path"]
            if img_path.exists():
                add_image(doc, img_path, blk["caption"])
            else:
                add_paragraph(doc, f"[画像が見つかりません: {blk['path']}]",
                              font=FONT_REGULAR, size_pt=9.0)
        elif t == "list_item":
            # 文献リスト
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Mm(5)
            p.paragraph_format.first_line_indent = Mm(-5)
            p.paragraph_format.space_after = Pt(2)
            for piece, kind in _parse_inline("・ " + blk["text"]):
                r = p.add_run(piece)
                set_run_font(r, FONT_REGULAR, 8.5, bold=(kind == "bold"))
        elif t == "note_item":
            # 注: 番号と本文
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Mm(5)
            p.paragraph_format.first_line_indent = Mm(-5)
            p.paragraph_format.space_after = Pt(2)
            num_run = p.add_run(f"{blk['num']}）")
            set_run_font(num_run, FONT_REGULAR, 8.0)
            for piece, kind in _parse_inline(blk["text"]):
                r = p.add_run(piece)
                set_run_font(r, FONT_REGULAR, 8.0, bold=(kind == "bold"))
        elif t == "para":
            # 本文段落 — 章タイトル「注」「文献」の場合は特別扱い
            if blk["text"] in ("注", "文献"):
                add_paragraph(doc, blk["text"], font=FONT_BOLD, size_pt=10.0,
                              bold=True, space_before=10, space_after=4)
            else:
                add_paragraph(doc, blk["text"], font=FONT_REGULAR, size_pt=9.0,
                              first_line_indent=True, space_after=2)


def main() -> None:
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"テンプレートが見つかりません: {TEMPLATE}")
    if not DRAFT_MD.exists():
        raise FileNotFoundError(f"原稿が見つかりません: {DRAFT_MD}")

    # テンプレートを開いて中身を空にする（sectPr / styles / theme を保持）
    doc = Document(str(TEMPLATE))
    clear_body_keep_sectPr(doc)

    # 原稿パース
    md_text = DRAFT_MD.read_text(encoding="utf-8")
    blocks = parse_markdown(md_text)

    # レンダリング
    render(blocks, doc)

    # 保存
    doc.save(str(OUT_DOCX))
    print(f"saved: {OUT_DOCX}")
    print(f"blocks rendered: {len(blocks)}")


if __name__ == "__main__":
    main()
