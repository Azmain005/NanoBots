# NanoBots - 3D Bloodstream Adventure Game

An exciting 3D game where you pilot a nanobot through the bloodstream, fighting viruses and collecting power-ups to save the body from infection. Built with Python and OpenGL.

## Features

- **Immersive 3D Environment**: Navigate through a dynamic bloodstream environment with realistic effects
- **Multiple Game Elements**:
  - Fight viruses with upgradeable weapons
  - Collect power-ups with unique abilities
  - Gather oxygen particles for health and points
  - Face challenging boss battles in each level
- **Progressive Difficulty**: 5 challenging levels with increasing difficulty
- **Power-ups System**:
  - Speed Boost (Blue) - Increases movement speed for 10 seconds
  - Magnet (Purple) - Attracts collectibles for 15 seconds
  - Laser (Red) - Enhanced weapon for 10 seconds
  - Health (Green) - Restores 25 HP
  - Invincibility (Pink) - Full heal + 10 seconds invincibility
- **Multiple View Modes**: Toggle between first-person and third-person perspectives

## Controls

- **Movement**: WASD or Arrow Keys
- **Shooting**: Spacebar or Left Mouse Button
- **View Toggle**: V (Switch between First/Third Person View)
- **Pause**: P
- **Restart**: R (when game is over)
- **Quit**: Q or ESC

## Requirements

- Python 3.x
- OpenGL
- PyOpenGL
- GLUT

## Installation

1. Ensure you have Python installed on your system
2. Install required dependencies:
   ```bash
   pip install PyOpenGL PyOpenGL-accelerate
   ```
3. Run the game:
   ```bash
   python nanobots.py
   ```

## Gameplay Tips

- Stay alert for boss battles at the end of each level
- Collect oxygen particles to maintain health and score points
- Use power-ups strategically, especially during boss fights
- Dodge enemy projectiles by moving around the tunnel
- The game speed increases gradually - stay focused!

## Development

This game is built using:

- Python for game logic
- OpenGL for 3D graphics rendering
- GLUT for window management and user input

## License

[MIT License](LICENSE)

## Acknowledgments

- OpenGL for providing the 3D graphics framework
- Python community for various resources and inspiration
