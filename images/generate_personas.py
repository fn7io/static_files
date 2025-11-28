#!/usr/bin/env python3
"""
Generate persona images using Google Gemini based on persona_prompts_243.csv
Saves images to reference_personas directory with full HTTP endpoints.
"""

import os
import sys
import csv
import time
import subprocess
from pathlib import Path
from datetime import datetime

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
    print("Warning: python-dotenv not installed. Using environment variables directly.")


class PersonaImageGenerator:
    """Generate persona images using Google Gemini API."""

    def __init__(self, api_key: str = None):
        """Initialize the generator with API key."""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Initialize the client with API key
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-3-pro-image-preview"

        # Base URL for hosted images
        self.base_url = "https://fn7io.github.io/static_files/images/reference_personas"

    def generate_persona_image(
        self,
        prompt: str,
        output_path: str,
        persona_info: dict
    ) -> bool:
        """
        Generate a single persona image.

        Args:
            prompt: AI prompt for image generation
            output_path: Full path where to save the image
            persona_info: Dictionary with persona metadata

        Returns:
            True if successful, False otherwise
        """
        try:
            # System prompt for consistent style
            system_prompt = """IMPORTANT STYLE REQUIREMENTS:
- Composition: Mid shot only (waist up to head), centered subject
- Background: Soft pastel gradient background (pink, blue, lavender, peach tones)
- Focus: Sharp focus on the person, they are the main subject
- Lighting: Soft, even lighting that flatters the subject
- Style: Professional, clean, modern portrait photography
- Background must be smooth gradient, no busy patterns or distracting elements
- REQUIRED: Must include visible "AI Generated" text tag/watermark on the image

"""

            # Combine system prompt with user prompt
            full_prompt = system_prompt + prompt

            # Generate image using Gemini API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[full_prompt]
            )

            # Process response to extract images
            images = []
            for part in response.parts:
                if part.text is not None:
                    print(f"  📝 Response text: {part.text[:100]}...")
                elif part.inline_data is not None:
                    image = part.as_image()
                    images.append(image)

            if not images:
                print("  ❌ No image generated in response")
                return False

            # Save the image
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            img_to_save = images[0]
            img_to_save.save(str(output_file))
            print(f"  ✅ Image saved to: {output_file}")

            return True

        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            return False


def get_processed_personas():
    """Get list of already processed persona filenames."""
    output_dir = Path("reference_personas")
    if not output_dir.exists():
        return set()

    return {f.name for f in output_dir.glob("*.jpg")} | {f.name for f in output_dir.glob("*.png")}


def load_persona_prompts():
    """Load all persona prompts from CSV."""
    csv_path = Path("persona_prompts_243.csv")

    if not csv_path.exists():
        print("❌ Error: persona_prompts_243.csv not found")
        return []

    personas = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            personas.append(row)

    return personas


def save_results_json(results: list):
    """Save results with full HTTP endpoints to JSON (excluding AI_Prompt)."""
    output_path = Path("persona_images_generated.json")

    if not results:
        print("⚠️  No results to save")
        return

    # Remove AI_Prompt from results and ensure Image_URL is present
    cleaned_results = []
    for result in results:
        cleaned = {k: v for k, v in result.items() if k != 'AI_Prompt'}
        cleaned_results.append(cleaned)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Results saved to: {output_path}")


def main():
    """Main function to process all personas."""
    print("🚀 Persona Image Generator")
    print("=" * 70)

    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        sys.exit(1)

    # Initialize generator
    try:
        generator = PersonaImageGenerator(api_key=api_key)
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        sys.exit(1)

    # Load persona prompts
    personas = load_persona_prompts()
    if not personas:
        print("❌ No persona prompts found")
        sys.exit(1)

    print(f"📊 Total personas to process: {len(personas)}")

    # Check for already processed personas
    processed = get_processed_personas()
    print(f"✅ Already processed: {len(processed)}")

    # Filter remaining personas
    remaining = [p for p in personas if p['Image_File_Name'] not in processed]
    print(f"🔄 Remaining to process: {len(remaining)}")

    if not remaining:
        print("\n✨ All personas have been processed!")
        return

    print(f"\n⚡ Generating continuously with no delays")
    print("=" * 70)

    successful = 0
    failed = 0
    results = []

    for i, persona in enumerate(remaining, 1):
        persona_name = persona['Persona_Name']
        image_filename = persona['Image_File_Name']
        prompt = persona['AI_Prompt']

        print(f"\n[{i}/{len(remaining)}] Generating: {persona_name}")
        print(f"  📝 Role: {persona['Role']}")
        print(f"  🏢 Industry: {persona['Industry_Name']}")
        print(f"  📁 File: {image_filename}")

        # Generate output path
        output_path = f"reference_personas/{image_filename}"

        # Generate image
        success = generator.generate_persona_image(
            prompt=prompt,
            output_path=output_path,
            persona_info=persona
        )

        if success:
            successful += 1
            # Add full URL to results
            result = persona.copy()
            result['Image_URL'] = f"{generator.base_url}/{image_filename}"
            results.append(result)
        else:
            failed += 1

        # No delay - generate continuously
        pass

    # Save results
    if results:
        save_results_json(results)

    # Summary
    print("\n" + "=" * 70)
    print("📊 Processing Summary:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📁 Total processed: {successful + len(processed)}/{len(personas)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
