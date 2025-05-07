## Hadolint (Dockerfile静的解析) 利用ガイド

Hadolint は、Dockerfile のベストプラクティス違反や一般的なエラーをチェックする静的解析ツールです。ShellCheck を利用して `RUN` 命令内のスクリプトも検証します。

### 1. インストール
- **Dockerイメージを利用 (推奨):**
  ```bash
  docker pull hadolint/hadolint
  ```
- **バイナリをダウンロード:** [Hadolint Releases](https://github.com/hadolint/hadolint/releases) からOSに合ったバイナリをダウンロード。
- **Homebrew (macOS):**
  ```bash
  brew install hadolint
  ```

### 2. 基本的な使い方
- **Dockerイメージ経由での実行:**
  ```bash
  docker run --rm -i hadolint/hadolint < Dockerfile
  # または
  docker run --rm -v $(pwd)/Dockerfile:/Dockerfile hadolint/hadolint /Dockerfile
  ```
- **インストール済みのバイナリで実行:**
  ```bash
  hadolint Dockerfile
  ```

- **出力フォーマット:** デフォルトはプレーンテキスト。JSON形式もサポート。
  ```bash
  hadolint --format json Dockerfile > hadolint-report.json
  ```

### 3. AIエージェントの役割 (mode_container_security_scan.mdc から呼び出される場合)
1. **実行**: PMからの指示、CI/CDパイプライン (Dockerfile変更時やイメージビルド前)、または自律的に `hadolint` を対象の `Dockerfile` に対して実行する。
2. **結果の解釈と報告**:
   - 出力 (特にJSON形式) を解析し、検出された問題を特定する。
   - 各問題について、以下をPMに報告する:
     - `file`: 対象ファイル名 (通常 Dockerfile)
     - `line`: 問題のある行番号
     - `code`: ルールID (例: `DL3006`, `SC2035`)
     - `level`: 重要度 (error, warning, info, style)
     - `message`: 問題の説明
   - 特に `error` や `warning` レベルの指摘を優先して報告する。
3. **修正提案**: 検出された問題に対して、Dockerfileの修正案を具体的に提案する。
   - 例: `DL3006` (Always tag the version of an image explicitly) -> `FROM ubuntu` を `FROM ubuntu:22.04` のように修正提案。
   - 例: `DL3008` (Pin versions in apt get install) -> `apt-get install -y <package>` を `apt-get install -y <package>=<version>` のように修正提案。
   - 例: `SC2035` (Use ./*glob* or -- *glob* so names with dashes won't become options) -> `RUN rm -rf *` を `RUN rm -rf ./*` に修正提案。
4. **CI/CD連携**: CI/CDパイプラインに組み込み、Dockerfileの変更時に自動的にチェックし、問題があれば警告またはビルド失敗とするようにPMに設定を促す。

### 4. よくある指摘と対応例
- **DL3000番台**: Dockerfileの書き方に関するHadolint独自のルール。
  - `DL3002`: `apt-get update` の後に `rm -rf /var/lib/apt/lists/*` を推奨。
  - `DL3018`: `apk add` でバージョンをピン止めすることを推奨。
- **SCxxxx番台**: ShellCheckによるシェルスクリプトの指摘。

### 5. 設定ファイル (`.hadolint.yaml`)
プロジェクトルートに設定ファイル を置くことで、特定のルールを無視したり、信頼するレジストリを指定したりできます。
```yaml
ignored:
  - DL3006 # Always tag the version of an image explicitly
  - SC2086 # Double quote to prevent globbing and word splitting

trustedRegistries:
  - docker.io
  - my-company.com:5000
```

### 6. 参考
- [Hadolint GitHub](https://github.com/hadolint/hadolint)
- [Hadolint Wiki (ルール一覧など)](https://github.com/hadolint/hadolint/wiki)
- [ShellCheck (SCxxxxルールの詳細)](https://www.shellcheck.net/) 