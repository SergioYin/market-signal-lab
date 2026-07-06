"""Command-line interface for CSV moving-average backtest reports."""

from __future__ import annotations

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from collections.abc import Mapping, Sequence
from importlib.resources import files
from io import StringIO
from pathlib import Path
import csv
import hashlib
import json
import os
import sys
import tempfile
from typing import Any

from market_signal_lab import __version__
from market_signal_lab.acceptance_receipt_index import (
    ACCEPTANCE_RECEIPT_INDEX_JSON_PATH,
    ACCEPTANCE_RECEIPT_INDEX_MARKDOWN_PATH,
    build_acceptance_receipt_index,
    render_acceptance_receipt_index,
)
from market_signal_lab.assumption_ledger_summary import (
    ASSUMPTION_LEDGER_SUMMARY_JSON_PATH,
    ASSUMPTION_LEDGER_SUMMARY_MARKDOWN_PATH,
    build_assumption_ledger_summary,
    render_assumption_ledger_summary,
)
from market_signal_lab.backtest import backtest_long_cash
from market_signal_lab.beginner_prediction_checklist import (
    build_beginner_prediction_checklist,
    render_beginner_prediction_checklist,
)
from market_signal_lab.cold_user_review_route import (
    INTEGRITY_ARTIFACT_PATHS,
    build_cold_user_review_route,
    render_cold_user_review_route,
)
from market_signal_lab.data import (
    REQUIRED_COLUMNS,
    PriceBar,
    load_ohlc_csv,
    load_static_fixture_provenance,
)
from market_signal_lab.html import render_html_report
from market_signal_lab.metrics import (
    annualized_return,
    max_drawdown,
    sharpe_like,
    total_return,
    volatility,
    win_rate_from_returns,
)
from market_signal_lab.manifest import build_manifest, render_manifest_markdown
from market_signal_lab.methodology_audit import (
    build_methodology_audit_review_template,
    build_methodology_audit_template,
    render_methodology_audit_template,
    render_methodology_audit_score,
    score_methodology_audit_review,
)
from market_signal_lab.packet import (
    build_pretrade_research_packet,
    render_pretrade_research_packet,
)
from market_signal_lab.prediction_readiness_audit import (
    build_prediction_readiness_audit,
    render_prediction_readiness_audit,
)
from market_signal_lab.promotion_readiness_check import (
    build_promotion_readiness_check,
    render_promotion_readiness_check,
)
from market_signal_lab.public_demo_evidence_receipt import (
    PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON_PATH,
    PUBLIC_DEMO_EVIDENCE_RECEIPT_MARKDOWN_PATH,
    build_public_demo_evidence_receipt,
    render_public_demo_evidence_receipt,
)
from market_signal_lab.reviewer_decision_matrix import (
    build_reviewer_decision_matrix,
    render_reviewer_decision_matrix,
)
from market_signal_lab.report import (
    build_exposure_trade_review,
    build_scenario_risk_interpretation,
    render_regime_comparison_report,
    render_experiment_report,
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
    build_reviewer_rerun_receipt,
    render_reviewer_rerun_receipt,
)
from market_signal_lab.scenario_card import build_scenario_card, render_scenario_card
from market_signal_lab.split import TrainTestSplit, split_train_test
from market_signal_lab.static_visual_capture_checklist import (
    CAPTURE_SOURCE_PATHS,
    STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG,
    STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_PATH,
    STATIC_VISUAL_CAPTURE_CHECKLIST_MARKDOWN_PATH,
    build_static_visual_capture_checklist,
    render_static_visual_capture_checklist,
)
from market_signal_lab.static_visual_capture_receipt import (
    STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS,
    STATIC_VISUAL_CAPTURE_RECEIPT_FLAG,
    STATIC_VISUAL_CAPTURE_RECEIPT_JSON_PATH,
    STATIC_VISUAL_CAPTURE_RECEIPT_MARKDOWN_PATH,
    build_static_visual_capture_receipt,
    render_static_visual_capture_receipt,
)
from market_signal_lab.static_visual_release_comparison import (
    SOURCE_RECEIPT_ARTIFACT_PATHS,
    STATIC_VISUAL_RELEASE_COMPARISON_FLAG,
    STATIC_VISUAL_RELEASE_COMPARISON_JSON_PATH,
    STATIC_VISUAL_RELEASE_COMPARISON_MARKDOWN_PATH,
    build_static_visual_release_comparison,
    render_static_visual_release_comparison,
)
from market_signal_lab.strategy_assumption_stress_kit import (
    STRATEGY_ASSUMPTION_STRESS_KIT_HTML_PATH,
    STRATEGY_ASSUMPTION_STRESS_KIT_HTML_TITLE,
    STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH,
    STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH,
    build_strategy_assumption_stress_kit,
    render_strategy_assumption_stress_kit,
)
from market_signal_lab.stress_kit_quickstart_card import (
    STRESS_KIT_QUICKSTART_CARD_FLAG,
    STRESS_KIT_QUICKSTART_CARD_JSON_PATH,
    STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH,
    build_stress_kit_quickstart_card,
    render_stress_kit_quickstart_card,
)
from market_signal_lab.strategies import moving_average_crossover_strategy
from market_signal_lab.sweep import (
    SweepResult,
    render_sweep_report,
    run_moving_average_sweep,
)
from market_signal_lab.thesis_ledger import (
    render_thesis_ledger_acceptance_summary,
    validate_cross_asset_thesis_ledger_packet,
)
from market_signal_lab.visual_acceptance_bundle import (
    VISUAL_ACCEPTANCE_BUNDLE_JSON_PATH,
    VISUAL_ACCEPTANCE_BUNDLE_MARKDOWN_PATH,
    build_visual_acceptance_bundle,
    render_visual_acceptance_bundle,
)
from market_signal_lab.visual_walkthrough_evidence_receipt import (
    VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_JSON_PATH,
    VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_MARKDOWN_PATH,
    build_visual_walkthrough_evidence_receipt,
    render_visual_walkthrough_evidence_receipt,
)

