"""
Run NewGAN Manager with minimal dependencies
"""
import sys
import os
import logging

# Add src directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

# Configure enhanced logging
log_file = os.path.join(current_dir, 'newgan_run.log')
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s: %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('NewGAN-Launcher')
logger.info("Starting NewGAN Manager...")

try:
    # Import the main app module
    logger.info("Importing main application module...")
    from src.newganmanager.app import main
    
    # Run the application
    logger.info("Starting application main loop...")
    app = main()
    app.main_loop()
    
except ModuleNotFoundError as e:
    logger.error(f"Module not found: {e}")
    logger.info("This likely means you need to install required dependencies.")
    print("\n" + "="*60)
    print("ERROR: Missing dependencies")
    print("="*60)
    print(f"Error details: {e}")
    print("\nTo install required dependencies, try:")
    print("pip install toga==0.3.0 toga-winforms==0.3.0")
    print("pip install dhooks==1.1.4 requests")
    print("\nIf you encounter C++ build errors, consider using simple_dev.py instead")
    
except Exception as e:
    logger.error(f"Error running application: {e}")
    logger.exception("Detailed error:")
    print(f"\nApplication failed to start: {e}")
    print("See newgan_run.log for details")
