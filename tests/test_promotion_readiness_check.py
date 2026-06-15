from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from market_signal_lab.promotion_readiness_check import (
    PROMOTION_READINESS_CHECK_ITEM_KEYS,
    PROMOTION_READINESS_CHECK_TOP_LEVEL_KEYS,
    build_promotion_readiness_check,
    render_promotion_readiness_check,
)
from market_signal_lab.thesis_ledger import build_cross_asset_thesis_ledger


SAMPLE_DATA = Path("examples/data/sample_tqqq_qld_like.csv")


def _source_sha256(raw_json: str | bytes) -> str:
    if isinstance(raw_json, str):
        raw_json = raw_json.encode("utf-8")
    return hashlib.sha256(raw_json).hexdigest()


def test_promotion_readiness_check_labels_gates_and_next_fixes() -> None:
    ledger = build_cross_asset_thesis_ledger(SAMPLE_DATA)

    payload = build_promotion_readiness_check(
        ledger,
        "reports/cross-asset-thesis-ledger.json",
        _source_sha256(json.dumps(ledger, separators=(",", ":")) + "\n"),
    )
    markdown = render_promotion_readiness_check(payload)

    assert tuple(payload) == PROMOTION_READINESS_CHECK_TOP_LEVEL_KEYS
    assert payload["artifact_type"] == "promotion_readiness_check"
    assert payload["schema_version"] == "1.0"
    assert payload["research_only"] is True
    assert payload["static_only"] is True
    assert payload["no_live_data"] is True
    assert payload["not_investment_advice"] is True
    assert tuple(payload["checks"][0]) == PROMOTION_READINESS_CHECK_ITEM_KEYS
    assert payload["source_artifact_role"] == (
        "Repo-relative static thesis-ledger JSON path read by this check."
    )
    assert len(payload["source_content_sha256"]) == 64
    assert all(char in "0123456789abcdef" for char in payload["source_content_sha256"])
    assert payload["default_outputs_role"] == (
        "Repo-relative paths written by --promotion-readiness-check when "
        "output overrides are not supplied."
    )

    labels = {item["check"]: item["label"] for item in payload["checks"]}
    assert labels == {
        "no_live_data_boundary": "PASS",
        "no_advice_boundary": "PASS",
        "benchmark_evidence": "PASS",
        "fee_evidence": "PASS",
        "drawdown_evidence": "PASS",
        "train_test_evidence": "WARN",
        "leveraged_caveat_evidence": "PASS",
    }
    assert payload["summary"]["release_gate"] == "PASS"
    assert payload["summary"]["promotion_gate"] == "WARN"
    assert payload["summary"]["pass_count"] == 6
    assert payload["summary"]["warn_count"] == 1
    assert payload["summary"]["fail_count"] == 0
    assert payload["summary"]["count_scope"] == (
        "Counts cover the checks array and are ordered PASS/WARN/FAIL."
    )
    assert payload["summary"]["label_meanings"] == {
        "PASS": "Expected documentation evidence and boundary wording are visible.",
        "WARN": (
            "Public review/release can continue, but broader promotion or citation "
            "stays on hold until resolved or explicitly disclosed."
        ),
        "FAIL": "Hold release or broader promotion until the listed fix is addressed.",
    }
    assert payload["actionable_next_fixes"] == [
        (
            "Before broader promotion or citation, attach a split-sweep or "
            "train/test artifact that shows train metrics, test metrics, and "
            "any return-gap or robustness labels, or explicitly disclose that "
            "the evidence is not yet present."
        )
    ]
    assert "# Public-Promotion Readiness Check" in markdown
    assert "- **Default outputs**: reports/promotion-readiness-check.md" in markdown
    assert "- **Release Gate**: PASS" in markdown
    assert "- **Promotion Gate**: WARN" in markdown
    assert "- **PASS/WARN/FAIL counts (checks array)**: 6 / 1 / 0" in markdown
    assert "PASS = Expected documentation evidence" in markdown
    assert "| train_test_evidence | WARN |" in markdown
    assert "| train_test_evidence | WARN | Public review/release can continue" in markdown
    assert "Broader promotion/citation stays on hold until resolved or explicitly disclosed." in markdown
    assert markdown.count("- **Next fix**:") == 1
    assert markdown.count("- **Review note**: No fix is listed for this PASS check") == 6
    assert (
        "### no_live_data_boundary\n\n"
        "- **Label**: PASS\n"
        "- **Evidence**: input_path=examples/data/sample_tqqq_qld_like.csv; "
        "static_source=True; flags=offline_only=True, "
        "no_broker_or_live_data=True, historical_diagnostics_only=True\n"
        "- **Next fix**"
        not in markdown
    )
    assert "not trading readiness, a forecast, a recommendation" in markdown


