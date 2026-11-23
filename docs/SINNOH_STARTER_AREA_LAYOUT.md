# Sinnoh Starter Area — First Playable Layout Pass

Scope: native GBA-style map conversion planning for Twinleaf Town and Route 201.
This is a layout specification, **not yet native pokeemerald map/tileset/script data**.
Do not spend time on sprite smoothing, HD assets, palette polish, or graphics pipeline work.

## Constraints
- Keep the existing Hoenn adventure intact.
- New game must offer a region-start choice: Hoenn or Sinnoh.
- Sinnoh first-pass start: Twinleaf Town.
- Twinleaf Town connects north to Route 201.
- Route 201 connects south to Twinleaf Town and west toward Lake Verity (Lake Verity is a follow-on map, not included in this pass).
- Use GBA-scale tiles, collision, warps, events, NPCs, and scripts once engine map integration begins.
- Preserve save compatibility and ensure the region choice is only used when creating a new save.

## Twinleaf Town layout intent (20 × 18)
Coordinate origin is top-left; X increases east, Y increases south.
- North exit to Route 201 centered around x=10, y=0.
- Player house and rival house are separate interiors; use two warp points per interior.
- Town paths form a walkable central spine from the southern entry area to the northern route exit.
- Place water/shoreline and trees as blocking perimeter features; keep the main path unobstructed.
- NPC placeholder: neighbor on the central path; guide near the northern exit with a Route 201 hint.
- Signpost near north path should identify Route 201.

## Route 201 layout intent (32 × 18)
- South connection returns to Twinleaf Town near x=10.
- West connection is a future Lake Verity exit/landing; do not create a dangling warp to a missing map.
- Tall-grass encounter area should be separated from the main safe walking lane.
- Two early trainers are placeholders, each with one low-level party slot.
- Add a signpost and keep the south route back to town reachable without crossing an encounter-only blocked tile.
- Encounter blueprint: six grass slots, randomized eligible non-Legendary pool, levels 2–4.
- Trainer placeholders: one Pokémon, levels 3–4.

## Acceptance checklist
- [ ] Both maps exist as native engine map assets and load in-game.
- [ ] All collision boundaries are walkable/blocking as intended.
- [ ] Twinleaf-to-Route-201 and Route-201-to-Twinleaf transitions work in both directions.
- [ ] Town interior warps enter/exit both houses correctly.
- [ ] NPCs and signposts have working scripts.
- [ ] Route grass encounters trigger and obey configured levels.
- [ ] Route trainers can be battled and defeated without softlocks.
- [ ] Starting-region selector offers Hoenn and Sinnoh on a new game.
- [ ] Selecting Sinnoh places the player in Twinleaf Town; selecting Hoenn leaves the existing Hoenn start unchanged.
- [ ] Save/load works from both starts.
- [ ] CI and a local emulator playtest pass.

## Next implementation order
1. Locate the exact engine map-group, layout, tileset, event, and warp formats at the pinned submodule revision.
2. Build Twinleaf Town native map data and working exits/interiors first.
3. Build Route 201 native map data and return transition.
4. Implement the new-game region selector and route the Sinnoh choice to Twinleaf.
5. Add event/encounter scripts and validate by compiling and emulator playtesting.
