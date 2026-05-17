from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_cli_generates_moving_average_backtest_report(tmp_path: Path) -> None:
    csv_path = tmp_path / "bars.csv"
    csv_path.write_text(
        "symbol,date,open,high,low,close\n"
        "AAA,2024-01-01,100,101,99,100\n"
        "AAA,2024-01-02,101,102,100,101\n"
        "AAA,2024-01-03,101,103,100,102\n"
        "AAA,2024-01-04,102,104,101,103\n"
        "AAA,2024-01-05,103,105,102,104\n"
        "BBB,2024-01-01,50,50.5,49.5,50\n"
        "BBB,2024-01-02,50.2,50.7,49.9,50.3\n"
        "BBB,2024-01-03,50.3,51,50,50.9\n",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(csv_path),
            "--symbol",
            "AAA",
            "--short-window",
            "2",
            "--long-window",
            "3",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Market Signal Experiment Report" in result.stdout
    assert "## Strategy Config" in result.stdout
    assert "## Metrics" in result.stdout
    assert "symbol: AAA" in result.stdout
