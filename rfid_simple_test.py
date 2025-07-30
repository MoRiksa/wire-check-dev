#!/usr/bin/env python3
"""
Simple RFID Test - Windows Compatible
Test RFID functionality without hardware dependencies
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import time
import threading
from datetime import datetime

class SimpleRFIDTest:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Simple RFID Test")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # RFID system state
        self.is_locked = False
        self.lock_reason = ""
        self.authorized_cards = {
            "1234567890": {"name": "Supervisor Card", "level": "admin"},
            "0987654321": {"name": "Technician Card", "level": "tech"},
            "1122334455": {"name": "Manager Card", "level": "manager"}
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="🔐 RFID System Test", 
                              font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # Lock status display
        self.status_frame = tk.LabelFrame(self.root, text="System Status", 
                                         font=('Arial', 14, 'bold'), bg='#f0f0f0')
        self.status_frame.pack(fill='x', padx=20, pady=10)
        
        self.lock_status_label = tk.Label(self.status_frame, text="🔓 UNLOCKED", 
                                         font=('Arial', 16, 'bold'), 
                                         bg='#d4edda', fg='#155724')
        self.lock_status_label.pack(pady=10)
        
        self.lock_reason_label = tk.Label(self.status_frame, text="System ready", 
                                         font=('Arial', 12), bg='#f0f0f0')
        self.lock_reason_label.pack(pady=5)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=20)
        
        # Lock button
        lock_btn = tk.Button(control_frame, text="🔒 LOCK SYSTEM", 
                            font=('Arial', 12, 'bold'),
                            bg='#dc3545', fg='white',
                            width=15, height=2,
                            command=self.lock_system)
        lock_btn.pack(side='left', padx=10)
        
        # Unlock button
        unlock_btn = tk.Button(control_frame, text="🔓 UNLOCK SYSTEM", 
                              font=('Arial', 12, 'bold'),
                              bg='#28a745', fg='white',
                              width=15, height=2,
                              command=self.unlock_system)
        unlock_btn.pack(side='left', padx=10)
        
        # RFID Card Simulation
        rfid_frame = tk.LabelFrame(self.root, text="RFID Card Simulation", 
                                  font=('Arial', 14, 'bold'), bg='#f0f0f0')
        rfid_frame.pack(fill='x', padx=20, pady=10)
        
        # Card ID input
        tk.Label(rfid_frame, text="Card ID:", font=('Arial', 12), bg='#f0f0f0').pack(pady=5)
        self.card_id_entry = tk.Entry(rfid_frame, font=('Arial', 12), width=20)
        self.card_id_entry.pack(pady=5)
        self.card_id_entry.insert(0, "1234567890")  # Default test card
        
        # Scan button\n        scan_btn = tk.Button(rfid_frame, text="📱 SCAN CARD", 
                            font=('Arial', 12, 'bold'),
                            bg='#007bff', fg='white',
                            width=20, height=2,
                            command=self.scan_card)
        scan_btn.pack(pady=10)
        
        # Authorized cards display
        cards_frame = tk.LabelFrame(self.root, text="Authorized Cards", 
                                   font=('Arial', 14, 'bold'), bg='#f0f0f0')
        cards_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Cards listbox
        self.cards_listbox = tk.Listbox(cards_frame, font=('Arial', 10), height=6)
        self.cards_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Populate cards list
        self.update_cards_list()
        
        # Log display
        log_frame = tk.LabelFrame(self.root, text="Activity Log", 
                                 font=('Arial', 14, 'bold'), bg='#f0f0f0')
        log_frame.pack(fill='x', padx=20, pady=10)
        
        self.log_text = tk.Text(log_frame, height=4, font=('Arial', 9))
        self.log_text.pack(fill='x', padx=10, pady=10)
        
        # Initial log
        self.log_activity("System initialized - RFID test mode active")
    
    def update_cards_list(self):
        """Update authorized cards display"""
        self.cards_listbox.delete(0, tk.END)
        for card_id, info in self.authorized_cards.items():
            display_text = f"{card_id} - {info['name']} ({info['level']})"
            self.cards_listbox.insert(tk.END, display_text)
    
    def log_activity(self, message):
        """Log activity with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}\\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update()
    
    def lock_system(self):
        """Lock the system (simulate NOT GOOD status)"""
        self.is_locked = True
        self.lock_reason = "NOT GOOD - Cross connection detected"
        
        # Update UI
        self.lock_status_label.config(text="🔒 LOCKED", bg='#f8d7da', fg='#721c24')
        self.lock_reason_label.config(text=f"Reason: {self.lock_reason}")
        
        self.log_activity(f"🔒 SYSTEM LOCKED: {self.lock_reason}")
        messagebox.showwarning("System Locked", 
                              f"System locked due to: {self.lock_reason}\\n\\n"
                              "Use authorized RFID card to unlock.")
    
    def unlock_system(self):
        """Unlock the system manually (for testing)"""
        if not self.is_locked:
            messagebox.showinfo("Info", "System is already unlocked")
            return
        
        self.is_locked = False
        self.lock_reason = ""
        
        # Update UI
        self.lock_status_label.config(text="🔓 UNLOCKED", bg='#d4edda', fg='#155724')
        self.lock_reason_label.config(text="System ready")
        
        self.log_activity("🔓 SYSTEM UNLOCKED: Manual unlock")
        messagebox.showinfo("System Unlocked", "System unlocked manually")
    
    def scan_card(self):
        """Simulate RFID card scan"""
        card_id = self.card_id_entry.get().strip()
        
        if not card_id:
            messagebox.showerror("Error", "Please enter a Card ID")
            return
        
        self.log_activity(f"📱 Card scanned: {card_id}")
        
        # Check if card is authorized
        if card_id in self.authorized_cards:
            card_info = self.authorized_cards[card_id]
            self.log_activity(f"✅ Card authorized: {card_info['name']} ({card_info['level']})")
            
            if self.is_locked:
                # Unlock with authorized card
                self.is_locked = False
                self.lock_reason = ""
                
                # Update UI
                self.lock_status_label.config(text="🔓 UNLOCKED", bg='#d4edda', fg='#155724')
                self.lock_reason_label.config(text="Unlocked by RFID card")
                
                self.log_activity(f"🔓 SYSTEM UNLOCKED by: {card_info['name']}")
                messagebox.showinfo("Access Granted", 
                                   f"System unlocked by:\\n{card_info['name']} ({card_info['level']})")
            else:
                messagebox.showinfo("Access Granted", 
                                   f"Card recognized:\\n{card_info['name']} ({card_info['level']})\\n\\nSystem already unlocked.")
        else:
            self.log_activity(f"❌ Card unauthorized: {card_id}")
            messagebox.showerror("Access Denied", 
                               f"Card {card_id} is not authorized!\\n\\nAccess denied.")
    
    def add_test_scenarios(self):
        """Add test scenario buttons"""
        scenario_frame = tk.Frame(self.root, bg='#f0f0f0')
        scenario_frame.pack(pady=10)
        
        # Scenario 1: Normal workflow
        scenario1_btn = tk.Button(scenario_frame, text="Test: Normal Workflow", 
                                 font=('Arial', 10),
                                 bg='#17a2b8', fg='white',
                                 command=self.test_normal_workflow)
        scenario1_btn.pack(side='left', padx=5)
        
        # Scenario 2: Unauthorized card
        scenario2_btn = tk.Button(scenario_frame, text="Test: Unauthorized Card", 
                                 font=('Arial', 10),
                                 bg='#ffc107', fg='black',
                                 command=self.test_unauthorized_card)
        scenario2_btn.pack(side='left', padx=5)
    
    def test_normal_workflow(self):
        """Test normal RFID workflow"""
        self.log_activity("🧪 Starting normal workflow test...")
        
        # Step 1: Lock system
        self.lock_system()
        self.root.after(2000, self._continue_normal_test)
    
    def _continue_normal_test(self):
        """Continue normal workflow test"""
        # Step 2: Scan authorized card
        self.card_id_entry.delete(0, tk.END)
        self.card_id_entry.insert(0, "1234567890")
        self.scan_card()
        
        self.log_activity("✅ Normal workflow test completed")
    
    def test_unauthorized_card(self):
        """Test unauthorized card scenario"""
        self.log_activity("🧪 Starting unauthorized card test...")
        
        # Lock system first
        if not self.is_locked:
            self.lock_system()
        
        # Try unauthorized card
        self.root.after(1000, self._continue_unauthorized_test)
    
    def _continue_unauthorized_test(self):
        """Continue unauthorized card test"""
        self.card_id_entry.delete(0, tk.END)
        self.card_id_entry.insert(0, "9999999999")  # Unauthorized card
        self.scan_card()
        
        self.log_activity("✅ Unauthorized card test completed")

def main():
    root = tk.Tk()
    app = SimpleRFIDTest(root)
    
    # Add test scenarios
    app.add_test_scenarios()
    
    root.mainloop()

if __name__ == '__main__':
    main()