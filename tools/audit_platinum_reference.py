"""Read-only structural inventory of a user-supplied Nintendo DS ROM.

This tool does not extract or redistribute game assets. It reads the NDS header,
NitroFS filename table, and FAT to report the presence and sizes of map-related
archives so an engine-import plan can be based on the supplied reference file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

MAP_RELATED_PREFIXES = ("fielddata/",)
MAP_RELATED_NAMES = {
    "fielddata/areadata/area_data.narc",
    "fielddata/areadata/area_build_model/area_build.narc",
    "fielddata/areadata/area_build_model/areabm_texset.narc",
    "fielddata/areadata/area_map_tex/map_tex_set.narc",
    "fielddata/areadata/area_move_model/move_model_list.narc",
    "fielddata/build_model/build_model.narc",
    "fielddata/encountdata/d_enc_data.narc",
    "fielddata/encountdata/p_enc_data.narc",
    "fielddata/encountdata/pl_enc_data.narc",
    "fielddata/eventdata/zone_event.narc",
    "fielddata/land_data/land_data.narc",
    "fielddata/mapmatrix/map_matrix.narc",
    "fielddata/maptable/mapname.bin",
    "fielddata/mm_list/move_model_list.narc",
    "fielddata/script/scr_seq.narc",
}


def read_nitrofs(data: bytes) -> list[dict]:
    fnt_offset, fnt_size = struct.unpack_from("<II", data, 0x40)
    fat_offset, fat_size = struct.unpack_from("<II", data, 0x48)
    if not fnt_size or not fat_size or fnt_offset + fnt_size > len(data):
        raise ValueError("ROM has invalid or missing NitroFS tables")
    if fat_offset + fat_size > len(data) or fat_size % 8:
        raise ValueError("ROM has an invalid FAT")

    fnt = data[fnt_offset:fnt_offset + fnt_size]
    directory_count = struct.unpack_from("<H", fnt, 6)[0]
    if not directory_count or directory_count * 8 > len(fnt):
        raise ValueError("ROM has an invalid FNT directory table")
    directories = [struct.unpack_from("<IHH", fnt, i * 8)
                   for i in range(directory_count)]
    fat = [struct.unpack_from("<II", data, fat_offset + i * 8)
           for i in range(fat_size // 8)]
    files: list[dict] = []
    visited: set[int] = set()

    def walk(directory_id: int, prefix: str = "") -> None:
        index = directory_id & 0x0FFF
        if index >= len(directories) or index in visited:
            raise ValueError("ROM has an invalid or cyclic FNT directory")
        visited.add(index)
        subtable_offset, first_file_id, _ = directories[index]
        if subtable_offset >= len(fnt):
            raise ValueError("ROM has an out-of-range FNT subtable")
        pos = subtable_offset
        file_id = first_file_id
        while pos < len(fnt):
            entry = fnt[pos]
            pos += 1
            if entry == 0:
                break
            is_directory = bool(entry & 0x80)
            name_length = entry & 0x7F
            name_bytes = fnt[pos:pos + name_length]
            if len(name_bytes) != name_length:
                raise ValueError("ROM has a truncated FNT filename")
            name = name_bytes.decode("ascii", "replace")
            pos += name_length
            path = prefix + name
            if is_directory:
                if pos + 2 > len(fnt):
                    raise ValueError("ROM has a truncated FNT directory entry")
                child_id = struct.unpack_from("<H", fnt, pos)[0]
                pos += 2
                walk(child_id, path + "/")
            else:
                if file_id >= len(fat):
                    raise ValueError("ROM FNT references a missing FAT entry")
                start, end = fat[file_id]
                if end < start or end > len(data):
                    raise ValueError("ROM FAT contains an invalid file range")
                files.append({"path": path, "file_id": file_id,
                              "offset": start, "size": end - start})
                file_id += 1
        else:
            raise ValueError("ROM FNT directory has no terminator")

    walk(0xF000)
    return files


def audit_rom(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < 0x160:
        raise ValueError("File is too small to be a Nintendo DS ROM")
    game_code = data[0x0C:0x10].decode("ascii", "replace")
    files = read_nitrofs(data)
    selected = [item for item in files
                if item["path"] in MAP_RELATED_NAMES]
    return {
        "file": path.name,
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "game_title": data[0:12].rstrip(b"\\0 ").decode("ascii", "replace"),
        "game_code": game_code,
        "revision": data[0x1E],
        "nitrofs_file_count": len(files),
        "map_related_files": selected,
        "asset_policy": "inventory only; no game assets are extracted or copied",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path, help="path to a user-supplied .nds file")
    args = parser.parse_args()
    print(json.dumps(audit_rom(args.rom), indent=2))


if __name__ == "__main__":
    main()
