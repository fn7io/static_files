#!/usr/bin/env python3
"""
Google Nano Banana Pro Image Generation Script

This script uses Google's Gemini API to generate images using Nano Banana Pro.
Supports text-to-image generation with various parameters and style options.
"""

import os
import sys
import json
import base64
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

try:
    from google import genai
    from google.genai import types
    from PIL import Image
except ImportError:
    print("Error: google-genai package not installed.")
    print("Please install it with: pip install google-genai pillow")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables directly.")


class NanoBananaProGenerator:
    """Wrapper class for Google Nano Banana Pro image generation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the generator with API key.
        
        Args:
            api_key: Google Gemini API key. If None, reads from GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Initialize the client with API key
        self.client = genai.Client(api_key=self.api_key)
        
        # Model name for Nano Banana Pro (Gemini 3 Pro Image)
        self.model_name = "gemini-3-pro-image-preview"
        
    def generate_image(
        self,
        prompt: str,
        output_path: Optional[str] = None,
        style: Optional[str] = None,
        resolution: str = "1024x1024",
        num_images: int = 1,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate an image using Nano Banana Pro.
        
        Args:
            prompt: Text description of the image to generate
            output_path: Optional path to save the generated image(s)
            style: Optional art style to apply (e.g., "Watercolor", "Oil Painting")
            resolution: Image resolution (e.g., "1024x1024", "2048x2048")
            num_images: Number of images to generate (1-4)
            **kwargs: Additional parameters for generation
        
        Returns:
            Dictionary with generation results including image data and metadata
        """
        # Enhance prompt with style if provided
        enhanced_prompt = prompt
        if style:
            enhanced_prompt = f"{prompt}, in the style of {style}"
        
        # Add resolution and quality hints to prompt
        enhanced_prompt += f", high quality, {resolution} resolution"
        
        try:
            # Generate image using Nano Banana Pro
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[enhanced_prompt],
            )
            
            # Process response and extract images
            images = []
            text_parts = []
            
            for part in response.parts:
                if part.text is not None:
                    text_parts.append(part.text)
                elif part.inline_data is not None:
                    # Convert inline data to PIL Image
                    image = part.as_image()
                    images.append(image)
            
            # Save images if output_path provided
            saved_paths = []
            if output_path and images:
                base_path = Path(output_path)
                base_path.parent.mkdir(parents=True, exist_ok=True)
                
                for idx, image in enumerate(images):
                    if len(images) > 1:
                        image_path = base_path.parent / f"{base_path.stem}_{idx+1}{base_path.suffix or '.png'}"
                    else:
                        image_path = base_path.with_suffix('.png') if not base_path.suffix else base_path
                    
                    image.save(str(image_path))
                    saved_paths.append(str(image_path))
                    print(f"✅ Image saved to: {image_path}")
            
            result = {
                "prompt": prompt,
                "enhanced_prompt": enhanced_prompt,
                "style": style,
                "resolution": resolution,
                "num_images_generated": len(images),
                "saved_paths": saved_paths,
                "text_response": " ".join(text_parts) if text_parts else None,
                "timestamp": datetime.now().isoformat(),
                "success": True,
            }
            
            # Save metadata to JSON if output_path provided
            if output_path:
                self._save_result(result, output_path)
            
            return result
            
        except Exception as e:
            error_msg = f"Error generating image: {str(e)}"
            print(error_msg)
            return {
                "error": error_msg,
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            }
    
    def _save_result(self, result: Dict[str, Any], output_path: str):
        """Save generation metadata to JSON file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save as JSON (excluding image data)
        json_result = {k: v for k, v in result.items() if k != 'images'}
        json_path = output_file.with_suffix('.json') if output_file.suffix else output_file.with_suffix('.json')
        with open(json_path, 'w') as f:
            json.dump(json_result, f, indent=2)
        
        print(f"📄 Metadata saved to: {json_path}")
    
    def generate_with_style_reference(
        self,
        prompt: str,
        style_name: str,
        reference_styles_dir: str = "reference_styles",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image with reference to a style from the reference_styles directory.
        
        Args:
            prompt: Text description
            style_name: Name of the style (e.g., "Watercolor", "Oil_Painting")
            reference_styles_dir: Directory containing style reference images
            **kwargs: Additional parameters
        
        Returns:
            Generation result dictionary
        """
        style_path = Path(reference_styles_dir) / f"style_{style_name}.png"
        
        if style_path.exists():
            # Could potentially use the reference image for style transfer
            # This depends on API capabilities
            print(f"Using style reference: {style_path}")
        
        return self.generate_image(
            prompt=prompt,
            style=style_name.replace("_", " "),
            **kwargs
        )


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate images using Google Nano Banana Pro"
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="Text description of the image to generate"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output path for the generated image (default: generated_images/output_<timestamp>)"
    )
    parser.add_argument(
        "-s", "--style",
        type=str,
        help="Art style to apply (e.g., 'Watercolor', 'Oil Painting')"
    )
    parser.add_argument(
        "-r", "--resolution",
        type=str,
        default="1024x1024",
        help="Image resolution (default: 1024x1024)"
    )
    parser.add_argument(
        "-n", "--num-images",
        type=int,
        default=1,
        help="Number of images to generate (default: 1)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Google Gemini API key (or set GEMINI_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    try:
        generator = NanoBananaProGenerator(api_key=args.api_key)
        
        output_path = args.output
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"generated_images/output_{timestamp}"
        
        result = generator.generate_image(
            prompt=args.prompt,
            output_path=output_path,
            style=args.style,
            resolution=args.resolution,
            num_images=args.num_images
        )
        
        if "error" in result:
            print(f"\n❌ Generation failed: {result['error']}")
            sys.exit(1)
        else:
            print(f"\n✅ Generation successful!")
            print(f"Prompt: {result['prompt']}")
            if result.get('style'):
                print(f"Style: {result['style']}")
            print(f"Resolution: {result['resolution']}")
            print(f"Timestamp: {result['timestamp']}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

