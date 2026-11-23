# Sinnoh opening implementation work

## Source assets confirmed
At pinned Sinnoh source revision `dd06b332cc5170920dc0be923337dafb7080f327`, the following source entries exist:
- `data/maps/TwinleafTown/map.json` and `scripts.inc`
- `data/layouts/TwinleafTown/map.bin` and `border.bin`
- `data/maps/Route201/map.json` and `scripts.inc`
- `data/layouts/Route201/map.bin` and `border.bin`

These are source-engine assets, not yet converted into this project's final GBA map registration/build. They are the first conversion targets.

## New Game region selection acceptance criteria
- New Game must present a clear choice: **Hoenn** or **Sinnoh**.
- Hoenn remains the default for backward compatibility, but Sinnoh is a selectable option (not merely a config/test-only option).
- Selecting Sinnoh must route the new save to the Sinnoh opening map, starting in Twinleaf Town player's house (2F), then connect to Twinleaf Town and Route 201.
- Selecting Hoenn must retain the original Hoenn start.
- Selection must be stored in the new save so continue/load never re-prompts or silently changes the start.
- Tests must cover both selections and default Hoenn; emulator test must confirm each route.

## Current implementation status
- Region-selection rules and unit tests exist in `tools/region_selection.py` and `tests/test_region_selection.py`.
- The rule resolver accepts explicit `hoenn` or `sinnoh`; tests cover both.
- **The in-game New Game menu and actual map-start routing are not yet wired up.** Do not treat the current unit tests as proof that the playable ROM can select Sinnoh.
- Next integration step: wire the choice into the engine New Game flow/save initialization and map-start constants, then test both starts in emulator.
