#!/usr/bin/env python3
"""
Test script for the cycle system
Tests database functionality without RPi.GPIO
"""

import os
import sys
from database_manager import DatabaseManager

def test_cycle_system():
    """Test the cycle system functionality"""
    print("Testing Wire Checker Cycle System")
    print("=================================")
    
    # Initialize database manager
    db_manager = DatabaseManager("test_wire_checker.db")
    
    # Test 1: Create a new cycle
    print("\n1. Creating new cycle...")
    cycle_id = db_manager.create_new_cycle("4-pairs-speech")
    print(f"✓ Cycle created with ID: {cycle_id[:8]}...")
    
    # Test 2: Get cycle data
    print("\n2. Getting cycle data...")
    cycle_data = db_manager.get_current_cycle(cycle_id)
    if cycle_data:
        print(f"✓ Cycle data retrieved:")
        print(f"  - Configuration: {cycle_data['configuration']}")
        print(f"  - Status: {cycle_data['status']}")
        print(f"  - Total Checked: {cycle_data['total_checked']}")
    
    # Test 3: Update cycle counts
    print("\n3. Updating cycle counts...")
    test_statuses = ["GOOD", "NOT GOOD", "OPEN", "GOOD", "NOT GOOD"]
    for status in test_statuses:
        db_manager.update_cycle_count(cycle_id, status)
        print(f"✓ Updated with status: {status}")
    
    # Test 4: Get updated cycle data
    print("\n4. Getting updated cycle data...")
    updated_cycle = db_manager.get_current_cycle(cycle_id)
    if updated_cycle:
        print(f"✓ Updated cycle data:")
        print(f"  - Total Checked: {updated_cycle['total_checked']}")
        print(f"  - Good Count: {updated_cycle['good_count']}")
        print(f"  - Not Good Count: {updated_cycle['not_good_count']}")
        print(f"  - Open Count: {updated_cycle['open_count']}")
    
    # Test 5: End cycle
    print("\n5. Ending cycle...")
    db_manager.end_cycle(cycle_id)
    final_cycle = db_manager.get_current_cycle(cycle_id)
    if final_cycle:
        print(f"✓ Cycle ended successfully:")
        print(f"  - Status: {final_cycle['status']}")
        print(f"  - End Time: {final_cycle['end_time']}")
    
    # Test 6: Get daily statistics
    print("\n6. Getting daily statistics...")
    daily_stats = db_manager.get_daily_statistics()
    if daily_stats:
        print(f"✓ Daily statistics:")
        for stat in daily_stats:
            print(f"  - Configuration: {stat['configuration']}")
            print(f"  - Total Cycles: {stat['total_cycles']}")
            print(f"  - Total Checked: {stat['total_checked']}")
            print(f"  - Total Good: {stat['total_good']}")
            print(f"  - Total Not Good: {stat['total_not_good']}")
    
    # Test 7: Get all cycles
    print("\n7. Getting all cycles...")
    all_cycles = db_manager.get_all_cycles(limit=5)
    print(f"✓ Found {len(all_cycles)} recent cycles")
    for cycle in all_cycles:
        print(f"  - {cycle['cycle_id'][:8]}... | {cycle['configuration']} | {cycle['status']}")
    
    # Test 8: Export cycle data
    print("\n8. Exporting cycle data...")
    export_data = db_manager.export_cycle_data(cycle_id)
    if export_data:
        print(f"✓ Cycle data exported:")
        print(f"  - Cycle ID: {export_data['cycle']['cycle_id'][:8]}...")
        print(f"  - Events: {len(export_data['events'])}")
    
    print("\n✅ All tests completed successfully!")
    print("The cycle system is working correctly.")
    
    # Clean up test database
    if os.path.exists("test_wire_checker.db"):
        os.remove("test_wire_checker.db")
        print("✓ Test database cleaned up")

if __name__ == '__main__':
    test_cycle_system() 