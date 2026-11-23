"""New-game starting-region selection rules.

This module validates the player's opening-region choice. It deliberately does
not invent engine map constants: those are supplied by the map-import adapter
once the Sinnoh map set and start maps have been integrated.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

SUPPORTED_REGIONS = ("hoenn", "sinnoh")


@dataclass(frozen=True)
class RegionStart:
    """Stable region-level start descriptor; map IDs are resolved by the engine."""

    region: str
    start_key: str


REGION_STARTS = {
    "hoenn": RegionStart(region="hoenn", start_key="hoenn_new_game_start"),
    "sinnoh": RegionStart(region="sinnoh", start_key="sinnoh_new_game_start"),
}


def available_starting_regions(config: Mapping) -> tuple[str, ...]:
    """Return configured region choices, rejecting unknown or duplicate IDs."""
    world = config.get("world", {})
    regions = world.get("regions", list(SUPPORTED_REGIONS))
    if not isinstance(regions, (list, tuple)) or not regions:
        raise ValueError("world.regions must be a non-empty list")
    normalized = tuple(str(region).strip().lower() for region in regions)
    if len(set(normalized)) != len(normalized):
        raise ValueError("world.regions contains duplicate region IDs")
    unknown = set(normalized) - set(SUPPORTED_REGIONS)
    if unknown:
        raise ValueError(f"unsupported starting region(s): {', '.join(sorted(unknown))}")
    return normalized


def resolve_starting_region(config: Mapping, choice: str | None = None) -> RegionStart:
    """Resolve a new game's selected opening region.

    If no choice is supplied, use the configured default. Both regions may
    remain part of the same adventure; this selects only the opening location.
    """
    selection = config.get("new_game_region_selection", {})
    if selection.get("enabled", True) is not True:
        raise ValueError("new-game region selection is disabled")
    available = available_starting_regions(config)
    selected = choice if choice is not None else selection.get("default", "hoenn")
    selected = str(selected).strip().lower()
    if selected not in available:
        raise ValueError(
            f"invalid starting region {selected!r}; choose one of: {', '.join(available)}"
        )
    return REGION_STARTS[selected]
