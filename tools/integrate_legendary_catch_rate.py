"""Set legendary, mythical, and Ultra Beast catch odds to a 30% baseline."""
from __future__ import annotations

import argparse
from pathlib import Path


def patch_legendary_catch_rate(source: str) -> str:
    """Use catch-rate 230 for special species (about 30% at full HP, Poké Ball)."""
    old = """    return gSpeciesInfo[species].catchRate;
}"""
    new = """    // Special encounters get an approachable baseline: about 30% with a
    // standard Poké Ball at full HP. Ball type, HP, status, and other normal
    // catch modifiers continue to apply.
    if (gSpeciesInfo[species].isRestrictedLegendary
        || gSpeciesInfo[species].isSubLegendary
        || gSpeciesInfo[species].isMythical
        || gSpeciesInfo[species].isUltraBeast)
        return 230;

    return gSpeciesInfo[species].catchRate;
}"""
    if new in source:
        return source
    if source.count(old) != 1:
        raise ValueError("Could not uniquely locate GetBattleMonCatchRate return")
    return source.replace(old, new, 1)


def integrate(engine_dir: Path) -> None:
    path = engine_dir / "src" / "battle_script_commands.c"
    source = path.read_text(encoding="utf-8")
    path.write_text(patch_legendary_catch_rate(source), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    integrate(args.engine_dir)
    print("Integrated 30% baseline catch rate for legendary-class encounters")


if __name__ == "__main__":
    main()
