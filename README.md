# Hoenn–Sinnoh Ultimate Randomizer

A Python-based randomizer project for a Pokémon adventure spanning Hoenn and Sinnoh.

## Project direction

The planned game experience combines both regions in a single connected adventure, with:
- Hoenn and Sinnoh both accessible as part of the main journey.
- Randomized starter choices.
- Gym and major-battle progression that scales with player progress.
- Legendary Pokémon encounter locations randomized across the supported world.
- Mega Evolution support.
- A broad Pokédex target, ultimately covering all Pokémon supported by the selected game engine.

## Current repository layout

The starter project is currently supplied as `hoenn-sinnoh-ultimate-randomizer-starter.zip`. It contains the initial Python package, configuration, tests, and design/implementation documents. Extract the archive into the repository root before running the project.

## Getting started

1. Extract `hoenn-sinnoh-ultimate-randomizer-starter.zip` into this repository.
2. Create a Python 3.11+ virtual environment.
3. Install the project and its development dependencies (see `pyproject.toml`).
4. Run the test suite with `python -m pytest`.

## Development principles

- Keep randomization deterministic when a seed is supplied.
- Validate configuration before changing game data.
- Preserve a reproducible log of the seed and applied settings.
- Keep ROM-specific patching separate from the randomization rules.
- Do not distribute copyrighted game ROMs; users must provide their own legally obtained game files.

## Status

This repository is at the starter/scaffolding stage. The detailed game design and implementation plan are in `docs/` inside the starter archive. The next implementation step is to extract the starter files into the repository root and run the existing tests before extending the randomizer.
