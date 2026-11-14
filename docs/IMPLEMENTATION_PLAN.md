# Implementation Plan

## Phase 0 — repository bootstrap

- [x] Record the agreed game design.
- [x] Add default randomizer settings.
- [x] Add deterministic selection primitives and tests.
- [x] Add settings validation, global progression scoring, Gym tier selection, starter filtering, and protected legendary-slot assignment.
- [x] Add root-level Python package and GitHub Actions test workflow.
- [ ] Import/pin the upstream engine revision after a clean baseline build.

## Phase 1 — engine baseline

1. Clone https://github.com/rh-hideout/pokeemerald-expansion in a separate working directory.
2. Follow the upstream README and toolchain instructions for the exact revision.
3. Build the untouched upstream project and record compiler/tool versions.
4. Pin the upstream commit SHA in docs/UPSTREAM.md.
5. Keep upstream history and license notices intact; avoid copying the engine wholesale into this scaffold before the baseline build is verified.

## Phase 2 — world integration

- Audit Hoenn map groups, map connections, warps, flags, and event scripts.
- Define the Sinnoh map import strategy and map ID allocation.
- Add a region travel hub and test transitions, save/load, and return paths.
- Namespace story flags to prevent Hoenn/Sinnoh collisions.
- Ensure both regions can be entered before either League is completed.

## Phase 3 — progression scaling

- Implement one monotonic global progression score from durable badges and story flags.
- Define Gym tier thresholds and leader rosters in configuration.
- Scale leader parties at battle setup; validate species, moves, items, and levels.
- Test visiting Gyms in either regional order.

## Phase 4 — randomization

- Parse a run seed and versioned settings.
- Use independent PRNG streams per subsystem.
- Randomize three distinct starter choices.
- Randomize eligible wild encounters.
- Place legendary species in eligible slots with rarity and duplicate controls.
- Preserve required story encounters by default.

## Phase 5 — Mega Evolution

- Confirm supported upstream Mega Evolution implementation and data.
- Integrate Mega Stones, form changes, abilities, and battle flow as needed.
- Test player and AI use, transformation/reversion, fainting, switching, and save compatibility.

## Phase 6 — quality and release

- Run automated tests and a clean ROM build.
- Playtest both region orders and all Gym tiers.
- Test randomizer seed reproducibility.
- Document known issues and legal build requirements.
- Produce a patch workflow; do not distribute a copyrighted base ROM.
