"""Build-time overlay for fresh, distinct starter choices on every new game."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

BANNED_STARTERS = set("""
ARTICUNO ZAPDOS MOLTRES MEWTWO MEW RAIKOU ENTEI SUICUNE LUGIA HO_OH CELEBI
REGIROCK REGICE REGISTEEL LATIAS LATIOS KYOGRE GROUDON RAYQUAZA JIRACHI DEOXYS
UXIE MESPRIT AZELF DIALGA PALKIA GIRATINA HEATRAN REGIGIGAS CRESSELIA PHIONE MANAPHY DARKRAI SHAYMIN ARCEUS
VICTINI COBALION TERRAKION VIRIZION TORNADUS THUNDURUS RESHIRAM ZEKROM LANDORUS KYUREM KELDEO MELOETTA GENESECT
XERNEAS YVELTAL ZYGARDE DIANCIE HOOPA VOLCANION TAPU_KOKO TAPU_LELE TAPU_BULU TAPU_FINI
COSMOG COSMOEM SOLGALEO LUNALA NECROZMA MAGEARNA MARSHADOW POIPOLE NAGANADEL STAKATAKA BLACEPHALON ZERAORA MELTAN MELMETAL
ZACIAN ZAMAZENTA ETERNATUS KUBFU URSHIFU ZARUDE REGIELEKI REGIDRAGO GLASTRIER SPECTRIER CALYREX ENAMORUS
WO_CHIEN CHIEN_PAO TING_LU CHI_YU KORAIDON MIRAIDON OKIDOGI MUNKIDORI FEZANDIPITI OGERPON TERAPAGOS PECHARUNT
""".split())


def parse_species_constants(species_header: str) -> list[str]:
    """Return base National Dex species, excluding legendary/mythical Pokémon and forms."""
    candidates = []
    for name, value in re.findall(
        r"^\s*SPECIES_([A-Z0-9_]+)\s*=\s*(\d+)\s*,",
        species_header,
        flags=re.MULTILINE,
    ):
        dex_number = int(value)
        if 1 <= dex_number <= 1025 and name not in BANNED_STARTERS:
            candidates.append((dex_number, "SPECIES_" + name))
    unique = {}
    for dex_number, constant in candidates:
        unique.setdefault(dex_number, constant)
    if len(unique) < 3:
        raise ValueError("Pinned species enum has fewer than three eligible starters")
    return list(unique.values())


def patch_starter_source(source: str, eligible_species: list[str]) -> str:
    """Replace the fixed trio with a runtime-randomized, no-duplicate species pool."""
    if len(eligible_species) < 3 or len(set(eligible_species)) != len(eligible_species):
        raise ValueError("starter pool must contain at least three distinct species")
    if '#include "random.h"' not in source:
        source = source.replace(
            '#include "main.h"',
            '#include "main.h"\n#include "random.h"',
            1,
        )
    replacement = (
        "static const u16 sStarterPool[] =\n{\n"
        + "".join(f"    {species},\n" for species in eligible_species)
        + "};\n\n"
        "static u16 sStarterMon[STARTER_MON_COUNT];\n\n"
        "static void RandomizeStarterChoices(void)\n"
        "{\n"
        "    u8 i;\n"
        "    for (i = 0; i < STARTER_MON_COUNT; i++)\n"
        "    {\n"
        "        u16 candidate;\n"
        "        bool8 duplicate;\n"
        "        do\n"
        "        {\n"
        "            u8 j;\n"
        "            candidate = sStarterPool[Random() % ARRAY_COUNT(sStarterPool)];\n"
        "            duplicate = FALSE;\n"
        "            for (j = 0; j < i; j++)\n"
        "            {\n"
        "                if (sStarterMon[j] == candidate)\n"
        "                    duplicate = TRUE;\n"
        "            }\n"
        "        } while (duplicate);\n"
        "        sStarterMon[i] = candidate;\n"
        "    }\n"
        "}\n"
    )
    pattern = re.compile(
        r"static const u16 sStarterMon\[STARTER_MON_COUNT\]\s*=\s*\{.*?\};",
        flags=re.DOTALL,
    )
    patched, count = pattern.subn(replacement, source, count=1)
    if count != 1:
        raise ValueError("Could not locate expected sStarterMon array")
    patched = patched.replace(
        "if (chosenStarterId > STARTER_MON_COUNT)",
        "if (chosenStarterId >= STARTER_MON_COUNT)",
    )
    call_anchor = "void CB2_ChooseStarter(void)\n{"
    if call_anchor not in patched:
        raise ValueError("Could not locate CB2_ChooseStarter")
    patched = patched.replace(
        call_anchor,
        call_anchor + "\n    // Generate one fresh trio when a new game enters starter selection.\n"
        "    RandomizeStarterChoices();",
        1,
    )
    return patched


def integrate(engine_dir: Path, seed: str | None = None) -> list[str]:
    """Apply runtime starter randomization; seed remains for CLI compatibility."""
    source_path = engine_dir / "src" / "starter_choose.c"
    species_path = engine_dir / "include" / "constants" / "species.h"
    source = source_path.read_text(encoding="utf-8")
    header = species_path.read_text(encoding="utf-8")
    pool = parse_species_constants(header)
    source_path.write_text(patch_starter_source(source, pool), encoding="utf-8")
    return pool


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    parser.add_argument("--seed", default=None, help="Legacy option; choices now use the game's runtime RNG")
    args = parser.parse_args()
    pool = integrate(args.engine_dir, args.seed)
    print(f"Integrated per-new-game starter randomization ({len(pool)} eligible species)")


if __name__ == "__main__":
    main()
