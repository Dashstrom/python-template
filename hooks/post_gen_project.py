"""Hook run after cookiecutter."""
import json
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

PROJECT_DIRECTORY = pathlib.Path(os.path.curdir).resolve()
DOCS = PROJECT_DIRECTORY / "docs"
RESOURCES = DOCS / "resources"
RAND = random.SystemRandom()
USE_FORMATER = os.environ.get("USE_FORMATER", "True").lower() not in (
    "false",
    "",
    "off",
    "0",
)

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


def escape(value: str) -> bytes:
    """Minimal but unsafe escaping of string."""
    return json.dumps(value.strip(), ensure_ascii=False).encode("utf-8")


def remove_file(filepath: str) -> None:
    """Remove a file from project."""
    (PROJECT_DIRECTORY / filepath).unlink()


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
    if USE_FORMATER:
        try:
            subprocess.check_call(["make", "format"])
            print("[FORMAT] formating done !")
        except subprocess.CalledProcessError:
            print(
                "[FORMAT] This error is excpected : "
                "it occurs when `make format` run for the first time. "
                "You can ignore it."
            )


def main() -> None:
    """Main function for the hook."""
    if "none" == "{{ cookiecutter.cli }}":  # type: ignore
        project = "{{ cookiecutter.__project_slug }}"
        remove_file(os.path.join(project, "cli.py"))
        remove_file(os.path.join(project, "__main__.py"))
        remove_file(os.path.join("tests", "test_cli.py"))
    if "{{ cookiecutter.docker }}" != "True":  # type: ignore
        remove_file("Dockerfile")
        remove_file("docker-compose.yml")
        remove_file(".dockerignore")
    colorize_logo()
    run("make", "setup")
    autoformat()
    if "{{ cookiecutter.push }}" == "True":  # type: ignore
        run("git", "push", "-uf", "origin", "main")
    print("\n\nYou can activate venv with the following commands :")
    if os.name == "posix":
        print(
            "\n  cd {{ cookiecutter.__clone_name }} && source venv/bin/activate\n"
        )
    else:
        print(
            "\n  cd {{ cookiecutter.__clone_name }}; venv/Scripts/activate.ps1\n"
        )


if __name__ == "__main__":
    main()
