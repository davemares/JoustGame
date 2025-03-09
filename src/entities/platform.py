"""
Platform - Platform entity class
"""
import pygame
from entities.entity import Entity
from utils.constants import PLATFORM_HEIGHT, WHITE

class Platform(Entity):
    """Platform entity that players and enemies can land on"""
    
    def __init__(self, x, y, width):
        """
        Initialize a platform
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            width (int): Platform width
        """
        height = PLATFORM_HEIGHT
        
        super().__init__(x, y, width, height)
        
        # Platforms don't move
        self.velocityX = 0
        self.velocityY = 0
        
        # For rendering
        self.spriteName = "platform"
    
    def update(self):
        """Update platform state (platforms don't move)"""
        pass
    
    def render(self, screen):
        """
        Render the platform
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        if self.sprite:
            # Use sprite if available, but stretch it to match the platform width
            # We need to scale the sprite to match the platform's width
            scaled_sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
            screen.blit(scaled_sprite, (self.rect.x, self.rect.y))
        else:
            # Fallback to a rectangle
            pygame.draw.rect(screen, self.getColor(), self.rect)
            
            # Add some detail to the platform
            pygame.draw.line(screen, (200, 200, 200), 
                            (self.rect.left, self.rect.top), 
                            (self.rect.right, self.rect.top), 2)
    
    def getColor(self):
        """
        Get the platform's color for rendering when no sprite is available
        
        Returns:
            tuple: RGB color tuple
        """
        # Platforms are brown
        return (139, 69, 19)


class Lava(Entity):
    """Lava entity at the bottom of the screen"""
    
    def __init__(self, y, width):
        """
        Initialize the lava
        
        Args:
            y (float): Y position (top of lava)
            width (int): Lava width (usually screen width)
        """
        from utils.constants import LAVA_HEIGHT, LAVA_COLOR
        
        height = LAVA_HEIGHT
        x = 0  # Lava spans the entire screen width
        
        super().__init__(x, y, width, height)
        
        self.color = LAVA_COLOR
        self.bubbleTimer = 0
        self.bubbles = []  # List of bubble positions (x, y, size, speed)
        
        # For rendering
        self.spriteName = "lava"
    
    def update(self):
        """Update lava state (animate bubbles)"""
        # Increment bubble timer
        self.bubbleTimer += 1
        
        # Create new bubbles
        if self.bubbleTimer % 15 == 0:  # Every 15 frames
            import random
            
            # Add a new bubble
            bubble_x = random.randint(0, self.width)
            bubble_y = self.y + self.height - 5  # Start near bottom
            bubble_size = random.randint(3, 8)
            bubble_speed = random.uniform(0.5, 1.5)
            
            self.bubbles.append([bubble_x, bubble_y, bubble_size, bubble_speed])
        
        # Update existing bubbles
        for i in range(len(self.bubbles) - 1, -1, -1):
            # Move bubble upward
            self.bubbles[i][1] -= self.bubbles[i][3]
            
            # Remove bubble if it reaches the top of lava
            if self.bubbles[i][1] < self.y:
                self.bubbles.pop(i)
    
    def render(self, screen):
        """
        Render the lava
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        if self.sprite:
            # Use sprite if available
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            # Fallback to a rectangle with animated bubbles
            pygame.draw.rect(screen, self.getColor(), self.rect)
    
    def getColor(self):
        """
        Get the lava's color for rendering when no sprite is available
        
        Returns:
            tuple: RGB color tuple
        """
        # Use the color from constants
        return self.color
    
    def render(self, screen):
        """
        Render the lava
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        if self.sprite:
            # Use sprite if available
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            # Fallback to a rectangle with animated bubbles
            pygame.draw.rect(screen, self.getColor(), self.rect)
            
            # Draw lava bubbles
            for bubble in self.bubbles:
                x, y, size, _ = bubble
                pygame.draw.circle(screen, (255, 200, 100), (int(x), int(y)), size)
            
            # Draw heat haze effect (wavy line at top of lava)
            from math import sin
            import pygame.gfxdraw
            
            for x in range(0, self.width, 4):
                offset = sin(x / 20 + self.bubbleTimer / 10) * 3
                pygame.gfxdraw.pixel(screen, x, int(self.y + offset), (255, 255, 200, 100))
