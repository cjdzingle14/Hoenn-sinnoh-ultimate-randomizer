# Secret Grotto & Ultra Beast Field Guide

This is the spoiler guide for the planned optional Hidden Grotto system. These are intended locations, not yet implemented in playable maps. Exact map coordinates, entrance tiles, event scripts, and encounter tables must be confirmed during the Hoenn/Sinnoh map audit before a release guide calls them final.

## How the system works

- Hidden Grotto entrances are optional exploration rewards, separate from ordinary wild grass/cave encounters.
- Each grotto has a concealed entrance or interactable environmental clue.
- A discovered grotto can contain an Ultra Beast encounter, a rare item, or a quiet/empty visit.
- Ultra Beast species and encounter assignments are reproducible from the run seed; each grotto has its own randomization stream so changing one grotto does not reshuffle every other one.
- Ultra Beasts are catchable. A small number of deeper/late-game grottos may use a tougher encounter tier.
- The player receives an in-game clue before or near each grotto. This document intentionally reveals every planned location.

## Hoenn — planned grotto locations

| Grotto | Where to look | Discovery clue |
|---|---|---|
| Petalburg Woods Grotto | Petalburg Woods, in a secluded pocket off the main forest path | Look behind the dense trees where the path seems to end. |
| Granite Grotto | Granite Cave, on an optional side passage away from the main descent | Check the dead-end alcove beyond the ordinary cave route. |
| Fiery Path Grotto | Fiery Path, behind a breakable-rock side route | Search the warm, isolated chamber past the rocks. |
| Mt. Pyre Grotto | Mt. Pyre exterior/side area, away from the main summit route | Look for a quiet ledge with an unusual shimmer. |
| Route 119 Grotto | Route 119, tucked into the tall-grass/rainforest area | Follow the narrow path beside the waterfall-side vegetation. |
| Shoal Cave Grotto | Shoal Cave, in an optional chamber reachable during the appropriate tide | Revisit the cave at the right tide and inspect the secluded chamber. |

## Sinnoh — planned grotto locations

| Grotto | Where to look | Discovery clue |
|---|---|---|
| Eterna Forest Grotto | Eterna Forest, off the interior forest path | Check the shadowed clearing behind the thick trees. |
| Wayward Cave Grotto | Wayward Cave, in an optional branch beyond the main passage | Inspect the isolated side chamber, not the bike-route entrance. |
| Mt. Coronet Grotto | Mt. Coronet, on a side floor away from the story route | Search the quiet alcove near the mountain's hidden passage. |
| Fuego Ironworks Grotto | Fuego Ironworks exterior, beyond the factory-side route | Look around the secluded edge of the works. |
| Great Marsh Grotto | Great Marsh, in a tucked-away marsh section | Watch for a dry pocket surrounded by reeds and water. |
| Snowpoint Grotto | Snowpoint Temple approach, in an optional outer chamber | Check the sheltered ice-side alcove before entering the deeper temple. |

## Important implementation notes

- The locations above are the design targets. Do not invent map group/map IDs or coordinates; record them only after inspecting the actual imported map data.
- If an intended landmark is not present in the final map set, move that grotto to the nearest clearly identifiable optional side area and update this guide.
- Add a map-name/coordinate table to this guide once the final event placements are committed.
- Keep all grottos reachable without requiring the player to complete the other region's League, consistent with the both-open design.
- Protect story-critical encounters and progression gates; grotto encounters must never replace required story events.
