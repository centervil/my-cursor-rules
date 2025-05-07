## Bandit (Python SAST) 利用ガイド

Bandit は Python コード向けの静的解析セキュリティテスト (SAST) ツールです。

### 1. インストール
```bash
pip install bandit
```

### 2. 基本的な使い方
プロジェクトのルートディレクトリで以下を実行します。
```bash
bandit -r path/to/your/python_code
```
- `-r`: 再帰的にスキャン
- `-f <format>`: 出力フォーマット指定 (例: `json`, `csv`, `html`)
  ```bash
  bandit -r src/ -f json -o bandit-report.json
  ```
- `-c <config_file>`: 設定ファイル指定 (例: `bandit.yaml`)

### 3. AIエージェントの役割 (mode_sast_execution.mdc から呼び出される場合)
1. **実行**: PMからの指示またはCI/CDパイプライン経由で `bandit` を適切なオプションで実行する。
2. **結果の解釈と報告**:
   - 出力 (特にJSON形式) を解析し、検出された問題 (Issue) を特定する。
   - 各Issueについて、以下をPMに報告する:
     - `test_id`: 問題の種類 (例: `B101` - assert文の使用)
     - `filename`: 問題のあるファイル
     - `line_number`: 問題のある行番号
     - `issue_text`: 問題の説明
     - `issue_severity`: 重要度 (High, Medium, Low)
     - `issue_confidence`: 信頼度 (High, Medium, Low)
   - 誤検知の可能性がある場合はその旨を付記する。
3. **修正提案**: 可能な範囲で、具体的な修正コードを提案する。
   - 例えば、`B101` (assert文) であれば、デバッグ目的以外での使用でないか確認を促すか、適切なエラーハンドリングへの変更を提案する。
   - `B608` (SQLインジェクションの可能性) であれば、プレースホルダの使用などを提案する。
4. **CI/CD連携**: GitHub ActionsなどのCI/CDパイプラインで実行される場合、結果をPRのコメントとして投稿したり、特定レベル以上の脆弱性があればビルドを失敗させるようにPMに設定を促す。

### 4. よく使われるオプション
- `-s <test_ids>`: 特定のテストIDのみ実行 (例: `-s B101,B608`)
- `-t <confidence_level>`: 指定した信頼度レベル以上の問題のみ報告 (例: `-t MEDIUM`)
- `-l <severity_level>`: 指定した重要度レベル以上の問題のみ報告 (例: `-l HIGH`)

### 5. 設定ファイル (bandit.yaml)
```yaml
tests:
  - B101 # assert_used
  - B608 # hardcoded_sql_expressions
skips:
  - B303 # md5
```
特定のテストを含めたり、スキップしたりできます。

### 6. 参考
- [Bandit GitHub](https://github.com/PyCQA/bandit) 