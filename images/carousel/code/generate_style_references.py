#!/usr/bin/env python3
"""
Generate style reference images for all carousel styles.

This script creates one reference image per style using Gemini,
saves them to the style_references folder, and updates generated_prompts.json.

Each reference shows 5 carousel slides arranged in a grid layout.

Usage:
    python generate_style_references.py              # Generate all missing references
    python generate_style_references.py --force      # Regenerate all references
    python generate_style_references.py --style "Minimalist"  # Generate specific style
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
REFS_DIR = DATA_DIR / "style_references"
PROMPTS_FILE = DATA_DIR / "generated_prompts.json"

# Base template for 5-slide grid carousel
GRID_TEMPLATE = """Create a carousel reference image showing 5 Instagram slides arranged in a 2x3 grid layout.

The layout should be:
- Slide 1 (large, left side): HOOK slide - tribe callout or attention grabber
- Slide 2 (top middle): PROBLEM slide - pain points with bullet list
- Slide 3 (top right): SOLUTION slide - benefits with bullet list  
- Slide 4 (bottom middle): QUOTE slide - testimonial with attribution
- Slide 5 (bottom right): CTA slide - call to action with button

STYLE: {style_name}
{style_description}

VISUAL REQUIREMENTS:
- Each slide should be clearly distinct
- Consistent visual style across all 5 slides
- Typography must be readable and clear
- {color_guidance}
- Professional, polished finish

SLIDE CONTENT EXAMPLE:
Slide 1: "FOR [TRIBE] ONLY" with tagline
Slide 2: "THE PROBLEM" with 3 bullet points
Slide 3: "THE SOLUTION" with 3 benefits
Slide 4: Quote with person's name and title
Slide 5: "JOIN NOW" with CTA button

Make it look like a real Instagram carousel preview - high quality, professional, and scroll-stopping."""

# Style definitions with optimized prompts for reference generation
STYLE_REFERENCE_PROMPTS = {
    "Modern Clean": {
        "style_description": """
- Contemporary sans-serif typography (Helvetica Neue, SF Pro style)
- Fresh, current color palette with single accent color
- Balanced white space, clean hierarchy
- No clutter, professional and timeless
- Crisp edges, modern aesthetic""",
        "color_guidance": "White/light gray backgrounds with blue or teal accent color",
        "filename": "ref_modern_clean.png"
    },
    
    "Minimalist": {
        "style_description": """
- Maximum white space - 70-80% empty space per slide
- Essential elements only, nothing superfluous
- Pure white or off-white backgrounds
- Thin, elegant typography in gray or black
- Single subtle accent color (sage green or dusty blue)
- Zen-like calm and breathing room""",
        "color_guidance": "Pure white backgrounds, thin gray text, minimal accent",
        "filename": "ref_minimalist.png"
    },
    
    "Simple Bold": {
        "style_description": """
- High contrast BLACK and WHITE only
- Massive oversized headlines that fill slides
- Strong visual hierarchy through scale
- Impactful, attention-grabbing typography
- No images, pure typographic design""",
        "color_guidance": "Strictly black and white, high contrast, no other colors",
        "filename": "ref_simple_bold.png"
    },
    
    "Elegant Premium": {
        "style_description": """
- Sophisticated serif fonts (Playfair Display, Didot style)
- Muted luxury colors: navy blue, cream, subtle gold accents
- Refined spacing and generous margins
- Premium, high-end magazine feel
- Subtle texture or fabric imagery""",
        "color_guidance": "Navy blue and cream palette with gold accents",
        "filename": "ref_elegant_premium.png"
    },
    
    "Aesthetic Soft": {
        "style_description": """
- Trendy Instagram-worthy aesthetic
- Soft gradients (pink to peach, sage to mint)
- Rounded corners on all elements
- Pleasing, harmonious pastel palette
- Dreamy, aspirational, feminine vibe
- Soft shadows and gentle curves""",
        "color_guidance": "Pastel gradients - soft pink, peach, sage, mint tones",
        "filename": "ref_aesthetic_soft.png"
    },
    
    "Professional Corporate": {
        "style_description": """
- Business-ready, trustworthy appearance
- Structured grid layout with clear sections
- Corporate blue color scheme (navy, royal blue, white)
- Clean data presentation style
- Sans-serif fonts (Arial, Roboto style)
- Professional and authoritative""",
        "color_guidance": "Corporate blue palette - navy, royal blue, white, gray",
        "filename": "ref_professional_corporate.png"
    },
    
    "Warm Friendly": {
        "style_description": """
