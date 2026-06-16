#!/usr/bin/env python3
"""Project self-check utility."""

from __future__ import annotations

from pathlib import Path
import compileall
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from market_signal_lab.beginner_prediction_checklist import (
    BEGINNER_PREDICTION_CHECKLIST_DEFAULT_OUTPUT_KEYS,
    BEGINNER_PREDICTION_CHECKLIST_READING_STEP_KEYS,
    BEGINNER_PREDICTION_CHECKLIST_RISK_BOUNDARY_KEYS,
    BEGINNER_PREDICTION_CHECKLIST_TOP_LEVEL_KEYS,
    build_beginner_prediction_checklist,
    render_beginner_prediction_checklist,
)
from market_signal_lab.assumption_ledger_summary import (
    ASSUMPTION_ITEM_KEYS,
    ASSUMPTION_LEDGER_SUMMARY_COMMAND,
    ASSUMPTION_LEDGER_SUMMARY_JSON_PATH,
    ASSUMPTION_LEDGER_SUMMARY_MARKDOWN_PATH,
    ASSUMPTION_LEDGER_SUMMARY_TOP_LEVEL_KEYS,
    BOUNDARY_FLAGS as ASSUMPTION_LEDGER_SUMMARY_BOUNDARY_FLAGS,
    EVIDENCE_PATH_KEYS,
    NOT_CLAIMED_KEYS,
    RISK_BOUNDARY_KEYS,
    build_assumption_ledger_summary,
    render_assumption_ledger_summary,
)
from market_signal_lab.prediction_readiness_audit import (
    PREDICTION_READINESS_AUDIT_TOP_LEVEL_KEYS,
    PREDICTION_READINESS_CRITERION_KEYS,
    build_prediction_readiness_audit,
    render_prediction_readiness_audit,
)
from market_signal_lab.promotion_readiness_check import (
    PROMOTION_READINESS_CHECK_ITEM_KEYS,
    PROMOTION_READINESS_CHECK_TOP_LEVEL_KEYS,
    build_promotion_readiness_check,
    render_promotion_readiness_check,
)
from market_signal_lab.public_demo_evidence_receipt import (
    PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON_PATH,
    PUBLIC_DEMO_EVIDENCE_RECEIPT_MARKDOWN_PATH,
    build_public_demo_evidence_receipt,
    render_public_demo_evidence_receipt,
)
from market_signal_lab.reviewer_acceptance_scorecard import (
    build_reviewer_acceptance_scorecard,
    render_reviewer_acceptance_scorecard,
)
from market_signal_lab.reviewer_bundle import (
    build_reviewer_evidence_bundle,
    render_reviewer_evidence_bundle,
)
from market_signal_lab.reviewer_rerun_receipt import (
    BOUNDARY_FLAGS as REVIEWER_RERUN_RECEIPT_BOUNDARY_FLAGS,
    CHECKLIST_KEYS,
    EXPECTED_ARTIFACTS,
    EXPECTED_ARTIFACT_KEYS,
    REVIEWER_RERUN_RECEIPT_TOP_LEVEL_KEYS,
    VERIFICATION_COMMANDS,
    VERIFICATION_COMMAND_KEYS,
    build_reviewer_rerun_receipt,
    render_reviewer_rerun_receipt,
)
from market_signal_lab.strategy_assumption_stress_kit import (
    ASSUMPTION_GROUP_KEYS,
    BEGINNER_RISK_BOUNDARY_KEYS as STRESS_KIT_BEGINNER_RISK_BOUNDARY_KEYS,
    BOUNDARY_FLAGS as STRATEGY_ASSUMPTION_STRESS_KIT_BOUNDARY_FLAGS,
    LEVERAGED_ETF_LIKE_CAVEAT_KEYS,
    RELEASE_READINESS_BOUNDARY_CLAIM_KEYS,
    RELEASE_READINESS_OUTPUT_PATH_KEYS,
    RELEASE_READINESS_RECEIPT_KEYS,
    RELEASE_READINESS_RERUN_COMMAND_KEYS,
    STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND,
    STRATEGY_ASSUMPTION_STRESS_KIT_FOCUSED_TEST_COMMAND,
    STRATEGY_ASSUMPTION_STRESS_KIT_HTML_ARTIFACT_LINKS,
    STRATEGY_ASSUMPTION_STRESS_KIT_HTML_PATH,
    STRATEGY_ASSUMPTION_STRESS_KIT_HTML_TITLE,
    STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH,
    STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH,
    STRATEGY_ASSUMPTION_STRESS_KIT_OUTPUT_PATHS,
    STRATEGY_ASSUMPTION_STRESS_KIT_SELF_CHECK_COMMAND,
    STRATEGY_ASSUMPTION_STRESS_KIT_TOP_LEVEL_KEYS,
    STRESS_CHECK_KEYS,
    build_strategy_assumption_stress_kit,
    render_strategy_assumption_stress_kit,
)
from market_signal_lab.stress_kit_quickstart_card import (
    QUICKSTART_BOUNDARY_FLAGS,
    QUICKSTART_COMPLETION_RECEIPT_KEYS,
    QUICKSTART_OUT_OF_SCOPE_ITEMS,
    QUICKSTART_REVIEWER_CHECKLIST_ITEM_KEYS,
    QUICKSTART_STOP_CONDITION_KEYS,
    STRESS_KIT_QUICKSTART_CARD_COMMAND,
    STRESS_KIT_QUICKSTART_CARD_JSON_PATH,
    STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH,
    STRESS_KIT_QUICKSTART_CARD_TOP_LEVEL_KEYS,
    build_stress_kit_quickstart_card,
    render_stress_kit_quickstart_card,
)
from market_signal_lab.html import render_html_report
from market_signal_lab.thesis_ledger import (
    build_cross_asset_thesis_ledger,
    render_cross_asset_thesis_ledger,
    render_thesis_ledger_acceptance_summary,
    validate_cross_asset_thesis_ledger_packet,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"
CSV_PATH = Path("examples/data/sample_tqqq_qld_like.csv")
DOC_LINK_SOURCES = (
    Path("README.md"),
    Path("docs/architecture.md"),
    Path("docs/adr/0001-static-research-artifacts.md"),
    Path("docs/index.md"),
    Path("docs/quick-tour-preview.md"),
    Path("docs/three-minute-review.md"),
    Path("docs/local-audit-commands.md"),
    Path("docs/public-share-copy.md"),
    Path("docs/reviewer-faq.md"),
    Path("docs/reviewer-decision-tree.md"),
    Path("docs/reviewer-decision-matrix.md"),
    Path("docs/promotion-readiness-check.md"),
    Path("docs/artifact-gallery.md"),
    Path("docs/cold-review-checklist.md"),
    Path("docs/config-files.md"),
    Path("docs/data-provenance.md"),
    Path("docs/example-data.md"),
    Path("docs/metric-guide.md"),
    Path("docs/methodology-audit.md"),
    Path("docs/methodology-audit-review-schema.md"),
    Path("docs/assumption-ledger-summary.md"),
    Path("docs/strategy-assumption-stress-kit.md"),
    Path("docs/scenario-risk-glossary.md"),
    Path("docs/static-gallery-manifest.md"),
    Path("docs/thesis-ledger-60-second-walkthrough.md"),
    Path("docs/split-sweep-walkthrough.md"),
    Path("docs/release-notes-v0.3.0.md"),
    Path("docs/release-notes-v0.4.0.md"),
    Path("docs/release-notes-v0.5.0.md"),
    Path("docs/release-notes-v0.6.0.md"),
    Path("docs/release-notes-v0.7.0.md"),
    Path("docs/release-notes-v0.8.0.md"),
    Path("docs/release-notes-v0.9.0.md"),
    Path("docs/release-notes-v1.0.0.md"),
    Path("docs/release-notes-v1.1.0.md"),
    Path("docs/release-notes-v1.2.0.md"),
    Path("docs/release-notes-v1.2.1.md"),
    Path("docs/release-notes-v1.3.0.md"),
    Path("docs/release-notes-v1.3.1.md"),
    Path("docs/release-notes-v1.3.2.md"),
    Path("docs/release-notes-v1.3.3.md"),
    Path("docs/release-notes-v1.3.4.md"),
    Path("docs/release-notes-v1.3.5.md"),
    Path("docs/release-notes-v1.4.0.md"),
    Path("docs/release-notes-v1.5.0.md"),
    Path("docs/release-notes-v1.6.0.md"),
    Path("docs/release-notes-v1.7.0.md"),
    Path("docs/release-notes-v1.8.0.md"),
    Path("docs/release-notes-v1.9.0.md"),
    Path("docs/release-notes-v1.9.1.md"),
    Path("docs/release-notes-v1.10.0.md"),
    Path("docs/release-notes-v1.11.0.md"),
    Path("docs/release-notes-v1.12.0.md"),
    Path("docs/release-notes-v1.13.0.md"),
    Path("docs/release-notes-v1.14.0.md"),
    Path("docs/release-notes-v1.15.0.md"),
    Path("docs/release-notes-v1.16.0.md"),
    Path("docs/release-notes-v1.17.0.md"),
    Path("docs/release-notes-v1.18.0.md"),
    Path("docs/release-notes-v1.19.0.md"),
    Path("docs/release-notes-v1.20.0.md"),
    Path("docs/release-notes-v1.20.1.md"),
    Path("docs/release-notes-v1.20.2.md"),
    Path("docs/release-notes-v1.20.3.md"),
    Path("docs/release-notes-v1.20.4.md"),
    Path("docs/release-notes-v1.21.0.md"),
    Path("docs/release-notes-v1.22.0.md"),
    Path("docs/release-notes-v1.22.1.md"),
    Path("docs/release-notes-v1.23.0.md"),
    Path("docs/release-notes-v1.27.0.md"),
    Path("docs/release-v1.26.0.md"),
    Path("docs/release-notes-v1.26.0.md"),
    Path("docs/release-v1.27.0.md"),
    Path("docs/release-v1.28.0.md"),
    Path("docs/release-v1.29.0.md"),
    Path("docs/release-v1.30.3.md"),
    Path("docs/release-v1.30.2.md"),
    Path("docs/release-v1.30.1.md"),
    Path("docs/release-v1.30.0.md"),
    Path("docs/release-v0.3.0.md"),
    Path("docs/release-v0.4.0.md"),
    Path("docs/release-v0.5.0.md"),
    Path("docs/release-v0.6.0.md"),
    Path("docs/release-v0.7.0.md"),
    Path("docs/release-v0.8.0.md"),
    Path("docs/release-v0.9.0.md"),
    Path("docs/release-v1.0.0.md"),
    Path("docs/release-v1.1.0.md"),
    Path("docs/release-v1.2.0.md"),
    Path("docs/release-v1.2.1.md"),
    Path("docs/release-v1.3.0.md"),
    Path("docs/release-v1.3.1.md"),
    Path("docs/release-v1.3.2.md"),
    Path("docs/release-v1.3.3.md"),
    Path("docs/release-v1.3.4.md"),
    Path("docs/release-v1.3.5.md"),
    Path("docs/release-v1.4.0.md"),
    Path("docs/release-v1.5.0.md"),
    Path("docs/release-v1.6.0.md"),
    Path("docs/release-v1.7.0.md"),
    Path("docs/release-v1.8.0.md"),
    Path("docs/release-v1.9.0.md"),
    Path("docs/release-v1.9.1.md"),
    Path("docs/release-v1.10.0.md"),
    Path("docs/release-v1.11.0.md"),
    Path("docs/release-v1.12.0.md"),
    Path("docs/release-v1.13.0.md"),
    Path("docs/release-v1.14.0.md"),
    Path("docs/release-v1.15.0.md"),
    Path("docs/release-v1.16.0.md"),
    Path("docs/release-v1.17.0.md"),
    Path("docs/release-v1.18.0.md"),
    Path("docs/release-v1.19.0.md"),
    Path("docs/release-v1.20.0.md"),
    Path("docs/release-v1.20.1.md"),
    Path("docs/release-v1.20.2.md"),
    Path("docs/release-v1.20.3.md"),
    Path("docs/release-v1.20.4.md"),
    Path("docs/release-v1.21.0.md"),
    Path("docs/release-v1.22.0.md"),
    Path("docs/risk-boundaries.md"),
)
FIXTURE_PROVENANCE_FILES = (
    Path("examples/data/sample_tqqq_qld_like.csv.provenance.json"),
    Path("examples/data/sample_multi_regime.csv.provenance.json"),
)
HTML_LINK_SOURCES = (
    Path("index.html"),
    Path("reports/index.html"),
    Path("reports/regime-comparison.html"),
    Path("reports/methodology-audit-score.html"),
    Path(STRATEGY_ASSUMPTION_STRESS_KIT_HTML_PATH),
)
V131_ROOT_LANDING_LINKS = (
    "reports/index.html",
    "docs/cold-user-evidence-card.md",
    "docs/index.md",
    "README.md",
    "docs/static-gallery-manifest.md",
    "docs/static-gallery-walkthrough.svg",
    "docs/quick-tour-preview.md",
    "docs/quick-tour-preview.svg",
    "docs/thesis-ledger-60-second-walkthrough.md",
    "docs/artifact-gallery.md",
    "docs/split-sweep-walkthrough.md",
    "docs/risk-boundaries.md",
    "docs/data-provenance.md",
    "docs/methodology-audit-review-schema.md",
    "docs/assumption-ledger-summary.md",
    "docs/architecture.md",
    "docs/adr/0001-static-research-artifacts.md",
    "docs/three-minute-review.md",
    "docs/local-audit-commands.md",
    "docs/public-share-copy.md",
    "docs/reviewer-decision-tree.md",
    "reports/reviewer-evidence-bundle.md",
    "reports/public-demo-evidence-receipt.md",
    "reports/reviewer-rerun-receipt.md",
    "reports/reviewer-acceptance-scorecard.md",
    "reports/stress-kit-quickstart-card.md",
    "reports/stress-kit-quickstart-card.json",
    "reports/assumption-ledger-summary.md",
    "reports/assumption-ledger-summary.json",
    "reports/beginner-prediction-checklist.md",
    "docs/release-v1.30.3.md",
    "docs/release-v1.30.2.md",
    "docs/release-v1.30.1.md",
    "docs/release-v1.30.0.md",
    "docs/release-v1.29.0.md",
    "docs/release-v1.28.0.md",
    "docs/release-v1.26.0.md",
    "docs/release-notes-v1.26.0.md",
    "docs/release-v1.27.0.md",
    "docs/release-notes-v1.23.0.md",
    "docs/release-notes-v1.22.1.md",
    "docs/release-notes-v1.22.0.md",
    "docs/release-v1.22.0.md",
    "docs/release-notes-v1.21.0.md",
    "docs/release-v1.21.0.md",
    "docs/release-notes-v1.20.4.md",
    "docs/release-v1.20.4.md",
    "docs/release-notes-v1.20.3.md",
    "docs/release-v1.20.3.md",
    "docs/release-notes-v1.20.2.md",
    "docs/release-v1.20.2.md",
    "docs/release-notes-v1.20.1.md",
    "docs/release-v1.20.1.md",
    "docs/release-notes-v1.20.0.md",
    "docs/release-v1.20.0.md",
    "docs/release-notes-v1.19.0.md",
    "docs/release-v1.19.0.md",
    "docs/release-notes-v1.18.0.md",
    "docs/release-v1.18.0.md",
    "docs/release-notes-v1.17.0.md",
    "docs/release-v1.17.0.md",
    "docs/release-notes-v1.16.0.md",
    "docs/release-v1.16.0.md",
    "docs/release-notes-v1.15.0.md",
    "docs/release-v1.15.0.md",
    "docs/release-notes-v1.14.0.md",
    "docs/release-v1.14.0.md",
    "docs/release-notes-v1.13.0.md",
    "docs/release-v1.13.0.md",
    "docs/release-notes-v1.12.0.md",
    "docs/release-v1.12.0.md",
    "docs/release-notes-v1.11.0.md",
    "docs/release-v1.11.0.md",
    "docs/release-notes-v1.10.0.md",
    "docs/release-v1.10.0.md",
    "docs/release-notes-v1.9.1.md",
    "docs/release-v1.9.1.md",
    "docs/release-notes-v1.9.0.md",
    "docs/release-v1.9.0.md",
    "docs/release-notes-v1.3.1.md",
    "docs/release-v1.3.1.md",
)
V090_DEMO_LINK_CONTRACT = {
    Path("docs/split-sweep-walkthrough.md"): (
        "../reports/sample-sweep-split.html",
        "../reports/sample-sweep-split.md",
        "../reports/sample-sweep-split.json",
    ),
    Path("reports/index.html"): (
        "../docs/split-sweep-walkthrough.md",
        "sample-sweep-split.html",
        "sample-sweep-split.md",
        "sample-sweep-split.json",
    ),
}
V130_STATIC_GALLERY_LINKS = (
    "../docs/artifact-gallery.md",
    "../docs/static-gallery-manifest.md",
    "../docs/static-gallery-walkthrough.svg",
    "../docs/split-sweep-walkthrough.md",
    "sample-manifest.md",
    "sample-report.html",
    "sample-report.md",
    "sample-report.json",
    "pretrade-packet.md",
    "pretrade-packet.json",
    "scenario-card.md",
    "scenario-card.json",
    "methodology-audit-score.html",
    "methodology-audit-score.md",
    "methodology-audit-score.json",
    "fee-sensitivity.md",
    "fee-sensitivity.json",
    "cross-asset-thesis-ledger.md",
    "cross-asset-thesis-ledger.json",
    "reviewer-evidence-bundle.md",
    "reviewer-evidence-bundle.json",
    "public-demo-evidence-receipt.md",
    "public-demo-evidence-receipt.json",
    "reviewer-rerun-receipt.md",
    "reviewer-rerun-receipt.json",
    "reviewer-acceptance-scorecard.md",
    "reviewer-acceptance-scorecard.json",
    "reviewer-decision-matrix.md",
    "reviewer-decision-matrix.json",
    "promotion-readiness-check.md",
    "promotion-readiness-check.json",
    "strategy-assumption-stress-kit.md",
    "strategy-assumption-stress-kit.json",
    "strategy-assumption-stress-kit.html",
    "stress-kit-quickstart-card.md",
    "stress-kit-quickstart-card.json",
    "assumption-ledger-summary.md",
    "assumption-ledger-summary.json",
    "cold-user-review-route.md",
    "cold-user-review-route.json",
    "beginner-prediction-checklist.md",
    "beginner-prediction-checklist.json",
    "prediction-readiness-audit.md",
    "prediction-readiness-audit.json",
    "regime-comparison.html",
    "regime-comparison.md",
    "regime-comparison.json",
    "sample-sweep.html",
    "sample-sweep.md",
    "sample-sweep.json",
    "sample-sweep-split.html",
    "sample-sweep-split.md",
    "sample-sweep-split.json",
)
V130_STATIC_GALLERY_REQUIRED_TEXT = (
    "Scenario/Risk Interpretation",
    "scenario_risk_interpretation",
)
V160_STATIC_PRIMARY_ACTIONS = {
    "sample-report": ("View sample report", "sample-report.html"),
    "beginner-checklist": (
        "Beginner backtest checklist",
        "beginner-prediction-checklist.md",
    ),
    "prediction-readiness-audit": (
        "Prediction-readiness audit",
        "prediction-readiness-audit.md",
    ),
    "verification-command": ("Run one verification command", "#verify"),
}
V160_STATIC_GALLERY_REQUIRED_SECTIONS = (
    "Static research sample",
    "Beginner boundary",
    "Run One Verification Command",
    "What To Read First",
    "Secondary Docs And Release Links",
)
V160_STATIC_GALLERY_REQUIRED_COMMAND = (
    "python -m market_signal_lab.cli --validate-thesis-ledger"
)
REGIME_COMPARISON_HTML_REQUIRED_LINKS = (
    "regime-comparison.md",
    "regime-comparison.json",
)
REGIME_COMPARISON_HTML_REQUIRED_TEXT = (
    "<title>Regime Comparison - Market Signal Lab</title>",
    "<h1>Regime Comparison - Market Signal Lab</h1>",
    "Related Artifacts",
    "Caveats",
    "synthetic",
    "not investment advice",
    "live-trading signal",
)
V129_STRESS_KIT_QUICKSTART_ROUTE = Path("docs/release-v1.29.0.md")
V129_STRESS_KIT_QUICKSTART_REQUIRED_LINKS = (
    "../reports/stress-kit-quickstart-card.md",
    "../reports/stress-kit-quickstart-card.json",
)
V129_STRESS_KIT_QUICKSTART_REQUIRED_TEXT = (
    "static reviewer checklist only",
    "no live-data",
    "broker/account",
    "order",
    "position-sizing",
    "forecast",
    "recommendation",
    "investment-advice",
)
PRETRADE_PACKET_JSON = Path("reports/pretrade-packet.json")
PRETRADE_PACKET_MARKDOWN = Path("reports/pretrade-packet.md")
BEGINNER_PREDICTION_CHECKLIST_JSON = Path(
    "reports/beginner-prediction-checklist.json"
)
BEGINNER_PREDICTION_CHECKLIST_MARKDOWN = Path(
    "reports/beginner-prediction-checklist.md"
)
PREDICTION_READINESS_AUDIT_JSON = Path("reports/prediction-readiness-audit.json")
PREDICTION_READINESS_AUDIT_MARKDOWN = Path("reports/prediction-readiness-audit.md")
PROMOTION_READINESS_CHECK_JSON = Path("reports/promotion-readiness-check.json")
PROMOTION_READINESS_CHECK_MARKDOWN = Path("reports/promotion-readiness-check.md")
REVIEWER_RERUN_RECEIPT_JSON = Path("reports/reviewer-rerun-receipt.json")
REVIEWER_RERUN_RECEIPT_MARKDOWN = Path("reports/reviewer-rerun-receipt.md")
PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON = Path(PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON_PATH)
PUBLIC_DEMO_EVIDENCE_RECEIPT_MARKDOWN = Path(
    PUBLIC_DEMO_EVIDENCE_RECEIPT_MARKDOWN_PATH
)
STRATEGY_ASSUMPTION_STRESS_KIT_JSON = Path(
    STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH
)
STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN = Path(
    STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH
)
STRATEGY_ASSUMPTION_STRESS_KIT_HTML = Path(
    STRATEGY_ASSUMPTION_STRESS_KIT_HTML_PATH
)
STRESS_KIT_QUICKSTART_CARD_JSON = Path(STRESS_KIT_QUICKSTART_CARD_JSON_PATH)
STRESS_KIT_QUICKSTART_CARD_MARKDOWN = Path(STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH)
ASSUMPTION_LEDGER_SUMMARY_JSON = Path(ASSUMPTION_LEDGER_SUMMARY_JSON_PATH)
ASSUMPTION_LEDGER_SUMMARY_MARKDOWN = Path(ASSUMPTION_LEDGER_SUMMARY_MARKDOWN_PATH)
BEGINNER_PREDICTION_CHECKLIST_REQUIRED_SOURCES = (
    Path("reports/sample-report.md"),
    Path("reports/sample-report.json"),
    Path("reports/pretrade-packet.md"),
    Path("reports/scenario-card.md"),
    Path("docs/methodology-audit.md"),
    Path("docs/risk-boundaries.md"),
)
BEGINNER_PREDICTION_CHECKLIST_CORE_NO_ADVICE_PHRASES = (
    "predictions of future returns, recommendations, trading instructions, or investment advice",
    "not guidance about QLD, TQQQ, or any leveraged ETF",
    "No live-data workflow",
    "broker or account workflow",
    "orders or order routing, position sizing",
    "recommendation engine, forecast engine",
    "investment advice is provided",
)
PRETRADE_PACKET_TOP_LEVEL_KEYS = (
    "packet_type",
    "schema_version",
    "research_only",
    "historical_diagnostics_only",
    "no_broker_or_live_data",
    "note",
    "source",
    "strategy_config",
    "assumptions",
    "historical_diagnostics",
    "beginner_checklist",
    "risk_boundaries",
)
PRETRADE_PACKET_REQUIRED_METRICS = (
    "total_return",
    "buy_and_hold_total_return",
    "strategy_minus_buy_and_hold_return",
    "max_drawdown",
)
PRETRADE_PACKET_REQUIRED_EXPOSURE = (
    "period_count",
    "average_exposure",
    "percent_periods_in_market",
    "exposure_changes",
    "entries_to_market",
    "exits_to_cash",
    "total_fee_drag",
    "research_only",
    "note",
)
PRETRADE_PACKET_MARKDOWN_SECTIONS = (
    "# Pre-Trade Research Packet",
    "## Source",
    "## Assumptions",
    "## Historical Diagnostics",
    "## Scenario/Risk Interpretation",
    "## Beginner Checklist",
    "## Risk Boundaries",
)
SAMPLE_ARTIFACTS = (
    Path("reports/index.html"),
    Path("reports/sample-report.md"),
    Path("reports/sample-report.json"),
    Path("reports/sample-report.html"),
    Path("reports/sample-manifest.md"),
    Path("reports/pretrade-packet.md"),
    Path("reports/pretrade-packet.json"),
    Path("reports/scenario-card.md"),
    Path("reports/scenario-card.json"),
    Path("reports/methodology-audit-template.md"),
    Path("reports/methodology-audit-template.json"),
    Path("reports/methodology-audit-review-template.json"),
    Path("reports/methodology-audit-score.md"),
    Path("reports/methodology-audit-score.json"),
    Path("reports/methodology-audit-score.html"),
    Path("reports/regime-comparison.md"),
    Path("reports/regime-comparison.json"),
    Path("reports/regime-comparison.html"),
    Path("reports/sample-sweep.md"),
    Path("reports/sample-sweep.json"),
    Path("reports/sample-sweep.html"),
    Path("reports/cross-asset-thesis-ledger.md"),
    Path("reports/cross-asset-thesis-ledger.json"),
    Path("reports/cross-asset-thesis-ledger-acceptance.md"),
    Path("reports/cross-asset-thesis-ledger-acceptance.json"),
    Path("reports/reviewer-evidence-bundle.md"),
    Path("reports/reviewer-evidence-bundle.json"),
    Path(PUBLIC_DEMO_EVIDENCE_RECEIPT_MARKDOWN_PATH),
    Path(PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON_PATH),
    Path("reports/reviewer-rerun-receipt.md"),
    Path("reports/reviewer-rerun-receipt.json"),
    Path("reports/reviewer-acceptance-scorecard.md"),
    Path("reports/reviewer-acceptance-scorecard.json"),
    Path("reports/reviewer-decision-matrix.md"),
    Path("reports/reviewer-decision-matrix.json"),
    Path("reports/promotion-readiness-check.md"),
    Path("reports/promotion-readiness-check.json"),
    Path(STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH),
    Path(STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH),
    Path(STRATEGY_ASSUMPTION_STRESS_KIT_HTML_PATH),
    Path(STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH),
    Path(STRESS_KIT_QUICKSTART_CARD_JSON_PATH),
    Path(ASSUMPTION_LEDGER_SUMMARY_MARKDOWN_PATH),
    Path(ASSUMPTION_LEDGER_SUMMARY_JSON_PATH),
    Path("reports/beginner-prediction-checklist.md"),
    Path("reports/beginner-prediction-checklist.json"),
    Path("reports/prediction-readiness-audit.md"),
    Path("reports/prediction-readiness-audit.json"),
    Path("reports/sample-sweep-split.md"),
    Path("reports/sample-sweep-split.json"),
    Path("reports/sample-sweep-split.html"),
    Path("reports/fee-sensitivity.md"),
    Path("reports/fee-sensitivity.json"),
)
PUBLIC_CLAIM_SOURCES = (Path("index.html"),) + DOC_LINK_SOURCES + SAMPLE_ARTIFACTS
FORBIDDEN_PUBLIC_CLAIM_RE = re.compile(
    r"\b("
    r"should\s+(buy|sell|hold|trade)|"
    r"recommend(s|ed|ing)?\s+(buying|selling|holding|trading)|"
    r"will\s+(outperform|beat\s+the\s+market|make\s+money|profit)|"
    r"guarantee(s|d)?\s+(return|profit|performance)|"
    r"live\s+trading\s+signal"
    r")\b",
    re.IGNORECASE,
)

GALLERY_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Market Signal Lab Sample Reports</title>
  <style>
    body { font-family: system-ui, sans-serif; line-height: 1.45; margin: 0; color: #1f2328; background: #ffffff; }
    main { max-width: 960px; margin: 0 auto; padding: 1.25rem; }
    h1 { font-size: 1.75rem; margin: 0 0 0.5rem; }
    h2 { font-size: 1.05rem; margin: 1.25rem 0 0.45rem; }
    p { margin: 0.45rem 0; }
    a { color: #0969da; }
    .primary-actions { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.75rem; margin: 1rem 0; }
    .primary-actions a { border: 1px solid #0969da; border-radius: 8px; padding: 0.85rem; background: #f6f8fa; color: #0969da; font-weight: 700; text-decoration: none; }
    .secondary-links { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 0.75rem; margin: 0.75rem 0; }
    .secondary-links section { border-top: 1px solid #d0d7de; padding-top: 0.65rem; }
    code, pre { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 0.9rem; }
    pre { overflow-x: auto; border: 1px solid #d0d7de; border-radius: 8px; padding: 0.85rem; background: #f6f8fa; }
    .artifact-path { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 0.85rem; color: #57606a; overflow-wrap: anywhere; }
  </style>
</head>
<body>
  <main>
    <h1>Market Signal Lab Sample Reports</h1>
    <p><strong>Static research sample:</strong> start with one readable report, one beginner checklist, and one local command. This page has no JavaScript, no external assets, no live data, no broker connection, and no trading account workflow.</p>
    <p><strong>Beginner boundary:</strong> these checked-in artifacts use synthetic sample data. They are research-only review aids, not investment advice, not recommendations, not forecasts, and not a guarantee of future returns.</p>
    <section class="primary-actions" aria-label="Primary actions">
      <a href="sample-report.html">View sample report</a>
      <a href="beginner-prediction-checklist.md">Beginner backtest checklist</a>
      <a href="prediction-readiness-audit.md">Prediction-readiness audit</a>
      <a href="#verify">Run one verification command</a>
    </section>
    <p>First-time public reviewers can follow the compact <a href="cold-user-review-route.md">Cold-user review route</a> before running code; it is an orientation path only, not advice, a forecast, or a recommendation.</p>
    <p>For stress-kit review, open the <a href="stress-kit-quickstart-card.md">Stress Kit Quickstart Card</a> first as a two-minute static/no-advice route before the full <a href="strategy-assumption-stress-kit.html">Strategy assumption stress kit</a>.</p>
    <p>Cold reviewers can also open the <a href="assumption-ledger-summary.md">Assumption Ledger Summary</a> for one compact list of strategy assumptions, risk boundaries, generated evidence paths, and explicit non-claims.</p>
    <h2 id="verify">Run One Verification Command</h2>
    <p>From the repository root, run this deterministic local check. It checks the checked-in thesis-ledger packet shape and public research boundaries; it does not validate financial correctness, profitability, or future performance.</p>
    <pre><code>python -m market_signal_lab.cli --validate-thesis-ledger</code></pre>
    <h2>What To Read First</h2>
    <p class="artifact-path">reports/sample-report.html</p>
    <p>The sample report shows Scenario/Risk Interpretation text and matching scenario_risk_interpretation JSON for one historical backtest-shaped artifact.</p>
    <p class="artifact-path">reports/beginner-prediction-checklist.md</p>
    <p>The Beginner Backtest Reading Checklist explains how to read assumptions, fees, exposure, drawdown, and caveats without treating a backtest as a prediction.</p>
    <p class="artifact-path">reports/prediction-readiness-audit.md</p>
    <p>The Prediction-readiness audit checks whether the static thesis-ledger artifact keeps historical diagnostics, non-advice boundaries, benchmark fields, fees, drawdown, exposure, train/test review questions, and leveraged ETF-like caveats visible. It is a documentation-boundary audit only, not a trading signal, order workflow, position-sizing input, forecast, recommendation, or investment-advice approval.</p>
    <p><strong>Leveraged ETF-like limits:</strong> the sample names are placeholders, and leveraged ETF products can behave in ways beginners may not expect. Daily resets make multi-day results depend on the path of daily moves; losses can grow quickly; and real funds include fund expenses, financing costs, tracking differences, taxes, liquidity, and market impact that these sample artifacts do not model.</p>
    <p><strong>Regime-comparison limits:</strong> the bull, choppy, and drawdown-recovery labels are deterministic fixture scenarios for research review and tests. They are not market classifications, recommendations, forecasts, or a guarantee of future returns.</p>
    <h2>Secondary Docs And Release Links</h2>
    <div class="secondary-links">
      <section>
        <h2>Core Artifacts</h2>
        <ul>
          <li><a href="sample-report.md">Sample report Markdown</a> and <a href="sample-report.json">JSON</a></li>
          <li><a href="pretrade-packet.md">Pre-trade packet</a> and <a href="pretrade-packet.json">JSON</a></li>
          <li><a href="scenario-card.md">Scenario card</a> and <a href="scenario-card.json">JSON</a></li>
          <li><a href="methodology-audit-score.html">Methodology audit score</a>, <a href="methodology-audit-score.md">Markdown</a>, and <a href="methodology-audit-score.json">JSON</a></li>
          <li><a href="regime-comparison.html">Regime comparison</a>, <a href="regime-comparison.md">Markdown</a>, and <a href="regime-comparison.json">JSON</a></li>
        </ul>
      </section>
      <section>
        <h2>More Samples</h2>
        <ul>
          <li><a href="fee-sensitivity.md">Fee sensitivity</a> and <a href="fee-sensitivity.json">JSON</a></li>
          <li><a href="cross-asset-thesis-ledger.md">Cross-asset thesis ledger</a> for QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE, plus <a href="cross-asset-thesis-ledger.json">JSON</a></li>
          <li><a href="reviewer-evidence-bundle.md">Reviewer evidence bundle</a> and <a href="reviewer-evidence-bundle.json">JSON</a></li>
          <li><a href="public-demo-evidence-receipt.md">Public demo evidence receipt</a> and <a href="public-demo-evidence-receipt.json">JSON</a> - deterministic artifact hashes, fixture boundaries, and no-live-data/no-advice claims</li>
          <li><a href="reviewer-rerun-receipt.md">Reviewer rerun receipt</a> and <a href="reviewer-rerun-receipt.json">JSON</a></li>
          <li><a href="reviewer-acceptance-scorecard.md">Reviewer acceptance scorecard</a> and <a href="reviewer-acceptance-scorecard.json">JSON</a></li>
          <li><a href="reviewer-decision-matrix.md">Reviewer decision matrix</a> and <a href="reviewer-decision-matrix.json">JSON</a></li>
          <li><a href="promotion-readiness-check.md">Promotion-readiness check</a> and <a href="promotion-readiness-check.json">JSON</a> - release/promotion gate labels, evidence checks, PASS review notes, and WARN/FAIL next fixes</li>
          <li><a href="strategy-assumption-stress-kit.html">Strategy assumption stress kit</a>, <a href="strategy-assumption-stress-kit.md">Markdown release-readiness receipt</a>, and <a href="strategy-assumption-stress-kit.json">JSON receipt</a></li>
          <li><a href="stress-kit-quickstart-card.md">Stress Kit Quickstart Card</a> and <a href="stress-kit-quickstart-card.json">JSON</a> - two-minute static/no-advice route before the full stress kit</li>
          <li><a href="assumption-ledger-summary.md">Assumption ledger summary</a> and <a href="assumption-ledger-summary.json">JSON</a> - compact assumptions, risk boundaries, evidence paths, and non-claims</li>
          <li><a href="cold-user-review-route.md">Cold-user review route</a> and <a href="cold-user-review-route.json">JSON</a></li>
          <li><a href="prediction-readiness-audit.md">Prediction-readiness audit</a> and <a href="prediction-readiness-audit.json">JSON</a></li>
          <li><a href="beginner-prediction-checklist.json">Beginner checklist JSON</a></li>
          <li><a href="sample-sweep-split.html">Split sweep</a>, <a href="sample-sweep-split.md">Markdown</a>, and <a href="sample-sweep-split.json">JSON</a></li>
          <li><a href="sample-sweep.html">Parameter sweep</a>, <a href="sample-sweep.md">Markdown</a>, and <a href="sample-sweep.json">JSON</a></li>
          <li><a href="sample-manifest.md">Sample manifest</a></li>
        </ul>
      </section>
      <section>
        <h2>Docs And Releases</h2>
        <ul>
          <li><a href="../docs/artifact-gallery.md">Artifact gallery notes</a></li>
          <li><a href="../docs/static-gallery-manifest.md">Static demo manifest</a></li>
          <li><a href="../docs/static-gallery-walkthrough.svg">Static gallery walkthrough</a></li>
          <li><a href="../docs/split-sweep-walkthrough.md">Split-sweep walkthrough</a></li>
          <li><a href="../docs/local-audit-commands.md">Local audit commands</a></li>
          <li><a href="../docs/release-v1.30.3.md">v1.30.3 release notes</a></li>
          <li><a href="../docs/release-v1.30.2.md">v1.30.2 release notes</a></li>
          <li><a href="../docs/release-v1.30.1.md">v1.30.1 release notes</a></li>
          <li><a href="../docs/release-v1.30.0.md">v1.30.0 release notes</a></li>
          <li><a href="../docs/release-v1.29.0.md">v1.29.0 release notes</a></li>
          <li><a href="../docs/release-v1.28.0.md">v1.28.0 release notes</a></li>
          <li><a href="../docs/release-v1.27.0.md">v1.27.0 release notes</a></li>
          <li><a href="../docs/release-v1.26.0.md">v1.26.0 release notes</a></li>
          <li><a href="../docs/release-notes-v1.26.0.md">v1.26.0 release docs</a></li>
          <li><a href="../docs/release-v1.25.0.md">v1.25.0 release notes</a></li>
          <li><a href="../docs/release-notes-v1.24.0.md">v1.24.0 release notes</a></li>
        </ul>
      </section>
    </div>
  </main>
</body>
</html>
"""



MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_HREF_RE = re.compile(r"\bhref\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
HTML_PRIMARY_ACTIONS_SECTION_RE = re.compile(
    r"<section\b(?=[^>]*\bclass\s*=\s*[\"'][^\"']*\bprimary-actions\b[^\"']*[\"'])"
    r"[^>]*>(.*?)</section>",
    re.IGNORECASE | re.DOTALL,
)
HTML_REFERENCE_ATTR_RE = re.compile(
    r"\b(?:href|src|poster)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
    re.IGNORECASE,
)
HTML_SRCSET_ATTR_RE = re.compile(
    r"\bsrcset\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
    re.IGNORECASE,
)
FENCED_BLOCK_RE = re.compile(r"(^|\n)```.*?(\n```|$)", re.DOTALL)


def run_compileall() -> bool:
    print("1) Running Python compilation check...")
    ok = compileall.compile_dir(str(REPO_ROOT / "market_signal_lab"), quiet=1)
    ok &= compileall.compile_dir(str(REPO_ROOT / "tests"), quiet=1)
    return bool(ok)


def run_pytest() -> bool:
    print("2) Running pytest, excluding wheel smoke...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-m", "not wheel_smoke"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("pytest failed")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return False
    return True


def run_docs_link_check() -> bool:
    print("4) Checking documentation and gallery links...")
    issues = [
        *find_markdown_link_issues(REPO_ROOT, DOC_LINK_SOURCES),
        *find_html_link_issues(REPO_ROOT, HTML_LINK_SOURCES),
    ]
    if issues:
        print("Documentation/gallery link check failed")
        for issue in issues:
            print(f"- {issue}")
        return False
    return True


def run_demo_acceptance_check() -> bool:
    print("5) Checking static demo acceptance links...")
    issues = [
        *find_v090_demo_acceptance_issues(REPO_ROOT),
        *find_v130_static_gallery_issues(REPO_ROOT),
        *find_v131_root_landing_issues(REPO_ROOT),
        *find_v160_static_dashboard_issues(REPO_ROOT),
        *find_v129_stress_kit_quickstart_route_issues(REPO_ROOT),
        *find_regime_comparison_html_issues(REPO_ROOT),
        *find_pretrade_packet_acceptance_issues(REPO_ROOT),
        *find_reviewer_rerun_receipt_issues(REPO_ROOT),
        *find_beginner_prediction_checklist_issues(REPO_ROOT),
        *find_prediction_readiness_audit_issues(REPO_ROOT),
        *find_promotion_readiness_check_issues(REPO_ROOT),
        *find_strategy_assumption_stress_kit_issues(REPO_ROOT),
        *find_stress_kit_quickstart_card_issues(REPO_ROOT),
        *find_assumption_ledger_summary_issues(REPO_ROOT),
    ]
    if issues:
        print("Static demo acceptance check failed")
        for issue in issues:
            print(f"- {issue}")
        return False
    return True


def run_public_claim_check() -> bool:
    print("6) Checking public no-advice claim boundaries...")
    issues = find_public_claim_issues(REPO_ROOT, PUBLIC_CLAIM_SOURCES)
    if issues:
        print("Public claim boundary check failed")
        for issue in issues:
            print(f"- {issue}")
        return False
    return True


def run_fixture_provenance_check() -> bool:
    print("7) Checking static fixture provenance metadata...")
    issues = find_fixture_provenance_issues(REPO_ROOT)
    if issues:
        print("Static fixture provenance check failed")
        for issue in issues:
            print(f"- {issue}")
        return False
    return True


def run_sample_artifact_generation() -> bool:
    print("3) Generating sample artifacts...")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    for command in _sample_artifact_commands():
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print("Sample artifact generation failed")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            return False

    ledger = build_cross_asset_thesis_ledger(CSV_PATH)
    (REPORTS_DIR / "cross-asset-thesis-ledger.md").write_text(
        render_cross_asset_thesis_ledger(ledger),
        encoding="utf-8",
    )
    ledger_json = json.dumps(ledger, separators=(",", ":")) + "\n"
    (REPORTS_DIR / "cross-asset-thesis-ledger.json").write_text(
        ledger_json,
        encoding="utf-8",
    )
    ledger_acceptance = validate_cross_asset_thesis_ledger_packet(ledger)
    (REPORTS_DIR / "cross-asset-thesis-ledger-acceptance.md").write_text(
        render_thesis_ledger_acceptance_summary(ledger_acceptance),
        encoding="utf-8",
    )
    (REPORTS_DIR / "cross-asset-thesis-ledger-acceptance.json").write_text(
        json.dumps(ledger_acceptance, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    prediction_readiness_audit = build_prediction_readiness_audit(
        ledger,
        "reports/cross-asset-thesis-ledger.json",
    )
    (REPORTS_DIR / "prediction-readiness-audit.md").write_text(
        render_prediction_readiness_audit(prediction_readiness_audit),
        encoding="utf-8",
    )
    (REPORTS_DIR / "prediction-readiness-audit.json").write_text(
        json.dumps(prediction_readiness_audit, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    promotion_readiness_check = build_promotion_readiness_check(
        ledger,
        "reports/cross-asset-thesis-ledger.json",
        hashlib.sha256(ledger_json.encode("utf-8")).hexdigest(),
    )
    (REPORTS_DIR / "promotion-readiness-check.md").write_text(
        render_promotion_readiness_check(promotion_readiness_check),
        encoding="utf-8",
    )
    (REPORTS_DIR / "promotion-readiness-check.json").write_text(
        json.dumps(promotion_readiness_check, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    reviewer_receipt = build_reviewer_rerun_receipt()
    (REPORTS_DIR / "reviewer-rerun-receipt.md").write_text(
        render_reviewer_rerun_receipt(reviewer_receipt),
        encoding="utf-8",
    )
    (REPORTS_DIR / "reviewer-rerun-receipt.json").write_text(
        json.dumps(reviewer_receipt, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    reviewer_acceptance_scorecard = build_reviewer_acceptance_scorecard()
    (REPORTS_DIR / "reviewer-acceptance-scorecard.md").write_text(
        render_reviewer_acceptance_scorecard(reviewer_acceptance_scorecard),
        encoding="utf-8",
    )
    (REPORTS_DIR / "reviewer-acceptance-scorecard.json").write_text(
        json.dumps(reviewer_acceptance_scorecard, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    beginner_checklist = build_beginner_prediction_checklist()
    (REPORTS_DIR / "beginner-prediction-checklist.md").write_text(
        render_beginner_prediction_checklist(beginner_checklist),
        encoding="utf-8",
    )
    (REPORTS_DIR / "beginner-prediction-checklist.json").write_text(
        json.dumps(beginner_checklist, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    stress_kit = build_strategy_assumption_stress_kit()
    (REPORTS_DIR / STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN.name).write_text(
        render_strategy_assumption_stress_kit(stress_kit),
        encoding="utf-8",
    )
    (REPORTS_DIR / STRATEGY_ASSUMPTION_STRESS_KIT_JSON.name).write_text(
        json.dumps(stress_kit, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (REPORTS_DIR / STRATEGY_ASSUMPTION_STRESS_KIT_HTML.name).write_text(
        render_html_report(
            render_strategy_assumption_stress_kit(stress_kit),
            title=STRATEGY_ASSUMPTION_STRESS_KIT_HTML_TITLE,
            artifact_links=STRATEGY_ASSUMPTION_STRESS_KIT_HTML_ARTIFACT_LINKS,
        ),
        encoding="utf-8",
    )
    quickstart_card = build_stress_kit_quickstart_card()
    (REPORTS_DIR / STRESS_KIT_QUICKSTART_CARD_MARKDOWN.name).write_text(
        render_stress_kit_quickstart_card(quickstart_card),
        encoding="utf-8",
    )
    (REPORTS_DIR / STRESS_KIT_QUICKSTART_CARD_JSON.name).write_text(
        json.dumps(quickstart_card, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    assumption_ledger_summary = build_assumption_ledger_summary()
    (REPORTS_DIR / ASSUMPTION_LEDGER_SUMMARY_MARKDOWN.name).write_text(
        render_assumption_ledger_summary(assumption_ledger_summary),
        encoding="utf-8",
    )
    (REPORTS_DIR / ASSUMPTION_LEDGER_SUMMARY_JSON.name).write_text(
        json.dumps(assumption_ledger_summary, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    (REPORTS_DIR / "index.html").write_text(GALLERY_HTML, encoding="utf-8")

    public_demo_receipt = build_public_demo_evidence_receipt(REPO_ROOT)
    (REPORTS_DIR / "public-demo-evidence-receipt.md").write_text(
        render_public_demo_evidence_receipt(public_demo_receipt),
        encoding="utf-8",
    )
    (REPORTS_DIR / "public-demo-evidence-receipt.json").write_text(
        json.dumps(public_demo_receipt, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    reviewer_bundle = build_reviewer_evidence_bundle(REPO_ROOT)
    (REPORTS_DIR / "reviewer-evidence-bundle.md").write_text(
        render_reviewer_evidence_bundle(reviewer_bundle),
        encoding="utf-8",
    )
    (REPORTS_DIR / "reviewer-evidence-bundle.json").write_text(
        json.dumps(reviewer_bundle, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    for artifact in SAMPLE_ARTIFACTS:
        path = REPO_ROOT / artifact
        if not path.exists():
            print(f"Missing sample artifact: {artifact}")
            return False
        if path.stat().st_size == 0:
            print(f"Empty sample artifact: {artifact}")
            return False

    print(
        "Created sample report gallery, report, pre-trade packet, scenario "
        "card, methodology audit artifacts, manifest, sweep, split sweep, "
        "fee sensitivity, cross-asset thesis ledger, reviewer evidence bundle, "
        "public demo evidence receipt, reviewer rerun receipt, reviewer "
        "decision matrix, beginner backtest-reading checklist, "
        "strategy assumption stress kit, stress kit quickstart card, "
        "assumption ledger summary, prediction-readiness audit, "
        "thesis-ledger acceptance, regime comparison, and HTML artifacts."
    )
    return True


def find_markdown_link_issues(
    repo_root: Path = REPO_ROOT,
    markdown_files: tuple[Path, ...] = DOC_LINK_SOURCES,
) -> list[str]:
    return find_local_link_issues(repo_root, markdown_files)


def find_html_link_issues(
    repo_root: Path = REPO_ROOT,
    html_files: tuple[Path, ...] = HTML_LINK_SOURCES,
) -> list[str]:
    return find_local_link_issues(repo_root, html_files)


def find_local_link_issues(
    repo_root: Path,
    source_files: tuple[Path, ...],
) -> list[str]:
    issues: list[str] = []
    for relative_source in source_files:
        source = repo_root / relative_source
        if not source.exists():
            issues.append(f"{relative_source}: source file is missing")
            continue

        text = source.read_text(encoding="utf-8")
        for raw_target in _raw_links_for_source(relative_source, text):
            target = _normalize_markdown_link_target(raw_target)
            if _is_external_or_anchor_only_link(target):
                continue

            link_path = _local_markdown_link_path(repo_root, source, target)
            if not link_path.exists():
                issues.append(f"{relative_source}: broken link to {raw_target}")

    return issues


def find_v090_demo_acceptance_issues(repo_root: Path = REPO_ROOT) -> list[str]:
    issues: list[str] = []
    for relative_source, required_targets in V090_DEMO_LINK_CONTRACT.items():
        source = repo_root / relative_source
        if not source.exists():
            issues.append(f"{relative_source}: source file is missing")
            continue

        text = source.read_text(encoding="utf-8")
        links = _local_links_for_source(relative_source, text)
        if relative_source.suffix == ".html" and "<script" in text.lower():
            issues.append(f"{relative_source}: static demo must not include scripts")
        if relative_source.suffix == ".html":
            for target in _html_remote_or_absolute_references(text):
                issues.append(
                    f"{relative_source}: static demo must use relative local links "
                    f"and assets, found {target}"
                )

        for target in required_targets:
            if target not in links:
                issues.append(f"{relative_source}: missing required demo link to {target}")
                continue

            link_path = _local_markdown_link_path(repo_root, source, target)
            if not link_path.exists():
                issues.append(f"{relative_source}: broken required demo link to {target}")
            elif link_path.stat().st_size == 0:
                issues.append(f"{relative_source}: required demo link target is empty: {target}")

    return issues


def find_v130_static_gallery_issues(repo_root: Path = REPO_ROOT) -> list[str]:
    relative_source = Path("reports/index.html")
    source = repo_root / relative_source
    if not source.exists():
        return [f"{relative_source}: source file is missing"]

    text = source.read_text(encoding="utf-8")
    issues: list[str] = []
    lowered = text.lower()
    if "<script" in lowered:
        issues.append(f"{relative_source}: static gallery must not include scripts")
    for target in _html_remote_or_absolute_references(text):
        issues.append(
            f"{relative_source}: static gallery must use relative local links "
            f"and assets, found {target}"
        )

    links = _local_links_for_source(relative_source, text)
    for required_text in V130_STATIC_GALLERY_REQUIRED_TEXT:
        if required_text not in text:
            issues.append(
                f"{relative_source}: missing v1.3 gallery inventory text "
                f"{required_text}"
            )
    for target in V130_STATIC_GALLERY_LINKS:
        if target not in links:
            issues.append(f"{relative_source}: missing v1.3 gallery link to {target}")
            continue
        link_path = _local_markdown_link_path(repo_root, source, target)
        if not link_path.exists():
            issues.append(f"{relative_source}: broken v1.3 gallery link to {target}")
        elif link_path.stat().st_size == 0:
            issues.append(f"{relative_source}: v1.3 gallery link target is empty: {target}")

    return issues


def find_v160_static_dashboard_issues(repo_root: Path = REPO_ROOT) -> list[str]:
    relative_source = Path("reports/index.html")
    source = repo_root / relative_source
    if not source.exists():
        return [f"{relative_source}: source file is missing"]

    text = source.read_text(encoding="utf-8")
    issues: list[str] = []
    primary_sections = HTML_PRIMARY_ACTIONS_SECTION_RE.findall(text)
    if len(primary_sections) != 1:
        issues.append(f"{relative_source}: must have one primary actions section")
    primary_section_start = re.search(
        r"<section\b(?=[^>]*\bclass\s*=\s*[\"'][^\"']*\bprimary-actions\b[^\"']*[\"'])"
        r"[^>]*>",
        text,
        re.IGNORECASE,
    )
    if not primary_section_start or not re.search(
        r'\baria-label\s*=\s*["\']Primary actions["\']',
        primary_section_start.group(0),
        re.IGNORECASE,
    ):
        issues.append(f"{relative_source}: missing primary actions landmark")
    if V160_STATIC_GALLERY_REQUIRED_COMMAND not in text:
        issues.append(f"{relative_source}: missing verification command")
    for required_text in V160_STATIC_GALLERY_REQUIRED_SECTIONS:
        if required_text not in text:
            issues.append(
                f"{relative_source}: missing simplified gallery text {required_text}"
            )

    links = _local_links_for_source(relative_source, text)
    primary_section = primary_sections[0] if len(primary_sections) == 1 else ""
    primary_links = HTML_HREF_RE.findall(primary_section)
    if len(primary_links) != 4:
        issues.append(f"{relative_source}: primary actions must contain exactly 4 links")
    for title, target in V160_STATIC_PRIMARY_ACTIONS.values():
        if title not in primary_section:
            issues.append(f"{relative_source}: missing primary action {title}")
        if target not in primary_links:
            issues.append(f"{relative_source}: missing primary action link to {target}")
            continue
        if target.startswith("#"):
            if f'id="{target[1:]}"' not in text:
                issues.append(
                    f"{relative_source}: broken primary action anchor {target}"
                )
            continue
        link_path = _local_markdown_link_path(repo_root, source, target)
        if not link_path.exists():
            issues.append(f"{relative_source}: broken primary action link to {target}")
        elif link_path.stat().st_size == 0:
            issues.append(
                f"{relative_source}: primary action link target is empty: {target}"
            )

    return issues


def find_v131_root_landing_issues(repo_root: Path = REPO_ROOT) -> list[str]:
    relative_source = Path("index.html")
    source = repo_root / relative_source
    if not source.exists():
        return [f"{relative_source}: source file is missing"]

    text = source.read_text(encoding="utf-8")
    issues: list[str] = []
    lowered = text.lower()
    if "<script" in lowered:
        issues.append(f"{relative_source}: root landing must not include scripts")
    for target in _html_remote_or_absolute_references(text):
        issues.append(
            f"{relative_source}: root landing must use relative local links "
            f"and assets, found {target}"
        )

    links = _local_links_for_source(relative_source, text)
    for target in V131_ROOT_LANDING_LINKS:
        if target not in links:
            issues.append(f"{relative_source}: missing v1.3.1 landing link to {target}")
            continue
        link_path = _local_markdown_link_path(repo_root, source, target)
        if not link_path.exists():
            issues.append(f"{relative_source}: broken v1.3.1 landing link to {target}")
        elif link_path.stat().st_size == 0:
            issues.append(f"{relative_source}: v1.3.1 landing link target is empty: {target}")

    return issues


def find_v129_stress_kit_quickstart_route_issues(
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    source = repo_root / V129_STRESS_KIT_QUICKSTART_ROUTE
    if not source.exists():
        return [f"{V129_STRESS_KIT_QUICKSTART_ROUTE}: route document is missing"]

    text = source.read_text(encoding="utf-8")
    issues: list[str] = []
    for target in V129_STRESS_KIT_QUICKSTART_REQUIRED_LINKS:
        if f"]({target})" not in text:
            issues.append(
                f"{V129_STRESS_KIT_QUICKSTART_ROUTE}: missing quickstart link {target}"
            )
        link_path = _local_markdown_link_path(repo_root, source, target)
        if not link_path.exists():
            issues.append(
                f"{V129_STRESS_KIT_QUICKSTART_ROUTE}: quickstart resource is missing {target}"
            )
        elif link_path.stat().st_size == 0:
            issues.append(
                f"{V129_STRESS_KIT_QUICKSTART_ROUTE}: quickstart resource is empty {target}"
            )

    for required_text in V129_STRESS_KIT_QUICKSTART_REQUIRED_TEXT:
        if required_text not in text:
            issues.append(
                f"{V129_STRESS_KIT_QUICKSTART_ROUTE}: missing no-advice boundary text {required_text}"
            )

    return issues


def find_regime_comparison_html_issues(repo_root: Path = REPO_ROOT) -> list[str]:
    relative_source = Path("reports/regime-comparison.html")
    source = repo_root / relative_source
    if not source.exists():
        return [f"{relative_source}: source file is missing"]

    text = source.read_text(encoding="utf-8")
    issues: list[str] = []
    lowered = text.lower()
    if "<script" in lowered:
        issues.append(f"{relative_source}: regime comparison HTML must not include scripts")
    for target in _html_remote_or_absolute_references(text):
        issues.append(
            f"{relative_source}: regime comparison HTML must use relative local "
            f"links and assets, found {target}"
        )

    links = _local_links_for_source(relative_source, text)
    for required_text in REGIME_COMPARISON_HTML_REQUIRED_TEXT:
        if required_text not in text:
            issues.append(
                f"{relative_source}: missing regime comparison HTML text "
                f"{required_text}"
            )
    for target in REGIME_COMPARISON_HTML_REQUIRED_LINKS:
        if target not in links:
            issues.append(
                f"{relative_source}: missing regime comparison HTML link to {target}"
            )
            continue
        link_path = _local_markdown_link_path(repo_root, source, target)
        if not link_path.exists():
            issues.append(
                f"{relative_source}: broken regime comparison HTML link to {target}"
            )
        elif link_path.stat().st_size == 0:
            issues.append(
                f"{relative_source}: regime comparison HTML link target is empty: {target}"
            )

    return issues


def find_pretrade_packet_acceptance_issues(repo_root: Path = REPO_ROOT) -> list[str]:
    issues: list[str] = []
    json_path = repo_root / PRETRADE_PACKET_JSON
    markdown_path = repo_root / PRETRADE_PACKET_MARKDOWN

    if not json_path.exists():
        issues.append(f"{PRETRADE_PACKET_JSON}: packet JSON is missing")
        packet: object = {}
    else:
        try:
            packet = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(f"{PRETRADE_PACKET_JSON}: invalid JSON: {exc.msg}")
            packet = {}

    if not isinstance(packet, dict):
        issues.append(f"{PRETRADE_PACKET_JSON}: packet must be a JSON object")
        packet = {}

    _extend_missing_key_issues(
        issues,
        PRETRADE_PACKET_JSON,
        packet,
        PRETRADE_PACKET_TOP_LEVEL_KEYS,
    )

    if packet.get("packet_type") != "pretrade_research_packet":
        issues.append(
            f"{PRETRADE_PACKET_JSON}: packet_type must be pretrade_research_packet"
        )
    if packet.get("schema_version") != "1.0":
        issues.append(f"{PRETRADE_PACKET_JSON}: schema_version must be 1.0")
    for key in (
        "research_only",
        "historical_diagnostics_only",
        "no_broker_or_live_data",
    ):
        if packet.get(key) is not True:
            issues.append(f"{PRETRADE_PACKET_JSON}: {key} must be true")

    note = packet.get("note")
    if not _contains_all_terms(
        note,
        ("not investment advice", "not trading guidance", "not a broker"),
    ):
        issues.append(
            f"{PRETRADE_PACKET_JSON}: note must preserve research-only non-advice wording"
        )

    source = _dict_value(packet.get("source"))
    expected_source = {
        "input_path": str(CSV_PATH),
        "first_date": "2024-01-02",
        "last_date": "2024-01-11",
        "row_count": 8,
    }
    for key, expected in expected_source.items():
        if source.get(key) != expected:
            issues.append(
                f"{PRETRADE_PACKET_JSON}: source.{key} must be {expected!r}"
            )

    strategy_config = _dict_value(packet.get("strategy_config"))
    expected_strategy = {
        "symbol": "QQQ_LIKE",
        "short_window": 20,
        "long_window": 50,
        "fee_bps": 10.0,
    }
    for key, expected in expected_strategy.items():
        if strategy_config.get(key) != expected:
            issues.append(
                f"{PRETRADE_PACKET_JSON}: strategy_config.{key} must be {expected!r}"
            )

    assumptions = packet.get("assumptions")
    if not _is_non_empty_string_list(assumptions) or len(assumptions) < 5:
        issues.append(
            f"{PRETRADE_PACKET_JSON}: assumptions must include the packet scope assumptions"
        )

    diagnostics = _dict_value(packet.get("historical_diagnostics"))
    metrics = _dict_value(diagnostics.get("metrics"))
    exposure = _dict_value(diagnostics.get("exposure_trade_review"))
    scenario = _dict_value(diagnostics.get("scenario_risk_interpretation"))
    _extend_missing_key_issues(
        issues,
        PRETRADE_PACKET_JSON,
        metrics,
        PRETRADE_PACKET_REQUIRED_METRICS,
        prefix="historical_diagnostics.metrics",
    )
    _extend_missing_key_issues(
        issues,
        PRETRADE_PACKET_JSON,
        exposure,
        PRETRADE_PACKET_REQUIRED_EXPOSURE,
        prefix="historical_diagnostics.exposure_trade_review",
    )
    if exposure.get("research_only") is not True:
        issues.append(
            f"{PRETRADE_PACKET_JSON}: historical_diagnostics.exposure_trade_review.research_only must be true"
        )
    if (
        scenario.get("research_only") is not True
        or scenario.get("historical_diagnostics_only") is not True
    ):
        issues.append(
            f"{PRETRADE_PACKET_JSON}: scenario_risk_interpretation must preserve research-only historical flags"
        )
    for key in ("exposure", "drawdown", "fee_drag", "buy_and_hold_comparison"):
        value = scenario.get(key)
        if (
            not isinstance(value, dict)
            or not isinstance(value.get("summary"), str)
            or not value["summary"].strip()
        ):
            issues.append(
                f"{PRETRADE_PACKET_JSON}: scenario_risk_interpretation.{key}.summary must be a non-empty string"
            )

    checklist = packet.get("beginner_checklist")
    if not isinstance(checklist, list) or len(checklist) < 7:
        issues.append(
            f"{PRETRADE_PACKET_JSON}: beginner_checklist must include the seven review items"
        )
    else:
        for index, item in enumerate(checklist, start=1):
            if not isinstance(item, dict):
                issues.append(
                    f"{PRETRADE_PACKET_JSON}: beginner_checklist[{index}] must be an object"
                )
                continue
            if not isinstance(item.get("item"), str) or not item["item"].strip():
                issues.append(
                    f"{PRETRADE_PACKET_JSON}: beginner_checklist[{index}].item must be a non-empty string"
                )
            if item.get("status") != "review_required":
                issues.append(
                    f"{PRETRADE_PACKET_JSON}: beginner_checklist[{index}].status must be review_required"
                )

    boundaries = _dict_value(packet.get("risk_boundaries"))
    for key in (
        "non_advice",
        "sample_backtest_limits",
        "leveraged_etf_like",
        "scope_limits",
    ):
        if not isinstance(boundaries.get(key), str) or not boundaries[key].strip():
            issues.append(
                f"{PRETRADE_PACKET_JSON}: risk_boundaries.{key} must be a non-empty string"
            )
    if not _contains_all_terms(
        boundaries.get("sample_backtest_limits"),
        ("supplied historical rows", "simplified assumptions", "future returns"),
    ):
        issues.append(
            f"{PRETRADE_PACKET_JSON}: risk_boundaries.sample_backtest_limits must preserve sample/backtest limitation wording"
        )
    if not _contains_all_terms(
        boundaries.get("leveraged_etf_like"),
        ("daily reset", "path-dependent", "losses"),
    ):
        issues.append(
            f"{PRETRADE_PACKET_JSON}: risk_boundaries.leveraged_etf_like must preserve leveraged ETF-like risk wording"
        )
    if not _contains_all_terms(
        boundaries.get("scope_limits"),
        ("no broker", "live-data", "order routing", "recommendation"),
    ):
        issues.append(
            f"{PRETRADE_PACKET_JSON}: risk_boundaries.scope_limits must preserve scope limits"
        )

    if not markdown_path.exists():
        issues.append(f"{PRETRADE_PACKET_MARKDOWN}: packet Markdown is missing")
        markdown = ""
    else:
        markdown = markdown_path.read_text(encoding="utf-8")
        if not markdown.strip():
            issues.append(f"{PRETRADE_PACKET_MARKDOWN}: packet Markdown is empty")

    for required_text in PRETRADE_PACKET_MARKDOWN_SECTIONS:
        if required_text not in markdown:
            issues.append(
                f"{PRETRADE_PACKET_MARKDOWN}: missing packet section {required_text}"
            )
    for required_text in (
        str(CSV_PATH),
        "2024-01-02 to 2024-01-11",
        "Rows reviewed**: 8",
        "Strategy minus buy-and-hold return",
        "Leveraged ETF-like boundary",
        "Scope limits",
        "not investment advice",
    ):
        if required_text not in markdown:
            issues.append(
                f"{PRETRADE_PACKET_MARKDOWN}: missing packet text {required_text}"
            )
    if markdown.count("- [ ] ") < 7:
        issues.append(
            f"{PRETRADE_PACKET_MARKDOWN}: packet Markdown must render the seven checklist items"
        )

    return issues


def find_reviewer_rerun_receipt_issues(
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    issues: list[str] = []
    json_path = repo_root / REVIEWER_RERUN_RECEIPT_JSON
    markdown_path = repo_root / REVIEWER_RERUN_RECEIPT_MARKDOWN

    if not json_path.exists():
        issues.append(f"{REVIEWER_RERUN_RECEIPT_JSON}: receipt JSON is missing")
        payload: object = {}
    else:
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                f"{REVIEWER_RERUN_RECEIPT_JSON}: invalid JSON: {exc.msg}"
            )
            payload = {}

    if not isinstance(payload, dict):
        issues.append(f"{REVIEWER_RERUN_RECEIPT_JSON}: receipt must be a JSON object")
        payload = {}

    if tuple(payload) != REVIEWER_RERUN_RECEIPT_TOP_LEVEL_KEYS:
        issues.append(
            f"{REVIEWER_RERUN_RECEIPT_JSON}: top-level keys must match "
            "the reviewer rerun receipt schema order"
        )
    if payload.get("artifact_type") != "reviewer_rerun_receipt":
        issues.append(
            f"{REVIEWER_RERUN_RECEIPT_JSON}: artifact_type must be reviewer_rerun_receipt"
        )
    if payload.get("schema_version") != "1.0":
        issues.append(f"{REVIEWER_RERUN_RECEIPT_JSON}: schema_version must be 1.0")
    for key in REVIEWER_RERUN_RECEIPT_BOUNDARY_FLAGS:
        if payload.get(key) is not True:
            issues.append(f"{REVIEWER_RERUN_RECEIPT_JSON}: {key} must be true")

    defaults = _dict_value(payload.get("default_outputs"))
    if defaults.get("markdown") != str(REVIEWER_RERUN_RECEIPT_MARKDOWN):
        issues.append(
            f"{REVIEWER_RERUN_RECEIPT_JSON}: default_outputs.markdown must be {REVIEWER_RERUN_RECEIPT_MARKDOWN}"
        )
    if defaults.get("json") != str(REVIEWER_RERUN_RECEIPT_JSON):
        issues.append(
            f"{REVIEWER_RERUN_RECEIPT_JSON}: default_outputs.json must be {REVIEWER_RERUN_RECEIPT_JSON}"
        )

    commands = payload.get("verification_commands")
    if not isinstance(commands, list) or not commands:
        issues.append(
            f"{REVIEWER_RERUN_RECEIPT_JSON}: verification_commands must be a non-empty list"
        )
    else:
        command_values = []
        for index, command in enumerate(commands):
            if not isinstance(command, dict):
                issues.append(
                    f"{REVIEWER_RERUN_RECEIPT_JSON}: verification_commands[{index}] must be an object"
                )
                continue
            if tuple(command) != VERIFICATION_COMMAND_KEYS:
                issues.append(
                    f"{REVIEWER_RERUN_RECEIPT_JSON}: verification_commands[{index}] keys must be command, purpose, expected_artifacts"
                )
            command_values.append(command.get("command"))
        for required_command in (
            command["command"] for command in VERIFICATION_COMMANDS
        ):
            if required_command not in command_values:
                issues.append(
                    f"{REVIEWER_RERUN_RECEIPT_JSON}: missing verification command {required_command}"
                )

    artifacts = payload.get("expected_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        issues.append(
            f"{REVIEWER_RERUN_RECEIPT_JSON}: expected_artifacts must be a non-empty list"
        )
    else:
        artifact_paths = []
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                issues.append(
                    f"{REVIEWER_RERUN_RECEIPT_JSON}: expected_artifacts[{index}] must be an object"
                )
                continue
            if tuple(artifact) != EXPECTED_ARTIFACT_KEYS:
                issues.append(
                    f"{REVIEWER_RERUN_RECEIPT_JSON}: expected_artifacts[{index}] keys must be path, format, source_command"
                )
            artifact_paths.append(artifact.get("path"))
        for required_path in (artifact["path"] for artifact in EXPECTED_ARTIFACTS):
            if required_path not in artifact_paths:
                issues.append(
                    f"{REVIEWER_RERUN_RECEIPT_JSON}: missing expected artifact {required_path}"
                )

    checklist = payload.get("checklist")
    if not isinstance(checklist, list) or not checklist:
        issues.append(f"{REVIEWER_RERUN_RECEIPT_JSON}: checklist must be non-empty")
    else:
        statuses = set()
        for index, item in enumerate(checklist):
            if not isinstance(item, dict):
                issues.append(
                    f"{REVIEWER_RERUN_RECEIPT_JSON}: checklist[{index}] must be an object"
                )
                continue
            if tuple(item) != CHECKLIST_KEYS:
                issues.append(
                    f"{REVIEWER_RERUN_RECEIPT_JSON}: checklist[{index}] keys must be status, check, note"
                )
            statuses.add(item.get("status"))
        if statuses != {"PASS", "WARN"}:
            issues.append(
                f"{REVIEWER_RERUN_RECEIPT_JSON}: checklist statuses must include PASS and WARN only"
            )

    if not markdown_path.exists():
        issues.append(f"{REVIEWER_RERUN_RECEIPT_MARKDOWN}: receipt Markdown is missing")
        markdown = ""
    else:
        markdown = markdown_path.read_text(encoding="utf-8")
        if not markdown.strip():
            issues.append(f"{REVIEWER_RERUN_RECEIPT_MARKDOWN}: receipt Markdown is empty")

    for required_text in (
        "# Reviewer Rerun Receipt",
        "## Public Verification Commands",
        "## Expected Artifacts",
        "## PASS/WARN Checklist",
        "## No-Live-Data / No-Advice Boundaries",
        "python -m market_signal_lab.cli --reviewer-rerun-receipt",
        "python -m market_signal_lab.cli --cold-user-review-route",
        "python -m market_signal_lab.cli --prediction-readiness-audit",
        "python scripts/selfcheck.py",
        "python -m pytest",
        "No command fetches live market data",
        "provides investment advice",
    ):
        if required_text not in markdown:
            issues.append(
                f"{REVIEWER_RERUN_RECEIPT_MARKDOWN}: missing receipt text {required_text}"
            )

    expected_payload = build_reviewer_rerun_receipt()
    if payload != expected_payload:
        issues.append(
            f"{REVIEWER_RERUN_RECEIPT_JSON}: does not match deterministic reviewer rerun receipt output; run python -m market_signal_lab.cli --reviewer-rerun-receipt"
        )
    expected_markdown = render_reviewer_rerun_receipt(expected_payload)
    if markdown and markdown != expected_markdown:
        issues.append(
            f"{REVIEWER_RERUN_RECEIPT_MARKDOWN}: does not match deterministic reviewer rerun receipt output; run python -m market_signal_lab.cli --reviewer-rerun-receipt"
        )

    return issues


def find_beginner_prediction_checklist_issues(
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    issues: list[str] = []
    json_path = repo_root / BEGINNER_PREDICTION_CHECKLIST_JSON
    markdown_path = repo_root / BEGINNER_PREDICTION_CHECKLIST_MARKDOWN

    if not json_path.exists():
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: checklist JSON is missing"
        )
        payload: object = {}
    else:
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: invalid JSON: {exc.msg}"
            )
            payload = {}

    if not isinstance(payload, dict):
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: checklist must be a JSON object"
        )
        payload = {}

    for key in BEGINNER_PREDICTION_CHECKLIST_TOP_LEVEL_KEYS:
        if key not in payload:
            issues.append(f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: missing {key}")
    if tuple(payload) != BEGINNER_PREDICTION_CHECKLIST_TOP_LEVEL_KEYS:
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: top-level keys must match "
            "the beginner prediction checklist schema order"
        )

    if payload.get("artifact_type") != "beginner_prediction_checklist":
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: artifact_type must be beginner_prediction_checklist"
        )
    if payload.get("schema_version") != "1.0":
        issues.append(f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: schema_version must be 1.0")
    for key in (
        "research_only",
        "static_only",
        "historical_diagnostics_only",
        "no_live_data",
        "no_broker_or_account",
        "no_orders_or_position_sizing",
        "no_recommendations_or_forecasts",
    ):
        if payload.get(key) is not True:
            issues.append(f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: {key} must be true")

    purpose = payload.get("purpose")
    if not _contains_all_terms(
        purpose,
        (
            "historical backtest",
            "prediction of future returns",
            "recommendation",
            "advice",
        ),
    ):
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: purpose must preserve non-prediction wording"
        )

    reuse_reason = payload.get("public_reviewer_reuse_reason")
    if not _contains_all_terms(
        reuse_reason,
        (
            "public reviewers",
            "reference this artifact",
            "deterministic",
            "static review template",
            "future-return predictions",
            "recommendations",
            "trading instructions",
            "investment advice",
        ),
    ):
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: public_reviewer_reuse_reason must explain why public reviewers can reference the artifact without weakening no-advice boundaries"
        )

    defaults = _dict_value(payload.get("default_outputs"))
    if tuple(defaults) != BEGINNER_PREDICTION_CHECKLIST_DEFAULT_OUTPUT_KEYS:
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: default_outputs keys must "
            "be markdown then json"
        )
    if defaults.get("markdown") != str(BEGINNER_PREDICTION_CHECKLIST_MARKDOWN):
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: default_outputs.markdown must be {BEGINNER_PREDICTION_CHECKLIST_MARKDOWN}"
        )
    if defaults.get("json") != str(BEGINNER_PREDICTION_CHECKLIST_JSON):
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: default_outputs.json must be {BEGINNER_PREDICTION_CHECKLIST_JSON}"
        )

    recommended_sources = payload.get("recommended_sources_to_open")
    if not _is_non_empty_string_list(recommended_sources):
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: recommended_sources_to_open must be a non-empty list of local paths"
        )
        recommended_source_paths: set[Path] = set()
    else:
        recommended_source_paths = {Path(path) for path in recommended_sources}
        for source_path in recommended_source_paths:
            if source_path.is_absolute() or _is_external_or_anchor_only_link(
                str(source_path)
            ):
                issues.append(
                    f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: recommended source must be a local relative path: {source_path}"
                )
                continue
            resolved_source = repo_root / source_path
            if not resolved_source.exists():
                issues.append(
                    f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: recommended source is missing: {source_path}"
                )
            elif resolved_source.stat().st_size == 0:
                issues.append(
                    f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: recommended source is empty: {source_path}"
                )
        for source_path in BEGINNER_PREDICTION_CHECKLIST_REQUIRED_SOURCES:
            if source_path not in recommended_source_paths:
                issues.append(
                    f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: missing recommended source {source_path}"
                )

    steps = payload.get("reading_steps")
    if not isinstance(steps, list) or len(steps) < 5:
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: reading_steps must include the beginner reading route"
        )
    else:
        for index, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                issues.append(
                    f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: reading_steps[{index}] must be an object"
                )
                continue
            if tuple(step) != BEGINNER_PREDICTION_CHECKLIST_READING_STEP_KEYS:
                issues.append(
                    f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: "
                    f"reading_steps[{index}] keys must be step, label, "
                    "beginner_note"
                )
            for key in BEGINNER_PREDICTION_CHECKLIST_READING_STEP_KEYS:
                if not isinstance(step.get(key), str) or not step[key].strip():
                    issues.append(
                        f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: reading_steps[{index}].{key} must be a non-empty string"
                    )

    do_not_use_for = payload.get("do_not_use_for")
    if not _is_non_empty_string_list(do_not_use_for):
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: do_not_use_for must be a non-empty list of boundary phrases"
        )
    else:
        for required_phrase in (
            "prediction of future returns",
            "investment advice",
            "trading recommendation",
            "live execution or signal use",
            "broker, account, or order workflow",
            "position sizing",
        ):
            if required_phrase not in do_not_use_for:
                issues.append(
                    f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: do_not_use_for must include {required_phrase}"
                )

    boundaries = _dict_value(payload.get("risk_boundaries"))
    if tuple(boundaries) != BEGINNER_PREDICTION_CHECKLIST_RISK_BOUNDARY_KEYS:
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: risk_boundaries keys must "
            "match the beginner prediction checklist schema order"
        )
    if not _contains_all_terms(
        boundaries.get("historical_backtest_limits"),
        ("supplied rows", "simplified calculations", "future returns"),
    ):
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: historical backtest limits must preserve sample/backtest wording"
        )
    if not _contains_all_terms(
        boundaries.get("leveraged_etf_daily_reset_path_dependency"),
        ("daily reset", "path-dependent", "volatility drag", "losses"),
    ):
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: leveraged ETF boundary must preserve daily-reset/path-dependency wording"
        )
    if not _contains_all_terms(
        boundaries.get("scope_limits"),
        ("no live-data", "broker", "orders", "position sizing", "forecast"),
    ):
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_JSON}: scope limits must preserve public-safe boundaries"
        )

    if not markdown_path.exists():
        issues.append(
            f"{BEGINNER_PREDICTION_CHECKLIST_MARKDOWN}: checklist Markdown is missing"
        )
        markdown = ""
    else:
        markdown = markdown_path.read_text(encoding="utf-8")
        if not markdown.strip():
            issues.append(
                f"{BEGINNER_PREDICTION_CHECKLIST_MARKDOWN}: checklist Markdown is empty"
            )

    for required_text in (
        "# Beginner Backtest Reading Checklist",
        "## Why Public Reviewers Might Reference It",
        "## How To Read A Historical Backtest",
        "## Risk Boundaries",
        "reference this artifact",
        "Leveraged ETF daily-reset and path-dependency risk",
        "predictions of future returns, recommendations, trading instructions, or investment advice",
        "no_live_data",
        "python -m market_signal_lab.cli --beginner-prediction-checklist",
    ):
        if required_text not in markdown:
            issues.append(
                f"{BEGINNER_PREDICTION_CHECKLIST_MARKDOWN}: missing checklist text {required_text}"
            )
    combined_boundary_text = "\n".join(
        str(value)
        for value in (
            purpose,
            reuse_reason,
            boundaries.get("historical_backtest_limits"),
            boundaries.get("leveraged_etf_daily_reset_path_dependency"),
            boundaries.get("scope_limits"),
            markdown,
        )
    )
    for required_phrase in BEGINNER_PREDICTION_CHECKLIST_CORE_NO_ADVICE_PHRASES:
        if required_phrase not in combined_boundary_text:
            issues.append(
                f"{BEGINNER_PREDICTION_CHECKLIST_MARKDOWN}: missing core no-advice phrase {required_phrase}"
            )

    return issues


def find_prediction_readiness_audit_issues(
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    issues: list[str] = []
    json_path = repo_root / PREDICTION_READINESS_AUDIT_JSON
    markdown_path = repo_root / PREDICTION_READINESS_AUDIT_MARKDOWN

    if not json_path.exists():
        issues.append(f"{PREDICTION_READINESS_AUDIT_JSON}: audit JSON is missing")
        payload: object = {}
    else:
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                f"{PREDICTION_READINESS_AUDIT_JSON}: invalid JSON: {exc.msg}"
            )
            payload = {}

    if not isinstance(payload, dict):
        issues.append(
            f"{PREDICTION_READINESS_AUDIT_JSON}: audit must be a JSON object"
        )
        payload = {}

    if tuple(payload) != PREDICTION_READINESS_AUDIT_TOP_LEVEL_KEYS:
        issues.append(
            f"{PREDICTION_READINESS_AUDIT_JSON}: top-level keys must match "
            "the prediction-readiness audit schema order"
        )
    if payload.get("audit_type") != "prediction_readiness_audit":
        issues.append(
            f"{PREDICTION_READINESS_AUDIT_JSON}: audit_type must be prediction_readiness_audit"
        )
    if payload.get("schema_version") != "1.0":
        issues.append(f"{PREDICTION_READINESS_AUDIT_JSON}: schema_version must be 1.0")
    for key in (
        "research_only",
        "historical_diagnostics_only",
        "not_investment_advice",
    ):
        if payload.get(key) is not True:
            issues.append(f"{PREDICTION_READINESS_AUDIT_JSON}: {key} must be true")
    if payload.get("source_artifact") != "reports/cross-asset-thesis-ledger.json":
        issues.append(
            f"{PREDICTION_READINESS_AUDIT_JSON}: source_artifact must point to reports/cross-asset-thesis-ledger.json"
        )

    summary = _dict_value(payload.get("summary"))
    if summary.get("overall_label") not in {"PASS", "WARN", "FAIL"}:
        issues.append(
            f"{PREDICTION_READINESS_AUDIT_JSON}: summary.overall_label must be PASS, WARN, or FAIL"
        )
    if not _contains_all_terms(
        summary.get("review_boundary"),
        (
            "static historical artifact",
            "not a prediction",
            "forecast",
            "recommendation",
            "trading instruction",
            "investment-advice",
        ),
    ):
        issues.append(
            f"{PREDICTION_READINESS_AUDIT_JSON}: summary.review_boundary must preserve non-prediction wording"
        )

    criteria = payload.get("criteria")
    if not isinstance(criteria, list) or len(criteria) != 6:
        issues.append(
            f"{PREDICTION_READINESS_AUDIT_JSON}: criteria must include the six prediction-readiness checks"
        )
        criteria = []
    labels: list[str] = []
    criterion_names: set[str] = set()
    for index, criterion in enumerate(criteria, start=1):
        if not isinstance(criterion, dict):
            issues.append(
                f"{PREDICTION_READINESS_AUDIT_JSON}: criteria[{index}] must be an object"
            )
            continue
        if tuple(criterion) != PREDICTION_READINESS_CRITERION_KEYS:
            issues.append(
                f"{PREDICTION_READINESS_AUDIT_JSON}: criteria[{index}] keys must be criterion, label, status, evidence, review_note"
            )
        criterion_names.add(str(criterion.get("criterion")))
        labels.append(str(criterion.get("label")))
        if criterion.get("label") not in {"PASS", "WARN", "FAIL"}:
            issues.append(
                f"{PREDICTION_READINESS_AUDIT_JSON}: criteria[{index}].label must be PASS, WARN, or FAIL"
            )
        for key in PREDICTION_READINESS_CRITERION_KEYS:
            if not isinstance(criterion.get(key), str) or not criterion[key].strip():
                issues.append(
                    f"{PREDICTION_READINESS_AUDIT_JSON}: criteria[{index}].{key} must be a non-empty string"
                )

    for required_criterion in (
        "static_data",
        "non_advice_boundary",
        "benchmark_presence",
        "fee_drawdown_exposure_presence",
        "train_test_diagnostics",
        "leveraged_etf_caveats",
    ):
        if required_criterion not in criterion_names:
            issues.append(
                f"{PREDICTION_READINESS_AUDIT_JSON}: missing criterion {required_criterion}"
            )
    if summary.get("pass_count") != labels.count("PASS"):
        issues.append(f"{PREDICTION_READINESS_AUDIT_JSON}: summary.pass_count is stale")
    if summary.get("warn_count") != labels.count("WARN"):
        issues.append(f"{PREDICTION_READINESS_AUDIT_JSON}: summary.warn_count is stale")
    if summary.get("fail_count") != labels.count("FAIL"):
        issues.append(f"{PREDICTION_READINESS_AUDIT_JSON}: summary.fail_count is stale")

    commands = payload.get("verification_commands")
    if not _is_non_empty_string_list(commands):
        issues.append(
            f"{PREDICTION_READINESS_AUDIT_JSON}: verification_commands must be a non-empty list"
        )
    else:
        for required_command in (
            "python -m market_signal_lab.cli --prediction-readiness-audit",
            "python -m market_signal_lab.cli --validate-thesis-ledger",
            "python -m pytest",
        ):
            if required_command not in commands:
                issues.append(
                    f"{PREDICTION_READINESS_AUDIT_JSON}: missing verification command {required_command}"
                )

    if not markdown_path.exists():
        issues.append(
            f"{PREDICTION_READINESS_AUDIT_MARKDOWN}: audit Markdown is missing"
        )
        markdown = ""
    else:
        markdown = markdown_path.read_text(encoding="utf-8")
        if not markdown.strip():
            issues.append(
                f"{PREDICTION_READINESS_AUDIT_MARKDOWN}: audit Markdown is empty"
            )

    for required_text in (
        "# Prediction-Readiness Audit",
        "## How to Read This",
        "## Summary",
        "## Leveraged ETF Risk Boundary",
        "## Criteria",
        "## Evidence Notes",
        "## Verification Commands",
        "not as a market outlook, action cue, or position-sizing input",
        "Daily reset and compounding can make multi-day results path-dependent",
        "python -m market_signal_lab.cli --prediction-readiness-audit",
    ):
        if required_text not in markdown:
            issues.append(
                f"{PREDICTION_READINESS_AUDIT_MARKDOWN}: missing audit text {required_text}"
            )

    return issues


def find_promotion_readiness_check_issues(
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    issues: list[str] = []
    json_path = repo_root / PROMOTION_READINESS_CHECK_JSON
    markdown_path = repo_root / PROMOTION_READINESS_CHECK_MARKDOWN
    ledger_path = repo_root / Path("reports/cross-asset-thesis-ledger.json")

    if not json_path.exists():
        issues.append(f"{PROMOTION_READINESS_CHECK_JSON}: check JSON is missing")
        payload: object = {}
    else:
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                f"{PROMOTION_READINESS_CHECK_JSON}: invalid JSON: {exc.msg}"
            )
            payload = {}

    if not isinstance(payload, dict):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: check must be a JSON object"
        )
        payload = {}

    if tuple(payload) != PROMOTION_READINESS_CHECK_TOP_LEVEL_KEYS:
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: top-level keys must match "
            "the promotion-readiness check schema order"
        )
    if payload.get("artifact_type") != "promotion_readiness_check":
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: artifact_type must be promotion_readiness_check"
        )
    if payload.get("schema_version") != "1.0":
        issues.append(f"{PROMOTION_READINESS_CHECK_JSON}: schema_version must be 1.0")
    for key in (
        "research_only",
        "static_only",
        "historical_diagnostics_only",
        "no_live_data",
        "no_broker_or_account",
        "no_orders_or_position_sizing",
        "no_recommendations_or_forecasts",
        "not_investment_advice",
    ):
        if payload.get(key) is not True:
            issues.append(f"{PROMOTION_READINESS_CHECK_JSON}: {key} must be true")
    if payload.get("source_artifact") != "reports/cross-asset-thesis-ledger.json":
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: source_artifact must point to reports/cross-asset-thesis-ledger.json"
        )
    source_content_sha256 = payload.get("source_content_sha256")
    if not isinstance(source_content_sha256, str) or not re.fullmatch(
        r"[0-9a-f]{64}",
        source_content_sha256,
    ):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: source_content_sha256 must be a lowercase sha256 hex digest"
        )
    if payload.get("source_artifact_role") != (
        "Repo-relative static thesis-ledger JSON path read by this check."
    ):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: source_artifact_role must describe the static input path"
        )

    defaults = _dict_value(payload.get("default_outputs"))
    if defaults.get("markdown") != str(PROMOTION_READINESS_CHECK_MARKDOWN):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: default_outputs.markdown must be {PROMOTION_READINESS_CHECK_MARKDOWN}"
        )
    if defaults.get("json") != str(PROMOTION_READINESS_CHECK_JSON):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: default_outputs.json must be {PROMOTION_READINESS_CHECK_JSON}"
        )
    if payload.get("default_outputs_role") != (
        "Repo-relative paths written by --promotion-readiness-check when "
        "output overrides are not supplied."
    ):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: default_outputs_role must describe CLI default output paths"
        )

    summary = _dict_value(payload.get("summary"))
    for key in ("release_gate", "promotion_gate"):
        if summary.get(key) not in {"PASS", "WARN", "FAIL"}:
            issues.append(
                f"{PROMOTION_READINESS_CHECK_JSON}: summary.{key} must be PASS, WARN, or FAIL"
            )
    label_meanings = _dict_value(summary.get("label_meanings"))
    for label in ("PASS", "WARN", "FAIL"):
        if not isinstance(label_meanings.get(label), str) or not label_meanings[
            label
        ].strip():
            issues.append(
                f"{PROMOTION_READINESS_CHECK_JSON}: summary.label_meanings.{label} must be a non-empty string"
            )
    if summary.get("count_scope") != (
        "Counts cover the checks array and are ordered PASS/WARN/FAIL."
    ):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: summary.count_scope must define count order and scope"
        )
    if not _contains_all_terms(
        summary.get("interpretation"),
        (
            "release gate",
            "promotion gate",
            "neither gate",
            "trading readiness",
            "forecast",
            "recommendation",
            "investment advice",
        ),
    ):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: summary.interpretation must preserve gate boundary wording"
        )

    checks = payload.get("checks")
    if not isinstance(checks, list) or len(checks) != 7:
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: checks must include the seven promotion-readiness checks"
        )
        checks = []
    labels: list[str] = []
    check_names: set[str] = set()
    for index, check in enumerate(checks, start=1):
        if not isinstance(check, dict):
            issues.append(
                f"{PROMOTION_READINESS_CHECK_JSON}: checks[{index}] must be an object"
            )
            continue
        if tuple(check) != PROMOTION_READINESS_CHECK_ITEM_KEYS:
            issues.append(
                f"{PROMOTION_READINESS_CHECK_JSON}: checks[{index}] keys must be "
                f"{', '.join(PROMOTION_READINESS_CHECK_ITEM_KEYS)}"
            )
        check_names.add(str(check.get("check")))
        labels.append(str(check.get("label")))
        if check.get("label") not in {"PASS", "WARN", "FAIL"}:
            issues.append(
                f"{PROMOTION_READINESS_CHECK_JSON}: checks[{index}].label must be PASS, WARN, or FAIL"
            )
        for key in PROMOTION_READINESS_CHECK_ITEM_KEYS:
            if not isinstance(check.get(key), str) or not check[key].strip():
                issues.append(
                    f"{PROMOTION_READINESS_CHECK_JSON}: checks[{index}].{key} must be a non-empty string"
                )

    for required_check in (
        "no_live_data_boundary",
        "no_advice_boundary",
        "benchmark_evidence",
        "fee_evidence",
        "drawdown_evidence",
        "train_test_evidence",
        "leveraged_caveat_evidence",
    ):
        if required_check not in check_names:
            issues.append(
                f"{PROMOTION_READINESS_CHECK_JSON}: missing check {required_check}"
            )
    if summary.get("pass_count") != labels.count("PASS"):
        issues.append(f"{PROMOTION_READINESS_CHECK_JSON}: summary.pass_count is stale")
    if summary.get("warn_count") != labels.count("WARN"):
        issues.append(f"{PROMOTION_READINESS_CHECK_JSON}: summary.warn_count is stale")
    if summary.get("fail_count") != labels.count("FAIL"):
        issues.append(f"{PROMOTION_READINESS_CHECK_JSON}: summary.fail_count is stale")

    next_fixes = payload.get("actionable_next_fixes")
    if not isinstance(next_fixes, list) or not all(
        isinstance(fix, str) and fix.strip() for fix in next_fixes
    ):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: actionable_next_fixes must be a list of strings"
        )

    public_boundaries = payload.get("public_boundaries")
    if not _is_non_empty_string_list(public_boundaries):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: public_boundaries must be a non-empty list"
        )
    else:
        boundary_text = " ".join(public_boundaries)
        if not _contains_all_terms(
            boundary_text,
            (
                "static thesis-ledger json artifact only",
                "does not fetch live market data",
                "connect to brokers",
                "route orders",
                "position",
                "not market outlooks",
                "forecasts",
                "recommendations",
                "investment advice",
            ),
        ):
            issues.append(
                f"{PROMOTION_READINESS_CHECK_JSON}: public_boundaries must preserve no-live-data and no-advice claims"
            )

    commands = payload.get("verification_commands")
    if not _is_non_empty_string_list(commands):
        issues.append(
            f"{PROMOTION_READINESS_CHECK_JSON}: verification_commands must be a non-empty list"
        )
    else:
        for required_command in (
            "python -m market_signal_lab.cli --promotion-readiness-check",
            "python -m market_signal_lab.cli --prediction-readiness-audit",
            "python -m market_signal_lab.cli --validate-thesis-ledger",
            "python -m pytest",
        ):
            if required_command not in commands:
                issues.append(
                    f"{PROMOTION_READINESS_CHECK_JSON}: missing verification command {required_command}"
                )

    if not markdown_path.exists():
        issues.append(
            f"{PROMOTION_READINESS_CHECK_MARKDOWN}: check Markdown is missing"
        )
        markdown = ""
    else:
        markdown = markdown_path.read_text(encoding="utf-8")
        if not markdown.strip():
            issues.append(
                f"{PROMOTION_READINESS_CHECK_MARKDOWN}: check Markdown is empty"
            )

    for required_text in (
        "# Public-Promotion Readiness Check",
        "## Gate Labels",
        "## Checks",
        "## Evidence and Follow-Up",
        "## Actionable Next Fixes",
        "## Public Boundaries",
        "## Verification Commands",
        "**Release Gate**",
        "**Promotion Gate**",
        "**PASS/WARN/FAIL counts (checks array)**",
        "**Count scope**",
        "**Label meanings**",
        "**Source content SHA-256**",
        "**Default outputs**",
        "not trading readiness, a forecast, a recommendation, or investment advice",
        "No fix is listed for this PASS check; keep the evidence visible",
        "Public review/release can continue",
        "Broader promotion/citation stays on hold until resolved or explicitly disclosed",
        "does not fetch live market data",
        "PASS/WARN/FAIL labels are documentation readiness labels only",
        "python -m market_signal_lab.cli --promotion-readiness-check",
    ):
        if required_text not in markdown:
            issues.append(
                f"{PROMOTION_READINESS_CHECK_MARKDOWN}: missing check text {required_text}"
            )

    if not ledger_path.exists():
        issues.append("reports/cross-asset-thesis-ledger.json: source ledger is missing")
    else:
        ledger_bytes = ledger_path.read_bytes()
        try:
            ledger = json.loads(ledger_bytes.decode("utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                f"reports/cross-asset-thesis-ledger.json: invalid JSON: {exc.msg}"
            )
        else:
            expected_source_content_sha256 = hashlib.sha256(
                ledger_bytes
            ).hexdigest()
            if payload.get("source_content_sha256") != expected_source_content_sha256:
                issues.append(
                    f"{PROMOTION_READINESS_CHECK_JSON}: source_content_sha256 must match reports/cross-asset-thesis-ledger.json bytes"
                )
            expected_payload = build_promotion_readiness_check(
                ledger,
                "reports/cross-asset-thesis-ledger.json",
                expected_source_content_sha256,
            )
            if payload != expected_payload:
                issues.append(
                    f"{PROMOTION_READINESS_CHECK_JSON}: does not match deterministic promotion-readiness check output; run python -m market_signal_lab.cli --promotion-readiness-check"
                )
            expected_markdown = render_promotion_readiness_check(expected_payload)
            if markdown and markdown != expected_markdown:
                issues.append(
                    f"{PROMOTION_READINESS_CHECK_MARKDOWN}: does not match deterministic promotion-readiness check output; run python -m market_signal_lab.cli --promotion-readiness-check"
                )

    return issues


def find_strategy_assumption_stress_kit_issues(
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    issues: list[str] = []
    json_path = repo_root / STRATEGY_ASSUMPTION_STRESS_KIT_JSON
    markdown_path = repo_root / STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN
    html_path = repo_root / STRATEGY_ASSUMPTION_STRESS_KIT_HTML

    if not json_path.exists():
        issues.append(f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: kit JSON is missing")
        payload: object = {}
    else:
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: invalid JSON: {exc.msg}"
            )
            payload = {}

    if not isinstance(payload, dict):
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: kit must be a JSON object"
        )
        payload = {}

    if tuple(payload) != STRATEGY_ASSUMPTION_STRESS_KIT_TOP_LEVEL_KEYS:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: top-level keys must match "
            "the strategy assumption stress kit schema order"
        )
    if payload.get("artifact_type") != "strategy_assumption_stress_kit":
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: artifact_type must be strategy_assumption_stress_kit"
        )
    if payload.get("schema_version") != "1.0":
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: schema_version must be 1.0"
        )
    for key in STRATEGY_ASSUMPTION_STRESS_KIT_BOUNDARY_FLAGS:
        if payload.get(key) is not True:
            issues.append(f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: {key} must be true")

    purpose = payload.get("purpose")
    if not _contains_all_terms(
        purpose,
        (
            "static checklist",
            "strategy writeup",
            "leveraged etf-like caveats",
            "forecast",
            "recommendation",
            "order workflow",
            "investment advice",
        ),
    ):
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: purpose must preserve stress-kit non-advice wording"
        )

    defaults = _dict_value(payload.get("default_outputs"))
    if defaults.get("markdown") != str(STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN):
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: default_outputs.markdown must be {STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN}"
        )
    if defaults.get("json") != str(STRATEGY_ASSUMPTION_STRESS_KIT_JSON):
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: default_outputs.json must be {STRATEGY_ASSUMPTION_STRESS_KIT_JSON}"
        )

    assumption_groups = payload.get("assumption_groups")
    if not isinstance(assumption_groups, list) or len(assumption_groups) != 4:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: assumption_groups must include the four assumption groups"
        )
        assumption_groups = []
    _extend_row_shape_issues(
        issues,
        STRATEGY_ASSUMPTION_STRESS_KIT_JSON,
        assumption_groups,
        ASSUMPTION_GROUP_KEYS,
        "assumption_groups",
    )

    stress_checks = payload.get("stress_checks")
    if not isinstance(stress_checks, list) or len(stress_checks) != 4:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: stress_checks must include the four stress checks"
        )
        stress_checks = []
    _extend_row_shape_issues(
        issues,
        STRATEGY_ASSUMPTION_STRESS_KIT_JSON,
        stress_checks,
        STRESS_CHECK_KEYS,
        "stress_checks",
    )

    risk_boundaries = payload.get("beginner_risk_boundaries")
    if not isinstance(risk_boundaries, list) or len(risk_boundaries) != 3:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: beginner_risk_boundaries must include the three beginner boundaries"
        )
        risk_boundaries = []
    _extend_row_shape_issues(
        issues,
        STRATEGY_ASSUMPTION_STRESS_KIT_JSON,
        risk_boundaries,
        STRESS_KIT_BEGINNER_RISK_BOUNDARY_KEYS,
        "beginner_risk_boundaries",
    )

    leveraged_caveats = payload.get("leveraged_etf_like_caveats")
    if not isinstance(leveraged_caveats, list) or len(leveraged_caveats) != 4:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: leveraged_etf_like_caveats must include the four leveraged ETF-like caveats"
        )
        leveraged_caveats = []
    _extend_row_shape_issues(
        issues,
        STRATEGY_ASSUMPTION_STRESS_KIT_JSON,
        leveraged_caveats,
        LEVERAGED_ETF_LIKE_CAVEAT_KEYS,
        "leveraged_etf_like_caveats",
    )

    do_not_use_for = payload.get("do_not_use_for")
    if not _is_non_empty_string_list(do_not_use_for):
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: do_not_use_for must be a non-empty list"
        )
    else:
        for required_phrase in (
            "live data workflow",
            "broker, account, or order workflow",
            "position sizing",
            "forecasting future returns",
            "trading recommendation",
            "investment advice",
        ):
            if required_phrase not in do_not_use_for:
                issues.append(
                    f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: do_not_use_for must include {required_phrase}"
                )

    receipt = payload.get("release_readiness_receipt")
    if not isinstance(receipt, dict):
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt must be an object"
        )
        receipt = {}
    elif tuple(receipt) != RELEASE_READINESS_RECEIPT_KEYS:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt keys must match the schema order"
        )
    if (
        receipt.get("receipt_type")
        != "strategy_assumption_stress_kit_release_readiness"
    ):
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.receipt_type must identify the stress-kit release receipt"
        )

    receipt_commands = receipt.get("rerun_commands")
    if not isinstance(receipt_commands, list) or len(receipt_commands) != 3:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.rerun_commands must list the three focused rerun commands"
        )
        receipt_commands = []
    for index, item in enumerate(receipt_commands):
        if not isinstance(item, dict):
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.rerun_commands[{index}] must be an object"
            )
            continue
        if tuple(item) != RELEASE_READINESS_RERUN_COMMAND_KEYS:
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.rerun_commands[{index}] keys must be "
                f"{', '.join(RELEASE_READINESS_RERUN_COMMAND_KEYS)}"
            )
        for key in ("command", "purpose"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                issues.append(
                    f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.rerun_commands[{index}].{key} must be a non-empty string"
                )
        if not isinstance(item.get("generated_output_paths"), list):
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.rerun_commands[{index}].generated_output_paths must be a list"
            )
        elif not all(
            isinstance(path, str) and path.strip()
            for path in item["generated_output_paths"]
        ):
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.rerun_commands[{index}].generated_output_paths must contain only non-empty strings"
            )
    for required_command in (
        STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND,
        STRATEGY_ASSUMPTION_STRESS_KIT_SELF_CHECK_COMMAND,
        STRATEGY_ASSUMPTION_STRESS_KIT_FOCUSED_TEST_COMMAND,
    ):
        if not any(
            isinstance(item, dict) and item.get("command") == required_command
            for item in receipt_commands
        ):
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt missing rerun command {required_command}"
            )

    receipt_outputs = receipt.get("generated_output_paths")
    if not isinstance(receipt_outputs, list) or len(receipt_outputs) != 3:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.generated_output_paths must list the three stress-kit outputs"
        )
        receipt_outputs = []
    _extend_row_shape_issues(
        issues,
        STRATEGY_ASSUMPTION_STRESS_KIT_JSON,
        receipt_outputs,
        RELEASE_READINESS_OUTPUT_PATH_KEYS,
        "release_readiness_receipt.generated_output_paths",
    )
    for required_path in STRATEGY_ASSUMPTION_STRESS_KIT_OUTPUT_PATHS:
        if not any(
            isinstance(item, dict) and item.get("path") == required_path
            for item in receipt_outputs
        ):
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt missing generated output path {required_path}"
            )

    receipt_boundaries = receipt.get("boundary_claims")
    if not isinstance(receipt_boundaries, list) or len(receipt_boundaries) != 5:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.boundary_claims must list the five public boundary claims"
        )
        receipt_boundaries = []
    _extend_row_shape_issues(
        issues,
        STRATEGY_ASSUMPTION_STRESS_KIT_JSON,
        receipt_boundaries,
        RELEASE_READINESS_BOUNDARY_CLAIM_KEYS,
        "release_readiness_receipt.boundary_claims",
    )
    for required_claim in (
        "no_live_data",
        "no_broker_or_account",
        "no_orders_or_position_sizing",
        "no_recommendations_or_forecasts",
        "not_investment_advice",
    ):
        if not any(
            isinstance(item, dict)
            and item.get("claim") == required_claim
            and item.get("status") == "PASS"
            for item in receipt_boundaries
        ):
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt missing PASS boundary claim {required_claim}"
            )

    reviewer_notes = receipt.get("reviewer_notes")
    if not _is_non_empty_string_list(reviewer_notes):
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.reviewer_notes must be a non-empty list"
        )
    else:
        for required_phrase in (
            "repository root",
            "command exits 0",
            "does not prove financial correctness",
        ):
            if not any(required_phrase in note for note in reviewer_notes):
                issues.append(
                    f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: release_readiness_receipt.reviewer_notes must mention {required_phrase}"
                )

    commands = payload.get("verification_commands")
    if not _is_non_empty_string_list(commands):
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: verification_commands must be a non-empty list"
        )
    else:
        for required_command in (
            STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND,
            STRATEGY_ASSUMPTION_STRESS_KIT_SELF_CHECK_COMMAND,
            "python -m pytest",
        ):
            if required_command not in commands:
                issues.append(
                    f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: missing verification command {required_command}"
                )

    if not markdown_path.exists():
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN}: kit Markdown is missing"
        )
        markdown = ""
    else:
        markdown = markdown_path.read_text(encoding="utf-8")
        if not markdown.strip():
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN}: kit Markdown is empty"
            )

    if not html_path.exists():
        issues.append(f"{STRATEGY_ASSUMPTION_STRESS_KIT_HTML}: kit HTML is missing")
        html = ""
    else:
        html = html_path.read_text(encoding="utf-8")
        if not html.strip():
            issues.append(f"{STRATEGY_ASSUMPTION_STRESS_KIT_HTML}: kit HTML is empty")

    for required_text in (
        f"<title>{STRATEGY_ASSUMPTION_STRESS_KIT_HTML_TITLE}</title>",
        f"<h1>{STRATEGY_ASSUMPTION_STRESS_KIT_HTML_TITLE}</h1>",
        "Related Artifacts",
        "strategy-assumption-stress-kit.md",
        "strategy-assumption-stress-kit.json",
        "not investment advice",
        "no_live_data",
        "no_broker_or_account",
        "no_orders_or_position_sizing",
        "no_recommendations_or_forecasts",
        "path_dependency",
        "volatility_drag",
        "extreme_drawdown",
        "Release-Readiness Receipt",
        "Exact Rerun Commands",
        "Generated Output Paths",
        "No-Live-Data / No-Advice Boundaries",
        *STRATEGY_ASSUMPTION_STRESS_KIT_OUTPUT_PATHS,
    ):
        if required_text not in html:
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_HTML}: missing kit HTML text {required_text}"
            )

    for required_text in (
        "# Strategy Assumption Stress Kit",
        "## What This Artifact Is",
        "## Assumptions To Stress",
        "## Stress Checks",
        "## Beginner Risk Boundaries",
        "## Leveraged ETF-Like Caveats",
        "## Do Not Use This For",
        "## Release-Readiness Receipt",
        "### Exact Rerun Commands",
        "### Generated Output Paths",
        "### No-Live-Data / No-Advice Boundaries",
        "## Boundary Flags",
        "## Verification Commands",
        "prediction, recommendation, trading instruction, order workflow, or investment advice",
        "without live market data, broker connections, account access, orders, forecasts, recommendations, or position sizing",
        "daily reset, path dependency, volatility drag, and extreme drawdown caveats",
        STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND,
        STRATEGY_ASSUMPTION_STRESS_KIT_FOCUSED_TEST_COMMAND,
        STRATEGY_ASSUMPTION_STRESS_KIT_HTML_PATH,
        "**PASS no_live_data**",
        "does not prove financial correctness",
    ):
        if required_text not in markdown:
            issues.append(
                f"{STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN}: missing kit text {required_text}"
            )

    expected_payload = build_strategy_assumption_stress_kit()
    if payload != expected_payload:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON}: does not match deterministic strategy assumption stress kit output; run {STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND}"
        )
    expected_markdown = render_strategy_assumption_stress_kit(expected_payload)
    if markdown and markdown != expected_markdown:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN}: does not match deterministic strategy assumption stress kit output; run {STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND}"
        )
    expected_html = render_html_report(
        expected_markdown,
        title=STRATEGY_ASSUMPTION_STRESS_KIT_HTML_TITLE,
        artifact_links=STRATEGY_ASSUMPTION_STRESS_KIT_HTML_ARTIFACT_LINKS,
    )
    if html and html != expected_html:
        issues.append(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_HTML}: does not match deterministic strategy assumption stress kit output; run {STRATEGY_ASSUMPTION_STRESS_KIT_COMMAND}"
        )

    return issues


def find_stress_kit_quickstart_card_issues(
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    issues: list[str] = []
    json_path = repo_root / STRESS_KIT_QUICKSTART_CARD_JSON
    markdown_path = repo_root / STRESS_KIT_QUICKSTART_CARD_MARKDOWN

    if not json_path.exists():
        issues.append(f"{STRESS_KIT_QUICKSTART_CARD_JSON}: card JSON is missing")
        payload: object = {}
    else:
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                f"{STRESS_KIT_QUICKSTART_CARD_JSON}: invalid JSON: {exc.msg}"
            )
            payload = {}

    if not isinstance(payload, dict):
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: card must be a JSON object"
        )
        payload = {}

    if tuple(payload) != STRESS_KIT_QUICKSTART_CARD_TOP_LEVEL_KEYS:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: top-level keys must match "
            "the stress kit quickstart card schema order"
        )
    if payload.get("artifact_type") != "stress_kit_quickstart_card":
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: artifact_type must be stress_kit_quickstart_card"
        )
    if payload.get("schema_version") != "1.0":
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: schema_version must be 1.0"
        )
    for key in QUICKSTART_BOUNDARY_FLAGS:
        if payload.get(key) is not True:
            issues.append(f"{STRESS_KIT_QUICKSTART_CARD_JSON}: {key} must be true")
    if payload.get("estimated_review_time_minutes") != 2:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: estimated_review_time_minutes must be 2"
        )

    purpose = payload.get("purpose")
    if not _contains_all_terms(
        purpose,
        (
            "strategy assumption stress kit",
            "two-minute",
            "static artifact boundary review",
        ),
    ):
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: purpose must preserve quickstart boundary-review wording"
        )

    source_artifact = _dict_value(payload.get("source_artifact"))
    if source_artifact.get("markdown_path") != STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: source_artifact.markdown_path must be {STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH}"
        )
    if source_artifact.get("json_path") != STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: source_artifact.json_path must be {STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH}"
        )

    defaults = _dict_value(payload.get("default_outputs"))
    if defaults.get("markdown") != str(STRESS_KIT_QUICKSTART_CARD_MARKDOWN):
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: default_outputs.markdown must be {STRESS_KIT_QUICKSTART_CARD_MARKDOWN}"
        )
    if defaults.get("json") != str(STRESS_KIT_QUICKSTART_CARD_JSON):
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: default_outputs.json must be {STRESS_KIT_QUICKSTART_CARD_JSON}"
        )

    checklist = payload.get("reviewer_checklist")
    if not isinstance(checklist, list) or len(checklist) != 5:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: reviewer_checklist must include the five quickstart checks"
        )
        checklist = []
    _extend_row_shape_issues(
        issues,
        STRESS_KIT_QUICKSTART_CARD_JSON,
        checklist,
        QUICKSTART_REVIEWER_CHECKLIST_ITEM_KEYS,
        "reviewer_checklist",
    )
    for required_step in (
        "scope",
        "assumptions",
        "stress_language",
        "leveraged_etf_like_caveats",
        "boundaries",
    ):
        if not any(
            isinstance(item, dict) and item.get("step") == required_step
            for item in checklist
        ):
            issues.append(
                f"{STRESS_KIT_QUICKSTART_CARD_JSON}: missing reviewer checklist step {required_step}"
            )

    stop_conditions = payload.get("stop_conditions")
    if not isinstance(stop_conditions, list) or len(stop_conditions) != 2:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: stop_conditions must include the two stop conditions"
        )
        stop_conditions = []
    _extend_row_shape_issues(
        issues,
        STRESS_KIT_QUICKSTART_CARD_JSON,
        stop_conditions,
        QUICKSTART_STOP_CONDITION_KEYS,
        "stop_conditions",
    )

    receipt = _dict_value(payload.get("completion_receipt"))
    if tuple(receipt) != QUICKSTART_COMPLETION_RECEIPT_KEYS:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: completion_receipt keys must match the schema order"
        )
    if receipt.get("source_command") != STRESS_KIT_QUICKSTART_CARD_COMMAND:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: completion_receipt.source_command must be {STRESS_KIT_QUICKSTART_CARD_COMMAND}"
        )
    if receipt.get("generated_output_paths") != [
        str(STRESS_KIT_QUICKSTART_CARD_MARKDOWN),
        str(STRESS_KIT_QUICKSTART_CARD_JSON),
    ]:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: completion_receipt.generated_output_paths must list the quickstart Markdown and JSON outputs"
        )
    if not _contains_all_terms(
        receipt.get("review_boundary"),
        (
            "static documentation boundaries",
            "does not validate financial correctness",
            "robustness",
            "suitability",
            "future performance",
        ),
    ):
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: completion_receipt.review_boundary must preserve review-only wording"
        )

    do_not_use_for = payload.get("do_not_use_for")
    if not _is_non_empty_string_list(do_not_use_for):
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: do_not_use_for must be a non-empty list"
        )
    else:
        for required_phrase in QUICKSTART_OUT_OF_SCOPE_ITEMS:
            if required_phrase not in do_not_use_for:
                issues.append(
                    f"{STRESS_KIT_QUICKSTART_CARD_JSON}: do_not_use_for must include {required_phrase}"
                )

    if not markdown_path.exists():
        issues.append(f"{STRESS_KIT_QUICKSTART_CARD_MARKDOWN}: card Markdown is missing")
        markdown = ""
    else:
        markdown = markdown_path.read_text(encoding="utf-8")
        if not markdown.strip():
            issues.append(f"{STRESS_KIT_QUICKSTART_CARD_MARKDOWN}: card Markdown is empty")

    for required_text in (
        "# Stress Kit Quickstart Card",
        "## Source",
        "## Two-Minute Reviewer Checklist",
        "## Stop Conditions",
        "## Completion Receipt",
        "## Boundaries",
        "## Do Not Use This For",
        STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH,
        STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH,
        STRESS_KIT_QUICKSTART_CARD_COMMAND,
        STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH,
        STRESS_KIT_QUICKSTART_CARD_JSON_PATH,
        "no_live_data",
        "no_broker_or_account",
        "no_orders_or_position_sizing",
        "not validate financial correctness",
        "daily reset, path dependency, volatility drag",
    ):
        if required_text not in markdown:
            issues.append(
                f"{STRESS_KIT_QUICKSTART_CARD_MARKDOWN}: missing card text {required_text}"
            )

    expected_payload = build_stress_kit_quickstart_card()
    if payload != expected_payload:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_JSON}: does not match deterministic stress kit quickstart card output; run {STRESS_KIT_QUICKSTART_CARD_COMMAND}"
        )
    expected_markdown = render_stress_kit_quickstart_card(expected_payload)
    if markdown and markdown != expected_markdown:
        issues.append(
            f"{STRESS_KIT_QUICKSTART_CARD_MARKDOWN}: does not match deterministic stress kit quickstart card output; run {STRESS_KIT_QUICKSTART_CARD_COMMAND}"
        )

    return issues


def find_assumption_ledger_summary_issues(
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    issues: list[str] = []
    json_path = repo_root / ASSUMPTION_LEDGER_SUMMARY_JSON
    markdown_path = repo_root / ASSUMPTION_LEDGER_SUMMARY_MARKDOWN

    if not json_path.exists():
        issues.append(f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: summary JSON is missing")
        payload: object = {}
    else:
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(
                f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: invalid JSON: {exc.msg}"
            )
            payload = {}

    if not isinstance(payload, dict):
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: summary must be a JSON object"
        )
        payload = {}

    if tuple(payload) != ASSUMPTION_LEDGER_SUMMARY_TOP_LEVEL_KEYS:
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: top-level keys must match "
            "the assumption ledger summary schema order"
        )
    if payload.get("artifact_type") != "assumption_ledger_summary":
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: artifact_type must be assumption_ledger_summary"
        )
    if payload.get("schema_version") != "1.0":
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: schema_version must be 1.0"
        )
    for key in ASSUMPTION_LEDGER_SUMMARY_BOUNDARY_FLAGS:
        if payload.get(key) is not True:
            issues.append(f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: {key} must be true")

    defaults = _dict_value(payload.get("default_outputs"))
    if defaults.get("markdown") != str(ASSUMPTION_LEDGER_SUMMARY_MARKDOWN):
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: default_outputs.markdown must be {ASSUMPTION_LEDGER_SUMMARY_MARKDOWN}"
        )
    if defaults.get("json") != str(ASSUMPTION_LEDGER_SUMMARY_JSON):
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: default_outputs.json must be {ASSUMPTION_LEDGER_SUMMARY_JSON}"
        )

    strategy_assumptions = payload.get("strategy_assumptions")
    if not isinstance(strategy_assumptions, list) or len(strategy_assumptions) != 4:
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: strategy_assumptions must include the four assumption rows"
        )
        strategy_assumptions = []
    _extend_row_shape_issues(
        issues,
        ASSUMPTION_LEDGER_SUMMARY_JSON,
        strategy_assumptions,
        ASSUMPTION_ITEM_KEYS,
        "strategy_assumptions",
    )

    risk_boundaries = payload.get("risk_boundaries")
    if not isinstance(risk_boundaries, list) or len(risk_boundaries) != 4:
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: risk_boundaries must include the four boundary rows"
        )
        risk_boundaries = []
    _extend_row_shape_issues(
        issues,
        ASSUMPTION_LEDGER_SUMMARY_JSON,
        risk_boundaries,
        RISK_BOUNDARY_KEYS,
        "risk_boundaries",
    )

    evidence_paths = payload.get("generated_evidence_paths")
    if not isinstance(evidence_paths, list) or len(evidence_paths) != 6:
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: generated_evidence_paths must include the six evidence rows"
        )
        evidence_paths = []
    _extend_row_shape_issues(
        issues,
        ASSUMPTION_LEDGER_SUMMARY_JSON,
        evidence_paths,
        EVIDENCE_PATH_KEYS,
        "generated_evidence_paths",
    )
    for required_path in (
        str(ASSUMPTION_LEDGER_SUMMARY_MARKDOWN),
        str(ASSUMPTION_LEDGER_SUMMARY_JSON),
    ):
        if not any(
            isinstance(item, dict) and item.get("path") == required_path
            for item in evidence_paths
        ):
            issues.append(
                f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: generated_evidence_paths missing {required_path}"
            )

    not_claimed = payload.get("not_claimed")
    if not isinstance(not_claimed, list) or len(not_claimed) != 4:
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: not_claimed must include the four non-claim rows"
        )
        not_claimed = []
    _extend_row_shape_issues(
        issues,
        ASSUMPTION_LEDGER_SUMMARY_JSON,
        not_claimed,
        NOT_CLAIMED_KEYS,
        "not_claimed",
    )

    commands = payload.get("verification_commands")
    if not _is_non_empty_string_list(commands):
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: verification_commands must be a non-empty list"
        )
    else:
        for required_command in (
            ASSUMPTION_LEDGER_SUMMARY_COMMAND,
            "python scripts/selfcheck.py",
            "python -m pytest",
        ):
            if required_command not in commands:
                issues.append(
                    f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: missing verification command {required_command}"
                )

    if not markdown_path.exists():
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_MARKDOWN}: summary Markdown is missing"
        )
        markdown = ""
    else:
        markdown = markdown_path.read_text(encoding="utf-8")
        if not markdown.strip():
            issues.append(
                f"{ASSUMPTION_LEDGER_SUMMARY_MARKDOWN}: summary Markdown is empty"
            )

    for required_text in (
        "# Assumption Ledger Summary",
        "## Strategy Assumptions",
        "## Risk Boundaries",
        "## Generated Evidence Paths",
        "## What Is Not Being Claimed",
        "## Boundary Flags",
        "## Verification Commands",
        "not as a verdict on strategy quality or suitability",
        "does not read live data, connect to brokers or accounts, route orders, size positions, forecast, recommend, or provide investment advice",
        ASSUMPTION_LEDGER_SUMMARY_COMMAND,
        str(ASSUMPTION_LEDGER_SUMMARY_MARKDOWN),
        str(ASSUMPTION_LEDGER_SUMMARY_JSON),
    ):
        if required_text not in markdown:
            issues.append(
                f"{ASSUMPTION_LEDGER_SUMMARY_MARKDOWN}: missing summary text {required_text}"
            )

    expected_payload = build_assumption_ledger_summary()
    if payload != expected_payload:
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON}: does not match deterministic assumption ledger summary output; run {ASSUMPTION_LEDGER_SUMMARY_COMMAND}"
        )
    expected_markdown = render_assumption_ledger_summary(expected_payload)
    if markdown and markdown != expected_markdown:
        issues.append(
            f"{ASSUMPTION_LEDGER_SUMMARY_MARKDOWN}: does not match deterministic assumption ledger summary output; run {ASSUMPTION_LEDGER_SUMMARY_COMMAND}"
        )

    return issues


def find_public_claim_issues(
    repo_root: Path = REPO_ROOT,
    public_files: tuple[Path, ...] = PUBLIC_CLAIM_SOURCES,
) -> list[str]:
    issues: list[str] = []
    for relative_source in public_files:
        source = repo_root / relative_source
        if not source.exists():
            issues.append(f"{relative_source}: source file is missing")
            continue

        text = source.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            match = FORBIDDEN_PUBLIC_CLAIM_RE.search(line)
            if match and not _is_negated_public_claim(line, match):
                issues.append(
                    f"{relative_source}:{line_number}: forbidden public claim "
                    f"'{match.group(0)}'"
                )

    return issues


def find_fixture_provenance_issues(repo_root: Path = REPO_ROOT) -> list[str]:
    issues: list[str] = []
    for relative_path in FIXTURE_PROVENANCE_FILES:
        path = repo_root / relative_path
        if not path.exists():
            issues.append(f"{relative_path}: provenance metadata file is missing")
            continue

        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(f"{relative_path}: invalid JSON: {exc.msg}")
            continue

        if not isinstance(raw, dict):
            issues.append(f"{relative_path}: metadata must be a JSON object")
            continue

        for key in ("dataset_label", "data_kind", "source", "created_date", "as_of_date"):
            if not isinstance(raw.get(key), str) or not raw[key].strip():
                issues.append(f"{relative_path}: {key} must be a non-empty string")
        if raw.get("data_kind") != "synthetic_static_fixture":
            issues.append(
                f"{relative_path}: data_kind must be synthetic_static_fixture"
            )
        if raw.get("research_only") is not True:
            issues.append(f"{relative_path}: research_only must be true")
        limitations = raw.get("limitations")
        if not _is_non_empty_string_list(limitations):
            issues.append(
                f"{relative_path}: limitations must be a non-empty list of strings"
            )

        regimes = raw.get("regimes")
        if regimes is not None:
            if not isinstance(regimes, list) or not regimes:
                issues.append(f"{relative_path}: regimes must be a non-empty list")
            else:
                for index, regime in enumerate(regimes, start=1):
                    if not isinstance(regime, dict):
                        issues.append(
                            f"{relative_path}: regimes[{index}] must be an object"
                        )
                        continue
                    for key in ("symbol", "regime", "description"):
                        if not isinstance(regime.get(key), str) or not regime[key].strip():
                            issues.append(
                                f"{relative_path}: regimes[{index}].{key} "
                                "must be a non-empty string"
                            )
                    assumptions = regime.get("assumptions")
                    if not _is_non_empty_string_list(assumptions):
                        issues.append(
                            f"{relative_path}: regimes[{index}].assumptions "
                            "must be a non-empty list of strings"
                        )
                    for key in (
                        "synthetic_only",
                        "not_predictive",
                        "not_live_trading",
                    ):
                        if regime.get(key) is not True:
                            issues.append(
                                f"{relative_path}: regimes[{index}].{key} "
                                "must be true"
                            )

        csv_path = path.with_name(path.name.removesuffix(".provenance.json"))
        if not csv_path.exists():
            issues.append(f"{relative_path}: source CSV is missing")

    return issues


def _is_non_empty_string_list(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def _dict_value(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        return value
    return {}


def _extend_missing_key_issues(
    issues: list[str],
    relative_path: Path,
    value: dict[str, object],
    required_keys: tuple[str, ...],
    *,
    prefix: str = "",
) -> None:
    for key in required_keys:
        if key not in value:
            dotted_key = f"{prefix}.{key}" if prefix else key
            issues.append(f"{relative_path}: missing {dotted_key}")


def _extend_row_shape_issues(
    issues: list[str],
    relative_path: Path,
    rows: list[object],
    required_keys: tuple[str, ...],
    field_name: str,
) -> None:
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            issues.append(f"{relative_path}: {field_name}[{index}] must be an object")
            continue
        if tuple(row) != required_keys:
            issues.append(
                f"{relative_path}: {field_name}[{index}] keys must be "
                f"{', '.join(required_keys)}"
            )
        for key in required_keys:
            if not isinstance(row.get(key), str) or not row[key].strip():
                issues.append(
                    f"{relative_path}: {field_name}[{index}].{key} must be a non-empty string"
                )


def _contains_all_terms(value: object, terms: tuple[str, ...]) -> bool:
    if not isinstance(value, str):
        return False
    lowered = value.lower()
    return all(term in lowered for term in terms)


def _is_negated_public_claim(line: str, match: re.Match[str]) -> bool:
    claim = match.group(0).lower()
    prefix = line[max(0, match.start() - 80) : match.start()].lower()
    direct_prefix = line[max(0, match.start() - 25) : match.start()].lower()
    if re.search(r"\b(no|not|never|without)\b", direct_prefix):
        return True
    if claim == "live trading signal" and re.search(r"\bnot\b", prefix):
        return True
    return False


def _strip_fenced_code_blocks(text: str) -> str:
    return FENCED_BLOCK_RE.sub("\n", text)


def _normalize_markdown_link_target(target: str) -> str:
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return unquote(target)


def _is_external_or_anchor_only_link(target: str) -> bool:
    return (
        not target
        or target.startswith("#")
        or target.startswith(("http://", "https://", "mailto:"))
    )


def _local_markdown_link_path(repo_root: Path, source: Path, target: str) -> Path:
    target_without_fragment = target.split("#", 1)[0].split("?", 1)[0]
    if target_without_fragment.startswith("/"):
        return repo_root / target_without_fragment.lstrip("/")
    return (source.parent / target_without_fragment).resolve()


def _raw_links_for_source(relative_source: Path, text: str) -> list[str]:
    if relative_source.suffix == ".html":
        return HTML_HREF_RE.findall(text)
    return MARKDOWN_LINK_RE.findall(_strip_fenced_code_blocks(text))


def _local_links_for_source(relative_source: Path, text: str) -> set[str]:
    return {
        _normalize_markdown_link_target(target)
        for target in _raw_links_for_source(relative_source, text)
        if not _is_external_or_anchor_only_link(_normalize_markdown_link_target(target))
    }


def _html_remote_or_absolute_references(text: str) -> list[str]:
    targets = [
        _normalize_markdown_link_target(target)
        for target in (
            *_html_reference_attr_values(text),
            *_html_srcset_reference_values(text),
        )
    ]
    return [
        target
        for target in targets
        if _is_non_local_html_reference(target)
    ]


def _html_reference_attr_values(text: str) -> list[str]:
    return [_first_present_group(match) for match in HTML_REFERENCE_ATTR_RE.findall(text)]


def _html_srcset_reference_values(text: str) -> list[str]:
    values: list[str] = []
    for raw_srcset in (
        _first_present_group(match) for match in HTML_SRCSET_ATTR_RE.findall(text)
    ):
        for candidate in raw_srcset.split(","):
            reference = candidate.strip().split(None, 1)[0]
            if reference:
                values.append(reference)
    return values


def _first_present_group(groups: tuple[str, str, str]) -> str:
    return next((group for group in groups if group), "")


def _is_non_local_html_reference(target: str) -> bool:
    if target.startswith("#"):
        return False
    return (
        target.startswith(("//", "/"))
        or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE) is not None
    )


def _sample_artifact_commands() -> list[list[str]]:
    return [
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--methodology-audit-template",
            "--output",
            "reports/methodology-audit-template.md",
            "--json-output",
            "reports/methodology-audit-template.json",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--methodology-audit-review-template",
            "--json-output",
            "reports/methodology-audit-review-template.json",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--score-methodology-audit",
            "examples/configs/methodology-audit-review.json",
            "--output",
            "reports/methodology-audit-score.md",
            "--json-output",
            "reports/methodology-audit-score.json",
            "--html-output",
            "reports/methodology-audit-score.html",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--config",
            "examples/configs/single-backtest-report.json",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(CSV_PATH),
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
            "reports/pretrade-packet.md",
            "--json-output",
            "reports/pretrade-packet.json",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(CSV_PATH),
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
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(CSV_PATH),
            "--symbol",
            "QQQ_LIKE",
            "--sweep",
            "--short-windows",
            "10,20",
            "--long-windows",
            "50,100",
            "--fee-bps",
            "10.0",
            "--top-n",
            "3",
            "--output",
            "reports/sample-sweep.md",
            "--json-output",
            "reports/sample-sweep.json",
            "--html-output",
            "reports/sample-sweep.html",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            str(CSV_PATH),
            "--symbol",
            "QQQ_LIKE",
            "--sweep",
            "--short-windows",
            "1,2",
            "--long-windows",
            "2,3",
            "--fee-bps",
            "10.0",
            "--top-n",
            "3",
            "--split-ratio",
            "0.5",
            "--output",
            "reports/sample-sweep-split.md",
            "--json-output",
            "reports/sample-sweep-split.json",
            "--html-output",
            "reports/sample-sweep-split.html",
        ],
        [
            sys.executable,
            "scripts/fee_sensitivity.py",
            "--markdown-output",
            "reports/fee-sensitivity.md",
            "--json-output",
            "reports/fee-sensitivity.json",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--reviewer-rerun-receipt",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--reviewer-decision-matrix",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--beginner-prediction-checklist",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--strategy-assumption-stress-kit",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--stress-kit-quickstart-card",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--assumption-ledger-summary",
        ],
        [
            sys.executable,
            "-m",
            "market_signal_lab.cli",
            "--regime-comparison",
        ],
    ]


def main() -> int:
    checks = [
        ("compileall", run_compileall),
        ("pytest", run_pytest),
        ("sample artifact generation", run_sample_artifact_generation),
        ("documentation/gallery link check", run_docs_link_check),
        ("static demo acceptance check", run_demo_acceptance_check),
        ("public claim boundary check", run_public_claim_check),
        ("static fixture provenance check", run_fixture_provenance_check),
    ]

    passed = True
    for name, check in checks:
        if not check():
            print(f"FAIL: {name}")
            passed = False
        else:
            print(f"PASS: {name}")

    print("Selfcheck completed.")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
