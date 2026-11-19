import unittest

from tools.region_selection import (
    available_starting_regions,
    resolve_starting_region,
)


BASE_CONFIG = {
    "world": {"regions": ["hoenn", "sinnoh"]},
    "new_game_region_selection": {"enabled": True, "default": "hoenn"},
}


class RegionSelectionTests(unittest.TestCase):
    def test_both_regions_are_offered(self):
        self.assertEqual(available_starting_regions(BASE_CONFIG), ("hoenn", "sinnoh"))

    def test_default_preserves_hoenn_opening(self):
        self.assertEqual(resolve_starting_region(BASE_CONFIG).start_key, "hoenn_new_game_start")

    def test_player_can_choose_sinnoh(self):
        start = resolve_starting_region(BASE_CONFIG, "sinnoh")
        self.assertEqual(start.region, "sinnoh")
        self.assertEqual(start.start_key, "sinnoh_new_game_start")

    def test_choice_is_case_and_whitespace_tolerant(self):
        self.assertEqual(resolve_starting_region(BASE_CONFIG, "  SINNOH ").region, "sinnoh")

    def test_rejects_unavailable_region(self):
        config = {"world": {"regions": ["hoenn"]}, "new_game_region_selection": {"enabled": True}}
        with self.assertRaisesRegex(ValueError, "invalid starting region"):
            resolve_starting_region(config, "sinnoh")

    def test_rejects_unknown_configured_region(self):
        config = {"world": {"regions": ["hoenn", "kanto"]}}
        with self.assertRaisesRegex(ValueError, "unsupported starting region"):
            available_starting_regions(config)

    def test_rejects_duplicate_region_ids(self):
        config = {"world": {"regions": ["hoenn", "hoenn"]}}
        with self.assertRaisesRegex(ValueError, "duplicate"):
            available_starting_regions(config)

    def test_both_regions_can_still_belong_to_one_adventure(self):
        # Choosing Sinnoh changes the opening location, not world availability.
        self.assertEqual(available_starting_regions(BASE_CONFIG), ("hoenn", "sinnoh"))


if __name__ == "__main__":
    unittest.main()
