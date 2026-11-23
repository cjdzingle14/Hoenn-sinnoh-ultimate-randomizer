"""Validate the prototype Sinnoh grid assets and region-start configuration."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
MAP_FILES = (
    ROOT / "data/sinnoh/twinleaf_town_grid.json",
    ROOT / "data/sinnoh/route_201_grid.json",
)
REGION_FILE = ROOT / "data/new_game_region_selection.json"


def validate_grid(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    width, height = data.get("size", [0, 0])
    rows = data.get("tiles", [])
    if len(rows) != height:
        errors.append(f"{path.name}: expected {height} rows, got {len(rows)}")
    for y, row in enumerate(rows):
        if len(row) != width:
            errors.append(f"{path.name}: row {y} expected width {width}, got {len(row)}")
        unknown = set(row) - set(data.get("legend", {}))
        if unknown:
            errors.append(f"{path.name}: row {y} uses unknown tile codes {sorted(unknown)}")
    event_ids = [event.get("id") for event in data.get("events", [])]
    if len(event_ids) != len(set(event_ids)):
        errors.append(f"{path.name}: event IDs are not unique")
    for event in data.get("events", []):
        tile = event.get("tile")
        if tile and not (0 <= tile[0] < width and 0 <= tile[1] < height):
            errors.append(f"{path.name}: event {event.get('id')} outside map at {tile}")
    return errors


def validate_region_selector(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    selector = data.get("new_game_region_selection", {})
    options = selector.get("options", [])
    ids = [option.get("id") for option in options]
    errors: list[str] = []
    if not selector.get("enabled"):
        errors.append("new-game region selection is disabled")
    if len(ids) != len(set(ids)):
        errors.append("region IDs are not unique")
    if "HOENN" not in ids or "SINNOH" not in ids:
        errors.append("both HOENN and SINNOH choices must exist")
    sinnoh = next((option for option in options if option.get("id") == "SINNOH"), {})
    if sinnoh.get("start_map") != "SINNOH_TWINLEAF_TOWN":
        errors.append("Sinnoh must start in Twinleaf Town")
    if selector.get("selection_scope") != "new_game_only":
        errors.append("region selection must only affect new games")
    return errors


def main() -> int:
    errors = [error for path in MAP_FILES for error in validate_grid(path)]
    errors.extend(validate_region_selector(REGION_FILE))
    if errors:
        print("\n".join("ERROR: " + error for error in errors))
        return 1
    print("Prototype Sinnoh grids and region selector are structurally valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
