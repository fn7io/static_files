#!/usr/bin/env python3
"""
Remove person from reference style images using Google Gemini 3 Pro Image Preview.

This script takes a reference style image containing a person/portrait,
and generates a version with the person removed while preserving the 
background and artistic style.

Usage:
    python remove_person.py style_Watercolor.png
    python remove_person.py --all  # Process all images in reference_styles/
"""

import os
import sys
from pathlib import Path

try:
    from google import genai
    from PIL import Image
except ImportError:
    print("Error: google-genai package not installed.")
    print("Please install it with: pip install google-genai pillow")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def remove_person_from_image(
    input_path: str,
    output_path: str,
    api_key: str = None
) -> str:
    """
    Remove the person from an image while preserving the background and style.
    
    Args:
        input_path: Path to the input image
        output_path: Path to save the modified image
        api_key: Google Gemini API key (or uses env var)
    
    Returns:
        Path to the saved image, or None if failed
    """
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key required. Set GEMINI_API_KEY environment variable.")
    
    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.0-flash-exp-image-generation"  # Use the image editing model
    
    # Load the image
    img = Image.open(input_path)
    print(f"📸 Original image size: {img.size}")
    
    # Instagram Reel dimensions (9:16 aspect ratio)
    REEL_WIDTH = 1080
    REEL_HEIGHT = 1920
    
    # Create prompt for person removal
    prompt = f"""Edit this image to remove the person/portrait from the image completely.

CRITICAL INSTRUCTIONS:
- Remove ONLY the person (face, body, clothing) from the image
- Fill the area where the person was with a seamless continuation of the background
- Maintain the EXACT same artistic style, color palette, and texture throughout
- The background should flow naturally through where the person was
- Keep all other elements (flowers, patterns, scenery, objects) intact
- The result should look like the original image was always just a background/scene without any person
- Output the image in a vertical 9:16 aspect ratio format ({REEL_WIDTH}x{REEL_HEIGHT} pixels) suitable for Instagram Reels
- Extend or crop the composition as needed to fit this vertical format while preserving the style

Do NOT:
- Change the overall style or mood of the image
- Add new elements that weren't in the original background
- Leave any traces or artifacts of the person"""

    print(f"\n🎨 Removing person from: {Path(input_path).name}")
    
    try:
        # Generate edited image using the API with the source image
        response = client.models.generate_content(
            model=model_name,
            contents=[
                img,
                prompt
            ],
            config=genai.types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"]
            )
        )
        
        # Process response to extract images
        images = []
        for part in response.parts:
            if part.text is not None:
                print(f"📝 Response: {part.text[:200]}...")
            elif part.inline_data is not None:
                # Convert to PIL Image
                image = part.as_image()
                images.append(image)
        
        if images:
            # Save the result
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            img_result = images[0]
            
            # Convert Gemini Image to PIL Image
            # The Gemini API returns an Image object with _pil_image attribute or we need to decode from data
            if hasattr(img_result, '_pil_image') and img_result._pil_image is not None:
                img_to_save = img_result._pil_image
            elif hasattr(img_result, 'data'):
                # Decode from base64 data
                import io
                import base64
                img_data = base64.b64decode(img_result.data)
                img_to_save = Image.open(io.BytesIO(img_data))
            else:
                # Try to save directly first, then reload for resize
                temp_path = output_file.with_suffix('.temp.png')
                img_result.save(str(temp_path))
                img_to_save = Image.open(str(temp_path))
            
            # Get size and resize to Instagram Reel dimensions
            current_w, current_h = img_to_save.size
            print(f"📐 Generated image size: {current_w}x{current_h}")
            
            if (current_w, current_h) != (REEL_WIDTH, REEL_HEIGHT):
                print(f"📐 Resizing to Instagram Reel size ({REEL_WIDTH}x{REEL_HEIGHT})")
                img_to_save = img_to_save.resize((REEL_WIDTH, REEL_HEIGHT), Image.Resampling.LANCZOS)
            
            print(f"📐 Final size: {img_to_save.size}")
            img_to_save.save(str(output_file))
            
            # Clean up temp file if exists
            temp_path = output_file.with_suffix('.temp.png')
            if temp_path.exists():
                temp_path.unlink()
            
            print(f"✅ Modified image saved to: {output_file}")
            return str(output_file)
        else:
            print("❌ No images generated in response")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Remove person from reference style images"
    )
    parser.add_argument(
        "input",
        type=str,
        nargs="?",
        help="Input image filename (e.g., style_Watercolor.png) or 'all' to process all"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output path (default: modified_styles/<same filename>)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all images in reference_styles/"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Google Gemini API key (or set GEMINI_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    # Determine base directory
    script_dir = Path(__file__).parent
    input_dir = script_dir / "reference_styles"
    output_dir = script_dir / "modified_styles"
    
    if args.all:
        # Process all images
        images = list(input_dir.glob("style_*.png"))
        print(f"Found {len(images)} style images total")
        
        # Skip already processed images
        already_done = set(f.name for f in output_dir.glob("style_*.png"))
        images_to_process = [img for img in images if img.name not in already_done]
        print(f"Already processed: {len(already_done)}, Remaining: {len(images_to_process)}")
        
        for idx, img_path in enumerate(images_to_process, 1):
            print(f"\n[{idx}/{len(images_to_process)}] Processing {img_path.name}")
            output_path = output_dir / img_path.name
            result = remove_person_from_image(
                str(img_path),
                str(output_path),
                api_key=args.api_key
            )
            if result:
                print(f"✨ Processed: {img_path.name}\n")
            else:
                print(f"❌ Failed: {img_path.name}\n")
    
    elif args.input:
        # Process single image
        input_path = input_dir / args.input
        
        if not input_path.exists():
            # Try as absolute path
            input_path = Path(args.input)
        
        if not input_path.exists():
            print(f"❌ Error: Input image not found: {args.input}")
            sys.exit(1)
        
        output_path = args.output or str(output_dir / input_path.name)
        
        result = remove_person_from_image(
            str(input_path),
            output_path,
            api_key=args.api_key
        )
        
        if result:
            print(f"\n✨ Success! Modified image: {result}")
        else:
            print("\n❌ Failed to process image")
            sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

