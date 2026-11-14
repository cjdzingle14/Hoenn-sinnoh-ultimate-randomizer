"""Seeded, independent Hidden Grotto outcome selection."""
from __future__ import annotations
from typing import Sequence, TypeVar
from tools.randomizer_core import rng_for, weighted_choice
T = TypeVar("T")

def choose_grotto_outcome(grotto_id: str, *, seed: str, ultra_beasts: Sequence[T],
                          rare_items: Sequence[T], weights: dict[str, int] | None = None
                          ) -> tuple[str, T | None]:
    """Return a reproducible result: ultra_beast, rare_item, or empty."""
    if not isinstance(grotto_id, str) or not grotto_id.strip():
        raise ValueError("grotto_id must be a non-empty string")
    if len(set(ultra_beasts)) != len(ultra_beasts):
        raise ValueError("ultra_beasts must not contain duplicates")
    if len(set(rare_items)) != len(rare_items):
        raise ValueError("rare_items must not contain duplicates")
    chances = weights or {"ultra_beast": 45, "rare_item": 35, "empty": 20}
    if set(chances) != {"ultra_beast", "rare_item", "empty"}:
        raise ValueError("weights must define ultra_beast, rare_item, and empty")
    if any(type(value) is not int or value < 0 for value in chances.values()) or not any(chances.values()):
        raise ValueError("weights must be non-negative integers with a positive total")
    if chances["ultra_beast"] and not ultra_beasts:
        raise ValueError("ultra_beasts pool cannot be empty when its weight is positive")
    if chances["rare_item"] and not rare_items:
        raise ValueError("rare_items pool cannot be empty when its weight is positive")
    stream = f"grotto:{grotto_id}"
    active_chances = {kind: weight for kind, weight in chances.items() if weight > 0}
    outcome = weighted_choice(active_chances, seed=seed, stream=f"{stream}:outcome")
    if outcome == "empty":
        return outcome, None
    pool = ultra_beasts if outcome == "ultra_beast" else rare_items
    return outcome, rng_for(seed, f"{stream}:{outcome}").choice(list(pool))