def test_promotion_readiness_check_fails_release_and_promotion_on_boundaries() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    ledger["offline_only"] = False
    ledger["no_broker_or_live_data"] = False
    ledger["research_only"] = False
    ledger["note"] = "Historical artifact."
    ledger["risk_boundaries"]["non_advice"] = ""

    payload = build_promotion_readiness_check(
        ledger,
        "ledger.json",
        _source_sha256(json.dumps(ledger)),
    )

    labels = {item["check"]: item["label"] for item in payload["checks"]}
    assert labels["no_live_data_boundary"] == "FAIL"
    assert labels["no_advice_boundary"] == "FAIL"
    assert payload["summary"]["release_gate"] == "FAIL"
    assert payload["summary"]["promotion_gate"] == "FAIL"
    assert any("Keep promotion on hold" in fix for fix in payload["actionable_next_fixes"])


def test_promotion_readiness_check_fails_missing_evidence_fields() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    del ledger["strategy_config"]["fee_bps"]
    del ledger["assets"][0]["metrics"]["buy_and_hold_total_return"]
    del ledger["assets"][0]["metrics"]["max_drawdown"]
    del ledger["assets"][0]["exposure_trade_review"]["total_fee_drag"]

    payload = build_promotion_readiness_check(
        ledger,
        "ledger.json",
        _source_sha256(json.dumps(ledger)),
    )

    checks = {item["check"]: item for item in payload["checks"]}
    assert checks["benchmark_evidence"]["label"] == "FAIL"
    assert "QQQ_LIKE" in checks["benchmark_evidence"]["evidence"]
    assert checks["fee_evidence"]["label"] == "FAIL"
    assert "strategy_config.fee_bps" in checks["fee_evidence"]["evidence"]
    assert checks["drawdown_evidence"]["label"] == "FAIL"
    assert "QQQ_LIKE.metrics.max_drawdown" in checks["drawdown_evidence"]["evidence"]
    assert payload["summary"]["release_gate"] == "FAIL"


def test_promotion_readiness_check_fails_empty_assets_without_crashing() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    ledger["assets"] = []

    payload = build_promotion_readiness_check(
        ledger,
        "ledger.json",
        _source_sha256(json.dumps(ledger)),
    )

    checks = {item["check"]: item for item in payload["checks"]}
    assert payload["summary"]["asset_symbols"] == []
    assert checks["benchmark_evidence"]["label"] == "FAIL"
    assert checks["benchmark_evidence"]["evidence"] == (
        "asset_count=0; missing_symbols=none"
    )
    assert checks["fee_evidence"]["label"] == "FAIL"
    assert checks["drawdown_evidence"]["label"] == "FAIL"
    assert checks["leveraged_caveat_evidence"]["label"] == "FAIL"
    assert payload["summary"]["release_gate"] == "FAIL"
    assert payload["summary"]["promotion_gate"] == "FAIL"


def test_promotion_readiness_check_fails_missing_leveraged_caveat() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    ledger["risk_boundaries"]["leveraged_etf_like"] = "Review leveraged examples."

    payload = build_promotion_readiness_check(
        ledger,
        "ledger.json",
        _source_sha256(json.dumps(ledger)),
    )

    checks = {item["check"]: item for item in payload["checks"]}
    assert checks["leveraged_caveat_evidence"]["label"] == "FAIL"
    assert "leveraged_symbols=QLD_LIKE, TQQQ_LIKE" in (
        checks["leveraged_caveat_evidence"]["evidence"]
    )
    assert payload["summary"]["release_gate"] == "FAIL"
    assert payload["summary"]["promotion_gate"] == "FAIL"


def test_promotion_readiness_check_passes_train_test_when_present() -> None:
    ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    ledger["validation_split"] = {"split_ratio": 0.7}

    payload = build_promotion_readiness_check(
        ledger,
        "ledger.json",
        _source_sha256(json.dumps(ledger)),
    )

    labels = {item["check"]: item["label"] for item in payload["checks"]}
    assert labels["train_test_evidence"] == "PASS"
    assert payload["summary"]["release_gate"] == "PASS"
    assert payload["summary"]["promotion_gate"] == "PASS"
    assert payload["actionable_next_fixes"] == []
    markdown = render_promotion_readiness_check(payload)
    assert "- **Next fix**:" not in markdown
    assert "No fix is listed for this PASS check" in markdown


def test_promotion_readiness_check_rejects_non_object_input() -> None:
    with pytest.raises(
        ValueError,
        match="Promotion-readiness check input must be a JSON object",
    ):
        build_promotion_readiness_check([], "ledger.json", _source_sha256("[]"))


