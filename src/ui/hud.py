"""
HUD - Heads-Up Display for the game
"""
import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

class HUD:
    """Heads-Up Display showing score, lives, and wave information"""
    
    def __init__(self, game):
        """
        Initialize the HUD
        
        Args:
            game (Game): Reference to the main game object
        """
        self.game = game
        self.font = None
        self.smallFont = None
        self.loadFonts()
    
    def loadFonts(self):
        """Load fonts for the HUD"""
        # Use default pygame font for now
        self.font = pygame.font.Font(None, 36)
        self.smallFont = pygame.font.Font(None, 24)
    
    def render(self, screen):
        """
        Render the HUD
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        # Render player scores
        self._renderScores(screen)
        
        # Render player lives
        self._renderLives(screen)
        
        # Render wave number
        self._renderWaveInfo(screen)
    
    def _renderScores(self, screen):
        """
        Render player scores
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        # Player 1 score (top left)
        if len(self.game.entity_manager.players) > 0:
            player1 = self.game.entity_manager.players[0]
            score_text = self.font.render(f"SCORE: {player1.score}", True, WHITE)
            screen.blit(score_text, (20, 20))
        
        # Player 2 score (top right, if applicable)
        if len(self.game.entity_manager.players) > 1:
            player2 = self.game.entity_manager.players[1]
            score_text = self.font.render(f"SCORE: {player2.score}", True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))
    
    def _renderLives(self, screen):
        """
        Render player lives
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        # Player 1 lives (top left, below score)
        if len(self.game.entity_manager.players) > 0:
            player1 = self.game.entity_manager.players[0]
            lives_text = self.font.render(f"LIVES: {player1.lives}", True, WHITE)
            screen.blit(lives_text, (20, 60))
            
            # Draw life icons
            for i in range(player1.lives):
                # Draw a simple icon (will be replaced with sprite)
                pygame.draw.circle(screen, (255, 200, 0), (160 + i * 30, 70), 10)
        
        # Player 2 lives (top right, below score, if applicable)
        if len(self.game.entity_manager.players) > 1:
            player2 = self.game.entity_manager.players[1]
            lives_text = self.font.render(f"LIVES: {player2.lives}", True, WHITE)
            screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 20, 60))
            
            # Draw life icons
            for i in range(player2.lives):
                # Draw a simple icon (will be replaced with sprite)
                pygame.draw.circle(screen, (0, 200, 255), 
                                  (SCREEN_WIDTH - 160 - i * 30, 70), 10)
    
    def _renderWaveInfo(self, screen):
        """
        Render wave information
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        # Wave number (bottom center)
        wave_text = self.font.render(f"WAVE {self.game.level_manager.currentWave}", True, WHITE)
        screen.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, SCREEN_HEIGHT - 40))
        
        # Enemy count
        enemy_count = len(self.game.entity_manager.enemies)
        enemy_text = self.smallFont.render(f"ENEMIES: {enemy_count}", True, WHITE)
        screen.blit(enemy_text, (SCREEN_WIDTH // 2 - enemy_text.get_width() // 2, SCREEN_HEIGHT - 70))
        
        # Egg count
        egg_count = len(self.game.entity_manager.eggs)
        if egg_count > 0:
            egg_text = self.smallFont.render(f"EGGS: {egg_count}", True, WHITE)
            screen.blit(egg_text, (SCREEN_WIDTH // 2 - egg_text.get_width() // 2, SCREEN_HEIGHT - 100))
        
        # "Get Ready" text during wave transition
        if self.game.level_manager.waveComplete and self.game.level_manager.waveDelay > 0:
            ready_text = self.font.render("GET READY!", True, (255, 255, 0))
            screen.blit(ready_text, (SCREEN_WIDTH // 2 - ready_text.get_width() // 2, SCREEN_HEIGHT // 2))
