#!/usr/bin/env python3
"""
Test script for Terra CLI
This script tests all major Terra CLI functionality to ensure it's working properly
"""

import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

# Colors for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def log_info(message):
    print(f"{BLUE}[TEST]{NC} {message}")

def log_success(message):
    print(f"{GREEN}[PASS]{NC} {message}")

def log_error(message):
    print(f"{RED}[FAIL]{NC} {message}")

def log_warning(message):
    print(f"{YELLOW}[WARN]{NC} {message}")

def test_terra_cli_import():
    """Test that Terra CLI can be imported"""
    log_info("Testing Terra CLI import...")
    
    try:
        # Add terra CLI to path
        terra_cli_path = Path(__file__).parent / "terra" / "cli"
        sys.path.insert(0, str(terra_cli_path))
        
        # Test importing main CLI
        from terra_cli import FernCLI
        cli = FernCLI()
        
        log_success("Terra CLI import successful")
        return True
    except Exception as e:
        log_error(f"Failed to import Terra CLI: {e}")
        return False

def test_command_imports():
    """Test that all command modules can be imported"""
    log_info("Testing command module imports...")
    
    try:
        terra_cli_path = Path(__file__).parent / "terra" / "cli"
        sys.path.insert(0, str(terra_cli_path))
        
        # Test importing all commands
        from commands.bloom import BloomCommand
        from commands.sprout import SproutCommand
        from commands.fire import FireCommand
        from commands.prepare import PrepareCommand
        from commands.install import InstallCommand
        from commands.templates import TemplatesCommand
        
        # Test creating instances
        commands = {
            'bloom': BloomCommand(),
            'sprout': SproutCommand(),
            'fire': FireCommand(),
            'prepare': PrepareCommand(),
            'install': InstallCommand(),
            'templates': TemplatesCommand(),
        }
        
        log_success("All command modules imported successfully")
        return True
    except Exception as e:
        log_error(f"Failed to import command modules: {e}")
        return False

def test_utils_imports():
    """Test that all utility modules can be imported"""
    log_info("Testing utility module imports...")
    
    try:
        terra_cli_path = Path(__file__).parent / "terra" / "cli"
        sys.path.insert(0, str(terra_cli_path))
        
        # Test importing all utils
        from utils.colors import Colors, print_colored
        from utils.config import config
        from utils.templates import TemplateManager
        
        log_success("All utility modules imported successfully")
        return True
    except Exception as e:
        log_error(f"Failed to import utility modules: {e}")
        return False

def test_help_command():
    """Test the help command"""
    log_info("Testing help command...")
    
    try:
        terra_cli_path = Path(__file__).parent / "terra" / "cli"
        sys.path.insert(0, str(terra_cli_path))
        
        from terra_cli import FernCLI
        cli = FernCLI()
        
        # Test help command (should not raise exception)
        cli.run(['help'])
        
        log_success("Help command works")
        return True
    except Exception as e:
        log_error(f"Help command failed: {e}")
        return False

def test_bloom_command():
    """Test the bloom command"""
    log_info("Testing bloom command...")
    
    try:
        terra_cli_path = Path(__file__).parent / "terra" / "cli"
        sys.path.insert(0, str(terra_cli_path))
        
        from commands.bloom import BloomCommand
        bloom = BloomCommand()
        
        # Test bloom command (should not raise exception)
        bloom.execute([])
        
        log_success("Bloom command works")
        return True
    except Exception as e:
        log_error(f"Bloom command failed: {e}")
        return False

def test_templates_command():
    """Test the templates command"""
    log_info("Testing templates command...")
    
    try:
        terra_cli_path = Path(__file__).parent / "terra" / "cli"
        sys.path.insert(0, str(terra_cli_path))
        
        from commands.templates import TemplatesCommand
        templates = TemplatesCommand()
        
        # Test templates list command
        templates.execute(['list'])
        
        log_success("Templates command works")
        return True
    except Exception as e:
        log_error(f"Templates command failed: {e}")
        return False

def test_sprout_command():
    """Test the sprout command with a temporary project"""
    log_info("Testing sprout command...")
    
    try:
        terra_cli_path = Path(__file__).parent / "terra" / "cli"
        sys.path.insert(0, str(terra_cli_path))
        
        from commands.sprout import SproutCommand
        sprout = SproutCommand()
        
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Test sprout command
                sprout.execute(['test_project'])
                
                # Check if project was created
                if Path('test_project').exists():
                    log_success("Sprout command works")
                    return True
                else:
                    log_warning("Sprout command ran but project directory not found")
                    return False
            finally:
                os.chdir(original_cwd)
                
    except Exception as e:
        log_error(f"Sprout command failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist in the Terra CLI"""
    log_info("Testing Terra CLI file structure...")
    
    terra_dir = Path(__file__).parent / "terra"
    required_files = [
        "README.md",
        "setup.py",
        "requirements.txt",
        "install.sh",
        "cli/terra_cli.py",
        "cli/commands/__init__.py",
        "cli/commands/bloom.py",
        "cli/commands/sprout.py",
        "cli/commands/fire.py",
        "cli/commands/prepare.py",
        "cli/commands/install.py",
        "cli/commands/templates.py",
        "cli/utils/__init__.py",
        "cli/utils/colors.py",
        "cli/utils/config.py",
        "cli/utils/templates.py",
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (terra_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        log_error(f"Missing files: {', '.join(missing_files)}")
        return False
    else:
        log_success("All required files exist")
        return True

def test_flare_structure():
    """Test that Flare directory structure exists"""
    log_info("Testing Flare structure...")
    
    flare_dir = Path(__file__).parent / "flare"
    required_dirs = [
        "templates",
        "extensions",
        "tools",
        "templates/game",
        "templates/dashboard",
        "templates/creative",
        "templates/portfolio",
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not (flare_dir / dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        log_error(f"Missing directories: {', '.join(missing_dirs)}")
        return False
    else:
        log_success("All required Flare directories exist")
        return True

def main():
    """Run all tests"""
    print("="*60)
    print("Terra CLI Test Suite")
    print("="*60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Flare Structure", test_flare_structure),
        ("Terra CLI Import", test_terra_cli_import),
        ("Command Imports", test_command_imports),
        ("Utils Imports", test_utils_imports),
        ("Help Command", test_help_command),
        ("Bloom Command", test_bloom_command),
        ("Templates Command", test_templates_command),
        ("Sprout Command", test_sprout_command),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            log_error(f"Test {test_name} crashed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        log_success("All tests passed! Terra CLI is ready.")
        return 0
    else:
        log_error(f"{failed} tests failed. Please fix the issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
