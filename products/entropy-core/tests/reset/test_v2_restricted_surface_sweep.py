"""Regression sweep for Core V2 restricted-surface boundaries."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

V2_BOUNDARY_DOCS = (
    ROOT / "docs" / "CODEX_PROMPT.md",
    ROOT / "PHASE_HANDOFF.md",
    ROOT / "README.md",
    ROOT / "docs" / "tasks.md",
    ROOT / "docs" / "CORE_V2_ROADMAP.md",
    ROOT / "docs" / "core" / "V2_KERNEL_FOUNDATION_INVENTORY.md",
    ROOT / "docs" / "audit" / "SCHEMA_EVOLUTION_FOUNDATIONS_REVIEW.md",
    ROOT / "docs" / "audit" / "EVIDENCE_QUERY_HARDENING_REVIEW.md",
    ROOT / "docs" / "audit" / "PRODUCT_BRIDGE_ADOPTION_READINESS_REVIEW.md",
)

APPROVAL_PATTERNS = (
    r"public sdk\s*:\s*(approved|enabled|open)",
    r"hosted service\s*:\s*(approved|enabled|open)",
    r"runtime rag\s*:\s*(approved|enabled|open)",
    r"product runtime ownership\s*:\s*(approved|enabled|open)",
    r"product report authorship\s*:\s*(approved|enabled|open)",
    r"external delivery approval\s*:\s*(approved|enabled|open)",
    r"live execution\s*:\s*(approved|enabled|open)",
    r"holdout access\s*:\s*(approved|enabled|open)",
    r"broker/exchange execution\s*:\s*(approved|enabled|open)",
    r"production credentials\s*:\s*(approved|enabled|open)",
    r"external compliance\s*:\s*(approved|enabled|open)",
    r"capital scope\s*:\s*(approved|enabled|open)",
)


def v2_boundary_text() -> str:
    return " ".join(
        " ".join(path.read_text(encoding="utf-8").lower().split()) for path in V2_BOUNDARY_DOCS
    )


def test_v2_public_and_product_surfaces_stay_blocked() -> None:
    text = v2_boundary_text()

    for blocked_surface in (
        "public sdk",
        "hosted service",
        "runtime rag",
        "product runtime ownership",
        "product report authorship",
        "product workspace edits",
        "external delivery approval",
    ):
        assert blocked_surface in text
    for approval_pattern in APPROVAL_PATTERNS[:6]:
        assert re.search(approval_pattern, text) is None


def test_v2_live_holdout_compliance_and_capital_surfaces_stay_blocked() -> None:
    text = v2_boundary_text()

    for blocked_surface in (
        "live execution",
        "holdout access",
        "broker/exchange execution",
        "production credentials",
        "external compliance certification",
        "capital scope",
    ):
        assert blocked_surface in text
    for approval_pattern in APPROVAL_PATTERNS[6:]:
        assert re.search(approval_pattern, text) is None


def test_v2_review_docs_do_not_claim_unsupported_readiness() -> None:
    text = v2_boundary_text()

    for unsupported_claim in (
        "does not claim product readiness",
        "hosted service readiness",
        "live execution readiness",
        "holdout readiness",
        "external compliance readiness",
        "capital readiness",
        "oos/performance confirmation",
    ):
        assert unsupported_claim in text
    for approval_pattern in (
        r"production readiness\s*:\s*(approved|true|yes)",
        r"capital-ready\s*:\s*(approved|true|yes)",
        r"investment advice\s*:\s*(approved|true|yes)",
        r"oos/performance\s*:\s*(approved|confirmed|true|yes)",
    ):
        assert re.search(approval_pattern, text) is None
