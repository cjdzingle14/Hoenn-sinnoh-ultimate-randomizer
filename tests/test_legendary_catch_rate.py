from tools.integrate_legendary_catch_rate import patch_legendary_catch_rate


def test_special_species_receive_230_catch_rate():
    source = """static u32 GetBattleMonCatchRate(struct BattlePokemon *battleMon)
{
    enum Species species = battleMon->species;
    return gSpeciesInfo[species].catchRate;
}"""
    patched = patch_legendary_catch_rate(source)
    assert "isRestrictedLegendary" in patched
    assert "isSubLegendary" in patched
    assert "isMythical" in patched
    assert "isUltraBeast" in patched
    assert "return 230;" in patched
    assert "return gSpeciesInfo[species].catchRate;" in patched


def test_patch_is_idempotent():
    source = """static u32 GetBattleMonCatchRate(struct BattlePokemon *battleMon)
{
    enum Species species = battleMon->species;
    return gSpeciesInfo[species].catchRate;
}"""
    once = patch_legendary_catch_rate(source)
    assert patch_legendary_catch_rate(once) == once


def test_patch_fails_closed_when_source_changes():
    import pytest
    with pytest.raises(ValueError):
        patch_legendary_catch_rate("static u32 GetBattleMonCatchRate(void) { return 1; }")