- Approachable, welcoming feel
- Warm color palette: coral, peach, cream, soft orange
- Soft shadows, gentle curves
- Friendly, rounded typography
- Inviting and comforting atmosphere
- Human and personal touch""",
        "color_guidance": "Warm sunset colors - coral, peach, cream, soft orange",
        "filename": "ref_warm_friendly.png"
    },
    
    "Dark Dramatic": {
        "style_description": """
- Deep charcoal or navy backgrounds
- High contrast white or light text
- Moody, premium atmosphere
- Bold typography with dramatic weight
- Sophisticated and mysterious
- Cinema-like visual impact""",
        "color_guidance": "Dark charcoal/navy backgrounds with white bold text, optional blue accent",
        "filename": "ref_dark_dramatic.png"
    },
    
    "Playful Colorful": {
        "style_description": """
- Vibrant multi-color palette (primary colors)
- Fun geometric shapes and patterns
- Energetic, dynamic composition
- Bold color blocks and contrasts
- Youthful, fun, exciting energy
- Memphis design influence""",
        "color_guidance": "Bright primary colors - red, yellow, blue with fun shapes",
        "filename": "ref_playful_colorful.png"
    },
    
    "Soft Organic": {
        "style_description": """
- Natural earth tones: sage green, terracotta, sand, cream
- Gentle curves and flowing organic shapes
- Subtle natural textures
- Calming, grounding presence
- Sustainable, eco-friendly aesthetic
- Nature-inspired elements""",
        "color_guidance": "Earth tones - sage green, terracotta, sand, warm cream",
        "filename": "ref_soft_organic.png"
    },
    
    "Retro Vintage": {
        "style_description": """
- Nostalgic 70s color palette: faded orange, brown, mustard, cream
- Film grain texture overlay effect
- Retro typography with character
- Throwback vibes, analog feel
- Warm, nostalgic aesthetic
- Groovy, vintage design elements""",
        "color_guidance": "70s palette - faded orange, brown, mustard, cream with grain texture",
        "filename": "ref_retro_vintage.png"
    },
    
    "Tech Futuristic": {
        "style_description": """
- Dark mode base (near-black or dark blue)
- Neon accents: cyan, magenta, electric blue
- Glassmorphism or frosted glass effects
- Gradient mesh backgrounds
- Digital-native, cutting edge
- Sci-fi inspired aesthetic""",
        "color_guidance": "Dark mode with neon cyan/magenta accents, gradient meshes",
        "filename": "ref_tech_futuristic.png"
    },
    
    "Editorial Magazine": {
        "style_description": """
- High-fashion magazine layout
- Serif headlines (Didot, Bodoni style)
- Black, white, with one bold accent color
- Asymmetric sophisticated grid
- Editorial photography feel
- Vogue/Harper's Bazaar aesthetic""",
        "color_guidance": "Black and white with one bold accent (red or blue)",
        "filename": "ref_editorial_magazine.png"
    },
    
    "Bold Typography": {
        "style_description": """
- Text-dominant design - words ARE the design
- Massive headlines filling entire slides
- Minimal to no imagery
- Strong typographic hierarchy
- Color blocks as backgrounds
- Statement-making typography""",
        "color_guidance": "Bold color blocks with contrasting large text",
        "filename": "ref_bold_typography.png"
    },
    
    "Handcrafted Artisan": {
        "style_description": """
- Craft paper or cardboard texture backgrounds
- Hand-drawn elements and illustrations
- Hand-lettered typography feel
- Authentic, artisanal warmth
- Imperfect perfection aesthetic
- Small business, maker vibe""",
        "color_guidance": "Kraft paper browns, warm creams, hand-drawn black elements",
        "filename": "ref_handcrafted_artisan.png"
    },
    
    "Lo-fi Raw": {
        "style_description": """
- Unpolished UGC aesthetic
- Low production value feel (intentional)
- Screenshot-style frames
- Authentic imperfection
- Notes app or phone screenshot vibe
- Casual, real, unfiltered look""",
        "color_guidance": "Notes app yellow, screenshot gray, casual unpolished look",
        "filename": "ref_lofi_raw.png"
    }
}


def build_prompt(style_name: str, style_data: dict) -> str:
    """Build the full prompt for a style reference."""
    return GRID_TEMPLATE.format(
        style_name=style_name.upper(),
        style_description=style_data["style_description"],
        color_guidance=style_data["color_guidance"]
    )


def load_prompts():
    """Load prompts from JSON file."""
    with open(PROMPTS_FILE) as f:
        return json.load(f)


