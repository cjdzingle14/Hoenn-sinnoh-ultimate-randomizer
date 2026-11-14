# Hoenn–Sinnoh Ultimate Randomizer

A custom Pokémon GBA ROM-hack project targeting a single adventure that includes both Hoenn and Sinnoh. The selected engine foundation is [RHH's pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion).

## Agreed game direction

- Hoenn and Sinnoh are both available in the main adventure.
- Gym leaders and major battles scale with global player progression.
- Three distinct starter species are selected reproducibly from the eligible pool.
- Legendary Pokémon can be assigned to eligible encounter slots across both regions.
- Mega Evolution is included, using verified support from the pinned engine revision.
- Pokédex coverage targets the species and forms supported by the selected engine revision.

## Current status

**The repository now contains the first runnable Python randomizer rules package. It is not yet a playable ROM hack.**

Implemented in the root project:
- Stable, independent random-number streams based on a user seed.
- Deterministic distinct selection and weighted selection primitives.
- Settings validation for the two-region world, Gym scaling, starters, legendary duplicate policy, and Mega Evolution toggle.
- A monotonic global progression score and Gym-tier selection helper.
- Starter selection with banned-species filtering.
- Legendary encounter assignment with protected story slots and configurable duplicate policy.
- Unit tests and a GitHub Actions test workflow.

The actual pokeemerald-expansion source tree is not yet part of this repository and no modified GBA ROM has been built. See [the engine foundation and integration roadmap](docs/ENGINE_FOUNDATION.md).

## Run the randomizer tests

Requires Python 3.10 or newer.

```bash
python -m pip install pytest
python -m pytest -q
```

The GitHub Actions workflow runs this same test suite on pushes to main, pull requests to main, and manual dispatch.

## Engine foundation

The selected game engine is [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion). Follow its upstream [installation and build instructions](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md). Clone it with Git rather than downloading a source ZIP so its history and branches are preserved.

The planned integration sequence is to pin an upstream revision, verify an unchanged baseline build, inventory the engine's data and maps, then implement the Hoenn/Sinnoh world, progression systems, and engine adapter in tested stages.

## Development principles

- The same seed and versioned settings must reproduce the same result.
- Independent PRNG streams prevent unrelated settings from reshuffling other systems.
- Validate settings and engine targets before changing game data.
- Record the seed, settings, and upstream engine revision for reproducibility.
- Never assume every modern Pokémon feature fits the GBA engine's memory or ROM layout.
- Do not distribute copyrighted ROMs or proprietary assets. Users must supply any legally obtained base files required by their own patching workflow.

## Documentation

- [Engine foundation and implementation roadmap](docs/ENGINE_FOUNDATION.md)
- [Starter game design](docs/GAME_DESIGN.md)
- [Implementation plan](docs/IMPLEMENTATION_PLAN.md)
- [Randomizer settings](config/randomizer.json)
- [Canonical game design configuration](config/game_design.json)
