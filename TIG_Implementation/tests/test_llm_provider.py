"""
Unit tests for LLM Provider abstraction layer
"""

import sys
import os
import pytest
from unittest.mock import Mock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.llm_provider import (
    BaseLLMProvider,
    OpenAIProvider,
    ClaudeProvider,
    get_llm_provider
)


class TestLLMProviderFactory:
    """Test the get_llm_provider factory function"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_openai_provider(self):
        """Test getting OpenAI provider"""
        provider = get_llm_provider('openai')
        assert isinstance(provider, OpenAIProvider)
        assert provider.model == 'gpt-4'  # default model
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    def test_get_claude_provider(self):
        """Test getting Claude provider"""
        provider = get_llm_provider('claude')
        assert isinstance(provider, ClaudeProvider)
        assert 'claude' in provider.model.lower()
    
    @patch.dict(os.environ, {'LLM_PROVIDER': 'claude', 'ANTHROPIC_API_KEY': 'test_key'})
    def test_provider_from_env(self):
        """Test reading provider from environment variable"""
        provider = get_llm_provider()  # Should read from LLM_PROVIDER env var
        assert isinstance(provider, ClaudeProvider)
    
    def test_invalid_provider(self):
        """Test error handling for invalid provider"""
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            get_llm_provider('invalid_provider')


class TestOpenAIProvider:
    """Test OpenAI provider implementation"""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_initialization(self):
        """Test OpenAI provider initialization"""
        provider = OpenAIProvider()
        assert provider.api_key == 'test_key'
        assert provider.model == 'gpt-4'
    
    def test_missing_api_key(self):
        """Test error when API key is missing"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key not found"):
                OpenAIProvider()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('agents.llm_provider.OpenAI')
    def test_generate(self, mock_openai_class):
        """Test text generation with OpenAI"""
        # Mock the OpenAI client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        provider = OpenAIProvider()
        messages = [{"role": "user", "content": "Hello"}]
        response = provider.generate(messages)
        
        assert response == "Test response"
        mock_client.chat.completions.create.assert_called_once()


class TestClaudeProvider:
    """Test Claude provider implementation"""
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    def test_initialization(self):
        """Test Claude provider initialization"""
        provider = ClaudeProvider()
        assert provider.api_key == 'test_key'
        assert 'claude' in provider.model.lower()
    
    def test_missing_api_key(self):
        """Test error when API key is missing"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Anthropic API key not found"):
                ClaudeProvider()
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    @patch('agents.llm_provider.Anthropic')
    def test_generate(self, mock_anthropic_class):
        """Test text generation with Claude"""
        # Mock the Anthropic client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock(text="Test response")]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client
        
        provider = ClaudeProvider()
        messages = [{"role": "user", "content": "Hello"}]
        response = provider.generate(messages)
        
        assert response == "Test response"
        mock_client.messages.create.assert_called_once()
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    @patch('agents.llm_provider.Anthropic')
    def test_system_message_handling(self, mock_anthropic_class):
        """Test that system messages are handled correctly"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock(text="Test response")]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client
        
        provider = ClaudeProvider()
        messages = [
            {"role": "system", "content": "You are helpful"},
            {"role": "user", "content": "Hello"}
        ]
        response = provider.generate(messages)
        
        # Verify system message was passed separately
        call_args = mock_client.messages.create.call_args
        assert 'system' in call_args[1]
        assert call_args[1]['system'] == "You are helpful"


class TestProviderSwitching:
    """Test switching between providers"""
    
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'openai_key',
        'ANTHROPIC_API_KEY': 'claude_key'
    })
    def test_switch_providers(self):
        """Test that we can switch between providers"""
        openai_provider = get_llm_provider('openai')
        claude_provider = get_llm_provider('claude')
        
        assert isinstance(openai_provider, OpenAIProvider)
        assert isinstance(claude_provider, ClaudeProvider)
        assert openai_provider.api_key != claude_provider.api_key


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
