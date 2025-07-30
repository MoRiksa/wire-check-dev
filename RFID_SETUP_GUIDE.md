# RFID RDM6300 Setup Guide

## Hardware Connection

### Pin Connections
```
RDM6300 Reader -> Raspberry Pi
RX              -> GPIO 14 (TXD)
TX              -> GPIO 15 (RXD)
VCC             -> 5V
GND             -> GND
```

### Physical Pin Layout
```
Raspberry Pi GPIO Header:
Pin 8  (GPIO 14 - TXD) -> RDM6300 RX
Pin 10 (GPIO 15 - RXD) -> RDM6300 TX
Pin 2  (5V)            -> RDM6300 VCC
Pin 6  (GND)           -> RDM6300 GND
```

## Software Configuration

### 1. Enable UART
```bash
sudo raspi-config
```
- Navigate to: Interface Options -> Serial Port
- Disable serial console: **No**
- Enable serial port hardware: **Yes**

### 2. Edit Boot Config
```bash
sudo nano /boot/config.txt
```
Add line:
```
enable_uart=1
```

### 3. Reboot
```bash
sudo reboot
```

### 4. Test Serial Port
```bash
ls -la /dev/ttyAMA0
```
Should show the serial device.

## Testing RFID

### Quick Test
```bash
cd wire_checker-python-dev
python3 rfid_simple_test.py
```

### Full System Test
```bash
python3 test_rfid_system.py
```

## Troubleshooting

### No Serial Device
- Check `/boot/config.txt` has `enable_uart=1`
- Verify connections: RX->TX, TX->RX
- Reboot after config changes

### Permission Denied
```bash
sudo usermod -a -G dialout $USER
sudo reboot
```

### Card Not Reading
- Check 5V power supply
- Verify RX/TX are not swapped
- Test with known working 125kHz card
- Check baudrate (9600 for RDM6300)

## Card Format
RDM6300 sends 12-byte data:
- Start byte: 0x02
- 10 ASCII hex digits (card ID)
- End byte: 0x03

Example: `0x02 31 32 33 34 35 36 37 38 39 30 0x03`
Card ID: `1234567890`