BUNDLED_REGIME_CONFIGS = (
    Path("examples/configs/multi-regime-bull-report.json"),
    Path("examples/configs/multi-regime-choppy-report.json"),
    Path("examples/configs/multi-regime-drawdown-recovery-report.json"),
)
BUNDLED_RESOURCE_ROOT = "_resources"
REGIME_COMPARISON_OUTPUT = Path("reports/regime-comparison.md")
REGIME_COMPARISON_JSON_OUTPUT = Path("reports/regime-comparison.json")
REGIME_COMPARISON_HTML_OUTPUT = Path("reports/regime-comparison.html")
SCENARIO_CARD_OUTPUT = Path("reports/scenario-card.md")
SCENARIO_CARD_JSON_OUTPUT = Path("reports/scenario-card.json")
THESIS_LEDGER_DEFAULT_JSON = Path("reports/cross-asset-thesis-ledger.json")
THESIS_LEDGER_ACCEPTANCE_OUTPUT = Path(
    "reports/cross-asset-thesis-ledger-acceptance.md"
)
THESIS_LEDGER_ACCEPTANCE_JSON_OUTPUT = Path(
    "reports/cross-asset-thesis-ledger-acceptance.json"
)
REVIEWER_EVIDENCE_BUNDLE_OUTPUT = Path("reports/reviewer-evidence-bundle.md")
REVIEWER_EVIDENCE_BUNDLE_JSON_OUTPUT = Path("reports/reviewer-evidence-bundle.json")
PUBLIC_DEMO_EVIDENCE_RECEIPT_OUTPUT = Path(
    PUBLIC_DEMO_EVIDENCE_RECEIPT_MARKDOWN_PATH
)
PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON_OUTPUT = Path(
    PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON_PATH
)
PUBLIC_DEMO_EVIDENCE_RECEIPT_FLAG = "--public-demo-evidence-receipt"
REVIEWER_RERUN_RECEIPT_OUTPUT = Path("reports/reviewer-rerun-receipt.md")
REVIEWER_RERUN_RECEIPT_JSON_OUTPUT = Path("reports/reviewer-rerun-receipt.json")
ACCEPTANCE_RECEIPT_INDEX_OUTPUT = Path(ACCEPTANCE_RECEIPT_INDEX_MARKDOWN_PATH)
ACCEPTANCE_RECEIPT_INDEX_JSON_OUTPUT = Path(ACCEPTANCE_RECEIPT_INDEX_JSON_PATH)
ACCEPTANCE_RECEIPT_INDEX_FLAG = "--acceptance-receipt-index"
VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_OUTPUT = Path(
    VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_MARKDOWN_PATH
)
VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_JSON_OUTPUT = Path(
    VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_JSON_PATH
)
VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_FLAG = (
    "--visual-walkthrough-evidence-receipt"
)
VISUAL_ACCEPTANCE_BUNDLE_OUTPUT = Path(VISUAL_ACCEPTANCE_BUNDLE_MARKDOWN_PATH)
VISUAL_ACCEPTANCE_BUNDLE_JSON_OUTPUT = Path(VISUAL_ACCEPTANCE_BUNDLE_JSON_PATH)
VISUAL_ACCEPTANCE_BUNDLE_FLAG = "--visual-acceptance-bundle"
REVIEWER_ACCEPTANCE_SCORECARD_OUTPUT = Path(
    "reports/reviewer-acceptance-scorecard.md"
)
REVIEWER_ACCEPTANCE_SCORECARD_JSON_OUTPUT = Path(
    "reports/reviewer-acceptance-scorecard.json"
)
REVIEWER_ACCEPTANCE_SCORECARD_FLAG = "--reviewer-acceptance-scorecard"
REVIEWER_DECISION_MATRIX_OUTPUT = Path("reports/reviewer-decision-matrix.md")
REVIEWER_DECISION_MATRIX_JSON_OUTPUT = Path(
    "reports/reviewer-decision-matrix.json"
)
BEGINNER_PREDICTION_CHECKLIST_OUTPUT = Path(
    "reports/beginner-prediction-checklist.md"
)
BEGINNER_PREDICTION_CHECKLIST_JSON_OUTPUT = Path(
    "reports/beginner-prediction-checklist.json"
)
PREDICTION_READINESS_AUDIT_OUTPUT = Path("reports/prediction-readiness-audit.md")
PREDICTION_READINESS_AUDIT_JSON_OUTPUT = Path(
    "reports/prediction-readiness-audit.json"
)
PROMOTION_READINESS_CHECK_OUTPUT = Path("reports/promotion-readiness-check.md")
PROMOTION_READINESS_CHECK_JSON_OUTPUT = Path(
    "reports/promotion-readiness-check.json"
)
PROMOTION_READINESS_CHECK_DEFAULT_INPUT = object()
REVIEWER_DECISION_MATRIX_FLAG = "--reviewer-decision-matrix"
PREDICTION_READINESS_AUDIT_FLAG = "--prediction-readiness-audit"
PROMOTION_READINESS_CHECK_FLAG = "--promotion-readiness-check"
COLD_USER_REVIEW_ROUTE_OUTPUT = Path("reports/cold-user-review-route.md")
COLD_USER_REVIEW_ROUTE_JSON_OUTPUT = Path("reports/cold-user-review-route.json")
COLD_USER_REVIEW_ROUTE_FLAG = "--cold-user-review-route"
COLD_USER_REVIEW_ROUTE_STATIC_RESOURCES = tuple(
    Path(path) for path in INTEGRITY_ARTIFACT_PATHS
)
STRATEGY_ASSUMPTION_STRESS_KIT_OUTPUT = Path(
    STRATEGY_ASSUMPTION_STRESS_KIT_MARKDOWN_PATH
)
STRATEGY_ASSUMPTION_STRESS_KIT_JSON_OUTPUT = Path(
    STRATEGY_ASSUMPTION_STRESS_KIT_JSON_PATH
)
STRATEGY_ASSUMPTION_STRESS_KIT_HTML_OUTPUT = Path(
    STRATEGY_ASSUMPTION_STRESS_KIT_HTML_PATH
)
STRATEGY_ASSUMPTION_STRESS_KIT_FLAG = "--strategy-assumption-stress-kit"
STRESS_KIT_QUICKSTART_CARD_OUTPUT = Path(
    STRESS_KIT_QUICKSTART_CARD_MARKDOWN_PATH
)
STRESS_KIT_QUICKSTART_CARD_JSON_OUTPUT = Path(
    STRESS_KIT_QUICKSTART_CARD_JSON_PATH
)
ASSUMPTION_LEDGER_SUMMARY_OUTPUT = Path(ASSUMPTION_LEDGER_SUMMARY_MARKDOWN_PATH)
ASSUMPTION_LEDGER_SUMMARY_JSON_OUTPUT = Path(ASSUMPTION_LEDGER_SUMMARY_JSON_PATH)
ASSUMPTION_LEDGER_SUMMARY_FLAG = "--assumption-ledger-summary"
STATIC_VISUAL_CAPTURE_CHECKLIST_OUTPUT = Path(
    STATIC_VISUAL_CAPTURE_CHECKLIST_MARKDOWN_PATH
)
STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_OUTPUT = Path(
    STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_PATH
)
STATIC_VISUAL_CAPTURE_CHECKLIST_STATIC_RESOURCES = tuple(
    Path(path) for path in CAPTURE_SOURCE_PATHS
)
STATIC_VISUAL_CAPTURE_RECEIPT_OUTPUT = Path(
    STATIC_VISUAL_CAPTURE_RECEIPT_MARKDOWN_PATH
)
STATIC_VISUAL_CAPTURE_RECEIPT_JSON_OUTPUT = Path(
    STATIC_VISUAL_CAPTURE_RECEIPT_JSON_PATH
)
STATIC_VISUAL_CAPTURE_RECEIPT_STATIC_RESOURCES = tuple(
    Path(path) for path in STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS
)
STATIC_VISUAL_RELEASE_COMPARISON_OUTPUT = Path(
    STATIC_VISUAL_RELEASE_COMPARISON_MARKDOWN_PATH
)
STATIC_VISUAL_RELEASE_COMPARISON_JSON_OUTPUT = Path(
    STATIC_VISUAL_RELEASE_COMPARISON_JSON_PATH
)
STATIC_VISUAL_RELEASE_COMPARISON_STATIC_RESOURCES = tuple(
    Path(path)
    for path in (
        *SOURCE_RECEIPT_ARTIFACT_PATHS,
        *STATIC_VISUAL_CAPTURE_ARTIFACT_PATHS,
    )
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    _reject_reviewer_rerun_receipt_mode_conflicts(args, parser)
    _reject_cold_user_review_route_mode_conflicts(args, parser)
    _reject_prediction_readiness_audit_mode_conflicts(args, parser)
    _reject_beginner_prediction_checklist_mode_conflicts(args, parser)
    _reject_public_demo_evidence_receipt_mode_conflicts(args, parser)
    _reject_acceptance_receipt_index_mode_conflicts(args, parser)
    _reject_visual_walkthrough_evidence_receipt_mode_conflicts(args, parser)
    _reject_visual_acceptance_bundle_mode_conflicts(args, parser)
    _reject_reviewer_acceptance_scorecard_mode_conflicts(args, parser)
    _reject_reviewer_decision_matrix_mode_conflicts(args, parser)
    _reject_promotion_readiness_check_mode_conflicts(args, parser)
    _reject_strategy_assumption_stress_kit_mode_conflicts(args, parser)
    _reject_stress_kit_quickstart_card_mode_conflicts(args, parser)
    _reject_assumption_ledger_summary_mode_conflicts(args, parser)
    _reject_static_visual_capture_checklist_mode_conflicts(args, parser)
    _reject_static_visual_capture_receipt_mode_conflicts(args, parser)
    _reject_static_visual_release_comparison_mode_conflicts(args, parser)

    try:
        if args.reviewer_rerun_receipt:
            args = _resolve_reviewer_rerun_receipt_args(args, parser)
            report, json_payload, manifest_payload = _run_reviewer_rerun_receipt()
        elif args.cold_user_review_route:
            args = _resolve_cold_user_review_route_args(args, parser)
            report, json_payload, manifest_payload = _run_cold_user_review_route()
        elif args.reviewer_acceptance_scorecard:
            args = _resolve_reviewer_acceptance_scorecard_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_reviewer_acceptance_scorecard()
            )
        elif args.methodology_audit_review_template:
            args = _resolve_methodology_audit_review_template_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_methodology_audit_review_template()
            )
        elif args.score_methodology_audit is not None:
            args = _resolve_methodology_audit_score_args(args, parser)
            report, json_payload, manifest_payload = _run_methodology_audit_score(args)
        elif args.methodology_audit_template:
            args = _resolve_methodology_audit_template_args(args, parser)
            report, json_payload, manifest_payload = _run_methodology_audit_template()
        elif args.validate_thesis_ledger is not None:
            args = _resolve_thesis_ledger_validation_args(args, parser)
            report, json_payload, manifest_payload = _run_thesis_ledger_validation(args)
        elif args.regime_comparison:
            args = _resolve_regime_comparison_args(args, parser)
            report, json_payload, manifest_payload = _run_regime_comparison(args)
        elif args.reviewer_evidence_bundle:
            args = _resolve_reviewer_evidence_bundle_args(args, parser)
            report, json_payload, manifest_payload = _run_reviewer_evidence_bundle()
        elif args.public_demo_evidence_receipt:
            args = _resolve_public_demo_evidence_receipt_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_public_demo_evidence_receipt()
            )
        elif args.acceptance_receipt_index:
            args = _resolve_acceptance_receipt_index_args(args, parser)
            report, json_payload, manifest_payload = _run_acceptance_receipt_index()
        elif args.visual_walkthrough_evidence_receipt:
            args = _resolve_visual_walkthrough_evidence_receipt_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_visual_walkthrough_evidence_receipt()
            )
        elif args.visual_acceptance_bundle:
            args = _resolve_visual_acceptance_bundle_args(args, parser)
            report, json_payload, manifest_payload = _run_visual_acceptance_bundle()
        elif args.beginner_prediction_checklist:
            args = _resolve_beginner_prediction_checklist_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_beginner_prediction_checklist()
            )
        elif args.prediction_readiness_audit is not None:
            args = _resolve_prediction_readiness_audit_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_prediction_readiness_audit(args)
            )
        elif args.promotion_readiness_check is not None:
            args = _resolve_promotion_readiness_check_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_promotion_readiness_check(args)
            )
        elif args.reviewer_decision_matrix:
            args = _resolve_reviewer_decision_matrix_args(args, parser)
            report, json_payload, manifest_payload = _run_reviewer_decision_matrix()
        elif args.strategy_assumption_stress_kit:
            args = _resolve_strategy_assumption_stress_kit_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_strategy_assumption_stress_kit()
            )
        elif args.stress_kit_quickstart_card:
            args = _resolve_stress_kit_quickstart_card_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_stress_kit_quickstart_card()
            )
        elif args.assumption_ledger_summary:
            args = _resolve_assumption_ledger_summary_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_assumption_ledger_summary()
            )
        elif args.static_visual_capture_checklist:
            args = _resolve_static_visual_capture_checklist_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_static_visual_capture_checklist()
            )
        elif args.static_visual_capture_receipt:
            args = _resolve_static_visual_capture_receipt_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_static_visual_capture_receipt()
            )
        elif args.static_visual_release_comparison:
            args = _resolve_static_visual_release_comparison_args(args, parser)
            report, json_payload, manifest_payload = (
                _run_static_visual_release_comparison()
            )
        else:
            args = _resolve_args(args, parser)
            if args.scenario_card:
                report, json_payload, manifest_payload = _run_scenario_card(args)
            elif args.pretrade_packet:
                report, json_payload, manifest_payload = _run_pretrade_packet(args)
            else:
                report, json_payload, manifest_payload = (
                    _run_sweep(args) if args.sweep else _run_backtest(args)
                )
        _write_outputs(args, report, json_payload, manifest_payload)
    except (OSError, ValueError, ArgumentTypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    return 0


def _reject_beginner_prediction_checklist_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.beginner_prediction_checklist:
        return

    _reject_mode_conflicts(
        args,
        parser,
        "--beginner-prediction-checklist",
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_public_demo_evidence_receipt_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.public_demo_evidence_receipt:
        return

    _reject_mode_conflicts(
        args,
        parser,
        PUBLIC_DEMO_EVIDENCE_RECEIPT_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_acceptance_receipt_index_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.acceptance_receipt_index:
        return

    _reject_mode_conflicts(
        args,
        parser,
        ACCEPTANCE_RECEIPT_INDEX_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_visual_walkthrough_evidence_receipt_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.visual_walkthrough_evidence_receipt:
        return

    _reject_mode_conflicts(
        args,
        parser,
        VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_visual_acceptance_bundle_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.visual_acceptance_bundle:
        return

    _reject_mode_conflicts(
        args,
        parser,
        VISUAL_ACCEPTANCE_BUNDLE_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
    )


def _reject_reviewer_rerun_receipt_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.reviewer_rerun_receipt:
        return

    _reject_mode_conflicts(
        args,
        parser,
        "--reviewer-rerun-receipt",
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_cold_user_review_route_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.cold_user_review_route:
        return

    _reject_mode_conflicts(
        args,
        parser,
        COLD_USER_REVIEW_ROUTE_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_prediction_readiness_audit_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if args.prediction_readiness_audit is None:
        return

    _reject_mode_conflicts(
        args,
        parser,
        PREDICTION_READINESS_AUDIT_FLAG,
        include_beginner_prediction_checklist=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_reviewer_acceptance_scorecard_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.reviewer_acceptance_scorecard:
        return

    _reject_mode_conflicts(
        args,
        parser,
        REVIEWER_ACCEPTANCE_SCORECARD_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_reviewer_decision_matrix_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.reviewer_decision_matrix:
        return

    _reject_mode_conflicts(
        args,
        parser,
        REVIEWER_DECISION_MATRIX_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_promotion_readiness_check_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if args.promotion_readiness_check is None:
        return

    _reject_mode_conflicts(
        args,
        parser,
        PROMOTION_READINESS_CHECK_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_strategy_assumption_stress_kit_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.strategy_assumption_stress_kit:
        return

    _reject_mode_conflicts(
        args,
        parser,
        STRATEGY_ASSUMPTION_STRESS_KIT_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_stress_kit_quickstart_card_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.stress_kit_quickstart_card:
        return

    _reject_mode_conflicts(
        args,
        parser,
        STRESS_KIT_QUICKSTART_CARD_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_assumption_ledger_summary_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.assumption_ledger_summary:
        return

    _reject_mode_conflicts(
        args,
        parser,
        ASSUMPTION_LEDGER_SUMMARY_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_static_visual_capture_checklist_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.static_visual_capture_checklist:
        return

    if args.public_demo_evidence_receipt:
        parser.error(
            f"{STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG} cannot be combined with "
            f"{PUBLIC_DEMO_EVIDENCE_RECEIPT_FLAG}"
        )

    _reject_mode_conflicts(
        args,
        parser,
        STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_static_visual_capture_receipt_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.static_visual_capture_receipt:
        return

    if args.static_visual_capture_checklist:
        parser.error(
            f"{STATIC_VISUAL_CAPTURE_RECEIPT_FLAG} cannot be combined with "
            f"{STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG}"
        )

    _reject_mode_conflicts(
        args,
        parser,
        STATIC_VISUAL_CAPTURE_RECEIPT_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
    )


def _reject_static_visual_release_comparison_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
) -> None:
    if not args.static_visual_release_comparison:
        return

    _reject_mode_conflicts(
        args,
        parser,
        STATIC_VISUAL_RELEASE_COMPARISON_FLAG,
        include_beginner_prediction_checklist=True,
        include_prediction_readiness_audit=True,
        include_cold_user_review_route=True,
        include_reviewer_rerun_receipt=True,
        include_reviewer_acceptance_scorecard=True,
        include_reviewer_decision_matrix=True,
        include_promotion_readiness_check=True,
        include_strategy_assumption_stress_kit=True,
        include_stress_kit_quickstart_card=True,
        include_assumption_ledger_summary=True,
        include_acceptance_receipt_index=True,
        include_visual_walkthrough_evidence_receipt=True,
        include_visual_acceptance_bundle=True,
        include_public_demo_evidence_receipt=True,
        include_static_visual_capture_checklist=True,
        include_static_visual_capture_receipt=True,
    )


def _reject_mode_conflicts(
    args: Namespace,
    parser: ArgumentParser,
    mode_flag: str,
    *,
    include_beginner_prediction_checklist: bool = False,
    include_prediction_readiness_audit: bool = False,
    include_cold_user_review_route: bool = False,
    include_reviewer_rerun_receipt: bool = False,
    include_reviewer_acceptance_scorecard: bool = False,
    include_reviewer_decision_matrix: bool = False,
    include_promotion_readiness_check: bool = False,
    include_strategy_assumption_stress_kit: bool = False,
    include_stress_kit_quickstart_card: bool = False,
    include_assumption_ledger_summary: bool = False,
    include_acceptance_receipt_index: bool = False,
    include_visual_walkthrough_evidence_receipt: bool = False,
    include_visual_acceptance_bundle: bool = False,
    include_public_demo_evidence_receipt: bool = False,
    include_static_visual_capture_checklist: bool = False,
    include_static_visual_capture_receipt: bool = False,
) -> None:
    for flag, selected in (
        ("--pretrade-packet", args.pretrade_packet),
        ("--scenario-card", args.scenario_card),
        ("--validate-thesis-ledger", args.validate_thesis_ledger is not None),
        ("--methodology-audit-template", args.methodology_audit_template),
        (
            "--methodology-audit-review-template",
            args.methodology_audit_review_template,
        ),
        ("--score-methodology-audit", args.score_methodology_audit is not None),
        ("--reviewer-evidence-bundle", args.reviewer_evidence_bundle),
        (
            "--reviewer-rerun-receipt",
            include_reviewer_rerun_receipt and args.reviewer_rerun_receipt,
        ),
        (
            REVIEWER_DECISION_MATRIX_FLAG,
            include_reviewer_decision_matrix
            and args.reviewer_decision_matrix,
        ),
        (
            "--beginner-prediction-checklist",
            include_beginner_prediction_checklist
            and args.beginner_prediction_checklist,
        ),
        (
            ACCEPTANCE_RECEIPT_INDEX_FLAG,
            include_acceptance_receipt_index and args.acceptance_receipt_index,
        ),
        (
            VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_FLAG,
            include_visual_walkthrough_evidence_receipt
            and args.visual_walkthrough_evidence_receipt,
        ),
        (
            VISUAL_ACCEPTANCE_BUNDLE_FLAG,
            include_visual_acceptance_bundle and args.visual_acceptance_bundle,
        ),
        (
            PUBLIC_DEMO_EVIDENCE_RECEIPT_FLAG,
            include_public_demo_evidence_receipt
            and args.public_demo_evidence_receipt,
        ),
        (
            STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG,
            include_static_visual_capture_checklist
            and args.static_visual_capture_checklist,
        ),
        (
            STATIC_VISUAL_CAPTURE_RECEIPT_FLAG,
            include_static_visual_capture_receipt
            and args.static_visual_capture_receipt,
        ),
        (
            PREDICTION_READINESS_AUDIT_FLAG,
            include_prediction_readiness_audit
            and args.prediction_readiness_audit is not None,
        ),
        (
            PROMOTION_READINESS_CHECK_FLAG,
            include_promotion_readiness_check
            and args.promotion_readiness_check is not None,
        ),
        (
            COLD_USER_REVIEW_ROUTE_FLAG,
            include_cold_user_review_route and args.cold_user_review_route,
        ),
        (
            REVIEWER_ACCEPTANCE_SCORECARD_FLAG,
            include_reviewer_acceptance_scorecard
            and args.reviewer_acceptance_scorecard,
        ),
        (
            STRATEGY_ASSUMPTION_STRESS_KIT_FLAG,
            include_strategy_assumption_stress_kit
            and args.strategy_assumption_stress_kit,
        ),
        (
            STRESS_KIT_QUICKSTART_CARD_FLAG,
            include_stress_kit_quickstart_card
            and args.stress_kit_quickstart_card,
        ),
        (
            ASSUMPTION_LEDGER_SUMMARY_FLAG,
            include_assumption_ledger_summary and args.assumption_ledger_summary,
        ),
        ("--regime-comparison", args.regime_comparison),
        ("--sweep", args.sweep),
        ("--symbol", args.symbol is not None),
        ("--short-window", args.short_window is not None),
        ("--long-window", args.long_window is not None),
        ("--fee-bps", args.fee_bps is not None),
        ("--short-windows", args.short_windows is not None),
        ("--long-windows", args.long_windows is not None),
        ("--top-n", args.top_n is not None),
        ("--split-ratio", args.split_ratio is not None),
        ("--split-cutoff", args.split_cutoff is not None),
    ):
        if selected:
            parser.error(f"{mode_flag} cannot be combined with {flag}")


def _write_outputs(
    args: Namespace,
    report: str,
    json_payload: dict[str, Any],
    manifest_payload: dict[str, Any],
) -> None:
    if args.output:
        _write_text(args.output, report)
    elif getattr(args, "methodology_audit_review_template", False):
        if args.json_output is None:
            print(report, end="")
    else:
        print(report, end="")

    if args.json_output:
        _write_text(args.json_output, _compact_json(json_payload))

    if args.html_output:
        _write_text(
            args.html_output,
            render_html_report(
                report,
                title=_html_report_title(args),
                artifact_links=_html_artifact_links(args),
            ),
        )

    if args.manifest_output:
        _write_text(args.manifest_output, render_manifest_markdown(manifest_payload))


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _html_report_title(args: Namespace) -> str:
    if getattr(args, "score_methodology_audit", None) is not None:
        return "Methodology Audit Score - Market Signal Lab"
    if getattr(args, "regime_comparison", False):
        return "Regime Comparison - Market Signal Lab"
    if getattr(args, "strategy_assumption_stress_kit", False):
        return STRATEGY_ASSUMPTION_STRESS_KIT_HTML_TITLE
    return "Market Signal Lab Report"


def _html_artifact_links(args: Namespace) -> tuple[tuple[str, str], ...]:
    if args.html_output is None:
        return ()

    links: list[tuple[str, str]] = []
    if getattr(args, "score_methodology_audit", None) is not None:
        for label, path in (
            ("Markdown score", args.output),
            ("JSON score", args.json_output),
        ):
            if path is not None:
                links.append((label, _relative_output_link(args.html_output, path)))
        return tuple(links)

    if getattr(args, "strategy_assumption_stress_kit", False):
        for label, path in (
            ("Markdown kit", args.output),
            ("JSON kit", args.json_output),
        ):
            if path is not None:
                links.append((label, _relative_output_link(args.html_output, path)))
        return tuple(links)

    if not getattr(args, "regime_comparison", False):
        return ()

    for label, path in (
        ("Markdown report", args.output),
        ("JSON data", args.json_output),
    ):
        if path is not None:
            links.append((label, _relative_output_link(args.html_output, path)))
    return tuple(links)


def _relative_output_link(source_path: Path, target_path: Path) -> str:
    return os.path.relpath(target_path, start=source_path.parent).replace(os.sep, "/")


def _build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="market-signal-lab",
        description="Generate static research artifacts and moving-average backtest reports.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "csv_path",
        type=Path,
        nargs="?",
        help="Path to a CSV file of OHLC data.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Optional JSON config file. CLI flags override config values.",
    )
    parser.add_argument(
        "--symbol",
        help="Filter by symbol when the input CSV contains a symbol column.",
    )
    parser.add_argument(
        "--short-window",
        type=int,
        default=None,
        help="Short moving-average window (default: 20).",
    )
    parser.add_argument(
        "--long-window",
        type=int,
        default=None,
        help="Long moving-average window (default: 50).",
    )
    parser.add_argument(
        "--fee-bps",
        type=float,
        default=None,
        help="Round-trip fee in basis points (default: 0.0).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output file path for the markdown report.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        metavar="PATH",
        help="Optional output file path for a compact JSON report.",
    )
    parser.add_argument(
        "--html-output",
        type=Path,
        help="Optional output file path for a static HTML report artifact.",
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        help="Optional output file path for a Markdown experiment manifest.",
    )
    parser.add_argument(
        "--pretrade-packet",
        action="store_true",
        default=None,
        help=(
            "Generate a research-only pre-trade packet from the single-backtest "
            "path. Requires --json-output PATH; writes Markdown via --output "
            "or stdout."
        ),
    )
    parser.add_argument(
        "--scenario-card",
        action="store_true",
        default=None,
        help=(
            "Generate a compact research-only scenario card from the "
            "single-backtest path. Defaults to reports/scenario-card.md and "
            "reports/scenario-card.json when neither --output nor "
            "--json-output is set."
        ),
    )
    parser.add_argument(
        "--validate-thesis-ledger",
        nargs="?",
        const=THESIS_LEDGER_DEFAULT_JSON,
        type=Path,
        metavar="PATH",
        help=(
            "Validate a cross-asset thesis-ledger JSON packet. When PATH is "
            "omitted, validates reports/cross-asset-thesis-ledger.json if it "
            "exists, otherwise uses the bundled demo ledger from the installed "
            "package; when no output path is supplied, writes Markdown/JSON "
            "acceptance artifacts under reports."
        ),
    )
    parser.add_argument(
        "--methodology-audit-template",
        action="store_true",
        default=False,
        help=(
            "Print or write a static Markdown methodology audit template for "
            "reviewers. Does not read CSV data, fetch live data, connect to "
            "brokers, or generate trading advice."
        ),
    )
    parser.add_argument(
        "--methodology-audit-review-template",
        action="store_true",
        default=False,
        help=(
            "Print or write a blank static methodology audit review JSON "
            "skeleton for reviewers to fill. Optional --json-output writes "
            "the JSON file. Does not read market data, fetch live data, "
            "connect to brokers, or generate trading advice."
        ),
    )
    parser.add_argument(
        "--score-methodology-audit",
        type=Path,
        metavar="PATH",
        help=(
            "Score a reviewer-filled methodology audit JSON file and print or "
            "write a static Markdown summary. Optional --json-output writes "
            "the compact score summary. Does not read market data, fetch live "
            "data, connect to brokers, or generate trading advice."
        ),
    )
    parser.add_argument(
        "--reviewer-evidence-bundle",
        action="store_true",
        default=False,
        help=(
            "Write a static reviewer evidence bundle linking the gallery, "
            "thesis-ledger acceptance route, methodology risks, and no-advice "
            "boundaries, with an artifact hash summary for local static review "
            "files. Defaults to reports/reviewer-evidence-bundle.md and "
            "reports/reviewer-evidence-bundle.json."
        ),
    )
    parser.add_argument(
        PUBLIC_DEMO_EVIDENCE_RECEIPT_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic public demo evidence receipt covering "
            "static gallery/backtest artifacts, source fixture boundaries, "
            "artifact hashes, and no-live-data/no-advice claims. Defaults to "
            f"{PUBLIC_DEMO_EVIDENCE_RECEIPT_OUTPUT} and "
            f"{PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON_OUTPUT}. Does not read live "
            "market data, connect to brokers, inspect accounts, route orders, "
            "size positions, forecast, recommend, or provide investment advice."
        ),
    )
    parser.add_argument(
        "--reviewer-rerun-receipt",
        action="store_true",
        default=False,
        help=(
            "Write a static reviewer rerun receipt with exact public verification "
            "commands, expected artifacts, no-live-data/no-advice boundaries, and "
            "a PASS/WARN checklist. Defaults to "
            "reports/reviewer-rerun-receipt.md and "
            "reports/reviewer-rerun-receipt.json. Does not read CSV data, fetch "
            "live data, connect to brokers, inspect accounts, route orders, size "
            "positions, forecast, recommend, or provide investment advice."
        ),
    )
    parser.add_argument(
        ACCEPTANCE_RECEIPT_INDEX_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic acceptance receipt index linking the "
            "public demo evidence receipt, reviewer rerun receipt, reviewer "
            "evidence bundle, fixture provenance, artifact hashes, and "
            "no-live-data/no-advice boundaries. Defaults to "
            f"{ACCEPTANCE_RECEIPT_INDEX_OUTPUT} and "
            f"{ACCEPTANCE_RECEIPT_INDEX_JSON_OUTPUT}. Does not read CSV data, "
            "fetch live data, connect to brokers, inspect accounts, route "
            "orders, size positions, forecast, recommend, or provide "
            "investment advice."
        ),
    )
    parser.add_argument(
        VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic visual walkthrough evidence receipt tying "
            "docs/static-gallery-walkthrough.svg, reports/index.html, the "
            "public demo evidence receipt, reviewer rerun receipt, and "
            "acceptance receipt index into one cold-review route. Defaults to "
            f"{VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_OUTPUT} and "
            f"{VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_JSON_OUTPUT}. Does not read "
            "CSV data, fetch live data, connect to brokers, inspect accounts, "
            "route orders, size positions, forecast, recommend, or provide "
            "investment advice."
        ),
    )
    parser.add_argument(
        VISUAL_ACCEPTANCE_BUNDLE_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic bounded visual acceptance bundle tying the "
            "static visual walkthrough, gallery first screen, visual receipt, "
            "acceptance receipt index, reviewer acceptance scorecard, "
            "cold-user route, artifact hashes, and no-live-data/no-advice "
            "boundaries together. Defaults to "
            f"{VISUAL_ACCEPTANCE_BUNDLE_OUTPUT} and "
            f"{VISUAL_ACCEPTANCE_BUNDLE_JSON_OUTPUT}. Does not read CSV data, "
            "fetch live data, connect to brokers, inspect accounts, route "
            "orders, size positions, forecast, recommend, or provide "
            "investment advice."
        ),
    )
    parser.add_argument(
        REVIEWER_ACCEPTANCE_SCORECARD_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic reviewer acceptance scorecard summarizing "
            "public-review readiness, reproducibility evidence, risk "
            "boundaries, and next actions using existing static artifact "
            "paths. Defaults to reports/reviewer-acceptance-scorecard.md and "
            "reports/reviewer-acceptance-scorecard.json. Does not read CSV "
            "data, fetch live data, connect to brokers, create orders, size "
            "positions, or provide forecasts, recommendations, trading "
            "instructions, or investment advice."
        ),
    )
    parser.add_argument(
        COLD_USER_REVIEW_ROUTE_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic cold-user review route and checklist for "
            "checked-in static artifacts, including repo-relative artifact "
            "hashes and public review boundaries. Defaults to "
            "reports/cold-user-review-route.md and "
            "reports/cold-user-review-route.json. Does not read CSV data, "
            "fetch live data, connect to brokers, create orders, size "
            "positions, or provide forecasts, recommendations, or investment "
            "advice."
        ),
    )
    parser.add_argument(
        "--beginner-prediction-checklist",
        action="store_true",
        default=False,
        help=(
            "Write a static beginner checklist explaining how to read historical "
            "backtest and related checklist artifacts without treating them as "
            "predictions of future returns, recommendations, or advice. Does "
            "not read CSV data, fetch live data, connect to brokers, create "
            "orders, size positions, or use strategy parameters. Only --output and "
            "--json-output customize its files; defaults to "
            "reports/beginner-prediction-checklist.md and "
            "reports/beginner-prediction-checklist.json."
        ),
    )
    parser.add_argument(
        REVIEWER_DECISION_MATRIX_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a static reviewer decision matrix for deciding whether a "
            "static backtest artifact is safe to release and safe to promote. "
            "Does not read CSV data, fetch live data, connect to brokers, "
            "create orders, size positions, forecast, recommend, or provide "
            "investment advice. Only --output and --json-output customize files; "
            "defaults to reports/reviewer-decision-matrix.md and "
            "reports/reviewer-decision-matrix.json."
        ),
    )
    parser.add_argument(
        PREDICTION_READINESS_AUDIT_FLAG,
        nargs="?",
        const=THESIS_LEDGER_DEFAULT_JSON,
        type=Path,
        metavar="PATH",
        help=(
            "Audit a static thesis-ledger JSON artifact for prediction-readiness "
            "review labels. When PATH is omitted, reads "
            "reports/cross-asset-thesis-ledger.json if it exists, otherwise "
            "uses the bundled demo ledger. Only --output and --json-output "
            "customize files; defaults to reports/prediction-readiness-audit.md "
            "and reports/prediction-readiness-audit.json when neither is set. "
            "Uses only a static JSON artifact and does not provide forecasts, "
            "recommendations, trading instructions, or investment advice."
        ),
    )
    parser.add_argument(
        PROMOTION_READINESS_CHECK_FLAG,
        nargs="?",
        const=PROMOTION_READINESS_CHECK_DEFAULT_INPUT,
        type=Path,
        metavar="PATH",
        help=(
            "Run a focused public-promotion readiness check on a static "
            "cross-asset thesis-ledger JSON artifact. When PATH is omitted, "
            "reads reports/cross-asset-thesis-ledger.json if it exists, "
            "otherwise uses the bundled demo ledger. Only --output and "
            "--json-output customize files; defaults to "
            "reports/promotion-readiness-check.md and "
            "reports/promotion-readiness-check.json when neither is set. "
            "Reports release/promotion gates, no-live-data/no-advice "
            "boundaries, benchmark/fee/drawdown/train-test/leveraged caveat "
            "evidence, and next fixes without forecasts, recommendations, "
            "trading instructions, or investment advice."
        ),
    )
    parser.add_argument(
        STRATEGY_ASSUMPTION_STRESS_KIT_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic static strategy assumption stress kit "
            "covering assumptions, stress checks, beginner risk boundaries, "
            "and leveraged ETF-like path dependency, volatility drag, and "
            f"extreme drawdown caveats. Defaults to "
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_HTML_OUTPUT}, "
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_OUTPUT}, and "
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_JSON_OUTPUT}; --html-output can "
            "customize the browser-openable artifact path. Does not read CSV "
            "data, fetch live data, connect to brokers, create orders, size "
            "positions, use strategy parameters, forecast, recommend, or "
            "provide investment advice."
        ),
    )
    parser.add_argument(
        STRESS_KIT_QUICKSTART_CARD_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic two-minute quickstart card that condenses "
            "the Strategy Assumption Stress Kit into the shortest reviewer "
            "entry point; open the Markdown output first. "
            f"Defaults to {STRESS_KIT_QUICKSTART_CARD_OUTPUT} and "
            f"{STRESS_KIT_QUICKSTART_CARD_JSON_OUTPUT}. Does not read CSV "
            "data, fetch live data, connect to brokers, create orders, size "
            "positions, forecast, recommend, or provide investment advice."
        ),
    )
    parser.add_argument(
        ASSUMPTION_LEDGER_SUMMARY_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic static assumption ledger summary for cold "
            "reviewers, covering strategy assumptions, risk boundaries, "
            "generated evidence paths, and explicit non-claims. Defaults to "
            f"{ASSUMPTION_LEDGER_SUMMARY_OUTPUT} and "
            f"{ASSUMPTION_LEDGER_SUMMARY_JSON_OUTPUT}. Does not read CSV "
            "data, fetch live data, connect to brokers, create orders, size "
            "positions, forecast, recommend, or provide investment advice."
        ),
    )
    parser.add_argument(
        STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic static visual capture checklist for cold "
            "reviewers who need to capture a local static gallery screenshot "
            "or GIF while preserving public-safe no-live-data, no-broker, "
            "no-order, no-position-sizing, no-forecast, no-recommendation, "
            "and no-advice boundaries. Defaults to "
            f"{STATIC_VISUAL_CAPTURE_CHECKLIST_OUTPUT} and "
            f"{STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_OUTPUT}. Does not capture "
            "images, read CSV data, fetch live data, connect to brokers, "
            "create orders, size positions, forecast, recommend, or provide "
            "investment advice."
        ),
    )
    parser.add_argument(
        STATIC_VISUAL_CAPTURE_RECEIPT_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic static visual capture receipt that scans "
            "existing static visual, gallery, walkthrough, route, and checklist "
            "artifacts, recording relative paths, present/missing status, "
            "bytes, SHA-256, roles, routes, known regeneration commands, and "
            "public evidence notes. Defaults to "
            f"{STATIC_VISUAL_CAPTURE_RECEIPT_OUTPUT} and "
            f"{STATIC_VISUAL_CAPTURE_RECEIPT_JSON_OUTPUT}. Does not capture "
            "images, read CSV data, fetch live data, connect to brokers, "
            "inspect accounts, create orders, size positions, forecast, "
            "recommend, or provide investment advice."
        ),
    )
    parser.add_argument(
        STATIC_VISUAL_RELEASE_COMPARISON_FLAG,
        action="store_true",
        default=False,
        help=(
            "Write a deterministic release-to-release static visual receipt "
            "comparison using existing static visual capture receipt artifacts, "
            "the v1.30.7 receipt baseline, current repo-relative artifact "
            "presence, SHA-256 hashes, and a reviewer checklist. Defaults to "
            f"{STATIC_VISUAL_RELEASE_COMPARISON_OUTPUT} and "
            f"{STATIC_VISUAL_RELEASE_COMPARISON_JSON_OUTPUT}. Does not fetch "
            "release tags, capture images, read CSV data, fetch live data, "
            "connect to brokers, inspect accounts, create orders, size "
            "positions, forecast, recommend, or provide investment advice."
        ),
    )
    parser.add_argument(
        "--regime-comparison",
        action="store_true",
        default=False,
        help=(
            "Run bundled bull/choppy/drawdown-recovery demo configs, usable "
            "from an empty current directory after wheel install, and write "
            "Markdown/JSON/HTML comparison artifacts under reports by default."
        ),
    )
    parser.add_argument(
        "--sweep",
        action="store_true",
        default=None,
        help="Run a moving-average parameter sweep instead of a single report.",
    )
    parser.add_argument(
        "--short-windows",
        type=_parse_integer_list,
        default=None,
        help="Comma-separated short-window values for --sweep (default: 10,20,50).",
    )
    parser.add_argument(
        "--long-windows",
        type=_parse_integer_list,
        default=None,
        help="Comma-separated long-window values for --sweep (default: 50,100,200).",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        help="Limit --sweep output to the top N ranked results.",
    )
    split_group = parser.add_mutually_exclusive_group()
    split_group.add_argument(
        "--split-ratio",
        type=_parse_split_ratio,
        metavar="RATIO",
        help=(
            "Use the first RATIO share of rows for training and the rest for "
            "testing; with --sweep, adds train/test rank and return-gap "
            "diagnostics. Must be greater than 0 and less than 1."
        ),
    )
    split_group.add_argument(
        "--split-cutoff",
        metavar="YYYY-MM-DD",
        help=(
            "Use rows before this date for training and rows on or after it "
            "for testing; with --sweep, adds train/test rank and return-gap "
            "diagnostics."
        ),
    )
    return parser


