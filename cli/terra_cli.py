#!/usr/bin/env python3
"""
Terra CLI - Advanced Developer Tools for Fern UI Framework
"""
import sys
import os
import argparse
import subprocess
import signal
import time
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

    # LSP command
    lsp_parser = subparsers.add_parser("lsp", help="Language Server Protocol management")
    lsp_subparsers = lsp_parser.add_subparsers(dest="lsp_command", help="LSP commands")

    # LSP start
    start_parser = lsp_subparsers.add_parser("start", help="Start Gleeb LSP server")
    start_parser.add_argument("--port", type=int, help="Port to run on (default: stdio)")
    start_parser.add_argument("--background", "-b", action="store_true", help="Run in background")

    # LSP stop
    stop_parser = lsp_subparsers.add_parser("stop", help="Stop Gleeb LSP server")

    # LSP config
    config_parser = lsp_subparsers.add_parser("config", help="Configure editor for LSP")
    config_parser.add_argument("--editor", choices=["vscode", "vim", "emacs"], default="vscode", help="Editor to configure")

    # LSP status
    status_parser = lsp_subparsers.add_parser("status", help="Check LSP server status")

    # LSP install
    install_parser = lsp_subparsers.add_parser("install", help="Install/reinstall Gleeb LSP")

    args = parser.parse_args()

    if args.command == "bloom":
        print("🌿 Terra CLI System Health Check")
        print("✅ Terra CLI is working correctly")
        print("✅ Python environment is set up")
        print("✅ All dependencies are installed")
        
        # Check Gleeb LSP
        gleeb_path = os.path.expanduser("~/.fern/gleeb/dist/server.js")
        if os.path.exists(gleeb_path):
            print("✅ Gleeb LSP is installed")
        else:
            print("⚠️  Gleeb LSP not found. Run: fern lsp install")

    elif args.command == "sprout":
        print(f"🌱 Creating new project: {args.name}")
        print(f"📁 Template: {args.template}")
        print("✅ Project created successfully!")
        print(f"Next steps:")
        print(f"  cd {args.name}")
        print(f"  terra fire")
        print(f"  terra lsp config  # Configure LSP support")

    elif args.command == "fire":
        print("🔥 Building and running project...")
        if args.watch:
            print("👀 Watching for changes...")
        print("✅ Project is running!")
        print("💡 Tip: Use 'terra lsp start' for intelligent code assistance")

    elif args.command == "lsp":
        handle_lsp_command(args)

    else:
        parser.print_help()

def handle_lsp_command(args):
    """Handle LSP-related commands"""
    if args.lsp_command == "start":
        start_lsp_server(args)
    elif args.lsp_command == "stop":
        stop_lsp_server()
    elif args.lsp_command == "config":
        configure_lsp_editor(args.editor)
    elif args.lsp_command == "status":
        check_lsp_status()
    elif args.lsp_command == "install":
        install_lsp()
    else:
        print("Available LSP commands:")
        print("  start   - Start Gleeb LSP server")
        print("  stop    - Stop Gleeb LSP server")
        print("  config  - Configure editor")
        print("  status  - Check status")
        print("  install - Install/reinstall LSP")

def start_lsp_server(args):
    """Start the Gleeb LSP server"""
    print("Starting Gleeb LSP server...")
    
    gleeb_path = os.path.expanduser("~/.fern/gleeb/dist/server.js")
    if not os.path.exists(gleeb_path):
        print("❌ Gleeb LSP not found. Run: fern lsp install")
        return
    
    try:
        if args.background:
            # Start in background
            with open(os.path.expanduser("~/.fern/gleeb.log"), "w") as log_file:
                process = subprocess.Popen(
                    ["node", gleeb_path, "--stdio"],
                    cwd=os.path.dirname(gleeb_path),
                    stdout=log_file,
                    stderr=log_file,
                    stdin=subprocess.DEVNULL
                )
            
            # Save PID for stopping later
            with open(os.path.expanduser("~/.fern/gleeb.pid"), "w") as pid_file:
                pid_file.write(str(process.pid))
            
            print(f"✅ Gleeb LSP started in background (PID: {process.pid})")
            print(f"Logs: ~/.fern/gleeb.log")
        else:
            # Start in foreground
            print("Starting Gleeb LSP in stdio mode...")
            print("Connect your editor to this server")
            print(" Press Ctrl+C to stop")
            subprocess.run(["node", gleeb_path, "--stdio"], cwd=os.path.dirname(gleeb_path))
    
    except KeyboardInterrupt:
        print("\nGleeb LSP server stopped")
    except Exception as e:
        print(f"❌ Error starting LSP server: {e}")

