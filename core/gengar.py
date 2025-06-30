#!/usr/bin/env python3
"""
G.E.N.G.A.R - Gage's Enhanced Next-Gen AI Responder
Core AI Assistant Module
Author: Gage Ayala
"""

import os
import sys
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional

# Import core modules
from .ai_handler import AIHandler
from .commands import CommandHandler
from .config import Config
from .voice import VoiceHandler

class GENGAR:
    """
    Main G.E.N.G.A.R AI Assistant class
    Handles core functionality, command routing, and system management
    """
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize G.E.N.G.A.R with configuration"""
        self.config = Config(config_path)
        self.ai_handler = AIHandler(self.config)
        self.command_handler = CommandHandler(self.config)
        self.voice_handler = VoiceHandler(self.config)
        
        # Setup logging
        self.setup_logging()
        
        # System state
        self.is_running = False
        self.session_start = None
        self.command_history = []
        
        self.logger.info("G.E.N.G.A.R initialized successfully")
    
    def setup_logging(self):
        """Configure logging for the system"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = f"{log_dir}/gengar_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger("GENGAR")
    
    async def start(self):
        """Start G.E.N.G.A.R AI Assistant"""
        self.is_running = True
        self.session_start = datetime.now()
        
        self.logger.info("Starting G.E.N.G.A.R AI Assistant...")
        print("🤖 G.E.N.G.A.R is now online and ready to assist!")
        print("💬 Type 'help' for available commands or 'exit' to quit")
        
        # Initialize voice if enabled
        if self.config.get("voice_enabled", False):
            await self.voice_handler.initialize()
        
        # Start command loop
        await self.command_loop()
    
    async def command_loop(self):
        """Main command processing loop"""
        while self.is_running:
            try:
                # Get user input
                user_input = await self.get_user_input()
                
                if not user_input.strip():
                    continue
                
                # Process command
                response = await self.process_command(user_input)
                
                # Display response
                await self.display_response(response)
                
                # Log command
                self.log_command(user_input, response)
                
            except KeyboardInterrupt:
                print("\n🛑 Shutdown signal received...")
                break
            except Exception as e:
                self.logger.error(f"Error in command loop: {e}")
                print(f"❌ Error: {e}")
        
        await self.shutdown()
    
    async def get_user_input(self) -> str:
        """Get user input from text or voice"""
        if self.config.get("voice_enabled", False):
            # Voice input
            return await self.voice_handler.listen()
        else:
            # Text input
            return input("🎤 G.E.N.G.A.R > ")
    
    async def process_command(self, user_input: str) -> str:
        """Process user input and return response"""
        try:
            # Check for system commands first
            if user_input.lower() in ['exit', 'quit', 'shutdown']:
                self.is_running = False
                return "🛑 Shutting down G.E.N.G.A.R..."
            
            if user_input.lower() in ['help', '?']:
                return self.get_help_text()
            
            if user_input.lower() == 'status':
                return self.get_system_status()
            
            # Check for custom commands
            command_response = await self.command_handler.execute(user_input)
            if command_response:
                return command_response
            
            # Fall back to AI processing
            ai_response = await self.ai_handler.process(user_input)
            return ai_response
            
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            return f"❌ Error processing command: {e}"
    
    async def display_response(self, response: str):
        """Display response to user via text or voice"""
        print(f"🤖 G.E.N.G.A.R: {response}")
        
        if self.config.get("voice_enabled", False):
            await self.voice_handler.speak(response)
    
    def get_help_text(self) -> str:
        """Get help information"""
        help_text = """
🤖 G.E.N.G.A.R AI Assistant - Available Commands:

📋 System Commands:
  • help, ? - Show this help message
  • status - Show system status
  • exit, quit, shutdown - Exit G.E.N.G.A.R

🔧 Custom Commands:
  • scan [target] - Network port scan
  • vpn status - Check VPN connection
  • firewall logs - Show firewall logs
  • system info - Get system information
  • network scan [range] - Scan network range

🧠 AI Features:
  • Ask questions about cybersecurity
  • Request help with penetration testing
  • Get explanations of security concepts
  • Discuss CTF challenges and techniques

💡 Examples:
  • "What is SQL injection?"
  • "Help me understand privilege escalation"
  • "Scan 192.168.1.1"
  • "Check VPN status"
        """
        return help_text.strip()
    
    def get_system_status(self) -> str:
        """Get current system status"""
        uptime = datetime.now() - self.session_start if self.session_start else "N/A"
        
        status = f"""
📊 G.E.N.G.A.R System Status:

🕐 Session Start: {self.session_start}
⏱️  Uptime: {uptime}
🎤 Voice Enabled: {self.config.get('voice_enabled', False)}
🤖 AI Model: {self.config.get('ai_model', 'GPT-4')}
📝 Commands Processed: {len(self.command_history)}
🔧 Custom Commands: {len(self.command_handler.commands)}
        """
        return status.strip()
    
    def log_command(self, user_input: str, response: str):
        """Log command and response"""
        command_log = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "session_duration": str(datetime.now() - self.session_start) if self.session_start else "N/A"
        }
        
        self.command_history.append(command_log)
        
        # Save to log file
        log_file = f"logs/commands_{datetime.now().strftime('%Y%m%d')}.json"
        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(command_log) + '\n')
        except Exception as e:
            self.logger.error(f"Error logging command: {e}")
    
    async def shutdown(self):
        """Graceful shutdown of G.E.N.G.A.R"""
        self.logger.info("Shutting down G.E.N.G.A.R...")
        
        # Cleanup voice handler
        if self.config.get("voice_enabled", False):
            await self.voice_handler.cleanup()
        
        # Save session summary
        self.save_session_summary()
        
        print("👋 G.E.N.G.A.R shutdown complete. Goodbye!")
    
    def save_session_summary(self):
        """Save session summary to file"""
        if not self.session_start:
            return
        
        session_duration = datetime.now() - self.session_start
        
        summary = {
            "session_start": self.session_start.isoformat(),
            "session_end": datetime.now().isoformat(),
            "duration": str(session_duration),
            "total_commands": len(self.command_history),
            "commands_processed": [cmd["user_input"] for cmd in self.command_history]
        }
        
        summary_file = f"logs/session_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving session summary: {e}")

def main():
    """Main entry point for G.E.N.G.A.R"""
    gengar = GENGAR()
    
    try:
        asyncio.run(gengar.start())
    except KeyboardInterrupt:
        print("\n🛑 G.E.N.G.A.R interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main() 