# 🎨 ASCII Animation Gallery

A beautiful web-based ASCII art animation gallery with terminal modal interface. Experience dynamic ASCII animations in an authentic terminal environment through your browser.

![ASCII Animation Gallery](https://img.shields.io/badge/ASCII-Animation%20Gallery-brightgreen) ![Python](https://img.shields.io/badge/Python-3.7+-blue) ![Flask](https://img.shields.io/badge/Flask-2.0+-red) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **🎬 Interactive Animation Gallery**: Card-based interface showcasing all available animations
- **💻 Terminal Modal**: Authentic terminal experience with green-on-black ASCII display
- **🔄 Dynamic Animations**: Real-time orbital motion, matrix rain, bouncing balls, and more
- **🎭 ASCII Art Reveal**: Spectacular reveal animations for static ASCII art
- **📺 Slideshow Mode**: Automatically cycles through all animations (12 seconds each)
- **🎲 Random Animation**: Surprise yourself with a random animation selection
- **⏸️ Playback Controls**: Pause, resume, and close animations at any time
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **⌨️ Keyboard Controls**: ESC key to close, intuitive navigation

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Flask 2.0+

### Installation

1. **Clone or download the project**:
   ```bash
   git clone <your-repo-url>
   cd ascii-animation-gallery
   ```

2. **Install Flask** (if not already installed):
   ```bash
   pip install flask
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

5. **Click any animation card** to launch the terminal and enjoy! 🎉

## 📁 Project Structure

```
ascii-animation-gallery/
├── app.py                      # Main Flask application
├── main.py                     # Animation system integration
├── asciiArt.txt               # ASCII art definitions
├── templates/
│   └── index.html             # Main web interface template
├── animations/
│   ├── math_animations.py     # Mathematical animations (orbital, matrix, etc.)
│   ├── ascii_animations.py   # ASCII art reveal animations
│   └── art_loader.py          # ASCII art loading utilities
├── static/                    # (Optional) Static assets
└── README.md                  # This file
```

## 🎮 How to Use

### 🖱️ Web Interface

1. **Browse Animations**: View all available animations in the card gallery
2. **Click to Play**: Click any animation card to open the terminal modal
3. **Control Playback**: Use pause/resume buttons in the terminal header
4. **Close Terminal**: Click the ✕ button or press ESC key
5. **Slideshow Mode**: Click "🎬 Slideshow All" for automatic playback
6. **Random Fun**: Click "🎲 Random" for a surprise animation

### ⌨️ Keyboard Shortcuts

- **ESC**: Close terminal modal
- **Click outside modal**: Close terminal modal

### 🎬 Available Animations

#### 🌌 Dynamic Animations
1. **Orbital Motion** - Planet orbiting a star with background stars
2. **Binary Stars** - Two stars orbiting around their center of mass
3. **Matrix Rain** - Digital rain effect with Japanese characters
4. **Bouncing Ball** - Physics simulation of a ball bouncing in a box
5. **Test Animation** - Simple counter animation for testing

#### 🎭 ASCII Art Animations
6. **Berserk Logo** - Animated reveal of the iconic Berserk logo
7. **Monas** - Indonesian national symbol animation
8. **Onkar** - Sacred symbol reveal animation
9. **Cyberpunk Art** - Futuristic ASCII art animation

*Note: ASCII art animations use a spectacular "chaos-to-order" reveal effect*

## 🛠️ Technical Details

### Architecture

- **Backend**: Flask web framework with Python
- **Frontend**: Pure HTML5, CSS3, and JavaScript (no external dependencies)
- **Animation System**: Frame-based animation with configurable timing
- **Terminal Emulation**: CSS-styled terminal with authentic monospace display
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox

### Animation System

The gallery uses a sophisticated frame-based animation system:

```python
def create_animation():
    frames = []
    for i in range(total_frames):
        # Generate frame content
        frame = create_frame_content(i)
        frames.append(frame)
    return frames
```

### API Endpoints

- `GET /` - Main gallery interface
- `GET /get_animation/<key>` - Fetch specific animation frames
- `GET /get_slideshow` - Fetch all animations for slideshow mode

## 🎨 Adding New Animations

### Adding a Dynamic Animation

1. **Create animation function** in `app.py`:
   ```python
   def create_my_animation():
       frames = []
       for i in range(60):  # 60 frames
           # Create your frame content here
           frame = generate_frame(i)
           frames.append(frame)
       return frames
   ```

2. **Register in animation registry**:
   ```python
   ANIMATION_GENERATORS["10"] = ("My Animation", create_my_animation)
   ```

### Adding ASCII Art

1. **Add art to `asciiArt.txt`**:
   ```
   my art name
       ___
      /   \
     | o o |
      \___/
   ```

2. **Art will automatically appear** in the gallery with reveal animation

## 🎯 Customization

### Styling

Modify the CSS in `templates/index.html` to customize:
- **Colors**: Change the color scheme variables
- **Layout**: Adjust grid and flexbox properties
- **Terminal**: Modify terminal appearance and animations
- **Cards**: Customize animation card styling

### Animation Timing

Adjust animation speed by modifying:
```javascript
startAnimation(delay_in_milliseconds)
```

### Terminal Appearance

Customize terminal colors and fonts:
```css
.terminal-screen {
    background: #0d1117;
    color: #00ff41;  /* Matrix green */
    font-family: 'Courier New', monospace;
}
```

## 🐛 Troubleshooting

### Common Issues

**Q: Animations not showing**
- Ensure Flask is running without errors
- Check browser console for JavaScript errors
- Verify all template files are in the correct location

**Q: Template not found error**
- Ensure `templates/index.html` exists
- Check that the Flask app is looking for the correct template name

**Q: Blank terminal screen**
- Check network tab in browser dev tools
- Verify animation endpoints are responding
- Look for errors in Flask console

**Q: Animations too fast/slow**
- Modify the delay parameter in `startAnimation()`
- Adjust frame generation in animation functions

### Development Mode

Run with debug mode for detailed error information:
```python
app.run(debug=True, threaded=True, port=5000)
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-animation`
3. **Add your animation** following the patterns in the codebase
4. **Test thoroughly** in different browsers
5. **Submit a pull request**

### Animation Guidelines

- **Frame-based**: Use the frame-based system for consistency
- **Terminal-friendly**: Ensure animations work well in monospace font
- **Performance**: Keep frame counts reasonable (< 200 frames)
- **Responsive**: Test on different screen sizes

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **ASCII Art**: Various sources and original creations
- **Animation Concepts**: Inspired by classic terminal animations
- **Design**: Modern web design with retro terminal aesthetics

## 🔮 Future Enhancements

- [ ] **Sound Effects**: Add optional audio for animations
- [ ] **Custom Upload**: Allow users to upload their own ASCII art
- [ ] **Animation Editor**: Built-in frame-by-frame editor
- [ ] **Export Options**: Save animations as GIF or video
- [ ] **Themes**: Multiple color schemes and terminal styles
- [ ] **Performance Metrics**: FPS counter and performance monitoring
- [ ] **Fullscreen Mode**: Immersive fullscreen terminal experience

## 📞 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section** above
2. **Review the browser console** for error messages
3. **Check Flask logs** for backend errors
4. **Open an issue** on the project repository

## 🌟 Show Your Support

If you found this project helpful:
- ⭐ Star the repository
- 🍴 Fork and contribute
- 📢 Share with others
- 🐛 Report bugs and suggest features

---

**Made with ❤️ for ASCII art enthusiasts and terminal lovers everywhere!**

*Experience the magic of ASCII animation in your browser - where retro meets modern web technology.*