""" Converts a list of list into gray-scale PNG image. """
import os
import pathlib
from typing import List, Optional, Tuple, Union

import svgwrite  # type: ignore[import]
from PIL import Image, ImageDraw, PngImagePlugin

PathLike = Union[os.PathLike, pathlib.Path, str]

COLOR_1 = (255, 0, 0)
COLOR_2 = (0, 255, 0)
COLOR_3 = (0, 0, 255)


class PolyDraw:
    """Class for create logo."""

    def __init__(self) -> None:
        self.svg = svgwrite.Drawing(size=(2048, 2048))
        self.images = [
            Image.new("RGBA", (size, size), (255, 255, 255, 0))
            for size in (16, 24, 32, 48, 64, 96, 128, 256, 512, 1024, 2048)
        ]
        self.drawings = [ImageDraw.Draw(image) for image in self.images]

    def circle(
        self,
        cx: float,  # pylint: disable=invalid-name
        cy: float,  # pylint: disable=invalid-name
        r: float,  # pylint: disable=invalid-name
        fill: Optional[Tuple[int, int, int]],
        stroke: Optional[Tuple[int, int, int]],
        stroke_width: float,
    ) -> None:
        """Draw a circle."""
        midline = int(stroke_width / 2)
        for image, drawing in zip(self.images, self.drawings):
            width, height = image.size
            rayon = r + stroke_width / 2
            drawing.ellipse(
                (
                    int((cx - rayon - midline) * width),
                    int((cy - rayon - midline) * height),
                    int((cx + rayon + midline) * width) - 1,
                    int((cy + rayon + midline) * height) - 1,
                ),
                fill=fill,
                outline=stroke,
                width=int(stroke_width * min(width, height)),
            )
        extra = {}
        extra["fill"] = svgwrite.rgb(*fill) if fill is not None else "none"
        extra["stroke"] = (
            svgwrite.rgb(*stroke) if stroke is not None else "none"
        )
        if stroke_width is not None:
            extra["stroke_width"] = stroke_width * 2048
        self.svg.add(
            self.svg.circle(center=(cx * 2048, cy * 2048), r=r * 2048, **extra)
        )

    def polyline(
        self,
        points: List[Tuple[float, float]],
        fill: Optional[Tuple[int, int, int]],
    ) -> None:
        """Draw polyline structure."""
        for image, drawing in zip(self.images, self.drawings):
            drawing.polygon(
                xy=[
                    (
                        round(x * image.size[0]) - 1,
                        round(y * image.size[1]) - 1,
                    )
                    for x, y in points
                ],
                fill=fill,
            )
        self.svg.add(
            self.svg.polyline(
                points=[(x * 2048, y * 2048) for x, y in points],
                fill=svgwrite.rgb(*fill),
            )
        )

    def draw_logo(
        self,
    ) -> None:
        """Draw a logo."""
        y = 0.5  # pylint: disable=invalid-name
        x = 0.5  # pylint: disable=invalid-name
        size = 1.0
        ring_ratio = 4.3 / 16
        crytal_ratio = 9 / 16
        inclination_x = 1 / 32
        inclination_y = 1 / 32
        x = x + size * inclination_x / 2  # pylint: disable=invalid-name
        y = y + size * inclination_y / 2  # pylint: disable=invalid-name
        size -= size * inclination_x

        ring_size = size * (1 - ring_ratio)
        crystal_size = size * crytal_ratio
        stroke = (size - ring_size) / 2

        self.circle(
            cx=x - size * inclination_x,
            cy=y - size * inclination_y,
            r=size / 2 - stroke / 2,
            fill=None,
            stroke=COLOR_1,
            stroke_width=stroke,
        )
        self.circle(
            cx=x,
            cy=y,
            r=size / 2 - stroke / 2,
            fill=None,
            stroke=COLOR_2,
            stroke_width=stroke,
        )

        x = x - size * inclination_x / 2  # pylint: disable=invalid-name
        y = y - size * inclination_y / 2  # pylint: disable=invalid-name

        y_top = y - crystal_size / 2
        y_bottom = y_top + crystal_size
        y_mid = y
        y_front = y_mid + crystal_size * inclination_y * 2

        x_left = x - crystal_size / 2
        x_right = x_left + crystal_size
        x_mid = x
        x_front = x_mid + crystal_size * inclination_x * 2
        self.polyline(
            points=[
                (x_mid, y_top),
                (x_left, y_mid),
                (x_mid, y_bottom),
                (x_right, y_mid),
            ],
            fill=COLOR_3,
        )
        self.polyline(
            points=[
                (x_mid, y_top),
                (x_left, y_mid),
                (x_mid, y_bottom),
                (x_front, y_front),
                (x_right, y_mid),
            ],
            fill=COLOR_2,
        )
        self.polyline(
            points=[
                (x_mid, y_top),
                (x_left, y_mid),
                (x_front, y_front),
            ],
            fill=COLOR_1,
        )

    def save(self, path: PathLike) -> None:
        """Save to path with attribution."""
        path = pathlib.Path(path)
        path.mkdir(parents=True, exist_ok=True)
        with (path / "favicon.svg").open("w", encoding="utf-8") as file:
            self.svg.write(file)
            file.write(
                "\n<!-- Created by Dashstrom, this logo is under CC BY "
                "https://creativecommons.org/licenses/by/4.0/ -->\n",
            )
        info = PngImagePlugin.PngInfo()
        info.add_text("Author", "Dashstrom")
        info.add_text("License", "CC BY")
        images: List[Image.Image] = []
        for image in self.images:
            width, height = image.size
            num_pixels = width * height
            num_colors = len(image.getcolors(num_pixels)) + 1
            # Max palette size = 256
            if num_colors > 256:
                num_colors = 256
            image = image.convert(mode="P", palette=1, colors=num_colors)
            if width <= 256 or height <= 256:
                images.append(image)
            image.save(
                path / f"favicon{width}x{height}.png",
                optimize=True,
                format="png",
                pnginfo=info,
            )

        images[-1].save(
            path / "favicon.ico",
            format="ICO",
            append_images=images,
            sizes=[image.size for image in images],
            bitmap_format="png",
        )


def generate_logos() -> None:
    """Generate all logo."""
    draw = PolyDraw()
    draw.draw_logo()
    draw.save("{{ cookiecutter.__pypi_name }}/docs/resources")


if __name__ == "__main__":
    generate_logos()
