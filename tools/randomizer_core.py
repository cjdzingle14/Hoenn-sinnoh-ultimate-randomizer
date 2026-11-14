"""Small deterministic randomizer primitives; no game assets or ROM parsing."""
from __future__ import annotations

import hashlib
import random
from typing import Sequence, TypeVar

T = TypeVar("T")


def _stream_seed(seed: str, stream: str) -> int:
    """Derive a stable independent seed for one randomizer subsystem."""
    payload = f"hsur:v1:{seed}:{stream}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def rng_for(seed: str, stream: str) -> random.Random:
    return random.Random(_stream_seed(seed, stream))


def choose_distinct(items: Sequence[T], count: int, *, seed: str, stream: str) -> list[T]:
    """Choose distinct entries reproducibly, preserving source list semantics."""
    if count < 0:
        raise ValueError("count must be non-negative")
    if count > len(items):
        raise ValueError("not enough unique entries in pool")
    if len(set(items)) != len(items):
        raise ValueError("input pool must not contain duplicates")
    result = list(items)
    rng_for(seed, stream).shuffle(result)
    return result[:count]


def weighted_choice(weights: dict[T, int], *, seed: str, stream: str) -> T:
    """Choose one key using positive integer weights."""
    if not weights or any((not isinstance(w, int) or w <= 0) for w in weights.values()):
        raise ValueError("weights must be a non-empty mapping of positive integers")
    rng = rng_for(seed, stream)
    population = list(weights)
    return rng.choices(population, weights=[weights[k] for k in population], k=1)[0]
