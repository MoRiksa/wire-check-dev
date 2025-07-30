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

# Diagnostic information
pair_status = [False, False, False, False]  # Status of each pair
cross_connections = []
in_to_in_connections = []
out_to_out_connections = []

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
    global current_status, good_counter, not_good_counter, pair_status, cross_connections, in_to_in_connections, out_to_out_connections
    previous_status = None
    
    # Simulate wire testing for demo purposes with diagnostic info
    test_scenarios = [
        # Scenario 1: All good
        {"status": "GOOD", "pairs": [True, True, True, True], "cross": [], "in_in": [], "out_out": []},
        # Scenario 2: Pair 1 open
        {"status": "OPEN", "pairs": [False, True, True, True], "cross": [], "in_in": [], "out_out": []},
        # Scenario 3: Cross connection
        {"status": "NOT GOOD", "pairs": [True, True, True, True], "cross": [(0, 1)], "in_in": [], "out_out": []},
        # Scenario 4: Multiple issues
        {"status": "NOT GOOD", "pairs": [False, True, False, True], "cross": [(1, 3)], "in_in": [(0, 2)], "out_out": []},
        # Scenario 5: All pairs open
        {"status": "OPEN", "pairs": [False, False, False, False], "cross": [], "in_in": [], "out_out": []},
    ]
    test_index = 0
    
    while True:
        try:
            # Simulate status changes for demo
            with status_lock:
                scenario = test_scenarios[test_index % len(test_scenarios)]
                current_status = scenario["status"]
                pair_status = scenario["pairs"]
                cross_connections = scenario["cross"]
                in_to_in_connections = scenario["in_in"]
                out_to_out_connections = scenario["out_out"]
                
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
            
            time.sleep(4)  # Change status every 4 seconds for demo
            
        except Exception as e:
            print(f"Error in wire checker loop: {e}")
            time.sleep(1)

def get_diagnostic_message():
    """Generate diagnostic message based on current status"""
    global pair_status, cross_connections, in_to_in_connections, out_to_out_connections
    
    messages = []
    
    # Check for open pairs
    open_pairs = []
    for i, (output_pin, input_pin) in enumerate(WIRE_PAIRS):
        if not pair_status[i]:
            open_pairs.append(f"Pair {i+1}: GPIO{output_pin} ↔ GPIO{input_pin}")
    
    if open_pairs:
        messages.append("OPEN PAIRS:")
        messages.extend(open_pairs)
    
    # Check for cross connections
    if cross_connections:
        messages.append("\nCROSS CONNECTIONS:")
        for pair1, pair2 in cross_connections:
            out1, in1 = WIRE_PAIRS[pair1]
            out2, in2 = WIRE_PAIRS[pair2]
            messages.append(f"GPIO{out1} → GPIO{in2} (wrong connection)")
    
    # Check for IN-to-IN connections
    if in_to_in_connections:
        messages.append("\nIN-TO-IN CONNECTIONS:")
        for pair1, pair2 in in_to_in_connections:
            _, in1 = WIRE_PAIRS[pair1]
            _, in2 = WIRE_PAIRS[pair2]
            messages.append(f"GPIO{in1} ↔ GPIO{in2} (should not be connected)")
    
    # Check for OUT-to-OUT connections
    if out_to_out_connections:
        messages.append("\nOUT-TO-OUT CONNECTIONS:")
        for pair1, pair2 in out_to_out_connections:
            out1, _ = WIRE_PAIRS[pair1]
            out2, _ = WIRE_PAIRS[pair2]
            messages.append(f"GPIO{out1} ↔ GPIO{out2} (should not be connected)")
    
    if not messages:
        return "All connections are correct!"
    
    return "\n".join(messages)

