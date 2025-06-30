#!/usr/bin/env python3
"""
Configuration Management for G.E.N.G.A.R
Author: Gage Ayala
"""

import json
import os
from typing import Any, Dict, Optional

class Config:
    """Configuration management for G.E.N.G.A.R"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
                return self.get_default_config()
        else:
            # Create default config
            default_config = self.get_default_config()
            self.save_config(default_config)
            return default_config
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "ai_model": "gpt-4",
            "openai_api_key": "",
            "voice_enabled": False,
            "voice_engine": "pyttsx3",
            "voice_rate": 150,
            "voice_volume": 0.9,
            "log_level": "INFO",
            "log_file": "logs/gengar.log",
            "commands": {
                "scan": {
                    "enabled": True,
                    "timeout": 30
                },
                "vpn": {
                    "enabled": True,
                    "check_interval": 60
                },
                "firewall": {
                    "enabled": True,
                    "log_path": "/var/log/firewall.log"
                }
            },
            "network": {
                "default_scan_ports": "1-1000",
                "scan_timeout": 5,
                "max_threads": 100
            },
            "security": {
                "allowed_ips": [],
                "blocked_ips": [],
                "vpn_required": False
            }
        }
    
    def save_config(self, config: Optional[Dict[str, Any]] = None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save to file
        self.save_config()
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values"""
        for key, value in updates.items():
            self.set(key, value) 