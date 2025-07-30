import time
import threading
import tkinter as tk
from tkinter import ttk
import pygame
import os

# Initialize pygame mixer for audio
pygame.mixer.init()

# Global variables for status
current_status = "INITIALIZING"
status_lock = threading.Lock()
audio_lock = threading.Lock()

# Counters
good_counter = 0
not_good_counter = 0

# Audio file paths
AUDIO_GOOD = "sound/good.mp3"
AUDIO_NOT_GOOD = "sound/not_good.mp3"

def play_audio(file_path):
    """Play audio file using pygame"""
    try:
        with audio_lock:
            if os.path.exists(file_path):
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                # Wait for audio to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            else:
                print(f"Audio file not found: {file_path}")
    except Exception as e:
        print(f"Error playing audio: {e}")

def play_good_sound():
    """Play GOOD audio"""
    play_audio(AUDIO_GOOD)

def play_not_good_sound():
    """Play NOT GOOD audio"""
    play_audio(AUDIO_NOT_GOOD)

def wire_checker_loop():
    """Main wire checker loop running in background thread"""
    global current_status, good_counter, not_good_counter
    previous_status = None
    
    # Simulate wire testing for demo purposes
    test_sequence = ["OPEN", "GOOD", "NOT GOOD", "GOOD", "OPEN", "NOT GOOD"]
    test_index = 0
    
    while True:
        try:
            # Simulate status changes for demo
            with status_lock:
                current_status = test_sequence[test_index % len(test_sequence)]
                
                # Play audio when status changes
                if current_status != previous_status:
                    if current_status == "GOOD":
                        print("Status: GOOD - Playing GOOD audio")
                        threading.Thread(target=play_good_sound, daemon=True).start()
                    elif current_status == "NOT GOOD":
                        print("Status: NOT GOOD - Playing NOT GOOD audio")
                        threading.Thread(target=play_not_good_sound, daemon=True).start()
                    else:
                        print(f"Status: {current_status} - No audio")
                    
                    # Increment counters only when transitioning from OPEN
                    if previous_status == "OPEN":
                        if current_status == "GOOD":
                            good_counter += 1
                        elif current_status == "NOT GOOD":
                            not_good_counter += 1
                    
                    previous_status = current_status
                
                test_index += 1
            
            time.sleep(3)  # Change status every 3 seconds for demo
            
        except Exception as e:
            print(f"Error in wire checker loop: {e}")
            time.sleep(1)

class WireCheckerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wire Checker Status - 4 Pairs (Speech) - DEMO")
        self.root.geometry("1024x768")  # Optimized for 7-inch TFT
        self.root.configure(bg='#f0f0f0')
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Create main frame
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Title
        title_label = tk.Label(main_frame, text="Wire Checker Status - 4 Pairs (Speech) - DEMO", 
                              font=('Arial', 28, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 40))
        
        # Status display
        self.status_label = tk.Label(main_frame, text="INITIALIZING", 
                                    font=('Arial', 42, 'bold'), 
                                    width=25, height=5,
                                    relief='raised', borderwidth=6)
        self.status_label.pack(pady=40)
        
        # Solenoid status
        self.solenoid_label = tk.Label(main_frame, text="Solenoid: OFF", 
                                      font=('Arial', 22, 'bold'), 
                                      bg='#f0f0f0', fg='#dc3545')
        self.solenoid_label.pack(pady=(0, 25))
        
        # Audio status
        self.audio_label = tk.Label(main_frame, text="Audio: Speech Files", 
                                   font=('Arial', 18, 'bold'), 
                                   bg='#f0f0f0', fg='#007bff')
        self.audio_label.pack(pady=(0, 25))
        
        # Demo info
        demo_label = tk.Label(main_frame, text="DEMO MODE: Status changes every 3 seconds", 
                             font=('Arial', 16, 'bold'), 
                             bg='#fff3cd', fg='#856404',
                             relief='raised', borderwidth=3)
        demo_label.pack(pady=(0, 25))
        
        # Counters frame
        counters_frame = tk.Frame(main_frame, bg='#f0f0f0')
        counters_frame.pack(pady=(0, 25))
        
        # Good counter
        self.good_counter_label = tk.Label(counters_frame, text="GOOD Count: 0", 
                                          font=('Arial', 20, 'bold'), 
                                          bg='#d4edda', fg='#155724',
                                          relief='raised', borderwidth=3)
        self.good_counter_label.pack(side='left', padx=(0, 30))
        
        # NOT GOOD counter
        self.not_good_counter_label = tk.Label(counters_frame, text="NOT GOOD Count: 0", 
                                              font=('Arial', 20, 'bold'), 
                                              bg='#f8d7da', fg='#721c24',
                                              relief='raised', borderwidth=3)
        self.not_good_counter_label.pack(side='left')
        
        # Last updated label
        self.last_updated_label = tk.Label(main_frame, text="Last updated: -", 
                                          font=('Arial', 18), bg='#f0f0f0')
        self.last_updated_label.pack(pady=(25, 0))
        
        # Wire pairs info
        pairs_frame = tk.Frame(main_frame, bg='#f0f0f0')
        pairs_frame.pack(pady=(40, 0))
        
        pairs_label = tk.Label(pairs_frame, text="Wire Pairs:", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0')
        pairs_label.pack()
        
        pairs_info = tk.Label(pairs_frame, 
                             text="GPIO17 ↔ GPIO27\nGPIO22 ↔ GPIO10\nGPIO9 ↔ GPIO11\nGPIO5 ↔ GPIO6", 
                             font=('Arial', 18), bg='#f0f0f0', justify='left')
        pairs_info.pack()
        
        # Start updating the UI
        self.update_ui()
    
    def update_ui(self):
        """Update the UI with current status"""
        with status_lock:
            status = current_status
        
        # Update status label
        self.status_label.config(text=status)
        
        # Update solenoid status
        if status == "GOOD":
            self.solenoid_label.config(text="Solenoid: ON", fg='#28a745')
        else:
            self.solenoid_label.config(text="Solenoid: OFF", fg='#dc3545')
        
        # Update counters
        self.good_counter_label.config(text=f"GOOD Count: {good_counter}")
        self.not_good_counter_label.config(text=f"NOT GOOD Count: {not_good_counter}")
        
        # Update colors based on status
        if status == "GOOD":
            self.status_label.config(bg='#d4edda', fg='#155724')
        elif status == "OPEN":
            self.status_label.config(bg='#fff3cd', fg='#856404')
        elif status == "NOT GOOD":
            self.status_label.config(bg='#f8d7da', fg='#721c24')
        else:  # INITIALIZING
            self.status_label.config(bg='#e2e3e5', fg='#383d41')
        
        # Update last updated time
        current_time = time.strftime("%H:%M:%S")
        self.last_updated_label.config(text=f"Last updated: {current_time}")
        
        # Schedule next update
        self.root.after(500, self.update_ui)

def main():
    # Check if audio files exist
    if not os.path.exists(AUDIO_GOOD) or not os.path.exists(AUDIO_NOT_GOOD):
        print("Audio files not found. Please run create_speech_audio.py first.")
        return
    
    print("Wire Checker Speech Demo Starting...")
    print("Status will cycle every 3 seconds to demonstrate audio functionality.")
    print("Audio files:")
    print(f"- GOOD: {AUDIO_GOOD}")
    print(f"- NOT GOOD: {AUDIO_NOT_GOOD}")
    
    # Start the wire checker in a background thread
    wire_checker_thread = threading.Thread(target=wire_checker_loop, daemon=True)
    wire_checker_thread.start()
    
    # Create and run the Tkinter UI
    root = tk.Tk()
    app = WireCheckerUI(root)
    
    # Handle window close
    def on_closing():
        print("Closing Wire Checker Demo...")
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    print("Wire Checker UI starting...")
    root.mainloop()

if __name__ == '__main__':
    main() 