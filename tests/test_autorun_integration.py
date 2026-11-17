import unittest

from tools.integrate_autorun import patch_auto_run_source, patch_littleroot_script


class AutoRunIntegrationTests(unittest.TestCase):
    def test_auto_run_does_not_require_b_button_or_running_shoes_flag(self):
        source = """if (!(gPlayerAvatar.flags & PLAYER_AVATAR_FLAG_UNDERWATER)
     && (heldKeys & B_BUTTON)
     && FlagGet(FLAG_SYS_B_DASH)
     && IsRunningDisallowed(behavior) == 0)
    {
        PlayerRun(direction);
    }
"""
        patched = patch_auto_run_source(source)
        self.assertNotIn("heldKeys & B_BUTTON", patched)
        self.assertNotIn("FLAG_SYS_B_DASH", patched)
        self.assertIn("IsRunningDisallowed(behavior) == 0", patched)
        self.assertIn("PlayerRun(direction);", patched)

    def test_auto_run_patch_rejects_missing_or_ambiguous_gate(self):
        with self.assertRaises(ValueError):
            patch_auto_run_source("if (TRUE) { PlayerRun(direction); }")
        source = "&& (heldKeys & B_BUTTON)\n&& FlagGet(FLAG_SYS_B_DASH)\n" * 2
        with self.assertRaises(ValueError):
            patch_auto_run_source(source)

    def test_mom_running_shoes_scene_is_disabled_after_pokedex(self):
        source = """LittlerootTown_OnTransition:
\tcall_if_eq VAR_LITTLEROOT_TOWN_STATE, 3, LittlerootTown_EventScript_SetMomStandingInFrontOfDoorPos
\tend

LittlerootTown_EventScript_GiveRunningShoesTrigger::
\tmsgbox LittlerootTown_Text_WaitPlayer, MSGBOX_DEFAULT
\tcall LittlerootTown_EventScript_GiveRunningShoes
\tend

LittlerootTown_EventScript_SetHomeDoorCoordsMale::
\treturn
"""
        patched = patch_littleroot_script(source)
        self.assertNotIn("call_if_eq VAR_LITTLEROOT_TOWN_STATE, 3", patched)
        event = patched.split("LittlerootTown_EventScript_GiveRunningShoesTrigger::", 1)[1]
        self.assertIn("\tend", event.split("LittlerootTown_EventScript_SetHomeDoorCoordsMale::", 1)[0])
        self.assertNotIn("LittlerootTown_EventScript_GiveRunningShoes\n", event)

    def test_mom_patch_rejects_unexpected_engine_script(self):
        with self.assertRaises(ValueError):
            patch_littleroot_script("no matching event script")


if __name__ == "__main__":
    unittest.main()
