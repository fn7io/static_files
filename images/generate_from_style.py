#!/usr/bin/env python3
"""
Extend background of reference style images using Google Nano Banana Pro.

This script takes a reference style image and extends the background
to better showcase the art style while maintaining the original face/portrait.
"""

import os
import sys
from pathlib import Path
from PIL import Image
import base64
import io

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


def image_to_base64(image_path: str) -> str:
    """Convert image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def generate_from_style(
    image_path: str,
    style_name: str,
    style_description: str,
    output_path: str,
    api_key: str = None
):
    """
    Extend the background of an image using Nano Banana Pro.
    
    Args:
        image_path: Path to the input image
        style_name: Name of the art style
        style_description: Description of the style
        output_path: Path to save the extended image
        api_key: Google Gemini API key (or uses env var)
    """
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key required. Set GEMINI_API_KEY environment variable.")
    
    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    model_name = "gemini-3-pro-image-preview"
    
    # Load and prepare the image
    img = Image.open(image_path)
    print(f"📸 Original image size: {img.size}")
    
    # Target size for all extended images (matching Watercolor extended image)
    TARGET_WIDTH = 1264
    TARGET_HEIGHT = 848
    
    # Create prompt for new image generation from style reference
    prompt = f"""Generate a new image in the style of '{style_name}'.
    
Style Description: {style_description}

Subject Requirement:
- The image MUST feature a portrait of a female in her mid-20s.
- This portrait (face and upper body) should occupy approximately 30% of the total image area.
- The subject should be positioned in a way that balances the composition (e.g., centered or using rule of thirds).

Style & Composition Requirements:
- The remaining 70% of the image must be a rich, detailed environment or background that fully embodies the '{style_name}' style.
- Use the background to showcase the defining characteristics of the style (e.g., textures, patterns, lighting, brushwork, color palette).
- The goal is to create a reference image that is a perfect example of the '{style_name}' style.
- The final image dimensions must be exactly {TARGET_WIDTH} pixels wide by {TARGET_HEIGHT} pixels tall.

Instruction Summary:
Create a {TARGET_WIDTH}x{TARGET_HEIGHT} image in the '{style_name}' style featuring a female in her mid-20s (30% of frame) set against a detailed, style-appropriate background (70% of frame)."""

    print(f"\n🎨 Generating new image for: {style_name}")
    print(f"📝 Style: {style_description}\n")
    
    try:
        # Generate extended image using the API
        # Format: pass only the prompt, NOT the reference image
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt]
        )
        
        # Process response to extract images
        images = []
        for part in response.parts:
            if part.text is not None:
                print(f"📝 Response text: {part.text[:200]}...")
            elif part.inline_data is not None:
                # Convert to PIL Image
                image = part.as_image()
                images.append(image)
        
        if not images:
            # Alternative: Generate new image with style description (without reference)
            print("⚠️  No image in response. Trying alternative generation method...")
            
            alt_prompt = f"""Create a {style_name} style portrait with an extended, detailed background.

Style: {style_description}

The image should have:
- A portrait in the center
- Extensive background that clearly shows the {style_name} style
- Background should be the main focus showcasing: {style_description}
- Wide composition with much more background than foreground
- Maintain the exact artistic style: {style_description}"""
            
            response = client.models.generate_content(
                model=model_name,
                contents=[alt_prompt]
            )
            
            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    images.append(image)
        
        if images:
            # Save the first result
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Target size for all extended images (matching Watercolor extended image)
            TARGET_WIDTH = 1264
            TARGET_HEIGHT = 848
            
            # Handle different image types
            img_to_save = images[0]
            if not isinstance(img_to_save, Image.Image):
                # Convert to PIL Image if needed
                if hasattr(img_to_save, 'to_pil'):
                    img_to_save = img_to_save.to_pil()
                elif hasattr(img_to_save, 'data'):
                    from io import BytesIO
                    import base64
                    img_data = base64.b64decode(img_to_save.data)
                    img_to_save = Image.open(BytesIO(img_data))
            
            # Resize to target dimensions if needed
            if hasattr(img_to_save, 'size') and img_to_save.size != (TARGET_WIDTH, TARGET_HEIGHT):
                print(f"📐 Resizing from {img_to_save.size} to target size {TARGET_WIDTH}x{TARGET_HEIGHT}")
                img_to_save = img_to_save.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
            
            img_to_save.save(str(output_file))
            print(f"✅ Extended image saved to: {output_file}")
            if hasattr(img_to_save, 'size'):
                print(f"📐 Final size: {img_to_save.size}")
            return str(output_file)
        else:
            print("❌ No images generated in response")
            print("💡 Tip: The API response format may vary. Check the response structure.")
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
        description="Extend background of reference style images"
    )
    parser.add_argument(
        "style_name",
        type=str,
        help="Name of the style (e.g., 'Cyberpunk', 'Watercolor')"
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        default=None,
        help="Input image path (default: reference_styles/style_<StyleName>.png)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output path (default: reference_styles_extended/style_<StyleName>_extended.png)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Google Gemini API key (or set GEMINI_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    # Determine input path
    if args.input:
        input_path = args.input
    else:
        style_file = args.style_name.replace(" ", "_")
        input_path = f"reference_styles/style_{style_file}.png"
    
    if not Path(input_path).exists():
        print(f"❌ Error: Input image not found: {input_path}")
        sys.exit(1)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        style_file = args.style_name.replace(" ", "_")
        output_path = f"reference_styles_extended/style_{style_file}.png"
    
    # Read style description from CSV
    csv_path = Path("combined_tables.csv")
    style_description = None
    if csv_path.exists():
        import csv
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Style Name'] == args.style_name:
                    style_description = row['Description']
                    break
    
    if not style_description:
        style_description = f"{args.style_name} art style"
        print(f"⚠️  Style description not found in CSV, using default")
    
    # Extend background
    result = generate_from_style(
        image_path=input_path,
        style_name=args.style_name,
        style_description=style_description,
        output_path=output_path,
        api_key=args.api_key
    )
    
    if result:
        print(f"\n✨ Success! Extended image: {result}")
    else:
        print("\n❌ Failed to extend image")
        sys.exit(1)


if __name__ == "__main__":
    main()

