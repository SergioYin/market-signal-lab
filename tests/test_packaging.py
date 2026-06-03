from __future__ import annotations

import re
from pathlib import Path

from market_signal_lab import __version__


PROJECT_ROOT = Path(__file__).resolve().parents[1]


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

    assert 'readme = "README.md"' in pyproject
    assert 'authors = [{ name = "SergioYin" }]' in pyproject
    assert '"backtesting"' in pyproject
    assert "[project.urls]" in pyproject
    assert 'Homepage = "https://sergioyin.github.io/market-signal-lab/"' in pyproject
    assert 'Repository = "https://github.com/SergioYin/market-signal-lab"' in pyproject
    assert 'market-signal-lab = "market_signal_lab.cli:main"' in pyproject


def test_package_version_matches_project_metadata() -> None:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text()
    match = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)

    assert match is not None
    assert __version__ == match.group(1)


def test_package_version_tracks_current_release() -> None:
    assert __version__ == "1.20.4"
