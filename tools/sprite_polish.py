"""Audit GBA sprite assets and make crisp, non-destructive comparison previews.

This tool deliberately does not overwrite game assets. GBA Pokémon graphics use
indexed palettes, so destructive RGB filters and smooth scaling can break builds.
"""
from __future__ import annotations

import argparse
import colorsys
from pathlib import Path
from PIL import Image


def palette_report(path: Path) -> tuple[str, int, bool]:
    """Return source mode, visible-color count, and whether transparency exists."""
    with Image.open(path) as image:
        mode = image.mode
        rgba = image.convert("RGBA")
        colors = rgba.getcolors(maxcolors=65536)
        if colors is None:
            raise ValueError("image has more than 65,536 distinct RGBA colors")
        visible_colors = sum(1 for count, color in colors if color[3] > 0)
        alpha = rgba.getchannel("A")
        has_transparency = alpha.getextrema()[0] == 0
        return mode, visible_colors, has_transparency


def gba_sprite_files(root: Path) -> list[Path]:
    """Limit strict 4bpp checks to explicit GBA-converted Pokémon PNG assets."""
    return sorted(path for path in root.rglob("*.png") if "_gba" in path.stem)


def audit(root: Path) -> list[str]:
    """Check GBA-converted Pokémon assets against 4bpp palette constraints."""
    issues: list[str] = []
    for path in gba_sprite_files(root):
        try:
            mode, colors, has_transparency = palette_report(path)
            if colors > 15:
                issues.append(f"{path}: {colors} visible colors; 4bpp sprites reserve one of 16 entries for transparency")
            if not has_transparency:
                issues.append(f"{path}: no transparent pixels detected; verify sprite background")
        except (OSError, ValueError) as exc:
            issues.append(f"{path}: could not inspect ({exc})")
    return issues


def make_previews(root: Path, destination: Path, scale: int = 3) -> int:
    """Write nearest-neighbor previews of GBA-converted PNGs without touching sources."""
    if scale < 2:
        raise ValueError("preview scale must be at least 2")
    count = 0
    for path in gba_sprite_files(root):
        relative = path.relative_to(root)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(path) as image:
            image = image.convert("RGBA")
            image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST).save(target)
        count += 1
    return count



def grade_palette_file(source: Path, destination: Path, saturation: float = 1.08, contrast: float = 1.04) -> None:
    """Write a subtle color-grade candidate while preserving palette slot zero."""
    lines = source.read_text(encoding="utf-8").splitlines()
    if len(lines) < 4 or lines[0] != "JASC-PAL" or lines[1] != "0100":
        raise ValueError(f"{source}: unsupported JASC palette header")
    try:
        declared = int(lines[2])
        entries = [tuple(map(int, line.split())) for line in lines[3:]]
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{source}: malformed palette data") from exc
    if len(entries) != declared or any(len(rgb) != 3 or any(c < 0 or c > 255 for c in rgb) for rgb in entries):
        raise ValueError(f"{source}: palette entry count or RGB values are invalid")

    graded = [entries[0]]
    for red, green, blue in entries[1:]:
        h, sat, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
        sat = min(1.0, sat * saturation)
        channels = colorsys.hsv_to_rgb(h, sat, value)
        adjusted = tuple(
            max(0, min(255, round((channel * 255 - 127.5) * contrast + 127.5)))
            for channel in channels
        )
        graded.append(adjusted)

    destination.parent.mkdir(parents=True, exist_ok=True)
    output = ["JASC-PAL", "0100", str(declared)]
    output.extend(f"{r} {g} {b}" for r, g, b in graded)
    destination.write_text("\\n".join(output) + "\\n", encoding="utf-8")


def make_palette_previews(root: Path, destination: Path) -> int:
    """Create optional, reversible color-grade candidates for GBA Pokémon palettes."""
    count = 0
    for path in sorted(root.rglob("*_gba.pal")):
        relative = path.relative_to(root)
        target = destination / relative
        grade_palette_file(path, target)
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    parser.add_argument("--preview-dir", type=Path, help="optional output directory for crisp comparison PNGs")
    parser.add_argument("--scale", type=int, default=3)
    parser.add_argument("--palette-preview-dir", type=Path, help="optional output directory for subtle color-grade palette candidates")
    args = parser.parse_args()

    roots = [args.engine_dir / "graphics" / "pokemon"]
    roots = [root for root in roots if root.is_dir()]
    if not roots:
        parser.error("no graphics/pokemon folder found under --engine-dir")

    total_issues = 0
    for root in roots:
        issues = audit(root)
        print(f"{root}: checked {len(gba_sprite_files(root))} PNG files")
        for issue in issues:
            print(f"REVIEW: {issue}")
        total_issues += len(issues)

    if args.preview_dir:
        count = sum(make_previews(root, args.preview_dir / root.name, args.scale) for root in roots)
        print(f"Wrote {count} nearest-neighbor previews to {args.preview_dir}")
    if args.palette_preview_dir:
        count = sum(make_palette_previews(root, args.palette_preview_dir / root.name) for root in roots)
        print(f"Wrote {count} color-grade palette candidates to {args.palette_preview_dir}")
    print(f"Manual review items: {total_issues}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
