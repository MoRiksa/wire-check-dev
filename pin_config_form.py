import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import re
import subprocess
import sys
import glob
from responsive_ui_base import ResponsiveUI

# Handle GPIO import for Windows testing
try:
    import RPi.GPIO as GPIO
    RASPBERRY_PI = True
except ImportError:
    print("RPi.GPIO not found. Running in Windows test mode.")
    from mock_gpio import GPIO
    RASPBERRY_PI = False

class PinConfigForm(ResponsiveUI):
    def __init__(self, root):
        super().__init__()
        self.root = root
        
        # Setup responsive window
        self.window_width, self.window_height = self.setup_responsive_window(
            root, "Pin Configuration Form", 900, 700
        )
        
        self.root.configure(bg='#f0f0f0')
        
        # Configuration data
        self.config_data = {
            'product_name': '',
            'product_no': '',
            'wire_pairs': []
        }
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        self.create_widgets()
        self.load_existing_config()
    
    def create_widgets(self):
        # Create scrollable frame using responsive UI base
        container, main_frame = self.create_scrollable_frame(self.root, bg='#f0f0f0')
        container.pack(fill='both', expand=True, padx=self.get_padding(20), pady=self.get_padding(20))
        
        # Title
        title_label = self.create_responsive_label(main_frame, "Wire Checker Pin Configuration", 
                                                  style="title", bg='#f0f0f0')
        title_label.pack(pady=(self.get_padding(10), self.get_padding(15)))
        
        # Product info frame
        product_frame = self.create_responsive_labelframe(main_frame, "Product Information", bg='#f0f0f0')
        product_frame.pack(fill='x', pady=(0, self.get_padding(15)), padx=self.get_padding(10))
        
        # Configure grid weights for responsiveness
        product_frame.grid_columnconfigure(1, weight=1)
        
        # Product name
        name_label = self.create_responsive_label(product_frame, "Product Name:", style="normal", bg='#f0f0f0')
        name_label.grid(row=0, column=0, sticky='w', padx=self.get_padding(10), pady=self.get_padding(8))
        self.product_name_entry = self.create_responsive_entry(product_frame, width=25)
        self.product_name_entry.grid(row=0, column=1, sticky='ew', padx=self.get_padding(10), pady=self.get_padding(8))
        
        # Product number
        no_label = self.create_responsive_label(product_frame, "Product No:", style="normal", bg='#f0f0f0')
        no_label.grid(row=1, column=0, sticky='w', padx=self.get_padding(10), pady=self.get_padding(8))
        self.product_no_entry = self.create_responsive_entry(product_frame, width=25)
        self.product_no_entry.grid(row=1, column=1, sticky='ew', padx=self.get_padding(10), pady=self.get_padding(8))
        
        # Wire pairs frame
        pairs_frame = tk.LabelFrame(main_frame, text="Wire Pair Configuration", 
                                   font=('Arial', 14, 'bold'), bg='#f0f0f0')
        pairs_frame.pack(fill='x', pady=(0, 15), padx=10)
        
        # Headers
        tk.Label(pairs_frame, text="Pair", font=('Arial', 14, 'bold'), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=5)
        tk.Label(pairs_frame, text="PIN OUT (GPIO)", font=('Arial', 14, 'bold'), bg='#f0f0f0').grid(row=0, column=1, padx=10, pady=5)
        tk.Label(pairs_frame, text="PIN IN (GPIO)", font=('Arial', 14, 'bold'), bg='#f0f0f0').grid(row=0, column=2, padx=10, pady=5)
        
        # Wire pair entries
        self.pair_entries = []
        for i in range(6):  # Support up to 6 pairs
            pair_label = tk.Label(pairs_frame, text=f"Pair {i+1}:", font=('Arial', 12), bg='#f0f0f0')
            pair_label.grid(row=i+1, column=0, padx=10, pady=5)
            
            pin_out_entry = tk.Entry(pairs_frame, font=('Arial', 12), width=15)
            pin_out_entry.grid(row=i+1, column=1, padx=10, pady=5)
            
            pin_in_entry = tk.Entry(pairs_frame, font=('Arial', 12), width=15)
            pin_in_entry.grid(row=i+1, column=2, padx=10, pady=5)
            
            self.pair_entries.append((pin_out_entry, pin_in_entry))
        
        # Template info
        template_frame = tk.LabelFrame(main_frame, text="Template Example", 
                                      font=('Arial', 12, 'bold'), bg='#f0f0f0')
        template_frame.pack(fill='x', pady=(0, 15), padx=10)
        
        template_text = """Example Configuration:
Product Name: Test Wire Assembly
Product No: TWA-001
Pair 1: GPIO17 → GPIO27
Pair 2: GPIO22 → GPIO10
Pair 3: GPIO9 → GPIO11
Pair 4: GPIO5 → GPIO6"""
        
        tk.Label(template_frame, text=template_text, font=('Arial', 10), 
                bg='#f0f0f0', justify='left').pack(padx=10, pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=15, padx=10)
        
        # Save button
        save_btn = tk.Button(buttons_frame, text="Save Configuration", 
                            font=('Arial', 14, 'bold'),
                            bg='#28a745', fg='white',
                            width=20, height=2,
                            command=self.save_config)
        save_btn.pack(side='left', padx=10)
        
        # Load template button
        template_btn = tk.Button(buttons_frame, text="Load Template", 
                                font=('Arial', 14, 'bold'),
                                bg='#007bff', fg='white',
                                width=20, height=2,
                                command=self.load_template)
        template_btn.pack(side='left', padx=10)
        
        # Load from file button
        load_file_btn = tk.Button(buttons_frame, text="Load from File", 
                                 font=('Arial', 14, 'bold'),
                                 bg='#6c757d', fg='white',
                                 width=20, height=2,
                                 command=self.load_from_file)
        load_file_btn.pack(side='left', padx=10)
        
        # Clear button
        clear_btn = tk.Button(buttons_frame, text="Clear All", 
                             font=('Arial', 14, 'bold'),
                             bg='#dc3545', fg='white',
                             width=20, height=2,
                             command=self.clear_form)
        clear_btn.pack(side='left', padx=10)
        
        # Apply button
        apply_btn = tk.Button(buttons_frame, text="Apply & Test", 
                             font=('Arial', 14, 'bold'),
                             bg='#17a2b8', fg='white',
                             width=20, height=2,
                             command=self.apply_config)
        apply_btn.pack(side='left', padx=10)
        
        # Second row of buttons
        buttons_frame2 = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame2.pack(pady=10, padx=10)
        
        # Create template button
        create_template_btn = tk.Button(buttons_frame2, text="Create Template", 
                                       font=('Arial', 14, 'bold'),
                                       bg='#20c997', fg='white',
                                       width=20, height=2,
                                       command=self.create_template_file)
        create_template_btn.pack(side='left', padx=10)
        
        # Run custom checker button
        run_custom_btn = tk.Button(buttons_frame2, text="Run Custom Checker", 
                                  font=('Arial', 14, 'bold'),
                                  bg='#e83e8c', fg='white',
                                  width=20, height=2,
                                  command=self.run_custom_checker)
        run_custom_btn.pack(side='left', padx=10)
        
        # Back to main button
        back_btn = tk.Button(buttons_frame2, text="Back to Main", 
                            font=('Arial', 14, 'bold'),
                            bg='#6c757d', fg='white',
                            width=20, height=2,
                            command=self.back_to_main)
        back_btn.pack(side='left', padx=10)
    
    def load_template(self):
        """Load default template configuration"""
        self.product_name_entry.delete(0, tk.END)
        self.product_name_entry.insert(0, "Test Wire Assembly")
        
        self.product_no_entry.delete(0, tk.END)
        self.product_no_entry.insert(0, "TWA-001")
        
        # Default 4-pair configuration
        default_pairs = [(17, 27), (22, 10), (9, 11), (5, 6)]
        
        for i, (out_pin, in_pin) in enumerate(default_pairs):
            if i < len(self.pair_entries):
                self.pair_entries[i][0].delete(0, tk.END)
                self.pair_entries[i][0].insert(0, str(out_pin))
                self.pair_entries[i][1].delete(0, tk.END)
                self.pair_entries[i][1].insert(0, str(in_pin))
    
    def clear_form(self):
        """Clear all form fields"""
        self.product_name_entry.delete(0, tk.END)
        self.product_no_entry.delete(0, tk.END)
        
        for out_entry, in_entry in self.pair_entries:
            out_entry.delete(0, tk.END)
            in_entry.delete(0, tk.END)
    
    def validate_config(self):
        """Validate the configuration data"""
        # Check product info
        if not self.product_name_entry.get().strip():
            messagebox.showerror("Error", "Product Name is required")
            return False
        
        if not self.product_no_entry.get().strip():
            messagebox.showerror("Error", "Product No is required")
            return False
        
        # Check wire pairs
        wire_pairs = []
        used_pins = set()
        
        for i, (out_entry, in_entry) in enumerate(self.pair_entries):
            out_pin = out_entry.get().strip()
            in_pin = in_entry.get().strip()
            
            if out_pin or in_pin:  # If either field has data
                if not (out_pin and in_pin):
                    messagebox.showerror("Error", f"Pair {i+1}: Both PIN OUT and PIN IN must be specified")
                    return False
                
                try:
                    out_pin_num = int(out_pin)
                    in_pin_num = int(in_pin)
                except ValueError:
                    messagebox.showerror("Error", f"Pair {i+1}: PIN numbers must be integers")
                    return False
                
                if out_pin_num in used_pins or in_pin_num in used_pins:
                    messagebox.showerror("Error", f"Pair {i+1}: PIN {out_pin_num} or {in_pin_num} is already used")
                    return False
                
                used_pins.add(out_pin_num)
                used_pins.add(in_pin_num)
                wire_pairs.append((out_pin_num, in_pin_num))
        
        if not wire_pairs:
            messagebox.showerror("Error", "At least one wire pair must be configured")
            return False
        
        return True
    
    def save_config(self):
        """Save configuration to file"""
        if not self.validate_config():
            return
        
        # Collect data
        self.config_data['product_name'] = self.product_name_entry.get().strip()
        self.config_data['product_no'] = self.product_no_entry.get().strip()
        
        wire_pairs = []
        for i, (out_entry, in_entry) in enumerate(self.pair_entries):
            out_pin = out_entry.get().strip()
            in_pin = in_entry.get().strip()
            
            if out_pin and in_pin:
                wire_pairs.append({
                    'pair_number': i + 1,
                    'pin_out': int(out_pin),
                    'pin_in': int(in_pin)
                })
        
        self.config_data['wire_pairs'] = wire_pairs
        
        # Save to file
        config_file = 'pin_configuration.json'
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config_data, f, indent=4)
            
            messagebox.showinfo("Success", f"Configuration saved to {config_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def load_existing_config(self):
        """Load existing configuration if available"""
        config_file = 'pin_configuration.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    self.config_data = json.load(f)
                
                # Populate form
                self.product_name_entry.insert(0, self.config_data.get('product_name', ''))
                self.product_no_entry.insert(0, self.config_data.get('product_no', ''))
                
                for pair_data in self.config_data.get('wire_pairs', []):
                    pair_num = pair_data['pair_number'] - 1
                    if pair_num < len(self.pair_entries):
                        self.pair_entries[pair_num][0].insert(0, str(pair_data['pin_out']))
                        self.pair_entries[pair_num][1].insert(0, str(pair_data['pin_in']))
                        
            except Exception as e:
                print(f"Error loading existing configuration: {e}")
    
    def load_from_file(self):
        """Load configuration from text file"""
        file_path = filedialog.askopenfilename(
            title="Select Configuration File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="pin_config_template.txt"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Parse the content
            self.parse_template_content(content)
            messagebox.showinfo("Success", "Configuration loaded from file successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def parse_template_content(self, content):
        """Parse template content and populate form"""
        lines = content.split('\n')
        
        # Clear form first
        self.clear_form()
        
        for line in lines:
            line = line.strip()
            
            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue
            
            # Parse product name
            if line.startswith('Product Name:'):
                product_name = line.split(':', 1)[1].strip()
                if not product_name.startswith('['):
                    self.product_name_entry.insert(0, product_name)
            
            # Parse product number
            elif line.startswith('Product No:'):
                product_no = line.split(':', 1)[1].strip()
                if not product_no.startswith('['):
                    self.product_no_entry.insert(0, product_no)
            
            # Parse wire pairs
            elif line.startswith('Pair '):
                # Extract pair number and GPIO pins
                match = re.match(r'Pair (\d+):\s*GPIO(\d+)\s*->\s*GPIO(\d+)', line)
                if match:
                    pair_num = int(match.group(1)) - 1
                    out_pin = match.group(2)
                    in_pin = match.group(3)
                    
                    if pair_num < len(self.pair_entries):
                        self.pair_entries[pair_num][0].insert(0, out_pin)
                        self.pair_entries[pair_num][1].insert(0, in_pin)
    
    def apply_config(self):
        """Apply configuration and start wire checker"""
        if not self.validate_config():
            return
        
        # Save first
        self.save_config()
        
        # Create custom wire checker with this configuration
        self.create_custom_checker()
        
        messagebox.showinfo("Success", "Configuration applied! Custom wire checker created.")
    
    def create_custom_checker(self):
        """Create a custom wire checker based on configuration"""
        # Collect wire pairs
        wire_pairs = []
        for i, (out_entry, in_entry) in enumerate(self.pair_entries):
            out_pin = out_entry.get().strip()
            in_pin = in_entry.get().strip()
            
            if out_pin and in_pin:
                wire_pairs.append((int(out_pin), int(in_pin)))
        
        product_name = self.product_name_entry.get().strip()
        product_no = self.product_no_entry.get().strip()
        
        # Generate custom wire checker file
        custom_checker_code = self.generate_custom_checker_code(wire_pairs, product_name, product_no)
        
        # Save custom checker
        custom_file = f'wire_checker_custom_{product_no.replace("-", "_").lower()}.py'
        try:
            with open(custom_file, 'w') as f:
                f.write(custom_checker_code)
            print(f"Custom wire checker created: {custom_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create custom checker: {e}")
    
    def create_template_file(self):
        """Create a template file for manual editing"""
        file_path = filedialog.asksaveasfilename(
            title="Save Template File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="my_pin_config_template.txt"
        )
        
        if not file_path:
            return
        
        # Get current form data or use template
        product_name = self.product_name_entry.get().strip() or "[Enter your product name here]"
        product_no = self.product_no_entry.get().strip() or "[Enter your product number here]"
        
        template_content = f"""# Wire Checker Pin Configuration Template
# Fill in your configuration below

# Product Information
Product Name: {product_name}
Product No: {product_no}

# Wire Pair Configuration
# Format: Pair X: GPIOX -> GPIOY (where X is OUT pin, Y is IN pin)
"""
        
        # Add current pairs or empty template
        for i in range(6):
            out_pin = self.pair_entries[i][0].get().strip()
            in_pin = self.pair_entries[i][1].get().strip()
            
            if out_pin and in_pin:
                template_content += f"Pair {i+1}: GPIO{out_pin} -> GPIO{in_pin}\n"
            else:
                template_content += f"Pair {i+1}: GPIO__ -> GPIO__\n"
        
        template_content += """
# Instructions:
# 1. Fill in the Product Name and Product No
# 2. Replace __ with actual GPIO pin numbers
# 3. Save this file and use "Load from File" in the Pin Configuration Form
# 4. Each GPIO pin can only be used once
# 5. Avoid pins 2,3,4 (LEDs), 13,15 (solenoids), 18 (buzzer)
"""
        
        try:
            with open(file_path, 'w') as f:
                f.write(template_content)
            
            messagebox.showinfo("Success", f"Template file created: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create template file: {e}")
    
    def run_custom_checker(self):
        """Run the most recently created custom checker"""
        # Look for custom checker files
        custom_files = glob.glob('wire_checker_custom_*.py')
        
        if not custom_files:
            messagebox.showwarning("No Custom Checker", "No custom wire checker found. Please create one first using 'Apply & Test'.")
            return
        
        # Use the most recent one
        custom_file = max(custom_files, key=os.path.getmtime)
        
        try:
            # Close current window
            self.root.destroy()
            
            # Run the custom checker
            subprocess.run([sys.executable, custom_file])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run custom checker: {e}")
    
    def back_to_main(self):
        """Return to main menu"""
        try:
            self.root.destroy()
            
            subprocess.run([sys.executable, 'wire_checker_main.py'])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return to main menu: {e}")
    
    def generate_custom_checker_code(self, wire_pairs, product_name, product_no):
        """Generate custom wire checker code"""
        pairs_str = str(wire_pairs).replace(' ', '')
        
        return f'''# Custom Wire Checker for {product_name} ({product_no})
# Generated automatically by Pin Configuration Form

# Handle GPIO import for Windows testing
try:
    import RPi.GPIO as GPIO
    RASPBERRY_PI = True
except ImportError:
    print("RPi.GPIO not found. Running in Windows test mode.")
    from mock_gpio import GPIO
    RASPBERRY_PI = False
import time
import threading
import tkinter as tk
from tkinter import ttk
import os
from database_manager import DatabaseManager

# Product Information
PRODUCT_NAME = "{product_name}"
PRODUCT_NO = "{product_no}"

# GPIO pin assignments
RED_LED = 2
YELLOW_LED = 3
GREEN_LED = 4
BUZZER = 18
SOLENOID = 13
SOLENOID2 = 15

# Wire pairs (output, input) - Custom Configuration
WIRE_PAIRS = {pairs_str}

# Global variables
current_status = "INITIALIZING"
status_lock = threading.Lock()
cycle_id = os.environ.get('WIRE_CHECKER_CYCLE_ID', None)
db_manager = DatabaseManager() if cycle_id else None
good_counter = 0
not_good_counter = 0
pair_status = [False] * {len(wire_pairs)}

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(SOLENOID, GPIO.OUT)
GPIO.setup(SOLENOID2, GPIO.OUT)

# Setup wire pairs
for output_pin, input_pin in WIRE_PAIRS:
    GPIO.setup(output_pin, GPIO.OUT)
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize to off state
GPIO.output(BUZZER, GPIO.HIGH)
GPIO.output(SOLENOID, GPIO.HIGH)
GPIO.output(SOLENOID2, GPIO.HIGH)

def test_wire_pair(output_pin, input_pin):
    """Test if a wire pair is properly connected"""
    GPIO.output(output_pin, GPIO.HIGH)
    time.sleep(0.01)
    high_received = GPIO.input(input_pin)
    
    GPIO.output(output_pin, GPIO.LOW)
    time.sleep(0.01)
    low_received = GPIO.input(input_pin)
    
    return high_received and not low_received

def wire_checker_loop():
    """Main wire checker loop"""
    global current_status, good_counter, not_good_counter, pair_status
    previous_status = None
    
    while True:
        try:
            # Test each pair
            pair_results = []
            for i, (output_pin, input_pin) in enumerate(WIRE_PAIRS):
                is_connected = test_wire_pair(output_pin, input_pin)
                pair_results.append(is_connected)
                pair_status[i] = is_connected
            
            # Determine status
            all_connected = all(pair_results)
            
            with status_lock:
                if all_connected:
                    current_status = "GOOD"
                    GPIO.output(GREEN_LED, GPIO.HIGH)
                    GPIO.output(RED_LED, GPIO.LOW)
                    GPIO.output(YELLOW_LED, GPIO.LOW)
                    GPIO.output(SOLENOID, GPIO.LOW)
                else:
                    current_status = "OPEN"
                    GPIO.output(YELLOW_LED, GPIO.HIGH)
                    GPIO.output(RED_LED, GPIO.LOW)
                    GPIO.output(GREEN_LED, GPIO.LOW)
                    GPIO.output(SOLENOID, GPIO.HIGH)
                
                # Update counters
                if previous_status == "OPEN":
                    if current_status == "GOOD":
                        good_counter += 1
                
                # Update database
                if db_manager and cycle_id and current_status != previous_status:
                    if current_status in ["GOOD", "OPEN"]:
                        db_manager.update_cycle_count(cycle_id, current_status)
                
                previous_status = current_status
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error in wire checker loop: {{e}}")
            time.sleep(1)

class CustomWireCheckerUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Wire Checker - {{PRODUCT_NAME}} ({{PRODUCT_NO}})")
        self.root.geometry("1024x768")
        self.root.configure(bg='#f0f0f0')
        
        self.root.eval('tk::PlaceWindow . center')
        
        # Create main frame
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Title
        title_label = tk.Label(main_frame, text=f"{{PRODUCT_NAME}} ({{PRODUCT_NO}})", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 20))
        
        subtitle_label = tk.Label(main_frame, text=f"Wire Checker - {{len(WIRE_PAIRS)}} Pairs", 
                                 font=('Arial', 20, 'bold'), bg='#f0f0f0')
        subtitle_label.pack(pady=(0, 40))
        
        # Status display
        self.status_label = tk.Label(main_frame, text="INITIALIZING", 
                                    font=('Arial', 42, 'bold'), 
                                    width=25, height=5,
                                    relief='raised', borderwidth=6)
        self.status_label.pack(pady=40)
        
        # Counters
        counters_frame = tk.Frame(main_frame, bg='#f0f0f0')
        counters_frame.pack(pady=25)
        
        self.good_counter_label = tk.Label(counters_frame, text="GOOD Count: 0", 
                                          font=('Arial', 20, 'bold'), 
                                          bg='#d4edda', fg='#155724',
                                          relief='raised', borderwidth=3)
        self.good_counter_label.pack(side='left', padx=30)
        
        # Wire pairs info
        pairs_frame = tk.Frame(main_frame, bg='#f0f0f0')
        pairs_frame.pack(pady=30)
        
        pairs_label = tk.Label(pairs_frame, text="Wire Pair Configuration:", 
                              font=('Arial', 18, 'bold'), bg='#f0f0f0')
        pairs_label.pack()
        
        pairs_text = "\\n".join([f"Pair {{i+1}}: GPIO{{out}} ↔ GPIO{{inp}}" 
                                for i, (out, inp) in enumerate(WIRE_PAIRS)])
        
        pairs_info = tk.Label(pairs_frame, text=pairs_text, 
                             font=('Arial', 16), bg='#f0f0f0', justify='left')
        pairs_info.pack()
        
        # Start updating
        self.update_ui()
    
    def update_ui(self):
        """Update the UI with current status"""
        with status_lock:
            status = current_status
        
        self.status_label.config(text=status)
        self.good_counter_label.config(text=f"GOOD Count: {{good_counter}}")
        
        # Update colors
        if status == "GOOD":
            self.status_label.config(bg='#d4edda', fg='#155724')
        elif status == "OPEN":
            self.status_label.config(bg='#fff3cd', fg='#856404')
        else:
            self.status_label.config(bg='#e2e3e5', fg='#383d41')
        
        self.root.after(500, self.update_ui)

def main():
    # Start wire checker thread
    wire_checker_thread = threading.Thread(target=wire_checker_loop, daemon=True)
    wire_checker_thread.start()
    
    # Create UI
    root = tk.Tk()
    app = CustomWireCheckerUI(root)
    
    def on_closing():
        GPIO.output(RED_LED, GPIO.LOW)
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(YELLOW_LED, GPIO.LOW)
        GPIO.output(SOLENOID, GPIO.HIGH)
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()
'''

def main():
    root = tk.Tk()
    app = PinConfigForm(root)
    root.mainloop()

if __name__ == '__main__':
    main()