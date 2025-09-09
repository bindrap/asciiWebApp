# animations/math_animations.py
import os
import time
import math
import random
import sys

def clear():
    # For web interface compatibility
    print("CLEAR_SCREEN")  # This will be caught by our web handler

def web_safe_sleep(duration):
    """Sleep function that works better with web streaming"""
    time.sleep(min(duration, 0.2))  # Cap sleep time for better web responsiveness

# === Orbital Motion ===
def animate_orbit():
    width, height = 20, 10
    for i in range(40):
        clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        angle = i * 0.3
        x = int(width // 2 + 7 * math.cos(angle))
        y = int(height // 2 + 4 * math.sin(angle))
        if 0 <= y < height and 0 <= x < width:
            grid[y][x] = "◉"
        grid[height//2][width//2] = "★"
        print("\n".join("".join(row) for row in grid))
        web_safe_sleep(0.15)

# === Binary Stars ===
def animate_binary_stars():
    width, height = 25, 12
    for i in range(40):
        clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        angle = i * 0.2
        r = 6
        x1 = int(width//2 + r * math.cos(angle))
        y1 = int(height//2 + r * math.sin(angle))
        x2 = int(width//2 + r * math.cos(angle + math.pi))
        y2 = int(height//2 + r * math.sin(angle + math.pi))
        if 0 <= y1 < height and 0 <= x1 < width:
            grid[y1][x1] = "⊛"
        if 0 <= y2 < height and 0 <= x2 < width:
            grid[y2][x2] = "⊗"
        grid[height//2][width//2] = "●"
        print("\n".join("".join(row) for row in grid))
        web_safe_sleep(0.12)

# === Devil rising from Lava ===
def animate_devil_from_lava():
    width, height = 40, 12
    lava_wave = [3,5,4,6,5,7,6,5,4,5,6,5,4,3,4,5,6,7,6,5]
    devil = [
        "  ▄████▄  ",
        " ██▀  ▀██ ",
        " ██    ██ ",
        "  ▀█▄▄█▀  ",
        "   ▄██▄   ",
        "  ▄▀  ▀▄  ",
        " █  ▄▄  █ ",
        " █ ████ █ ",
        "  █    █  ",
        "  ▀▀▀▀▀▀  "
    ]
    devil_h, devil_w = len(devil), len(devil[0])
    center_x = width // 2 - devil_w // 2
    for frame in range(30):
        clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        # lava
        for x in range(width):
            wave_h = int(10 - (lava_wave[x % len(lava_wave)] + math.sin(frame*0.3 + x*0.2)*1.5))
            wave_h = max(0, min(height-1, wave_h))
            for y in range(wave_h, height):
                grid[y][x] = random.choice(["█","▓","▒","░","*"])
        # devil rising
        dy = height + 10 - frame*1.5
        if dy < height:
            for dr in range(devil_h):
                gr = dy + dr
                if 0 <= gr < height:
                    for dc in range(devil_w):
                        ch = devil[dr][dc]
                        if ch != " " and 0 <= center_x+dc < width:
                            grid[int(gr)][center_x+dc] = ch
        # embers
        for _ in range(5):
            x = random.randint(0,width-1)
            y = random.randint(0,height//2)
            grid[y][x] = random.choice(["*","+","✦"])
        print("\n".join("".join(row) for row in grid))
        web_safe_sleep(0.15)

# === Matrix Rain ===
def animate_matrix_rain():
    width, height = 50, 15
    chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789"
    columns = []
    for x in range(width):
        columns.append({
            "y": random.randint(-height,0),
            "speed": random.choice([1,2,3]),
            "chars": [random.choice(chars) for _ in range(random.randint(5,15))]
        })
    for frame in range(80):
        clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        for x,col in enumerate(columns):
            for i,char in enumerate(col["chars"]):
                y = col["y"]+i
                if 0 <= y < height:
                    grid[y][x] = char
            col["y"] += col["speed"]
            if col["y"] > height+len(col["chars"]):
                col["y"] = random.randint(-height,-5)
                col["speed"] = random.choice([1,2,3])
                col["chars"] = [random.choice(chars) for _ in range(random.randint(5,15))]
        print("\n".join("".join(row) for row in grid))
        web_safe_sleep(0.08)

# === Bouncing Ball ===
def animate_bouncing_ball():
    width, height = 30, 12
    x, y = width//2, height//2
    dx, dy = 1, 1
    for frame in range(80):
        clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        for i in range(width): 
            grid[0][i] = grid[height-1][i] = "─"
        for i in range(height): 
            grid[i][0] = grid[i][width-1] = "│"
        grid[0][0], grid[0][-1], grid[-1][0], grid[-1][-1] = "┌","┐","└","┘"
        x += dx
        y += dy
        if x <= 1 or x >= width-2: 
            dx *= -1
        if y <= 1 or y >= height-2: 
            dy *= -1
        grid[y][x] = "●"
        print("\n".join("".join(row) for row in grid))
        web_safe_sleep(0.08)

# === Wave Pattern ===
def animate_wave():
    width, height = 60, 15
    for frame in range(80):
        clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        for x in range(width):
            y1 = int(height//2 + math.sin(frame*0.1 + x*0.1)*3)
            y2 = int(height//2 + math.sin(frame*0.15 + x*0.05)*2)
            y3 = int(height//2 + math.sin(frame*0.2 + x*0.15)*1.5)
            for y in [y1, y2, y3]:
                if 0 <= y < height: 
                    grid[y][x] = random.choice(["~","≈","∼"])
        print("\n".join("".join(row) for row in grid))
        web_safe_sleep(0.08)

# === DNA Helix ===
def animate_dna_helix():
    width, height = 30, 15
    for frame in range(60):
        clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        for y in range(height):
            a1 = frame*0.2 + y*0.5
            a2 = a1 + math.pi
            x1 = int(width//2 + 8*math.cos(a1))
            x2 = int(width//2 + 8*math.cos(a2))
            if 0 <= x1 < width: 
                grid[y][x1] = "O"
            if 0 <= x2 < width: 
                grid[y][x2] = "O"
            if y % 3 == 0 and 0 <= x1 < width and 0 <= x2 < width:
                for x in range(min(x1,x2)+1, max(x1,x2)):
                    if 0 <= x < width:
                        grid[y][x] = "─"
        print("\n".join("".join(row) for row in grid))
        web_safe_sleep(0.12)

# === Spiral Galaxy ===
def animate_spiral_galaxy():
    width, height = 50, 20
    for frame in range(100):
        clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        cx, cy = width//2, height//2
        for arm in range(4):
            off = arm * math.pi/2
            for r in range(1, min(width//2, height)):
                angle = off + frame*0.1 + r*0.3
                x = int(cx + r*math.cos(angle))
                y = int(cy + r*math.sin(angle)*0.5)
                if 0 <= x < width and 0 <= y < height:
                    grid[y][x] = random.choice(["●","◉","○","*","·","+","✦"])
        grid[cy][cx] = "◯"
        for _ in range(20):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if grid[y][x] == " ": 
                grid[y][x] = random.choice(["·","‧","∘"])
        print("\n".join("".join(row) for row in grid))
        web_safe_sleep(0.1)

# === Fire Effect ===
def animate_fire():
    width, height = 40, 20
    fire_chars = ["░", "▒", "▓", "█", "*", "+", "^", "~"]
    colors = [" ", ".", ":", "*", "o", "O", "#", "█"]
    
    for frame in range(100):
        clear()
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        # Generate fire base
        for x in range(width):
            intensity = random.uniform(0.5, 1.0)
            fire_height = int(height * intensity)
            
            for y in range(height - fire_height, height):
                distance_from_base = height - y
                char_index = min(len(colors) - 1, 
                               int(distance_from_base * len(colors) / fire_height))
                grid[y][x] = colors[char_index]
        
        # Add flickering
        for _ in range(width // 2):
            x = random.randint(0, width - 1)
            y = random.randint(height // 2, height - 1)
            grid[y][x] = random.choice(fire_chars)
        
        print("\n".join("".join(row) for row in grid))
        web_safe_sleep(0.1)

# === Registry ===
MATH_ANIMATIONS = {
    "1": ("Orbital Motion", animate_orbit),
    "2": ("Binary Stars", animate_binary_stars),
    "3": ("Devil from Lava", animate_devil_from_lava),
    "4": ("Matrix Rain", animate_matrix_rain),
    "5": ("Bouncing Ball", animate_bouncing_ball),
    "6": ("Wave Pattern", animate_wave),
    "7": ("DNA Helix", animate_dna_helix),
    "8": ("Spiral Galaxy", animate_spiral_galaxy),
    "9": ("Fire Effect", animate_fire),
}