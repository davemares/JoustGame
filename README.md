# Joust Game

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
