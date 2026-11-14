"""Validated game rules layered on the deterministic randomizer primitives."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence, TypeVar

from tools.randomizer_core import choose_distinct, rng_for

T = TypeVar("T")


def validate_settings(settings: Mapping[str, Any]) -> None:
    """Raise ValueError when required project settings are missing or inconsistent."""
    errors: list[str] = []
    if settings.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    world = settings.get("world")
    if not isinstance(world, Mapping):
        errors.append("world must be an object")
    else:
        regions = world.get("regions")
        if world.get("mode") != "both_open":
            errors.append("world.mode must be 'both_open'")
        if not isinstance(regions, list) or not {"hoenn", "sinnoh"}.issubset(regions):
            errors.append("world.regions must include hoenn and sinnoh")
        if world.get("travel_unlocked_at_start") is not True:
            errors.append("both-open world travel must be unlocked at start")

    gyms = settings.get("gym_progression")
    if not isinstance(gyms, Mapping):
        errors.append("gym_progression must be an object")
    else:
        thresholds = gyms.get("tier_thresholds")
        if (
            not isinstance(thresholds, list)
            or not thresholds
            or any(type(value) is not int or value < 0 for value in thresholds)
            or thresholds[0] != 0
            or any(a >= b for a, b in zip(thresholds, thresholds[1:]))
        ):
            errors.append("gym_progression.tier_thresholds must be strictly increasing non-negative integers starting at 0")
        if gyms.get("mode") != "scaled":
            errors.append("gym_progression.mode must be 'scaled'")

    starters = settings.get("starters")
    if not isinstance(starters, Mapping):
        errors.append("starters must be an object")
    else:
        if starters.get("mode") != "random_three_per_region":
            errors.append("starters.mode must be 'random_three_per_region'")
        if starters.get("regions") != ["hoenn", "sinnoh"]:
            errors.append("starters.regions must list hoenn and sinnoh in order")
        if starters.get("choices_per_region") != 3:
            errors.append("starters.choices_per_region must be 3")
        if starters.get("player_picks_per_region") != 1:
            errors.append("starters.player_picks_per_region must be 1")
        if starters.get("unique_across_both_regions") is not True:
            errors.append("starters.unique_across_both_regions must be true")

    encounters = settings.get("encounters")
    if not isinstance(encounters, Mapping):
        errors.append("encounters must be an object")
    elif encounters.get("legendary_duplicate_policy") not in {"allow", "unique"}:
        errors.append("encounters.legendary_duplicate_policy must be 'allow' or 'unique'")

    mega = settings.get("mega_evolution")
    if not isinstance(mega, Mapping) or type(mega.get("enabled")) is not bool:
        errors.append("mega_evolution.enabled must be a boolean")

    if errors:
        raise ValueError("Invalid randomizer settings:\n- " + "\n- ".join(errors))


def load_settings(path: str | Path) -> dict[str, Any]:
    """Load and validate a JSON settings file."""
    with Path(path).open("r", encoding="utf-8") as handle:
        settings = json.load(handle)
    if not isinstance(settings, dict):
        raise ValueError("settings root must be a JSON object")
    validate_settings(settings)
    return settings


def progression_score(total_badges: int, completed_milestones: int) -> int:
    """Return a monotonic global score from durable progress flags."""
    if type(total_badges) is not int or total_badges < 0:
        raise ValueError("total_badges must be a non-negative integer")
    if type(completed_milestones) is not int or completed_milestones < 0:
        raise ValueError("completed_milestones must be a non-negative integer")
    return total_badges + completed_milestones


def gym_tier_for_progress(score: int, thresholds: Sequence[int]) -> int:
    """Return the zero-based Gym tier selected by a global progression score."""
    if type(score) is not int or score < 0:
        raise ValueError("score must be a non-negative integer")
    if (
        not thresholds
        or any(type(value) is not int or value < 0 for value in thresholds)
        or thresholds[0] != 0
        or any(a >= b for a, b in zip(thresholds, thresholds[1:]))
    ):
        raise ValueError("thresholds must be strictly increasing non-negative integers starting at 0")

    tier = 0
    for index, threshold in enumerate(thresholds):
        if score < threshold:
            break
        tier = index
    return tier


def choose_starters(
    eligible_species: Sequence[T],
    *,
    seed: str,
    banned_species: Iterable[T] = (),
) -> list[T]:
    """Choose three distinct starters from the eligible, non-banned pool."""
    banned = set(banned_species)
    pool = [species for species in eligible_species if species not in banned]
    return choose_distinct(pool, 3, seed=seed, stream="starters")


def choose_regional_starters(
    eligible_species: Sequence[T],
    *,
    seed: str,
    banned_species: Iterable[T] = (),
) -> dict[str, list[T]]:
    """Choose three unique options per region; all six are distinct across regions."""
    banned = set(banned_species)
    pool = list(dict.fromkeys(species for species in eligible_species if species not in banned))
    hoenn = choose_distinct(pool, 3, seed=seed, stream="starters:hoenn")
    selected_hoenn = set(hoenn)
    sinnoh_pool = [species for species in pool if species not in selected_hoenn]
    sinnoh = choose_distinct(sinnoh_pool, 3, seed=seed, stream="starters:sinnoh")
    return {"hoenn": hoenn, "sinnoh": sinnoh}


def place_legendary_encounters(
    eligible_slots: Sequence[str],
    legendary_species: Sequence[T],
    *,
    seed: str,
    duplicate_policy: str = "allow",
    protected_slots: Iterable[str] = (),
) -> dict[str, T]:
    """Assign legendary species to eligible slots, leaving protected slots untouched."""
    if duplicate_policy not in {"allow", "unique"}:
        raise ValueError("duplicate_policy must be 'allow' or 'unique'")
    if len(set(eligible_slots)) != len(eligible_slots):
        raise ValueError("eligible_slots must not contain duplicates")
    if len(set(legendary_species)) != len(legendary_species):
        raise ValueError("legendary_species must not contain duplicates")

    protected = set(protected_slots)
    slots = [slot for slot in eligible_slots if slot not in protected]
    if not slots or not legendary_species:
        return {}

    if duplicate_policy == "unique":
        assignments = choose_distinct(
            legendary_species,
            min(len(slots), len(legendary_species)),
            seed=seed,
            stream="legendary_placement",
        )
    else:
        rng = rng_for(seed, "legendary_placement")
        assignments = [rng.choice(legendary_species) for _ in slots]

    return dict(zip(slots, assignments))
