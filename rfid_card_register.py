#!/usr/bin/env python3
"""
RFID Card Registration - Raspberry Pi
Register new RFID cards to the system
"""

import serial
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class RFIDCardRegister:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 RFID Card Registration")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # RFID serial connection
        self.ser = None
        self.cards_file = "authorized_cards.json"
        self.authorized_cards = self.load_cards()
        
        self.create_widgets()
        self.init_serial()
    
    def load_cards(self):
        """Load authorized cards from file"""
        if os.path.exists(self.cards_file):
            try:
                with open(self.cards_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default cards
        return {
            "0012588345": {
                "name": "User Card",
                "level": "admin", 
                "description": "Primary user access card",
                "registered": datetime.now().isoformat()
            }
        }
    
    def save_cards(self):
        """Save authorized cards to file"""
        try:
            with open(self.cards_file, 'w') as f:
                json.dump(self.authorized_cards, f, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save cards: {e}")
            return False
    
    def init_serial(self):
        """Initialize RFID serial connection"""
        try:
            self.ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
            self.status_label.config(text="📡 RFID Reader: Connected", fg='green')
        except Exception as e:
            self.status_label.config(text=f"❌ RFID Reader: {e}", fg='red')
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="🔐 RFID Card Registration", 
                              font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # Status
        self.status_label = tk.Label(self.root, text="📡 RFID Reader: Connecting...", 
                                    font=('Arial', 12), bg='#f0f0f0')
        self.status_label.pack(pady=5)
        
        # Card scanning section
        scan_frame = tk.LabelFrame(self.root, text="Scan New Card", 
                                  font=('Arial', 14, 'bold'), bg='#f0f0f0')
        scan_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(scan_frame, text="Place RFID card near reader...", 
                font=('Arial', 12), bg='#f0f0f0').pack(pady=10)
        
        self.scan_button = tk.Button(scan_frame, text="🔍 Start Scanning", 
                                    font=('Arial', 12, 'bold'),
                                    bg='#007bff', fg='white',
                                    command=self.toggle_scanning)
        self.scan_button.pack(pady=10)
        
        # Card details section
        details_frame = tk.LabelFrame(self.root, text="Card Details", 
                                     font=('Arial', 14, 'bold'), bg='#f0f0f0')
        details_frame.pack(fill='x', padx=20, pady=10)
        
        # Card ID (read-only)
        tk.Label(details_frame, text="Card ID:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w', padx=10)
        self.card_id_var = tk.StringVar()
        self.card_id_entry = tk.Entry(details_frame, textvariable=self.card_id_var, 
                                     font=('Arial', 12), state='readonly', width=30)
        self.card_id_entry.pack(padx=10, pady=5)
        
        # Card name
        tk.Label(details_frame, text="Card Name:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w', padx=10)
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(details_frame, textvariable=self.name_var, 
                                  font=('Arial', 12), width=30)
        self.name_entry.pack(padx=10, pady=5)
        
        # Access level
        tk.Label(details_frame, text="Access Level:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w', padx=10)
        self.level_var = tk.StringVar(value="tech")
        level_combo = ttk.Combobox(details_frame, textvariable=self.level_var, 
                                  values=["admin", "manager", "tech"], state="readonly")
        level_combo.pack(padx=10, pady=5)
        
        # Description
        tk.Label(details_frame, text="Description:", font=('Arial', 12), bg='#f0f0f0').pack(anchor='w', padx=10)
        self.desc_var = tk.StringVar()
        self.desc_entry = tk.Entry(details_frame, textvariable=self.desc_var, 
                                  font=('Arial', 12), width=30)
        self.desc_entry.pack(padx=10, pady=5)
        
        # Register button
        self.register_button = tk.Button(details_frame, text="✅ Register Card", 
                                        font=('Arial', 12, 'bold'),
                                        bg='#28a745', fg='white',
                                        command=self.register_card,
                                        state='disabled')
        self.register_button.pack(pady=15)
        
        # Registered cards list
        list_frame = tk.LabelFrame(self.root, text="Registered Cards", 
                                  font=('Arial', 14, 'bold'), bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Cards listbox with scrollbar
        list_container = tk.Frame(list_frame, bg='#f0f0f0')
        list_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.cards_listbox = tk.Listbox(list_container, font=('Arial', 10))
        scrollbar = tk.Scrollbar(list_container, orient='vertical', command=self.cards_listbox.yview)
        self.cards_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.cards_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Delete button
        delete_button = tk.Button(list_frame, text="🗑️ Delete Selected", 
                                 font=('Arial', 10),
                                 bg='#dc3545', fg='white',
                                 command=self.delete_card)
        delete_button.pack(pady=5)
        
        # Update cards list
        self.update_cards_list()
        
        # Start scanning automatically
        self.scanning = False
        self.root.after(1000, self.toggle_scanning)
    
    def update_cards_list(self):
        """Update registered cards display"""
        self.cards_listbox.delete(0, tk.END)
        for card_id, info in self.authorized_cards.items():
            display_text = f"{card_id} - {info['name']} ({info['level']})"
            self.cards_listbox.insert(tk.END, display_text)
    
    def toggle_scanning(self):
        """Toggle RFID scanning"""
        if not self.ser:
            messagebox.showerror("Error", "RFID reader not connected")
            return
        
        if not self.scanning:
            self.scanning = True
            self.scan_button.config(text="⏹️ Stop Scanning", bg='#dc3545')
            self.scan_rfid()
        else:
            self.scanning = False
            self.scan_button.config(text="🔍 Start Scanning", bg='#007bff')
    
    def scan_rfid(self):
        """Scan for RFID cards"""
        if not self.scanning or not self.ser:
            return
        
        try:
            if self.ser.in_waiting:
                data = self.ser.read(14)
                
                if len(data) >= 14 and data[0] == 0x02 and data[-1] == 0x03:
                    tag = data[1:11].decode('utf-8')
                    
                    # Update card ID field
                    self.card_id_var.set(tag)
                    
                    # Check if card already registered
                    if tag in self.authorized_cards:
                        info = self.authorized_cards[tag]
                        self.name_var.set(info['name'])
                        self.level_var.set(info['level'])
                        self.desc_var.set(info.get('description', ''))
                        
                        messagebox.showinfo("Card Found", 
                                          f"Card already registered:\\n{info['name']} ({info['level']})")
                        self.register_button.config(text="✏️ Update Card", state='normal')
                    else:
                        # New card
                        self.name_var.set("")
                        self.level_var.set("tech")
                        self.desc_var.set("")
                        
                        messagebox.showinfo("New Card", f"New card detected: {tag}\\nPlease fill in details.")
                        self.register_button.config(text="✅ Register Card", state='normal')
                        
                        # Focus on name entry
                        self.name_entry.focus()
        
        except Exception as e:
            print(f"Scan error: {e}")
        
        # Continue scanning
        if self.scanning:
            self.root.after(100, self.scan_rfid)
    
    def register_card(self):
        """Register/update card"""
        card_id = self.card_id_var.get().strip()
        name = self.name_var.get().strip()
        level = self.level_var.get()
        description = self.desc_var.get().strip()
        
        if not card_id:
            messagebox.showerror("Error", "No card ID detected")
            return
        
        if not name:
            messagebox.showerror("Error", "Please enter card name")
            return
        
        # Register card
        self.authorized_cards[card_id] = {
            "name": name,
            "level": level,
            "description": description,
            "registered": datetime.now().isoformat()
        }
        
        if self.save_cards():
            self.update_cards_list()
            messagebox.showinfo("Success", f"Card registered successfully:\\n{name} ({level})")
            
            # Clear form
            self.card_id_var.set("")
            self.name_var.set("")
            self.level_var.set("tech")
            self.desc_var.set("")
            self.register_button.config(state='disabled')
    
    def delete_card(self):
        """Delete selected card"""
        selection = self.cards_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a card to delete")
            return
        
        # Get card ID from selection
        selected_text = self.cards_listbox.get(selection[0])
        card_id = selected_text.split(" - ")[0]
        
        if card_id in self.authorized_cards:
            card_name = self.authorized_cards[card_id]['name']
            
            if messagebox.askyesno("Confirm Delete", 
                                  f"Delete card:\\n{card_name} ({card_id})?"):
                del self.authorized_cards[card_id]
                if self.save_cards():
                    self.update_cards_list()
                    messagebox.showinfo("Success", "Card deleted successfully")
    
    def __del__(self):
        """Cleanup"""
        if self.ser:
            try:
                self.ser.close()
            except:
                pass

def main():
    root = tk.Tk()
    app = RFIDCardRegister(root)
    root.mainloop()

if __name__ == '__main__':
    main()