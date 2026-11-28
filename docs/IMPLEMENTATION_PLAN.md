# Implementation Plan

## Phase 0 — repository bootstrap
- [x] Record the agreed game design.
- [x] Add default randomizer settings and tests.
- [x] Add GitHub Actions CI.
- [x] Pin the Sinnoh-capable pokeemerald-expansion fork as a Git submodule.

## Phase 1 — Sinnoh source validation
- [x] Confirm native Twinleaf Town and Route 201 map JSON and layouts exist.
- [x] Confirm Twinleaf ↔ Route 201 ↔ Sandgem Town map connections.
- [ ] Complete a clean build with all gameplay overlays.

## Phase 2 — new-game region selector
- [x] Add a new-game choice: A starts Sinnoh; B starts Hoenn.
- [x] Preserve the original Hoenn truck opening.
- [x] Route Sinnoh to Twinleaf Town and the Rowan introduction.
- [ ] Compile and emulator-test both openings, save/load, and new-game resets.

## Phase 3 — world and progression
- [ ] Build and validate the full Sinnoh map/warp graph.
- [ ] Add a region travel hub and test transitions, save/load, and return paths.
- [ ] Implement global progression and scaled Gym rosters.
- [ ] Test visiting Gyms in either regional order.

## Phase 4 — randomizer integration
- [ ] Verify starter, wild, trainer, item, and encounter overlays against the Sinnoh-capable engine.
- [ ] Randomize eligible wild encounters across both regions.
- [ ] Place legendary species in eligible slots with rarity and duplicate controls.
- [ ] Preserve required story encounters by default.

## Phase 5 — Secret Hidden Grottos and Ultra Beasts
- [ ] Audit final Hoenn and Sinnoh map data and assign exact grotto landmarks.
- [ ] Add concealed entrances and environmental clues.
- [x] Keep the tested Python rule layer for deterministic grotto outcomes.
- [ ] Connect grotto rules to in-game event scripts and encounter tables.
- [ ] Test entrances, region order, save/load, and seed reproducibility.

## Phase 6 — quality and release
- [ ] Build the unmodified engine, then the modified game.
- [ ] Run map connectivity, progression reachability, and randomization tests.
- [ ] Playtest both region starts and all Gym tiers.
- [ ] Produce a patch workflow; do not distribute copyrighted base ROMs.
