from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tomllib
import venv
import zipfile
from pathlib import Path

import pytest

from market_signal_lab import __version__


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INSTALLED_DEFAULT_COMMAND_RESOURCES = (
    "examples/configs/multi-regime-bull-report.json",
    "examples/configs/multi-regime-choppy-report.json",
    "examples/configs/multi-regime-drawdown-recovery-report.json",
    "examples/data/sample_multi_regime.csv",
    "examples/data/sample_multi_regime.csv.provenance.json",
    "docs/methodology-audit.md",
    "reports/assumption-ledger-summary.md",
    "reports/assumption-ledger-summary.json",
    "reports/beginner-prediction-checklist.md",
    "reports/cross-asset-thesis-ledger.json",
    "reports/index.html",
    "reports/reviewer-acceptance-scorecard.json",
    "reports/reviewer-acceptance-scorecard.md",
    "reports/reviewer-evidence-bundle.json",
    "reports/reviewer-evidence-bundle.md",
    "reports/reviewer-rerun-receipt.md",
    "reports/stress-kit-quickstart-card.md",
    "reports/stress-kit-quickstart-card.json",
    "reports/strategy-assumption-stress-kit.md",
    "reports/strategy-assumption-stress-kit.json",
    "reports/strategy-assumption-stress-kit.html",
    "reports/sample-report.md",
)
STRATEGY_ASSUMPTION_STRESS_KIT_RESOURCES = (
    "reports/strategy-assumption-stress-kit.html",
    "reports/strategy-assumption-stress-kit.md",
    "reports/strategy-assumption-stress-kit.json",
)
STRESS_KIT_QUICKSTART_CARD_RESOURCES = (
    "reports/stress-kit-quickstart-card.md",
    "reports/stress-kit-quickstart-card.json",
)
ASSUMPTION_LEDGER_SUMMARY_RESOURCES = (
    "reports/assumption-ledger-summary.md",
    "reports/assumption-ledger-summary.json",
)


def test_project_declares_minimal_build_system() -> None:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text()

    assert "[build-system]" in pyproject
    assert 'requires = ["setuptools>=68"]' in pyproject
    assert 'build-backend = "setuptools.build_meta"' in pyproject


def test_project_metadata_declares_mit_license_file() -> None:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text()
    license_text = (PROJECT_ROOT / "LICENSE").read_text()

    assert 'license = { file = "LICENSE" }' in pyproject
    assert "License :: OSI Approved :: MIT License" in pyproject
    assert license_text.startswith("MIT License\n")
    assert "Permission is hereby granted, free of charge" in license_text


def test_project_metadata_declares_public_package_context() -> None:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text()
    metadata = tomllib.loads(pyproject)
    project = metadata["project"]

    assert project["readme"] == "README.md"
    assert project["dependencies"] == []
    assert project["optional-dependencies"]["test"] == ["pytest>=8"]
    assert 'authors = [{ name = "SergioYin" }]' in pyproject
    assert '"backtesting"' in pyproject
    assert project["urls"]["Homepage"] == "https://sergioyin.github.io/market-signal-lab/"
    assert project["urls"]["Repository"] == "https://github.com/SergioYin/market-signal-lab"
    assert project["scripts"]["market-signal-lab"] == "market_signal_lab.cli:main"


def test_project_metadata_includes_bundled_cli_resources() -> None:
    metadata = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text())

    package_data = metadata["tool"]["setuptools"]["package-data"]

    assert package_data["market_signal_lab"] == [
        "_resources/**/*.csv",
        "_resources/**/*.html",
        "_resources/**/*.json",
        "_resources/**/*.md",
    ]
    for resource in INSTALLED_DEFAULT_COMMAND_RESOURCES:
        assert (PROJECT_ROOT / "market_signal_lab" / "_resources" / resource).is_file()
    resource_gallery = (
        PROJECT_ROOT / "market_signal_lab" / "_resources" / "reports" / "index.html"
    ).read_text(encoding="utf-8")
    assert 'href="stress-kit-quickstart-card.md"' in resource_gallery
    assert 'href="stress-kit-quickstart-card.json"' in resource_gallery
    for resource in (
        STRESS_KIT_QUICKSTART_CARD_RESOURCES
        + ASSUMPTION_LEDGER_SUMMARY_RESOURCES
    ):
        packaged_resource = PROJECT_ROOT / "market_signal_lab" / "_resources" / resource
        checked_in_report = PROJECT_ROOT / resource

        assert packaged_resource.read_bytes() == checked_in_report.read_bytes()


