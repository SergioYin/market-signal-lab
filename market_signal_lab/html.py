"""Static HTML report artifact rendering."""

from __future__ import annotations

from html import escape
import re


RESEARCH_ONLY_WARNING = (
    "Research-only: this artifact is for historical signal research, not "
    "investment advice, not a recommendation, and not evidence of future "
    "performance."
)


def render_html_report(
    markdown_report: str,
    title: str = "Market Signal Lab Report",
) -> str:
    """Render a Markdown report string as a minimal static HTML artifact."""

    escaped_title = escape(title)
    escaped_warning = escape(RESEARCH_ONLY_WARNING)
    report_html = _render_supported_markdown(markdown_report)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>{escaped_title}</title>\n"
        "  <style>\n"
        "    body { font-family: system-ui, sans-serif; line-height: 1.5; margin: 2rem; }\n"
        "    table { border-collapse: collapse; min-width: max-content; }\n"
        "    th, td { border: 1px solid #d0d7de; padding: 0.35rem 0.5rem; text-align: right; }\n"
        "    th { background: #f6f8fa; }\n"
        "    th:first-child, td:first-child { text-align: left; }\n"
        "    blockquote { border-left: 4px solid #d0d7de; color: #57606a; margin-left: 0; padding-left: 1rem; }\n"
        "    .table-wrap { overflow-x: auto; }\n"
        "  </style>\n"
        "</head>\n"
        "<body>\n"
        f"  <h1>{escaped_title}</h1>\n"
        f"  <p><strong>{escaped_warning}</strong></p>\n"
        f"{report_html}"
        "</body>\n"
        "</html>\n"
    )


def _render_supported_markdown(markdown_report: str) -> str:
    """Render the report Markdown subset emitted by this package."""

    lines = markdown_report.splitlines()
    html_lines: list[str] = []
    index = 0
    in_list = False

    while index < len(lines):
        line = lines[index]

        if not line:
            if in_list:
                html_lines.append("  </ul>")
                in_list = False
            index += 1
            continue

        if _is_markdown_table_start(lines, index):
            if in_list:
                html_lines.append("  </ul>")
                in_list = False
            table_lines: list[str] = []
            while index < len(lines) and lines[index].startswith("|"):
                table_lines.append(lines[index])
                index += 1
            html_lines.extend(_render_markdown_table(table_lines))
            continue

        if line.startswith("- "):
            if not in_list:
                html_lines.append("  <ul>")
                in_list = True
            html_lines.append(f"    <li>{_render_inline_markdown(line[2:])}</li>")
            index += 1
            continue

        if in_list:
            html_lines.append("  </ul>")
            in_list = False

        if line.startswith("## "):
            html_lines.append(f"  <h2>{_render_inline_markdown(line[3:])}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"  <h1>{_render_inline_markdown(line[2:])}</h1>")
        elif line.startswith("> "):
            html_lines.append(f"  <blockquote>{_render_inline_markdown(line[2:])}</blockquote>")
        else:
            html_lines.append(f"  <p>{_render_inline_markdown(line)}</p>")
        index += 1

    if in_list:
        html_lines.append("  </ul>")

    return "\n".join(html_lines) + "\n"


def _is_markdown_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    return lines[index].startswith("|") and _is_markdown_table_separator(lines[index + 1])


def _is_markdown_table_separator(line: str) -> bool:
    cells = _split_markdown_table_row(line)
    return bool(cells) and all(set(cell.strip()) <= {"-"} and cell.strip() for cell in cells)


def _render_markdown_table(table_lines: list[str]) -> list[str]:
    headers = _split_markdown_table_row(table_lines[0])
    body_rows = [_split_markdown_table_row(line) for line in table_lines[2:]]
    html_lines = [
        '  <div class="table-wrap">',
        "    <table>",
        "      <thead>",
        "        <tr>",
    ]
    html_lines.extend(f"          <th>{_render_inline_markdown(header)}</th>" for header in headers)
    html_lines.extend(
        [
            "        </tr>",
            "      </thead>",
            "      <tbody>",
        ]
    )
    for row in body_rows:
        html_lines.append("        <tr>")
        html_lines.extend(f"          <td>{_render_inline_markdown(cell)}</td>" for cell in row)
        html_lines.append("        </tr>")
    html_lines.extend(
        [
            "      </tbody>",
            "    </table>",
            "  </div>",
        ]
    )
    return html_lines


def _split_markdown_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _render_inline_markdown(text: str) -> str:
    escaped_text = escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped_text)
