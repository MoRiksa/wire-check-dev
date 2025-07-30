 #!/bin/bash

# Installation script for Wire Checker Desktop Shortcut
echo "Installing Wire Checker Desktop Shortcut..."

# Make sure we're in the right directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Run the Python installation script
python3 install_desktop_shortcut.py

echo "Installation complete!"
echo "You can now run the Wire Checker from your desktop."