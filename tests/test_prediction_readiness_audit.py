from __future__ import annotations

from copy import deepcopy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from market_signal_lab.prediction_readiness_audit import (
    PREDICTION_READINESS_AUDIT_TOP_LEVEL_KEYS,
    PREDICTION_READINESS_CRITERION_KEYS,
    build_prediction_readiness_audit,
    render_prediction_readiness_audit,
)
from market_signal_lab.thesis_ledger import build_cross_asset_thesis_ledger


SAMPLE_DATA = Path("examples/data/sample_tqqq_qld_like.csv")


def test_prediction_readiness_audit_labels_expected_criteria() -> None:
    ledger = build_cross_asset_thesis_ledger(SAMPLE_DATA)

    payload = build_prediction_readiness_audit(
        ledger,
        "reports/cross-asset-thesis-ledger.json",
    )
    markdown = render_prediction_readiness_audit(payload)

    assert tuple(payload) == PREDICTION_READINESS_AUDIT_TOP_LEVEL_KEYS
    assert payload["audit_type"] == "prediction_readiness_audit"
    assert payload["schema_version"] == "1.0"
    assert payload["research_only"] is True
    assert payload["historical_diagnostics_only"] is True
    assert payload["not_investment_advice"] is True
    assert payload["asset_symbols"] == ["QQQ_LIKE", "QLD_LIKE", "TQQQ_LIKE"]
    assert tuple(payload["criteria"][0]) == PREDICTION_READINESS_CRITERION_KEYS

    labels = {item["criterion"]: item["label"] for item in payload["criteria"]}
    assert labels == {
        "static_data": "PASS",
        "non_advice_boundary": "PASS",
        "benchmark_presence": "PASS",
        "fee_drawdown_exposure_presence": "PASS",
        "train_test_diagnostics": "WARN",
        "leveraged_etf_caveats": "PASS",
    }
    assert payload["summary"] == {
        "overall_label": "WARN",
        "pass_count": 5,
        "warn_count": 1,
        "fail_count": 0,
        "review_boundary": (
            "This audit checks whether required labels and supporting "
            "fields are visible in a static historical artifact for "
            "public review. It is not a prediction, forecast, "
            "recommendation, trading instruction, or investment-advice "
            "approval."
        ),
    }
    assert "# Prediction-Readiness Audit" in markdown
    assert "## How to Read This" in markdown
    assert (
        "Read PASS as a documentation item found, WARN as a review question, "
        "and FAIL as a missing or incomplete boundary."
    ) in markdown
    assert "| train_test_diagnostics | WARN |" in markdown
    assert "not investment advice" in markdown
    assert "## Leveraged ETF Risk Boundary" in markdown
    assert "Daily reset and compounding can make multi-day results path-dependent" in (
        markdown
    )
    assert "not as a market outlook, action cue, or position-sizing input" in markdown


def test_prediction_readiness_audit_fails_missing_non_advice_boundary() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    ledger["research_only"] = False
    ledger["note"] = "Historical sample artifact."
    ledger["risk_boundaries"]["non_advice"] = ""

    payload = build_prediction_readiness_audit(ledger, "ledger.json")

    labels = {item["criterion"]: item["label"] for item in payload["criteria"]}
    assert labels["non_advice_boundary"] == "FAIL"
    assert payload["summary"]["overall_label"] == "FAIL"


def test_prediction_readiness_audit_fails_missing_benchmark_fields() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    del ledger["assets"][0]["metrics"]["buy_and_hold_total_return"]

    payload = build_prediction_readiness_audit(ledger, "ledger.json")

    labels = {item["criterion"]: item["label"] for item in payload["criteria"]}
    benchmark = next(
        item
        for item in payload["criteria"]
        if item["criterion"] == "benchmark_presence"
    )
    assert labels["benchmark_presence"] == "FAIL"
    assert ledger["assets"][0]["symbol"] in benchmark["evidence"]
    assert payload["summary"]["overall_label"] == "FAIL"


def test_prediction_readiness_audit_fails_non_static_data_boundary() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    ledger["offline_only"] = False
    ledger["no_broker_or_live_data"] = False
    ledger["source"]["input_path"] = "live/provider.csv"
    ledger["data_provenance"] = {}

    payload = build_prediction_readiness_audit(ledger, "ledger.json")

    static_data = next(
        item for item in payload["criteria"] if item["criterion"] == "static_data"
    )
    assert static_data["label"] == "FAIL"
    assert static_data["status"] == "Static/offline data boundaries are incomplete."
    assert payload["summary"]["overall_label"] == "FAIL"


def test_prediction_readiness_audit_fails_missing_fee_drawdown_exposure_fields() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    del ledger["strategy_config"]["fee_bps"]
    del ledger["assets"][0]["metrics"]["max_drawdown"]
    del ledger["assets"][0]["exposure_trade_review"]["total_fee_drag"]

    payload = build_prediction_readiness_audit(ledger, "ledger.json")

    criterion = next(
        item
        for item in payload["criteria"]
        if item["criterion"] == "fee_drawdown_exposure_presence"
    )
    assert criterion["label"] == "FAIL"
    assert "strategy_config.fee_bps" in criterion["evidence"]
    assert "QQQ_LIKE.metrics.max_drawdown" in criterion["evidence"]
    assert "QQQ_LIKE.exposure_trade_review.total_fee_drag" in criterion["evidence"]
    assert payload["summary"]["overall_label"] == "FAIL"


