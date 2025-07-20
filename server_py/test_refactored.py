#!/usr/bin/env python3
"""
Simple test script to verify the refactored implementation works correctly.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import load_config, AppConfig, GeminiCLIConfig
from src.gemini_client import GeminiClient, GeminiClientError
from src.tools import ToolManager

class TestRefactoredImplementation(unittest.TestCase):
    
    def test_config_loading(self):
        """Test that configuration loads correctly."""
        config = load_config()
        self.assertIsInstance(config, AppConfig)
        self.assertIsInstance(config.gemini_cli, GeminiCLIConfig)
        self.assertEqual(config.gemini_cli.model, "gemini-2.5-flash")
        self.assertTrue(config.gemini_cli.all_files)
        self.assertTrue(config.gemini_cli.sandbox)
    
    def test_gemini_client_initialization(self):
        """Test GeminiClient initialization."""
        config = GeminiCLIConfig()
        client = GeminiClient(config)
        self.assertIsInstance(client, GeminiClient)
    
    @patch('subprocess.run')
    def test_gemini_client_verify_executable(self, mock_run):
        """Test gemini executable verification."""
        mock_run.return_value = MagicMock(returncode=0)
        config = GeminiCLIConfig()
        client = GeminiClient(config)
        
        # Should not raise an exception
        client._verify_gemini_executable()
    
    @patch('subprocess.run')
    def test_gemini_client_verify_executable_not_found(self, mock_run):
        """Test gemini executable verification when not found."""
        mock_run.side_effect = FileNotFoundError()
        config = GeminiCLIConfig()
        client = GeminiClient(config)
        
        with self.assertRaises(GeminiClientError):
            client._verify_gemini_executable()
    
    def test_gemini_client_build_command(self):
        """Test command building."""
        config = GeminiCLIConfig()
        client = GeminiClient(config)
        
        cmd = client._build_gemini_command("ask", "test question")
        self.assertIn("gemini", cmd)
        self.assertIn("ask", cmd)
        self.assertIn("--model", cmd)
        self.assertIn("gemini-2.5-flash", cmd)
        self.assertIn("--all-files", cmd)
        self.assertIn("--sandbox", cmd)
        self.assertIn("--prompt", cmd)
        self.assertIn("test question", cmd)
    
    def test_gemini_client_process_output(self):
        """Test output processing."""
        config = GeminiCLIConfig()
        client = GeminiClient(config)
        
        test_output = """Some output
Loaded cached credentials.
[DEBUG] Some debug info
More output
Flushing log events to Clearcut.
Final output"""
        
        processed = client._process_gemini_output(test_output)
        self.assertNotIn("Loaded cached credentials.", processed)
        self.assertNotIn("[DEBUG]", processed)
        self.assertNotIn("Flushing log events to Clearcut.", processed)
        self.assertIn("Some output", processed)
        self.assertIn("More output", processed)
        self.assertIn("Final output", processed)

if __name__ == '__main__':
    unittest.main() 