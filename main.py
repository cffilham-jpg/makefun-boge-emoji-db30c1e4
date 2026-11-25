"""Write one octopus emoji as the agent's entire entry.
Its many arms evoke an agent coordinating several tool calls at once.
"""

import hashlib
import os
import tempfile
from pathlib import Path

LINE = "🐙"
CHAR_LIMIT = 16


def _resolve_output_dir() -> Path:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        path = Path(env_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    try:
        out = Path("out")
        out.mkdir(parents=True, exist_ok=True)
        return out
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-boge-emoji-db30c1e4-"))


def validate(path: Path) -> None:
    data = path.read_bytes()
    text = data.decode("utf-8")
    if text != LINE:
        raise ValueError("entry.txt must contain the selected emoji exactly")
    if not 1 <= len(text) <= CHAR_LIMIT:
        raise ValueError("entry.txt character count must be between 1 and 16")
    if len(text) != 1:
        raise ValueError("entry.txt must contain exactly one Unicode character")
    if "\n" in text or "\r" in text:
        raise ValueError("entry.txt must fit on one line without line breaks")
    if text.endswith("\n"):
        raise ValueError("entry.txt must not end with a newline")
    if text != text.strip():
        raise ValueError("entry.txt must not have whitespace at either edge")


def main() -> None:
    out_dir = _resolve_output_dir()
    entry = out_dir / "entry.txt"
    entry.write_bytes(LINE.encode("utf-8"))
    validate(entry)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
