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
    Path("docs/cold-review-checklist.md"),
    Path("docs/config-files.md"),
    Path("docs/data-provenance.md"),
    Path("docs/example-data.md"),
    Path("docs/metric-guide.md"),
    Path("docs/scenario-risk-glossary.md"),
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
    Path("docs/release-notes-v1.3.3.md"),
    Path("docs/release-notes-v1.3.4.md"),
    Path("docs/release-notes-v1.3.5.md"),
    Path("docs/release-notes-v1.4.0.md"),
    Path("docs/release-notes-v1.5.0.md"),
    Path("docs/release-notes-v1.6.0.md"),
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
V160_STATIC_DASHBOARD_CARDS = {
    "single-report": (
        "Single Report",
        "reports/sample-report.html",
        ("sample-report.html", "sample-report.md", "sample-report.json"),
    ),
    "regime-comparison": (
        "Regime Comparison",
        "reports/regime-comparison.html",
        ("regime-comparison.html", "regime-comparison.md", "regime-comparison.json"),
    ),
    "fee-sensitivity": (
        "Fee Sensitivity",
        "reports/fee-sensitivity.md",
        ("fee-sensitivity.md", "fee-sensitivity.json"),
    ),
    "split-sweep": (
        "Split Sweep",
        "reports/sample-sweep-split.html",
        ("sample-sweep-split.html", "sample-sweep-split.md", "sample-sweep-split.json"),
    ),
    "manifest": (
        "Manifest",
        "reports/sample-manifest.md",
        ("sample-manifest.md", "../docs/static-gallery-manifest.md"),
    ),
}
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
SAMPLE_ARTIFACTS = (
    Path("reports/index.html"),
    Path("reports/sample-report.md"),
    Path("reports/sample-report.json"),
    Path("reports/sample-report.html"),
    Path("reports/sample-manifest.md"),
    Path("reports/regime-comparison.md"),
    Path("reports/regime-comparison.json"),
    Path("reports/regime-comparison.html"),
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
  <style>
    body { font-family: system-ui, sans-serif; line-height: 1.45; margin: 0; color: #1f2328; background: #ffffff; }
    main { max-width: 1120px; margin: 0 auto; padding: 1.25rem; }
    h1 { font-size: 1.75rem; margin: 0 0 0.5rem; }
    h2 { font-size: 1.05rem; margin: 1.25rem 0 0.45rem; }
    p { margin: 0.45rem 0; }
    a { color: #0969da; }
    .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 0.75rem; margin: 1rem 0; }
    .dashboard-card { border: 1px solid #d0d7de; border-radius: 8px; padding: 0.85rem; background: #f6f8fa; }
    .dashboard-card h2 { margin-top: 0; }
    .artifact-path { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 0.85rem; color: #57606a; overflow-wrap: anywhere; }
    .artifact-links { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-top: 0.65rem; }
    .artifact-links a { border: 1px solid #d0d7de; border-radius: 6px; padding: 0.2rem 0.45rem; background: #ffffff; text-decoration: none; }
  </style>
</head>
<body>
  <main>
    <h1>Market Signal Lab Sample Reports</h1>
    <p><strong>v1.6.0 static artifact dashboard:</strong> open the checked-in outputs before running the CLI. The first-screen cards expose the local artifact paths for the single report, regime comparison, fee sensitivity, split sweep, and manifest.</p>
    <p><strong>Public-safe research samples:</strong> these artifacts use synthetic sample data and require no JavaScript, remote data, broker connection, or trading account. They are research-only review aids, not investment advice, not recommendations, not forecasts, and not a guarantee of future returns.</p>
    <section class="dashboard" aria-label="Static artifact dashboard">
      <article class="dashboard-card" data-artifact="single-report">
        <h2>Single Report</h2>
        <p class="artifact-path">reports/sample-report.html</p>
        <p>Scenario/Risk Interpretation in HTML plus matching scenario_risk_interpretation JSON.</p>
        <p class="artifact-links"><a href="sample-report.html">HTML</a><a href="sample-report.md">Markdown</a><a href="sample-report.json">JSON</a></p>
      </article>
      <article class="dashboard-card" data-artifact="regime-comparison">
        <h2>Regime Comparison</h2>
        <p class="artifact-path">reports/regime-comparison.html</p>
        <p>Synthetic bull, choppy, and drawdown-recovery fixture diagnostics.</p>
        <p class="artifact-links"><a href="regime-comparison.html">HTML</a><a href="regime-comparison.md">Markdown</a><a href="regime-comparison.json">JSON</a></p>
      </article>
      <article class="dashboard-card" data-artifact="fee-sensitivity">
        <h2>Fee Sensitivity</h2>
        <p class="artifact-path">reports/fee-sensitivity.md</p>
        <p>Research-only fee_bps assumption comparison for the single backtest settings.</p>
        <p class="artifact-links"><a href="fee-sensitivity.md">Markdown</a><a href="fee-sensitivity.json">JSON</a></p>
      </article>
      <article class="dashboard-card" data-artifact="split-sweep">
        <h2>Split Sweep</h2>
        <p class="artifact-path">reports/sample-sweep-split.html</p>
        <p>Train/test ranking, return-gap, and robustness_flag diagnostics.</p>
        <p class="artifact-links"><a href="sample-sweep-split.html">HTML</a><a href="sample-sweep-split.md">Markdown</a><a href="sample-sweep-split.json">JSON</a><a href="../docs/split-sweep-walkthrough.md">Walkthrough</a></p>
      </article>
      <article class="dashboard-card" data-artifact="manifest">
        <h2>Manifest</h2>
        <p class="artifact-path">reports/sample-manifest.md</p>
        <p>Reproduction record plus static gallery contract for local relative links.</p>
        <p class="artifact-links"><a href="sample-manifest.md">Sample</a><a href="../docs/static-gallery-manifest.md">Static Demo</a></p>
      </article>
    </section>
    <p><strong>Leveraged ETF-like limits:</strong> the sample names are placeholders, and leveraged ETF products can behave in ways beginners may not expect. Daily resets make multi-day results depend on the path of daily moves; losses can grow quickly; and real funds include fund expenses, financing costs, tracking differences, taxes, liquidity, and market impact that these sample artifacts do not model.</p>
    <p><strong>Regime-comparison limits:</strong> the bull, choppy, and drawdown-recovery labels are deterministic fixture scenarios for research review and tests. They are not market classifications, recommendations, forecasts, or a guarantee of future returns.</p>
    <h2>Open These First</h2>
    <ul>
      <li><a href="../docs/cold-review-checklist.md">Cold review checklist</a></li>
      <li><a href="../docs/static-gallery-manifest.md">Static demo manifest</a></li>
      <li><a href="../docs/artifact-gallery.md">Artifact gallery notes</a></li>
      <li><a href="../docs/split-sweep-walkthrough.md">Split-sweep walkthrough</a></li>
      <li><a href="sample-manifest.md">Sample manifest</a></li>
    </ul>
    <h2>Parameter Sweep</h2>
    <ul>
      <li><a href="sample-sweep.html">HTML sweep</a></li>
      <li><a href="sample-sweep.md">Markdown sweep</a></li>
      <li><a href="sample-sweep.json">JSON sweep</a></li>
    </ul>
  </main>
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
        *find_v160_static_dashboard_issues(REPO_ROOT),
        *find_regime_comparison_html_issues(REPO_ROOT),
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

    print(
        "Created sample report gallery, report, manifest, sweep, split sweep, "
        "fee sensitivity, regime comparison, and HTML artifacts."
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
    if "v1.6.0 static artifact dashboard" not in text:
        issues.append(f"{relative_source}: missing v1.6 dashboard heading text")
    if 'aria-label="Static artifact dashboard"' not in text:
        issues.append(f"{relative_source}: missing v1.6 dashboard landmark")

    links = _local_links_for_source(relative_source, text)
    for card_id, (title, visible_path, required_links) in V160_STATIC_DASHBOARD_CARDS.items():
        if f'data-artifact="{card_id}"' not in text:
            issues.append(f"{relative_source}: missing v1.6 dashboard card {card_id}")
        if f"<h2>{title}</h2>" not in text:
            issues.append(f"{relative_source}: missing v1.6 dashboard title {title}")
        if visible_path not in text:
            issues.append(
                f"{relative_source}: missing v1.6 dashboard artifact path {visible_path}"
            )
        for target in required_links:
            if target not in links:
                issues.append(
                    f"{relative_source}: missing v1.6 dashboard link to {target}"
                )
                continue
            link_path = _local_markdown_link_path(repo_root, source, target)
            if not link_path.exists():
                issues.append(f"{relative_source}: broken v1.6 dashboard link to {target}")
            elif link_path.stat().st_size == 0:
                issues.append(
                    f"{relative_source}: v1.6 dashboard link target is empty: {target}"
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