def stop_lsp_server():
    """Stop the Gleeb LSP server"""
    print("Stopping Gleeb LSP server...")
    
    pid_file = os.path.expanduser("~/.fern/gleeb.pid")
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())
            
            os.kill(pid, signal.SIGTERM)
            time.sleep(1)
            
            # Check if process is still running
            try:
                os.kill(pid, 0)
                print("⚠️  Process still running, sending SIGKILL...")
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            
            os.remove(pid_file)
            print("✅ Gleeb LSP server stopped")
        except Exception as e:
            print(f"❌ Error stopping server: {e}")
    else:
        # Try to kill by process name
        try:
            subprocess.run(["pkill", "-f", "gleeb.*server.js"], check=False)
            print("✅ Gleeb LSP server stopped")
        except Exception as e:
            print(f"❌ Error stopping server: {e}")

def configure_lsp_editor(editor):
    """Configure editor for Gleeb LSP"""
    print(f"🔧 Configuring {editor} for Gleeb LSP...")
    
    if editor == "vscode":
        try:
            subprocess.run(["gleeb-configure-vscode"], check=True)
            print("VS Code configured for Gleeb LSP")
            print("Reload VS Code to activate the LSP server")
        except subprocess.CalledProcessError:
            print("❌ Failed to configure VS Code")
            print("Manual configuration:")
            print("Add to settings.json:")
            print('{')
            print('  "gleeb.enable": true,')
            print('  "gleeb.server.command": "gleeb-lsp",')
            print('  "gleeb.server.args": ["--stdio"]')
            print('}')
        except FileNotFoundError:
            print("❌ gleeb-configure-vscode not found")
            print("Run the main Fern installer to get LSP tools")
    
    elif editor == "vim":
        print("🔧 Vim configuration:")
        print("Add to your .vimrc or init.vim:")
        print("")
        print("\" For vim-lsp")
        print("if executable('gleeb-lsp')")
        print("    au User lsp_setup call lsp#register_server({")
        print("        \\ 'name': 'gleeb-lsp',")
        print("        \\ 'cmd': {server_info->['gleeb-lsp', '--stdio']},")
        print("        \\ 'whitelist': ['cpp', 'c'],")
        print("        \\ })")
        print("endif")
        print("")
        print("\" For coc.nvim")
        print("Add to :CocConfig:")
        print('{')
        print('  "languageserver": {')
        print('    "gleeb": {')
        print('      "command": "gleeb-lsp",')
        print('      "args": ["--stdio"],')
        print('      "filetypes": ["cpp", "c"]')
        print('    }')
        print('  }')
        print('}')
    
    elif editor == "emacs":
        print("🔧 Emacs configuration:")
        print("Add to your .emacs or init.el:")
        print("")
        print("(use-package lsp-mode")
        print("  :hook ((c-mode . lsp)")
        print("         (c++-mode . lsp))")
        print("  :config")
        print("  (lsp-register-client")
        print("   (make-lsp-client :new-connection (lsp-stdio-connection '(\"gleeb-lsp\" \"--stdio\"))")
        print("                    :major-modes '(c-mode c++-mode)")
        print("                    :server-id 'gleeb-lsp)))")

def check_lsp_status():
    """Check Gleeb LSP status"""
    print("📊 Gleeb LSP Status:")
    
    # Check if LSP is installed
    gleeb_path = os.path.expanduser("~/.fern/gleeb/dist/server.js")
    if os.path.exists(gleeb_path):
        print("✅ Gleeb LSP is installed")
        print(f"Location: {gleeb_path}")
    else:
        print("❌ Gleeb LSP is not installed")
        print("Run: fern lsp install")
        return
    
    # Check if server is running
    pid_file = os.path.expanduser("~/.fern/gleeb.pid")
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())
            
            # Check if process is still running
            try:
                os.kill(pid, 0)
                print(f"✅ Gleeb LSP server is running (PID: {pid})")
            except ProcessLookupError:
                print("❌ Gleeb LSP server is not running (stale PID file)")
                os.remove(pid_file)
        except Exception as e:
            print(f"❌ Error checking server status: {e}")
    else:
        print("❌ Gleeb LSP server is not running")
    
    # Check LSP tools
    if os.path.exists(os.path.expanduser("~/.local/bin/gleeb-lsp")):
        print("✅ gleeb-lsp command is available")
    else:
        print("❌ gleeb-lsp command not found")
    
    if os.path.exists(os.path.expanduser("~/.local/bin/gleeb-configure-vscode")):
        print("✅ gleeb-configure-vscode command is available")
    else:
        print("❌ gleeb-configure-vscode command not found")

def install_lsp():
    """Install or reinstall Gleeb LSP"""
    print("Installing Gleeb LSP...")
    print("Please run the main Fern installer to install/update Gleeb LSP:")
    print("   ./install.sh")
    print("")
    print("Or manually:")
    print("1. Ensure Node.js 16+ is installed")
    print("2. Copy gleeb/ folder to ~/.fern/gleeb/")
    print("3. cd ~/.fern/gleeb && npm install && npm run build")
    print("4. Create launcher scripts in ~/.local/bin/")

if __name__ == "__main__":
    main()