def _resolve_args(args: Namespace, parser: ArgumentParser) -> Namespace:
    config_values = _load_config(args.config) if args.config else {}
    if args.split_ratio is not None:
        config_values.pop("split_cutoff", None)
    if args.split_cutoff is not None:
        config_values.pop("split_ratio", None)

    resolved = Namespace()
    for key, default in _default_args().items():
        value = getattr(args, key)
        if value is None and key in config_values:
            value = config_values[key]
        if value is None:
            value = default
        setattr(resolved, key, value)

    resolved.config = args.config
    if resolved.csv_path is None:
        parser.error("the following arguments are required: csv_path")
    if resolved.pretrade_packet and resolved.sweep:
        parser.error("--pretrade-packet uses the single-backtest path, not --sweep")
    if resolved.scenario_card and resolved.sweep:
        parser.error("--scenario-card uses the single-backtest path, not --sweep")
    if resolved.pretrade_packet and resolved.scenario_card:
        parser.error("choose only one card mode: --pretrade-packet or --scenario-card")
    if resolved.pretrade_packet and resolved.json_output is None:
        parser.error("--pretrade-packet requires --json-output PATH")
    if (
        resolved.scenario_card
        and resolved.output is None
        and resolved.json_output is None
    ):
        resolved.output = SCENARIO_CARD_OUTPUT
        resolved.json_output = SCENARIO_CARD_JSON_OUTPUT
    if resolved.split_ratio is not None and resolved.split_cutoff is not None:
        parser.error(
            "choose only one validation split option: --split-ratio or "
            "--split-cutoff (config keys: split_ratio or split_cutoff)"
        )

    return resolved


