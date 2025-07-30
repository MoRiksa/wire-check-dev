#!/bin/bash

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