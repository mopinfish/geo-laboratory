"""口頭説明スクリプトと想定問答集を1本の印刷用 docx に結合する。

FOSS4G Hiroshima 2026 のポスター発表当日、手元に置く紙資料として使う想定。
入力は Markdown 2本（正本）で、このスクリプトは変換のみを行う。内容の修正は
必ず Markdown 側で行い、本スクリプトを再実行すること。

pandoc が生成する docx は表が左詰め・罫線なしになるため、生成後に OOXML を
直接パッチする（グローバル作業ルールの「pandoc 生成 docx のテーブルレイアウト」
に対応）:

1. w:tblLayout type="fixed" → "autofit"
2. w:tblW を pct 5000（本文幅100%）に設定
3. w:tblGrid の各 w:gridCol を本文幅で等分再計算
4. w:tblInd（左インデント）を除去
5. 罫線（w:tblBorders）を付与
6. 先頭行以外の w:tblHeader を除去（改ページ時のヘッダー繰り返しを抑止）

あわせてページ設定（A4縦・左右余白15mm）と日本語フォントを設定する。
実行日時やコミットハッシュは埋め込まないため、同一入力なら再実行で同じ内容になる。

実行方法:
    uv run python scripts/build_exp002_talk_materials_docx.py

出力: docs/posters/exp002_kitagi_foss4g2026_talk_materials.docx
"""

from __future__ import annotations

import re
import shutil
import subprocess
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSTER_DIR = PROJECT_ROOT / "docs" / "posters"
TMP_DIR = PROJECT_ROOT / "tmp"

TALK_MD = POSTER_DIR / "exp002_kitagi_foss4g2026_talk_script.md"
QA_MD = POSTER_DIR / "exp002_kitagi_foss4g2026_qa.md"
OUT_DOCX = POSTER_DIR / "exp002_kitagi_foss4g2026_talk_materials.docx"

# ページ設定（twips: 1mm = 56.7 twips）
PAGE_W, PAGE_H = 11906, 16838          # A4 縦
MARGIN_LR, MARGIN_TB = 850, 1134       # 左右 15mm / 上下 20mm
BODY_W = PAGE_W - 2 * MARGIN_LR        # 本文幅 = 10206 twips（180mm）

FONT_ASCII = "Helvetica Neue"
FONT_EASTASIA = "Hiragino Kaku Gothic ProN"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

PAGE_BREAK = """
```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
"""

HEADER = """# FOSS4G Hiroshima 2026 ポスター発表 当日資料

**Detecting Quarry Pond Remnants on a Japanese Island Heritage Site Using Sentinel-2 Imagery and Open-Source Remote Sensing Tools** — Noboru Otsuka (Geolonia Inc.)

掲出: Sakura Lounge, September 1–3, 2026 ／ コアタイム: September 2, 13:00–15:00

本資料は口頭説明スクリプトと想定問答集を1本にまとめた印刷用ドキュメントである。正本は
`docs/posters/exp002_kitagi_foss4g2026_talk_script.md` と
`docs/posters/exp002_kitagi_foss4g2026_qa.md` で、内容の修正は Markdown 側で行い
`scripts/build_exp002_talk_materials_docx.py` を再実行して再生成する。

**構成**

- 第1部 口頭説明スクリプト — 1画面カード、詳細チートシート、30秒版 / 2〜3分版 / 5分版、定型フレーズ、運用メモ
- 第2部 想定問答集 — 33問（手法・閾値・季節差・偽陽性・現地検証・再現性・127丁場・展開・データとライセンス）
"""


def demote_headings(md: str) -> str:
    """見出しを1段下げる（結合後の文書で H1 を1つに保つ）。"""
    return re.sub(r"^(#{1,5}) ", r"#\1 ", md, flags=re.MULTILINE)


def build_markdown() -> Path:
    talk = demote_headings(TALK_MD.read_text(encoding="utf-8"))
    qa = demote_headings(QA_MD.read_text(encoding="utf-8"))
    combined = "\n".join([HEADER, PAGE_BREAK, talk, PAGE_BREAK, qa])
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    path = TMP_DIR / "exp002_talk_materials_combined.md"
    path.write_text(combined, encoding="utf-8")
    return path


def run_pandoc(md_path: Path) -> None:
    cmd = [
        "pandoc", str(md_path),
        "--from", "gfm+raw_attribute",
        "--to", "docx",
        "--output", str(OUT_DOCX),
        "--wrap", "none",
    ]
    subprocess.run(cmd, check=True)


