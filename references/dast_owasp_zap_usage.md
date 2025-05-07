## OWASP ZAP (DAST) 利用ガイド

OWASP ZAP (Zed Attack Proxy) は、実行中のWebアプリケーションの脆弱性を検出するための動的アプリケーションセキュリティテスト (DAST) ツールです。

### 1. インストールと起動
- **デスクトップ版**: [公式サイト](https://www.zaproxy.org/download/) からダウンロードしてインストール。
- **Docker版**: `docker run -u zap -p 8080:8080 -i owasp/zap2docker-stable zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true -config api.key=<YOUR_API_KEY>` (APIキーは適宜設定)

### 2. 基本的なスキャン方法 (AIエージェントがAPI経由で操作する場合)
ZAP APIを利用してスキャンを実行します。PMはターゲットURLやスキャンポリシーを設定・指示します。

**スキャン手順の概要 (API経由):**
1.  **ターゲットURLの設定**: スキャン対象のアプリケーションURLを指定。
2.  **Spider (クローラー) の実行**: アプリケーションの構造を把握。
    - `zap.spider.scan(url=target_url)`
3.  **Active Scan (動的スキャン) の実行**: 実際に攻撃リクエストを送信して脆弱性を検査。
    - `zap.ascan.scan(url=target_url, recurse=True, scanpolicyname='Default Policy')` (スキャンポリシーはPMが指示)
4.  **結果の取得**: スキャン結果 (アラート) を取得。
    - `zap.core.alerts(baseurl=target_url)`

Pythonクライアントライブラリ (`python-owasp-zap-v2.4`) の利用例:
```python
from zapv2 import ZAPv2

target_url = 'http://yourapp.com'
zap = ZAPv2(apikey='YOUR_API_KEY', proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

# Spiderの実行
zap.spider.scan(target_url)
while (int(zap.spider.status(scanid)) < 100):
    time.sleep(1)

# Active Scanの実行
zap.ascan.scan(target_url, scanpolicyname='Default Policy') # Default PolicyはPMの指示で変更
while (int(zap.ascan.status(scanid)) < 100):
    time.sleep(1)

# 結果の取得
alerts = zap.core.alerts(baseurl=target_url)
for alert in alerts:
    print(f"Alert: {alert['alert']}, Risk: {alert['risk']}, URL: {alert['url']}")
```

### 3. AIエージェントの役割 (mode_dast_execution.mdc から呼び出される場合)
1. **準備**: PMからスキャン対象のURL、認証情報 (必要な場合)、スキャンポリシー名などの指示を受け取る。
2. **スキャン実行**: 上記のようなAPI呼び出しを通じて、SpiderおよびActive Scanを実行する。
3. **結果の解釈と報告**:
   - 取得したアラート情報を解析する。
   - 各アラートについて、以下をPMに報告する:
     - `alert`: 脆弱性の名称 (例: Cross Site Scripting (Reflected))
     - `risk`: リスクレベル (High, Medium, Low, Informational)
     - `confidence`: 信頼度
     - `url`: 脆弱性が検出されたURL
     - `param`: 関連するパラメータ
     - `description`: 詳細説明
     - `solution`: 推奨される対策
   - 特にリスクレベルが高いものや信頼度が高いものを優先して報告する。
4. **簡単な修正提案**: 設定変更や単純な入力バリデーションで対応可能な脆弱性については、修正方法を提案する。
5. **CI/CD連携**: CI/CDパイプライン (ステージング環境デプロイ後など) で実行されるようにPMに設定を促し、結果を自動的に報告する仕組みを提案する。

### 4. スキャンポリシー
ZAPはスキャンポリシーによって、どのような脆弱性をテストするかを制御します。デフォルトポリシー以外にも、特定のテスト項目に絞ったポリシーや、より攻撃的なポリシーなどを作成・利用できます (PMが設定)。

### 5. 注意点
- **対象環境への影響**: Active Scanは実際に攻撃リクエストを送信するため、本番環境ではなく、ステージング環境やテスト環境に対して実行することが原則です。
- **スキャン時間**: 大規模なアプリケーションの場合、スキャンに時間がかかることがあります。
- **認証**: 認証が必要なページのスキャンには、適切な認証設定が必要です (ZAPのコンテキスト設定など)。

### 6. 参考
- [OWASP ZAP公式サイト](https://www.zaproxy.org/)
- [ZAP APIドキュメント](https://www.zaproxy.org/docs/api/)
- [python-owasp-zap-v2.4 PyPI](https://pypi.org/project/python-owasp-zap-v2.4/) 