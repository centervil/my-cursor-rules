## Semgrep (多言語SAST) 利用ガイド

Semgrep は、多言語に対応した高速な静的解析セキュリティテスト (SAST) ツールです。ルールセットに基づいてコードパターンを検出し、脆弱性やバグ、コーディング規約違反などを発見します。

### 1. インストール
```bash
pip install semgrep
# または、Dockerを利用
docker pull returntocorp/semgrep
```

### 2. 基本的な使い方
```bash
semgrep scan --config auto path/to/your/code
```
- `scan`: スキャンを実行するサブコマンド。
- `--config auto`: プロジェクト内の言語やフレームワークに基づいて、適切なルールセットを自動的に選択します。
- `--config <ruleset>`: 特定のルールセットを指定 (例: `p/python`, `p/javascript`, `r/java.spring.security`など)。利用可能なルールは [Semgrep Registry](https://semgrep.dev/explore) で確認できます。
- `--output <filename>`: 結果を指定ファイルに出力。
- `--json`: 結果をJSON形式で出力。
  ```bash
  semgrep scan --config auto --json --output semgrep-report.json src/
  ```

### 3. AIエージェントの役割 (mode_sast_execution.mdc から呼び出される場合)
1. **実行**: PMからの指示、CI/CDパイプライン、または自律的な判断に基づき、適切なルールセット (`--config auto` または特定のセット) を指定して `semgrep` を実行する。
2. **結果の解釈と報告**:
   - JSON出力を解析し、検出された問題 (Finding) を特定する。
   - 各Findingについて、以下をPMに報告する:
     - `check_id`: ルールID (例: `python.lang.security.dangerous-subprocess-use`)
     - `path`: 問題のあるファイル
     - `start.line`: 問題のある箇所の開始行
     - `end.line`: 問題のある箇所の終了行
     - `extra.message`: 問題の詳細な説明
     - `extra.severity`: 重要度 (ERROR, WARNING, INFO)
     - `extra.metadata.category`: カテゴリ (security, correctnessなど)
   - 誤検知の可能性がある場合はその旨を付記する。
3. **修正提案**: 可能な範囲で、具体的な修正コードを提案する。Semgrepの出力には修正案が含まれる場合があるため、それを参考にすることも有効。
4. **カスタムルールの検討**: プロジェクト固有のコーディング規約や脆弱性パターンがある場合、PMにカスタムルールの作成を提案・相談する。

### 4. ルールセット
- **Semgrep Registry**: [https://semgrep.dev/explore](https://semgrep.dev/explore) で公開されている多数のルールセットを利用可能。
- **カスタムルール**: YAML形式で独自のルールを作成可能。
  ```yaml
  rules:
    - id: no-print-in-prod
      patterns:
        - pattern: print(...)
      message: "Production code should not contain print statements."
      languages: [python]
      severity: WARNING
  ```

### 5. CI/CD連携
GitHub Actionsなどで簡単に連携可能。Semgrep CI を利用すると、PRへのコメント投稿などが自動化できます。
[Semgrep CI Documentation](https://semgrep.dev/docs/semgrep-ci/)

### 6. 参考
- [Semgrep公式サイト](https://semgrep.dev/)
- [Semgrepドキュメント](https://semgrep.dev/docs/) 