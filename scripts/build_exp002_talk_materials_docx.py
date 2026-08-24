"""口頭説明スクリプトと想定問答集から、印刷用 docx を2種類生成する。

FOSS4G Hiroshima 2026 の発表当日、手元に置く紙資料として使う想定。
入力は Markdown 2本（正本）で、このスクリプトは変換のみを行う。内容の修正は
必ず Markdown 側で行い、本スクリプトを再実行すること。

生成する2つの docx:

1. `exp002_kitagi_foss4g2026_talk_materials.docx` — 口頭説明スクリプト（第1部）と
   想定問答集（第2部）を結合した全体版（目次なし、約18ページ）。
2. `exp002_kitagi_foss4g2026_qa.docx` — 想定問答集のみの単独版。質疑応答5分間に
   壇上で検索する用途のため、全体版から目次なしで質問だけを抜き出す。索引・目次は
   持たない（発表者が明示的に不要と判断）。本文の文字サイズは15pt下限まで引き上げる
   （全体版は既存の約18ページのページ組みを崩さないため対象外。詳細は
   `patch_font_floor()` のdocstring）。

pandoc が生成する docx は表が左詰め・罫線なしになるため、生成後に OOXML を
直接パッチする（グローバル作業ルールの「pandoc 生成 docx のテーブルレイアウト」
に対応）。このパッチ処理（`patch_docx()` 以下の一群）は両方の docx で共有し、
出力先だけを引数で切り替える。処理内容:

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

出力:
    docs/posters/exp002_kitagi_foss4g2026_talk_materials.docx
    docs/posters/exp002_kitagi_foss4g2026_qa.docx
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
QA_OUT_DOCX = POSTER_DIR / "exp002_kitagi_foss4g2026_qa.docx"

# ページ設定（twips: 1mm = 56.7 twips）
PAGE_W, PAGE_H = 11906, 16838          # A4 縦
MARGIN_LR, MARGIN_TB = 850, 1134       # 左右 15mm / 上下 20mm
BODY_W = PAGE_W - 2 * MARGIN_LR        # 本文幅 = 10206 twips（180mm）

FONT_ASCII = "Helvetica Neue"
FONT_EASTASIA = "Hiragino Kaku Gothic ProN"

# 想定問答単独版のみに適用する本文サイズの下限（pt）。質疑応答の5分間に壇上で
# 検索する用途のため、全体版（既存・約18ページ、pandoc既定の12pt本文）より
# 大きくする。全体版はページ組みが既にレビュー済みのため対象外にする
# （patch_font_floor() 参照）。
QA_BODY_FLOOR_PT = 15.0

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


def run_pandoc(md_path: Path, out_path: Path) -> None:
    cmd = [
        "pandoc", str(md_path),
        "--from", "gfm+raw_attribute",
        "--to", "docx",
        "--output", str(out_path),
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


def patch_font_floor(xml: str, floor_pt: float) -> str:
    """styles.xml 内の文字サイズ（w:sz / w:szCs）が floor_pt を下回らないよう引き上げる。

    docDefaults（本文既定値。pandoc 既定は12pt）だけでなく、見出しスタイルも対象にする。
    想定問答の各項目見出し（`### Qn-n.`）は Heading3 に変換され、pandoc 既定では
    14pt しかなく docDefaults 側だけ上げても下限を割ったままになるため。
    罫線幅の `w:sz` 属性（例: `<w:top w:sz="4" .../>`）は要素の形が異なる
    （属性としての w:sz であり、`<w:sz w:val="N"/>` という独立要素ではない）ため
    このパターンには一致せず、意図せず変更されない。
    """
    floor_half = round(floor_pt * 2)

    def bump(m: re.Match) -> str:
        val = int(m.group(1))
        if val >= floor_half:
            return m.group(0)
        return m.group(0).replace(f'"{val}"', f'"{floor_half}"', 1)

    xml = re.sub(r'<w:sz w:val="(\d+)"\s*/>', bump, xml)
    xml = re.sub(r'<w:szCs w:val="(\d+)"\s*/>', bump, xml)
    return xml


def patch_core_props(xml: str) -> str:
    """実行時刻の埋め込みを除去する（同一入力なら再実行でバイト一致させるため）。

    pandoc は dcterms:created / dcterms:modified に実行時刻を書き込む。生成履歴は
    git と print_log で管理するため、成果物からは除去して決定的にする。
    """
    return re.sub(r"<dcterms:(created|modified)[^>]*>[^<]*</dcterms:\1>", "", xml)


def patch_docx(path: Path, body_floor_pt: float | None = None) -> int:
    """docx の OOXML を直接パッチする。両方の出力ファイルがこの1つの実装を共有する。

    `body_floor_pt` を指定した出力だけ、本文サイズの下限を追加で適用する
    （`QA_BODY_FLOOR_PT` 参照）。パッチ処理そのもの（ページ設定・表・フォント種別・
    実行時刻除去）は常に両方の出力に同一に適用される。
    """
    tmp = path.with_suffix(".patching.docx")
    n_tables = 0
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(
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
                xml = patch_styles(data.decode("utf-8"))
                if body_floor_pt is not None:
                    xml = patch_font_floor(xml, body_floor_pt)
                data = xml.encode("utf-8")
            elif item.filename == "docProps/core.xml":
                data = patch_core_props(data.decode("utf-8")).encode("utf-8")
            info = zipfile.ZipInfo(item.filename, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = item.compress_type
            info.external_attr = item.external_attr
            zout.writestr(info, data)
    shutil.move(tmp, path)
    return n_tables


class Checker:
    """検証の各アサーションを件数付きで集計する。

    既存の `assert` 単発方式では「何件検査したか」が分からず、本タスクが要求する
    「拡張前後のチェック件数」を報告できない。失敗はすぐ例外にせず集めておき、
    `finish()` でまとめて報告する（1件目の失敗で終了せず、全チェックを実行できる）。
    """

    def __init__(self) -> None:
        self.count = 0
        self.errors: list[str] = []

    def check(self, cond: bool, msg: str) -> None:
        self.count += 1
        if not cond:
            self.errors.append(msg)

    def finish(self) -> None:
        if self.errors:
            detail = "\n".join(f"  - {e}" for e in self.errors)
            raise AssertionError(
                f"{len(self.errors)} / {self.count} 件のチェックが失敗:\n{detail}"
            )


def verify_common(c: Checker, path: Path, *, body_floor_pt: float | None = None) -> dict:
    """両方の docx に共通する検証（XML整形式性・ページ設定・表・フォント・決定性）。

    `body_floor_pt` を指定した場合のみ、docDefaults と Heading1〜3 の文字サイズが
    その値以上であることも確認する（想定問答単独版のみが指定する）。
    """
    import xml.etree.ElementTree as ET

    c.check(path.is_file(), f"ファイルが存在しない: {path}")
    if not path.is_file():
        return {}

    with zipfile.ZipFile(path) as z:
        c.check(z.testzip() is None, f"{path.name}: zip が壊れている")
        # 全 XML パーツの整形式性を走査する
        xml_parts = [n for n in z.namelist() if n.endswith((".xml", ".rels"))]
        for name in xml_parts:
            try:
                ET.fromstring(z.read(name))
                ok = True
            except ET.ParseError:
                ok = False
            c.check(ok, f"{path.name}: XML パーツが整形式でない: {name}")
        doc = z.read("word/document.xml").decode("utf-8")
        styles = z.read("word/styles.xml").decode("utf-8")
        core = z.read("docProps/core.xml").decode("utf-8")

    c.check(f'<w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>' in doc,
            f"{path.name}: ページサイズが A4 でない")
    # 4辺すべての余白を検査する
    for attr, expected in (("top", MARGIN_TB), ("right", MARGIN_LR),
                           ("bottom", MARGIN_TB), ("left", MARGIN_LR)):
        c.check(f'w:{attr}="{expected}"' in doc,
                f"{path.name}: {attr} 余白が {expected} twips でない")
    c.check('<w:tblLayout w:type="fixed"/>' not in doc,
            f"{path.name}: fixed レイアウトが残っている")
    c.check("<w:tblInd" not in doc, f"{path.name}: tblInd が残っている")

    # 既定フォント（docDefaults）が設定されているか
    m = re.search(r"<w:docDefaults>.*?</w:docDefaults>", styles, re.DOTALL)
    c.check(bool(m), f"{path.name}: styles.xml に docDefaults がない")
    if m:
        c.check(f'w:ascii="{FONT_ASCII}"' in m.group(0),
                f"{path.name}: 既定の欧文フォントが設定されていない")
        c.check(f'w:eastAsia="{FONT_EASTASIA}"' in m.group(0),
                f"{path.name}: 既定の日本語フォントが設定されていない")

    c.check("dcterms:created" not in core and "dcterms:modified" not in core,
            f"{path.name}: 実行時刻が埋め込まれている（決定的でない）")

    n_tbl = doc.count("<w:tbl>")
    c.check(doc.count("<w:tblBorders>") == n_tbl, f"{path.name}: 罫線のない表がある")
    c.check(doc.count('<w:tblW w:w="5000" w:type="pct"/>') == n_tbl,
            f"{path.name}: 幅100%でない表がある")
    c.check(doc.count('<w:tblLayout w:type="autofit"/>') == n_tbl,
            f"{path.name}: autofit でない表がある")
    c.check(doc.count("<w:tblHeader") == n_tbl,
            f"{path.name}: ヘッダー繰り返しが残っている（先頭行のみ想定）")
    for grid in re.findall(r"<w:tblGrid>(.*?)</w:tblGrid>", doc, re.DOTALL):
        widths = [int(w) for w in re.findall(r'w:w="(\d+)"', grid)]
        c.check(sum(widths) == BODY_W,
                f"{path.name}: 列幅の合計が本文幅と一致しない: {sum(widths)}")

    if body_floor_pt is not None:
        floor_half = round(body_floor_pt * 2)
        dd = re.search(r"<w:docDefaults>.*?</w:docDefaults>", styles, re.DOTALL)
        dd_sizes = [int(v) for v in re.findall(r'<w:sz w:val="(\d+)"', dd.group(0))] if dd else []
        c.check(bool(dd_sizes) and min(dd_sizes) >= floor_half,
                f"{path.name}: docDefaults の本文サイズが {body_floor_pt}pt 未満: {dd_sizes}")
        # 想定問答の項目見出し（`### Qn-n.`）は Heading3 になるため、本文相当の見出し
        # スタイルも下限を満たすことを確認する（docDefaults だけでは見出しは動かない）。
        sizes = {
            styleid: [int(v) for v in re.findall(r'<w:sz w:val="(\d+)"', block)]
            for styleid, block in re.findall(
                r'<w:style[^>]*w:styleId="(Normal|BodyText|Heading[123]|Title)"'
                r'[^>]*>(.*?)</w:style>',
                styles, re.DOTALL,
            )
        }
        for styleid, vals in sizes.items():
            if vals:
                c.check(min(vals) >= floor_half,
                        f"{path.name}: スタイル {styleid} の文字サイズが "
                        f"{body_floor_pt}pt 未満: {vals}")

    return {"tables": n_tbl, "xml_parts": len(xml_parts), "checks": c.count}


def pandoc_readback(path: Path) -> str:
    """docx を pandoc で plain テキストへ読み戻す（本文がどこまで到達しているかの検証用）。"""
    return subprocess.run(
        ["pandoc", "-f", "docx", "-t", "plain", "--wrap", "none", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout


def verify_talk_materials() -> dict:
    """結合版（第1部＋第2部）を検証する。"""
    c = Checker()
    common = verify_common(c, OUT_DOCX)

    with zipfile.ZipFile(OUT_DOCX) as z:
        doc = z.read("word/document.xml").decode("utf-8")
    page_breaks = doc.count('w:type="page"')

    text = pandoc_readback(OUT_DOCX)
    required = ["1画面カード", "30秒版", "2〜3分版", "5分版",
                "not individually field-confirmed quarry ponds",
                "113", "145", "127", "CC BY 4.0"]
    for r in required:
        c.check(r in text, f"{OUT_DOCX.name}: 本文に到達しない必須文字列: {r}")
    n_q = len(re.findall(r"^Q\d+-\d+\.", text, re.MULTILINE))
    c.check(n_q >= 33, f"{OUT_DOCX.name}: 想定問答の項目数が不足: {n_q}")

    c.finish()
    return {**common, "page_breaks": page_breaks, "questions": n_q,
            "text_chars": len(text), "checks": c.count}


def verify_qa() -> dict:
    """想定問答単独版を検証する。

    全体版の検証に加え、以下を確認する:
    - 想定問答集（`exp002_kitagi_foss4g2026_qa.md`）の33問すべてが Q番号・EN/JP問い・
      EN/JP回答つきで存在する（Q番号は正本 Markdown から動的に取得し、ハードコードしない）
    - 第1部（口頭説明スクリプト）由来の文字列が混入していない
    - 本文サイズが15pt下限を満たす（`verify_common` の `body_floor_pt` 経由）
    """
    c = Checker()
    common = verify_common(c, QA_OUT_DOCX, body_floor_pt=QA_BODY_FLOOR_PT)

    text = pandoc_readback(QA_OUT_DOCX)

    qa_src = QA_MD.read_text(encoding="utf-8")
    q_ids = re.findall(r"^### (Q\d+-\d+)\.", qa_src, re.MULTILINE)
    c.check(len(q_ids) == 33, f"{QA_MD.name}: 想定問答の項目数が33でない: {len(q_ids)}")

    for qid in q_ids:
        c.check(
            re.search(rf"^{re.escape(qid)}\.", text, re.MULTILINE) is not None,
            f"{QA_OUT_DOCX.name}: 本文に到達しない想定問答: {qid}",
        )
    n_q = len(re.findall(r"^Q\d+-\d+\.", text, re.MULTILINE))
    c.check(n_q == 33, f"{QA_OUT_DOCX.name}: 想定問答の項目数が33でない: {n_q}")

    for label, pattern in (
        ("JP 問い", r"^- JP:"),
        ("EN 回答", r"^- A \(EN\):"),
        ("JP 回答", r"^- A \(JP\):"),
        ("根拠欄", r"^- 根拠:"),
    ):
        n = len(re.findall(pattern, text, re.MULTILINE))
        c.check(n == 33, f"{QA_OUT_DOCX.name}: {label}が33件でない: {n}")

    # 第1部（口頭説明スクリプト）由来の内容が混じっていないこと
    part1_markers = ["1画面カード", "30秒版", "2〜3分版", "5分版",
                      "前提訂正", "当日資料", "第1部 口頭説明スクリプト"]
    for marker in part1_markers:
        c.check(marker not in text,
                f"{QA_OUT_DOCX.name}: 第1部由来の文字列が混入している: {marker}")

    c.finish()
    return {**common, "questions": n_q, "text_chars": len(text), "checks": c.count}


def verify() -> dict:
    """両方の docx を検証する（結合版・想定問答単独版）。"""
    return {"talk_materials": verify_talk_materials(), "qa": verify_qa()}


def main() -> None:
    # 1. 結合版（第1部＋第2部）
    md_path = build_markdown()
    print(f"combined markdown: {md_path.relative_to(PROJECT_ROOT)} "
          f"({len(md_path.read_text(encoding='utf-8')):,} chars)")
    run_pandoc(md_path, OUT_DOCX)
    n_tables = patch_docx(OUT_DOCX)
    size = OUT_DOCX.stat().st_size
    print(f"docx: {OUT_DOCX.relative_to(PROJECT_ROOT)} ({size:,} bytes)")
    print(f"  page: A4 portrait {PAGE_W}x{PAGE_H} twips, margins LR={MARGIN_LR} TB={MARGIN_TB}")
    print(f"  tables patched: {n_tables} (autofit / 100% width / borders / header repeat removed)")
    print(f"  fonts: ascii={FONT_ASCII}, eastAsia={FONT_EASTASIA}")

    # 2. 想定問答単独版（第2部のみ、目次なし）
    run_pandoc(QA_MD, QA_OUT_DOCX)
    n_tables_qa = patch_docx(QA_OUT_DOCX, body_floor_pt=QA_BODY_FLOOR_PT)
    size_qa = QA_OUT_DOCX.stat().st_size
    print(f"docx: {QA_OUT_DOCX.relative_to(PROJECT_ROOT)} ({size_qa:,} bytes)")
    print(f"  page: A4 portrait {PAGE_W}x{PAGE_H} twips, margins LR={MARGIN_LR} TB={MARGIN_TB}, "
          f"body floor={QA_BODY_FLOOR_PT}pt")
    print(f"  tables patched: {n_tables_qa} (autofit / 100% width / borders / header repeat removed)")

    r = verify()
    rt, rq = r["talk_materials"], r["qa"]
    print(f"verified talk materials: {rt['checks']} checks passed — "
          f"{rt['xml_parts']} XML parts well-formed, tables={rt['tables']}, "
          f"page breaks={rt['page_breaks']}, questions={rt['questions']}, "
          f"extracted text={rt['text_chars']:,} chars")
    print(f"verified qa-only: {rq['checks']} checks passed — "
          f"{rq['xml_parts']} XML parts well-formed, tables={rq['tables']}, "
          f"questions={rq['questions']}, extracted text={rq['text_chars']:,} chars")


if __name__ == "__main__":
    main()