def test_cli_writes_promotion_readiness_check_defaults(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--promotion-readiness-check",
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
    markdown_path = tmp_path / "reports" / "promotion-readiness-check.md"
    json_path = tmp_path / "reports" / "promotion-readiness-check.json"
    markdown = markdown_path.read_text(encoding="utf-8")
    raw_json = json_path.read_text(encoding="utf-8")
    payload = json.loads(raw_json)
    assert "# Public-Promotion Readiness Check" in markdown
    assert list(payload) == list(PROMOTION_READINESS_CHECK_TOP_LEVEL_KEYS)
    assert raw_json.startswith(
        '{"artifact_type":"promotion_readiness_check","schema_version":"1.0",'
        '"research_only":true'
    )
    assert payload["source_artifact"] == "reports/cross-asset-thesis-ledger.json"
    assert len(payload["source_content_sha256"]) == 64
    assert payload["summary"]["release_gate"] == "PASS"
    assert payload["summary"]["promotion_gate"] == "WARN"


def test_cli_promotion_readiness_check_accepts_custom_input_and_outputs(
    tmp_path: Path,
) -> None:
    ledger_path = tmp_path / "ledger.json"
    markdown_path = tmp_path / "promotion.md"
    json_path = tmp_path / "promotion.json"
    ledger_raw = json.dumps(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    ledger_path.write_text(ledger_raw, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--promotion-readiness-check",
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
    raw_json = json_path.read_text(encoding="utf-8")
    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(raw_json)
    assert payload["source_artifact"] == ledger_path.name
    assert payload["source_content_sha256"] == _source_sha256(ledger_raw)
    assert payload["source_artifact_role"] == (
        "Repo-relative static thesis-ledger JSON path read by this check."
    )
    assert payload["default_outputs"] == {
        "markdown": "reports/promotion-readiness-check.md",
        "json": "reports/promotion-readiness-check.json",
    }
    assert payload["default_outputs_role"] == (
        "Repo-relative paths written by --promotion-readiness-check when "
        "output overrides are not supplied."
    )
    assert str(ledger_path.parent) not in raw_json
    assert str(ledger_path.parent) not in markdown
    assert "- **Source content SHA-256**:" in markdown
    assert "Repo-relative static thesis-ledger JSON path read by this check" in markdown
    assert "Repo-relative paths written by --promotion-readiness-check" in markdown
    assert "leveraged_caveat_evidence" in markdown


def test_cli_promotion_readiness_check_hash_distinguishes_same_filename_inputs(
    tmp_path: Path,
) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    first_dir.mkdir()
    second_dir.mkdir()
    first_path = first_dir / "ledger.json"
    second_path = second_dir / "ledger.json"
    first_raw = json.dumps(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    second_ledger = deepcopy(build_cross_asset_thesis_ledger(SAMPLE_DATA))
    second_ledger["validation_split"] = {"split_ratio": 0.7}
    second_raw = json.dumps(second_ledger)
    first_path.write_text(first_raw, encoding="utf-8")
    second_path.write_text(second_raw, encoding="utf-8")

    outputs: list[dict[str, object]] = []
    for ledger_path in (first_path, second_path):
        json_path = ledger_path.parent / "promotion.json"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "market_signal_lab.cli",
                "--promotion-readiness-check",
                str(ledger_path),
                "--json-output",
                str(json_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        outputs.append(json.loads(json_path.read_text(encoding="utf-8")))

    assert outputs[0]["source_artifact"] == "ledger.json"
    assert outputs[1]["source_artifact"] == "ledger.json"
    assert outputs[0]["source_content_sha256"] == _source_sha256(first_raw)
    assert outputs[1]["source_content_sha256"] == _source_sha256(second_raw)
    assert outputs[0]["source_content_sha256"] != outputs[1]["source_content_sha256"]


def test_cli_promotion_readiness_check_rejects_incompatible_options() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--promotion-readiness-check",
            "--html-output",
            "promotion.html",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "--promotion-readiness-check writes Markdown/JSON, not HTML" in result.stderr


def test_cli_promotion_readiness_check_rejects_other_modes() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--promotion-readiness-check",
            "--prediction-readiness-audit",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert (
        "--prediction-readiness-audit cannot be combined with "
        "--promotion-readiness-check"
    ) in result.stderr


def test_cli_promotion_readiness_check_rejects_two_input_paths() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--promotion-readiness-check",
            "reports/cross-asset-thesis-ledger.json",
            "extra-ledger.json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert (
        "--promotion-readiness-check accepts only one ledger JSON path"
        in result.stderr
    )


def test_cli_promotion_readiness_check_rejects_invalid_json(tmp_path: Path) -> None:
    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text("{", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--promotion-readiness-check",
            str(ledger_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert f"Invalid promotion-readiness check JSON {ledger_path}" in result.stderr
