import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
from database_manager import DatabaseManager

# Handle GPIO import for Windows testing
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("RPi.GPIO not found. Using mock GPIO for testing.")
    from mock_gpio import GPIO

class WireCheckerSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Wire Checker - Select Configuration")
        self.root.geometry("1024x768")  # Optimized for 7-inch TFT
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Create main frame
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=60, pady=60)
        
        # Title
        title_label = tk.Label(main_frame, text="Wire Checker System", 
                              font=('Arial', 32, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 50))
        
        # Subtitle
        subtitle_label = tk.Label(main_frame, text="Select the number of wire pairs to test:", 
                                 font=('Arial', 22), bg='#f0f0f0')
        subtitle_label.pack(pady=(0, 50))
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=30)
        
        # 3 Pairs Button
        self.btn_3pairs = tk.Button(buttons_frame, text="3 Wire Pairs", 
                                    font=('Arial', 24, 'bold'),
                                    width=30, height=3,
                                    bg='#007bff', fg='white',
                                    relief='raised', borderwidth=4,
                                    command=self.run_3pairs)
        self.btn_3pairs.pack(pady=25)
        
        # 4 Pairs Button
        self.btn_4pairs = tk.Button(buttons_frame, text="4 Wire Pairs", 
                                    font=('Arial', 24, 'bold'),
                                    width=30, height=3,
                                    bg='#28a745', fg='white',
                                    relief='raised', borderwidth=4,
                                    command=self.run_4pairs)
        self.btn_4pairs.pack(pady=25)
        
        # 4 Pairs Speech Button
        self.btn_4pairs_speech = tk.Button(buttons_frame, text="4 Wire Pairs (Speech)", 
                                           font=('Arial', 24, 'bold'),
                                           width=30, height=3,
                                           bg='#17a2b8', fg='white',
                                           relief='raised', borderwidth=4,
                                           command=self.run_4pairs_speech)
        self.btn_4pairs_speech.pack(pady=25)
        
        # Statistics Button
        self.btn_statistics = tk.Button(buttons_frame, text="View Statistics", 
                                       font=('Arial', 24, 'bold'),
                                       width=30, height=3,
                                       bg='#6f42c1', fg='white',
                                       relief='raised', borderwidth=4,
                                       command=self.view_statistics)
        self.btn_statistics.pack(pady=25)
        
        # Pin Configuration Button
        self.btn_pin_config = tk.Button(buttons_frame, text="Pin Configuration", 
                                        font=('Arial', 24, 'bold'),
                                        width=30, height=3,
                                        bg='#fd7e14', fg='white',
                                        relief='raised', borderwidth=4,
                                        command=self.pin_configuration)
        self.btn_pin_config.pack(pady=25)
        
        # Information frame
        info_frame = tk.Frame(main_frame, bg='#f0f0f0')
        info_frame.pack(pady=(40, 0))
        
        info_label = tk.Label(info_frame, 
                             text="3 Pairs: GPIO17↔27, GPIO22↔10, GPIO9↔11\n"
                                  "4 Pairs: GPIO17↔27, GPIO22↔10, GPIO9↔11, GPIO5↔6\n"
                                  "4 Pairs (Speech): Same as 4 Pairs but with MP3 audio + Cycle tracking\n"
                                  "Statistics: View daily statistics and cycle history\n"
                                  "Pin Configuration: Setup custom PIN IN/OUT configuration with product info", 
                             font=('Arial', 18), bg='#f0f0f0', justify='left')
        info_label.pack()
        
        # Exit button
        exit_btn = tk.Button(main_frame, text="Exit", 
                            font=('Arial', 20),
                            width=20, height=3,
                            bg='#dc3545', fg='white',
                            command=self.root.destroy)
        exit_btn.pack(pady=(40, 0))
    
    def run_3pairs(self):
        """Run the 3-pair wire checker"""
        try:
            # Create new cycle
            cycle_id = self.db_manager.create_new_cycle("3-pairs")
            
            # Close the selector window
            self.root.destroy()
            
            # Run the 3-pair wire checker with cycle ID
            env = os.environ.copy()
            env['WIRE_CHECKER_CYCLE_ID'] = cycle_id
            subprocess.run([sys.executable, 'wire_checker_3pairs.py'], env=env)
            
        except Exception as e:
            print(f"Error running 3-pair wire checker: {e}")
    
    def run_4pairs(self):
        """Run the 4-pair wire checker"""
        try:
            # Create new cycle
            cycle_id = self.db_manager.create_new_cycle("4-pairs")
            
            # Close the selector window
            self.root.destroy()
            
            # Run the 4-pair wire checker with cycle ID
            env = os.environ.copy()
            env['WIRE_CHECKER_CYCLE_ID'] = cycle_id
            subprocess.run([sys.executable, 'wire_checker_4pairs.py'], env=env)
            
        except Exception as e:
            print(f"Error running 4-pair wire checker: {e}")
    
    def run_4pairs_speech(self):
        """Run the 4-pair wire checker with speech"""
        try:
            # Create new cycle
            cycle_id = self.db_manager.create_new_cycle("4-pairs-speech")
            
            # Close the selector window
            self.root.destroy()
            
            # Run the 4-pair speech wire checker with cycle ID
            env = os.environ.copy()
            env['WIRE_CHECKER_CYCLE_ID'] = cycle_id
            subprocess.run([sys.executable, 'wire_checker_4pairs_speech.py'], env=env)
            
        except Exception as e:
            print(f"Error running 4-pair speech wire checker: {e}")
    
    def view_statistics(self):
        """View statistics and cycle data"""
        try:
            # Close the selector window
            self.root.destroy()
            
            # Run the statistics viewer
            subprocess.run([sys.executable, 'statistics_viewer.py'])
            
        except Exception as e:
            print(f"Error running statistics viewer: {e}")
    
    def pin_configuration(self):
        """Open pin configuration form"""
        try:
            # Close the selector window
            self.root.destroy()
            
            # Run the pin configuration form
            subprocess.run([sys.executable, 'pin_config_form.py'])
            
        except Exception as e:
            print(f"Error running pin configuration form: {e}")

def main():
    root = tk.Tk()
    app = WireCheckerSelector(root)
    root.mainloop()

if __name__ == '__main__':
    main()
