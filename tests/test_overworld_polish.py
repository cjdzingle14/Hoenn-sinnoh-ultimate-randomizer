from pathlib import Path

import pytest

from tools.integrate_overworld_polish import grade_palette_text, integrate


def palette_text():
    colors = [
        (24, 41, 82), (255, 255, 255), (222, 230, 238), (189, 205, 230),
        (156, 180, 222), (131, 131, 139), (98, 98, 123), (65, 74, 106),
        (189, 189, 131), (115, 189, 246), (98, 172, 238), (115, 189, 246),
        (98, 164, 222), (82, 139, 197), (74, 115, 172), (115, 197, 164),
    ]
    return "JASC-PAL\n0100\n16\n" + "".join(f"{r} {g} {b}\n" for r, g, b in colors)


def entries(text):
    return [tuple(map(int, line.split())) for line in text.splitlines()[3:]]


def test_grade_preserves_transparency_and_placeholder_colors():
    source = palette_text()
    result = grade_palette_text(source)
    before, after = entries(source), entries(result)
    assert after[0] == before[0]
    assert after[3] != before[3]
    assert all(channel % 8 == 0 for rgb in after[1:] for channel in rgb)
    assert grade_palette_text(result) == result


def test_grade_preserves_magenta_and_black_placeholders():
    colors = [(1, 2, 3), (255, 0, 255)] + [(0, 0, 0)] * 14
    source = "JASC-PAL\n0100\n16\n" + "".join(f"{r} {g} {b}\n" for r, g, b in colors)
    after = entries(grade_palette_text(source))
    assert after[0] == (1, 2, 3)
    assert after[1:] == colors[1:]


def test_rejects_malformed_palette():
    with pytest.raises(ValueError):
        grade_palette_text("not a palette")


def test_integration_only_changes_tileset_palettes_and_is_repeatable(tmp_path: Path):
    engine = tmp_path / "engine"
    primary = engine / "data" / "tilesets" / "primary" / "general" / "palettes"
    secondary = engine / "data" / "tilesets" / "secondary" / "petalburg" / "palettes"
    primary.mkdir(parents=True)
    secondary.mkdir(parents=True)
    (primary / "00.pal").write_text(palette_text(), encoding="utf-8")
    (secondary / "00.pal").write_text(palette_text(), encoding="utf-8")
    unrelated = engine / "graphics" / "pokemon" / "example.pal"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_text(palette_text(), encoding="utf-8")

    assert integrate(engine) == (2, 2)
    assert integrate(engine) == (0, 2)
    assert entries((primary / "00.pal").read_text(encoding="utf-8"))[3] != entries(palette_text())[3]
    assert unrelated.read_text(encoding="utf-8") == palette_text()
