# Sinnoh first playable milestone

Work branch: `feature/sinnoh-first-playable`

This milestone is deliberately limited to the opening playable slice. It does not include graphics polish or sprite smoothing.

## Player-facing goal

At the beginning of a new save, offer **Hoenn** or **Sinnoh**. Choosing Hoenn must preserve the existing Hoenn new-game flow and spawn point. Choosing Sinnoh must start in **Twinleaf Town**, with a working exit/connection to **Route 201**.

## Native-engine tasks

1. Inspect the pinned pokeemerald-expansion revision and its map, layout, tileset, event, warp, connection, and script conventions.
2. Allocate map IDs in the engine's existing map-group system; avoid collisions and keep the map list/metadata consistent.
3. Convert Twinleaf Town into a GBA-compatible map layout and implement its entrances, exits, NPC/event placeholders, and warp behavior needed for the opening.
4. Convert Route 201 into a GBA-compatible layout and implement the connection/warps from Twinleaf.
5. Implement a new-game region selection in the engine's normal startup flow. Persist the choice in the new save and route the player to the matching spawn. Do not change the existing Hoenn start path.
6. Integrate the overlay into CI before the ROM compile and add source-level tests that fail if either map, the route connection, or the region branch is missing.
7. Build the engine and test both new-game choices in an emulator.

## Acceptance checklist

- [ ] New game offers Hoenn and Sinnoh.
- [ ] Hoenn selection still starts at the original Hoenn location.
- [ ] Sinnoh selection starts in Twinleaf Town.
- [ ] Twinleaf Town to Route 201 is traversable in both directions where designed.
- [ ] Map IDs, map layouts, event data, warps, and connections are valid and non-colliding.
- [ ] CI integration runs before the ROM build.
- [ ] ROM compiles and passes header validation.
- [ ] Emulator smoke test confirms both region starts and the route transition.

## Implementation boundary / honest status

The repository's engine is a pinned Git submodule; the root repository does not currently contain its C map source or binary map assets as ordinary files. Native map conversion must be made against the checked-out submodule so that real layouts, headers, events, and scripts can be validated and compiled. This document is a working implementation spec, not evidence that maps or selector are already playable.