def _resolve_regime_comparison_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error("--regime-comparison uses bundled configs and does not take csv_path")
    if args.config is not None:
        parser.error("--regime-comparison uses bundled configs and does not take --config")
    if args.pretrade_packet:
        parser.error("--pretrade-packet cannot be combined with --regime-comparison")
    if args.scenario_card:
        parser.error("--scenario-card cannot be combined with --regime-comparison")

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))

    resolved.output = args.output or REGIME_COMPARISON_OUTPUT
    resolved.json_output = args.json_output or REGIME_COMPARISON_JSON_OUTPUT
    resolved.html_output = args.html_output or REGIME_COMPARISON_HTML_OUTPUT
    resolved.manifest_output = args.manifest_output
    resolved.configs = BUNDLED_REGIME_CONFIGS
    resolved.regime_comparison = True
    return resolved


def _resolve_thesis_ledger_validation_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.config is not None:
        parser.error("--validate-thesis-ledger does not take --config")
    if args.regime_comparison:
        parser.error("--validate-thesis-ledger cannot be combined with --regime-comparison")
    if args.pretrade_packet:
        parser.error("--validate-thesis-ledger cannot be combined with --pretrade-packet")
    if args.scenario_card:
        parser.error("--validate-thesis-ledger cannot be combined with --scenario-card")
    if args.sweep:
        parser.error("--validate-thesis-ledger cannot be combined with --sweep")
    if args.html_output is not None:
        parser.error("--validate-thesis-ledger writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error("--validate-thesis-ledger does not write experiment manifests")

    input_path = args.validate_thesis_ledger
    if args.csv_path is not None:
        if input_path != THESIS_LEDGER_DEFAULT_JSON:
            parser.error(
                "--validate-thesis-ledger accepts only one ledger JSON path"
            )
        input_path = args.csv_path

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.thesis_ledger_json = input_path
    resolved.output = args.output
    resolved.json_output = args.json_output
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.validate_thesis_ledger = input_path
    if resolved.output is None and resolved.json_output is None:
        resolved.output = THESIS_LEDGER_ACCEPTANCE_OUTPUT
        resolved.json_output = THESIS_LEDGER_ACCEPTANCE_JSON_OUTPUT
    return resolved


def _resolve_reviewer_evidence_bundle_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error("--reviewer-evidence-bundle does not take csv_path")
    if args.config is not None:
        parser.error("--reviewer-evidence-bundle does not take --config")
    if args.pretrade_packet:
        parser.error("--reviewer-evidence-bundle cannot be combined with --pretrade-packet")
    if args.scenario_card:
        parser.error("--reviewer-evidence-bundle cannot be combined with --scenario-card")
    if args.validate_thesis_ledger is not None:
        parser.error(
            "--reviewer-evidence-bundle cannot be combined with "
            "--validate-thesis-ledger"
        )
    if args.methodology_audit_template:
        parser.error(
            "--reviewer-evidence-bundle cannot be combined with "
            "--methodology-audit-template"
        )
    if args.methodology_audit_review_template:
        parser.error(
            "--reviewer-evidence-bundle cannot be combined with "
            "--methodology-audit-review-template"
        )
    if args.score_methodology_audit is not None:
        parser.error(
            "--reviewer-evidence-bundle cannot be combined with "
            "--score-methodology-audit"
        )
    if args.reviewer_acceptance_scorecard:
        parser.error(
            "--reviewer-evidence-bundle cannot be combined with "
            f"{REVIEWER_ACCEPTANCE_SCORECARD_FLAG}"
        )
    if args.regime_comparison:
        parser.error("--reviewer-evidence-bundle cannot be combined with --regime-comparison")
    if args.sweep:
        parser.error("--reviewer-evidence-bundle cannot be combined with --sweep")
    if args.html_output is not None:
        parser.error("--reviewer-evidence-bundle writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error("--reviewer-evidence-bundle does not write experiment manifests")

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or REVIEWER_EVIDENCE_BUNDLE_OUTPUT
    resolved.json_output = args.json_output or REVIEWER_EVIDENCE_BUNDLE_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.reviewer_evidence_bundle = True
    return resolved


def _resolve_public_demo_evidence_receipt_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{PUBLIC_DEMO_EVIDENCE_RECEIPT_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{PUBLIC_DEMO_EVIDENCE_RECEIPT_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(
            f"{PUBLIC_DEMO_EVIDENCE_RECEIPT_FLAG} writes Markdown/JSON, not HTML"
        )
    if args.manifest_output is not None:
        parser.error(
            f"{PUBLIC_DEMO_EVIDENCE_RECEIPT_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or PUBLIC_DEMO_EVIDENCE_RECEIPT_OUTPUT
    resolved.json_output = args.json_output or PUBLIC_DEMO_EVIDENCE_RECEIPT_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.public_demo_evidence_receipt = True
    return resolved


def _resolve_acceptance_receipt_index_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{ACCEPTANCE_RECEIPT_INDEX_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{ACCEPTANCE_RECEIPT_INDEX_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(f"{ACCEPTANCE_RECEIPT_INDEX_FLAG} writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error(
            f"{ACCEPTANCE_RECEIPT_INDEX_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or ACCEPTANCE_RECEIPT_INDEX_OUTPUT
    resolved.json_output = args.json_output or ACCEPTANCE_RECEIPT_INDEX_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.acceptance_receipt_index = True
    return resolved


def _resolve_visual_walkthrough_evidence_receipt_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(
            f"{VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_FLAG} does not take csv_path"
        )
    if args.config is not None:
        parser.error(
            f"{VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_FLAG} does not take --config"
        )
    if args.html_output is not None:
        parser.error(
            f"{VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_FLAG} writes Markdown/JSON, not HTML"
        )
    if args.manifest_output is not None:
        parser.error(
            f"{VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_OUTPUT
    resolved.json_output = (
        args.json_output or VISUAL_WALKTHROUGH_EVIDENCE_RECEIPT_JSON_OUTPUT
    )
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.visual_walkthrough_evidence_receipt = True
    return resolved


def _resolve_visual_acceptance_bundle_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{VISUAL_ACCEPTANCE_BUNDLE_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{VISUAL_ACCEPTANCE_BUNDLE_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(f"{VISUAL_ACCEPTANCE_BUNDLE_FLAG} writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error(
            f"{VISUAL_ACCEPTANCE_BUNDLE_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or VISUAL_ACCEPTANCE_BUNDLE_OUTPUT
    resolved.json_output = args.json_output or VISUAL_ACCEPTANCE_BUNDLE_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.visual_acceptance_bundle = True
    return resolved


def _resolve_reviewer_acceptance_scorecard_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{REVIEWER_ACCEPTANCE_SCORECARD_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{REVIEWER_ACCEPTANCE_SCORECARD_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(
            f"{REVIEWER_ACCEPTANCE_SCORECARD_FLAG} writes Markdown/JSON, not HTML"
        )
    if args.manifest_output is not None:
        parser.error(
            f"{REVIEWER_ACCEPTANCE_SCORECARD_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or REVIEWER_ACCEPTANCE_SCORECARD_OUTPUT
    resolved.json_output = (
        args.json_output or REVIEWER_ACCEPTANCE_SCORECARD_JSON_OUTPUT
    )
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.reviewer_acceptance_scorecard = True
    return resolved


def _resolve_cold_user_review_route_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{COLD_USER_REVIEW_ROUTE_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{COLD_USER_REVIEW_ROUTE_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(f"{COLD_USER_REVIEW_ROUTE_FLAG} writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error(
            f"{COLD_USER_REVIEW_ROUTE_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or COLD_USER_REVIEW_ROUTE_OUTPUT
    resolved.json_output = args.json_output or COLD_USER_REVIEW_ROUTE_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.cold_user_review_route = True
    return resolved


def _resolve_reviewer_rerun_receipt_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error("--reviewer-rerun-receipt does not take csv_path")
    if args.config is not None:
        parser.error("--reviewer-rerun-receipt does not take --config")
    if args.html_output is not None:
        parser.error("--reviewer-rerun-receipt writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error("--reviewer-rerun-receipt does not write experiment manifests")

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or REVIEWER_RERUN_RECEIPT_OUTPUT
    resolved.json_output = args.json_output or REVIEWER_RERUN_RECEIPT_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.reviewer_rerun_receipt = True
    return resolved


def _resolve_beginner_prediction_checklist_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error("--beginner-prediction-checklist does not take csv_path")
    if args.config is not None:
        parser.error("--beginner-prediction-checklist does not take --config")
    if args.html_output is not None:
        parser.error("--beginner-prediction-checklist writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error(
            "--beginner-prediction-checklist does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or BEGINNER_PREDICTION_CHECKLIST_OUTPUT
    resolved.json_output = (
        args.json_output or BEGINNER_PREDICTION_CHECKLIST_JSON_OUTPUT
    )
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.beginner_prediction_checklist = True
    return resolved


def _resolve_reviewer_decision_matrix_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error("--reviewer-decision-matrix does not take csv_path")
    if args.config is not None:
        parser.error("--reviewer-decision-matrix does not take --config")
    if args.html_output is not None:
        parser.error("--reviewer-decision-matrix writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error(
            "--reviewer-decision-matrix does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or REVIEWER_DECISION_MATRIX_OUTPUT
    resolved.json_output = args.json_output or REVIEWER_DECISION_MATRIX_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.reviewer_decision_matrix = True
    return resolved


def _resolve_prediction_readiness_audit_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.config is not None:
        parser.error(f"{PREDICTION_READINESS_AUDIT_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(
            f"{PREDICTION_READINESS_AUDIT_FLAG} writes Markdown/JSON, not HTML"
        )
    if args.manifest_output is not None:
        parser.error(
            f"{PREDICTION_READINESS_AUDIT_FLAG} does not write experiment manifests"
        )

    input_path = args.prediction_readiness_audit
    if args.csv_path is not None:
        if input_path != THESIS_LEDGER_DEFAULT_JSON:
            parser.error(
                f"{PREDICTION_READINESS_AUDIT_FLAG} accepts only one ledger "
                "JSON path"
            )
        input_path = args.csv_path

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.prediction_readiness_audit = input_path
    resolved.output = args.output
    resolved.json_output = args.json_output
    if resolved.output is None and resolved.json_output is None:
        resolved.output = PREDICTION_READINESS_AUDIT_OUTPUT
        resolved.json_output = PREDICTION_READINESS_AUDIT_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    return resolved


def _resolve_promotion_readiness_check_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.config is not None:
        parser.error(f"{PROMOTION_READINESS_CHECK_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(
            f"{PROMOTION_READINESS_CHECK_FLAG} writes Markdown/JSON, not HTML"
        )
    if args.manifest_output is not None:
        parser.error(
            f"{PROMOTION_READINESS_CHECK_FLAG} does not write experiment manifests"
        )

    input_path = args.promotion_readiness_check
    if args.csv_path is not None:
        if input_path is not PROMOTION_READINESS_CHECK_DEFAULT_INPUT:
            parser.error(
                f"{PROMOTION_READINESS_CHECK_FLAG} accepts only one ledger JSON path"
            )
        input_path = args.csv_path
    elif input_path is PROMOTION_READINESS_CHECK_DEFAULT_INPUT:
        input_path = THESIS_LEDGER_DEFAULT_JSON

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.promotion_readiness_check = input_path
    resolved.output = args.output
    resolved.json_output = args.json_output
    if resolved.output is None and resolved.json_output is None:
        resolved.output = PROMOTION_READINESS_CHECK_OUTPUT
        resolved.json_output = PROMOTION_READINESS_CHECK_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    return resolved


def _resolve_strategy_assumption_stress_kit_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{STRATEGY_ASSUMPTION_STRESS_KIT_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{STRATEGY_ASSUMPTION_STRESS_KIT_FLAG} does not take --config")
    if args.manifest_output is not None:
        parser.error(
            f"{STRATEGY_ASSUMPTION_STRESS_KIT_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output
    resolved.json_output = args.json_output
    resolved.html_output = args.html_output
    if (
        resolved.output is None
        and resolved.json_output is None
        and resolved.html_output is None
    ):
        resolved.output = STRATEGY_ASSUMPTION_STRESS_KIT_OUTPUT
        resolved.json_output = STRATEGY_ASSUMPTION_STRESS_KIT_JSON_OUTPUT
        resolved.html_output = STRATEGY_ASSUMPTION_STRESS_KIT_HTML_OUTPUT
    elif resolved.html_output is not None:
        resolved.output = resolved.output or STRATEGY_ASSUMPTION_STRESS_KIT_OUTPUT
        resolved.json_output = (
            resolved.json_output or STRATEGY_ASSUMPTION_STRESS_KIT_JSON_OUTPUT
        )
    resolved.manifest_output = None
    resolved.strategy_assumption_stress_kit = True
    return resolved


def _resolve_stress_kit_quickstart_card_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{STRESS_KIT_QUICKSTART_CARD_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{STRESS_KIT_QUICKSTART_CARD_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(f"{STRESS_KIT_QUICKSTART_CARD_FLAG} writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error(
            f"{STRESS_KIT_QUICKSTART_CARD_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or STRESS_KIT_QUICKSTART_CARD_OUTPUT
    resolved.json_output = args.json_output or STRESS_KIT_QUICKSTART_CARD_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.stress_kit_quickstart_card = True
    return resolved


def _resolve_assumption_ledger_summary_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{ASSUMPTION_LEDGER_SUMMARY_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{ASSUMPTION_LEDGER_SUMMARY_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(f"{ASSUMPTION_LEDGER_SUMMARY_FLAG} writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error(
            f"{ASSUMPTION_LEDGER_SUMMARY_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or ASSUMPTION_LEDGER_SUMMARY_OUTPUT
    resolved.json_output = args.json_output or ASSUMPTION_LEDGER_SUMMARY_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.assumption_ledger_summary = True
    return resolved


def _resolve_static_visual_capture_checklist_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(
            f"{STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG} writes Markdown/JSON, not HTML"
        )
    if args.manifest_output is not None:
        parser.error(
            f"{STATIC_VISUAL_CAPTURE_CHECKLIST_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or STATIC_VISUAL_CAPTURE_CHECKLIST_OUTPUT
    resolved.json_output = (
        args.json_output or STATIC_VISUAL_CAPTURE_CHECKLIST_JSON_OUTPUT
    )
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.static_visual_capture_checklist = True
    return resolved


def _resolve_static_visual_capture_receipt_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{STATIC_VISUAL_CAPTURE_RECEIPT_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{STATIC_VISUAL_CAPTURE_RECEIPT_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(
            f"{STATIC_VISUAL_CAPTURE_RECEIPT_FLAG} writes Markdown/JSON, not HTML"
        )
    if args.manifest_output is not None:
        parser.error(
            f"{STATIC_VISUAL_CAPTURE_RECEIPT_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or STATIC_VISUAL_CAPTURE_RECEIPT_OUTPUT
    resolved.json_output = args.json_output or STATIC_VISUAL_CAPTURE_RECEIPT_JSON_OUTPUT
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.static_visual_capture_receipt = True
    return resolved


def _resolve_static_visual_release_comparison_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error(f"{STATIC_VISUAL_RELEASE_COMPARISON_FLAG} does not take csv_path")
    if args.config is not None:
        parser.error(f"{STATIC_VISUAL_RELEASE_COMPARISON_FLAG} does not take --config")
    if args.html_output is not None:
        parser.error(
            f"{STATIC_VISUAL_RELEASE_COMPARISON_FLAG} writes Markdown/JSON, not HTML"
        )
    if args.manifest_output is not None:
        parser.error(
            f"{STATIC_VISUAL_RELEASE_COMPARISON_FLAG} does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output or STATIC_VISUAL_RELEASE_COMPARISON_OUTPUT
    resolved.json_output = (
        args.json_output or STATIC_VISUAL_RELEASE_COMPARISON_JSON_OUTPUT
    )
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.static_visual_release_comparison = True
    return resolved


def _resolve_methodology_audit_template_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error("--methodology-audit-template does not take csv_path")
    if args.config is not None:
        parser.error("--methodology-audit-template does not take --config")
    if args.pretrade_packet:
        parser.error(
            "--methodology-audit-template cannot be combined with --pretrade-packet"
        )
    if args.scenario_card:
        parser.error(
            "--methodology-audit-template cannot be combined with --scenario-card"
        )
    if args.validate_thesis_ledger is not None:
        parser.error(
            "--methodology-audit-template cannot be combined with "
            "--validate-thesis-ledger"
        )
    if args.regime_comparison:
        parser.error(
            "--methodology-audit-template cannot be combined with --regime-comparison"
        )
    if args.sweep:
        parser.error("--methodology-audit-template cannot be combined with --sweep")
    if args.html_output is not None:
        parser.error("--methodology-audit-template writes Markdown/JSON, not HTML")
    if args.manifest_output is not None:
        parser.error("--methodology-audit-template does not write experiment manifests")

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output
    resolved.json_output = args.json_output
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.methodology_audit_template = True
    return resolved


def _resolve_methodology_audit_review_template_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error("--methodology-audit-review-template does not take csv_path")
    if args.config is not None:
        parser.error("--methodology-audit-review-template does not take --config")
    if args.output is not None:
        parser.error(
            "--methodology-audit-review-template writes JSON via stdout or "
            "--json-output, not Markdown"
        )
    if args.pretrade_packet:
        parser.error(
            "--methodology-audit-review-template cannot be combined with "
            "--pretrade-packet"
        )
    if args.scenario_card:
        parser.error(
            "--methodology-audit-review-template cannot be combined with "
            "--scenario-card"
        )
    if args.validate_thesis_ledger is not None:
        parser.error(
            "--methodology-audit-review-template cannot be combined with "
            "--validate-thesis-ledger"
        )
    if args.methodology_audit_template:
        parser.error(
            "--methodology-audit-review-template cannot be combined with "
            "--methodology-audit-template"
        )
    if args.score_methodology_audit is not None:
        parser.error(
            "--methodology-audit-review-template cannot be combined with "
            "--score-methodology-audit"
        )
    if args.regime_comparison:
        parser.error(
            "--methodology-audit-review-template cannot be combined with "
            "--regime-comparison"
        )
    if args.sweep:
        parser.error(
            "--methodology-audit-review-template cannot be combined with --sweep"
        )
    if args.html_output is not None:
        parser.error("--methodology-audit-review-template writes JSON, not HTML")
    if args.manifest_output is not None:
        parser.error(
            "--methodology-audit-review-template does not write experiment manifests"
        )

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = None
    resolved.json_output = args.json_output
    resolved.html_output = None
    resolved.manifest_output = None
    resolved.methodology_audit_review_template = True
    return resolved


def _resolve_methodology_audit_score_args(
    args: Namespace,
    parser: ArgumentParser,
) -> Namespace:
    if args.csv_path is not None:
        parser.error("--score-methodology-audit does not take csv_path")
    if args.config is not None:
        parser.error("--score-methodology-audit does not take --config")
    if args.pretrade_packet:
        parser.error(
            "--score-methodology-audit cannot be combined with --pretrade-packet"
        )
    if args.scenario_card:
        parser.error(
            "--score-methodology-audit cannot be combined with --scenario-card"
        )
    if args.validate_thesis_ledger is not None:
        parser.error(
            "--score-methodology-audit cannot be combined with "
            "--validate-thesis-ledger"
        )
    if args.methodology_audit_template:
        parser.error(
            "--score-methodology-audit cannot be combined with "
            "--methodology-audit-template"
        )
    if args.methodology_audit_review_template:
        parser.error(
            "--score-methodology-audit cannot be combined with "
            "--methodology-audit-review-template"
        )
    if args.regime_comparison:
        parser.error(
            "--score-methodology-audit cannot be combined with --regime-comparison"
        )
    if args.sweep:
        parser.error("--score-methodology-audit cannot be combined with --sweep")
    if args.manifest_output is not None:
        parser.error("--score-methodology-audit does not write experiment manifests")

    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, getattr(args, key, default))
    resolved.csv_path = None
    resolved.output = args.output
    resolved.json_output = args.json_output
    resolved.html_output = args.html_output
    resolved.manifest_output = None
    resolved.score_methodology_audit = args.score_methodology_audit
    return resolved


def _default_args() -> dict[str, Any]:
    return {
        "csv_path": None,
        "symbol": None,
        "short_window": 20,
        "long_window": 50,
        "fee_bps": 0.0,
        "output": None,
        "json_output": None,
        "html_output": None,
        "manifest_output": None,
        "sweep": False,
        "short_windows": (10, 20, 50),
        "long_windows": (50, 100, 200),
        "top_n": None,
        "split_ratio": None,
        "split_cutoff": None,
        "pretrade_packet": False,
        "scenario_card": False,
    }


def _load_config(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(), parse_constant=_reject_json_constant)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON config {path}: {exc.msg}") from exc

    if not isinstance(raw, dict):
        raise ValueError("Config file must contain a JSON object")

    allowed_keys = set(_default_args())
    unknown_keys = sorted(set(raw) - allowed_keys)
    if unknown_keys:
        keys = ", ".join(unknown_keys)
        raise ValueError(f"Unknown config option(s): {keys}")

    return {
        key: _coerce_config_value(key, value)
        for key, value in raw.items()
        if value is not None
    }


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"Invalid JSON constant: {value}")


def _coerce_config_value(key: str, value: Any) -> Any:
    if key in {"csv_path", "output", "json_output", "html_output", "manifest_output"}:
        if not isinstance(value, str):
            raise ValueError(f"Config option {key!r} must be a string path")
        return Path(value)
    if key in {"symbol", "split_cutoff"}:
        if not isinstance(value, str):
            raise ValueError(f"Config option {key!r} must be a string")
        return value
    if key in {"short_window", "long_window", "top_n"}:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"Config option {key!r} must be an integer")
        return value
    if key == "fee_bps":
        if not isinstance(value, int | float) or isinstance(value, bool):
            raise ValueError("Config option 'fee_bps' must be numeric")
        return float(value)
    if key == "sweep":
        if not isinstance(value, bool):
            raise ValueError("Config option 'sweep' must be a boolean")
        return value
    if key == "pretrade_packet":
        if not isinstance(value, bool):
            raise ValueError("Config option 'pretrade_packet' must be a boolean")
        return value
    if key == "scenario_card":
        if not isinstance(value, bool):
            raise ValueError("Config option 'scenario_card' must be a boolean")
        return value
    if key in {"short_windows", "long_windows"}:
        return _coerce_config_integer_list(key, value)
    if key == "split_ratio":
        if not isinstance(value, int | float) or isinstance(value, bool):
            raise ValueError("Config option 'split_ratio' must be numeric")
        return _parse_split_ratio(str(value))

    raise ValueError(f"Unsupported config option: {key}")


def _coerce_config_integer_list(key: str, value: Any) -> tuple[int, ...]:
    if isinstance(value, str):
        return _parse_integer_list(value)
    if not isinstance(value, list):
        raise ValueError(f"Config option {key!r} must be a list of integers")
    if not value:
        raise ValueError(f"Config option {key!r} must not be empty")
    if not all(isinstance(item, int) and not isinstance(item, bool) for item in value):
        raise ValueError(f"Config option {key!r} must be a list of integers")

    return tuple(value)


def _run_backtest(args: Namespace) -> tuple[str, dict[str, Any], dict[str, Any]]:
    csv_path = Path(args.csv_path)
    provenance = _load_provenance_payload(csv_path)
    bars = _load_bars(csv_path, symbol=args.symbol)
    split = _build_validation_split(args, bars)
    validation_split = _build_validation_split_metadata(args, split)
    signals = moving_average_crossover_strategy(
        bars,
        short_window=args.short_window,
        long_window=args.long_window,
    )
    target_exposures = [signal.target_exposure for signal in signals]
    backtest_curve = backtest_long_cash(
        bars=bars,
        target_exposures=target_exposures,
        fee_bps=args.fee_bps,
    )

    strategy_returns = [record.strategy_return for record in backtest_curve[1:]]
    buy_and_hold_returns = [record.market_return for record in backtest_curve[1:]]
    strategy_total_return = total_return(strategy_returns)
    buy_and_hold_total_return = total_return(buy_and_hold_returns)
    metrics = {
        "total_return": strategy_total_return,
        "buy_and_hold_total_return": buy_and_hold_total_return,
        "strategy_minus_buy_and_hold_return": strategy_total_return
        - buy_and_hold_total_return,
        "annualized_return": annualized_return(strategy_returns),
        "max_drawdown": max_drawdown(strategy_returns),
        "volatility": volatility(strategy_returns),
        "sharpe_like": sharpe_like(strategy_returns),
        "win_rate": win_rate_from_returns(strategy_returns),
    }
    risk_notes = ["Model exposure states use close-price moving averages only."]
    if args.symbol:
        risk_notes.append(f"Filtered to symbol: {args.symbol}.")

    strategy_config = {"short_window": args.short_window, "long_window": args.long_window}
    if args.symbol:
        strategy_config["symbol"] = args.symbol
    if args.fee_bps:
        strategy_config["fee_bps"] = args.fee_bps

    report = render_experiment_report(
        strategy_config=strategy_config,
        backtest_curve=backtest_curve,
        metrics=metrics,
        risk_notes=tuple(risk_notes),
        validation_split=validation_split,
        data_provenance=provenance,
    )
    exposure_trade_review = build_exposure_trade_review(backtest_curve)
    scenario_risk_interpretation = build_scenario_risk_interpretation(
        backtest_curve,
        metrics,
    )

    json_payload = {
        "strategy_config": strategy_config,
        "metrics": metrics,
        "exposure_trade_review": exposure_trade_review,
        "scenario_risk_interpretation": scenario_risk_interpretation,
        "first_date": bars[0].date.isoformat() if bars else None,
        "last_date": bars[-1].date.isoformat() if bars else None,
        "row_count": len(bars),
    }
    if validation_split is not None:
        json_payload["validation_split"] = validation_split
    if provenance is not None:
        json_payload["data_provenance"] = provenance

    manifest_payload = build_manifest(
        input_path=args.csv_path,
        symbol=args.symbol,
        mode="backtest",
        strategy_config=strategy_config,
        fee_bps=args.fee_bps,
        output_paths=_output_paths(args),
        data_provenance=provenance,
    )

    return report, json_payload, manifest_payload


def _run_pretrade_packet(args: Namespace) -> tuple[str, dict[str, Any], dict[str, Any]]:
    _, backtest_payload, _ = _run_backtest(args)
    packet_payload = build_pretrade_research_packet(
        backtest_payload,
        input_path=Path(args.csv_path),
    )
    report = render_pretrade_research_packet(packet_payload)
    manifest_payload = build_manifest(
        input_path=args.csv_path,
        symbol=args.symbol,
        mode="pretrade_packet",
        strategy_config=backtest_payload.get("strategy_config"),
        fee_bps=args.fee_bps,
        output_paths=_output_paths(args),
        data_provenance=backtest_payload.get("data_provenance"),
    )
    return report, packet_payload, manifest_payload


def _run_methodology_audit_template() -> tuple[str, dict[str, Any], dict[str, Any]]:
    payload = build_methodology_audit_template()
    report = render_methodology_audit_template(payload)
    return report, payload, {}


def _run_reviewer_evidence_bundle() -> tuple[str, dict[str, Any], dict[str, Any]]:
    payload = build_reviewer_evidence_bundle()
    report = render_reviewer_evidence_bundle(payload)
    return report, payload, {}


def _run_public_demo_evidence_receipt() -> tuple[str, dict[str, Any], dict[str, Any]]:
    payload = build_public_demo_evidence_receipt()
    report = render_public_demo_evidence_receipt(payload)
    return report, payload, {}


def _run_acceptance_receipt_index() -> tuple[str, dict[str, Any], dict[str, Any]]:
    payload = build_acceptance_receipt_index()
    report = render_acceptance_receipt_index(payload)
    return report, payload, {}


def _run_visual_walkthrough_evidence_receipt() -> tuple[
    str, dict[str, Any], dict[str, Any]
]:
    payload = build_visual_walkthrough_evidence_receipt()
    report = render_visual_walkthrough_evidence_receipt(payload)
    return report, payload, {}


def _run_visual_acceptance_bundle() -> tuple[str, dict[str, Any], dict[str, Any]]:
    payload = build_visual_acceptance_bundle()
    report = render_visual_acceptance_bundle(payload)
    return report, payload, {}


def _run_reviewer_acceptance_scorecard() -> tuple[
    str, dict[str, Any], dict[str, Any]
]:
    payload = build_reviewer_acceptance_scorecard()
    report = render_reviewer_acceptance_scorecard(payload)
    return report, payload, {}


def _run_cold_user_review_route() -> tuple[str, dict[str, Any], dict[str, Any]]:
    with _bundled_resource_worktree(COLD_USER_REVIEW_ROUTE_STATIC_RESOURCES) as root:
        payload = build_cold_user_review_route(root)
    report = render_cold_user_review_route(payload)
    return report, payload, {}


def _run_reviewer_rerun_receipt() -> tuple[str, dict[str, Any], dict[str, Any]]:
    payload = build_reviewer_rerun_receipt()
    report = render_reviewer_rerun_receipt(payload)
    return report, payload, {}


def _run_beginner_prediction_checklist() -> tuple[
    str, dict[str, Any], dict[str, Any]
]:
    payload = build_beginner_prediction_checklist()
    report = render_beginner_prediction_checklist(payload)
    return report, payload, {}


def _run_reviewer_decision_matrix() -> tuple[
    str, dict[str, Any], dict[str, Any]
]:
    payload = build_reviewer_decision_matrix()
    report = render_reviewer_decision_matrix(payload)
    return report, payload, {}


def _run_prediction_readiness_audit(
    args: Namespace,
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    input_path = Path(args.prediction_readiness_audit)
    try:
        ledger = _load_defaultable_json(input_path, THESIS_LEDGER_DEFAULT_JSON)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid prediction-readiness audit JSON {input_path}: {exc.msg}"
        ) from exc
    payload = build_prediction_readiness_audit(ledger, str(input_path))
    report = render_prediction_readiness_audit(payload)
    return report, payload, {}


def _run_promotion_readiness_check(
    args: Namespace,
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    input_path = Path(args.promotion_readiness_check)
    try:
        ledger, source_bytes = _load_defaultable_json_with_bytes(
            input_path,
            THESIS_LEDGER_DEFAULT_JSON,
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid promotion-readiness check JSON {input_path}: {exc.msg}"
        ) from exc
    payload = build_promotion_readiness_check(
        ledger,
        _public_source_artifact_path(input_path),
        hashlib.sha256(source_bytes).hexdigest(),
    )
    report = render_promotion_readiness_check(payload)
    return report, payload, {}


def _run_strategy_assumption_stress_kit() -> tuple[
    str, dict[str, Any], dict[str, Any]
]:
    payload = build_strategy_assumption_stress_kit()
    report = render_strategy_assumption_stress_kit(payload)
    return report, payload, {}


def _run_stress_kit_quickstart_card() -> tuple[
    str, dict[str, Any], dict[str, Any]
]:
    payload = build_stress_kit_quickstart_card()
    report = render_stress_kit_quickstart_card(payload)
    return report, payload, {}


def _run_assumption_ledger_summary() -> tuple[str, dict[str, Any], dict[str, Any]]:
    payload = build_assumption_ledger_summary()
    report = render_assumption_ledger_summary(payload)
    return report, payload, {}


def _run_static_visual_capture_checklist() -> tuple[
    str, dict[str, Any], dict[str, Any]
]:
    with _bundled_resource_worktree(
        STATIC_VISUAL_CAPTURE_CHECKLIST_STATIC_RESOURCES
    ) as root:
        payload = build_static_visual_capture_checklist(root)
    report = render_static_visual_capture_checklist(payload)
    return report, payload, {}


def _run_static_visual_capture_receipt() -> tuple[str, dict[str, Any], dict[str, Any]]:
    with _bundled_resource_worktree(STATIC_VISUAL_CAPTURE_RECEIPT_STATIC_RESOURCES) as root:
        payload = build_static_visual_capture_receipt(root)
    report = render_static_visual_capture_receipt(payload)
    return report, payload, {}


def _run_static_visual_release_comparison() -> tuple[
    str, dict[str, Any], dict[str, Any]
]:
    with _bundled_resource_worktree(
        STATIC_VISUAL_RELEASE_COMPARISON_STATIC_RESOURCES
    ) as root:
        payload = build_static_visual_release_comparison(root)
    report = render_static_visual_release_comparison(payload)
    return report, payload, {}


def _run_methodology_audit_review_template() -> tuple[
    str, dict[str, Any], dict[str, Any]
]:
    payload = build_methodology_audit_review_template()
    report = _compact_json(payload)
    return report, payload, {}


def _run_methodology_audit_score(
    args: Namespace,
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    input_path = Path(args.score_methodology_audit)
    try:
        payload = json.loads(
            input_path.read_text(encoding="utf-8"),
            parse_constant=_reject_json_constant,
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid methodology audit JSON {input_path}: {exc.msg}"
        ) from exc
    summary = score_methodology_audit_review(payload)
    report = render_methodology_audit_score(summary)
    return report, summary, {}


def _run_scenario_card(args: Namespace) -> tuple[str, dict[str, Any], dict[str, Any]]:
    _, backtest_payload, _ = _run_backtest(args)
    card_payload = build_scenario_card(
        backtest_payload,
        input_path=Path(args.csv_path),
    )
    report = render_scenario_card(card_payload)
    manifest_payload = build_manifest(
        input_path=args.csv_path,
        symbol=args.symbol,
        mode="scenario_card",
        strategy_config=backtest_payload.get("strategy_config"),
        fee_bps=args.fee_bps,
        output_paths=_output_paths(args),
        data_provenance=backtest_payload.get("data_provenance"),
    )
    return report, card_payload, manifest_payload


def _run_thesis_ledger_validation(
    args: Namespace,
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    input_path = Path(args.thesis_ledger_json)
    try:
        packet = _load_defaultable_json(input_path, THESIS_LEDGER_DEFAULT_JSON)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid thesis-ledger JSON {input_path}: {exc.msg}") from exc
    summary = validate_cross_asset_thesis_ledger_packet(packet)
    report = render_thesis_ledger_acceptance_summary(summary)
    return report, summary, {}


def _run_sweep(args: Namespace) -> tuple[str, dict[str, Any], dict[str, Any]]:
    csv_path = Path(args.csv_path)
    provenance = _load_provenance_payload(csv_path)
    bars = _load_bars(csv_path, symbol=args.symbol)
    split = _build_validation_split(args, bars)
    validation_split = _build_validation_split_metadata(args, split)
    results = run_moving_average_sweep(
        bars=bars,
        short_windows=args.short_windows,
        long_windows=args.long_windows,
        fee_bps=args.fee_bps,
        top_n=args.top_n,
        train_bars=split.train if split is not None else None,
        test_bars=split.test if split is not None else None,
    )
    report = render_sweep_report(
        results,
        validation_split=validation_split,
        data_provenance=provenance,
    )
    sweep_config: dict[str, Any] = {
        "short_windows": list(args.short_windows),
        "long_windows": list(args.long_windows),
        "fee_bps": args.fee_bps,
        "top_n": args.top_n,
    }
    if args.symbol:
        sweep_config["symbol"] = args.symbol

    json_payload = {
        "sweep_config": sweep_config,
        "ranked_results": [
            _serialize_sweep_result(rank, result)
            for rank, result in enumerate(results, start=1)
        ],
    }
    if validation_split is not None:
        json_payload["validation_split"] = validation_split
    if provenance is not None:
        json_payload["data_provenance"] = provenance

    manifest_payload = build_manifest(
        input_path=args.csv_path,
        symbol=args.symbol,
        mode="sweep",
        sweep_config=sweep_config,
        fee_bps=args.fee_bps,
        output_paths=_output_paths(args),
        data_provenance=provenance,
    )

    return report, json_payload, manifest_payload


def _run_regime_comparison(args: Namespace) -> tuple[str, dict[str, Any], dict[str, Any]]:
    with _bundled_resource_worktree() as resource_root:
        regimes = []
        for config_path in args.configs:
            read_config_path = _bundled_read_path(config_path, resource_root)
            config_values = _load_config(read_config_path)
            run_args = _args_from_config_values(config_values)
            run_args.csv_path = _bundled_read_path(Path(run_args.csv_path), resource_root)
            _, payload, _ = _run_backtest(run_args)
            row = _build_regime_comparison_row(config_path, run_args, payload)
            regimes.append(_sanitize_bundled_resource_paths(row, resource_root))

    summary = _build_regime_comparison_summary(regimes)
    report = render_regime_comparison_report(regimes, summary)
    json_payload = {
        "comparison_config": {
            "source_configs": [str(path) for path in args.configs],
            "research_only": True,
            "note": (
                "Bundled deterministic regime comparison; not investment advice, "
                "not a recommendation, and not a prediction."
            ),
        },
        "assumptions": [
            (
                "Bundled regime labels are deterministic synthetic-only fixture "
                "scenarios, not market classifications, forecasts, or live-trading "
                "signals."
            ),
            (
                "Each row uses the configured moving-average settings and "
                "same-period close-to-close buy-and-hold comparison."
            ),
            "Provenance is loaded from adjacent static fixture metadata when available.",
        ],
        "summary": summary,
        "caveats": [
            "This artifact uses synthetic static fixture data for research workflows only.",
            (
                "Results are hypothetical, historical, and sensitive to data, "
                "fees, and chosen parameters."
            ),
            (
                "Nothing in this JSON is investment advice, trading guidance, "
                "a recommendation, a prediction, or a live-trading signal."
            ),
        ],
        "regimes": regimes,
    }
    manifest_payload = build_manifest(
        input_path=", ".join(str(path) for path in args.configs),
        symbol=None,
        mode="regime_comparison",
        fee_bps=0.0,
        output_paths=_output_paths(args),
    )
    return report, json_payload, manifest_payload


def _args_from_config_values(config_values: Mapping[str, Any]) -> Namespace:
    resolved = Namespace()
    for key, default in _default_args().items():
        setattr(resolved, key, config_values.get(key, default))
    if resolved.csv_path is None:
        raise ValueError("Bundled regime config is missing csv_path")
    if resolved.split_ratio is not None and resolved.split_cutoff is not None:
        raise ValueError(
            "Bundled regime config must choose only one validation split option"
        )
    return resolved


def _build_regime_comparison_row(
    config_path: Path,
    run_args: Namespace,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    symbol = str(payload["strategy_config"]["symbol"])
    metrics = dict(payload["metrics"])
    exposure = dict(payload["exposure_trade_review"])
    scenario = dict(payload["scenario_risk_interpretation"])
    return {
        "source_config": str(config_path),
        "csv_path": str(run_args.csv_path),
        "symbol": symbol,
        "regime_label": _regime_label(symbol),
        "generation_assumptions": _regime_generation_assumptions(
            payload.get("data_provenance"),
            symbol,
        ),
        "strategy_config": dict(payload["strategy_config"]),
        "metrics": metrics,
        "exposure_trade_review": exposure,
        "scenario_risk_interpretation": scenario,
        "first_date": payload["first_date"],
        "last_date": payload["last_date"],
        "row_count": payload["row_count"],
        "data_provenance": payload.get("data_provenance"),
        "interpretation": _build_regime_interpretation(metrics, exposure),
        "research_only": True,
        "synthetic_only": True,
        "not_predictive": True,
        "not_live_trading": True,
    }


def _build_regime_interpretation(
    metrics: Mapping[str, float],
    exposure: Mapping[str, Any],
) -> dict[str, Any]:
    period_count = int(exposure["period_count"])
    exposure_changes = int(exposure["exposure_changes"])
    whipsaw_rate = _ratio(exposure_changes, period_count)
    cash_time = float(exposure["percent_periods_in_cash"])
    return_gap = float(metrics["strategy_minus_buy_and_hold_return"])
    max_drawdown_value = float(metrics["max_drawdown"])
    change_label = "change" if exposure_changes == 1 else "changes"

    return {
        "cash_time": cash_time,
        "whipsaw_rate": whipsaw_rate,
        "buy_and_hold_summary": (
            "Strategy minus buy-and-hold was "
            f"{_format_percent(return_gap)} over this deterministic sample."
        ),
        "cash_time_summary": (
            "The model spent "
            f"{_format_percent(cash_time)} of close-to-close periods in cash, "
            "so lower exposure means more missed market movement and less time "
            "bearing market risk in this sample."
        ),
        "drawdown_summary": (
            "The worst modeled peak-to-trough decline was "
            f"{_format_percent(max_drawdown_value)}; more negative values show "
            "larger interim losses before recovery."
        ),
        "whipsaw_summary": (
            f"{exposure_changes} exposure {change_label} across {period_count} periods "
            f"produced a whipsaw rate of {_format_percent(whipsaw_rate)}. "
            "Higher values indicate more historical switching between market "
            "and cash states."
        ),
    }


def _regime_generation_assumptions(
    data_provenance: Any,
    symbol: str,
) -> dict[str, Any]:
    if not isinstance(data_provenance, Mapping):
        return _fallback_regime_generation_assumptions()

    regimes = data_provenance.get("regimes")
    if not _is_non_text_sequence(regimes):
        return _fallback_regime_generation_assumptions()

    for regime in regimes:
        if isinstance(regime, Mapping) and regime.get("symbol") == symbol:
            return {
                "source": str(regime.get("description", "")),
                "assumptions": list(regime.get("assumptions", ())),
                "synthetic_only": regime.get("synthetic_only") is True,
                "not_predictive": regime.get("not_predictive") is True,
                "not_live_trading": regime.get("not_live_trading") is True,
            }

    return _fallback_regime_generation_assumptions()


def _fallback_regime_generation_assumptions() -> dict[str, Any]:
    return {
        "source": "No matching per-regime provenance metadata was found.",
        "assumptions": [
            "Treat this row as a research-only comparison row, not a forecast.",
        ],
        "synthetic_only": True,
        "not_predictive": True,
        "not_live_trading": True,
    }


def _build_regime_comparison_summary(
    regimes: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    best_strategy = max(regimes, key=lambda row: row["metrics"]["total_return"])
    best_buy_hold = max(
        regimes,
        key=lambda row: row["metrics"]["buy_and_hold_total_return"],
    )
    largest_drawdown = min(regimes, key=lambda row: row["metrics"]["max_drawdown"])
    highest_whipsaw = max(
        regimes,
        key=lambda row: row["interpretation"]["whipsaw_rate"],
    )
    most_cash = max(
        regimes,
        key=lambda row: row["exposure_trade_review"]["percent_periods_in_cash"],
    )
    return {
        "best_strategy_total_return_symbol": best_strategy["symbol"],
        "best_buy_and_hold_total_return_symbol": best_buy_hold["symbol"],
        "largest_drawdown_symbol": largest_drawdown["symbol"],
        "highest_whipsaw_symbol": highest_whipsaw["symbol"],
        "most_cash_time_symbol": most_cash["symbol"],
        "research_only": True,
    }


def _load_provenance_payload(csv_path: Path) -> dict[str, Any] | None:
    provenance = load_static_fixture_provenance(csv_path)
    if provenance is None:
        return None
    return provenance.as_dict()


def _load_defaultable_json(path: Path, bundled_default: Path) -> Any:
    source_bytes = _load_defaultable_json_bytes(path, bundled_default)
    return json.loads(
        source_bytes.decode("utf-8"),
        parse_constant=_reject_json_constant,
    )


def _load_defaultable_json_with_bytes(
    path: Path,
    bundled_default: Path,
) -> tuple[Any, bytes]:
    source_bytes = _load_defaultable_json_bytes(path, bundled_default)
    return (
        json.loads(
            source_bytes.decode("utf-8"),
            parse_constant=_reject_json_constant,
        ),
        source_bytes,
    )


def _load_defaultable_json_bytes(path: Path, bundled_default: Path) -> bytes:
    if path.exists() or path != bundled_default:
        return path.read_bytes()

    return _bundled_resource(bundled_default).read_bytes()


def _public_source_artifact_path(path: Path) -> str:
    if not path.is_absolute() and ".." not in path.parts:
        return path.as_posix()

    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name or "ledger.json"


def _bundled_resource_worktree(
    logical_paths: Sequence[Path] | None = None,
) -> tempfile.TemporaryDirectory[str]:
    worktree = tempfile.TemporaryDirectory(prefix="market-signal-lab-")
    root = Path(worktree.name)
    try:
        for logical_path in logical_paths or (
            *BUNDLED_REGIME_CONFIGS,
            Path("examples/data/sample_multi_regime.csv"),
            Path("examples/data/sample_multi_regime.csv.provenance.json"),
        ):
            resource = _bundled_resource(logical_path)
            target = root / logical_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(resource.read_bytes())
    except BaseException:
        worktree.cleanup()
        raise

    return worktree


def _bundled_resource(logical_path: Path):
    resource = files("market_signal_lab").joinpath(
        BUNDLED_RESOURCE_ROOT,
        *logical_path.parts,
    )
    if not resource.is_file():
        raise FileNotFoundError(
            "Bundled resource is missing: "
            f"{BUNDLED_RESOURCE_ROOT}/{logical_path.as_posix()}"
        )
    return resource


def _bundled_read_path(path: Path, resource_root: str | Path) -> Path:
    if path.exists():
        return path
    if path.is_absolute() or ".." in path.parts:
        return path
    bundled_path = Path(resource_root) / path
    if bundled_path.exists():
        return bundled_path
    return path


def _sanitize_bundled_resource_paths(value: Any, resource_root: str | Path) -> Any:
    root = Path(resource_root)
    if isinstance(value, dict):
        return {
            key: _sanitize_bundled_resource_paths(nested, root)
            for key, nested in value.items()
        }
    if isinstance(value, list):
        return [_sanitize_bundled_resource_paths(nested, root) for nested in value]
    if isinstance(value, str):
        try:
            relative = Path(value).relative_to(root)
        except ValueError:
            return value
        return relative.as_posix()
    return value


def _compact_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, separators=(",", ":")) + "\n"


def _serialize_sweep_result(rank: int, result: SweepResult) -> dict[str, Any]:
    row: dict[str, Any] = {
        "rank": rank,
        "windows": {
            "short_window": result.short_window,
            "long_window": result.long_window,
        },
        "metrics": result.metrics,
    }
    if result.train_metrics is not None:
        row["train_metrics"] = result.train_metrics
    if result.test_metrics is not None:
        row["test_metrics"] = result.test_metrics
    if result.robustness is not None:
        row["robustness"] = result.robustness

    return row


def _build_validation_split(
    args: Namespace,
    bars: Sequence[PriceBar],
) -> TrainTestSplit | None:
    if args.split_ratio is None and args.split_cutoff is None:
        return None

    return split_train_test(
        bars,
        train_ratio=args.split_ratio,
        cutoff_date=args.split_cutoff,
    )


def _build_validation_split_metadata(
    args: Namespace,
    split: TrainTestSplit | None,
) -> dict[str, Any] | None:
    if split is None:
        return None

    metadata: dict[str, Any] = {
        "train": _partition_metadata(split.train),
        "test": _partition_metadata(split.test),
        "research_only": True,
        "note": "Validation split metadata is a research note, not trading guidance.",
    }
    if args.split_ratio is not None:
        metadata["method"] = "ratio"
        metadata["split_ratio"] = args.split_ratio
    else:
        metadata["method"] = "cutoff"
        metadata["split_cutoff"] = args.split_cutoff

    return metadata


def _partition_metadata(bars: Sequence[PriceBar]) -> dict[str, Any]:
    return {
        "first_date": bars[0].date.isoformat(),
        "last_date": bars[-1].date.isoformat(),
        "row_count": len(bars),
    }


def _regime_label(symbol: str) -> str:
    return symbol.lower().removesuffix("_regime").replace("_", " ")


def _format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def _ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _is_non_text_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    )


def _output_paths(args: Namespace) -> dict[str, Path | None]:
    return {
        "html_report": args.html_output,
        "json_report": args.json_output,
        "manifest": args.manifest_output,
        "markdown_report": args.output,
    }


def _load_bars(path: Path, symbol: str | None = None) -> list[PriceBar]:
    if symbol is None:
        return load_ohlc_csv(path)

    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError(f"CSV is missing data rows: {path}")
    header = rows[0].keys()
    if "symbol" not in header:
        raise ValueError("CSV is missing required column(s): symbol")

    symbol_rows = [row for row in rows if row.get("symbol") == symbol]
    if not symbol_rows:
        raise ValueError(f"No rows found for symbol {symbol!r}")

    return _load_rows_as_csv(symbol_rows)


def _load_rows_as_csv(rows: Sequence[dict[str, str]]) -> list[PriceBar]:
    source = StringIO()
    writer = csv.DictWriter(source, fieldnames=list(REQUIRED_COLUMNS))
    writer.writeheader()
    for row in rows:
        writer.writerow({column: row[column] for column in REQUIRED_COLUMNS})

    source.seek(0)
    return load_ohlc_csv(source)


def _parse_integer_list(value: str) -> tuple[int, ...]:
    values: list[int] = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            raise ArgumentTypeError("list values must be comma-separated integers")
        try:
            values.append(int(item))
        except ValueError as exc:
            raise ArgumentTypeError(
                "list values must be comma-separated integers"
            ) from exc

    return tuple(values)


def _parse_split_ratio(value: str) -> float:
    try:
        ratio = float(value)
    except ValueError as exc:
        raise ArgumentTypeError("split ratio must be a floating point value") from exc

    if not 0 < ratio < 1:
        raise ArgumentTypeError("split ratio must be greater than 0 and less than 1")

    return ratio


if __name__ == "__main__":
    raise SystemExit(main())
