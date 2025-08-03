# Terra CLI

<p align="center">
  <img src="assets/logo.png" alt="Terra CLI logo" width="200"/>
</p>

**Advanced Developer Tools for Fern UI Framework**

Terra is the command-line interface that orchestrates Fern UI Framework development with powerful, intuitive commands. Think of it as the conductor of your Fern development orchestra.

## Features

- **Project Creation**: `fern sprout` - Create new Fern projects with customizable templates
- **Build & Run**: `fern fire` - Build and run projects for multiple platforms (Linux, Web)
- **Health Check**: `fern bloom` - Verify system dependencies and configuration
- **Project Preparation**: `fern prepare` - Prepare projects for deployment
- **Template Management**: `fern templates` - Manage and create project templates
- **Web Cache Management**: `fern web-cache` - Optimize web build performance
- **Cross-Platform**: Native Linux applications and WebAssembly for web
- **Live Reload**: Real-time development feedback with hot reloading

## Performance Features

- **Fast Web Builds**: Precompiled library caching reduces web build time from 60s to 3s
- **Intelligent Caching**: Automatic cache invalidation when source files change
- **Port Management**: Automatic port resolution and graceful server shutdown
- **Global Installation**: Source files installed globally for seamless web builds

## Quick Start

### Installation

```bash
# Clone the Fern framework repository
git clone https://github.com/fernkit/fern.git
cd fern

# Install Terra CLI and Fern framework
./install.sh
```

This will:
- Build and install the Fern C++ library globally
- Set up the Terra CLI in your PATH
- Install source files for web compilation
- Configure your shell environment

### Your First Fern App

```bash
# Check system health
fern bloom

# Create a new project
fern sprout my_awesome_app

# Enter project directory
cd my_awesome_app

# Run your app (Linux)
fern fire

# Run for web platform (optimized with caching!)
fern fire -p web
```

## Commands Reference

### `fern bloom` - System Health Check
Verifies that all dependencies are installed and configured correctly.

```bash
fern bloom
```

**What it checks:**
- Python 3 installation
- C++ compiler (g++, clang++ optional)
- CMake build system
- Fern C++ library installation
- System dependencies (X11, fontconfig, freetype)
- Emscripten (for web builds)
- Global source installation

**Sample Output:**
```
🌿 Fern Health Check
===================
✓ Python 3.12.0 - Available
✓ g++ (Ubuntu 11.4.0) - Available
✓ CMake 3.22.1 - Available
✓ pkg-config - Available
✓ Fern C++ library - Installed (/usr/local/lib/libfern.a)
⚠ clang++ - Not found (optional)
✓ Emscripten 3.1.45 - Available
✓ Global source files - Installed (~/.fern/src)

Your system is ready for Fern development!
```

### `fern sprout <project_name>` - Create New Project
Creates a new Fern project with the specified name using templates.

```bash
fern sprout my_project
fern sprout --template advanced my_complex_app
```

**Project structure created:**
```
my_project/
├── lib/                   # Main source code
│   └── main.cpp          # Entry point with Fern UI code
├── web/                  # Web platform customization
│   └── template.html     # Custom HTML template
├── linux/                # Linux platform files
├── assets/               # Images, fonts, resources
│   └── fonts/           # TTF font files
├── examples/             # Example code and tutorials
├── fern.yaml            # Project configuration
└── README.md            # Project documentation
```

**Project Configuration (`fern.yaml`):**
```yaml
name: test
version: 1.0.0
description: A new Fern project

dependencies:
  fern: ^0.1.0

platforms:
  web:
    enabled: true
    port: 8000
  linux:
    enabled: true
    
build:
  incremental: true
  optimize: false
```

### `fern fire [options]` - Build and Run
Builds and runs your Fern project with optimized compilation.

```bash
# Run for Linux (default)
fern fire

# Run for web platform (uses cached compilation!)
fern fire -p web
fern fire --platform web

# Run specific file
fern fire main.cpp
fern fire -p web examples/button_demo.cpp
```

**Options:**
- `-p, --platform <platform>` - Target platform (linux, web)
- `-h, --help` - Show help

