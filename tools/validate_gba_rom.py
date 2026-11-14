"""Validate the standard Game Boy Advance ROM header before publishing a build."""
from __future__ import annotations

import argparse
from pathlib import Path

# Nintendo's 156-byte logo required by the GBA boot ROM.
GBA_LOGO = bytes.fromhex(
    "24 ff ae 51 69 9a a2 21 3d 84 82 0a 84 e4 09 ad "
    "11 24 8b 98 c0 81 7f 21 a3 52 be 19 93 09 ce 20 "
    "10 46 4a 4a f8 27 31 ec 58 c7 e8 33 82 e3 ce bf "
    "85 f4 df 94 ce 4b 09 c1 94 56 8a c0 13 72 a7 fc "
    "9f 84 4d 73 a3 ca 9a 61 58 97 a3 27 fc 03 98 76 "
    "23 1d c7 61 03 04 ae 56 bf 38 84 00 40 a7 0e fd "
    "ff 52 fe 03 6f 95 30 f1 97 fb c0 85 60 d6 80 25 "
    "a9 63 be 03 01 4e 38 e2 f9 a2 34 ff bb 3e 03 44 "
    "78 00 90 cb 88 11 3a 94 65 c0 7c 63 87 f0 3c af "
    "d6 25 e4 8b 38 0a ac 72 21 d4 f8 07"
)


def validate_gba_rom(data: bytes) -> list[str]:
    """Return header/format errors; an empty list means structurally valid GBA ROM."""
    errors: list[str] = []
    if len(data) < 0xC0:
        return ["ROM is smaller than the 0xC0-byte GBA header"]
    if len(data) % 4:
        errors.append("ROM size must be a multiple of 4 bytes")
    if data[0x04:0xA0] != GBA_LOGO:
        errors.append("Nintendo GBA logo at 0x04-0x9F does not match")
    if data[0xB2] != 0x96:
        errors.append("GBA fixed header byte at 0xB2 must be 0x96")
    checksum = (-(sum(data[0xA0:0xBD]) + 0x19)) & 0xFF
    if data[0xBD] != checksum:
        errors.append(
            f"GBA header checksum mismatch: found 0x{data[0xBD]:02X}, expected 0x{checksum:02X}"
        )
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path, help="built .gba ROM to validate")
    args = parser.parse_args()
    if args.rom.suffix.lower() != ".gba":
        parser.error("ROM filename must end in .gba")
    errors = validate_gba_rom(args.rom.read_bytes())
    if errors:
        raise SystemExit("\n".join(f"ERROR: {error}" for error in errors))
    print(f"Valid GBA header: {args.rom} ({args.rom.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
