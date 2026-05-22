#!/usr/bin/env python3
"""Project self-check utility."""

from __future__ import annotations

from pathlib import Path
import compileall
import json
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
    Path("docs/static-gallery-manifest.md"),
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
    Path("docs/risk-boundaries.md"),
)
FIXTURE_PROVENANCE_FILES = (
    Path("examples/data/sample_tqqq_qld_like.csv.provenance.json"),
)
HTML_LINK_SOURCES = (
    Path("index.html"),
    Path("reports/index.html"),
)
V131_ROOT_LANDING_LINKS = (
    "reports/index.html",
    "docs/index.md",
    "README.md",
    "docs/static-gallery-manifest.md",
    "docs/artifact-gallery.md",
    "docs/split-sweep-walkthrough.md",
    "docs/risk-boundaries.md",
    "docs/data-provenance.md",
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
    "../docs/split-sweep-walkthrough.md",
    "sample-manifest.md",
    "sample-report.html",
    "sample-report.md",
    "sample-report.json",
    "fee-sensitivity.md",
    "fee-sensitivity.json",
    "sample-sweep.html",
    "sample-sweep.md",
    "sample-sweep.json",
    "sample-sweep-split.html",
    "sample-sweep-split.md",
    "sample-sweep-split.json",
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
</head>
<body>
  <h1>Market Signal Lab Sample Reports</h1>
  <p><strong>Start with the artifact trail:</strong> this static gallery shows the checked-in outputs before you run the CLI: human-readable reports, machine-readable JSON, browser-openable HTML, and the manifest that records the sample inputs and outputs.</p>
  <p><strong>What to inspect first:</strong> open the artifact notes for a map, the sample manifest for reproducibility, and the split-sweep walkthrough if you are reading train/test robustness fields for the first time.</p>
  <p><strong>Public-safe research samples:</strong> these artifacts use synthetic sample data and require no JavaScript, remote data, broker connection, or trading account. They are research-only review aids, not investment advice, not recommendations, and not evidence of future performance.</p>
  <p><strong>Leveraged ETF-like limits:</strong> the sample names are placeholders, and leveraged ETF products can behave in ways beginners may not expect. Daily resets make multi-day results depend on the path of daily moves; losses can grow quickly; and real funds include fund expenses, financing costs, tracking differences, taxes, liquidity, and market impact that these sample artifacts do not model.</p>
  <h2>Open These First</h2>
  <ul>
    <li><a href="../docs/static-gallery-manifest.md">Static demo manifest</a></li>
    <li><a href="../docs/artifact-gallery.md">Artifact gallery notes</a></li>
    <li><a href="../docs/split-sweep-walkthrough.md">Split-sweep walkthrough</a></li>
    <li><a href="sample-manifest.md">Sample manifest</a></li>
  </ul>
  <h2>Single Backtest</h2>
  <ul>
    <li><a href="sample-report.html">HTML report</a></li>
    <li><a href="sample-report.md">Markdown report</a></li>
    <li><a href="sample-report.json">JSON report</a></li>
    <li><a href="fee-sensitivity.md">Fee sensitivity Markdown</a></li>
    <li><a href="fee-sensitivity.json">Fee sensitivity JSON</a></li>
  </ul>
  <h2>Parameter Sweep</h2>
  <ul>
    <li><a href="sample-sweep.html">HTML sweep</a></li>
    <li><a href="sample-sweep.md">Markdown sweep</a></li>
    <li><a href="sample-sweep.json">JSON sweep</a></li>
  </ul>
  <h2>Split Sweep</h2>
  <p><a href="../docs/split-sweep-walkthrough.md">Beginner walkthrough for reading split-sweep robustness fields</a></p>
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
HTML_HREF_RE = re.compile(r"\bhref\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
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

    (REPORTS_DIR / "index.html").write_text(GALLERY_HTML, encoding="utf-8")

    for artifact in SAMPLE_ARTIFACTS:
        path = REPO_ROOT / artifact
        if not path.exists():
            print(f"Missing sample artifact: {artifact}")
            return False
        if path.stat().st_size == 0:
            print(f"Empty sample artifact: {artifact}")
            return False

    print("Created sample report gallery, report, manifest, sweep, split sweep, fee sensitivity, and HTML artifacts.")
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
        if (
            not isinstance(limitations, list)
            or not limitations
            or not all(isinstance(item, str) and item.strip() for item in limitations)
        ):
            issues.append(
                f"{relative_path}: limitations must be a non-empty list of strings"
            )

        csv_path = path.with_name(path.name.removesuffix(".provenance.json"))
        if not csv_path.exists():
            issues.append(f"{relative_path}: source CSV is missing")

    return issues


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
        [
            sys.executable,
            "scripts/fee_sensitivity.py",
            "--markdown-output",
            "reports/fee-sensitivity.md",
            "--json-output",
            "reports/fee-sensitivity.json",
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
