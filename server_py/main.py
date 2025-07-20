#!/usr/bin/env python3
"""
Entry point for the gemini-cli-mcp server.
This file imports the main functionality from the src directory.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main function from src/main.py
from src.main import main

if __name__ == "__main__":
    main() 