from pathlib import Path

import pytest

from tools.integrate_runtime_randomizers import (
    patch_flags,
    patch_trainer_util,
    patch_wild_encounter,
)


def species_pool():
    return [f"SPECIES_TEST_{i}" for i in range(12)]


def test_wild_randomization_is_runtime_gated_and_idempotent():
    source = '#include "global.h"\n\nvoid CreateWildMon(enum Species species, u8 level)\n{\n    ZeroEnemyPartyMons();\n}\n'
    patched = patch_wild_encounter(source, species_pool())
    assert "FLAG_RANDOMIZER_DISABLE_WILD" in patched
    assert "sRandomizerWildSpecies[Random() % ARRAY_COUNT(sRandomizerWildSpecies)]" in patched
    assert "ZeroEnemyPartyMons();" in patched
    assert patch_wild_encounter(patched, species_pool()) == patched


def test_trainer_randomization_is_runtime_gated_and_rebuilds_moveset():
    source = (
        '#include "global.h"\n#include "random.h"\n#include "trainer_util.h"\n'
        'void GenerateMonFromTrainerMon(struct Pokemon *mon, const struct TrainerMon *trainerMon, struct TrainerGenerator *trainer)\n'
        '{\n    u32 data;\n}\n'
    )
    patched = patch_trainer_util(source, species_pool())
    assert "FLAG_RANDOMIZER_DISABLE_TRAINERS" in patched
    assert "randomizedTrainerMon.species = sRandomizerTrainerSpecies" in patched
    assert "randomizedTrainerMon.moves[i] = MOVE_NONE;" in patched
    assert "trainerMon = &randomizedTrainerMon;" in patched
    assert patch_trainer_util(patched, species_pool()) == patched


def test_flags_claim_only_known_unused_slots():
    source = (
        "#define FLAG_UNUSED_0x493                                           0x493 // Unused Flag\n"
        "#define FLAG_UNUSED_0x494                                           0x494 // Unused Flag\n"
    )
    patched = patch_flags(source)
    assert "#define FLAG_RANDOMIZER_DISABLE_WILD" in patched
    assert "#define FLAG_RANDOMIZER_DISABLE_TRAINERS" in patched
    assert patch_flags(patched) == patched


def test_runtime_hooks_fail_closed_if_upstream_shape_changes():
    with pytest.raises(ValueError):
        patch_wild_encounter("void CreateWildMon(void) {}", species_pool())
    with pytest.raises(ValueError):
        patch_trainer_util("void GenerateMonFromTrainerMon(void) {}", species_pool())
