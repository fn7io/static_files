#!/usr/bin/env python3
"""
Generate carousel images from prompts.
Uses the NanoBananaProGenerator from generate_image.py
"""

import json
import sys
import argparse
from pathlib import Path

# Add parent directory to path to import generate_image
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from generate_image import NanoBananaProGenerator


# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "reference_carousels"


def load_prompts():
    """Load generated prompts."""
    prompts_file = DATA_DIR / "generated_prompts.json"
    if not prompts_file.exists():
        print("❌ No generated_prompts.json found. Run generate_prompts.py first.")
        sys.exit(1)
    
    with open(prompts_file) as f:
        return json.load(f)


def generate_single(generator, prompt_data, output_dir):
    """Generate a single carousel image."""
    prompt_id = prompt_data["id"]
    industry = prompt_data["industry_name"]
    pack = prompt_data["pack_name"]
    style = prompt_data["style_name"]
    prompt = prompt_data["prompt"]
    filename = prompt_data["filename"]
    
    output_path = output_dir / filename.replace('.png', '')
    
    print(f"\n{'='*60}")
    print(f"#{prompt_id}: {industry} / {pack} / {style}")
    print(f"{'='*60}")
    
    result = generator.generate_image(
        prompt=prompt,
        output_path=str(output_path),
        resolution="5400x1080",
    )
    
    if result.get("success"):
        print(f"✅ Saved: {filename}")
        return filename
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown')}")
        return None


def generate_batch(start=1, count=10, industry_filter=None, pack_filter=None, style_filter=None):
    """Generate a batch of carousel images with optional filters."""
    data = load_prompts()
    prompts = data["prompts"]
    
    # Apply filters
    filtered = prompts
    
    if industry_filter:
        filtered = [p for p in filtered if industry_filter.lower() in p["industry_id"].lower()]
    
    if pack_filter:
        filtered = [p for p in filtered if pack_filter.lower() in p["pack_id"].lower()]
    
    if style_filter:
        filtered = [p for p in filtered if style_filter.lower() in p["style_name"].lower()]
    
    # Apply range
    filtered = [p for p in filtered if p["id"] >= start][:count]
    
    if not filtered:
        print("❌ No prompts match your filters.")
        return []
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generator = NanoBananaProGenerator()
    
    print(f"\n🎨 Generating {len(filtered)} carousels")
    print(f"📁 Output: {OUTPUT_DIR}\n")
    
    results = []
    for prompt_data in filtered:
        filename = generate_single(generator, prompt_data, OUTPUT_DIR)
        if filename:
            results.append({
                "id": prompt_data["id"],
                "industry": prompt_data["industry_name"],
                "pack": prompt_data["pack_name"],
                "style": prompt_data["style_name"],
                "filename": filename
            })
    
    print(f"\n{'='*60}")
    print(f"✅ Generated {len(results)}/{len(filtered)} carousels")
    print(f"{'='*60}\n")
    
    return results


def list_prompts(industry_filter=None, pack_filter=None, style_filter=None):
    """List available prompts."""
    data = load_prompts()
    prompts = data["prompts"]
    
    # Apply filters
    filtered = prompts
    
    if industry_filter:
        filtered = [p for p in filtered if industry_filter.lower() in p["industry_id"].lower()]
    
    if pack_filter:
        filtered = [p for p in filtered if pack_filter.lower() in p["pack_id"].lower()]
    
    if style_filter:
        filtered = [p for p in filtered if style_filter.lower() in p["style_name"].lower()]
    
    print(f"\n📋 Available prompts: {len(filtered)}\n")
    
    current_industry = None
    for p in filtered:
        if p["industry_name"] != current_industry:
            current_industry = p["industry_name"]
            print(f"\n  {current_industry} ({p['sector']})")
            print(f"  {'-'*40}")
        
        print(f"    #{p['id']:3d} | {p['pack_name']:<25} | {p['style_name']}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate carousel images from prompts"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List available prompts"
    )
    parser.add_argument(
        "--start", type=int, default=1,
        help="Start from prompt ID (default: 1)"
    )
    parser.add_argument(
        "--count", type=int, default=10,
        help="Number of carousels to generate (default: 10)"
    )
    parser.add_argument(
        "--industry", type=str,
        help="Filter by industry (partial match)"
    )
    parser.add_argument(
        "--pack", type=str,
        help="Filter by pack (partial match)"
    )
    parser.add_argument(
        "--style", type=str,
        help="Filter by style (partial match)"
    )
    parser.add_argument(
        "--single", type=int,
        help="Generate a single prompt by ID"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_prompts(args.industry, args.pack, args.style)
        return
    
    if args.single:
        data = load_prompts()
        prompt = next((p for p in data["prompts"] if p["id"] == args.single), None)
        if not prompt:
            print(f"❌ Prompt #{args.single} not found.")
            return
        
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        generator = NanoBananaProGenerator()
        generate_single(generator, prompt, OUTPUT_DIR)
        return
    
    generate_batch(
        start=args.start,
        count=args.count,
        industry_filter=args.industry,
        pack_filter=args.pack,
        style_filter=args.style
    )


if __name__ == "__main__":
    main()

