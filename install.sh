#!/bin/bash
#
# Terra CLI Installation Script
# Installs Terra CLI - Fern UI Framework Developer Tools
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo -e "${CYAN}$1${NC}"
}

show_banner() {
    echo ""
    log_header "========================================"
    log_header "🌿 Terra CLI Installation"
    log_header "Advanced Developer Tools for Fern UI"
    log_header "========================================"
    echo ""
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "This script should not be run as root"
        exit 1
    fi
}

# Check Python dependencies
check_python() {
    log_info "Checking Python installation..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        echo "Please install Python 3.7+ and try again"
        exit 1
    fi
    
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3 is required but not installed"
        echo "Please install pip3 and try again"
        exit 1
    fi
    
    # Check Python version
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ $(echo "$python_version < 3.7" | bc -l) -eq 1 ]]; then
        log_error "Python 3.7+ is required, but found Python $python_version"
        exit 1
    fi
    
    log_success "Python $python_version found"
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    # Install requirements
    pip3 install -r requirements.txt --user
    
    log_success "Python dependencies installed"
}

# Install Terra CLI
install_terra_cli() {
    log_info "Installing Terra CLI..."
    
    # Create ~/.local/bin directory if it doesn't exist
    mkdir -p "$HOME/.local/bin"
    
    # Create Terra CLI launcher script
    cat > "$HOME/.local/bin/fern" << EOF
#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add Terra CLI directory to path
TERRA_CLI_DIR = Path("$PWD/cli")
sys.path.insert(0, str(TERRA_CLI_DIR))

from terra_cli import main

if __name__ == "__main__":
    main()
EOF
    
    # Make it executable
    chmod +x "$HOME/.local/bin/fern"
    
    # Also create 'terra' command alias
    cat > "$HOME/.local/bin/terra" << EOF
#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add Terra CLI directory to path
TERRA_CLI_DIR = Path("$PWD/cli")
sys.path.insert(0, str(TERRA_CLI_DIR))

from terra_cli import main

if __name__ == "__main__":
    main()
EOF
    
    chmod +x "$HOME/.local/bin/terra"
    
    log_success "Terra CLI installed successfully"
}

# Setup PATH
setup_path() {
    log_info "Setting up PATH..."
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        log_warning "~/.local/bin is not in your PATH"
        log_warning "Add the following line to your ~/.bashrc or ~/.zshrc:"
        echo ""
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
        
        # Temporarily add to PATH for this session
        export PATH="$HOME/.local/bin:$PATH"
        
        log_info "PATH updated for this session"
    else
        log_success "~/.local/bin is already in PATH"
    fi
}

# Create Terra configuration
create_config() {
    log_info "Creating Terra configuration..."
    
    CONFIG_DIR="$HOME/.terra"
    mkdir -p "$CONFIG_DIR"
    
    cat > "$CONFIG_DIR/config.yaml" << EOF
# Terra CLI Configuration
version: "0.1.0"
terra_dir: "$PWD"
templates_dir: "$PWD/templates"
default_template: "basic"

# Fern framework integration
fern:
  repository: "https://github.com/fernkit/fern.git"
  install_path: "$HOME/.fern"
  
# Development settings
dev:
  auto_reload: true
  show_build_output: true
  default_platform: "linux"
  
# Web development
web:
  default_port: 8000
  auto_open_browser: true
  
# Templates
templates:
  update_on_startup: false
  custom_templates_dir: "$HOME/.terra/custom_templates"
EOF
    
    log_success "Terra configuration created at $CONFIG_DIR/config.yaml"
}

# Setup templates
setup_templates() {
    log_info "Setting up project templates..."
    
    TEMPLATES_DIR="$PWD/templates"
    mkdir -p "$TEMPLATES_DIR"
    
    # Create basic template
    mkdir -p "$TEMPLATES_DIR/basic"
    cat > "$TEMPLATES_DIR/basic/template.yaml" << EOF
name: "Basic Fern Project"
description: "A simple Fern UI application template"
version: "1.0.0"
author: "Terra CLI"

files:
  - src: "main.cpp"
    dest: "lib/main.cpp"
  - src: "fern.yaml"
    dest: "fern.yaml"
  - src: "README.md"
    dest: "README.md"
  - src: "template.html"
    dest: "web/template.html"

variables:
  - name: "project_name"
    description: "Project name"
    type: "string"
    required: true
  - name: "author"
    description: "Author name"
    type: "string"
    default: "Unknown"
EOF
    
    log_success "Project templates set up"
}

# Test installation
test_installation() {
    log_info "Testing Terra CLI installation..."
    
    if command -v fern &> /dev/null; then
        log_success "✅ 'fern' command is available"
        
        # Test basic functionality
        if fern --version &> /dev/null; then
            log_success "✅ Terra CLI is working correctly"
        else
            log_warning "⚠️  Terra CLI installed but may have issues"
        fi
        
        if command -v terra &> /dev/null; then
            log_success "✅ 'terra' command alias is available"
        fi
    else
        log_error "❌ Terra CLI installation failed"
        echo "Please check the installation logs above"
        exit 1
    fi
}

# Show post-installation instructions
show_instructions() {
    echo ""
    log_header "🎉 Terra CLI Installation Complete!"
    echo ""
    echo "You can now use Terra CLI with the following commands:"
    echo ""
    echo "  fern --help        # Show help"
    echo "  fern --version     # Show version"
    echo "  fern bloom         # Check system health"
    echo "  fern sprout <name> # Create new project"
    echo "  fern fire          # Build and run project"
    echo ""
    echo "To get started with Fern UI Framework:"
    echo ""
    echo "  1. Install the Fern framework:"
    echo "     git clone https://github.com/fernkit/fern.git"
    echo "     cd fern && ./install.sh"
    echo ""
    echo "  2. Create your first project:"
    echo "     fern sprout my_awesome_app"
    echo ""
    echo "  3. Start developing:"
    echo "     cd my_awesome_app"
    echo "     fern fire"
    echo ""
    echo "For more information, visit:"
    echo "  • Terra CLI: https://github.com/fernkit/terra"
    echo "  • Fern Framework: https://github.com/fernkit/fern"
    echo ""
    log_success "Happy coding with Terra CLI! 🌿"
}

# Main installation function
main() {
    show_banner
    
    check_root
    check_python
    install_python_deps
    install_terra_cli
    setup_path
    create_config
    setup_templates
    test_installation
    show_instructions
}

# Run main function
main "$@"
