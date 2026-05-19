"""Experiment manifest helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def build_manifest(
    *,
    input_path: str | Path,
    symbol: str | None,
    mode: str,
    fee_bps: float,
    strategy_config: Mapping[str, Any] | None = None,
    sweep_config: Mapping[str, Any] | None = None,
    output_paths: Mapping[str, str | Path | None] | None = None,
    data_provenance: Mapping[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a deterministic research-only manifest dictionary for one run."""

    manifest: dict[str, Any] = {}
    if generated_at is not None:
        manifest["generated_at"] = generated_at

    manifest.update(
        {
            "input_path": str(input_path),
            "symbol": symbol,
            "mode": mode,
        }
    )

    if strategy_config is not None:
        manifest["strategy_config"] = dict(strategy_config)
    if sweep_config is not None:
        manifest["sweep_config"] = dict(sweep_config)

    manifest["fee_bps"] = fee_bps
    if data_provenance is not None:
        manifest["data_provenance"] = dict(data_provenance)
    manifest["output_paths"] = _normalize_output_paths(output_paths or {})
    manifest["research_only"] = True
    return manifest


def render_manifest_markdown(manifest: Mapping[str, Any]) -> str:
    """Render an experiment manifest dictionary as Markdown."""

    lines = ["# Experiment Manifest", ""]
    for key, value in manifest.items():
        if isinstance(value, Mapping):
            if lines[-1] != "":
                lines.append("")
            lines.extend([f"## {key}", "", *_render_mapping(value), ""])
        else:
            lines.append(f"- **{key}**: {_format_value(value)}")

    return "\n".join(lines).rstrip() + "\n"


def _normalize_output_paths(
    output_paths: Mapping[str, str | Path | None],
) -> dict[str, str]:
    return {
        key: str(value)
        for key, value in sorted(output_paths.items())
        if value is not None
    }


def _render_mapping(values: Mapping[str, Any]) -> list[str]:
    if not values:
        return ["- None"]

    return [f"- **{key}**: {_format_value(value)}" for key, value in values.items()]


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "None"
    if isinstance(value, float):
        return f"{value:.4f}"
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return ", ".join(_format_value(item) for item in value)
    return str(value)
