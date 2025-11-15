import json
import os
from typing import Dict, List, Any

class FileManager:
    # type of mathode
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_to_file(self, filename: str, data: Any) -> bool:
        """Save data to JSON file"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return False
    
    def load_from_file(self, filename: str) -> Any:
        """Load data from JSON file"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as file:
                    return json.load(file)
            return []
        except Exception as e:
            print(f"Error loading from {filename}: {e}")
            return []
    
    def append_to_file(self, filename: str, new_data: Any) -> bool:
        """Append data to JSON file"""
        try:
            existing_data = self.load_from_file(filename)
            if isinstance(existing_data, list):
                existing_data.append(new_data)
            elif isinstance(existing_data, dict):
                existing_data.update(new_data)
            return self.save_to_file(filename, existing_data)
        except Exception as e:
            print(f"Error appending to {filename}: {e}")
            return False