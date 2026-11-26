# Hoenn–Sinnoh Ultimate Randomizer

A custom Pokémon GBA ROM-hack project targeting one adventure with both Hoenn and Sinnoh, using an Emerald-engine foundation.

## Agreed direction

- Hoenn and Sinnoh open from the beginning.
- A new-game region choice starts the player in Littleroot Town or Twinleaf Town.
- Gym leaders and major battles scale with global progress.
- Three distinct starter species are selected at runtime for each new game.
- Legendary Pokémon can be assigned to eligible encounter slots across both regions.
- Optional Hidden Grottos across both regions contain Ultra Beasts, rare items, or empty discoveries.

## Sinnoh engine foundation

The engine submodule now tracks [LiderMorti00's Sinnoh Pokeemerald Expansion](https://github.com/LiderMorti00/Sinnoh-pokeemerald-expansion), pinned to commit `762efac5eda195c59af3962cb39043c899720dc3`.

That source includes native Emerald-format Sinnoh map data, including Twinleaf Town, Route 201, their map layouts, event scripts, connections, and the wider Platinum map set. The source author describes the project as a playable Platinum demake with some event bugs; our project uses it as an integration foundation, not as proof that the combined Hoenn/Sinnoh game is complete.

The source is included as a Git submodule and retains its upstream history. Credit the original author and contributors when redistributing derived work. Do not commit commercial ROMs or compiled copyrighted game images.

## Current project status

The Sinnoh map source is now available inside `vendor/pokeemerald-expansion`. The next integration milestone is to make the new-game region selector start Sinnoh at Twinleaf while leaving the Hoenn start unchanged, then validate the connected opening sequence and save behavior.

The combined game is **not yet a verified playable build**. CI must validate the imported engine against our existing gameplay overlays and compile a fresh GBA ROM before a test build can be called playable.

## Tests and build

Requires Python 3.10 or newer.

```bash
python -m pip install pytest Pillow
python -m pytest -q
python -m tools.validate_sinnoh_maps --engine-dir vendor/pokeemerald-expansion
python -m tools.integrate_starters --engine-dir vendor/pokeemerald-expansion
make -C vendor/pokeemerald-expansion -j2
```

GitHub Actions checks the Sinnoh map data, applies the existing gameplay overlays, builds the custom ROM, validates its GBA header, and uploads a test artifact. Graphics smoothing and palette-polish steps are intentionally disabled.

## Principles

- Preserve the existing Hoenn start and gameplay unless a change is explicitly required.
- Keep the engine revision pinned; do not build against a moving branch.
- Validate map connections, story flags, and randomizer targets before changing engine data.
- Do not assume every modern feature fits GBA memory or ROM layout.
- Do not distribute copyrighted ROMs or proprietary assets.

## Documentation

- [Engine foundation and integration roadmap](docs/ENGINE_FOUNDATION.md)
- [Starter game design](docs/GAME_DESIGN.md)
- [Implementation plan](docs/IMPLEMENTATION_PLAN.md)
- [Secret Grotto & Ultra Beast spoiler guide](docs/SECRET_GROTTO_GUIDE.md)
- [Sinnoh engine source and build status](docs/UPSTREAM.md)
