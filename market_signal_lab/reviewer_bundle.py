"""Static reviewer evidence bundle for cold review handoffs."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
from typing import Any


INSPECTION_STEPS = (
    {
        "step": "open_static_gallery",
        "label": "Open the static gallery first screen",
        "path": "reports/index.html",
        "purpose": "Review checked-in Markdown/JSON/HTML artifacts before installing anything.",
    },
    {
        "step": "read_thesis_ledger_acceptance",
        "label": "Read the thesis-ledger acceptance summary",
        "path": "reports/cross-asset-thesis-ledger-acceptance.md",
        "purpose": "Confirm the cross-asset packet shape and research-boundary checks.",
    },
    {
        "step": "run_acceptance_command",
        "label": "Rerun the deterministic acceptance command",
        "command": "python -m market_signal_lab.cli --validate-thesis-ledger",
        "purpose": "Regenerate the acceptance artifacts from the checked-in JSON packet.",
    },
    {
        "step": "review_methodology_risks",
        "label": "Review methodology and leverage-risk caveats",
        "path": "docs/methodology-audit.md",
        "purpose": "Check look-ahead, survivorship, overfitting, fees/slippage, and daily-reset leveraged ETF risk.",
    },
)


BOUNDARY_FLAGS = {
    "research_only": True,
    "static_only": True,
    "no_live_data": True,
    "no_broker_or_account": True,
    "no_orders_or_position_sizing": True,
    "no_recommendations_or_forecasts": True,
}

INTEGRITY_ARTIFACT_PATHS = (
    "reports/index.html",
    "reports/cross-asset-thesis-ledger.json",
    "reports/cross-asset-thesis-ledger-acceptance.md",
    "reports/cross-asset-thesis-ledger-acceptance.json",
    "docs/methodology-audit.md",
)


def build_reviewer_evidence_bundle(
    artifact_root: Path | str = Path("."),
) -> dict[str, Any]:
    """Build a deterministic public-safe reviewer evidence bundle payload."""

    return {
        "bundle_type": "reviewer_evidence_bundle",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "primary_route": "reports/index.html -> reports/cross-asset-thesis-ledger-acceptance.md -> python -m market_signal_lab.cli --validate-thesis-ledger",
        "inspection_steps": list(INSPECTION_STEPS),
        "risk_boundaries": [
            "All metrics are historical diagnostics from bundled static/synthetic sample data.",
            "QLD_LIKE and TQQQ_LIKE examples model daily-reset leveraged ETF-like behavior; path dependency, volatility drag, and extreme drawdowns can make multi-day results differ sharply from simple 2x/3x expectations.",
            "The bundle is not a trading bot, signal service, broker workflow, order workflow, position-sizing workflow, forecast engine, recommendation, or investment advice.",
        ],
        "verification_commands": [
            "python -m market_signal_lab.cli --reviewer-evidence-bundle",
            "python -m market_signal_lab.cli --validate-thesis-ledger",
            "python scripts/selfcheck.py",
            "python -m pytest",
        ],
        "artifact_integrity_summary": build_artifact_integrity_summary(
            artifact_root,
            INTEGRITY_ARTIFACT_PATHS,
        ),
    }


def build_artifact_integrity_summary(
    artifact_root: Path | str,
    artifact_paths: tuple[str, ...] = INTEGRITY_ARTIFACT_PATHS,
) -> dict[str, Any]:
    """Return deterministic SHA-256 byte hashes for local static artifacts."""

    root = Path(artifact_root)
    artifacts = [
        _artifact_integrity_record(root, artifact_path)
        for artifact_path in artifact_paths
    ]
    status_counts = _artifact_status_counts(artifacts)
    integrity_status = _artifact_integrity_status(status_counts)
    return {
        "summary_type": "artifact_integrity_summary",
        "algorithm": "sha256",
        "scope": "local static reviewer evidence artifacts only; hashes confirm file bytes at generation time, not financial correctness",
        "integrity_status": integrity_status,
        "interpretation": _artifact_integrity_interpretation(
            integrity_status,
            status_counts,
            len(artifacts),
        ),
        "caveat": "This is a local file-byte integrity check only; it does not validate financial correctness, future performance, recommendations, or investment suitability.",
        "artifact_count": len(artifacts),
        "present_count": status_counts["present"],
        "missing_count": status_counts["missing"],
        "invalid_count": status_counts["invalid_path"],
        "artifacts": artifacts,
    }


def _artifact_status_counts(artifacts: list[dict[str, Any]]) -> dict[str, int]:
    return {
        status: sum(1 for artifact in artifacts if artifact["status"] == status)
        for status in ("present", "missing", "invalid_path")
    }


def _artifact_integrity_status(status_counts: dict[str, int]) -> str:
    if status_counts["invalid_path"] > 0:
        return "FAIL"
    if status_counts["missing"] > 0:
        return "WARN"
    return "PASS"


def _artifact_integrity_interpretation(
    integrity_status: str,
    status_counts: dict[str, int],
    artifact_count: int,
) -> str:
    if integrity_status == "FAIL":
        return (
            "FAIL: One or more configured artifact paths were rejected as unsafe, "
            "so the integrity summary is not complete until the path list is fixed."
        )
    if integrity_status == "WARN":
        return (
            "WARN: "
            f"{status_counts['present']} of {artifact_count} expected static reviewer "
            "artifacts were present and hashed; missing artifacts should be regenerated "
            "before cold review."
        )
    return (
        "PASS: All expected static reviewer artifacts were present and hashed at "
        "generation time."
    )


def _artifact_integrity_record(root: Path, artifact_path: str) -> dict[str, Any]:
    requested_path = PurePosixPath(artifact_path)
    if requested_path.is_absolute() or ".." in requested_path.parts:
        return _empty_artifact_integrity_record(
            "[invalid artifact path]",
            "invalid_path",
        )

    path = root / artifact_path
    if not path.is_file():
        return _empty_artifact_integrity_record(artifact_path, "missing")

    data = path.read_bytes()
    return {
        "path": artifact_path,
        "status": "present",
        "byte_count": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def _empty_artifact_integrity_record(path: str, status: str) -> dict[str, Any]:
    return {
        "path": path,
        "status": status,
        "byte_count": 0,
        "sha256": None,
    }


def render_reviewer_evidence_bundle(payload: dict[str, Any]) -> str:
    """Render the reviewer evidence bundle as Markdown."""

    lines = [
        "# Reviewer Evidence Bundle",
        "",
        "This bundle is a compact cold-review handoff for Market Signal Lab. It points a reviewer to the static first screen, the thesis-ledger acceptance artifact, the deterministic rerun command, and the methodology-risk caveats without adding live data, broker/account access, orders, forecasts, recommendations, or investment advice.",
        "",
        "## First-screen route",
        "",
        f"1. Open `{payload['inspection_steps'][0]['path']}` to inspect checked-in sample artifacts before installing anything.",
        f"2. Read `{payload['inspection_steps'][1]['path']}` for the current cross-asset thesis-ledger acceptance summary.",
        f"3. Rerun `{payload['inspection_steps'][2]['command']}` to regenerate the acceptance artifacts from the checked-in JSON packet.",
        f"4. Review `{payload['inspection_steps'][3]['path']}` before citing any historical diagnostic as review context.",
        "",
        "## Verification commands",
        "",
    ]
    lines.extend(f"- `{command}`" for command in payload["verification_commands"])
    integrity = payload["artifact_integrity_summary"]
    lines.extend(
        [
            "",
            "## Artifact hash summary",
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
    lines.extend(
        [
            "",
            "## Beginner risk boundaries",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in payload["risk_boundaries"])
    lines.extend(
        [
            "",
            "## Boundary flags",
            "",
            f"- research_only: `{payload['research_only']}`",
            f"- static_only: `{payload['static_only']}`",
            f"- no_live_data: `{payload['no_live_data']}`",
            f"- no_broker_or_account: `{payload['no_broker_or_account']}`",
            f"- no_orders_or_position_sizing: `{payload['no_orders_or_position_sizing']}`",
            f"- no_recommendations_or_forecasts: `{payload['no_recommendations_or_forecasts']}`",
            "",
        ]
    )
    return "\n".join(lines)
