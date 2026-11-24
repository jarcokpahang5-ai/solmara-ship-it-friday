"""Ship It Friday -- make.fun entry.

One line, from the deployer's own mouth: the Friday-afternoon deploy
every engineer swears they will never do again, until next Friday.
It names the exact moment, owns the risk, and leaves the consequences
to Monday.

The program writes the line to <MAKEFUN_OUTPUT_DIR>/entry.txt (the
file the sealed gate checks: UTF-8 text, 1 to 200 characters, not
only whitespace) and also prints it to stdout.

Pure Python 3 standard library only; deterministic; no network.
SPDX-License-Identifier: MIT
"""

import os

# The line itself: one sentence about shipping it on a Friday.
LINE = (
    "Friday 4:59 PM: I shipped it anyway -- the tests are red, "
    "the rollback plan is a prayer, and Monday me can deal with it."
)

MAX_CHARS = 180


def output_path():
    """Resolve the entry file from MAKEFUN_OUTPUT_DIR, default /output."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(directory, "entry.txt")


def validate(line):
    """Check that the line is a single well-formed sentence."""
    if not isinstance(line, str):
        raise ValueError("line must be text")
    if not line or line != line.strip():
        raise ValueError("line must be a single non-blank line")
    if "\n" in line or "\r" in line:
        raise ValueError("line must not contain a line break")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    if "Friday" not in line:
        raise ValueError("line must mention Friday")
    if "ship" not in line.lower():
        raise ValueError("line must mention shipping")
    return line


def store(line):
    """Write the line to the entry file and print it."""
    path = output_path()
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print(line)


def main():
    """Validate first, so only a well-formed line is ever stored."""
    store(validate(LINE))


if __name__ == "__main__":
    main()
