## Trivy (多目的SCA・コンテナスキャン) 利用ガイド

Trivy は、コンテナイメージ、ファイルシステム、Gitリポジトリ内のOSパッケージやアプリケーション依存関係の脆弱性を検出できる包括的なスキャナです。ソフトウェアコンポジション解析 (SCA) としても、コンテナセキュリティスキャンツールとしても利用されます。

### 1. インストール
[Trivy Installation Guide](https://aquasecurity.github.io/trivy/v0.50/getting-started/installation/) を参照 (OSごとのバイナリ、Dockerイメージ、Homebrewなど多数の方法あり)。

### 2. 基本的な使い方

- **コンテナイメージのスキャン:**
  ```bash
  trivy image <イメージ名>
  # 例: trivy image python:3.9-slim
  ```

- **ファイルシステム (ディレクトリ) のスキャン (依存関係ファイルを含む):**
  ```bash
  trivy fs path/to/your/project
  # 例: trivy fs .
  ```
  プロジェクトルートで実行すると、`requirements.txt`, `Pipfile.lock`, `pom.xml`, `package-lock.json` などを自動で検出しスキャンします。

- **Gitリポジトリのスキャン:**
  ```bash
  trivy repo <リポジトリURL>
  # 例: trivy repo https://github.com/your/repo
  ```

- **特定の脆弱性タイプのみスキャン:**
  - `--vuln-type os`: OSパッケージの脆弱性のみ
  - `--vuln-type library`: アプリケーションライブラリの脆弱性のみ

- **出力フォーマット指定:**
  - `-f json`: JSON形式で出力
    ```bash
    trivy image -f json -o trivy-report.json myapp:latest
    trivy fs --vuln-type library -f json -o trivy-lib-report.json .
    ```
  - `-f table`: 表形式 (デフォルト)
  - `-f template --template "@<テンプレートファイル>"`: カスタムテンプレートで出力

- **深刻度フィルタリング:**
  - `--severity CRITICAL,HIGH`: 指定した深刻度以上の脆弱性のみ表示

### 3. AIエージェントの役割 (mode_sca_execution.mdc または mode_container_security_scan.mdc から呼び出される場合)

1.  **実行対象とコマンドの選択**: PMの指示やコンテキスト (コンテナイメージビルド後か、コードスキャンか) に基づき、適切なTrivyコマンド (`image`, `fs`, `repo`) とオプションを選択して実行する。
2.  **結果の解釈と報告**:
    - JSON出力を解析し、検出された脆弱性 (Vulnerability) を特定する。
    - 各脆弱性について、以下をPMに報告する:
        - `Target`: スキャン対象 (例: `python:3.9-slim (debian 11.3)` や `requirements.txt`)
        - `Class` (Trivy v0.24以前) / `Type` (Trivy v0.25以降): 脆弱性の種類 (os-pkgs, lang-pkgs)
        - `VulnerabilityID`: 脆弱性ID (CVE-xxxx-xxxx, GHSA-xxxx-xxxx-xxxxなど)
        - `PkgName`: パッケージ名
        - `InstalledVersion`: 現在のバージョン
        - `FixedVersion`: 修正済みバージョン (存在する場合)
        - `Severity`: 深刻度 (CRITICAL, HIGH, MEDIUM, LOW, UNKNOWN)
        - `Title` / `Description`: 脆弱性の概要
    - 特に `FixedVersion` が提供されている場合は、アップデートを強く推奨する。
3.  **修正提案 (アップデート提案)**:
    - 脆弱性が見つかったパッケージについて、`FixedVersion` で示された安全なバージョンへのアップデートを提案する。
    - OSパッケージの脆弱性の場合、ベースイメージの更新や特定のパッケージの更新を提案する。
4.  **CI/CD連携**: CI/CDパイプラインに組み込み、イメージビルド後やコードマージ前にスキャンを実行し、結果に応じてビルドを制御するようにPMに設定を促す。

### 4. 注意点
- `trivy fs` でライブラリの脆弱性をスキャンする場合、言語によっては適切なロックファイル (`Pipfile.lock`, `package-lock.json` など) が存在するとより精度が向上します。
- 脆弱性データベースは定期的に更新されるため、Trivy自体やデータベースの更新も重要です (`trivy --download-db-only`)。

### 5. 参考
- [Trivy 公式ドキュメント](https://aquasecurity.github.io/trivy/)
- [Trivy GitHub](https://github.com/aquasecurity/trivy) 