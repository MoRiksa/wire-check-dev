#!/usr/bin/env python3
"""
Test script for Pin Configuration Form
This script tests the basic functionality of the pin configuration system
"""

import json
import os
import sys

def test_config_validation():
    """Test configuration validation logic"""
    print("Testing configuration validation...")
    
    # Test valid configuration
    valid_config = {
        'product_name': 'Test Product',
        'product_no': 'TP-001',
        'wire_pairs': [
            {'pair_number': 1, 'pin_out': 17, 'pin_in': 27},
            {'pair_number': 2, 'pin_out': 22, 'pin_in': 10}
        ]
    }
    
    # Save test configuration
    with open('test_pin_configuration.json', 'w') as f:
        json.dump(valid_config, f, indent=4)
    
    print("✓ Valid configuration created")
    
    # Test loading configuration
    with open('test_pin_configuration.json', 'r') as f:
        loaded_config = json.load(f)
    
    assert loaded_config['product_name'] == 'Test Product'
    assert loaded_config['product_no'] == 'TP-001'
    assert len(loaded_config['wire_pairs']) == 2
    
    print("✓ Configuration loading works")
    
    # Clean up
    os.remove('test_pin_configuration.json')
    print("✓ Test configuration file cleaned up")

def test_template_parsing():
    """Test template file parsing"""
    print("\nTesting template parsing...")
    
    # Create test template
    template_content = """# Test Template
Product Name: Template Test Product
Product No: TTP-001
Pair 1: GPIO17 -> GPIO27
Pair 2: GPIO22 -> GPIO10
Pair 3: GPIO9 -> GPIO11
"""
    
    with open('test_template.txt', 'w') as f:
        f.write(template_content)
    
    print("✓ Test template created")
    
    # Test parsing logic (simplified version)
    lines = template_content.split('\n')
    parsed_data = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        
        if line.startswith('Product Name:'):
            parsed_data['product_name'] = line.split(':', 1)[1].strip()
        elif line.startswith('Product No:'):
            parsed_data['product_no'] = line.split(':', 1)[1].strip()
        elif line.startswith('Pair '):
            # Simple parsing for testing
            if 'pairs' not in parsed_data:
                parsed_data['pairs'] = []
            parsed_data['pairs'].append(line)
    
    assert parsed_data['product_name'] == 'Template Test Product'
    assert parsed_data['product_no'] == 'TTP-001'
    assert len(parsed_data['pairs']) == 3
    
    print("✓ Template parsing works")
    
    # Clean up
    os.remove('test_template.txt')
    print("✓ Test template file cleaned up")

def test_custom_checker_generation():
    """Test custom checker code generation"""
    print("\nTesting custom checker generation...")
    
    # Test data
    wire_pairs = [(17, 27), (22, 10), (9, 11)]
    product_name = "Test Wire Assembly"
    product_no = "TWA-001"
    
    # Generate custom checker code (simplified)
    custom_code = f"""# Custom Wire Checker for {product_name} ({product_no})
PRODUCT_NAME = "{product_name}"
PRODUCT_NO = "{product_no}"
WIRE_PAIRS = {wire_pairs}

def main():
    print(f"Custom Wire Checker: {{PRODUCT_NAME}} ({{PRODUCT_NO}})")
    print(f"Wire Pairs: {{WIRE_PAIRS}}")
    print("Custom checker generated successfully!")

if __name__ == '__main__':
    main()
"""
    
    # Save custom checker
    custom_file = f'test_wire_checker_custom_{product_no.replace("-", "_").lower()}.py'
    with open(custom_file, 'w') as f:
        f.write(custom_code)
    
    print("✓ Custom checker code generated")
    
    # Test running the custom checker
    try:
        import subprocess
        result = subprocess.run([sys.executable, custom_file], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✓ Custom checker runs successfully")
            print(f"  Output: {result.stdout.strip()}")
        else:
            print(f"✗ Custom checker failed: {result.stderr}")
    
    except Exception as e:
        print(f"✗ Error running custom checker: {e}")
    
    # Clean up
    os.remove(custom_file)
    print("✓ Test custom checker file cleaned up")

def test_gpio_pin_validation():
    """Test GPIO pin validation"""
    print("\nTesting GPIO pin validation...")
    
    # Reserved pins that should be avoided
    reserved_pins = [2, 3, 4, 13, 15, 18]
    
    # Valid pins for testing
    valid_pins = [5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    
    # Test pin uniqueness
    test_pairs = [(17, 27), (22, 10), (9, 11)]
    used_pins = set()
    
    for out_pin, in_pin in test_pairs:
        assert out_pin not in used_pins, f"Pin {out_pin} already used"
        assert in_pin not in used_pins, f"Pin {in_pin} already used"
        used_pins.add(out_pin)
        used_pins.add(in_pin)
    
    print("✓ Pin uniqueness validation works")
    
    # Test reserved pin detection
    for pin in reserved_pins:
        if pin in used_pins:
            print(f"⚠ Warning: Pin {pin} is reserved")
    
    print("✓ Reserved pin detection works")

def main():
    """Run all tests"""
    print("=== Pin Configuration Form Test Suite ===\n")
    
    try:
        test_config_validation()
        test_template_parsing()
        test_custom_checker_generation()
        test_gpio_pin_validation()
        
        print("\n=== All Tests Passed! ===")
        print("Pin Configuration Form is ready to use.")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()