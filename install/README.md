# Installation Files

This directory contains files for setting up the Wire Checker system on Raspberry Pi.

## 📁 Files in this Directory

### 🔧 Installation Scripts
- **`install.sh`** - Main installation script (bash)
- **`install_desktop_shortcut.py`** - Python script to create desktop shortcut

## 🚀 Installation

### Automatic Installation
```bash
./install.sh
```

### Manual Installation
```bash
python3 install_desktop_shortcut.py
```

## 📋 What the Installation Does

1. **Creates Launcher Script**: `wire_checker_launcher.sh` (executable)
2. **Creates Desktop Shortcut**: `Wire Checker.desktop`
3. **Creates Application Icon**: `wire_checker_icon.png`
4. **Installs to Desktop**: Copies shortcut to user's desktop folder

## 🖥️ Requirements

- Raspberry Pi (recommended)
- Python 3.6+
- Desktop environment (for desktop shortcut)
- Write permissions to desktop directory

## 📝 Notes

- The installation creates a desktop shortcut for easy access
- The launcher script handles path resolution and error checking
- The icon is generated programmatically if PIL is available
- Installation can be run multiple times safely 