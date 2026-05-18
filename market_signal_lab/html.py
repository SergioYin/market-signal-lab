"""Static HTML report artifact rendering."""

from __future__ import annotations

from html import escape


RESEARCH_ONLY_WARNING = (
    "Research-only: this artifact is for historical signal research, not "
    "investment advice, not a recommendation, and not evidence of future "
    "performance."
)


def render_html_report(
    markdown_report: str,
    title: str = "Market Signal Lab Report",
) -> str:
    """Wrap a Markdown report string in a minimal static HTML page."""

    escaped_title = escape(title)
    escaped_warning = escape(RESEARCH_ONLY_WARNING)
    escaped_report = escape(markdown_report)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>{escaped_title}</title>\n"
        "</head>\n"
        "<body>\n"
        f"  <h1>{escaped_title}</h1>\n"
        f"  <p><strong>{escaped_warning}</strong></p>\n"
        f"  <pre>{escaped_report}</pre>\n"
        "</body>\n"
        "</html>\n"
    )
