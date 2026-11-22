# Overworld HD-inspired palette pass

## What this changes

The first overworld graphics pass applies a restrained color grade to the
pinned engine's primary and secondary tileset palettes. It increases color
separation and saturation, then quantizes the result to the Game Boy Advance's
5-bit-per-channel color grid. It preserves palette index zero (transparency),
black and magenta placeholders, and the existing 16-color palette layout.

This is a build-time asset change against
`vendor/pokeemerald-expansion/data/tilesets`, not a preview-only operation.

## What it does not change

- Tile PNG artwork or tile dimensions.
- Metatile definitions or tile indices.
- Collision/behavior attributes, map layouts, or animation data.
- Pokémon battle sprites or UI palettes.

The game remains native GBA resolution (240×160). This is an HD-inspired
color/clarity pass, not true high-resolution rendering. A later art pass can
redraw selected terrain, foliage, water, and building tiles while preserving
their tile slots and metatile behavior; those replacements need in-game review.

The operation is repeatable: already quantized palettes are not graded again.
