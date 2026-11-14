# Hoenn–Sinnoh Ultimate Randomizer

A custom Pokémon GBA ROM-hack project targeting one adventure with both Hoenn and Sinnoh, using [RHH's pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion).

## Agreed direction

- Hoenn and Sinnoh open from the beginning.
- Gym leaders and major battles scale with global progress.
- Three distinct starter species are selected from the eligible non-Legendary pool at runtime for each new game; the selected Pokémon remains part of that save.
- Legendary Pokémon can be assigned to eligible encounter slots across both regions.
- Mega Evolution uses support from the pinned engine revision.
- Pokédex coverage targets species and forms supported by that engine revision.
- Optional secret Hidden Grottos across both regions contain seeded Ultra Beast encounters, rare items, or empty discoveries.

## Current implementation

The project now has its first engine gameplay integrations in CI. Before compiling, the workflow applies source overlays to the pinned engine. The starter overlay builds a pool of eligible non-Legendary base species and selects three distinct options using the game's runtime random-number generator whenever a new game enters starter selection. This avoids reusing the same build-time trio across every new save. The submodule remains pinned and unchanged in Git.

This is **not yet the completed two-region game**. Sinnoh maps and travel, live gym scaling, wild encounter randomization, legendary placement, and Hidden Grotto map/event integration still need engine integration.

## Tests and build

Requires Python 3.10 or newer.

```bash
python -m pip install pytest
python -m pytest -q
python -m tools.integrate_starters --engine-dir vendor/pokeemerald-expansion
make -C vendor/pokeemerald-expansion -j2
```

Starter choices now use runtime game randomness rather than the configured build seed. GitHub Actions builds and uploads the custom ROM on pushes to main.

## Principles

- Seeded subsystems remain reproducible where configured; starter choices are randomized at runtime for each new game.
- Independent PRNG streams keep unrelated systems stable.
- Validate settings and engine targets before changing game data.
- Do not assume every modern feature fits GBA memory or ROM layout.
- Do not distribute copyrighted ROMs or proprietary assets.

## Documentation

- [Engine foundation and integration roadmap](docs/ENGINE_FOUNDATION.md)
- [Starter game design](docs/GAME_DESIGN.md)
- [Implementation plan](docs/IMPLEMENTATION_PLAN.md)
- [Secret Grotto & Ultra Beast spoiler guide](docs/SECRET_GROTTO_GUIDE.md)
- [Upstream engine pin and build status](docs/UPSTREAM.md)
