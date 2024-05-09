"""Script for compress image."""

import argparse
from io import BytesIO
from PIL import Image
from pathlib import Path


def compress(path: str, inplace: bool = False) -> None:
    """Compress images using adaptive palette and optimize PNG."""
    if inplace:
        output = Path(path).resolve()
    else:
        output = Path(path).with_suffix(".compress.png").resolve()
    orignal_size = Path(path).stat().st_size
    base_im = Image.open(path).convert("RGBA")
    data = list(base_im.getdata())
    im = Image.new(base_im.mode, base_im.size)
    im.putdata(data)
    im = im.convert("P", palette=Image.ADAPTIVE, colors=256)
    with BytesIO() as stream:
        im.save(stream, optimize=True, format="PNG")
        size = len(stream.getbuffer())
        with output.open("wb") as output_stream:
            output_stream.write(stream.getvalue())
    print(f"Compress {orignal_size} to {size} at {output}")


def main() -> None:
    """Entrypoint for compress."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        help="Path to image.",
    )
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Compress inplace.",
    )
    args = parser.parse_args()
    compress(args.path, args.inplace)


if __name__ == "__main__":
    main()
