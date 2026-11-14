"""Add persistent wild/trainer randomizer toggles to the in-game Options screen."""
from __future__ import annotations

import argparse
from pathlib import Path


def _replace_once(source: str, old: str, new: str, label: str) -> str:
    if new in source:
        return source
    if source.count(old) != 1:
        raise ValueError(f"Could not uniquely locate {label} in option_menu.c")
    return source.replace(old, new, 1)


def patch_option_menu(source: str) -> str:
    """Add two runtime toggles while keeping the stock Options screen layout."""
    source = _replace_once(
        source,
        '#include "global.h"\n',
        '#include "global.h"\n#include "event_data.h"\n',
        "global.h include",
    )
    source = _replace_once(
        source,
        "#define tWindowFrameType data[6]\n",
        "#define tWindowFrameType data[6]\n#define tRandomizerWildDisabled data[7]\n#define tRandomizerTrainersDisabled data[8]\n",
        "task data fields",
    )
    source = _replace_once(
        source,
        "    MENUITEM_FRAMETYPE,\n    MENUITEM_CANCEL,",
        "    MENUITEM_FRAMETYPE,\n    MENUITEM_RANDOMIZER_WILD,\n    MENUITEM_RANDOMIZER_TRAINERS,\n    MENUITEM_CANCEL,",
        "menu item enum",
    )
    source = _replace_once(
        source,
        "#define YPOS_FRAMETYPE    (MENUITEM_FRAMETYPE * 16)\n",
        "#define YPOS_FRAMETYPE    (MENUITEM_FRAMETYPE * 12)\n#define YPOS_RANDOMIZER_WILD (MENUITEM_RANDOMIZER_WILD * 12)\n#define YPOS_RANDOMIZER_TRAINERS (MENUITEM_RANDOMIZER_TRAINERS * 12)\n",
        "menu row positions",
    )
    source = _replace_once(
        source,
        "static void FrameType_DrawChoices(u8 selection);\n",
        "static void FrameType_DrawChoices(u8 selection);\nstatic void Randomizer_DrawChoices(u8 disabled, u8 y);\n",
        "randomizer draw prototype",
    )
    source = _replace_once(
        source,
        '    [MENUITEM_FRAMETYPE]   = COMPOUND_STRING("FRAME"),\n    [MENUITEM_CANCEL]',
        '    [MENUITEM_FRAMETYPE]   = COMPOUND_STRING("FRAME"),\n    [MENUITEM_RANDOMIZER_WILD] = COMPOUND_STRING("WILD RANDOMIZER"),\n    [MENUITEM_RANDOMIZER_TRAINERS] = COMPOUND_STRING("TRAINER RANDOMIZER"),\n    [MENUITEM_CANCEL]',
        "menu item labels",
    )
    source = _replace_once(
        source,
        "        gTasks[taskId].tWindowFrameType = gSaveBlock2Ptr->optionsWindowFrameType;\n",
        "        gTasks[taskId].tWindowFrameType = gSaveBlock2Ptr->optionsWindowFrameType;\n"
        "        gTasks[taskId].tRandomizerWildDisabled = FlagGet(FLAG_RANDOMIZER_DISABLE_WILD);\n"
        "        gTasks[taskId].tRandomizerTrainersDisabled = FlagGet(FLAG_RANDOMIZER_DISABLE_TRAINERS);\n",
        "randomizer option initialization",
    )
        "        FrameType_DrawChoices(gTasks[taskId].tWindowFrameType);\\n"
        "        HighlightOptionMenuItem(gTasks[taskId].tMenuSelection);\\n",
        "        FrameType_DrawChoices(gTasks[taskId].tWindowFrameType);\\n"
        "        Randomizer_DrawChoices(gTasks[taskId].tRandomizerWildDisabled, YPOS_RANDOMIZER_WILD);\\n"
        "        Randomizer_DrawChoices(gTasks[taskId].tRandomizerTrainersDisabled, YPOS_RANDOMIZER_TRAINERS);\\n"
        "        HighlightOptionMenuItem(gTasks[taskId].tMenuSelection);\\n",
        "randomizer option drawing during initialization",
    )
    source = _replace_once(
        source,
        "        case MENUITEM_FRAMETYPE:\n"
        "            previousOption = gTasks[taskId].tWindowFrameType;\n"
        "            gTasks[taskId].tWindowFrameType = FrameType_ProcessInput(gTasks[taskId].tWindowFrameType);\n"
        "\n"
        "            if (previousOption != gTasks[taskId].tWindowFrameType)\n"
        "                FrameType_DrawChoices(gTasks[taskId].tWindowFrameType);\n"
        "            break;\n"
        "        default:",
        "        case MENUITEM_FRAMETYPE:\n"
        "            previousOption = gTasks[taskId].tWindowFrameType;\n"
        "            gTasks[taskId].tWindowFrameType = FrameType_ProcessInput(gTasks[taskId].tWindowFrameType);\n"
        "\n"
        "            if (previousOption != gTasks[taskId].tWindowFrameType)\n"
        "                FrameType_DrawChoices(gTasks[taskId].tWindowFrameType);\n"
        "            break;\n"
        "        case MENUITEM_RANDOMIZER_WILD:\n"
        "            if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))\n"
        "            {\n"
        "                gTasks[taskId].tRandomizerWildDisabled ^= 1;\n"
        "                Randomizer_DrawChoices(gTasks[taskId].tRandomizerWildDisabled, YPOS_RANDOMIZER_WILD);\n"
        "                sArrowPressed = TRUE;\n"
        "            }\n"
        "            break;\n"
        "        case MENUITEM_RANDOMIZER_TRAINERS:\n"
        "            if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))\n"
        "            {\n"
        "                gTasks[taskId].tRandomizerTrainersDisabled ^= 1;\n"
        "                Randomizer_DrawChoices(gTasks[taskId].tRandomizerTrainersDisabled, YPOS_RANDOMIZER_TRAINERS);\n"
        "                sArrowPressed = TRUE;\n"
        "            }\n"
        "            break;\n"
        "        default:",
        "randomizer input handlers",
    )
    source = _replace_once(
        source,
        "    gSaveBlock2Ptr->optionsWindowFrameType = gTasks[taskId].tWindowFrameType;\n",
        "    gSaveBlock2Ptr->optionsWindowFrameType = gTasks[taskId].tWindowFrameType;\n"
        "    if (gTasks[taskId].tRandomizerWildDisabled)\n"
        "        FlagSet(FLAG_RANDOMIZER_DISABLE_WILD);\n"
        "    else\n"
        "        FlagClear(FLAG_RANDOMIZER_DISABLE_WILD);\n"
        "    if (gTasks[taskId].tRandomizerTrainersDisabled)\n"
        "        FlagSet(FLAG_RANDOMIZER_DISABLE_TRAINERS);\n"
        "    else\n"
        "        FlagClear(FLAG_RANDOMIZER_DISABLE_TRAINERS);\n",
        "randomizer option persistence",
    )
    source = _replace_once(
        source,
        "static void HighlightOptionMenuItem(u8 index)\n{\n"
        "    SetGpuReg(REG_OFFSET_WIN0H, WIN_RANGE(16, DISPLAY_WIDTH - 16));\n"
        "    SetGpuReg(REG_OFFSET_WIN0V, WIN_RANGE(index * 16 + 40, index * 16 + 56));\n"
        "}",
        "static void HighlightOptionMenuItem(u8 index)\n{\n"
        "    SetGpuReg(REG_OFFSET_WIN0H, WIN_RANGE(16, DISPLAY_WIDTH - 16));\n"
        "    SetGpuReg(REG_OFFSET_WIN0V, WIN_RANGE(index * 12 + 40, index * 12 + 52));\n"
        "}",
        "menu highlight geometry",
    )
    source = _replace_once(
        source,
        "static void FrameType_DrawChoices(u8 selection)\n{",
        "static void Randomizer_DrawChoices(u8 disabled, u8 y)\n"
        "{\n"
        "    u8 styles[2] = {0, 0};\n"
        "    styles[disabled ? 1 : 0] = 1;\n"
        "    DrawOptionMenuChoice(gText_BattleSceneOn, 104, y, styles[0]);\n"
        "    DrawOptionMenuChoice(gText_BattleSceneOff, GetStringRightAlignXOffset(FONT_NORMAL, gText_BattleSceneOff, 198), y, styles[1]);\n"
        "}\n\n"
        "static void FrameType_DrawChoices(u8 selection)\n{",
        "randomizer choice renderer",
    )
    source = _replace_once(
        source,
        "AddTextPrinterParameterized(WIN_OPTIONS, FONT_NORMAL, sOptionMenuItemsNames[i], 8, (i * 16) + 1, TEXT_SKIP_DRAW, NULL);",
        "AddTextPrinterParameterized(WIN_OPTIONS, FONT_NORMAL, sOptionMenuItemsNames[i], 8, (i * 12) + 1, TEXT_SKIP_DRAW, NULL);",
        "compact menu row spacing",
    )
    # All existing choice rows use the same vertical rhythm as the labels.
    for old, new in (
        ("(MENUITEM_TEXTSPEED * 16)", "(MENUITEM_TEXTSPEED * 12)"),
        ("(MENUITEM_BATTLESCENE * 16)", "(MENUITEM_BATTLESCENE * 12)"),
        ("(MENUITEM_BATTLESTYLE * 16)", "(MENUITEM_BATTLESTYLE * 12)"),
        ("(MENUITEM_SOUND * 16)", "(MENUITEM_SOUND * 12)"),
        ("(MENUITEM_BUTTONMODE * 16)", "(MENUITEM_BUTTONMODE * 12)"),
    ):
        source = source.replace(old, new)
    return source


def integrate(engine_dir: Path) -> None:
    path = engine_dir / "src" / "option_menu.c"
    source = path.read_text(encoding="utf-8")
    path.write_text(patch_option_menu(source), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    integrate(args.engine_dir)
    print("Integrated persistent wild/trainer toggles into the in-game Options screen")


if __name__ == "__main__":
    main()
