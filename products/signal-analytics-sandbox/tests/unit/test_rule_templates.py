from __future__ import annotations

import re

from signal_sandbox.extraction.rule_templates import TEMPLATES, template_sha256

EXPECTED_TEMPLATE_HASHES = {
    "binance_spot_v1": (
        "8de9f14c2eb6b9c0d73e64c3cbb001e9d30383ae33127c70110ff07aad896130"
    )
}


def test_templates_are_versioned() -> None:
    assert set(TEMPLATES) == set(EXPECTED_TEMPLATE_HASHES)
    for template_id, template in TEMPLATES.items():
        assert re.match(r"^[a-z0-9_]+_v[0-9]+$", template_id)
        assert template.template_id == template_id
        assert template.pattern_sha256 == template_sha256(template.pattern)
        assert template.pattern_sha256 == EXPECTED_TEMPLATE_HASHES[template_id]
