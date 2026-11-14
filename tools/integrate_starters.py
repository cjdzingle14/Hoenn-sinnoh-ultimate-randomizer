"""Build-time overlay for deterministic starter selection in the pinned engine."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from tools.game_rules import choose_starters

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
        species_header, flags=re.MULTILINE
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

def patch_starter_source(source: str, starters: list[str]) -> str:
    if len(starters) != 3 or len(set(starters)) != 3:
        raise ValueError("exactly three distinct starter constants are required")
    replacement = (
        "static const u16 sStarterMon[STARTER_MON_COUNT] =\n{\n"
        + "".join(f"    {species},\n" for species in starters)
        + "};"
    )
    pattern = re.compile(
        r"static const u16 sStarterMon\[STARTER_MON_COUNT\]\s*=\s*\{.*?\};",
        flags=re.DOTALL
    )
    patched, count = pattern.subn(replacement, source, count=1)
    if count != 1:
        raise ValueError("Could not locate expected sStarterMon array")
    return patched.replace(
        "if (chosenStarterId > STARTER_MON_COUNT)",
        "if (chosenStarterId >= STARTER_MON_COUNT)"
    )

def integrate(engine_dir: Path, seed: str) -> list[str]:
    source_path = engine_dir / "src" / "starter_choose.c"
    species_path = engine_dir / "include" / "constants" / "species.h"
    source = source_path.read_text(encoding="utf-8")
    header = species_path.read_text(encoding="utf-8")
    starters = choose_starters(parse_species_constants(header), seed=seed)
    source_path.write_text(patch_starter_source(source, starters), encoding="utf-8")
    return starters

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    parser.add_argument("--seed", default=None)
    args = parser.parse_args()
    if args.seed is None:
        settings = json.loads(Path("config/randomizer.json").read_text(encoding="utf-8"))
        args.seed = settings["seed"]
    starters = integrate(args.engine_dir, args.seed)
    print(f"Integrated starters (seed={args.seed}): {', '.join(starters)}")

if __name__ == "__main__":
    main()
