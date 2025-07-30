# Handle serial import for Windows compatibility
try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    print("pyserial not available - using simulation mode")
    SERIAL_AVAILABLE = False
    
import time
import json
import os
import threading
from datetime import datetime

# Handle GPIO import
try:
    import RPi.GPIO as GPIO
    RASPBERRY_PI = True
except ImportError:
    from mock_gpio import GPIO
    RASPBERRY_PI = False

class RFIDManager:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.is_reading = False
        self.authorized_cards = []
        self.lock_status = False
        self.last_card_id = None
        
        # Load authorized cards
        self.load_authorized_cards()
        
        # Initialize serial connection
        self.init_serial()
    
    def init_serial(self):
        """Initialize serial connection to RDM6300"""
        try:
            if RASPBERRY_PI and SERIAL_AVAILABLE:
                self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
                print(f"RFID Reader connected on {self.port}")
            else:
                print("RFID Reader simulation mode (Windows/No Serial)")
                self.serial_conn = None
        except Exception as e:
            print(f"Failed to connect RFID Reader: {e}")
            self.serial_conn = None
    
    def load_authorized_cards(self):
        """Load authorized RF ID cards from file"""
        config_file = 'rfid_authorized_cards.json'
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    self.authorized_cards = data.get('authorized_cards', [])
            else:
                # Default authorized cards
                self.authorized_cards = [
                    {"id": "1234567890", "name": "Supervisor Card", "level": "admin"},
                    {"id": "0987654321", "name": "Technician Card", "level": "tech"},
                    {"id": "1122334455", "name": "Manager Card", "level": "manager"}
                ]
                self.save_authorized_cards()
            
            print(f"Loaded {len(self.authorized_cards)} authorized RF ID cards")
            
        except Exception as e:
            print(f"Error loading authorized cards: {e}")
            self.authorized_cards = []
    
    def save_authorized_cards(self):
        """Save authorized cards to file"""
        config_file = 'rfid_authorized_cards.json'
        try:
            data = {
                'authorized_cards': self.authorized_cards,
                'updated_at': datetime.now().isoformat()
            }
            with open(config_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving authorized cards: {e}")
    
    def add_authorized_card(self, card_id, name, level="tech"):
        """Add new authorized card"""
        new_card = {
            "id": card_id,
            "name": name,
            "level": level,
            "added_at": datetime.now().isoformat()
        }
        
        # Check if card already exists
        for card in self.authorized_cards:
            if card['id'] == card_id:
                card.update(new_card)
                self.save_authorized_cards()
                return True
        
        # Add new card
        self.authorized_cards.append(new_card)
        self.save_authorized_cards()
        return True
    
    def remove_authorized_card(self, card_id):
        """Remove authorized card"""
        self.authorized_cards = [card for card in self.authorized_cards if card['id'] != card_id]
        self.save_authorized_cards()
    
    def is_card_authorized(self, card_id):
        """Check if card is authorized"""
        for card in self.authorized_cards:
            if card['id'] == card_id:
                return True, card
        return False, None
    
    def read_card(self):
        """Read RF ID card from RDM6300"""
        if not self.serial_conn:
            # Simulation mode for Windows testing
            return self.simulate_card_read()
        
        try:
            if self.serial_conn.in_waiting > 0:
                # RDM6300 sends 12 bytes: STX(1) + DATA(10) + ETX(1)
                data = self.serial_conn.read(12)
                
                if len(data) == 12 and data[0] == 0x02 and data[11] == 0x03:
                    # Extract card ID from bytes 1-10
                    card_id = ''.join([f'{b:02X}' for b in data[1:11]])
                    return card_id
            
        except Exception as e:
            print(f"Error reading RFID card: {e}")
        
        return None
    
    def simulate_card_read(self):
        """Simulate card reading for Windows testing"""
        # Return a test card ID occasionally
        import random
        if random.random() < 0.1:  # 10% chance
            test_cards = ["1234567890", "0987654321", "1122334455", "INVALID123"]
            return random.choice(test_cards)
        return None
    
    def start_reading(self, callback=None):
        """Start continuous card reading"""
        self.is_reading = True
        
        def read_loop():
            while self.is_reading:
                try:
                    card_id = self.read_card()
                    if card_id and card_id != self.last_card_id:
                        self.last_card_id = card_id
                        
                        # Check authorization
                        is_authorized, card_info = self.is_card_authorized(card_id)
                        
                        if callback:
                            callback(card_id, is_authorized, card_info)
                        
                        print(f"RFID Card: {card_id} - {'AUTHORIZED' if is_authorized else 'UNAUTHORIZED'}")
                    
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"Error in RFID read loop: {e}")
                    time.sleep(1)
        
        # Start reading in separate thread
        read_thread = threading.Thread(target=read_loop, daemon=True)
        read_thread.start()
    
    def stop_reading(self):
        """Stop card reading"""
        self.is_reading = False
        if self.serial_conn:
            self.serial_conn.close()
    
    def get_authorized_cards_list(self):
        """Get list of authorized cards for display"""
        return self.authorized_cards.copy()

