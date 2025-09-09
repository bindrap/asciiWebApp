# art_loader.py
import os

def load_ascii_art(filepath="asciiArt.txt"):
    """
    Load ASCII art from a file. Each block starts with a header (non-indented line),
    followed by indented or non-empty lines of art.
    Returns: dict of {header: [list of lines]}
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"ASCII art file not found: {filepath}")

    arts = {}
    current_name = None
    current_lines = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.rstrip("\n")

            # Skip empty lines
            if not stripped.strip():
                continue

            # Header: non-indented and non-empty
            if stripped == stripped.lstrip():
                if current_name and current_lines:
                    arts[current_name.lower()] = current_lines
                current_name = stripped.strip()
                current_lines = []
            else:
                # Part of art (may be indented)
                current_lines.append(stripped)

        # Don't forget the last block
        if current_name and current_lines:
            arts[current_name.lower()] = current_lines

    return arts