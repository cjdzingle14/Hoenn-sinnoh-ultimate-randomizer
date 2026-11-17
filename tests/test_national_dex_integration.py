import unittest

from tools.integrate_national_dex import patch_new_game_source


class NationalDexIntegrationTests(unittest.TestCase):
    def test_enables_national_dex_after_event_data_initialization(self):
        source = """void NewGameInitData(void)
{
    ResetPokedex();
    InitEventData();
    ClearTVShowData();
}
"""
        patched = patch_new_game_source(source)
        init_pos = patched.index("InitEventData();")
        enable_pos = patched.index("EnableNationalPokedex();")
        next_init = patched.index("ClearTVShowData();")
        self.assertLess(init_pos, enable_pos)
        self.assertLess(enable_pos, next_init)

    def test_rejects_unexpected_or_ambiguous_engine_source(self):
        with self.assertRaises(ValueError):
            patch_new_game_source("void NewGameInitData(void) {}")
        with self.assertRaises(ValueError):
            patch_new_game_source("InitEventData();\nInitEventData();")


if __name__ == "__main__":
    unittest.main()
