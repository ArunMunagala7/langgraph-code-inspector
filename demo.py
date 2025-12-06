#!/usr/bin/env python3
"""
Demo script to showcase all features of the Code Understanding System.
Run this to see the system in action across multiple examples.
"""
import os
import time
from graph.workflow import run_code_inspector
from core.utils import format_code_output


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_example(name: str, code: str, language: str):
    """Run and display analysis for one example."""
    print_section(f"DEMO: {name}")
    print(f"Language: {language}")
    print(f"\nCode:\n{'-' * 40}")
    print(code)
    print('-' * 40)
    
    print("\n⏳ Running analysis...\n")
    
    # Run the workflow
    result = run_code_inspector(code, language)
    
    # Display key highlights
    print("\n✨ KEY HIGHLIGHTS:\n")
    
    if result.get('explanations'):
        print(f"📝 Simple Explanation:")
        print(f"   {result['explanations'].get('simple', 'N/A')}\n")
    
    if result.get('analysis'):
        analysis = result['analysis']
        
        if analysis.get('bugs'):
            print(f"🐛 Bugs Detected: {len(analysis['bugs'])}")
            for bug in analysis['bugs']:
                desc = bug if isinstance(bug, str) else bug.get('description', str(bug))
                print(f"   • {desc}")
            print()
        
        if analysis.get('complexity'):
            print(f"⚡ Complexity:")
            print(f"   • Time: {analysis['complexity'].get('time', 'N/A')}")
            print(f"   • Space: {analysis['complexity'].get('space', 'N/A')}")
            print()
        
        if analysis.get('suggestions'):
            print(f"💡 Suggestions: {len(analysis['suggestions'])}")
            for sugg in analysis['suggestions'][:2]:  # Show first 2
                desc = sugg if isinstance(sugg, str) else sugg.get('description', str(sugg))
                print(f"   • {desc}")
            print()
    
    if result.get('knowledge_graph'):
        kg = result['knowledge_graph']
        print(f"📊 Knowledge Graph: {len(kg.get('nodes', []))} nodes, {len(kg.get('edges', []))} edges\n")
    
    print("\n" + "⏸" * 40)
    input("Press ENTER to continue to next demo...")


def main():
    """Run the complete demo."""
    print("\n" + "🌟" * 40)
    print("  MULTI-AGENT CODE UNDERSTANDING SYSTEM - DEMO")
    print("🌟" * 40)
    
    demos = [
        {
            "name": "Simple Loop (Array Sum)",
            "language": "python",
            "code": """def sum_array(arr):
    total = 0
    for x in arr:
        total += x
    return total"""
        },
        {
            "name": "Recursion with Bug (Fibonacci)",
            "language": "python",
            "code": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)"""
        },
        {
            "name": "Algorithm (Binary Search)",
            "language": "python",
            "code": """def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1"""
        },
        {
            "name": "JavaScript Function",
            "language": "javascript",
            "code": """function factorial(n) {
    if (n === 0 || n === 1) {
        return 1;
    }
    return n * factorial(n - 1);
}"""
        }
    ]
    
    print(f"\n📋 This demo will analyze {len(demos)} code examples.")
    print("   Each example showcases different features of the system.\n")
    
    input("Press ENTER to start the demo...")
    
    for i, demo in enumerate(demos, 1):
        print(f"\n\n{'🔹' * 40}")
        print(f"  DEMO {i} of {len(demos)}")
        print(f"{'🔹' * 40}")
        
        try:
            demo_example(demo['name'], demo['code'], demo['language'])
        except KeyboardInterrupt:
            print("\n\n⚠️  Demo interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error in demo: {e}")
            continue
    
    print("\n\n" + "🎉" * 40)
    print("  DEMO COMPLETE!")
    print("🎉" * 40)
    print("\n✨ Key Takeaways:")
    print("   • Multi-agent workflow processes code systematically")
    print("   • Detects bugs (e.g., Fibonacci negative input issue)")
    print("   • Provides complexity analysis (Big-O notation)")
    print("   • Generates visualizations (flowcharts & call graphs)")
    print("   • Creates multi-level explanations")
    print("   • Builds lightweight JSON knowledge graphs")
    print("\n📁 All results saved in outputs/ directory")
    print("📖 See README.md for more information")
    print("\n🚀 Ready to analyze your own code!")
    print(f"\n   Run: python main.py --file your_code.py")
    print()


if __name__ == "__main__":
    main()
