#!/usr/bin/env python3
"""
Installation script to create desktop shortcut for Wire Checker
Run this script once to set up the desktop shortcut
"""

import os
import sys
import shutil
from pathlib import Path

def create_launcher_script():
    """Create the launcher script"""
    launcher_content = '''#!/bin/bash

# Wire Checker Launcher Script
# This script launches the wire checker application

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if required files exist
if [ ! -f "wire_checker_main.py" ]; then
    echo "Error: wire_checker_main.py not found in $SCRIPT_DIR"
    exit 1
fi

# Launch the wire checker main application
echo "Starting Wire Checker System..."
python3 wire_checker_main.py
'''
    
    with open('wire_checker_launcher.sh', 'w') as f:
        f.write(launcher_content)
    
    # Make the launcher script executable
    os.chmod('wire_checker_launcher.sh', 0o755)
    print("✓ Launcher script created: wire_checker_launcher.sh")

def create_desktop_file():
    """Create the desktop shortcut file"""
    # Get current directory
    current_dir = os.getcwd()
    
    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Wire Checker
Comment=Wire Checker System for testing wire connections
Exec={current_dir}/wire_checker_launcher.sh
Icon={current_dir}/wire_checker_icon.png
Terminal=false
Categories=Utility;Electronics;
Keywords=wire;checker;raspberry;gpio;
"""
    
    with open('Wire Checker.desktop', 'w') as f:
        f.write(desktop_content)
    print("✓ Desktop file created: Wire Checker.desktop")

def create_icon():
    """Create a simple icon file (PNG)"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a 64x64 image with a blue background
        img = Image.new('RGB', (64, 64), color='#007bff')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple wire icon
        draw.rectangle([10, 20, 54, 24], fill='white')  # Horizontal wire
        draw.rectangle([30, 10, 34, 54], fill='white')  # Vertical wire
        draw.ellipse([8, 18, 12, 22], fill='#28a745')  # Green dot
        draw.ellipse([52, 18, 56, 22], fill='#dc3545')  # Red dot
        
        # Save the icon
        img.save('wire_checker_icon.png')
        print("✓ Icon created: wire_checker_icon.png")
        
    except ImportError:
        print("⚠ PIL not available, creating empty icon file")
        # Create an empty file as fallback
        with open('wire_checker_icon.png', 'w') as f:
            f.write('')
        print("✓ Empty icon file created: wire_checker_icon.png")

def install_to_desktop():
    """Install the desktop shortcut to the user's desktop"""
    desktop_dir = os.path.expanduser("~/Desktop")
    
    if not os.path.exists(desktop_dir):
        print(f"⚠ Desktop directory not found: {desktop_dir}")
        return False
    
    # Copy desktop file to desktop
    desktop_file = "Wire Checker.desktop"
    if os.path.exists(desktop_file):
        shutil.copy2(desktop_file, desktop_dir)
        print(f"✓ Desktop shortcut installed to: {desktop_dir}")
        return True
    else:
        print("⚠ Desktop file not found")
        return False

def main():
    print("Wire Checker Desktop Shortcut Installer")
    print("=" * 40)
    
    # Check if we're on Raspberry Pi
    if not os.path.exists('/proc/cpuinfo'):
        print("⚠ This script is designed for Raspberry Pi")
    
    # Create all necessary files
    create_launcher_script()
    create_icon()
    create_desktop_file()
    
    # Install to desktop
    if install_to_desktop():
        print("\n✓ Installation complete!")
        print("You can now double-click 'Wire Checker' on your desktop to run the application.")
    else:
        print("\n⚠ Installation partially complete.")
        print("Please manually copy 'Wire Checker.desktop' to your desktop folder.")
    
    print("\nFiles created:")
    print("- wire_checker_launcher.sh (executable launcher)")
    print("- Wire Checker.desktop (desktop shortcut)")
    print("- wire_checker_icon.png (application icon)")

if __name__ == "__main__":
    main()