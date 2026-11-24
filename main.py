"""Ship It Friday -- make.fun entry.

One line, from the deployer's own mouth: the Friday-afternoon deploy
every engineer swears they will never do again, until next Friday.
It names the exact moment, owns the risk, and leaves the consequences
to Monday.

The program validates the line, writes it to
<MAKEFUN_OUTPUT_DIR>/entry.txt (the file the sealed gate checks:
UTF-8 text, 1 to 200 characters, not only whitespace) and prints it
to stdout.

Pure Python 3 standard library only; deterministic; no network.
SPDX-License-Identifier: MIT
"""

import os

# The entry line itself -- the judged content. It is a single literal
# so the wording can never drift between validation and output.
ENTRY_LINE = (
    "Friday 4:59 PM: I shipped it anyway -- the tests are red, "
    "the rollback plan is a prayer, and Monday me can deal with it."
)

# Sealed-gate limits for /output/entry.txt: 1 to 200 characters.
MIN_CHARS = 1
MAX_CHARS = 200

# Words the line must carry to stay on theme.
REQUIRED_WORDS = ("Friday", "ship")


def build_entry():
    """Return the entry line exactly as it must be judged."""
    return ENTRY_LINE


def validate_entry(line):
    """Check that a candidate line is a single well-formed entry.

    Raises ValueError with a specific reason for the first failing
    check, so a bad line is reported instead of silently stored.
    """
    if not isinstance(line, str):
        raise ValueError("entry must be text, got %s" % type(line).__name__)
    if line != line.strip():
        raise ValueError("entry must not start or end with whitespace")
    if not line:
        raise ValueError("entry must not be empty")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    length = len(line)
    if length < MIN_CHARS or length > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, outside the %d-%d range"
            % (length, MIN_CHARS, MAX_CHARS)
        )
    lowered = line.lower()
    for word in REQUIRED_WORDS:
        if word.lower() not in lowered:
            raise ValueError("entry must mention %r" % word)
    return line


def resolve_output_path():
    """Resolve the entry file from MAKEFUN_OUTPUT_DIR, default /output."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(directory, "entry.txt")


def write_entry(path, line):
    """Write the line to the entry file, creating its directory."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return path


def verify_entry(path, line):
    """Re-read the stored file and confirm it holds exactly the line."""
    with open(path, "r", encoding="utf-8") as handle:
        stored = handle.read()
    if stored != line + "\n":
        raise ValueError("stored entry does not match the validated line")
    return stored


def main():
    """Build, validate, store, verify, then print the entry line."""
    line = validate_entry(build_entry())
    path = write_entry(resolve_output_path(), line)
    verify_entry(path, line)
    print(line)


if __name__ == "__main__":
    main()
