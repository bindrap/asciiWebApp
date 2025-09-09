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

# Animation registry with frame generators
ANIMATION_GENERATORS = {
    "1": ("Orbital Motion", create_orbital_animation),
    "2": ("Binary Stars", create_binary_stars_animation),
    "3": ("Devil from Lava", lambda: create_ascii_art_reveal("devil")),
    "4": ("Matrix Rain", create_matrix_rain_animation),
    "5": ("Bouncing Ball", create_bouncing_ball_animation),
    "6": ("Wave Pattern", lambda: ["Wave pattern coming soon..."]),
    "7": ("DNA Helix", lambda: ["DNA helix coming soon..."]),
    "8": ("Spiral Galaxy", lambda: ["Spiral galaxy coming soon..."]),
    "9": ("Fire Effect", lambda: ["Fire effect coming soon..."]),
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
    app.run(debug=True, threaded=True, port=5000)