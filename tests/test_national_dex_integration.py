import unittest

from tools.integrate_national_dex import patch_pokedex_source


class NationalDexIntegrationTests(unittest.TestCase):
    def test_enables_national_dex_after_new_game_reset(self):
        source = """void ResetPokedex(void)
{
    DisableNationalPokedex();
    ClearDexFlags();
}
"""
        patched = patch_pokedex_source(source)
        self.assertIn("DisableNationalPokedex();", patched)
        self.assertIn("EnableNationalPokedex();", patched)
        self.assertLess(patched.index("DisableNationalPokedex();"), patched.index("EnableNationalPokedex();"))

    def test_rejects_unexpected_or_ambiguous_engine_source(self):
        with self.assertRaises(ValueError):
            patch_pokedex_source("void ResetPokedex(void) {}")
        with self.assertRaises(ValueError):
            patch_pokedex_source("DisableNationalPokedex();\nDisableNationalPokedex();")


if __name__ == "__main__":
    unittest.main()
