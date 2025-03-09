"""
Menu - Game menu system
"""
import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, YELLOW, RED, GREEN, BLUE

class MenuItem:
    """Menu item class for menu options"""
    
    def __init__(self, text, action, x=0, y=0, width=200, height=50):
        """
        Initialize a menu item
        
        Args:
            text (str): Text to display
            action (function): Function to call when selected
            x (int): X position
            y (int): Y position
            width (int): Item width
            height (int): Item height
        """
        self.text = text
        self.action = action
        self.rect = pygame.Rect(x, y, width, height)
        self.selected = False
    
    def render(self, screen, font):
        """
        Render the menu item
        
        Args:
            screen (pygame.Surface): Surface to render on
            font (pygame.font.Font): Font to use for text
        """
        # Draw background
        color = YELLOW if self.selected else WHITE
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        
        # Draw text
        text_surf = font.render(self.text, True, color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def isMouseOver(self, mousePos):
        """
        Check if mouse is over this item
        
        Args:
            mousePos (tuple): Mouse position (x, y)
            
        Returns:
            bool: True if mouse is over this item, False otherwise
        """
        return self.rect.collidepoint(mousePos)


class Menu:
    """Base menu class"""
    
    def __init__(self, game):
        """
        Initialize a menu
        
        Args:
            game (Game): Reference to the main game object
        """
        self.game = game
        self.items = []
        self.selectedIndex = 0
        self.font = pygame.font.Font(None, 36)
        self.titleFont = pygame.font.Font(None, 72)
        self.title = "Menu"
        self.backgroundColor = (0, 0, 40)
    
    def addItem(self, text, action):
        """
        Add an item to the menu
        
        Args:
            text (str): Item text
            action (function): Function to call when selected
        """
        # Calculate position based on number of items
        x = SCREEN_WIDTH // 2 - 100
        y = SCREEN_HEIGHT // 2 - len(self.items) * 30 + len(self.items) * 60
        
        # Create and add the item
        item = MenuItem(text, action, x, y)
        self.items.append(item)
        
        # Update selected state
        self._updateSelectedStates()
    
    def _updateSelectedStates(self):
        """Update the selected state of all items"""
        for i, item in enumerate(self.items):
            item.selected = (i == self.selectedIndex)
    
    def selectNext(self):
        """Select the next menu item"""
        self.selectedIndex = (self.selectedIndex + 1) % len(self.items)
        self._updateSelectedStates()
    
    def selectPrevious(self):
        """Select the previous menu item"""
        self.selectedIndex = (self.selectedIndex - 1) % len(self.items)
        self._updateSelectedStates()
    
    def activateSelected(self):
        """Activate the currently selected item"""
        if 0 <= self.selectedIndex < len(self.items):
            self.items[self.selectedIndex].action()
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selectPrevious()
            elif event.key == pygame.K_DOWN:
                self.selectNext()
            elif event.key == pygame.K_RETURN:
                self.activateSelected()
        
        elif event.type == pygame.MOUSEMOTION:
            # Check if mouse is over any item
            for i, item in enumerate(self.items):
                if item.isMouseOver(event.pos):
                    self.selectedIndex = i
                    self._updateSelectedStates()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if clicked on any item
                for item in self.items:
                    if item.isMouseOver(event.pos):
                        item.action()
    
    def render(self, screen):
        """
        Render the menu
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        # Draw background
        screen.fill(self.backgroundColor)
        
        # Draw title
        title_surf = self.titleFont.render(self.title, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)
        
        # Draw items
        for item in self.items:
            item.render(screen, self.font)


class MainMenu(Menu):
    """Main menu for the game"""
    
    def __init__(self, game):
        """
        Initialize the main menu
        
        Args:
            game (Game): Reference to the main game object
        """
        super().__init__(game)
        
        # Set title
        self.title = "JOUST"
        
        # Add menu items
        self.addItem("Single Player", self._startSinglePlayer)
        self.addItem("Two Players (Co-op)", self._startCoopMultiplayer)
        self.addItem("Two Players (Versus)", self._startVersusMultiplayer)
        self.addItem("Options", self._showOptions)
        self.addItem("High Scores", self._showHighScores)
        self.addItem("Exit", self._exitGame)
    
    def _startSinglePlayer(self):
        """Start a single player game"""
        self.game.start_game(1)
    
    def _startCoopMultiplayer(self):
        """Start a cooperative multiplayer game"""
        self.game.start_game(2, "co-op")
    
    def _startVersusMultiplayer(self):
        """Start a versus multiplayer game"""
        self.game.start_game(2, "versus")
    
    def _showOptions(self):
        """Show options menu"""
        # Not implemented yet
        pass
    
    def _showHighScores(self):
        """Show high scores"""
        # Not implemented yet
        pass
    
    def _exitGame(self):
        """Exit the game"""
        self.game.quit_game()
    
    def render(self, screen):
        """
        Render the main menu
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        super().render(screen)
        
        # Draw additional decorations
        # Draw joust knights on either side of the title
        pygame.draw.polygon(screen, RED, [(100, 150), (150, 100), (200, 150), (150, 200)])
        pygame.draw.polygon(screen, BLUE, [(SCREEN_WIDTH - 100, 150), 
                                          (SCREEN_WIDTH - 150, 100), 
                                          (SCREEN_WIDTH - 200, 150), 
                                          (SCREEN_WIDTH - 150, 200)])
        
        # Draw version and copyright
        version_text = self.font.render("Version 1.0", True, WHITE)
        screen.blit(version_text, (20, SCREEN_HEIGHT - 40))
        
        copyright_text = self.font.render("© 2025", True, WHITE)
        screen.blit(copyright_text, (SCREEN_WIDTH - copyright_text.get_width() - 20, 
                                    SCREEN_HEIGHT - 40))


class PauseMenu(Menu):
    """Pause menu for the game"""
    
    def __init__(self, game):
        """
        Initialize the pause menu
        
        Args:
            game (Game): Reference to the main game object
        """
        super().__init__(game)
        
        # Set title
        self.title = "PAUSED"
        
        # Add menu items
        self.addItem("Resume", self._resumeGame)
        self.addItem("Options", self._showOptions)
        self.addItem("Main Menu", self._returnToMainMenu)
        self.addItem("Exit", self._exitGame)
    
    def _resumeGame(self):
        """Resume the game"""
        self.game.resume_game()
    
    def _showOptions(self):
        """Show options menu"""
        # Not implemented yet
        pass
    
    def _returnToMainMenu(self):
        """Return to the main menu"""
        from game import GameState
        self.game.state = GameState.MAIN_MENU
    
    def _exitGame(self):
        """Exit the game"""
        self.game.quit_game()
    
    def render(self, screen):
        """
        Render the pause menu
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Draw menu
        super().render(screen)


class GameOverMenu(Menu):
    """Game over menu for the game"""
    
    def __init__(self, game):
        """
        Initialize the game over menu
        
        Args:
            game (Game): Reference to the main game object
        """
        super().__init__(game)
        
        # Set title
        self.title = "GAME OVER"
        
        # Add menu items
        self.addItem("Play Again", self._playAgain)
        self.addItem("High Scores", self._showHighScores)
        self.addItem("Main Menu", self._returnToMainMenu)
        self.addItem("Exit", self._exitGame)
        
        # High score entry
        self.enteringHighScore = False
        self.playerName = ""
        self.nameFont = pygame.font.Font(None, 48)
    
    def _playAgain(self):
        """Start a new game"""
        self.game.start_game(self.game.num_players)
    
    def _showHighScores(self):
        """Show high scores"""
        # Not implemented yet
        pass
    
    def _returnToMainMenu(self):
        """Return to the main menu"""
        from game import GameState
        self.game.state = GameState.MAIN_MENU
    
    def _exitGame(self):
        """Exit the game"""
        self.game.quit_game()
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        if self.enteringHighScore:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Submit high score
                    if self.playerName:
                        self.game.score_manager.add_high_score(self.playerName)
                        self.enteringHighScore = False
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character
                    self.playerName = self.playerName[:-1]
                elif event.unicode.isalnum() and len(self.playerName) < 3:
                    # Add character (limit to 3 characters)
                    self.playerName += event.unicode.upper()
        else:
            super().handle_event(event)
    
    def render(self, screen):
        """
        Render the game over menu
        
        Args:
            screen (pygame.Surface): Surface to render on
        """
        # Draw background
        screen.fill(self.backgroundColor)
        
        # Draw title
        title_surf = self.titleFont.render(self.title, True, RED)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)
        
        # Draw final score
        if len(self.game.entity_manager.players) > 0:
            player1 = self.game.entity_manager.players[0]
            score_text = self.font.render(f"Final Score: {player1.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
            screen.blit(score_text, score_rect)
        
        # Draw high score entry if applicable
        if self.enteringHighScore:
            prompt_text = self.font.render("New High Score! Enter your initials:", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
            screen.blit(prompt_text, prompt_rect)
            
            name_text = self.nameFont.render(self.playerName + "_", True, WHITE)
            name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
            screen.blit(name_text, name_rect)
        else:
            # Draw menu items
            for item in self.items:
                item.render(screen, self.font)