**Web Build Performance:**
- **First build**: ~45-60 seconds (builds cache)
- **Subsequent builds**: ~2-5 seconds (uses cache)
- **After source changes**: ~45-60 seconds (rebuilds cache automatically)

**Sample Output:**
```
🌿 Running main.cpp (web)
=========================
ℹ Building single file for web...
ℹ Found Fern source for web build at: /home/user/.fern/src/cpp
ℹ Using cached Fern web library
ℹ Compiling for web...
✓ Build successful!
ℹ Starting local web server...
✓ 🔥 Fern Fire started (web)!

ℹ Open your browser to: http://localhost:8000/main_temp.html
ℹ Press Ctrl+C to stop the server
```

### `fern web-cache [action]` - Web Cache Management
Manage the precompiled web library cache for faster builds.

```bash
# Check cache status
fern web-cache status

# Clear cache (will rebuild automatically)
fern web-cache clear

# Force rebuild cache
fern web-cache rebuild
```

**Cache Status Output:**
```
🌿 Fern Web Cache Status
========================
✓ Web cache is available
ℹ Cache location: /home/user/.fern/cache/web
ℹ Library file: libfern_web.a
ℹ Size: 0.4 MB
ℹ Last modified: 2025-08-03 15:45:32
ℹ Source location: /home/user/.fern/src/cpp
✓ Cache is up to date
```

### `fern prepare <platform>` - Prepare for Deployment
Prepares your project for deployment to the specified platform.

```bash
fern prepare web      # Creates optimized web build
fern prepare linux    # Creates distribution-ready Linux build
```

### `fern templates` - Template Management
Manage project templates for different use cases.

```bash
fern templates list              # Show available templates
fern templates create my_template # Create custom template
fern templates install <name>    # Install community template
```

### `fern lsp` - Language Server Protocol
Manage VS Code integration and language server features.

```bash
fern lsp start        # Start LSP server
fern lsp config       # Configure VS Code integration
fern lsp stop         # Stop LSP server
```

## Platform Support

### Linux (Native)
- **Technology**: X11/Wayland with OpenGL rendering
- **Features**: Native performance, system integration, window management
- **Build**: Uses g++/clang++ with CMake
- **Output**: Native executable with dynamic linking
- **Performance**: 60+ FPS, minimal memory usage

### Web (WebAssembly)
- **Technology**: Emscripten + WebAssembly + WebGL
- **Features**: Runs in any modern browser, responsive design
- **Build**: Uses emcc compiler with optimized caching
- **Output**: HTML + WASM + JS files
- **Performance**: Near-native speed in browsers


## Web Template Customization

Terra creates highly customizable HTML templates for web builds:

