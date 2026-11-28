from __future__ import annotations

import json

from tools.patch_sinnoh_hidden_items import WAYWARD_ITEMS, patch_map


def test_wayward_cave_hidden_item_operands_are_numeric(tmp_path):
    map_path = tmp_path / "map.json"
    data = {
        "bg_events": [
            {"type": "hidden_item", "item": item, "flag": f"FLAG_{item}"}
            for item in WAYWARD_ITEMS
        ]
    }
    map_path.write_text(json.dumps(data), encoding="utf-8")

    patch_map(map_path)

    patched = json.loads(map_path.read_text(encoding="utf-8"))
    actual = {event["item"]: event["flag"] for event in patched["bg_events"]}
    assert actual == {
        numeric_item: numeric_flag
        for numeric_item, numeric_flag in WAYWARD_ITEMS.values()
    }
