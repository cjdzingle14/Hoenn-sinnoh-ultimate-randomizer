"""Build-time overlay unlocking HM field actions from HM ownership, not badges or party moves."""
from __future__ import annotations

import argparse
from pathlib import Path

FIELD_OLD = """static bool32 HasBadgeForFieldMove(enum FieldMove fieldMove)
{
    return FlagGet(gFieldMoveInfo[fieldMove].arg + FLAG_BADGE01_GET);
}"""
FIELD_NEW = """static enum Item GetHMItemForFieldMove(enum FieldMove fieldMove)
{
    switch (fieldMove)
    {
    case FIELD_MOVE_CUT: return ITEM_HM_CUT;
    case FIELD_MOVE_FLY: return ITEM_HM_FLY;
    case FIELD_MOVE_SURF: return ITEM_HM_SURF;
    case FIELD_MOVE_STRENGTH: return ITEM_HM_STRENGTH;
    case FIELD_MOVE_FLASH: return ITEM_TM_FLASH;
    case FIELD_MOVE_ROCK_SMASH: return ITEM_HM_ROCK_SMASH;
    case FIELD_MOVE_WATERFALL: return ITEM_HM_WATERFALL;
    case FIELD_MOVE_DIVE: return ITEM_HM_DIVE;
    default: return ITEM_NONE;
    }
}

static bool32 HasHMItemForFieldMove(enum FieldMove fieldMove)
{
    enum Item item = GetHMItemForFieldMove(fieldMove);
    return item != ITEM_NONE && CheckBagHasItem(item, 1);
}"""

PARTY_OLD = """static void SetPartyMonFieldSelectionActions(struct Pokemon *mons, u8 slotId)
{
    u8 i, j;

    sPartyMenuInternal->numActions = 0;
    AppendToList(sPartyMenuInternal->actions, &sPartyMenuInternal->numActions, MENU_SUMMARY);

    // Add field moves to action list
    for (i = 0; i < MAX_MON_MOVES; i++)
    {
        for (j = 0; j != FIELD_MOVES_COUNT; j++)
        {
            if (!FieldMove_IsVisible(j))
                continue;

            if (GetMonData(&mons[slotId], i + MON_DATA_MOVE1) == FieldMove_GetMoveId(j))
            {
                AppendToList(sPartyMenuInternal->actions, &sPartyMenuInternal->numActions, j + MENU_FIELD_MOVES);
                break;
            }
        }
    }

    if (!InBattlePike())
    {"""
PARTY_NEW = """static enum Item GetHMItemForFieldMove(enum FieldMove fieldMove)
{
    switch (fieldMove)
    {
    case FIELD_MOVE_CUT: return ITEM_HM_CUT;
    case FIELD_MOVE_FLY: return ITEM_HM_FLY;
    case FIELD_MOVE_SURF: return ITEM_HM_SURF;
    case FIELD_MOVE_STRENGTH: return ITEM_HM_STRENGTH;
    case FIELD_MOVE_FLASH: return ITEM_TM_FLASH;
    case FIELD_MOVE_ROCK_SMASH: return ITEM_HM_ROCK_SMASH;
    case FIELD_MOVE_WATERFALL: return ITEM_HM_WATERFALL;
    case FIELD_MOVE_DIVE: return ITEM_HM_DIVE;
    default: return ITEM_NONE;
    }
}

static void SetPartyMonFieldSelectionActions(struct Pokemon *mons, u8 slotId)
{
    u8 i, j;

    sPartyMenuInternal->numActions = 0;
    AppendToList(sPartyMenuInternal->actions, &sPartyMenuInternal->numActions, MENU_SUMMARY);

    // Show an HM action on any selected Pokémon once its HM item is owned.
    for (j = 0; j != FIELD_MOVES_COUNT; j++)
    {
        bool8 knowsMove = FALSE;
        enum Item hmItem;
        if (!FieldMove_IsVisible(j))
            continue;
        for (i = 0; i < MAX_MON_MOVES; i++)
        {
            if (GetMonData(&mons[slotId], i + MON_DATA_MOVE1) == FieldMove_GetMoveId(j))
            {
                knowsMove = TRUE;
                break;
            }
        }
        hmItem = GetHMItemForFieldMove(j);
        if (knowsMove || (hmItem != ITEM_NONE && CheckBagHasItem(hmItem, 1)))
            AppendToList(sPartyMenuInternal->actions, &sPartyMenuInternal->numActions, j + MENU_FIELD_MOVES);
    }

    if (!InBattlePike())
    {"""

def patch_field_move(source: str) -> str:
    if FIELD_NEW in source:
        return source
    if source.count(FIELD_OLD) != 1:
        raise ValueError("Expected exactly one badge-based field-move unlock function")
    source = source.replace(FIELD_OLD, FIELD_NEW, 1)
    source = source.replace(".isUnlockedFunc = HasBadgeForFieldMove,", ".isUnlockedFunc = HasHMItemForFieldMove,")
    if '#include "item.h"' not in source:
        source = source.replace('#include "global.h"', '#include "global.h"\n#include "item.h"', 1)
    if '#include "constants/items.h"' not in source:
        source = source.replace('#include "constants/field_move.h"', '#include "constants/field_move.h"\n#include "constants/items.h"', 1)
    if "HasBadgeForFieldMove" in source:
        raise ValueError("Badge-based field-move unlock reference remains")
    return source


def patch_party_menu(source: str) -> str:
    if PARTY_NEW in source:
        return source
    if source.count(PARTY_OLD) != 1:
        raise ValueError("Expected exactly one party field-move action builder")
    source = source.replace(PARTY_OLD, PARTY_NEW, 1)
    if '#include "constants/items.h"' not in source:
        source = source.replace('#include "constants/field_move.h"', '#include "constants/field_move.h"\n#include "constants/items.h"', 1)
    return source


def integrate(engine_dir: Path) -> None:
    field_path = engine_dir / "src" / "field_move.c"
    party_path = engine_dir / "src" / "party_menu.c"
    field_path.write_text(patch_field_move(field_path.read_text(encoding="utf-8")), encoding="utf-8")
    party_path.write_text(patch_party_menu(party_path.read_text(encoding="utf-8")), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    integrate(args.engine_dir)
    print("Integrated HM-item field unlocks without party HM moves or badge gates")


if __name__ == "__main__":
    main()
