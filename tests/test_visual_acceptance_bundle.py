from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from market_signal_lab.visual_acceptance_bundle import (
    ACCEPTANCE_SURFACES,
    BOUNDARY_FLAGS,
    VISUAL_ACCEPTANCE_ARTIFACT_PATHS,
    VISUAL_ACCEPTANCE_BUNDLE_COMMAND,
    build_visual_acceptance_bundle,
    render_visual_acceptance_bundle,
)


VISUAL_ACCEPTANCE_BUNDLE_TOP_LEVEL_KEYS = (
    "artifact_type",
    "schema_version",
    *BOUNDARY_FLAGS,
    "purpose",
    "default_outputs",
    "verification_command",
    "acceptance_surfaces",
    "acceptance_checks",
    "reviewer_rerun_commands",
    "artifact_integrity_summary",
    "not_claimed",
)

ACCEPTANCE_SURFACE_KEYS = ("label", "path", "acceptance_role")
ACCEPTANCE_CHECK_KEYS = ("check", "label", "status", "review_note")


class VisualAcceptanceBundleTests(unittest.TestCase):
    def test_hashes_bounded_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            svg_path = tmp_path / "docs" / "static-gallery-walkthrough.svg"
            svg_path.parent.mkdir()
            svg_path.write_text("<svg></svg>\n", encoding="utf-8")
            scorecard_path = (
                tmp_path / "reports" / "reviewer-acceptance-scorecard.md"
            )
            scorecard_path.parent.mkdir()
            scorecard_path.write_text(
                "# Reviewer Acceptance Scorecard\n",
                encoding="utf-8",
            )

            payload = build_visual_acceptance_bundle(tmp_path)

        for key in BOUNDARY_FLAGS:
            self.assertIs(payload[key], True)
        self.assertEqual(payload["artifact_type"], "visual_acceptance_bundle")
        self.assertEqual(
            payload["verification_command"],
            VISUAL_ACCEPTANCE_BUNDLE_COMMAND,
        )
        self.assertEqual(
            payload["default_outputs"],
            {
                "markdown": "reports/visual-acceptance-bundle.md",
                "json": "reports/visual-acceptance-bundle.json",
            },
        )
        integrity = payload["artifact_integrity_summary"]
        self.assertEqual(
            integrity["artifact_count"],
            len(VISUAL_ACCEPTANCE_ARTIFACT_PATHS),
        )
        self.assertEqual(integrity["present_count"], 2)
        self.assertEqual(
            integrity["missing_count"],
            len(VISUAL_ACCEPTANCE_ARTIFACT_PATHS) - 2,
        )
        self.assertEqual(
            {
                artifact["path"]: artifact["sha256"]
                for artifact in integrity["artifacts"]
                if artifact["status"] == "present"
            },
            {
                "docs/static-gallery-walkthrough.svg": hashlib.sha256(
                    b"<svg></svg>\n"
                ).hexdigest(),
                "reports/reviewer-acceptance-scorecard.md": hashlib.sha256(
                    b"# Reviewer Acceptance Scorecard\n"
                ).hexdigest(),
            },
        )

    def test_preserves_schema_order(self) -> None:
        payload = build_visual_acceptance_bundle()

        self.assertEqual(tuple(payload), VISUAL_ACCEPTANCE_BUNDLE_TOP_LEVEL_KEYS)
        self.assertEqual(
            [
                artifact["path"]
                for artifact in payload["artifact_integrity_summary"]["artifacts"]
            ],
            list(VISUAL_ACCEPTANCE_ARTIFACT_PATHS),
        )
        self.assertEqual(
            [surface["path"] for surface in payload["acceptance_surfaces"]],
            [surface["path"] for surface in ACCEPTANCE_SURFACES],
        )
        self.assertTrue(
            all(
                tuple(surface) == ACCEPTANCE_SURFACE_KEYS
                for surface in payload["acceptance_surfaces"]
            )
        )
        self.assertTrue(
            all(
                tuple(check) == ACCEPTANCE_CHECK_KEYS
                for check in payload["acceptance_checks"]
            )
        )

    def test_builds_fresh_nested_objects(self) -> None:
        payload = build_visual_acceptance_bundle()
        payload["acceptance_surfaces"][0]["unexpected"] = "extra"
        payload["acceptance_checks"][0]["unexpected"] = "extra"
        payload["reviewer_rerun_commands"].append("extra")
        payload["artifact_integrity_summary"]["artifacts"][0]["path"] = "extra"
        payload["not_claimed"].append("extra")

        fresh_payload = build_visual_acceptance_bundle()

        self.assertEqual(
            tuple(fresh_payload["acceptance_surfaces"][0]),
            ACCEPTANCE_SURFACE_KEYS,
        )
        self.assertEqual(
            tuple(fresh_payload["acceptance_checks"][0]),
            ACCEPTANCE_CHECK_KEYS,
        )
        self.assertNotIn("extra", fresh_payload["reviewer_rerun_commands"])
        self.assertEqual(
            fresh_payload["artifact_integrity_summary"]["artifacts"][0]["path"],
            VISUAL_ACCEPTANCE_ARTIFACT_PATHS[0],
        )
        self.assertNotIn("extra", fresh_payload["not_claimed"])

    def test_markdown_surfaces_boundaries(self) -> None:
        payload = build_visual_acceptance_bundle()

        markdown = render_visual_acceptance_bundle(payload)

        self.assertIn("# Visual Acceptance Bundle", markdown)
        self.assertIn("docs/static-gallery-walkthrough.svg", markdown)
        self.assertIn("reports/visual-walkthrough-evidence-receipt.md", markdown)
        self.assertIn("reports/acceptance-receipt-index.md", markdown)
        self.assertIn("reports/reviewer-acceptance-scorecard.md", markdown)
        self.assertIn("reports/cold-user-review-route.md", markdown)
        self.assertIn("## Artifact Integrity Summary", markdown)
        self.assertIn("No live data, broker, account", markdown)
        self.assertIn("not_investment_advice", markdown)
