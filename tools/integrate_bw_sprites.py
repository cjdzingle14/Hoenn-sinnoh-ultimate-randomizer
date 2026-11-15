"""Convert PokeAPI Gen V-style sprites into the pinned engine's GBA asset slots.

The source sprites are downloaded at build time and are never committed to this
repository. Existing asset dimensions and the engine's 4bpp palette limit are
preserved. Species without a complete source set are left untouched.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import re
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

SOURCE_REVISION = "c0542f7c51215d9672439012838c99f520596cbd"
SOURCE_ROOT = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/"
    f"{SOURCE_REVISION}/sprites/pokemon/versions/generation-v/black-white"
)
MAX_DEX = 1025
MAX_VISIBLE_COLORS = 15


def parse_species(species_header: str) -> list[tuple[int, str]]:
    """Return one base species constant for each National Dex number."""
    found: dict[int, str] = {}
    pattern = re.compile(r"^\s*SPECIES_([A-Z0-9_]+)\s*=\s*(\d+)\s*,", re.MULTILINE)
    for name, raw_number in pattern.findall(species_header):
        number = int(raw_number)
        if 1 <= number <= MAX_DEX:
            found.setdefault(number, name)
    return sorted(found.items())


def species_directory(engine_graphics: Path, constant: str) -> Path | None:
    """Resolve common underscore/hyphen naming conventions without guessing."""
    for candidate in (constant.lower(), constant.lower().replace("_", "-")):
        path = engine_graphics / candidate
        if path.is_dir():
            return path
    return None


def _download(url: str, destination: Path, attempts: int = 3) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size:
        return True
    request = urllib.request.Request(
        url, headers={"User-Agent": "Hoenn-Sinnoh-Randomizer-Sprite-Builder/1.0"}
    )
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                data = response.read()
            if not data:
                return False
            destination.write_bytes(data)
            return True
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return False
            if attempt == attempts - 1:
                raise
        except (OSError, TimeoutError):
            if attempt == attempts - 1:
                raise
    return False


def _source_paths(dex: int) -> dict[str, str]:
    return {
        "front_animated": f"{SOURCE_ROOT}/animated/{dex}.gif",
        "front": f"{SOURCE_ROOT}/{dex}.png",
        "back": f"{SOURCE_ROOT}/back/{dex}.png",
        "shiny_front": f"{SOURCE_ROOT}/shiny/{dex}.png",
        "icon": (
            "https://raw.githubusercontent.com/PokeAPI/sprites/"
            f"{SOURCE_REVISION}/sprites/pokemon/versions/generation-v/icons/{dex}.png"
        ),
    }


def fit_to_box(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Fit a transparent sprite into one existing engine frame, centered."""
    image = source.convert("RGBA")
    bounds = image.getchannel("A").getbbox()
    if bounds:
        image = image.crop(bounds)
    width, height = size
    scale = min(width / image.width, height / image.height)
    resized = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.NEAREST,
    )
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.alpha_composite(
        resized, ((width - resized.width) // 2, (height - resized.height) // 2)
    )
    return canvas


def fit_front_sheet(source_path: Path, size: tuple[int, int]) -> Image.Image:
    """Build the engine's two-frame vertical sheet from an animated GIF or static PNG."""
    width, height = size
    frame_size = (width, height // 2) if height == width * 2 else size
    frames = []
    with Image.open(source_path) as source:
        if getattr(source, "is_animated", False):
            for frame_index in range(min(2, getattr(source, "n_frames", 1))):
                source.seek(frame_index)
                frames.append(fit_to_box(source.convert("RGBA"), frame_size))
        else:
            frames.append(fit_to_box(source.convert("RGBA"), frame_size))
    if not frames:
        raise ValueError(f"no usable animation frames in {source_path}")
    while len(frames) < 2 and height == width * 2:
        frames.append(frames[0].copy())
    if height != width * 2:
        return frames[0]
    sheet = Image.new("RGBA", size, (0, 0, 0, 0))
    sheet.alpha_composite(frames[0], (0, 0))
    sheet.alpha_composite(frames[1], (0, frame_size[1]))
    return sheet


def make_palette(front: Image.Image) -> list[tuple[int, int, int]]:
    """Build a shared 15-color palette from a front sprite; slot zero is transparent."""
    rgba = front.convert("RGBA")
    rgb_bytes = rgba.convert("RGB").tobytes()
    alpha_bytes = rgba.getchannel("A").tobytes()
    opaque_pixels = [
        tuple(rgb_bytes[offset:offset + 3])
        for offset in range(0, len(rgb_bytes), 3)
        if alpha_bytes[offset // 3] > 0
    ]
    if not opaque_pixels:
        raise ValueError("sprite has no opaque pixels")
    sample = Image.new("RGB", (len(opaque_pixels), 1))
    sample.putdata(opaque_pixels)
    quantized = sample.quantize(colors=MAX_VISIBLE_COLORS, method=Image.Quantize.MEDIANCUT)
    raw = (quantized.getpalette() or [])[: MAX_VISIBLE_COLORS * 3]
    raw.extend([0] * (MAX_VISIBLE_COLORS * 3 - len(raw)))
    colors = [tuple(raw[i:i + 3]) for i in range(0, MAX_VISIBLE_COLORS * 3, 3)]
    return [(0, 0, 0), *colors]


def _palette_image(colors: list[tuple[int, int, int]]) -> Image.Image:
    palette = Image.new("P", (1, 1))
    flat = [channel for color in colors[1:] for channel in color]
    flat.extend([0] * (768 - len(flat)))
    palette.putpalette(flat)
    return palette


def indexed_gba(image: Image.Image, colors: list[tuple[int, int, int]]) -> Image.Image:
    """Map opaque pixels to palette entries 1-15 and transparent pixels to 0."""
    rgba = image.convert("RGBA")
    quantized = rgba.convert("RGB").quantize(
        palette=_palette_image(colors), dither=Image.Dither.NONE
    )
    indices = bytearray(quantized.tobytes())
    alpha = rgba.getchannel("A").tobytes()
    for index, opacity in enumerate(alpha):
        indices[index] = 0 if opacity == 0 else min(15, indices[index] + 1)
    output = Image.new("P", rgba.size)
    flat = [channel for color in colors for channel in color]
    flat.extend([0] * (768 - len(flat)))
    output.putpalette(flat)
    output.putdata(indices)
    output.info["transparency"] = 0
    return output


def write_jasc_palette(path: Path, colors: list[tuple[int, int, int]]) -> None:
    lines = ["JASC-PAL", "0100", "16"]
    lines.extend(f"{red} {green} {blue}" for red, green, blue in colors)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _open_fit(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as source:
        return fit_to_box(source, size)


def integrate_species(directory: Path, dex: int, cache: Path) -> bool:
    """Replace front/back normal and shiny palette art for one species."""
    front_target, back_target = directory / "anim_front.png", directory / "back.png"
    if not front_target.exists() or not back_target.exists():
        return False
    with Image.open(front_target) as current:
        front_size = current.size
    with Image.open(back_target) as current:
        back_size = current.size

    source_files: dict[str, Path] = {}
    paths = _source_paths(dex)
    animated_path = cache / "front_animated" / f"{dex}.gif"
    if _download(paths["front_animated"], animated_path):
        source_files["front_animated"] = animated_path
    else:
        static_path = cache / "front" / f"{dex}.png"
        if not _download(paths["front"], static_path):
            return False
        source_files["front"] = static_path

    for key in ("back", "shiny_front", "icon"):
        target = cache / key / f"{dex}.png"
        if not _download(paths[key], target):
            if key == "icon":
                continue
            return False
        source_files[key] = target

    front_source = source_files.get("front_animated", source_files.get("front"))
    normal_front = fit_front_sheet(front_source, front_size)
    normal_back = _open_fit(source_files["back"], back_size)
    shiny_frame_size = (
        front_size[0],
        front_size[1] // 2 if front_size[1] == front_size[0] * 2 else front_size[1],
    )
    shiny_front = _open_fit(source_files["shiny_front"], shiny_frame_size)
    normal_colors, shiny_colors = make_palette(normal_front), make_palette(shiny_front)

    replacements = {
        "anim_front.png": normal_front,
        "back.png": normal_back,
        "anim_front_gba.png": indexed_gba(normal_front, normal_colors),
        "back_gba.png": indexed_gba(normal_back, normal_colors),
    }
    if "icon" in source_files and (directory / "icon.png").exists():
        with Image.open(directory / "icon.png") as current_icon:
            icon_size = current_icon.size
        icon = fit_front_sheet(source_files["icon"], icon_size)
        replacements["icon.png"] = icon
        replacements["icon_gba.png"] = indexed_gba(icon, make_palette(icon))

    for name, image in replacements.items():
        image.save(directory / name, format="PNG")
    write_jasc_palette(directory / "normal.pal", normal_colors)
    write_jasc_palette(directory / "normal_gba.pal", normal_colors)
    write_jasc_palette(directory / "shiny.pal", shiny_colors)
    write_jasc_palette(directory / "shiny_gba.pal", shiny_colors)
    return True


def integrate(engine_dir: Path, cache_dir: Path, limit: int = MAX_DEX) -> tuple[int, int]:
    species_header = engine_dir / "include/constants/species.h"
    graphics_root = engine_dir / "graphics/pokemon"
    species = [
        (dex, name)
        for dex, name in parse_species(species_header.read_text(encoding="utf-8"))
        if dex <= limit
    ]
    jobs = []
    for dex, name in species:
        directory = species_directory(graphics_root, name)
        if directory is not None:
            jobs.append((dex, directory))
    successes, failures = 0, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = {
            executor.submit(integrate_species, directory, dex, cache_dir): (dex, directory.name)
            for dex, directory in jobs
        }
        for future in concurrent.futures.as_completed(futures):
            dex, name = futures[future]
            try:
                if future.result():
                    successes += 1
                else:
                    failures.append((dex, name))
            except Exception as exc:
                failures.append((dex, f"{name}: {exc}"))
    if failures:
        sample = ", ".join(f"{dex}:{name}" for dex, name in failures[:20])
        print(f"Skipped {len(failures)} species without a complete source set: {sample}")
    return successes, len(jobs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    parser.add_argument(
        "--cache-dir", type=Path,
        default=Path(tempfile.gettempdir()) / "pokeapi-bw-cache",
    )
    parser.add_argument(
        "--limit", type=int, default=MAX_DEX,
        help="National Dex limit; useful for sample builds",
    )
    args = parser.parse_args()
    if not 1 <= args.limit <= MAX_DEX:
        parser.error(f"--limit must be between 1 and {MAX_DEX}")
    updated, found = integrate(args.engine_dir, args.cache_dir, args.limit)
    print(f"Gen V-style sprite integration: updated {updated}/{found} engine species (Dex limit {args.limit}).")
    if updated == 0:
        raise SystemExit("No Pokémon sprite assets were updated; refusing to build an unchanged sprite pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
