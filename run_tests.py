#!/usr/bin/env python3
"""
Test execution script for Autonomize AI Test Suite
Can be invoked within CI/CD pipeline
"""
import argparse
import sys
import subprocess
from pathlib import Path
import json


def run_tests(test_suite=None, marker=None, html_report=True, json_report=True, coverage=True):
    """
    Run test suite with specified options
    
    Args:
        test_suite: Specific test suite to run (agent_integration, model_integration, etc.)
        marker: Pytest marker to filter tests (p0, p1, etc.)
        html_report: Generate HTML report
        json_report: Generate JSON report
        coverage: Generate coverage report
    """
    # Base pytest command (use uv run if available, otherwise direct pytest)
    import shutil
    if shutil.which("uv"):
        cmd = ["uv", "run", "pytest", "-v"]
    else:
        cmd = ["pytest", "-v"]
    
    # Add test path
    if test_suite:
        test_path = f"tests/{test_suite}/"
    else:
        test_path = "tests/"
    cmd.append(test_path)
    
    # Add marker if specified
    if marker:
        cmd.extend(["-m", marker])
    
    # Add HTML report
    if html_report:
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        cmd.extend([
            "--html=reports/report.html",
            "--self-contained-html"
        ])
    
    # Add JSON report
    if json_report:
        cmd.extend([
            "--json-report",
            "--json-report-file=reports/report.json"
        ])
    
    # Add coverage
    if coverage:
        cmd.extend([
            "--cov=tests",
            "--cov-report=html:reports/coverage",
            "--cov-report=term-missing"
        ])
    
    # Add JUnit XML for CI/CD
    cmd.extend([
        "--junitxml=reports/junit.xml"
    ])
    
    # Run tests
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    
    return result.returncode


def generate_summary_report():
    """Generate summary report from JSON test results"""
    report_file = Path("reports/report.json")
    
    if not report_file.exists():
        print("No JSON report found")
        return
    
    with open(report_file, 'r') as f:
        report_data = json.load(f)
    
    summary = {
        "total_tests": report_data.get("summary", {}).get("total", 0),
        "passed": report_data.get("summary", {}).get("passed", 0),
        "failed": report_data.get("summary", {}).get("failed", 0),
        "skipped": report_data.get("summary", {}).get("skipped", 0),
        "duration": report_data.get("duration", 0)
    }
    
    # Calculate pass rate
    if summary["total_tests"] > 0:
        summary["pass_rate"] = (summary["passed"] / summary["total_tests"]) * 100
    else:
        summary["pass_rate"] = 0
    
    # Print summary
    print("\n" + "="*50)
    print("TEST EXECUTION SUMMARY")
    print("="*50)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Skipped: {summary['skipped']}")
    print(f"Pass Rate: {summary['pass_rate']:.2f}%")
    print(f"Duration: {summary['duration']:.2f}s")
    print("="*50)
    
    # Defect summary
    if report_data.get("tests"):
        failed_tests = [t for t in report_data["tests"] if t.get("outcome") == "failed"]
        if failed_tests:
            print("\nDEFECT SUMMARY")
            print("-"*50)
            for test in failed_tests:
                print(f"Test: {test.get('nodeid', 'Unknown')}")
                if test.get("call", {}).get("longrepr"):
                    error = test["call"]["longrepr"][:200]  # First 200 chars
                    print(f"Error: {error}")
                print()
    
    # Recommendations
    print("\nRECOMMENDATIONS")
    print("-"*50)
    if summary["pass_rate"] < 80:
        print("⚠️  Pass rate is below 80%. Review failed tests immediately.")
    if summary["failed"] > 0:
        print("⚠️  Failed tests detected. Investigate and fix before deployment.")
    if summary["pass_rate"] >= 95:
        print("✅ Excellent pass rate. Proceed with confidence.")
    print()
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="Run Autonomize AI Test Suite")
    parser.add_argument(
        "--suite",
        choices=["agent_integration", "model_integration", "ui_ux_validation", "safety_privacy"],
        help="Specific test suite to run"
    )
    parser.add_argument(
        "--marker",
        choices=["p0", "p1", "p2", "p3", "smoke", "regression"],
        help="Pytest marker to filter tests"
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Skip HTML report generation"
    )
    parser.add_argument(
        "--no-json",
        action="store_true",
        help="Skip JSON report generation"
    )
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Skip coverage report generation"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Generate summary report after tests"
    )
    
    args = parser.parse_args()
    
    # Run tests
    exit_code = run_tests(
        test_suite=args.suite,
        marker=args.marker,
        html_report=not args.no_html,
        json_report=not args.no_json,
        coverage=not args.no_coverage
    )
    
    # Generate summary if requested
    if args.summary or exit_code != 0:
        generate_summary_report()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

