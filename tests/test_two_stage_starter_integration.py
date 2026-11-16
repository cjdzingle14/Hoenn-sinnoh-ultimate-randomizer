import unittest

from tools.integrate_two_stage_starters import (
    patch_battle_setup_source,
    patch_lab_script,
    patch_specials_source,
    patch_starter_source,
    patch_vars_header,
)


class TwoStageStarterIntegrationTests(unittest.TestCase):
    def test_save_vars_replace_four_consecutive_unused_slots(self):
        source = "\n".join(
            f"#define VAR_UNUSED_0x{address:04X}                                0x{address:04X} // Unused Var"
            for address in range(0x40F7, 0x40FB)
        )
        patched = patch_vars_header(source)
        self.assertIn("VAR_TEST5_FIRST_STARTER_1", patched)
        self.assertIn("VAR_TEST5_FIRST_STARTER_3", patched)
        self.assertIn("VAR_TEST5_STARTER_STAGE", patched)

    def test_lab_offer_uses_second_starter_special_before_progression_advances(self):
        source = "call RivalGift\n\tsetvar VAR_BIRCH_LAB_STATE, 5\n"
        patched = patch_lab_script(source)
        self.assertLess(patched.index("special ChooseSecondStarter"), patched.index("setvar VAR_BIRCH_LAB_STATE, 5"))
        self.assertNotIn("special ChooseStarter", patched)

    def test_source_persists_first_trio_and_excludes_it_from_second(self):
        source = '''
#include "main.h"
#include "event_data.h"
static u16 sStarterMon[STARTER_MON_COUNT];
static const u16 sStarterPool[] = { SPECIES_A, SPECIES_B, SPECIES_C, SPECIES_D };
static void RandomizeStarterChoices(void)
{
    u8 i;
    for (i = 0; i < STARTER_MON_COUNT; i++) { sStarterMon[i] = 0; }
}
static u16 sStarterLabelWindowId;
static void Task_StarterChoose(u8 taskId)
{
    AddTextPrinterParameterized(0, FONT_NORMAL, gText_BirchInTrouble, 0, 1, 0, NULL);
}
static void Task_HandleConfirmStarterInput(u8 taskId)
{
    switch (Menu_ProcessInputNoWrapClearOnChoose())
    {
    case 0:
        gSpecialVar_Result = gTasks[taskId].tStarterSelection;
        break;
    }
}
'''
        patched = patch_starter_source(source)
        self.assertIn("VarSet(VAR_TEST5_FIRST_STARTER_1, sStarterMon[0])", patched)
        self.assertIn("candidate == firstOffer[j]", patched)
        self.assertIn("VarSet(VAR_TEST5_STARTER_STAGE, 2)", patched)
        self.assertIn("sText_SecondStarterPrompt", patched)

    def test_second_callback_grants_without_restarting_tutorial_battle(self):
        source = """
static void CB2_GiveStarter(void);
static void CB2_StartFirstBattle(void)
{
}
void ChooseStarter(void)
{
    SetMainCallback2(CB2_ChooseStarter);
    gMain.savedCallback = CB2_GiveStarter;
}
static void CB2_GiveStarter(void)
{
    ScriptGiveMon(starterMon, 5, ITEM_NONE);
    SetMainCallback2(CB2_StartFirstBattle);
}
"""
        patched = patch_battle_setup_source(source)
        self.assertIn("void ChooseSecondStarter(void)", patched)
        self.assertIn("ScriptGiveMon(starterMon, 5, ITEM_NONE)", patched)
        self.assertIn("CB2_ReturnToFieldContinueScriptPlayMapMusic", patched)
        self.assertEqual(patched.count("SetMainCallback2(CB2_StartFirstBattle);"), 1)

    def test_second_special_is_registered(self):
        patched = patch_specials_source("def_special ChooseStarter, waitstate=1\n")
        self.assertIn("def_special ChooseSecondStarter, waitstate=1", patched)

    def test_rejects_missing_progression_anchor(self):
        with self.assertRaises(ValueError):
            patch_lab_script("no matching lab state transition")


if __name__ == "__main__":
    unittest.main()
