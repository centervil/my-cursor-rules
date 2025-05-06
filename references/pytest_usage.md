# Pytest 利用ガイド

これは `pytest` を利用する際の基本的なガイドラインとベストプラクティスです。

## 基本的な使い方

- **テスト実行**: プロジェクトルートで `pytest` コマンドを実行すると、`tests` ディレクトリ内の `test_*.py` または `*_test.py` という名前のファイルからテスト関数を自動で発見し実行します。
- **特定のテスト実行**: `pytest tests/unit/test_module.py::test_function` のように指定して特定のテスト関数やファイルのみを実行できます。
- **詳細表示**: `pytest -v` で詳細な情報を表示します。
- **カバレッジ測定**: `pytest --cov=my_package --cov-report=html` のように `pytest-cov` プラグインを使ってカバレッジを測定し、HTMLレポートを生成できます (`my_package` はテスト対象のパッケージ名)。

## テスト関数の書き方

- テスト関数は `def test_something():` のように `test_` で始まる名前をつけます。
- `assert` 文を使って期待される結果を検証します。
  ```python
  def test_addition():
      assert 1 + 1 == 2
  ```

## フィクスチャ (`conftest.py`)

- 複数のテストで共通して利用する前処理やテストデータは、`tests/conftest.py` にフィクスチャとして定義できます。
- フィクスチャはテスト関数に引数として渡すことで利用できます。
  ```python
  # conftest.py
  import pytest
  
  @pytest.fixture
  def sample_data():
      return {"key": "value"}
  
  # test_example.py
  def test_using_fixture(sample_data):
      assert sample_data["key"] == "value"
  ```

## ベストプラクティス

- **独立性**: 各テストは他のテストから独立しているべきです。テストの実行順序に依存しないようにします。
- **明確性**: テストの目的と検証内容が明確にわかるように、テスト名やアサーションを記述します。
- **網羅性**: 重要な機能やエッジケースをカバーするようにテストを作成します。
- **高速性**: テストは頻繁に実行されるため、可能な限り高速に動作するように心がけます。

詳細な情報は公式ドキュメントを参照してください: [pytest documentation](https://docs.pytest.org/) 