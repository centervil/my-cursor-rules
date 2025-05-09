# Python Script Example for Generating Quality Dashboard Data
# 品質ダッシュボード用データ生成スクリプト例
# Source: project_management_guide.md (section 3.3 CI/CDパイプラインとの統合)
# Filename in guide: scripts/generate_dashboard.py

import json
import xml.etree.ElementTree as ET
from pathlib import Path
import datetime

# Define paths to report files (these would typically be artifacts from CI)
REPORTS_DIR = Path("./reports_input") # Assume reports are copied here by CI
COVERAGE_XML_FILE = REPORTS_DIR / "coverage.xml"
PYLINT_JSON_FILE = REPORTS_DIR / "pylint-report.json"
FLAKE8_TXT_FILE = REPORTS_DIR / "flake8-report.txt"

OUTPUT_DIR = Path("./dashboard_output")
OUTPUT_JSON_FILE = OUTPUT_DIR / "dashboard_data.json"
OUTPUT_HTML_FILE = OUTPUT_DIR / "quality_dashboard.html"

def parse_coverage_xml(file_path: Path) -> dict:
    # coverage.xmlからカバレッジ情報を抽出
    # ...（実装例は省略）
    return {"coverage": 85.0}

def parse_pylint_json(file_path: Path) -> dict:
    # pylint-report.jsonから警告・エラー数を集計
    # ...（実装例は省略）
    return {"pylint_score": 9.2, "errors": 1, "warnings": 3}

def parse_flake8_txt(file_path: Path) -> dict:
    """Parses flake8 text report to count total issues."""
    data = {"total_issues": 0}
    try:
        if not file_path.exists():
            print(f"Warning: Flake8 report not found: {file_path}")
            return data
        with open(file_path, 'r') as f:
            lines = f.readlines()
        data["total_issues"] = len([line for line in lines if line.strip()])
    except Exception as e:
        print(f"Error parsing Flake8 TXT: {e}")
    return data

def generate_html_report(dashboard_data: dict, output_file: Path):
    """Generates a simple HTML report from the dashboard data."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quality Dashboard</title>
        <style>
            body {{ font-family: sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }}
            .container {{ background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;}}
            h2 {{ color: #555; margin-top: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            .metric {{ font-size: 1.2em; }}
            .timestamp {{ font-size: 0.9em; color: #777; margin-bottom:20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Quality Dashboard</h1>
            <p class="timestamp">Report generated on: {dashboard_data['generation_timestamp']}</p>
            
            <h2>Test Coverage</h2>
            <p class="metric">Overall Coverage: <strong>{dashboard_data['coverage']['coverage_percentage']:.2f}%</strong></p>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Total Lines</td><td>{dashboard_data['coverage'].get('lines_total','N/A')}</td></tr>
                <tr><td>Covered Lines</td><td>{dashboard_data['coverage'].get('lines_covered','N/A')}</td></tr>
            </table>

            <h2>Static Analysis - Pylint</h2>
            <p class="metric">Total Pylint Issues: <strong>{dashboard_data['pylint']['total_issues']}</strong></p>
            <table>
                <tr><th>Type</th><th>Count</th></tr>
                <tr><td>Errors</td><td>{dashboard_data['pylint']['errors']}</td></tr>
                <tr><td>Warnings</td><td>{dashboard_data['pylint']['warnings']}</td></tr>
                <tr><td>Refactor</td><td>{dashboard_data['pylint']['refactor']}</td></tr>
                <tr><td>Convention</td><td>{dashboard_data['pylint']['convention']}</td></tr>
            </table>

            <h2>Static Analysis - Flake8</h2>
            <p class="metric">Total Flake8 Issues: <strong>{dashboard_data['flake8']['total_issues']}</strong></p>

        </div>
    </body>
    </html>
    """
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(html_content)
        print(f"HTML report generated: {output_file}")
    except Exception as e:
        print(f"Error generating HTML report: {e}")

def main():
    # レポートファイルのパス
    coverage = parse_coverage_xml(COVERAGE_XML_FILE)
    pylint = parse_pylint_json(PYLINT_JSON_FILE)
    # ...他ツールの集計も同様に
    # ダッシュボード用データを出力
    dashboard_data = {"coverage": coverage, "pylint": pylint}
    with open(OUTPUT_JSON_FILE, "w") as f:
        json.dump(dashboard_data, f, indent=2)
    print(f"Dashboard data JSON generated: {OUTPUT_JSON_FILE}")
        
    generate_html_report(dashboard_data, OUTPUT_HTML_FILE)

if __name__ == "__main__":
    main()
# 詳細な実装例・拡張はquality_dashboard_guide.md参照 