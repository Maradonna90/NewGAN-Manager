"""
Simple development launcher for NewGAN Manager
This script creates a simplified environment to run core functionality
without needing the full GUI implementation
"""
import os
import sys
import logging
import json

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

# Configure logging
# UTF-8 kodlaması ile dosya handlerı oluştur
log_file_handler = logging.FileHandler("newgan_dev.log", encoding="utf-8")

# Konsol çıktısı için handler
console_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s: %(levelname)s: %(message)s",
    handlers=[
        log_file_handler,
        console_handler
    ]
)
logger = logging.getLogger("NewGAN-Dev")
logger.info("Starting NewGAN Manager in simplified development mode...")

# Import core functionality (non-GUI components)
try:
    from src.config_manager import Config_Manager
    from src.profile_manager import Profile_Manager
    from src.mapper import Mapper
    from src.rtfparser import RTF_Parser
    from src.reporter import Reporter
    from src.xmlparser import XML_Parser
    
    logger.info("Successfully imported core modules")
    
    # Test configuration
    config_path = os.path.join(current_dir, 'src', 'newganmanager', '.user', 'default_cfg.json')
    if os.path.exists(config_path):
        logger.info(f"Default config exists at: {config_path}")
        with open(config_path, 'r') as f:
            config = json.load(f)
            logger.info(f"Default config content: {config}")
    else:
        logger.warning(f"Default config not found at: {config_path}")
    
    # Create a development menu
    print("\n" + "="*50)
    print("NewGAN Manager - Development Mode")
    print("="*50)
    print("1. Test RTF Parser")
    print("2. Test Mapper")
    print("3. Test Profile Manager")
    print("4. Test XML Parser")
    print("5. Exit")
    
    choice = input("\nSelect an option (1-5): ")
    
    if choice == "1":
        # Test RTF Parser
        rtf_file = input("Enter path to RTF file to parse: ")
        # Temizle tırnak işaretlerini
        rtf_file = rtf_file.strip('"').strip("'")
        if os.path.exists(rtf_file):
            parser = RTF_Parser()
            if parser.is_rtf_valid(rtf_file):
                logger.info(f"Parsing RTF file: {rtf_file}")
                rtf_data = parser.parse_rtf(rtf_file)
                logger.info(f"Parsed {len(rtf_data)} entries from RTF")
                for i, entry in enumerate(rtf_data[:5]):  # Show first 5 entries
                    logger.info(f"Entry {i+1}: {entry}")
            else:
                logger.error("Invalid RTF file")
        else:
            logger.error(f"RTF file not found: {rtf_file}")
    
    elif choice == "2":
        # Test Mapper
        logger.info("Testing Mapper functionality")
        img_dir = input("Enter image directory path: ")
        # Temizle tırnak işaretlerini
        img_dir = img_dir.strip('"').strip("'")
        # Geliştirilmiş dizin analizi
        if os.path.exists(img_dir):
            logger.info(f"Checking image directory structure: {img_dir}")
            subdirs = [d for d in os.listdir(img_dir) if os.path.isdir(os.path.join(img_dir, d))]
            logger.info(f"Found subdirectories: {subdirs}")
            
            # Her alt dizin için detaylı analiz
            print("\n" + "-"*40)
            print("Detailed Image Directory Analysis")
            print("-"*40)
            
            total_images = 0
            image_extensions = [".png", ".jpg", ".jpeg", ".bmp"]
            
            for subdir in subdirs:
                subdir_path = os.path.join(img_dir, subdir)
                files = [f for f in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, f))]
                image_files = [f for f in files if any(f.lower().endswith(ext) for ext in image_extensions)]
                
                image_count = len(image_files)
                total_images += image_count
                
                # Log her klasördeki resim sayısını
                logger.info(f"Directory '{subdir}' contains {image_count} images")
                print(f"Directory '{subdir}': {image_count} images")
                
                # İlk birkaç resmin bilgisini göster
                if image_files:
                    sample_count = min(3, len(image_files))
                    print(f"  Sample images: {', '.join(image_files[:sample_count])}...")
            
            print("-"*40)
            print(f"Total images across all directories: {total_images}")
            print("-"*40)
            
            # Alt dizinleri görüntülemek için ek seçenek
            view_details = input("\nView details of a specific directory? (Enter directory name or 'no' to skip): ")
            view_details = view_details.strip('"').strip("'")
            
            if view_details.lower() != 'no' and view_details in subdirs:
                detail_path = os.path.join(img_dir, view_details)
                files = [f for f in os.listdir(detail_path) if os.path.isfile(os.path.join(detail_path, f))]
                image_files = [f for f in files if any(f.lower().endswith(ext) for ext in image_extensions)]
                
                print(f"\nDetailed view of '{view_details}' directory:")
                print("-"*40)
                
                # Dosya uzantılarına göre sayım
                ext_counts = {}
                for f in image_files:
                    ext = os.path.splitext(f)[1].lower()
                    ext_counts[ext] = ext_counts.get(ext, 0) + 1
                
                for ext, count in ext_counts.items():
                    print(f"File type {ext}: {count} files")
                
                # Dosya boyutları analizi
                if image_files:
                    total_size = sum(os.path.getsize(os.path.join(detail_path, f)) for f in image_files)
                    avg_size = total_size / len(image_files) if image_files else 0
                    print(f"Total size: {total_size / (1024*1024):.2f} MB")
                    print(f"Average file size: {avg_size / 1024:.2f} KB")
        else:
            logger.error(f"Image directory not found: {img_dir}")
    
    elif choice == "3":
        # Test Profile Manager
        logger.info("Testing Profile Manager")
        profile_name = input("Enter profile name to test: ")
        # Temizle tırnak işaretlerini
        profile_name = profile_name.strip('"').strip("'")
        config_mgr = Config_Manager()
        profile_path = os.path.join(current_dir, 'src', 'newganmanager', '.user', f"{profile_name}.json")
        
        if os.path.exists(profile_path):
            logger.info(f"Profile exists: {profile_path}")
            profile_data = config_mgr.load_config(profile_path)
            logger.info(f"Profile data: {profile_data}")
        else:
            logger.info(f"Creating test profile: {profile_name}")
            # Create a test profile with minimal data
            test_profile = {
                "img_dir": "",
                "rtf": "",
                "used_pics": {}
            }
            with open(profile_path, 'w') as f:
                json.dump(test_profile, f)
            logger.info(f"Created test profile at: {profile_path}")

    elif choice == "4":
        # Test XML Parser
        logger.info("Testing XML Parser")
        xml_file = input("Enter config.xml path to test: ")
        # Temizle tırnak işaretlerini
        xml_file = xml_file.strip('"').strip("'")
        if os.path.exists(xml_file):
            parser = XML_Parser()
            logger.info(f"Testing XML parser with file: {xml_file}")
            # Simple test to read XML
            try:
                uid = input("Enter player UID to look up: ")
                # Temizle tırnak işaretlerini
                uid = uid.strip('"').strip("'")
                img_path = parser.get_imgpath_from_uid(xml_file, uid)
                logger.info(f"Found image path for UID {uid}: {img_path}")
            except Exception as e:
                logger.error(f"Error parsing XML: {e}")
        else:
            logger.error(f"XML file not found: {xml_file}")
    
    else:
        logger.info("Exiting development mode")
        
except Exception as e:
    logger.error(f"Error in development mode: {e}")
    logger.exception("Detailed error:")

logger.info("Development mode session completed")
