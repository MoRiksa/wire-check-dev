# Wire Checker System

A comprehensive wire testing system for Raspberry Pi with support for 3 or 4 wire pairs, featuring speech audio feedback and detailed diagnostic capabilities.

## 🚀 Quick Start

### 1. Run the Main Application
```bash
python3 wire_checker_main.py
```

### 2. Select Configuration
- **3 Wire Pairs**: Basic wire testing (GPIO17↔27, GPIO22↔10, GPIO9↔11)
- **4 Wire Pairs**: Extended wire testing (adds GPIO5↔6)
- **4 Wire Pairs (Speech)**: Same as 4 pairs but with MP3 audio feedback
- **Pin Configuration**: Create custom pin configurations with product information

## 📁 Project Structure

```
wire_checker/
├── 📄 wire_checker_main.py              # Main application launcher
├── 📄 wire_checker_3pairs.py           # 3-pair wire checker
├── 📄 wire_checker_4pairs.py           # 4-pair wire checker
├── 📄 wire_checker_4pairs_speech.py    # 4-pair with speech audio
├── 📄 wire_checker_launcher.sh         # Desktop launcher script
├── 📄 Wire Checker.desktop             # Desktop shortcut
├── 📄 database_manager.py              # SQLite database management
├── 📄 statistics_viewer.py             # Statistics viewer
├── 📄 server_export.py                 # Server export module
├── 📄 pin_config_form.py               # Pin configuration form
├── 📄 pin_config_template.txt          # Template for manual pin config
├── 📄 PIN_CONFIG_GUIDE.md              # Pin configuration guide
├── 📄 backup.zip                       # Backup files
├── 📄 NOTES.md                         # Development notes
├── 📄 .gitignore                       # Git ignore file
│
├── 📁 sound/                           # Audio files
│   ├── 🔊 good.mp3                     # "GOOD" audio file
│   └── 🔊 not_good.mp3                 # "NOT GOOD" audio file
│
├── 📁 install/                         # Installation files
│   ├── 🔧 install.sh                   # Installation script
│   └── 🔧 install_desktop_shortcut.py  # Desktop shortcut installer
│
└── 📁 temp/                            # Temporary/Testing files
    ├── 📄 wire_checker_4pairs_speech_macos.py  # macOS test version
    ├── 📄 wire_checker_speech_test.py          # Speech test demo
    ├── 📄 test_audio.py                        # Audio testing
    ├── 📄 test_diagnostic.py                   # Diagnostic testing
    ├── 📄 create_speech_audio.py               # Audio file generator
    ├── 📄 test_cycle_system.py                 # Cycle system testing
    └── 📄 README_speech.md                     # Speech feature docs
```

## 🎯 Features

### Core Functionality
- **3-Pair Testing**: GPIO17↔27, GPIO22↔10, GPIO9↔11
- **4-Pair Testing**: Adds GPIO5↔6 to 3-pair configuration
- **Custom Pin Configuration**: Create your own pin assignments with product info
- **Speech Audio**: MP3 audio feedback for status changes
- **7-inch TFT Optimized**: Large fonts and touch-friendly interface
- **Cycle Management**: Track individual testing sessions with unique IDs
- **Persistent Storage**: SQLite database for reliable data storage
- **Statistics Tracking**: Daily and historical statistics

### Diagnostic Capabilities
- **Open Pair Detection**: Shows which specific pairs are not connected
- **Cross Connection Detection**: Identifies wrong wire connections
- **IN-to-IN Connection Detection**: Detects input pin cross-connections
- **OUT-to-OUT Connection Detection**: Detects output pin cross-connections
- **Real-time Status**: Updates every 500ms with detailed diagnostics

### Hardware Control
- **LED Indicators**: Red (NOT GOOD), Yellow (OPEN), Green (GOOD)
- **Solenoid Control**: Two solenoids for mechanical feedback
- **Audio Feedback**: Speech files or buzzer sounds

## 🎯 Pin Configuration Feature

### Custom Pin Setup
The Pin Configuration Form allows you to:
- **Product Information**: Enter product name and part number
- **Custom Pin Assignment**: Define your own GPIO pin pairs (up to 6 pairs)
- **Template Support**: Use notepad templates or direct form input
- **Automatic Generation**: Creates custom wire checker with your configuration

### Usage Methods
1. **Direct Form Input**: Use the GUI form to enter pin configurations
2. **Template File**: Edit text templates in notepad and import them
3. **Load Existing**: Import previously saved configurations

### Template Format
```
Product Name: My Wire Assembly
Product No: MWA-001
Pair 1: GPIO17 -> GPIO27
Pair 2: GPIO22 -> GPIO10
Pair 3: GPIO9 -> GPIO11
Pair 4: GPIO5 -> GPIO6
```

See `PIN_CONFIG_GUIDE.md` for detailed instructions.

