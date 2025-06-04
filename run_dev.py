"""
Development mode runner for NewGAN Manager
"""
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import the main modules
from src.newganmanager.app import main

if __name__ == '__main__':
    # Run the application
    print("Starting NewGAN Manager in development mode...")
    main().main_loop()
