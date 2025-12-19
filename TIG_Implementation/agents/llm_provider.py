"""
LLM Provider Abstraction Layer

This module provides a unified interface for different LLM providers (OpenAI, Claude).
Allows easy switching between providers via configuration.
"""

import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM provider
        
        Args:
            api_key: API key for the provider (if None, reads from env)
            model: Model name to use (if None, uses default)
        """
        self.api_key = api_key
        self.model = model or self.get_default_model()
        self._validate_api_key()
    
    @abstractmethod
    def get_default_model(self) -> str:
        """Return the default model name for this provider"""
        pass
    
    @abstractmethod
    def _validate_api_key(self):
        """Validate that API key is available"""
        pass
    
    @abstractmethod
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int = 1500, 
        temperature: float = 0.7
    ) -> str:
        """
        Generate text using the LLM
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            
        Returns:
            Generated text response
        """
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider implementation"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize OpenAI provider"""
        super().__init__(api_key, model)
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key)
        print(f"✓ OpenAI provider initialized (model: {self.model})")
    
    def get_default_model(self) -> str:
        """Return default OpenAI model"""
        return os.getenv("OPENAI_MODEL", "gpt-4")
    
    def _validate_api_key(self):
        """Validate OpenAI API key"""
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
    
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int = 1500, 
        temperature: float = 0.7
    ) -> str:
        """Generate text using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            content = response.choices[0].message.content
            
            # Strip markdown code blocks if present
            # OpenAI often wraps JSON in ```json ... ```
            if content and content.strip().startswith("```"):
                content = content.strip()
                
                # Remove opening markdown
                if content.startswith("```json"):
                    content = content[7:]  # Remove ```json
                elif content.startswith("```"):
                    content = content[3:]   # Remove ```
                
                # Remove closing markdown
                if content.endswith("```"):
                    content = content[:-3]  # Remove ```
                
                content = content.strip()
            
            return content
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")

    def generate_with_debug(self, messages: List[Dict[str, str]], max_tokens: int = 1500, temperature: float = 0.7 ) -> Dict[str, str]:
        """
        Generate text using OpenAI API with debug information
        :returns: Dict with 'content' (processed) and 'raw_content' (original resposne)
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )

            # Get raw content (before any processing)
            raw_content = response.choices[0].message.content

            #process content
            content=raw_content
            if content and content.strip().startswith("```"):
                content = content.strip()

                # remove open markdown
                if content.startswith("```json"):
                    content = content[7:]
                elif content.startswith("```"):
                    content = content[3:]

                # Remove closing markdown
                if content.endswith("```"):
                    content = content[:-3]

                content = content.strip()

            return {
                'content': content,
                'raw_content': raw_content
            }

        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")




class ClaudeProvider(BaseLLMProvider):
    """Anthropic Claude provider implementation"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize Claude provider"""
        super().__init__(api_key, model)
        from anthropic import Anthropic
        self.client = Anthropic(api_key=self.api_key)
        print(f"✓ Claude provider initialized (model: {self.model})")
    
    def get_default_model(self) -> str:
        """Return default Claude model"""
        return os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    
    def _validate_api_key(self):
        """Validate Anthropic API key"""
        if not self.api_key:
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )
    
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int = 1500, 
        temperature: float = 0.7
    ) -> str:
        """Generate text using Claude API"""
        try:
            # Claude API expects system message separately
            system_message = None
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append(msg)
            
            # If no user messages, convert system to user
            if not user_messages and system_message:
                user_messages = [{"role": "user", "content": system_message}]
                system_message = None
            
            # Create API call parameters
            api_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": user_messages
            }
            
            # Add system message if present
            if system_message:
                api_params["system"] = system_message
            
            response = self.client.messages.create(**api_params)
            content = response.content[0].text
            
            # Strip markdown code blocks if present (same as OpenAI)
            if content and content.strip().startswith("```"):
                content = content.strip()
                
                # Remove opening markdown
                if content.startswith("```json"):
                    content = content[7:]
                elif content.startswith("```"):
                    content = content[3:]
                
                # Remove closing markdown
                if content.endswith("```"):
                    content = content[:-3]
                
                content = content.strip()
            
            return content
            
        except Exception as e:
            raise RuntimeError(f"Claude API error: {str(e)}")

    def generate_with_debug(
            self,
            messages: List[Dict[str, str]],
            max_tokens: int = 1500,
            temperature: float = 0.7
    ) -> Dict[str, str]:
        """
        Generate text using Claude API with debug information

        Returns:
            Dict with 'content' (processed) and 'raw_content' (original response)
        """
        try:
            # Extract system message
            system_msg = next((m['content'] for m in messages if m['role'] == 'system'), None)
            user_messages = [m for m in messages if m['role'] != 'system']

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_msg,
                messages=user_messages
            )

            # Get raw content
            raw_content = response.content[0].text

            # Process content (strip markdown)
            content = raw_content
            if content and content.strip().startswith("```"):
                content = content.strip()

                # Remove opening markdown
                if content.startswith("```json"):
                    content = content[7:]
                elif content.startswith("```"):
                    content = content[3:]

                # Remove closing markdown
                if content.endswith("```"):
                    content = content[:-3]

                content = content.strip()

            return {
                'content': content,
                'raw_content': raw_content
            }

        except Exception as e:
            raise RuntimeError(f"Claude API error: {str(e)}")

def get_llm_provider(
    provider_name: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None
) -> BaseLLMProvider:
    """
    Factory function to get LLM provider instance
    
    Args:
        provider_name: Provider name ('openai' or 'claude'). 
                      If None, reads from LLM_PROVIDER env var (default: 'openai')
        api_key: API key for the provider (optional)
        model: Model name to use (optional)
        
    Returns:
        Initialized LLM provider instance
        
    Raises:
        ValueError: If provider name is invalid
        
    Example:
        >>> provider = get_llm_provider('claude')
        >>> response = provider.generate([
        ...     {"role": "user", "content": "Hello!"}
        ... ])
    """
    if not provider_name:
        provider_name = os.getenv("LLM_PROVIDER", "openai").lower()
    
    provider_name = provider_name.lower()
    
    if provider_name == "openai":
        return OpenAIProvider(api_key=api_key, model=model)
    elif provider_name == "claude":
        return ClaudeProvider(api_key=api_key, model=model)
    else:
        raise ValueError(
            f"Unknown LLM provider: '{provider_name}'. "
            f"Supported providers: 'openai', 'claude'"
        )
