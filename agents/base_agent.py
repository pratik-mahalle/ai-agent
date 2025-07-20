"""
Base Agent Class

Provides common functionality for all AI agents in the system.
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseAgent(ABC):
    """Base class for all AI agents in the system."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"agent.{name}")
        
        # Initialize Gemini client
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Agent state
        self.conversation_history: List[Dict[str, Any]] = []
        self.last_updated = datetime.now()
    
    @abstractmethod
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request and return a response."""
        pass
    
    def add_to_history(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to the conversation history."""
        entry = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.conversation_history.append(entry)
        self.last_updated = datetime.now()
    
    def get_context(self, max_entries: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation context."""
        return self.conversation_history[-max_entries:]
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history.clear()
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        return {
            'name': self.name,
            'description': self.description,
            'last_updated': self.last_updated.isoformat(),
            'conversation_length': len(self.conversation_history),
            'status': 'active'
        }
    async def generate_response(self, prompt: str, system_message: str = None) -> str:
        """Generate a response using Google Gemini API."""
        # Construct the full prompt with system message and context
        full_prompt = ""
        
        if system_message:
            full_prompt += f"System: {system_message}\n\n"
        
        # Add recent context
        context = self.get_context(5)
        for entry in context:
            role = entry['role']
            content = entry['content']
            if role == 'system':
                continue  # Skip system messages from context
            elif role == 'user':
                full_prompt += f"Human: {content}\n"
            elif role == 'assistant':
                full_prompt += f"Assistant: {content}\n"
        
        full_prompt += f"\nHuman: {prompt}\n\nAssistant:"
        
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def log_activity(self, activity: str, details: Optional[Dict] = None):
        """Log agent activity."""
        self.logger.info(f"{activity}: {details or 'No details'}")
        self.add_to_history('system', activity, details) 