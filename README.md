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

The project applies engine source overlays during CI before compiling the ROM. The starter overlay selects three distinct eligible species at runtime for each new game. The build also integrates runtime wild/trainer randomization, reusable TMs, HM item-based field move access, a rival Poké Ball gift, and streamlined Nurse Joy healing.

The graphics pipeline downloads pinned Gen V-style battle sprites at build time, converts them to the engine's existing GBA dimensions and 4bpp palette limits, and applies a restrained overworld tileset palette grade. It preserves the pinned engine submodule and does not commit downloaded sprite artwork.

This is **not yet the completed two-region game**. Sinnoh maps and travel, live gym scaling, legendary placement, and Hidden Grotto map/event integration still need engine integration.

## Tests and build

Requires Python 3.10 or newer.

\`\`\`bash
python -m pip install pytest Pillow
python -m pytest -q
python -m tools.integrate_starters --engine-dir vendor/pokeemerald-expansion
make -C vendor/pokeemerald-expansion -j2
\`\`\`

GitHub Actions applies the graphics and gameplay overlays, builds the custom ROM, validates its GBA header, and uploads a test artifact.

## Principles

- Seeded subsystems remain reproducible where configured; starter choices are randomized at runtime for each new save.
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
- [Sprite polish and display pipeline](docs/SPRITE_POLISH.md)
- [HD-inspired overworld palette pass](docs/OVERWORLD_POLISH.md)
