from __future__ import annotations

import struct

import pytest

from tools.audit_platinum_reference import audit_rom, read_nitrofs


def minimal_nds_rom() -> bytes:
    data = bytearray(0x204)
    data[:12] = b"TEST GAME\\0\\0\\0"
    data[0x0C:0x10] = b"TEST"
    data[0x1E] = 2
    # FNT header, one directory-table entry, then its filename subtable.
    subtable = bytes([1]) + b"x" + bytes([0])
    fnt = (struct.pack("<IHH", 16, 0, 1)
           + struct.pack("<IHH", 16, 0, 0xF000)
           + subtable)
    data[0x40:0x48] = struct.pack("<II", 0x180, len(fnt))
    data[0x48:0x50] = struct.pack("<II", 0x190, 8)
    data[0x180:0x180 + len(fnt)] = fnt
    data[0x190:0x198] = struct.pack("<II", 0x200, 0x204)
    data[0x200:0x204] = b"DATA"
    return bytes(data)


def test_read_nitrofs_lists_file_and_fat_size():
    entries = read_nitrofs(minimal_nds_rom())
    assert entries == [{"path": "x", "file_id": 0, "offset": 0x200, "size": 4}]


def test_audit_reports_header_and_file_inventory(tmp_path):
    rom = tmp_path / "sample.nds"
    rom.write_bytes(minimal_nds_rom())
    result = audit_rom(rom)
    assert result["file"] == "sample.nds"
    assert result["game_code"] == "TEST"
    assert result["revision"] == 2
    assert result["nitrofs_file_count"] == 1
    assert result["map_related_files"] == []


def test_read_nitrofs_rejects_missing_tables():
    with pytest.raises(ValueError, match="invalid or missing NitroFS"):
        read_nitrofs(bytes(0x200))
