"""
Enemy - Enemy entity classes
"""
import random
import pygame
import math
from entities.entity import Entity
from utils.constants import (
    GRAVITY, FLAP_POWER, MAX_VERTICAL_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT,
    ENEMY_TYPES, LAVA_Y_POSITION
)

class Enemy(Entity):
    """Base class for all enemy entities"""
    
    def __init__(self, x, y, enemyType):
        """
        Initialize an enemy
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            enemyType (str): Type of enemy (BOUNDER, HUNTER, SHADOW_LORD, PTERODACTYL)
        """
        # Enemy dimensions
        width = 64
        height = 64
        
        super().__init__(x, y, width, height)
        
        self.enemyType = enemyType
        self.settings = ENEMY_TYPES[enemyType]
        self.speed = self.settings["speed"]
        self.points = self.settings["points"]
        self.color = self.settings["color"]
        
        # For rendering
        self.spriteName = enemyType.lower()
        
        # AI behavior
        self.flapTimer = 0
        self.flapInterval = random.randint(30, 60)  # Frames between flaps
        self.changeDirectionTimer = 0
        self.changeDirectionInterval = random.randint(60, 180)  # Frames between direction changes
        
        # Initial direction
        self.velocityX = random.choice([-1, 1]) * self.speed * 0.5
        self.facingRight = self.velocityX > 0
    
    def update(self, players=None, platforms=None):
        """
        Update enemy state
        
        Args:
            players (list): List of player entities
            platforms (list): List of platform entities
        """
        # Apply gravity
        self.velocityY += GRAVITY * 0.8  # Enemies are slightly less affected by gravity
        
        # Cap vertical speed
        if self.velocityY > MAX_VERTICAL_SPEED:
            self.velocityY = MAX_VERTICAL_SPEED
        
        # AI behavior
        self._updateAI(players)
        
        # Update position
        super().update()
        
        # Check for lava collision
        if self.y + self.height > LAVA_Y_POSITION:
            # Enemies try to avoid lava
            self.velocityY = -FLAP_POWER
    
    def _updateAI(self, players):
        """
        Update enemy AI behavior
        
        Args:
            players (list): List of player entities
        """
        # Decrease timers
        self.flapTimer -= 1
        self.changeDirectionTimer -= 1
        
        # Random flapping
        if self.flapTimer <= 0:
            self._flap()
            self.flapTimer = random.randint(30, 60)
        
        # Random direction changes
        if self.changeDirectionTimer <= 0:
            self._changeDirection()
            self.changeDirectionTimer = random.randint(60, 180)
    
    def _flap(self):
        """Make the enemy flap to gain altitude"""
        self.velocityY -= FLAP_POWER * 0.7  # Enemies flap with less power than players
        
        # Cap upward velocity
        if self.velocityY < -MAX_VERTICAL_SPEED * 0.8:
            self.velocityY = -MAX_VERTICAL_SPEED * 0.8
    
    def _changeDirection(self):
        """Change the enemy's horizontal direction"""
        self.velocityX = random.choice([-1, 1]) * self.speed * random.uniform(0.5, 1.0)
        self.facingRight = self.velocityX > 0
    
    def getColor(self):
        """
        Get the enemy's color for rendering when no sprite is available
        
        Returns:
            tuple: RGB color tuple
        """
        # Use the color from settings
        if self.color == "red":
            return (255, 0, 0)
        elif self.color == "gray":
            return (128, 128, 128)
        elif self.color == "blue":
            return (0, 0, 255)
        elif self.color == "purple":
            return (128, 0, 128)
        else:
            return (255, 255, 255)  # Default to white
    
    def turnToEgg(self, x=None, y=None):
        """
        Turn this enemy into an egg
        
        Args:
            x (float, optional): X position for the egg
            y (float, optional): Y position for the egg
            
        Returns:
            Egg: The created egg entity
        """
        from entities.egg import Egg
        
        # Use current position if not specified
        if x is None:
            x = self.x
        if y is None:
            y = self.y
            
        # Create an egg at the enemy's position
        egg = Egg(x, y, self.enemyType)
        
        # Deactivate the enemy
        self.deactivate()
        
        return egg


class Bounder(Enemy):
    """Bounder enemy - Basic enemy with predictable movement"""
    
    def __init__(self, x, y):
        """
        Initialize a Bounder enemy
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
        """
        super().__init__(x, y, "BOUNDER")
    
    def _updateAI(self, players):
        """
        Update Bounder AI behavior - simple and predictable
        
        Args:
            players (list): List of player entities
        """
        super()._updateAI(players)
        
        # Bounders just move randomly, so no additional AI logic needed


