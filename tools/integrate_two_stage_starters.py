"""Integrate a one-time second Birch starter offer after the Route 103 rival fight."""
from __future__ import annotations

import argparse
from pathlib import Path


VAR_NAMES = (
    "VAR_TEST5_FIRST_STARTER_1",
    "VAR_TEST5_FIRST_STARTER_2",
    "VAR_TEST5_FIRST_STARTER_3",
    "VAR_TEST5_STARTER_STAGE",
)


def _replace_function_body(source: str, signature: str, body: str) -> str:
    start = source.find(signature)
    if start < 0:
        raise ValueError(f"Could not locate {signature}")
    brace = source.find("{", start)
    depth = 0
    for pos in range(brace, len(source)):
        if source[pos] == "{":
            depth += 1
        elif source[pos] == "}":
            depth -= 1
            if depth == 0:
                return source[:brace] + "{\n" + body.rstrip() + "\n}" + source[pos + 1:]
    raise ValueError(f"Unclosed function {signature}")


def patch_vars_header(source: str) -> str:
    old = "\n".join(
        f"#define VAR_UNUSED_0x{address:04X}                                0x{address:04X} // Unused Var"
        for address in range(0x40F7, 0x40FB)
    )
    new = "\n".join((
        "#define VAR_TEST5_FIRST_STARTER_1                         0x40F7 // First offer species 1",
        "#define VAR_TEST5_FIRST_STARTER_2                         0x40F8 // First offer species 2",
        "#define VAR_TEST5_FIRST_STARTER_3                         0x40F9 // First offer species 3",
        "#define VAR_TEST5_STARTER_STAGE                           0x40FA // 0=first, 1=second pending, 2=complete",
    ))
    if source.count(old) != 1:
        raise ValueError("Could not uniquely locate four consecutive unused save vars 0x40F7-0x40FA")
    return source.replace(old, new, 1)


def patch_starter_source(source: str) -> str:
    if "VAR_TEST5_STARTER_STAGE" in source:
        raise ValueError("Two-stage starter patch already applied")
    if '#include "event_data.h"' not in source:
        source = source.replace('#include "main.h"', '#include "main.h"\n#include "event_data.h"', 1)

    body = """    u8 i;
    u16 firstOffer[STARTER_MON_COUNT] =
    {
        VarGet(VAR_TEST5_FIRST_STARTER_1),
        VarGet(VAR_TEST5_FIRST_STARTER_2),
        VarGet(VAR_TEST5_FIRST_STARTER_3),
    };

    for (i = 0; i < STARTER_MON_COUNT; i++)
    {
        u16 candidate;
        bool8 duplicate;
        do
        {
            u8 j;
            candidate = sStarterPool[Random() % ARRAY_COUNT(sStarterPool)];
            duplicate = FALSE;
            if (VarGet(VAR_TEST5_STARTER_STAGE) == 1)
            {
                for (j = 0; j < STARTER_MON_COUNT; j++)
                {
                    if (candidate == firstOffer[j])
                        duplicate = TRUE;
                }
            }
            for (j = 0; j < i; j++)
            {
                if (sStarterMon[j] == candidate)
                    duplicate = TRUE;
            }
        } while (duplicate);
        sStarterMon[i] = candidate;
    }

    // Persist all three species offered in the first screen before the rival fight.
    if (VarGet(VAR_TEST5_STARTER_STAGE) == 0)
    {
        VarSet(VAR_TEST5_FIRST_STARTER_1, sStarterMon[0]);
        VarSet(VAR_TEST5_FIRST_STARTER_2, sStarterMon[1]);
        VarSet(VAR_TEST5_FIRST_STARTER_3, sStarterMon[2]);
    }"""
    source = _replace_function_body(source, "static void RandomizeStarterChoices(void)", body)

    confirm_anchor = "gSpecialVar_Result = gTasks[taskId].tStarterSelection;"
    if source.count(confirm_anchor) != 1:
        raise ValueError("Could not uniquely locate starter confirmation")
    confirm_add = confirm_anchor + """
        // Advance the save-backed offer stage only after the player confirms a choice.
        if (VarGet(VAR_TEST5_STARTER_STAGE) == 0)
            VarSet(VAR_TEST5_STARTER_STAGE, 1);
        else if (VarGet(VAR_TEST5_STARTER_STAGE) == 1)
            VarSet(VAR_TEST5_STARTER_STAGE, 2);"""
    source = source.replace(confirm_anchor, confirm_add, 1)

    prompt_anchor = 'static u16 sStarterLabelWindowId;'
    if source.count(prompt_anchor) != 1:
        raise ValueError("Could not locate starter UI static declarations")
    source = source.replace(
        prompt_anchor,
        prompt_anchor + '\nstatic const u8 sText_SecondStarterPrompt[] = _("Choose your second Pokémon!");',
        1,
    )
    old_prompt = 'AddTextPrinterParameterized(0, FONT_NORMAL, gText_BirchInTrouble, 0, 1, 0, NULL);'
    if source.count(old_prompt) != 1:
        raise ValueError("Could not uniquely locate starter-screen prompt")
    new_prompt = """if (VarGet(VAR_TEST5_STARTER_STAGE) == 1)
        AddTextPrinterParameterized(0, FONT_NORMAL, sText_SecondStarterPrompt, 0, 1, 0, NULL);
    else
        AddTextPrinterParameterized(0, FONT_NORMAL, gText_BirchInTrouble, 0, 1, 0, NULL);"""
    source = source.replace(old_prompt, new_prompt, 1)
    return source


def patch_lab_script(source: str) -> str:
    anchor = "\tsetvar VAR_BIRCH_LAB_STATE, 5"
    if source.count(anchor) != 1:
        raise ValueError("Could not uniquely locate the one-time post-rival Birch lab progression")
    return source.replace(
        anchor,
        "\t@ Second starter offer: this runs only on the first return after the Route 103 rival battle.\n"
        "\tspecial ChooseStarter\n" + anchor,
        1,
    )


def integrate(engine_dir: Path) -> None:
    vars_path = engine_dir / "include" / "constants" / "vars.h"
    starter_path = engine_dir / "src" / "starter_choose.c"
    lab_path = engine_dir / "data" / "maps" / "LittlerootTown_ProfessorBirchsLab" / "scripts.inc"
    vars_path.write_text(patch_vars_header(vars_path.read_text(encoding="utf-8")), encoding="utf-8")
    starter_path.write_text(patch_starter_source(starter_path.read_text(encoding="utf-8")), encoding="utf-8")
    lab_path.write_text(patch_lab_script(lab_path.read_text(encoding="utf-8")), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    integrate(args.engine_dir)
    print("Integrated save-backed second starter offer after the Route 103 rival battle")


if __name__ == "__main__":
    main()
