#!/usr/bin/env python3
"""
Generate all carousel prompts by combining:
- Industries (from industry_mapping.json)
- Element Packs (from elements.json)
- Styles (from styles.csv / industry_mapping recommended_styles)

Output: Generated prompts in data/generated_prompts.json
"""

import json
from pathlib import Path
from itertools import product


# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "reference_carousels"


def load_data():
    """Load all configuration data."""
    with open(DATA_DIR / "industry_mapping.json") as f:
        industry_mapping = json.load(f)
    
    with open(DATA_DIR / "elements.json") as f:
        elements = json.load(f)
    
    return industry_mapping, elements


def get_style_visual(style_name: str) -> dict:
    """Get visual description for a style."""
    STYLE_VISUALS = {
        "Modern Clean": {
            "visual": "Contemporary sans-serif typography, fresh color palette with one accent, balanced white space",
            "colors": "Fresh current palette, single accent color",
            "typography": "Clean sans-serif (Helvetica Neue style)"
        },
        "Minimalist": {
            "visual": "Maximum white space, essential elements only, neutral palette",
            "colors": "White/light gray background, single muted accent",
            "typography": "Thin elegant sans-serif"
        },
        "Simple Bold": {
            "visual": "High contrast black/white, oversized headlines, strong hierarchy",
            "colors": "Pure black and white only",
            "typography": "Massive bold condensed"
        },
        "Elegant Premium": {
            "visual": "Sophisticated serif fonts, muted luxury colors, refined spacing",
            "colors": "Navy, cream, subtle gold accents",
            "typography": "Playfair or Didot style serif"
        },
        "Aesthetic Soft": {
            "visual": "Soft gradients, rounded corners, pleasing color harmony",
            "colors": "Blush pink, sage green, soft lavender pastels",
            "typography": "Modern rounded sans-serif"
        },
        "Professional Corporate": {
            "visual": "Clean business aesthetic, structured grid, trustworthy feel",
            "colors": "Blue color scheme with white",
            "typography": "Professional sans-serif"
        },
        "Warm Friendly": {
            "visual": "Approachable feel, warm palette, soft shadows, inviting",
            "colors": "Coral, peach, cream, soft orange",
            "typography": "Rounded friendly sans-serif"
        },
        "Dark Dramatic": {
            "visual": "Deep backgrounds, high contrast text, moody premium feel",
            "colors": "Charcoal or navy backgrounds, white text",
            "typography": "Bold contrast typography"
        },
        "Playful Colorful": {
            "visual": "Vibrant multi-color palette, fun shapes, energetic",
            "colors": "Vibrant harmonious primaries",
            "typography": "Bold playful sans-serif"
        },
        "Soft Organic": {
            "visual": "Natural earth tones, gentle curves, subtle textures, calming",
            "colors": "Sage, terracotta, sand, cream",
            "typography": "Soft rounded serif or sans"
        },
        "Retro Vintage": {
            "visual": "Nostalgic colors, film grain texture, throwback vibes",
            "colors": "Faded orange, brown, cream, mustard",
            "typography": "Retro-inspired with character"
        },
        "Tech Futuristic": {
            "visual": "Dark mode, neon accents, glassmorphism, digital-native",
            "colors": "Near black with neon cyan/purple/green",
            "typography": "Modern tech sans-serif"
        },
        "Editorial Magazine": {
            "visual": "High-fashion layout, asymmetric grid, sophisticated",
            "colors": "Black, white, one accent color",
            "typography": "Elegant serif headlines"
        },
        "Bold Typography": {
            "visual": "Text-dominant design, massive headlines, minimal imagery",
            "colors": "High contrast color blocks",
            "typography": "Massive bold typography as art"
        },
        "Handcrafted Artisan": {
            "visual": "Texture overlays, hand-drawn elements, craft feel",
            "colors": "Warm craft paper tones",
            "typography": "Hand-lettered style"
        },
        "Lo-fi Raw": {
            "visual": "Unpolished authentic, raw textures, UGC feel",
            "colors": "Muted desaturated, imperfect",
            "typography": "Casual handwritten or simple system"
        }
    }
    return STYLE_VISUALS.get(style_name, {"visual": style_name, "colors": "", "typography": ""})


