from pathlib import Path

from tools.sinnoh_maps import load_maps, reachable_from, validate_map_graph


def test_blueprint_graph_validates():
    maps = load_maps()
    assert validate_map_graph(maps) == []


def test_route_201_reachable_from_twinleaf():
    maps = load_maps()
    reached = reachable_from(maps, "SINNOH_TWINLEAF_TOWN")
    assert "SINNOH_ROUTE_201" in reached


def test_graph_rejects_unknown_map_connection():
    maps = load_maps()
    maps["SINNOH_TWINLEAF_TOWN"]["connections"].append(
        {"direction": "west", "destination": "NOT_A_MAP", "landing": [1, 1]}
    )
    errors = validate_map_graph(maps)
    assert any("unknown destination NOT_A_MAP" in error for error in errors)


def test_graph_rejects_out_of_bounds_landing():
    maps = load_maps()
    maps["SINNOH_TWINLEAF_TOWN"]["connections"][0]["landing"] = [999, 999]
    errors = validate_map_graph(maps)
    assert any("outside SINNOH_ROUTE_201" in error for error in errors)
