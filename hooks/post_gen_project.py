"""Python scripts that run after your project is generated."""
import pathlib
import subprocess
import sys
import operator
import os
import random
import xml.etree.ElementTree as ET
from math import sqrt
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Tuple,
    Union,
)

RAND = random.SystemRandom()
PathLike = Union[os.PathLike, pathlib.Path, str]


class Color:
    """Represent a color."""

    __slots__ = "red", "green", "blue"

    def __init__(self, r: float, g: float, b: float, /) -> None:
        """Instantiate color class."""
        self.red = r
        self.green = g
        self.blue = b

    def _apply(
        self,
        callback: Callable[[float, float], float],
        other: Any,
    ) -> "Color":
        if isinstance(other, Color):
            return Color(
                callback(self.red, other.red),
                callback(self.green, other.green),
                callback(self.blue, other.blue),
            )
        if isinstance(other, (float, int)):
            return Color(
                callback(self.red, other),
                callback(self.green, other),
                callback(self.blue, other),
            )
        return NotImplemented

    def __str__(self) -> str:
        return (
            f"{self.__class__.__qualname__}("
            f"{self.red},"
            f"{self.green},"
            f"{self.blue}"
            ")"
        )

    def __sub__(self, other: Any) -> "Color":
        return self._apply(operator.sub, other)

    def __add__(self, other: Any) -> "Color":
        return self._apply(operator.add, other)

    def __mul__(self, other: Any) -> "Color":
        return self._apply(operator.mul, other)

    def __pow__(self, other: Any) -> "Color":
        return self._apply(operator.pow, other)

    def dot(self, other: "Color") -> "Color":
        """Dot product."""
        return Color(
            self.green * other.blue - other.green * other.blue,
            self.blue * other.red - other.red * other.blue,
            self.red * other.green - other.red * other.green,
        )

    def norm(self) -> float:
        """Normalize color."""
        return self.euclidian_distance(BLACK)

    def manhattan_distance(self, other: "Color") -> float:
        """Return distance to other color."""
        return (
            self.red
            - other.red
            + self.green
            - other.green
            + self.blue
            - other.blue
        )

    def euclidian_distance(self, other: "Color") -> float:
        """Return distance to other color."""
        return sqrt(((self - other) ** 2).manhattan_distance(BLACK))

    def distance_to_straight(self, other: "Color", vector: "Color") -> float:
        """Return distance to two color."""
        return (other - self).dot(vector).norm() / vector.norm()

    @classmethod
    def random(cls) -> "Color":
        """Generate random color."""
        return cls(
            RAND.randint(0, 255),
            RAND.randint(0, 255),
            RAND.randint(0, 255),
        )

    def css(self) -> str:
        """Get css representation."""
        return (
            "rgb("
            f"{max(min(int(self.red), 255), 0)},"
            f"{max(min(int(self.green), 255), 0)},"
            f"{max(min(int(self.blue), 255), 0)}"
            ")"
        )

    @classmethod
    def improved_random(cls) -> "Color":
        """Generate random color without black, white and grey."""
        while True:
            color = cls(
                RAND.randint(16, 224),
                RAND.randint(16, 224),
                RAND.randint(16, 224),
            )
            if color.euclidian_distance(BLACK) >= 64:
                break
            break
        return color


XMLAtomicType = Union[str, int, float, Color, None]
XMLTupleType = Tuple[XMLAtomicType, ...]
XMLIterableType = List[Union[XMLTupleType, XMLAtomicType]]
XMLType = Union[XMLAtomicType, XMLTupleType, XMLIterableType]

WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
DEEP_BLUE = Color(0, 0, 64)
YELLOW_BRIGHT = Color(255, 255, 224)


def xml_serialyze_atomic(value: XMLAtomicType) -> str:
    """Serialize atomic xml value."""
    if value is None:
        return "none"
    elif isinstance(value, (str, int, float)):
        return str(value)
    elif isinstance(value, Color):
        return value.css()
    err_msg = f"Value {value} of type {type(value)} is not serialyze"
    raise TypeError(err_msg)


def xml_serialyze_tuple(value: XMLTupleType) -> str:
    """Serialize tuple xml value."""
    if not isinstance(value, tuple):
        err_msg = f"Value {value} of type {type(value)} is not serialyze"
        raise TypeError(err_msg)
    return ",".join(xml_serialyze_atomic(obj) for obj in value)


def xml_serialyze_list(value: XMLIterableType) -> str:
    """Serialize list xml value."""
    if not isinstance(value, list):
        err_msg = f"Value {value} of type {type(value)} is not serialyze"
        raise TypeError(err_msg)
    result = []
    for obj in value:
        try:
            result.append(xml_serialyze_atomic(obj))  # type: ignore[arg-type]
        except TypeError:
            result.append(xml_serialyze_tuple(obj))  # type: ignore[arg-type]
    return " ".join(result)


def xml_serialyze(value: XMLType) -> str:
    """Serialize xml value."""
    try:
        return xml_serialyze_atomic(value)  # type: ignore[arg-type]
    except TypeError:
        try:
            return xml_serialyze_tuple(value)  # type: ignore[arg-type]
        except TypeError:
            try:
                return xml_serialyze_list(value)  # type: ignore[arg-type]
            except TypeError as err:
                raise err from None