## 🔧 Installation

### Automatic Installation
```bash
cd install/
./install.sh
```

### Manual Installation
```bash
cd install/
python3 install_desktop_shortcut.py
```

## 🎵 Audio Setup

The speech version uses MP3 files in the `sound/` directory:
- `sound/good.mp3` - Plays when status is "GOOD"
- `sound/not_good.mp3` - Plays when status is "NOT GOOD"

## 📊 Status Types

| Status | LED | Audio | Description |
|--------|-----|-------|-------------|
| **GOOD** | 🟢 Green | "GOOD" | All pairs connected correctly |
| **OPEN** | 🟡 Yellow | None | One or more pairs not connected |
| **NOT GOOD** | 🔴 Red | "NOT GOOD" | Cross connections detected |

## 🔍 Diagnostic Information

The speech version provides detailed diagnostic information:

### Open Pairs
```
OPEN PAIRS:
Pair 1: GPIO17 ↔ GPIO27
Pair 3: GPIO9 ↔ GPIO11
```

### Cross Connections
```
CROSS CONNECTIONS:
GPIO17 → GPIO10 (wrong connection)
```

### IN-to-IN Connections
```
IN-TO-IN CONNECTIONS:
GPIO27 ↔ GPIO11 (should not be connected)
```

## 🖥️ System Requirements

### Raspberry Pi
- Raspberry Pi (any model)
- Python 3.6+
- RPi.GPIO library
- pygame (for speech version)

### Dependencies
```bash
pip3 install pygame
```

## 🧪 Testing

### Audio Testing
```bash
cd temp/
python3 test_audio.py
```

### Diagnostic Testing
```bash
cd temp/
python3 test_diagnostic.py
```

### Speech Demo (macOS)
```bash
cd temp/
python3 wire_checker_4pairs_speech_macos.py
```

### Cycle System Testing
```bash
cd temp/
python3 test_cycle_system.py
```

## 🔧 GPIO Pin Configuration

### 3-Pair Configuration
- **Pair 1**: GPIO17 ↔ GPIO27
- **Pair 2**: GPIO22 ↔ GPIO10
- **Pair 3**: GPIO9 ↔ GPIO11

### 4-Pair Configuration
- **Pair 1**: GPIO17 ↔ GPIO27
- **Pair 2**: GPIO22 ↔ GPIO10
- **Pair 3**: GPIO9 ↔ GPIO11
- **Pair 4**: GPIO5 ↔ GPIO6

### Hardware Pins
- **LEDs**: GPIO 2 (Red), 3 (Yellow), 4 (Green)
- **Solenoids**: GPIO 13, 15
- **Buzzer**: GPIO 18 (disabled in speech version)

## 📝 Development Notes

- All UI elements optimized for 7-inch TFT screens
- Speech audio uses pygame for cross-platform compatibility
- Diagnostic features provide pin-level detail for troubleshooting
- Thread-safe audio playback with proper locking mechanisms

## 🔄 Cycle Management

### How Cycles Work
- **Unique Cycle ID**: Each testing session gets a unique identifier
- **Real-time Tracking**: Counts are updated as wires are tested
- **Persistent Storage**: All data stored in SQLite database
- **Statistics Viewing**: View daily and historical statistics

### Cycle Features
- **Automatic Creation**: Cycles start when you select a configuration
- **Live Updates**: Real-time count display during testing
- **Cycle Closure**: "Close Cycle" button to end session
- **Data Export**: Ready for server transmission (future enhancement)

### Statistics Available
- **Daily Statistics**: Aggregated data by configuration
- **Cycle History**: Detailed view of all completed cycles
- **Real-time Counts**: Good, Not Good, and Open counts
- **Export Ready**: JSON format for server integration

## 🚀 Usage

### Standard Usage
1. **Start the application**: `python3 wire_checker_main.py`
2. **Select configuration**: Choose 3-pair, 4-pair, 4-pair speech, pin configuration, or view statistics
3. **Connect wires**: Follow the GPIO pin configuration
4. **Monitor status**: Watch LED indicators, diagnostic information, and cycle counts
5. **Close cycle**: Use "Close Cycle" button when testing session is complete
6. **View statistics**: Use "View Statistics" to see historical data

### Custom Pin Configuration Usage
1. **Access Pin Config**: Click "Pin Configuration" from main menu
2. **Enter Product Info**: Fill in product name and part number
3. **Configure Pins**: Enter GPIO pin pairs or load from template
4. **Create Template**: Use "Create Template" for notepad editing
5. **Load from File**: Import configuration from text file
6. **Apply & Test**: Generate and run custom wire checker
7. **Run Custom Checker**: Use "Run Custom Checker" to run previously created configurations

## 📞 Support

For issues or questions, check the diagnostic information displayed on screen or refer to the test files in the `temp/` directory. 