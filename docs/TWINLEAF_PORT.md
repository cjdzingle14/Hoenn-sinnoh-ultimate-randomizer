# Twinleaf Town first playable slice

Branch: `feature/twinleaf-first-playable`

## Goal

Replace the logical Sinnoh map manifest with a working opening slice in the GBA engine. The first checkpoint is a new-game start in Twinleaf Town (player's bedroom), exit to the player's house, then Twinleaf outdoors. Do not include graphics-polishing work.

## Existing source to import/audit

Pinned source: `LiderMorti00/Sinnoh-pokeemerald-expansion` at
`dd06b332cc5170920dc0be923337dafb7080f327`.

Confirmed source map folders:
- `data/maps/TwinleafTown` (outdoor town)
- `data/maps/TwinleafTown_MainHouse_1F` (player home ground floor)
- `data/maps/TwinleafTown_MainHouse_2F` (player bedroom/start)
- `data/maps/TwinleafTown_Haouse1` (source spelling preserved)
- `data/maps/TwinleafTown_House2`
- `data/maps/Twinleaf_Town_RivalsHouse_F1`
- `data/maps/Twinleaf_Town_RivalsHouse_F2`

Each confirmed map folder has a `map.json` and `scripts.inc`; corresponding layouts exist under `data/layouts/<source-name>/` with `map.bin` and `border.bin`.

## Import order / checkpoint criteria

1. [ ] Resolve map-name spelling and ID collisions against current engine (notably source typo `Haouse1`).
2. [ ] Import/register the player-house 2F, player-house 1F, and Twinleaf outdoor map with their layouts and scripts.
3. [ ] Verify all layout assets, object graphics, script symbols, music, region-map section, flags, and variables referenced by these maps exist in the target engine.
4. [ ] Add a temporary Sinnoh start route to the player's bedroom. Keep Hoenn as the default start until the Sinnoh route is verified.
5. [ ] Verify bedroom-to-1F-to-town warp chain, collision, map transitions, object events, and save/load in emulator.
6. [ ] Once stable, add Route 201 west as the next connected slice; do not stub destinations or claim unreachable maps are playable.

## Scope guard

This document is an implementation tracker only. It does not itself import map data or create a playable ROM. The upstream map JSON, scripts, and binary layouts are source references and must be adapted/merged into the target engine before a build can be called successful.
