from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts import selfcheck


def test_selfcheck_regenerates_static_gallery_contract() -> None:
    assert Path("reports/index.html") in selfcheck.SAMPLE_ARTIFACTS
    assert Path("reports/index.html") in selfcheck.HTML_LINK_SOURCES

    gallery = selfcheck.GALLERY_HTML
    assert "<script" not in gallery.lower()
    assert "research-only" in gallery
    assert "not investment advice" in gallery

    expected_links = {
        "../docs/split-sweep-walkthrough.md",
        "sample-report.html",
        "sample-sweep.html",
        "sample-sweep-split.html",
    }
    for link in expected_links:
        assert f'href="{link}"' in gallery


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


def test_docs_link_sources_include_canonical_docs_map() -> None:
    assert Path("docs/index.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/split-sweep-walkthrough.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v0.8.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v0.8.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v0.9.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v0.9.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-notes-v1.0.0.md") in selfcheck.DOC_LINK_SOURCES
    assert Path("docs/release-v1.0.0.md") in selfcheck.DOC_LINK_SOURCES


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
        "provenance metadata file is missing"
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


def _split_sweep_command() -> list[str]:
    split_commands = [
        command
        for command in selfcheck._sample_artifact_commands()
        if "reports/sample-sweep-split.md" in command
    ]
    assert len(split_commands) == 1
    return split_commands[0]


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
