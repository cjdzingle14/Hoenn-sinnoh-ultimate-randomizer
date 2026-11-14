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

**The repository contains the first runnable Python randomizer rules package and a pinned engine submodule. It is not yet a playable ROM hack.**

Implemented in the root project:
- Stable, independent random-number streams based on a user seed.
- Deterministic distinct selection and weighted selection primitives.
- Settings validation for the two-region world, Gym scaling, starters, legendary duplicate policy, and Mega Evolution toggle.
- A monotonic global progression score and Gym-tier selection helper.
- Starter selection with banned-species filtering.
- Legendary encounter assignment with protected story slots and duplicate policy.
- Unit tests and a GitHub Actions test workflow.
- RHH pokeemerald-expansion pinned as a Git submodule at a recorded upstream commit.

The engine submodule has not yet passed a baseline build, and no modified GBA ROM has been built. See [the engine foundation and integration roadmap](docs/ENGINE_FOUNDATION.md) and [the upstream pin/build instructions](docs/UPSTREAM.md).

## Run the randomizer tests

Requires Python 3.10 or newer.

```bash
python -m pip install pytest
python -m pytest -q
```

GitHub Actions runs this test suite on pushes to main, pull requests to main, and manual dispatch.

## Clone the complete project

Use recursive cloning so the pinned engine source is checked out too:

```bash
git clone --recurse-submodules https://github.com/cjdzingle14/Hoenn-sinnoh-ultimate-randomizer.git
cd Hoenn-sinnoh-ultimate-randomizer
git submodule status
```

If you already cloned without submodules, run:

```bash
git submodule update --init --recursive
```

## Engine foundation

The selected game engine is [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion), included as a submodule at the exact revision recorded in [docs/UPSTREAM.md](docs/UPSTREAM.md). Follow the upstream installation and build instructions for that pinned revision. Build the unmodified engine first; do not start engine-specific changes until the baseline build succeeds.

## Development principles

- The same seed and versioned settings must reproduce the same result.
- Independent PRNG streams prevent unrelated settings from reshuffling other systems.
- Validate settings and engine targets before changing game data.
- Record the seed, settings, and upstream engine revision for reproducibility.
- Never assume every modern Pokémon feature fits the GBA engine's memory or ROM layout.
- Do not distribute copyrighted ROMs or proprietary assets. Users must supply any legally obtained base files required by their own patching workflow.

## Documentation

- [Engine foundation and integration roadmap](docs/ENGINE_FOUNDATION.md)
- [Starter game design](docs/GAME_DESIGN.md)
- [Implementation plan](docs/IMPLEMENTATION_PLAN.md)
- [Upstream engine pin and build status](docs/UPSTREAM.md)
- [Randomizer settings](config/randomizer.json)
- [Canonical game design configuration](config/game_design.json)