def build_prompt(industry: dict, pack: dict, style_name: str, content_examples: dict) -> str:
    """Build a complete image generation prompt."""
    style_info = get_style_visual(style_name)
    
    # Build slide content based on pack
    slides_description = []
    for slide in pack["slide_sequence"]:
        slide_num = slide["slide"]
        element = slide["element"]
        purpose = slide["purpose"]
        slides_description.append(f"Slide {slide_num}: [{element.upper()}] {purpose}")
    
    slides_text = ", ".join(slides_description)
    
    # Get industry-specific content
    tribe_example = content_examples.get("tribe_callout_examples", ["Target Audience"])[0]
    pain_example = content_examples.get("pain_points", ["Common problem"])[0]
    stat_example = content_examples.get("stat_examples", ["90%+ results"])[0]
    cta_example = content_examples.get("cta_examples", ["Get Started"])[0]
    
    prompt = f"""Create a single horizontal image (5400x1080 pixels) showing 5 Instagram carousel slides side by side.

INDUSTRY: {industry["name"]} ({industry["sector"]})
TONE: {industry["content_profile"]["tone"]}
PACK: {pack["pack_name"]}

STYLE: {style_name.upper()}
- Visual: {style_info["visual"]}
- Colors: {style_info["colors"]}
- Typography: {style_info["typography"]}

SLIDE STRUCTURE:
{slides_text}

CONTENT GUIDANCE:
- Target audience example: "{tribe_example}"
- Pain point example: "{pain_example}"
- Stat example: "{stat_example}"
- CTA example: "{cta_example}"

DESIGN PRINCIPLES:
1. MESSAGE FIRST - Text must be instantly readable
2. Clean layouts with generous breathing room
3. Limited color palette (2-3 colors max)
4. Consistent visual language across all 5 slides
5. Typography-driven, not decoration-driven
6. NO busy backgrounds or overwhelming patterns

Each slide is 1080x1080 pixels. Keep text large and clear. Make it scroll-stopping."""

    return prompt


