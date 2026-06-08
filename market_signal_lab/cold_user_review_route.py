"""Cold-user review route for checked-in static artifacts."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
from typing import Any


ARTIFACT_TYPE = "cold_user_review_route"
SCHEMA_VERSION = "1.0"
SUMMARY_TYPE = "cold_user_artifact_integrity_summary"
HASH_ALGORITHM = "sha256"
STATUS_PRESENT = "present"
STATUS_MISSING = "missing"
STATUS_INVALID_PATH = "invalid_path"
STATUS_KEYS = (STATUS_PRESENT, STATUS_MISSING, STATUS_INVALID_PATH)
INVALID_ARTIFACT_PATH_LABEL = "[invalid artifact path]"
MISSING_HASH_PLACEHOLDER = "missing"

BOUNDARY_FLAG_KEYS = (
    "research_only",
    "static_only",
    "historical_diagnostics_only",
    "no_live_data",
    "no_broker_or_account",
    "no_orders_or_position_sizing",
    "no_recommendations_or_forecasts",
)
BOUNDARY_FLAGS = {key: True for key in BOUNDARY_FLAG_KEYS}

COLD_USER_REVIEW_ROUTE_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "route",
    "checklist",
    "do_not_use_for",
    "verification_commands",
    "artifact_integrity_summary",
)
COLD_USER_REVIEW_ROUTE_DEFAULT_OUTPUT_KEYS = ("markdown", "json")
COLD_USER_REVIEW_ROUTE_STEP_KEYS = (
    "step",
    "label",
    "path",
    "review_question",
    "expected_public_signal",
)
COLD_USER_REVIEW_CHECKLIST_KEYS = (
    "check",
    "label",
    "status",
    "review_note",
)

DEFAULT_OUTPUTS = {
    "markdown": "reports/cold-user-review-route.md",
    "json": "reports/cold-user-review-route.json",
}

ROUTE_STEPS = (
    {
        "step": "open_gallery",
        "label": "Open the checked-in artifact gallery",
        "path": "reports/index.html",
        "review_question": "Can a first-time reviewer find the sample artifacts without running setup?",
        "expected_public_signal": "The first screen is a local static artifact, not a live service.",
    },
    {
        "step": "read_sample_report",
        "label": "Read the sample Markdown report",
        "path": "reports/sample-report.md",
        "review_question": "Are metrics framed as historical diagnostics rather than forecasts?",
        "expected_public_signal": "The report describes a fixed historical sample and its assumptions.",
    },
    {
        "step": "check_beginner_boundary",
        "label": "Check the beginner reading boundary",
        "path": "reports/beginner-prediction-checklist.md",
        "review_question": "Does the checklist keep predictions, recommendations, and advice out of scope?",
        "expected_public_signal": "A non-expert reader gets plain scope limits before citing or sharing the artifact.",
    },
    {
        "step": "review_evidence_bundle",
        "label": "Review the public evidence handoff",
        "path": "reports/reviewer-evidence-bundle.md",
        "review_question": "Does the handoff identify static files and deterministic verification commands?",
        "expected_public_signal": "The route can be checked from local files without private context.",
    },
    {
        "step": "inspect_methodology_risks",
        "label": "Inspect methodology and risk caveats",
        "path": "docs/methodology-audit.md",
        "review_question": "Are look-ahead, fees, overfitting, and leveraged ETF risks visible?",
        "expected_public_signal": "Known research limitations are documented next to the artifacts.",
    },
)

CHECKLIST = (
    {
        "check": "static_first_screen",
        "label": "Static first screen is available",
        "status": "PASS",
        "review_note": "Start from reports/index.html and checked-in files only.",
    },
    {
        "check": "public_paths_only",
        "label": "Route uses repo-relative public paths",
        "status": "PASS",
        "review_note": "Paths are stable repo artifacts and exclude machine-specific locations.",
    },
    {
        "check": "non_advice_boundary",
        "label": "Non-advice boundary is explicit",
        "status": "PASS",
        "review_note": "Artifacts are historical research diagnostics, not recommendations or forecasts.",
    },
    {
        "check": "deterministic_verification",
        "label": "Deterministic verification commands are listed",
        "status": "PASS",
        "review_note": "Commands regenerate static review artifacts without live data or broker access.",
    },
    {
        "check": "artifact_hashes",
        "label": "Artifact byte hashes are recorded",
        "status": "PASS",
        "review_note": "Hashes identify local bytes at generation time, not financial correctness.",
    },
)

DO_NOT_USE_FOR = (
    "prediction of future returns",
    "investment advice",
    "trading recommendation",
    "live execution or signal use",
    "broker, account, or order workflow",
    "position sizing",
)
VERIFICATION_COMMANDS = (
    "python -m market_signal_lab.cli --cold-user-review-route",
    "python -m market_signal_lab.cli --reviewer-evidence-bundle",
    "python -m market_signal_lab.cli --beginner-prediction-checklist",
    "python scripts/selfcheck.py",
    "python -m pytest",
)
INTEGRITY_ARTIFACT_PATHS = tuple(step["path"] for step in ROUTE_STEPS)


def build_cold_user_review_route(
    artifact_root: Path | str = Path("."),
) -> dict[str, Any]:
    """Build a deterministic cold-user route payload for static artifacts."""

    return {
        "artifact_type": ARTIFACT_TYPE,
        "schema_version": SCHEMA_VERSION,
        **BOUNDARY_FLAGS,
        "purpose": (
            "Provide a first-time public reviewer with a deterministic route "
            "through checked-in static artifacts before running any code or "
            "citing historical diagnostics as review context."
        ),
        "default_outputs": dict(DEFAULT_OUTPUTS),
        "route": [dict(step) for step in ROUTE_STEPS],
        "checklist": [dict(item) for item in CHECKLIST],
        "do_not_use_for": list(DO_NOT_USE_FOR),
        "verification_commands": list(VERIFICATION_COMMANDS),
        "artifact_integrity_summary": build_artifact_integrity_summary(
            artifact_root,
            INTEGRITY_ARTIFACT_PATHS,
        ),
    }


def build_artifact_integrity_summary(
    artifact_root: Path | str,
    artifact_paths: tuple[str, ...] = INTEGRITY_ARTIFACT_PATHS,
) -> dict[str, Any]:
    """Return deterministic SHA-256 byte hashes for public static artifacts."""

    root = Path(artifact_root)
    artifacts = [
        _artifact_integrity_record(root, artifact_path)
        for artifact_path in artifact_paths
    ]
    status_counts = {
        status: sum(1 for artifact in artifacts if artifact["status"] == status)
        for status in STATUS_KEYS
    }
    return {
        "summary_type": SUMMARY_TYPE,
        "algorithm": HASH_ALGORITHM,
        "scope": (
            "repo-relative checked-in static artifacts only; hashes confirm "
            "local file bytes at generation time, not financial correctness"
        ),
        "integrity_status": _integrity_status(status_counts),
        "artifact_count": len(artifacts),
        "present_count": status_counts[STATUS_PRESENT],
        "missing_count": status_counts[STATUS_MISSING],
        "invalid_count": status_counts[STATUS_INVALID_PATH],
        "artifacts": artifacts,
    }


def render_cold_user_review_route(payload: dict[str, Any]) -> str:
    """Render a cold-user review route payload as Markdown."""

    integrity = payload["artifact_integrity_summary"]
    lines = [
        "# Cold-User Review Route",
        "",
        (
            "Use this deterministic route to review checked-in Market Signal "
            "Lab artifacts from a public, first-time-reader perspective. It is "
            "limited to static historical diagnostics with no live data, no "
            "broker/account access, no orders, no forecasts, no recommendations, "
            "no position sizing, and no investment advice."
        ),
        "",
        "## Route",
        "",
    ]
    for index, step in enumerate(payload["route"], start=1):
        lines.extend(
            [
                f"{index}. **{step['label']}**",
                f"   - Path: `{step['path']}`",
                f"   - Review question: {step['review_question']}",
                f"   - Expected public signal: {step['expected_public_signal']}",
            ]
        )

    lines.extend(["", "## Checklist", ""])
    for item in payload["checklist"]:
        lines.append(
            f"- **{item['label']}** (`{item['status']}`): {item['review_note']}"
        )

    lines.extend(
        [
            "",
            "## Artifact Hash Summary",
            "",
            f"- Integrity status: `{integrity['integrity_status']}`",
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
            sha256=artifact["sha256"] or MISSING_HASH_PLACEHOLDER,
        )
        for artifact in integrity["artifacts"]
    )
    lines.extend(["", "## Do Not Use This For", ""])
    lines.extend(f"- {item}" for item in payload["do_not_use_for"])
    lines.extend(["", "## Verification Commands", ""])
    lines.extend(f"- `{command}`" for command in payload["verification_commands"])
    lines.extend(["", "## Boundary Flags", ""])
    lines.extend(f"- {key}: `{payload[key]}`" for key in BOUNDARY_FLAGS)
    lines.append("")
    return "\n".join(lines)


def _artifact_integrity_record(root: Path, artifact_path: str) -> dict[str, Any]:
    requested_path = PurePosixPath(artifact_path)
    if requested_path.is_absolute() or ".." in requested_path.parts:
        return _empty_artifact_integrity_record(
            INVALID_ARTIFACT_PATH_LABEL,
            STATUS_INVALID_PATH,
        )

    path = root / artifact_path
    if not path.is_file():
        return _empty_artifact_integrity_record(artifact_path, STATUS_MISSING)

    data = path.read_bytes()
    return {
        "path": artifact_path,
        "status": STATUS_PRESENT,
        "byte_count": len(data),
        "sha256": hashlib.new(HASH_ALGORITHM, data).hexdigest(),
    }


def _empty_artifact_integrity_record(path: str, status: str) -> dict[str, Any]:
    return {
        "path": path,
        "status": status,
        "byte_count": 0,
        "sha256": None,
    }


def _integrity_status(status_counts: dict[str, int]) -> str:
    if status_counts[STATUS_INVALID_PATH]:
        return "FAIL"
    if status_counts[STATUS_MISSING]:
        return "WARN"
    return "PASS"
