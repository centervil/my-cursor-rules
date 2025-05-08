# Python Script Example for Generating Quality Dashboard Data
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
    """Parses coverage.xml to extract key coverage metrics."""
    data = {"coverage_percentage": 0.0, "lines_total": 0, "lines_covered": 0, "branches_total": 0, "branches_covered": 0}
    try:
        if not file_path.exists():
            print(f"Warning: Coverage file not found: {file_path}")
            return data
        
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        data["coverage_percentage"] = float(root.get("line-rate", 0)) * 100
        # More detailed parsing can be added here for lines, branches, etc.
        # For simplicity, focusing on the main percentage.
        packages = root.find('packages')
        if packages is not None:
            lines_total, lines_covered = 0, 0
            branches_total, branches_covered = 0,0
            for package in packages.findall('package'):
                for class_element in package.find('classes').findall('class'):
                    lines = class_element.find('lines')
                    if lines is not None:
                        for line in lines.findall('line'):
                            lines_total += 1
                            if line.get('hits') != '0':
                                lines_covered += 1
                            # Branch coverage requires more complex parsing of condition-coverage attribute
            data["lines_total"] = lines_total
            data["lines_covered"] = lines_covered
            # Branch parsing would go here

    except Exception as e:
        print(f"Error parsing coverage XML: {e}")
    return data

def parse_pylint_json(file_path: Path) -> dict:
    """Parses pylint JSON report to count issues by type."""
    data = {"total_issues": 0, "errors": 0, "warnings": 0, "refactor": 0, "convention": 0}
    try:
        if not file_path.exists():
            print(f"Warning: Pylint report not found: {file_path}")
            return data
            
        with open(file_path, 'r') as f:
            issues = json.load(f)
        data["total_issues"] = len(issues)
        for issue in issues:
            if issue["type"].lower() == "error":
                data["errors"] += 1
            elif issue["type"].lower() == "warning":
                data["warnings"] += 1
            elif issue["type"].lower() == "refactor":
                data["refactor"] += 1
            elif issue["type"].lower() == "convention":
                data["convention"] += 1
    except Exception as e:
        print(f"Error parsing Pylint JSON: {e}")
    return data

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
    """Main function to generate dashboard data and HTML report."""
    # Ensure input directory exists for dummy file creation if needed
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    # Create dummy report files if they don't exist for standalone script execution
    if not COVERAGE_XML_FILE.exists():
        with open(COVERAGE_XML_FILE, 'w') as f:
            f.write('<coverage line-rate="0.85" version="6.0"><packages><package name="src" line-rate="0.85"><classes><class name="module.py" filename="src/module.py" line-rate="0.85"><lines><line number="1" hits="1"/><line number="2" hits="0"/></lines></class></classes></package></packages></coverage>')
    if not PYLINT_JSON_FILE.exists():
        with open(PYLINT_JSON_FILE, 'w') as f:
            json.dump([{"type": "error", "message": "dummy error"}], f)
    if not FLAKE8_TXT_FILE.exists():
        with open(FLAKE8_TXT_FILE, 'w') as f:
            f.write("src/module.py:1:1: E001 dummy flake8 error\n")

    coverage_data = parse_coverage_xml(COVERAGE_XML_FILE)
    pylint_data = parse_pylint_json(PYLINT_JSON_FILE)
    flake8_data = parse_flake8_txt(FLAKE8_TXT_FILE)

    dashboard_data = {
        "generation_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "coverage": coverage_data,
        "pylint": pylint_data,
        "flake8": flake8_data,
        # Add data from other tools here (e.g., Mypy, Bandit)
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(OUTPUT_JSON_FILE, 'w') as f:
            json.dump(dashboard_data, f, indent=4)
        print(f"Dashboard data JSON generated: {OUTPUT_JSON_FILE}")
    except Exception as e:
        print(f"Error writing dashboard JSON: {e}")
        
    generate_html_report(dashboard_data, OUTPUT_HTML_FILE)

if __name__ == "__main__":
    main() 