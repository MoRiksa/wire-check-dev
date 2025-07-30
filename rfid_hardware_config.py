# RFID Hardware Configuration
# Sesuaikan dengan setup hardware Anda

# RFID Reader Configuration
RFID_CONFIG = {
    # Serial port untuk RFID reader RDM6300
    # RDM6300 RX -> GPIO 14 (TXD)
    # RDM6300 TX -> GPIO 15 (RXD) 
    # RDM6300 VCC -> 5V, GND -> GND
    'port': '/dev/ttyAMA0',  # Hardware UART GPIO 14-15
                             # Enable: sudo raspi-config -> Interface -> Serial
                             # Add 'enable_uart=1' to /boot/config.txt
    
    'baudrate': 9600,        # RDM6300 default baudrate
    'timeout': 1,            # Serial read timeout
    
    # Card ID format
    'card_id_length': 10,    # RDM6300 sends 10-byte card ID
    'start_byte': 0x02,      # STX byte
    'end_byte': 0x03,        # ETX byte
}

# GPIO Pin Configuration
GPIO_CONFIG = {
    # Solenoid control pins
    'solenoid_1': 13,        # Main solenoid
    'solenoid_2': 15,        # Secondary solenoid
    
    # LED indicators (jika diperlukan)
    'led_red': 2,
    'led_yellow': 3,
    'led_green': 4,
    
    # Buzzer (jika diperlukan)
    'buzzer': 18,
}

# System Behavior
SYSTEM_CONFIG = {
    # Auto-lock behavior
    'auto_lock_on_not_good': True,
    'lock_timeout': 0,       # 0 = no timeout, manual unlock only
    
    # Logging
    'enable_audit_log': True,
    'max_log_entries': 1000,
    'log_file': 'rfid_unlock_log.json',
    
    # Card management
    'max_authorized_cards': 50,
    'default_card_level': 'tech',
}

# Default Authorized Cards (untuk testing)
DEFAULT_CARDS = [
    {
        'id': '0012588345',
        'name': 'User Card',
        'level': 'admin',
        'description': 'Primary user access card'
    },
    {
        'id': '1234567890',
        'name': 'Supervisor Card',
        'level': 'admin',
        'description': 'Main supervisor access'
    },
    {
        'id': '0987654321', 
        'name': 'Technician Card',
        'level': 'tech',
        'description': 'Technician access'
    },
    {
        'id': '1122334455',
        'name': 'Manager Card', 
        'level': 'manager',
        'description': 'Manager access'
    }
]