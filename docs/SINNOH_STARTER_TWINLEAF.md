# Sinnoh First Area: Twinleaf Town (First Pass)

## Target
Begin the Sinnoh side of the Hoenn–Sinnoh project with **Twinleaf Town**, the first town in Pokémon Diamond/Pearl/Platinum. This is the first Sinnoh area to implement and test; it is not intended to replace Hoenn or make the full Sinnoh region available at once.

## Player experience
- Make Twinleaf Town the first Sinnoh starting area, with a clear transition into Route 201.
- Preserve the familiar town layout and landmarks: the player's home, rival's home, town path/grass edges, and the Route 201 exit toward Lake Verity.
- Keep navigation simple and readable at the GBA tile scale.
- Use the existing Emerald engine's map/event/warp conventions and reuse compatible tiles where practical; add a Sinnoh visual palette/tileset only when it can be built and tested reliably.

## First-pass implementation checklist
1. Inspect the pinned pokeemerald-expansion map, warp, event, metatile, and tileset conventions.
2. Create a Twinleaf Town map using GBA-sized tiles and collision/behavior data.
3. Add warp points for the player's home and rival's home, and the outbound Route 201 connection.
4. Add the minimum town NPCs/signs needed to orient the player; leave optional dialogue and decoration for later passes.
5. Add a map connection/entry path that can be reached from the project's Sinnoh start selection without disturbing Hoenn.
6. Build and run map validation; test entry, exits, house warps, collisions, and save/reload.
7. Only after Twinleaf is stable, begin Route 201 and Lake Verity.

## Scope and acceptance criteria
- Twinleaf Town is a distinct Sinnoh map, not a renamed Hoenn map.
- Player can enter and leave the town without softlocks.
- Both house interiors are reachable through working warps and return to the correct outdoor location.
- Map collision, map scripts, and map connections compile and pass basic checks.
- Hoenn's existing start and routes remain unchanged.

## Notes / blockers
This document defines the first-area work and acceptance criteria. Actual map data, tiles, events, and warps still need to be implemented against the pinned engine checkout and validated in a built ROM. Do not mark Twinleaf as playable or complete based on this plan alone.
