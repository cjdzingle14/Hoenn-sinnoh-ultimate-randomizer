# Sinnoh reference-ROM audit

## Scope and handling

The supplied reference is a Nintendo DS ROM identified by its header as
`CPUE` (`POKEMON PL`). The audit tool reads the DS filesystem tables and
counts members in selected data archives. It does **not** export or copy map
geometry, textures, sprites, scripts, sound, or other game assets into this
repository.

The Nintendo DS data is not directly compatible with the project's
`pokeemerald-expansion` GBA engine. The intended implementation is a set of
original GBA maps, events, scripts, and warp connections authored against the
pinned engine—not a conversion or redistribution of the DS ROM's proprietary
assets.

## Initial structural findings

The supplied ROM contains these relevant archive families:

| Archive | Members | Purpose to investigate |
|---|---:|---|
| `fielddata/mapmatrix/map_matrix.narc` | 289 | World/map-matrix organization |
| `fielddata/land_data/land_data.narc` | 666 | Land/map data records |
| `fielddata/eventdata/zone_event.narc` | 534 | Per-area event records |
| `fielddata/script/scr_seq.narc` | 1,124 | Field-script records |
| `fielddata/encountdata/pl_enc_data.narc` | 183 | Platinum encounter records |
| `fielddata/areadata/area_data.narc` | 75 | Area metadata |

These are archive member counts, not counts of playable towns or routes. The
records use Nintendo DS-specific formats and need format-aware interpretation
before any map relationships or start coordinates can be relied on.

## GBA implementation direction

The first playable Sinnoh slice should be authored from scratch using the
existing GBA engine's map format and available engine tilesets:

1. A small original village map inspired by the role of Twinleaf Town.
2. The player's home and rival's home as separate interiors.
3. A short route connecting the village to a lake-side story location.
4. A second route to an original research-lab town.
5. Warps, map connections, collision, object events, scripted events, and
   save/load validation.
6. A new-game start selector that routes to a real, compiled GBA map ID.

The exact engine map IDs, tileset IDs, object graphics, script commands, and
warp coordinates must be read from the pinned `pokeemerald-expansion` source
and validated by a successful ROM build. Logical keys such as
`sinnoh_new_game_start` are not valid engine map IDs.

## Local audit command

```bash
python -m tools.inspect_ds_reference "/path/to/your/reference.nds"
```

The command prints a JSON inventory. It does not write extracted game assets.
