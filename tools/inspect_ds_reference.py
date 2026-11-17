"""Inspect a user-supplied Nintendo DS ROM without extracting game assets.

The report records filesystem paths, archive member counts, and basic map
matrix identifiers. It deliberately does not export graphics, maps, scripts,
or other copyrighted game content.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path

TARGET_ARCHIVES = {
    "fielddata/areadata/area_data.narc",
    "fielddata/encountdata/pl_enc_data.narc",
    "fielddata/eventdata/zone_event.narc",
    "fielddata/land_data/land_data.narc",
    "fielddata/mapmatrix/map_matrix.narc",
    "fielddata/script/scr_seq.narc",
}


class RomFormatError(ValueError):
    """Raised when a supplied ROM has invalid Nintendo DS filesystem data."""


def _u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def _u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def _parse_nitrofs(data: bytes) -> dict[str, tuple[int, int]]:
    if len(data) < 0x50:
        raise RomFormatError("file is too small to contain a Nintendo DS header")
    fnt_offset, fnt_size = struct.unpack_from("<II", data, 0x40)
    fat_offset, fat_size = struct.unpack_from("<II", data, 0x48)
    if not fnt_size or not fat_size or fat_size % 8:
        raise RomFormatError("Nintendo DS FNT/FAT header values are invalid")
    if fnt_offset + fnt_size > len(data) or fat_offset + fat_size > len(data):
        raise RomFormatError("Nintendo DS FNT/FAT table extends beyond the file")
    fnt = data[fnt_offset:fnt_offset + fnt_size]
    file_count = fat_size // 8
    ranges = [struct.unpack_from("<II", data, fat_offset + i * 8) for i in range(file_count)]
    for start, end in ranges:
        if start > end or end > len(data):
            raise RomFormatError("FAT contains an invalid file range")

    files: dict[str, tuple[int, int]] = {}
    visited: set[int] = set()

    def walk(directory_id: int, prefix: str = "", depth: int = 0) -> None:
        if depth > 32 or directory_id in visited:
            raise RomFormatError("FNT contains a directory cycle or excessive depth")
        visited.add(directory_id)
        record = (directory_id & 0x0FFF) * 8
        if record + 8 > len(fnt):
            raise RomFormatError("FNT directory record is outside the table")
        subtable, first_file_id, _parent = struct.unpack_from("<IHH", fnt, record)
        if subtable >= len(fnt):
            raise RomFormatError("FNT subtable offset is outside the table")
        pos = subtable
        file_id = first_file_id
        while pos < len(fnt):
            kind_and_length = fnt[pos]
            pos += 1
            if kind_and_length == 0:
                break
            is_directory = bool(kind_and_length & 0x80)
            name_length = kind_and_length & 0x7F
            if not name_length or pos + name_length > len(fnt):
                raise RomFormatError("FNT contains an invalid filename")
            name = fnt[pos:pos + name_length].decode("ascii", "replace")
            pos += name_length
            path = f"{prefix}{name}"
            if is_directory:
                if pos + 2 > len(fnt):
                    raise RomFormatError("FNT directory entry is truncated")
                child_id = _u16(fnt, pos)
                pos += 2
                walk(child_id, path + "/", depth + 1)
            else:
                if file_id >= file_count:
                    raise RomFormatError("FNT file ID exceeds FAT file count")
                files[path] = ranges[file_id]
                file_id += 1

    walk(0xF000)
    return files


def _split_narc_members(blob: bytes) -> list[bytes]:
    if len(blob) < 0x10 or blob[:4] != b"NARC":
        raise RomFormatError("expected a NARC archive")
    declared_size = _u32(blob, 8)
    if declared_size > len(blob) or declared_size < 0x10:
        raise RomFormatError("NARC declared size is invalid")
    pos = 0x10
    ranges: list[tuple[int, int]] | None = None
    gmif_data: bytes | None = None
    while pos + 8 <= declared_size:
        magic = blob[pos:pos + 4]
        size = _u32(blob, pos + 4)
        if size < 8 or pos + size > declared_size:
            raise RomFormatError("NARC contains an invalid block size")
        block = blob[pos + 8:pos + size]
        if magic == b"BTAF":
            if len(block) < 4:
                raise RomFormatError("NARC BTAF block is truncated")
            count = _u16(block, 0)
            if 4 + count * 8 > len(block):
                raise RomFormatError("NARC BTAF file table is truncated")
            ranges = [struct.unpack_from("<II", block, 4 + i * 8) for i in range(count)]
        elif magic == b"GMIF":
            gmif_data = block
        pos += size
    if ranges is None or gmif_data is None:
        raise RomFormatError("NARC is missing BTAF or GMIF")
    members = []
    for start, end in ranges:
        if start > end or end > len(gmif_data):
            raise RomFormatError("NARC member range is invalid")
        members.append(gmif_data[start:end])
    return members


def inspect_rom(path: str | Path) -> dict:
    rom_path = Path(path)
    data = rom_path.read_bytes()
    if len(data) < 0x200 or data[0x12] not in (0, 2):
        raise RomFormatError("file does not look like a supported Nintendo DS ROM")
    game_code = data[0x0C:0x10].decode("ascii", "replace")
    files = _parse_nitrofs(data)
    archive_report = {}
    for archive_path in sorted(TARGET_ARCHIVES):
        if archive_path not in files:
            archive_report[archive_path] = {"present": False}
            continue
        start, end = files[archive_path]
        members = _split_narc_members(data[start:end])
        archive_report[archive_path] = {
            "present": True, "bytes": end - start, "members": len(members)
        }

    matrix_path = "fielddata/mapmatrix/map_matrix.narc"
    matrix_ids: list[str] = []
    if matrix_path in files:
        start, end = files[matrix_path]
        for member in _split_narc_members(data[start:end]):
            hints = re.findall(rb"[A-Za-z][A-Za-z0-9_]{5,30}", member)
            if hints:
                matrix_ids.append(hints[0].decode("ascii", "replace"))

    return {
        "rom_file": rom_path.name,
        "rom_bytes": len(data),
        "game_code": game_code,
        "filesystem_file_count": len(files),
        "target_archives": archive_report,
        "map_matrix_identifier_count": len(matrix_ids),
        "map_matrix_identifiers_sample": matrix_ids[:40],
        "asset_extraction_performed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", help="path to a user-supplied Nintendo DS ROM")
    parser.add_argument("--output", help="optional JSON report path")
    args = parser.parse_args()
    rendered = json.dumps(inspect_rom(args.rom), indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
