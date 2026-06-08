from __future__ import annotations

import json
import subprocess
from pathlib import Path

from market_signal_lab.beginner_prediction_checklist import (
    build_beginner_prediction_checklist,
    render_beginner_prediction_checklist,
)
from scripts import selfcheck


def test_selfcheck_pytest_excludes_wheel_smoke(monkeypatch) -> None:
    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(args[0], 0, "", "")

    monkeypatch.setattr(selfcheck.subprocess, "run", fake_run)

    assert selfcheck.run_pytest() is True

    command = calls[0][0][0]
    assert command[-3:] == ["pytest", "-m", "not wheel_smoke"]


def test_selfcheck_regenerates_static_gallery_contract() -> None:
    assert Path("reports/index.html") in selfcheck.SAMPLE_ARTIFACTS
    assert Path("reports/index.html") in selfcheck.HTML_LINK_SOURCES
    assert (
        Path("reports/cross-asset-thesis-ledger-acceptance.md")
        in selfcheck.SAMPLE_ARTIFACTS
    )
    assert (
        Path("reports/cross-asset-thesis-ledger-acceptance.json")
        in selfcheck.SAMPLE_ARTIFACTS
    )
    assert Path("docs/release-notes-v1.14.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.14.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.15.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.15.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.16.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.16.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/architecture.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/adr/0001-static-research-artifacts.md") in (
        selfcheck.DOC_LINK_SOURCES
    )
    assert Path("docs/release-notes-v1.19.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.19.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.18.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.17.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/methodology-audit-review-schema.md") in (
        selfcheck.DOC_LINK_SOURCES
    )
    assert Path("reports/methodology-audit-score.html") in selfcheck.SAMPLE_ARTIFACTS
    assert Path("reports/methodology-audit-score.html") in selfcheck.HTML_LINK_SOURCES

    gallery = selfcheck.GALLERY_HTML
    assert "<script" not in gallery.lower()
    assert "src=" not in gallery.lower()
    assert "http://" not in gallery
    assert "https://" not in gallery
    assert "research-only" in gallery
    assert "not investment advice" in gallery
    assert "not a guarantee of future returns" in gallery
    assert "Regime comparison" in gallery
    assert "Secondary Docs And Release Links" in gallery
    assert 'aria-label="Primary actions"' in gallery
    for required_text in selfcheck.V130_STATIC_GALLERY_REQUIRED_TEXT:
        assert required_text in gallery
    assert "no JavaScript, no external assets, no live data" in gallery
    assert selfcheck.V160_STATIC_GALLERY_REQUIRED_COMMAND in gallery
    for required_text in selfcheck.V160_STATIC_GALLERY_REQUIRED_SECTIONS:
        assert required_text in gallery
    for title, link in selfcheck.V160_STATIC_PRIMARY_ACTIONS.values():
        assert title in gallery
        assert f'href="{link}"' in gallery
    primary_section = selfcheck.HTML_PRIMARY_ACTIONS_SECTION_RE.search(gallery)
    assert primary_section is not None
    primary_section = primary_section.group(1)
    assert "documentation-boundary audit only" in gallery
    assert "not a trading signal" in gallery
    assert "order workflow" in gallery
    assert "position-sizing input" in gallery
    assert primary_section.count("<a ") == 4

    expected_links = {
        "../docs/split-sweep-walkthrough.md",
        "../docs/local-audit-commands.md",
        "../docs/release-notes-v1.23.0.md",
        "../docs/release-notes-v1.22.1.md",
        "../docs/release-notes-v1.22.0.md",
        "../docs/release-v1.22.0.md",
        "sample-report.html",
        "methodology-audit-score.html",
        "methodology-audit-score.md",
        "methodology-audit-score.json",
        "fee-sensitivity.md",
        "fee-sensitivity.json",
        "cross-asset-thesis-ledger.md",
        "cross-asset-thesis-ledger.json",
        "reviewer-evidence-bundle.md",
        "reviewer-evidence-bundle.json",
        "regime-comparison.html",
        "regime-comparison.md",
        "regime-comparison.json",
        "sample-sweep.html",
        "sample-sweep-split.html",
        "../docs/static-gallery-manifest.md",
        "../docs/static-gallery-walkthrough.svg",
    }
    for link in expected_links:
        assert f'href="{link}"' in gallery


def test_v131_root_landing_contract_accepts_current_tree() -> None:
    issues = selfcheck.find_v131_root_landing_issues(selfcheck.REPO_ROOT)

    assert issues == []


def test_v131_root_landing_is_static_and_local() -> None:
    assert Path("index.html") in selfcheck.HTML_LINK_SOURCES
    assert Path("index.html") in selfcheck.PUBLIC_CLAIM_SOURCES

    landing = Path("index.html").read_text(encoding="utf-8")
    assert "<script" not in landing.lower()
    assert "src=" not in landing.lower()
    assert "http://" not in landing
    assert "https://" not in landing
    assert "reports/index.html" in landing
    assert "docs/cold-user-evidence-card.md" in landing
    assert "docs/index.md" in landing
    assert "docs/static-gallery-manifest.md" in landing
    assert "docs/methodology-audit.md" in landing
    assert "docs/methodology-audit-review-schema.md" in landing
    assert "docs/architecture.md" in landing
    assert "docs/adr/0001-static-research-artifacts.md" in landing
    assert "docs/release-notes-v1.19.0.md" in landing
    assert "docs/release-v1.19.0.md" in landing
    assert "docs/release-notes-v1.21.0.md" in landing
    assert "docs/release-v1.21.0.md" in landing
    assert "docs/release-notes-v1.23.0.md" in landing
    assert "docs/release-notes-v1.22.1.md" in landing
    assert "docs/release-notes-v1.22.0.md" in landing
    assert "docs/release-v1.22.0.md" in landing
    assert "reports/reviewer-evidence-bundle.md" in landing
    assert "reports/beginner-prediction-checklist.md" in landing
    assert "docs/release-notes-v1.18.0.md" in landing
    assert "docs/release-v1.17.0.md" in landing
    assert "docs/release-notes-v1.16.0.md" in landing
    assert "docs/release-v1.16.0.md" in landing
    assert "docs/release-notes-v1.14.0.md" in landing
    assert "docs/release-v1.14.0.md" in landing
    assert "docs/release-notes-v1.15.0.md" in landing
    assert "docs/release-v1.15.0.md" in landing
    assert "docs/release-notes-v1.13.0.md" in landing
    assert "docs/release-v1.13.0.md" in landing
    assert "docs/release-notes-v1.12.0.md" in landing
    assert "docs/release-v1.12.0.md" in landing
    assert "docs/release-notes-v1.11.0.md" in landing
    assert "docs/release-v1.11.0.md" in landing
    assert "docs/release-notes-v1.10.0.md" in landing
    assert "docs/release-v1.10.0.md" in landing
    assert "docs/release-notes-v1.9.1.md" in landing
    assert "docs/release-v1.9.1.md" in landing
    assert "does not connect to brokers" in landing
    assert "investment advice" in landing


def test_evidence_card_docs_exist_and_are_linked_from_public_indexes() -> None:
    evidence_card_docs = (
        Path("docs/cold-user-evidence-card.md"),
        Path("docs/evidence-card-walkthrough.svg"),
    )
    source_links = {
        Path("README.md"): (
            "docs/cold-user-evidence-card.md",
            "docs/evidence-card-walkthrough.svg",
        ),
        Path("index.html"): (
            "docs/cold-user-evidence-card.md",
        ),
        Path("docs/index.md"): (
            "cold-user-evidence-card.md",
            "evidence-card-walkthrough.svg",
        ),
        Path("docs/static-gallery-manifest.md"): (
            "cold-user-evidence-card.md",
            "evidence-card-walkthrough.svg",
        ),
    }

    for document_file in evidence_card_docs:
        assert (selfcheck.REPO_ROOT / document_file).is_file()

    for source_file, required_links in source_links.items():
        source_text = (selfcheck.REPO_ROOT / source_file).read_text(encoding="utf-8")
        assert "file://" not in source_text
        assert str(selfcheck.REPO_ROOT) not in source_text
        for required_link in required_links:
            assert required_link in source_text


