# Overworld HD-inspired palette pass

## What this changes

The first overworld graphics pass applies a restrained color grade to the
pinned engine's primary and secondary tileset palettes. It increases color
separation and saturation, then quantizes the result to the Game Boy Advance's
5-bit-per-channel color grid. It preserves palette index zero (transparency),
black and magenta placeholders, and the existing 16-color palette layout.

This is an actual build-time asset change: the integration runs against
`vendor/pokeemerald-expansion/data/tilesets` before the ROM is compiled.
It does not merely create preview images.

## What it deliberately does not change

- Tile PNG artwork or tile dimensions.
- Metatile definitions or tile indices.
- Collision/behavior attributes, map layouts, or animation data.
- Pokémon battle sprites or UI palettes.
- The pinned engine submodule or Test 3 build.

The game remains native GBA resolution (240×160). This is an HD-inspired
color/clarity pass, not true high-resolution rendering. A later art pass can
redraw selected terrain, foliage, water, and building tiles while preserving
their tile slots and metatile behavior; those replacements need visual
in-game review before broad rollout.

## Build integration

The CI engine job runs:

```bash
python -m tools.integrate_overworld_polish --engine-dir vendor/pokeemerald-expansion
```

The operation is repeatable: already quantized palettes are not graded again.
Unit tests cover transparency, reserved colors, palette validation, and
primary/secondary tileset discovery.
