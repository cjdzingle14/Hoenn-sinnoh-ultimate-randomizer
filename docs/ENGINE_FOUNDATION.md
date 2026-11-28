# Engine foundation and integration plan

## Selected foundation

Use [LiderMorti00's Sinnoh Pokeemerald Expansion](https://github.com/LiderMorti00/Sinnoh-pokeemerald-expansion), a pokeemerald-expansion fork containing native GBA-format Sinnoh maps, layouts, scripts, and story data.

The engine is included as a Git submodule at `vendor/pokeemerald-expansion`, pinned to commit `762efac5eda195c59af3962cb39043c899720dc3`. See [UPSTREAM.md](UPSTREAM.md) for source details and build validation.

**Do not copy a commercial Pokémon ROM into this repository.** Do not commit copyrighted ROM images or proprietary assets.

## Repository status and integration boundary

This repository contains:
- A Python randomizer package with deterministic selection primitives.
- Validated settings, progression scoring, Gym-tier selection, starter filtering, and legendary placement rules.
- GitHub Actions CI and a pinned Sinnoh-capable engine submodule.
- Native Sinnoh map source including Twinleaf Town and Route 201.

The source maps are present in the engine; that does not yet mean the combined game is integrated. The region selector, separate region story state, map transition graph, and save/load behavior still require implementation and validation.

## Target game structure

One adventure should offer both Hoenn and Sinnoh as main-story regions. On a fresh game, the player chooses a starting region:
- Hoenn starts in Littleroot Town with the existing Hoenn opening unchanged.
- Sinnoh starts in Twinleaf Town and follows the Sinnoh opening sequence.

The two regions must ultimately be connected and share a global progression model without colliding story flags.

## Implementation sequence

### Phase 0 — repository foundation
- [x] Record agreed game design and feature requirements.
- [x] Add the Python randomizer package and tests.
- [x] Add GitHub Actions CI.
- [x] Pin the Sinnoh-capable pokeemerald-expansion fork as a Git submodule.

### Phase 1 — Sinnoh source validation
- [x] Confirm native Twinleaf Town and Route 201 map JSON and layouts exist.
- [x] Confirm the map data includes Twinleaf ↔ Route 201 connections.
- [ ] Run CI against all existing gameplay overlays and fix any engine-version incompatibilities.
- [ ] Complete an unchanged engine baseline build and record toolchain details.

### Phase 2 — region selection and opening sequence
- [ ] Add a new-game region selector with Hoenn and Sinnoh choices.
- [ ] Keep the current Hoenn start in Littleroot Town unchanged.
- [ ] Route a Sinnoh selection to Twinleaf Town with the correct player spawn and facing.
- [ ] Initialize region-specific story variables and flags without collisions.
- [ ] Verify the Sinnoh opening sequence through Route 201 and the first visit to Sandgem Town.
- [ ] Test new save, reset, save/load, and both region selections.

### Phase 3 — world and progression
- [ ] Build and validate the Sinnoh map/warp graph.
- [ ] Add a region travel hub and test transitions, save/load, and return paths.
- [ ] Implement global progression and scaled Gym rosters.
- [ ] Test visiting Gyms in either regional order.

### Phase 4 — randomizer integration
- [ ] Verify starter, wild, trainer, item, and encounter overlays against the Sinnoh-capable engine.
- [ ] Randomize eligible wild encounters across both regions.
- [ ] Place legendary species in eligible slots with rarity and duplicate controls.
- [ ] Preserve required story encounters by default.

### Phase 5 — Secret Hidden Grottos and Ultra Beasts
- [ ] Audit final Hoenn and Sinnoh map data and assign exact grotto landmarks.
- [ ] Add concealed entrances and environmental clues.
- [x] Keep the tested Python rule layer for deterministic grotto outcomes.
- [ ] Connect grotto rules to in-game event scripts and encounter tables.
- [ ] Test entrances, region order, save/load, and seed reproducibility.

### Phase 6 — quality and release
- [ ] Build the unmodified engine, then the modified game.
- [ ] Run map connectivity, progression reachability, and randomization tests.
- [ ] Playtest both region starts and all Gym tiers.
- [ ] Produce a patch workflow; do not distribute copyrighted base ROMs.

## Technical constraints

- Keep the engine revision pinned; do not silently follow a moving branch.
- Check every symbol and data format before applying overlays.
- Treat map connectivity and progression reachability as testable graph problems.
- Keep randomization deterministic where configured.
- Avoid storing or distributing copyrighted ROM images or proprietary assets.
