# Wire Checker with RFID Locking System
# Integrates RF ID card unlock functionality

# Handle GPIO import
try:
    import RPi.GPIO as GPIO
    RASPBERRY_PI = True
except ImportError:
    from mock_gpio import GPIO
    RASPBERRY_PI = False

import time
import threading
import tkinter as tk
from tkinter import ttk
import os
from rfid_manager import get_solenoid_lock_manager

# GPIO pin assignments
RED_LED = 2
YELLOW_LED = 3
GREEN_LED = 4
BUZZER = 18

# Wire pairs (output, input)
WIRE_PAIRS = [
    (17, 27),  # Pair 1
    (22, 10),  # Pair 2
    (9, 11),   # Pair 3
    (5, 6)     # Pair 4
]

# Global variables
current_status = "INITIALIZING"
status_lock = threading.Lock()
good_counter = 0
not_good_counter = 0

# RFID Lock Manager
lock_manager = get_solenoid_lock_manager()

# Setup GPIO
if RASPBERRY_PI:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    GPIO.setup(YELLOW_LED, GPIO.OUT)
    GPIO.setup(BUZZER, GPIO.OUT)
    
    # Setup wire pairs
    for output_pin, input_pin in WIRE_PAIRS:
        GPIO.setup(output_pin, GPIO.OUT)
        GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # Initialize outputs
    GPIO.output(BUZZER, GPIO.HIGH)

def test_wire_pair(output_pin, input_pin):
    """Test if a wire pair is properly connected"""
    if not RASPBERRY_PI:
        import random
        return random.choice([True, False])
    
    GPIO.output(output_pin, GPIO.HIGH)
    time.sleep(0.01)
    high_received = GPIO.input(input_pin)
    
    GPIO.output(output_pin, GPIO.LOW)
    time.sleep(0.01)
    low_received = GPIO.input(input_pin)
    
    return high_received and not low_received

def wire_checker_loop():
    """Main wire checker loop with RFID locking"""
    global current_status, good_counter, not_good_counter
    previous_status = None
    
    while True:
        try:
            # Test each pair
            pair_results = []
            for output_pin, input_pin in WIRE_PAIRS:
                is_connected = test_wire_pair(output_pin, input_pin)
                pair_results.append(is_connected)
            
            # Determine status
            all_connected = all(pair_results)
            
            with status_lock:
                if all_connected:
                    current_status = "GOOD"
                    if RASPBERRY_PI:
                        GPIO.output(GREEN_LED, GPIO.HIGH)
                        GPIO.output(RED_LED, GPIO.LOW)
                        GPIO.output(YELLOW_LED, GPIO.LOW)
                    
                    # Unlock solenoids for GOOD status
                    if lock_manager.is_locked:
                        # Don't auto-unlock, require RFID
                        pass
                    else:
                        lock_manager.control_solenoid(True)  # Enable solenoids
                
                else:
                    # Check if any pairs are connected (partial connection)
                    any_connected = any(pair_results)
                    
                    if any_connected:
                        current_status = "NOT GOOD"
                        if RASPBERRY_PI:
                            GPIO.output(RED_LED, GPIO.HIGH)
                            GPIO.output(GREEN_LED, GPIO.LOW)
                            GPIO.output(YELLOW_LED, GPIO.LOW)
                        
                        # LOCK solenoids for NOT GOOD status
                        lock_manager.lock_solenoids("NOT GOOD - Cross connection detected")
                        
                    else:
                        current_status = "OPEN"
                        if RASPBERRY_PI:
                            GPIO.output(YELLOW_LED, GPIO.HIGH)
                            GPIO.output(RED_LED, GPIO.LOW)
                            GPIO.output(GREEN_LED, GPIO.LOW)
                        
                        # Don't lock for OPEN status, just disable solenoids
                        lock_manager.control_solenoid(False)
                
                # Update counters
                if previous_status == "OPEN":
                    if current_status == "GOOD":
                        good_counter += 1
                    elif current_status == "NOT GOOD":
                        not_good_counter += 1
                
                previous_status = current_status
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error in wire checker loop: {e}")
            time.sleep(1)

class WireCheckerRFIDUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wire Checker with RFID Locking")
        self.root.geometry("1000x800")
        self.root.configure(bg='#f0f0f0')
        
        self.root.eval('tk::PlaceWindow . center')
        
        # Create main frame
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Title
        title_label = tk.Label(main_frame, text="Wire Checker with RFID Locking", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 20))
        
        # Status display
        self.status_label = tk.Label(main_frame, text="INITIALIZING", 
                                    font=('Arial', 36, 'bold'), 
                                    width=20, height=3,
                                    relief='raised', borderwidth=6)
        self.status_label.pack(pady=30)
        
        # RFID Lock Status
        rfid_frame = tk.LabelFrame(main_frame, text="RFID Lock Status", 
                                  font=('Arial', 16, 'bold'), bg='#f0f0f0')
        rfid_frame.pack(fill='x', pady=(0, 20))
        
        self.lock_status_label = tk.Label(rfid_frame, text="🔓 UNLOCKED", 
                                         font=('Arial', 18, 'bold'), 
                                         bg='#d4edda', fg='#155724',
                                         relief='raised', borderwidth=3)
        self.lock_status_label.pack(pady=10)
        
        self.rfid_info_label = tk.Label(rfid_frame, text="Tap authorized RFID card to unlock when locked", 
                                       font=('Arial', 14), bg='#f0f0f0')
        self.rfid_info_label.pack(pady=5)
        
        # Counters
        counters_frame = tk.Frame(main_frame, bg='#f0f0f0')
        counters_frame.pack(pady=20)
        
        self.good_counter_label = tk.Label(counters_frame, text="GOOD Count: 0", 
                                          font=('Arial', 18, 'bold'), 
                                          bg='#d4edda', fg='#155724',
                                          relief='raised', borderwidth=3)
        self.good_counter_label.pack(side='left', padx=20)
        
        self.not_good_counter_label = tk.Label(counters_frame, text="NOT GOOD Count: 0", 
                                              font=('Arial', 18, 'bold'), 
                                              bg='#f8d7da', fg='#721c24',
                                              relief='raised', borderwidth=3)
        self.not_good_counter_label.pack(side='left', padx=20)
        
        # Wire pairs info
        pairs_frame = tk.LabelFrame(main_frame, text="Wire Pairs Configuration", 
                                   font=('Arial', 14, 'bold'), bg='#f0f0f0')
        pairs_frame.pack(fill='x', pady=(0, 20))
        
        pairs_text = "\\n".join([f"Pair {i+1}: GPIO{out} ↔ GPIO{inp}" 
                                for i, (out, inp) in enumerate(WIRE_PAIRS)])
        
        pairs_info = tk.Label(pairs_frame, text=pairs_text, 
                             font=('Arial', 14), bg='#f0f0f0')
        pairs_info.pack(pady=10)
        
        # RFID Management
        rfid_mgmt_frame = tk.Frame(main_frame, bg='#f0f0f0')
        rfid_mgmt_frame.pack(pady=20)
        
        manage_cards_btn = tk.Button(rfid_mgmt_frame, text="🔐 Manage RFID Cards", 
                                    font=('Arial', 14, 'bold'),
                                    bg='#343a40', fg='white',
                                    width=20, height=2,
                                    command=self.manage_rfid_cards)
        manage_cards_btn.pack(side='left', padx=10)
        
        test_lock_btn = tk.Button(rfid_mgmt_frame, text="🧪 Test Lock", 
                                 font=('Arial', 14, 'bold'),
                                 bg='#dc3545', fg='white',
                                 width=15, height=2,
                                 command=self.test_lock)
        test_lock_btn.pack(side='left', padx=10)
        
        # Status info
        info_frame = tk.LabelFrame(main_frame, text="System Information", 
                                  font=('Arial', 14, 'bold'), bg='#f0f0f0')
        info_frame.pack(fill='x', pady=(0, 20))
        
        info_text = """🔒 RFID Locking System Active
• GOOD status: Solenoids enabled
• NOT GOOD status: Solenoids LOCKED (requires RFID unlock)
• OPEN status: Solenoids disabled (no lock)
• Tap authorized RFID card to unlock when locked"""
        
        info_label = tk.Label(info_frame, text=info_text, 
                             font=('Arial', 12), bg='#f0f0f0', justify='left')
        info_label.pack(pady=10)
        
        # Back button
        back_btn = tk.Button(main_frame, text="🔙 Back to Main", 
                            font=('Arial', 14, 'bold'),
                            bg='#6c757d', fg='white',
                            width=20, height=2,
                            command=self.back_to_main)
        back_btn.pack(pady=20)
        
        # Start updating UI
        self.update_ui()
    
    def update_ui(self):
        """Update UI with current status"""
        with status_lock:
            status = current_status
        
        # Update status label
        self.status_label.config(text=status)
        
        # Update colors based on status
        if status == "GOOD":
            self.status_label.config(bg='#d4edda', fg='#155724')
        elif status == "OPEN":
            self.status_label.config(bg='#fff3cd', fg='#856404')
        elif status == "NOT GOOD":
            self.status_label.config(bg='#f8d7da', fg='#721c24')
        else:  # INITIALIZING
            self.status_label.config(bg='#e2e3e5', fg='#383d41')
        
        # Update counters
        self.good_counter_label.config(text=f"GOOD Count: {good_counter}")
        self.not_good_counter_label.config(text=f"NOT GOOD Count: {not_good_counter}")
        
        # Update RFID lock status
        lock_status = lock_manager.get_lock_status()
        if lock_status['is_locked']:
            self.lock_status_label.config(text="🔒 LOCKED", bg='#f8d7da', fg='#721c24')
            self.rfid_info_label.config(text=f"LOCKED: {lock_status['lock_reason']}")
        else:
            self.lock_status_label.config(text="🔓 UNLOCKED", bg='#d4edda', fg='#155724')
            self.rfid_info_label.config(text="System ready - solenoids can be controlled")
        
        # Schedule next update
        self.root.after(500, self.update_ui)
    
    def manage_rfid_cards(self):
        """Open RFID card management"""
        try:
            import subprocess
            import sys
            subprocess.Popen([sys.executable, 'rfid_card_manager.py'])
        except Exception as e:
            print(f"Error opening RFID manager: {e}")
    
    def test_lock(self):
        """Test lock functionality"""
        if lock_manager.is_locked:
            tk.messagebox.showinfo("Already Locked", 
                                  "System is already locked. Tap authorized RFID card to unlock.")
        else:
            lock_manager.lock_solenoids("Manual test lock")
            tk.messagebox.showinfo("Test Lock", 
                                  "Solenoids locked for testing. Tap authorized RFID card to unlock.")
    
    def back_to_main(self):
        """Return to main menu"""
        try:
            self.root.destroy()
            
            import subprocess
            import sys
            subprocess.run([sys.executable, 'wire_checker_main_windows.py'])
            
        except Exception as e:
            print(f"Error returning to main menu: {e}")

def main():
    # Start wire checker thread
    wire_checker_thread = threading.Thread(target=wire_checker_loop, daemon=True)
    wire_checker_thread.start()
    
    # Create UI
    root = tk.Tk()
    app = WireCheckerRFIDUI(root)
    
    def on_closing():
        if RASPBERRY_PI:
            GPIO.output(RED_LED, GPIO.LOW)
            GPIO.output(GREEN_LED, GPIO.LOW)
            GPIO.output(YELLOW_LED, GPIO.LOW)
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()