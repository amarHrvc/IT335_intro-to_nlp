"""
Ollama LLM Provider - Free Local LLM Support

Provides integration with Ollama for running local LLMs (Llama, Mistral, etc.)
No API keys required - completely free!
"""

import os
import requests
from typing import List, Dict, Optional
import json


class OllamaProvider:
    """
    Ollama provider for local LLMs
    
    Installation:
    1. Download Ollama: https://ollama.ai/download
    2. Install a model: ollama pull llama2
    3. Run: ollama serve (starts on localhost:11434)
    """
    
    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama provider
        
        Args:
            model: Model name (llama2, mistral, codellama, etc.)
            base_url: Ollama API endpoint (default: localhost:11434)
        """
        self.model = model
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/generate"
        
        # Check if Ollama is running
        if not self._check_ollama_running():
            print("⚠️ Ollama not detected. Starting instructions:")
            print("1. Download: https://ollama.ai/download")
            print("2. Install model: ollama pull llama2")
            print("3. Run: ollama serve")
            print("\nUsing fallback mode for now...")
            self.available = False
        else:
            print(f"✓ Ollama provider initialized (model: {self.model})")
            self.available = True
    
    def _check_ollama_running(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_default_model(self) -> str:
        """Return default Ollama model"""
        return "llama2"
    
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int = 1500, 
        temperature: float = 0.7
    ) -> str:
        """
        Generate text using Ollama
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text response
        """
        if not self.available:
            return self._fallback_response(messages)
        
        # Convert messages to prompt
        prompt = self._messages_to_prompt(messages)
        
        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                print(f"⚠️ Ollama error: {response.status_code}")
                return self._fallback_response(messages)
                
        except Exception as e:
            print(f"⚠️ Ollama request failed: {e}")
            return self._fallback_response(messages)
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to single prompt"""
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
    
    def _fallback_response(self, messages: List[Dict[str, str]]) -> str:
        """Template-based fallback when Ollama not available"""
        # Extract user message
        user_msg = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_msg = msg.get("content", "")
                break
        
        # Simple template response
        return json.dumps({
            "note": "Ollama not available - using template",
            "message": "This is a template response. Install Ollama for real LLM generation."
        })


def get_ollama_provider(model: str = "llama2") -> OllamaProvider:
    """
    Factory function to create Ollama provider
    
    Args:
        model: Model name (llama2, mistral, codellama)
        
    Returns:
        OllamaProvider instance
    """
    return OllamaProvider(model=model)
