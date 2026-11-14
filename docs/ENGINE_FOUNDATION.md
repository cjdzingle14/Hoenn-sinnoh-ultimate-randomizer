# Engine foundation and integration plan

## Selected foundation

Use [RHH's pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion) as the game engine, as selected in the project design.

The upstream project is a decompilation-based GBA ROM-hack development base, not a ready-to-play game. It is included in this repository as a Git submodule at `vendor/pokeemerald-expansion`, pinned to commit `4da9230cf7c1f1d7b0d47b45783b202666fffece`. See [UPSTREAM.md](UPSTREAM.md) for recursive clone instructions and the baseline build gate.

**Do not copy a commercial Pokémon ROM into this repository.** Users must supply any legally obtained source assets or ROM data required by their own local workflow. Do not commit copyrighted ROMs or compiled game images.

## Repository status and integration boundary

This repository now contains:
- A Python randomizer package with deterministic selection primitives.
- Validated settings, progression scoring, Gym-tier selection, starter filtering, and legendary placement rules.
- Unit tests and GitHub Actions CI.
- The pinned pokeemerald-expansion Git submodule.
- Project design and integration documentation.

The engine submodule is present but its unmodified baseline build has not yet been run. The Python randomizer and the ROM-hack engine are related project components, but they are not interchangeable:

- The engine contains game code, maps, scripts, data tables, graphics, and the build system.
- The randomizer tooling will generate or apply reproducible changes to supported engine data.
- Shared design/configuration documents define intended behavior so engine changes and randomizer output stay consistent.

Do not claim a playable ROM or engine integration is complete until the upstream baseline and modified game both build successfully.

## Target game structure

The design target is one adventure with both Hoenn and Sinnoh available as main-story regions. The implementation should favor a coherent world and progression system over treating Sinnoh as a separate post-game add-on.

### Agreed features

1. **Both regions open:** Hoenn and Sinnoh are both part of the main adventure. The final route and travel graph must make movement between them possible.
2. **Scaled Gym progression:** Gym leaders and major trainers scale according to the player's progression state, not simply a fixed region order.
3. **Randomized starters:** starter choices are selected from the configured eligible pool using a reproducible seed.
4. **Legendary encounters anywhere:** legendary species can be assigned to eligible encounter locations throughout the supported world, subject to configurable encounter rules.
5. **Broad Pokédex coverage:** target all Pokémon supported by the pinned expansion version. Exact species/form coverage must be validated against that version's data.
6. **Mega Evolution:** include Mega Evolution in the design, subject to the selected engine revision's supported mechanics and a verified implementation.

## Proposed architecture

Keep the project in separable layers:

- **Upstream engine:** pinned pokeemerald-expansion revision and its native C/data/build structure.
- **Game data layer:** declarative tables for region/map metadata, Gym progression tiers, starter pools, legendary eligibility, and species/form support.
- **Randomizer core:** deterministic algorithms that accept a seed and validated configuration, then produce a change plan.
- **Engine adapter:** translates the change plan into the exact data/script formats used by the pinned engine revision. It must fail safely when a target symbol, map, species, or table is missing.
- **Validation:** unit tests for rules plus integration checks against the checked-out engine data.
- **Build and packaging:** reproducible build that outputs a patch or build artifact without committing a copyrighted base ROM.

## Implementation sequence

### Phase 0 — repository foundation
- [x] Record agreed game design and feature requirements.
- [x] Add the Python randomizer package and settings.
- [x] Add deterministic rules and unit tests.
- [x] Add GitHub Actions CI.
- [x] Add pokeemerald-expansion as a pinned Git submodule.
- [ ] Run an unchanged upstream baseline build and record toolchain details.

### Phase 1 — engine inventory
- Inventory engine species, forms, maps, warps, encounter tables, Gym leaders, and progression flags.
- Define stable internal IDs for Hoenn and Sinnoh map/route metadata.
- Define schema validation for engine-backed game configuration.
- Build a map/warp graph and test that both regions are reachable.

### Phase 2 — world and progression
- Design Sinnoh map import strategy and map ID allocation.
- Add a region travel hub and test transitions, save/load, and return paths.
- Namespace story flags to prevent Hoenn/Sinnoh collisions.
- Implement global progression and scaled Gym rosters.
- Test visiting Gyms in either regional order.

### Phase 3 — randomizer integration
- Implement engine data extraction and adapter.
- Randomize three distinct starter choices.
- Randomize eligible wild encounters.
- Place legendary species in eligible slots with rarity and duplicate controls.
- Preserve required story encounters by default.

### Phase 4 — Mega Evolution and coverage
- Confirm supported upstream Mega Evolution implementation and data.
- Verify species, forms, stones, abilities, and battle hooks.
- Validate species/form coverage against the pinned engine.

### Phase 5 — build, test, and release
- Build the unmodified engine, then the modified game.
- Run automated checks for map connectivity, progression reachability, encounter validity, and deterministic randomization.
- Produce a patch workflow for users to apply to their own legally obtained base files.
- Document installation and troubleshooting.

## Technical constraints

- Keep the upstream engine revision pinned; do not build against a moving branch without recording the exact commit.
- Never assume every modern Pokémon feature fits in the GBA engine's memory or ROM layout. Check engine limits and build output.
- Treat map connectivity and progression reachability as testable graph problems.
- Keep randomization deterministic: the same configuration and seed must produce the same result.
- Never silently discard unsupported species, forms, moves, abilities, or items; report them in a validation summary.
- Avoid storing or distributing copyrighted ROM images and proprietary game assets.

## Current next step

The upstream source is now pinned as a Git submodule. The next major milestone is to clone this repository recursively in a supported development environment, install the pinned engine's toolchain, and run an unchanged baseline build. Only after that succeeds should engine-specific modifications begin.
