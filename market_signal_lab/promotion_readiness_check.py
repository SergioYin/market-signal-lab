"""Public-promotion readiness checks for static thesis-ledger artifacts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from market_signal_lab.packet import LEVERAGED_ETF_RISK_BOUNDARY


PROMOTION_READINESS_CHECK_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    "research_only",
    "static_only",
    "historical_diagnostics_only",
    "no_live_data",
    "no_broker_or_account",
    "no_orders_or_position_sizing",
    "no_recommendations_or_forecasts",
    "not_investment_advice",
    "source_artifact",
    "source_content_sha256",
    "source_artifact_role",
    "default_outputs",
    "default_outputs_role",
    "summary",
    "checks",
    "actionable_next_fixes",
    "public_boundaries",
    "verification_commands",
)
PROMOTION_READINESS_CHECK_ITEM_KEYS = (
    "check",
    "label",
    "release_gate_impact",
    "promotion_gate_impact",
    "evidence",
    "next_fix",
)

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
UNKNOWN_SYMBOL = "unknown"


def build_promotion_readiness_check(
    ledger: Mapping[str, Any],
    source_artifact: str,
    source_content_sha256: str,
) -> dict[str, Any]:
    """Build a deterministic public-promotion readiness payload."""

    if not isinstance(ledger, Mapping):
        raise ValueError("Promotion-readiness check input must be a JSON object")

    assets = _sequence_of_mappings(ledger.get("assets"))
    asset_symbols = [
        _string_value(asset.get("symbol"), UNKNOWN_SYMBOL) for asset in assets
    ]
    checks = [
        _check_no_live_data_boundary(ledger),
        _check_no_advice_boundary(ledger),
        _check_benchmark_evidence(assets),
        _check_fee_evidence(ledger, assets),
        _check_drawdown_evidence(assets),
        _check_train_test_evidence(ledger),
        _check_leveraged_caveat_evidence(ledger, asset_symbols),
    ]
    labels = [check["label"] for check in checks]
    release_gate = _release_gate(labels)
    promotion_gate = _promotion_gate(labels)

    return {
        "artifact_type": "promotion_readiness_check",
        "schema_version": "1.0",
        "research_only": True,
        "static_only": True,
        "historical_diagnostics_only": True,
        "no_live_data": True,
        "no_broker_or_account": True,
        "no_orders_or_position_sizing": True,
        "no_recommendations_or_forecasts": True,
        "not_investment_advice": True,
        "source_artifact": source_artifact,
        "source_content_sha256": source_content_sha256,
        "source_artifact_role": (
            "Repo-relative static thesis-ledger JSON path read by this check."
        ),
        "default_outputs": {
            "markdown": "reports/promotion-readiness-check.md",
            "json": "reports/promotion-readiness-check.json",
        },
        "default_outputs_role": (
            "Repo-relative paths written by --promotion-readiness-check when "
            "output overrides are not supplied."
        ),
        "summary": {
            "release_gate": release_gate,
            "promotion_gate": promotion_gate,
            "label_meanings": {
                PASS: "Expected documentation evidence and boundary wording are visible.",
                WARN: (
                    "Public review/release can continue, but broader promotion "
                    "or citation stays on hold until resolved or explicitly disclosed."
                ),
                FAIL: "Hold release or broader promotion until the listed fix is addressed.",
            },
            "count_scope": "Counts cover the checks array and are ordered PASS/WARN/FAIL.",
            "pass_count": labels.count(PASS),
            "warn_count": labels.count(WARN),
            "fail_count": labels.count(FAIL),
            "asset_symbols": asset_symbols,
            "interpretation": (
                "Release Gate checks whether the static artifact can be shared "
                "for review. Promotion Gate checks whether broader public "
                "promotion has enough visible evidence and boundary wording. "
                "Neither gate is trading readiness, forecast validation, "
                "recommendation approval, suitability review, or investment advice."
            ),
        },
        "checks": checks,
        "actionable_next_fixes": [
            check["next_fix"] for check in checks if check["label"] != PASS
        ],
        "public_boundaries": [
            (
                "This check reads a static thesis-ledger JSON artifact only; it "
                "does not fetch live market data, connect to brokers, inspect "
                "accounts, route orders, or size positions."
            ),
            (
                "PASS/WARN/FAIL labels are documentation readiness labels only, "
                "not market outlooks, buy/sell/hold signals, forecasts, "
                "recommendations, suitability conclusions, or investment advice."
            ),
            LEVERAGED_ETF_RISK_BOUNDARY,
        ],
        "verification_commands": [
            "python -m market_signal_lab.cli --promotion-readiness-check",
            "python -m market_signal_lab.cli --prediction-readiness-audit",
            "python -m market_signal_lab.cli --validate-thesis-ledger",
            "python -m pytest",
        ],
    }


def render_promotion_readiness_check(payload: Mapping[str, Any]) -> str:
    """Render a public-promotion readiness payload as Markdown."""

    summary = _mapping(payload.get("summary"))
    lines = [
        "# Public-Promotion Readiness Check",
        "",
        (
            "Focused static check for whether the cross-asset thesis ledger has "
            "enough public-facing evidence and boundary language for broader "
            "promotion. It is not trading readiness, a forecast, a recommendation, "
            "or investment advice."
        ),
        "",
        "## Gate Labels",
        "",
        f"- **Source artifact**: {payload.get('source_artifact', 'unknown')} "
        f"({payload.get('source_artifact_role', 'input artifact')})",
        f"- **Source content SHA-256**: "
        f"{payload.get('source_content_sha256', 'unknown')}",
        f"- **Default outputs**: "
        f"{_mapping(payload.get('default_outputs')).get('markdown', 'unknown')}, "
        f"{_mapping(payload.get('default_outputs')).get('json', 'unknown')} "
        f"({payload.get('default_outputs_role', 'default output paths')})",
        f"- **Release Gate**: {summary.get('release_gate', 'UNKNOWN')}",
        f"- **Promotion Gate**: {summary.get('promotion_gate', 'UNKNOWN')}",
        f"- **PASS/WARN/FAIL counts (checks array)**: {summary.get('pass_count', 0)} / "
        f"{summary.get('warn_count', 0)} / {summary.get('fail_count', 0)}",
        f"- **Count scope**: {summary.get('count_scope', '')}",
        f"- **Label meanings**: {_format_label_meanings(summary.get('label_meanings'))}",
        f"- **Interpretation**: {summary.get('interpretation', '')}",
        "",
        "## Checks",
        "",
        "| check | label | release gate impact | promotion gate impact |",
        "|---|---|---|---|",
    ]
    for item in payload.get("checks", ()):
        check = _mapping(item)
        lines.append(
            "| "
            f"{check.get('check', '')} | "
            f"{check.get('label', '')} | "
            f"{check.get('release_gate_impact', '')} | "
            f"{check.get('promotion_gate_impact', '')} |"
        )

    lines.extend(["", "## Evidence and Follow-Up", ""])
    for item in payload.get("checks", ()):
        check = _mapping(item)
        label = check.get("label", "")
        lines.append(f"### {check.get('check', 'check')}")
        lines.append("")
        lines.append(f"- **Label**: {label}")
        lines.append(f"- **Evidence**: {check.get('evidence', '')}")
        if label == PASS:
            lines.append(
                "- **Review note**: No fix is listed for this PASS check; keep "
                "the evidence visible in public review materials."
            )
        else:
            lines.append(f"- **Next fix**: {check.get('next_fix', '')}")
        lines.append("")

    lines.extend(["## Actionable Next Fixes", ""])
    next_fixes = payload.get("actionable_next_fixes", ())
    if next_fixes:
        lines.extend(f"- {fix}" for fix in next_fixes)
    else:
        lines.append("- No blocking fixes found in this static ledger artifact.")

    lines.extend(["", "## Public Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in payload.get("public_boundaries", ()))
    lines.extend(["", "## Verification Commands", ""])
    lines.extend(f"- `{command}`" for command in payload.get("verification_commands", ()))
    lines.append("")
    return "\n".join(lines)


def _check_no_live_data_boundary(ledger: Mapping[str, Any]) -> dict[str, str]:
    source = _mapping(ledger.get("source"))
    provenance = _mapping(ledger.get("data_provenance"))
    input_path = str(source.get("input_path", ""))
    static_source = input_path.startswith("examples/data/") or bool(provenance)
    required_flags = {
        "offline_only": ledger.get("offline_only") is True,
        "no_broker_or_live_data": ledger.get("no_broker_or_live_data") is True,
        "historical_diagnostics_only": ledger.get("historical_diagnostics_only")
        is True,
    }
    label = PASS if static_source and all(required_flags.values()) else FAIL
    return _check(
        check="no_live_data_boundary",
        label=label,
        evidence=(
            f"input_path={input_path}; static_source={static_source}; "
            f"flags={_format_bool_mapping(required_flags)}"
        ),
        next_fix=(
            "Keep promotion on hold until the ledger declares offline/static "
            "historical data, no broker/live data, and a checked-in sample source."
        ),
    )


def _check_no_advice_boundary(ledger: Mapping[str, Any]) -> dict[str, str]:
    boundaries = _mapping(ledger.get("risk_boundaries"))
    text = _combined_text(
        ledger.get("note"),
        boundaries.get("non_advice"),
        boundaries.get("scope_limits"),
    )
    required_terms = (
        "not investment advice",
        "not a recommendation",
        "not a prediction",
    )
    label = (
        PASS
        if ledger.get("research_only") is True
        and all(term in text for term in required_terms)
        else FAIL
    )
    return _check(
        check="no_advice_boundary",
        label=label,
        evidence=(
            f"research_only={ledger.get('research_only')}; "
            f"required_terms={', '.join(required_terms)}"
        ),
        next_fix=(
            "Add explicit research-only, not-investment-advice, not-a-"
            "recommendation, and not-a-prediction wording near the promoted claim."
        ),
    )


def _check_benchmark_evidence(
    assets: Sequence[Mapping[str, Any]],
) -> dict[str, str]:
    required = ("buy_and_hold_total_return", "strategy_minus_buy_and_hold_return")
    missing = [
        _asset_symbol(asset)
        for asset in assets
        if not all(key in _mapping(asset.get("metrics")) for key in required)
    ]
    label = PASS if assets and not missing else FAIL
    return _check(
        check="benchmark_evidence",
        label=label,
        evidence=f"asset_count={len(assets)}; missing_symbols={_format_list(missing)}",
        next_fix=(
            "Regenerate or edit the ledger so every asset includes same-period "
            "buy-and-hold return and strategy-minus-buy-and-hold fields."
        ),
    )


def _check_fee_evidence(
    ledger: Mapping[str, Any],
    assets: Sequence[Mapping[str, Any]],
) -> dict[str, str]:
    missing: list[str] = []
    if "fee_bps" not in _mapping(ledger.get("strategy_config")):
        missing.append("strategy_config.fee_bps")
    for asset in assets:
        symbol = _asset_symbol(asset)
        if "total_fee_drag" not in _mapping(asset.get("exposure_trade_review")):
            missing.append(f"{symbol}.exposure_trade_review.total_fee_drag")
    label = PASS if assets and not missing else FAIL
    return _check(
        check="fee_evidence",
        label=label,
        evidence=f"missing={_format_list(missing)}",
        next_fix=(
            "Add the modeled fee basis-point assumption and per-asset total fee "
            "drag before promotion copy mentions performance comparisons."
        ),
    )


def _check_drawdown_evidence(
    assets: Sequence[Mapping[str, Any]],
) -> dict[str, str]:
    missing = [
        f"{_asset_symbol(asset)}.metrics.max_drawdown"
        for asset in assets
        if "max_drawdown" not in _mapping(asset.get("metrics"))
    ]
    label = PASS if assets and not missing else FAIL
    return _check(
        check="drawdown_evidence",
        label=label,
        evidence=f"missing={_format_list(missing)}",
        next_fix=(
            "Add max_drawdown for every asset and keep drawdown language framed "
            "as historical diagnostics, not future loss bounds."
        ),
    )


def _check_train_test_evidence(ledger: Mapping[str, Any]) -> dict[str, str]:
    has_validation_split = "validation_split" in ledger
    has_ranked_train_test = any(
        "train_metrics" in row and "test_metrics" in row
        for row in _sequence_of_mappings(ledger.get("ranked_results"))
    )
    label = PASS if has_validation_split or has_ranked_train_test else WARN
    return _check(
        check="train_test_evidence",
        label=label,
        evidence=(
            f"validation_split={has_validation_split}; "
            f"ranked_train_test={has_ranked_train_test}"
        ),
        next_fix=(
            "Before broader promotion or citation, attach a split-sweep or "
            "train/test artifact that shows train metrics, test metrics, and "
            "any return-gap or robustness labels, or explicitly disclose that "
            "the evidence is not yet present."
        ),
    )


def _check_leveraged_caveat_evidence(
    ledger: Mapping[str, Any],
    asset_symbols: Sequence[str],
) -> dict[str, str]:
    boundary = str(
        _mapping(ledger.get("risk_boundaries")).get("leveraged_etf_like", "")
    )
    text = boundary.lower()
    required_terms = ("leveraged", "daily reset", "path-dependent", "losses")
    leveraged_symbols = [
        symbol for symbol in asset_symbols if symbol.startswith(("QLD", "TQQQ"))
    ]
    label = (
        PASS
        if leveraged_symbols and all(term in text for term in required_terms)
        else FAIL
    )
    return _check(
        check="leveraged_caveat_evidence",
        label=label,
        evidence=(
            f"leveraged_symbols={_format_list(leveraged_symbols)}; "
            f"required_terms={', '.join(required_terms)}"
        ),
        next_fix=(
            "Add visible leveraged ETF-like caveats covering daily reset, "
            "path dependency, magnified losses, fees, spreads, liquidity, and "
            "tracking differences."
        ),
    )


def _check(check: str, label: str, evidence: str, next_fix: str) -> dict[str, str]:
    return {
        "check": check,
        "label": label,
        "release_gate_impact": _release_impact(label),
        "promotion_gate_impact": _promotion_impact(label),
        "evidence": evidence,
        "next_fix": next_fix,
    }


def _release_gate(labels: Sequence[str]) -> str:
    return FAIL if FAIL in labels else PASS


def _promotion_gate(labels: Sequence[str]) -> str:
    if FAIL in labels:
        return FAIL
    if WARN in labels:
        return WARN
    return PASS


def _release_impact(label: str) -> str:
    if label == FAIL:
        return "Blocks public release until fixed."
    if label == WARN:
        return "Public review/release can continue; keep the WARN visible."
    return "No release blocker found."


def _promotion_impact(label: str) -> str:
    if label == FAIL:
        return "Blocks promotion."
    if label == WARN:
        return "Broader promotion/citation stays on hold until resolved or explicitly disclosed."
    return "No promotion blocker found."


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


def _asset_symbol(asset: Mapping[str, Any]) -> str:
    return _string_value(asset.get("symbol"), UNKNOWN_SYMBOL)


def _format_list(values: Sequence[str]) -> str:
    return ", ".join(values) if values else "none"


def _format_bool_mapping(values: Mapping[str, bool]) -> str:
    return ", ".join(f"{key}={value}" for key, value in values.items())


def _format_label_meanings(value: Any) -> str:
    meanings = _mapping(value)
    parts = []
    for label in (PASS, WARN, FAIL):
        meaning = meanings.get(label)
        if meaning:
            parts.append(f"{label} = {meaning}")
    return "; ".join(parts)
