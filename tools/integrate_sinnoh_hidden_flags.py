"""Normalize Sinnoh hidden-item flags to assembler numeric constants."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

# These six flags are reserved for Wayward Cave 1F in the pinned Sinnoh fork.
# Numeric literals are required here because mapjson emits the flag token
# directly into GNU as, where the final two aliases are unresolved.
HIDDEN_FLAGS = {
    "FLAG_HIDDEN_ITEM_WAYWARDCAVE_1F_YELLOW_SHARD": "0x493",
    "FLAG_HIDDEN_ITEM_WAYWARDCAVE_1F_GREAT_BALL": "0x494",
    "FLAG_HIDDEN_ITEM_WAYWARDCAVE_1F_RED_SHARD": "0x495",
    "FLAG_HIDDEN_ITEM_WAYWARDCAVE_1F_GREEN_SHARD": "0x496",
    "FLAG_HIDDEN_ITEM_WAYWARDCAVE_1F_SUPER_POTION": "0x497",
    "FLAG_HIDDEN_ITEM_WAYWARDCAVE_1F_BLUE_SHARD": "0x498",
}


def normalize_map(map_path: Path) -> int:
    data = json.loads(map_path.read_text(encoding="utf-8"))
    changed = 0
    for event in data.get("bg_events", []):
        flag = event.get("flag")
        if event.get("type") == "hidden_item" and flag in HIDDEN_FLAGS:
            event["flag"] = HIDDEN_FLAGS[flag]
            changed += 1
    if changed != len(HIDDEN_FLAGS):
        raise ValueError(
            f"Expected {len(HIDDEN_FLAGS)} Wayward Cave hidden items; normalized {changed}"
        )
    map_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    map_path = args.engine_dir / "data" / "maps" / "WaywardCave_1F" / "map.json"
    count = normalize_map(map_path)
    print(f"Normalized {count} Wayward Cave hidden-item flags for GNU as")


if __name__ == "__main__":
    main()
