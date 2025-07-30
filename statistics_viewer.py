#!/usr/bin/env python3
"""
Statistics Viewer for Wire Checker
Shows cycle data and daily statistics
"""

import tkinter as tk
from tkinter import ttk
from database_manager import DatabaseManager
from datetime import datetime, date
import os

class StatisticsViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Wire Checker Statistics")
        self.root.geometry("1024x768")  # Optimized for 7-inch TFT
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Create main frame
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Title
        title_label = tk.Label(main_frame, text="Wire Checker Statistics", 
                              font=('Arial', 28, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 40))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill='both', pady=20)
        
        # Today's Statistics Tab
        self.create_today_tab()
        
        # Recent Cycles Tab
        self.create_cycles_tab()
        
        # Back button
        back_btn = tk.Button(main_frame, text="Back to Main Menu", 
                            font=('Arial', 18, 'bold'),
                            width=25, height=2,
                            bg='#6c757d', fg='white',
                            relief='raised', borderwidth=3,
                            command=self.back_to_main)
        back_btn.pack(pady=(30, 0))
    
    def create_today_tab(self):
        """Create today's statistics tab"""
        today_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(today_frame, text="Today's Statistics")
        
        # Get today's statistics
        today_stats = self.db_manager.get_daily_statistics()
        
        if today_stats:
            # Create statistics display
            for i, stat in enumerate(today_stats):
                stat_frame = tk.Frame(today_frame, bg='#f8f9fa', relief='raised', borderwidth=2)
                stat_frame.pack(fill='x', padx=20, pady=10)
                
                # Configuration name
                config_label = tk.Label(stat_frame, text=f"Configuration: {stat['configuration']}", 
                                       font=('Arial', 20, 'bold'), bg='#f8f9fa')
                config_label.pack(pady=(10, 5))
                
                # Statistics grid
                stats_frame = tk.Frame(stat_frame, bg='#f8f9fa')
                stats_frame.pack(pady=10)
                
                # Total cycles
                cycles_label = tk.Label(stats_frame, text=f"Total Cycles: {stat['total_cycles']}", 
                                       font=('Arial', 16, 'bold'), bg='#e3f2fd', fg='#1565c0',
                                       relief='raised', borderwidth=2)
                cycles_label.grid(row=0, column=0, padx=10, pady=5)
                
                # Total checked
                checked_label = tk.Label(stats_frame, text=f"Total Checked: {stat['total_checked']}", 
                                        font=('Arial', 16, 'bold'), bg='#fff3cd', fg='#856404',
                                        relief='raised', borderwidth=2)
                checked_label.grid(row=0, column=1, padx=10, pady=5)
                
                # Good count
                good_label = tk.Label(stats_frame, text=f"Good: {stat['total_good']}", 
                                     font=('Arial', 16, 'bold'), bg='#d4edda', fg='#155724',
                                     relief='raised', borderwidth=2)
                good_label.grid(row=1, column=0, padx=10, pady=5)
                
                # Not good count
                not_good_label = tk.Label(stats_frame, text=f"Not Good: {stat['total_not_good']}", 
                                         font=('Arial', 16, 'bold'), bg='#f8d7da', fg='#721c24',
                                         relief='raised', borderwidth=2)
                not_good_label.grid(row=1, column=1, padx=10, pady=5)
                
                # Open count
                open_label = tk.Label(stats_frame, text=f"Open: {stat['total_open']}", 
                                     font=('Arial', 16, 'bold'), bg='#e2e3e5', fg='#383d41',
                                     relief='raised', borderwidth=2)
                open_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        else:
            # No data message
            no_data_label = tk.Label(today_frame, text="No statistics available for today", 
                                    font=('Arial', 18), bg='#f0f0f0', fg='#6c757d')
            no_data_label.pack(pady=50)
    
    def create_cycles_tab(self):
        """Create recent cycles tab"""
        cycles_frame = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(cycles_frame, text="Recent Cycles")
        
        # Get recent cycles
        recent_cycles = self.db_manager.get_all_cycles(limit=20)
        
        if recent_cycles:
            # Create scrollable frame
            canvas = tk.Canvas(cycles_frame, bg='#f0f0f0')
            scrollbar = ttk.Scrollbar(cycles_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add cycle data
            for cycle in recent_cycles:
                cycle_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief='raised', borderwidth=2)
                cycle_frame.pack(fill='x', padx=20, pady=5)
                
                # Cycle ID and status
                id_label = tk.Label(cycle_frame, text=f"Cycle: {cycle['cycle_id'][:8]}... | Status: {cycle['status']}", 
                                   font=('Arial', 14, 'bold'), bg='#f8f9fa')
                id_label.pack(pady=(10, 5))
                
                # Configuration
                config_label = tk.Label(cycle_frame, text=f"Configuration: {cycle['configuration']}", 
                                       font=('Arial', 12), bg='#f8f9fa')
                config_label.pack()
                
                # Time information
                start_time = cycle['start_time']
                end_time = cycle['end_time'] if cycle['end_time'] else "Active"
                time_label = tk.Label(cycle_frame, text=f"Start: {start_time} | End: {end_time}", 
                                     font=('Arial', 12), bg='#f8f9fa')
                time_label.pack()
                
                # Statistics
                stats_label = tk.Label(cycle_frame, 
                                      text=f"Total: {cycle['total_checked']} | Good: {cycle['good_count']} | Not Good: {cycle['not_good_count']} | Open: {cycle['open_count']}", 
                                      font=('Arial', 12, 'bold'), bg='#f8f9fa')
                stats_label.pack(pady=(0, 10))
            
            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            # No data message
            no_data_label = tk.Label(cycles_frame, text="No recent cycles available", 
                                    font=('Arial', 18), bg='#f0f0f0', fg='#6c757d')
            no_data_label.pack(pady=50)
    
    def back_to_main(self):
        """Return to main menu"""
        self.root.destroy()
        import subprocess
        subprocess.run(['python3', 'wire_checker_main.py'])

def main():
    root = tk.Tk()
    app = StatisticsViewer(root)
    root.mainloop()

if __name__ == '__main__':
    main() 