# Google Nano Banana Pro Image Generation

This project provides a Python script to generate images using Google's Nano Banana Pro model via the Gemini API.

## Features

- 🎨 Text-to-image generation with Nano Banana Pro
- 🖼️ Style support (can reference styles from `reference_styles/` directory)
- 📐 Configurable resolution (up to 4K)
- 🔒 Secure API key management
- 💾 Save generation results with metadata

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey) or [MakerSuite](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Configure API Key

**Option A: Environment Variable (Recommended)**

```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Option B: .env File**

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

**Option C: Pass as Argument**

You can pass the API key directly when running the script (see Usage below).

## Usage

### Command Line

**Basic usage:**
```bash
python generate_image.py "a serene landscape with mountains and a lake"
```

**With style:**
```bash
python generate_image.py "a portrait of a person" --style "Watercolor"
```

**With custom resolution:**
```bash
python generate_image.py "a futuristic city" --resolution "2048x2048"
```

**Full example:**
```bash
python generate_image.py \
  "a beautiful sunset over the ocean" \
  --style "Oil Painting" \
  --resolution "1024x1024" \
  --output "my_image" \
  --num-images 1
```

### Python Script

```python
from generate_image import NanoBananaProGenerator

# Initialize generator
generator = NanoBananaProGenerator()

# Generate image
result = generator.generate_image(
    prompt="a cat wearing a space helmet",
    style="Anime",
    resolution="1024x1024",
    output_path="outputs/space_cat"
)

print(result)
```

### Using Style References

If you want to use styles from the `reference_styles/` directory:

```python
from generate_image import NanoBananaProGenerator

generator = NanoBananaProGenerator()

result = generator.generate_with_style_reference(
    prompt="a portrait of a person",
    style_name="Watercolor",  # Matches style_Watercolor.png
    reference_styles_dir="reference_styles"
)
```

## Available Styles

You can use any of the styles from your `reference_styles/` directory. Some examples:

- Watercolor
- Oil Painting
- Anime
- Photorealism
- Impressionism
- Surrealism
- Cyberpunk
- Pixel Art
- And many more...

## Output

The script generates:
- JSON file with generation metadata and results
- Image files (format depends on API response)

Output files are saved to:
- Custom path if `--output` is specified
- `generated_images/output_<timestamp>` by default

## API Notes

This implementation uses:
- **Model**: `gemini-3-pro-image-preview` (Nano Banana Pro)
- **Library**: `google-genai` (not `google-generativeai`)
- **API**: Google Gemini API via Google AI Studio

The code automatically:
- Extracts images from API response
- Saves images as PNG files
- Stores metadata in JSON format

For the latest API documentation, visit:
- [Google AI for Developers](https://ai.google.dev/gemini-api/docs/image-generation)
- [Google AI Studio](https://aistudio.google.com/)

## Troubleshooting

### "API key required" error
- Make sure you've set `GEMINI_API_KEY` environment variable
- Or pass `--api-key` argument
- Or create a `.env` file with your key

### "Model not found" error
- Verify the model name is correct
- Check if Nano Banana Pro is available in your region
- Try using `gemini-1.5-pro` or `gemini-pro` as alternatives

### Import errors
- Run `pip install -r requirements.txt`
- Make sure you're using Python 3.8+

## License

This code is provided as-is for educational and development purposes.

