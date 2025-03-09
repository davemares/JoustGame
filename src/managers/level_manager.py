"""
Level Manager - Manages game levels and wave progression
"""
import pygame
from utils.constants import WAVE_SETTINGS, ENEMY_SPAWN_DELAY, SCREEN_WIDTH, SCREEN_HEIGHT, EGG_COLLECT_ALL_BONUS

class LevelManager:
    """Manages game levels, waves, and progression"""
    
    def __init__(self, game):
        """
        Initialize the level manager
        
        Args:
            game (Game): Reference to the main game object
        """
        self.game = game
        
        # Wave tracking
        self.currentWave = 0
        self.waveComplete = False
        self.waveDelay = 0
        
        # Background elements
        self.background = None
    
    def reset(self):
        """Reset the level manager for a new game"""
        self.currentWave = 0
        self.waveComplete = False
        self.waveDelay = 0
        
        # Load background
        self._loadBackground()
    
    def _loadBackground(self):
        """Load the background image"""
        # Create a simple background (will be replaced with an actual image)
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((20, 20, 60))  # Dark blue background
        
        # Add some simple background elements
        for x in range(0, SCREEN_WIDTH, 100):
            for y in range(0, SCREEN_HEIGHT - 100, 100):
                # Draw a small star
                pygame.draw.circle(self.background, (255, 255, 200), (x + 50, y + 50), 1)
        
        # Draw a castle silhouette
        castle_points = [
            (100, SCREEN_HEIGHT - 200),  # Left base
            (100, SCREEN_HEIGHT - 300),  # Left wall
            (150, SCREEN_HEIGHT - 300),  # Left tower base
            (150, SCREEN_HEIGHT - 350),  # Left tower top
            (200, SCREEN_HEIGHT - 350),  # Left tower right
            (200, SCREEN_HEIGHT - 300),  # Left tower bottom
            (300, SCREEN_HEIGHT - 300),  # Wall
            (300, SCREEN_HEIGHT - 400),  # Main tower left
            (400, SCREEN_HEIGHT - 400),  # Main tower top
            (400, SCREEN_HEIGHT - 300),  # Main tower right
            (500, SCREEN_HEIGHT - 300),  # Wall
            (500, SCREEN_HEIGHT - 350),  # Right tower left
            (550, SCREEN_HEIGHT - 350),  # Right tower top
            (550, SCREEN_HEIGHT - 300),  # Right tower bottom
            (600, SCREEN_HEIGHT - 300),  # Right wall
            (600, SCREEN_HEIGHT - 200),  # Right base
        ]
        pygame.draw.polygon(self.background, (40, 40, 80), castle_points)
    
    def start_wave(self):
        """Start the current wave"""
        # Increment wave number
        self.currentWave += 1
        
        # Get enemy counts for this wave
        numBounders, numHunters, numShadowLords = self._getWaveEnemyCounts()
        
        # Spawn enemies
        self.game.entity_manager.spawnEnemies(numBounders, numHunters, numShadowLords)
        
        # Reset wave state
        self.waveComplete = False
        
        # Play wave start sound
        self.game.sound_manager.play_sound("wave_start")
    
    def _getWaveEnemyCounts(self):
        """
        Get the number of each enemy type for the current wave
        
        Returns:
            tuple: (numBounders, numHunters, numShadowLords)
        """
        # Use predefined wave settings if available
        if self.currentWave in WAVE_SETTINGS:
            return WAVE_SETTINGS[self.currentWave]
        
        # For waves beyond the predefined settings, scale difficulty
        baseWave = max(WAVE_SETTINGS.keys())
        baseBounders, baseHunters, baseShadowLords = WAVE_SETTINGS[baseWave]
        
        # Increase enemy counts based on wave number
        waveDiff = self.currentWave - baseWave
        numBounders = max(0, baseBounders + waveDiff // 3)
        numHunters = baseHunters + waveDiff // 2
        numShadowLords = baseShadowLords + waveDiff // 1
        
        return (numBounders, numHunters, numShadowLords)
    
    def check_wave_complete(self):
        """
        Check if the current wave is complete
        
        Returns:
            bool: True if wave is complete, False otherwise
        """
        # Wave is complete when all enemies are defeated
        if len(self.game.entity_manager.enemies) == 0:
            if not self.waveComplete:
                self.waveComplete = True
                self.waveDelay = ENEMY_SPAWN_DELAY // 16  # Convert ms to frames at 60 FPS
                
                # Check for all eggs collected bonus
                if self.game.entity_manager.getAllEggsCollected():
                    # Award bonus to all players
                    for player in self.game.entity_manager.players:
                        if player.active and player.isAlive:
                            player.addScore(EGG_COLLECT_ALL_BONUS)
                    
                    # Play bonus sound
                    self.game.sound_manager.play_sound("bonus")
            
            return True
        
        return False
    
    def next_wave(self):
        """Prepare for the next wave"""
        # Decrease wave delay
        if self.waveDelay > 0:
            self.waveDelay -= 1
            return
        
        # Start the next wave
        self.start_wave()
    
    def render_background(self, screen):
        """
        Render the level background
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            # Fallback to a solid color
            screen.fill((0, 0, 0))
        
        # Draw wave number
        font = pygame.font.Font(None, 36)
        wave_text = font.render(f"WAVE {self.currentWave}", True, (255, 255, 255))
        screen.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, SCREEN_HEIGHT - 40))
        
        # Draw "Get Ready" text during wave delay
        if self.waveComplete and self.waveDelay > 0:
            ready_text = font.render("GET READY!", True, (255, 255, 0))
            screen.blit(ready_text, (SCREEN_WIDTH // 2 - ready_text.get_width() // 2, SCREEN_HEIGHT // 2))
