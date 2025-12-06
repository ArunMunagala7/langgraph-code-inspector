# 🎨 Mermaid Diagram to Image Conversion

This feature allows you to convert the generated Mermaid flowcharts and call graphs into beautiful PNG images that can be easily viewed and shared.

## 📋 Prerequisites

You need to install **Mermaid CLI** (mmdc) to use this feature.

### Installation Options:

**Option 1: Using npm (Recommended)**
```bash
npm install -g @mermaid-js/mermaid-cli
```

**Option 2: Using yarn**
```bash
yarn global add @mermaid-js/mermaid-cli
```

**Option 3: Using Docker**
```bash
docker pull minlag/mermaid-cli
```

### Verify Installation:
```bash
mmdc --version
```

## 🚀 Usage

### Method 1: During Analysis (Automatic)

Generate images automatically when running code analysis:

```bash
# Analyze code and generate images
python main.py --sample python_binary_search --generate-images

# With custom code
python main.py --code "your code" --language python --generate-images
```

### Method 2: Convert Existing Analysis (Manual)

Convert previously generated analyses to images:

```bash
# Convert the latest analysis
python generate_images.py

# Convert a specific file
python generate_images.py --file outputs/analysis_20251205_194118.json

# Convert all analyses
python generate_images.py --all

# Specify output directory
python generate_images.py --output-dir my_images/
```

### Method 3: Python API

Use the converter directly in your code:

```python
from core.mermaid_converter import convert_mermaid_to_image, convert_analysis_to_images

# Convert a single Mermaid diagram
mermaid_code = """
flowchart TD
    Start([Start])
    Start --> End([End])
"""
convert_mermaid_to_image(mermaid_code, "output.png")

# Convert all diagrams in an analysis file
results = convert_analysis_to_images("outputs/analysis_123.json")
```

## 📊 Output

The generated images will be saved in `outputs/images/` by default:

```
outputs/images/
├── analysis_20251205_194118_flowchart.png
├── analysis_20251205_194118_callgraph.png
├── analysis_20251205_194217_flowchart.png
└── analysis_20251205_194217_callgraph.png
```

## 🎨 Customization

The converter uses a beautiful custom theme with:
- **Primary Color**: Purple gradient (#667eea → #764ba2)
- **Secondary Color**: Light blue (#a0c4ff)
- **Background**: White (default)
- **Smooth Curves**: Basis curve style for flowcharts

You can modify these in `core/mermaid_converter.py` by editing the `config` dictionary.

## 📖 Examples

### Example 1: Quick Image Generation

```bash
# Run analysis with images
python main.py --sample python_bubble_sort --generate-images

# Check the outputs/images/ directory
ls -lh outputs/images/
```

### Example 2: Batch Convert All Analyses

```bash
# Convert all existing analyses
python generate_images.py --all

# Images will be in outputs/images/
```

### Example 3: Custom Output Location

```bash
# Save images to a custom directory
python generate_images.py --output-dir diagrams/
```

## 🐛 Troubleshooting

### Error: "mmdc: command not found"

**Solution**: Install Mermaid CLI using npm:
```bash
npm install -g @mermaid-js/mermaid-cli
```

### Error: "Chromium not found"

Mermaid CLI requires Chromium/Puppeteer. Install with:
```bash
npm install -g @mermaid-js/mermaid-cli
```

### Timeout Errors

For complex diagrams, increase the timeout in `mermaid_converter.py`:
```python
result = subprocess.run(cmd, timeout=60)  # Increase from 30 to 60
```

## ✨ Features

- ✅ Automatic conversion during analysis
- ✅ Batch conversion of existing analyses
- ✅ Custom themes and styling
- ✅ High-quality PNG output
- ✅ Configurable output directories
- ✅ Error handling and validation

## 📚 More Information

- Mermaid CLI: https://github.com/mermaid-js/mermaid-cli
- Mermaid Documentation: https://mermaid.js.org/
- Mermaid Live Editor: https://mermaid.live/

## 💡 Tips

1. **High Resolution**: The images are generated at high resolution suitable for presentations
2. **Themes**: You can change themes to 'dark', 'forest', or 'neutral' in the converter
3. **Batch Processing**: Use `--all` flag to convert multiple analyses at once
4. **Integration**: Embed the PNG images in documentation, presentations, or reports
