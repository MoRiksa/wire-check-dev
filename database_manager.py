#!/usr/bin/env python3
"""
Database Manager for Wire Checker Cycles
Uses SQLite for lightweight, reliable storage
"""

import sqlite3
import time
import uuid
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path="wire_checker.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create cycles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cycles (
                cycle_id TEXT PRIMARY KEY,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                configuration TEXT,
                total_checked INTEGER DEFAULT 0,
                good_count INTEGER DEFAULT 0,
                not_good_count INTEGER DEFAULT 0,
                open_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Create cycle_events table for detailed logging
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cycle_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cycle_id TEXT,
                timestamp TIMESTAMP,
                status TEXT,
                details TEXT,
                FOREIGN KEY (cycle_id) REFERENCES cycles (cycle_id)
            )
        ''')
        
        # Create statistics table for aggregated data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                configuration TEXT,
                total_cycles INTEGER DEFAULT 0,
                total_checked INTEGER DEFAULT 0,
                total_good INTEGER DEFAULT 0,
                total_not_good INTEGER DEFAULT 0,
                total_open INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_new_cycle(self, configuration):
        """Create a new cycle and return its ID"""
        cycle_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO cycles (cycle_id, start_time, configuration, status)
            VALUES (?, ?, ?, 'active')
        ''', (cycle_id, start_time, configuration))
        
        conn.commit()
        conn.close()
        
        return cycle_id
    
    def get_current_cycle(self, cycle_id):
        """Get current cycle data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM cycles WHERE cycle_id = ?
        ''', (cycle_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'cycle_id': result[0],
                'start_time': result[1],
                'end_time': result[2],
                'configuration': result[3],
                'total_checked': result[4],
                'good_count': result[5],
                'not_good_count': result[6],
                'open_count': result[7],
                'status': result[8]
            }
        return None
    
    def update_cycle_count(self, cycle_id, status):
        """Update cycle counts based on status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current counts
        cursor.execute('''
            SELECT total_checked, good_count, not_good_count, open_count 
            FROM cycles WHERE cycle_id = ?
        ''', (cycle_id,))
        
        result = cursor.fetchone()
        if result:
            total_checked, good_count, not_good_count, open_count = result
            
            # Update counts based on status
            total_checked += 1
            if status == "GOOD":
                good_count += 1
            elif status == "NOT GOOD":
                not_good_count += 1
            elif status == "OPEN":
                open_count += 1
            
            # Update database
            cursor.execute('''
                UPDATE cycles 
                SET total_checked = ?, good_count = ?, not_good_count = ?, open_count = ?
                WHERE cycle_id = ?
            ''', (total_checked, good_count, not_good_count, open_count, cycle_id))
            
            # Log the event
            cursor.execute('''
                INSERT INTO cycle_events (cycle_id, timestamp, status, details)
                VALUES (?, ?, ?, ?)
            ''', (cycle_id, datetime.now(), status, f"Status changed to {status}"))
            
            conn.commit()
        
        conn.close()
    
    def end_cycle(self, cycle_id):
        """End a cycle and mark it as completed"""
        end_time = datetime.now()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE cycles 
            SET end_time = ?, status = 'completed'
            WHERE cycle_id = ?
        ''', (end_time, cycle_id))
        
        conn.commit()
        conn.close()
        
        # Update daily statistics in separate connection
        self.update_daily_statistics(cycle_id)
    
    def update_daily_statistics(self, cycle_id):
        """Update daily statistics when cycle ends"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get cycle data
        cursor.execute('''
            SELECT configuration, total_checked, good_count, not_good_count, open_count
            FROM cycles WHERE cycle_id = ?
        ''', (cycle_id,))
        
        result = cursor.fetchone()
        if result:
            configuration, total_checked, good_count, not_good_count, open_count = result
            today = datetime.now().date()
            
            # Check if statistics for today exist
            cursor.execute('''
                SELECT id FROM statistics WHERE date = ? AND configuration = ?
            ''', (today, configuration))
            
            if cursor.fetchone():
                # Update existing statistics
                cursor.execute('''
                    UPDATE statistics 
                    SET total_cycles = total_cycles + 1,
                        total_checked = total_checked + ?,
                        total_good = total_good + ?,
                        total_not_good = total_not_good + ?,
                        total_open = total_open + ?
                    WHERE date = ? AND configuration = ?
                ''', (total_checked, good_count, not_good_count, open_count, today, configuration))
            else:
                # Create new statistics
                cursor.execute('''
                    INSERT INTO statistics (date, configuration, total_cycles, total_checked, 
                                         total_good, total_not_good, total_open)
                    VALUES (?, ?, 1, ?, ?, ?, ?)
                ''', (today, configuration, total_checked, good_count, not_good_count, open_count))
        
        conn.commit()
        conn.close()
    
    def get_daily_statistics(self, date=None):
        """Get statistics for a specific date (default: today)"""
        if date is None:
            date = datetime.now().date()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT configuration, total_cycles, total_checked, total_good, 
                   total_not_good, total_open
            FROM statistics WHERE date = ?
        ''', (date,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'configuration': row[0],
                'total_cycles': row[1],
                'total_checked': row[2],
                'total_good': row[3],
                'total_not_good': row[4],
                'total_open': row[5]
            }
            for row in results
        ]
    
    def get_all_cycles(self, limit=50):
        """Get recent cycles"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cycle_id, start_time, end_time, configuration, 
                   total_checked, good_count, not_good_count, open_count, status
            FROM cycles 
            ORDER BY start_time DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'cycle_id': row[0],
                'start_time': row[1],
                'end_time': row[2],
                'configuration': row[3],
                'total_checked': row[4],
                'good_count': row[5],
                'not_good_count': row[6],
                'open_count': row[7],
                'status': row[8]
            }
            for row in results
        ]
    
    def export_cycle_data(self, cycle_id):
        """Export cycle data for server transmission"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get cycle data
        cursor.execute('''
            SELECT * FROM cycles WHERE cycle_id = ?
        ''', (cycle_id,))
        
        cycle_data = cursor.fetchone()
        
        # Get cycle events
        cursor.execute('''
            SELECT * FROM cycle_events WHERE cycle_id = ?
            ORDER BY timestamp
        ''', (cycle_id,))
        
        events_data = cursor.fetchall()
        
        conn.close()
        
        if cycle_data:
            return {
                'cycle': {
                    'cycle_id': cycle_data[0],
                    'start_time': cycle_data[1],
                    'end_time': cycle_data[2],
                    'configuration': cycle_data[3],
                    'total_checked': cycle_data[4],
                    'good_count': cycle_data[5],
                    'not_good_count': cycle_data[6],
                    'open_count': cycle_data[7],
                    'status': cycle_data[8]
                },
                'events': [
                    {
                        'id': event[0],
                        'cycle_id': event[1],
                        'timestamp': event[2],
                        'status': event[3],
                        'details': event[4]
                    }
                    for event in events_data
                ]
            }
        return None 