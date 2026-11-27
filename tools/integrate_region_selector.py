"""Apply a new-game Hoenn/Sinnoh choice to the pinned Sinnoh-capable engine."""

from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    content = path.read_text(encoding="utf-8")
    if new in content:
        return
    if old not in content:
        raise SystemExit(f"Expected integration anchor not found in {path}: {old[:100]!r}")
    path.write_text(content.replace(old, new, 1), encoding="utf-8")


def integrate(engine_dir: Path) -> None:
    header = engine_dir / "include" / "new_game.h"
    replace_once(
        header,
        "#endif // GUARD_NEW_GAME_H",
        """#define NEW_GAME_START_REGION_HOENN 0
#define NEW_GAME_START_REGION_SINNOH 1

extern u8 gNewGameStartRegion;

#endif // GUARD_NEW_GAME_H""",
    )

    new_game = engine_dir / "src" / "new_game.c"
    replace_once(
        new_game,
        "EWRAM_DATA bool8 gEnableContestDebugging = FALSE;",
        """EWRAM_DATA bool8 gEnableContestDebugging = FALSE;
EWRAM_DATA u8 gNewGameStartRegion = NEW_GAME_START_REGION_HOENN;""",
    )
    replace_once(
        new_game,
        """static void WarpToTruck(void)
{
    SetWarpDestination(MAP_GROUP(MAP_TWINLEAF_TOWN_MAIN_HOUSE_2F), MAP_NUM(MAP_TWINLEAF_TOWN_MAIN_HOUSE_2F), WARP_ID_NONE, -1, -1);
    WarpIntoMap();
}""",
        """static void WarpToTruck(void)
{
    if (IS_FRLG)
        SetWarpDestination(MAP_GROUP(MAP_PALLET_TOWN_PLAYERS_HOUSE_2F), MAP_NUM(MAP_PALLET_TOWN_PLAYERS_HOUSE_2F), WARP_ID_NONE, 6, 6);
    else if (gNewGameStartRegion == NEW_GAME_START_REGION_SINNOH)
        SetWarpDestination(MAP_GROUP(MAP_TWINLEAF_TOWN_MAIN_HOUSE_2F), MAP_NUM(MAP_TWINLEAF_TOWN_MAIN_HOUSE_2F), WARP_ID_NONE, -1, -1);
    else
        SetWarpDestination(MAP_GROUP(MAP_INSIDE_OF_TRUCK), MAP_NUM(MAP_INSIDE_OF_TRUCK), WARP_ID_NONE, -1, -1);
    WarpIntoMap();
}""",
    )

    main_menu = engine_dir / "src" / "main_menu.c"
    replace_once(
        main_menu,
        '#include "main.h"\n',
        '#include "main.h"\n#include "new_game.h"\n',
    )
    replace_once(
        main_menu,
        "static u8 sBirchSpeechMainTaskId;\n",
        """static u8 sBirchSpeechMainTaskId;
static const u8 sText_ChooseStartingRegion[] = _("A: SINNOH    B: HOENN");
""",
    )
    replace_once(
        main_menu,
        "static void Task_HandleMainMenuAPressed(u8);\n",
        "static void Task_HandleMainMenuAPressed(u8);\nstatic void Task_ChooseStartingRegion(u8);\n",
    )
    replace_once(
        main_menu,
        """            // Proyecto Sinnoh: intro del Prof. Serbal en lugar del discurso de Abedul
            DestroyTask(taskId);
            StartRowanIntro();
            return;
            break;""",
        """            gTasks[taskId].data[0] = 0;
            gTasks[taskId].func = Task_ChooseStartingRegion;
            gPlttBufferUnfaded[BG_PLTT_ID(15) + 1] = RGB_WHITE;
            gPlttBufferFaded[BG_PLTT_ID(15) + 1] = RGB_WHITE;
            SetGpuReg(REG_OFFSET_WIN0H, 0);
            SetGpuReg(REG_OFFSET_WIN0V, 0);
            BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
            return;
            break;""",
    )
    replace_once(
        main_menu,
        "static void Task_HandleMainMenuBPressed(u8 taskId)",
        """static void Task_ChooseStartingRegion(u8 taskId)
{
    switch (gTasks[taskId].data[0])
    {
    case 0:
        FillBgTilemapBufferRect_Palette0(0, 0, 0, 0, DISPLAY_TILE_WIDTH, DISPLAY_TILE_HEIGHT);
        CreateMainMenuErrorWindow(sText_ChooseStartingRegion);
        gTasks[taskId].data[0]++;
        break;
    case 1:
        if (!gPaletteFade.active)
            gTasks[taskId].data[0]++;
        break;
    case 2:
        RunTextPrinters();
        if (IsTextPrinterActiveOnWindow(7))
            break;
        if (JOY_NEW(A_BUTTON))
        {
            PlaySE(SE_SELECT);
            gNewGameStartRegion = NEW_GAME_START_REGION_SINNOH;
            DestroyTask(taskId);
            StartRowanIntro();
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            gNewGameStartRegion = NEW_GAME_START_REGION_HOENN;
            FreeAllWindowBuffers();
            Task_NewGameBirchSpeech_Init(taskId);
        }
        break;
    }
}

static void Task_HandleMainMenuBPressed(u8 taskId)""",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    integrate(args.engine_dir)
    print("New-game region choice integrated: A = Sinnoh, B = Hoenn")


if __name__ == "__main__":
    main()
