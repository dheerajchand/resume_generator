#!/usr/bin/env python3
"""
Script to fix the demographic achievement with accurate geospatial machine learning description
"""

import json
import os
from pathlib import Path

def fix_demographic_text(text):
    """Fix demographic achievement descriptions with accurate geospatial ML details"""
    
    # Replace the current misclassified voters text with the corrected version
    old_patterns = [
        "Discovered 2.7M misclassified Democratic voters through data analysis",
        "Uncovered decades of demographic miscoding in voter files, discovering 2.7M previously mischaracterized Democratic voters"
    ]
    
    new_text = "Discovered systematic race coding errors affecting all Black and Asian-American voters, then developed geospatial machine learning algorithms that improved automated demographic classification accuracy from 23% to 64%"
    
    for pattern in old_patterns:
        text = text.replace(pattern, new_text)
    
    # Update summary text as well
    summary_old = "Discovered 2.7M misclassified voters"
    summary_new = "Discovered systematic demographic coding errors affecting all Black and Asian-American voters, developed geospatial ML algorithms improving classification accuracy from 23% to 64%"
    text = text.replace(summary_old, summary_new)
    
    return text

def process_resume_file(file_path):
    """Process a single resume JSON file"""
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert to string, fix text, convert back
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        fixed_str = fix_demographic_text(json_str)
        fixed_data = json.loads(fixed_str)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Fixed: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all resume files"""
    
    # Find all resume_data.json files
    input_dir = Path("inputs")
    resume_files = list(input_dir.glob("*/resume_data.json"))
    
    print(f"Found {len(resume_files)} resume files to process")
    print("=" * 50)
    
    successful = 0
    failed = 0
    
    for file_path in resume_files:
        if process_resume_file(file_path):
            successful += 1
        else:
            failed += 1
    
    print("=" * 50)
    print(f"✅ Successfully processed: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(resume_files)}")

if __name__ == "__main__":
    main()
