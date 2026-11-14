# Game Design

## World structure: both-open

Hoenn and Sinnoh are available from the beginning through an in-game travel mechanism, such as a port or airport hub. The player chooses the order of regional exploration. Access to either region must not depend on completing the other region's League.

## Shared progression

Use a global progression score derived from durable milestones rather than current party level alone. The first rules prototype combines total badges across both regions with major story milestones. The score is monotonic: optional detours and party changes must not reduce it.

Gym roster selection uses the global score to select a configured tier. The selected tier is fixed when battle setup begins so a leader cannot change strength mid-battle.

## Gym scaling

Scaling should preserve each Gym's identity while changing team size, levels, moves, held items, and evolution stage by tier. The exact leader roster and level curves require an engine/map/trainer inventory before they can be implemented safely.

## Starter randomization

Select three distinct eligible species from the configured pool using the run seed and a dedicated randomization stream. Exclude unsupported or banned species. Starter selection must not change when unrelated encounter settings are changed.

## Legendary distribution

Legendary species can be assigned to eligible wild encounter slots across both regions. Use a configurable duplicate policy and protect story-critical encounter slots by default. The Python prototype currently supports protected slot IDs and allow/unique duplicate policies; engine encounter table discovery is still pending.

## Mega Evolution

Mega Evolution is a feature requirement. Use only mechanics, items, species forms, and battle hooks supported by the selected pokeemerald-expansion revision. Verify every Mega-capable species, stone, ability, and form transition against that revision; do not assume upstream APIs remain stable.

## Randomizer reproducibility

A seed plus versioned settings must reproduce the same randomized result. Independent deterministic streams are used for starters, wild encounters, and legendary placement so adding a random draw to one subsystem does not reshuffle all others.
