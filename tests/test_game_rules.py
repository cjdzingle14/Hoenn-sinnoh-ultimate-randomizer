import json
import tempfile
import unittest
from pathlib import Path

from tools.game_rules import (
    choose_starters,
    gym_tier_for_progress,
    load_settings,
    place_legendary_encounters,
    progression_score,
    validate_settings,
)


class GameRulesTests(unittest.TestCase):
    def test_repository_settings_load_and_validate(self):
        path = Path(__file__).parents[1] / "config" / "randomizer.json"
        settings = load_settings(path)
        self.assertEqual(settings["world"]["mode"], "both_open")

    def test_invalid_settings_report_inconsistent_world(self):
        settings = {
            "schema_version": 1,
            "world": {"mode": "separate", "regions": ["hoenn"], "travel_unlocked_at_start": False},
            "gym_progression": {"mode": "scaled", "tier_thresholds": [0, 2, 2]},
            "starters": {"mode": "random_three_distinct"},
            "encounters": {"legendary_duplicate_policy": "allow"},
            "mega_evolution": {"enabled": True},
        }
        with self.assertRaisesRegex(ValueError, "both_open"):
            validate_settings(settings)

    def test_progression_and_tier_selection(self):
        score = progression_score(4, 2)
        self.assertEqual(score, 6)
        self.assertEqual(gym_tier_for_progress(score, [0, 2, 4, 6, 8]), 3)
        self.assertEqual(gym_tier_for_progress(99, [0, 2, 4]), 2)

    def test_progression_rejects_negative_values(self):
        with self.assertRaises(ValueError):
            progression_score(-1, 0)

    def test_starters_are_three_distinct_and_exclude_banned(self):
        pool = ["Treecko", "Torchic", "Mudkip", "Turtwig", "Chimchar", "Piplup"]
        result = choose_starters(pool, seed="alpha", banned_species={"Treecko"})
        self.assertEqual(len(result), 3)
        self.assertEqual(len(set(result)), 3)
        self.assertNotIn("Treecko", result)
        self.assertEqual(result, choose_starters(pool, seed="alpha", banned_species={"Treecko"}))

    def test_legendary_slots_respect_protected_story_encounters(self):
        result = place_legendary_encounters(
            ["ROUTE_101", "CAVE_DEPTHS", "STORY_ALTAR"],
            ["Latias", "Latios", "Rayquaza"],
            seed="world-seed",
            duplicate_policy="unique",
            protected_slots={"STORY_ALTAR"},
        )
        self.assertNotIn("STORY_ALTAR", result)
        self.assertEqual(len(result), 2)
        self.assertEqual(len(set(result.values())), 2)
        self.assertEqual(
            result,
            place_legendary_encounters(
                ["ROUTE_101", "CAVE_DEPTHS", "STORY_ALTAR"],
                ["Latias", "Latios", "Rayquaza"],
                seed="world-seed",
                duplicate_policy="unique",
                protected_slots={"STORY_ALTAR"},
            ),
        )

    def test_legendary_placement_can_allow_duplicates(self):
        slots = ["A", "B", "C", "D"]
        result = place_legendary_encounters(
            slots, ["Mewtwo"], seed="repeatable", duplicate_policy="allow"
        )
        self.assertEqual(result, {slot: "Mewtwo" for slot in slots})


if __name__ == "__main__":
    unittest.main()
