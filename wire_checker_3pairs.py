import RPi.GPIO as GPIO
import time
import threading
import tkinter as tk
from tkinter import ttk
import os
import subprocess
import sys
from database_manager import DatabaseManager

# GPIO pin assignments
RED_LED = 2
YELLOW_LED = 3
GREEN_LED = 4
BUZZER = 18
SOLENOID = 13
SOLENOID2 = 15

# Wire pairs (output, input) - 3 pairs only
WIRE_PAIRS = [
    (17, 27),  # Pair 1
    (22, 10),  # Pair 2
    (9, 11)    # Pair 3
]

# Global variables for status
current_status = "INITIALIZING"
status_lock = threading.Lock()
buzzer_lock = threading.Lock()

# Cycle management
cycle_id = os.environ.get('WIRE_CHECKER_CYCLE_ID', None)
db_manager = DatabaseManager() if cycle_id else None

# Counters
good_counter = 0
not_good_counter = 0

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(SOLENOID, GPIO.OUT)
GPIO.setup(SOLENOID2, GPIO.OUT)

# Setup all output pins
for output_pin, input_pin in WIRE_PAIRS:
    GPIO.setup(output_pin, GPIO.OUT)
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize buzzer and solenoid to silent/off state
GPIO.output(BUZZER, GPIO.HIGH)
GPIO.output(SOLENOID, GPIO.HIGH)
GPIO.output(SOLENOID2, GPIO.HIGH)

def buzzer_control(enable):
    """Control buzzer - True to turn on, False to turn off"""
    with buzzer_lock:
        if enable:
            GPIO.output(BUZZER, GPIO.LOW)
        else:
            GPIO.output(BUZZER, GPIO.HIGH)

def solenoid_control(enable):
    """Control solenoid - True to turn on, False to turn off"""
    if enable:
        GPIO.output(SOLENOID, GPIO.HIGH)
    else:
        GPIO.output(SOLENOID, GPIO.LOW)

def solenoid2_control(enable):
    """Control solenoid2 - True to turn on, False to turn off"""
    if enable:
        GPIO.output(SOLENOID2, GPIO.HIGH)
    else:
        GPIO.output(SOLENOID2, GPIO.LOW)

def beep_once():
    """Make one beep sound"""
    buzzer_control(True)
    time.sleep(0.1)
    buzzer_control(False)

def beep_multiple(times):
    """Make multiple beep sounds"""
    for _ in range(times):
        beep_once()
        time.sleep(0.1)  # Small pause between beeps

def test_wire_pair(output_pin, input_pin):
    """Test if a wire pair is properly connected"""
    # Send HIGH signal
    GPIO.output(output_pin, GPIO.HIGH)
    time.sleep(0.01)
    high_received = GPIO.input(input_pin)
    
    # Send LOW signal
    GPIO.output(output_pin, GPIO.LOW)
    time.sleep(0.01)
    low_received = GPIO.input(input_pin)
    
    # Return True if properly connected (HIGH when output is HIGH, LOW when output is LOW)
    return high_received and not low_received

def test_cross_connections():
    """Test for cross connections between different pairs"""
    cross_connections = []
    
    # Test if output from one pair affects input of another pair
    for i, (out1, in1) in enumerate(WIRE_PAIRS):
        for j, (out2, in2) in enumerate(WIRE_PAIRS):
            if i != j:  # Don't test same pair
                # Test if output from pair i affects input of pair j
                GPIO.output(out1, GPIO.HIGH)
                time.sleep(0.01)
                if GPIO.input(in2):  # Cross connection detected
                    cross_connections.append((i, j))
                GPIO.output(out1, GPIO.LOW)
                time.sleep(0.01)
    
    return cross_connections

