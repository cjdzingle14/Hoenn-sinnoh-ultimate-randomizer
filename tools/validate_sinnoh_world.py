"""Validate the logical connectivity of the planned original Sinnoh GBA slice."""
from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path


def validate_world(config: dict) -> list[str]:
    errors: list[str] = []
    maps = config.get("maps", [])
    ids = [entry.get("id") for entry in maps]
    if not ids or any(not item for item in ids):
        return ["maps must contain entries with non-empty ids"]
    if len(ids) != len(set(ids)):
        errors.append("map ids must be unique")
    known = set(ids)
    external = set(config.get("external_maps", []))
    if known & external:
        errors.append("external_maps must not duplicate maps in the playable slice")
    start = config.get("start_map")
    if start not in known:
        errors.append(f"start_map {start!r} is not declared")
        return errors

    graph = {map_id: set() for map_id in known}
    for entry in maps:
        source = entry["id"]
        for target in entry.get("connections", []) + entry.get("warps", []):
            if target not in known and target not in external:
                errors.append(f"{source} references unknown map {target}")
            elif target in known:
                graph[source].add(target)
                graph[target].add(source)

    reached = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for target in graph[current] - reached:
            reached.add(target)
            queue.append(target)
    unreachable = sorted(known - reached)
    if unreachable:
        errors.append("maps unreachable from start_map: " + ", ".join(unreachable))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", nargs="?", default="config/sinnoh_world_slice.json")
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    errors = validate_world(config)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Sinnoh slice graph valid: {len(config['maps'])} logical maps reachable from {config['start_map']}")


if __name__ == "__main__":
    main()
