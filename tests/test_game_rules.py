import unittest
from pathlib import Path

from tools.game_rules import (
    choose_regional_starters,
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
            "starters": {
                "mode": "random_three_per_region",
                "regions": ["hoenn", "sinnoh"],
                "choices_per_region": 3,
                "player_picks_per_region": 1,
                "unique_across_both_regions": True,
            },
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

    def test_each_region_gets_three_choices_and_all_six_are_unique(self):
        pool = [
            "Treecko", "Torchic", "Mudkip", "Turtwig", "Chimchar", "Piplup",
            "Bulbasaur", "Charmander", "Squirtle", "Chikorita", "Cyndaquil", "Totodile",
        ]
        result = choose_regional_starters(pool, seed="two-region-run")
        self.assertEqual(set(result), {"hoenn", "sinnoh"})
        self.assertEqual(len(result["hoenn"]), 3)
        self.assertEqual(len(result["sinnoh"]), 3)
        self.assertEqual(len(set(result["hoenn"] + result["sinnoh"])), 6)
        self.assertEqual(result, choose_regional_starters(pool, seed="two-region-run"))

    def test_regional_starters_exclude_banned_and_require_six_eligible(self):
        pool = ["A", "B", "C", "D", "E", "F", "BANNED"]
        result = choose_regional_starters(pool, seed="regional", banned_species={"BANNED"})
        self.assertEqual(len(set(result["hoenn"] + result["sinnoh"])), 6)
        with self.assertRaises(ValueError):
            choose_regional_starters(pool[:5], seed="too-small")

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
