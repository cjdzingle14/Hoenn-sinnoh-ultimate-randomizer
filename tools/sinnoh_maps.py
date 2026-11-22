"""Validate the Sinnoh starter-area map graph blueprint.

This is an integration scaffold: it validates region data and reachability,
not native pokeemerald map binaries or a compiled ROM.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BLUEPRINT_PATH = Path(__file__).parents[1] / "data" / "sinnoh" / "first_area_blueprint.json"


def load_maps(path: Path = BLUEPRINT_PATH) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("Unsupported Sinnoh blueprint schema")
    maps = payload.get("maps", [])
    result = {map_data["id"]: map_data for map_data in maps}
    if len(result) != len(maps):
        raise ValueError("Map IDs must be unique")
    return result


def validate_map_graph(maps: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for map_id, map_data in maps.items():
        dims = map_data.get("dimensions", {})
        if not isinstance(dims.get("width"), int) or dims["width"] <= 0:
            errors.append(f"{map_id}: width must be a positive integer")
        if not isinstance(dims.get("height"), int) or dims["height"] <= 0:
            errors.append(f"{map_id}: height must be a positive integer")
        for connection in map_data.get("connections", []):
            destination = connection.get("destination")
            if destination not in maps and destination != "SINNOH_LAKE_VERITY":
                errors.append(f"{map_id}: unknown destination {destination}")
                continue
            landing = connection.get("landing")
            if destination in maps and landing:
                target_dims = maps[destination]["dimensions"]
                x, y = landing
                if not (0 <= x < target_dims["width"] and 0 <= y < target_dims["height"]):
                    errors.append(f"{map_id}: landing {landing} outside {destination}")
        for encounter in map_data.get("encounter_slots", []):
            lo, hi = encounter.get("level_min"), encounter.get("level_max")
            if not isinstance(lo, int) or not isinstance(hi, int) or lo < 1 or lo > hi:
                errors.append(f"{map_id}: invalid encounter level range {lo}-{hi}")
    return errors


def reachable_from(maps: dict[str, Any], start: str) -> set[str]:
    if start not in maps:
        raise KeyError(f"Unknown start map: {start}")
    reached: set[str] = set()
    pending = [start]
    while pending:
        current = pending.pop()
        if current in reached:
            continue
        reached.add(current)
        for edge in maps[current].get("connections", []):
            dest = edge.get("destination")
            if dest in maps and dest not in reached:
                pending.append(dest)
    return reached


def main() -> int:
    maps = load_maps()
    errors = validate_map_graph(maps)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    reached = reachable_from(maps, "SINNOH_TWINLEAF_TOWN")
    required = {"SINNOH_TWINLEAF_TOWN", "SINNOH_ROUTE_201"}
    missing = required - reached
    if missing:
        print("ERROR: unreachable required maps: " + ", ".join(sorted(missing)))
        return 1
    print(f"Sinnoh blueprint OK: {len(maps)} maps, {len(reached)} starter-area maps reachable")
    print("Lake Verity is marked as the next map target but is not implemented.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
