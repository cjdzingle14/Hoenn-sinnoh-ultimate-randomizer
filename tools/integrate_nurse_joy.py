"""Apply the streamlined Nurse Joy flow to both RS and FRLG engine scripts."""
from __future__ import annotations

import argparse
from pathlib import Path


def _replace_section(source: str, start: str, end: str, replacement: str) -> str:
    a = source.find(start)
    if a < 0:
        raise ValueError(f"Missing script label: {start}")
    b = source.find(end, a + len(start))
    if b < 0:
        raise ValueError(f"Missing following script label: {end}")
    return source[:a] + replacement + source[b:]


def patch_rs_nurse(source: str) -> str:
    source = _replace_section(
        source,
        "Common_EventScript_PkmnCenterNurse::",
        "EventScript_PkmnCenterNurse_Goodbye::",
        """Common_EventScript_PkmnCenterNurse::
\tlock
\tfaceplayer
\tsetvar VAR_0x8004, 0
\tgoto EventScript_PkmnCenterNurse_HealPkmn
\tend

""",
    )
    source = _replace_section(
        source,
        "EventScript_PkmnCenterNurse_HealPkmn::",
        "EventScript_PkmnCenterNurse_IllTakeYourPkmn::",
        """EventScript_PkmnCenterNurse_HealPkmn::
\tincrementgamestat GAME_STAT_USED_POKECENTER
\tcall EventScript_PkmnCenterNurse_TakeAndHealPkmn
\tgoto EventScript_PkmnCenterNurse_ReturnPkmn
\tend

""",
    )
    source = _replace_section(
        source,
        "EventScript_PkmnCenterNurse_ReturnPkmn::",
        "EventScript_PkmnCenterNurse_ReturnPkmn2::",
        """EventScript_PkmnCenterNurse_ReturnPkmn::
\tmessage gText_RestoredPkmnToFullHealth
\twaitmessage
\treturn

""",
    )
    return source


def patch_frlg_nurse(source: str) -> str:
    source = _replace_section(
        source,
        "EventScript_PkmnCenterNurse_Frlg::",
        "EventScript_PkmnCenterNurse_HealPkmn_Frlg::",
        """EventScript_PkmnCenterNurse_Frlg::
\tlock
\tcall EventScript_PkmnCenterNurse_HealPkmn_Frlg
\treturn

""",
    )
    source = _replace_section(
        source,
        "EventScript_PkmnCenterNurse_HealPkmn_Frlg::",
        "EventScript_PkmnCenterNurse_TakeAndHealPkmn_Frlg::",
        """EventScript_PkmnCenterNurse_HealPkmn_Frlg::
\tincrementgamestat GAME_STAT_USED_POKECENTER
\tcall EventScript_PkmnCenterNurse_TakeAndHealPkmn_Frlg
\tgoto EventScript_PkmnCenterNurse_ReturnPkmn_Frlg
\tend

""",
    )
    source = _replace_section(
        source,
        "EventScript_PkmnCenterNurse_ReturnPkmn_Frlg::",
        "EventScript_PkmnCenterNurse_PlayerWaitingInUnionRoom_Frlg::",
        """EventScript_PkmnCenterNurse_ReturnPkmn_Frlg::
\tmessage Text_RestoredPkmnToFullHealth_Frlg
\twaitmessage
\treturn

""",
    )
    return source


def integrate(engine_dir: Path) -> tuple[Path, Path]:
    rs_path = engine_dir / "data/scripts/pkmn_center_nurse.inc"
    frlg_path = engine_dir / "data/scripts/pkmn_center_nurse_frlg.inc"
    rs = rs_path.read_text(encoding="utf-8")
    frlg = frlg_path.read_text(encoding="utf-8")
    rs_path.write_text(patch_rs_nurse(rs), encoding="utf-8")
    frlg_path.write_text(patch_frlg_nurse(frlg), encoding="utf-8")
    return rs_path, frlg_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    for path in integrate(args.engine_dir):
        print(f"Applied streamlined Nurse Joy healing flow: {path}")


if __name__ == "__main__":
    main()
