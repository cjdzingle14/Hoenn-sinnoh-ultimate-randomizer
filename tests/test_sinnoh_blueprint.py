"""Structural checks for the initial Sinnoh map blueprint.

This validates the design data only; it does not compile maps into the ROM.
"""
import json
from pathlib import Path

BLUEPRINT = Path(__file__).parents[1] / "data" / "sinnoh" / "first_area_blueprint.json"


def load_blueprint():
    return json.loads(BLUEPRINT.read_text(encoding="utf-8"))


def test_twinleaf_and_route_201_are_defined():
    data = load_blueprint()
    maps = {entry["id"]: entry for entry in data["maps"]}
    assert "SINNOH_TWINLEAF_TOWN" in maps
    assert "SINNOH_ROUTE_201" in maps


def test_initial_map_connections_are_bidirectional():
    maps = {entry["id"]: entry for entry in load_blueprint()["maps"]}
    twinleaf_targets = {c["destination"] for c in maps["SINNOH_TWINLEAF_TOWN"]["connections"]}
    route_targets = {c["destination"] for c in maps["SINNOH_ROUTE_201"]["connections"]}
    assert "SINNOH_ROUTE_201" in twinleaf_targets
    assert "SINNOH_TWINLEAF_TOWN" in route_targets


def test_route_201_has_early_game_encounters_and_trainers():
    route = next(m for m in load_blueprint()["maps"] if m["id"] == "SINNOH_ROUTE_201")
    slots = route["encounter_slots"]
    assert slots and all(1 <= s["level_min"] <= s["level_max"] <= 10 for s in slots)
    assert route["trainer_placeholders"]
    assert all(t["team_size"] >= 1 for t in route["trainer_placeholders"])


def test_map_dimensions_and_interior_warp_counts_are_sane():
    for map_data in load_blueprint()["maps"]:
        dims = map_data["dimensions"]
        assert dims["width"] > 0 and dims["height"] > 0
    town = next(m for m in load_blueprint()["maps"] if m["id"] == "SINNOH_TWINLEAF_TOWN")
    assert all(interior["warp_count"] >= 1 for interior in town["interiors"])


def test_lake_verity_is_next_connection_target():
    data = load_blueprint()
    route = next(m for m in data["maps"] if m["id"] == "SINNOH_ROUTE_201")
    assert any(c["destination"] == "SINNOH_LAKE_VERITY" for c in route["connections"])
    assert data["next_map_placeholder"]["status"] == "planned"
