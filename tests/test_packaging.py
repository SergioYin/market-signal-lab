from __future__ import annotations

import os
import re
import subprocess
import sys
import tomllib
import venv
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
    "reports/cross-asset-thesis-ledger.json",
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
        "_resources/**/*.json",
    ]
    for resource in INSTALLED_DEFAULT_COMMAND_RESOURCES:
        assert (PROJECT_ROOT / "market_signal_lab" / "_resources" / resource).is_file()


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
        "--beginner-prediction-checklist",
        "--prediction-readiness-audit",
        "--validate-thesis-ledger",
        "--regime-comparison",
    ):
        _run_wheel_smoke_command(console_script, flag, empty_cwd, env)

    assert (empty_cwd / "reports" / "reviewer-evidence-bundle.md").is_file()
    assert (empty_cwd / "reports" / "beginner-prediction-checklist.md").is_file()
    assert (
        empty_cwd / "reports" / "cross-asset-thesis-ledger-acceptance.json"
    ).is_file()
    assert (empty_cwd / "reports" / "prediction-readiness-audit.json").is_file()
    assert (empty_cwd / "reports" / "regime-comparison.html").is_file()


def test_package_version_matches_project_metadata() -> None:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text()
    match = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)

    assert match is not None
    assert __version__ == match.group(1)


def test_package_version_tracks_current_release() -> None:
    assert __version__ == "1.24.0"


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
