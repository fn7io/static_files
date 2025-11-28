#!/usr/bin/env python3
"""
Generate carousel style reference images.

Format: 1000x200 pixels (5 slides at 200x200 each) horizontal strip.

Usage:
    python generate_all.py --batch 1      # Generate 1
    python generate_all.py --batch 20     # Generate 20
    python generate_all.py --resume       # Resume pending
    python generate_all.py --status       # Show progress
"""

import json
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from generate_image import NanoBananaProGenerator

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "reference_carousels"
PROMPTS_FILE = DATA_DIR / "generated_prompts.json"
URL_PREFIX = "https://fn7io.github.io/static_files/images/reference_carousels/"


def load_prompts():
    with open(PROMPTS_FILE) as f:
        return json.load(f)


def save_prompts(data):
    with open(PROMPTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def build_carousel_prompt(prompt_data):
    """Build a prompt for 5-slide carousel strip."""
    style = prompt_data["style_name"]
    pack = prompt_data["pack_name"]
    industry = prompt_data["industry_name"]
    hook = prompt_data["hook_pattern"]
    
    # Style-specific visual instructions
    style_visuals = {
        "Modern Clean": "white background, blue accent, clean sans-serif font",
        "Minimalist": "pure white, thin gray text, maximum whitespace",
        "Simple Bold": "black and white only, huge bold text",
        "Elegant Premium": "navy and cream, gold accents, serif font",
        "Aesthetic Soft": "pastel pink/sage gradient, rounded corners",
        "Professional Corporate": "blue and white, clean grid layout",
        "Warm Friendly": "coral and peach tones, rounded friendly font",
        "Dark Dramatic": "charcoal background, white text, moody",
        "Playful Colorful": "bright primary colors, fun shapes",
        "Soft Organic": "earth tones (sage, terracotta), natural feel",
        "Retro Vintage": "faded orange/brown, 70s typography",
        "Tech Futuristic": "dark mode, neon cyan accents",
        "Editorial Magazine": "black/white with red accent, serif headlines",
        "Bold Typography": "giant text filling slides, color blocks",
        "Handcrafted Artisan": "craft paper texture, hand-lettered",
        "Lo-fi Raw": "unpolished, casual handwriting, authentic"
    }
    
    visual = style_visuals.get(style, style)
    
    # Pack-specific slide content
    pack_content = {
        "For [Tribe] Only": "Slide1:'For You' Slide2:'Problem' Slide3:'Solution' Slide4:'Quote' Slide5:'Join'",
        "Founder Story / Anti-Ad": "Slide1:'Truth' Slide2:'Before' Slide3:'After' Slide4:'Proof' Slide5:'Start'",
        "Social Proof Carousel": "Slide1:'Claim' Slide2:'Stats' Slide3:'Review' Slide4:'Features' Slide5:'CTA'",
        "Myth Buster Carousel": "Slide1:'Myth' Slide2:'Why' Slide3:'Truth' Slide4:'Proof' Slide5:'Learn'",
        "Insider Secret Reveal": "Slide1:'Secret' Slide2:'Swipe' Slide3:'Tips' Slide4:'Works' Slide5:'Save'",
        "Problem → Solution Carousel": "Slide1:'Stop' Slide2:'Before/After' Slide3:'How' Slide4:'Results' Slide5:'Start'",
        "Price Math Carousel": "Slide1:'Price' Slide2:'Compare' Slide3:'Include' Slide4:'Worth it' Slide5:'Now'",
        "X vs Y Comparison": "Slide1:'X vs Y' Slide2:'Compare' Slide3:'Winner' Slide4:'Proof' Slide5:'Try'",
        "Educational Carousel": "Slide1:'Hook' Slide2:'Point 1' Slide3:'Point 2' Slide4:'Tip' Slide5:'Follow'",
        "FOMO Launch Carousel": "Slide1:'Limited' Slide2:'Product' Slide3:'Includes' Slide4:'Proof' Slide5:'Act'"
    }
    
    content = pack_content.get(pack, "Slide1:'Hook' Slide2:'Point' Slide3:'Point' Slide4:'Proof' Slide5:'CTA'")
    
    return f"""Create a horizontal banner showing 5 carousel slides in a row.

STYLE: {style.upper()} - {visual}

Show 5 slides side by side. Each slide has bold text:
{content}

Make it clean and cohesive in the {style} style for {industry}."""


def generate_single(generator, prompt_data, output_dir, max_retries=2):
    """Generate a single carousel strip."""
    prompt_id = prompt_data["id"]
    style = prompt_data["style_name"]
    pack = prompt_data["pack_name"][:20]
    industry = prompt_data["industry_name"][:15]
    filename = prompt_data["filename"]
    
    print(f"#{prompt_id:03d} | {style[:15]:15} | {pack:20} | {industry}...", end=" ", flush=True)
    
    output_path = output_dir / filename.replace('.png', '')
    prompt = build_carousel_prompt(prompt_data)
    
    for attempt in range(1, max_retries + 1):
        try:
            result = generator.generate_image(
                prompt=prompt,
                output_path=str(output_path),
            )
            
            # Post-process: crop to 1000x200 if successful
            if result.get("success") and result.get("saved_paths"):
                try:
                    from PIL import Image
                    img_path = result["saved_paths"][0]
                    img = Image.open(img_path)
                    w, h = img.size
                    # Crop center region to 5:1 aspect ratio, then resize to 1000x200
                    target_ratio = 5.0
                    current_ratio = w / h
                    if current_ratio < target_ratio:
                        # Too tall, crop height
                        new_h = int(w / target_ratio)
                        top = (h - new_h) // 2
                        img = img.crop((0, top, w, top + new_h))
                    else:
                        # Too wide, crop width
                        new_w = int(h * target_ratio)
                        left = (w - new_w) // 2
                        img = img.crop((left, 0, left + new_w, h))
                    # Resize to exact 1000x200
                    img = img.resize((1000, 200), Image.LANCZOS)
                    img.save(img_path)
                except Exception as crop_err:
                    print(f" (crop failed: {crop_err})", end="")
            
            if result.get("success"):
                print("✅")
                return {"status": "success", "filename": filename, "url": URL_PREFIX + filename, "generated_at": datetime.now().isoformat()}
            
            error = result.get('error', 'Unknown')
            if '500' in str(error) and attempt < max_retries:
                print(f"⚠️", end=" ", flush=True)
                time.sleep(5)
                continue
            
            print(f"❌ {str(error)[:40]}")
            return {"status": "failed", "filename": filename, "error": str(error)[:200], "attempted_at": datetime.now().isoformat()}
            
        except Exception as e:
            if attempt < max_retries:
                print(f"⚠️", end=" ", flush=True)
                time.sleep(5)
                continue
            print(f"❌ {str(e)[:40]}")
            return {"status": "exception", "filename": filename, "error": str(e)[:200], "attempted_at": datetime.now().isoformat()}
    
    return {"status": "failed", "filename": filename, "error": "Max retries", "attempted_at": datetime.now().isoformat()}


def get_pending(data):
    return [p for p in data["prompts"] if p.get("generation_status", {}).get("status") != "success"]


def print_status(data):
    total = len(data["prompts"])
    success = sum(1 for p in data["prompts"] if p.get("generation_status", {}).get("status") == "success")
    failed = sum(1 for p in data["prompts"] if p.get("generation_status", {}).get("status") in ["failed", "exception"])
    print(f"\n📊 {success}/{total} ({100*success/total:.1f}%) | ✅ {success} | ❌ {failed} | ⏳ {total-success-failed}")


def main():
    parser = argparse.ArgumentParser(description="Generate carousel references")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--batch", type=int, default=177)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retry-failed", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--delay", type=float, default=2.0)
    args = parser.parse_args()
    
    data = load_prompts()
    
    if args.status:
        print_status(data)
        return
    
    if args.resume:
        to_process = get_pending(data)[:args.batch]
    elif args.retry_failed:
        to_process = [p for p in data["prompts"] if p.get("generation_status", {}).get("status") in ["failed", "exception"]][:args.batch]
    else:
        to_process = [p for p in data["prompts"] if p["id"] >= args.start][:args.batch]
    
    if not to_process:
        print("✅ Nothing to process!")
        print_status(data)
        return
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generator = NanoBananaProGenerator()
    
    print(f"\n🎨 Generating {len(to_process)} carousels (1000x200px) → {OUTPUT_DIR}\n")
    
    for i, prompt_data in enumerate(to_process):
        if not args.retry_failed and prompt_data.get("generation_status", {}).get("status") == "success":
            continue
        
        result = generate_single(generator, prompt_data, OUTPUT_DIR)
        prompt_data["generation_status"] = result
        save_prompts(data)
        
        if i < len(to_process) - 1:
            time.sleep(args.delay)
    
    print_status(data)


if __name__ == "__main__":
    main()
