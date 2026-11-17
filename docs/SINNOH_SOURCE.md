# Sinnoh Engine Source Audit

Selected reference: [LiderMorti00/Sinnoh-pokeemerald-expansion](https://github.com/LiderMorti00/Sinnoh-pokeemerald-expansion/tree/dd06b332cc5170920dc0be923337dafb7080f327)

Pinned revision: `dd06b332cc5170920dc0be923337dafb7080f327`

## Findings

- The repository is a fork of `rh-hideout/pokeemerald-expansion`.
- Its source tree contains Sinnoh map definitions, GBA layouts, scripts, and related engine data.
- A recursive tree inspection found 334 Sinnoh-related map directories by names for Sinnoh towns, routes, lakes, and post-game areas.
- Examples include Twinleaf Town, Sandgem Town, Jubilife City, Eterna City, Hearthome City, Canalave City, Snowpoint City, and Lake Acuity.
- This is materially more useful than the previous nine-location logical map manifest: it is an existing GBA-engine implementation to audit and integrate.

## Important limitations

This repository is being pinned as the candidate engine source, not yet treated as a finished merge. Its fork may include engine changes and map registrations that conflict with the current project. The existing starter, randomizer, National Dex, and region-selection work must be checked against it before accepting a ROM build.

A successful compile alone is insufficient. Verify the Hoenn start, Sinnoh start, map transitions, event scripts, encounters, trainers, save/load, and randomizer behavior in an emulator.

No Nintendo DS ROM assets are copied by this change.
