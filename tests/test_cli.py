from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from market_signal_lab.report import (
    EXPOSURE_TRADE_REVIEW_NOTE,
    SCENARIO_RISK_COMPARISON_KEYS,
    SCENARIO_RISK_DRAWDOWN_KEYS,
    SCENARIO_RISK_EXPOSURE_KEYS,
    SCENARIO_RISK_FEE_DRAG_KEYS,
    SCENARIO_RISK_INTERPRETATION_KEYS,
    SCENARIO_RISK_INTERPRETATION_NOTE,
)


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
    assert result.stdout.strip() == "market-signal-lab 1.17.0"
    assert result.stderr == ""


def test_cli_prints_static_methodology_audit_template_without_csv_path() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--methodology-audit-template",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "# Methodology Audit Template" in result.stdout
    assert "Look-ahead bias" in result.stdout
    assert "Survivorship bias" in result.stdout
    assert "Overfitting" in result.stdout
    assert "Fees and slippage" in result.stdout
    assert "Daily reset leveraged ETF risk" in result.stdout
    assert "Live trading and advice boundary" in result.stdout
    assert "not investment advice" in result.stdout
    assert "not a live-trading, broker, account, order, or position-sizing workflow" in (
        result.stdout
    )
    assert result.stderr == ""


def test_cli_writes_static_methodology_audit_template_json(tmp_path: Path) -> None:
    markdown_path = tmp_path / "methodology-audit-template.md"
    json_path = tmp_path / "methodology-audit-template.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--methodology-audit-template",
            "--output",
            str(markdown_path),
            "--json-output",
            str(json_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Methodology Audit Template" in markdown
    assert payload["template_type"] == "methodology_audit_template"
    assert payload["schema_version"] == "1.0"
    assert payload["research_only"] is True
    assert payload["static_only"] is True
    assert payload["no_live_data"] is True
    assert payload["no_broker_or_account"] is True
    assert payload["no_orders_or_position_sizing"] is True
    assert payload["no_recommendations_or_forecasts"] is True
    assert payload["review_status_values"] == ["PASS", "WARN", "FAIL"]
    assert [row["check"] for row in payload["checks"]] == [
        "Look-ahead bias",
        "Survivorship bias",
        "Overfitting",
        "Fees and slippage",
        "Daily reset leveraged ETF risk",
        "Live trading and advice boundary",
    ]


def test_cli_rejects_csv_for_static_methodology_audit_template() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--methodology-audit-template",
            str(SAMPLE_DATA),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "--methodology-audit-template does not take csv_path" in result.stderr


def test_cli_scores_methodology_audit_review_json(tmp_path: Path) -> None:
    markdown_path = tmp_path / "methodology-audit-score.md"
    json_path = tmp_path / "methodology-audit-score.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--score-methodology-audit",
            "examples/configs/methodology-audit-review.json",
            "--output",
            str(markdown_path),
            "--json-output",
            str(json_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Methodology Audit Score" in markdown
    assert "- **PASS**: 5" in markdown
    assert "- **WARN**: 1" in markdown
    assert "- **FAIL**: 0" in markdown
    assert "promote_with_warnings" in markdown
    assert payload["summary_type"] == "methodology_audit_score"
    assert payload["counts"] == {"pass": 5, "warn": 1, "fail": 0}
    assert payload["promotion_gate_suggestion"] == "promote_with_warnings"
    assert payload["no_live_data"] is True
    assert payload["no_broker_or_account"] is True
    assert payload["no_orders_or_position_sizing"] is True
    assert payload["no_recommendations_or_forecasts"] is True


def test_cli_writes_methodology_audit_score_html_with_boundary_and_links(
    tmp_path: Path,
) -> None:
    markdown_path = tmp_path / "methodology-audit-score.md"
    json_path = tmp_path / "methodology-audit-score.json"
    html_path = tmp_path / "methodology-audit-score.html"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--score-methodology-audit",
            "examples/configs/methodology-audit-review.json",
            "--output",
            str(markdown_path),
            "--json-output",
            str(json_path),
            "--html-output",
            str(html_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    html = html_path.read_text(encoding="utf-8")
    assert "<title>Methodology Audit Score - Market Signal Lab</title>" in html
    assert "<h1>Methodology Audit Score - Market Signal Lab</h1>" in html
    assert "Related Artifacts" in html
    assert 'href="methodology-audit-score.md"' in html
    assert 'href="methodology-audit-score.json"' in html
    assert "This scorer only summarizes a local reviewer-filled JSON file." in html
    assert "does not read market data, fetch live data, connect to brokers" in html
    assert "inspect accounts, route orders, size positions, forecast" in html
    assert "recommend, certify strategy quality, or provide investment advice" in html
    assert "<script" not in html.lower()
    assert "http://" not in html
    assert "https://" not in html


def test_cli_rejects_invalid_methodology_audit_status(tmp_path: Path) -> None:
    review_path = tmp_path / "bad-methodology-audit-review.json"
    review_payload = json.loads(
        Path("examples/configs/methodology-audit-review.json").read_text(
            encoding="utf-8"
        )
    )
    review_payload["checks"][0]["status"] = "MAYBE"
    review_path.write_text(json.dumps(review_payload), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--score-methodology-audit",
            str(review_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert (
        "Look-ahead bias: invalid status 'MAYBE'; "
        "expected one of PASS, WARN, FAIL"
    ) in result.stderr


def test_cli_rejects_invalid_methodology_audit_check_name(tmp_path: Path) -> None:
    review_path = tmp_path / "bad-methodology-audit-review.json"
    review_payload = json.loads(
        Path("examples/configs/methodology-audit-review.json").read_text(
            encoding="utf-8"
        )
    )
    review_payload["checks"][1]["check"] = "Survival bias"
    review_path.write_text(json.dumps(review_payload), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--score-methodology-audit",
            str(review_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert (
        "checks[2].check must be 'Survivorship bias', got 'Survival bias'"
    ) in result.stderr


def test_cli_scores_fail_methodology_audit_status(tmp_path: Path) -> None:
    review_path = tmp_path / "fail-methodology-audit-review.json"
    json_path = tmp_path / "fail-methodology-audit-score.json"
    review_payload = json.loads(
        Path("examples/configs/methodology-audit-review.json").read_text(
            encoding="utf-8"
        )
    )
    review_payload["checks"][0]["status"] = "FAIL"
    review_path.write_text(json.dumps(review_payload), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--score-methodology-audit",
            str(review_path),
            "--json-output",
            str(json_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["counts"] == {"pass": 4, "warn": 1, "fail": 1}
    assert payload["promotion_gate_suggestion"] == "do_not_promote"
    assert "do_not_promote" in result.stdout


def test_cli_rejects_csv_for_methodology_audit_score() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--score-methodology-audit",
            "examples/configs/methodology-audit-review.json",
            str(SAMPLE_DATA),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "--score-methodology-audit does not take csv_path" in result.stderr


def test_cli_validates_default_cross_asset_thesis_ledger(tmp_path: Path) -> None:
    repo_root = Path.cwd()
    env = {**os.environ, "PYTHONPATH": str(repo_root)}
    ledger_dir = tmp_path / "reports"
    ledger_dir.mkdir()
    (ledger_dir / "cross-asset-thesis-ledger.json").write_text(
        (repo_root / "reports/cross-asset-thesis-ledger.json").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--validate-thesis-ledger",
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    markdown_path = ledger_dir / "cross-asset-thesis-ledger-acceptance.md"
    json_path = ledger_dir / "cross-asset-thesis-ledger-acceptance.json"
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Thesis-Ledger Acceptance Summary" in markdown
    assert "- **Accepted**: True" in markdown
    assert "not investment advice" in markdown
    assert payload["accepted"] is True
    assert payload["error_count"] == 0
    assert payload["asset_symbols"] == ["QQQ_LIKE", "QLD_LIKE", "TQQQ_LIKE"]


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
    interpretation = payload["scenario_risk_interpretation"]
    assert interpretation["research_only"] is True
    assert interpretation["historical_diagnostics_only"] is True
    assert interpretation["note"] == SCENARIO_RISK_INTERPRETATION_NOTE
    assert interpretation["exposure"]["period_count"] == 3
    assert interpretation["exposure"]["average_exposure"] == 1 / 3
    assert interpretation["exposure"]["percent_periods_in_market"] == 1 / 3
    assert "Higher exposure" in interpretation["exposure"]["summary"]
    assert interpretation["drawdown"]["max_drawdown"] == 0.0
    assert "peak-to-trough decline" in interpretation["drawdown"]["summary"]
    assert interpretation["fee_drag"]["total_fee_drag"] == 0.0
    assert "historical cost assumption" in interpretation["fee_drag"]["summary"]
    comparison = interpretation["buy_and_hold_comparison"]
    assert abs(comparison["strategy_total_return"] - (1 / 102)) < 1e-12
    assert abs(comparison["buy_and_hold_total_return"] - 0.03) < 1e-12
    assert (
        abs(comparison["strategy_minus_buy_and_hold_return"] + 0.02019607843137261)
        < 1e-12
    )
    assert "same period" in comparison["summary"]
    assert payload["first_date"] == "2024-01-01"
    assert payload["last_date"] == "2024-01-04"
    assert payload["row_count"] == 4


def test_cli_writes_pretrade_research_packet(tmp_path: Path) -> None:
    markdown_path = tmp_path / "pretrade-packet.md"
    json_path = tmp_path / "pretrade-packet.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--short-window",
            "20",
            "--long-window",
            "50",
            "--fee-bps",
            "10.0",
            "--pretrade-packet",
            "--output",
            str(markdown_path),
            "--json-output",
            str(json_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Pre-Trade Research Packet" in markdown
    assert "## Assumptions" in markdown
    assert "## Historical Diagnostics" in markdown
    assert "## Beginner Checklist" in markdown
    assert "## Risk Boundaries" in markdown
    assert "not investment advice" in markdown
    assert "finished above buy-and-hold in this historical sample" in markdown
    assert "beat buy-and-hold" not in markdown
    assert "not evidence of future returns" in markdown
    assert "Leveraged ETF-like boundary" in markdown
    assert payload["packet_type"] == "pretrade_research_packet"
    assert payload["research_only"] is True
    assert payload["no_broker_or_live_data"] is True
    assert payload["source"]["input_path"] == str(SAMPLE_DATA)
    assert payload["strategy_config"]["symbol"] == "QQQ_LIKE"
    assert "metrics" in payload["historical_diagnostics"]
    assert "exposure_trade_review" in payload["historical_diagnostics"]
    assert payload["beginner_checklist"][0]["status"] == "review_required"
    assert "future returns" in payload["risk_boundaries"]["sample_backtest_limits"]
    assert "broker workflow" in payload["risk_boundaries"]["scope_limits"]


def test_cli_pretrade_packet_requires_json_output_path() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(SAMPLE_DATA),
            "--pretrade-packet",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "--pretrade-packet requires --json-output PATH" in result.stderr


def test_cli_writes_scenario_card_defaults_with_expected_shape(tmp_path: Path) -> None:
    repo_root = Path.cwd()
    env = {**os.environ, "PYTHONPATH": str(repo_root)}

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(repo_root / SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--short-window",
            "20",
            "--long-window",
            "50",
            "--fee-bps",
            "10.0",
            "--scenario-card",
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    markdown_path = tmp_path / "reports/scenario-card.md"
    json_path = tmp_path / "reports/scenario-card.json"
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    for heading in (
        "# Scenario Card",
        "## Source",
        "## Assumptions",
        "## Key Metrics",
        "## Diagnostics",
        "## Scenario/Risk Interpretation",
        "## Risk Labels",
        "## Next Review Checklist",
    ):
        assert heading in markdown
    assert "not investment advice" in markdown
    assert "Leveraged ETF-like risk" in markdown
    assert markdown.count("- [ ] ") == 5

    assert payload["card_type"] == "scenario_card"
    assert payload["schema_version"] == "1.0"
    assert payload["research_only"] is True
    assert payload["historical_diagnostics_only"] is True
    assert payload["no_broker_or_live_data"] is True
    assert payload["strategy_config"]["symbol"] == "QQQ_LIKE"
    assert set(payload["key_metrics"]) == {
        "total_return",
        "buy_and_hold_total_return",
        "strategy_minus_buy_and_hold_return",
        "max_drawdown",
        "volatility",
        "sharpe_like",
        "win_rate",
    }
    assert set(payload["diagnostics"]) == {
        "exposure",
        "fees",
        "drawdown",
        "scenario_risk_interpretation",
    }
    assert "leveraged_etf_like" in payload["risk_labels"]
    assert payload["next_review_checklist"][0]["status"] == "review_required"


def test_cli_scenario_card_with_json_output_prints_markdown_to_stdout(
    tmp_path: Path,
) -> None:
    repo_root = Path.cwd()
    env = {**os.environ, "PYTHONPATH": str(repo_root)}
    json_path = tmp_path / "scenario-card.json"
    default_markdown_path = tmp_path / "reports/scenario-card.md"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(repo_root / SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--scenario-card",
            "--json-output",
            str(json_path),
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "# Scenario Card" in result.stdout
    assert not default_markdown_path.exists()
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["card_type"] == "scenario_card"


def test_cli_scenario_card_with_output_does_not_default_json(
    tmp_path: Path,
) -> None:
    repo_root = Path.cwd()
    env = {**os.environ, "PYTHONPATH": str(repo_root)}
    output_path = tmp_path / "scenario-card.md"
    default_json_path = tmp_path / "reports/scenario-card.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(repo_root / SAMPLE_DATA),
            "--symbol",
            "QQQ_LIKE",
            "--scenario-card",
            "--output",
            str(output_path),
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert "# Scenario Card" in output_path.read_text(encoding="utf-8")
    assert not default_json_path.exists()


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


def test_checked_single_backtest_config_outputs_scenario_risk_fields(
    tmp_path: Path,
) -> None:
    markdown_path = tmp_path / "sample-report.md"
    json_path = tmp_path / "sample-report.json"
    html_path = tmp_path / "sample-report.html"
    manifest_path = tmp_path / "sample-manifest.md"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--config",
            "examples/configs/single-backtest-report.json",
            "--output",
            str(markdown_path),
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

    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    html = html_path.read_text(encoding="utf-8")
    manifest = manifest_path.read_text(encoding="utf-8")

    assert "## Scenario/Risk Interpretation" in markdown
    assert "Historical diagnostics only" in markdown
    assert "<h2>Scenario/Risk Interpretation</h2>" in html
    assert "examples/data/sample_tqqq_qld_like.csv" in manifest
    assert "synthetic_static_fixture" in manifest

    assert payload["strategy_config"] == {
        "short_window": 20,
        "long_window": 50,
        "symbol": "QQQ_LIKE",
        "fee_bps": 10.0,
    }
    assert payload["data_provenance"]["data_kind"] == "synthetic_static_fixture"
    interpretation = payload["scenario_risk_interpretation"]
    assert interpretation["research_only"] is True
    assert interpretation["historical_diagnostics_only"] is True
    assert set(interpretation) == SCENARIO_RISK_INTERPRETATION_KEYS
    assert set(interpretation["exposure"]) == SCENARIO_RISK_EXPOSURE_KEYS
    assert set(interpretation["drawdown"]) == SCENARIO_RISK_DRAWDOWN_KEYS
    assert set(interpretation["fee_drag"]) == SCENARIO_RISK_FEE_DRAG_KEYS
    assert (
        set(interpretation["buy_and_hold_comparison"])
        == SCENARIO_RISK_COMPARISON_KEYS
    )
    assert interpretation["note"] == SCENARIO_RISK_INTERPRETATION_NOTE
    assert "Historical diagnostics only" in interpretation["note"]
    assert "not investment advice" in interpretation["note"]


def test_checked_multi_regime_config_outputs_regime_provenance(
    tmp_path: Path,
) -> None:
    markdown_path = tmp_path / "multi-regime-bull-report.md"
    json_path = tmp_path / "multi-regime-bull-report.json"
    html_path = tmp_path / "multi-regime-bull-report.html"
    manifest_path = tmp_path / "multi-regime-bull-manifest.md"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--config",
            "examples/configs/multi-regime-bull-report.json",
            "--output",
            str(markdown_path),
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

    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    manifest = manifest_path.read_text(encoding="utf-8")

    assert "BULL_REGIME (bull, 12 rows)" in markdown
    assert "CHOPPY_REGIME (choppy, 12 rows)" in markdown
    assert "DRAWDOWN_RECOVERY_REGIME (drawdown_recovery, 12 rows)" in markdown
    assert payload["strategy_config"]["symbol"] == "BULL_REGIME"
    assert payload["row_count"] == 12
    assert payload["data_provenance"]["dataset_label"] == "sample_multi_regime"
    assert payload["data_provenance"]["regimes"] == [
        {
            "symbol": "BULL_REGIME",
            "regime": "bull",
            "description": (
                "Monotonic upward path used to exercise trend-following examples."
            ),
            "assumptions": [
                "Close prices increase every sample period by construction.",
                "Open prices equal the prior close after the first row.",
                "High and low prices are synthetic padding around open and close.",
            ],
            "synthetic_only": True,
            "not_predictive": True,
            "not_live_trading": True,
            "row_count": 12,
        },
        {
            "symbol": "CHOPPY_REGIME",
            "regime": "choppy",
            "description": "Alternating path that ends near flat after repeated reversals.",
            "assumptions": [
                "Close prices alternate around the starting level by construction.",
                "Open prices equal the prior close after the first row.",
                "High and low prices are synthetic padding around open and close.",
            ],
            "synthetic_only": True,
            "not_predictive": True,
            "not_live_trading": True,
            "row_count": 12,
        },
        {
            "symbol": "DRAWDOWN_RECOVERY_REGIME",
            "regime": "drawdown_recovery",
            "description": "Decline followed by recovery for drawdown diagnostics.",
            "assumptions": [
                "Close prices fall first and then recover by construction.",
                "Open prices equal the prior close after the first row.",
                "High and low prices are synthetic padding around open and close.",
            ],
            "synthetic_only": True,
            "not_predictive": True,
            "not_live_trading": True,
            "row_count": 12,
        },
    ]
    assert "examples/data/sample_multi_regime.csv" in manifest
    assert "sample_multi_regime" in manifest


def test_cli_regime_comparison_writes_markdown_json_and_html(
    tmp_path: Path,
) -> None:
    markdown_path = tmp_path / "regime-comparison.md"
    json_path = tmp_path / "regime-comparison.json"
    html_path = tmp_path / "regime-comparison.html"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--regime-comparison",
            "--output",
            str(markdown_path),
            "--json-output",
            str(json_path),
            "--html-output",
            str(html_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == ""

    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    html = html_path.read_text(encoding="utf-8")

    assert "# Regime Comparison Report" in markdown
    assert "BULL_REGIME" in markdown
    assert "CHOPPY_REGIME" in markdown
    assert "DRAWDOWN_RECOVERY_REGIME" in markdown
    assert "Buy-and-hold comparison" in markdown
    assert "Exposure/cash-time" in markdown
    assert "Whipsaw" in markdown
    assert "not investment advice" in markdown
    assert "not a recommendation" in markdown
    assert "not a prediction" in markdown

    assert list(payload) == [
        "comparison_config",
        "assumptions",
        "summary",
        "caveats",
        "regimes",
    ]
    assert list(payload["comparison_config"]) == [
        "source_configs",
        "research_only",
        "note",
    ]
    assert list(payload["summary"]) == [
        "best_strategy_total_return_symbol",
        "best_buy_and_hold_total_return_symbol",
        "largest_drawdown_symbol",
        "highest_whipsaw_symbol",
        "most_cash_time_symbol",
        "research_only",
    ]
    assert payload["assumptions"] == [
        (
            "Bundled regime labels are deterministic synthetic-only fixture "
            "scenarios, not market classifications, forecasts, or live-trading "
            "signals."
        ),
        (
            "Each row uses the configured moving-average settings and same-period "
            "close-to-close buy-and-hold comparison."
        ),
        "Provenance is loaded from adjacent static fixture metadata when available.",
    ]
    assert payload["caveats"] == [
        "This artifact uses synthetic static fixture data for research workflows only.",
        (
            "Results are hypothetical, historical, and sensitive to data, fees, "
            "and chosen parameters."
        ),
        (
            "Nothing in this JSON is investment advice, trading guidance, "
            "a recommendation, a prediction, or a live-trading signal."
        ),
    ]
    assert payload["comparison_config"]["research_only"] is True
    assert payload["comparison_config"]["source_configs"] == [
        "examples/configs/multi-regime-bull-report.json",
        "examples/configs/multi-regime-choppy-report.json",
        "examples/configs/multi-regime-drawdown-recovery-report.json",
    ]
    assert [row["regime_label"] for row in payload["regimes"]] == [
        "bull",
        "choppy",
        "drawdown recovery",
    ]
    assert [row["symbol"] for row in payload["regimes"]] == [
        "BULL_REGIME",
        "CHOPPY_REGIME",
        "DRAWDOWN_RECOVERY_REGIME",
    ]
    first_regime = payload["regimes"][0]
    assert list(first_regime) == [
        "source_config",
        "csv_path",
        "symbol",
        "regime_label",
        "generation_assumptions",
        "strategy_config",
        "metrics",
        "exposure_trade_review",
        "scenario_risk_interpretation",
        "first_date",
        "last_date",
        "row_count",
        "data_provenance",
        "interpretation",
        "research_only",
        "synthetic_only",
        "not_predictive",
        "not_live_trading",
    ]
    assert first_regime["research_only"] is True
    assert first_regime["synthetic_only"] is True
    assert first_regime["not_predictive"] is True
    assert first_regime["not_live_trading"] is True
    assert first_regime["generation_assumptions"] == {
        "source": "Monotonic upward path used to exercise trend-following examples.",
        "assumptions": [
            "Close prices increase every sample period by construction.",
            "Open prices equal the prior close after the first row.",
            "High and low prices are synthetic padding around open and close.",
        ],
        "synthetic_only": True,
        "not_predictive": True,
        "not_live_trading": True,
    }
    assert set(first_regime["metrics"]) == {
        "total_return",
        "buy_and_hold_total_return",
        "strategy_minus_buy_and_hold_return",
        "annualized_return",
        "max_drawdown",
        "volatility",
        "sharpe_like",
        "win_rate",
    }
    assert first_regime["metrics"]["buy_and_hold_total_return"] > 0
    assert first_regime["data_provenance"]["dataset_label"] == "sample_multi_regime"
    assert first_regime["data_provenance"]["research_only"] is True
    assert first_regime["data_provenance"]["regimes"][0]["regime"] == "bull"
    assert "percent_periods_in_cash" in first_regime["exposure_trade_review"]
    assert "whipsaw_rate" in first_regime["interpretation"]
    assert "drawdown_summary" in first_regime["interpretation"]
    assert payload["summary"]["research_only"] is True

    assert "<title>Regime Comparison - Market Signal Lab</title>" in html
    assert "<h1>Regime Comparison - Market Signal Lab</h1>" in html
    assert '<nav aria-label="Related artifacts">' in html
    assert '<a href="regime-comparison.md">Markdown report</a>' in html
    assert '<a href="regime-comparison.json">JSON data</a>' in html
    assert "<h1>Regime Comparison Report</h1>" in html
    assert "<th>strategy_return</th>" in html
    assert "<h2>Caveats</h2>" in html
    assert "Research-only" in html
    assert "<script" not in html.lower()
    assert "http://" not in html
    assert "https://" not in html


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
