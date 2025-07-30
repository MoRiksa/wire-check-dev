#!/usr/bin/env python3
"""
Server Export Module for Wire Checker
Handles sending cycle data to external server
"""

import json
import requests
from database_manager import DatabaseManager
from datetime import datetime
import os

class ServerExporter:
    def __init__(self, server_url=None, api_key=None):
        self.server_url = server_url or os.environ.get('WIRE_CHECKER_SERVER_URL')
        self.api_key = api_key or os.environ.get('WIRE_CHECKER_API_KEY')
        self.db_manager = DatabaseManager()
    
    def export_cycle_to_server(self, cycle_id):
        """Export a specific cycle to the server"""
        if not self.server_url:
            print("Warning: No server URL configured")
            return False
        
        try:
            # Get cycle data
            cycle_data = self.db_manager.export_cycle_data(cycle_id)
            if not cycle_data:
                print(f"Error: No data found for cycle {cycle_id}")
                return False
            
            # Prepare headers
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Wire-Checker-Client/1.0'
            }
            
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            # Send data to server
            response = requests.post(
                f"{self.server_url}/api/cycles",
                json=cycle_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✓ Cycle {cycle_id[:8]}... exported successfully")
                return True
            else:
                print(f"✗ Server error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Network error: {e}")
            return False
        except Exception as e:
            print(f"✗ Export error: {e}")
            return False
    
    def export_all_completed_cycles(self):
        """Export all completed cycles to server"""
        if not self.server_url:
            print("Warning: No server URL configured")
            return False
        
        try:
            # Get all completed cycles
            all_cycles = self.db_manager.get_all_cycles(limit=1000)
            completed_cycles = [c for c in all_cycles if c['status'] == 'completed']
            
            if not completed_cycles:
                print("No completed cycles to export")
                return True
            
            print(f"Exporting {len(completed_cycles)} completed cycles...")
            
            success_count = 0
            for cycle in completed_cycles:
                if self.export_cycle_to_server(cycle['cycle_id']):
                    success_count += 1
            
            print(f"✓ Exported {success_count}/{len(completed_cycles)} cycles successfully")
            return success_count == len(completed_cycles)
            
        except Exception as e:
            print(f"✗ Export error: {e}")
            return False
    
    def export_daily_statistics(self, date=None):
        """Export daily statistics to server"""
        if not self.server_url:
            print("Warning: No server URL configured")
            return False
        
        try:
            # Get daily statistics
            daily_stats = self.db_manager.get_daily_statistics(date)
            
            if not daily_stats:
                print("No daily statistics to export")
                return True
            
            # Prepare data
            export_data = {
                'date': date.isoformat() if date else datetime.now().date().isoformat(),
                'statistics': daily_stats,
                'exported_at': datetime.now().isoformat()
            }
            
            # Prepare headers
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Wire-Checker-Client/1.0'
            }
            
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            # Send data to server
            response = requests.post(
                f"{self.server_url}/api/statistics",
                json=export_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✓ Daily statistics exported successfully")
                return True
            else:
                print(f"✗ Server error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Network error: {e}")
            return False
        except Exception as e:
            print(f"✗ Export error: {e}")
            return False
    
    def test_server_connection(self):
        """Test server connectivity"""
        if not self.server_url:
            print("Warning: No server URL configured")
            return False
        
        try:
            response = requests.get(
                f"{self.server_url}/api/health",
                timeout=10
            )
            
            if response.status_code == 200:
                print("✓ Server connection successful")
                return True
            else:
                print(f"✗ Server error: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
            return False

def main():
    """Test the server export functionality"""
    print("Wire Checker Server Export Test")
    print("===============================")
    
    # Initialize exporter
    exporter = ServerExporter()
    
    # Test server connection
    print("\n1. Testing server connection...")
    if exporter.test_server_connection():
        print("✓ Server is reachable")
    else:
        print("✗ Server is not reachable")
    
    # Test cycle export (if server is available)
    if exporter.server_url:
        print("\n2. Testing cycle export...")
        # Get a completed cycle
        all_cycles = exporter.db_manager.get_all_cycles(limit=1)
        if all_cycles:
            cycle_id = all_cycles[0]['cycle_id']
            exporter.export_cycle_to_server(cycle_id)
        else:
            print("No cycles available for export")
    
    print("\n✅ Server export test completed")

if __name__ == '__main__':
    main() 