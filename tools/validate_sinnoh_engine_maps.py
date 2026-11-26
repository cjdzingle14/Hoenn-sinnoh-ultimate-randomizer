"""Validate that the first Sinnoh slice resolves to real maps in the pinned GBA engine."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate(engine_root: Path, manifest_path: Path) -> list[str]:
    errors: list[str] = []
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    groups_path = engine_root / "data/maps/map_groups.json"
    if not groups_path.is_file():
        return [f"engine map registry not found: {groups_path}"]
    groups = json.loads(groups_path.read_text(encoding="utf-8"))
    registered = {name for group in groups.get("group_order", []) for name in groups.get(group, [])}
    map_by_id = {}
    for entry in manifest.get("maps", []):
        source = entry["source"]
        map_path = engine_root / "data/maps" / source / "map.json"
        if not map_path.is_file():
            errors.append(f"native map data missing: {map_path}")
            continue
        data = json.loads(map_path.read_text(encoding="utf-8"))
        if data.get("id") != entry["id"]:
            errors.append(f"{source}: manifest id does not match native id (manifest {entry['id']}, engine {data.get('id')})")
        if source not in registered:
            errors.append(f"{source}: not registered in data/maps/map_groups.json")
        map_by_id[entry["id"]] = data

    start = manifest.get("start_map")
    if start not in map_by_id:
        errors.append(f"start map {start!r} is not a verified native map")
        return errors

    graph = {map_id: set() for map_id in map_by_id}
    for map_id, data in map_by_id.items():
        for connection in data.get("connections") or []:
            target = connection.get("map")
            if target in graph:
                graph[map_id].add(target)
                graph[target].add(map_id)
        for warp in data.get("warp_events") or []:
            target = warp.get("dest_map")
            if target in graph:
                graph[map_id].add(target)
                graph[target].add(map_id)

    reached = {start}
    pending = [start]
    while pending:
        current = pending.pop()
        for target in graph[current] - reached:
            reached.add(target)
            pending.append(target)
    if reached != set(graph):
        errors.append("native maps unreachable from start: " + ", ".join(sorted(set(graph) - reached)))

    # These checks deliberately bind the manifest to real engine map IDs.
    for region_key in ("hoenn_start",):
        region_map = manifest.get(region_key, {})
        source = region_map.get("source")
        path = engine_root / "data/maps" / str(source) / "map.json"
        if not path.is_file():
            errors.append(f"{region_key}: native map data missing: {path}")
        else:
            native = json.loads(path.read_text(encoding="utf-8"))
            if native.get("id") != region_map.get("id"):
                errors.append(f"{region_key}: manifest id does not match native map id")
            if source not in registered:
                errors.append(f"{region_key}: map is not registered in map_groups.json")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", default="vendor/pokeemerald-expansion")
    parser.add_argument("--manifest", default="config/sinnoh_world_slice.json")
    args = parser.parse_args()
    errors = validate(Path(args.engine), Path(args.manifest))
    if errors:
        raise SystemExit("\\n".join(errors))
    print("Native Sinnoh map slice verified: Twinleaf home -> Twinleaf Town -> Route 201 -> Sandgem Town")
    print("Hoenn Littleroot start map is also present and registered.")


if __name__ == "__main__":
    main()
