"""
Configuration Utility

Manages application configuration and settings.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import json

class Config:
    """Configuration manager for the Cloud-Native AI Agent."""
    
    def __init__(self, config_file: Optional[str] = None):
        # Load environment variables
        load_dotenv()
        
        # Load configuration file if provided
        self.config_file = config_file
        self.config_data = {}
        
        if config_file and os.path.exists(config_file):
            self.load_config_file()
        
        # Set default values
        self._set_defaults()
    
    def _set_defaults(self):
        """Set default configuration values."""
        self.defaults = {
            'gemini': {
                'api_key': os.getenv('GEMINI_API_KEY'),
                'model': 'gemini-1.5-flash',
                'max_tokens': 1000,
                'temperature': 0.7
            },
            'scraping': {
                'timeout': int(os.getenv('REQUEST_TIMEOUT', 30)),
                'max_retries': int(os.getenv('MAX_RETRIES', 3)),
                'user_agent': os.getenv('USER_AGENT', 'Mozilla/5.0 (compatible; CloudNativeAIAgent/1.0)')
            },
            'cache': {
                'expiry_hours': int(os.getenv('CACHE_EXPIRY_HOURS', 6)),
                'max_size': int(os.getenv('MAX_CACHE_SIZE', 1000))
            },
            'database': {
                'url': os.getenv('DATABASE_URL', 'sqlite:///cloud_native_agent.db')
            },
            'logging': {
                'level': os.getenv('LOG_LEVEL', 'INFO'),
                'debug': os.getenv('DEBUG', 'False').lower() == 'true'
            },
            'credentials': {
                'linux_foundation': {
                    'username': os.getenv('LINUX_FOUNDATION_USERNAME'),
                    'password': os.getenv('LINUX_FOUNDATION_PASSWORD')
                },
                'cncf': {
                    'username': os.getenv('CNCF_USERNAME'),
                    'password': os.getenv('CNCF_PASSWORD')
                }
            }
        }
    
    def load_config_file(self):
        """Load configuration from file."""
        try:
            with open(self.config_file, 'r') as f:
                self.config_data = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config file {self.config_file}: {e}")
            self.config_data = {}
    
    def save_config_file(self):
        """Save configuration to file."""
        if not self.config_file:
            return
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config file {self.config_file}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        # Check config file first
        if key in self.config_data:
            return self.config_data[key]
        
        # Check environment variables
        env_value = os.getenv(key.upper())
        if env_value is not None:
            return env_value
        
        # Check defaults
        keys = key.split('.')
        value = self.defaults
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set a configuration value."""
        self.config_data[key] = value
        
        # Save to file if possible
        self.save_config_file()
    
    def get_gemini_config(self) -> Dict[str, Any]:
        """Get Gemini configuration."""
        return {
            'api_key': self.get('gemini.api_key'),
            'model': self.get('gemini.model'),
            'max_tokens': self.get('gemini.max_tokens'),
            'temperature': self.get('gemini.temperature')
        }
    
    def get_scraping_config(self) -> Dict[str, Any]:
        """Get web scraping configuration."""
        return {
            'timeout': self.get('scraping.timeout'),
            'max_retries': self.get('scraping.max_retries'),
            'user_agent': self.get('scraping.user_agent')
        }
    
    def get_cache_config(self) -> Dict[str, Any]:
        """Get cache configuration."""
        return {
            'expiry_hours': self.get('cache.expiry_hours'),
            'max_size': self.get('cache.max_size')
        }
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration."""
        return {
            'url': self.get('database.url')
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return {
            'level': self.get('logging.level'),
            'debug': self.get('logging.debug')
        }
    
    def get_credentials(self, service: str) -> Dict[str, str]:
        """Get credentials for a specific service."""
        return self.get(f'credentials.{service}', {})
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate the configuration and return any issues."""
        issues = []
        warnings = []
        
        # Check required settings
        if not self.get('gemini.api_key'):
            issues.append("Gemini API key is required")
        
        # Check optional settings
        if not self.get('credentials.linux_foundation.username'):
            warnings.append("Linux Foundation credentials not set (optional)")
        
        if not self.get('credentials.cncf.username'):
            warnings.append("CNCF credentials not set (optional)")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
    
    def update_from_dict(self, config_dict: Dict[str, Any]):
        """Update configuration from a dictionary."""
        self.config_data.update(config_dict)
        self.save_config_file()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.config_data = {}
        self.save_config_file()
    
    def export_config(self) -> Dict[str, Any]:
        """Export current configuration."""
        return {
            'config_file': self.config_data,
            'defaults': self.defaults,
            'validation': self.validate_config()
        } 