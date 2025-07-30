import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import time
import threading

# Handle GPIO import for Windows testing
try:
    import RPi.GPIO as GPIO
    RASPBERRY_PI = True
except ImportError:
    print("RPi.GPIO not found. Running in Windows test mode.")
    from mock_gpio import GPIO
    RASPBERRY_PI = False

class AutoPinDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Pin Detection - Teaching Mode")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Detection state
        self.is_detecting = False
        self.detected_pairs = []
        self.available_pins = [5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27]
        self.reserved_pins = [2, 3, 4, 13, 15, 18]  # LEDs, solenoids, buzzer
        
        # Setup GPIO
        if RASPBERRY_PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            self.setup_gpio_pins()
        
        self.create_widgets()
    
    def setup_gpio_pins(self):
        """Setup GPIO pins for detection"""
        for pin in self.available_pins:
            try:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            except:
                pass
    
    def create_widgets(self):
        # Main frame with scrolling
        canvas = tk.Canvas(self.root, bg='#f0f0f0')
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        scrollbar.pack(side="right", fill="y", pady=30)
        
        main_frame = scrollable_frame
        
        # Title
        title_label = tk.Label(main_frame, text="🔍 Auto Pin Detection - Teaching Mode", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(10, 20))
        
        # Instructions
        instructions_frame = tk.LabelFrame(main_frame, text="Instructions", 
                                         font=('Arial', 14, 'bold'), bg='#f0f0f0')
        instructions_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        instructions_text = """1. Connect your sample wire assembly to any available GPIO pins
2. Click "START TEACHING" to begin auto detection
3. System will scan all pins and detect connections
4. Review detected pin pairs
5. Enter product information and save configuration"""
        
        tk.Label(instructions_frame, text=instructions_text, 
                font=('Arial', 12), bg='#f0f0f0', justify='left').pack(padx=10, pady=10)
        
        # Detection control
        control_frame = tk.LabelFrame(main_frame, text="Detection Control", 
                                    font=('Arial', 14, 'bold'), bg='#f0f0f0')
        control_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        # Start/Stop buttons
        buttons_frame = tk.Frame(control_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=10)
        
        self.start_btn = tk.Button(buttons_frame, text="🎯 START TEACHING", 
                                  font=('Arial', 16, 'bold'),
                                  bg='#28a745', fg='white',
                                  width=20, height=2,
                                  command=self.start_detection)
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(buttons_frame, text="⏹️ STOP", 
                                 font=('Arial', 16, 'bold'),
                                 bg='#dc3545', fg='white',
                                 width=15, height=2,
                                 command=self.stop_detection,
                                 state='disabled')
        self.stop_btn.pack(side='left', padx=10)
        
        # Status display
        self.status_label = tk.Label(control_frame, text="Ready to start detection", 
                                    font=('Arial', 14, 'bold'), 
                                    bg='#e2e3e5', fg='#383d41',
                                    relief='raised', borderwidth=2)
        self.status_label.pack(pady=10)
        
        # Detection results
        results_frame = tk.LabelFrame(main_frame, text="Detected Pin Pairs", 
                                    font=('Arial', 14, 'bold'), bg='#f0f0f0')
        results_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        # Results display
        self.results_text = tk.Text(results_frame, height=8, width=60,
                                   font=('Arial', 12), bg='#f8f9fa',
                                   relief='sunken', borderwidth=2)
        self.results_text.pack(pady=10, padx=10)
        
        # Product information
        product_frame = tk.LabelFrame(main_frame, text="Product Information", 
                                    font=('Arial', 14, 'bold'), bg='#f0f0f0')
        product_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        # Product name
        tk.Label(product_frame, text="Product Name:", font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.product_name_entry = tk.Entry(product_frame, font=('Arial', 12), width=30)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Product number
        tk.Label(product_frame, text="Product No:", font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.product_no_entry = tk.Entry(product_frame, font=('Arial', 12), width=30)
        self.product_no_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Save button
        save_frame = tk.Frame(main_frame, bg='#f0f0f0')
        save_frame.pack(pady=20)
        
        self.save_btn = tk.Button(save_frame, text="💾 SAVE CONFIGURATION", 
                                 font=('Arial', 16, 'bold'),
                                 bg='#007bff', fg='white',
                                 width=25, height=2,
                                 command=self.save_configuration,
                                 state='disabled')
        self.save_btn.pack(side='left', padx=10)
        
        # Back button
        back_btn = tk.Button(save_frame, text="🔙 Back to Main", 
                            font=('Arial', 14, 'bold'),
                            bg='#6c757d', fg='white',
                            width=20, height=2,
                            command=self.back_to_main)
        back_btn.pack(side='left', padx=10)
    
    def start_detection(self):
        """Start auto pin detection"""
        self.is_detecting = True
        self.detected_pairs = []
        
        # Update UI
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_label.config(text="🔍 Detecting pins... Please wait", bg='#fff3cd', fg='#856404')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Scanning GPIO pins...\n")
        
        # Start detection in separate thread
        detection_thread = threading.Thread(target=self.detect_pins, daemon=True)
        detection_thread.start()
    
    def stop_detection(self):
        """Stop auto pin detection"""
        self.is_detecting = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="Detection stopped", bg='#f8d7da', fg='#721c24')
    
    def detect_pins(self):
        """Main detection logic"""
        try:
            self.update_results("Starting pin detection...\n")
            
            # Test all possible pin combinations
            detected_connections = []
            
            for out_pin in self.available_pins:
                if not self.is_detecting:
                    break
                    
                self.update_results(f"Testing GPIO{out_pin} as output...\n")
                
                try:
                    # Set as output
                    GPIO.setup(out_pin, GPIO.OUT)
                    
                    # Test with other pins as input
                    for in_pin in self.available_pins:
                        if in_pin == out_pin or not self.is_detecting:
                            continue
                        
                        try:
                            # Set as input
                            GPIO.setup(in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                            
                            # Test connection
                            if self.test_connection(out_pin, in_pin):
                                connection = (out_pin, in_pin)
                                if connection not in detected_connections:
                                    detected_connections.append(connection)
                                    self.update_results(f"✅ Found connection: GPIO{out_pin} → GPIO{in_pin}\n")
                            
                        except Exception as e:
                            continue
                    
                    # Reset pin
                    GPIO.setup(out_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                    
                except Exception as e:
                    continue
                
                time.sleep(0.1)  # Small delay
            
            # Process results
            if detected_connections:
                self.detected_pairs = detected_connections
                self.update_results(f"\n🎉 Detection complete! Found {len(detected_connections)} connections.\n")
                self.status_label.config(text=f"✅ Found {len(detected_connections)} pin pairs", 
                                       bg='#d4edda', fg='#155724')
                self.save_btn.config(state='normal')
            else:
                self.update_results("\n⚠️ No connections detected. Please check your wiring.\n")
                self.status_label.config(text="❌ No connections found", bg='#f8d7da', fg='#721c24')
            
        except Exception as e:
            self.update_results(f"\n❌ Error during detection: {e}\n")
            self.status_label.config(text="❌ Detection error", bg='#f8d7da', fg='#721c24')
        
        finally:
            self.is_detecting = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
    
    def test_connection(self, out_pin, in_pin):
        """Test if two pins are connected"""
        try:
            # Send HIGH signal
            GPIO.output(out_pin, GPIO.HIGH)
            time.sleep(0.01)
            high_received = GPIO.input(in_pin)
            
            # Send LOW signal  
            GPIO.output(out_pin, GPIO.LOW)
            time.sleep(0.01)
            low_received = GPIO.input(in_pin)
            
            # Connection exists if input follows output
            return high_received and not low_received
            
        except:
            return False
    
    def update_results(self, text):
        """Update results display"""
        def update():
            self.results_text.insert(tk.END, text)
            self.results_text.see(tk.END)
            self.root.update()
        
        self.root.after(0, update)
    
    def save_configuration(self):
        """Save detected configuration"""
        if not self.detected_pairs:
            messagebox.showwarning("No Data", "No pin pairs detected to save.")
            return
        
        product_name = self.product_name_entry.get().strip()
        product_no = self.product_no_entry.get().strip()
        
        if not product_name or not product_no:
            messagebox.showerror("Missing Info", "Please enter Product Name and Product No.")
            return
        
        # Create configuration
        config_data = {
            'product_name': product_name,
            'product_no': product_no,
            'wire_pairs': [],
            'detection_method': 'auto_detect',
            'detected_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        for i, (out_pin, in_pin) in enumerate(self.detected_pairs):
            config_data['wire_pairs'].append({
                'pair_number': i + 1,
                'pin_out': out_pin,
                'pin_in': in_pin
            })
        
        # Save to file
        config_file = f'auto_detected_{product_no.replace("-", "_").lower()}.json'
        try:
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
            
            # Generate custom checker
            self.generate_custom_checker(config_data)
            
            messagebox.showinfo("Success", 
                              f"Configuration saved!\n\n"
                              f"Product: {product_name}\n"
                              f"Part No: {product_no}\n"
                              f"Pin Pairs: {len(self.detected_pairs)}\n"
                              f"File: {config_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def generate_custom_checker(self, config_data):
        """Generate custom wire checker from detected configuration"""
        wire_pairs = [(pair['pin_out'], pair['pin_in']) for pair in config_data['wire_pairs']]
        product_name = config_data['product_name']
        product_no = config_data['product_no']
        
        custom_code = f'''# Auto-Detected Wire Checker for {product_name} ({product_no})
# Generated by Auto Pin Detection on {config_data['detected_at']}

# Handle GPIO import for Windows testing
try:
    import RPi.GPIO as GPIO
    RASPBERRY_PI = True
except ImportError:
    from mock_gpio import GPIO
    RASPBERRY_PI = False

import time
import threading
import tkinter as tk

# Product Information
PRODUCT_NAME = "{product_name}"
PRODUCT_NO = "{product_no}"

# Auto-detected wire pairs (output, input)
WIRE_PAIRS = {wire_pairs}

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup pins
for output_pin, input_pin in WIRE_PAIRS:
    GPIO.setup(output_pin, GPIO.OUT)
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def test_wire_pair(output_pin, input_pin):
    """Test if a wire pair is properly connected"""
    GPIO.output(output_pin, GPIO.HIGH)
    time.sleep(0.01)
    high_received = GPIO.input(input_pin)
    
    GPIO.output(output_pin, GPIO.LOW)
    time.sleep(0.01)
    low_received = GPIO.input(input_pin)
    
    return high_received and not low_received

def main():
    print(f"Auto-Detected Wire Checker: {{PRODUCT_NAME}} ({{PRODUCT_NO}})")
    print(f"Detected {{len(WIRE_PAIRS)}} wire pairs:")
    for i, (out, inp) in enumerate(WIRE_PAIRS, 1):
        print(f"  Pair {{i}}: GPIO{{out}} → GPIO{{inp}}")
    
    print("\\nTesting connections...")
    while True:
        all_good = True
        for i, (out_pin, in_pin) in enumerate(WIRE_PAIRS, 1):
            connected = test_wire_pair(out_pin, in_pin)
            status = "✅ GOOD" if connected else "❌ OPEN"
            print(f"Pair {{i}} (GPIO{{out_pin}}→GPIO{{in_pin}}): {{status}}")
            if not connected:
                all_good = False
        
        overall = "🟢 ALL GOOD" if all_good else "🟡 CHECK CONNECTIONS"
        print(f"Overall Status: {{overall}}\\n")
        time.sleep(1)

if __name__ == '__main__':
    main()
'''
        
        # Save custom checker
        custom_file = f'wire_checker_auto_{product_no.replace("-", "_").lower()}.py'
        with open(custom_file, 'w') as f:
            f.write(custom_code)
    
    def back_to_main(self):
        """Return to main menu"""
        try:
            if RASPBERRY_PI:
                GPIO.cleanup()
            self.root.destroy()
            
            import subprocess
            import sys
            subprocess.run([sys.executable, 'wire_checker_main_windows.py'])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return to main menu: {e}")

def main():
    root = tk.Tk()
    app = AutoPinDetector(root)
    root.mainloop()

if __name__ == '__main__':
    main()