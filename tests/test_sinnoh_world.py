import json
from pathlib import Path

from tools.validate_sinnoh_world import validate_world


def test_first_sinnoh_slice_allows_declared_adjacent_native_maps():
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / "config/sinnoh_world_slice.json").read_text(encoding="utf-8"))
    assert validate_world(config) == []


def test_first_sinnoh_slice_still_rejects_undeclared_map_references():
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / "config/sinnoh_world_slice.json").read_text(encoding="utf-8"))
    config["maps"][0]["warps"].append("MAP_NOT_IN_ENGINE_OR_SLICE")
    errors = validate_world(config)
    assert any("references unknown map MAP_NOT_IN_ENGINE_OR_SLICE" in error for error in errors)
