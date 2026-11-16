"""Build-time overlay that unlocks the engine's National Pokédex from a new game."""
from __future__ import annotations

import argparse
from pathlib import Path


def patch_pokedex_source(source: str) -> str:
    """Keep the National Dex enabled after the new-game Pokédex reset."""
    anchor = "    DisableNationalPokedex();"
    if source.count(anchor) != 1:
        raise ValueError("Could not uniquely locate ResetPokedex National Dex reset")
    return source.replace(
        anchor,
        anchor + "\n    // This adventure spans multiple regions: use the full National Dex from the start.\n"
        "    EnableNationalPokedex();",
        1,
    )


def integrate(engine_dir: Path) -> None:
    source_path = engine_dir / "src" / "pokedex.c"
    source_path.write_text(
        patch_pokedex_source(source_path.read_text(encoding="utf-8")),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    integrate(args.engine_dir)
    print("Enabled National Pokédex from the start of a new game")


if __name__ == "__main__":
    main()
