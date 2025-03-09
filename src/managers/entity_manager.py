"""
Entity Manager - Manages all game entities
"""
import random
import pygame
from entities.player import Player
from entities.enemy import Bounder, Hunter, ShadowLord, Pterodactyl
from entities.platform import Platform, Lava
from utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORM_POSITIONS, 
    LAVA_Y_POSITION, PTERODACTYL_SPAWN_TIME,
    BOTTOM_PLATFORM_Y, BOTTOM_PLATFORM_CONFIGS
)

class EntityManager:
    """Manages all game entities and their interactions"""
    
    def __init__(self, game):
        """
        Initialize the entity manager
        
        Args:
            game (Game): Reference to the main game object
        """
        self.game = game
        
        # Entity lists
        self.players = []
        self.enemies = []
        self.eggs = []
        self.platforms = []
        self.lava = None
        self.pterodactyl = None
        
        # Pterodactyl spawn timer
        self.pterodactylTimer = 0
        self.pterodactylActive = False
        
        # Asset loader reference
        self.asset_loader = game.asset_loader
    
    def reset(self, numPlayers=1):
        """
        Reset all entities for a new game
        
        Args:
            numPlayers (int): Number of players (1 or 2)
        """
        # Clear entity lists
        self.players = []
        self.enemies = []
        self.eggs = []
        self.platforms = []
        self.pterodactyl = None
        self.pterodactylTimer = 0
        self.pterodactylActive = False
        
        # Create players
        self._createPlayers(numPlayers)
        
        # Create platforms
        self._createPlatforms()
        
        # Create lava
        self._createLava()
    
    def _createPlayers(self, numPlayers):
        """
        Create player entities
        
        Args:
            numPlayers (int): Number of players (1 or 2)
        """
        # Create player 1
        player1 = Player(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 1)
        player1.sprite = self.asset_loader.getImage("player1")
        self.players.append(player1)
        
        # Create player 2 if in multiplayer mode
        if numPlayers > 1:
            player2 = Player(2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 2)
            player2.sprite = self.asset_loader.getImage("player2")
            self.players.append(player2)
    
    def _createPlatforms(self):
        """Create platform entities"""
        # Create platforms based on predefined positions
        for x, y, width in PLATFORM_POSITIONS:
            platform = Platform(x, y, width)
            platform.sprite = self.asset_loader.getImage("platform")
            self.platforms.append(platform)
            
        # Create bottom platforms based on current wave
        self._createBottomPlatforms()
    
    def _createBottomPlatforms(self):
        """Create bottom platforms that change based on the current wave"""
        # Get current wave from level manager
        current_wave = self.game.level_manager.currentWave
        
        # Handle the case when current_wave is 0 (game start)
        # Use wave 1 configuration for wave 0
        if current_wave == 0:
            config_wave = 1
        else:
            # If wave is higher than our configs, use the highest defined config
            config_wave = min(current_wave, max(BOTTOM_PLATFORM_CONFIGS.keys()))
        
        # Get platform sections for this wave
        platform_sections = BOTTOM_PLATFORM_CONFIGS[config_wave]
        
        # Create each platform section
        for x, width in platform_sections:
            platform = Platform(x, BOTTOM_PLATFORM_Y, width)
            platform.sprite = self.asset_loader.getImage("platform")
            self.platforms.append(platform)
    
    def _createLava(self):
        """Create lava entity"""
        self.lava = Lava(LAVA_Y_POSITION, SCREEN_WIDTH)
        self.lava.sprite = self.asset_loader.getImage("lava")
    
    def spawnEnemies(self, numBounders, numHunters, numShadowLords):
        """
        Spawn enemies for a new wave
        
        Args:
            numBounders (int): Number of Bounder enemies to spawn
            numHunters (int): Number of Hunter enemies to spawn
            numShadowLords (int): Number of Shadow Lord enemies to spawn
        """
        # Spawn Bounders
        for _ in range(numBounders):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT // 2)
            enemy = Bounder(x, y)
            enemy.sprite = self.asset_loader.getImage("bounder")
            self.enemies.append(enemy)
        
        # Spawn Hunters
        for _ in range(numHunters):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT // 2)
            enemy = Hunter(x, y)
            enemy.sprite = self.asset_loader.getImage("hunter")
            self.enemies.append(enemy)
        
        # Spawn Shadow Lords
        for _ in range(numShadowLords):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT // 3)
            enemy = ShadowLord(x, y)
            enemy.sprite = self.asset_loader.getImage("shadow_lord")
            self.enemies.append(enemy)
        
        # Reset pterodactyl timer
        self.pterodactylTimer = PTERODACTYL_SPAWN_TIME // 16  # Convert ms to frames at 60 FPS
        self.pterodactylActive = False
    
    def spawnPterodactyl(self):
        """Spawn a pterodactyl"""
        if not self.pterodactylActive:
            # Spawn from left or right edge
            x = -50 if random.random() < 0.5 else SCREEN_WIDTH + 50
            y = random.randint(50, SCREEN_HEIGHT // 3)
            
            self.pterodactyl = Pterodactyl(x, y)
            self.pterodactyl.sprite = self.asset_loader.getImage("pterodactyl")
            self.pterodactylActive = True
            
            # Play pterodactyl screech sound
            self.game.sound_manager.play_sound("pterodactyl")
    
    def handle_event(self, event):
        """
        Handle pygame events for entities
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        # Player input is now handled in the update method to ensure continuous response
    
    def update(self):
        """Update all entities"""
        # Handle player input continuously
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.handleInput(keys)
            player.update()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.players, self.platforms)
            
            # Check for enemy-platform collisions
            self._handleEnemyPlatformCollisions(enemy)
            
            # Check for enemy-player collisions (jousting)
            self._handleJoustCollisions(enemy)
            
            # Remove inactive enemies
            if not enemy.active:
                self.enemies.remove(enemy)
        
        # Update eggs
        for egg in self.eggs[:]:
            egg.update(self.platforms)
            
            # Check for egg-player collisions (collection)
            self._handleEggCollections(egg)
            
            # Handle egg hatching
            if not egg.active:
                # If egg hatched into a new enemy
                if hasattr(egg, 'hatchedEnemy') and egg.hatchedEnemy:
                    self.enemies.append(egg.hatchedEnemy)
                
                # Remove inactive eggs
                self.eggs.remove(egg)
        
        # Update platforms
        for platform in self.platforms:
            platform.update()
        
        # Update lava
        if self.lava:
            self.lava.update()
        
        # Update pterodactyl
        if self.pterodactyl:
            self.pterodactyl.update(self.players, self.platforms)
            
            # Check for pterodactyl-player collisions
            self._handlePterodactylCollisions()
            
            # Remove inactive pterodactyl
            if not self.pterodactyl.active:
                self.pterodactyl = None
                self.pterodactylActive = False
        
        # Handle pterodactyl spawning
        self._handlePterodactylSpawning()
        
        # Check for player-platform collisions
        for player in self.players:
            self._handlePlayerPlatformCollisions(player)
    
    def _handlePlayerPlatformCollisions(self, player):
        """
        Handle collisions between a player and platforms
        
        Args:
            player (Player): The player to check
        """
        if not player.active or not player.isAlive:
            return
            
        # Store old position for collision resolution
        oldY = player.y
        oldVelocityY = player.velocityY
        
        # Create a slightly larger collision rect for more reliable platform detection
        # This helps catch collisions that might happen between frames
        expanded_rect = player.rect.inflate(4, 4)  # Expand collision rect slightly
        
        # Check for platform collisions
        landed = False
        for platform in self.platforms:
            # First check with the expanded rect for more reliable detection
            if expanded_rect.colliderect(platform.rect):
                # Check if landing on platform (player's feet are above or at the platform top and moving downward)
                if oldY + player.height <= platform.rect.top + 15 and player.velocityY > 0:
                    # Land on platform
                    player.y = platform.rect.top - player.height
                    player.rect.y = int(player.y)
                    player.velocityY = 0
                    landed = True
                    # Play landing sound
                    self.game.sound_manager.play_sound("land")
                    break  # Exit loop once landed
        
        # If we're falling fast, do an additional ray cast check to prevent tunneling
        if not landed and oldVelocityY > 10:
            # Simulate the player's position at multiple points during this frame
            steps = max(1, int(oldVelocityY / 5))  # More steps for higher velocities
            step_size = oldVelocityY / steps
            
            for step in range(1, steps + 1):
                # Calculate intermediate position
                test_y = oldY + step_size * step
                test_rect = pygame.Rect(player.rect.x, int(test_y), player.rect.width, player.rect.height)
                
                for platform in self.platforms:
                    if test_rect.colliderect(platform.rect):
                        if oldY + player.height <= platform.rect.top + 15:
                            # Land on platform
                            player.y = platform.rect.top - player.height
                            player.rect.y = int(player.y)
                            player.velocityY = 0
                            # Play landing sound
                            self.game.sound_manager.play_sound("land")
                            return  # Exit the method once landed
    
    def _handleEnemyPlatformCollisions(self, enemy):
        """
        Handle collisions between an enemy and platforms
        
        Args:
            enemy (Enemy): The enemy to check
        """
        if not enemy.active:
            return
            
        # Store old position for collision resolution
        oldY = enemy.y
        oldVelocityY = enemy.velocityY
        
        # Create a slightly larger collision rect for more reliable platform detection
        expanded_rect = enemy.rect.inflate(4, 4)  # Expand collision rect slightly
        
        # Check for platform collisions
        landed = False
        for platform in self.platforms:
            # First check with the expanded rect for more reliable detection
            if expanded_rect.colliderect(platform.rect):
                # Check if landing on platform (enemy's feet are above or at the platform top and moving downward)
                if oldY + enemy.height <= platform.rect.top + 15 and enemy.velocityY > 0:
                    # Land on platform
                    enemy.y = platform.rect.top - enemy.height
                    enemy.rect.y = int(enemy.y)
                    enemy.velocityY = 0
                    landed = True
                    break  # Exit loop once landed
        
        # If we're falling fast, do an additional ray cast check to prevent tunneling
        if not landed and oldVelocityY > 10:
            # Simulate the enemy's position at multiple points during this frame
            steps = max(1, int(oldVelocityY / 5))  # More steps for higher velocities
            step_size = oldVelocityY / steps
            
            for step in range(1, steps + 1):
                # Calculate intermediate position
                test_y = oldY + step_size * step
                test_rect = pygame.Rect(enemy.rect.x, int(test_y), enemy.rect.width, enemy.rect.height)
                
                for platform in self.platforms:
                    if test_rect.colliderect(platform.rect):
                        if oldY + enemy.height <= platform.rect.top + 15:
                            # Land on platform
                            enemy.y = platform.rect.top - enemy.height
                            enemy.rect.y = int(enemy.y)
                            enemy.velocityY = 0
                            return  # Exit the method once landed
    
    def _handleJoustCollisions(self, enemy):
        """
        Handle jousting collisions between an enemy and players
        
        Args:
            enemy (Enemy): The enemy to check
        """
        if not enemy.active:
            return
            
        for player in self.players:
            if not player.active or not player.isAlive or player.invincibilityTimer > 0:
                continue
                
            if player.collidesWith(enemy):
                # Jousting collision
                if player.isAbove(enemy):
                    # Player wins joust
                    egg = enemy.turnToEgg()
                    # Assign egg sprite
                    egg.sprite = self.asset_loader.getImage("egg")
                    self.eggs.append(egg)
                    
                    # Add score to player
                    player.addScore(enemy.points)
                    
                    # Play enemy defeat sound
                    self.game.sound_manager.play_sound("enemy_defeat")
                    
                    # Small upward boost for player
                    player.velocityY = -5
                elif enemy.isAbove(player):
                    # Enemy wins joust
                    player.die()
                    
                    # Play player death sound
                    self.game.sound_manager.play_sound("player_death")
                    
                    # Check for game over
                    if player.lives <= 0:
                        # Last player died, game over
                        if all(p.lives <= 0 for p in self.players):
                            self.game.game_over()
                else:
                    # Tie (bounce off each other)
                    player.velocityX = -player.velocityX
                    enemy.velocityX = -enemy.velocityX
                    
                    # Play bounce sound
                    self.game.sound_manager.play_sound("bounce")
    
    def _handleEggCollections(self, egg):
        """
        Handle egg collection by players
        
        Args:
            egg (Egg): The egg to check
        """
        if not egg.active:
            return
            
        for player in self.players:
            if not player.active or not player.isAlive:
                continue
                
            if player.collidesWith(egg):
                # Collect egg
                points = egg.collect()
                player.addScore(points)
                
                # Play egg collect sound
                self.game.sound_manager.play_sound("egg_collect")
    
    def _handlePterodactylCollisions(self):
        """Handle collisions between the pterodactyl and players"""
        if not self.pterodactyl or not self.pterodactyl.active:
            return
            
        for player in self.players:
            if not player.active or not player.isAlive or player.invincibilityTimer > 0:
                continue
                
            if player.collidesWith(self.pterodactyl):
                # Check for precise strike to mouth
                if player.isAbove(self.pterodactyl) and self.pterodactyl.isVulnerable(player.rect):
                    # Player defeats pterodactyl
                    self.pterodactyl.deactivate()
                    self.pterodactylActive = False
                    
                    # Add score to player
                    player.addScore(self.pterodactyl.points)
                    
                    # Play pterodactyl defeat sound
                    self.game.sound_manager.play_sound("pterodactyl_defeat")
                else:
                    # Pterodactyl defeats player
                    player.die()
                    
                    # Play player death sound
                    self.game.sound_manager.play_sound("player_death")
                    
                    # Check for game over
                    if player.lives <= 0:
                        # Last player died, game over
                        if all(p.lives <= 0 for p in self.players):
                            self.game.game_over()
    
    def _handlePterodactylSpawning(self):
        """Handle pterodactyl spawning logic"""
        # Only spawn pterodactyl if there are enemies and no pterodactyl already
        if len(self.enemies) > 0 and not self.pterodactylActive:
            # Decrease timer
            self.pterodactylTimer -= 1
            
            # Spawn pterodactyl when timer expires
            if self.pterodactylTimer <= 0:
                self.spawnPterodactyl()
    
    def render(self, screen):
        """
        Render all entities
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        # Render platforms
        for platform in self.platforms:
            platform.render(screen)
        
        # Render lava
        if self.lava:
            self.lava.render(screen)
        
        # Render eggs
        for egg in self.eggs:
            egg.render(screen)
        
        # Render enemies
        for enemy in self.enemies:
            enemy.render(screen)
        
        # Render pterodactyl
        if self.pterodactyl:
            self.pterodactyl.render(screen)
        
        # Render players
        for player in self.players:
            player.render(screen)
    
    def getActivePlayerCount(self):
        """
        Get the number of active players
        
        Returns:
            int: Number of active players
        """
        return sum(1 for player in self.players if player.lives > 0)
    
    def getAllEggsCollected(self):
        """
        Check if all eggs have been collected
        
        Returns:
            bool: True if all eggs are collected, False otherwise
        """
        return len(self.eggs) == 0
