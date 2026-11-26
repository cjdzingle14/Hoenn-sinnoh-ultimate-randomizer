# Hoenn–Sinnoh Ultimate Randomizer

A custom Pokémon GBA ROM-hack project targeting one adventure with both Hoenn and Sinnoh, using an Emerald-engine foundation.

## Agreed direction

- Hoenn and Sinnoh open from the beginning.
- A new-game choice selects Hoenn (Littleroot) or Sinnoh (Twinleaf).
- Gym leaders and major battles scale with global progress.
- Three distinct starter species are selected at runtime for each new game.
- Legendary Pokémon can be assigned to eligible encounter slots across both regions.
- Optional Hidden Grottos across both regions contain Ultra Beasts, rare items, or empty discoveries.

## Sinnoh engine foundation

The engine submodule tracks [LiderMorti00's Sinnoh Pokeemerald Expansion](https://github.com/LiderMorti00/Sinnoh-pokeemerald-expansion), pinned to commit `762efac5eda195c59af3962cb39043c899720dc3`.

The source includes native Emerald-format Sinnoh maps, layouts, events, and story data. The project now validates Twinleaf Town and Route 201 and integrates a new-game selector: press **A** for Sinnoh or **B** for Hoenn. Hoenn retains the original truck opening; Sinnoh uses the Twinleaf opening and Rowan intro.

The selector and combined build still require automated compilation and emulator testing before the game can be called playable. Credit the original source author and contributors. Do not commit commercial ROMs or compiled copyrighted game images.

## Tests and build

```bash
python -m pip install pytest Pillow
python -m pytest -q
python -m tools.validate_sinnoh_maps --engine-dir vendor/pokeemerald-expansion
python -m tools.integrate_region_selector --engine-dir vendor/pokeemerald-expansion
make -C vendor/pokeemerald-expansion -j2
```

Graphics smoothing and palette-polish stages are intentionally disabled.

## Documentation

- [Engine foundation and integration roadmap](docs/ENGINE_FOUNDATION.md)
- [Starter game design](docs/GAME_DESIGN.md)
- [Implementation plan](docs/IMPLEMENTATION_PLAN.md)
- [Secret Grotto & Ultra Beast spoiler guide](docs/SECRET_GROTTO_GUIDE.md)
- [Sinnoh engine source and build status](docs/UPSTREAM.md)
