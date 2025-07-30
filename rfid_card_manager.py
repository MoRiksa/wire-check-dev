import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from rfid_manager import RFIDManager

class RFIDCardManager:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID Card Management")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        self.rfid_manager = RFIDManager()
        self.create_widgets()
        self.refresh_cards_list()
    
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
        title_label = tk.Label(main_frame, text="🔐 RFID Card Management", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(10, 20))
        
        # Add new card section
        add_card_frame = tk.LabelFrame(main_frame, text="Add New Authorized Card", 
                                      font=('Arial', 14, 'bold'), bg='#f0f0f0')
        add_card_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        # Card input fields
        input_frame = tk.Frame(add_card_frame, bg='#f0f0f0')
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Card ID:", font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5)
        self.card_id_entry = tk.Entry(input_frame, font=('Arial', 12), width=20)
        self.card_id_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="Card Name:", font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=2, sticky='w', padx=5)
        self.card_name_entry = tk.Entry(input_frame, font=('Arial', 12), width=25)
        self.card_name_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(input_frame, text="Access Level:", font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=5)
        self.card_level_combo = ttk.Combobox(input_frame, font=('Arial', 12), width=17,
                                            values=["admin", "manager", "tech", "operator"])
        self.card_level_combo.set("tech")
        self.card_level_combo.grid(row=1, column=1, padx=5)
        
        # Buttons
        buttons_frame = tk.Frame(add_card_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=10)
        
        add_btn = tk.Button(buttons_frame, text="➕ Add Card", 
                           font=('Arial', 12, 'bold'),
                           bg='#28a745', fg='white',
                           width=15, height=2,
                           command=self.add_card)
        add_btn.pack(side='left', padx=10)
        
        scan_btn = tk.Button(buttons_frame, text="📱 Scan Card", 
                            font=('Arial', 12, 'bold'),
                            bg='#007bff', fg='white',
                            width=15, height=2,
                            command=self.scan_card)
        scan_btn.pack(side='left', padx=10)
        
        # Authorized cards list
        cards_frame = tk.LabelFrame(main_frame, text="Authorized Cards", 
                                   font=('Arial', 14, 'bold'), bg='#f0f0f0')
        cards_frame.pack(fill='both', expand=True, pady=(0, 20), padx=10)
        
        # Treeview for cards list
        columns = ('ID', 'Name', 'Level', 'Added Date')
        self.cards_tree = ttk.Treeview(cards_frame, columns=columns, show='headings', height=12)
        
        # Define headings
        self.cards_tree.heading('ID', text='Card ID')
        self.cards_tree.heading('Name', text='Card Name')
        self.cards_tree.heading('Level', text='Access Level')
        self.cards_tree.heading('Added Date', text='Added Date')
        
        # Define column widths
        self.cards_tree.column('ID', width=150)
        self.cards_tree.column('Name', width=200)
        self.cards_tree.column('Level', width=100)
        self.cards_tree.column('Added Date', width=150)
        
        # Scrollbar for treeview
        tree_scrollbar = ttk.Scrollbar(cards_frame, orient='vertical', command=self.cards_tree.yview)
        self.cards_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.cards_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        tree_scrollbar.pack(side='right', fill='y', pady=10)
        
        # Card management buttons
        manage_frame = tk.Frame(main_frame, bg='#f0f0f0')
        manage_frame.pack(pady=10)
        
        refresh_btn = tk.Button(manage_frame, text="🔄 Refresh", 
                               font=('Arial', 12, 'bold'),
                               bg='#17a2b8', fg='white',
                               width=15, height=2,
                               command=self.refresh_cards_list)
        refresh_btn.pack(side='left', padx=10)
        
        remove_btn = tk.Button(manage_frame, text="🗑️ Remove Card", 
                              font=('Arial', 12, 'bold'),
                              bg='#dc3545', fg='white',
                              width=15, height=2,
                              command=self.remove_card)
        remove_btn.pack(side='left', padx=10)
        
        test_btn = tk.Button(manage_frame, text="🧪 Test Lock/Unlock", 
                            font=('Arial', 12, 'bold'),
                            bg='#fd7e14', fg='white',
                            width=18, height=2,
                            command=self.test_lock_unlock)
        test_btn.pack(side='left', padx=10)
        
        # Status display
        status_frame = tk.LabelFrame(main_frame, text="RFID System Status", 
                                    font=('Arial', 14, 'bold'), bg='#f0f0f0')
        status_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        self.status_text = tk.Text(status_frame, height=6, width=80,
                                  font=('Arial', 11), bg='#f8f9fa',
                                  relief='sunken', borderwidth=2)
        self.status_text.pack(pady=10, padx=10)
        
        # Back button
        back_btn = tk.Button(main_frame, text="🔙 Back to Main", 
                            font=('Arial', 14, 'bold'),
                            bg='#6c757d', fg='white',
                            width=20, height=2,
                            command=self.back_to_main)
        back_btn.pack(pady=20)
        
        # Start RFID reading for scan function
        self.rfid_manager.start_reading(self.on_card_detected)
        
        # Update status
        self.update_status()
    
    def add_card(self):
        """Add new authorized card"""
        card_id = self.card_id_entry.get().strip()
        card_name = self.card_name_entry.get().strip()
        card_level = self.card_level_combo.get()
        
        if not card_id or not card_name:
            messagebox.showerror("Error", "Please enter Card ID and Card Name")
            return
        
        try:
            success = self.rfid_manager.add_authorized_card(card_id, card_name, card_level)
            if success:
                messagebox.showinfo("Success", f"Card '{card_name}' added successfully!")
                self.clear_inputs()
                self.refresh_cards_list()
                self.update_status(f"✅ Added card: {card_name} ({card_id})")
            else:
                messagebox.showerror("Error", "Failed to add card")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add card: {e}")
    
    def scan_card(self):
        """Scan card to get ID automatically"""
        self.update_status("📱 Please tap your RFID card on the reader...")
        
        # Set flag to capture next scanned card
        self.scanning_for_input = True
    
    def on_card_detected(self, card_id, is_authorized, card_info):
        """Handle detected RFID card"""
        if hasattr(self, 'scanning_for_input') and self.scanning_for_input:
            # Auto-fill card ID
            self.card_id_entry.delete(0, tk.END)
            self.card_id_entry.insert(0, card_id)
            self.scanning_for_input = False
            self.update_status(f"📱 Card scanned: {card_id}")
        else:
            # Regular detection
            status = "AUTHORIZED" if is_authorized else "UNAUTHORIZED"
            name = card_info['name'] if card_info else "Unknown"
            self.update_status(f"🔍 Card detected: {card_id} - {status} ({name})")
    
    def remove_card(self):
        """Remove selected card"""
        selected = self.cards_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a card to remove")
            return
        
        item = self.cards_tree.item(selected[0])
        card_id = item['values'][0]
        card_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Removal", f"Remove card '{card_name}' ({card_id})?"):
            try:
                self.rfid_manager.remove_authorized_card(card_id)
                messagebox.showinfo("Success", f"Card '{card_name}' removed successfully!")
                self.refresh_cards_list()
                self.update_status(f"🗑️ Removed card: {card_name} ({card_id})")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove card: {e}")
    
    def refresh_cards_list(self):
        """Refresh the cards list display"""
        # Clear existing items
        for item in self.cards_tree.get_children():
            self.cards_tree.delete(item)
        
        # Add cards
        cards = self.rfid_manager.get_authorized_cards_list()
        for card in cards:
            added_date = card.get('added_at', 'Unknown')
            if added_date != 'Unknown':
                try:
                    # Format date
                    date_obj = datetime.fromisoformat(added_date.replace('Z', '+00:00'))
                    added_date = date_obj.strftime('%Y-%m-%d %H:%M')
                except:
                    pass
            
            self.cards_tree.insert('', 'end', values=(
                card['id'],
                card['name'],
                card['level'],
                added_date
            ))
    
    def test_lock_unlock(self):
        """Test lock/unlock functionality"""
        from rfid_manager import get_solenoid_lock_manager
        
        lock_manager = get_solenoid_lock_manager()
        
        if lock_manager.is_locked:
            self.update_status("🔒 System is currently LOCKED. Tap authorized card to unlock.")
        else:
            # Test lock
            lock_manager.lock_solenoids("Test lock from RFID manager")
            self.update_status("🔒 Test LOCK activated. Tap authorized card to unlock.")
    
    def clear_inputs(self):
        """Clear input fields"""
        self.card_id_entry.delete(0, tk.END)
        self.card_name_entry.delete(0, tk.END)
        self.card_level_combo.set("tech")
    
    def update_status(self, message=None):
        """Update status display"""
        if message:
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.status_text.see(tk.END)
        
        # Show system status
        cards_count = len(self.rfid_manager.get_authorized_cards_list())
        status_info = f"\n📊 System Status:\n"
        status_info += f"   • Authorized Cards: {cards_count}\n"
        status_info += f"   • RFID Reader: {'Connected' if self.rfid_manager.serial_conn else 'Simulation Mode'}\n"
        
        from rfid_manager import get_solenoid_lock_manager
        try:
            lock_manager = get_solenoid_lock_manager()
            lock_status = lock_manager.get_lock_status()
            status_info += f"   • Solenoid Lock: {'🔒 LOCKED' if lock_status['is_locked'] else '🔓 UNLOCKED'}\n"
            if lock_status['is_locked']:
                status_info += f"   • Lock Reason: {lock_status['lock_reason']}\n"
        except:
            status_info += f"   • Solenoid Lock: Not initialized\n"
        
        # Update status periodically
        self.root.after(5000, lambda: self.update_status())
    
    def back_to_main(self):
        """Return to main menu"""
        try:
            self.rfid_manager.stop_reading()
            self.root.destroy()
            
            import subprocess
            import sys
            subprocess.run([sys.executable, 'wire_checker_main_windows.py'])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return to main menu: {e}")

def main():
    root = tk.Tk()
    app = RFIDCardManager(root)
    root.mainloop()

if __name__ == '__main__':
    main()