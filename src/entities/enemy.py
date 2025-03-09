"""
Enemy - Enemy entity classes
"""
import random
import pygame
import math
from entities.entity import Entity
from utils.constants import (
    GRAVITY, FLAP_POWER, MAX_VERTICAL_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT,
    ENEMY_TYPES, LAVA_Y_POSITION, FLAP_MOMENTUM_GAIN, MAX_FLAP_MOMENTUM,
    FLAP_MOMENTUM_DECAY, HORIZONTAL_AIR_CONTROL
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
        
        # Momentum physics variables
        self.flapMomentum = random.uniform(1.0, 1.5)  # Start with some momentum
        self.isGrounded = False  # Whether enemy is on a platform
        self.isFlapping = False
    
    def update(self, players=None, platforms=None):
        """
        Update enemy state
        
        Args:
            players (list): List of player entities
            platforms (list): List of platform entities
        """
        # Apply gravity - enemies are moderately affected by gravity
        self.velocityY += GRAVITY * 0.7  # Balanced gravity for enemies
        
        # Cap vertical speed
        if self.velocityY > MAX_VERTICAL_SPEED:
            self.velocityY = MAX_VERTICAL_SPEED
        
        # Decay flap momentum when not flapping
        if not self.isFlapping and self.flapMomentum > 1.0:
            self.flapMomentum -= FLAP_MOMENTUM_DECAY * 0.3  # Much slower decay for enemies
            if self.flapMomentum < 1.0:
                self.flapMomentum = 1.0
        
        # Reset flapping state each frame
        self.isFlapping = False
        
        # AI behavior
        self._updateAI(players)
        
        # Update position
        super().update()
        
        # Check for lava collision
        if self.y + self.height > LAVA_Y_POSITION:
            # Enemies try to avoid lava
            self._flap()
            self._flap()  # Double flap to escape lava
            
        # Add vertical screen constraints to keep enemies on screen
        if self.y < 0:
            # If enemy is trying to fly off the top of the screen, push them back down
            self.y = 0
            self.velocityY = abs(self.velocityY) * 0.5  # Bounce down at half speed
        elif self.y > SCREEN_HEIGHT - 100 and self.velocityY > 0:
            # If enemy is near the bottom of the screen and still falling, make them flap
            if random.random() < 0.3:  # 30% chance to flap when near bottom
                self._flap()
    
    def _updateAI(self, players):
        """
        Update enemy AI behavior
        
        Args:
            players (list): List of player entities
        """
        # Decrease timers
        self.flapTimer -= 1
        self.changeDirectionTimer -= 1
        
        # Moderate flapping when grounded
        if self.isGrounded:
            # Reasonable chance to flap when on a platform
            if random.random() < 0.15:  # 15% chance each frame to take off
                self._flap()
                if random.random() < 0.6:  # 60% chance for double flap
                    self._flap()
                self.flapTimer = random.randint(10, 25)  # Reasonable interval after takeoff
        
        # Random flapping (in air or on ground)
        if self.flapTimer <= 0:
            self._flap()
            # Vary flap interval based on enemy type and position
            if self.isGrounded:
                self.flapTimer = random.randint(15, 30)  # Moderate flapping when grounded
            else:
                # Balanced flapping in air
                self.flapTimer = random.randint(20, 40)  # Normal flapping in air
                
        # Occasional random flapping when in air to maintain altitude
        elif not self.isGrounded and random.random() < 0.05:  # 5% chance each frame
            self._flap()  # Extra flaps while airborne
        
        # Random direction changes
        if self.changeDirectionTimer <= 0:
            self._changeDirection()
            self.changeDirectionTimer = random.randint(60, 180)
    
    def _flap(self):
        """Make the enemy flap to gain altitude"""
        self.isFlapping = True
        
        # Build up flap momentum with each flap - moderate gain
        self.flapMomentum += FLAP_MOMENTUM_GAIN * 0.9  # Slightly faster momentum gain than players
        if self.flapMomentum > MAX_FLAP_MOMENTUM * 0.8:  # Lower max momentum than players
            self.flapMomentum = MAX_FLAP_MOMENTUM * 0.8
        
        # Apply flap force with momentum multiplier - balanced flapping
        self.velocityY -= FLAP_POWER * self.flapMomentum * 1.1  # Enemies flap with slightly more power
        
        # Give a small boost when taking off from ground
        if self.isGrounded:
            self.velocityY -= FLAP_POWER * 0.5  # Small boost when taking off
        
        # Reset grounded state when flapping
        self.isGrounded = False
        
        # Cap upward velocity at higher value
        if self.velocityY < -MAX_VERTICAL_SPEED * 0.95:
            self.velocityY = -MAX_VERTICAL_SPEED * 0.95
    
    def _changeDirection(self):
        """Change the enemy's horizontal direction"""
        # Calculate air control factor - reduced control in air
        airControlFactor = 1.0 if self.isGrounded else HORIZONTAL_AIR_CONTROL * 1.2  # Slightly better air control than players
        
        # Apply direction change with air control factor
        self.velocityX = random.choice([-1, 1]) * self.speed * random.uniform(0.5, 1.0) * airControlFactor
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
        # Bounders have a higher chance to flap when grounded
        if self.isGrounded and random.random() < 0.2:  # 20% chance each frame
            self._flap()
            
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
        self.flapTimer = random.randint(10, 30)  # Hunters flap more frequently
    
    def _updateAI(self, players):
        """
        Update Hunter AI behavior - chase closest player
        
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
        
        # Hunters always try to take off when grounded
        if self.isGrounded:
            if random.random() < 0.25:  # 25% chance each frame to take off when grounded
                self._flap()
                self._flap()  # Double flap to ensure takeoff
        
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
            
            # Flap to match player's height - more aggressive flapping
            if self.targetPlayer.y < self.y - 30:  # Reduced height threshold
                if random.random() < 0.4:  # Increased flap chance
                    self._flap()
                    if random.random() < 0.3:  # 30% chance for double flap
                        self._flap()
        
        # Basic AI behavior from parent (after our custom logic)
        super()._updateAI(players)


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
        
        # Shadow Lords start with higher momentum
        self.flapMomentum = random.uniform(1.5, 2.0)  # Start with higher momentum
    
    def _updateAI(self, players):
        """
        Update Shadow Lord AI behavior - erratic and unpredictable
        
        Args:
            players (list): List of player entities
        """
        # Shadow Lords hate being on platforms and always try to take off
        if self.isGrounded:
            if random.random() < 0.35:  # 35% chance each frame to take off when grounded
                self._flap()
                self._flap()  # Double flap to ensure takeoff
                if random.random() < 0.3:  # Sometimes triple flap for extra height
                    self._flap()
        
        # Decrease dash timer
        self.dashTimer -= 1
        
        # Perform dash when timer expires
        if self.dashTimer <= 0:
            # Start a dash in a random direction
            self.dashDirection = random.choice([-1, 1])
            self.velocityX = self.dashDirection * self.speed * 2.0  # Faster dash
            self.facingRight = self.dashDirection > 0
            
            # Always flap during dash for vertical movement
            self._flap()
            if random.random() < 0.6:  # 60% chance for double flap
                self._flap()
            
            # Reset dash timer with shorter interval
            self.dashTimer = random.randint(60, 180)  # More frequent dashes
        
        # Random vertical movement - much more aggressive
        if random.random() < 0.1 * self.erraticFactor:  # Doubled chance
            if random.random() < 0.7:  # Increased flap probability
                self._flap()
                if random.random() < 0.4:  # 40% chance for double flap
                    self._flap()
            else:
                # Occasional dive
                self.velocityY += GRAVITY * 2
        
        # Basic AI behavior from parent (after our custom logic)
        super()._updateAI(players)


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
        # Pterodactyls prefer not to stay on the ground
        if self.isGrounded:
            # Take off with double flap
            self._flap()
            self._flap()  # Double flap to ensure takeoff
        
        # Occasional random flapping to stay airborne
        if random.random() < 0.08:  # 8% chance each frame
            self._flap()
        
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
            
            # Move horizontally toward player with moderate speed
            if self.targetPlayer.x < self.x:
                self.velocityX = -self.speed * 1.2  # Slightly faster horizontal movement
                self.facingRight = False
            else:
                self.velocityX = self.speed * 1.2  # Slightly faster horizontal movement
                self.facingRight = True
            
            # Balanced vertical movement toward player
            if self.targetPlayer.y < self.y - 20:  # Normal threshold
                self._flap()
                if random.random() < 0.3:  # 30% chance for double flap
                    self._flap()
            elif self.targetPlayer.y > self.y + 50:
                # Occasional dive to catch up to player below
                if random.random() < 0.2:
                    self.velocityY += GRAVITY * 0.8
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
