from __future__ import annotations

from pathlib import Path

from signal_sandbox.reports import is_customer_safe_wording

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_demo_script_has_15_minute_structure_and_limitations() -> None:
    script = (PROJECT_ROOT / "docs/pilot/DEMO_SCRIPT.md").read_text(encoding="utf-8")

    for required in (
        "## 0:00-1:30 - Opening",
        "## 1:30-3:30 - Buyer Pain",
        "## 3:30-6:00 - Method Walkthrough",
        "## 6:00-9:00 - Three-Channel Internal Result",
        "## 9:00-11:00 - Limitations",
        "## 11:00-13:00 - Pilot Shape",
        "## 13:00-15:00 - Close",
        "Gate: `approve_internal_only`",
    ):
        assert required in script


def test_demo_script_explains_value_without_forbidden_customer_wording() -> None:
    script = (PROJECT_ROOT / "docs/pilot/DEMO_SCRIPT.md").read_text(encoding="utf-8")

    assert "what was said, what could be normalized" in script
    assert "This is not externally deliverable yet." in script
    assert "Do not promise future profit" in script
    assert is_customer_safe_wording(script)
