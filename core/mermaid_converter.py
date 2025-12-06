"""
Mermaid to Image Converter
Converts Mermaid diagrams to PNG images using mermaid-cli (mmdc)
"""
import os
import subprocess
import json
from typing import Optional
from pathlib import Path


def check_mermaid_cli_installed() -> bool:
    """
    Check if mermaid-cli (mmdc) is installed.
    
    Returns:
        True if installed, False otherwise
    """
    try:
        result = subprocess.run(['mmdc', '--version'], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_mermaid_cli_instructions() -> str:
    """
    Return installation instructions for mermaid-cli.
    
    Returns:
        Installation instructions as string
    """
    return """
╔════════════════════════════════════════════════════════════════════════╗
║         Mermaid CLI (mmdc) Installation Required                      ║
╚════════════════════════════════════════════════════════════════════════╝

To convert Mermaid diagrams to images, you need to install mermaid-cli.

📦 Installation Options:

Option 1: Using npm (recommended)
  npm install -g @mermaid-js/mermaid-cli

Option 2: Using yarn
  yarn global add @mermaid-js/mermaid-cli

Option 3: Using Docker
  docker pull minlag/mermaid-cli

After installation, verify with:
  mmdc --version

📖 More info: https://github.com/mermaid-js/mermaid-cli
"""


def convert_mermaid_to_image(mermaid_code: str, 
                            output_path: str,
                            diagram_type: str = "flowchart",
                            theme: str = "default",
                            background: str = "white") -> bool:
    """
    Convert Mermaid diagram code to PNG image.
    
    Args:
        mermaid_code: Mermaid diagram syntax
        output_path: Path to save the PNG image
        diagram_type: Type of diagram (flowchart, graph, etc.)
        theme: Mermaid theme (default, dark, forest, neutral)
        background: Background color
        
    Returns:
        True if successful, False otherwise
    """
    if not check_mermaid_cli_installed():
        print("❌ Mermaid CLI not installed!")
        print(install_mermaid_cli_instructions())
        return False
    
    # Create temporary mermaid file
    temp_mmd = "temp_diagram.mmd"
    
    try:
        # Write mermaid code to file
        with open(temp_mmd, 'w') as f:
            f.write(mermaid_code)
        
        # Configure mermaid
        config = {
            "theme": theme,
            "themeVariables": {
                "primaryColor": "#667eea",
                "primaryTextColor": "#fff",
                "primaryBorderColor": "#764ba2",
                "lineColor": "#764ba2",
                "secondaryColor": "#a0c4ff",
                "tertiaryColor": "#f8f9fa"
            },
            "flowchart": {
                "curve": "basis",
                "padding": 20
            }
        }
        
        config_file = "temp_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        # Run mermaid-cli
        cmd = [
            'mmdc',
            '-i', temp_mmd,
            '-o', output_path,
            '-t', theme,
            '-b', background,
            '-c', config_file
        ]
        
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True,
                              timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Image saved to: {output_path}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout: Conversion took too long")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Clean up temporary files
        if os.path.exists(temp_mmd):
            os.remove(temp_mmd)
        if os.path.exists(config_file):
            os.remove(config_file)


def convert_analysis_to_images(analysis_file: str, 
                               output_dir: str = "outputs/images") -> dict:
    """
    Convert all Mermaid diagrams in an analysis file to images.
    
    Args:
        analysis_file: Path to the analysis JSON file
        output_dir: Directory to save images
        
    Returns:
        Dictionary with paths to generated images
    """
    if not check_mermaid_cli_installed():
        print(install_mermaid_cli_instructions())
        return {}
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load analysis
    try:
        with open(analysis_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading analysis file: {e}")
        return {}
    
    results = {}
    base_name = Path(analysis_file).stem
    
    # Convert flowchart
    if 'flowchart' in data and data['flowchart']:
        flowchart_path = os.path.join(output_dir, f"{base_name}_flowchart.png")
        print(f"\n🎨 Converting flowchart...")
        if convert_mermaid_to_image(data['flowchart'], flowchart_path):
            results['flowchart'] = flowchart_path
    
    # Convert call graph
    if 'call_graph' in data and data['call_graph']:
        callgraph_path = os.path.join(output_dir, f"{base_name}_callgraph.png")
        print(f"\n🎨 Converting call graph...")
        if convert_mermaid_to_image(data['call_graph'], callgraph_path, "graph"):
            results['call_graph'] = callgraph_path
    
    return results


if __name__ == "__main__":
    import sys
    import glob
    
    print("\n" + "="*80)
    print("🎨 MERMAID DIAGRAM TO IMAGE CONVERTER")
    print("="*80 + "\n")
    
    # Check if mermaid-cli is installed
    if not check_mermaid_cli_installed():
        print(install_mermaid_cli_instructions())
        sys.exit(1)
    
    print("✅ Mermaid CLI is installed!\n")
    
    # Find latest analysis file
    analysis_files = glob.glob("outputs/analysis_*.json")
    if not analysis_files:
        print("❌ No analysis files found in outputs/")
        print("Run: python main.py --sample python_binary_search")
        sys.exit(1)
    
    latest_file = max(analysis_files, key=os.path.getctime)
    print(f"📄 Latest analysis: {latest_file}\n")
    
    # Convert to images
    results = convert_analysis_to_images(latest_file)
    
    if results:
        print("\n" + "="*80)
        print("✅ CONVERSION COMPLETE!")
        print("="*80)
        for diagram_type, path in results.items():
            print(f"  • {diagram_type}: {path}")
        print("\n💡 Open the PNG files to view your diagrams!\n")
    else:
        print("\n❌ No diagrams were converted.\n")
