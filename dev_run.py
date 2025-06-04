"""
Dev mode runner for NewGAN Manager with simplified imports
"""
import sys
import os

# Make the 'src' directory available for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

# Create a simple stub for problematic modules
class StubModule:
    """Stub class for modules we don't want to install"""
    def __getattr__(self, name):
        return self
    
    def __call__(self, *args, **kwargs):
        return self

# Create a simple logger for development
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s: %(message)s",
    handlers=[logging.FileHandler("newgan_dev.log"), logging.StreamHandler()]
)
logger = logging.getLogger("NewGAN-Dev")
logger.info("Starting NewGAN Manager in DEV mode...")

# Mock problematic modules
import builtins
original_import = builtins.__import__

def mock_import(name, globals=None, locals=None, fromlist=(), level=0):
    problematic_modules = ['aiohttp', 'multidict', 'pycairo', 'PyGObject']
    
    if name in problematic_modules:
        logger.warning(f"Stubbing problematic module: {name}")
        return StubModule()
    return original_import(name, globals, locals, fromlist, level)

# Override built-in import
builtins.__import__ = mock_import

try:
    # Configure a minimal GUI environment (might be needed for toga without proper dependencies)
    os.environ['TOGA_BACKEND'] = 'dummy'
    
    # Try importing and running the app in safe mode
    logger.info("Loading application modules...")
    from src.config_manager import Config_Manager
    from src.profile_manager import Profile_Manager
    from src.mapper import Mapper
    from src.rtfparser import RTF_Parser
    from src.reporter import Reporter
    from src.xmlparser import XML_Parser

    logger.info("Loaded core modules successfully")
    logger.info("Starting application...")
    
    # Try a simplified import - might need further modification
    from src.newganmanager.app import NewGANManager
    
    # Create a simple app instance
    app = NewGANManager()
    logger.info("Application initialized")
    
    # This might fail, but we can add fallback code here
    try:
        app.startup()
        logger.info("Application started up successfully")
    except Exception as e:
        logger.error(f"Error starting app: {e}")
        # We could add fallback GUI here if needed
        
except Exception as e:
    logger.error(f"Failed to import modules: {e}")
    logger.exception("Detailed error:")

logger.info("Dev script finished executing")
