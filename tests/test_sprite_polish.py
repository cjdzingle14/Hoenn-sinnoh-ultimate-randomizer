from pathlib import Path

from PIL import Image

from tools.sprite_polish import audit, gba_sprite_files, make_previews, palette_report


def test_palette_report_counts_visible_colors_and_alpha(tmp_path: Path):
    path = tmp_path / "test_gba.png"
    image = Image.new("RGBA", (16, 1), (0, 0, 0, 0))
    for x in range(15):
        image.putpixel((x, 0), (x * 10, 20, 30, 255))
    image.save(path)

    mode, colors, transparent = palette_report(path)

    assert mode == "RGBA"
    assert colors == 15
    assert transparent is True


def test_audit_flags_more_than_fifteen_visible_colors(tmp_path: Path):
    path = tmp_path / "test_gba.png"
    image = Image.new("RGBA", (17, 1), (0, 0, 0, 0))
    for x in range(16):
        image.putpixel((x, 0), (x * 10, 20, 30, 255))
    image.save(path)

    issues = audit(tmp_path)

    assert any("16 visible colors" in issue for issue in issues)


def test_only_explicit_gba_assets_are_selected(tmp_path: Path):
    Image.new("RGBA", (2, 2), (0, 0, 0, 0)).save(tmp_path / "front.png")
    Image.new("RGBA", (2, 2), (0, 0, 0, 0)).save(tmp_path / "front_gba.png")

    assert [p.name for p in gba_sprite_files(tmp_path)] == ["front_gba.png"]


def test_preview_uses_nearest_neighbor_and_keeps_source_unchanged(tmp_path: Path):
    source = tmp_path / "pokemon"
    source.mkdir()
    asset = source / "sample_gba.png"
    image = Image.new("RGBA", (2, 1))
    image.putpixel((0, 0), (255, 0, 0, 255))
    image.putpixel((1, 0), (0, 0, 255, 255))
    image.save(asset)
    original = asset.read_bytes()

    output = tmp_path / "preview"
    assert make_previews(source, output, scale=3) == 1
    preview = Image.open(output / "sample_gba.png").convert("RGBA")

    assert preview.size == (6, 3)
    assert preview.getpixel((0, 0)) == (255, 0, 0, 255)
    assert preview.getpixel((5, 2)) == (0, 0, 255, 255)
    assert asset.read_bytes() == original