def test_public_share_reviewer_and_promotion_docs_are_linked() -> None:
    public_handoff_docs = (
        Path("docs/public-share-summary.md"),
        Path("docs/reviewer-faq.md"),
        Path("docs/promotion-checklist.md"),
    )
    source_links = {
        Path("README.md"): (
            "docs/public-share-summary.md",
            "docs/reviewer-faq.md",
            "docs/promotion-checklist.md",
        ),
        Path("index.html"): (
            "docs/public-share-summary.md",
            "docs/reviewer-faq.md",
            "docs/promotion-checklist.md",
        ),
        Path("docs/index.md"): (
            "public-share-summary.md",
            "reviewer-faq.md",
            "promotion-checklist.md",
            "architecture.md",
            "adr/0001-static-research-artifacts.md",
            "methodology-audit.md",
            "methodology-audit-review-schema.md",
        ),
        Path("docs/static-gallery-manifest.md"): (
            "public-share-summary.md",
            "reviewer-faq.md",
            "promotion-checklist.md",
            "architecture.md",
            "adr/0001-static-research-artifacts.md",
            "methodology-audit.md",
            "methodology-audit-review-schema.md",
        ),
    }

    for document_file in public_handoff_docs:
        assert (selfcheck.REPO_ROOT / document_file).is_file()

    for source_file, required_links in source_links.items():
        source_text = (selfcheck.REPO_ROOT / source_file).read_text(encoding="utf-8")
        assert "file://" not in source_text
        assert str(selfcheck.REPO_ROOT) not in source_text
        for required_link in required_links:
            assert required_link in source_text


def test_v131_root_landing_contract_covers_evidence_card_and_release_docs() -> None:
    required_links = {
        "docs/cold-user-evidence-card.md",
        "docs/methodology-audit-review-schema.md",
        "docs/architecture.md",
        "docs/adr/0001-static-research-artifacts.md",
        "docs/three-minute-review.md",
        "docs/local-audit-commands.md",
        "docs/public-share-copy.md",
        "docs/reviewer-decision-tree.md",
        "docs/quick-tour-preview.md",
        "docs/quick-tour-preview.svg",
        "reports/reviewer-evidence-bundle.md",
        "reports/beginner-prediction-checklist.md",
        "docs/release-notes-v1.23.0.md",
        "docs/release-notes-v1.22.1.md",
        "docs/release-notes-v1.22.0.md",
        "docs/release-v1.22.0.md",
        "docs/release-notes-v1.21.0.md",
        "docs/release-v1.21.0.md",
        "docs/release-notes-v1.20.4.md",
        "docs/release-v1.20.4.md",
        "docs/release-notes-v1.20.3.md",
        "docs/release-v1.20.3.md",
        "docs/release-notes-v1.20.2.md",
        "docs/release-v1.20.2.md",
        "docs/release-notes-v1.20.1.md",
        "docs/release-v1.20.1.md",
        "docs/release-notes-v1.20.0.md",
        "docs/release-v1.20.0.md",
        "docs/release-notes-v1.19.0.md",
        "docs/release-v1.19.0.md",
        "docs/release-notes-v1.18.0.md",
        "docs/release-v1.18.0.md",
        "docs/release-notes-v1.17.0.md",
        "docs/release-v1.17.0.md",
        "docs/release-notes-v1.15.0.md",
        "docs/release-v1.15.0.md",
        "docs/release-notes-v1.14.0.md",
        "docs/release-v1.14.0.md",
        "docs/release-notes-v1.13.0.md",
        "docs/release-v1.13.0.md",
        "docs/release-notes-v1.12.0.md",
        "docs/release-v1.12.0.md",
        "docs/release-notes-v1.11.0.md",
        "docs/release-v1.11.0.md",
    }

    assert required_links.issubset(set(selfcheck.V131_ROOT_LANDING_LINKS))


def test_v131_root_landing_contract_requires_gallery_link(tmp_path: Path) -> None:
    _write_v131_landing_fixture(tmp_path, omit_link="reports/index.html")

    issues = selfcheck.find_v131_root_landing_issues(tmp_path)

    assert issues == [
        "index.html: missing v1.3.1 landing link to reports/index.html"
    ]


def test_v131_root_landing_contract_rejects_remote_assets(tmp_path: Path) -> None:
    _write_v131_landing_fixture(
        tmp_path,
        extra_html='<link rel="stylesheet" href="/assets/site.css">\n'
        '<img src="https://example.com/chart.png" alt="Remote chart">\n',
    )

    issues = selfcheck.find_v131_root_landing_issues(tmp_path)

    assert issues == [
        "index.html: root landing must use relative local links and assets, "
        "found /assets/site.css",
        "index.html: root landing must use relative local links and assets, "
        "found https://example.com/chart.png",
    ]


def test_v090_demo_acceptance_contract_accepts_current_tree() -> None:
    issues = selfcheck.find_v090_demo_acceptance_issues(selfcheck.REPO_ROOT)

    assert issues == []


def test_v090_demo_acceptance_contract_reports_missing_required_link(tmp_path: Path) -> None:
    _write_demo_contract_fixture(
        tmp_path,
        '<a href="../docs/split-sweep-walkthrough.md">Walkthrough</a>\n'
        '<a href="sample-sweep-split.html">HTML split sweep</a>\n'
        '<a href="sample-sweep-split.md">Markdown split sweep</a>\n',
    )

    issues = selfcheck.find_v090_demo_acceptance_issues(tmp_path)

    assert issues == [
        "reports/index.html: missing required demo link to sample-sweep-split.json"
    ]


def test_v090_demo_acceptance_contract_reports_empty_target(tmp_path: Path) -> None:
    _write_demo_contract_fixture(
        tmp_path,
        '<a href="../docs/split-sweep-walkthrough.md">Walkthrough</a>\n'
        '<a href="sample-sweep-split.html">HTML split sweep</a>\n'
        '<a href="sample-sweep-split.md">Markdown split sweep</a>\n'
        '<a href="sample-sweep-split.json">JSON split sweep</a>\n',
        json_text="",
    )

    issues = selfcheck.find_v090_demo_acceptance_issues(tmp_path)

    assert issues == [
        "docs/split-sweep-walkthrough.md: required demo link target is empty: "
        "../reports/sample-sweep-split.json",
        "reports/index.html: required demo link target is empty: sample-sweep-split.json",
    ]


def test_v090_demo_acceptance_contract_rejects_remote_gallery_assets(
    tmp_path: Path,
) -> None:
    _write_demo_contract_fixture(
        tmp_path,
        '<a href="../docs/split-sweep-walkthrough.md">Walkthrough</a>\n'
        '<a href="sample-sweep-split.html">HTML split sweep</a>\n'
        '<a href="sample-sweep-split.md">Markdown split sweep</a>\n'
        '<a href="sample-sweep-split.json">JSON split sweep</a>\n'
        '<a HREF = "https://example.com/report.html">Remote report</a>\n'
        '<img SRC = "//example.com/chart.png" alt="Remote chart">\n',
    )

    issues = selfcheck.find_v090_demo_acceptance_issues(tmp_path)

    assert issues == [
        "reports/index.html: static demo must use relative local links and assets, "
        "found https://example.com/report.html",
        "reports/index.html: static demo must use relative local links and assets, "
        "found //example.com/chart.png",
    ]


def test_v130_static_gallery_contract_accepts_current_tree() -> None:
    issues = selfcheck.find_v130_static_gallery_issues(selfcheck.REPO_ROOT)

    assert issues == []


def test_v130_static_gallery_contract_requires_manifest_link(tmp_path: Path) -> None:
    _write_v130_gallery_fixture(tmp_path, omit_link="../docs/static-gallery-manifest.md")

    issues = selfcheck.find_v130_static_gallery_issues(tmp_path)

    assert issues == [
        "reports/index.html: missing v1.3 gallery link to ../docs/static-gallery-manifest.md"
    ]


def test_v130_static_gallery_contract_requires_scenario_risk_inventory(
    tmp_path: Path,
) -> None:
    _write_v130_gallery_fixture(tmp_path, include_required_text=False)

    issues = selfcheck.find_v130_static_gallery_issues(tmp_path)

    assert issues == [
        "reports/index.html: missing v1.3 gallery inventory text "
        "Scenario/Risk Interpretation",
        "reports/index.html: missing v1.3 gallery inventory text "
        "scenario_risk_interpretation",
    ]


