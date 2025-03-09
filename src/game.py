"""
Game - Main game loop and state management
"""
import os
import pygame
from enum import Enum, auto
from ui.menu import MainMenu, PauseMenu, GameOverMenu
from ui.hud import HUD
from managers.entity_manager import EntityManager
from managers.level_manager import LevelManager
from managers.score_manager import ScoreManager
from managers.sound_manager import SoundManager
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from utils.asset_loader import AssetLoader

class GameState(Enum):
    """Game state enumeration"""
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()

class Game:
    """Main game class handling the game loop, state management, and rendering"""
    
    def __init__(self):
        """Initialize the game"""
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Set up the game state
        self.state = GameState.MAIN_MENU
        self.running = True
        
        # Load assets
        self.asset_loader = AssetLoader()
        
        # Set up the managers
        self.entity_manager = EntityManager(self)
        self.level_manager = LevelManager(self)
        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()
        
        # Set up the UI
        self.main_menu = MainMenu(self)
        self.pause_menu = PauseMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.hud = HUD(self)
        
        # Game settings
        self.num_players = 1  # Default to single player
        self.difficulty = "Normal"  # Default difficulty
        self.game_mode = "co-op"  # Default multiplayer mode
        
        # Load assets
        self._load_assets()
    
    def _load_assets(self):
        """Load all game assets"""
        # Load images, sounds, and fonts
        self.asset_loader.loadImages()
        self.asset_loader.loadSounds()
        self.asset_loader.loadFonts()
        
        # Load sounds through sound manager
        self.sound_manager.load_sounds(self.asset_loader)
        
        # Play background music
        self.sound_manager.play_music("main_theme")
    
    def start_game(self, num_players=1, mode="co-op"):
        """Start a new game"""
        self.num_players = num_players
        self.game_mode = mode
        self.state = GameState.PLAYING
        
        # Reset game state
        self.score_manager.reset()
        self.level_manager.reset()
        self.entity_manager.reset(num_players)
        
        # Start the first wave
        self.level_manager.start_wave()
    
    def pause_game(self):
        """Pause the game"""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
            self.sound_manager.pause_music()
    
    def resume_game(self):
        """Resume the game"""
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
            self.sound_manager.resume_music()
    
    def game_over(self):
        """End the game"""
        self.state = GameState.GAME_OVER
        self.sound_manager.play_sound("game_over")
        
        # Check for high score
        if self.score_manager.check_high_score():
            # Set game over menu to high score entry mode
            self.game_over_menu.enteringHighScore = True
            self.game_over_menu.playerName = ""
    
    def quit_game(self):
        """Quit the game"""
        self.running = False
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            # Handle key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.pause_game()
                    elif self.state == GameState.PAUSED:
                        self.resume_game()
            
            # Pass events to the current state handler
            if self.state == GameState.MAIN_MENU:
                self.main_menu.handle_event(event)
            elif self.state == GameState.PLAYING:
                self.entity_manager.handle_event(event)
            elif self.state == GameState.PAUSED:
                self.pause_menu.handle_event(event)
            elif self.state == GameState.GAME_OVER:
                self.game_over_menu.handle_event(event)
    
    def update(self):
        """Update game state"""
        if self.state == GameState.PLAYING:
            # Update entities
            self.entity_manager.update()
            
            # Check for wave completion
            if self.level_manager.check_wave_complete():
                self.level_manager.next_wave()
    
    def render(self):
        """Render the game"""
        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        # Render based on game state
        if self.state == GameState.MAIN_MENU:
            self.main_menu.render(self.screen)
        elif self.state == GameState.PLAYING:
            # Render level background
            self.level_manager.render_background(self.screen)
            
            # Render entities
            self.entity_manager.render(self.screen)
            
            # Render HUD
            self.hud.render(self.screen)
        elif self.state == GameState.PAUSED:
            # Render the game (as background)
            self.level_manager.render_background(self.screen)
            self.entity_manager.render(self.screen)
            
            # Render pause menu
            self.pause_menu.render(self.screen)
        elif self.state == GameState.GAME_OVER:
            self.game_over_menu.render(self.screen)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Render
            self.render()
            
            # Cap the frame rate
            self.clock.tick(FPS)
