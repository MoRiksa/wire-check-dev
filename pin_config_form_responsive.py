import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import re
import subprocess
import sys
import glob
from responsive_ui_base import ResponsiveUI

class PinConfigFormResponsive(ResponsiveUI):
    def __init__(self, root):
        super().__init__()
        self.root = root
        
        # Setup responsive window
        self.window_width, self.window_height = self.setup_responsive_window(
            root, "Pin Configuration Form", 1000, 800
        )
        
        self.root.configure(bg='#f0f0f0')
        
        # Configuration data
        self.config_data = {
            'product_name': '',
            'product_no': '',
            'wire_pairs': []
        }
        
        self.create_widgets()
        self.load_existing_config()
    
    def create_widgets(self):
        # Create main container with grid layout
        main_container = self.create_responsive_frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=self.get_padding(15), pady=self.get_padding(15))
        
        # Configure main container grid
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Title section
        title_frame = self.create_responsive_frame(main_container, bg='#f0f0f0')
        title_frame.grid(row=0, column=0, sticky='ew', pady=(0, self.get_padding(15)))
        
        title_label = self.create_responsive_label(title_frame, "📌 Wire Checker Pin Configuration", 
                                                  style="title", bg='#f0f0f0')
        title_label.pack()
        
        # Scrollable content area
        scroll_container, content_frame = self.create_scrollable_frame(main_container, bg='#f0f0f0')
        scroll_container.grid(row=1, column=0, sticky='nsew')
        
        # Product Information Section
        self.create_product_section(content_frame)
        
        # Wire Pairs Section
        self.create_wire_pairs_section(content_frame)
        
        # Template Section
        self.create_template_section(content_frame)
        
        # Action Buttons Section
        self.create_buttons_section(content_frame)
    
    def create_product_section(self, parent):
        """Create product information section"""
        product_frame = self.create_responsive_labelframe(parent, "Product Information", bg='#f0f0f0')
        product_frame.pack(fill='x', pady=(0, self.get_padding(15)), padx=self.get_padding(10))
        
        # Configure grid
        product_frame.grid_columnconfigure(1, weight=1)
        product_frame.grid_columnconfigure(3, weight=1)
        
        # Product name
        name_label = self.create_responsive_label(product_frame, "Product Name:", style="normal", bg='#f0f0f0')
        name_label.grid(row=0, column=0, sticky='w', padx=self.get_padding(10), pady=self.get_padding(8))
        
        self.product_name_entry = self.create_responsive_entry(product_frame)
        self.product_name_entry.grid(row=0, column=1, sticky='ew', padx=self.get_padding(10), pady=self.get_padding(8))
        
        # Product number
        no_label = self.create_responsive_label(product_frame, "Product No:", style="normal", bg='#f0f0f0')
        no_label.grid(row=0, column=2, sticky='w', padx=self.get_padding(10), pady=self.get_padding(8))
        
        self.product_no_entry = self.create_responsive_entry(product_frame)
        self.product_no_entry.grid(row=0, column=3, sticky='ew', padx=self.get_padding(10), pady=self.get_padding(8))
    
    def create_wire_pairs_section(self, parent):
        """Create wire pairs configuration section"""
        pairs_frame = self.create_responsive_labelframe(parent, "Wire Pair Configuration (Up to 6 pairs)", bg='#f0f0f0')
        pairs_frame.pack(fill='x', pady=(0, self.get_padding(15)), padx=self.get_padding(10))
        
        # Configure grid for responsive layout
        for i in range(3):
            pairs_frame.grid_columnconfigure(i*2+1, weight=1)
            pairs_frame.grid_columnconfigure(i*2+2, weight=1)
        
        # Headers
        headers = ["Pair", "PIN OUT (GPIO)", "PIN IN (GPIO)"]
        for i, header in enumerate(headers):
            header_label = self.create_responsive_label(pairs_frame, header, style="heading", bg='#e9ecef')
            header_label.grid(row=0, column=i, sticky='ew', padx=self.get_padding(5), pady=self.get_padding(5))
        
        # Wire pair entries (2 columns of 3 pairs each)
        self.pair_entries = []
        for i in range(6):
            row = (i % 3) + 1
            col_offset = (i // 3) * 3
            
            # Pair label
            pair_label = self.create_responsive_label(pairs_frame, f"Pair {i+1}:", style="normal", bg='#f0f0f0')
            pair_label.grid(row=row, column=col_offset, sticky='w', padx=self.get_padding(5), pady=self.get_padding(3))
            
            # PIN OUT entry
            pin_out_entry = self.create_responsive_entry(pairs_frame, width=12)
            pin_out_entry.grid(row=row, column=col_offset+1, sticky='ew', padx=self.get_padding(5), pady=self.get_padding(3))
            
            # PIN IN entry
            pin_in_entry = self.create_responsive_entry(pairs_frame, width=12)
            pin_in_entry.grid(row=row, column=col_offset+2, sticky='ew', padx=self.get_padding(5), pady=self.get_padding(3))
            
            self.pair_entries.append((pin_out_entry, pin_in_entry))
    
    def create_template_section(self, parent):
        """Create template information section"""
        template_frame = self.create_responsive_labelframe(parent, "Template Example", bg='#f0f0f0')
        template_frame.pack(fill='x', pady=(0, self.get_padding(15)), padx=self.get_padding(10))
        
        template_text = """Example Configuration:
Product Name: Test Wire Assembly    Product No: TWA-001
Pair 1: GPIO17 → GPIO27    Pair 2: GPIO22 → GPIO10    Pair 3: GPIO9 → GPIO11"""
        
        template_label = self.create_responsive_label(template_frame, template_text, style="small", 
                                                     bg='#f8f9fa', justify='left', relief='sunken', borderwidth=1)
        template_label.pack(fill='x', padx=self.get_padding(10), pady=self.get_padding(8))
    
    def create_buttons_section(self, parent):
        """Create action buttons section"""
        # Main buttons frame
        buttons_main_frame = self.create_responsive_frame(parent, bg='#f0f0f0')
        buttons_main_frame.pack(fill='x', pady=self.get_padding(15), padx=self.get_padding(10))
        
        # First row of buttons
        buttons_row1 = self.create_responsive_frame(buttons_main_frame, bg='#f0f0f0')
        buttons_row1.pack(fill='x', pady=(0, self.get_padding(10)))
        
        btn_width, btn_height = self.get_button_size(15, 2)
        
        # Save button
        save_btn = self.create_responsive_button(buttons_row1, "💾 Save Configuration", 
                                                command=self.save_config, style="success",
                                                width=btn_width, height=btn_height)
        save_btn.pack(side='left', padx=self.get_padding(5))
        
        # Load template button
        template_btn = self.create_responsive_button(buttons_row1, "📋 Load Template", 
                                                    command=self.load_template, style="primary",
                                                    width=btn_width, height=btn_height)
        template_btn.pack(side='left', padx=self.get_padding(5))
        
        # Load from file button
        load_file_btn = self.create_responsive_button(buttons_row1, "📁 Load from File", 
                                                     command=self.load_from_file, style="info",
                                                     width=btn_width, height=btn_height)
        load_file_btn.pack(side='left', padx=self.get_padding(5))
        
        # Clear button
        clear_btn = self.create_responsive_button(buttons_row1, "🗑️ Clear All", 
                                                 command=self.clear_form, style="warning",
                                                 width=btn_width, height=btn_height)
        clear_btn.pack(side='left', padx=self.get_padding(5))
        
        # Second row of buttons
        buttons_row2 = self.create_responsive_frame(buttons_main_frame, bg='#f0f0f0')
        buttons_row2.pack(fill='x')
        
        # Apply button
        apply_btn = self.create_responsive_button(buttons_row2, "✅ Apply & Test", 
                                                 command=self.apply_config, style="success",
                                                 width=btn_width, height=btn_height)
        apply_btn.pack(side='left', padx=self.get_padding(5))
        
        # Create template button
        create_template_btn = self.create_responsive_button(buttons_row2, "📝 Create Template", 
                                                           command=self.create_template_file, style="info",
                                                           width=btn_width, height=btn_height)
        create_template_btn.pack(side='left', padx=self.get_padding(5))
        
        # Run custom checker button
        run_custom_btn = self.create_responsive_button(buttons_row2, "🚀 Run Custom Checker", 
                                                      command=self.run_custom_checker, style="primary",
                                                      width=btn_width, height=btn_height)
        run_custom_btn.pack(side='left', padx=self.get_padding(5))
        
        # Back button
        back_btn = self.create_responsive_button(buttons_row2, "🔙 Back to Main", 
                                                command=self.back_to_main, style="secondary",
                                                width=btn_width, height=btn_height)
        back_btn.pack(side='left', padx=self.get_padding(5))
    
    # Keep all the original methods for functionality
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
            
            if out_pin or in_pin:
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
                
                self.product_name_entry.insert(0, self.config_data.get('product_name', ''))
                self.product_no_entry.insert(0, self.config_data.get('product_no', ''))
                
                for pair_data in self.config_data.get('wire_pairs', []):
                    pair_num = pair_data['pair_number'] - 1
                    if pair_num < len(self.pair_entries):
                        self.pair_entries[pair_num][0].insert(0, str(pair_data['pin_out']))
                        self.pair_entries[pair_num][1].insert(0, str(pair_data['pin_in']))
                        
            except Exception as e:
                print(f"Error loading existing configuration: {e}")
    
    def apply_config(self):
        """Apply configuration and start wire checker"""
        if not self.validate_config():
            return
        
        self.save_config()
        messagebox.showinfo("Success", "Configuration applied! Custom wire checker ready.")
    
    def load_from_file(self):
        """Load configuration from text file"""
        messagebox.showinfo("Info", "Load from file functionality - select a template file")
    
    def create_template_file(self):
        """Create a template file for manual editing"""
        messagebox.showinfo("Info", "Create template functionality - generate template file")
    
    def run_custom_checker(self):
        """Run the custom checker"""
        messagebox.showinfo("Info", "Run custom checker functionality")
    
    def back_to_main(self):
        """Return to main menu"""
        try:
            self.root.destroy()
            subprocess.run([sys.executable, 'wire_checker_main_windows.py'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return to main menu: {e}")

def main():
    root = tk.Tk()
    app = PinConfigFormResponsive(root)
    root.mainloop()

if __name__ == '__main__':
    main()