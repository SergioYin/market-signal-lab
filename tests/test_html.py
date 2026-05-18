from __future__ import annotations

from market_signal_lab.html import RESEARCH_ONLY_WARNING, render_html_report


def test_render_html_report_escapes_title_and_markdown_content() -> None:
    html = render_html_report(
        "# <Report>\n\n<script>alert('x')</script> & data\n",
        title="Lab <Report>",
    )

    assert "<title>Lab &lt;Report&gt;</title>" in html
    assert "<h1>Lab &lt;Report&gt;</h1>" in html
    assert "# &lt;Report&gt;" in html
    assert "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt; &amp; data" in html
    assert "<script>" not in html
    assert RESEARCH_ONLY_WARNING in html
