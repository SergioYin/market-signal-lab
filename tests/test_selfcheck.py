from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts import selfcheck


def test_selfcheck_regenerates_static_gallery_contract() -> None:
    assert Path("reports/index.html") in selfcheck.SAMPLE_ARTIFACTS

    gallery = selfcheck.GALLERY_HTML
    assert "<script" not in gallery.lower()
    assert "research-only" in gallery
    assert "not investment advice" in gallery

    expected_links = {
        "sample-report.html",
        "sample-sweep.html",
        "sample-sweep-split.html",
    }
    for link in expected_links:
        assert f'href="{link}"' in gallery


def test_selfcheck_regenerates_split_sweep_artifacts() -> None:
    expected_artifacts = {
        Path("reports/sample-sweep-split.md"),
        Path("reports/sample-sweep-split.json"),
        Path("reports/sample-sweep-split.html"),
    }

    assert expected_artifacts.issubset(set(selfcheck.SAMPLE_ARTIFACTS))

    split_command = _split_sweep_command()
    assert "--sweep" in split_command
    assert split_command[split_command.index("--short-windows") + 1] == "1,2"
    assert split_command[split_command.index("--long-windows") + 1] == "2,3"
    assert split_command[split_command.index("--split-ratio") + 1] == "0.5"
    assert "reports/sample-sweep-split.json" in split_command
    assert "reports/sample-sweep-split.html" in split_command


def test_split_sweep_sample_artifact_has_non_zero_diagnostics(tmp_path: Path) -> None:
    command = _split_sweep_command()
    output_paths = {
        "reports/sample-sweep-split.md": tmp_path / "sample-sweep-split.md",
        "reports/sample-sweep-split.json": tmp_path / "sample-sweep-split.json",
        "reports/sample-sweep-split.html": tmp_path / "sample-sweep-split.html",
    }
    command = [str(output_paths.get(value, value)) for value in command]

    result = subprocess.run(
        command,
        cwd=selfcheck.REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads((tmp_path / "sample-sweep-split.json").read_text())

    assert payload["sweep_config"]["short_windows"] == [1, 2]
    assert payload["sweep_config"]["long_windows"] == [2, 3]
    assert payload["validation_split"]["split_ratio"] == 0.5

    top_result = payload["ranked_results"][0]
    assert top_result["train_metrics"]["total_return"] != 0.0
    assert top_result["test_metrics"]["total_return"] != 0.0


def _split_sweep_command() -> list[str]:
    split_commands = [
        command
        for command in selfcheck._sample_artifact_commands()
        if "reports/sample-sweep-split.md" in command
    ]
    assert len(split_commands) == 1
    return split_commands[0]
