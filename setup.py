#!/usr/bin/env python3
"""
Terra CLI Setup Script
Installation script for Terra CLI - Fern UI Framework Developer Tools
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="terra-cli",
    version="0.1.0",
    description="Terra CLI - Advanced developer tools for Fern UI Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rishi Ahuja",
    author_email="team@fern-ui.dev",
    url="https://github.com/fernkit/terra",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyYAML>=5.4.1",
        "colorama>=0.4.4",
        "requests>=2.25.1",
        "click>=8.0.0",
        "jinja2>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=8.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fern=cli.terra_cli:main",
            "terra=cli.terra_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.7",
    keywords="fern ui framework cli development tools terra",
    project_urls={
        "Bug Reports": "https://github.com/fernkit/terra/issues",
        "Source": "https://github.com/fernkit/terra",
        "Documentation": "https://fernkit.in/docs/terra",
        "Fern Framework": "https://github.com/fernkit/fern",
    },
)
