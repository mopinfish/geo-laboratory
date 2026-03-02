# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

地理空間情報に関する実験リポジトリ。実験計画・実装・結果・考察を体系的に管理する。主言語はPython。

## Directory Structure

- `docs/plans/` - 実験計画ドキュメント
- `docs/results/` - 実験結果
- `docs/reports/` - 学術論文形式のレポート
- `notebooks/` - Jupyter Notebook
- `src/` - ユーティリティクラス・各種モジュール
- `data/` - 実験データ
- `refs/` - 先行研究の論文等
- `tmp/` - 一時ファイル（Git管理外）
- `scripts/` - 繰り返し処理用スクリプト

## Conventions

- ドキュメントおよびコメントは日本語で記述する
- レポート（`docs/reports/`）は学術論文の形式に従う
- `tmp/` 配下のファイルはコミットしない

## ドキュメント規約

### レポート (`docs/reports/`)

実験結果の解釈・考察を学術論文形式でまとめる。構成はダイヤモンド構造（分野の紹介→課題の紹介→仮説・要件定義→アプローチ→実験ブロック→全体の解釈→課題への貢献→分野への貢献）に従う。

参考文献の記載規則:
- 「学術文献」と「プロジェクト内参照」の2セクションに分ける
- 学術文献には本分析との関連を `—` に続けて付記する
- 番号リストは使わず箇条書き（`- `）で記載する
- 和文献を先に五十音順、次に洋文献をアルファベット順に並べる
- 和雑誌: `著者名（出版年）文献名．「雑誌名」，**巻**（号），頁．`
- 和単行本: `著者名（出版年）『書名』，出版社．`
- 博士論文: `著者名（提出年）論文タイトル．博士論文，大学．`
- 洋雑誌: `Author, F. (Year) Title. *Journal Name*, **Vol**(Issue), Pages.`
- 洋単行本: `Author(s) (Year) *Book Title*. Place: Publisher.`
- 著者間は和文「・」、洋文「and」を使用（`&` は使わない）
- プロジェクト内参照: 計画書・ノートブック・データ等への相対パス

### 先行研究の管理 (`refs/`)

参照する論文は `refs/` に配置する。PDF等をマークダウン変換したファイルも同ディレクトリに格納する。
