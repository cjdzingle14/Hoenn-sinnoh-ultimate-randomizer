import unittest
from tools.grotto_rules import choose_grotto_outcome

class GrottoRulesTests(unittest.TestCase):
    def setUp(self):
        self.beasts = ["Nihilego", "Buzzwole", "Pheromosa", "Xurkitree"]
        self.items = ["Master Ball", "Rare Candy", "Gold Bottle Cap"]

    def test_same_seed_and_grotto_are_reproducible(self):
        args = dict(seed="alpha", ultra_beasts=self.beasts, rare_items=self.items)
        self.assertEqual(choose_grotto_outcome("petalburg-woods", **args),
                         choose_grotto_outcome("petalburg-woods", **args))

    def test_each_grotto_has_its_own_deterministic_stream(self):
        args = dict(seed="alpha", ultra_beasts=self.beasts, rare_items=self.items)
        for grotto in ("petalburg-woods", "granite-cave"):
            self.assertEqual(choose_grotto_outcome(grotto, **args),
                             choose_grotto_outcome(grotto, **args))

    def test_forced_empty_and_ultra_beast_outcomes(self):
        args = dict(seed="alpha", ultra_beasts=self.beasts, rare_items=self.items)
        self.assertEqual(choose_grotto_outcome("empty", **args,
            weights={"ultra_beast": 0, "rare_item": 0, "empty": 1}), ("empty", None))
        kind, species = choose_grotto_outcome("beast", **args,
            weights={"ultra_beast": 1, "rare_item": 0, "empty": 0})
        self.assertEqual(kind, "ultra_beast")
        self.assertIn(species, self.beasts)

    def test_invalid_pools_and_weights_are_rejected(self):
        with self.assertRaises(ValueError):
            choose_grotto_outcome("bad", seed="alpha", ultra_beasts=[],
                rare_items=self.items, weights={"ultra_beast": 1, "rare_item": 1, "empty": 1})
        with self.assertRaises(ValueError):
            choose_grotto_outcome("bad", seed="alpha", ultra_beasts=self.beasts,
                rare_items=self.items, weights={"beast": 1})

if __name__ == "__main__":
    unittest.main()
