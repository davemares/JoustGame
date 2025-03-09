"""
Score Manager - Manages game scores and high scores
"""
import os
import json
import pygame

class ScoreManager:
    """Manages game scores and high scores"""
    
    def __init__(self):
        """Initialize the score manager"""
        self.currentScore = 0
        self.highScores = []
        self.highScoreFile = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                         "data", "high_scores.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.highScoreFile), exist_ok=True)
        
        # Load high scores
        self.loadHighScores()
    
    def reset(self):
        """Reset the current score"""
        self.currentScore = 0
    
    def addScore(self, points):
        """
        Add points to the current score
        
        Args:
            points (int): Points to add
        """
        self.currentScore += points
    
    def getScore(self):
        """
        Get the current score
        
        Returns:
            int: Current score
        """
        return self.currentScore
    
    def loadHighScores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.highScoreFile):
                with open(self.highScoreFile, 'r') as f:
                    self.highScores = json.load(f)
            else:
                # Initialize with default high scores
                self.highScores = [
                    {"name": "AAA", "score": 10000},
                    {"name": "BBB", "score": 8000},
                    {"name": "CCC", "score": 6000},
                    {"name": "DDD", "score": 4000},
                    {"name": "EEE", "score": 2000}
                ]
                self.saveHighScores()
        except Exception as e:
            print(f"Error loading high scores: {e}")
            # Initialize with default high scores
            self.highScores = [
                {"name": "AAA", "score": 10000},
                {"name": "BBB", "score": 8000},
                {"name": "CCC", "score": 6000},
                {"name": "DDD", "score": 4000},
                {"name": "EEE", "score": 2000}
            ]
    
    def saveHighScores(self):
        """Save high scores to file"""
        try:
            with open(self.highScoreFile, 'w') as f:
                json.dump(self.highScores, f)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    def check_high_score(self):
        """
        Check if the current score is a high score
        
        Returns:
            bool: True if current score is a high score, False otherwise
        """
        # Sort high scores
        self.highScores.sort(key=lambda x: x["score"], reverse=True)
        
        # Check if current score is higher than the lowest high score
        if len(self.highScores) < 10 or self.currentScore > self.highScores[-1]["score"]:
            return True
        
        return False
    
    def add_high_score(self, name):
        """
        Add the current score to high scores
        
        Args:
            name (str): Player name (initials)
        """
        # Add new high score
        self.highScores.append({"name": name, "score": self.currentScore})
        
        # Sort high scores
        self.highScores.sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only top 10
        if len(self.highScores) > 10:
            self.highScores = self.highScores[:10]
        
        # Save high scores
        self.saveHighScores()
    
    def get_high_scores(self):
        """
        Get the list of high scores
        
        Returns:
            list: List of high score dictionaries
        """
        # Sort high scores
        self.highScores.sort(key=lambda x: x["score"], reverse=True)
        
        return self.highScores
