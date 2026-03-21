# geo-laboratory

地理空間情報に関する実験リポジトリ。実験計画・実装・結果・考察を体系的に管理する。

## セットアップ

### 前提条件

- Python 3.11以上
- [uv](https://docs.astral.sh/uv/)（パッケージマネージャ）

### 依存パッケージのインストール

```bash
uv sync
```

`pyproject.toml` に記載された全依存パッケージがインストールされ、`.venv/` に仮想環境が作成される。

### パッケージの追加

新しいパッケージが必要な場合は `uv add` で追加する。

```bash
uv add <パッケージ名>
```

## ノートブックの実行

```bash
uv run jupyter notebook
```

特定のノートブックを直接開く場合:

```bash
uv run jupyter notebook notebooks/<ノートブック名>.ipynb
```

`uv run` により `.venv` 内のPython環境で実行されるため、手動での仮想環境の有効化は不要。

## ディレクトリ構成

```
docs/
  plans/          実験計画ドキュメント
  experiments/    ノートブックと一対一で対応する実験内容ドキュメント
  reports/        学術論文形式のレポート
  presentations/  プレゼンテーション用発表資料（pptx形式）
  results/        実験結果
notebooks/        Jupyter Notebook
src/              ユーティリティクラス・各種モジュール
data/             実験データ
refs/             先行研究の論文等
scripts/          繰り返し処理用スクリプト
tmp/              一時ファイル（Git管理外）
```

## 実験一覧

| ID | テーマ | ノートブック |
|----|--------|------------|
| exp001 | 静岡県3都市の道路ネットワーク比較分析 | `notebooks/exp001_shizuoka_road_network.ipynb` |
| exp002 | 北木島（岡山県笠岡市）丁場水域検出 | `notebooks/exp002_kitagi_quarry_water_detection.ipynb` |
