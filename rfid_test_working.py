#!/usr/bin/env python3
"""
RFID Test - Working Version
Based on user's working reference code
"""

import serial
import time

def test_rfid_reader():
    """Test RFID reader with working configuration"""
    try:
        # Buka koneksi ke serial0 (GPIO15 / RX)
        ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
        
        print("🔍 RFID Reader Test - Working Version")
        print("📡 Port: /dev/serial0")
        print("⚡ Baudrate: 9600")
        print("📋 Expected card: 0012588345")
        print("-" * 40)
        print("Silakan dekatkan RFID tag...")
        print("Tekan Ctrl+C untuk stop")
        print()
        
        while True:
            if ser.in_waiting:
                data = ser.read(14)  # RDM6300 kirim 14 byte
                
                print(f"📥 Raw data ({len(data)} bytes): {data.hex()}")
                
                if len(data) >= 14 and data[0] == 0x02 and data[-1] == 0x03:
                    tag = data[1:11].decode('utf-8')
                    print(f"✅ ID Tag RFID: {tag}")
                    
                    # Check if it's the expected card
                    if tag == "0012588345":
                        print("🎉 AUTHORIZED CARD DETECTED!")
                    else:
                        print("⚠️  Unknown card")
                    
                    print("-" * 40)
                else:
                    print("❌ Invalid data format")
                    if len(data) > 0:
                        print(f"   Start byte: 0x{data[0]:02x} (expected: 0x02)")
                        if len(data) >= 14:
                            print(f"   End byte: 0x{data[-1]:02x} (expected: 0x03)")
                    print("-" * 40)
            
            time.sleep(0.1)
            
    except serial.SerialException as e:
        print(f"❌ Serial error: {e}")
        print("💡 Check:")
        print("   - RFID hardware connections")
        print("   - Serial port permissions: sudo usermod -a -G dialout $USER")
        print("   - UART enabled in raspi-config")
    except KeyboardInterrupt:
        print("\n🛑 Test stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        try:
            ser.close()
            print("📴 Serial connection closed")
        except:
            pass

def test_authorized_cards():
    """Test with list of authorized cards"""
    authorized_cards = {
        "0012588345": {"name": "User Card", "level": "admin"},
        "1234567890": {"name": "Supervisor Card", "level": "admin"},
        "0987654321": {"name": "Technician Card", "level": "tech"},
    }
    
    try:
        ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
        
        print("🔐 RFID Authorization Test")
        print("📋 Authorized Cards:")
        for card_id, info in authorized_cards.items():
            print(f"   {card_id} - {info['name']} ({info['level']})")
        print("-" * 50)
        print("Silakan dekatkan RFID tag...")
        print("Tekan Ctrl+C untuk stop")
        print()
        
        while True:
            if ser.in_waiting:
                data = ser.read(14)
                
                if len(data) >= 14 and data[0] == 0x02 and data[-1] == 0x03:
                    tag = data[1:11].decode('utf-8')
                    print(f"📱 Card scanned: {tag}")
                    
                    if tag in authorized_cards:
                        card_info = authorized_cards[tag]
                        print(f"✅ AUTHORIZED: {card_info['name']} ({card_info['level']})")
                        print("🔓 Access granted - System unlocked")
                    else:
                        print("❌ UNAUTHORIZED CARD")
                        print("🔒 Access denied - System remains locked")
                    
                    print("-" * 50)
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 Test stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        try:
            ser.close()
        except:
            pass

if __name__ == "__main__":
    print("🧪 RFID Test Options:")
    print("1. Basic RFID reader test")
    print("2. Authorization test")
    
    choice = input("\nPilih test (1/2): ").strip()
    
    if choice == "1":
        test_rfid_reader()
    elif choice == "2":
        test_authorized_cards()
    else:
        print("❌ Invalid choice")