# ------------------------------------------------------------------ OOXML パッチ
def patch_sect_pr(xml: str) -> str:
    """ページサイズと余白を A4縦・左右15mm に設定する。"""
    pg_sz = f'<w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>'
    pg_mar = (f'<w:pgMar w:top="{MARGIN_TB}" w:right="{MARGIN_LR}" '
              f'w:bottom="{MARGIN_TB}" w:left="{MARGIN_LR}" '
              'w:header="720" w:footer="720" w:gutter="0"/>')
    if "<w:pgSz" in xml:
        xml = re.sub(r"<w:pgSz[^/]*/>", pg_sz, xml)
    else:
        # <w:sectPr> / <w:sectPr ...> の閉じ山括弧の直後に挿入する
        xml = re.sub(r"(<w:sectPr[^>]*>)", lambda m: m.group(1) + pg_sz, xml, count=1)
    if "<w:pgMar" in xml:
        xml = re.sub(r"<w:pgMar[^/]*/>", pg_mar, xml)
    else:
        xml = xml.replace(pg_sz, pg_sz + pg_mar, 1)
    return xml


def patch_tables(xml: str) -> tuple[str, int]:
    """表を本文幅100%・罫線付き・autofit にし、ヘッダー繰り返しを抑止する。"""
    borders = (
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        "</w:tblBorders>"
    )

    def fix_tbl_pr(m: re.Match) -> str:
        pr = m.group(0)
        pr = pr.replace('<w:tblLayout w:type="fixed"/>', '<w:tblLayout w:type="autofit"/>')
        pr = re.sub(r"<w:tblInd[^/]*/>", "", pr)
        pr = re.sub(r"<w:tblW[^/]*/>", f'<w:tblW w:w="5000" w:type="pct"/>', pr)
        if "<w:tblW" not in pr:
            pr = pr.replace("<w:tblPr>", '<w:tblPr><w:tblW w:w="5000" w:type="pct"/>', 1)
        if "<w:tblBorders>" not in pr:
            pr = pr.replace("</w:tblPr>", borders + "</w:tblPr>", 1)
        if "<w:tblLayout" not in pr:
            pr = pr.replace("</w:tblPr>", '<w:tblLayout w:type="autofit"/></w:tblPr>', 1)
        return pr

    xml = re.sub(r"<w:tblPr>.*?</w:tblPr>", fix_tbl_pr, xml, flags=re.DOTALL)

    def fix_grid(m: re.Match) -> str:
        grid = m.group(0)
        cols = re.findall(r"<w:gridCol[^/]*/>", grid)
        if not cols:
            return grid
        each = BODY_W // len(cols)
        rest = BODY_W - each * (len(cols) - 1)
        new = "".join(
            f'<w:gridCol w:w="{rest if i == len(cols) - 1 else each}"/>'
            for i in range(len(cols))
        )
        return f"<w:tblGrid>{new}</w:tblGrid>"

    xml, n_tables = re.subn(r"<w:tblGrid>.*?</w:tblGrid>", fix_grid, xml, flags=re.DOTALL)

    # 先頭行以外の tblHeader を除去（pandoc は全行に付与する）
    def fix_headers(m: re.Match) -> str:
        tbl = m.group(0)
        parts = re.split(r"(<w:tr\b)", tbl)
        out, row_idx = [], 0
        for part in parts:
            if part == "<w:tr":
                row_idx += 1
                out.append(part)
                continue
            if row_idx > 1:
                part = re.sub(r"<w:tblHeader[^/]*/>", "", part)
            out.append(part)
        return "".join(out)

    xml = re.sub(r"<w:tbl>.*?</w:tbl>", fix_headers, xml, flags=re.DOTALL)
    return xml, n_tables


def patch_styles(xml: str) -> str:
    """既定フォントに日本語フォントを設定する。"""
    return re.sub(
        r'<w:rFonts[^/]*/>',
        f'<w:rFonts w:ascii="{FONT_ASCII}" w:hAnsi="{FONT_ASCII}" '
        f'w:eastAsia="{FONT_EASTASIA}" w:cs="{FONT_ASCII}"/>',
        xml,
        count=1,
    )


def patch_core_props(xml: str) -> str:
    """実行時刻の埋め込みを除去する（同一入力なら再実行でバイト一致させるため）。

    pandoc は dcterms:created / dcterms:modified に実行時刻を書き込む。生成履歴は
    git と print_log で管理するため、成果物からは除去して決定的にする。
    """
    return re.sub(r"<dcterms:(created|modified)[^>]*>[^<]*</dcterms:\1>", "", xml)


