# Sinnoh First Area: Twinleaf Town + Route 201 (First Pass)

## Target
Begin the Sinnoh side of the Hoenn–Sinnoh project with **Twinleaf Town** and the adjoining **Route 201**. This is the first connected Sinnoh slice to implement and test; it is not intended to replace Hoenn or make the full Sinnoh region available at once.

## Player experience
- Twinleaf Town is the Sinnoh start area, with a clear north/east connection into Route 201.
- Route 201 should connect Twinleaf Town toward Lake Verity and include a recognizable route path, grass patches for wild encounters, trees/edges, and basic trainer/NPC placement.
- Preserve the familiar Twinleaf landmarks: player's home, rival's home, paths, and town exit.
- Keep navigation and encounter spaces readable at the GBA tile scale.
- Use the Emerald engine's map/event/warp conventions and reuse compatible tiles where practical; add Sinnoh visual assets only when they can be built and tested reliably.

## First-pass implementation checklist
1. Inspect pinned pokeemerald-expansion map, warp, event, metatile, tileset, encounter, and trainer conventions.
2. Create Twinleaf Town map with GBA-sized tiles, collision/behavior data, homes, and signs.
3. Create Route 201 map connecting Twinleaf to Lake Verity's planned entrance; add route paths, grass encounter areas, obstacles, and transition points.
4. Add house warp points and route map connections in both directions; ensure no dead ends or softlocks.
5. Add minimal NPCs/trainers/signs to orient the player; keep optional dialogue and decoration for later.
6. Make the Twinleaf + Route 201 slice reachable from the project's Sinnoh start selection without disturbing Hoenn.
7. Build and run map validation; test transitions, house warps, collisions, encounters, trainer battles, and save/reload.
8. Once this slice is stable, begin Lake Verity.

## Scope and acceptance criteria
- Twinleaf Town and Route 201 are distinct Sinnoh maps, not renamed Hoenn maps.
- Player can travel from Twinleaf to Route 201 and back.
- Route 201 leads toward the planned Lake Verity connection.
- Player's and rival's houses have working interior warps and return to correct outdoor locations.
- Route grass encounters and basic trainer interactions function if included in this first pass.
- Map collision, scripts, encounters, and connections compile and pass basic checks.
- Hoenn's existing start and routes remain unchanged.

## Notes / blockers
This document defines the initial connected area and acceptance criteria. Actual map data, tiles, events, trainers, encounters, and warps still need to be implemented against the pinned engine checkout and validated in a built ROM. Do not mark Twinleaf or Route 201 playable/completed based on this plan alone.
