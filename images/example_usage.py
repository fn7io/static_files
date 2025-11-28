#!/usr/bin/env python3
"""
Example usage of Google Nano Banana Pro image generation.
"""

from generate_image import NanoBananaProGenerator
import os

def main():
    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  Please set GEMINI_API_KEY environment variable")
        print("   export GEMINI_API_KEY='your_key_here'")
        return
    
    # Initialize generator
    print("🚀 Initializing Nano Banana Pro generator...")
    generator = NanoBananaProGenerator()
    
    # Example 1: Simple image generation
    print("\n📸 Example 1: Generating a simple image...")
    result1 = generator.generate_image(
        prompt="a serene landscape with mountains and a lake at sunset",
        output_path="generated_images/landscape"
    )
    print(f"✅ Generated {result1.get('num_images_generated', 0)} image(s)")
    
    # Example 2: Image with style
    print("\n🎨 Example 2: Generating with art style...")
    result2 = generator.generate_image(
        prompt="a portrait of a person",
        style="Watercolor",
        output_path="generated_images/portrait_watercolor"
    )
    print(f"✅ Generated {result2.get('num_images_generated', 0)} image(s)")
    
    # Example 3: Using style reference
    print("\n🖼️  Example 3: Using style reference from reference_styles...")
    result3 = generator.generate_with_style_reference(
        prompt="a futuristic cityscape",
        style_name="Cyberpunk",
        output_path="generated_images/cyberpunk_city"
    )
    print(f"✅ Generated {result3.get('num_images_generated', 0)} image(s)")
    
    # Example 4: High resolution
    print("\n📐 Example 4: High resolution image...")
    result4 = generator.generate_image(
        prompt="a detailed close-up of a flower",
        resolution="2048x2048",
        output_path="generated_images/flower_hd"
    )
    print(f"✅ Generated {result4.get('num_images_generated', 0)} image(s)")
    
    print("\n✨ All examples completed!")
    print("📁 Check the 'generated_images' directory for results")

if __name__ == "__main__":
    main()


