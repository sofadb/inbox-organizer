#!/usr/bin/env python3

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

def organize_files():
    inbox_dir = Path("/data/inbox")
    journal_dir = Path("/data/journal")
    
    # Pattern to match YYYYMMDDHHMMSS.md files
    pattern = re.compile(r'^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})\.md$')
    
    if not inbox_dir.exists():
        print(f"Inbox directory {inbox_dir} does not exist")
        return
    
    # Create journal directory if it doesn't exist
    journal_dir.mkdir(parents=True, exist_ok=True)
    
    files_moved = 0
    
    for file_path in inbox_dir.glob("*.md"):
        filename = file_path.name
        match = pattern.match(filename)
        
        if match:
            year, month, day, hour, minute, second = match.groups()
            
            # Create target directory structure: /journal/YYYY/MM/DD/
            target_dir = journal_dir / year / month / day
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Target file path
            target_file = target_dir / filename
            
            try:
                # Move the file
                shutil.move(str(file_path), str(target_file))
                print(f"Moved {filename} to {target_file}")
                files_moved += 1
            except Exception as e:
                print(f"Error moving {filename}: {e}")
        else:
            print(f"Skipping {filename} - doesn't match pattern YYYYMMDDHHMMSS.md")
    
    print(f"Successfully moved {files_moved} files")

if __name__ == "__main__":
    organize_files()