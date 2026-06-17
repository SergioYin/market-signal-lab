"""Deterministic reviewer rerun receipt artifact."""

from __future__ import annotations

from typing import Any


BOUNDARY_FLAGS = {
    "research_only": True,
    "static_only": True,
    "no_live_data": True,
    "no_broker_or_account": True,
    "no_orders_or_position_sizing": True,
    "no_recommendations_or_forecasts": True,
    "not_investment_advice": True,
}

REVIEWER_RERUN_RECEIPT_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "verification_commands",
    "expected_artifacts",
    "checklist",
    "review_boundaries",
)

VERIFICATION_COMMAND_KEYS = (
    "command",
    "purpose",
    "expected_artifacts",
)
EXPECTED_ARTIFACT_KEYS = ("path", "format", "source_command")
CHECKLIST_KEYS = ("status", "check", "note")

VERIFICATION_COMMANDS = (
    {
        "command": "python -m market_signal_lab.cli --reviewer-rerun-receipt",
        "purpose": "Regenerate this reviewer rerun receipt from stdlib-only code.",
        "expected_artifacts": [
            "reports/reviewer-rerun-receipt.md",
            "reports/reviewer-rerun-receipt.json",
        ],
    },
    {
        "command": "python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt",
        "purpose": (
            "Regenerate the cold-review receipt tying the static walkthrough "
            "SVG, gallery, public demo receipt, rerun receipt, and acceptance "
            "index."
        ),
        "expected_artifacts": [
            "reports/visual-walkthrough-evidence-receipt.md",
            "reports/visual-walkthrough-evidence-receipt.json",
        ],
    },
    {
        "command": "python -m market_signal_lab.cli --reviewer-evidence-bundle",
        "purpose": "Regenerate the cold-review evidence bundle and boundary flags.",
        "expected_artifacts": [
            "reports/reviewer-evidence-bundle.md",
            "reports/reviewer-evidence-bundle.json",
        ],
    },
    {
        "command": "python -m market_signal_lab.cli --cold-user-review-route",
        "purpose": "Regenerate the first-time public review route and integrity summary.",
        "expected_artifacts": [
            "reports/cold-user-review-route.md",
            "reports/cold-user-review-route.json",
        ],
    },
    {
        "command": "python -m market_signal_lab.cli --prediction-readiness-audit",
        "purpose": "Regenerate the static thesis-ledger prediction-readiness boundary audit.",
        "expected_artifacts": [
            "reports/prediction-readiness-audit.md",
            "reports/prediction-readiness-audit.json",
        ],
    },
    {
        "command": "python -m market_signal_lab.cli --validate-thesis-ledger",
        "purpose": "Regenerate the thesis-ledger acceptance summary from checked-in JSON.",
        "expected_artifacts": [
            "reports/cross-asset-thesis-ledger-acceptance.md",
            "reports/cross-asset-thesis-ledger-acceptance.json",
        ],
    },
    {
        "command": "python scripts/selfcheck.py",
        "purpose": (
            "Regenerate and validate the full checked-in sample artifact set "
            "used by repository reviewers."
        ),
        "expected_artifacts": [
            "checked-in sample artifacts declared by "
            "scripts/selfcheck.py::SAMPLE_ARTIFACTS"
        ],
    },
    {
        "command": "python -m pytest",
        "purpose": "Run the repository test suite for reproducibility.",
        "expected_artifacts": [],
    },
)

EXPECTED_ARTIFACTS = (
    {
        "path": "reports/reviewer-rerun-receipt.md",
        "format": "markdown",
        "source_command": "python -m market_signal_lab.cli --reviewer-rerun-receipt",
    },
    {
        "path": "reports/reviewer-rerun-receipt.json",
        "format": "json",
        "source_command": "python -m market_signal_lab.cli --reviewer-rerun-receipt",
    },
    {
        "path": "reports/visual-walkthrough-evidence-receipt.md",
        "format": "markdown",
        "source_command": "python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt",
    },
    {
        "path": "reports/visual-walkthrough-evidence-receipt.json",
        "format": "json",
        "source_command": "python -m market_signal_lab.cli --visual-walkthrough-evidence-receipt",
    },
    {
        "path": "reports/reviewer-evidence-bundle.md",
        "format": "markdown",
        "source_command": "python -m market_signal_lab.cli --reviewer-evidence-bundle",
    },
    {
        "path": "reports/reviewer-evidence-bundle.json",
        "format": "json",
        "source_command": "python -m market_signal_lab.cli --reviewer-evidence-bundle",
    },
    {
        "path": "reports/cold-user-review-route.md",
        "format": "markdown",
        "source_command": "python -m market_signal_lab.cli --cold-user-review-route",
    },
    {
        "path": "reports/cold-user-review-route.json",
        "format": "json",
        "source_command": "python -m market_signal_lab.cli --cold-user-review-route",
    },
    {
        "path": "reports/prediction-readiness-audit.md",
        "format": "markdown",
        "source_command": "python -m market_signal_lab.cli --prediction-readiness-audit",
    },
    {
        "path": "reports/prediction-readiness-audit.json",
        "format": "json",
        "source_command": "python -m market_signal_lab.cli --prediction-readiness-audit",
    },
    {
        "path": "reports/cross-asset-thesis-ledger-acceptance.md",
        "format": "markdown",
        "source_command": "python -m market_signal_lab.cli --validate-thesis-ledger",
    },
    {
        "path": "reports/cross-asset-thesis-ledger-acceptance.json",
        "format": "json",
        "source_command": "python -m market_signal_lab.cli --validate-thesis-ledger",
    },
)

