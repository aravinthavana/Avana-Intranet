"""
Utility functions for data management, backups, and file operations
"""
import os
import json
import shutil
from datetime import datetime, timedelta
from typing import Any, List
import threading

# File locking
_file_locks = {}
_locks_lock = threading.Lock()

def get_file_lock(filepath: str) -> threading.Lock:
    """Get or create a lock for a specific file"""
    with _locks_lock:
        if filepath not in _file_locks:
            _file_locks[filepath] = threading.Lock()
        return _file_locks[filepath]

def create_backup(filepath: str, backup_dir: str = None) -> str:
    """
    Create a timestamped backup of a file
    Returns the backup file path
    """
    if not os.path.exists(filepath):
        return None
    
    # Determine backup directory
    if backup_dir is None:
        file_dir = os.path.dirname(filepath)
        backup_dir = os.path.join(file_dir, 'backups')
    
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate backup filename with timestamp
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"{name}_backup_{timestamp}{ext}"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Copy file to backup
    shutil.copy2(filepath, backup_path)
    
    return backup_path

def cleanup_old_backups(backup_dir: str, retention_days: int = 30):
    """Remove backup files older than retention_days"""
    if not os.path.exists(backup_dir):
        return
    
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    
    for filename in os.listdir(backup_dir):
        filepath = os.path.join(backup_dir, filename)
        
        # Check if file is old enough to delete
        if os.path.isfile(filepath):
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_time < cutoff_date:
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Error removing old backup {filepath}: {e}")

def read_json_safe(filepath: str) -> List[Any]:
    """
    Safely read JSON file with file locking
    Returns empty list if file doesn't exist
    """
    lock = get_file_lock(filepath)
    
    with lock:
        if not os.path.exists(filepath):
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filepath}")
            return []
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return []

def write_json_safe(filepath: str, data: Any, create_backup: bool = True) -> bool:
    """
    Safely write JSON file with file locking and optional backup
    Returns True if successful, False otherwise
    """
    lock = get_file_lock(filepath)
    
    with lock:
        try:
            # Create backup if file exists and backup is enabled
            if create_backup and os.path.exists(filepath):
                backup_enabled = os.getenv('BACKUP_ENABLED', 'True').lower() == 'true'
                if backup_enabled:
                    file_dir = os.path.dirname(filepath)
                    backup_dir = os.path.join(file_dir, 'backups')
                    create_backup(filepath, backup_dir)
                    
                    # Cleanup old backups
                    retention_days = int(os.getenv('BACKUP_RETENTION_DAYS', 30))
                    cleanup_old_backups(backup_dir, retention_days)
            
            # Write data to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error writing to {filepath}: {e}")
            return False
