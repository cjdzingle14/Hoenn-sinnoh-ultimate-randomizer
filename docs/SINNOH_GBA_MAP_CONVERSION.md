# Sinnoh GBA Map Conversion — First Playable Slice

This branch is focused exclusively on converting Sinnoh maps into engine-compatible GBA maps. Sprite smoothing, palette polish, and other visual polish are out of scope.

## First playable slice
- [ ] Twinleaf Town
- [ ] Route 201 (connected to Twinleaf)

## Conversion requirements
- [ ] Inspect and document the source map/layout, metatiles, tilesets, palette data, object events, warps, and scripts from the Sinnoh source fork.
- [ ] Convert tiles to GBA-compatible tile graphics and palettes (4bpp, indexed palette constraints).
- [ ] Rebuild map layouts and metatile attributes.
- [ ] Implement collision and elevation/behavior attributes.
- [ ] Implement NPC/object events, warps, and map connections needed for the opening slice.
- [ ] Register converted maps in the target engine and route New Game to Twinleaf.
- [ ] Build the ROM and verify both maps in an emulator; confirm walking, collisions, warps, and transitions.
- [ ] Expand only after this slice is playable.

## Source/integration base
Sinnoh-enabled expansion submodule pinned by the integration branch. The map graph manifest is planning-only; these checklist items require actual engine map assets and registrations.
