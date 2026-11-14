"""Build-time wild encounter and trainer party randomization overlays."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from tools.randomizer_core import rng_for

# Exclude legendary/mythical species from ordinary wild and trainer pools.
EXCLUDED = set("""
ARTICUNO ZAPDOS MOLTRES MEWTWO MEW RAIKOU ENTEI SUICUNE LUGIA HO_OH CELEBI
REGIROCK REGICE REGISTEEL LATIAS LATIOS KYOGRE GROUDON RAYQUAZA JIRACHI DEOXYS
UXIE MESPRIT AZELF DIALGA PALKIA GIRATINA HEATRAN REGIGIGAS CRESSELIA PHIONE MANAPHY DARKRAI SHAYMIN ARCEUS
VICTINI COBALION TERRAKION VIRIZION TORNADUS THUNDURUS RESHIRAM ZEKROM LANDORUS KYUREM KELDEO MELOETTA GENESECT
XERNEAS YVELTAL ZYGARDE DIANCIE HOOPA VOLCANION TAPU_KOKO TAPU_LELE TAPU_BULU TAPU_FINI
COSMOG COSMOEM SOLGALEO LUNALA NECROZMA MAGEARNA MARSHADOW POIPOLE NAGANADEL STAKATAKA BLACEPHALON ZERAORA MELTAN MELMETAL
ZACIAN ZAMAZENTA ETERNATUS KUBFU URSHIFU ZARUDE REGIELEKI REGIDRAGO GLASTRIER SPECTRIER CALYREX ENAMORUS
WO_CHIEN CHIEN_PAO TING_LU CHI_YU KORAIDON MIRAIDON OKIDOGI MUNKIDORI FEZANDIPITI OGERPON TERAPAGOS PECHARUNT
""".split())


def parse_species_constants(header: str) -> list[str]:
    found = {}
    for name, number in re.findall(r"^\s*SPECIES_([A-Z0-9_]+)\s*=\s*(\d+)\s*,", header, re.M):
        dex = int(number)
        if 1 <= dex <= 1025 and name not in EXCLUDED:
            found.setdefault(dex, "SPECIES_" + name)
    if len(found) < 10:
        raise ValueError("Could not build a sufficiently large base-species pool")
    return list(found.values())


def randomize_wild_data(data: dict, species: list[str], seed: str) -> int:
    changed = 0
    groups = data.get("wild_encounter_groups")
    if not isinstance(groups, list):
        raise ValueError("wild_encounter_groups missing from wild encounter JSON")
    for group in groups:
        for encounter in group.get("encounters", []):
            map_id = encounter.get("map", "unknown_map")
            for method, table in encounter.items():
                if not isinstance(table, dict) or not isinstance(table.get("mons"), list):
                    continue
                for slot, mon in enumerate(table["mons"]):
                    if not isinstance(mon, dict) or not isinstance(mon.get("species"), str):
                        continue
                    # Keep level ranges, encounter rates, slot weights, and map layout intact.
                    rng = rng_for(seed, f"wild:{map_id}:{method}:{slot}")
                    mon["species"] = species[rng.randrange(len(species))]
                    changed += 1
    if changed == 0:
        raise ValueError("No wild encounter slots were found; refusing to produce a no-op patch")
    return changed


def _species_line(line: str, names: set[str]) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith(("#", "/*", "*", "//")) or ":" in stripped:
        return None
    # Competitive syntax permits Nickname (Species) (M) @ Item.
    match = re.search(r"\((SPECIES_[A-Z0-9_]+|[^()]+)\)", stripped)
    candidate = match.group(1).strip() if match else stripped.split(" @ ", 1)[0].split(" (", 1)[0].strip()
    normalized = candidate.upper().replace(" ", "_").replace("-", "_").replace("'", "")
    if normalized.startswith("SPECIES_"):
        normalized = normalized[8:]
    if normalized in names:
        return candidate, normalized
    return None


def randomize_trainer_parties(source: str, species: list[str], seed: str) -> tuple[str, int]:
    names = {item.removeprefix("SPECIES_") for item in species}
    output = []
    current_trainer = "outside"
    slot = 0
    changed = 0
    for line in source.splitlines(keepends=True):
        header = re.match(r"^===\s*(.*?)\s*===", line)
        if header:
            current_trainer = header.group(1)
            slot = 0
            output.append(line)
            continue
        found = _species_line(line, names)
        if found:
            old, _ = found
            rng = rng_for(seed, f"trainer:{current_trainer}:{slot}")
            replacement = species[rng.randrange(len(species))]
            # Trainer-party preprocessor accepts SPECIES_* constants directly.
            newline = "\n" if line.endswith("\n") else ""
            output.append(replacement + newline)
            slot += 1
            changed += 1
        elif line.lstrip().startswith("- "):
            # Species-specific moves can become invalid after species replacement.
            # Let the engine assign level-up moves for the randomized species.
            continue
        else:
            output.append(line)
    if changed == 0:
        raise ValueError("No trainer Pokémon entries were recognized; refusing to produce a no-op patch")
    return "".join(output), changed


def increase_rival_pokeball_gift(script: str, amount: int = 10) -> tuple[str, int]:
    """Set both rival-name-specific early Poké Ball gifts to the requested amount."""
    lines = script.splitlines(keepends=True)
    patched = 0
    active = False
    for index, line in enumerate(lines):
        if line.startswith("LittlerootTown_ProfessorBirchsLab_EventScript_MayGivePokeBalls::") or line.startswith("LittlerootTown_ProfessorBirchsLab_EventScript_BrendanGivePokeBalls::"):
            active = True
            continue
        if active and line.lstrip().startswith("giveitem ITEM_POKE_BALL,"):
            ending = "\\n" if line.endswith("\\n") else ""
            indent = line[:len(line) - len(line.lstrip())]
            lines[index] = f"{indent}giveitem ITEM_POKE_BALL, {amount}{ending}"
            patched += 1
            active = False
        elif active and line.strip().endswith("::"):
            active = False
    if patched != 2:
        raise ValueError(f"Expected to patch both rival Poké Ball gift scripts; found {patched}")
    return "".join(lines), patched

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    parser.add_argument("--seed", default=None)
    args = parser.parse_args()
    settings = json.loads(Path("config/randomizer.json").read_text(encoding="utf-8"))
    seed = args.seed or settings["seed"]
    header = (args.engine_dir / "include/constants/species.h").read_text(encoding="utf-8")
    pool = parse_species_constants(header)

    wild_path = args.engine_dir / "src/data/wild_encounters.json"
    wild = json.loads(wild_path.read_text(encoding="utf-8"))
    wild_count = randomize_wild_data(wild, pool, seed)
    wild_path.write_text(json.dumps(wild, indent=2) + "\n", encoding="utf-8")

    trainer_path = args.engine_dir / "src/data/trainers.party"
    trainer_source = trainer_path.read_text(encoding="utf-8")
    trainer_result, trainer_count = randomize_trainer_parties(trainer_source, pool, seed)
    trainer_path.write_text(trainer_result, encoding="utf-8")

    rival_script_path = args.engine_dir / "data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc"
    rival_script = rival_script_path.read_text(encoding="utf-8")
    rival_script, rival_gifts = increase_rival_pokeball_gift(rival_script, 10)
    rival_script_path.write_text(rival_script, encoding="utf-8")
    print(f"Randomized {wild_count} wild slots and {trainer_count} trainer Pokémon; rival gifts: {rival_gifts} x 10 Poké Balls (seed={seed})")


if __name__ == "__main__":
    main()
