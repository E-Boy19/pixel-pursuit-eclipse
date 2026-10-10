# Pixel Pursuit: Eclipse 🌌

**Survive the swarm. Aim with precision. Fight until your last breath.**

Pixel Pursuit: Eclipse is a fullscreen 2D space-survival shooter built with Python and Pygame. Pilot a spaceship, fight off waves of hostile enemies, dodge incoming projectiles, and push your high score as far as possible.

Enemies spawn around the edges of the screen, pursue your spaceship, and fire bullets in your direction. Use movement, precise aiming, and alternate ammunition to survive for as long as you can.

## ✨ Features

- **Fullscreen Gameplay:** Automatically adapts to your display resolution.
- **Mouse-Based Aiming:** Aim your spaceship toward the cursor.
- **Dual Firing Modes:** Fire standard yellow bullets or faster red bullets with precise aiming.
- **Enemy AI:** Enemies pursue the player and periodically fire projectiles.
- **Collision Detection:** Uses pixel masks for accurate spaceship, enemy, and projectile collisions.
- **Health System:** Start with 250 HP and take damage from enemy collisions and bullets.
- **Dynamic Enemy Spawning:** New enemies appear as existing enemies are eliminated.
- **Animated Explosions:** Sprite-sheet animations for destroyed enemies and the player.
- **Score Tracking:** Earn points by eliminating enemies.
- **Persistent High Score:** Saves your highest score locally between sessions.
- **Sound Effects:** Audio feedback for firing, enemy destruction, and player destruction.
- **Pause and Resume:** Pause the action and resume when you're ready.

## 🎮 Controls

| Input | Action |
|---|---|
| `W` | Move up |
| `A` | Move left |
| `S` | Move down |
| `D` | Move right |
| Mouse movement | Aim the spaceship |
| Left mouse button | Fire a projectile |
| Right mouse button | Enable precision aiming for red bullets |
| `ESC` | Pause the game |
| Click anywhere | Resume while paused |
| `SPACE` | Start the game / restart after game over |
| `ESC` on the game-over screen | Quit the game |

**Combat tip:** Standard yellow bullets have some directional inaccuracy. Hold the right mouse button to use faster red bullets with more precise trajectories. Precision aiming temporarily disables WASD movement.

## 📂 Project Structure

```text
PixelPursuitEclipse/
├── game.py
├── setup/
│   ├── settings.py
│   ├── file_edit.py
│   ├── health.py
│   ├── bullets.py
│   ├── sprite_sheet.py
│   ├── target.py
│   ├── mobs.py
│   └── explosion.py
├── assets/
│   ├── fonts/
│   │   └── font.ttf
│   ├── sounds/
│   │   ├── laser.mp3
│   │   ├── enemy_blast.mp3
│   │   └── player_blast.mp3
│   └── images/
│       ├── background/
│       ├── bullets/
│       ├── targets/
│       ├── spritesheet/
│       ├── enemies/
│       └── player/
├── data/
│   └── data.data
├── requirements.txt
└── README.md
```

The `assets/` directory contains the graphics, font, and sound effects required by the game. The `data/` directory and high-score file are created automatically when the game starts.

Keep the asset files and directory structure intact; the program loads them using relative paths.

## 🚀 Getting Started

### Prerequisites

- Python 3 installed on your system.
- A desktop environment that supports fullscreen Pygame applications.
- Audio output for sound effects.

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/E-Boy19/pixel-pursuit-eclipse.git
```

**2. Navigate to the project directory**

```bash
cd PixelPursuitEclipse
```

**3. Create a virtual environment**

```bash
python3 -m venv .venv
```

**4. Activate the environment**

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install -r requirements.txt
```

**6. Launch the game**

```bash
python3 game.py
```

On Windows, you can also run:

```bash
python game.py
```

Press `SPACE` on the start screen to begin playing.

## ⚙️ Gameplay Mechanics

### Player Movement and Aiming

The spaceship moves with WASD and stays within the screen boundaries. Its orientation follows the mouse cursor, allowing you to aim independently of your movement direction.

### Weapons

The game features two projectile modes:

- **Yellow bullets:** Standard projectiles with slight directional inaccuracy.
- **Red bullets:** Faster, accurately aimed projectiles activated by holding the right mouse button.

Only one player projectile can be active at a time by default.

## 👨‍💻 Author

**Aaditya Garud**

Built with Python and Pygame 🐍

---

*Pixel Pursuit: Eclipse is a personal game development project exploring object-oriented programming, real-time game loops, enemy AI, projectile mechanics, collision detection, sprite-sheet animation, and persistent data storage.*
