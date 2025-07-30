#!/usr/bin/env python3
"""
Script to update all UI files to be responsive
This script applies responsive design patterns to all UI components
"""

import os
import re

def update_file_responsive(file_path, class_name):
    """Update a single file to be responsive"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add responsive UI import if not present
        if 'from responsive_ui_base import ResponsiveUI' not in content:
            # Find import section and add responsive UI import
            import_pattern = r'(import tkinter as tk\nfrom tkinter import [^\n]+)'
            if re.search(import_pattern, content):
                content = re.sub(import_pattern, r'\1\nfrom responsive_ui_base import ResponsiveUI', content)
        
        # Update class definition to inherit from ResponsiveUI
        class_pattern = f'class {class_name}:'
        if class_pattern in content and 'ResponsiveUI' not in content:
            content = content.replace(f'class {class_name}:', f'class {class_name}(ResponsiveUI):')
            
            # Add super().__init__() call
            init_pattern = f'def __init__\\(self, root\\):\n        self.root = root'
            replacement = f'def __init__(self, root):\n        super().__init__()\n        self.root = root'
            content = re.sub(init_pattern, replacement, content)
        
        # Update geometry settings to use responsive window setup
        geometry_pattern = r'self\.root\.geometry\(["\'](\d+)x(\d+)["\']?\)'
        if re.search(geometry_pattern, content):
            match = re.search(geometry_pattern, content)
            width, height = match.groups()
            
            # Replace geometry with responsive setup
            old_geometry = match.group(0)
            new_setup = f'''# Setup responsive window
        self.window_width, self.window_height = self.setup_responsive_window(
            root, root.title() or "Application", {width}, {height}
        )'''
            content = content.replace(old_geometry, new_setup)
        
        # Update common UI elements
        updates = [
            # Font updates
            (r"font=\('Arial', (\d+), 'bold'\)", lambda m: f"font=('Arial', self.get_font_size({m.group(1)}), 'bold')"),
            (r"font=\('Arial', (\d+)\)", lambda m: f"font=('Arial', self.get_font_size({m.group(1)}))"),
            
            # Padding updates
            (r"padx=(\d+)", lambda m: f"padx=self.get_padding({m.group(1)})"),
            (r"pady=(\d+)", lambda m: f"pady=self.get_padding({m.group(1)})"),
            (r"pady=\((\d+), (\d+)\)", lambda m: f"pady=(self.get_padding({m.group(1)}), self.get_padding({m.group(2)}))"),
            
            # Button width/height updates
            (r"width=(\d+), height=(\d+)", lambda m: f"width=self.get_button_size({m.group(1)}, {m.group(2)})[0], height=self.get_button_size({m.group(1)}, {m.group(2)})[1]"),
        ]
        
        for pattern, replacement in updates:
            if callable(replacement):
                content = re.sub(pattern, replacement, content)
            else:
                content = re.sub(pattern, replacement, content)
        
        # Write updated content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Update all UI files to be responsive"""
    
    # Files to update with their main class names
    ui_files = [
        ('auto_pin_detector.py', 'AutoPinDetector'),
        ('guided_wire_teaching.py', 'GuidedWireTeaching'),
        ('rfid_card_manager.py', 'RFIDCardManager'),
        ('wire_checker_with_rfid.py', 'WireCheckerRFIDUI'),
    ]
    
    print("🔄 Updating UI files to be responsive...")
    
    updated_count = 0
    for file_path, class_name in ui_files:
        if os.path.exists(file_path):
            if update_file_responsive(file_path, class_name):
                updated_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print(f"\n✅ Updated {updated_count} UI files to be responsive!")
    print("\n📱 All UI components now support:")
    print("   • Automatic screen size detection")
    print("   • Responsive font scaling")
    print("   • Adaptive button sizing")
    print("   • Dynamic padding adjustment")
    print("   • Proper window centering")
    print("   • Minimum size constraints")

if __name__ == '__main__':
    main()