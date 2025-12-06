#!/usr/bin/env python3
"""
Generate PNG images from Mermaid diagrams in analysis files.
This script converts flowcharts and call graphs to viewable images.
"""
import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.mermaid_converter import (
    check_mermaid_cli_installed,
    install_mermaid_cli_instructions,
    convert_analysis_to_images
)
import glob
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Convert Mermaid diagrams to PNG images",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--file",
        type=str,
        help="Specific analysis JSON file to convert"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert all analysis files in outputs/"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs/images",
        help="Directory to save images (default: outputs/images)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("🎨 MERMAID DIAGRAM TO IMAGE CONVERTER")
    print("="*80 + "\n")
    
    # Check if mermaid-cli is installed
    if not check_mermaid_cli_installed():
        print(install_mermaid_cli_instructions())
        sys.exit(1)
    
    print("✅ Mermaid CLI (mmdc) is installed!\n")
    
    # Determine which files to convert
    files_to_convert = []
    
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ Error: File not found: {args.file}")
            sys.exit(1)
        files_to_convert = [args.file]
    elif args.all:
        files_to_convert = glob.glob("outputs/analysis_*.json")
        if not files_to_convert:
            print("❌ No analysis files found in outputs/")
            sys.exit(1)
    else:
        # Default: convert latest file
        analysis_files = glob.glob("outputs/analysis_*.json")
        if not analysis_files:
            print("❌ No analysis files found in outputs/")
            print("💡 Run: python main.py --sample python_binary_search")
            sys.exit(1)
        files_to_convert = [max(analysis_files, key=os.path.getctime)]
    
    print(f"📁 Converting {len(files_to_convert)} file(s)...\n")
    
    # Convert each file
    all_results = {}
    for file_path in files_to_convert:
        print(f"\n{'='*80}")
        print(f"📄 Processing: {file_path}")
        print('='*80)
        
        results = convert_analysis_to_images(file_path, args.output_dir)
        if results:
            all_results[file_path] = results
    
    # Summary
    print("\n" + "="*80)
    print("✅ CONVERSION COMPLETE!")
    print("="*80)
    
    if all_results:
        for file_path, images in all_results.items():
            print(f"\n{os.path.basename(file_path)}:")
            for diagram_type, image_path in images.items():
                print(f"  ✓ {diagram_type}: {image_path}")
        
        print(f"\n📂 All images saved in: {args.output_dir}/")
        print("💡 Open the PNG files to view your diagrams!\n")
    else:
        print("\n⚠️  No diagrams were converted.\n")


if __name__ == "__main__":
    main()
