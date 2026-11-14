# Sprite polish and display pipeline

## Target

The first graphics pass targets Pokémon battle front/back sprites, icons, and
GBA-converted Pokémon palette assets in the pinned `pokeemerald-expansion` engine.
Trainer graphics are reserved for a later pass. The game remains
a native GBA 240×160 render; no emulator-side shader is required.

## Why this is asset-first

Pizza Boy A Basic is the target emulator. This project will not rely on a custom
shader being available in that edition. Any visual improvements must be baked
into valid game assets or supported by the GBA renderer itself.

GBA sprite assets are constrained: Pokémon pictures are generally indexed
4bpp graphics with a maximum of 16 palette entries. Applying ordinary blur,
bilinear scaling, or unrestricted RGB filters can destroy pixel edges, exceed
palette limits, or break the engine's graphics conversion. The pipeline
therefore starts with a non-destructive audit and nearest-neighbor previews.

## First-pass tool

Install Pillow in the local Python environment, then run from the repository
root after checking out the submodule:

```bash
python -m pip install Pillow
python -m tools.sprite_polish --engine-dir vendor/pokeemerald-expansion
python -m tools.sprite_polish --engine-dir vendor/pokeemerald-expansion --preview-dir /tmp/sprite-previews --scale 3
python -m tools.sprite_polish --engine-dir vendor/pokeemerald-expansion --palette-preview-dir /tmp/palette-previews
```

- The audit checks explicit GBA-converted Pokémon PNGs (`*_gba.png`) for
  more than 15 visible colors or missing transparent pixels. Source artwork
  and non-GBA preview assets are deliberately excluded.
- Preview output uses nearest-neighbor scaling only, preserving hard pixel
  edges. It writes to a separate directory and never overwrites source assets.
- Optional palette previews apply a restrained saturation/contrast grade to
  slots 1–15 while preserving slot 0; candidates are written separately and
  are never installed automatically.
- Warnings are review items, not automatic failures; verify any flagged asset
  against the engine's actual graphics conversion rules before changing it.

## Visual polish rules

1. Preserve original Pokémon designs, silhouettes, animation frames, and sprite
   dimensions used by the engine.
2. Keep battle assets within the engine's palette and compression constraints.
3. Avoid blur, bilinear filtering, AI redraws, and global recoloring.
4. Compare front/back sprites, icons, and overworld appearances together so
   palette changes remain consistent.
5. Only replace an asset after checking it in-game and rebuilding the ROM.

## Shader note

A GBA ROM cannot install a modern GPU shader into an emulator. A shader is an
emulator display effect, not a Pokémon sprite property. Since Pizza Boy A Basic
may not expose user shader controls, this project prioritizes crisp indexed
assets and avoids promising an unsupported emulator option. A later optional
GBA-side palette/shading effect would need to be designed around the engine's
palette and performance limits and tested on hardware/emulators.

## Safety gate

This pass does not overwrite upstream graphics or change the pinned submodule.
The next step after the audit is to inspect representative sprite sheets and
palettes, then compare the optional palette-grade candidates in-game before deciding
  whether any should become an actual asset change.
