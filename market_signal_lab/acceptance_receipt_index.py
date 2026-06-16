"""Deterministic acceptance receipt index for public review artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from market_signal_lab.reviewer_bundle import build_artifact_integrity_summary


ACCEPTANCE_RECEIPT_INDEX_MARKDOWN_PATH = "reports/acceptance-receipt-index.md"
ACCEPTANCE_RECEIPT_INDEX_JSON_PATH = "reports/acceptance-receipt-index.json"
ACCEPTANCE_RECEIPT_INDEX_COMMAND = (
    "python -m market_signal_lab.cli --acceptance-receipt-index"
)

BOUNDARY_FLAGS = {
    "research_only": True,
    "static_only": True,
    "fixture_or_static_data_only": True,
    "no_live_data": True,
    "no_broker_or_account": True,
    "no_orders_or_position_sizing": True,
    "no_recommendations_or_forecasts": True,
    "not_investment_advice": True,
}

INDEXED_RECEIPTS = (
    {
        "label": "Public demo evidence receipt",
        "markdown_path": "reports/public-demo-evidence-receipt.md",
        "json_path": "reports/public-demo-evidence-receipt.json",
        "source_command": "python -m market_signal_lab.cli --public-demo-evidence-receipt",
        "evidence_role": (
            "Links public gallery/backtest evidence, fixture provenance paths, "
            "artifact hashes, and no-live-data/no-advice claims."
        ),
    },
    {
        "label": "Reviewer rerun receipt",
        "markdown_path": "reports/reviewer-rerun-receipt.md",
        "json_path": "reports/reviewer-rerun-receipt.json",
        "source_command": "python -m market_signal_lab.cli --reviewer-rerun-receipt",
        "evidence_role": (
            "Lists deterministic public rerun commands, expected artifacts, "
            "PASS/WARN checks, and no-live-data/no-advice boundaries."
        ),
    },
    {
        "label": "Reviewer evidence bundle",
        "markdown_path": "reports/reviewer-evidence-bundle.md",
        "json_path": "reports/reviewer-evidence-bundle.json",
        "source_command": "python -m market_signal_lab.cli --reviewer-evidence-bundle",
        "evidence_role": (
            "Ties the gallery, thesis-ledger acceptance route, methodology "
            "risks, verification commands, and artifact hash summary together."
        ),
    },
)

FIXTURE_PROVENANCE = (
    {
        "fixture_path": "examples/data/sample_tqqq_qld_like.csv",
        "provenance_path": "examples/data/sample_tqqq_qld_like.csv.provenance.json",
        "use": (
            "Synthetic static OHLC fixture used by single report, sweep, fee "
            "sensitivity, and cross-asset thesis-ledger demo artifacts."
        ),
    },
    {
        "fixture_path": "examples/data/sample_multi_regime.csv",
        "provenance_path": "examples/data/sample_multi_regime.csv.provenance.json",
        "use": (
            "Synthetic static multi-regime fixture used by deterministic "
            "regime-comparison demo artifacts."
        ),
    },
)

REVIEWER_RERUN_COMMANDS = (
    ACCEPTANCE_RECEIPT_INDEX_COMMAND,
    "python -m market_signal_lab.cli --public-demo-evidence-receipt",
    "python -m market_signal_lab.cli --reviewer-rerun-receipt",
    "python -m market_signal_lab.cli --reviewer-evidence-bundle",
    "python scripts/selfcheck.py",
)

NOT_CLAIMED = (
    "This index does not execute rerun commands; it records deterministic public artifact links.",
    "SHA-256 hashes prove local file-byte identity at generation time only.",
    "Hashes and PASS/WARN labels do not validate financial correctness, future performance, suitability, recommendations, or investment advice.",
    "No live data, broker, account, order-routing, position-sizing, forecast, recommendation, or advice workflow is included.",
)

INDEX_ARTIFACT_PATHS = tuple(
    path
    for receipt in INDEXED_RECEIPTS
    for path in (receipt["markdown_path"], receipt["json_path"])
) + tuple(
    path
    for fixture in FIXTURE_PROVENANCE
    for path in (fixture["fixture_path"], fixture["provenance_path"])
)


def build_acceptance_receipt_index(
    artifact_root: Path | str = Path("."),
) -> dict[str, Any]:
    """Build a deterministic index linking public acceptance receipt evidence."""

    return {
        "artifact_type": "acceptance_receipt_index",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "purpose": (
            "Give public reviewers one bounded deterministic index linking the "
            "existing public demo evidence receipt, reviewer rerun receipt, "
            "reviewer evidence bundle, artifact hashes, fixture provenance, "
            "and no-live-data/no-advice boundaries."
        ),
        "default_outputs": {
            "markdown": ACCEPTANCE_RECEIPT_INDEX_MARKDOWN_PATH,
            "json": ACCEPTANCE_RECEIPT_INDEX_JSON_PATH,
        },
        "verification_command": ACCEPTANCE_RECEIPT_INDEX_COMMAND,
        "indexed_receipts": [dict(receipt) for receipt in INDEXED_RECEIPTS],
        "fixture_provenance": [dict(fixture) for fixture in FIXTURE_PROVENANCE],
        "reviewer_rerun_commands": list(REVIEWER_RERUN_COMMANDS),
        "artifact_integrity_summary": build_artifact_integrity_summary(
            artifact_root,
            INDEX_ARTIFACT_PATHS,
        ),
        "not_claimed": list(NOT_CLAIMED),
    }


def render_acceptance_receipt_index(payload: dict[str, Any]) -> str:
    """Render the acceptance receipt index as Markdown."""

    integrity = payload["artifact_integrity_summary"]
    lines = [
        "# Acceptance Receipt Index",
        "",
        payload["purpose"],
        "",
        "## Indexed Receipts",
        "",
    ]
    for receipt in payload["indexed_receipts"]:
        lines.extend(
            [
                f"- **{receipt['label']}**",
                f"  - Markdown: `{receipt['markdown_path']}`",
                f"  - JSON: `{receipt['json_path']}`",
                f"  - Rerun: `{receipt['source_command']}`",
                f"  - Role: {receipt['evidence_role']}",
            ]
        )

    lines.extend(["", "## Fixture Provenance", ""])
    for fixture in payload["fixture_provenance"]:
        lines.append(
            f"- `{fixture['fixture_path']}` with `{fixture['provenance_path']}`: "
            f"{fixture['use']}"
        )

    lines.extend(["", "## Reviewer Rerun Commands", ""])
    lines.extend(f"- `{command}`" for command in payload["reviewer_rerun_commands"])

    lines.extend(
        [
            "",
            "## Artifact Hash Index",
            "",
            f"- Integrity status: `{integrity['integrity_status']}`",
            f"- Interpretation: {integrity['interpretation']}",
            f"- Caveat: {integrity['caveat']}",
            f"- Algorithm: `{integrity['algorithm']}`",
            f"- Scope: {integrity['scope']}",
            f"- Present artifacts: `{integrity['present_count']}` of `{integrity['artifact_count']}`",
            "",
            "| Path | Status | Bytes | SHA-256 |",
            "| --- | --- | ---: | --- |",
        ]
    )
    lines.extend(
        "| {path} | {status} | {byte_count} | {sha256} |".format(
            path=artifact["path"],
            status=artifact["status"],
            byte_count=artifact["byte_count"],
            sha256=artifact["sha256"] or "missing",
        )
        for artifact in integrity["artifacts"]
    )

    lines.extend(["", "## Not Claimed", ""])
    lines.extend(f"- {claim}" for claim in payload["not_claimed"])
    lines.extend(["", "## Boundary Flags", ""])
    lines.extend(f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS)
    lines.append("")
    return "\n".join(lines)
