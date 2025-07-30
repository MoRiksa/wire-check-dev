# Pin Configuration Form Guide

## Overview
The Pin Configuration Form allows you to create custom wire checker configurations with your own PIN IN and PIN OUT assignments, along with product information.

## Features

### 1. Product Information Input
- **Product Name**: Enter the name of your product/wire assembly
- **Product No**: Enter the product number or part number

### 2. Wire Pair Configuration
- Support for up to 6 wire pairs
- **PIN OUT (GPIO)**: The GPIO pin that sends the signal
- **PIN IN (GPIO)**: The GPIO pin that receives the signal
- Each GPIO pin can only be used once

### 3. Template Support
- **Load Template**: Load default 4-pair configuration
- **Create Template**: Generate a text file template for manual editing
- **Load from File**: Import configuration from a text file

## How to Use

### Method 1: Direct Form Input
1. Run `python3 wire_checker_main.py`
2. Click "Pin Configuration"
3. Fill in Product Name and Product No
4. Enter GPIO pin numbers for each wire pair
5. Click "Save Configuration" to save
6. Click "Apply & Test" to create and run custom checker

### Method 2: Template File (Notepad)
1. In Pin Configuration Form, click "Create Template"
2. Save the template file (e.g., `my_config.txt`)
3. Open the file in notepad/text editor
4. Edit the configuration:
   ```
   Product Name: My Wire Assembly
   Product No: MWA-001
   Pair 1: GPIO17 -> GPIO27
   Pair 2: GPIO22 -> GPIO10
   Pair 3: GPIO9 -> GPIO11
   Pair 4: GPIO5 -> GPIO6
   ```
5. Save the file
6. In Pin Configuration Form, click "Load from File"
7. Select your edited template file
8. Click "Apply & Test"

### Method 3: Using Existing Template
1. Copy `pin_config_template.txt`
2. Edit it with your configuration
3. Use "Load from File" to import it

## Template Format

```
# Product Information
Product Name: Your Product Name
Product No: Your Product Number

# Wire Pair Configuration
Pair 1: GPIO17 -> GPIO27
Pair 2: GPIO22 -> GPIO10
Pair 3: GPIO9 -> GPIO11
Pair 4: GPIO5 -> GPIO6
```

## GPIO Pin Guidelines

### Available GPIO Pins
- Valid pins: 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27

### Reserved Pins (Avoid These)
- **GPIO 2**: Red LED
- **GPIO 3**: Yellow LED  
- **GPIO 4**: Green LED
- **GPIO 13**: Solenoid 1
- **GPIO 15**: Solenoid 2
- **GPIO 18**: Buzzer

## Generated Files

### Configuration File
- `pin_configuration.json`: Stores your configuration in JSON format
- Used by the system to remember your settings

### Custom Wire Checker
- `wire_checker_custom_[product_no].py`: Generated custom wire checker
- Contains your specific pin configuration
- Can be run independently

## Usage Examples

### Example 1: 3-Pair Configuration
```
Product Name: Basic Wire Harness
Product No: BWH-100
Pair 1: GPIO17 -> GPIO27
Pair 2: GPIO22 -> GPIO10
Pair 3: GPIO9 -> GPIO11
```

### Example 2: 6-Pair Configuration
```
Product Name: Complex Wire Assembly
Product No: CWA-200
Pair 1: GPIO17 -> GPIO27
Pair 2: GPIO22 -> GPIO10
Pair 3: GPIO9 -> GPIO11
Pair 4: GPIO5 -> GPIO6
Pair 5: GPIO7 -> GPIO8
Pair 6: GPIO19 -> GPIO20
```

## Validation Rules

1. **Product Information**: Both Product Name and Product No are required
2. **Pin Pairs**: If you specify one pin in a pair, you must specify both
3. **Unique Pins**: Each GPIO pin can only be used once across all pairs
4. **Valid Numbers**: PIN numbers must be valid integers
5. **Reserved Pins**: System will warn if you use reserved pins

## Troubleshooting

### "No Custom Checker Found"
- You need to create a configuration first using "Apply & Test"
- Check if `wire_checker_custom_*.py` files exist

### "PIN already used"
- Each GPIO pin can only be assigned once
- Check for duplicate pin assignments

### "Invalid PIN number"
- Ensure you're using valid GPIO pin numbers
- Avoid reserved pins (2, 3, 4, 13, 15, 18)

### Template File Not Loading
- Check file format matches the expected template
- Ensure GPIO pins are specified as numbers
- Verify the file is saved as plain text

## Integration with Main System

The Pin Configuration Form integrates seamlessly with the main Wire Checker system:

1. **Database Integration**: Custom configurations work with the cycle tracking system
2. **Statistics**: Custom checkers contribute to statistics and reporting
3. **Audio Support**: Custom checkers can use the same audio feedback system
4. **LED Control**: All LED indicators work the same way

## Best Practices

1. **Naming Convention**: Use clear, descriptive product names and numbers
2. **Documentation**: Keep a record of your pin assignments
3. **Testing**: Always test your configuration before production use
4. **Backup**: Save your template files for future reference
5. **Pin Planning**: Plan your pin assignments to avoid conflicts

## File Locations

- **Configuration**: `pin_configuration.json`
- **Template**: `pin_config_template.txt`
- **Custom Checkers**: `wire_checker_custom_*.py`
- **Form Application**: `pin_config_form.py`

This system provides maximum flexibility while maintaining the reliability and features of the original Wire Checker system.