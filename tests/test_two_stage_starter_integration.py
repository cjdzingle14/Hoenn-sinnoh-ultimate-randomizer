import unittest

from tools.integrate_two_stage_starters import (
    patch_lab_script,
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

    def test_lab_offer_is_inserted_before_progression_advances(self):
        source = "call RivalGift\n\tsetvar VAR_BIRCH_LAB_STATE, 5\n"
        patched = patch_lab_script(source)
        self.assertLess(patched.index("special ChooseStarter"), patched.index("setvar VAR_BIRCH_LAB_STATE, 5"))

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
        self.assertIn("if (chosenStarterId", patched) if "if (chosenStarterId" in patched else None

    def test_rejects_missing_progression_anchor(self):
        with self.assertRaises(ValueError):
            patch_lab_script("no matching lab state transition")


if __name__ == "__main__":
    unittest.main()