### Basic Template (`web/template.html`)
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{APP_NAME}} - Powered by Fern UI</title>
    
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        
        .header {
            color: white;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .app-container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        #canvas {
            border-radius: 10px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }
        
        .loading {
            color: white;
            font-size: 18px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌿 {{APP_NAME}}</h1>
        <p>Built with Fern UI Framework</p>
    </div>
    
    <div class="app-container">
        <div id="loading" class="loading">Loading...</div>
        <canvas id="canvas" style="display: none;"></canvas>
    </div>
    
    <script>
        var Module = {
            canvas: document.getElementById('canvas'),
            preRun: [],
            postRun: [function() {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('canvas').style.display = 'block';
                console.log('🌿 Fern app initialized successfully!');
            }],
            print: function(text) {
                console.log('[Fern]', text);
            },
            printErr: function(text) {
                console.error('[Fern Error]', text);
            }
        };
    </script>
    {{{ SCRIPT }}}
</body>
</html>
```


## Development Workflow

### Standard Development Process
1. **Create Project**: `fern sprout my_app`
2. **Health Check**: `fern bloom`
3. **Develop**: Edit `lib/main.cpp` with your favorite editor
4. **Test Linux**: `fern fire` (instant feedback)
5. **Test Web**: `fern fire -p web` (cached builds!)
6. **Customize**: Edit `web/template.html` for web styling
7. **Deploy**: `fern prepare web` for production

### Hot Development Tips
- **Fast Iteration**: Web builds use aggressive caching for 10x speed improvement
- **Multi-Platform**: Test both platforms quickly with single commands
- **Live Reload**: Changes reflect immediately in both platforms
- **Debug Mode**: Use `fern fire --debug` for enhanced debugging
- **Port Management**: Multiple projects can run simultaneously

### Performance Monitoring
```bash
# Check web cache performance
fern web-cache status

# Monitor build times
time fern fire -p web main.cpp

# Clear cache when needed
fern web-cache clear
```

## Integration with Development Tools

### VS Code Integration
```bash
# Configure VS Code for Fern development
fern lsp config

# Auto-completion, syntax highlighting, and debugging
# IntelliSense for Fern UI components
# Integrated terminal with Terra CLI
```

### Git Integration
```gitignore
# .gitignore for Fern projects
build/
*.o
*.a
*_temp.html
*_temp.js
*_temp.wasm
.vscode/settings.json
node_modules/
```

## Performance & Optimization

### Web Build Optimization Details
The Terra CLI implements sophisticated caching mechanisms:

**Before Optimization:**
- Every web build: 45-60 seconds
- Compiled entire Fern library every time
- No incremental builds
- Poor developer experience

**After Optimization:**
- First build: 45-60 seconds (creates cache)
- Subsequent builds: 2-5 seconds (uses cache)
- Automatic cache invalidation
- 15x faster development cycle

**Technical Implementation:**
```bash
# Cache location
~/.fern/cache/web/libfern_web.a

# Cache management
- Timestamp-based invalidation
- Individual source file compilation
- Static library creation with emar
- Intelligent source detection
```

## Troubleshooting

### Common Issues & Solutions

#### **Terra CLI not found**
```bash
# Check installation
which fern

# Add to PATH manually
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Restart terminal
source ~/.bashrc
```

#### **Build errors on Linux**
```bash
# Check dependencies
fern bloom

# Install missing packages (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install build-essential cmake pkg-config \
    libx11-dev libxext-dev libfontconfig1-dev libfreetype6-dev

# Install missing packages (Fedora/RHEL)
sudo dnf groupinstall "Development Tools"
sudo dnf install cmake pkg-config libX11-devel fontconfig-devel freetype-devel
```

#### **Web builds fail**
```bash
# Install Emscripten
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk
./emsdk install latest
./emsdk activate latest
source ./emsdk_env.sh

# Add to shell profile
echo 'source /path/to/emsdk/emsdk_env.sh' >> ~/.bashrc
```

#### **Slow web builds**
```bash
# Check cache status
fern web-cache status

# Clear and rebuild cache
fern web-cache clear
fern fire -p web examples/basic.cpp  # This will rebuild cache
```

#### **Port conflicts**
```bash
# Terra automatically finds available ports
# If port 8000 is busy, it tries 8001, 8002, etc.

# Or specify custom port in fern.yaml:
platforms:
  web:
    port: 3000
```

#### **Missing source files for web builds**
```bash
# Reinstall with source files
cd /path/to/fern/repository
./install.sh

# Verify installation
fern bloom
```

### Debug Mode
```bash
# Enable verbose output
export FERN_DEBUG=1
fern fire -p web main.cpp

# Check detailed logs
tail -f ~/.fern/logs/terra.log
```

## Contributing to Terra CLI

### Development Setup
```bash
# Clone repository
git clone https://github.com/fernkit/fern.git
cd fern

# Install in development mode
./install.sh --dev

# Run tests
python3 -m pytest cli/tests/

# Code formatting
black cli/
isort cli/
```

### Adding New Commands
```python
# cli/commands/my_command.py
class MyCommand:
    def execute(self, args):
        print_header("My Custom Command")
        # Implementation here

# Register in cli/terra_cli.py
from commands.my_command import MyCommand

self.commands['my-command'] = MyCommand()
```

### Testing
```bash
# Unit tests
python3 -m pytest cli/tests/test_commands.py

# Integration tests
python3 -m pytest cli/tests/test_integration.py

# Performance tests
python3 cli/tests/benchmark_builds.py
```

## License

MIT License - see [LICENSE](LICENSE) file for details.


<p align="center">
  <strong>Terra CLI - Powering the Future of Fern UI Development</strong><br>
</p>
