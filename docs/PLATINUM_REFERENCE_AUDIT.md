# Platinum reference ROM audit

## Input inspected

A user-supplied file named `Platinum Reforged (v0.3.0-alpha).nds` was inspected locally as a structural reference only.

- Container: Nintendo DS ROM image
- Internal game title: `POKEMON PL`
- Game code: `CPUE`
- Revision byte: `1`
- File size: 268,435,456 bytes (256 MiB)
- SHA-256: `ee8fe7b8db1003be22fd2fd3cf43537c14d1cbb49c2dc5736636d60682dd79a6`
- NitroFS inventory: 774 files

The audit reads the NDS header, NitroFS filename table, and FAT. It does not unpack, copy, or commit game assets.

## Map and field-data structures found

The ROM's NitroFS contains the following relevant paths:

| Purpose | Reference file | Size |
|---|---|---:|
| Map/area metadata | `fielddata/areadata/area_data.narc` | 1,252 B |
| Area/building models | `fielddata/areadata/area_build_model/area_build.narc` | 6,468 B |
| Area model textures | `fielddata/areadata/area_build_model/areabm_texset.narc` | 1,617,848 B |
| Area map textures | `fielddata/areadata/area_map_tex/map_tex_set.narc` | 1,872,684 B |
| Movement model list | `fielddata/areadata/area_move_model/move_model_list.narc` | 1,432 B |
| Field/building models | `fielddata/build_model/build_model.narc` | 2,250,892 B |
| Diamond/Pearl encounter archive | `fielddata/encountdata/d_enc_data.narc` | 79,108 B |
| Platinum encounter archive | `fielddata/encountdata/pl_enc_data.narc` | 79,108 B |
| Zone events | `fielddata/eventdata/zone_event.narc` | 157,928 B |
| Land/map data | `fielddata/land_data/land_data.narc` | 16,125,840 B |
| Map matrices/connections | `fielddata/mapmatrix/map_matrix.narc` | 13,052 B |
| Map names | `fielddata/maptable/mapname.bin` | 9,488 B |
| Field scripts | `fielddata/script/scr_seq.narc` | 307,448 B |

These are Nintendo DS-specific containers and formats. Their presence confirms that the reference ROM has separate map geometry/land data, map matrices, zone events, scripts, and encounter data. It does **not** mean those files can be dropped into pokeemerald-expansion.

## GBA implementation decision

The target project uses the pinned `pokeemerald-expansion` GBA engine. A Nintendo DS map archive is not a compatible GBA map set: map layouts, tilesets, palettes, event formats, script bytecode, object models, and runtime assumptions differ.

Therefore the safe implementation path is:

1. Use the supplied Platinum build as a **visual and structural reference** for Sinnoh geography, route order, town connections, landmarks, and event-flow planning.
2. Create original GBA-native Sinnoh maps, tilesets, object placements, scripts, and map connections for the target engine. Do not copy or commit proprietary Platinum assets or extracted ROM data.
3. Assign engine-native map IDs and names only after the new maps exist in the GBA project.
4. Add a region-selection screen to the genuine New Game flow, save the selected opening region, and route to the verified Hoenn or Sinnoh start map.
5. Add a two-way travel hub so both regions remain open in the same save, regardless of the selected opening region.
6. Test both openings, travel in both directions, save/load, and the first starter sequence before producing a playable test ROM.

## Current blockers and boundaries

- The ROM audit identifies the reference's relevant map-data containers, but no individual Sinnoh map has yet been converted to a GBA-native layout.
- The region-choice branch currently has logical configuration and unit tests only; it does not yet alter the playable ROM's New Game flow.
- The project must first have a verified clean build of the pinned GBA engine before engine-side map and menu changes can be validated.
- The original NDS file remains local to the user's environment; this repository receives only this audit and the read-only inventory tool, not the ROM or its extracted assets.

## Repeatable audit

Run:

```bash
python -m tools.audit_platinum_reference "/path/to/Platinum Reforged (v0.3.0-alpha).nds"
```

The command reports the header identity, file hash, NitroFS file count, and selected map-related filenames/sizes. It does not extract any content.