class SolenoidLockManager:
    def __init__(self, solenoid_pin=13, solenoid2_pin=15):
        self.solenoid_pin = solenoid_pin
        self.solenoid2_pin = solenoid2_pin
        self.is_locked = False
        self.lock_reason = ""
        self.rfid_manager = RFIDManager()
        
        # Setup GPIO
        if RASPBERRY_PI:
            GPIO.setup(self.solenoid_pin, GPIO.OUT)
            GPIO.setup(self.solenoid2_pin, GPIO.OUT)
            GPIO.output(self.solenoid_pin, GPIO.HIGH)  # Default off
            GPIO.output(self.solenoid2_pin, GPIO.HIGH)  # Default off
        
        # Start RFID reading
        self.rfid_manager.start_reading(self.on_card_scanned)
    
    def lock_solenoids(self, reason="NOT GOOD status"):
        """Lock solenoids - cannot be unlocked except by authorized RFID"""
        self.is_locked = True
        self.lock_reason = reason
        
        if RASPBERRY_PI:
            GPIO.output(self.solenoid_pin, GPIO.HIGH)  # Lock position
            GPIO.output(self.solenoid2_pin, GPIO.HIGH)  # Lock position
        
        print(f"🔒 SOLENOIDS LOCKED: {reason}")
        return True
    
    def unlock_solenoids(self, card_info=None):
        """Unlock solenoids - only via authorized RFID"""
        if not self.is_locked:
            return True
        
        self.is_locked = False
        self.lock_reason = ""
        
        if RASPBERRY_PI:
            GPIO.output(self.solenoid_pin, GPIO.LOW)   # Unlock position
            GPIO.output(self.solenoid2_pin, GPIO.LOW)  # Unlock position
        
        unlock_by = card_info['name'] if card_info else "Unknown"
        print(f"🔓 SOLENOIDS UNLOCKED by: {unlock_by}")
        
        # Log unlock event
        self.log_unlock_event(card_info)
        return True
    
    def on_card_scanned(self, card_id, is_authorized, card_info):
        """Handle RFID card scan"""
        if self.is_locked and is_authorized:
            self.unlock_solenoids(card_info)
            return True
        elif self.is_locked and not is_authorized:
            print(f"❌ UNAUTHORIZED CARD: {card_id}")
            return False
        
        return False
    
    def control_solenoid(self, enable, force=False):
        """Control solenoid with lock check"""
        if self.is_locked and not force:
            print(f"🔒 Solenoid control blocked - LOCKED ({self.lock_reason})")
            return False
        
        if RASPBERRY_PI:
            if enable:
                GPIO.output(self.solenoid_pin, GPIO.LOW)   # On
                GPIO.output(self.solenoid2_pin, GPIO.LOW)  # On
            else:
                GPIO.output(self.solenoid_pin, GPIO.HIGH)  # Off
                GPIO.output(self.solenoid2_pin, GPIO.HIGH) # Off
        
        return True
    
    def log_unlock_event(self, card_info):
        """Log unlock events for audit"""
        log_file = 'rfid_unlock_log.json'
        
        event = {
            'timestamp': datetime.now().isoformat(),
            'card_id': card_info['id'] if card_info else 'Unknown',
            'card_name': card_info['name'] if card_info else 'Unknown',
            'card_level': card_info['level'] if card_info else 'Unknown',
            'lock_reason': self.lock_reason
        }
        
        try:
            # Load existing log
            log_data = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            
            # Add new event
            log_data.append(event)
            
            # Keep only last 1000 events
            if len(log_data) > 1000:
                log_data = log_data[-1000:]
            
            # Save log
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"Error logging unlock event: {e}")
    
    def get_lock_status(self):
        """Get current lock status"""
        return {
            'is_locked': self.is_locked,
            'lock_reason': self.lock_reason,
            'authorized_cards_count': len(self.rfid_manager.authorized_cards)
        }
    
    def add_authorized_card(self, card_id, name, level="tech"):
        """Add authorized card"""
        return self.rfid_manager.add_authorized_card(card_id, name, level)
    
    def get_authorized_cards(self):
        """Get authorized cards list"""
        return self.rfid_manager.get_authorized_cards_list()

# Global instance
solenoid_lock_manager = None

def get_solenoid_lock_manager():
    """Get global solenoid lock manager instance"""
    global solenoid_lock_manager
    if solenoid_lock_manager is None:
        solenoid_lock_manager = SolenoidLockManager()
    return solenoid_lock_manager