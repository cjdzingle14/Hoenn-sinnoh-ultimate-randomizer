import unittest
from tools.integrate_starters import parse_species_constants, patch_starter_source


class StarterIntegrationTests(unittest.TestCase):
    def test_parser_excludes_legendary_and_form_entries(self):
        header = """
SPECIES_BULBASAUR = 1,
SPECIES_MEWTWO = 150,
SPECIES_TREECKO = 252,
SPECIES_TURTWIG = 387,
SPECIES_PIKACHU_COSPLAY = 10001,
"""
        self.assertEqual(parse_species_constants(header), [
            "SPECIES_BULBASAUR", "SPECIES_TREECKO", "SPECIES_TURTWIG"
        ])

    def test_patch_builds_runtime_randomized_distinct_pool(self):
        source = """
#include "main.h"
static const u16 sStarterMon[STARTER_MON_COUNT] =
{
    GRASS_STARTER,
    FIRE_STARTER,
    WATER_STARTER,
};
u16 GetStarterPokemon(u16 chosenStarterId)
{
    if (chosenStarterId > STARTER_MON_COUNT)
        chosenStarterId = 0;
    return sStarterMon[chosenStarterId];
}
void CB2_ChooseStarter(void)
{
    StartSelection();
}
"""
        patched = patch_starter_source(source, [
            "SPECIES_BULBASAUR", "SPECIES_TREECKO", "SPECIES_TURTWIG",
            "SPECIES_PIKACHU", "SPECIES_EEVEE",
        ])
        self.assertIn('#include "random.h"', patched)
        self.assertIn("static const u16 sStarterPool[]", patched)
        self.assertIn("candidate = sStarterPool[Random() % ARRAY_COUNT(sStarterPool)]", patched)
        self.assertIn("if (sStarterMon[j] == candidate)", patched)
        self.assertIn("RandomizeStarterChoices();", patched)
        self.assertIn("chosenStarterId >= STARTER_MON_COUNT", patched)
        self.assertNotIn("GRASS_STARTER", patched)

    def test_patch_rejects_pool_with_fewer_than_three_species(self):
        with self.assertRaises(ValueError):
            patch_starter_source("void CB2_ChooseStarter(void)\\n{", ["SPECIES_A", "SPECIES_B"])


if __name__ == "__main__":
    unittest.main()