def test_in_to_in_connections():
    """Test if any input pins are connected to each other"""
    input_pins = [in_pin for _, in_pin in WIRE_PAIRS]
    in_to_in_connections = []
    
    for i, in1 in enumerate(input_pins):
        for j, in2 in enumerate(input_pins):
            if i != j:
                # Set one input as output temporarily to test connection
                GPIO.setup(in1, GPIO.OUT)
                GPIO.output(in1, GPIO.HIGH)
                time.sleep(0.01)
                if GPIO.input(in2):  # IN-to-IN connection detected
                    in_to_in_connections.append((i, j))
                GPIO.output(in1, GPIO.LOW)
                GPIO.setup(in1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Restore as input
    
    return in_to_in_connections

def test_out_to_out_connections():
    """Test if any output pins are connected to each other"""
    output_pins = [out_pin for out_pin, _ in WIRE_PAIRS]
    out_to_out_connections = []
    
    for i, out1 in enumerate(output_pins):
        for j, out2 in enumerate(output_pins):
            if i != j:
                # Set one output to HIGH, other to LOW, then check if they're connected
                GPIO.output(out1, GPIO.HIGH)
                GPIO.output(out2, GPIO.LOW)
                time.sleep(0.01)
                
                # If they're connected, the HIGH should override the LOW
                # We can detect this by temporarily setting out2 as input
                GPIO.setup(out2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                time.sleep(0.01)
                if GPIO.input(out2):  # OUT-to-OUT connection detected
                    out_to_out_connections.append((i, j))
                GPIO.setup(out2, GPIO.OUT)  # Restore as output
                GPIO.output(out2, GPIO.LOW)
    
    return out_to_out_connections

def wire_checker_loop():
    """Main wire checker loop running in background thread"""
    global current_status, good_counter, not_good_counter
    previous_status = None
    
    while True:
        try:
            # Test each pair individually
            pair_results = []
            for output_pin, input_pin in WIRE_PAIRS:
                is_connected = test_wire_pair(output_pin, input_pin)
                pair_results.append(is_connected)
            
            # Test for various types of cross connections
            cross_connections = test_cross_connections()
            in_to_in_connections = test_in_to_in_connections()
            out_to_out_connections = test_out_to_out_connections()
            
            # Determine status
            all_connected = all(pair_results)
            any_open = not all_connected
            has_cross_connections = (len(cross_connections) > 0 or 
                                   len(in_to_in_connections) > 0 or 
                                   len(out_to_out_connections) > 0)
            
            with status_lock:
                if has_cross_connections:
                    current_status = "NOT GOOD"
                    GPIO.output(RED_LED, GPIO.HIGH)
                    GPIO.output(GREEN_LED, GPIO.LOW)
                    GPIO.output(YELLOW_LED, GPIO.LOW)
                    solenoid_control(True)  # Turn off solenoid
                    solenoid2_control(False)  # Turn on solenoid2
                elif all_connected:
                    current_status = "GOOD"
                    GPIO.output(GREEN_LED, GPIO.HIGH)
                    GPIO.output(RED_LED, GPIO.LOW)
                    GPIO.output(YELLOW_LED, GPIO.LOW)
                    solenoid_control(False)   # Turn on solenoid
                    solenoid2_control(True)  # Turn off solenoid2
                else:
                    current_status = "OPEN"
                    GPIO.output(YELLOW_LED, GPIO.HIGH)
                    GPIO.output(RED_LED, GPIO.LOW)
                    GPIO.output(GREEN_LED, GPIO.LOW)
                    solenoid_control(False)  # Turn off solenoid
                    solenoid2_control(False)  # Turn off solenoid2
                # Only beep when status changes
                if current_status != previous_status:
                    if current_status == "GOOD":
                        beep_once()
                    elif current_status == "NOT GOOD":
                        beep_multiple(5)
                    # No beep for OPEN or INITIALIZING
                
                # Update cycle counts in database
                if db_manager and cycle_id and current_status != previous_status:
                    if current_status in ["GOOD", "NOT GOOD", "OPEN"]:
                        db_manager.update_cycle_count(cycle_id, current_status)
                
                # Increment local counters only when transitioning from OPEN
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

class WireCheckerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wire Checker Status - 3 Pairs")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Create main frame
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Title
        title_label = tk.Label(main_frame, text="Wire Checker Status - 3 Pairs", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 30))
        
        # Status display
        self.status_label = tk.Label(main_frame, text="INITIALIZING", 
                                    font=('Arial', 36, 'bold'), 
                                    width=20, height=4,
                                    relief='raised', borderwidth=4)
        self.status_label.pack(pady=30)
        
        # Solenoid status
        self.solenoid_label = tk.Label(main_frame, text="Solenoid: OFF", 
                                      font=('Arial', 18, 'bold'), 
                                      bg='#f0f0f0', fg='#dc3545')
        self.solenoid_label.pack(pady=(0, 20))
        
        # Cycle information
        if cycle_id:
            cycle_info = f"Cycle ID: {cycle_id[:8]}..."
            self.cycle_label = tk.Label(main_frame, text=cycle_info, 
                                       font=('Arial', 16, 'bold'), 
                                       bg='#e3f2fd', fg='#1565c0',
                                       relief='raised', borderwidth=2)
            self.cycle_label.pack(pady=(0, 20))
        
        # Counters frame
        counters_frame = tk.Frame(main_frame, bg='#f0f0f0')
        counters_frame.pack(pady=(0, 20))
        
        # Good counter
        self.good_counter_label = tk.Label(counters_frame, text="GOOD Count: 0", 
                                          font=('Arial', 16, 'bold'), 
                                          bg='#d4edda', fg='#155724',
                                          relief='raised', borderwidth=2)
        self.good_counter_label.pack(side='left', padx=(0, 20))
        
        # NOT GOOD counter
        self.not_good_counter_label = tk.Label(counters_frame, text="NOT GOOD Count: 0", 
                                              font=('Arial', 16, 'bold'), 
                                              bg='#f8d7da', fg='#721c24',
                                              relief='raised', borderwidth=2)
        self.not_good_counter_label.pack(side='left')
        
        # Last updated label
        self.last_updated_label = tk.Label(main_frame, text="Last updated: -", 
                                          font=('Arial', 14), bg='#f0f0f0')
        self.last_updated_label.pack(pady=(20, 0))
        
        # Wire pairs info
        pairs_frame = tk.Frame(main_frame, bg='#f0f0f0')
        pairs_frame.pack(pady=(30, 0))
        
        pairs_label = tk.Label(pairs_frame, text="Wire Pairs:", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        pairs_label.pack()
        
        pairs_info = tk.Label(pairs_frame, 
                             text="GPIO17 ↔ GPIO27\nGPIO22 ↔ GPIO10\nGPIO9 ↔ GPIO11", 
                             font=('Arial', 14), bg='#f0f0f0', justify='left')
        pairs_info.pack()
        
        # Close cycle button
        if cycle_id:
            close_btn = tk.Button(main_frame, text="Close Cycle", 
                                 font=('Arial', 18, 'bold'),
                                 width=20, height=2,
                                 bg='#dc3545', fg='white',
                                 relief='raised', borderwidth=3,
                                 command=self.close_cycle)
            close_btn.pack(pady=(30, 0))
        
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
        
        # Update cycle information from database
        if db_manager and cycle_id:
            cycle_data = db_manager.get_current_cycle(cycle_id)
            if cycle_data:
                cycle_info = f"Cycle: {cycle_id[:8]}... | Total: {cycle_data['total_checked']} | Good: {cycle_data['good_count']} | Not Good: {cycle_data['not_good_count']}"
                self.cycle_label.config(text=cycle_info)
        
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
    
    def close_cycle(self):
        """Close the current cycle and return to main menu"""
        if db_manager and cycle_id:
            # End the cycle in database
            db_manager.end_cycle(cycle_id)
            
            # Show completion message
            import tkinter.messagebox as messagebox
            cycle_data = db_manager.get_current_cycle(cycle_id)
            if cycle_data:
                message = f"Cycle completed!\n\nTotal Checked: {cycle_data['total_checked']}\nGood: {cycle_data['good_count']}\nNot Good: {cycle_data['not_good_count']}\nOpen: {cycle_data['open_count']}"
                messagebox.showinfo("Cycle Complete", message)
            
            # Close current window and return to main menu
            self.root.destroy()
            subprocess.run([sys.executable, 'wire_checker_main.py'])

def main():
    # Start the wire checker in a background thread
    wire_checker_thread = threading.Thread(target=wire_checker_loop, daemon=True)
    wire_checker_thread.start()
    
    # Create and run the Tkinter UI
    root = tk.Tk()
    app = WireCheckerUI(root)
    
    # Handle window close
    def on_closing():
        print("Closing Wire Checker...")
        buzzer_control(False)  # Ensure buzzer is off
        solenoid_control(False)  # Ensure solenoid is off
        solenoid2_control(False)  # Ensure solenoid2 is off
        GPIO.output(RED_LED, GPIO.LOW)
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(YELLOW_LED, GPIO.LOW)
        # GPIO.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    print("Wire Checker UI starting...")
    root.mainloop()

if __name__ == '__main__':
    main()
