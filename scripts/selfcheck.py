#!/usr/bin/env python3
"""Project self-check utility.

Runs syntax compilation, test suite, and a CLI smoke test that writes
``reports/sample-report.md``.
"""

from __future__ import annotations

from pathlib import Path
import compileall
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = REPO_ROOT / "reports" / "sample-report.md"
CSV_PATH = REPO_ROOT / "examples" / "data" / "sample_tqqq_qld_like.csv"


def run_compileall() -> bool:
    print("1) Running Python compilation check...")
    # Compile the library and tests to catch syntax/import-time issues.
    ok = compileall.compile_dir(str(REPO_ROOT / "market_signal_lab"), quiet=1)
    ok &= compileall.compile_dir(str(REPO_ROOT / "tests"), quiet=1)
    return bool(ok)


def run_pytest() -> bool:
    print("2) Running pytest...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("pytest failed")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return False
    return True


def run_cli_smoke_test() -> bool:
    print("3) Running CLI smoke test...")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "market_signal_lab.cli",
        str(CSV_PATH),
        "--symbol",
        "QQQ_LIKE",
        "--short-window",
        "20",
        "--long-window",
        "50",
        "--fee-bps",
        "10.0",
        "--output",
        str(REPORT_PATH),
    ]

    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print("CLI smoke test failed")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return False

    if not REPORT_PATH.exists():
        print("CLI smoke test did not create reports/sample-report.md")
        return False

    if REPORT_PATH.stat().st_size == 0:
        print("CLI smoke test created an empty reports/sample-report.md")
        return False

    print(f"Created {REPORT_PATH.relative_to(REPO_ROOT)}")
    return True


def main() -> int:
    checks = [
        ("compileall", run_compileall),
        ("pytest", run_pytest),
        ("CLI smoke test", run_cli_smoke_test),
    ]

    passed = True
    for name, check in checks:
        if not check():
            print(f"FAIL: {name}")
            passed = False
        else:
            print(f"PASS: {name}")

    print("Selfcheck completed.")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
