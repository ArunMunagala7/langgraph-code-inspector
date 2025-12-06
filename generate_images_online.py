"""
Online Mermaid to Image Converter (No Installation Required!)
Uses Mermaid.ink API to convert diagrams to images without local dependencies.
"""
import os
import json
import base64
import urllib.request
import urllib.parse
from typing import Optional, Dict
from pathlib import Path
import zlib
import ssl


def encode_mermaid_url(mermaid_code: str) -> str:
    """
    Encode Mermaid diagram for URL using base64.
    
    Args:
        mermaid_code: Mermaid diagram syntax
        
    Returns:
        Encoded URL string
    """
    # Remove extra whitespace
    mermaid_code = mermaid_code.strip()
    
    # Encode to bytes and compress
    encoded = base64.urlsafe_b64encode(
        zlib.compress(mermaid_code.encode('utf-8'), 9)
    ).decode('ascii')
    
    return encoded


def download_mermaid_image(mermaid_code: str, 
                          output_path: str,
                          format: str = "png",
                          theme: str = "default") -> bool:
    """
    Download Mermaid diagram as image using Mermaid.ink API.
    
    Args:
        mermaid_code: Mermaid diagram syntax
        output_path: Path to save the image
        format: Image format (png, svg)
        theme: Mermaid theme (default, dark, forest, neutral)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Encode the diagram
        encoded = encode_mermaid_url(mermaid_code)
        
        # Build URL (using mermaid.ink service)
        url = f"https://mermaid.ink/img/{encoded}?theme={theme}&type={format}"
        
        print(f"  🌐 Downloading from Mermaid.ink...")
        
        # Create SSL context that doesn't verify certificates (for local development)
        ssl_context = ssl._create_unverified_context()
        
        # Download the image
        with urllib.request.urlopen(url, timeout=30, context=ssl_context) as response:
            if response.status == 200:
                image_data = response.read()
                
                # Save to file
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
                print(f"  ✅ Saved: {output_path}")
                return True
            else:
                print(f"  ❌ Error: HTTP {response.status}")
                return False
                
    except urllib.error.URLError as e:
        print(f"  ❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def convert_analysis_to_images_online(analysis_file: str, 
                                     output_dir: str = "outputs/images",
                                     theme: str = "default") -> Dict[str, str]:
    """
    Convert all Mermaid diagrams in an analysis file to images using online API.
    NO INSTALLATION REQUIRED - uses mermaid.ink web service.
    
    Args:
        analysis_file: Path to the analysis JSON file
        output_dir: Directory to save images
        theme: Mermaid theme (default, dark, forest, neutral)
        
    Returns:
        Dictionary with paths to generated images
    """
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
    
    print(f"\n📊 Converting diagrams from: {analysis_file}")
    print("="*80)
    
    # Convert flowchart
    if 'flowchart' in data and data['flowchart']:
        flowchart_path = os.path.join(output_dir, f"{base_name}_flowchart.png")
        print(f"\n🎨 Converting flowchart...")
        if download_mermaid_image(data['flowchart'], flowchart_path, theme=theme):
            results['flowchart'] = flowchart_path
    
    # Convert call graph
    if 'call_graph' in data and data['call_graph']:
        callgraph_path = os.path.join(output_dir, f"{base_name}_callgraph.png")
        print(f"\n🎨 Converting call graph...")
        if download_mermaid_image(data['call_graph'], callgraph_path, theme=theme):
            results['call_graph'] = callgraph_path
    
    return results


if __name__ == "__main__":
    import sys
    import glob
    
    print("\n" + "="*80)
    print("🎨 ONLINE MERMAID TO IMAGE CONVERTER (No Installation!)")
    print("="*80)
    print("\nUsing Mermaid.ink web service - no local dependencies needed!")
    print("Internet connection required.\n")
    
    # Find latest analysis file
    analysis_files = glob.glob("outputs/analysis_*.json")
    if not analysis_files:
        print("❌ No analysis files found in outputs/")
        print("💡 Run: python main.py --sample python_binary_search")
        sys.exit(1)
    
    latest_file = max(analysis_files, key=os.path.getctime)
    
    # Convert to images
    results = convert_analysis_to_images_online(latest_file)
    
    if results:
        print("\n" + "="*80)
        print("✅ CONVERSION COMPLETE!")
        print("="*80)
        for diagram_type, path in results.items():
            print(f"  • {diagram_type}: {path}")
        print("\n💡 Open the PNG files to view your diagrams!")
        print("📂 Location: outputs/images/\n")
    else:
        print("\n❌ No diagrams were converted.\n")
