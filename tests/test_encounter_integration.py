import unittest
from tools.integrate_encounters import randomize_wild_data, randomize_trainer_parties

class EncounterIntegrationTests(unittest.TestCase):
    def test_wild_randomization_preserves_levels_and_rates(self):
        data = {"wild_encounter_groups": [{"encounters": [{
            "map": "MAP_ROUTE101",
            "land_mons": {"encounter_rate": 20, "mons": [
                {"min_level": 2, "max_level": 3, "species": "SPECIES_WURMPLE"}
            ]}
        }]}]}
        count = randomize_wild_data(data, ["SPECIES_TREECKO", "SPECIES_TURTWIG"], "test")
        self.assertEqual(count, 1)
        mon = data["wild_encounter_groups"][0]["encounters"][0]["land_mons"]["mons"][0]
        self.assertIn(mon["species"], {"SPECIES_TREECKO", "SPECIES_TURTWIG"})
        self.assertEqual((mon["min_level"], mon["max_level"]), (2, 3))
        self.assertEqual(data["wild_encounter_groups"][0]["encounters"][0]["land_mons"]["encounter_rate"], 20)

    def test_trainer_randomization_keeps_levels_and_party_size(self):
        source = "=== TRAINER_TEST ===\nName: TEST\n\nPoochyena\nLevel: 7\nIVs: 0 HP\n"
        patched, count = randomize_trainer_parties(source, ["SPECIES_TREECKO", "SPECIES_TURTWIG"], "test")
        self.assertEqual(count, 1)
        self.assertIn("Level: 7", patched)
        self.assertNotIn("Poochyena", patched)
        self.assertTrue(any(x in patched for x in ["SPECIES_TREECKO", "SPECIES_TURTWIG"]))

if __name__ == "__main__":
    unittest.main()
