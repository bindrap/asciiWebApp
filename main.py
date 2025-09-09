# main.py
import os
import time
import random
import argparse
from animations.math_animations import MATH_ANIMATIONS
from animations.ascii_animations import build_ascii_animations

MAX_WIDTH = 80  # For centering

# === Load all animations ===
def build_animations():
    animations = {}

    # Add math-based animations (e.g., "1", "2", ...)
    for key, (name, func) in MATH_ANIMATIONS.items():
        animations[key] = (name, func)

    # Add ASCII art animations (e.g., "9", "10", ...)
    ascii_anims, ascii_arts = build_ascii_animations(start_index=len(MATH_ANIMATIONS) + 1)
    animations.update(ascii_anims)

    return animations, ascii_arts

# === Utility: Print centered ASCII art ===
def print_ascii_art(lines):
    if not lines:
        return
    width = max(len(line) for line in lines)
    for line in lines:
        padding = " " * max(0, (MAX_WIDTH - width) // 2)
        print(padding + line)

# === Run animation in an infinite loop until Ctrl+C ===
def run_animation_loop(name, func):
    print(f"🔄 Running '{name}' in loop. Press Ctrl+C to stop.")
    time.sleep(1)
    try:
        while True:
            func()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user. Goodbye! 🎬")

# === Sort animation items by numeric key (handles "1", "2", ..., "10" correctly) ===
def sorted_animation_items(animations):
    """Return animations sorted by integer value of key."""
    return sorted(animations.items(), key=lambda item: int(item[0]))

# === Main ===
def main():
    animations, ascii_arts = build_animations()

    parser = argparse.ArgumentParser(description="🎨 Animated ASCII Art Collection 🎨")
    parser.add_argument(
        "animation_key",
        nargs="?",
        help="Animation number (e.g. 1 or -1). Negative shortcut: -1 = 1, -2 = 2, etc."
    )
    parser.add_argument(
        "--loop", "-L",
        action="store_true",
        help="Run animation in a continuous loop until interrupted"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available animations in order"
    )
    parser.add_argument(
        "--view", "-v",
        help="View raw ASCII art by name (case-insensitive)"
    )

    args = parser.parse_args()

    # Handle: --list
    if args.list:
        print("Available Animations:")
        for key, (name, _) in sorted_animation_items(animations):
            print(f"  {key}: {name}")
        return

    # Handle: --view
    if args.view:
        query = args.view.lower()
        matches = [name for name in ascii_arts.keys() if query in name]
        if not matches:
            print(f"No art found matching '{args.view}'")
            return
        for name in matches:
            print(f"\n🎨 {name.title()} 🎨\n")
            print_ascii_art(ascii_arts[name])
        return

    # Handle: Direct animation run (e.g. 1, -2)
    if args.animation_key:
        # Support negative shortcuts: -1 → "1", -2 → "2"
        key = args.animation_key.lstrip("-")

        if key not in animations:
            print(f"❌ Invalid animation number: {key}")
            print("Use --list to see available options.")
            return

        name, func = animations[key]

        if args.loop:
            run_animation_loop(name, func)
        else:
            print(f"▶️ Starting: {name}")
            time.sleep(1)
            func()
        return

    # === Interactive Menu ===
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("🎨 Animated ASCII Art Collection 🎨".center(MAX_WIDTH))
        print("=" * MAX_WIDTH)

        # Display animations in correct numeric order
        for key, (name, _) in sorted_animation_items(animations):
            print(f"  {key:2}: {name}")

        print("\n  0: Exit")
        print("  r: Random animation")
        print("  v: View raw art by name")
        print("  L: Run in Loop (e.g. 'L1' or 'L-2')")
        print("-" * MAX_WIDTH)

        choice = input("\nChoose an option: ").strip().lower()

        if choice == "0":
            print("\n👋 Thanks for watching!")
            break

        elif choice == "r":
            key = random.choice(list(animations.keys()))
            name, func = animations[key]
            print(f"\n🎲 Random: {name}")
            time.sleep(1)
            func()
            input("\nPress Enter to continue...")

        elif choice == "v":
            query = input("Enter art name to view: ").strip().lower()
            matches = [name for name in ascii_arts.keys() if query in name]
            if not matches:
                print(f"No match for '{query}'. Press Enter...")
                input()
            else:
                for name in matches:
                    print(f"\n📌 {name.title()}\n")
                    print_ascii_art(ascii_arts[name])
                print("\nPress Enter to continue...")
                input()

        elif choice.startswith("l"):  # Loop mode: L1, L-2
            key = choice[1:].lstrip("-")
            if key in animations:
                name, func = animations[key]
                run_animation_loop(name, func)
            else:
                print("❌ Invalid loop command. Use L1, L2, etc.")
                input("Press Enter...")

        elif choice in animations:
            name, func = animations[choice]
            print(f"\n▶️ Starting: {name}")
            time.sleep(1)
            func()
            input("\nPress Enter to continue...")

        else:
            print("❌ Invalid choice. Press Enter...")
            input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Animation stopped. Goodbye! 🎬")
    except Exception as e:
        print(f"\n💥 An error occurred: {e}")