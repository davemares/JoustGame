"""
Sound Manager - Manages game sounds and music
"""
import os
import pygame

class SoundManager:
    """Manages game sounds and music"""
    
    def __init__(self):
        """Initialize the sound manager"""
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Sound dictionaries
        self.sounds = {}
        self.music = {}
        
        # Volume settings
        self.soundVolume = 0.7
        self.musicVolume = 0.5
        
        # Music state
        self.currentMusic = None
    
    def load_sounds(self, assetLoader):
        """
        Load sound effects from asset loader
        
        Args:
            assetLoader (AssetLoader): Asset loader containing sounds
        """
        # Get sounds from asset loader if available
        for name, sound in assetLoader.sounds.items():
            if sound is not None:
                self.sounds[name] = sound
                self.sounds[name].set_volume(self.soundVolume)
        
        # Create placeholder sounds for any missing sounds
        self._createPlaceholderSounds()
    
    def _createPlaceholderSounds(self):
        """Create placeholder sounds for development"""
        # Create simple sounds using pygame.mixer.Sound
        self._createBeepSound("player_death", 200, 300)
        self._createBeepSound("enemy_defeat", 500, 150)
        self._createBeepSound("egg_collect", 800, 100)
        self._createBeepSound("bounce", 300, 50)
        self._createBeepSound("pterodactyl", 100, 500)
        self._createBeepSound("pterodactyl_defeat", 600, 300)
        self._createBeepSound("wave_start", 400, 200)
        self._createBeepSound("bonus", 700, 250)
        self._createBeepSound("game_over", 150, 400)
        
        # Create placeholder music
        self._createPlaceholderMusic("main_theme")
        self._createPlaceholderMusic("game_over")
    
    def _createBeepSound(self, name, frequency, duration):
        """
        Create a simple beep sound
        
        Args:
            name (str): Sound name
            frequency (int): Beep frequency
            duration (int): Beep duration in milliseconds
        """
        # Create a Sound object from an in-memory WAV file
        sampleRate = 44100
        bits = 16
        
        # Create a short array representing a sine wave
        import numpy as np
        import io
        import wave
        
        duration = duration / 1000.0  # Convert to seconds
        samples = int(sampleRate * duration)
        bufferSize = samples * 2  # 16-bit samples
        
        # Generate sine wave
        t = np.linspace(0, duration, samples, False)
        tone = np.sin(2 * np.pi * frequency * t) * 32767 * 0.5
        
        # Convert to 16-bit signed integers
        tone = tone.astype(np.int16)
        
        # Create WAV file in memory
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(bits // 8)
            wav.setframerate(sampleRate)
            wav.writeframes(tone.tobytes())
        
        # Create Sound object from buffer
        buffer.seek(0)
        self.sounds[name] = pygame.mixer.Sound(buffer)
        self.sounds[name].set_volume(self.soundVolume)
    
    def _createPlaceholderMusic(self, name):
        """
        Create placeholder music
        
        Args:
            name (str): Music name
        """
        # For now, just store the name
        self.music[name] = name
    
    def play_sound(self, name):
        """
        Play a sound effect
        
        Args:
            name (str): Sound name
        """
        if name in self.sounds:
            self.sounds[name].play()
    
    def play_music(self, name):
        """
        Play background music
        
        Args:
            name (str): Music name
        """
        # In a real implementation, this would play an actual music file
        # For now, just store the current music name
        self.currentMusic = name
    
    def stop_music(self):
        """Stop the currently playing music"""
        pygame.mixer.music.stop()
        self.currentMusic = None
    
    def pause_music(self):
        """Pause the currently playing music"""
        pygame.mixer.music.pause()
    
    def resume_music(self):
        """Resume the paused music"""
        pygame.mixer.music.unpause()
    
    def set_sound_volume(self, volume):
        """
        Set the sound effect volume
        
        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        self.soundVolume = max(0.0, min(1.0, volume))
        
        # Update volume for all sounds
        for sound in self.sounds.values():
            sound.set_volume(self.soundVolume)
    
    def set_music_volume(self, volume):
        """
        Set the music volume
        
        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        self.musicVolume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.musicVolume)
