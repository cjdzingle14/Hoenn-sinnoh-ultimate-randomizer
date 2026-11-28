"""Normalize Wayward Cave hidden-item operands for GNU assembler map macros.

The Sinnoh fork stores these six entries with symbolic enum/flag names that are
not available as absolute expressions in the map-event assembler. The numeric
values below are taken from the fork's items.h and flags.h at the pinned
submodule revision. The JSON schema intentionally stores these operands as
strings, so mapjson emits valid assembler expressions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

WAYWARD_ITEMS = {
    "ITEM_YELLOW_SHARD": ("150", "0x493"),
    "ITEM_GREAT_BALL": ("2", "0x494"),
    "ITEM_RED_SHARD": ("148", "0x495"),
    "ITEM_GREEN_SHARD": ("151", "0x496"),
    "ITEM_SUPER_POTION": ("29", "0x497"),
    "ITEM_BLUE_SHARD": ("149", "0x498"),
}


def patch_map(map_path: Path) -> None:
    try:
        data = json.loads(map_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read {map_path}: {exc}") from exc

    hidden_items = [
        event for event in data.get("bg_events", [])
        if event.get("type") == "hidden_item"
    ]
    seen: set[str] = set()
    for event in hidden_items:
        item = event.get("item")
        if item not in WAYWARD_ITEMS:
            continue
        numeric_item, numeric_flag = WAYWARD_ITEMS[item]
        event["item"] = numeric_item
        event["flag"] = numeric_flag
        seen.add(item)

    missing = set(WAYWARD_ITEMS) - seen
    if missing:
        raise SystemExit(
            f"Wayward Cave hidden-item patch expected entries not found: {sorted(missing)}"
        )

    map_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    map_path = args.engine_dir / "data" / "maps" / "WaywardCave_1F" / "map.json"
    patch_map(map_path)
    print("Normalized six Wayward Cave hidden-item operands for GBA assembly")


if __name__ == "__main__":
    main()
