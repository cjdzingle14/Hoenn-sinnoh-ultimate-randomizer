from tools.integrate_tm_hm import NEW, OLD, patch_party_menu


def test_tms_are_not_removed_after_learning():
    source = "        if (!GetItemImportance(item))\n            RemoveBagItem(item, 1);"
    patched = patch_party_menu(source)
    assert OLD not in patched
    assert NEW in patched
    assert "GetItemTMHMIndex(item) > NUM_TECHNICAL_MACHINES" in patched


def test_patch_is_idempotent():
    assert patch_party_menu(NEW) == NEW


def test_patch_fails_if_engine_source_changed():
    import pytest
    with pytest.raises(ValueError, match="exactly one"):
        patch_party_menu("void unrelated(void) {}")
