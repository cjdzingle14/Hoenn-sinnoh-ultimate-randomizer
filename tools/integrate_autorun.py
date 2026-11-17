"""Build-time overlay for always-on running and skipping Mom's Running Shoes scene."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def patch_auto_run_source(source: str) -> str:
    """Remove the B-button and Running Shoes flag gates from normal running."""
    pattern = re.compile(
        r"(?m)^([ \t]*)&& \(heldKeys & B_BUTTON\)\r?\n\1&& FlagGet\(FLAG_SYS_B_DASH\)\r?\n"
    )
    patched, count = pattern.subn("", source, count=1)
    if count != 1:
        raise ValueError("Could not uniquely locate the standard B-button running gate")
    return patched


def patch_littleroot_script(source: str) -> str:
    """Disable the post-Pokédex Mom/Running Shoes scene; auto-run replaces it."""
    transition_call = (
        "\tcall_if_eq VAR_LITTLEROOT_TOWN_STATE, 3, "
        "LittlerootTown_EventScript_SetMomStandingInFrontOfDoorPos"
    )
    if source.count(transition_call) != 1:
        raise ValueError("Could not uniquely locate Mom's post-Pokédex map transition")

    patched = source.replace(
        transition_call,
        "\t@ Auto-run is enabled from the start; skip Mom's Running Shoes scene.",
        1,
    )

    start_marker = "LittlerootTown_EventScript_GiveRunningShoesTrigger::"
    next_marker = "\nLittlerootTown_EventScript_SetHomeDoorCoordsMale::"
    if patched.count(start_marker) != 1 or patched.count(next_marker) != 1:
        raise ValueError("Could not uniquely locate Mom's Running Shoes event script")

    start = patched.index(start_marker)
    end = patched.index(next_marker, start)
    replacement = (
        start_marker
        + "\n\t@ Auto-run replaces this event; do not start Mom's Running Shoes scene.\n"
        + "\tend\n"
    )
    return patched[:start] + replacement + patched[end + 1 :]


def integrate(engine_dir: Path) -> None:
    movement_path = engine_dir / "src" / "field_player_avatar.c"
    littleroot_path = engine_dir / "data" / "maps" / "LittlerootTown" / "scripts.inc"

    movement = movement_path.read_text(encoding="utf-8")
    littleroot = littleroot_path.read_text(encoding="utf-8")

    movement_path.write_text(patch_auto_run_source(movement), encoding="utf-8")
    littleroot_path.write_text(patch_littleroot_script(littleroot), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    integrate(args.engine_dir)
    print("Enabled auto-run from the start and disabled Mom's Running Shoes scene")


if __name__ == "__main__":
    main()
