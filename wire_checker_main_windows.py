import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
from responsive_ui_base import ResponsiveUI

class WireCheckerSelector(ResponsiveUI):
    def __init__(self, root):
        super().__init__()
        self.root = root
        
        # Setup responsive window
        self.window_width, self.window_height = self.setup_responsive_window(
            root, "Wire Checker - Select Configuration (Windows Test Mode)", 1024, 768
        )
        
        self.root.configure(bg='#f0f0f0')
        
        # Create main responsive frame
        main_frame = self.create_responsive_frame(root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=self.get_padding(40), pady=self.get_padding(40))
        
        # Title
        title_label = self.create_responsive_label(main_frame, "Wire Checker System", 
                                                  style="title", bg='#f0f0f0')
        title_label.pack(pady=(0, self.get_padding(20)))
        
        # Windows test mode notice
        notice_label = self.create_responsive_label(main_frame, "🖥️ Windows Test Mode - GPIO functions simulated", 
                                                   style="subtitle", bg='#fff3cd', fg='#856404',
                                                   relief='raised', borderwidth=2)
        notice_label.pack(pady=(0, self.get_padding(20)))
        
        # Subtitle
        subtitle_label = self.create_responsive_label(main_frame, "Select configuration or test Pin Configuration:", 
                                                     style="heading", bg='#f0f0f0')
        subtitle_label.pack(pady=(0, self.get_padding(30)))
        
        # Buttons frame
        buttons_frame = self.create_responsive_frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=self.get_padding(20))
        
        # Pin Configuration Button (Main feature for testing)
        btn_width, btn_height = self.get_button_size(25, 3)
        self.btn_pin_config = self.create_responsive_button(buttons_frame, "📌 Pin Configuration", 
                                                           command=self.pin_configuration, style="warning",
                                                           width=btn_width, height=btn_height)
        self.btn_pin_config.pack(pady=self.get_padding(15))
        
        # Test Pin Config Form Button
        self.btn_test_form = self.create_responsive_button(buttons_frame, "🧪 Test Pin Config Form", 
                                                          command=self.test_pin_form, style="success",
                                                          width=btn_width, height=btn_height)
        self.btn_test_form.pack(pady=self.get_padding(15))
        
        # Auto Pin Detection Button
        self.btn_auto_detect = self.create_responsive_button(buttons_frame, "🔍 Auto Pin Detection", 
                                                            command=self.auto_pin_detection, style="info",
                                                            width=btn_width, height=btn_height)
        self.btn_auto_detect.pack(pady=self.get_padding(15))
        
        # Guided Wire Teaching Button
        self.btn_guided_teaching = self.create_responsive_button(buttons_frame, "🎯 Guided Wire Teaching", 
                                                                command=self.guided_wire_teaching, style="danger",
                                                                width=btn_width, height=btn_height)
        self.btn_guided_teaching.pack(pady=self.get_padding(15))
        
        # RFID Card Manager Button
        self.btn_rfid_manager = self.create_responsive_button(buttons_frame, "🔐 RFID Card Manager", 
                                                             command=self.rfid_card_manager, style="dark",
                                                             width=btn_width, height=btn_height)
        self.btn_rfid_manager.pack(pady=self.get_padding(15))
        
        # Wire Checker with RFID Button
        self.btn_wire_checker_rfid = self.create_responsive_button(buttons_frame, "🔒 Wire Checker + RFID", 
                                                                  command=self.wire_checker_rfid, style="secondary",
                                                                  width=btn_width, height=btn_height)
        self.btn_wire_checker_rfid.pack(pady=self.get_padding(15))
        
        # Information frame
        info_frame = self.create_responsive_labelframe(main_frame, "System Information", bg='#f0f0f0')
        info_frame.pack(fill='x', pady=(self.get_padding(30), 0), padx=self.get_padding(20))
        
        info_text = """Pin Configuration: Setup custom PIN IN/OUT configuration with product info
Test Pin Config Form: Direct access to pin configuration form
Auto Pin Detection: Teaching mode - auto detect connected pins
Guided Wire Teaching: Step-by-step wire identification with names & colors
RFID Card Manager: Manage authorized cards for solenoid unlock
Wire Checker + RFID: Wire testing with RFID locking system

⚠️ Note: This is Windows test mode. GPIO functions are simulated.
For actual hardware testing, run on Raspberry Pi."""
        
        info_label = self.create_responsive_label(info_frame, info_text, style="normal", 
                                                 bg='#f0f0f0', justify='left', wraplength=self.window_width-100)
        info_label.pack(padx=self.get_padding(15), pady=self.get_padding(15))
        
        # Exit button
        exit_btn_width, exit_btn_height = self.get_button_size(15, 2)
        exit_btn = self.create_responsive_button(main_frame, "Exit", 
                                                command=self.root.destroy, style="danger",
                                                width=exit_btn_width, height=exit_btn_height)
        exit_btn.pack(pady=(self.get_padding(30), 0))
    
    def pin_configuration(self):
        """Open pin configuration form"""
        try:
            # Close the selector window
            self.root.destroy()
            
            # Run the pin configuration form
            subprocess.run([sys.executable, 'pin_config_form.py'])
            
        except Exception as e:
            print(f"Error running pin configuration form: {e}")
    
    def test_pin_form(self):
        """Direct test of pin configuration form"""
        try:
            # Close the selector window
            self.root.destroy()
            
            # Run the pin configuration form directly
            subprocess.run([sys.executable, 'pin_config_form.py'])
            
        except Exception as e:
            print(f"Error running pin configuration form: {e}")
    
    def auto_pin_detection(self):
        """Open auto pin detection - teaching mode"""
        try:
            # Close the selector window
            self.root.destroy()
            
            # Run the auto pin detector
            subprocess.run([sys.executable, 'auto_pin_detector.py'])
            
        except Exception as e:
            print(f"Error running auto pin detector: {e}")
    
    def guided_wire_teaching(self):
        """Open guided wire teaching - step by step"""
        try:
            # Close the selector window
            self.root.destroy()
            
            # Run the guided wire teaching
            subprocess.run([sys.executable, 'guided_wire_teaching.py'])
            
        except Exception as e:
            print(f"Error running guided wire teaching: {e}")
    
    def rfid_card_manager(self):
        """Open RFID card management"""
        try:
            # Close the selector window
            self.root.destroy()
            
            # Run the RFID card manager
            subprocess.run([sys.executable, 'rfid_card_manager.py'])
            
        except Exception as e:
            print(f"Error running RFID card manager: {e}")
    
    def wire_checker_rfid(self):
        """Open wire checker with RFID locking"""
        try:
            # Close the selector window
            self.root.destroy()
            
            # Run the wire checker with RFID
            subprocess.run([sys.executable, 'wire_checker_with_rfid.py'])
            
        except Exception as e:
            print(f"Error running wire checker with RFID: {e}")

def main():
    root = tk.Tk()
    app = WireCheckerSelector(root)
    root.mainloop()

if __name__ == '__main__':
    main()