#!/usr/bin/env python3
"""
Simple script to test the MP3 audio files
"""

import pygame
import os
import time

def test_audio_files():
    """Test the MP3 audio files"""
    
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Audio file paths
    audio_files = {
        "GOOD": "sound/good.mp3",
        "NOT GOOD": "sound/not_good.mp3"
    }
    
    print("Testing MP3 Audio Files")
    print("=======================")
    
    for status, file_path in audio_files.items():
        print(f"\nTesting {status} audio: {file_path}")
        
        if os.path.exists(file_path):
            try:
                # Load and play the audio
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                
                print(f"✓ Playing {status} audio...")
                
                # Wait for audio to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                print(f"✓ {status} audio completed successfully!")
                
            except Exception as e:
                print(f"✗ Error playing {status} audio: {e}")
        else:
            print(f"✗ Audio file not found: {file_path}")
    
    print("\nAudio test completed!")

if __name__ == '__main__':
    test_audio_files() 