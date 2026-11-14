import unittest

from tools.randomizer_core import choose_distinct, weighted_choice


class RandomizerCoreTests(unittest.TestCase):
    def test_starters_are_reproducible(self):
        pool = ["Treecko", "Torchic", "Mudkip", "Turtwig", "Chimchar", "Piplup"]
        first = choose_distinct(pool, 3, seed="abc123", stream="starters")
        second = choose_distinct(pool, 3, seed="abc123", stream="starters")
        self.assertEqual(first, second)
        self.assertEqual(len(set(first)), 3)

    def test_streams_are_independent(self):
        pool = list(range(30))
        self.assertNotEqual(
            choose_distinct(pool, 8, seed="abc123", stream="starters"),
            choose_distinct(pool, 8, seed="abc123", stream="wild"),
        )

    def test_invalid_pool(self):
        with self.assertRaises(ValueError):
            choose_distinct(["A", "A"], 1, seed="x", stream="starters")

    def test_weighted_choice_reproducible(self):
        weights = {"common": 90, "rare": 10}
        self.assertEqual(
            weighted_choice(weights, seed="seed", stream="legendary"),
            weighted_choice(weights, seed="seed", stream="legendary"),
        )


if __name__ == "__main__":
    unittest.main()
