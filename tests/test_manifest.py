from pathlib import Path

from market_signal_lab.manifest import build_manifest, render_manifest_markdown


def test_build_manifest_includes_research_only_run_metadata() -> None:
    manifest = build_manifest(
        generated_at="2026-05-19T12:00:00Z",
        input_path=Path("data/bars.csv"),
        symbol="AAA",
        mode="backtest",
        strategy_config={"short_window": 2, "long_window": 3},
        fee_bps=1.5,
        output_paths={
            "manifest": Path("reports/manifest.md"),
            "markdown_report": Path("reports/report.md"),
            "json_report": None,
        },
    )

    assert manifest == {
        "generated_at": "2026-05-19T12:00:00Z",
        "input_path": "data/bars.csv",
        "symbol": "AAA",
        "mode": "backtest",
        "strategy_config": {"short_window": 2, "long_window": 3},
        "fee_bps": 1.5,
        "output_paths": {
            "manifest": "reports/manifest.md",
            "markdown_report": "reports/report.md",
        },
        "research_only": True,
    }


def test_build_manifest_omits_generated_at_when_not_provided() -> None:
    manifest = build_manifest(
        input_path="data/bars.csv",
        symbol=None,
        mode="sweep",
        sweep_config={"short_windows": [2, 3], "long_windows": [4, 5]},
        fee_bps=0.0,
    )

    assert "generated_at" not in manifest
    assert manifest["sweep_config"] == {
        "short_windows": [2, 3],
        "long_windows": [4, 5],
    }
    assert manifest["research_only"] is True


def test_build_manifest_includes_static_fixture_provenance_when_provided() -> None:
    provenance = {
        "dataset_label": "sample_tqqq_qld_like",
        "data_kind": "synthetic_static_fixture",
        "source": "Hand-authored deterministic OHLC sample.",
        "created_date": "2026-05-18",
        "as_of_date": "2026-05-18",
        "limitations": ["Synthetic static fixture only."],
        "metadata_path": "examples/data/sample_tqqq_qld_like.csv.provenance.json",
        "research_only": True,
    }

    manifest = build_manifest(
        input_path="examples/data/sample_tqqq_qld_like.csv",
        symbol="QQQ_LIKE",
        mode="backtest",
        fee_bps=0.0,
        data_provenance=provenance,
    )

    assert manifest["data_provenance"] == provenance


def test_render_manifest_markdown_renders_nested_sections() -> None:
    markdown = render_manifest_markdown(
        {
            "input_path": "data/bars.csv",
            "symbol": None,
            "mode": "sweep",
            "sweep_config": {"short_windows": [2, 3], "fee_bps": 0.0},
            "fee_bps": 0.0,
            "output_paths": {"manifest": "reports/manifest.md"},
            "research_only": True,
        }
    )

    assert markdown == (
        "# Experiment Manifest\n"
        "\n"
        "- **input_path**: data/bars.csv\n"
        "- **symbol**: None\n"
        "- **mode**: sweep\n"
        "\n"
        "## sweep_config\n"
        "\n"
        "- **short_windows**: 2, 3\n"
        "- **fee_bps**: 0.0000\n"
        "\n"
        "- **fee_bps**: 0.0000\n"
        "\n"
        "## output_paths\n"
        "\n"
        "- **manifest**: reports/manifest.md\n"
        "\n"
        "- **research_only**: true\n"
    )
