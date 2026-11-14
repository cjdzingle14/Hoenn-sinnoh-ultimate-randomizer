"""Build-time overlay making technical machines reusable without changing other item use."""
from __future__ import annotations

import argparse
from pathlib import Path

OLD = """        if (!GetItemImportance(item))
            RemoveBagItem(item, 1);"""
NEW = """        // TMs and HMs are reusable; keep both items in the bag after teaching."""


def patch_party_menu(source: str) -> str:
    if NEW in source:
        return source
    count = source.count(OLD)
    if count != 1:
        raise ValueError(f"Expected exactly one TM/HM consumption check, found {count}")
    source = source.replace(OLD, NEW, 1)
    declaration = "    enum Item item = gSpecialVar_ItemId;\\n\\n    if (gPartyMenu.learnMoveState == 0)"
    if source.count(declaration) != 1:
        raise ValueError("Expected exactly one TM/HM item local in Task_LearnedMove")
    return source.replace(declaration, "    if (gPartyMenu.learnMoveState == 0)", 1)


def integrate(engine_dir: Path) -> None:
    path = engine_dir / "src" / "party_menu.c"
    original = path.read_text(encoding="utf-8")
    path.write_text(patch_party_menu(original), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    integrate(args.engine_dir)
    print("Integrated reusable Technical Machines")


if __name__ == "__main__":
    main()
