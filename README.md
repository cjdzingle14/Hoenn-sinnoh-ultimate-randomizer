# Hoenn–Sinnoh Ultimate Randomizer

A custom Pokémon GBA ROM-hack project targeting one adventure with both Hoenn and Sinnoh, using [RHH's pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion).

## Agreed direction

- Hoenn and Sinnoh open from the beginning.
- Gym leaders and major battles scale with global progress.
- Three distinct starter species are selected reproducibly from the eligible pool.
- Legendary Pokémon can be assigned to eligible encounter slots across both regions.
- Mega Evolution uses support from the pinned engine revision.
- Pokédex coverage targets species and forms supported by that engine revision.
- Optional secret Hidden Grottos across both regions contain seeded Ultra Beast encounters, rare items, or empty discoveries.

## Current implementation

The project now has its first engine gameplay integration in CI. Before compiling, the workflow applies a source overlay to the pinned engine: it chooses three distinct non-Legendary base species from the engine species enum using the configured seed, replaces the starter selection array, and corrects the starter index upper-bound check. The submodule remains pinned and unchanged in Git.

This is **not yet the completed two-region game**. Sinnoh maps and travel, live gym scaling, wild encounter randomization, legendary placement, and Hidden Grotto map/event integration still need engine integration.

## Tests and build

Requires Python 3.10 or newer.

```bash
python -m pip install pytest
python -m pytest -q
python -m tools.integrate_starters --engine-dir vendor/pokeemerald-expansion
make -C vendor/pokeemerald-expansion -j2
```

The default seed comes from config/randomizer.json. Change its seed to generate a different reproducible trio. GitHub Actions builds and uploads the custom starter-integration ROM on pushes to main.

## Principles

- The same seed and versioned settings reproduce the same result.
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