def test_v130_static_gallery_contract_rejects_remote_assets(tmp_path: Path) -> None:
    _write_v130_gallery_fixture(
        tmp_path,
        extra_html='<link rel="stylesheet" href=/assets/site.css>\n'
        '<img src="https://example.com/chart.png" alt="Remote chart">\n',
    )

    issues = selfcheck.find_v130_static_gallery_issues(tmp_path)

    assert issues == [
        "reports/index.html: static gallery must use relative local links and assets, "
        "found /assets/site.css",
        "reports/index.html: static gallery must use relative local links and assets, "
        "found https://example.com/chart.png",
    ]


def test_v130_static_gallery_contract_rejects_common_remote_asset_attrs(
    tmp_path: Path,
) -> None:
    _write_v130_gallery_fixture(
        tmp_path,
        extra_html='<video poster="file:preview.png"></video>\n'
        '<img srcset="local-small.png 1x, //example.com/chart.png 2x" alt="Chart">\n',
    )

    issues = selfcheck.find_v130_static_gallery_issues(tmp_path)

    assert issues == [
        "reports/index.html: static gallery must use relative local links and assets, "
        "found file:preview.png",
        "reports/index.html: static gallery must use relative local links and assets, "
        "found //example.com/chart.png",
    ]


def test_v130_static_gallery_contract_rejects_non_local_schemes(
    tmp_path: Path,
) -> None:
    _write_v130_gallery_fixture(
        tmp_path,
        extra_html='<a href=javascript:alert(1)>Action</a>\n'
        '<img src="data:image/png;base64,abc" alt="Inline">\n',
    )

    issues = selfcheck.find_v130_static_gallery_issues(tmp_path)

    assert issues == [
        "reports/index.html: static gallery must use relative local links and assets, "
        "found javascript:alert(1)",
        "reports/index.html: static gallery must use relative local links and assets, "
        "found data:image/png;base64,abc",
    ]


def test_v160_static_dashboard_contract_accepts_current_tree() -> None:
    issues = selfcheck.find_v160_static_dashboard_issues(selfcheck.REPO_ROOT)

    assert issues == []


def test_v160_static_dashboard_contract_requires_four_primary_actions(
    tmp_path: Path,
) -> None:
    reports_dir = tmp_path / "reports"
    docs_dir = tmp_path / "docs"
    reports_dir.mkdir()
    docs_dir.mkdir()
    for path in (
        reports_dir / "sample-report.html",
        reports_dir / "sample-report.md",
        reports_dir / "sample-report.json",
        reports_dir / "pretrade-packet.md",
        reports_dir / "pretrade-packet.json",
        reports_dir / "scenario-card.md",
        reports_dir / "scenario-card.json",
        reports_dir / "regime-comparison.html",
        reports_dir / "regime-comparison.md",
        reports_dir / "regime-comparison.json",
        reports_dir / "fee-sensitivity.md",
        reports_dir / "fee-sensitivity.json",
        reports_dir / "cross-asset-thesis-ledger.md",
        reports_dir / "cross-asset-thesis-ledger.json",
        reports_dir / "reviewer-evidence-bundle.md",
        reports_dir / "reviewer-evidence-bundle.json",
        reports_dir / "beginner-prediction-checklist.md",
        reports_dir / "beginner-prediction-checklist.json",
        reports_dir / "sample-sweep-split.html",
        reports_dir / "sample-sweep-split.md",
        reports_dir / "sample-sweep-split.json",
        reports_dir / "sample-manifest.md",
        docs_dir / "static-gallery-manifest.md",
    ):
        path.write_text("artifact\n", encoding="utf-8")
    (reports_dir / "index.html").write_text(
        '<main>\n'
        '<section class="primary-actions" aria-label="Primary actions">\n'
        '<a href="sample-report.html">View sample report</a>\n'
        "</section>\n"
        "</main>\n",
        encoding="utf-8",
    )

    issues = selfcheck.find_v160_static_dashboard_issues(tmp_path)

    assert issues == [
        "reports/index.html: missing verification command",
        "reports/index.html: missing simplified gallery text Static research sample",
        "reports/index.html: missing simplified gallery text Beginner boundary",
        "reports/index.html: missing simplified gallery text Run One Verification Command",
        "reports/index.html: missing simplified gallery text What To Read First",
        "reports/index.html: missing simplified gallery text Secondary Docs And Release Links",
        "reports/index.html: primary actions must contain exactly 4 links",
        "reports/index.html: missing primary action Beginner backtest checklist",
        (
            "reports/index.html: missing primary action link to "
            "beginner-prediction-checklist.md"
        ),
        "reports/index.html: missing primary action Prediction-readiness audit",
        (
            "reports/index.html: missing primary action link to "
            "prediction-readiness-audit.md"
        ),
        "reports/index.html: missing primary action Run one verification command",
        "reports/index.html: missing primary action link to #verify",
    ]


def test_v160_static_dashboard_contract_checks_primary_action_text_in_section(
    tmp_path: Path,
) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    for path in (
        reports_dir / "sample-report.html",
        reports_dir / "beginner-prediction-checklist.md",
        reports_dir / "prediction-readiness-audit.md",
    ):
        path.write_text("artifact\n", encoding="utf-8")
    (reports_dir / "index.html").write_text(
        '<main>\n'
        "<p>Static research sample</p>\n"
        "<p>Beginner boundary</p>\n"
        "<h2>Run One Verification Command</h2>\n"
        "<p>What To Read First</p>\n"
        "<p>Secondary Docs And Release Links</p>\n"
        '<p>Beginner backtest checklist</p>\n'
        '<section aria-label="Primary actions" class="primary-actions featured">\n'
        '<a href="sample-report.html">View sample report</a>\n'
        '<a href="beginner-prediction-checklist.md">Read checklist</a>\n'
        '<a href="prediction-readiness-audit.md">Prediction-readiness audit</a>\n'
        '<a href="#verify">Run one verification command</a>\n'
        "</section>\n"
        '<h2 id="verify">Verify</h2>\n'
        "<pre>python -m market_signal_lab.cli --validate-thesis-ledger</pre>\n"
        "</main>\n",
        encoding="utf-8",
    )

    issues = selfcheck.find_v160_static_dashboard_issues(tmp_path)

    assert issues == [
        "reports/index.html: missing primary action Beginner backtest checklist"
    ]


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


def test_selfcheck_regenerates_pretrade_packet_artifacts() -> None:
    expected_artifacts = {
        Path("reports/pretrade-packet.md"),
        Path("reports/pretrade-packet.json"),
    }

    assert expected_artifacts.issubset(set(selfcheck.SAMPLE_ARTIFACTS))
    assert expected_artifacts.issubset(set(selfcheck.PUBLIC_CLAIM_SOURCES))
    assert "pretrade-packet.md" in selfcheck.V130_STATIC_GALLERY_LINKS
    assert "pretrade-packet.json" in selfcheck.V130_STATIC_GALLERY_LINKS
    assert 'href="pretrade-packet.md"' in selfcheck.GALLERY_HTML
    assert 'href="pretrade-packet.json"' in selfcheck.GALLERY_HTML

    command = _pretrade_packet_command()
    assert "--pretrade-packet" in command
    assert command[command.index("--output") + 1] == "reports/pretrade-packet.md"
    assert command[command.index("--json-output") + 1] == "reports/pretrade-packet.json"


def test_selfcheck_regenerates_scenario_card_artifacts() -> None:
    expected_artifacts = {
        Path("reports/scenario-card.md"),
        Path("reports/scenario-card.json"),
    }

    assert expected_artifacts.issubset(set(selfcheck.SAMPLE_ARTIFACTS))
    assert expected_artifacts.issubset(set(selfcheck.PUBLIC_CLAIM_SOURCES))
    assert "scenario-card.md" in selfcheck.V130_STATIC_GALLERY_LINKS
    assert "scenario-card.json" in selfcheck.V130_STATIC_GALLERY_LINKS
    assert 'href="scenario-card.md"' in selfcheck.GALLERY_HTML
    assert 'href="scenario-card.json"' in selfcheck.GALLERY_HTML

    command = _scenario_card_command()
    assert "--scenario-card" in command
    assert "--output" not in command
    assert "--json-output" not in command


