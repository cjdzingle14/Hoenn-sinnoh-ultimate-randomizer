import json

from tools.integrate_sinnoh_hidden_flags import HIDDEN_FLAGS, normalize_map


def test_normalize_wayward_cave_hidden_item_flags(tmp_path):
    map_path = tmp_path / "map.json"
    map_path.write_text(
        json.dumps({
            "bg_events": [
                {"type": "hidden_item", "flag": flag}
                for flag in HIDDEN_FLAGS
            ]
        }),
        encoding="utf-8",
    )

    assert normalize_map(map_path) == 6
    result = json.loads(map_path.read_text(encoding="utf-8"))
    assert [event["flag"] for event in result["bg_events"]] == list(HIDDEN_FLAGS.values())
