#!/usr/bin/env python3
"""
Voice Handler for G.E.N.G.A.R
Author: Gage Ayala
"""

import asyncio
import logging
from typing import Optional

class VoiceHandler:
    """Handles voice input and output for G.E.N.G.A.R"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("GENGAR.Voice")
        self.voice_enabled = config.get("voice_enabled", False)
        self.voice_engine = config.get("voice_engine", "pyttsx3")
        self.voice_rate = config.get("voice_rate", 150)
        self.voice_volume = config.get("voice_volume", 0.9)
        
        # Voice engine instances
        self.tts_engine = None
        self.stt_engine = None
    
    async def initialize(self):
        """Initialize voice capabilities"""
        if not self.voice_enabled:
            return
        
        try:
            if self.voice_engine == "pyttsx3":
                await self._init_pyttsx3()
            else:
                self.logger.warning(f"Voice engine {self.voice_engine} not supported")
                
        except Exception as e:
            self.logger.error(f"Error initializing voice: {e}")
            self.voice_enabled = False
    
    async def _init_pyttsx3(self):
        """Initialize pyttsx3 text-to-speech engine"""
        try:
            import pyttsx3
            
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', self.voice_rate)
            self.tts_engine.setProperty('volume', self.voice_volume)
            
            # Get available voices and set a good one
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer a male voice for G.E.N.G.A.R
                for voice in voices:
                    if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            self.logger.info("pyttsx3 voice engine initialized successfully")
            
        except ImportError:
            self.logger.error("pyttsx3 not installed. Install with: pip install pyttsx3")
            self.voice_enabled = False
            self.tts_engine = None
        except Exception as e:
            self.logger.error(f"Error initializing pyttsx3: {e}")
            self.voice_enabled = False
            self.tts_engine = None
    
    async def speak(self, text: str):
        """Convert text to speech"""
        if not self.voice_enabled or not self.tts_engine:
            return
        
        try:
            # Run TTS in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._speak_sync, text)
            
        except Exception as e:
            self.logger.error(f"Error speaking text: {e}")
    
    def _speak_sync(self, text: str):
        """Synchronous text-to-speech (runs in executor)"""
        try:
            if self.tts_engine is not None:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as e:
            self.logger.error(f"Error in synchronous speech: {e}")
    
    async def listen(self) -> str:
        """Listen for voice input and convert to text"""
        if not self.voice_enabled:
            return ""
        
        try:
            # For now, return empty string as speech recognition is complex
            # This would be implemented with speech_recognition or similar
            self.logger.info("Voice input not yet implemented")
            return ""
            
        except Exception as e:
            self.logger.error(f"Error listening for voice input: {e}")
            return ""
    
    async def cleanup(self):
        """Cleanup voice resources"""
        if self.tts_engine:
            try:
                self.tts_engine.stop()
                self.tts_engine = None
            except Exception as e:
                self.logger.error(f"Error cleaning up TTS engine: {e}")
        
        self.logger.info("Voice handler cleaned up")
    
    def is_available(self) -> bool:
        """Check if voice capabilities are available"""
        return self.voice_enabled and self.tts_engine is not None
    
    def get_voice_info(self) -> dict:
        """Get information about voice capabilities"""
        return {
            "enabled": self.voice_enabled,
            "engine": self.voice_engine,
            "rate": self.voice_rate,
            "volume": self.voice_volume,
            "available": self.is_available()
        } 