"""Command-line interface for CSV moving-average backtest reports."""

from __future__ import annotations

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from collections.abc import Mapping, Sequence
from io import StringIO
from pathlib import Path
import csv
import json
import os
import sys
from typing import Any

from market_signal_lab import __version__
from market_signal_lab.backtest import backtest_long_cash
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
from market_signal_lab.report import (
    build_exposure_trade_review,
    build_scenario_risk_interpretation,
    render_regime_comparison_report,
    render_experiment_report,
)
from market_signal_lab.reviewer_bundle import (
    build_reviewer_evidence_bundle,
    render_reviewer_evidence_bundle,
)
from market_signal_lab.scenario_card import build_scenario_card, render_scenario_card
from market_signal_lab.split import TrainTestSplit, split_train_test
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

BUNDLED_REGIME_CONFIGS = (
    Path("examples/configs/multi-regime-bull-report.json"),
    Path("examples/configs/multi-regime-choppy-report.json"),
    Path("examples/configs/multi-regime-drawdown-recovery-report.json"),
)
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.methodology_audit_review_template:
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
        description="Generate a moving-average crossover report from OHLC CSV data.",
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
            "omitted, validates reports/cross-asset-thesis-ledger.json; when "
            "no output path is supplied, writes Markdown/JSON acceptance "
            "artifacts under reports."
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
            "boundaries. Defaults to reports/reviewer-evidence-bundle.md and "
            "reports/reviewer-evidence-bundle.json."
        ),
    )
    parser.add_argument(
        "--regime-comparison",
        action="store_true",
        default=False,
        help=(
            "Run bundled bull/choppy/drawdown-recovery configs and write a "
            "deterministic comparison artifact under reports by default."
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
        packet = json.loads(
            input_path.read_text(encoding="utf-8"),
            parse_constant=_reject_json_constant,
        )
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
    regimes = []
    for config_path in args.configs:
        config_values = _load_config(config_path)
        run_args = _args_from_config_values(config_values)
        _, payload, _ = _run_backtest(run_args)
        regimes.append(_build_regime_comparison_row(config_path, run_args, payload))

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
    fallback = {
        "source": "No matching per-regime provenance metadata was found.",
        "assumptions": [
            "Treat this row as a research-only comparison row, not a forecast.",
        ],
        "synthetic_only": True,
        "not_predictive": True,
        "not_live_trading": True,
    }
    if not isinstance(data_provenance, Mapping):
        return fallback

    regimes = data_provenance.get("regimes")
    if not _is_non_text_sequence(regimes):
        return fallback

    for regime in regimes:
        if isinstance(regime, Mapping) and regime.get("symbol") == symbol:
            return {
                "source": str(regime.get("description", "")),
                "assumptions": list(regime.get("assumptions", ())),
                "synthetic_only": regime.get("synthetic_only") is True,
                "not_predictive": regime.get("not_predictive") is True,
                "not_live_trading": regime.get("not_live_trading") is True,
            }

    return fallback


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
