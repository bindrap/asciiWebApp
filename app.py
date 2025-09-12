# app.py - Terminal Modal Version
from flask import Flask, render_template, request, jsonify
import threading
import time
import json
import random
import math
import os
import sys

# Import your animation system
from main import build_animations, MAX_WIDTH

app = Flask(__name__)

# Build animations at startup
animations, ascii_arts = build_animations()

# Global state for animation control
current_animation = None
animation_running = False
stop_requested = False

class TerminalEmulator:
    def __init__(self):
        self.buffer = []
        self.current_frame = []
        
    def clear(self):
        """Clear the terminal"""
        self.current_frame = []
        
    def print_line(self, text):
        """Add a line to the current frame"""
        self.current_frame.append(str(text))
        
    def get_frame(self):
        """Get current frame as string"""
        return '\n'.join(self.current_frame)
        
    def new_frame(self):
        """Start a new frame"""
        frame_content = self.get_frame()
        self.buffer.append(frame_content)
        return frame_content

# Create terminal emulator instance
terminal = TerminalEmulator()

def create_orbital_animation():
    """Create orbital motion animation frames"""
    frames = []
    width, height = 30, 15
    
    for i in range(60):
        terminal.clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        # Planet orbit
        angle = i * 0.2
        x = int(width // 2 + 10 * math.cos(angle))
        y = int(height // 2 + 6 * math.sin(angle))
        
        if 0 <= y < height and 0 <= x < width:
            grid[y][x] = "◉"
        
        # Central star
        grid[height//2][width//2] = "★"
        
        # Add some stars
        for _ in range(8):
            sx = random.randint(0, width-1)
            sy = random.randint(0, height-1)
            if grid[sy][sx] == " ":
                grid[sy][sx] = "·"
        
        frame = "\n".join("".join(row) for row in grid)
        frames.append(frame)
    
    return frames

def create_binary_stars_animation():
    """Create binary stars animation frames"""
    frames = []
    width, height = 35, 18
    
    for i in range(80):
        terminal.clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        # Binary star system
        angle = i * 0.15
        r = 8
        
        # Star 1
        x1 = int(width//2 + r * math.cos(angle))
        y1 = int(height//2 + r * math.sin(angle))
        
        # Star 2
        x2 = int(width//2 + r * math.cos(angle + math.pi))
        y2 = int(height//2 + r * math.sin(angle + math.pi))
        
        if 0 <= y1 < height and 0 <= x1 < width:
            grid[y1][x1] = "⊛"
        if 0 <= y2 < height and 0 <= x2 < width:
            grid[y2][x2] = "⊗"
            
        # Center of mass
        grid[height//2][width//2] = "●"
        
        # Background stars
        for _ in range(12):
            sx = random.randint(0, width-1)
            sy = random.randint(0, height-1)
            if grid[sy][sx] == " ":
                grid[sy][sx] = random.choice(["·", "∘", "•"])
        
        frame = "\n".join("".join(row) for row in grid)
        frames.append(frame)
    
    return frames

def create_matrix_rain_animation():
    """Create Matrix rain animation frames"""
    frames = []
    width, height = 60, 20
    chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789"
    
    # Initialize columns
    columns = []
    for x in range(width):
        columns.append({
            "y": random.randint(-height, 0),
            "speed": random.choice([1, 2, 3]),
            "chars": [random.choice(chars) for _ in range(random.randint(5, 15))],
            "color": random.choice(["normal", "bright"])
        })
    
    for frame_num in range(100):
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        for x, col in enumerate(columns):
            for i, char in enumerate(col["chars"]):
                y = col["y"] + i
                if 0 <= y < height:
                    grid[y][x] = char
            
            col["y"] += col["speed"]
            if col["y"] > height + len(col["chars"]):
                col["y"] = random.randint(-height, -5)
                col["speed"] = random.choice([1, 2, 3])
                col["chars"] = [random.choice(chars) for _ in range(random.randint(5, 15))]
        
        frame = "\n".join("".join(row) for row in grid)
        frames.append(frame)
    
    return frames

def create_bouncing_ball_animation():
    """Create bouncing ball animation frames"""
    frames = []
    width, height = 40, 20
    x, y = width//2, height//2
    dx, dy = 2, 1
    
    for i in range(100):
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        # Draw borders
        for j in range(width):
            grid[0][j] = "─"
            grid[height-1][j] = "─"
        for j in range(height):
            grid[j][0] = "│"
            grid[j][width-1] = "│"
        
        # Corners
        grid[0][0] = "┌"
        grid[0][width-1] = "┐"
        grid[height-1][0] = "└"
        grid[height-1][width-1] = "┘"
        
        # Move ball
        x += dx
        y += dy
        
        # Bounce off walls
        if x <= 1 or x >= width-2:
            dx *= -1
        if y <= 1 or y >= height-2:
            dy *= -1
        
        # Draw ball with trail
        grid[y][x] = "●"
        if 0 <= y-dy < height and 0 <= x-dx < width:
            grid[y-dy][x-dx] = "○"
        
        frame = "\n".join("".join(row) for row in grid)
        frames.append(frame)
    
    return frames

def create_ascii_art_reveal(art_name):
    """Create ASCII art reveal animation frames"""
    if art_name not in ascii_arts:
        return [f"ASCII art '{art_name}' not found"]
    
    frames = []
    art_lines = ascii_arts[art_name]
    
    # Create chaos version first
    chaos_chars = list("░▒▓█▄▀▐▌▆▇▉▊▋●◉✦✧*+#@")
    chaos_grid = []
    
    for line in art_lines:
        chaos_line = ""
        for char in line:
            if char == " ":
                chaos_line += " "
            else:
                chaos_line += random.choice(chaos_chars)
        chaos_grid.append(chaos_line)
    
    # Start with chaos
    frames.append("\n".join(chaos_grid))
    
    # Gradually reveal
    positions = []
    for row_idx, line in enumerate(art_lines):
        for col_idx, char in enumerate(line):
            if char != " ":
                positions.append((row_idx, col_idx))
    
    random.shuffle(positions)
    current_grid = [list(line) for line in chaos_grid]
    
    # Reveal in chunks
    chunk_size = max(1, len(positions) // 30)  # 30 frames of reveal
    
    for i in range(0, len(positions), chunk_size):
        chunk = positions[i:i+chunk_size]
        for row_idx, col_idx in chunk:
            current_grid[row_idx][col_idx] = art_lines[row_idx][col_idx]
        
        frame = "\n".join("".join(row) for row in current_grid)
        frames.append(frame)
    
    # Add final clean version
    frames.append("\n".join(art_lines))
    
    return frames

def create_devil_from_lava_animation():
    """Create Devil from Lava animation frames"""
    frames = []
    width, height = 50, 20
    lava_wave = [3, 5, 4, 6, 5, 7, 6, 5, 4, 5, 6, 5, 4, 3, 4, 5, 6, 7, 6, 5]
    
    # Enhanced devil ASCII art
    devil = [
        "      ▄▄████▄▄      ",
        "    ██▀▀    ▀▀██    ",
        "   ██  ▄▄  ▄▄  ██   ",
        "   ██ ████████ ██   ",
        "    ██  ████  ██    ",
        "     ▀██▄▄▄▄██▀     ",
        "       ██████       ",
        "      ▄██  ██▄      ",
        "     ██      ██     ",
        "    ██   ▄▄   ██    ",
        "   ██   ████   ██   ",
        "   ██  ██████  ██   ",
        "    ██  ████  ██    ",
        "     ▀█▄▄▄▄▄▄█▀     ",
        "        ████        ",
        "       ██  ██       "
    ]
    
    devil_h, devil_w = len(devil), len(devil[0]) if devil else 0
    center_x = width // 2 - devil_w // 2
    
    for frame in range(60):
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        # Create dynamic lava
        for x in range(width):
            base_wave = lava_wave[x % len(lava_wave)]
            wave_h = int(height - 5 - (base_wave + math.sin(frame * 0.3 + x * 0.2) * 2))
            wave_h = max(0, min(height - 1, wave_h))
            
            for y in range(wave_h, height):
                intensity = (height - y) / (height - wave_h + 1)
                if intensity > 0.8:
                    grid[y][x] = "█"
                elif intensity > 0.6:
                    grid[y][x] = "▓"
                elif intensity > 0.4:
                    grid[y][x] = "▒"
                elif intensity > 0.2:
                    grid[y][x] = "░"
                else:
                    grid[y][x] = random.choice(["*", "+", "·"])
        
        # Devil rising from lava
        devil_y = height - frame * 0.4
        if devil_y < height:
            for dr in range(devil_h):
                gr = int(devil_y + dr)
                if 0 <= gr < height:
                    for dc in range(devil_w):
                        if center_x + dc < width and devil[dr][dc] != " ":
                            grid[gr][center_x + dc] = devil[dr][dc]
        
        # Add embers and sparks
        for _ in range(8):
            x = random.randint(0, width - 1)
            y = random.randint(0, height // 2)
            if grid[y][x] == " ":
                grid[y][x] = random.choice(["*", "+", "✦", "✧", "◦"])
        
        frame_str = "\n".join("".join(row) for row in grid)
        frames.append(frame_str)
    
    return frames

def create_wave_animation():
    """Create Wave Pattern animation frames"""
    frames = []
    width, height = 70, 20
    
    for frame in range(100):
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        # Create multiple wave layers
        for x in range(width):
            # Primary wave
            y1 = int(height // 2 + math.sin(frame * 0.15 + x * 0.1) * 4)
            # Secondary wave
            y2 = int(height // 2 + math.sin(frame * 0.1 + x * 0.08) * 3)
            # Tertiary wave
            y3 = int(height // 2 + math.sin(frame * 0.2 + x * 0.12) * 2)
            
            # Draw waves with different characters
            waves = [(y1, "~"), (y2, "≈"), (y3, "∼")]
            
            for y, char in waves:
                if 0 <= y < height:
                    grid[y][x] = char
                
                # Add wave crests
                if abs(math.sin(frame * 0.15 + x * 0.1)) > 0.9:
                    if 0 <= y - 1 < height:
                        grid[y - 1][x] = "^"
                    if 0 <= y + 1 < height:
                        grid[y + 1][x] = "v"
        
        # Add foam particles
        for _ in range(10):
            x = random.randint(0, width - 1)
            y = random.randint(height // 3, 2 * height // 3)
            if grid[y][x] == " ":
                grid[y][x] = random.choice(["·", "°", "◦", "∘"])
        
        frame_str = "\n".join("".join(row) for row in grid)
        frames.append(frame_str)
    
    return frames

def create_dna_helix_animation():
    """Create DNA Helix animation frames"""
    frames = []
    width, height = 40, 25
    
    for frame in range(80):
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        center_x = width // 2
        
        # Draw the DNA double helix
        for y in range(height):
            # Calculate the angle for this row
            angle = frame * 0.2 + y * 0.4
            
            # Left and right strands
            x1 = int(center_x + 10 * math.cos(angle))
            x2 = int(center_x + 10 * math.cos(angle + math.pi))
            
            # Draw backbone
            if 0 <= x1 < width:
                grid[y][x1] = "●"
            if 0 <= x2 < width:
                grid[y][x2] = "●"
            
            # Draw base pairs (connecting lines) every few rows
            if y % 4 == 0:
                x_min, x_max = min(x1, x2), max(x1, x2)
                for x in range(x_min + 1, x_max):
                    if 0 <= x < width:
                        # Use different base pair characters
                        if (y // 4) % 4 == 0:
                            grid[y][x] = "─"
                        elif (y // 4) % 4 == 1:
                            grid[y][x] = "═"
                        elif (y // 4) % 4 == 2:
                            grid[y][x] = "⋯"
                        else:
                            grid[y][x] = "┅"
                
                # Add base letters at connection points
                mid_x = (x1 + x2) // 2
                if 0 <= mid_x < width:
                    bases = ["A", "T", "G", "C"]
                    grid[y][mid_x] = bases[(y // 4) % 4]
        
        frame_str = "\n".join("".join(row) for row in grid)
        frames.append(frame_str)
    
    return frames

def create_spiral_galaxy_animation():
    """Create Spiral Galaxy animation frames"""
    frames = []
    width, height = 60, 30
    
    for frame in range(120):
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        cx, cy = width // 2, height // 2
        
        # Create spiral arms
        for arm in range(4):
            arm_offset = arm * math.pi / 2
            
            # Draw spiral arm
            for r in range(1, min(width // 2, height)):
                angle = arm_offset + frame * 0.05 + r * 0.2
                
                # Calculate position
                x = int(cx + r * math.cos(angle))
                y = int(cy + r * math.sin(angle) * 0.6)  # Flatten vertically
                
                if 0 <= x < width and 0 <= y < height:
                    # Distance from center affects brightness
                    distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    
                    if distance < 3:
                        grid[y][x] = "◯"  # Core
                    elif distance < 8:
                        grid[y][x] = "●"  # Inner spiral
                    elif distance < 15:
                        grid[y][x] = "◉"  # Mid spiral
                    else:
                        grid[y][x] = random.choice(["○", "*", "·", "✦"])
        
        # Add background stars
        for _ in range(30):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if grid[y][x] == " ":
                grid[y][x] = random.choice(["·", "∘", "°", "+"])
        
        # Add central black hole
        if 0 <= cx < width and 0 <= cy < height:
            grid[cy][cx] = "⬤"
        
        frame_str = "\n".join("".join(row) for row in grid)
        frames.append(frame_str)
    
    return frames

def create_fire_animation():
    """Create Fire Effect animation frames"""
    frames = []
    width, height = 50, 25
    
    for frame in range(120):
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        # Create fire base
        base_height = height - 3
        
        for x in range(width):
            # Create random flame height
            flame_intensity = random.uniform(0.6, 1.0)
            flame_height = int(base_height * flame_intensity)
            
            # Add wind effect
            wind_offset = int(math.sin(frame * 0.1 + x * 0.1) * 2)
            
            for y in range(height - flame_height, height):
                actual_x = max(0, min(width - 1, x + wind_offset))
                
                # Distance from base affects character choice
                distance_from_base = height - y
                heat_intensity = distance_from_base / flame_height
                
                if heat_intensity > 0.9:
                    grid[y][actual_x] = "█"
                elif heat_intensity > 0.7:
                    grid[y][actual_x] = "▓"
                elif heat_intensity > 0.5:
                    grid[y][actual_x] = "▒"
                elif heat_intensity > 0.3:
                    grid[y][actual_x] = "░"
                elif heat_intensity > 0.1:
                    grid[y][actual_x] = random.choice(["*", "+", "^"])
                else:
                    grid[y][actual_x] = random.choice(["·", "°", "∘"])
        
        # Add sparks and embers
        for _ in range(15):
            x = random.randint(0, width - 1)
            y = random.randint(0, height // 2)
            if grid[y][x] == " ":
                grid[y][x] = random.choice(["*", "+", "✦", "✧", "◦", "°"])
        
        # Add flickering effect
        for _ in range(width // 3):
            x = random.randint(0, width - 1)
            y = random.randint(height // 2, height - 1)
            grid[y][x] = random.choice(["▄", "▀", "▌", "▐"])
        
        frame_str = "\n".join("".join(row) for row in grid)
        frames.append(frame_str)
    
    return frames

# Animation registry with frame generators
ANIMATION_GENERATORS = {
    "1": ("Orbital Motion", create_orbital_animation),
    "2": ("Binary Stars", create_binary_stars_animation),
    "3": ("Devil from Lava", create_devil_from_lava_animation),
    "4": ("Matrix Rain", create_matrix_rain_animation),
    "5": ("Bouncing Ball", create_bouncing_ball_animation),
    "6": ("Wave Pattern", create_wave_animation),
    "7": ("DNA Helix", create_dna_helix_animation),
    "8": ("Spiral Galaxy", create_spiral_galaxy_animation),
    "9": ("Fire Effect", create_fire_animation),
    "10": ("Animate Berserk Logo", lambda: create_ascii_art_reveal("berserk logo")),
    "11": ("Animate Monas", lambda: create_ascii_art_reveal("monas")),
    "12": ("Animate Onkar", lambda: create_ascii_art_reveal("onkar")),
    "13": ("Animate Cyberpunk", lambda: create_ascii_art_reveal("cyberpunk")),
}

@app.route('/')
def index():
    # Create a clean data structure for the template (no functions)
    animations_data = {}
    for key, (name, _) in ANIMATION_GENERATORS.items():
        animations_data[key] = name
    
    return render_template('index.html', animations=animations_data)

@app.route('/get_animation/<key>')
def get_animation(key):
    """Generate and return animation frames"""
    global animation_running, stop_requested
    
    if key not in ANIMATION_GENERATORS:
        return jsonify({"error": "Animation not found"}), 404
    
    name, generator = ANIMATION_GENERATORS[key]
    
    try:
        # Generate frames
        frames = generator()
        
        return jsonify({
            "name": name,
            "frames": frames,
            "frame_delay": 100  # milliseconds between frames
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_slideshow')
def get_slideshow():
    """Get all animations for slideshow"""
    try:
        slideshow_data = []
        
        for key in sorted(ANIMATION_GENERATORS.keys(), key=int):
            name, generator = ANIMATION_GENERATORS[key]
            frames = generator()
            slideshow_data.append({
                "key": key,
                "name": name,
                "frames": frames,
                "duration": 12000  # 12 seconds per animation
            })
        
        return jsonify({"animations": slideshow_data})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🎨 ASCII Animation Gallery (Terminal Modal Version) starting...")
    print("Available animations:", list(ANIMATION_GENERATORS.keys()))
    app.run(host='0.0.0.0', debug=False, threaded=True, port=5000)