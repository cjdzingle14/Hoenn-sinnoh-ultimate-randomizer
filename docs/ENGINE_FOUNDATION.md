# Engine foundation and integration plan

## Selected foundation

Use [RHH's pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion) as the game engine, as selected in the project design.

The upstream project is a decompilation-based GBA ROM-hack development base, not a ready-to-play game. It must be cloned with Git so its commit history and branches are retained. Follow the upstream [installation and build guide](https://github.com/rh-hideout/pokeemerald-expansion/blob/master/INSTALL.md) for the developer's operating system and toolchain.

**Do not copy a commercial Pokémon ROM into this repository.** Each developer must supply any legally obtained source assets or ROM data required by their own local workflow. Do not commit copyrighted ROMs or compiled game images.

## Repository status and integration boundary

At this stage this repository contains a Python randomizer starter archive, project notes, and a GitHub Actions test workflow. It does not yet contain the pokeemerald-expansion source tree. The Python starter and the ROM-hack engine are related project components, but they are not interchangeable:

- The engine contains the game code, maps, scripts, data tables, graphics, and build system.
- The randomizer tooling will eventually generate or apply reproducible changes to supported engine data.
- Shared design/configuration documents should define the intended behavior so that engine changes and randomizer output stay consistent.

Do not claim a playable ROM or an engine integration exists until the upstream source has been added and a clean build has succeeded.

## Target game structure

The design target is one adventure with both Hoenn and Sinnoh available as main-story regions. The implementation should favor a coherent world and progression system over treating Sinnoh as a separate post-game add-on.

### Agreed features

1. **Both regions open:** Hoenn and Sinnoh are both part of the main adventure. The final route and travel graph must make movement between them possible.
2. **Scaled Gym progression:** Gym leaders and major trainers scale according to the player's progression state, not simply a fixed region order.
3. **Randomized starters:** starter choices are selected from the configured eligible pool using a reproducible seed.
4. **Legendary encounters anywhere:** legendary species can be assigned to eligible encounter locations throughout the supported world, subject to configurable encounter rules.
5. **Broad Pokédex coverage:** target all Pokémon supported by the chosen expansion version. Exact species/form coverage must be validated against that version's data.
6. **Mega Evolution:** include Mega Evolution in the design, subject to the selected engine version's supported mechanics and a verified implementation.

## Proposed architecture

Keep the project in separable layers:

- **Upstream engine:** the pinned pokeemerald-expansion revision and its native C/data/build structure.
- **Game data layer:** declarative tables for region/map metadata, Gym progression tiers, starter pools, legendary eligibility, and species/form support.
- **Randomizer core:** deterministic algorithms that accept a seed and validated configuration, then produce a change plan.
- **Engine adapter:** translates the change plan into the exact data/script formats used by the pinned engine revision. It must fail safely when a target symbol, map, species, or table is missing.
- **Validation:** unit tests for rules plus integration checks against the checked-out engine data.
- **Build and packaging:** a reproducible build that outputs a patch or build artifact without committing a copyrighted base ROM.

## Implementation sequence

### Phase 0 — establish a buildable foundation
- Preserve the existing Python starter and its tests.
- Add the upstream project as a Git submodule or documented Git remote after choosing and pinning a stable upstream revision.
- Verify the upstream engine builds unchanged before making game modifications.
- Record the exact upstream revision and toolchain in the repository.

### Phase 1 — inventory and data model
- Inventory the engine's species, forms, maps, warps, encounter tables, Gym leaders, and progression flags.
- Define stable internal IDs for Hoenn and Sinnoh map/route metadata.
- Add schema validation for the game configuration.
- Build a map/warp graph and test that both regions are reachable.

### Phase 2 — progression and content systems
- Implement a progression-state model for scaled Gyms and major battles.
- Implement seeded starter selection and verify identical output for identical seeds.
- Implement legendary placement with eligibility constraints and collision checks.
- Verify species and form coverage against the engine's actual data.

### Phase 3 — Mega Evolution and integration
- Confirm the pinned engine revision's Mega Evolution support and identify any gaps.
- Integrate Mega Evolution without duplicating existing engine functionality.
- Add engine-adapter changes and integration tests.

### Phase 4 — build, patch, and release
- Build the unmodified engine, then the modified game.
- Run automated checks for map connectivity, progression reachability, encounter validity, and deterministic randomization.
- Produce a patch workflow for users to apply to their own legally obtained base files.
- Document installation and troubleshooting.

## Technical constraints

- Pin the upstream engine revision; do not build against a moving branch without recording the exact commit.
- Never assume that every modern Pokémon feature fits in the GBA engine's memory or ROM layout. Check engine limits and build output.
- Treat map connectivity and progression reachability as testable graph problems.
- Keep randomization deterministic: the same configuration and seed must produce the same result.
- Never silently discard unsupported species, forms, moves, abilities, or items; report them in a validation summary.
- Avoid storing or distributing copyrighted ROM images and proprietary game assets.

## Current next step

The next meaningful milestone is to establish a real checkout of pokeemerald-expansion and verify its baseline build. The GitHub file-editing connection can maintain source files and documentation, but a full native engine build requires a build environment with Git, make, and the supported ARM toolchain. That build must be run and its result checked before engine implementation is considered validated.
