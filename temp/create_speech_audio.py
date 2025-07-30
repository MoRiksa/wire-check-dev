#!/usr/bin/env python3
"""
Script to create speech audio files for wire checker
"""

import os
import subprocess
import sys

def create_speech_audio():
    """Create speech audio files using text-to-speech"""
    
    # Check if espeak is available
    try:
        subprocess.run(['espeak', '--version'], capture_output=True, check=True)
        print("Using espeak for text-to-speech...")
        
        # Create "GOOD" audio with female US English voice
        print("Creating 'good.wav' with female US English voice...")
        subprocess.run([
            'espeak', '-w', 'good.wav', 
            '-v', 'mb-en1',    # Female MBROLA voice en1
            '-s', '130',       # Slightly slow
            '-p', '45',        # Slightly higher pitch
            '-a', '90',        # Medium amplitude
            'GOOD'
        ], check=True)
        
        # Create "NOT GOOD" audio with female US English voice
        print("Creating 'not_good.wav' with female US English voice...")
        subprocess.run([
            'espeak', '-w', 'not_good.wav',
            '-v', 'mb-en1',    # Female MBROLA voice en1
            '-s', '130',       # Slightly slow
            '-p', '45',        # Slightly higher pitch
            '-a', '90',        # Medium amplitude
            'Not good'
        ], check=True)
        
        print("Audio files created successfully!")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("espeak not found. Trying alternative methods...")
        
        # Try using say command (macOS)
        try:
            subprocess.run(['say', '--version'], capture_output=True, check=True)
            print("Using macOS 'say' command...")
            
            # Create "GOOD" audio with female voice
            print("Creating 'good.wav' with female voice...")
            subprocess.run([
                'say', '-o', 'good.wav', 
                '-v', 'Samantha',  # Female voice on macOS
                'GOOD'
            ], check=True)
            
            # Create "NOT GOOD" audio with female voice
            print("Creating 'not_good.wav' with female voice...")
            subprocess.run([
                'say', '-o', 'not_good.wav', 
                '-v', 'Samantha',  # Female voice on macOS
                'NOT GOOD'
            ], check=True)
            
            print("Audio files created successfully!")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("No text-to-speech engine found.")
            print("Please install espeak or use a system with text-to-speech capabilities.")
            return False

def create_simple_beep_audio():
    """Create simple beep audio files as fallback"""
    try:
        import numpy as np
        import wave
        
        print("Creating simple beep audio files...")
        
        # Create "GOOD" beep (higher frequency)
        sample_rate = 44100
        duration = 0.5
        frequency = 800
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
        audio_data = (audio_data * 32767).astype(np.int16)
        
        with wave.open('good.wav', 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        # Create "NOT GOOD" beep (lower frequency, longer duration)
        duration = 0.8
        frequency = 400
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
        audio_data = (audio_data * 32767).astype(np.int16)
        
        with wave.open('not_good.wav', 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        print("Simple beep audio files created successfully!")
        return True
        
    except ImportError:
        print("numpy not available. Cannot create beep audio files.")
        return False

def main():
    print("Wire Checker Speech Audio Creator")
    print("=================================")
    
    # Try to create speech audio first
    if create_speech_audio():
        print("\nSpeech audio files created successfully!")
        print("Files created:")
        print("- good.wav")
        print("- not_good.wav")
    else:
        print("\nFalling back to simple beep audio...")
        if create_simple_beep_audio():
            print("\nBeep audio files created successfully!")
            print("Files created:")
            print("- good.wav (high frequency beep)")
            print("- not_good.wav (low frequency beep)")
        else:
            print("\nFailed to create audio files.")
            print("Please install espeak or numpy to create audio files.")
            sys.exit(1)

if __name__ == '__main__':
    main() 