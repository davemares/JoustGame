"""
Entity - Base class for all game entities
"""
import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Entity:
    """Base class for all game entities"""
    
    def __init__(self, x, y, width, height):
        """
        Initialize an entity
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            width (int): Entity width
            height (int): Entity height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocityX = 0
        self.velocityY = 0
        self.rect = pygame.Rect(x, y, width, height)
        self.active = True
        self.sprite = None
        self.animation = None
        self.animationFrame = 0
        self.animationSpeed = 0.2
        self.facingRight = True
    
    def update(self):
        """Update entity state (to be overridden by subclasses)"""
        # Update position based on velocity
        self.x += self.velocityX
        self.y += self.velocityY
        
        # Update the rect position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Handle screen wrapping (horizontal only)
        self._handleScreenWrap()
    
    def _handleScreenWrap(self):
        """Handle screen wrapping for entities"""
        # Wrap horizontally
        if self.x < -self.width:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = -self.width
    
    def render(self, screen):
        """
        Render the entity
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        if not self.active:
            return
            
        if self.sprite:
            # Flip the sprite based on direction
            sprite_to_render = self.sprite
            if not self.facingRight:
                sprite_to_render = pygame.transform.flip(self.sprite, True, False)
            
            screen.blit(sprite_to_render, (self.rect.x, self.rect.y))
        else:
            # Fallback to a colored rectangle if no sprite is available
            color = self.getColor()
            pygame.draw.rect(screen, color, self.rect)
    
    def getColor(self):
        """
        Get the entity's color for rendering when no sprite is available
        
        Returns:
            tuple: RGB color tuple
        """
        # Default to white, subclasses can override this
        return (255, 255, 255)
    
    def collidesWith(self, other):
        """
        Check if this entity collides with another entity
        
        Args:
            other (Entity): The other entity to check collision with
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        return self.active and other.active and self.rect.colliderect(other.rect)
    
    def isAbove(self, other):
        """
        Check if this entity is above another entity
        
        Args:
            other (Entity): The other entity to check
            
        Returns:
            bool: True if this entity is above the other, False otherwise
        """
        # For jousting, we consider an entity above if its bottom is higher than
        # the other entity's midpoint
        return self.rect.bottom < other.rect.centery
    
    def deactivate(self):
        """Deactivate the entity (remove from game)"""
        self.active = False
