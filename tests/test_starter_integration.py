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

    def test_patch_replaces_starters_and_fixes_bounds(self):
        source = """
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
"""
        patched = patch_starter_source(source, [
            "SPECIES_PIKACHU", "SPECIES_EEVEE", "SPECIES_TURTWIG"
        ])
        self.assertIn("SPECIES_PIKACHU", patched)
        self.assertIn("SPECIES_EEVEE", patched)
        self.assertIn("SPECIES_TURTWIG", patched)
        self.assertIn("chosenStarterId >= STARTER_MON_COUNT", patched)
        self.assertNotIn("GRASS_STARTER", patched)

if __name__ == "__main__":
    unittest.main()
