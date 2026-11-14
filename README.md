# Hoenn–Sinnoh Ultimate Randomizer

A custom Pokémon GBA ROM-hack project targeting a single adventure that includes both Hoenn and Sinnoh. The selected engine foundation is [RHH's pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion).

## Project direction

The planned game experience combines both regions in one connected main adventure, with:

- Hoenn and Sinnoh both accessible during the main journey.
- Gym leaders and major battles that scale with player progression.
- Randomized starter choices.
- Legendary Pokémon encounters randomized across eligible locations throughout the world.
- Mega Evolution.
- Broad Pokédex coverage for the species and forms supported by the selected engine revision.

## Current status

**This project is in the foundation/scaffolding stage; it is not yet a playable ROM hack.**

The repository currently includes:

- The original Python randomizer starter archive.
- A GitHub Actions workflow that extracts the starter and runs its Python tests.
- Project-level design and engine integration documentation.

The pokeemerald-expansion source tree has not yet been added to this repository, and no modified game has been built. See [the engine foundation and integration roadmap](docs/ENGINE_FOUNDATION.md) for the architecture, constraints, and implementation phases.

## Getting started with the current starter

1. Extract `hoenn-sinnoh-ultimate-randomizer-starter.zip` into a working directory.
2. Use Python 3.11 or newer.
3. Install the project and its development dependencies as described in the starter's `pyproject.toml`.
4. Run `python -m pytest -q` from the extracted project directory.

The GitHub Actions workflow runs these starter tests on pushes to `main`, pull requests to `main`, and manual dispatch. A configured workflow is not proof that the tests passed; check the Actions run for its result.

## Engine foundation

The game engine is [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion). Follow its upstream [installation and build instructions](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md). Clone it with Git rather than downloading a source ZIP, because its commit history is needed for ongoing development.

The intended integration is to pin a known upstream revision, verify an unchanged baseline build, then add the Hoenn/Sinnoh world, progression systems, randomizer adapter, and game features in tested stages.

## Development principles

- Keep randomization deterministic when a seed is supplied.
- Validate configuration and engine targets before changing game data.
- Record the seed, settings, and upstream engine revision for reproducibility.
- Keep randomizer rules separate from engine-specific patching.
- Check engine memory, ROM-size, and data-table limits rather than assuming every feature fits.
- Do not distribute copyrighted game ROMs or proprietary assets. Users must provide any legally obtained base files required by their own patching workflow.

## Documentation

- [Engine foundation and implementation roadmap](docs/ENGINE_FOUNDATION.md)
- [Original starter archive](hoenn-sinnoh-ultimate-randomizer-starter.zip)
