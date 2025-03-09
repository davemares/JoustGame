# Joust Game

A Python implementation of the classic arcade game Joust with dynamic difficulty progression.

## Game Overview

In this reimagining of the classic arcade game, players control knights riding flying ostriches/storks, engaging in aerial jousting combat against various enemy types. The game features:

- Flying physics with gravity and flapping mechanics
- Jousting combat system (higher altitude wins)
- Multiple enemy types with different behaviors
- Dynamic platform system that changes with game progression
- Wave-based level progression with increasing difficulty

## Dynamic Bottom Platform System

The game features a dynamic bottom platform system that changes based on the current wave/level:
- Level 1: Full platform across the bottom (safe landing zone)
- Level 2: Two large platform sections with a gap in the middle
- Level 3: Three medium sections with larger gaps
- Level 4: Four smaller sections with even more gaps
- Level 5: Small scattered platforms
- Level 6+: Minimal platforms (highest difficulty)

## Installation

1. Clone this repository:
```
git clone https://github.com/davemares/JoustGame.git
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the game:
```
python src/main.py
```

## Controls

- **Player 1**: Arrow keys to move, Up to flap
- **Player 2** (if enabled): WASD to move, W to flap
- **P**: Pause game
- **ESC**: Exit to main menu

## Project Structure

- `src/` - Main source code directory
  - `entities/` - Game entities (player, enemies, platforms, etc.)
  - `managers/` - Game managers (entity, level, score, sound)
  - `ui/` - User interface components
  - `utils/` - Utility functions and constants
- `assets/` - Game assets (images, sounds, fonts)
- `data/` - Game data (high scores)

## Requirements

- Python 3.6+
- Pygame

A modern reimplementation of the classic arcade game Joust, where players control knights riding flying ostriches battling enemy knights on buzzards.

## Game Overview

Players control flying mounts (ostrich for Player 1, stork for Player 2) and battle waves of enemy knights by jousting - colliding with enemies while at a higher altitude. Defeated enemies turn into eggs that can be collected for bonus points.

### Core Features

- Single-player and multiplayer modes (co-op and versus)
- Multiple enemy types with increasing difficulty
- Platform-based arena with hazards (lava pit, pterodactyl)
- Wave-based progression with increasing challenge
- Score system with high score tracking

## Installation

1. Ensure you have Python 3.8+ installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python src/main.py
   ```

## Controls

- **Left/Right Arrow Keys**: Move horizontally
- **Spacebar**: Flap wings (gain altitude)
- **Escape**: Pause game
- **Player 2 Controls (Multiplayer)**:
  - **A/D**: Move horizontally
  - **W**: Flap wings

## Development

This game is built with Python and Pygame. The codebase is organized as follows:

- `src/`: Source code
  - `main.py`: Entry point
  - `game.py`: Main game loop and state management
  - `entities/`: Game entity classes (players, enemies, platforms)
  - `ui/`: User interface elements
  - `utils/`: Utility functions and helpers
- `assets/`: Game assets
  - `images/`: Sprites and visual elements
  - `sounds/`: Sound effects and music
  - `fonts/`: Game fonts

## License

This project is open source and available under the MIT License.
