"""Comprehensive unit tests for hued.palettes and package metadata."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

import hued
from hued.palettes import ColorPalette


class TestHarmonySchemes:
    BASE = (255, 60, 52)

    def test_init_validation(self) -> None:
        p = ColorPalette([255, 60, 52])
        assert p.base_color == (255, 60, 52)
        assert p.palette == [(255, 60, 52)]

        with pytest.raises(ValueError):
            ColorPalette((256, 0, 0))
        with pytest.raises(ValueError):
            ColorPalette((255, 0))
        with pytest.raises(TypeError):
            ColorPalette("#FF0000")  # type: ignore[arg-type]

    def test_complementary_analogous_triadic_split(self) -> None:
        palette = ColorPalette(self.BASE)
        assert palette.generate_complementary() == [(255, 60, 52), (51, 247, 255)]
        assert palette.generate_analogous() == [(255, 51, 145), (255, 60, 52), (255, 161, 51)]
        assert palette.generate_triadic() == [(255, 60, 52), (51, 255, 59), (59, 51, 255)]
        assert palette.generate_split_complementary() == [
            (255, 60, 52),
            (51, 255, 161),
            (51, 145, 255),
        ]

    def test_tetradic_distinct_from_square(self) -> None:
        palette = ColorPalette(self.BASE)
        square = palette.generate_square()
        assert square == [(255, 60, 52), (145, 255, 51), (51, 247, 255), (161, 51, 255)]

        tetradic = palette.generate_tetradic()  # default angle=60 (rectangular)
        assert len(tetradic) == 4
        assert tetradic != square
        assert palette.generate_tetradic(angle=90) == square

    def test_monochromatic_and_edge_cases(self) -> None:
        palette = ColorPalette(self.BASE)
        expected = [
            (51, 2, 0), (73, 3, 0), (95, 4, 0), (118, 5, 0),
            (140, 5, 0), (162, 6, 0), (184, 7, 0), (206, 8, 0),
            (228, 9, 0), (251, 10, 0), (255, 27, 18), (255, 48, 40),
            (255, 70, 62), (255, 91, 84), (255, 112, 106),
            (255, 134, 129), (255, 155, 151), (255, 176, 173),
            (255, 197, 195), (255, 219, 217), (255, 240, 239),
            (255, 255, 255),
        ]
        assert palette.generate_monochromatic() == expected
        assert palette.palette_to_hex() == [
            "#330200", "#490300", "#5F0400", "#760500",
            "#8C0500", "#A20600", "#B80700", "#CE0800",
            "#E40900", "#FB0A00", "#FF1B12", "#FF3028",
            "#FF463E", "#FF5B54", "#FF706A", "#FF8681",
            "#FF9B97", "#FFB0AD", "#FFC5C3", "#FFDBD9",
            "#FFF0EF", "#FFFFFF",
        ]

        # Regression: shades=1 previously raised ZeroDivisionError
        assert palette.generate_monochromatic(shades=1) == [self.BASE]
        with pytest.raises(ValueError):
            palette.generate_monochromatic(shades=0)
        with pytest.raises(TypeError):
            palette.generate_monochromatic(shades=True)  # type: ignore[arg-type]


class TestMutationRandomAndGradients:
    def test_random_palette_and_dict_palette_to_hex(self) -> None:
        palette = ColorPalette((10, 20, 30))

        # set_as_current=False preserves base_color and palette
        preview = palette.generate_random_palette(set_as_current=False)
        assert isinstance(preview, dict)
        assert palette.base_color == (10, 20, 30)
        assert palette.palette == [(10, 20, 30)]

        # set_as_current=True sets dict palette, and palette_to_hex() works on it
        current = palette.generate_random_palette(set_as_current=True)
        assert palette.palette is current
        hex_dict = palette.palette_to_hex()
        assert isinstance(hex_dict, dict)
        assert set(hex_dict.keys()) == set(current.keys())
        assert isinstance(hex_dict["Base Color"], str) and hex_dict["Base Color"].startswith("#")
        assert all(h.startswith("#") for h in hex_dict["Triadic Palette"])

        # add_color / remove_color raise clear TypeError on dict palettes
        with pytest.raises(TypeError):
            palette.add_color((1, 2, 3))
        with pytest.raises(TypeError):
            palette.remove_color((1, 2, 3))

    def test_add_remove_and_random_colors(self) -> None:
        palette = ColorPalette((0, 0, 0))
        palette.add_color((255, 255, 255))
        assert palette.palette == [(0, 0, 0), (255, 255, 255)]
        palette.remove_color((0, 0, 0))
        assert palette.palette == [(255, 255, 255)]

        color = palette.generate_random_color()
        assert set(color.keys()) == {"RGB Color", "HEX Color", "HSL Color"}
        hexes = palette.generate_random_hex_colors(5)
        assert len(hexes) == 5 and all(len(h) == 7 and h.startswith("#") for h in hexes)
        assert palette.generate_random_hex_colors(0) == []
        with pytest.raises(ValueError):
            palette.generate_random_hex_colors(-1)

    @pytest.mark.parametrize("space", ["rgb", "linear", "lab", "hsl"])
    def test_generate_gradient_spaces(self, space: str) -> None:
        palette = ColorPalette((255, 60, 52))
        start, end = (255, 60, 52), (51, 247, 255)
        grad = palette.generate_gradient(start, end, steps=5, space=space)
        assert len(grad) == 6
        assert grad[0] == start
        assert grad[-1] == end
        # Does not mutate self.palette
        assert palette.palette == [(255, 60, 52)]

        # Self-gradient identity (regression for int() truncation on (3, 3, 3))
        assert palette.generate_gradient((3, 3, 3), (3, 3, 3), steps=5, space=space) == [
            (3, 3, 3)
        ] * 6

    def test_generate_gradient_validation(self) -> None:
        palette = ColorPalette((0, 0, 0))
        with pytest.raises(ValueError):
            palette.generate_gradient((0, 0, 0), (255, 255, 255), steps=0)
        with pytest.raises(ValueError):
            palette.generate_gradient((0, 0, 0), (255, 255, 255), steps=3, space="cmyk")


class TestExportAndMetadata:
    def test_export_list_and_dict_all_formats(self, tmp_path: Path) -> None:
        sub = tmp_path / "dir.with.dots"
        sub.mkdir()

        cp = ColorPalette((255, 60, 52))
        cp.generate_complementary()

        json_path = sub / "comp.json"
        txt_path = sub / "comp.txt"
        csv_path = sub / "comp.csv"
        css_path = sub / "comp.css"

        cp.export_palette(json_path)
        cp.export_palette(str(txt_path))
        cp.export_palette(csv_path)
        cp.export_palette(css_path)

        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data == [
            {"rgb": [255, 60, 52], "hex": "#FF3C34"},
            {"rgb": [51, 247, 255], "hex": "#33F7FF"},
        ]
        assert "#FF3C34" in txt_path.read_text(encoding="utf-8")
        with csv_path.open(encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        assert rows[0] == ["Type", "Index", "Hex", "R", "G", "B"]
        assert rows[1] == ["Simple Palette", "0", "#FF3C34", "255", "60", "52"]
        css_text = css_path.read_text(encoding="utf-8")
        assert "--palette-color-0: #FF3C34;" in css_text

        # Dictionary export
        cp.generate_random_palette()
        for ext in (".json", ".txt", ".csv", ".css"):
            out = sub / f"random{ext}"
            cp.export_palette(out)
            assert out.stat().st_size > 0

        # Regression: extensionless filename named "json" must be rejected
        with pytest.raises(ValueError):
            cp.export_palette(sub / "json")
        with pytest.raises(ValueError):
            cp.export_palette(sub / "palette.xml")

        cp.palette = []
        with pytest.raises(ValueError):
            cp.export_palette(sub / "empty.json")

    def test_package_version_and_typing_marker(self) -> None:
        repo_root = Path(__file__).resolve().parent.parent
        pyproject_text = (repo_root / "pyproject.toml").read_text(encoding="utf-8")
        assert f'version = "{hued.__version__}"' in pyproject_text
        assert (Path(hued.__file__).resolve().parent / "py.typed").is_file()
        for symbol in hued.__all__:
            assert hasattr(hued, symbol), f"Missing export: {symbol}"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