def test_prediction_readiness_audit_uses_unknown_for_missing_symbols() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    del ledger["assets"][0]["symbol"]
    del ledger["assets"][0]["metrics"]["buy_and_hold_total_return"]

    payload = build_prediction_readiness_audit(ledger, "ledger.json")

    benchmark = next(
        item
        for item in payload["criteria"]
        if item["criterion"] == "benchmark_presence"
    )
    assert payload["asset_symbols"][0] == "unknown"
    assert "missing_symbols=unknown" in benchmark["evidence"]
    assert "None" not in benchmark["evidence"]


def test_prediction_readiness_audit_fails_missing_leveraged_caveats() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    ledger["risk_boundaries"]["leveraged_etf_like"] = "Review leveraged examples."

    payload = build_prediction_readiness_audit(ledger, "ledger.json")

    labels = {item["criterion"]: item["label"] for item in payload["criteria"]}
    assert labels["leveraged_etf_caveats"] == "FAIL"
    assert payload["summary"]["overall_label"] == "FAIL"


def test_prediction_readiness_audit_rejects_non_object_input() -> None:
    with pytest.raises(
        ValueError,
        match="Prediction-readiness audit input must be a JSON object",
    ):
        build_prediction_readiness_audit([], "ledger.json")


def test_cli_writes_prediction_readiness_audit_defaults(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--prediction-readiness-audit",
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    markdown_path = tmp_path / "reports" / "prediction-readiness-audit.md"
    json_path = tmp_path / "reports" / "prediction-readiness-audit.json"
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "# Prediction-Readiness Audit" in markdown
    assert payload["source_artifact"] == "reports/cross-asset-thesis-ledger.json"
    assert payload["summary"]["overall_label"] == "WARN"


def test_cli_prediction_readiness_audit_accepts_custom_input_and_outputs(
    tmp_path: Path,
) -> None:
    ledger_path = tmp_path / "ledger.json"
    markdown_path = tmp_path / "audit.md"
    json_path = tmp_path / "audit.json"
    ledger_path.write_text(
        json.dumps(build_cross_asset_thesis_ledger(SAMPLE_DATA)),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--prediction-readiness-audit",
            str(ledger_path),
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
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["source_artifact"] == str(ledger_path)
    assert "leveraged_etf_caveats" in markdown_path.read_text(encoding="utf-8")


def test_cli_prediction_readiness_audit_json_output_only_prints_markdown(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": str(repo_root)}
    json_path = tmp_path / "audit.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--prediction-readiness-audit",
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
    assert "# Prediction-Readiness Audit" in result.stdout
    assert result.stderr == ""
    assert json.loads(json_path.read_text(encoding="utf-8"))["audit_type"] == (
        "prediction_readiness_audit"
    )
    assert not (tmp_path / "reports" / "prediction-readiness-audit.md").exists()


def test_cli_prediction_readiness_audit_markdown_output_only_skips_default_json(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": str(repo_root)}
    markdown_path = tmp_path / "audit.md"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--prediction-readiness-audit",
            "--output",
            str(markdown_path),
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert "# Prediction-Readiness Audit" in markdown_path.read_text(
        encoding="utf-8"
    )
    assert not (tmp_path / "reports" / "prediction-readiness-audit.json").exists()


def test_cli_prediction_readiness_audit_help_describes_boundaries() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--help",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    help_text = " ".join(result.stdout.split())
    assert "--prediction-readiness-audit [PATH]" in help_text
    assert "Only --output and --json-output customize files" in help_text
    assert "Uses only a static JSON artifact" in help_text


def test_cli_prediction_readiness_audit_rejects_strategy_flags() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--prediction-readiness-audit",
            "--symbol",
            "QQQ_LIKE",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert (
        "--prediction-readiness-audit cannot be combined with --symbol"
        in result.stderr
    )


@pytest.mark.parametrize(
    ("extra_args", "message"),
    [
        (
            ["--config", "examples/configs/single-backtest-report.json"],
            "--prediction-readiness-audit does not take --config",
        ),
        (
            ["--html-output", "audit.html"],
            "--prediction-readiness-audit writes Markdown/JSON, not HTML",
        ),
        (
            ["--manifest-output", "manifest.md"],
            "--prediction-readiness-audit does not write experiment manifests",
        ),
        (
            ["--beginner-prediction-checklist"],
            (
                "--prediction-readiness-audit cannot be combined with "
                "--beginner-prediction-checklist"
            ),
        ),
    ],
)
def test_cli_prediction_readiness_audit_rejects_incompatible_options(
    extra_args: list[str],
    message: str,
) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--prediction-readiness-audit",
            *extra_args,
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert message in result.stderr


def test_cli_prediction_readiness_audit_rejects_two_input_paths() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--prediction-readiness-audit",
            "ledger-a.json",
            "ledger-b.json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert (
        "--prediction-readiness-audit accepts only one ledger JSON path"
        in result.stderr
    )


def test_cli_prediction_readiness_audit_rejects_invalid_json(tmp_path: Path) -> None:
    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text("{", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--prediction-readiness-audit",
            str(ledger_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert f"Invalid prediction-readiness audit JSON {ledger_path}" in result.stderr
