#!/usr/bin/env python3
"""Project self-check utility."""

from __future__ import annotations

from pathlib import Path
import compileall
import re
import subprocess
import sys
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"
CSV_PATH = Path("examples/data/sample_tqqq_qld_like.csv")
DOC_LINK_SOURCES = (
    Path("README.md"),
    Path("docs/index.md"),
    Path("docs/artifact-gallery.md"),
    Path("docs/config-files.md"),
    Path("docs/data-provenance.md"),
    Path("docs/example-data.md"),
    Path("docs/metric-guide.md"),
    Path("docs/release-notes-v0.3.0.md"),
    Path("docs/release-notes-v0.4.0.md"),
    Path("docs/release-notes-v0.5.0.md"),
    Path("docs/release-notes-v0.6.0.md"),
    Path("docs/release-notes-v0.7.0.md"),
    Path("docs/release-notes-v0.8.0.md"),
    Path("docs/release-v0.3.0.md"),
    Path("docs/release-v0.4.0.md"),
    Path("docs/release-v0.5.0.md"),
    Path("docs/release-v0.6.0.md"),
    Path("docs/release-v0.7.0.md"),
    Path("docs/release-v0.8.0.md"),
    Path("docs/risk-boundaries.md"),
)
SAMPLE_ARTIFACTS = (
    Path("reports/index.html"),
    Path("reports/sample-report.md"),
    Path("reports/sample-report.json"),
    Path("reports/sample-report.html"),
    Path("reports/sample-manifest.md"),
    Path("reports/sample-sweep.md"),
    Path("reports/sample-sweep.json"),
    Path("reports/sample-sweep.html"),
    Path("reports/sample-sweep-split.md"),
    Path("reports/sample-sweep-split.json"),
    Path("reports/sample-sweep-split.html"),
)

GALLERY_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Market Signal Lab Sample Reports</title>
</head>
<body>
  <h1>Market Signal Lab Sample Reports</h1>
  <p><strong>Public-safe research samples:</strong> these artifacts use synthetic sample data. They are research-only, not investment advice, not recommendations, and not evidence of future performance.</p>
  <h2>Single Backtest</h2>
  <ul>
    <li><a href="sample-report.html">HTML report</a></li>
    <li><a href="sample-report.md">Markdown report</a></li>
    <li><a href="sample-report.json">JSON report</a></li>
  </ul>
  <h2>Parameter Sweep</h2>
  <ul>
    <li><a href="sample-sweep.html">HTML sweep</a></li>
    <li><a href="sample-sweep.md">Markdown sweep</a></li>
    <li><a href="sample-sweep.json">JSON sweep</a></li>
  </ul>
  <h2>Split Sweep</h2>
  <ul>
    <li><a href="sample-sweep-split.html">HTML split sweep</a></li>
    <li><a href="sample-sweep-split.md">Markdown split sweep</a></li>
    <li><a href="sample-sweep-split.json">JSON split sweep</a></li>
  </ul>
  <h2>Reproduction</h2>
  <ul>
    <li><a href="sample-manifest.md">Sample manifest</a></li>
  </ul>
</body>
</html>
"""


MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCED_BLOCK_RE = re.compile(r"(^|\n)```.*?(\n```|$)", re.DOTALL)


def run_compileall() -> bool:
    print("1) Running Python compilation check...")
    # Compile the library and tests to catch syntax/import-time issues.
    ok = compileall.compile_dir(str(REPO_ROOT / "market_signal_lab"), quiet=1)
    ok &= compileall.compile_dir(str(REPO_ROOT / "tests"), quiet=1)
    return bool(ok)


def run_pytest() -> bool:
    print("2) Running pytest...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest"],
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
    print("3) Checking documentation links...")
    issues = find_markdown_link_issues(REPO_ROOT, DOC_LINK_SOURCES)
    if issues:
        print("Documentation link check failed")
        for issue in issues:
            print(f"- {issue}")
        return False
    return True


def run_sample_artifact_generation() -> bool:
    print("4) Generating sample artifacts...")
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

    (REPORTS_DIR / "index.html").write_text(GALLERY_HTML, encoding="utf-8")

    for artifact in SAMPLE_ARTIFACTS:
        path = REPO_ROOT / artifact
        if not path.exists():
            print(f"Missing sample artifact: {artifact}")
            return False
        if path.stat().st_size == 0:
            print(f"Empty sample artifact: {artifact}")
            return False

    print("Created sample report gallery, report, manifest, sweep, split sweep, and HTML artifacts.")
    return True


def find_markdown_link_issues(
    repo_root: Path = REPO_ROOT,
    markdown_files: tuple[Path, ...] = DOC_LINK_SOURCES,
) -> list[str]:
    issues: list[str] = []
    for relative_source in markdown_files:
        source = repo_root / relative_source
        if not source.exists():
            issues.append(f"{relative_source}: source file is missing")
            continue

        text = _strip_fenced_code_blocks(source.read_text(encoding="utf-8"))
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = _normalize_markdown_link_target(raw_target)
            if _is_external_or_anchor_only_link(target):
                continue

            link_path = _local_markdown_link_path(repo_root, source, target)
            if not link_path.exists():
                issues.append(f"{relative_source}: broken link to {raw_target}")

    return issues


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


def _sample_artifact_commands() -> list[list[str]]:
    return [
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
            "--output",
            "reports/sample-report.md",
            "--json-output",
            "reports/sample-report.json",
            "--html-output",
            "reports/sample-report.html",
            "--manifest-output",
            "reports/sample-manifest.md",
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
    ]


def main() -> int:
    checks = [
        ("compileall", run_compileall),
        ("pytest", run_pytest),
        ("documentation link check", run_docs_link_check),
        ("sample artifact generation", run_sample_artifact_generation),
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
