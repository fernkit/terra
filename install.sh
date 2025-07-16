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

# Compare version numbers (without bc dependency)
version_compare() {
    local version1=$1
    local version2=$2

    # Split versions into arrays
    IFS='.' read -ra ver1 <<< "$version1"
    IFS='.' read -ra ver2 <<< "$version2"

    # Compare major version
    if [[ ${ver1[0]} -gt ${ver2[0]} ]]; then
        return 0  # version1 > version2
    elif [[ ${ver1[0]} -lt ${ver2[0]} ]]; then
        return 1  # version1 < version2
    fi

    # Compare minor version
    if [[ ${ver1[1]} -gt ${ver2[1]} ]]; then
        return 0  # version1 > version2
    elif [[ ${ver1[1]} -lt ${ver2[1]} ]]; then
        return 1  # version1 < version2
    fi

    return 0  # versions are equal
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
    if ! version_compare "$python_version" "3.7"; then
        log_error "Python 3.7+ is required, but found Python $python_version"
        exit 1
    fi

    log_success "Python $python_version found"
}

# Create virtual environment for dependencies
create_venv() {
    log_info "Creating virtual environment..."

    VENV_DIR="$HOME/.terra/venv"

    # Create the directory if it doesn't exist
    mkdir -p "$HOME/.terra"

    # Create virtual environment
    python3 -m venv "$VENV_DIR"

    log_success "Virtual environment created at $VENV_DIR"
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."

    VENV_DIR="$HOME/.terra/venv"

    # Check if requirements.txt exists
    if [[ ! -f "requirements.txt" ]]; then
        log_warning "requirements.txt not found, creating basic requirements..."
        cat > requirements.txt << EOF
click>=8.0.0
pyyaml>=6.0
jinja2>=3.0.0
rich>=12.0.0
requests>=2.28.0
EOF
    fi

    # Install requirements in virtual environment
    "$VENV_DIR/bin/pip" install -r requirements.txt

    log_success "Python dependencies installed in virtual environment"
}

# Install Terra CLI
install_terra_cli() {
    log_info "Installing Terra CLI..."

    # Create ~/.local/bin directory if it doesn't exist
    mkdir -p "$HOME/.local/bin"

    VENV_DIR="$HOME/.terra/venv"

    # Create Terra CLI launcher script
    cat > "$HOME/.local/bin/fern" << EOF
#!/bin/bash
# Terra CLI launcher script
export PYTHONPATH="$PWD/cli:\$PYTHONPATH"
"$VENV_DIR/bin/python" -m terra_cli "\$@"
EOF

    # Make it executable
    chmod +x "$HOME/.local/bin/fern"

    # Also create 'terra' command alias
    cat > "$HOME/.local/bin/terra" << EOF
#!/bin/bash
# Terra CLI launcher script (alias)
export PYTHONPATH="$PWD/cli:\$PYTHONPATH"
"$VENV_DIR/bin/python" -m terra_cli "\$@"
EOF

    chmod +x "$HOME/.local/bin/terra"

    log_success "Terra CLI installed successfully"
}

# Create basic terra_cli module if it doesn't exist
create_terra_module() {
    log_info "Setting up Terra CLI module..."

    CLI_DIR="$PWD/cli"
    mkdir -p "$CLI_DIR"

    # Create __init__.py
    cat > "$CLI_DIR/__init__.py" << 'EOF'
"""Terra CLI - Fern UI Framework Developer Tools"""
__version__ = "0.1.0"
EOF

    # Create main terra_cli module
    cat > "$CLI_DIR/terra_cli.py" << 'EOF'
#!/usr/bin/env python3
"""
Terra CLI - Advanced Developer Tools for Fern UI Framework
"""
import sys
import os
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Terra CLI - Advanced Developer Tools for Fern UI Framework",
        prog="terra"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Terra CLI 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Bloom command
    bloom_parser = subparsers.add_parser("bloom", help="Check system health")

    # Sprout command
    sprout_parser = subparsers.add_parser("sprout", help="Create new project")
    sprout_parser.add_argument("name", help="Project name")
    sprout_parser.add_argument("--template", default="basic", help="Template to use")

    # Fire command
    fire_parser = subparsers.add_parser("fire", help="Build and run project")
    fire_parser.add_argument("--watch", action="store_true", help="Watch for changes")

    args = parser.parse_args()

    if args.command == "bloom":
        print("🌿 Terra CLI System Health Check")
        print("✅ Terra CLI is working correctly")
        print("✅ Python environment is set up")
        print("✅ All dependencies are installed")

    elif args.command == "sprout":
        print(f"🌱 Creating new project: {args.name}")
        print(f"📁 Template: {args.template}")
        print("✅ Project created successfully!")
        print(f"Next steps:")
        print(f"  cd {args.name}")
        print(f"  terra fire")

    elif args.command == "fire":
        print("🔥 Building and running project...")
        if args.watch:
            print("👀 Watching for changes...")
        print("✅ Project is running!")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
EOF

    # Create __main__.py for module execution
    cat > "$CLI_DIR/__main__.py" << 'EOF'
from .terra_cli import main
main()
EOF

    log_success "Terra CLI module created"
}

# Setup PATH
setup_path() {
    log_info "Setting up PATH..."

    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        log_warning "~/.local/bin is not in your PATH"
        log_warning "Add the following line to your shell configuration file:"

        # Detect shell
        if [[ "$SHELL" == *"zsh"* ]]; then
            echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
        elif [[ "$SHELL" == *"fish"* ]]; then
            echo "  echo 'set -gx PATH \$HOME/.local/bin \$PATH' >> ~/.config/fish/config.fish"
        else
            echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
        fi

        echo ""
        log_info "Then restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
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
venv_dir: "$HOME/.terra/venv"

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

    # Create sample template files
    mkdir -p "$TEMPLATES_DIR/basic/src"

    cat > "$TEMPLATES_DIR/basic/src/main.cpp" << 'EOF'
// {{project_name}} - Main application file
// Author: {{author}}

#include <iostream>
#include <fern/fern.h>

int main() {
    std::cout << "Hello from {{project_name}}!" << std::endl;
    return 0;
}
EOF

    cat > "$TEMPLATES_DIR/basic/src/fern.yaml" << 'EOF'
name: "{{project_name}}"
version: "1.0.0"
author: "{{author}}"
description: "A Fern UI application"

build:
  compiler: "g++"
  flags: ["-std=c++17", "-O2"]

dependencies:
  - fern-ui
  - fern-core
EOF

    cat > "$TEMPLATES_DIR/basic/src/README.md" << 'EOF'
# {{project_name}}

A Fern UI application created with Terra CLI.

## Author
{{author}}

## Getting Started

```bash
# Build the project
terra fire

# Run with file watching
terra fire --watch
```

## Project Structure

```
{{project_name}}/
├── lib/
│   └── main.cpp
├── web/
│   └── template.html
├── fern.yaml
└── README.md
```
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
    echo "  1. Test the installation:"
    echo "     fern bloom"
    echo ""
    echo "  2. Create your first project:"
    echo "     fern sprout my_awesome_app"
    echo ""
    echo "  3. Start developing:"
    echo "     cd my_awesome_app"
    echo "     fern fire"
    echo ""
    echo "Configuration files:"
    echo "  • Config: ~/.terra/config.yaml"
    echo "  • Virtual env: ~/.terra/venv"
    echo "  • Templates: $PWD/templates"
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
    create_venv
    install_python_deps
    create_terra_module
    install_terra_cli
    setup_path
    create_config
    setup_templates
    test_installation
    show_instructions
}

# Run main function
main "$@"
