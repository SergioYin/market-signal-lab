"""Prediction-readiness audit for static sample report artifacts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


PREDICTION_READINESS_AUDIT_TOP_LEVEL_KEYS = (
    "audit_type",
    "schema_version",
    "research_only",
    "historical_diagnostics_only",
    "not_investment_advice",
    "source_artifact",
    "summary",
    "criteria",
    "asset_symbols",
    "verification_commands",
)
PREDICTION_READINESS_CRITERION_KEYS = (
    "criterion",
    "label",
    "status",
    "evidence",
    "review_note",
)
PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
UNKNOWN_SYMBOL = "unknown"


def build_prediction_readiness_audit(
    ledger: Mapping[str, Any],
    source_artifact: str,
) -> dict[str, Any]:
    """Build a deterministic audit summary from a thesis-ledger JSON object."""

    if not isinstance(ledger, Mapping):
        raise ValueError("Prediction-readiness audit input must be a JSON object")

    assets = _sequence_of_mappings(ledger.get("assets"))
    asset_symbols = [
        _string_value(asset.get("symbol"), UNKNOWN_SYMBOL) for asset in assets
    ]
    criteria = [
        _audit_static_data(ledger),
        _audit_non_advice_boundary(ledger),
        _audit_benchmark_presence(assets),
        _audit_fee_drawdown_exposure_presence(ledger, assets),
        _audit_train_test_diagnostics(ledger),
        _audit_leveraged_etf_caveats(ledger, asset_symbols),
    ]
    fail_count = sum(1 for item in criteria if item["label"] == FAIL)
    warn_count = sum(1 for item in criteria if item["label"] == WARN)

    return {
        "audit_type": "prediction_readiness_audit",
        "schema_version": "1.0",
        "research_only": True,
        "historical_diagnostics_only": True,
        "not_investment_advice": True,
        "source_artifact": source_artifact,
        "summary": {
            "overall_label": FAIL if fail_count else (WARN if warn_count else PASS),
            "pass_count": sum(1 for item in criteria if item["label"] == PASS),
            "warn_count": warn_count,
            "fail_count": fail_count,
            "review_boundary": (
                "This audit checks whether required labels and supporting "
                "fields are visible in a static historical artifact for "
                "public review. It is not a prediction, forecast, "
                "recommendation, trading instruction, or investment-advice "
                "approval."
            ),
        },
        "criteria": criteria,
        "asset_symbols": asset_symbols,
        "verification_commands": [
            "python -m market_signal_lab.cli --prediction-readiness-audit",
            "python -m market_signal_lab.cli --validate-thesis-ledger",
            "python -m pytest",
        ],
    }


def render_prediction_readiness_audit(payload: Mapping[str, Any]) -> str:
    """Render a prediction-readiness audit payload as Markdown."""

    summary = _mapping(payload.get("summary"))
    lines = [
        "# Prediction-Readiness Audit",
        "",
        (
            "Static research audit for checking whether the sample artifact keeps "
            "historical diagnostics separate from predictions, recommendations, "
            "trading instructions, and investment advice."
        ),
        "",
        "## How to Read This",
        "",
        (
            "- Read PASS as a documentation item found, WARN as a review "
            "question, and FAIL as a missing or incomplete boundary."
        ),
        (
            "- Treat every row as a static documentation check, not as a "
            "market outlook, action cue, or position-sizing input."
        ),
        (
            "- For leveraged ETF-like rows, confirm the report names daily "
            "reset, path dependency, magnified losses, and unmodeled product "
            "costs."
        ),
        "",
        "## Summary",
        "",
        f"- **Source artifact**: {payload.get('source_artifact', 'unknown')}",
        f"- **Overall label**: {summary.get('overall_label', 'unknown')}",
        f"- **PASS/WARN/FAIL counts**: {summary.get('pass_count', 0)} / "
        f"{summary.get('warn_count', 0)} / {summary.get('fail_count', 0)}",
        f"- **Boundary**: {summary.get('review_boundary', '')}",
        "",
        "## Leveraged ETF Risk Boundary",
        "",
        (
            "Leveraged ETF-like examples are research fixtures only. Daily reset "
            "and compounding can make multi-day results path-dependent, losses "
            "can be magnified quickly, and real funds can differ because of "
            "expenses, financing, tracking differences, taxes, liquidity, "
            "spreads, and market impact that this audit does not model."
        ),
        "",
        "## Criteria",
        "",
        "| criterion | label | status |",
        "|---|---|---|",
    ]
    for criterion in payload.get("criteria", ()):
        item = _mapping(criterion)
        lines.append(
            "| "
            f"{item.get('criterion', '')} | "
            f"{item.get('label', '')} | "
            f"{item.get('status', '')} |"
        )

    lines.extend(["", "## Evidence Notes", ""])
    for criterion in payload.get("criteria", ()):
        item = _mapping(criterion)
        lines.append(f"### {item.get('criterion', 'criterion')}")
        lines.append("")
        lines.append(f"- **Label**: {item.get('label', '')}")
        lines.append(f"- **Status**: {item.get('status', '')}")
        lines.append(f"- **Evidence**: {item.get('evidence', '')}")
        lines.append(f"- **Review note**: {item.get('review_note', '')}")
        lines.append("")

    lines.extend(["## Verification Commands", ""])
    lines.extend(
        f"- `{command}`" for command in payload.get("verification_commands", ())
    )
    lines.append("")
    return "\n".join(lines)


def _audit_static_data(ledger: Mapping[str, Any]) -> dict[str, str]:
    source = _mapping(ledger.get("source"))
    provenance = _mapping(ledger.get("data_provenance"))
    static_flags = (
        ledger.get("offline_only") is True,
        ledger.get("no_broker_or_live_data") is True,
        ledger.get("historical_diagnostics_only") is True,
    )
    input_path = str(source.get("input_path", ""))
    static_source = input_path.startswith("examples/data/") or bool(provenance)
    label = PASS if all(static_flags) and static_source else FAIL
    return _criterion(
        criterion="static_data",
        label=label,
        status=(
            "Artifact is limited to static/offline historical rows."
            if label == PASS
            else "Static/offline data boundaries are incomplete."
        ),
        evidence=f"input_path={input_path}; offline_only={ledger.get('offline_only')}",
        review_note=(
            "Static sample rows are diagnostics only and do not update from "
            "live markets."
        ),
    )


def _audit_non_advice_boundary(ledger: Mapping[str, Any]) -> dict[str, str]:
    text = _combined_text(
        ledger.get("note"),
        _mapping(ledger.get("risk_boundaries")).get("non_advice"),
        _mapping(ledger.get("risk_boundaries")).get("scope_limits"),
    )
    required = ("not investment advice", "not a recommendation", "not a prediction")
    label = (
        PASS
        if ledger.get("research_only") is True
        and all(term in text for term in required)
        else FAIL
    )
    return _criterion(
        criterion="non_advice_boundary",
        label=label,
        status=(
            "Research-only and non-advice wording is present."
            if label == PASS
            else "Non-advice boundary wording is missing or incomplete."
        ),
        evidence=(
            f"research_only={ledger.get('research_only')}; "
            f"required_terms={', '.join(required)}"
        ),
        review_note=(
            "Passing this check does not change the artifact scope; it confirms "
            "the boundary label is present."
        ),
    )


def _audit_benchmark_presence(assets: Sequence[Mapping[str, Any]]) -> dict[str, str]:
    required = ("buy_and_hold_total_return", "strategy_minus_buy_and_hold_return")
    missing = [
        _string_value(asset.get("symbol"), UNKNOWN_SYMBOL)
        for asset in assets
        if not all(key in _mapping(asset.get("metrics")) for key in required)
    ]
    label = PASS if assets and not missing else FAIL
    return _criterion(
        criterion="benchmark_presence",
        label=label,
        status=(
            "Every asset includes same-period buy-and-hold benchmark fields."
            if label == PASS
            else "One or more assets are missing benchmark comparison fields."
        ),
        evidence=(
            f"asset_count={len(assets)}; missing_symbols={_format_list(missing)}"
        ),
        review_note="Benchmarks are comparison diagnostics only, not action guidance.",
    )


def _audit_fee_drawdown_exposure_presence(
    ledger: Mapping[str, Any],
    assets: Sequence[Mapping[str, Any]],
) -> dict[str, str]:
    missing: list[str] = []
    if "fee_bps" not in _mapping(ledger.get("strategy_config")):
        missing.append("strategy_config.fee_bps")
    for asset in assets:
        symbol = _string_value(asset.get("symbol"), UNKNOWN_SYMBOL)
        metrics = _mapping(asset.get("metrics"))
        exposure = _mapping(asset.get("exposure_trade_review"))
        if "max_drawdown" not in metrics:
            missing.append(f"{symbol}.metrics.max_drawdown")
        for key in (
            "total_fee_drag",
            "average_exposure",
            "percent_periods_in_market",
            "exposure_changes",
        ):
            if key not in exposure:
                missing.append(f"{symbol}.exposure_trade_review.{key}")
    label = PASS if assets and not missing else FAIL
    return _criterion(
        criterion="fee_drawdown_exposure_presence",
        label=label,
        status=(
            "Fee, drawdown, and exposure diagnostics are present."
            if label == PASS
            else "Fee, drawdown, or exposure diagnostics are incomplete."
        ),
        evidence=f"missing={_format_list(missing)}",
        review_note=(
            "These diagnostics describe modeled history only and omit taxes, "
            "spreads, market impact, and execution-quality assumptions."
        ),
    )


def _audit_train_test_diagnostics(ledger: Mapping[str, Any]) -> dict[str, str]:
    has_split = "validation_split" in ledger
    has_ranked_train_test = any(
        "train_metrics" in row and "test_metrics" in row
        for row in _sequence_of_mappings(ledger.get("ranked_results"))
    )
    label = PASS if has_split or has_ranked_train_test else WARN
    return _criterion(
        criterion="train_test_diagnostics",
        label=label,
        status=(
            "Train/test diagnostics are present."
            if label == PASS
            else "No train/test diagnostics are present in this ledger artifact."
        ),
        evidence=(
            f"validation_split={has_split}; ranked_train_test={has_ranked_train_test}"
        ),
        review_note=(
            "Absence is a review warning, not a failure of the static ledger "
            "shape; use split-sweep artifacts for historical train/test rank "
            "and return-gap documentation checks."
        ),
    )


def _audit_leveraged_etf_caveats(
    ledger: Mapping[str, Any],
    asset_symbols: Sequence[str],
) -> dict[str, str]:
    boundary = str(
        _mapping(ledger.get("risk_boundaries")).get("leveraged_etf_like", "")
    )
    text = boundary.lower()
    required = ("leveraged", "daily reset", "path-dependent", "losses")
    leveraged_symbols = [
        symbol for symbol in asset_symbols if symbol.startswith(("QLD", "TQQQ"))
    ]
    label = (
        PASS
        if leveraged_symbols and all(term in text for term in required)
        else FAIL
    )
    return _criterion(
        criterion="leveraged_etf_caveats",
        label=label,
        status=(
            "Leveraged ETF-like daily-reset and path-dependency caveats are present."
            if label == PASS
            else "Leveraged ETF-like caveats are missing or incomplete."
        ),
        evidence=(
            f"leveraged_symbols={_format_list(leveraged_symbols)}; "
            f"required_terms={', '.join(required)}"
        ),
        review_note=(
            "Leveraged ETF-like sample rows require extra caution because "
            "multi-day outcomes can diverge sharply from simple leverage "
            "multiples."
        ),
    )


def _criterion(
    criterion: str,
    label: str,
    status: str,
    evidence: str,
    review_note: str,
) -> dict[str, str]:
    return {
        "criterion": criterion,
        "label": label,
        "status": status,
        "evidence": evidence,
        "review_note": review_note,
    }


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sequence_of_mappings(value: Any) -> list[Mapping[str, Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _combined_text(*values: Any) -> str:
    return " ".join(str(value).lower() for value in values if value is not None)


def _string_value(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _format_list(values: Sequence[str]) -> str:
    return ", ".join(values) if values else "none"