class Hunter(Enemy):
    """Hunter enemy - More aggressive, chases the player"""
    
    def __init__(self, x, y):
        """
        Initialize a Hunter enemy
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
        """
        super().__init__(x, y, "HUNTER")
        
        # Hunter-specific properties
        self.targetPlayer = None
        self.aggressionFactor = random.uniform(0.6, 0.9)  # How aggressively to chase
    
    def _updateAI(self, players):
        """
        Update Hunter AI behavior - chase closest player
        
        Args:
            players (list): List of player entities
        """
        # Basic AI behavior from parent
        super()._updateAI(players)
        
        # Find closest active player
        closestPlayer = None
        closestDistance = float('inf')
        
        for player in players:
            if player.active and player.isAlive:
                distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
                if distance < closestDistance:
                    closestDistance = distance
                    closestPlayer = player
        
        # Chase the closest player
        if closestPlayer and random.random() < self.aggressionFactor:
            self.targetPlayer = closestPlayer
            
            # Move horizontally toward player
            if self.targetPlayer.x < self.x:
                self.velocityX = -self.speed
                self.facingRight = False
            else:
                self.velocityX = self.speed
                self.facingRight = True
            
            # Flap to match player's height
            if self.targetPlayer.y < self.y - 50 and random.random() < 0.3:
                self._flap()


class ShadowLord(Enemy):
    """Shadow Lord enemy - Fast with erratic movement patterns"""
    
    def __init__(self, x, y):
        """
        Initialize a Shadow Lord enemy
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
        """
        super().__init__(x, y, "SHADOW_LORD")
        
        # Shadow Lord-specific properties
        self.erraticFactor = random.uniform(0.7, 1.0)  # How erratic the movement is
        self.dashTimer = 0
        self.dashInterval = random.randint(120, 240)  # Frames between dashes
        self.dashDirection = random.choice([-1, 1])
    
    def _updateAI(self, players):
        """
        Update Shadow Lord AI behavior - erratic and unpredictable
        
        Args:
            players (list): List of player entities
        """
        # Basic AI behavior from parent
        super()._updateAI(players)
        
        # Decrease dash timer
        self.dashTimer -= 1
        
        # Perform dash when timer expires
        if self.dashTimer <= 0:
            # Start a dash in a random direction
            self.dashDirection = random.choice([-1, 1])
            self.velocityX = self.dashDirection * self.speed * 1.5
            self.facingRight = self.dashDirection > 0
            
            # Reset dash timer
            self.dashTimer = random.randint(120, 240)
        
        # Random vertical movement
        if random.random() < 0.05 * self.erraticFactor:
            if random.random() < 0.5:
                self._flap()
            else:
                # Occasional dive
                self.velocityY += GRAVITY * 2


class Pterodactyl(Enemy):
    """Pterodactyl enemy - Fast, invincible except for precise strikes"""
    
    def __init__(self, x, y):
        """
        Initialize a Pterodactyl enemy
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
        """
        super().__init__(x, y, "PTERODACTYL")
        
        # Pterodactyl-specific properties
        self.targetPlayer = None
        self.invincible = True  # Invincible except for mouth strikes
        self.mouthRect = pygame.Rect(0, 0, 20, 20)  # Will be positioned relative to main rect
        self.updateMouthPosition()
    
    def updateMouthPosition(self):
        """Update the position of the pterodactyl's mouth hitbox"""
        # Position depends on facing direction
        if self.facingRight:
            self.mouthRect.x = self.rect.right - 20
        else:
            self.mouthRect.x = self.rect.left
        
        # Vertical position
        self.mouthRect.y = self.rect.centery - 10
    
    def update(self, players=None, platforms=None):
        """
        Update pterodactyl state
        
        Args:
            players (list): List of player entities
            platforms (list): List of platform entities
        """
        super().update(players, platforms)
        
        # Update mouth position
        self.updateMouthPosition()
    
    def _updateAI(self, players):
        """
        Update Pterodactyl AI behavior - aggressively chase player
        
        Args:
            players (list): List of player entities
        """
        # Find closest active player
        closestPlayer = None
        closestDistance = float('inf')
        
        for player in players:
            if player.active and player.isAlive:
                distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
                if distance < closestDistance:
                    closestDistance = distance
                    closestPlayer = player
        
        # Always chase the closest player
        if closestPlayer:
            self.targetPlayer = closestPlayer
            
            # Move horizontally toward player
            if self.targetPlayer.x < self.x:
                self.velocityX = -self.speed
                self.facingRight = False
            else:
                self.velocityX = self.speed
                self.facingRight = True
            
            # Move vertically toward player
            if self.targetPlayer.y < self.y - 20:
                self._flap()
            elif self.targetPlayer.y > self.y + 20:
                # Let gravity do its work
                pass
            else:
                # Maintain altitude with occasional flaps
                if random.random() < 0.2:
                    self._flap()
    
    def isVulnerable(self, lance):
        """
        Check if the pterodactyl is vulnerable to a lance strike
        
        Args:
            lance (pygame.Rect): The lance hitbox
            
        Returns:
            bool: True if vulnerable, False otherwise
        """
        # Only vulnerable if struck in the mouth
        return lance.colliderect(self.mouthRect)
