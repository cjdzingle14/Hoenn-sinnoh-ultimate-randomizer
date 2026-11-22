"""Apply a restrained, GBA-safe color grade to overworld tileset palettes."""
from __future__ import annotations

import argparse
import colorsys
from pathlib import Path

TRANSPARENT_INDEX = 0
PRESERVED_COLORS = {(0, 0, 0), (255, 0, 255)}
SATURATION = 1.14
CONTRAST = 1.08
BRIGHTNESS = 2


def _quantize_gba(channel: float) -> int:
    value = max(0, min(255, channel))
    return max(0, min(248, round(value / 8) * 8))


def grade_rgb(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    red, green, blue = rgb
    hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
    saturation = min(1.0, saturation * SATURATION)
    channels = colorsys.hsv_to_rgb(hue, saturation, value)
    return tuple(
        _quantize_gba((channel * 255 - 127.5) * CONTRAST + 127.5 + BRIGHTNESS)
        for channel in channels
    )


def grade_palette_text(source: str) -> str:
    lines = source.splitlines()
    if len(lines) < 4 or lines[0] != "JASC-PAL" or lines[1] != "0100":
        raise ValueError("unsupported palette format; expected JASC-PAL 0100")
    try:
        declared = int(lines[2])
        entries = [tuple(map(int, line.split())) for line in lines[3:]]
    except (ValueError, TypeError) as exc:
        raise ValueError("malformed JASC palette data") from exc
    if declared != 16 or len(entries) != declared:
        raise ValueError(f"expected exactly 16 palette entries, found {len(entries)}")
    if any(len(rgb) != 3 or any(channel < 0 or channel > 255 for channel in rgb) for rgb in entries):
        raise ValueError("palette RGB values must contain three channels from 0 to 255")
    if all(rgb in PRESERVED_COLORS or all(channel % 8 == 0 for channel in rgb) for rgb in entries[1:]):
        return source.rstrip() + "\n"
    graded = []
    for index, rgb in enumerate(entries):
        if index == TRANSPARENT_INDEX or rgb in PRESERVED_COLORS:
            graded.append(rgb)
        else:
            graded.append(grade_rgb(rgb))
    output = ["JASC-PAL", "0100", "16"]
    output.extend(f"{red} {green} {blue}" for red, green, blue in graded)
    return "\n".join(output) + "\n"


def integrate(engine_dir: Path) -> tuple[int, int]:
    root = engine_dir / "data" / "tilesets"
    if not root.is_dir():
        raise FileNotFoundError(f"tileset data directory not found: {root}")
    palettes = sorted(
        path for path in root.rglob("*.pal")
        if "palettes" in path.relative_to(root).parts
    )
    if not palettes:
        raise FileNotFoundError(f"no tileset palette files found under {root}")
    changed = 0
    for path in palettes:
        original = path.read_text(encoding="utf-8")
        graded = grade_palette_text(original)
        if graded != original:
            path.write_text(graded, encoding="utf-8")
            changed += 1
    return changed, len(palettes)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    changed, checked = integrate(args.engine_dir)
    print(f"Overworld palette polish: changed {changed} of {checked} tileset palettes")
    print("Preserved tile indices, metatiles, collision attributes, animation data, and transparent palette slots.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
