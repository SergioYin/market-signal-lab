"""Deterministic public demo evidence receipt."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from market_signal_lab.reviewer_bundle import build_artifact_integrity_summary


PUBLIC_DEMO_EVIDENCE_RECEIPT_MARKDOWN_PATH = "reports/public-demo-evidence-receipt.md"
PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON_PATH = "reports/public-demo-evidence-receipt.json"
PUBLIC_DEMO_EVIDENCE_RECEIPT_COMMAND = (
    "python -m market_signal_lab.cli --public-demo-evidence-receipt"
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

EVIDENCE_ARTIFACT_PATHS = (
    "docs/static-gallery-walkthrough.svg",
    "reports/index.html",
    "reports/sample-report.md",
    "reports/sample-report.json",
    "reports/sample-report.html",
    "reports/sample-manifest.md",
    "reports/sample-sweep.md",
    "reports/sample-sweep.json",
    "reports/sample-sweep.html",
    "reports/sample-sweep-split.md",
    "reports/sample-sweep-split.json",
    "reports/sample-sweep-split.html",
    "reports/regime-comparison.md",
    "reports/regime-comparison.json",
    "reports/regime-comparison.html",
    "examples/data/sample_tqqq_qld_like.csv",
    "examples/data/sample_tqqq_qld_like.csv.provenance.json",
    "examples/data/sample_multi_regime.csv",
    "examples/data/sample_multi_regime.csv.provenance.json",
    "docs/data-provenance.md",
    "docs/artifact-gallery.md",
    "docs/static-gallery-manifest.md",
)

SOURCE_BOUNDARIES = (
    {
        "path": "examples/data/sample_tqqq_qld_like.csv",
        "provenance_path": "examples/data/sample_tqqq_qld_like.csv.provenance.json",
        "boundary": "Synthetic static OHLC fixture for deterministic report and sweep examples.",
    },
    {
        "path": "examples/data/sample_multi_regime.csv",
        "provenance_path": "examples/data/sample_multi_regime.csv.provenance.json",
        "boundary": "Synthetic static multi-regime fixture for deterministic regime-comparison examples.",
    },
)

GENERATED_ARTIFACT_GROUPS = (
    {
        "label": "Visual cold-review walkthrough",
        "paths": [
            "docs/static-gallery-walkthrough.svg",
            "reports/visual-walkthrough-evidence-receipt.md",
            "reports/visual-walkthrough-evidence-receipt.json",
        ],
        "verification": "Check the static SVG route and matching receipt before opening generated metrics.",
    },
    {
        "label": "Static gallery",
        "paths": ["reports/index.html"],
        "verification": "Open locally or from GitHub Pages; it contains no JavaScript or remote assets.",
    },
    {
        "label": "Single backtest report",
        "paths": [
            "reports/sample-report.md",
            "reports/sample-report.json",
            "reports/sample-report.html",
            "reports/sample-manifest.md",
        ],
        "verification": "Compare Markdown, JSON, HTML, and manifest paths for the same fixture-backed run.",
    },
    {
        "label": "Parameter sweep reports",
        "paths": [
            "reports/sample-sweep.md",
            "reports/sample-sweep.json",
            "reports/sample-sweep.html",
            "reports/sample-sweep-split.md",
            "reports/sample-sweep-split.json",
            "reports/sample-sweep-split.html",
        ],
        "verification": "Check ranked historical fixture diagnostics and split robustness fields without treating rankings as predictions.",
    },
    {
        "label": "Regime comparison reports",
        "paths": [
            "reports/regime-comparison.md",
            "reports/regime-comparison.json",
            "reports/regime-comparison.html",
        ],
        "verification": "Check synthetic bull, choppy, and drawdown-recovery fixture scenarios only.",
    },
)

REVIEWER_STEPS = (
    "Open docs/static-gallery-walkthrough.svg.",
    "Open reports/visual-walkthrough-evidence-receipt.md and compare it with reports/visual-walkthrough-evidence-receipt.json.",
    "Open reports/index.html.",
    "Open reports/public-demo-evidence-receipt.md and compare it with reports/public-demo-evidence-receipt.json.",
    "Check fixture provenance files next to examples/data/*.csv before reading reported metrics.",
    "Use the SHA-256 table as file-byte evidence for checked-in public artifacts only.",
    "Run python scripts/selfcheck.py for local regeneration and link/boundary checks.",
)

NOT_CLAIMED = (
    "No live market data was fetched by this receipt.",
    "No broker, account, order-routing, or position-sizing workflow is included.",
    "No report row is a recommendation, forecast, trading signal, or investment advice.",
    "Hashes prove local file-byte identity at generation time, not financial correctness or future performance.",
)


def build_public_demo_evidence_receipt(
    artifact_root: Path | str = Path("."),
) -> dict[str, Any]:
    """Build a deterministic receipt for the public static demo evidence trail."""

    return {
        "artifact_type": "public_demo_evidence_receipt",
        "schema_version": "1.0",
        **BOUNDARY_FLAGS,
        "purpose": (
            "Give cold public reviewers one deterministic receipt for checking "
            "the static gallery/backtest report artifacts, source fixture "
            "boundaries, and no-advice/no-live-data claims."
        ),
        "default_outputs": {
            "markdown": PUBLIC_DEMO_EVIDENCE_RECEIPT_MARKDOWN_PATH,
            "json": PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON_PATH,
        },
        "verification_command": PUBLIC_DEMO_EVIDENCE_RECEIPT_COMMAND,
        "reviewer_steps": list(REVIEWER_STEPS),
        "source_boundaries": [dict(boundary) for boundary in SOURCE_BOUNDARIES],
        "generated_artifact_groups": [
            {
                **group,
                "paths": list(group["paths"]),
            }
            for group in GENERATED_ARTIFACT_GROUPS
        ],
        "artifact_integrity_summary": build_artifact_integrity_summary(
            artifact_root,
            EVIDENCE_ARTIFACT_PATHS,
        ),
        "not_claimed": list(NOT_CLAIMED),
    }


def render_public_demo_evidence_receipt(payload: dict[str, Any]) -> str:
    """Render the public demo evidence receipt as Markdown."""

    integrity = payload["artifact_integrity_summary"]
    lines = [
        "# Public Demo Evidence Receipt",
        "",
        payload["purpose"],
        "",
        "## Reviewer Steps",
        "",
    ]
    lines.extend(f"{index}. {step}" for index, step in enumerate(payload["reviewer_steps"], 1))
    lines.extend(["", "## Generated Artifact Groups", ""])
    for group in payload["generated_artifact_groups"]:
        lines.append(f"- **{group['label']}**: {group['verification']}")
        lines.append(f"  - Paths: {', '.join(f'`{path}`' for path in group['paths'])}")

    lines.extend(["", "## Source Fixture Boundaries", ""])
    for boundary in payload["source_boundaries"]:
        lines.append(
            f"- `{boundary['path']}` with `{boundary['provenance_path']}`: "
            f"{boundary['boundary']}"
        )

    lines.extend(
        [
            "",
            "## Artifact Integrity Summary",
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
