from pathlib import Path

from tools.integrate_region_selector import integrate


def test_region_selector_patches_engine_and_is_idempotent(tmp_path: Path) -> None:
    engine = tmp_path
    (engine / "include" / "constants").mkdir(parents=True)
    (engine / "src").mkdir()
    (engine / "data" / "maps" / "LittlerootTown_ProfessorBirchsLab").mkdir(parents=True)
    (engine / "include" / "new_game.h").write_text(
        "#ifndef GUARD_NEW_GAME_H\nextern bool8 gDifferentSaveFile;\n#endif // GUARD_NEW_GAME_H\n",
        encoding="utf-8",
    )
    (engine / "include" / "constants" / "vars.h").write_text(
        "#define VAR_UNUSED_0x40E5                                0x40E5 // Unused Var\n",
        encoding="utf-8",
    )
    (engine / "src" / "new_game.c").write_text(
        '#include "constants/items.h"\n'
        "EWRAM_DATA bool8 gDifferentSaveFile = FALSE;\n"
        "EWRAM_DATA bool8 gEnableContestDebugging = FALSE;\n"
        "static void WarpToTruck(void)\n{\n"
        "    SetWarpDestination(MAP_GROUP(MAP_TWINLEAF_TOWN_MAIN_HOUSE_2F), "
        "MAP_NUM(MAP_TWINLEAF_TOWN_MAIN_HOUSE_2F), WARP_ID_NONE, -1, -1);\n"
        "    WarpIntoMap();\n}\n"
        "void NewGameInitData(void)\n{\n    InitEventData();\n}\n",
        encoding="utf-8",
    )
    (engine / "data" / "maps" / "LittlerootTown_ProfessorBirchsLab" / "scripts.inc").write_text(
        "LittlerootTown_ProfessorBirchsLab_MapScripts::\n"
        "\tmap_script MAP_SCRIPT_ON_TRANSITION, SandgemLab_OnTransition\n"
        "\t.byte 0\n"
        "LittlerootTown_ProfessorBirchsLab_OnTransition:\n\tend\n"
        "LittlerootTown_ProfessorBirchsLab_OnWarp:\n\t.2byte 0\n"
        "LittlerootTown_ProfessorBirchsLab_OnFrame:\n\t.2byte 0\n",
        encoding="utf-8",
    )
    (engine / "src" / "main_menu.c").write_text(
        '#include "main.h"\n'
        "static u8 sBirchSpeechMainTaskId;\n"
        "static void Task_HandleMainMenuAPressed(u8);\n"
        "static void Task_NewGameBirchSpeech_Init(u8);\n"
        "static void Task_HandleMainMenuAPressed(u8 taskId)\n{\n"
        "            // Proyecto Sinnoh: intro del Prof. Serbal en lugar del discurso de Abedul\n"
        "            DestroyTask(taskId);\n"
        "            StartRowanIntro();\n"
        "            return;\n"
        "            break;\n}\n"
        "static void Task_HandleMainMenuBPressed(u8 taskId)\n{\n}\n",
        encoding="utf-8",
    )

    integrate(engine)
    integrate(engine)

    header = (engine / "include" / "new_game.h").read_text(encoding="utf-8")
    vars_header = (engine / "include" / "constants" / "vars.h").read_text(encoding="utf-8")
    new_game = (engine / "src" / "new_game.c").read_text(encoding="utf-8")
    lab_scripts = (engine / "data" / "maps" / "LittlerootTown_ProfessorBirchsLab" / "scripts.inc").read_text(encoding="utf-8")
    main_menu = (engine / "src" / "main_menu.c").read_text(encoding="utf-8")

    assert "NEW_GAME_START_REGION_SINNOH" in header
    assert "VAR_START_REGION VAR_UNUSED_0x40E5" in vars_header
    assert '#include "constants/vars.h"' in new_game
    assert "gNewGameStartRegion = NEW_GAME_START_REGION_HOENN" in new_game
    assert "MAP_INSIDE_OF_TRUCK" in new_game
    assert "MAP_TWINLEAF_TOWN_MAIN_HOUSE_2F" in new_game
    assert "VarSet(VAR_START_REGION, gNewGameStartRegion);" in new_game
    assert "LittlerootTown_ProfessorBirchsLab_RegionOnTransition" in lab_scripts
    assert "goto_if_eq VAR_START_REGION, NEW_GAME_START_REGION_SINNOH, SandgemLab_OnTransition" in lab_scripts
    assert "goto LittlerootTown_ProfessorBirchsLab_OnTransition" in lab_scripts
    assert "LittlerootTown_ProfessorBirchsLab_RegionOnWarp" in lab_scripts
    assert "LittlerootTown_ProfessorBirchsLab_RegionOnFrame" in lab_scripts
    assert "LittlerootTown_ProfessorBirchsLab_OnWarp" in lab_scripts
    assert "LittlerootTown_ProfessorBirchsLab_OnFrame" in lab_scripts
    assert "sText_ChooseStartingRegion" in main_menu
    assert "gNewGameStartRegion = NEW_GAME_START_REGION_SINNOH" in main_menu
    assert "gNewGameStartRegion = NEW_GAME_START_REGION_HOENN" in main_menu
    assert "Task_NewGameBirchSpeech_Init" in main_menu
    assert main_menu.count("static void Task_ChooseStartingRegion(u8);") == 1
    assert main_menu.count("static void Task_ChooseStartingRegion(u8 taskId)") == 1
    assert "IsTextPrinterActiveOnWindow(7)" in main_menu
    assert "BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK)" in main_menu
    assert "RunTextPrinters();" in main_menu
    assert "FillBgTilemapBufferRect_Palette0(0, 0, 0, 0, DISPLAY_TILE_WIDTH, DISPLAY_TILE_HEIGHT);" in main_menu
    assert "FreeAllWindowBuffers();\n            Task_NewGameBirchSpeech_Init(taskId);" in main_menu