@pytest.mark.wheel_smoke
def test_wheel_console_script_smoke_from_empty_directory(tmp_path: Path) -> None:
    env = _isolated_subprocess_env()
    build_venv = tmp_path / "build-venv"
    try:
        venv.EnvBuilder(with_pip=True).create(build_venv)
    except subprocess.CalledProcessError as exc:
        pytest.skip(f"pip is required to build the wheel smoke-test fixture: {exc}")
    build_python = _venv_python(build_venv)
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    build_result = subprocess.run(
        [
            str(build_python),
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--no-build-isolation",
            "--wheel-dir",
            str(wheelhouse),
            str(PROJECT_ROOT),
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert build_result.returncode == 0, build_result.stderr

    wheels = sorted(wheelhouse.glob("market_signal_lab-*.whl"))
    assert len(wheels) == 1
    _assert_wheel_includes_resources(
        wheels[0],
        STRATEGY_ASSUMPTION_STRESS_KIT_RESOURCES
        + STRESS_KIT_QUICKSTART_CARD_RESOURCES
        + ASSUMPTION_LEDGER_SUMMARY_RESOURCES,
    )

    install_venv = tmp_path / "install-venv"
    venv.EnvBuilder(with_pip=True).create(install_venv)
    install_python = _venv_python(install_venv)
    install_result = subprocess.run(
        [
            str(install_python),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--no-deps",
            str(wheels[0]),
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert install_result.returncode == 0, install_result.stderr

    empty_cwd = tmp_path / "empty-cwd"
    empty_cwd.mkdir()
    console_script = _venv_script(install_venv, "market-signal-lab")
    installed_version = _probe_installed_wheel_version(install_python, empty_cwd, env)

    version_result = _run_wheel_smoke_command(
        console_script,
        "--version",
        empty_cwd,
        env,
    )
    assert version_result.stdout.strip() == f"market-signal-lab {installed_version}"

    for flag in (
        "--reviewer-evidence-bundle",
        "--reviewer-rerun-receipt",
        "--beginner-prediction-checklist",
        "--cold-user-review-route",
        "--prediction-readiness-audit",
        "--reviewer-acceptance-scorecard",
        "--strategy-assumption-stress-kit",
        "--stress-kit-quickstart-card",
        "--assumption-ledger-summary",
        "--validate-thesis-ledger",
        "--regime-comparison",
    ):
        _run_wheel_smoke_command(console_script, flag, empty_cwd, env)

    reviewer_decision_matrix_result = _run_wheel_smoke_module_command(
        install_python,
        "--reviewer-decision-matrix",
        empty_cwd,
        env,
    )
    assert reviewer_decision_matrix_result.stdout == ""
    assert reviewer_decision_matrix_result.stderr == ""

    assert (empty_cwd / "reports" / "reviewer-evidence-bundle.md").is_file()
    assert (empty_cwd / "reports" / "reviewer-rerun-receipt.md").is_file()
    assert (empty_cwd / "reports" / "beginner-prediction-checklist.md").is_file()
    scorecard_payload = json.loads(
        (
            empty_cwd / "reports" / "reviewer-acceptance-scorecard.json"
        ).read_text(encoding="utf-8")
    )
    assert scorecard_payload["artifact_type"] == "reviewer_acceptance_scorecard"
    assert scorecard_payload["overall_label"] == "WARN"
    assert (
        empty_cwd / "reports" / "reviewer-acceptance-scorecard.md"
    ).is_file()
    stress_kit_payload = json.loads(
        (empty_cwd / "reports" / "strategy-assumption-stress-kit.json").read_text(
            encoding="utf-8"
        )
    )
    assert stress_kit_payload["artifact_type"] == "strategy_assumption_stress_kit"
    assert stress_kit_payload["no_live_data"] is True
    assert (empty_cwd / "reports" / "strategy-assumption-stress-kit.md").is_file()
    quickstart_payload = json.loads(
        (empty_cwd / "reports" / "stress-kit-quickstart-card.json").read_text(
            encoding="utf-8"
        )
    )
    assert quickstart_payload["artifact_type"] == "stress_kit_quickstart_card"
    assert quickstart_payload["estimated_review_time_minutes"] == 2
    assert (empty_cwd / "reports" / "stress-kit-quickstart-card.md").is_file()
    ledger_summary_payload = json.loads(
        (empty_cwd / "reports" / "assumption-ledger-summary.json").read_text(
            encoding="utf-8"
        )
    )
    assert ledger_summary_payload["artifact_type"] == "assumption_ledger_summary"
    assert ledger_summary_payload["no_live_data"] is True
    assert ledger_summary_payload["not_investment_advice"] is True
    assert (empty_cwd / "reports" / "assumption-ledger-summary.md").is_file()
    assert (
        empty_cwd / "reports" / "cross-asset-thesis-ledger-acceptance.json"
    ).is_file()
    cold_user_route = json.loads(
        (empty_cwd / "reports" / "cold-user-review-route.json").read_text(
            encoding="utf-8"
        )
    )
    assert cold_user_route["artifact_integrity_summary"]["integrity_status"] == "PASS"
    assert (
        cold_user_route["artifact_integrity_summary"]["present_count"]
        == cold_user_route["artifact_integrity_summary"]["artifact_count"]
    )
    reviewer_decision_matrix_markdown = (
        empty_cwd / "reports" / "reviewer-decision-matrix.md"
    ).read_text(encoding="utf-8")
    reviewer_decision_matrix_payload = json.loads(
        (empty_cwd / "reports" / "reviewer-decision-matrix.json").read_text(
            encoding="utf-8"
        )
    )
    assert "# Reviewer Decision Matrix" in reviewer_decision_matrix_markdown
    assert reviewer_decision_matrix_payload["artifact_type"] == "reviewer_decision_matrix"
    assert reviewer_decision_matrix_payload["default_outputs"] == {
        "markdown": "reports/reviewer-decision-matrix.md",
        "json": "reports/reviewer-decision-matrix.json",
    }
    assert (empty_cwd / "reports" / "prediction-readiness-audit.json").is_file()
    assert (empty_cwd / "reports" / "regime-comparison.html").is_file()


def test_package_version_matches_project_metadata() -> None:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text()
    match = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)

    assert match is not None
    assert __version__ == match.group(1)


def test_package_version_tracks_current_release() -> None:
    assert __version__ == "1.30.2"


def _venv_python(venv_path: Path) -> Path:
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def _venv_script(venv_path: Path, name: str) -> Path:
    if sys.platform == "win32":
        return venv_path / "Scripts" / f"{name}.exe"
    return venv_path / "bin" / name


def _isolated_subprocess_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env.pop("VIRTUAL_ENV", None)
    env["PYTHONNOUSERSITE"] = "1"
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    return env


def _probe_installed_wheel_version(
    python: Path,
    cwd: Path,
    env: dict[str, str],
) -> str:
    result = subprocess.run(
        [
            str(python),
            "-I",
            "-c",
            "\n".join(
                (
                    "from importlib.metadata import version",
                    "import market_signal_lab",
                    "print(version('market-signal-lab'))",
                )
            ),
        ],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr

    installed_version = result.stdout.strip()
    assert installed_version == _project_version()
    return installed_version


def _project_version() -> str:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text()
    match = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)
    assert match is not None
    return match.group(1)


def _assert_wheel_includes_resources(
    wheel_path: Path,
    logical_resource_paths: tuple[str, ...],
) -> None:
    with zipfile.ZipFile(wheel_path) as wheel:
        packaged_paths = set(wheel.namelist())

    for resource_path in logical_resource_paths:
        assert (
            f"market_signal_lab/_resources/{resource_path}" in packaged_paths
        ), f"{resource_path} is missing from {wheel_path.name}"


def _run_wheel_smoke_command(
    console_script: Path,
    flag: str,
    cwd: Path,
    env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [str(console_script), flag],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result


def _run_wheel_smoke_module_command(
    python: Path,
    flag: str,
    cwd: Path,
    env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [str(python), "-I", "-m", "market_signal_lab.cli", flag],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result
