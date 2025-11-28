#!/usr/bin/env python3
"""
Generate carousel images using Gemini 3 Pro Image Preview.

This script reads prompts from generated_prompts.json and uses 
Google's Gemini 3 Pro Image Preview model to create images.
Optionally uses style reference images for better consistency.

Usage:
    python generate_with_gemini.py [--index INDEX] [--output OUTPUT_PATH]
    python generate_with_gemini.py --use-reference  # Use style reference images

Requirements:
    pip install google-genai pillow python-dotenv

Environment:
    GEMINI_API_KEY - Your Google Gemini API key
"""

import json
import sys
import base64
import argparse
from pathlib import Path

# Add parent directories to path to import shared generator
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from generate_image import NanoBananaProGenerator

try:
    from google import genai
    from google.genai import types
    from PIL import Image
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install: pip install google-genai pillow")
    sys.exit(1)


# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
REFS_DIR = DATA_DIR / "style_references"


def load_prompts(json_path: str) -> list:
    """Load prompts from the generated_prompts.json file."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data.get('prompts', [])


def load_reference_image(ref_path: str) -> Image.Image:
    """Load a reference image from the data directory."""
    full_path = DATA_DIR / ref_path
    if full_path.exists():
        return Image.open(full_path)
    return None


def generate_with_reference(prompt_text: str, reference_image: Image.Image, output_path: str) -> dict:
    """
    Generate an image using Gemini with a style reference.
    
    Uses the multimodal capability to show a reference image
    and ask for generation in that style.
    """
    import os
    from google import genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")
    
    client = genai.Client(api_key=api_key)
    
    # Enhanced prompt with reference context
    enhanced_prompt = f"""Look at the provided reference image showing a carousel style.

Generate a NEW carousel in EXACTLY this same visual style:
- Same color palette
- Same typography style  
- Same layout approach
- Same visual atmosphere

CONTENT TO GENERATE:
{prompt_text}

Create a horizontal strip showing 5 slides side by side in THIS EXACT style.
Match the reference image's aesthetic perfectly."""

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[
                reference_image,
                enhanced_prompt
            ],
        )
        
        # Extract generated image
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                
                # Save the image
                output_file = Path(output_path).with_suffix('.png')
                output_file.parent.mkdir(parents=True, exist_ok=True)
                image.save(str(output_file))
                
                return {
                    "success": True,
                    "saved_paths": [str(output_file)]
                }
        
        # If no image generated, check for text response
        text_parts = [p.text for p in response.parts if p.text]
        return {
            "success": False,
            "error": f"No image generated. Response: {' '.join(text_parts)[:200]}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Generate carousel images using Gemini 3 Pro Image Preview'
    )
    parser.add_argument(
        '--index', '-i',
        type=int,
        default=0,
        help='Index of the prompt to use (default: 0, first prompt)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output path for the generated image (default: auto-generated based on prompt)'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available prompts and exit'
    )
    parser.add_argument(
        '--use-reference', '-r',
        action='store_true',
        help='Use style reference image if available'
    )
    
    args = parser.parse_args()
    
    # Path to the prompts JSON file
    script_dir = Path(__file__).parent
    json_path = script_dir / '../data/generated_prompts.json'
    
    # Load prompts
    prompts = load_prompts(json_path)
    
    if not prompts:
        print("Error: No prompts found in the JSON file")
        sys.exit(1)
    
    print(f"Loaded {len(prompts)} prompts from {json_path}")
    
    # List mode
    if args.list:
        print("\nAvailable prompts:")
        for i, p in enumerate(prompts[:20]):  # Show first 20
            has_ref = "📷" if p.get('style_reference') else "  "
            print(f"  [{i}] {has_ref} {p.get('industry_name', 'Unknown')} - {p.get('style_name', 'Unknown')} - {p.get('pack_name', 'Unknown')}")
        if len(prompts) > 20:
            print(f"  ... and {len(prompts) - 20} more")
        print("\n📷 = has style reference image")
        sys.exit(0)
    
    # Validate index
    if args.index < 0 or args.index >= len(prompts):
        print(f"Error: Index {args.index} out of range. Valid range: 0-{len(prompts)-1}")
        sys.exit(1)
    
    # Get the selected prompt
    selected_prompt = prompts[args.index]
    prompt_text = selected_prompt.get('prompt', '')
    style_reference = selected_prompt.get('style_reference')
    
    if not prompt_text:
        print(f"Error: No prompt text found at index {args.index}")
        sys.exit(1)
    
    print(f"\n--- Selected Prompt Info ---")
    print(f"ID: {selected_prompt.get('id')}")
    print(f"Industry: {selected_prompt.get('industry_name')}")
    print(f"Style: {selected_prompt.get('style_name')}")
    print(f"Pack: {selected_prompt.get('pack_name')}")
    print(f"Reference: {style_reference or 'None'}")
    print(f"----------------------------\n")
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        filename = selected_prompt.get('filename', f'generated_{args.index}.png')
        output_dir = script_dir / '../output'
        output_dir.mkdir(exist_ok=True)
        output_path = str(output_dir / filename.replace('.png', ''))
    
    # Check for reference image usage
    reference_image = None
    if args.use_reference and style_reference:
        reference_image = load_reference_image(style_reference)
        if reference_image:
            print(f"📷 Using style reference: {style_reference}")
        else:
            print(f"⚠️  Reference not found: {style_reference}, proceeding without reference")
    
    # Generate the image
    if reference_image:
        print(f"Generating image with style reference...")
        result = generate_with_reference(prompt_text, reference_image, output_path)
    else:
        # Initialize generator (uses GEMINI_API_KEY from environment)
        try:
            generator = NanoBananaProGenerator()
        except ValueError as e:
            print(f"Error: {e}")
            print("Please set GEMINI_API_KEY environment variable")
            sys.exit(1)
        
        print(f"Generating image with Gemini 3 Pro Image Preview...")
        print(f"Prompt length: {len(prompt_text)} characters")
        
        result = generator.generate_image(
            prompt=prompt_text,
            output_path=output_path,
        )
    
    if result.get("success"):
        print(f"\n✓ Successfully generated image!")
        if result.get("saved_paths"):
            for path in result["saved_paths"]:
                print(f"  → {path}")
    else:
        print(f"\n✗ Error generating image: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == '__main__':
    main()