def get_status_summary():
    """Get a summary of the current status"""
    global pair_status, cross_connections, in_to_in_connections, out_to_out_connections
    
    total_issues = len([p for p in pair_status if not p]) + len(cross_connections) + len(in_to_in_connections) + len(out_to_out_connections)
    
    if total_issues == 0:
        return "All pairs connected correctly"
    elif any(not p for p in pair_status):
        open_count = len([p for p in pair_status if not p])
        return f"{open_count} pair(s) not connected"
    else:
        return f"{total_issues} connection issue(s) detected"

# Wire pairs (output, input)
WIRE_PAIRS = [
    (17, 27),  # Pair 1
    (22, 10),  # Pair 2
    (9, 11),    # Pair 3
    (5, 6)     # Pair 4
]

class WireCheckerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wire Checker Status - 4 Pairs (Speech) - macOS")
        self.root.geometry("1024x768")  # Optimized for 7-inch TFT
        self.root.configure(bg='#f0f0f0')
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Create main frame
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Title
        title_label = tk.Label(main_frame, text="Wire Checker Status - 4 Pairs (Speech)", 
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
        
        # Diagnostic section
        diagnostic_frame = tk.Frame(main_frame, bg='#f0f0f0')
        diagnostic_frame.pack(pady=(30, 0), fill='both', expand=True)
        
        diagnostic_label = tk.Label(diagnostic_frame, text="Diagnostic Information:", 
                                   font=('Arial', 20, 'bold'), bg='#f0f0f0')
        diagnostic_label.pack()
        
        # Status summary
        self.status_summary_label = tk.Label(diagnostic_frame, text="All pairs connected correctly", 
                                            font=('Arial', 18, 'bold'), 
                                            bg='#d4edda', fg='#155724',
                                            relief='raised', borderwidth=3)
        self.status_summary_label.pack(pady=(10, 20))
        
        # Diagnostic details
        self.diagnostic_text = tk.Text(diagnostic_frame, 
                                       height=8, width=60,
                                       font=('Arial', 14),
                                       bg='#f8f9fa', fg='#212529',
                                       relief='sunken', borderwidth=2,
                                       wrap='word')
        self.diagnostic_text.pack(pady=(0, 20))
        
        # Wire pairs info
        pairs_frame = tk.Frame(main_frame, bg='#f0f0f0')
        pairs_frame.pack(pady=(20, 0))
        
        pairs_label = tk.Label(pairs_frame, text="Expected Wire Pairs:", 
                              font=('Arial', 18, 'bold'), bg='#f0f0f0')
        pairs_label.pack()
        
        pairs_info = tk.Label(pairs_frame, 
                             text="Pair 1: GPIO17 ↔ GPIO27\nPair 2: GPIO22 ↔ GPIO10\nPair 3: GPIO9 ↔ GPIO11\nPair 4: GPIO5 ↔ GPIO6", 
                             font=('Arial', 16), bg='#f0f0f0', justify='left')
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
        
        # Update diagnostic information
        status_summary = get_status_summary()
        diagnostic_message = get_diagnostic_message()
        
        # Update status summary
        if status == "GOOD":
            self.status_summary_label.config(text=status_summary, bg='#d4edda', fg='#155724')
        elif status == "OPEN":
            self.status_summary_label.config(text=status_summary, bg='#fff3cd', fg='#856404')
        elif status == "NOT GOOD":
            self.status_summary_label.config(text=status_summary, bg='#f8d7da', fg='#721c24')
        else:
            self.status_summary_label.config(text="Initializing...", bg='#e2e3e5', fg='#383d41')
        
        # Update diagnostic text
        self.diagnostic_text.delete(1.0, tk.END)
        self.diagnostic_text.insert(1.0, diagnostic_message)
        
        # Update last updated time
        current_time = time.strftime("%H:%M:%S")
        self.last_updated_label.config(text=f"Last updated: {current_time}")
        
        # Schedule next update
        self.root.after(500, self.update_ui)

def main():
    # Check if audio files exist
    if not os.path.exists(AUDIO_GOOD) or not os.path.exists(AUDIO_NOT_GOOD):
        print("Audio files not found. Please ensure sound/good.mp3 and sound/not_good.mp3 exist.")
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