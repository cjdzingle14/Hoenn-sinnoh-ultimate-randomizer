from tools.integrate_hm_field import (
    FIELD_NEW, FIELD_OLD, PARTY_NEW, PARTY_OLD,
    patch_field_move, patch_party_menu,
)


def test_hm_unlock_requires_inventory_and_original_badge_gate():
    source = '#include "global.h"\n' + FIELD_OLD + '\n.isUnlockedFunc = HasBadgeForFieldMove,'
    patched = patch_field_move(source)
    assert FIELD_OLD not in patched
    assert FIELD_NEW in patched
    assert "CheckBagHasItem(item, 1)" in patched
    assert "FlagGet(gFieldMoveInfo[fieldMove].arg + FLAG_BADGE01_GET)" in patched
    assert "HasBadgeForFieldMove" not in patched


def test_party_actions_allow_hm_without_known_move():
    source = '#include "constants/field_move.h"\n' + PARTY_OLD + '\n}'
    patched = patch_party_menu(source)
    assert PARTY_OLD not in patched
    assert PARTY_NEW in patched
    assert "CheckBagHasItem(hmItem, 1)" in patched
    assert "IsFieldMoveUnlocked(j)" in patched
    assert "knowsMove ||" not in patched


def test_patch_rejects_unrecognized_engine_source():
    import pytest
    with pytest.raises(ValueError):
        patch_field_move("unrecognized source")
    with pytest.raises(ValueError):
        patch_party_menu("unrecognized source")


def test_all_eight_hms_map_to_their_matching_items():
    expected = [
        "FIELD_MOVE_CUT: return ITEM_HM_CUT",
        "FIELD_MOVE_FLY: return ITEM_HM_FLY",
        "FIELD_MOVE_SURF: return ITEM_HM_SURF",
        "FIELD_MOVE_STRENGTH: return ITEM_HM_STRENGTH",
        "FIELD_MOVE_FLASH: return ITEM_HM_FLASH",
        "FIELD_MOVE_ROCK_SMASH: return ITEM_HM_ROCK_SMASH",
        "FIELD_MOVE_WATERFALL: return ITEM_HM_WATERFALL",
        "FIELD_MOVE_DIVE: return ITEM_HM_DIVE",
    ]
    for mapping in expected:
        assert mapping in FIELD_NEW
        assert mapping in PARTY_NEW
