# Wire Checker with Speech Audio

This version of the wire checker uses speech audio files instead of buzzer sounds to provide status feedback.

## Files

- `wire_checker_4pairs_speech.py` - Main wire checker with speech audio
- `wire_checker_speech_test.py` - Demo version for testing on macOS
- `sound/good.mp3` - Audio file for "GOOD" status
- `sound/not_good.mp3` - Audio file for "NOT GOOD" status

## Setup

### 1. Install Dependencies

```bash
# Install pygame for audio playback
pip install pygame

# Optional: Install espeak for text-to-speech (Linux)
sudo apt-get install espeak

# Optional: Install numpy for fallback beep generation
pip install numpy
```

### 2. Audio Files

The wire checker uses MP3 audio files located in the `sound/` folder:
- `sound/good.mp3` - Audio for "GOOD" status
- `sound/not_good.mp3` - Audio for "NOT GOOD" status

### 3. Run the Wire Checker

```bash
python wire_checker_4pairs_speech.py
```

## Features

### Audio Feedback
- **GOOD Status**: Plays "GOOD" speech or high-frequency beep
- **NOT GOOD Status**: Plays "NOT GOOD" speech or low-frequency beep
- **OPEN Status**: No audio (same as original)

### Visual Feedback
- **Green LED**: GOOD status
- **Red LED**: NOT GOOD status  
- **Yellow LED**: OPEN status

### Hardware Control
- **Solenoid 1**: Activated when status is GOOD
- **Solenoid 2**: Activated when status is GOOD
- **Buzzer**: Disabled (replaced by speech audio)

## Audio Files

The wire checker uses MP3 audio files for speech feedback:
- `sound/good.mp3` - Audio for "GOOD" status
- `sound/not_good.mp3` - Audio for "NOT GOOD" status

## Customization

### Using Your Own Audio Files
Replace the audio files in the `sound/` folder with your own:
- `sound/good.mp3` - Your custom "GOOD" audio
- `sound/not_good.mp3` - Your custom "NOT GOOD" audio

### Modifying Audio Files
Simply replace the MP3 files in the `sound/` folder with your preferred audio files. The system supports any MP3 format.

## Troubleshooting

### No Audio Playback
1. Check if pygame is installed: `pip install pygame`
2. Verify audio files exist: `ls *.wav`
3. Check system audio settings

### No Text-to-Speech
1. Install espeak: `sudo apt-get install espeak` (Linux)
2. Or use the fallback beep sounds (requires numpy)

### Audio Files Not Found
1. Ensure the `sound/` folder exists with `good.mp3` and `not_good.mp3` files
2. Check if the audio files are valid MP3 format
3. Verify file permissions allow reading the audio files

## Differences from Original

| Feature | Original (`wire_checker_4pairs.py`) | Speech Version (`wire_checker_4pairs_speech.py`) |
|---------|--------------------------------------|--------------------------------------------------|
| Audio | Buzzer beeps | Speech audio files |
| GOOD Status | Single beep | "GOOD" speech |
| NOT GOOD Status | 5 beeps | "NOT GOOD" speech |
| OPEN Status | No sound | No sound |
| Dependencies | RPi.GPIO | RPi.GPIO + pygame |

## GPIO Pin Configuration

Same as original:
- **LEDs**: GPIO 2 (Red), 3 (Yellow), 4 (Green)
- **Solenoids**: GPIO 13, 15
- **Wire Pairs**: GPIO 17↔27, 22↔10, 9↔11, 5↔6
- **Buzzer**: GPIO 18 (disabled in speech version) 