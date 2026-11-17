# Game Design

## World structure: both-open

Hoenn and Sinnoh are available from the beginning through an in-game travel mechanism, such as a port or airport hub. The player chooses the order of regional exploration. Access to either region must not depend on completing the other region's League.

## Shared progression

Use a global progression score derived from durable milestones rather than current party level alone. The first rules prototype combines total badges across both regions with major story milestones. The score is monotonic: optional detours and party changes must not reduce it.

Gym roster selection uses the global score to select a configured tier. The selected tier is fixed when battle setup begins so a leader cannot change strength mid-battle.

## Gym scaling

Scaling should preserve each Gym's identity while changing team size, levels, moves, held items, and evolution stage by tier. The exact leader roster and level curves require an engine/map/trainer inventory before they can be implemented safely.

## Starter randomization

The Hoenn adventure has two starter selections. At the beginning, the player chooses one Pokémon from a randomized trio in Professor Birch's normal starter sequence. After defeating the Route 103 rival and returning to Birch's lab, Birch offers a second randomized trio. The second trio must exclude all three species offered in the first trio, so all six offered choices are unique. The first selection and its Pokémon must remain saved; the second selection is a separate, one-time grant and must never overwrite the first. Both Pokémon are added to the player's collection, using the party when space is available and the PC otherwise. The second offer must be triggered by the actual rival-defeat/lab-return progression, not merely by reopening the starter screen.

## Pokédex

Use the National Pokédex from the start of a new game. It must cover every species supported by the pinned engine revision, not only the Hoenn regional dex or a Sinnoh regional list. Seen/caught registration must remain shared and correct across both regions, and newly selected starters must register through the normal engine Pokédex flow. The player should not need to complete a regional Pokédex or wait for a late-game upgrade to access National mode.

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
