"""
Template management utilities for Terra CLI
"""

import os
import shutil
import yaml
from pathlib import Path
from typing import List, Dict, Optional

from .colors import print_info, print_success, print_error, print_warning

class TemplateManager:
    """Manages Fern project templates"""
    
    def __init__(self):
        self.templates_dir = Path.home() / ".fern" / "templates"
        self.flare_templates_dir = Path.home() / ".fern" / "flare" / "templates"
        self.builtin_templates = {
            "basic": "Basic Fern application",
            "game": "Game development template",
            "dashboard": "Dashboard/admin template",
            "mobile": "Mobile-style UI template"
        }
    
    def get_available_templates(self) -> Dict[str, str]:
        """Get list of available templates"""
        templates = {}
        
        # Add builtin templates
        templates.update(self.builtin_templates)
        
        # Add templates from ~/.fern/templates
        if self.templates_dir.exists():
            for template_dir in self.templates_dir.iterdir():
                if template_dir.is_dir():
                    templates[template_dir.name] = self._get_template_description(template_dir)
        
        # Add Flare templates
        if self.flare_templates_dir.exists():
            for template_dir in self.flare_templates_dir.iterdir():
                if template_dir.is_dir():
                    template_name = f"flare/{template_dir.name}"
                    templates[template_name] = self._get_template_description(template_dir)
        
        return templates
    
    def get_installed_templates(self) -> List[str]:
        """Get list of installed templates"""
        templates = []
        
        if self.templates_dir.exists():
            for template_dir in self.templates_dir.iterdir():
                if template_dir.is_dir():
                    templates.append(template_dir.name)
        
        return templates
    
    def template_exists(self, template_name: str) -> bool:
        """Check if a template exists"""
        if template_name in self.builtin_templates:
            return True
        
        # Check in ~/.fern/templates
        template_path = self.templates_dir / template_name
        if template_path.exists():
            return True
        
        # Check in Flare templates
        if template_name.startswith("flare/"):
            flare_template_name = template_name[6:]  # Remove "flare/" prefix
            flare_template_path = self.flare_templates_dir / flare_template_name
            return flare_template_path.exists()
        
        return False
    
    def get_template_path(self, template_name: str) -> Optional[Path]:
        """Get the path to a template"""
        if template_name in self.builtin_templates:
            # Return path to builtin template (we'll handle this in the sprout command)
            return None
        
        # Check in ~/.fern/templates
        template_path = self.templates_dir / template_name
        if template_path.exists():
            return template_path
        
        # Check in Flare templates
        if template_name.startswith("flare/"):
            flare_template_name = template_name[6:]  # Remove "flare/" prefix
            flare_template_path = self.flare_templates_dir / flare_template_name
            if flare_template_path.exists():
                return flare_template_path
        
        return None
    
    def create_template(self, template_name: str, source_path: Path) -> bool:
        """Create a new template from a source project"""
        try:
            template_path = self.templates_dir / template_name
            
            # Create templates directory if it doesn't exist
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy source to template directory
            shutil.copytree(source_path, template_path)
            
            # Create template metadata
            self._create_template_metadata(template_path, template_name)
            
            print_success(f"Template '{template_name}' created successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to create template: {e}")
            return False
    
    def install_template(self, template_name: str, template_url: str) -> bool:
        """Install a template from a URL or path"""
        try:
            import subprocess
            
            template_path = self.templates_dir / template_name
            
            # Create templates directory if it doesn't exist
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            
            # Clone or copy template
            if template_url.startswith(('http://', 'https://', 'git@')):
                # Git clone
                subprocess.run(['git', 'clone', template_url, str(template_path)], 
                             check=True, capture_output=True)
            else:
                # Local path
                shutil.copytree(template_url, template_path)
            
            print_success(f"Template '{template_name}' installed successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to install template: {e}")
            return False
    
    def remove_template(self, template_name: str) -> bool:
        """Remove a template"""
        try:
            template_path = self.templates_dir / template_name
            
            if not template_path.exists():
                print_error(f"Template '{template_name}' not found")
                return False
            
            if template_name in self.builtin_templates:
                print_error(f"Cannot remove builtin template '{template_name}'")
                return False
            
            shutil.rmtree(template_path)
            print_success(f"Template '{template_name}' removed successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to remove template: {e}")
            return False
    
    def _get_template_description(self, template_path: Path) -> str:
        """Get template description from metadata"""
        try:
            # Check for template.yaml
            yaml_path = template_path / "template.yaml"
            if yaml_path.exists():
                with open(yaml_path, 'r') as f:
                    data = yaml.safe_load(f)
                    return data.get('description', 'Custom template')
            
            # Check for README.md
            readme_path = template_path / "README.md"
            if readme_path.exists():
                with open(readme_path, 'r') as f:
                    # Get first line as description
                    first_line = f.readline().strip()
                    if first_line.startswith('# '):
                        return first_line[2:]
                    return first_line
            
            return "Custom template"
            
        except Exception:
            return "Custom template"
    
    def _create_template_metadata(self, template_path: Path, template_name: str):
        """Create template metadata file"""
        metadata = {
            'name': template_name,
            'description': f"Custom template: {template_name}",
            'version': '1.0.0',
            'author': 'User',
            'files': {
                'main': 'lib/main.cpp',
                'config': 'fern.yaml'
            }
        }
        
        with open(template_path / "template.yaml", 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False)