def save_prompts(data):
    """Save prompts to JSON file."""
    with open(PROMPTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def generate_style_reference(generator, style_name: str, style_data: dict, force: bool = False, max_retries: int = 2) -> dict:
    """Generate a single style reference image with retries."""
    output_path = REFS_DIR / style_data["filename"]
    
    # Check if already exists
    if output_path.exists() and not force:
        print(f"  ⏭️  {style_name}: Already exists, skipping")
        return {
            "status": "exists",
            "filename": style_data["filename"],
            "path": str(output_path)
        }
    
    print(f"  🎨 {style_name}...", end=" ", flush=True)
    
    prompt = build_prompt(style_name, style_data)
    
    for attempt in range(1, max_retries + 1):
        try:
            result = generator.generate_image(
                prompt=prompt,
                output_path=str(output_path.with_suffix('')),
            )
            
            if result.get("success"):
                print("✅")
                return {
                    "status": "success",
                    "filename": style_data["filename"],
                    "path": str(output_path),
                    "generated_at": datetime.now().isoformat()
                }
            
            error = result.get('error', 'Unknown')
            if '500' in str(error) and attempt < max_retries:
                print(f"⚠️ retry {attempt}...", end=" ", flush=True)
                time.sleep(5)
                continue
                
            print(f"❌ {str(error)[:50]}")
            return {
                "status": "failed",
                "error": str(error)
            }
            
        except Exception as e:
            if attempt < max_retries:
                print(f"⚠️ retry {attempt}...", end=" ", flush=True)
                time.sleep(5)
                continue
            print(f"❌ {str(e)[:50]}")
            return {
                "status": "exception",
                "error": str(e)
            }
    
    return {"status": "failed", "error": "Max retries exceeded"}


def update_prompts_with_references(data: dict) -> int:
    """Update all prompts with their style reference image paths."""
    updated = 0
    for prompt in data["prompts"]:
        style_name = prompt.get("style_name")
        if style_name in STYLE_REFERENCE_PROMPTS:
            ref_filename = STYLE_REFERENCE_PROMPTS[style_name]["filename"]
            ref_path = f"style_references/{ref_filename}"
            
            if prompt.get("style_reference") != ref_path:
                prompt["style_reference"] = ref_path
                updated += 1
    
    return updated


def main():
    parser = argparse.ArgumentParser(description="Generate style reference images")
    parser.add_argument("--force", action="store_true", help="Regenerate all references")
    parser.add_argument("--style", type=str, help="Generate specific style only")
    parser.add_argument("--list", action="store_true", help="List all styles")
    parser.add_argument("--update-json", action="store_true", help="Only update JSON, no generation")
    parser.add_argument("--delay", type=float, default=3.0, help="Delay between generations")
    args = parser.parse_args()
    
    # List mode
    if args.list:
        print("\n📋 Available styles:")
        for i, style in enumerate(STYLE_REFERENCE_PROMPTS.keys(), 1):
            ref_path = REFS_DIR / STYLE_REFERENCE_PROMPTS[style]["filename"]
            status = "✅" if ref_path.exists() else "⏳"
            print(f"  {i:2d}. {status} {style}")
        return
    
    # Create output directory
    REFS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load prompts data
    data = load_prompts()
    
    # Update JSON only mode
    if args.update_json:
        updated = update_prompts_with_references(data)
        save_prompts(data)
        print(f"✅ Updated {updated} prompts with style references")
        return
    
    # Determine which styles to generate
    if args.style:
        if args.style not in STYLE_REFERENCE_PROMPTS:
            print(f"❌ Unknown style: {args.style}")
            print(f"Available: {', '.join(STYLE_REFERENCE_PROMPTS.keys())}")
            sys.exit(1)
        styles_to_generate = {args.style: STYLE_REFERENCE_PROMPTS[args.style]}
    else:
        styles_to_generate = STYLE_REFERENCE_PROMPTS
    
    # Initialize generator
    try:
        generator = NanoBananaProGenerator()
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    print(f"\n🎨 Generating {len(styles_to_generate)} style references → {REFS_DIR}\n")
    print("Each reference shows 5 slides in a grid layout.\n")
    
    # Generate each style
    results = {"success": 0, "exists": 0, "failed": 0}
    for i, (style_name, style_data) in enumerate(styles_to_generate.items()):
        result = generate_style_reference(generator, style_name, style_data, args.force)
        results[result["status"]] = results.get(result["status"], 0) + 1
        
        if i < len(styles_to_generate) - 1 and result["status"] == "success":
            time.sleep(args.delay)
    
    # Update prompts JSON with references
    print("\n📝 Updating generated_prompts.json...")
    updated = update_prompts_with_references(data)
    save_prompts(data)
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"  ✅ Generated: {results.get('success', 0)}")
    print(f"  ⏭️  Existing: {results.get('exists', 0)}")
    print(f"  ❌ Failed: {results.get('failed', 0)}")
    print(f"  📝 Prompts updated: {updated}")


if __name__ == "__main__":
    main()
