import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
import threading

# Handle GPIO import
try:
    import RPi.GPIO as GPIO
    RASPBERRY_PI = True
except ImportError:
    from mock_gpio import GPIO
    RASPBERRY_PI = False

class GuidedWireTeaching:
    def __init__(self, root):
        self.root = root
        self.root.title("Guided Wire Teaching - Step by Step")
        self.root.geometry("1000x800")
        self.root.configure(bg='#f0f0f0')
        
        # Teaching state
        self.current_step = 0
        self.wire_definitions = []
        self.detected_pins = []
        self.is_teaching = False
        
        # Available pins
        self.available_pins = [5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27]
        
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
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
        main_frame = scrollable_frame
        
        # Title
        title_label = tk.Label(main_frame, text="🎯 Guided Wire Teaching", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(10, 20))
        
        # Instructions
        instructions_frame = tk.LabelFrame(main_frame, text="How It Works", 
                                         font=('Arial', 14, 'bold'), bg='#f0f0f0')
        instructions_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        instructions_text = """1. Define each wire by name, color, and function
2. Connect ONE wire at a time when prompted
3. System detects which GPIO pins are connected
4. Repeat for each wire in your assembly
5. System creates complete wire mapping"""
        
        tk.Label(instructions_frame, text=instructions_text, 
                font=('Arial', 12), bg='#f0f0f0', justify='left').pack(padx=10, pady=10)
        
        # Wire definition section
        definition_frame = tk.LabelFrame(main_frame, text="Wire Definition", 
                                       font=('Arial', 14, 'bold'), bg='#f0f0f0')
        definition_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        # Wire info inputs
        info_frame = tk.Frame(definition_frame, bg='#f0f0f0')
        info_frame.pack(pady=10)
        
        tk.Label(info_frame, text="Wire Name:", font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5)
        self.wire_name_entry = tk.Entry(info_frame, font=('Arial', 12), width=20)
        self.wire_name_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(info_frame, text="Wire Color:", font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=2, sticky='w', padx=5)
        self.wire_color_entry = tk.Entry(info_frame, font=('Arial', 12), width=15)
        self.wire_color_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(info_frame, text="Function:", font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=5)
        self.wire_function_entry = tk.Entry(info_frame, font=('Arial', 12), width=20)
        self.wire_function_entry.grid(row=1, column=1, padx=5)
        
        tk.Label(info_frame, text="Notes:", font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=2, sticky='w', padx=5)
        self.wire_notes_entry = tk.Entry(info_frame, font=('Arial', 12), width=15)
        self.wire_notes_entry.grid(row=1, column=3, padx=5)
        
        # Teaching control
        control_frame = tk.LabelFrame(main_frame, text="Teaching Control", 
                                    font=('Arial', 14, 'bold'), bg='#f0f0f0')
        control_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        # Current step display
        self.step_label = tk.Label(control_frame, text="Ready to start teaching", 
                                  font=('Arial', 16, 'bold'), 
                                  bg='#e2e3e5', fg='#383d41',
                                  relief='raised', borderwidth=2)
        self.step_label.pack(pady=10)
        
        # Buttons
        buttons_frame = tk.Frame(control_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=10)
        
        self.teach_btn = tk.Button(buttons_frame, text="🎯 TEACH THIS WIRE", 
                                  font=('Arial', 14, 'bold'),
                                  bg='#28a745', fg='white',
                                  width=20, height=2,
                                  command=self.teach_current_wire)
        self.teach_btn.pack(side='left', padx=10)
        
        self.next_btn = tk.Button(buttons_frame, text="➡️ NEXT WIRE", 
                                 font=('Arial', 14, 'bold'),
                                 bg='#007bff', fg='white',
                                 width=15, height=2,
                                 command=self.next_wire,
                                 state='disabled')
        self.next_btn.pack(side='left', padx=10)
        
        self.finish_btn = tk.Button(buttons_frame, text="✅ FINISH", 
                                   font=('Arial', 14, 'bold'),
                                   bg='#17a2b8', fg='white',
                                   width=15, height=2,
                                   command=self.finish_teaching,
                                   state='disabled')
        self.finish_btn.pack(side='left', padx=10)
        
        # Detection results
        results_frame = tk.LabelFrame(main_frame, text="Wire Mapping Results", 
                                    font=('Arial', 14, 'bold'), bg='#f0f0f0')
        results_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        self.results_text = tk.Text(results_frame, height=12, width=80,
                                   font=('Arial', 11), bg='#f8f9fa',
                                   relief='sunken', borderwidth=2)
        self.results_text.pack(pady=10, padx=10)
        
        # Product info
        product_frame = tk.LabelFrame(main_frame, text="Product Information", 
                                    font=('Arial', 14, 'bold'), bg='#f0f0f0')
        product_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        product_info_frame = tk.Frame(product_frame, bg='#f0f0f0')
        product_info_frame.pack(pady=10)
        
        tk.Label(product_info_frame, text="Product Name:", font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5)
        self.product_name_entry = tk.Entry(product_info_frame, font=('Arial', 12), width=30)
        self.product_name_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(product_info_frame, text="Product No:", font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=2, sticky='w', padx=5)
        self.product_no_entry = tk.Entry(product_info_frame, font=('Arial', 12), width=20)
        self.product_no_entry.grid(row=0, column=3, padx=5)
        
        # Save button
        save_frame = tk.Frame(main_frame, bg='#f0f0f0')
        save_frame.pack(pady=20)
        
        self.save_btn = tk.Button(save_frame, text="💾 SAVE WIRE MAPPING", 
                                 font=('Arial', 16, 'bold'),
                                 bg='#fd7e14', fg='white',
                                 width=25, height=2,
                                 command=self.save_wire_mapping,
                                 state='disabled')
        self.save_btn.pack()
    
    def teach_current_wire(self):
        """Teach current wire"""
        wire_name = self.wire_name_entry.get().strip()
        wire_color = self.wire_color_entry.get().strip()
        wire_function = self.wire_function_entry.get().strip()
        
        if not wire_name:
            messagebox.showerror("Error", "Please enter wire name")
            return
        
        # Update UI
        self.step_label.config(text=f"🔌 Connect {wire_name} ({wire_color}) wire and wait...", 
                              bg='#fff3cd', fg='#856404')
        self.teach_btn.config(state='disabled')
        
        # Start detection in thread
        self.is_teaching = True
        detection_thread = threading.Thread(target=self.detect_current_wire, 
                                          args=(wire_name, wire_color, wire_function), 
                                          daemon=True)
        detection_thread.start()
    
    def detect_current_wire(self, wire_name, wire_color, wire_function):
        """Detect current wire connection"""
        try:
            self.update_results(f"🔍 Detecting {wire_name} ({wire_color})...\n")
            
            # Scan for connections
            detected_connection = None
            
            for out_pin in self.available_pins:
                if not self.is_teaching:
                    break
                
                try:
                    GPIO.setup(out_pin, GPIO.OUT)
                    
                    for in_pin in self.available_pins:
                        if in_pin == out_pin or not self.is_teaching:
                            continue
                        
                        try:
                            GPIO.setup(in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                            
                            # Test connection
                            if self.test_connection(out_pin, in_pin):
                                detected_connection = (out_pin, in_pin)
                                break
                        except:
                            continue
                    
                    GPIO.setup(out_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                    
                    if detected_connection:
                        break
                        
                except:
                    continue
                
                time.sleep(0.1)
            
            # Process result
            if detected_connection:
                wire_info = {
                    'name': wire_name,
                    'color': wire_color,
                    'function': wire_function,
                    'notes': self.wire_notes_entry.get().strip(),
                    'pin_out': detected_connection[0],
                    'pin_in': detected_connection[1],
                    'step': len(self.wire_definitions) + 1
                }
                
                self.wire_definitions.append(wire_info)
                
                result_text = f"✅ {wire_name} ({wire_color}): GPIO{detected_connection[0]} → GPIO{detected_connection[1]}\n"
                result_text += f"   Function: {wire_function}\n"
                result_text += f"   Notes: {self.wire_notes_entry.get().strip()}\n\n"
                
                self.update_results(result_text)
                
                # Update UI
                self.root.after(0, lambda: self.step_label.config(
                    text=f"✅ {wire_name} detected: GPIO{detected_connection[0]} → GPIO{detected_connection[1]}", 
                    bg='#d4edda', fg='#155724'))
                
                self.root.after(0, lambda: self.next_btn.config(state='normal'))
                self.root.after(0, lambda: self.finish_btn.config(state='normal'))
                
            else:
                self.update_results(f"❌ No connection detected for {wire_name}\n")
                self.root.after(0, lambda: self.step_label.config(
                    text=f"❌ No connection found for {wire_name}", 
                    bg='#f8d7da', fg='#721c24'))
                self.root.after(0, lambda: self.teach_btn.config(state='normal'))
            
        except Exception as e:
            self.update_results(f"❌ Error detecting {wire_name}: {e}\n")
        
        finally:
            self.is_teaching = False
    
    def test_connection(self, out_pin, in_pin):
        """Test if two pins are connected"""
        try:
            GPIO.output(out_pin, GPIO.HIGH)
            time.sleep(0.01)
            high_received = GPIO.input(in_pin)
            
            GPIO.output(out_pin, GPIO.LOW)
            time.sleep(0.01)
            low_received = GPIO.input(in_pin)
            
            return high_received and not low_received
        except:
            return False
    
    def next_wire(self):
        """Prepare for next wire"""
        # Clear inputs
        self.wire_name_entry.delete(0, tk.END)
        self.wire_color_entry.delete(0, tk.END)
        self.wire_function_entry.delete(0, tk.END)
        self.wire_notes_entry.delete(0, tk.END)
        
        # Update UI
        self.current_step += 1
        self.step_label.config(text=f"Ready for wire #{self.current_step + 1}", 
                              bg='#e2e3e5', fg='#383d41')
        self.teach_btn.config(state='normal')
        self.next_btn.config(state='disabled')
    
    def finish_teaching(self):
        """Finish teaching process"""
        if not self.wire_definitions:
            messagebox.showwarning("No Data", "No wires have been taught yet.")
            return
        
        self.step_label.config(text=f"✅ Teaching complete! {len(self.wire_definitions)} wires mapped", 
                              bg='#d4edda', fg='#155724')
        self.teach_btn.config(state='disabled')
        self.next_btn.config(state='disabled')
        self.finish_btn.config(state='disabled')
        self.save_btn.config(state='normal')
        
        # Show summary
        summary = f"\n{'='*50}\n"
        summary += f"WIRE MAPPING SUMMARY\n"
        summary += f"{'='*50}\n"
        summary += f"Total Wires: {len(self.wire_definitions)}\n\n"
        
        for wire in self.wire_definitions:
            summary += f"{wire['step']}. {wire['name']} ({wire['color']})\n"
            summary += f"   GPIO{wire['pin_out']} → GPIO{wire['pin_in']}\n"
            summary += f"   Function: {wire['function']}\n"
            if wire['notes']:
                summary += f"   Notes: {wire['notes']}\n"
            summary += "\n"
        
        self.update_results(summary)
    
    def save_wire_mapping(self):
        """Save complete wire mapping"""
        product_name = self.product_name_entry.get().strip()
        product_no = self.product_no_entry.get().strip()
        
        if not product_name or not product_no:
            messagebox.showerror("Missing Info", "Please enter Product Name and Product No.")
            return
        
        # Create configuration
        config_data = {
            'product_name': product_name,
            'product_no': product_no,
            'teaching_method': 'guided_wire_teaching',
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_wires': len(self.wire_definitions),
            'wire_definitions': self.wire_definitions,
            'wire_pairs': []
        }
        
        # Convert to wire pairs format
        for wire in self.wire_definitions:
            config_data['wire_pairs'].append({
                'pair_number': wire['step'],
                'pin_out': wire['pin_out'],
                'pin_in': wire['pin_in'],
                'wire_name': wire['name'],
                'wire_color': wire['color'],
                'wire_function': wire['function'],
                'wire_notes': wire['notes']
            })
        
        # Save to file
        config_file = f'guided_teaching_{product_no.replace("-", "_").lower()}.json'
        try:
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
            
            messagebox.showinfo("Success", 
                              f"Wire mapping saved!\n\n"
                              f"Product: {product_name}\n"
                              f"Part No: {product_no}\n"
                              f"Total Wires: {len(self.wire_definitions)}\n"
                              f"File: {config_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save wire mapping: {e}")
    
    def update_results(self, text):
        """Update results display"""
        def update():
            self.results_text.insert(tk.END, text)
            self.results_text.see(tk.END)
            self.root.update()
        
        self.root.after(0, update)

def main():
    root = tk.Tk()
    app = GuidedWireTeaching(root)
    root.mainloop()

if __name__ == '__main__':
    main()