def test_selfcheck_regenerates_cross_asset_thesis_ledger_artifacts() -> None:
    expected_artifacts = {
        Path("reports/cross-asset-thesis-ledger.md"),
        Path("reports/cross-asset-thesis-ledger.json"),
    }

    assert expected_artifacts.issubset(set(selfcheck.SAMPLE_ARTIFACTS))
    assert expected_artifacts.issubset(set(selfcheck.PUBLIC_CLAIM_SOURCES))
    assert "cross-asset-thesis-ledger.md" in selfcheck.V130_STATIC_GALLERY_LINKS
    assert "cross-asset-thesis-ledger.json" in selfcheck.V130_STATIC_GALLERY_LINKS
    assert 'href="cross-asset-thesis-ledger.md"' in selfcheck.GALLERY_HTML
    assert 'href="cross-asset-thesis-ledger.json"' in selfcheck.GALLERY_HTML
    assert "QQQ_LIKE, QLD_LIKE, and TQQQ_LIKE" in selfcheck.GALLERY_HTML


def test_pretrade_packet_acceptance_contract_accepts_current_tree() -> None:
    issues = selfcheck.find_pretrade_packet_acceptance_issues(selfcheck.REPO_ROOT)

    assert issues == []


def test_beginner_prediction_checklist_contract_accepts_current_tree() -> None:
    issues = selfcheck.find_beginner_prediction_checklist_issues(selfcheck.REPO_ROOT)

    assert issues == []


def test_prediction_readiness_audit_contract_accepts_current_tree() -> None:
    issues = selfcheck.find_prediction_readiness_audit_issues(selfcheck.REPO_ROOT)

    assert issues == []


def test_prediction_readiness_audit_selfcheck_accepts_valid_fixture(
    tmp_path: Path,
) -> None:
    _write_prediction_readiness_audit_fixture(tmp_path)

    issues = selfcheck.find_prediction_readiness_audit_issues(tmp_path)

    assert issues == []


