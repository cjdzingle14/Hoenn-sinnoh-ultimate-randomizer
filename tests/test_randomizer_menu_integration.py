import pytest

from tools.integrate_randomizer_menu import patch_option_menu


OPTION_MENU_FIXTURE = """#include "global.h"
#define tWindowFrameType data[6]

enum
{
    MENUITEM_TEXTSPEED,
    MENUITEM_BATTLESCENE,
    MENUITEM_BATTLESTYLE,
    MENUITEM_SOUND,
    MENUITEM_BUTTONMODE,
    MENUITEM_FRAMETYPE,
    MENUITEM_CANCEL,
    MENUITEM_COUNT,
};

#define YPOS_FRAMETYPE    (MENUITEM_FRAMETYPE * 16)

static void FrameType_DrawChoices(u8 selection);

static const u8 *const sOptionMenuItemsNames[MENUITEM_COUNT] =
{
    [MENUITEM_FRAMETYPE]   = COMPOUND_STRING("FRAME"),
    [MENUITEM_CANCEL]      = COMPOUND_STRING("CANCEL"),
};

        gTasks[taskId].tWindowFrameType = gSaveBlock2Ptr->optionsWindowFrameType;
        FrameType_DrawChoices(gTasks[taskId].tWindowFrameType);

        case MENUITEM_FRAMETYPE:
            previousOption = gTasks[taskId].tWindowFrameType;
            gTasks[taskId].tWindowFrameType = FrameType_ProcessInput(gTasks[taskId].tWindowFrameType);

            if (previousOption != gTasks[taskId].tWindowFrameType)
                FrameType_DrawChoices(gTasks[taskId].tWindowFrameType);
            break;
        default:
            return;

    gSaveBlock2Ptr->optionsWindowFrameType = gTasks[taskId].tWindowFrameType;

static void HighlightOptionMenuItem(u8 index)
{
    SetGpuReg(REG_OFFSET_WIN0H, WIN_RANGE(16, DISPLAY_WIDTH - 16));
    SetGpuReg(REG_OFFSET_WIN0V, WIN_RANGE(index * 16 + 40, index * 16 + 56));
}

static void FrameType_DrawChoices(u8 selection)
{
}

AddTextPrinterParameterized(WIN_OPTIONS, FONT_NORMAL, sOptionMenuItemsNames[i], 8, (i * 16) + 1, TEXT_SKIP_DRAW, NULL);
"""


def test_menu_exposes_persistent_wild_and_trainer_toggles():
    patched = patch_option_menu(OPTION_MENU_FIXTURE)

    assert "WILD RANDOMIZER" in patched
    assert "TRAINER RANDOMIZER" in patched
    assert "FlagGet(FLAG_RANDOMIZER_DISABLE_WILD)" in patched
    assert "FlagGet(FLAG_RANDOMIZER_DISABLE_TRAINERS)" in patched
    assert "FlagSet(FLAG_RANDOMIZER_DISABLE_WILD)" in patched
    assert "FlagClear(FLAG_RANDOMIZER_DISABLE_WILD)" in patched
    assert "FlagSet(FLAG_RANDOMIZER_DISABLE_TRAINERS)" in patched
    assert "FlagClear(FLAG_RANDOMIZER_DISABLE_TRAINERS)" in patched
    assert "gTasks[taskId].tRandomizerWildDisabled ^= 1;" in patched
    assert "gTasks[taskId].tRandomizerTrainersDisabled ^= 1;" in patched
    assert "(i * 12) + 1" in patched
    assert "index * 12 + 40" in patched


def test_menu_patch_is_idempotent():
    patched = patch_option_menu(OPTION_MENU_FIXTURE)
    assert patch_option_menu(patched) == patched


def test_menu_patch_fails_closed_when_upstream_source_changes():
    with pytest.raises(ValueError):
        patch_option_menu('#include "global.h"\\n')
