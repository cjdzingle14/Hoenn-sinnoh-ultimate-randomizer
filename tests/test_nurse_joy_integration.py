from tools.integrate_nurse_joy import patch_rs_nurse, patch_frlg_nurse


RS_SOURCE = """Common_EventScript_PkmnCenterNurse::
\tlock
\tfaceplayer
\tmsgbox gText_WouldYouLikeToRestYourPkmn, MSGBOX_YESNO
\tgoto EventScript_PkmnCenterNurse_HealPkmn

EventScript_PkmnCenterNurse_Goodbye::
\tmessage gText_WeHopeToSeeYouAgain
\treturn

EventScript_PkmnCenterNurse_HealPkmn::
\tincrementgamestat GAME_STAT_USED_POKECENTER
\tcall EventScript_PkmnCenterNurse_IllTakeYourPkmn
\twaitmessage
\tcall EventScript_PkmnCenterNurse_TakeAndHealPkmn
\tgoto EventScript_PkmnCenterNurse_CheckPokerus

EventScript_PkmnCenterNurse_IllTakeYourPkmn::
\tmessage gText_IllTakeYourPkmn
\treturn

EventScript_PkmnCenterNurse_ReturnPkmn::
\tmessage gText_RestoredPkmnToFullHealth
\twaitmessage
\tapplymovement VAR_0x800B, Movement_PkmnCenterNurse_Bow
\treturn

EventScript_PkmnCenterNurse_ReturnPkmn2::
\tmessage gText_ThankYouForWaiting
"""


FRLG_SOURCE = """EventScript_PkmnCenterNurse_Frlg::
\tmessage Text_WelcomeWantToHealPkmn_Frlg
\tmultichoice 19, 8, MULTI_YESNO, FALSE
\tcase 0, EventScript_PkmnCenterNurse_HealPkmn_Frlg
\tend

EventScript_PkmnCenterNurse_HealPkmn_Frlg::
\tincrementgamestat GAME_STAT_USED_POKECENTER
\tmessage Text_TakeYourPkmnForFewSeconds_Frlg
\twaitmessage
\tcall EventScript_PkmnCenterNurse_TakeAndHealPkmn_Frlg
\tgoto EventScript_PkmnCenterNurse_CheckTrainerTowerAndUnionRoom_Frlg

EventScript_PkmnCenterNurse_TakeAndHealPkmn_Frlg::
\tdofieldeffect FLDEFF_POKECENTER_HEAL
\twaitfieldeffect FLDEFF_POKECENTER_HEAL
\tspecial HealPlayerParty
\treturn

EventScript_PkmnCenterNurse_ReturnPkmn_Frlg::
\tmessage Text_RestoredPkmnToFullHealth_Frlg
\twaitmessage
\tapplymovement VAR_LAST_TALKED, Movement_Bow
\treturn

EventScript_PkmnCenterNurse_PlayerWaitingInUnionRoom_Frlg::
\tmsgbox Text_RestoredPkmnToFullHealth_Frlg
"""


def test_rs_heals_immediately_and_only_speaks_afterward():
    patched = patch_rs_nurse(RS_SOURCE)
    opening = patched.split("EventScript_PkmnCenterNurse_Goodbye::", 1)[0]
    healing = patched.split("EventScript_PkmnCenterNurse_HealPkmn::", 1)[1].split(
        "EventScript_PkmnCenterNurse_IllTakeYourPkmn::", 1
    )[0]
    confirmation = patched.split("EventScript_PkmnCenterNurse_ReturnPkmn::", 1)[1].split(
        "EventScript_PkmnCenterNurse_ReturnPkmn2::", 1
    )[0]
    assert "msgbox" not in opening and "multichoice" not in opening
    assert "call EventScript_PkmnCenterNurse_TakeAndHealPkmn" in healing
    assert "IllTakeYourPkmn" not in healing
    assert "goto EventScript_PkmnCenterNurse_ReturnPkmn" in healing
    assert "gText_RestoredPkmnToFullHealth" in confirmation
    assert "WeHopeToSeeYouAgain" not in confirmation


def test_frlg_heals_immediately_and_only_speaks_afterward():
    patched = patch_frlg_nurse(FRLG_SOURCE)
    opening = patched.split("EventScript_PkmnCenterNurse_HealPkmn_Frlg::", 1)[0]
    healing = patched.split("EventScript_PkmnCenterNurse_HealPkmn_Frlg::", 1)[1].split(
        "EventScript_PkmnCenterNurse_TakeAndHealPkmn_Frlg::", 1
    )[0]
    confirmation = patched.split("EventScript_PkmnCenterNurse_ReturnPkmn_Frlg::", 1)[1].split(
        "EventScript_PkmnCenterNurse_PlayerWaitingInUnionRoom_Frlg::", 1
    )[0]
    assert "Text_WelcomeWantToHealPkmn_Frlg" not in opening
    assert "multichoice" not in opening
    assert "Text_TakeYourPkmnForFewSeconds_Frlg" not in healing
    assert "call EventScript_PkmnCenterNurse_TakeAndHealPkmn_Frlg" in healing
    assert "Text_RestoredPkmnToFullHealth_Frlg" in confirmation
    assert "WeHopeToSeeYouAgain" not in confirmation
