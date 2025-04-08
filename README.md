# Python自習

## 環境情報

- Python 3.11.11 (自分はpyenv使ってます)
- 仮想環境には venv を使用
- 必要なパッケージは `requirements.txt` を参照してください

## セットアップ手順（例）

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 開発・テスト用パッケージ

このプロジェクトでは `pytest` を使用しています。
`pytest` をインストールすれば、必要な依存（pluggy, packaging, iniconfig など）は自動で解決されます。