CHECKLIST = (
    {
        "status": "PASS",
        "check": "Receipt generation is deterministic",
        "note": "The receipt is built from fixed stdlib-only constants and does not read market data; PASS is a static receipt claim, not evidence that commands were executed.",
    },
    {
        "status": "PASS",
        "check": "Public verification commands are explicit",
        "note": "Commands are listed exactly as reviewers can run them from the repository root after normal Python setup.",
    },
    {
        "status": "PASS",
        "check": "No live-data or advice workflow is included",
        "note": "The receipt declares no live data, broker, account, order, position-sizing, forecast, recommendation, or investment-advice scope.",
    },
    {
        "status": "WARN",
        "check": "Environment-dependent checks still need local execution",
        "note": "Self-check and pytest results depend on the current Python environment and are not claimed by this static receipt.",
    },
)

REVIEW_BOUNDARIES = (
    "This receipt lists public rerun commands only; it does not execute them.",
    "Run commands from the repository root after normal Python setup.",
    "A command rerun succeeds only when the command exits 0 and the listed expected artifacts are present or updated.",
    "No command fetches live market data, connects to brokers, inspects accounts, routes orders, sizes positions, forecasts returns, recommends trades, or provides investment advice.",
    "PASS means the static receipt claims the boundary or expected artifact is declared; WARN means the reviewer should still run the command locally.",
)


def build_reviewer_rerun_receipt() -> dict[str, Any]:
    """Build a deterministic public-safe reviewer rerun receipt payload."""

    return {
        "artifact_type": "reviewer_rerun_receipt",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "purpose": (
            "Give public reviewers a compact deterministic receipt containing "
            "the exact rerun commands, expected artifacts, review boundaries, "
            "and PASS/WARN checks for public reproducibility review."
        ),
        "default_outputs": {
            "markdown": "reports/reviewer-rerun-receipt.md",
            "json": "reports/reviewer-rerun-receipt.json",
        },
        "verification_commands": [
            {
                **command,
                "expected_artifacts": list(command["expected_artifacts"]),
            }
            for command in VERIFICATION_COMMANDS
        ],
        "expected_artifacts": [dict(artifact) for artifact in EXPECTED_ARTIFACTS],
        "checklist": [dict(item) for item in CHECKLIST],
        "review_boundaries": list(REVIEW_BOUNDARIES),
    }


def render_reviewer_rerun_receipt(payload: dict[str, Any]) -> str:
    """Render the reviewer rerun receipt as Markdown."""

    lines = [
        "# Reviewer Rerun Receipt",
        "",
        payload["purpose"],
        "",
        "## Start Here",
        "",
        "- Open the [public static demo](https://sergioyin.github.io/market-signal-lab/) or the local [static sample gallery](index.html), then use the Reviewer Rerun Receipt card.",
        "- Run commands from the repository root after normal Python setup.",
        "- This receipt is static; it lists commands and expected outputs but does not execute them.",
        "- Success means the command exits 0 and the listed expected artifacts are present or updated.",
        "- PASS means a static receipt claim about declared boundaries or artifact paths, not proof that a command has run.",
        "",
        "## Public Verification Commands",
        "",
    ]
    for item in payload["verification_commands"]:
        lines.extend(
            [
                f"- `{item['command']}`",
                f"  - Purpose: {item['purpose']}",
                "  - Expected artifacts: "
                + _format_expected_artifacts(item["expected_artifacts"]),
            ]
        )

    lines.extend(["", "## Expected Artifacts", ""])
    for artifact in payload["expected_artifacts"]:
        lines.append(
            f"- `{artifact['path']}` ({artifact['format']}), from "
            f"`{artifact['source_command']}`"
        )

    lines.extend(["", "## PASS/WARN Checklist", ""])
    for item in payload["checklist"]:
        lines.append(f"- **{item['status']}**: {item['check']} - {item['note']}")

    lines.extend(["", "## No-Live-Data / No-Advice Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in payload["review_boundaries"])

    lines.extend(["", "## Boundary Flags", ""])
    lines.extend(f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS)
    lines.append("")
    return "\n".join(lines)


def _format_expected_artifacts(paths: list[str]) -> str:
    if not paths:
        return "none"
    return ", ".join(f"`{path}`" for path in paths)
