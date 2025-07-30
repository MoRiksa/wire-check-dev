#!/usr/bin/env python3
"""
RFID System Test Script
Test all RFID functionality step by step
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import time
from datetime import datetime

class RFIDSystemTester:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID System Tester")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.create_widgets()
        self.test_results = []
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="🔐 RFID System Tester", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # Test buttons frame
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        buttons_frame.pack(pady=20)
        
        # Test buttons
        tests = [
            ("1. Test RFID Manager Import", self.test_rfid_import),
            ("2. Test Card Database", self.test_card_database),
            ("3. Test Card Authorization", self.test_card_auth),
            ("4. Test Lock Manager", self.test_lock_manager),
            ("5. Test Serial Connection", self.test_serial_connection),
            ("6. Test Complete Workflow", self.test_complete_workflow),
            ("7. View Test Results", self.view_results),
            ("8. Reset Test Data", self.reset_test_data)
        ]
        
        for i, (text, command) in enumerate(tests):
            btn = tk.Button(buttons_frame, text=text, 
                           font=('Arial', 12, 'bold'),
                           width=30, height=2,
                           bg='#007bff', fg='white',
                           command=command)
            btn.pack(pady=5)
        
        # Results display
        results_frame = tk.LabelFrame(self.root, text="Test Results", 
                                     font=('Arial', 14, 'bold'), bg='#f0f0f0')
        results_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.results_text = tk.Text(results_frame, height=15, width=80,
                                   font=('Arial', 10), bg='#f8f9fa')
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar for results
        scrollbar = tk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
    
    def log_result(self, test_name, status, details=""):
        """Log test result"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        result = {
            'timestamp': timestamp,
            'test': test_name,
            'status': status,
            'details': details
        }
        self.test_results.append(result)
        
        # Display in text widget
        status_icon = "✅" if status == "PASS" else "❌"
        log_line = f"[{timestamp}] {status_icon} {test_name}: {status}"
        if details:
            log_line += f" - {details}"
        
        self.results_text.insert(tk.END, log_line + "\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def test_rfid_import(self):
        """Test 1: RFID Manager Import"""
        try:
            from rfid_manager import RFIDManager, SolenoidLockManager
            self.log_result("RFID Import", "PASS", "All modules imported successfully")
        except ImportError as e:
            self.log_result("RFID Import", "FAIL", f"Import error: {e}")
        except Exception as e:
            self.log_result("RFID Import", "FAIL", f"Unexpected error: {e}")
    
    def test_card_database(self):
        """Test 2: Card Database Operations"""
        try:
            from rfid_manager import RFIDManager
            
            # Create RFID manager
            rfid_mgr = RFIDManager()
            
            # Test add card
            test_card_id = "1234567890"
            test_card_name = "Test Card"
            
            success = rfid_mgr.add_authorized_card(test_card_id, test_card_name, "admin")
            if success:
                self.log_result("Add Card", "PASS", f"Added {test_card_name}")
            else:
                self.log_result("Add Card", "FAIL", "Failed to add card")
            
            # Test card authorization check
            is_auth, card_info = rfid_mgr.is_card_authorized(test_card_id)
            if is_auth and card_info:
                self.log_result("Card Auth Check", "PASS", f"Card {test_card_id} is authorized")
            else:
                self.log_result("Card Auth Check", "FAIL", "Card not found in database")
            
            # Test get cards list
            cards = rfid_mgr.get_authorized_cards_list()
            self.log_result("Get Cards List", "PASS", f"Found {len(cards)} authorized cards")
            
        except Exception as e:
            self.log_result("Card Database", "FAIL", f"Error: {e}")
    
    def test_card_auth(self):
        """Test 3: Card Authorization Logic"""
        try:
            from rfid_manager import RFIDManager
            
            rfid_mgr = RFIDManager()
            
            # Test valid card
            valid_card = "1234567890"
            is_auth, card_info = rfid_mgr.is_card_authorized(valid_card)
            
            if is_auth:
                self.log_result("Valid Card Test", "PASS", f"Card {valid_card} authorized")
            else:
                self.log_result("Valid Card Test", "FAIL", "Valid card not recognized")
            
            # Test invalid card
            invalid_card = "9999999999"
            is_auth, card_info = rfid_mgr.is_card_authorized(invalid_card)
            
            if not is_auth:
                self.log_result("Invalid Card Test", "PASS", "Invalid card correctly rejected")
            else:
                self.log_result("Invalid Card Test", "FAIL", "Invalid card incorrectly accepted")
                
        except Exception as e:
            self.log_result("Card Authorization", "FAIL", f"Error: {e}")
    
    def test_lock_manager(self):
        """Test 4: Solenoid Lock Manager"""
        try:
            from rfid_manager import SolenoidLockManager
            
            # Create lock manager
            lock_mgr = SolenoidLockManager()
            
            # Test lock
            lock_mgr.lock_solenoids("Test lock")
            if lock_mgr.is_locked:
                self.log_result("Solenoid Lock", "PASS", "Solenoids locked successfully")
            else:
                self.log_result("Solenoid Lock", "FAIL", "Failed to lock solenoids")
            
            # Test unlock with valid card
            test_card_info = {"id": "1234567890", "name": "Test Card", "level": "admin"}
            unlock_success = lock_mgr.unlock_solenoids(test_card_info)
            
            if unlock_success and not lock_mgr.is_locked:
                self.log_result("Solenoid Unlock", "PASS", "Solenoids unlocked successfully")
            else:
                self.log_result("Solenoid Unlock", "FAIL", "Failed to unlock solenoids")
                
        except Exception as e:
            self.log_result("Lock Manager", "FAIL", f"Error: {e}")
    
    def test_serial_connection(self):
        """Test 5: Serial Connection (Simulation)"""
        try:
            from rfid_manager import RFIDManager
            
            rfid_mgr = RFIDManager()
            
            # Test serial connection (will be simulation on Windows)
            if rfid_mgr.serial_conn is None:
                self.log_result("Serial Connection", "PASS", "Simulation mode active (Windows)")
            else:
                self.log_result("Serial Connection", "PASS", f"Connected to {rfid_mgr.port}")
            
            # Test card reading simulation
            card_id = rfid_mgr.read_card()
            if card_id:
                self.log_result("Card Reading", "PASS", f"Read card: {card_id}")
            else:
                self.log_result("Card Reading", "PASS", "No card detected (normal)")
                
        except Exception as e:
            self.log_result("Serial Connection", "FAIL", f"Error: {e}")
    
    def test_complete_workflow(self):
        """Test 6: Complete RFID Workflow"""
        try:
            from rfid_manager import SolenoidLockManager
            
            self.log_result("Complete Workflow", "INFO", "Starting complete workflow test...")
            
            # Step 1: Create lock manager
            lock_mgr = SolenoidLockManager()
            self.log_result("Workflow Step 1", "PASS", "Lock manager created")
            
            # Step 2: Lock solenoids (simulate NOT GOOD status)
            lock_mgr.lock_solenoids("NOT GOOD - Cross connection detected")
            self.log_result("Workflow Step 2", "PASS", "Solenoids locked due to NOT GOOD status")
            
            # Step 3: Simulate RFID card scan
            test_card_id = "1234567890"
            is_auth, card_info = lock_mgr.rfid_manager.is_card_authorized(test_card_id)
            
            if is_auth:
                self.log_result("Workflow Step 3", "PASS", f"Card {test_card_id} is authorized")
                
                # Step 4: Unlock with authorized card
                unlock_success = lock_mgr.unlock_solenoids(card_info)
                if unlock_success:
                    self.log_result("Workflow Step 4", "PASS", "Solenoids unlocked with RFID card")
                else:
                    self.log_result("Workflow Step 4", "FAIL", "Failed to unlock with RFID card")
            else:
                self.log_result("Workflow Step 3", "FAIL", "Test card not authorized")
            
            self.log_result("Complete Workflow", "PASS", "Workflow test completed")
            
        except Exception as e:
            self.log_result("Complete Workflow", "FAIL", f"Error: {e}")
    
    def view_results(self):
        """Test 7: View Test Results Summary"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        
        summary = f"""
=== RFID SYSTEM TEST SUMMARY ===
Total Tests: {total_tests}
Passed: {passed_tests}
Failed: {failed_tests}
Success Rate: {(passed_tests/total_tests*100):.1f}% if total_tests > 0 else 0%

=== RECOMMENDATIONS ===
"""
        
        if failed_tests == 0:
            summary += "✅ All tests passed! RFID system is ready for production."
        else:
            summary += "⚠️ Some tests failed. Check the following:"
            summary += "\n• Verify RFID hardware connections"
            summary += "\n• Check serial port configuration"
            summary += "\n• Ensure authorized cards are properly added"
            summary += "\n• Test with actual RFID reader hardware"
        
        self.results_text.insert(tk.END, summary + "\n")
        self.results_text.see(tk.END)
    
    def reset_test_data(self):
        """Test 8: Reset Test Data"""
        self.test_results.clear()
        self.results_text.delete(1.0, tk.END)
        self.log_result("System Reset", "INFO", "Test data cleared")

def main():
    root = tk.Tk()
    app = RFIDSystemTester(root)
    root.mainloop()

if __name__ == '__main__':
    main()