def generate_all_prompts():
    """Generate all industry × pack × style combinations."""
    industry_mapping, elements = load_data()
    
    # Get element packs
    packs = {p["pack_id"]: p for p in elements["element_packs"]["packs"]}
    
    # Content examples for each industry (from carousel_prompts.json template)
    content_examples = {
        "apparel_fashion": {
            "tribe_callout_examples": ["Sneakerheads", "Minimalist Dressers", "Sustainable Style Lovers"],
            "myth_examples": ["Quality = Expensive", "Trends matter most"],
            "stat_examples": ["50K+ happy customers", "97% would buy again"],
            "pain_points": ["Nothing fits right", "Closet full but nothing to wear"],
            "cta_examples": ["Shop the look", "Get styled"]
        },
        "beauty_personal_care": {
            "tribe_callout_examples": ["Sensitive Skin Warriors", "Clean Beauty Converts"],
            "myth_examples": ["More products = better skin", "Expensive = effective"],
            "stat_examples": ["94% saw results in 2 weeks", "10M+ products sold"],
            "pain_points": ["Nothing works for my skin", "Overwhelmed by options"],
            "cta_examples": ["Start your routine", "Take the quiz"]
        },
        "food_beverage": {
            "tribe_callout_examples": ["Busy Parents", "Fitness Foodies"],
            "myth_examples": ["Healthy = tasteless", "Meal prep takes hours"],
            "stat_examples": ["1M+ meals delivered", "4.9★ taste rating"],
            "pain_points": ["No time to cook", "Kids won't eat healthy"],
            "cta_examples": ["Order now", "Try free"]
        },
        "health_wellness": {
            "tribe_callout_examples": ["Sleep Strugglers", "Biohackers"],
            "myth_examples": ["Supplements don't work", "More sleep = lazy"],
            "stat_examples": ["89% better sleep in 7 days", "Clinically tested"],
            "pain_points": ["Always tired", "Can't focus"],
            "cta_examples": ["Start healing", "Take the assessment"]
        },
        "home_living": {
            "tribe_callout_examples": ["Small Space Dwellers", "First-Time Homeowners"],
            "myth_examples": ["Good furniture = expensive", "Trends over comfort"],
            "stat_examples": ["100K+ homes styled", "4.8★ quality rating"],
            "pain_points": ["Space too small", "Don't know my style"],
            "cta_examples": ["Shop now", "Get inspired"]
        },
        "pet_care": {
            "tribe_callout_examples": ["Anxious Pet Parents", "Senior Dog Owners"],
            "myth_examples": ["Grain-free is always better", "More food = more love"],
            "stat_examples": ["2M+ happy pets", "Vet recommended"],
            "pain_points": ["Worried about ingredients", "Pet won't eat anything"],
            "cta_examples": ["Shop for your pet", "Try risk-free"]
        },
        "marketing_sales_martech": {
            "tribe_callout_examples": ["Solo Founders", "Growth Marketers"],
            "myth_examples": ["More tools = better results", "Cold email is dead"],
            "stat_examples": ["40% increase in conversions", "10K+ companies trust us"],
            "pain_points": ["Too many tools, no results", "Can't prove ROI"],
            "cta_examples": ["Start free trial", "Book a demo"]
        },
        "hr_hrtech": {
            "tribe_callout_examples": ["Startup HR Teams", "Remote-First Companies"],
            "myth_examples": ["HR software is all the same", "Culture can't be measured"],
            "stat_examples": ["50% less admin time", "90% employee satisfaction"],
            "pain_points": ["Drowning in paperwork", "Can't retain talent"],
            "cta_examples": ["Simplify HR", "Start free"]
        },
        "productivity_collaboration": {
            "tribe_callout_examples": ["Remote Teams", "Project Managers"],
            "myth_examples": ["More meetings = more alignment", "Busy = productive"],
            "stat_examples": ["3hrs saved per week", "1M+ teams trust us"],
            "pain_points": ["Meetings eat my day", "Nothing gets done"],
            "cta_examples": ["Work smarter", "Try free"]
        },
        "finance_accounting_fintech": {
            "tribe_callout_examples": ["Startup CFOs", "Freelancers"],
            "myth_examples": ["Accounting is just tax time", "Excel is good enough"],
            "stat_examples": ["$50K avg savings found", "99.9% accuracy"],
            "pain_points": ["Don't know where money goes", "Tax time panic"],
            "cta_examples": ["Take control", "See your numbers"]
        },
        "developer_tools_devtools": {
            "tribe_callout_examples": ["Solo Devs", "Platform Engineers"],
            "myth_examples": ["Build everything yourself", "Monitoring is optional"],
            "stat_examples": ["50% faster deploys", "99.99% uptime"],
            "pain_points": ["Debugging takes forever", "On-call burnout"],
            "cta_examples": ["Deploy now", "Start building"]
        }
    }
    
    all_prompts = []
    prompt_id = 0
    
    for industry in industry_mapping["industries"]:
        industry_id = industry["id"]
        recommended_packs = industry.get("example_carousel_packs", [])
        primary_styles = industry["recommended_styles"]["primary"]
        secondary_styles = industry["recommended_styles"]["secondary"]
        all_styles = primary_styles + secondary_styles
        
        examples = content_examples.get(industry_id, {})
        
        for pack_id in recommended_packs:
            if pack_id not in packs:
                continue
            pack = packs[pack_id]
            
            for style_name in all_styles:
                prompt_id += 1
                prompt_text = build_prompt(industry, pack, style_name, examples)
                
                all_prompts.append({
                    "id": prompt_id,
                    "industry_id": industry_id,
                    "industry_name": industry["name"],
                    "sector": industry["sector"],
                    "pack_id": pack_id,
                    "pack_name": pack["pack_name"],
                    "style_name": style_name,
                    "style_tier": "primary" if style_name in primary_styles else "secondary",
                    "hook_pattern": pack["hook_pattern_primary"],
                    "prompt": prompt_text,
                    "filename": f"{prompt_id:03d}_{industry_id}_{pack_id}_{style_name.lower().replace(' ', '_')}.png"
                })
    
    return all_prompts


def main():
    """Generate and save all prompts."""
    print("🎨 Generating carousel prompts...")
    
    prompts = generate_all_prompts()
    
    # Save to file
    output = {
        "version": "4.0",
        "description": "Generated carousel prompts - Industry × Pack × Style combinations",
        "total_prompts": len(prompts),
        "generation_spec": {
            "format": "Single horizontal strip containing 5 slides side by side",
            "dimensions": "5400x1080 pixels (5 slides at 1080x1080 each)",
            "design_principles": [
                "MESSAGE FIRST - Text must be instantly readable",
                "Clean layouts with generous breathing room",
                "Limited color palette (2-3 colors max)",
                "Consistent visual language across all 5 slides",
                "Typography-driven, not decoration-driven",
                "NO busy backgrounds or overwhelming patterns"
            ]
        },
        "prompts": prompts
    }
    
    output_file = DATA_DIR / "generated_prompts.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    # Summary
    print(f"\n✅ Generated {len(prompts)} prompts")
    print(f"📁 Saved to: {output_file}")
    
    # Breakdown
    industries = set(p["industry_id"] for p in prompts)
    packs = set(p["pack_id"] for p in prompts)
    styles = set(p["style_name"] for p in prompts)
    
    print(f"\n📊 Breakdown:")
    print(f"   Industries: {len(industries)}")
    print(f"   Packs: {len(packs)}")
    print(f"   Styles: {len(styles)}")
    
    return prompts


if __name__ == "__main__":
    main()

