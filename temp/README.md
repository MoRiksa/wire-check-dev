# Temporary/Testing Files

This directory contains files used for development, testing, and demonstration purposes.

## 📁 Files in this Directory

### 🧪 Testing Files
- **`test_audio.py`** - Test script for MP3 audio files
- **`test_diagnostic.py`** - Test script for diagnostic features
- **`wire_checker_speech_test.py`** - Demo version of speech wire checker

### 🎵 Audio Generation
- **`create_speech_audio.py`** - Script to generate speech audio files using text-to-speech

### 🖥️ macOS Version
- **`wire_checker_4pairs_speech_macos.py`** - macOS-compatible version for testing (no RPi.GPIO dependency)

### 📚 Documentation
- **`README_speech.md`** - Documentation for speech audio features

## 🚀 Usage

### Test Audio Files
```bash
python3 test_audio.py
```

### Test Diagnostic Features
```bash
python3 test_diagnostic.py
```

### Run Speech Demo (macOS)
```bash
python3 wire_checker_4pairs_speech_macos.py
```

### Generate Speech Audio
```bash
python3 create_speech_audio.py
```

## 📝 Notes

- These files are for development and testing only
- The macOS version is for testing on non-Raspberry Pi systems
- Audio generation requires espeak or similar text-to-speech engine
- All files in this directory are not part of the main production system 