def patch_docx() -> int:
    tmp = OUT_DOCX.with_suffix(".patching.docx")
    n_tables = 0
    with zipfile.ZipFile(OUT_DOCX) as zin, zipfile.ZipFile(
        tmp, "w", zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                xml = data.decode("utf-8")
                xml = patch_sect_pr(xml)
                xml, n_tables = patch_tables(xml)
                data = xml.encode("utf-8")
            elif item.filename == "word/styles.xml":
                data = patch_styles(data.decode("utf-8")).encode("utf-8")
            elif item.filename == "docProps/core.xml":
                data = patch_core_props(data.decode("utf-8")).encode("utf-8")
            info = zipfile.ZipInfo(item.filename, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = item.compress_type
            info.external_attr = item.external_attr
            zout.writestr(info, data)
    shutil.move(tmp, OUT_DOCX)
    return n_tables


def verify() -> dict:
    """生成物を検証する。XMLの整形式性、ページ設定、表のパッチ、本文の到達性。"""
    import xml.etree.ElementTree as ET

    results = {}
    with zipfile.ZipFile(OUT_DOCX) as z:
        assert z.testzip() is None, "zip が壊れている"
        for name in ("word/document.xml", "word/styles.xml", "[Content_Types].xml"):
            ET.fromstring(z.read(name))  # 整形式でなければ例外
        doc = z.read("word/document.xml").decode("utf-8")

    assert f'<w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>' in doc, "ページサイズが A4 でない"
    assert f'w:left="{MARGIN_LR}"' in doc, "左余白が設定されていない"
    assert '<w:tblLayout w:type="fixed"/>' not in doc, "fixed レイアウトが残っている"
    assert "<w:tblInd" not in doc, "tblInd が残っている"

    with zipfile.ZipFile(OUT_DOCX) as z:
        core = z.read("docProps/core.xml").decode("utf-8")
    assert "dcterms:created" not in core and "dcterms:modified" not in core, \
        "実行時刻が埋め込まれている（決定的でない）"

    n_tbl = doc.count("<w:tbl>")
    assert doc.count("<w:tblBorders>") == n_tbl, "罫線のない表がある"
    assert doc.count('<w:tblW w:w="5000" w:type="pct"/>') == n_tbl, "幅100%でない表がある"
    assert doc.count("<w:tblHeader") == n_tbl, "ヘッダー繰り返しが残っている（先頭行のみ想定）"
    for grid in re.findall(r"<w:tblGrid>(.*?)</w:tblGrid>", doc, re.DOTALL):
        widths = [int(w) for w in re.findall(r'w:w="(\d+)"', grid)]
        assert sum(widths) == BODY_W, f"列幅の合計が本文幅と一致しない: {sum(widths)}"

    # pandoc で読み戻し、必須文字列が本文に到達しているか確認
    text = subprocess.run(
        ["pandoc", "-f", "docx", "-t", "plain", "--wrap", "none", str(OUT_DOCX)],
        check=True, capture_output=True, text=True,
    ).stdout
    required = ["1画面カード", "30秒版", "2〜3分版", "5分版",
                "not individually field-confirmed quarry ponds",
                "113", "145", "127", "CC BY 4.0"]
    missing = [r for r in required if r not in text]
    assert not missing, f"本文に到達しない必須文字列: {missing}"
    n_q = len(re.findall(r"^Q\d+-\d+\.", text, re.MULTILINE))
    assert n_q >= 33, f"想定問答の項目数が不足: {n_q}"

    results["tables"] = n_tbl
    results["page_breaks"] = doc.count('w:type="page"')
    results["questions"] = n_q
    results["text_chars"] = len(text)
    return results


def main() -> None:
    md_path = build_markdown()
    print(f"combined markdown: {md_path.relative_to(PROJECT_ROOT)} "
          f"({len(md_path.read_text(encoding='utf-8')):,} chars)")
    run_pandoc(md_path)
    n_tables = patch_docx()
    size = OUT_DOCX.stat().st_size
    print(f"docx: {OUT_DOCX.relative_to(PROJECT_ROOT)} ({size:,} bytes)")
    print(f"  page: A4 portrait {PAGE_W}x{PAGE_H} twips, margins LR={MARGIN_LR} TB={MARGIN_TB}")
    print(f"  tables patched: {n_tables} (autofit / 100% width / borders / header repeat removed)")
    print(f"  fonts: ascii={FONT_ASCII}, eastAsia={FONT_EASTASIA}")
    r = verify()
    print(f"verified: XML well-formed, tables={r['tables']}, page breaks={r['page_breaks']}, "
          f"questions={r['questions']}, extracted text={r['text_chars']:,} chars")


if __name__ == "__main__":
    main()
