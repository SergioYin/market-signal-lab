from __future__ import annotations

from market_signal_lab.html import RESEARCH_ONLY_WARNING, render_html_report


def test_render_html_report_escapes_title_and_markdown_content() -> None:
    html = render_html_report(
        "# <Report>\n\n<script>alert('x')</script> & data\n",
        title="Lab <Report>",
    )

    assert "<title>Lab &lt;Report&gt;</title>" in html
    assert "<h1>Lab &lt;Report&gt;</h1>" in html
    assert "<h1>&lt;Report&gt;</h1>" in html
    assert "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt; &amp; data" in html
    assert "<script>" not in html
    assert RESEARCH_ONLY_WARNING in html


def test_render_html_report_converts_markdown_tables() -> None:
    html = render_html_report(
        "\n".join(
            [
                "# Sweep",
                "",
                "| rank | robustness_flag | train_test_return_gap |",
                "| --- | --- | --- |",
                "| 1 | fragile | 3.44% |",
                "| 2 | not_flagged | 1.64% |",
                "",
            ]
        )
    )

    assert '<div class="table-wrap">' in html
    assert "<th>robustness_flag</th>" in html
    assert "<td>not_flagged</td>" in html
    assert "| rank | robustness_flag | train_test_return_gap |" not in html


def test_render_html_report_can_include_escaped_local_artifact_links() -> None:
    html = render_html_report(
        "# Regime\n\n## Caveats\n\n- Local only.\n",
        title="Regime <Comparison>",
        artifact_links=(
            ("Markdown <report>", "regime-comparison.md"),
            ("JSON data", "nested/regime-comparison.json?x=<bad>"),
        ),
    )

    assert "<title>Regime &lt;Comparison&gt;</title>" in html
    assert '<nav aria-label="Related artifacts">' in html
    assert '<a href="regime-comparison.md">Markdown &lt;report&gt;</a>' in html
    assert 'href="nested/regime-comparison.json?x=&lt;bad&gt;"' in html
    assert "<script" not in html.lower()
