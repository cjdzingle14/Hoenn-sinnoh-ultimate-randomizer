"""Build-time overlay that enables National mode after new-game event data initialization."""
from __future__ import annotations

import argparse
from pathlib import Path


def patch_new_game_source(source: str) -> str:
    """Enable National Dex only after InitEventData has cleared old flags and vars."""
    anchor = "    InitEventData();"
    if source.count(anchor) != 1:
        raise ValueError("Could not uniquely locate new-game InitEventData call")
    return source.replace(
        anchor,
        anchor
        + "\n    // Enable after InitEventData: it resets the National Dex flag and variable.\n"
        + "    EnableNationalPokedex();",
        1,
    )


def integrate(engine_dir: Path) -> None:
    source_path = engine_dir / "src" / "new_game.c"
    source_path.write_text(
        patch_new_game_source(source_path.read_text(encoding="utf-8")),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    integrate(args.engine_dir)
    print("Enabled National Pokédex after new-game event data initialization")


if __name__ == "__main__":
    main()
