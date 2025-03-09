#!/usr/bin/env python3
"""
Joust Game - Main Entry Point
A modern reimplementation of the classic arcade game Joust
"""
import os
import sys
import pygame
from game import Game

def main():
    """Main entry point for the Joust game."""
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()
    
    # Create game instance and run
    game = Game()
    game.run()
    
    # Clean up and exit
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    # Add the src directory to the path so we can import modules
    src_dir = os.path.dirname(os.path.abspath(__file__))
    if src_dir not in sys.path:
        sys.path.append(src_dir)
    
    main()
