# app.py
from flask import Flask, render_template, Response, request, jsonify
import threading
import queue
import time
import json

# Import your animation system
from main import build_animations, MAX_WIDTH

app = Flask(__name__)

# Build animations at startup
animations, ascii_arts = build_animations()

# Global queue for streaming animation frames
frame_queue = queue.Queue()

# Store current animation thread
current_thread = None
is_running = False

# === Routes ===

@app.route('/')
def index():
    # Sort animations by key (numeric)
    sorted_anims = sorted(animations.items(), key=lambda x: int(x[0]))
    return render_template('index.html', animations=sorted_anims, ascii_arts=ascii_arts)

@app.route('/start/<key>')
def start_animation(key):
    global current_thread, is_running

    if key not in animations:
        return jsonify({"error": "Animation not found"}), 404

    name, func = animations[key]

    def generate_frames():
        def stream_print(*args, **kwargs):
            line = " ".join(str(arg) for arg in args)
            # Center the line
            if len(line.strip()) > 0:
                padding = " " * max(0, (MAX_WIDTH - len(line)) // 2)
                frame = {"line": padding + line}
            else:
                frame = {"line": line}
            frame_queue.put(json.dumps(frame))
            time.sleep(0.01)  # Smooth out streaming

        # Redirect print to stream
        import builtins
        old_print = builtins.print
        builtins.print = stream_print

        try:
            frame_queue.put(json.dumps({"start": True, "name": name}))
            func()  # Run the animation
        except Exception as e:
            frame_queue.put(json.dumps({"error": str(e)}))
        finally:
            frame_queue.put(json.dumps({"done": True}))
            builtins.print = old_print

    # Stop any running animation
    if is_running:
        stop_animation()

    # Start new animation in thread
    is_running = True
    current_thread = threading.Thread(target=generate_frames)
    current_thread.start()

    return jsonify({"status": "started", "animation": name})

@app.route('/stream')
def stream():
    def event_stream():
        while is_running or not frame_queue.empty():
            try:
                data = frame_queue.get(timeout=1)
                yield f"data: {data}\n\n"
            except queue.Empty:
                continue
    return Response(event_stream(), mimetype="text/plain")

@app.route('/stop')
def stop_animation():
    global is_running
    is_running = False
    # Clear queue
    while not frame_queue.empty():
        try:
            frame_queue.get_nowait()
        except queue.Empty:
            break
    return jsonify({"status": "stopped"})

@app.route('/view/<name>')
def view_art(name):
    art = ascii_arts.get(name.lower())
    if not art:
        return jsonify({"error": "Art not found"}), 404
    return jsonify({"name": name.title(), "lines": art})

if __name__ == '__main__':
    app.run(debug=True, threaded=True)