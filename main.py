#!/usr/bin/env python3
"""
Main CLI for the Multi-Agent Code Understanding System.

Usage:
    python main.py                    # Interactive mode with sample selection
    python main.py --code "code"      # Analyze custom code
    python main.py --file path.py     # Analyze code from file
    python main.py --sample name      # Analyze a specific sample
"""
import argparse
import sys
import os
from datetime import datetime
from graph.workflow import run_code_inspector
from core.utils import format_code_output, save_output, create_timestamp_filename
from data.samples import SAMPLES, list_samples


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent Code Understanding System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--code",
        type=str,
        help="Code snippet to analyze (as string)"
    )
    
    parser.add_argument(
        "--file",
        type=str,
        help="Path to code file to analyze"
    )
    
    parser.add_argument(
        "--sample",
        type=str,
        choices=list_samples(),
        help="Name of sample code to analyze"
    )
    
    parser.add_argument(
        "--language",
        type=str,
        help="Programming language (auto-detected if not specified)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: outputs/output_TIMESTAMP.json)"
    )
    
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save output to file"
    )
    
    parser.add_argument(
        "--generate-images",
        action="store_true",
        help="Generate PNG images from Mermaid diagrams (requires mermaid-cli)"
    )
    
    args = parser.parse_args()
    
    # Determine code source
    code = None
    language = args.language
    
    if args.code:
        code = args.code
    elif args.file:
        if not os.path.exists(args.file):
            print(f"❌ Error: File not found: {args.file}")
            sys.exit(1)
        with open(args.file, 'r') as f:
            code = f.read()
    elif args.sample:
        sample = SAMPLES[args.sample]
        code = sample["code"]
        language = language or sample["language"]
    else:
        # Interactive mode
        print("\n" + "=" * 80)
        print("🎯 MULTI-AGENT CODE UNDERSTANDING SYSTEM")
        print("=" * 80)
        print("\nAvailable samples:")
        for i, name in enumerate(list_samples(), 1):
            print(f"  {i}. {name}")
        
        print("\nOptions:")
        print("  - Enter a number to select a sample")
        print("  - Enter 'custom' to paste your own code")
        print("  - Enter 'quit' to exit")
        
        choice = input("\nYour choice: ").strip()
        
        if choice.lower() == 'quit':
            print("Goodbye! 👋")
            sys.exit(0)
        elif choice.lower() == 'custom':
            print("\nPaste your code (press Ctrl+D when done):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            code = '\n'.join(lines)
        else:
            try:
                idx = int(choice) - 1
                sample_name = list_samples()[idx]
                sample = SAMPLES[sample_name]
                code = sample["code"]
                language = language or sample["language"]
                print(f"\n✓ Selected: {sample_name}")
            except (ValueError, IndexError):
                print(f"❌ Error: Invalid selection")
                sys.exit(1)
    
    if not code or not code.strip():
        print("❌ Error: No code provided")
        sys.exit(1)
    
    # Run the workflow
    try:
        final_state = run_code_inspector(code, language)
        
        # Display formatted output
        print("\n" + format_code_output(final_state))
        
        # Save output
        if not args.no_save:
            if args.output:
                output_filename = args.output
            else:
                output_filename = create_timestamp_filename("analysis", "json")
            
            # save_output returns the full path
            output_path = save_output(dict(final_state), output_filename)
            print(f"💾 Output saved to: {output_path}\n")
            
            # Generate images if requested
            if args.generate_images:
                from core.smart_diagram_generator import create_smart_flowchart
                from core.diagram_generator import create_callgraph_image
                
                print("🎨 Generating AI-powered diagrams...")
                
                # Create output directory
                output_dir = os.path.join(os.path.dirname(output_path), 'images')
                os.makedirs(output_dir, exist_ok=True)
                base_name = os.path.splitext(os.path.basename(output_path))[0]
                
                images = []
                
                # Generate smart flowchart
                print("\n🧠 Creating AI-generated flowchart...")
                flowchart_path = os.path.join(output_dir, f"{base_name}_flowchart.png")
                if create_smart_flowchart(
                    final_state['code'],
                    final_state['explanations'],
                    final_state['analysis'],
                    flowchart_path
                ):
                    images.append(flowchart_path)
                
                # Generate call graph
                print("\n📊 Creating call graph...")
                callgraph_path = os.path.join(output_dir, f"{base_name}_callgraph.png")
                if create_callgraph_image(final_state['knowledge_graph'], callgraph_path):
                    print(f"  ✅ Saved: {callgraph_path}")
                    images.append(callgraph_path)
                
                if images:
                    print(f"\n✅ Generated {len(images)} diagram images!")
                    for img in images:
                        print(f"  📸 {img}")
                else:
                    print("⚠️  Image generation failed.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
