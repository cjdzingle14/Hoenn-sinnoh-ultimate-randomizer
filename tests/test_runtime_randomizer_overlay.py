from tools.integrate_runtime_randomizers import patch_trainer_util, patch_wild_encounter

POOL = [f"SPECIES_TEST_{i}" for i in range(12)]


def test_wild_overlay_includes_runtime_rng_header():
    source = """#include "global.h"
void CreateWildMon(enum Species species, u8 level)
{
    ZeroEnemyPartyMons();
}
"""
    patched = patch_wild_encounter(source, POOL)
    assert '#include "random.h"' in patched
    assert "sRandomizerWildSpecies" in patched
    assert "Random() % ARRAY_COUNT(sRandomizerWildSpecies)" in patched
    assert "\\n#include" not in patched


def test_trainer_overlay_includes_runtime_rng_header():
    source = """#include "global.h"
void GenerateMonFromTrainerMon(struct Pokemon *mon, const struct TrainerMon *trainerMon, struct TrainerGenerator *trainer)
{
    u32 data;
}
"""
    patched = patch_trainer_util(source, POOL)
    assert '#include "random.h"' in patched
    assert '#include "event_data.h"' in patched
    assert "Random() % ARRAY_COUNT(sRandomizerTrainerSpecies)" in patched
    assert "\\n#include" not in patched


def test_trainer_overlay_is_idempotent_and_keeps_rng_header():
    source = """#include "global.h"
void GenerateMonFromTrainerMon(struct Pokemon *mon, const struct TrainerMon *trainerMon, struct TrainerGenerator *trainer)
{
    u32 data;
}
"""
    once = patch_trainer_util(source, POOL)
    twice = patch_trainer_util(once, POOL)
    assert twice == once


def test_randomizer_pool_must_have_unique_species():
    import pytest
    with pytest.raises(ValueError):
        patch_trainer_util(
            """#include "global.h"
void GenerateMonFromTrainerMon(struct Pokemon *mon, const struct TrainerMon *trainerMon, struct TrainerGenerator *trainer)
{
    u32 data;
}
""",
            POOL[:-1] + [POOL[0]],
        )