class Draw:
    """Class for create logo."""

    def __init__(self) -> None:
        self.doc = ET.Element(
            "svg",
            width="2048",
            height="2048",
            version="1.2",
            xmlns="http://www.w3.org/2000/svg",
            baseProfile="tiny",
        )
        self.xml = ET.ElementTree(self.doc)

    def draw(self, name: str, **attrib: XMLType) -> None:
        """Draw a figure."""
        ET.SubElement(
            self.doc,
            name,
            {
                attr.replace("_", "-"): xml_serialyze(value)
                for attr, value in attrib.items()
            },
        )

    def draw_logo(
        self, x: float, y: float, size: float, color: Optional["Color"] = None
    ) -> None:
        """Draw a logo."""
        if color is None:
            color = Color.improved_random()
        ring_ratio = 0.2
        crytal_ratio = 0.7
        inclination_x = 0.05
        inclination_y = 0.05
        x = x + size * inclination_x / 2
        y = y + size * inclination_y / 2
        size -= size * inclination_x
        shadow = color * 0.8 + DEEP_BLUE * 0.2
        luminous = color * 0.9 + YELLOW_BRIGHT * 0.1

        ring_size = size * (1 - ring_ratio)
        crystal_size = size * crytal_ratio
        stroke = (size - ring_size) / 2

        self.draw(
            "circle",
            cx=x - size * inclination_x,
            cy=y - size * inclination_y,
            r=size / 2 - stroke / 2,
            fill=None,
            stroke=shadow,
            stroke_width=stroke,
        )
        self.draw(
            "circle",
            cx=x,
            cy=y,
            r=size / 2 - stroke / 2,
            fill=None,
            stroke=color,
            stroke_width=stroke,
        )

        x = x - size * inclination_x / 2
        y = y - size * inclination_y / 2

        y_top = y - crystal_size / 2
        y_bottom = y_top + crystal_size
        y_mid = y
        y_front = y_mid + crystal_size * inclination_y * 2

        x_left = x - crystal_size / 2
        x_right = x_left + crystal_size
        x_mid = x
        x_front = x_mid + crystal_size * inclination_x * 2
        self.draw(
            "polyline",
            points=[
                (x_mid, y_top),
                (x_left, y_mid),
                (x_mid, y_bottom),
                (x_right, y_mid),
            ],
            fill=luminous,
        )
        self.draw(
            "polyline",
            points=[
                (x_mid, y_top),
                (x_left, y_mid),
                (x_mid, y_bottom),
                (x_front, y_front),
                (x_right, y_mid),
            ],
            fill=color,
        )
        self.draw(
            "polyline",
            points=[
                (x_mid, y_top),
                (x_left, y_mid),
                (x_front, y_front),
            ],
            fill=shadow,
        )

    def save(self, path: PathLike) -> None:
        """Save to path with attribution."""
        path = pathlib.Path(path)
        path.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as file:
            self.xml.write(file, encoding="utf-8")
            file.write(
                b"\n<!-- Created by Dashstrom, this logo is under CC BY "
                b"https://creativecommons.org/licenses/by/4.0/ -->",
            )


def generate_logo(path: PathLike) -> None:
    """Main function."""
    draw = Draw()
    draw.draw_logo(1024, 1024, size=2048)
    draw.save(path)


REPO = pathlib.Path(__file__).parent.resolve()
PROJECT = REPO / "{{ cookiecutter.__pypi_name }}"

REMOVED_IF_FALSE = {
    "{{ cookiecutter.docker }}": [
        "Dockerfile",
        "docker-compose.yml",
        ".dockerignore",
    ],
    "{{ cookiecutter.cli }}": [
        "{{ cookiecutter.__project_slug }}/cli.py",
        "{{ cookiecutter.__project_slug }}/__main__.py",
        "tests/test_cli.py",
    ],
}


def fatal(text: str) -> None:
    """Print error and exit."""
    print(f"ERROR: {text}", file=sys.stderr, flush=True)
    sys.exit(1)


def run(*args: str) -> None:
    """Run command on computer."""
    print("[RUN]", " ".join(args))
    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError:
        fatal("Command failed, exiting")


def remove_paths() -> None:
    """Remove paths."""
    for pred, paths in REMOVED_IF_FALSE.items():
        for path in paths:
            if pred.lower().strip() in (
                "no",
                "false",
                "n",
                "non",
                "0",
                "none",
                "",
            ):
                abspath = pathlib.Path(path).resolve()
                abspath.unlink()


def git() -> None:
    """Instansiate Git repository."""
    if "{{ cookiecutter.git }}" == "True":
        run("git", "init")
        run("git", "add", "*")
        run("git", "commit", "-m", "Initial commit")
        run("git", "branch", "-M", "main")
        run("git", "remote", "add", "origin", "{{ cookiecutter.__clone_url }}")
        # run("git", "push", "-u", "origin", "main")


def setup() -> None:
    """Setup virtual environnement and pre-commit."""
    if "{{ cookiecutter.setup }}" == "True":
        run("make", "setup")


def main() -> None:
    """Main function."""
    remove_paths()
    git()
    setup()
    generate_logo(PROJECT / "docs" / "resources" / "favicon.svg")


if __name__ == "__main__":
    main()
