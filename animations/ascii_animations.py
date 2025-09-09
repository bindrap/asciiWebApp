# animations/ascii_animations.py
import os
import time
import random
import re

ASCII_FILE = "asciiArt.txt"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def load_ascii_art(filepath=ASCII_FILE):
    """
    Parse asciiArt.txt into {header: [lines]} dict.
    A header is a line of plain text (letters/numbers/spaces only).
    """
    arts = {}
    current_name = None
    current_lines = []
    header_pattern = re.compile(r"^[A-Za-z0-9 ]+$")  # only word-like names

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.rstrip("\n")
            if not raw.strip():
                continue
            # treat it as a header only if it matches the pattern
            if header_pattern.match(raw.strip()):
                if current_name and current_lines:
                    arts[current_name.lower()] = current_lines
                current_name = raw.strip()
                current_lines = []
            else:
                current_lines.append(raw)

        if current_name and current_lines:
            arts[current_name.lower()] = current_lines

    return arts

def create_ascii_reveal_animation(ascii_lines):
    """Returns a function that animates the reveal & dissolve of given ASCII lines."""
    def animate():
        h = len(ascii_lines)
        w = max(len(row) for row in ascii_lines) if ascii_lines else 1
        chaos_chars = list("░▒▓█▄▀▐▌▆▇▉▊▋●◉✦✧*+#@")
        grid = [[random.choice(chaos_chars) for _ in range(w)] for _ in range(h)]

        def display():
            print("\n".join("".join(row) for row in grid))

        positions = [(r, c) for r in range(h) for c in range(len(ascii_lines[r]))]
        random.shuffle(positions)

        #clear()
        display()
        time.sleep(1)

        # Reveal
        for idx in range(0, len(positions), 5):
            #clear()
            for r, c in positions[idx:idx+5]:
                grid[r][c] = ascii_lines[r][c]
            display()
            time.sleep(0.05)

        time.sleep(2.0)

        # Dissolve
        random.shuffle(positions)
        for idx in range(0, len(positions), 5):
            #clear()
            for r, c in positions[idx:idx+5]:
                grid[r][c] = random.choice(chaos_chars)
            display()
            time.sleep(0.04)
    return animate

def build_ascii_animations(start_index=1):
    """
    Returns a dict of numeric keys -> (name, animation_fn) for all asciiArt.txt blocks.
    start_index lets math animations come first.
    """
    animations = {}
    ascii_arts = load_ascii_art()
    for idx, (header, lines) in enumerate(ascii_arts.items(), start=start_index):
        readable_name = header.title()
        animations[str(idx)] = (f"Animate {readable_name}", create_ascii_reveal_animation(lines))
    return animations, ascii_arts
