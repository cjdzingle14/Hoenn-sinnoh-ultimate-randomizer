from pathlib import Path

from PIL import Image

from tools.integrate_bw_sprites import (
    fit_front_sheet,
    fit_to_box,
    indexed_gba,
    integrate_species,
    make_palette,
    parse_species,
    write_jasc_palette,
)


def test_parse_species_uses_one_base_species_per_dex_number():
    header = """
    SPECIES_BULBASAUR = 1,
    SPECIES_IVYSAUR = 2,
    SPECIES_BULBASAUR_MEGA = 1,
    SPECIES_RILLABOOM = 812,
    """
    assert parse_species(header) == [(1, "BULBASAUR"), (2, "IVYSAUR"), (812, "RILLABOOM")]


def test_fit_to_box_preserves_aspect_and_transparency():
    source = Image.new("RGBA", (20, 10), (255, 0, 0, 255))
    result = fit_to_box(source, (32, 32))
    assert result.size == (32, 32)
    assert result.getpixel((0, 0))[3] == 0
    assert result.getpixel((16, 16)) == (255, 0, 0, 255)


def test_front_gif_keeps_two_vertical_animation_frames(tmp_path: Path):
    first = Image.new("RGBA", (24, 24), (255, 0, 0, 255))
    second = Image.new("RGBA", (24, 24), (0, 0, 255, 255))
    gif = tmp_path / "front.gif"
    first.save(gif, save_all=True, append_images=[second], duration=100, loop=0)
    sheet = fit_front_sheet(gif, (64, 128))
    assert sheet.size == (64, 128)
    assert sheet.getpixel((32, 32)) != sheet.getpixel((32, 96))


def test_gba_conversion_reserves_palette_zero_for_transparency():
    source = Image.new("RGBA", (4, 1), (0, 0, 0, 0))
    source.putpixel((1, 0), (255, 0, 0, 255))
    source.putpixel((2, 0), (0, 255, 0, 255))
    source.putpixel((3, 0), (0, 0, 255, 255))
    output = indexed_gba(source, make_palette(source))
    assert output.mode == "P"
    assert output.getpixel((0, 0)) == 0
    assert all(output.getpixel((x, 0)) > 0 for x in (1, 2, 3))
    assert output.info["transparency"] == 0


def test_jasc_palette_has_exactly_sixteen_entries(tmp_path: Path):
    palette = make_palette(Image.new("RGBA", (2, 2), (255, 0, 0, 255)))
    target = tmp_path / "normal.pal"
    write_jasc_palette(target, palette)
    lines = target.read_text().splitlines()
    assert lines[:3] == ["JASC-PAL", "0100", "16"]
    assert len(lines) == 19


def test_integrate_species_preserves_engine_dimensions_and_animation(tmp_path: Path, monkeypatch):
    import tools.integrate_bw_sprites as pipeline

    species = tmp_path / "graphics" / "pokemon" / "bulbasaur"
    species.mkdir(parents=True)
    Image.new("RGBA", (64, 128), (10, 20, 30, 255)).save(species / "anim_front.png")
    Image.new("RGBA", (64, 64), (10, 20, 30, 255)).save(species / "back.png")
    Image.new("RGBA", (32, 64), (10, 20, 30, 255)).save(species / "icon.png")
    Image.new("P", (32, 64)).save(species / "icon_gba.png")

    def fake_download(url, destination, attempts=3):
        destination.parent.mkdir(parents=True, exist_ok=True)
        color = (0, 255, 0, 255) if "/shiny/" in url else (255, 0, 0, 255)
        if url.endswith(".gif"):
            first = Image.new("RGBA", (96, 96), color)
            second = Image.new("RGBA", (96, 96), (0, 0, 255, 255))
            first.save(destination, save_all=True, append_images=[second], duration=100, loop=0)
        else:
            Image.new("RGBA", (96, 96), color).save(destination)
        return True

    monkeypatch.setattr(pipeline, "_download", fake_download)
    assert integrate_species(species, 1, tmp_path / "cache")
    with Image.open(species / "anim_front.png") as sheet:
        assert sheet.getpixel((32, 32)) != sheet.getpixel((32, 96))
    for name, size in (
        ("anim_front.png", (64, 128)),
        ("back.png", (64, 64)),
        ("anim_front_gba.png", (64, 128)),
        ("back_gba.png", (64, 64)),
        ("icon.png", (32, 64)),
        ("icon_gba.png", (32, 64)),
    ):
        with Image.open(species / name) as image:
            assert image.size == size
    for name in ("normal.pal", "normal_gba.pal", "shiny.pal", "shiny_gba.pal"):
        assert (species / name).read_text().splitlines()[2] == "16"
