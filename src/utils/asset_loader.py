"""
Asset Loader - Utility for loading and managing game assets
"""
import os
import pygame
import numpy

class AssetLoader:
    """Utility class for loading and managing game assets"""
    
    def __init__(self, base_dir=None):
        """
        Initialize the asset loader
        
        Args:
            base_dir (str, optional): Base directory for assets
        """
        if base_dir is None:
            # Default to project root directory
            self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        else:
            self.base_dir = base_dir
        
        # Asset directories
        self.image_dir = os.path.join(self.base_dir, "assets", "images")
        self.sound_dir = os.path.join(self.base_dir, "assets", "sounds")
        self.font_dir = os.path.join(self.base_dir, "assets", "fonts")
        
        # Asset dictionaries
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        
        # Create placeholder assets for development
        self._createPlaceholderAssets()
    
    def _createPlaceholderAssets(self):
        """Create placeholder assets for development"""
        # Create placeholder sprites
        self._createPlaceholderSprites()
    
    def _createPlaceholderSprites(self):
        """Create placeholder sprites for development"""
        # Player sprites (ostrich and stork)
        self._createColoredSprite("player1", (255, 200, 0), 64, 64)  # Yellow ostrich
        self._createColoredSprite("player2", (0, 200, 255), 64, 64)  # Blue stork
        
        # Enemy sprites
        self._createColoredSprite("bounder", (255, 0, 0), 64, 64)  # Red bounder
        self._createColoredSprite("hunter", (128, 128, 128), 64, 64)  # Gray hunter
        self._createColoredSprite("shadow_lord", (0, 0, 255), 64, 64)  # Blue shadow lord
        self._createColoredSprite("pterodactyl", (128, 0, 128), 80, 64)  # Purple pterodactyl
        
        # Egg sprite
        self._createColoredSprite("egg", (255, 255, 255), 32, 32)  # White egg
        
        # Platform sprite
        self._createColoredSprite("platform", (200, 200, 200), 100, 20)  # Gray platform
    
    def _createColoredSprite(self, name, color, width, height):
        """
        Create a simple colored sprite
        
        Args:
            name (str): Sprite name
            color (tuple): RGB color
            width (int): Sprite width
            height (int): Sprite height
        """
        # Create a surface
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw a shape based on the entity type
        if name == "player1" or name == "player2":
            # Draw a bird-like shape
            pygame.draw.ellipse(surface, color, (0, 0, width, height))
            pygame.draw.polygon(surface, color, [(width//2, 0), (width, height//3), (width//2, height//2)])
            # Draw a knight rider on top
            pygame.draw.rect(surface, (50, 50, 50), (width//4, 0, width//2, height//3))
            # Draw a lance
            pygame.draw.line(surface, (200, 200, 200), (width//2, height//4), (width, height//4), 3)
        
        elif name == "bounder" or name == "hunter" or name == "shadow_lord":
            # Draw a buzzard-like shape
            pygame.draw.ellipse(surface, color, (0, 0, width, height))
            pygame.draw.polygon(surface, color, [(width//2, 0), (0, height//3), (width//2, height//2)])
            # Draw a knight rider on top
            pygame.draw.rect(surface, (50, 50, 50), (width//4, 0, width//2, height//3))
            # Draw a lance
            pygame.draw.line(surface, (200, 200, 200), (width//2, height//4), (0, height//4), 3)
        
        elif name == "pterodactyl":
            # Draw a pterodactyl shape
            pygame.draw.ellipse(surface, color, (width//4, 0, width//2, height//2))
            pygame.draw.polygon(surface, color, [
                (width//4, height//4), 
                (0, height//2), 
                (width//4, height//2)
            ])
            pygame.draw.polygon(surface, color, [
                (3*width//4, height//4), 
                (width, height//2), 
                (3*width//4, height//2)
            ])
            # Draw wings
            pygame.draw.ellipse(surface, color, (width//4, height//2, width//2, height//2))
            
            # Draw mouth (vulnerable spot)
            mouth_rect = pygame.Rect(width - 20, height//2 - 10, 20, 20)
            pygame.draw.rect(surface, (255, 0, 0), mouth_rect)
        
        elif name == "egg":
            # Draw an egg shape
            pygame.draw.ellipse(surface, color, (0, 0, width, height))
            # Add some detail
            pygame.draw.ellipse(surface, (200, 200, 200), (width//4, height//4, width//2, height//2))
        
        elif name == "platform":
            # Draw a platform
            pygame.draw.rect(surface, color, (0, 0, width, height))
            # Add some detail
            pygame.draw.line(surface, (255, 255, 255), (0, 0), (width, 0), 2)
        
        # Store the sprite
        self.images[name] = surface
    
    def loadImages(self):
        """Load image assets"""
        # Check if image directory exists
        if not os.path.exists(self.image_dir):
            print(f"Warning: Image directory not found: {self.image_dir}")
            return
        
        # Load images from directory
        for filename in os.listdir(self.image_dir):
            if filename.endswith(('.png', '.jpg', '.bmp')):
                name = os.path.splitext(filename)[0]
                path = os.path.join(self.image_dir, filename)
                try:
                    self.images[name] = pygame.image.load(path).convert_alpha()
                except pygame.error as e:
                    print(f"Error loading image {filename}: {e}")
    
    def loadSounds(self):
        """Load sound assets"""
        # Check if sound directory exists
        if not os.path.exists(self.sound_dir):
            print(f"Warning: Sound directory not found: {self.sound_dir}")
            return
        
        # Load sounds from directory
        for filename in os.listdir(self.sound_dir):
            if filename.endswith(('.wav', '.ogg', '.mp3')):
                name = os.path.splitext(filename)[0]
                path = os.path.join(self.sound_dir, filename)
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                except pygame.error as e:
                    print(f"Error loading sound {filename}: {e}")
    
    def loadFonts(self):
        """Load font assets"""
        # Check if font directory exists
        if not os.path.exists(self.font_dir):
            print(f"Warning: Font directory not found: {self.font_dir}")
            return
        
        # Load fonts from directory
        for filename in os.listdir(self.font_dir):
            if filename.endswith(('.ttf')):
                name = os.path.splitext(filename)[0]
                path = os.path.join(self.font_dir, filename)
                try:
                    # Store fonts with different sizes
                    self.fonts[name] = {
                        'small': pygame.font.Font(path, 16),
                        'medium': pygame.font.Font(path, 24),
                        'large': pygame.font.Font(path, 36),
                        'title': pygame.font.Font(path, 72)
                    }
                except pygame.error as e:
                    print(f"Error loading font {filename}: {e}")
    
    def getImage(self, name):
        """
        Get an image by name
        
        Args:
            name (str): Image name
            
        Returns:
            pygame.Surface: The image surface
        """
        if name in self.images:
            return self.images[name]
        else:
            print(f"Warning: Image not found: {name}")
            # Return a placeholder
            return self._createMissingTexture(64, 64)
    
    def getSound(self, name):
        """
        Get a sound by name
        
        Args:
            name (str): Sound name
            
        Returns:
            pygame.mixer.Sound: The sound object
        """
        if name in self.sounds:
            return self.sounds[name]
        else:
            print(f"Warning: Sound not found: {name}")
            return None
    
    def getFont(self, name, size='medium'):
        """
        Get a font by name and size
        
        Args:
            name (str): Font name
            size (str): Font size ('small', 'medium', 'large', 'title')
            
        Returns:
            pygame.font.Font: The font object
        """
        if name in self.fonts and size in self.fonts[name]:
            return self.fonts[name][size]
        else:
            print(f"Warning: Font not found: {name} ({size})")
            # Return default font
            return pygame.font.Font(None, {'small': 16, 'medium': 24, 'large': 36, 'title': 72}[size])
    
    def _createMissingTexture(self, width, height):
        """
        Create a missing texture placeholder
        
        Args:
            width (int): Texture width
            height (int): Texture height
            
        Returns:
            pygame.Surface: The missing texture surface
        """
        # Create a checkered pattern for missing textures
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Fill with magenta and black checkers
        checker_size = 8
        for x in range(0, width, checker_size):
            for y in range(0, height, checker_size):
                color = (255, 0, 255) if (x // checker_size + y // checker_size) % 2 == 0 else (0, 0, 0)
                pygame.draw.rect(surface, color, (x, y, checker_size, checker_size))
        
        return surface
