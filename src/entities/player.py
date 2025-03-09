"""
Player - Player entity class
"""
import pygame
from entities.entity import Entity
from utils.constants import (
    GRAVITY, FLAP_POWER, MAX_VERTICAL_SPEED, 
    HORIZONTAL_ACCELERATION, HORIZONTAL_DECELERATION, MAX_HORIZONTAL_SPEED,
    SCREEN_HEIGHT, LAVA_Y_POSITION, PLAYER_INVINCIBILITY_TIME
)

class Player(Entity):
    """Player entity class for the ostrich/stork rider"""
    
    def __init__(self, x, y, playerNumber=1):
        """
        Initialize a player
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            playerNumber (int): Player number (1 or 2)
        """
        # Player dimensions
        width = 64
        height = 64
        
        super().__init__(x, y, width, height)
        
        self.playerNumber = playerNumber
        self.lives = 3
        self.score = 0
        self.isFlapping = False
        self.isAlive = True
        self.respawnTimer = 0
        self.invincibilityTimer = 0
        
        # Control keys (default to player 1)
        if playerNumber == 1:
            self.leftKey = pygame.K_LEFT
            self.rightKey = pygame.K_RIGHT
            self.flapKey = pygame.K_SPACE
            # Player 1 rides an ostrich
            self.mountType = "ostrich"
        else:
            # Player 2 controls
            self.leftKey = pygame.K_a
            self.rightKey = pygame.K_d
            self.flapKey = pygame.K_w
            # Player 2 rides a stork
            self.mountType = "stork"
    
    def handleInput(self, keys):
        """
        Handle player input
        
        Args:
            keys (pygame.key.ScancodeWrapper): Pressed keys
        """
        if not self.isAlive or self.respawnTimer > 0:
            return
        
        # Horizontal movement
        if keys[self.leftKey]:
            self.velocityX -= HORIZONTAL_ACCELERATION
            self.facingRight = False
            if self.velocityX < -MAX_HORIZONTAL_SPEED:
                self.velocityX = -MAX_HORIZONTAL_SPEED
        elif keys[self.rightKey]:
            self.velocityX += HORIZONTAL_ACCELERATION
            self.facingRight = True
            if self.velocityX > MAX_HORIZONTAL_SPEED:
                self.velocityX = MAX_HORIZONTAL_SPEED
        else:
            # Decelerate when no keys are pressed
            if self.velocityX > 0:
                self.velocityX -= HORIZONTAL_DECELERATION
                if self.velocityX < 0:
                    self.velocityX = 0
            elif self.velocityX < 0:
                self.velocityX += HORIZONTAL_DECELERATION
                if self.velocityX > 0:
                    self.velocityX = 0
        
        # Flapping (vertical movement)
        if keys[self.flapKey]:
            self.flap()
        else:
            self.isFlapping = False
    
    def flap(self):
        """Make the player flap to gain altitude"""
        self.isFlapping = True
        self.velocityY -= FLAP_POWER * 0.2  # Apply a fraction of flap power per frame
        
        # Cap upward velocity
        if self.velocityY < -MAX_VERTICAL_SPEED:
            self.velocityY = -MAX_VERTICAL_SPEED
    
    def update(self):
        """Update player state"""
        # Handle respawn timer
        if self.respawnTimer > 0:
            self.respawnTimer -= 1
            if self.respawnTimer <= 0:
                self.respawn()
            return
        
        # Handle invincibility timer
        if self.invincibilityTimer > 0:
            self.invincibilityTimer -= 1
        
        if not self.isAlive:
            return
        
        # Apply gravity
        self.velocityY += GRAVITY
        
        # Cap downward velocity
        if self.velocityY > MAX_VERTICAL_SPEED:
            self.velocityY = MAX_VERTICAL_SPEED
        
        # Update position
        super().update()
        
        # Check for lava collision
        if self.y + self.height > LAVA_Y_POSITION:
            self.die()
    
    def render(self, screen):
        """
        Render the player
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        # If respawning or invincible, flash the player
        if self.respawnTimer > 0 or (self.invincibilityTimer > 0 and pygame.time.get_ticks() % 200 < 100):
            return
        
        super().render(screen)
    
    def getColor(self):
        """
        Get the player's color for rendering when no sprite is available
        
        Returns:
            tuple: RGB color tuple
        """
        # Player 1 is yellow, Player 2 is blue
        return (255, 200, 0) if self.playerNumber == 1 else (0, 200, 255)
    
    def die(self):
        """Handle player death"""
        if self.invincibilityTimer > 0:
            return
            
        self.isAlive = False
        self.active = False
        self.lives -= 1
        
        if self.lives > 0:
            # Start respawn timer
            self.respawnTimer = 90  # About 1.5 seconds at 60 FPS
        
        # Play death sound (will be implemented in sound manager)
    
    def respawn(self):
        """Respawn the player"""
        # Reset position to center of screen
        self.x = 400 if self.playerNumber == 1 else 800
        self.y = 300
        
        # Reset velocity
        self.velocityX = 0
        self.velocityY = 0
        
        # Reset state
        self.isAlive = True
        self.active = True
        self.invincibilityTimer = PLAYER_INVINCIBILITY_TIME // 16  # Convert ms to frames at 60 FPS
    
    def addScore(self, points):
        """
        Add points to player's score
        
        Args:
            points (int): Points to add
        """
        self.score += points
        
        # Check for extra life
        if (self.score // 10000) > ((self.score - points) // 10000):
            self.addLife()
    
    def addLife(self):
        """Add an extra life"""
        self.lives += 1
        # Play extra life sound (will be implemented in sound manager)
