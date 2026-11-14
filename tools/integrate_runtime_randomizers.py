"""Integrate runtime wild and trainer randomization with persistent option flags."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from tools.integrate_encounters import parse_species_constants

FLAG_PATCHES = {
    "#define FLAG_UNUSED_0x493                                           0x493 // Unused Flag":
        "#define FLAG_RANDOMIZER_DISABLE_WILD                              0x493 // Cleared by default: wild randomization ON",
    "#define FLAG_UNUSED_0x494                                           0x494 // Unused Flag":
        "#define FLAG_RANDOMIZER_DISABLE_TRAINERS                          0x494 // Cleared by default: trainer randomization ON",
}

def _pool_source(pool: list[str], name: str) -> str:
    if len(pool) < 10 or len(pool) != len(set(pool)):
        raise ValueError("Randomizer species pool must contain at least ten unique species")
    entries = ",\n".join(f"    {species}" for species in pool)
    return f"static const u16 {name}[] = {{\n{entries}\n}};\n"

def _insert_after_global(source: str, addition: str) -> str:
    if addition.strip() in source:
        return source
    anchor = '#include "global.h"'
    if source.count(anchor) != 1:
        raise ValueError("Expected exactly one global.h include")
    return source.replace(anchor, anchor + "\n#include \"event_data.h\"\n" + addition, 1)

def patch_wild_encounter(source: str, pool: list[str]) -> str:
    array = _pool_source(pool, "sRandomizerWildSpecies")
    if "sRandomizerWildSpecies" not in source:
        source = _insert_after_global(source, array)
    anchor = """void CreateWildMon(enum Species species, u8 level)
{
    ZeroEnemyPartyMons();"""
    replacement = """void CreateWildMon(enum Species species, u8 level)
{
    // This runtime switch preserves the original encounter when randomization is disabled.
    if (!FlagGet(FLAG_RANDOMIZER_DISABLE_WILD))
        species = sRandomizerWildSpecies[Random() % ARRAY_COUNT(sRandomizerWildSpecies)];

    ZeroEnemyPartyMons();"""
    if replacement in source:
        return source
    if source.count(anchor) != 1:
        raise ValueError("Could not find the expected CreateWildMon implementation")
    if '#include "random.h"' not in source:
        source = source.replace('#include "global.h"', '#include "global.h"\n#include "random.h"', 1)
    return source.replace(anchor, replacement, 1)

def patch_trainer_util(source: str, pool: list[str]) -> str:
    array = _pool_source(pool, "sRandomizerTrainerSpecies")
    if "sRandomizerTrainerSpecies" not in source:
        source = _insert_after_global(source, array)
    anchor = """void GenerateMonFromTrainerMon(struct Pokemon *mon, const struct TrainerMon *trainerMon, struct TrainerGenerator *trainer)
{
    u32 data;"""
    replacement = """void GenerateMonFromTrainerMon(struct Pokemon *mon, const struct TrainerMon *trainerMon, struct TrainerGenerator *trainer)
{
    struct TrainerMon randomizedTrainerMon;
    u32 data;

    // Randomize at party-generation time so the in-game option can restore vanilla teams.
    if (!FlagGet(FLAG_RANDOMIZER_DISABLE_TRAINERS))
    {
        u8 i;
        memcpy(&randomizedTrainerMon, trainerMon, sizeof(randomizedTrainerMon));
        randomizedTrainerMon.species = sRandomizerTrainerSpecies[Random() % ARRAY_COUNT(sRandomizerTrainerSpecies)];
        randomizedTrainerMon.nickname = NULL;
        randomizedTrainerMon.ability = ABILITY_NONE;
        randomizedTrainerMon.gender = TRAINER_MON_RANDOM_GENDER;
        for (i = 0; i < MAX_MON_MOVES; i++)
            randomizedTrainerMon.moves[i] = MOVE_NONE;
        trainerMon = &randomizedTrainerMon;
    }"""
    if replacement in source:
        return source
    if source.count(anchor) != 1:
        raise ValueError("Could not find the expected GenerateMonFromTrainerMon implementation")
    return source.replace(anchor, replacement, 1)

def patch_flags(source: str) -> str:
    for old, new in FLAG_PATCHES.items():
        if new in source:
            continue
        if source.count(old) != 1:
            raise ValueError(f"Expected one unused flag slot for {new.split()[1]}")
        source = source.replace(old, new, 1)
    return source

def integrate(engine_dir: Path) -> int:
    header = (engine_dir / "include/constants/species.h").read_text(encoding="utf-8")
    pool = parse_species_constants(header)
    flags_path = engine_dir / "include/constants/flags.h"
    wild_path = engine_dir / "src/wild_encounter.c"
    trainer_path = engine_dir / "src/trainer_util.c"
    flags_path.write_text(patch_flags(flags_path.read_text(encoding="utf-8")), encoding="utf-8")
    wild_path.write_text(patch_wild_encounter(wild_path.read_text(encoding="utf-8"), pool), encoding="utf-8")
    trainer_path.write_text(patch_trainer_util(trainer_path.read_text(encoding="utf-8"), pool), encoding="utf-8")
    return len(pool)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    count = integrate(args.engine_dir)
    print(f"Integrated runtime wild/trainer randomization with {count} eligible species")

if __name__ == "__main__":
    main()
