#!/usr/bin/env python3
"""
utils/markdown_display.py - Markdown Display Utilities

This module provides utilities for displaying markdown-formatted content
in various formats for better user experience.
"""

import os
from datetime import datetime
from typing import Optional

def save_markdown_result(content: str, filename: str, title: str = "CrewAI Result") -> str:
    """
    Save markdown content to a file with proper formatting
    
    Args:
        content: The markdown content to save
        filename: Output filename (will be created in current directory)
        title: Title for the markdown document
    
    Returns:
        Path to the created file
    """
    # Ensure .md extension
    if not filename.endswith('.md'):
        filename += '.md'
    
    # Create full file path
    filepath = os.path.join(os.getcwd(), filename)
    
    # Write markdown content with header
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(str(content))
    
    return filepath

def display_markdown_options(content: str, filename: str = "crew_output.md", 
                           title: str = "CrewAI Result", show_console: bool = True) -> None:
    """
    Display markdown content with multiple output options
    
    Args:
        content: The markdown content to display
        filename: Output filename
        title: Title for the document
        show_console: Whether to show content in console
    """
    # Save to file
    filepath = save_markdown_result(content, filename, title)
    
    # Console output
    if show_console:
        print(f"\n📄 {title}:")
        print("=" * 50)
        print(content)
        print(f"\n💾 Result saved to: {filepath}")
        print("📖 Open the file in a markdown viewer for better formatting!")
        print("💡 Tip: VS Code preview, GitHub, or any markdown app will render it beautifully")
    else:
        print(f"💾 Result saved to: {filepath}")
        print("📖 Open the file in a markdown viewer for formatted output")

