"""Python scripts that run after your project is generated."""
import os
import pathlib
import re
import struct
import subprocess
import sys
import random
from typing import (
    IO,
    Callable,
    Tuple,
)
import zlib

RAND = random.SystemRandom()

PROJECT = pathlib.Path(os.getcwd()).resolve()
DOCS = PROJECT / "docs"
RESOURCES = DOCS / "resources"


COLOR_1 = (255, 0, 0)
COLOR_2 = (0, 255, 0)
COLOR_3 = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DEEP_BLUE = (0, 0, 64)
YELLOW_BRIGHT = (255, 255, 224)


def distance(
    color: Tuple[int, int, int], other: Tuple[int, int, int]
) -> float:
    """Get euclidian distance between two color."""
    return sum((c1 - c2) ** 2 for c1, c2 in zip(color, other)) ** 0.5


def generate_color() -> Tuple[int, int, int]:
    """Generate random color without black and white."""
    while True:
        color = (
            RAND.randint(16, 224),
            RAND.randint(16, 224),
            RAND.randint(16, 224),
        )
        if distance(color, BLACK) >= 64 and distance(color, WHITE) >= 32:
            return color


def colorize(
    color: Tuple[int, int, int], other: Tuple[int, int, int], ratio: float
) -> Tuple[int, int, int]:
    """Mix two colors."""
    return tuple(  # type: ignore[return-value]
        round(c1 * (1 - ratio) + c2 * ratio) for c1, c2 in zip(color, other)
    )


def edit_palette_png(
    data: IO[bytes],
    callback: Callable[[Tuple[int, int, int]], Tuple[int, int, int]],
) -> bytes:
    """Edit palette chunck inside png."""
    # Magic bytes (https://www.w3.org/TR/png/#5PNG-file-signature)
    magic = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    if data.read(8) != magic:
        raise ValueError()

    png = [magic]
    while True:
        chunck_raw_size = data.read(4)
        if len(chunck_raw_size) != 4:
            break
        chunck_size = struct.unpack("!I", chunck_raw_size)[0]
        chunck_type = data.read(4)
        chunck_data = data.read(chunck_size)
        chunck_crc = data.read(4)
        if chunck_type == b"PLTE":
            # PLTE Palette (https://www.w3.org/TR/png/#11PLTE)
            new_colors = []
            for i in range(len(chunck_data) // 3):
                color = tuple(chunck_data[i * 3 : (i + 1) * 3])
                new_color = callback(color)  # type: ignore[arg-type]
                new_colors.append(bytes(new_color))
            chunck_data = b"".join(new_colors)
            chunck_crc = struct.pack(
                "!I", zlib.crc32(chunck_type + chunck_data)
            )
        png.append(chunck_raw_size)
        png.append(chunck_type)
        png.append(chunck_data)
        png.append(chunck_crc)
    return b"".join(png)


def edit_palette_svg(
    data: IO[bytes],
    callback: Callable[[Tuple[int, int, int]], Tuple[int, int, int]],
) -> bytes:
    """Edit all color found in plaintext file."""

    def _callback(match: re.Match) -> bytes:
        color = tuple(map(int, match.groups()))
        new_color = callback(color)  # type: ignore[arg-type]
        return f"rgb({','.join(map(str, new_color))})".encode("utf-8")

    return re.sub(rb"rgb\((\d+),(\d+),(\d+)\)", _callback, data.read())


def colorize_logo() -> None:
    """Change color of all logo."""
    new_color = generate_color()
    shadow = colorize(new_color, DEEP_BLUE, 0.2)
    luminous = colorize(new_color, YELLOW_BRIGHT, 0.2)

    def callback(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        if color[0]:
            return shadow
        if color[1]:
            return new_color
        if color[2]:
            return luminous
        return color

    for path in RESOURCES.iterdir():
        if path.suffix == ".png":
            with path.open("rb") as reader:
                png = edit_palette_png(reader, callback)
            with path.open("wb") as writer:
                writer.write(png)
        elif path.suffix == ".svg":
            with path.open("rb") as reader:
                svg = edit_palette_svg(reader, callback)
            with path.open("wb") as writer:
                writer.write(svg)


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


def autoformat() -> None:
    """Format project."""
    print("[FORMAT] formating project with make format ...")
    try:
        subprocess.check_output(["make", "format"])
    except subprocess.CalledProcessError:
        pass
    print("[FORMAT] formating done !")


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
                "null",
                "",
            ):
                abspath = pathlib.Path(path).resolve()
                print(f"[REMOVE] {path}")
                abspath.unlink()


def git() -> None:
    """Instansiate Git repository."""
    if "{{ cookiecutter.git }}" == "True":
        run("git", "remote", "add", "origin", "{{ cookiecutter.__clone_url }}")
        if "{{ cookiecutter.push }}" == "True":
            run("git", "push", "-u", "origin", "main")


def main() -> None:
    """Main function."""
    remove_paths()
    colorize_logo()
    autoformat()
    git()


if __name__ == "__main__":
    main()
