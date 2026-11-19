# Game Design

## New-game starting region

At the start of a new game, offer **Hoenn** or **Sinnoh** as the player's opening region. Hoenn remains the default for existing behavior and backward compatibility. This choice selects the opening location and introductory sequence only; it does not lock the player out of the other region. Both regions remain part of the same adventure and are intended to be reachable from the beginning through the shared travel system.

The choice must be stored in the save so the correct opening flow is retained across save/load. The selection screen must appear only for a genuinely new game, not Continue or returning from another menu. Each option must resolve through verified engine map/script identifiers; do not use placeholder map IDs in production code.

The initial rules layer lives in `tools/region_selection.py`. It validates the configured choices and resolves stable logical start keys (`hoenn_new_game_start` / `sinnoh_new_game_start`). The engine-facing menu, save field, opening scripts, and actual Sinnoh start map are still pending map import and engine integration.

## World structure: both-open

Hoenn and Sinnoh are available from the beginning through an in-game travel mechanism, such as a port or airport hub. The player chooses the order of regional exploration. Access to either region must not depend on completing the other region's League.

## Shared progression

Use a global progression score derived from durable milestones rather than current party level alone. The first rules prototype combines total badges across both regions with major story milestones. The score is monotonic: optional detours and party changes must not reduce it.

Gym roster selection uses the global score to select a configured tier. The selected tier is fixed when battle setup begins so a leader cannot change strength mid-battle.

## Gym scaling

Scaling should preserve each Gym's identity while changing team size, levels, moves, held items, and evolution stage by tier. The exact leader roster and level curves require an engine/map/trainer inventory before they can be implemented safely.

## Starter randomization

Each region presents its own set of three randomized starter choices. The player chooses one Pokémon in Hoenn and one Pokémon in Sinnoh, for two starter selections total across the adventure. All six offered Pokémon are distinct across both regions, excluding unsupported and banned species. The long-term design uses a run seed and separate starter streams for Hoenn and Sinnoh. The current engine integration now generates a fresh trio of distinct non-Legendary base species at runtime whenever a new game enters the starter-selection screen. The chosen Pokémon is then saved as part of that playthrough. The second regional starter screen and persistent two-region starter grants remain future engine work; the Python rules prototype defines and tests the six-choice result.

## Legendary distribution

Legendary species can be assigned to eligible wild encounter slots across both regions. Use a configurable duplicate policy and protect story-critical encounter slots by default. The Python prototype currently supports protected slot IDs and allow/unique duplicate policies; engine encounter table discovery is still pending.

## Secret Hidden Grottos and Ultra Beasts

Add optional, concealed grotto discoveries across both regions. Grottos are separate from ordinary wild encounter tables and can yield a seeded Ultra Beast encounter, a rare item, or an empty visit. Ultra Beasts are catchable. Each grotto uses a dedicated deterministic randomization stream so changing one location does not reshuffle the others. Some late-game grottos may use a higher encounter tier, but both regions remain accessible from the start.

The intended Hoenn locations are Petalburg Woods, Granite Cave, Fiery Path, Mt. Pyre, Route 119, and Shoal Cave. The intended Sinnoh locations are Eterna Forest, Wayward Cave, Mt. Coronet, Fuego Ironworks, Great Marsh, and the Snowpoint Temple approach. The spoiler guide lists all planned locations and clues. These are design targets only: final map IDs, coordinates, access requirements, and in-game clues must be verified against the actual imported map data before being described as final.

## Mega Evolution

Mega Evolution is a feature requirement. Use only mechanics, items, species forms, and battle hooks supported by the selected pokeemerald-expansion revision. Verify every Mega-capable species, stone, ability, and form transition against that revision; do not assume upstream APIs remain stable.


## Pokémon Center healing dialogue

Pokémon Center healing should be streamlined: Nurse Joy does not display the usual greeting, introductory questions, or pre-healing dialogue. The healing process starts immediately when the player uses the counter. After the party has finished healing, Nurse Joy displays one short confirmation that the Pokémon are fully healed. Preserve the existing healing effect, sound, animation, and any required control flow; remove only the unnecessary dialogue. Apply consistently to every Pokémon Center in both regions.

## Randomizer reproducibility

A seed plus versioned settings must reproduce the same randomized result. Independent deterministic streams are used for regional starters, wild encounters, legendary placement, and each grotto so adding a random draw to one subsystem does not reshuffle all others.
