#!/usr/bin/env python3
"""
Process all style images to extend their backgrounds.
Runs one generation every 30 seconds to avoid API rate limits.
"""

import csv
import time
import subprocess
import sys
from pathlib import Path

# Styles already processed
processed_styles = {"Byzantine Icon"}

def get_all_styles():
    """Read all styles from the CSV file."""
    styles = []
    csv_path = Path("combined_tables.csv")
    
    if not csv_path.exists():
        print("❌ Error: combined_tables.csv not found")
        return []
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            style_name = row['Style Name'].strip()
            if style_name:  # Skip empty rows
                styles.append(style_name)
    
    return styles

def process_style(style_name):
    """Process a single style image."""
    print(f"\n{'='*70}")
    print(f"🎨 Processing: {style_name}")
    print(f"{'='*70}")
    
    output_path = f"reference_styles_extended/style_{style_name.replace(' ', '_')}.png"
    
    try:
        result = subprocess.run(
            ["python3", "generate_from_style.py", style_name, "--output", output_path],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout per image
        )
        
        if result.returncode == 0:
            print(f"✅ Successfully processed: {style_name}")
            return True
        else:
            print(f"❌ Error processing {style_name}:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  Timeout processing {style_name}")
        return False
    except Exception as e:
        print(f"❌ Exception processing {style_name}: {str(e)}")
        return False

def main():
    """Main function to process all styles."""
    all_styles = get_all_styles()
    
    if not all_styles:
        print("❌ No styles found to process")
        sys.exit(1)
    
    # Filter out already processed styles
    remaining_styles = [s for s in all_styles if s not in processed_styles]
    
    print(f"\n📊 Total styles: {len(all_styles)}")
    print(f"✅ Already processed: {len(processed_styles)} ({', '.join(processed_styles)})")
    print(f"🔄 Remaining to process: {len(remaining_styles)}")
    
    if not remaining_styles:
        print("\n✨ All styles have been processed!")
        return
    
    print(f"\n🚀 Starting batch processing...")
    print(f"⏱️  Delay between images: 30 seconds\n")
    
    successful = 0
    failed = 0
    
    for i, style_name in enumerate(remaining_styles, 1):
        print(f"\n[{i}/{len(remaining_styles)}] Processing {style_name}...")
        
        success = process_style(style_name)
        
        if success:
            successful += 1
        else:
            failed += 1
        
        # Wait 30 seconds before next image (except for the last one)
        if i < len(remaining_styles):
            print(f"\n⏳ Waiting 30 seconds before next image...")
            time.sleep(30)
    
    # Summary
    print(f"\n{'='*70}")
    print(f"📊 Processing Summary:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📁 Total processed: {successful + len(processed_styles)}/{len(all_styles)}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()


