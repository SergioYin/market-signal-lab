from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from market_signal_lab.report import EXPOSURE_TRADE_REVIEW_NOTE


SAMPLE_DATA = Path("examples/data/sample_tqqq_qld_like.csv")


def test_cli_prints_version_without_requiring_csv_path() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--version",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == "market-signal-lab 1.1.0\n"
    assert result.stderr == ""


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
    assert "- **Buy-and-hold total return**: 4.00%" in result.stdout
    assert "- **Strategy minus buy-and-hold return**: -2.04%" in result.stdout
    assert "## Strategy Config" in result.stdout
    assert "## Metrics" in result.stdout
    assert "symbol: AAA" in result.stdout


def test_cli_writes_backtest_json_report(tmp_path: Path) -> None:
    csv_path = tmp_path / "bars.csv"
    json_path = tmp_path / "backtest-report.json"
    csv_path.write_text(
        "symbol,date,open,high,low,close\n"
        "AAA,2024-01-01,100,101,99,100\n"
        "AAA,2024-01-02,101,102,100,101\n"
        "AAA,2024-01-03,101,103,100,102\n"
        "AAA,2024-01-04,102,104,101,103\n"
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
            "--json-output",
            str(json_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Market Signal Experiment Report" in result.stdout
    payload = json.loads(json_path.read_text())
    assert payload["strategy_config"] == {
        "short_window": 2,
        "long_window": 3,
        "symbol": "AAA",
    }
    assert set(payload["metrics"]) == {
        "total_return",
        "buy_and_hold_total_return",
        "strategy_minus_buy_and_hold_return",
        "annualized_return",
        "max_drawdown",
        "volatility",
        "sharpe_like",
        "win_rate",
    }
    assert abs(payload["metrics"]["buy_and_hold_total_return"] - 0.03) < 1e-12
    assert (
        abs(
            payload["metrics"]["strategy_minus_buy_and_hold_return"]
            + 0.02019607843137261
        )
        < 1e-12
    )
    assert payload["exposure_trade_review"] == {
        "period_count": 3,
        "periods_in_market": 1,
        "periods_in_cash": 2,
        "percent_periods_in_market": 1 / 3,
        "percent_periods_in_cash": 2 / 3,
        "average_exposure": 1 / 3,
        "exposure_changes": 1,
        "entries_to_market": 1,
        "exits_to_cash": 0,
        "total_fee_drag": 0.0,
        "research_only": True,
        "note": EXPOSURE_TRADE_REVIEW_NOTE,
    }
    assert payload["first_date"] == "2024-01-01"
    assert payload["last_date"] == "2024-01-04"
    assert payload["row_count"] == 4


def test_cli_writes_backtest_html_report(tmp_path: Path) -> None:
    csv_path = tmp_path / "bars.csv"
    html_path = tmp_path / "backtest-report.html"
    csv_path.write_text(
        "symbol,date,open,high,low,close\n"
        "AAA,2024-01-01,100,101,99,100\n"
        "AAA,2024-01-02,101,102,100,101\n"
        "AAA,2024-01-03,101,103,100,102\n"
        "AAA,2024-01-04,102,104,101,103\n"
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
            "--html-output",
            str(html_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Market Signal Experiment Report" in result.stdout
    html = html_path.read_text()
    assert "<!doctype html>" in html
    assert "<h1>Market Signal Experiment Report</h1>" in html
    assert "<li><strong>Backtest total return</strong>:" in html
    assert "Research-only" in html


def test_cli_backtest_outputs_validation_split_metadata(tmp_path: Path) -> None:
    csv_path = tmp_path / "bars.csv"
    json_path = tmp_path / "backtest-report.json"
    csv_path.write_text(
        "symbol,date,open,high,low,close\n"
        "AAA,2024-01-01,100,101,99,100\n"
        "AAA,2024-01-02,101,102,100,101\n"
        "AAA,2024-01-03,101,103,100,102\n"
        "AAA,2024-01-04,102,104,101,103\n"
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
            "--split-ratio",
            "0.5",
            "--json-output",
            str(json_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "## Validation split" in result.stdout
    assert "Research metadata only" in result.stdout
    payload = json.loads(json_path.read_text())
    assert payload["validation_split"] == {
        "train": {
            "first_date": "2024-01-01",
            "last_date": "2024-01-02",
            "row_count": 2,
        },
        "test": {
            "first_date": "2024-01-03",
            "last_date": "2024-01-04",
            "row_count": 2,
        },
        "research_only": True,
        "note": "Validation split metadata is a research note, not trading guidance.",
        "method": "ratio",
        "split_ratio": 0.5,
    }


def test_cli_loads_backtest_config_file(tmp_path: Path) -> None:
    csv_path = tmp_path / "bars.csv"
    json_path = tmp_path / "backtest-report.json"
    csv_path.write_text(
        "symbol,date,open,high,low,close\n"
        "AAA,2024-01-01,100,101,99,100\n"
        "AAA,2024-01-02,101,102,100,101\n"
        "AAA,2024-01-03,101,103,100,102\n"
        "AAA,2024-01-04,102,104,101,103\n"
    )
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "csv_path": str(csv_path),
                "symbol": "AAA",
                "short_window": 2,
                "long_window": 3,
                "fee_bps": 1.5,
                "json_output": str(json_path),
            }
        )
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--config",
            str(config_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Market Signal Experiment Report" in result.stdout
    payload = json.loads(json_path.read_text())
    assert payload["strategy_config"] == {
        "short_window": 2,
        "long_window": 3,
        "symbol": "AAA",
        "fee_bps": 1.5,
    }


def test_cli_flags_override_config_values(tmp_path: Path) -> None:
    config_output = tmp_path / "config-sweep.md"
    override_output = tmp_path / "override-sweep.md"
    json_path = tmp_path / "sweep-report.json"
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "csv_path": str(SAMPLE_DATA),
                "symbol": "QQQ_LIKE",
                "sweep": True,
                "short_windows": [1, 2],
                "long_windows": [2, 3],
                "top_n": 3,
                "split_ratio": 0.5,
                "output": str(config_output),
                "json_output": str(json_path),
            }
        )
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--config",
            str(config_path),
            "--top-n",
            "1",
            "--output",
            str(override_output),
            "--split-cutoff",
            "2024-01-08",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert not config_output.exists()
    report = override_output.read_text()
    assert report.count("\n| 1 |") == 1
    assert "\n| 2 |" not in report
    payload = json.loads(json_path.read_text())
    assert payload["sweep_config"]["top_n"] == 1
    assert payload["validation_split"]["method"] == "cutoff"
    assert payload["validation_split"]["split_cutoff"] == "2024-01-08"
    assert len(payload["ranked_results"]) == 1


def test_cli_positional_csv_path_overrides_config_csv_path(tmp_path: Path) -> None:
    config_csv_path = tmp_path / "config-bars.csv"
    override_csv_path = tmp_path / "override-bars.csv"
    json_path = tmp_path / "backtest-report.json"
    config_csv_path.write_text(
        "symbol,date,open,high,low,close\n"
        "CONFIG,2024-01-01,100,101,99,100\n"
        "CONFIG,2024-01-02,101,102,100,101\n"
        "CONFIG,2024-01-03,101,103,100,102\n"
    )
    override_csv_path.write_text(
        "symbol,date,open,high,low,close\n"
        "OVERRIDE,2024-01-01,100,101,99,100\n"
        "OVERRIDE,2024-01-02,101,102,100,101\n"
        "OVERRIDE,2024-01-03,101,103,100,102\n"
    )
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "csv_path": str(config_csv_path),
                "symbol": "OVERRIDE",
                "short_window": 1,
                "long_window": 2,
                "json_output": str(json_path),
            }
        )
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(override_csv_path),
            "--config",
            str(config_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(json_path.read_text())
    assert payload["strategy_config"]["symbol"] == "OVERRIDE"
    assert payload["row_count"] == 3


def test_cli_rejects_non_standard_json_config_constant(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text('{"csv_path": "bars.csv", "fee_bps": NaN}')

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--config",
            str(config_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "Invalid JSON constant: NaN" in result.stderr


def test_cli_rejects_invalid_config_type(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"csv_path": 123}))

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--config",
            str(config_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "Config option 'csv_path' must be a string path" in result.stderr


def test_cli_rejects_non_object_config(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(["csv_path", str(SAMPLE_DATA)]))

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--config",
            str(config_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "Config file must contain a JSON object" in result.stderr


def test_cli_rejects_unknown_config_key(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"csv_path": str(SAMPLE_DATA), "broker_order": "buy"})
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--config",
            str(config_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "Unknown config option(s): broker_order" in result.stderr


def test_cli_rejects_config_split_ratio_and_cutoff(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "csv_path": str(SAMPLE_DATA),
                "split_ratio": 0.5,
                "split_cutoff": "2024-01-08",
            }
        )
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--config",
            str(config_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "choose only one validation split option" in result.stderr


def test_cli_writes_markdown_manifest(tmp_path: Path) -> None:
    csv_path = tmp_path / "bars.csv"
    report_path = tmp_path / "backtest-report.md"
    manifest_path = tmp_path / "manifest.md"
    csv_path.write_text(
        "symbol,date,open,high,low,close\n"
        "AAA,2024-01-01,100,101,99,100\n"
        "AAA,2024-01-02,101,102,100,101\n"
        "AAA,2024-01-03,101,103,100,102\n"
        "AAA,2024-01-04,102,104,101,103\n"
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
            "--fee-bps",
            "1.5",
            "--output",
            str(report_path),
            "--manifest-output",
            str(manifest_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    manifest = manifest_path.read_text()
    assert "# Experiment Manifest" in manifest
    assert f"- **input_path**: {csv_path}" in manifest
    assert "- **symbol**: AAA" in manifest
    assert "- **mode**: backtest" in manifest
    assert "## strategy_config" in manifest
    assert "- **short_window**: 2" in manifest
    assert "- **long_window**: 3" in manifest
    assert "- **fee_bps**: 1.5000" in manifest
    assert "## output_paths" in manifest
    assert f"- **manifest**: {manifest_path}" in manifest
    assert f"- **markdown_report**: {report_path}" in manifest
    assert "- **research_only**: true" in manifest


def test_cli_creates_parent_directories_for_output_artifacts(tmp_path: Path) -> None:
    output_path = tmp_path / "new" / "reports" / "backtest-report.md"
    json_path = tmp_path / "new" / "json" / "backtest-report.json"
    html_path = tmp_path / "new" / "html" / "backtest-report.html"
    manifest_path = tmp_path / "new" / "manifest" / "manifest.md"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--short-window",
            "2",
            "--long-window",
            "3",
            "--output",
            str(output_path),
            "--json-output",
            str(json_path),
            "--html-output",
            str(html_path),
            "--manifest-output",
            str(manifest_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert "Market Signal Experiment Report" in output_path.read_text()
    assert json.loads(json_path.read_text())["strategy_config"]["symbol"] == "QQQ_LIKE"
    assert "<h1>Market Signal Experiment Report</h1>" in html_path.read_text()
    assert "# Experiment Manifest" in manifest_path.read_text()


def test_cli_outputs_static_fixture_provenance_for_bundled_sample(tmp_path: Path) -> None:
    output_path = tmp_path / "sample-report.md"
    json_path = tmp_path / "sample-report.json"
    manifest_path = tmp_path / "sample-manifest.md"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--short-window",
            "2",
            "--long-window",
            "3",
            "--output",
            str(output_path),
            "--json-output",
            str(json_path),
            "--manifest-output",
            str(manifest_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    markdown = output_path.read_text()
    payload = json.loads(json_path.read_text())
    manifest = manifest_path.read_text()

    assert "## Data Provenance" in markdown
    assert "sample_tqqq_qld_like" in markdown
    assert payload["data_provenance"]["data_kind"] == "synthetic_static_fixture"
    assert payload["data_provenance"]["research_only"] is True
    assert "## data_provenance" in manifest
    assert "synthetic_static_fixture" in manifest


def test_cli_sweep_prints_markdown_report_to_stdout() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--sweep",
            "--short-windows",
            "2,3",
            "--long-windows",
            "4,5",
            "--top-n",
            "2",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "# Moving Average Sweep Report" in result.stdout
    assert "Research-only" in result.stdout
    assert "| rank | short_window | long_window | total_return |" in result.stdout
    assert result.stdout.count("\n| 1 |") == 1
    assert result.stdout.count("\n| 2 |") == 1


def test_cli_sweep_writes_markdown_report_to_output_file(tmp_path: Path) -> None:
    output_path = tmp_path / "sweep-report.md"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--symbol",
            "TQQQ_LIKE",
            "--sweep",
            "--short-windows",
            "2,3",
            "--long-windows",
            "4,5",
            "--top-n",
            "1",
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    report = output_path.read_text()
    assert "# Moving Average Sweep Report" in report
    assert "| rank | short_window | long_window | total_return |" in report
    assert report.count("\n| 1 |") == 1
    assert "\n| 2 |" not in report


def test_cli_writes_sweep_json_report(tmp_path: Path) -> None:
    json_path = tmp_path / "sweep-report.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--sweep",
            "--short-windows",
            "2,3",
            "--long-windows",
            "4,5",
            "--top-n",
            "2",
            "--json-output",
            str(json_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "# Moving Average Sweep Report" in result.stdout
    payload = json.loads(json_path.read_text())
    assert payload["sweep_config"] == {
        "short_windows": [2, 3],
        "long_windows": [4, 5],
        "fee_bps": 0.0,
        "top_n": 2,
        "symbol": "QQQ_LIKE",
    }
    assert [result["rank"] for result in payload["ranked_results"]] == [1, 2]
    assert {
        "windows",
        "metrics",
    }.issubset(payload["ranked_results"][0])
    assert "train_metrics" not in payload["ranked_results"][0]
    assert "test_metrics" not in payload["ranked_results"][0]
    assert set(payload["ranked_results"][0]["windows"]) == {
        "short_window",
        "long_window",
    }
    assert set(payload["ranked_results"][0]["metrics"]) == {
        "total_return",
        "annualized_return",
        "max_drawdown",
        "volatility",
        "sharpe_like",
        "win_rate",
    }


def test_cli_writes_sweep_html_report(tmp_path: Path) -> None:
    html_path = tmp_path / "sweep-report.html"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--sweep",
            "--short-windows",
            "2,3",
            "--long-windows",
            "4,5",
            "--top-n",
            "1",
            "--html-output",
            str(html_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "# Moving Average Sweep Report" in result.stdout
    html = html_path.read_text()
    assert "<h1>Moving Average Sweep Report</h1>" in html
    assert "<th>rank</th>" in html
    assert "<th>total_return</th>" in html
    assert "Research-only" in html


def test_cli_sweep_outputs_validation_split_metadata(tmp_path: Path) -> None:
    output_path = tmp_path / "sweep-report.md"
    json_path = tmp_path / "sweep-report.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--sweep",
            "--short-windows",
            "2,3",
            "--long-windows",
            "4",
            "--top-n",
            "2",
            "--split-cutoff",
            "2024-01-08",
            "--output",
            str(output_path),
            "--json-output",
            str(json_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    report = output_path.read_text()
    assert "## Validation split" in report
    assert "not trading guidance" in report
    assert "train_total_return" in report
    assert "test_total_return" in report
    assert "train_rank" in report
    assert "test_rank" in report
    assert "robustness_flag" in report
    assert "parameter overfitting" in report
    assert "not a prediction" in report
    assert "stability claim" in report
    payload = json.loads(json_path.read_text())
    assert payload["validation_split"] == {
        "train": {
            "first_date": "2024-01-02",
            "last_date": "2024-01-05",
            "row_count": 4,
        },
        "test": {
            "first_date": "2024-01-08",
            "last_date": "2024-01-11",
            "row_count": 4,
        },
        "research_only": True,
        "note": "Validation split metadata is a research note, not trading guidance.",
        "method": "cutoff",
        "split_cutoff": "2024-01-08",
    }
    first_result = payload["ranked_results"][0]
    assert "train_metrics" in first_result
    assert "test_metrics" in first_result
    assert "robustness" in first_result
    assert set(first_result["train_metrics"]) == set(first_result["metrics"])
    assert set(first_result["test_metrics"]) == set(first_result["metrics"])
    assert set(first_result["robustness"]) == {
        "train_rank",
        "test_rank",
        "rank_delta",
        "train_test_return_gap",
        "robustness_flag",
    }
    assert not {
        "train_rank",
        "test_rank",
        "rank_delta",
        "train_test_return_gap",
        "robustness_flag",
    } & set(first_result)
    assert first_result["robustness"]["robustness_flag"] in {
        "fragile",
        "not_flagged",
    }
    markdown_rows = _split_sweep_markdown_rows(report)
    assert len(markdown_rows) == len(payload["ranked_results"])
    for markdown_row, json_row in zip(markdown_rows, payload["ranked_results"]):
        robustness = json_row["robustness"]
        assert markdown_row["rank"] == str(json_row["rank"])
        assert markdown_row["short_window"] == str(json_row["windows"]["short_window"])
        assert markdown_row["long_window"] == str(json_row["windows"]["long_window"])
        assert markdown_row["train_rank"] == str(robustness["train_rank"])
        assert markdown_row["test_rank"] == str(robustness["test_rank"])
        assert markdown_row["rank_delta"] == str(robustness["rank_delta"])
        assert markdown_row["train_total_return"] == _format_percent(
            json_row["train_metrics"]["total_return"]
        )
        assert markdown_row["test_total_return"] == _format_percent(
            json_row["test_metrics"]["total_return"]
        )
        assert markdown_row["train_test_return_gap"] == _format_percent(
            robustness["train_test_return_gap"]
        )
        assert markdown_row["robustness_flag"] == robustness["robustness_flag"]


def test_cli_rejects_split_sweep_windows_larger_than_partitions() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--sweep",
            "--short-windows",
            "2,3",
            "--long-windows",
            "4,5",
            "--split-cutoff",
            "2024-01-08",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "at least 5 rows to evaluate the largest long window" in result.stderr


def test_cli_rejects_mutually_exclusive_validation_split_flags() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--split-ratio",
            "0.5",
            "--split-cutoff",
            "2024-01-08",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "not allowed with argument" in result.stderr


def test_cli_rejects_invalid_sweep_window_flag() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--sweep",
            "--short-windows",
            "2,,3",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "list values must be comma-separated integers" in result.stderr


def test_cli_rejects_invalid_top_n_flag() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--sweep",
            "--top-n",
            "0",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "top_n must be at least 1 when set" in result.stderr


def test_cli_rejects_invalid_split_ratio_flag() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--split-ratio",
            "1.0",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "split ratio must be greater than 0 and less than 1" in result.stderr


def _split_sweep_markdown_rows(report: str) -> list[dict[str, str]]:
    header = (
        "| rank | short_window | long_window | total_return | train_rank | "
        "test_rank | rank_delta | train_total_return | test_total_return | "
        "train_test_return_gap | robustness_flag | annualized_return | "
        "max_drawdown | volatility | sharpe_like | win_rate |"
    )
    columns = [value.strip() for value in header.strip("|").split("|")]
    rows: list[dict[str, str]] = []
    in_split_table = False
    for line in report.splitlines():
        if line == header:
            in_split_table = True
            continue
        if not in_split_table:
            continue
        if line.startswith("| ---"):
            continue
        if not line.startswith("| "):
            break
        values = [value.strip() for value in line.strip("|").split("|")]
        rows.append(dict(zip(columns, values)))

    return rows


def _format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"
