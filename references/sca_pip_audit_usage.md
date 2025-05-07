## pip-audit (Python SCA) 利用ガイド

pip-audit は、Pythonプロジェクトの依存関係 (`requirements.txt` や `pyproject.toml` など) をスキャンし、既知の脆弱性 (CVE) を持つパッケージを検出するソフトウェアコンポジション解析 (SCA) ツールです。

### 1. インストール
```bash
pip install pip-audit
```

### 2. 基本的な使い方
プロジェクトのルートディレクトリや、依存関係ファイルがあるディレクトリで実行します。

- **requirements.txt をスキャン:**
  ```bash
  pip-audit -r requirements.txt
  ```
- **pyproject.toml (PoetryやFlitなど) をスキャン:**
  ```bash
  pip-audit
  ```
  (カレントディレクトリに `pyproject.toml` があれば自動で検知)
- **インストール済みの環境をスキャン:**
  ```bash
  pip-audit
  ```
  (アクティブなPython環境のパッケージをスキャン)

- **出力フォーマット指定:**
  - `-f json`: JSON形式で出力
    ```bash
    pip-audit -r requirements.txt -f json > pip-audit-report.json
    ```
  - `-f markdown`: Markdown形式で出力 (表形式)

- **脆弱性データベースのソース指定:**
  デフォルトは `PyPI` (OSV経由)。特定のデータベースを指定することも可能 (例: `vulnspy`)。

### 3. AIエージェントの役割 (mode_sca_execution.mdc から呼び出される場合)
1. **実行**: PMからの指示、CI/CDパイプライン、または依存関係更新時に自律的に `pip-audit` を実行する。
   - プロジェクトの依存関係管理ファイル (通常は `requirements.txt` または `pyproject.toml`) を対象とする。
2. **結果の解釈と報告**:
   - JSON出力を解析し、脆弱性が見つかった依存関係を特定する。
   - 各脆弱性について、以下をPMに報告する:
     - `name`: 脆弱性のあるパッケージ名
     - `version`: 現在のバージョン
     - `vulns[].id`: 脆弱性ID (例: CVE-2023-XXXXX, PYSEC-YYYY-ZZZ)
     - `vulns[].fix_versions`: 修正済みバージョン (存在する場合)
     - `vulns[].description`: 脆弱性の説明
   - 特に `fix_versions` が提供されている場合は、アップデートを強く推奨する。
3. **修正提案 (アップデート提案)**:
   - 脆弱性が見つかったパッケージについて、`fix_versions` で示された安全なバージョンへのアップデートを提案する。
   - アップデートによる互換性の問題がないか、関連するテストを実行して確認することを推奨する。
   - `GitHub Dependabot` と連携している場合は、DependabotからのPRの確認も促す。
4. **CI/CD連携**: CI/CDパイプラインに組み込み、脆弱性が検出された場合にビルドを失敗させるか警告を出すようにPMに設定を促す。

### 4. 注意点
- 脆弱性データベースは常に更新されるため、定期的なスキャンが重要です。
- 修正バージョンが存在しない場合や、アップデートによる影響が大きい場合は、PMとリスク評価や代替策を検討する必要があります。

### 5. 参考
- [pip-audit GitHub](https://github.com/pypa/pip-audit)
- [Open Source Vulnerabilities (OSV) database](https://osv.dev/) 