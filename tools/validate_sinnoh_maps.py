"""Validate the native Sinnoh opening maps in the pinned engine submodule."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_map(engine: Path, name: str) -> dict:
    path = engine / "data" / "maps" / name / "map.json"
    if not path.is_file():
        raise SystemExit(f"Missing Sinnoh map data: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot parse {path}: {exc}") from exc


def require_layout(engine: Path, map_data: dict, name: str) -> None:
    layout_name = map_data.get("layout")
    if not layout_name:
        raise SystemExit(f"{name} has no layout reference")
    layout_dir = engine / "data" / "layouts" / layout_name.removeprefix("LAYOUT_").title().replace("_", "")
    # Layout folder casing follows the map's declared layout; use the conventional
    # map-name folder when present, which is how this Sinnoh source stores them.
    layout_dir = engine / "data" / "layouts" / name
    if not (layout_dir / "map.bin").is_file() or not (layout_dir / "border.bin").is_file():
        raise SystemExit(f"Missing GBA map/border binary for {name} at {layout_dir}")


def connected(map_data: dict, target: str, direction: str | None = None) -> bool:
    return any(
        edge.get("map") == target and (direction is None or edge.get("direction") == direction)
        for edge in map_data.get("connections", [])
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    engine = args.engine_dir

    twinleaf = load_map(engine, "TwinleafTown")
    route201 = load_map(engine, "Route201")
    require_layout(engine, twinleaf, "TwinleafTown")
    require_layout(engine, route201, "Route201")

    if twinleaf.get("id") != "MAP_TWINLEAF_TOWN":
        raise SystemExit("Twinleaf Town map ID does not match expected engine constant")
    if route201.get("id") != "MAP_ROUTE201":
        raise SystemExit("Route 201 map ID does not match expected engine constant")
    if not connected(twinleaf, "MAP_ROUTE201", "up"):
        raise SystemExit("Twinleaf Town is not connected north to Route 201")
    if not connected(route201, "MAP_TWINLEAF_TOWN", "down"):
        raise SystemExit("Route 201 is not connected south to Twinleaf Town")
    if not connected(route201, "MAP_SANDGEM_TOWN", "right"):
        raise SystemExit("Route 201 is missing its east connection to Sandgem Town")

    print("Sinnoh opening map validation passed: Twinleaf Town ↔ Route 201 → Sandgem Town")


if __name__ == "__main__":
    main()
