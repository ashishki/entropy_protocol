from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

STARTER_POLICY_DIR = Path("templates/policies")
STARTER_PROFILES = ("soft", "medium", "hard")
CUSTOM_PROFILE = "custom"


class PolicyProfileSelectionError(ValueError):
    pass


@dataclass(frozen=True)
class PolicyProfileSelection:
    selected_profile: str
    policy_source: str
    policy_path: Path

    def to_metadata(self) -> dict[str, str]:
        return {
            key: _metadata_path(value) if key == "policy_path" else str(value)
            for key, value in asdict(self).items()
        }


def resolve_policy_profile(
    selected_profile: str,
    *,
    custom_policy_path: str | Path | None = None,
) -> PolicyProfileSelection:
    profile = selected_profile.strip().casefold()
    if profile in STARTER_PROFILES:
        return PolicyProfileSelection(
            selected_profile=profile,
            policy_source="starter_template",
            policy_path=STARTER_POLICY_DIR / f"starter_policy_{profile}.yaml",
        )
    if profile == CUSTOM_PROFILE:
        if custom_policy_path is None:
            raise PolicyProfileSelectionError(
                "custom profile requires a provided policy file or written risk rules"
            )
        return PolicyProfileSelection(
            selected_profile=CUSTOM_PROFILE,
            policy_source="custom_rules",
            policy_path=Path(custom_policy_path),
        )
    allowed = ", ".join((*STARTER_PROFILES, CUSTOM_PROFILE))
    raise PolicyProfileSelectionError(f"unsupported policy profile: {allowed}")


def format_policy_profile_selector_copy() -> str:
    return "\n".join(
        (
            "Policy profiles: soft, medium, hard, custom.",
            "Soft, medium, and hard are customizable audit presets.",
            "They are not trading advice and not optimal risk settings.",
            "Trader custom rules and prop/funded account rules have priority.",
            "Choose custom when the trader already has written risk rules.",
        )
    )


def _metadata_path(path: str | Path) -> str:
    value = Path(path)
    if value.is_absolute():
        return value.name
    return str(value)
