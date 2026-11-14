from tools.integrate_hm_field import (
    FIELD_NEW, FIELD_OLD, PARTY_NEW, PARTY_OLD,
    patch_field_move, patch_party_menu,
)


def test_hm_unlock_uses_inventory_not_badges():
    source = '#include "global.h"\n' + FIELD_OLD + '\n.isUnlockedFunc = HasBadgeForFieldMove,'
    patched = patch_field_move(source)
    assert FIELD_OLD not in patched
    assert FIELD_NEW in patched
    assert "CheckBagHasItem(item, 1)" in patched
    assert "HasBadgeForFieldMove" not in patched


def test_party_actions_allow_hm_without_known_move():
    source = '#include "constants/field_move.h"\n' + PARTY_OLD + '\n}'
    patched = patch_party_menu(source)
    assert PARTY_OLD not in patched
    assert PARTY_NEW in patched
    assert "CheckBagHasItem(hmItem, 1)" in patched
    assert "knowsMove ||" in patched


def test_patch_rejects_unrecognized_engine_source():
    import pytest
    with pytest.raises(ValueError):
        patch_field_move("unrecognized source")
    with pytest.raises(ValueError):
        patch_party_menu("unrecognized source")
