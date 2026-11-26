from __future__ import annotations

import struct

import pytest

from tools.inspect_ds_reference import RomFormatError, _split_narc_members, _parse_nitrofs


def test_rejects_short_header():
    with pytest.raises(RomFormatError):
        _parse_nitrofs(b"short")


def test_rejects_invalid_narc():
    with pytest.raises(RomFormatError):
        _split_narc_members(b"not a narc archive")


def test_counts_narc_members():
    btaf = b"BTAF" + struct.pack("<IHH", 28, 2, 0) + struct.pack("<IIII", 0, 0, 0, 0)
    gmif = b"GMIF" + struct.pack("<I", 8)
    total = 0x10 + len(btaf) + len(gmif)
    header = b"NARC" + b"\xff\xfe" + struct.pack("<HII", 0x10, total, 0x0100)
    assert len(_split_narc_members(header + btaf + gmif)) == 2
