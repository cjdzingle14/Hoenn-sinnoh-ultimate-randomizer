"""Audit GBA sprite assets and make crisp, non-destructive comparison previews.

This tool deliberately does not overwrite game assets. GBA Pokémon graphics use
indexed palettes, so destructive RGB filters and smooth scaling can break builds.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image


def palette_report(path: Path) -> tuple[str, int | None, bool]:
    """Return image mode, palette color count (if indexed), and transparency."""
    with Image.open(path) as image:
        mode = image.mode
        if mode == "P":
            used_colors = image.getcolors(maxcolors=256)
            colors = len(used_colors or [])
            transparent = "transparency" in image.info
            return mode, colors, transparent
        if mode in ("RGBA", "LA"):
            return mode, None, image.getchannel("A").getextrema()[0] == 0
        return mode, None, False


def audit(root: Path) -> list[str]:
    """Find PNGs that may need manual palette/transparency review."""
    issues: list[str] = []
    pngs = sorted(root.rglob("*.png"))
    for path in pngs:
        try:
            mode, colors, has_transparency = palette_report(path)
            if mode != "P":
                issues.append(f"{path}: mode={mode}; expected indexed/paletted PNG")
            elif colors is not None and colors > 16:
                issues.append(f"{path}: {colors} palette colors; GBA 4bpp assets allow at most 16")
            if not has_transparency:
                issues.append(f"{path}: no transparent color/channel detected; verify sprite background")
        except (OSError, ValueError) as exc:
            issues.append(f"{path}: could not inspect ({exc})")
    return issues


def make_previews(root: Path, destination: Path, scale: int = 3) -> int:
    """Write nearest-neighbor enlarged PNG previews without touching source assets."""
    if scale < 2:
        raise ValueError("preview scale must be at least 2")
    count = 0
    for path in sorted(root.rglob("*.png")):
        relative = path.relative_to(root)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(path) as image:
            image = image.convert("RGBA")
            image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST).save(target)
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    parser.add_argument("--preview-dir", type=Path, help="optional output directory for crisp comparison PNGs")
    parser.add_argument("--scale", type=int, default=3)
    args = parser.parse_args()

    roots = [args.engine_dir / "graphics" / "pokemon", args.engine_dir / "graphics" / "trainers"]
    roots = [root for root in roots if root.is_dir()]
    if not roots:
        parser.error("no graphics/pokemon or graphics/trainers folders found under --engine-dir")

    total_issues = 0
    for root in roots:
        issues = audit(root)
        print(f"{root}: checked {len(list(root.rglob('*.png')))} PNG files")
        for issue in issues:
            print(f"REVIEW: {issue}")
        total_issues += len(issues)

    if args.preview_dir:
        count = sum(make_previews(root, args.preview_dir / root.name, args.scale) for root in roots)
        print(f"Wrote {count} nearest-neighbor previews to {args.preview_dir}")
    print(f"Manual review items: {total_issues}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
