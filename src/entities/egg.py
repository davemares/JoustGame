"""
Egg - Egg entity class
"""
import pygame
from entities.entity import Entity
from utils.constants import GRAVITY, MAX_VERTICAL_SPEED, EGG_LIFETIME, EGG_POINTS

class Egg(Entity):
    """Egg entity that enemies turn into when defeated"""
    
    def __init__(self, x, y, enemyType):
        """
        Initialize an egg
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            enemyType (str): Type of enemy that created this egg
        """
        # Egg dimensions
        width = 32
        height = 32
        
        super().__init__(x, y, width, height)
        
        self.enemyType = enemyType
        self.points = EGG_POINTS
        self.lifetime = EGG_LIFETIME // 16  # Convert ms to frames at 60 FPS
        self.onGround = False
        self.bounceCount = 0
        self.maxBounces = 2
        
        # For rendering
        self.spriteName = "egg"
        
        # Initial velocity (eggs fall)
        self.velocityY = 2
        self.velocityX = 0
    
    def update(self, platforms=None):
        """
        Update egg state
        
        Args:
            platforms (list): List of platform entities
        """
        if not self.active:
            return
        
        # Decrease lifetime
        if self.onGround:
            self.lifetime -= 1
            if self.lifetime <= 0:
                self.hatch()
                return
        
        # Apply gravity if not on ground
        if not self.onGround:
            self.velocityY += GRAVITY * 1.2  # Eggs fall faster than players/enemies
            
            # Cap fall speed
            if self.velocityY > MAX_VERTICAL_SPEED:
                self.velocityY = MAX_VERTICAL_SPEED
        
        # Update position
        oldY = self.y
        super().update()
        
        # Check for platform collisions
        if platforms:
            self._handlePlatformCollisions(platforms, oldY)
    
    def _handlePlatformCollisions(self, platforms, oldY):
        """
        Handle collisions with platforms
        
        Args:
            platforms (list): List of platform entities
            oldY (float): Previous y position
        """
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Check if falling onto platform
                if oldY + self.height <= platform.rect.top and self.velocityY > 0:
                    # Land on platform
                    self.y = platform.rect.top - self.height
                    self.rect.y = int(self.y)
                    
                    # Bounce if not too many bounces
                    if self.bounceCount < self.maxBounces:
                        self.velocityY = -self.velocityY * 0.5  # Reduce bounce height
                        self.bounceCount += 1
                    else:
                        # Stop bouncing
                        self.velocityY = 0
                        self.onGround = True
                    
                    break
    
    def collect(self):
        """
        Collect the egg
        
        Returns:
            int: Points awarded for collecting the egg
        """
        self.deactivate()
        return self.points
    
    def getColor(self):
        """
        Get the egg's color for rendering when no sprite is available
        
        Returns:
            tuple: RGB color tuple
        """
        # Eggs are white
        return (255, 255, 255)
    
    def hatch(self):
        """
        Hatch the egg into a stronger enemy
        
        Returns:
            Enemy: The hatched enemy
        """
        from entities.enemy import Bounder, Hunter, ShadowLord
        
        # Create a stronger enemy based on the original type
        if self.enemyType == "BOUNDER":
            # Bounder eggs hatch into Hunters
            enemy = Hunter(self.x, self.y)
        elif self.enemyType == "HUNTER":
            # Hunter eggs hatch into Shadow Lords
            enemy = ShadowLord(self.x, self.y)
        else:
            # Shadow Lord eggs hatch into Bounders (cycle continues)
            enemy = Bounder(self.x, self.y)
        
        # Deactivate the egg
        self.deactivate()
        
        return enemy