def test_prediction_readiness_audit_selfcheck_detects_broken_audit_artifacts(
    tmp_path: Path,
) -> None:
    payload = _write_prediction_readiness_audit_fixture(tmp_path)
    payload["summary"]["pass_count"] = 99
    payload["summary"]["review_boundary"] = "Use this audit for trade approval."
    payload["verification_commands"] = ["python -m pytest"]
    payload["criteria"] = [
        item
        for item in payload["criteria"]
        if item["criterion"] != "static_data"
    ]
    (tmp_path / "reports" / "prediction-readiness-audit.json").write_text(
        json.dumps(payload, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (tmp_path / "reports" / "prediction-readiness-audit.md").write_text(
        "# Prediction-Readiness Audit\n",
        encoding="utf-8",
    )

    issues = selfcheck.find_prediction_readiness_audit_issues(tmp_path)

    assert (
        "reports/prediction-readiness-audit.json: summary.review_boundary must "
        "preserve non-prediction wording"
    ) in issues
    assert (
        "reports/prediction-readiness-audit.json: criteria must include the "
        "six prediction-readiness checks"
    ) in issues
    assert (
        "reports/prediction-readiness-audit.json: missing criterion static_data"
    ) in issues
    assert (
        "reports/prediction-readiness-audit.json: summary.pass_count is stale"
    ) in issues
    assert (
        "reports/prediction-readiness-audit.json: missing verification command "
        "python -m market_signal_lab.cli --prediction-readiness-audit"
    ) in issues
    assert (
        "reports/prediction-readiness-audit.md: missing audit text "
        "## How to Read This"
    ) in issues


def test_beginner_prediction_checklist_artifacts_are_in_public_gallery_contract() -> None:
    expected_artifacts = {
        Path("reports/beginner-prediction-checklist.md"),
        Path("reports/beginner-prediction-checklist.json"),
    }

    assert expected_artifacts.issubset(set(selfcheck.SAMPLE_ARTIFACTS))
    assert expected_artifacts.issubset(set(selfcheck.PUBLIC_CLAIM_SOURCES))
    assert "beginner-prediction-checklist.md" in selfcheck.V130_STATIC_GALLERY_LINKS
    assert "beginner-prediction-checklist.json" in selfcheck.V130_STATIC_GALLERY_LINKS
    assert 'href="beginner-prediction-checklist.md"' in selfcheck.GALLERY_HTML
    assert 'href="beginner-prediction-checklist.json"' in selfcheck.GALLERY_HTML
    assert "Beginner Backtest Reading Checklist" in selfcheck.GALLERY_HTML


def test_selfcheck_regenerates_beginner_prediction_checklist_via_cli() -> None:
    assert any(
        "--beginner-prediction-checklist" in command
        for command in selfcheck._sample_artifact_commands()
    )


def test_beginner_prediction_checklist_contract_reports_boundary_regressions(
    tmp_path: Path,
) -> None:
    reports_dir = tmp_path / "reports"
    docs_dir = tmp_path / "docs"
    reports_dir.mkdir()
    docs_dir.mkdir()

    for source_path in selfcheck.BEGINNER_PREDICTION_CHECKLIST_REQUIRED_SOURCES:
        path = tmp_path / source_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {source_path.name}\n", encoding="utf-8")

    payload = build_beginner_prediction_checklist()
    payload["recommended_sources_to_open"].remove("docs/risk-boundaries.md")
    payload["public_reviewer_reuse_reason"] = "Public checklist."
    payload["risk_boundaries"]["scope_limits"] = "Static artifact only."
    payload["risk_boundaries"][
        "leveraged_etf_daily_reset_path_dependency"
    ] = "Leveraged examples require caution."
    markdown = render_beginner_prediction_checklist(payload).replace(
        "predictions of future returns, recommendations, trading instructions, or investment advice",
        "predictions of future returns",
    )

    (reports_dir / "beginner-prediction-checklist.json").write_text(
        json.dumps(payload),
        encoding="utf-8",
    )
    (reports_dir / "beginner-prediction-checklist.md").write_text(
        markdown,
        encoding="utf-8",
    )

    issues = selfcheck.find_beginner_prediction_checklist_issues(tmp_path)

    assert (
        "reports/beginner-prediction-checklist.json: missing recommended source "
        "docs/risk-boundaries.md"
    ) in issues
    assert (
        "reports/beginner-prediction-checklist.json: "
        "public_reviewer_reuse_reason must explain why public reviewers can "
        "reference the artifact without weakening no-advice boundaries"
    ) in issues
    assert (
        "reports/beginner-prediction-checklist.json: scope limits must preserve "
        "public-safe boundaries"
    ) in issues
    assert (
        "reports/beginner-prediction-checklist.json: leveraged ETF boundary must "
        "preserve daily-reset/path-dependency wording"
    ) in issues
    assert (
        "reports/beginner-prediction-checklist.md: missing checklist text "
        "predictions of future returns, recommendations, trading instructions, or investment advice"
    ) in issues
    assert (
        "reports/beginner-prediction-checklist.md: missing core no-advice phrase "
        "predictions of future returns, recommendations, trading instructions, or investment advice"
    ) in issues


def test_beginner_prediction_checklist_contract_reports_schema_shape_regressions(
    tmp_path: Path,
) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()

    for source_path in selfcheck.BEGINNER_PREDICTION_CHECKLIST_REQUIRED_SOURCES:
        path = tmp_path / source_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {source_path.name}\n", encoding="utf-8")

    payload = build_beginner_prediction_checklist()
    payload["unexpected_schema_field"] = "extra"
    payload["default_outputs"] = {
        "json": "reports/beginner-prediction-checklist.json",
        "markdown": "reports/beginner-prediction-checklist.md",
    }
    payload["reading_steps"][0]["unexpected_step_field"] = "extra"
    payload["risk_boundaries"] = {
        "scope_limits": payload["risk_boundaries"]["scope_limits"],
        "historical_backtest_limits": payload["risk_boundaries"][
            "historical_backtest_limits"
        ],
        "leveraged_etf_daily_reset_path_dependency": payload["risk_boundaries"][
            "leveraged_etf_daily_reset_path_dependency"
        ],
    }

    (reports_dir / "beginner-prediction-checklist.json").write_text(
        json.dumps(payload),
        encoding="utf-8",
    )
    (reports_dir / "beginner-prediction-checklist.md").write_text(
        render_beginner_prediction_checklist(payload),
        encoding="utf-8",
    )

    issues = selfcheck.find_beginner_prediction_checklist_issues(tmp_path)

    assert (
        "reports/beginner-prediction-checklist.json: top-level keys must match "
        "the beginner prediction checklist schema order"
    ) in issues
    assert (
        "reports/beginner-prediction-checklist.json: default_outputs keys must "
        "be markdown then json"
    ) in issues
    assert (
        "reports/beginner-prediction-checklist.json: reading_steps[1] keys must "
        "be step, label, beginner_note"
    ) in issues
    assert (
        "reports/beginner-prediction-checklist.json: risk_boundaries keys must "
        "match the beginner prediction checklist schema order"
    ) in issues


def test_pretrade_packet_acceptance_contract_reports_packet_regressions(
    tmp_path: Path,
) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    packet = _valid_pretrade_packet_payload()
    packet["research_only"] = False
    del packet["historical_diagnostics"]["metrics"]["max_drawdown"]
    packet["historical_diagnostics"]["exposure_trade_review"]["research_only"] = False
    packet["beginner_checklist"][0]["status"] = "done"
    packet["risk_boundaries"]["sample_backtest_limits"] = "Backtest sample."
    packet["risk_boundaries"]["scope_limits"] = "Local artifact."
    (reports_dir / "pretrade-packet.json").write_text(
        json.dumps(packet),
        encoding="utf-8",
    )
    (reports_dir / "pretrade-packet.md").write_text(
        "# Pre-Trade Research Packet\n"
        "## Source\n"
        "- **Input path**: examples/data/sample_tqqq_qld_like.csv\n"
        "- **Date range**: 2024-01-02 to 2024-01-11\n"
        "- **Rows reviewed**: 8\n"
        "## Assumptions\n"
        "## Historical Diagnostics\n"
        "## Scenario/Risk Interpretation\n"
        "## Beginner Checklist\n"
        "- [ ] One\n",
        encoding="utf-8",
    )

    issues = selfcheck.find_pretrade_packet_acceptance_issues(tmp_path)

    assert "reports/pretrade-packet.json: research_only must be true" in issues
    assert (
        "reports/pretrade-packet.json: missing "
        "historical_diagnostics.metrics.max_drawdown"
    ) in issues
    assert (
        "reports/pretrade-packet.json: "
        "historical_diagnostics.exposure_trade_review.research_only must be true"
    ) in issues
    assert (
        "reports/pretrade-packet.json: "
        "beginner_checklist[1].status must be review_required"
    ) in issues
    assert (
        "reports/pretrade-packet.json: "
        "risk_boundaries.scope_limits must preserve scope limits"
    ) in issues
    assert (
        "reports/pretrade-packet.json: "
        "risk_boundaries.sample_backtest_limits must preserve sample/backtest limitation wording"
    ) in issues
    assert "reports/pretrade-packet.md: missing packet section ## Risk Boundaries" in issues
    assert (
        "reports/pretrade-packet.md: packet Markdown must render the seven checklist items"
    ) in issues


def test_docs_link_sources_include_canonical_docs_map() -> None:
    assert Path("docs/index.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/split-sweep-walkthrough.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v0.8.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v0.8.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v0.9.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v0.9.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.0.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.0.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.1.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.1.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.2.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.2.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.2.1.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.2.1.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/static-gallery-manifest.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/methodology-audit.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/methodology-audit-review-schema.md") in (
        selfcheck.DOC_LINK_SOURCES
    )
    assert Path("docs/release-notes-v1.3.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.3.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.3.1.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.3.1.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/scenario-risk-glossary.md") in selfcheck.DOC_LINK_SOURCES


def test_public_claim_sources_include_v110_release_docs() -> None:
    assert Path("docs/release-notes-v1.1.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.1.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.2.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.2.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.2.1.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.2.1.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/static-gallery-manifest.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/methodology-audit.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/methodology-audit-review-schema.md") in (
        selfcheck.PUBLIC_CLAIM_SOURCES
    )
    assert Path("docs/release-notes-v1.3.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.3.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.3.1.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.3.1.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/scenario-risk-glossary.md") in selfcheck.PUBLIC_CLAIM_SOURCES


def test_doc_sources_include_latest_release_docs() -> None:
    assert Path("docs/release-notes-v1.5.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.5.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.5.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.5.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.6.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.6.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.6.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.6.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.7.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.7.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.7.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.7.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.8.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.8.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.8.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.8.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.9.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.9.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.9.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.9.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.10.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.10.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.11.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.11.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.12.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.12.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.12.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.12.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.13.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.13.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.13.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.13.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.14.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.14.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.14.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.14.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.15.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.15.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.15.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.15.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.16.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.16.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.16.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.16.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/architecture.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/adr/0001-static-research-artifacts.md") in (
        selfcheck.DOC_LINK_SOURCES
    )
    assert Path("docs/release-notes-v1.19.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.19.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/architecture.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/adr/0001-static-research-artifacts.md") in (
        selfcheck.PUBLIC_CLAIM_SOURCES
    )
    assert Path("docs/release-notes-v1.19.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.19.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-notes-v1.18.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.17.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.18.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES
    assert Path("docs/release-v1.17.0.md") in selfcheck.PUBLIC_CLAIM_SOURCES


def test_regime_comparison_artifacts_are_in_public_gallery_contract() -> None:
    expected_artifacts = {
        Path("reports/regime-comparison.md"),
        Path("reports/regime-comparison.json"),
        Path("reports/regime-comparison.html"),
    }

    assert expected_artifacts.issubset(set(selfcheck.SAMPLE_ARTIFACTS))
    assert expected_artifacts.issubset(set(selfcheck.PUBLIC_CLAIM_SOURCES))
    assert Path("reports/regime-comparison.html") in selfcheck.HTML_LINK_SOURCES

    command = _regime_comparison_command()
    assert command == [
        selfcheck.sys.executable,
        "-m",
        "market_signal_lab.cli",
        "--regime-comparison",
    ]

    for link in (
        "regime-comparison.html",
        "regime-comparison.md",
        "regime-comparison.json",
    ):
        assert link in selfcheck.V130_STATIC_GALLERY_LINKS
        assert f'href="{link}"' in selfcheck.GALLERY_HTML

    readme = Path("README.md").read_text(encoding="utf-8")
    docs_index = Path("docs/index.md").read_text(encoding="utf-8")
    gallery_notes = Path("docs/artifact-gallery.md").read_text(encoding="utf-8")
    for public_doc in (readme, docs_index, gallery_notes, selfcheck.GALLERY_HTML):
        assert "regime comparison" in public_doc.lower()
        assert "synthetic" in public_doc
        assert "research-only" in public_doc
        assert "guarantee of future returns" in public_doc

    assert selfcheck.find_regime_comparison_html_issues(selfcheck.REPO_ROOT) == []


def test_regime_comparison_html_selfcheck_rejects_remote_assets_and_missing_links(
    tmp_path: Path,
) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    (reports_dir / "regime-comparison.md").write_text("# Regime\n", encoding="utf-8")

    (reports_dir / "regime-comparison.html").write_text(
        "\n".join(
            [
                "<!doctype html>",
                "<title>Regime Comparison - Market Signal Lab</title>",
                "<h1>Regime Comparison - Market Signal Lab</h1>",
                "<script src=\"remote.js\"></script>",
                '<link rel="stylesheet" href="/assets/report.css">',
                '<a href="regime-comparison.md">Markdown report</a>',
                "<h2>Caveats</h2>",
                "<p>synthetic and not investment advice; no live-trading signal.</p>",
            ]
        ),
        encoding="utf-8",
    )

    issues = selfcheck.find_regime_comparison_html_issues(tmp_path)

    assert issues == [
        "reports/regime-comparison.html: regime comparison HTML must not include scripts",
        (
            "reports/regime-comparison.html: regime comparison HTML must use "
            "relative local links and assets, found /assets/report.css"
        ),
        (
            "reports/regime-comparison.html: missing regime comparison HTML text "
            "Related Artifacts"
        ),
        (
            "reports/regime-comparison.html: missing regime comparison HTML link "
            "to regime-comparison.json"
        ),
    ]


def test_scenario_risk_glossary_defines_beginner_diagnostics() -> None:
    glossary = Path("docs/scenario-risk-glossary.md").read_text(encoding="utf-8")

    for term in (
        "Exposure",
        "Modeled entry",
        "Modeled exit",
        "Fee drag",
        "Drawdown",
        "Buy-and-hold gap",
    ):
        assert f"**{term}**" in glossary

    assert "research-only historical review aids" in glossary
    assert "not investment advice" in glossary
    assert "not evidence of future performance" in glossary


def test_split_sweep_walkthrough_sets_public_demo_boundaries() -> None:
    walkthrough = Path("docs/split-sweep-walkthrough.md").read_text(encoding="utf-8")

    assert "GitHub Pages-friendly" in walkthrough
    assert "not investment advice" in walkthrough
    assert "not a recommendation" in walkthrough
    assert "../reports/sample-sweep-split.html" in walkthrough
    assert "`robustness_flag`" in walkthrough
    assert "`not_flagged` only means" in walkthrough


def test_docs_link_check_accepts_repo_local_links(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (tmp_path / "README.md").write_text(
        "[Docs](docs/index.md)\n[External](https://example.com)\n",
        encoding="utf-8",
    )
    (docs_dir / "index.md").write_text(
        "[Risk](risk-boundaries.md)\n[Root](../README.md)\n[Anchor](#start-here)\n",
        encoding="utf-8",
    )
    (docs_dir / "risk-boundaries.md").write_text("# Risk\n", encoding="utf-8")

    issues = selfcheck.find_markdown_link_issues(
        tmp_path,
        (Path("README.md"), Path("docs/index.md")),
    )

    assert issues == []


def test_docs_link_check_reports_broken_local_links(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text(
        "[Missing](missing.md)\n"
        "```markdown\n"
        "[Ignored](also-missing.md)\n"
        "```\n",
        encoding="utf-8",
    )

    issues = selfcheck.find_markdown_link_issues(tmp_path, (Path("docs/index.md"),))

    assert issues == ["docs/index.md: broken link to missing.md"]


def test_html_link_check_accepts_gallery_local_links(tmp_path: Path) -> None:
    reports_dir = tmp_path / "reports"
    docs_dir = tmp_path / "docs"
    reports_dir.mkdir()
    docs_dir.mkdir()
    (reports_dir / "index.html").write_text(
        '<a href="sample-report.html">Report</a>\n'
        '<a href="../docs/split-sweep-walkthrough.md">Walkthrough</a>\n'
        '<a href="#top">Anchor</a>\n',
        encoding="utf-8",
    )
    (reports_dir / "sample-report.html").write_text("<h1>Report</h1>\n", encoding="utf-8")
    (docs_dir / "split-sweep-walkthrough.md").write_text("# Walkthrough\n", encoding="utf-8")

    issues = selfcheck.find_html_link_issues(tmp_path, (Path("reports/index.html"),))

    assert issues == []


def test_html_link_check_reports_broken_local_links(tmp_path: Path) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    (reports_dir / "index.html").write_text(
        '<a href="missing.html">Missing</a>\n',
        encoding="utf-8",
    )

    issues = selfcheck.find_html_link_issues(tmp_path, (Path("reports/index.html"),))

    assert issues == ["reports/index.html: broken link to missing.html"]


def test_public_claim_check_rejects_unqualified_advice_claims(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "This strategy should buy the sample symbol tomorrow.\n",
        encoding="utf-8",
    )

    issues = selfcheck.find_public_claim_issues(tmp_path, (Path("README.md"),))

    assert issues == ["README.md:1: forbidden public claim 'should buy'"]


def test_public_claim_check_does_not_overapply_negation(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "This is not advice, but the strategy should buy the sample symbol.\n",
        encoding="utf-8",
    )

    issues = selfcheck.find_public_claim_issues(tmp_path, (Path("README.md"),))

    assert issues == ["README.md:1: forbidden public claim 'should buy'"]


def test_public_claim_check_accepts_current_public_docs_and_reports() -> None:
    issues = selfcheck.find_public_claim_issues(
        selfcheck.REPO_ROOT,
        selfcheck.PUBLIC_CLAIM_SOURCES,
    )

    assert issues == []


def test_fixture_provenance_check_accepts_current_metadata() -> None:
    issues = selfcheck.find_fixture_provenance_issues(selfcheck.REPO_ROOT)

    assert issues == []


def test_fixture_provenance_check_reports_missing_metadata(tmp_path: Path) -> None:
    issues = selfcheck.find_fixture_provenance_issues(tmp_path)

    assert issues == [
        "examples/data/sample_tqqq_qld_like.csv.provenance.json: "
        "provenance metadata file is missing",
        "examples/data/sample_multi_regime.csv.provenance.json: "
        "provenance metadata file is missing",
    ]


def test_fixture_provenance_check_requires_regime_public_trust_flags(
    tmp_path: Path,
) -> None:
    data_dir = tmp_path / "examples" / "data"
    data_dir.mkdir(parents=True)
    for name in ("sample_tqqq_qld_like.csv", "sample_multi_regime.csv"):
        (data_dir / name).write_text("date,open,high,low,close\n", encoding="utf-8")

    base_metadata = {
        "dataset_label": "sample",
        "data_kind": "synthetic_static_fixture",
        "source": "Synthetic fixture.",
        "created_date": "2026-05-25",
        "as_of_date": "2026-05-25",
        "limitations": ["Synthetic-only; not live data."],
        "research_only": True,
    }
    (data_dir / "sample_tqqq_qld_like.csv.provenance.json").write_text(
        json.dumps(base_metadata),
        encoding="utf-8",
    )

    multi_metadata = dict(base_metadata)
    multi_metadata["regimes"] = [
        {
            "symbol": "BULL_REGIME",
            "regime": "bull",
            "description": "Synthetic upward fixture.",
            "assumptions": ["Close prices increase by construction."],
            "synthetic_only": True,
            "not_predictive": True,
            "row_count": 12,
        }
    ]
    (data_dir / "sample_multi_regime.csv.provenance.json").write_text(
        json.dumps(multi_metadata),
        encoding="utf-8",
    )

    issues = selfcheck.find_fixture_provenance_issues(tmp_path)

    assert issues == [
        "examples/data/sample_multi_regime.csv.provenance.json: "
        "regimes[1].not_live_trading must be true"
    ]


def test_canonical_docs_map_links_every_docs_markdown_file() -> None:
    docs_index = Path("docs/index.md").read_text(encoding="utf-8")
    linked_docs = {
        Path(target.split("#", 1)[0])
        for target in selfcheck.MARKDOWN_LINK_RE.findall(docs_index)
        if target.endswith(".md")
    }
    expected_docs = {path.name for path in Path("docs").glob("*.md")} - {"index.md"}

    assert expected_docs.issubset({path.name for path in linked_docs})


def test_split_sweep_sample_artifact_has_split_diagnostics(tmp_path: Path) -> None:
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

    assert payload["ranked_results"]
    for result in payload["ranked_results"]:
        assert set(result["train_metrics"]) == set(result["metrics"])
        assert set(result["test_metrics"]) == set(result["metrics"])
        assert set(result["robustness"]) == {
            "train_rank",
            "test_rank",
            "rank_delta",
            "train_test_return_gap",
            "robustness_flag",
        }
        assert result["robustness"]["train_rank"] >= 1
        assert result["robustness"]["test_rank"] >= 1
        assert result["robustness"]["robustness_flag"] in {"fragile", "not_flagged"}


def test_single_backtest_sample_artifact_has_exposure_and_scenario_risk_review(
    tmp_path: Path,
) -> None:
    command = _single_backtest_command()
    output_paths = {
        "reports/sample-report.md": tmp_path / "sample-report.md",
        "reports/sample-report.json": tmp_path / "sample-report.json",
        "reports/sample-report.html": tmp_path / "sample-report.html",
        "reports/sample-manifest.md": tmp_path / "sample-manifest.md",
    }
    command = [
        *command,
        "--output",
        str(output_paths["reports/sample-report.md"]),
        "--json-output",
        str(output_paths["reports/sample-report.json"]),
        "--html-output",
        str(output_paths["reports/sample-report.html"]),
        "--manifest-output",
        str(output_paths["reports/sample-manifest.md"]),
    ]

    result = subprocess.run(
        command,
        cwd=selfcheck.REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    markdown = (tmp_path / "sample-report.md").read_text(encoding="utf-8")
    html = (tmp_path / "sample-report.html").read_text(encoding="utf-8")
    payload = json.loads((tmp_path / "sample-report.json").read_text())

    assert "## Modeled Exposure Review" in markdown
    assert "## Scenario/Risk Interpretation" in markdown
    assert "- **Modeled entries**:" in markdown
    assert "- **Modeled exits**:" in markdown
    assert "- **Buy-and-hold comparison**:" in markdown
    assert "<h2>Modeled Exposure Review</h2>" in html
    assert "<h2>Scenario/Risk Interpretation</h2>" in html
    assert "Modeled entries" in html
    assert "Modeled exits" in html
    assert "Buy-and-hold comparison" in html

    review = payload["exposure_trade_review"]
    assert set(review) == {
        "period_count",
        "periods_in_market",
        "periods_in_cash",
        "percent_periods_in_market",
        "percent_periods_in_cash",
        "average_exposure",
        "exposure_changes",
        "entries_to_market",
        "exits_to_cash",
        "total_fee_drag",
        "research_only",
        "note",
    }
    assert review["period_count"] == 7
    assert review["research_only"] is True
    assert "not investment advice" in review["note"]
    assert "trading guidance" in review["note"]
    assert "instructions to buy, sell, hold, or size a position" in review["note"]

    interpretation = payload["scenario_risk_interpretation"]
    assert set(interpretation) == {
        "research_only",
        "historical_diagnostics_only",
        "note",
        "exposure",
        "drawdown",
        "fee_drag",
        "buy_and_hold_comparison",
    }
    assert interpretation["research_only"] is True
    assert interpretation["historical_diagnostics_only"] is True
    assert "not investment advice" in interpretation["note"]
    assert "trading guidance" in interpretation["note"]
    assert "prediction" in interpretation["note"]
    assert "broker connection or execution feature" in interpretation["note"]
    assert "summary" in interpretation["exposure"]
    assert "summary" in interpretation["drawdown"]
    assert "summary" in interpretation["fee_drag"]
    assert "summary" in interpretation["buy_and_hold_comparison"]

    readme = Path("README.md").read_text(encoding="utf-8")
    gallery_notes = Path("docs/artifact-gallery.md").read_text(encoding="utf-8")
    docs_index = Path("docs/index.md").read_text(encoding="utf-8")
    static_gallery = Path("reports/index.html").read_text(encoding="utf-8")
    static_manifest = Path("docs/static-gallery-manifest.md").read_text(encoding="utf-8")
    for public_doc in (
        readme,
        gallery_notes,
        docs_index,
        static_gallery,
        static_manifest,
    ):
        assert "Scenario/Risk Interpretation" in public_doc
        assert "scenario_risk_interpretation" in public_doc


def test_selfcheck_regenerates_fee_sensitivity_artifacts() -> None:
    expected_artifacts = {
        Path("reports/fee-sensitivity.md"),
        Path("reports/fee-sensitivity.json"),
    }

    assert expected_artifacts.issubset(set(selfcheck.SAMPLE_ARTIFACTS))

    command = _fee_sensitivity_command()
    assert "scripts/fee_sensitivity.py" in command
    assert command[command.index("--markdown-output") + 1] == "reports/fee-sensitivity.md"
    assert command[command.index("--json-output") + 1] == "reports/fee-sensitivity.json"


def test_fee_sensitivity_artifact_is_reproducible(tmp_path: Path) -> None:
    command = _fee_sensitivity_command()
    output_paths = {
        "reports/fee-sensitivity.md": tmp_path / "fee-sensitivity.md",
        "reports/fee-sensitivity.json": tmp_path / "fee-sensitivity.json",
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

    markdown = (tmp_path / "fee-sensitivity.md").read_text(encoding="utf-8")
    payload = json.loads((tmp_path / "fee-sensitivity.json").read_text(encoding="utf-8"))

    assert "# Fee Sensitivity Comparison" in markdown
    assert "| fee_bps | total_return | buy_and_hold_total_return |" in markdown
    assert "## Beginner Caveats" in markdown
    assert "no modeled exposure changes" in markdown
    assert "not investment advice" in markdown

    assert payload["artifact"] == "fee_sensitivity"
    assert payload["research_only"] is True
    assert payload["input_csv"] == "examples/data/sample_tqqq_qld_like.csv"
    assert payload["symbol"] == "QQQ_LIKE"
    assert payload["strategy_config"] == {"short_window": 20, "long_window": 50}
    assert payload["fee_bps_values"] == [0.0, 5.0, 10.0, 25.0, 50.0]
    assert len(payload["rows"]) == 5
    assert payload["data_provenance"]["data_kind"] == "synthetic_static_fixture"

    for row in payload["rows"]:
        assert set(row) == {
            "fee_bps",
            "total_return",
            "buy_and_hold_total_return",
            "strategy_minus_buy_and_hold_return",
            "max_drawdown",
            "modeled_exposure_changes",
            "modeled_entries",
            "modeled_exits",
            "average_exposure",
            "periods_in_market",
            "period_count",
            "total_fee_drag",
        }
        assert row["modeled_exposure_changes"] == 0
        assert row["modeled_entries"] == 0
        assert row["modeled_exits"] == 0
        assert row["average_exposure"] == 0.0
        assert row["total_fee_drag"] == 0.0


def _single_backtest_command() -> list[str]:
    backtest_commands = [
        command
        for command in selfcheck._sample_artifact_commands()
        if "examples/configs/single-backtest-report.json" in command
    ]
    assert len(backtest_commands) == 1
    return backtest_commands[0]


def _split_sweep_command() -> list[str]:
    split_commands = [
        command
        for command in selfcheck._sample_artifact_commands()
        if "reports/sample-sweep-split.md" in command
    ]
    assert len(split_commands) == 1
    return split_commands[0]


def _fee_sensitivity_command() -> list[str]:
    fee_commands = [
        command
        for command in selfcheck._sample_artifact_commands()
        if "reports/fee-sensitivity.md" in command
    ]
    assert len(fee_commands) == 1
    return fee_commands[0]


def _pretrade_packet_command() -> list[str]:
    packet_commands = [
        command
        for command in selfcheck._sample_artifact_commands()
        if "reports/pretrade-packet.md" in command
    ]
    assert len(packet_commands) == 1
    return packet_commands[0]


def _scenario_card_command() -> list[str]:
    card_commands = [
        command
        for command in selfcheck._sample_artifact_commands()
        if "--scenario-card" in command
    ]
    assert len(card_commands) == 1
    return card_commands[0]


def _valid_pretrade_packet_payload() -> dict[str, object]:
    return {
        "packet_type": "pretrade_research_packet",
        "schema_version": "1.0",
        "research_only": True,
        "historical_diagnostics_only": True,
        "no_broker_or_live_data": True,
        "note": (
            "Research-only packet; not investment advice, not trading guidance, "
            "and not a broker connection."
        ),
        "source": {
            "input_path": "examples/data/sample_tqqq_qld_like.csv",
            "first_date": "2024-01-02",
            "last_date": "2024-01-11",
            "row_count": 8,
        },
        "strategy_config": {
            "symbol": "QQQ_LIKE",
            "short_window": 20,
            "long_window": 50,
            "fee_bps": 10.0,
        },
        "assumptions": [
            "Uses the existing single-backtest moving-average workflow.",
            "Uses only the supplied local CSV path and optional symbol filter.",
            "Uses historical close-to-close sample rows; no live data is requested.",
            "Uses configured fee_bps as a simplified historical cost assumption.",
            "Does not connect to brokers, create orders, or provide execution steps.",
        ],
        "historical_diagnostics": {
            "metrics": {
                "total_return": 0.0,
                "buy_and_hold_total_return": 0.0169,
                "strategy_minus_buy_and_hold_return": -0.0169,
                "max_drawdown": 0.0,
            },
            "exposure_trade_review": {
                "period_count": 7,
                "average_exposure": 0.0,
                "percent_periods_in_market": 0.0,
                "exposure_changes": 0,
                "entries_to_market": 0,
                "exits_to_cash": 0,
                "total_fee_drag": 0.0,
                "research_only": True,
                "note": "Historical exposure metadata only.",
            },
            "scenario_risk_interpretation": {
                "research_only": True,
                "historical_diagnostics_only": True,
                "exposure": {"summary": "Exposure summary."},
                "drawdown": {"summary": "Drawdown summary."},
                "fee_drag": {"summary": "Fee summary."},
                "buy_and_hold_comparison": {"summary": "Comparison summary."},
            },
        },
        "beginner_checklist": [
            {"item": f"Review item {index}.", "status": "review_required"}
            for index in range(1, 8)
        ],
        "risk_boundaries": {
            "non_advice": "Research-only; not investment advice.",
            "sample_backtest_limits": (
                "Backtest and sample results are limited to the supplied "
                "historical rows and simplified assumptions. They are examples "
                "for review only, not evidence of future returns."
            ),
            "leveraged_etf_like": (
                "Daily reset mechanics are path-dependent and losses can grow."
            ),
            "scope_limits": (
                "This packet has no broker workflow, live-data workflow, "
                "order routing, or recommendation engine."
            ),
        },
    }


def _write_prediction_readiness_audit_fixture(
    tmp_path: Path,
    *,
    payload_overrides: dict[str, object] | None = None,
    markdown: str | None = None,
) -> dict[str, object]:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    ledger = selfcheck.build_cross_asset_thesis_ledger(selfcheck.CSV_PATH)
    payload = selfcheck.build_prediction_readiness_audit(
        ledger,
        "reports/cross-asset-thesis-ledger.json",
    )
    if payload_overrides:
        payload.update(payload_overrides)

    (reports_dir / "prediction-readiness-audit.json").write_text(
        json.dumps(payload, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (reports_dir / "prediction-readiness-audit.md").write_text(
        markdown
        if markdown is not None
        else selfcheck.render_prediction_readiness_audit(payload),
        encoding="utf-8",
    )
    return payload


def _regime_comparison_command() -> list[str]:
    regime_commands = [
        command
        for command in selfcheck._sample_artifact_commands()
        if "--regime-comparison" in command
    ]
    assert len(regime_commands) == 1
    return regime_commands[0]


def _write_demo_contract_fixture(
    tmp_path: Path,
    gallery_html: str,
    *,
    json_text: str = "{}\n",
) -> None:
    docs_dir = tmp_path / "docs"
    reports_dir = tmp_path / "reports"
    docs_dir.mkdir()
    reports_dir.mkdir()

    (docs_dir / "split-sweep-walkthrough.md").write_text(
        "[HTML split sweep](../reports/sample-sweep-split.html)\n"
        "[Markdown split sweep](../reports/sample-sweep-split.md)\n"
        "[JSON split sweep](../reports/sample-sweep-split.json)\n",
        encoding="utf-8",
    )
    (reports_dir / "index.html").write_text(gallery_html, encoding="utf-8")
    (reports_dir / "sample-sweep-split.html").write_text("<h1>Split</h1>\n", encoding="utf-8")
    (reports_dir / "sample-sweep-split.md").write_text("# Split\n", encoding="utf-8")
    (reports_dir / "sample-sweep-split.json").write_text(json_text, encoding="utf-8")


def _write_v130_gallery_fixture(
    tmp_path: Path,
    *,
    omit_link: str | None = None,
    extra_html: str = "",
    include_required_text: bool = True,
) -> None:
    docs_dir = tmp_path / "docs"
    reports_dir = tmp_path / "reports"
    docs_dir.mkdir()
    reports_dir.mkdir()

    for doc_name in (
        "artifact-gallery.md",
        "static-gallery-manifest.md",
        "static-gallery-walkthrough.svg",
        "split-sweep-walkthrough.md",
    ):
        doc_path = docs_dir / doc_name
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(f"# {doc_name}\n", encoding="utf-8")

    report_names = {
        target
        for target in selfcheck.V130_STATIC_GALLERY_LINKS
        if not target.startswith("../docs/")
    }
    for report_name in report_names:
        (reports_dir / report_name).write_text(f"{report_name}\n", encoding="utf-8")

    links = [
        target
        for target in selfcheck.V130_STATIC_GALLERY_LINKS
        if target != omit_link
    ]
    inventory_text = (
        "Scenario/Risk Interpretation scenario_risk_interpretation\n"
        if include_required_text
        else ""
    )
    html = inventory_text + extra_html + "\n".join(
        f'<a href="{target}">{target}</a>' for target in links
    )
    (reports_dir / "index.html").write_text(html, encoding="utf-8")


def _write_v131_landing_fixture(
    tmp_path: Path,
    *,
    omit_link: str | None = None,
    extra_html: str = "",
) -> None:
    docs_dir = tmp_path / "docs"
    reports_dir = tmp_path / "reports"
    docs_dir.mkdir()
    reports_dir.mkdir()

    (tmp_path / "README.md").write_text("# README\n", encoding="utf-8")
    (reports_dir / "index.html").write_text("<h1>Gallery</h1>\n", encoding="utf-8")
    (reports_dir / "reviewer-evidence-bundle.md").write_text(
        "# Reviewer Evidence Bundle\n",
        encoding="utf-8",
    )
    (reports_dir / "beginner-prediction-checklist.md").write_text(
        "# Beginner Backtest Reading Checklist\n",
        encoding="utf-8",
    )
    for doc_name in (
        "cold-user-evidence-card.md",
        "index.md",
        "static-gallery-manifest.md",
        "static-gallery-walkthrough.svg",
        "thesis-ledger-60-second-walkthrough.md",
        "artifact-gallery.md",
        "split-sweep-walkthrough.md",
        "risk-boundaries.md",
        "data-provenance.md",
        "methodology-audit-review-schema.md",
        "architecture.md",
        "adr/0001-static-research-artifacts.md",
        "three-minute-review.md",
        "local-audit-commands.md",
        "public-share-copy.md",
        "reviewer-decision-tree.md",
        "quick-tour-preview.md",
        "quick-tour-preview.svg",
        "release-notes-v1.23.0.md",
        "release-notes-v1.22.1.md",
        "release-notes-v1.22.0.md",
        "release-v1.22.0.md",
        "release-notes-v1.21.0.md",
        "release-v1.21.0.md",
        "release-notes-v1.20.4.md",
        "release-v1.20.4.md",
        "release-notes-v1.20.3.md",
        "release-v1.20.3.md",
        "release-notes-v1.20.2.md",
        "release-v1.20.2.md",
        "release-notes-v1.20.1.md",
        "release-v1.20.1.md",
        "release-notes-v1.20.0.md",
        "release-v1.20.0.md",
        "release-notes-v1.19.0.md",
        "release-v1.19.0.md",
        "release-notes-v1.18.0.md",
        "release-v1.18.0.md",
        "release-notes-v1.17.0.md",
        "release-v1.17.0.md",
        "release-notes-v1.16.0.md",
        "release-v1.16.0.md",
        "release-notes-v1.15.0.md",
        "release-v1.15.0.md",
        "release-notes-v1.14.0.md",
        "release-v1.14.0.md",
        "release-notes-v1.13.0.md",
        "release-v1.13.0.md",
        "release-notes-v1.12.0.md",
        "release-v1.12.0.md",
        "release-notes-v1.11.0.md",
        "release-v1.11.0.md",
        "release-notes-v1.10.0.md",
        "release-v1.10.0.md",
        "release-notes-v1.9.1.md",
        "release-v1.9.1.md",
        "release-notes-v1.9.0.md",
        "release-v1.9.0.md",
        "release-notes-v1.3.1.md",
        "release-v1.3.1.md",
    ):
        doc_path = docs_dir / doc_name
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(f"# {doc_name}\n", encoding="utf-8")

    links = [
        target
        for target in selfcheck.V131_ROOT_LANDING_LINKS
        if target != omit_link
    ]
    html = extra_html + "\n".join(
        f'<a href="{target}">{target}</a>' for target in links
    )
    (tmp_path / "index.html").write_text(html, encoding="utf-8")
