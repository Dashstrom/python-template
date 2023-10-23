"""Change crlf to lf."""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent.parent


def crlf2lf():
    excludes = [ROOT / ".cache", ROOT / ".vscode", ROOT / ".git"]
    excludes_ext = [".png", ".ico"]
    lf2crlf = [".bat", ".cmd", ".ps1"]
    for path in ROOT.glob("**/*"):
        if path.is_file():
            for exclude in excludes:
                if exclude in path.parents:
                    break
            else:
                if path.suffix not in excludes_ext:
                    if path.suffix in lf2crlf:
                        re_source = re.compile(rb"[^\r]\n")
                        repl = b"\r\n"
                    else:
                        re_source = re.compile(rb"\r\n")
                        repl = b"\n"
                    data = path.read_bytes()
                    data = re_source.sub(repl, data)
                    path.write_bytes(data)
                    print(path)


if __name__ == "__main__":
    crlf2lf()
