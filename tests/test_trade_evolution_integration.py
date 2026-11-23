import pytest

from tools.integrate_trade_evolutions import patch_trade_evolutions


EVOLUTION_FIXTURE = """            case EVO_LEVEL_BATTLE_ONLY:
                if (mode == EVO_MODE_BATTLE_ONLY && evolutions[i].param <= level)
                    conditionsMet = TRUE;
                break;

        case IF_TRADE_PARTNER_SPECIES:
            if (params[i].arg1 == partnerSpecies && partnerHoldEffect != HOLD_EFFECT_PREVENT_EVOLVE)
                currentCondition = TRUE;
            break;
"""


def test_trade_evolutions_trigger_on_level_up_at_level_37():
    patched = patch_trade_evolutions(EVOLUTION_FIXTURE)
    assert "case EVO_TRADE:" in patched
    assert "if (level >= 37)" in patched


def test_trade_partner_species_requirement_is_removed_for_solo_play():
    patched = patch_trade_evolutions(EVOLUTION_FIXTURE)
    assert "tradePartner == NULL" in patched
    assert "partnerHoldEffect != HOLD_EFFECT_PREVENT_EVOLVE" in patched


def test_patch_is_idempotent():
    patched = patch_trade_evolutions(EVOLUTION_FIXTURE)
    assert patch_trade_evolutions(patched) == patched


def test_patch_fails_closed_when_upstream_source_changes():
    with pytest.raises(ValueError):
        patch_trade_evolutions("unrecognized evolution code")
