
# 🌌 Galaxy Runner

Galaxy Runner is a fast-paced, visually dynamic runner game prototype built using [Kivy](https://kivy.org/). It features a 3D-perspective grid and responsive controls that simulate motion through a galaxy-themed track.

## 🚀 Features

- Dynamic 3D perspective grid using custom transformation math.
- Smooth real-time animation with Kivy's `Clock`.
- Responsive controls for both desktop and mobile:
  - Keyboard (left/right arrows)
  - Touch input (tap left/right side)
- Auto-adaptive layout that scales with screen resolution.

## Demo

*(I will add very soon a screenshot or screen recording of the game here)*

## Requirements

- Python 3.10.11 (or compatible Python 3.7+ version)
- Kivy 2.1.0 or newer

### Installation

Install Kivy and required components:

```bash
pip install kivy[base] kivy_examples
````

Or, for full feature support (audio, video, etc.):

```bash
pip install kivy[full]
```

## How It Works

* **Vertical and horizontal lines** are rendered to simulate a 3D grid.
* **Perspective math** gives depth illusion as lines converge toward a vanishing point.
* The player doesn't move in the Y-axis — instead, the grid scrolls to simulate forward motion.
* **Keyboard or touch inputs** update horizontal offset for left/right movement.

## 🎮 Controls

| Platform | Control Method         | Action          |
| -------- | ---------------------- | --------------- |
| Desktop  | Arrow Keys (`←` / `→`) | Move left/right |
| Mobile   | Tap Left/Right         | Move left/right |

## Gameplay

* Tap or press left/right to simulate dodging obstacles (to be added).
* Vertical speed (`SPEED_Y`) controls how fast the grid scrolls.
* Horizontal speed (`SPEED_X`) changes based on input.
* Currently a visual prototype — ideal base for adding:

  * Obstacles
  * Scoring
  * Collision detection
  * Background music

## Code Overview

### Main Components:

* `MainWidget`: Core class that handles rendering and user input.
* `update()`: Called 60 times per second to update line positions.
* `transform_perspective()`: Applies vanishing point transformation.
* `on_keyboard_down()` / `on_touch_down()`: Input listeners.

### Perspective Calculation:

```python
y_normalized = y / self.perspective_point_y
perspective_factor = 1 - y_normalized
offset_x = (x - self.perspective_point_x) * perspective_factor
```

## 📁 Project Structure

```
galaxy-runner/
│
├── main.py       # Main Kivy application
├── README.md     # Project documentation
└── galaxy.kv     # Kivy language file for UI design and layout
```

## 🏗️ Running the Game

Make sure you're in the project folder and run:

```bash
python main.py
```

> Replace `main.py` with the actual filename if different.

## 📦 Future Enhancements

* Add player avatar
* Introduce obstacles and collision logic
* Scoring system
* Sound effects and background music
* Menus and pause functionality
* Export to Android/iOS via [Buildozer](https://buildozer.readthedocs.io/en/latest/)

## 📄 License

This project is licensed under the **MIT License**.
You're free to use, modify, and distribute it for personal or educational purposes.



