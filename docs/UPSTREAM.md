# Sinnoh Engine Source

Selected engine source: [LiderMorti00's Sinnoh Pokeemerald Expansion](https://github.com/LiderMorti00/Sinnoh-pokeemerald-expansion)

- Repository: https://github.com/LiderMorti00/Sinnoh-pokeemerald-expansion
- Integration: Git submodule at `vendor/pokeemerald-expansion`
- Branch used to select the source: `master`
- Pinned commit: `762efac5eda195c59af3962cb39043c899720dc3`
- Previous shared pokeemerald-expansion base commit: `4da9230cf7c1f1d7b0d47b45783b202666fffece`
- Pin selected: 2026-11-26
- Build status: not yet verified with this project's gameplay overlays; GitHub Actions is the validation gate.

This repository is a fork of pokeemerald-expansion with Sinnoh map, layout, script, music, trainer, and story additions. The selected pin is an exact commit so the engine cannot silently change when the source branch moves. The submodule preserves the original Git history.

The Sinnoh source author reports Twinleaf Town, Routes 201–230, towns, cities, interiors, dungeons, warps, and story events. Some event scripts are explicitly described by the author as basic and potentially buggy. Treat the source as an integration base that requires testing, not as a guarantee that our combined game already works.

## Verified source landmarks

- `data/maps/TwinleafTown/map.json`
- `data/maps/Route201/map.json`
- `data/layouts/TwinleafTown/map.bin`
- `data/layouts/Route201/map.bin`

The Twinleaf map data connects north to Route 201. Route 201 connects back to Twinleaf and onward toward Sandgem Town. The automated validator checks these key files and connections in CI.

## Checkout

Clone this repository with submodules enabled:

```bash
git clone --recurse-submodules https://github.com/cjdzingle14/Hoenn-sinnoh-ultimate-randomizer.git
cd Hoenn-sinnoh-ultimate-randomizer
git submodule status
```

If the project was already cloned without submodules:

```bash
git submodule sync --recursive
git submodule update --init --recursive
```

## Build and integration gate

1. Check out the exact submodule commit recorded by this repository.
2. Run the Sinnoh map validator.
3. Apply the gameplay overlays and confirm they still match this engine revision.
4. Build the unmodified engine and the modified game.
5. Validate the GBA header and test the opening sequence in an emulator.

Do not call a ROM playable until the custom build succeeds and the Hoenn and Sinnoh starts have both been tested. Do not add commercial Pokémon ROMs or compiled ROM images to this repository.
