# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

地理空間情報に関する実験リポジトリ。実験計画・実装・結果・考察を体系的に管理する。主言語はPython。

## Directory Structure

- `docs/plans/` - 実験計画ドキュメント
- `docs/results/` - 実験結果
- `docs/reports/` - 学術論文形式のレポート
- `docs/presentations/` - プレゼンテーション用発表資料（pptx形式）
- `docs/experiments/` - ノートブックと一対一で対応する実験内容ドキュメント
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

### 実験ドキュメント (`docs/experiments/`)

`notebooks/` 配下の各ノートブックと一対一で対応するドキュメントを作成する。ノートブックの処理内容・設定定数・主要クラス・処理フロー・出力ファイル等を記載し、ノートブックを実行せずとも内容を把握できるようにする。

ファイル名はノートブックと対応させる（例: `exp001_shizuoka_road_network.ipynb` → `exp001_shizuoka_road_network.md`）。

構成:
- **見出し**: ノートブックファイル名 + 日本語の説明
- **概要**: ノートブックの目的と処理の全体像
- **重要な設定定数**: 分析パラメータをコードブロックで記載
- **主要クラス・関数**: 使用するクラス・関数のメソッド一覧と説明（テーブル形式）
- **処理フロー**: 処理の流れをテキストフローチャートで記載
- **出力ファイル**: 生成されるファイルの一覧（テーブル形式）
- **結果例**: 主要な結果の概要（実験実施後に記載）
- **次のステップ**: 後続の分析・作業への参照

### 発表資料 (`docs/presentations/`)

`docs/reports/` 配下のレポートをもとにプレゼンテーション用の発表資料をpptx形式で作成し、`docs/presentations/` に格納する。ファイル名はレポートと対応させる（例: `exp001_shizuoka_road_network_report.md` → `exp001_shizuoka_road_network_presentation.pptx`）。

### 先行研究の管理 (`refs/`)

参照する論文は `refs/` に配置する。PDF等をマークダウン変換したファイルも同ディレクトリに格納する。
