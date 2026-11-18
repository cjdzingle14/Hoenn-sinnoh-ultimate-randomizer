# Sprite polish and display pipeline

## Battle sprite integration

The build downloads a pinned revision of the PokeAPI Gen V Black & White sprite
set at build time. It does not commit downloaded image files to this repository.
The integration targets base species with a matching engine asset directory and
complete normal-front, normal-back, and shiny-front sources.

- Front sprites use the source animated GIF when available; the first two frames
  are placed into the engine's existing two-frame vertical sheet. Static fallback
  sprites are repeated into both frames.
- Back sprites keep the engine's existing dimensions.
- Shiny palettes are generated from the matching shiny front source.
- Party icons are updated when the PokeAPI icon source exists; otherwise the
  engine's current icon remains.
- Existing image dimensions are retained. GBA variants are indexed with at most
  15 visible colors plus transparent palette index zero.
- Species with missing source files or unsupported engine layouts are skipped
  rather than partially replaced.

The PokeAPI sprite repository describes its repository license as CC0 but also
states that Pokémon image contents are copyrighted by The Pokémon Company.
Some sprites for species introduced after Generation V are community-created.
Treat the output as copyrighted fan-game material: use it for private testing
and do not redistribute the resulting ROM or source artwork.

## Overworld palette pass

The build also applies a restrained saturation/contrast grade to primary and
secondary overworld tileset palettes. It quantizes colors to the GBA RGB555
grid and preserves transparent palette slot zero and black/magenta placeholders.
It does not redraw terrain, foliage, water, buildings, or tile artwork, and it
does not alter metatiles, collision, map layouts, or animation data.

## GBA limitations

The game remains native 240×160 GBA output. These changes provide a different,
cleaner pixel-art treatment within existing GBA sprite and palette limits; they
are not true HD rendering and do not install an emulator shader. Trainer sprites
and overworld object artwork are not replaced by the PokeAPI battle-sprite pass.
