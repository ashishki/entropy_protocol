from __future__ import annotations

from pathlib import Path

POLICY = Path("docs/PUBLIC_SAMPLE_SOURCE_POLICY_RU.md")


def _policy_text() -> str:
    return POLICY.read_text(encoding="utf-8").casefold()


def _normalized_policy_text() -> str:
    return " ".join(_policy_text().split())


def test_public_sample_policy_defines_source_license_and_privacy_rules() -> None:
    text = _policy_text()

    required_phrases = (
        "acceptable source types",
        "public regulatory datasets",
        "required source metadata",
        "source_license_or_terms",
        "source_accessed_date",
        "license and terms check",
        "source terms must be checked",
        "privacy and secret rejection criteria",
        "reporting owner names",
        "signatures",
        "remarks",
        "footnotes",
        "api keys",
        "bearer tokens",
    )
    for phrase in required_phrases:
        assert phrase in text

    forbidden_source_phrases = (
        "real customer exports",
        "telegram messages",
        "broker statements",
        "payment records",
    )
    for phrase in forbidden_source_phrases:
        assert phrase in text


def test_public_sample_policy_separates_demo_from_market_validation() -> None:
    text = _policy_text()

    required_boundaries = (
        "internal validation",
        "demo artifact",
        "must not say or imply",
        "qualified prospect call",
        "paid pilot report",
        "repeat commitment",
        "referral",
        "pmf evidence",
        "market pull",
    )
    for phrase in required_boundaries:
        assert phrase in text

    assert "public sample artifacts не являются qualified prospect calls" in text


def test_public_sample_policy_defines_outreach_readiness_gate() -> None:
    text = _normalized_policy_text()

    gate_phrases = (
        "outreach readiness gate",
        "reproducible reports",
        "explainable violations",
        "at least three risk scenarios",
        "two-minute readable demo",
        "3 paid audit reports",
        "10 qualified prospects",
        "within 14 days",
        "2 repeat audit commitments",
        "within 30 days",
    )
    for phrase in gate_phrases:
        assert phrase in text


def test_public_sample_policy_records_sec_form_4_candidate_boundary() -> None:
    text = _policy_text()

    required_source_details = (
        "sec edgar insider transactions data sets",
        "form 4",
        "non-derivative transactions",
        "trans_date",
        "issuertradingsymbol",
        "trans_acquired_disp_cd",
        "trans_shares",
        "trans_pricepershare",
        "market trade prints",
        "not trader account history",
    )
    for phrase in required_source_details:
        assert phrase in text


def test_public_sample_policy_preserves_starter_profile_and_telegram_boundaries() -> (
    None
):
    text = _normalized_policy_text()

    required_boundaries = (
        "soft",
        "medium",
        "hard",
        "not investment advice",
        "customizable audit presets",
        "strategy recommendations",
        "optimal risk settings",
        "trader custom rules",
        "prop/funded account rules",
        "adr-001",
        "operator-approved report delivery",
        "must not add broker apis",
        "signal parsing",
        "order blocking",
        "auto-advice",
        "live trading behavior",
    )
    for phrase in required_boundaries:
        assert phrase in text
