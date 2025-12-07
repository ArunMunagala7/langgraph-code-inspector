"""
Test script to compare Hybrid Mermaid approach vs Original Matplotlib approach
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['OPENAI_API_KEY'] = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')).read().strip().split('=')[1]

from graph.workflow import run_code_inspector
from core.smart_diagram_generator import create_smart_flowchart
from core.mermaid_generator import create_mermaid_flowchart


# Test with a moderately complex function
test_code = '''
def binary_search(arr, target):
    """Binary search algorithm"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
'''

print("="*100)
print("🧪 TESTING HYBRID FLOWCHART GENERATION")
print("="*100)
print("\n📝 Test Code: Binary Search")
print(test_code)
print()

# Run full analysis
print("🚀 Running code analysis...")
print("="*100)
result = run_code_inspector(test_code, 'python')

print("\n✅ Analysis complete!")
print(f"   - Bugs found: {len(result['analysis'].get('bugs', []))}")
print(f"   - Edge cases: {len(result['analysis'].get('edge_cases', []))}")
print(f"   - Suggestions: {len(result['analysis'].get('suggestions', []))}")

# Create output directory
os.makedirs('temp/comparison', exist_ok=True)

print("\n" + "="*100)
print("📊 COMPARISON: Two Flowchart Approaches")
print("="*100)

# Approach 1: Original Matplotlib (current system)
print("\n1️⃣  ORIGINAL APPROACH (Matplotlib + Manual Layout)")
print("-" * 80)
original_path = 'temp/comparison/original_matplotlib.png'
success1 = create_smart_flowchart(
    result['code'],
    result['explanations'],
    result['analysis'],
    original_path
)

if success1:
    size1 = os.path.getsize(original_path)
    print(f"   ✅ Generated: {original_path}")
    print(f"   📊 File size: {size1:,} bytes")
else:
    print("   ❌ Failed to generate")

# Approach 2: Hybrid Mermaid (new system)
print("\n2️⃣  HYBRID APPROACH (LLM → Mermaid Syntax)")
print("-" * 80)
mermaid_path = 'temp/comparison/hybrid_mermaid.png'
success2 = create_mermaid_flowchart(
    result['code'],
    result['explanations'],
    result['analysis'],
    mermaid_path
)

if success2:
    size2 = os.path.getsize(mermaid_path)
    print(f"   ✅ Generated: {mermaid_path}")
    print(f"   📊 File size: {size2:,} bytes")
    
    # Check if Mermaid code was saved
    mmd_path = mermaid_path.replace('.png', '.mmd')
    if os.path.exists(mmd_path):
        print(f"   📝 Mermaid code: {mmd_path}")
        print("\n   Preview of Mermaid syntax:")
        print("   " + "-" * 76)
        with open(mmd_path, 'r') as f:
            lines = f.read().split('\n')
            for line in lines[:15]:
                print(f"   {line}")
            if len(lines) > 15:
                print(f"   ... ({len(lines) - 15} more lines)")
else:
    print("   ❌ Failed to generate")

print("\n" + "="*100)
print("📈 RESULTS SUMMARY")
print("="*100)

if success1 and success2:
    print("\n✅ Both approaches successfully generated flowcharts!")
    print("\n🔍 Comparison:")
    print(f"   • Original (Matplotlib): {size1:,} bytes")
    print(f"   • Hybrid (Mermaid):      {size2:,} bytes")
    
    print("\n💡 Key Differences:")
    print("   Original Approach:")
    print("      + Custom Python control")
    print("      + Works offline")
    print("      - Complex collision detection code")
    print("      - Manual arrow routing")
    print("      - Hard to modify/maintain")
    
    print("\n   Hybrid Approach:")
    print("      + Industry-standard Mermaid syntax")
    print("      + Declarative (easier to debug)")
    print("      + Can render in browsers/GitHub/Notion")
    print("      + Automatic layout optimization")
    print("      - Requires mermaid-cli for PNG (or shows code preview)")
    
    print("\n📂 Compare the outputs in: temp/comparison/")
    print("   - original_matplotlib.png")
    print("   - hybrid_mermaid.png")
    print("   - hybrid_mermaid.mmd (Mermaid source)")

elif success1:
    print("\n⚠️  Only original approach succeeded")
elif success2:
    print("\n⚠️  Only hybrid approach succeeded")
else:
    print("\n❌ Both approaches failed")

print("\n" + "="*100)
print("🎯 RECOMMENDATION")
print("="*100)

if os.path.exists('temp/comparison/hybrid_mermaid.mmd'):
    print("""
The hybrid approach generates clean, industry-standard Mermaid syntax that can be:
1. Rendered by mermaid-cli (install: npm install -g @mermaid-js/mermaid-cli)
2. Embedded in Gradio UI using HTML/JavaScript
3. Viewed in GitHub, Notion, VS Code, and many other tools
4. Easily modified by editing the .mmd file

Next steps:
• Install mermaid-cli for full PNG rendering
• Or integrate Mermaid.js in the Gradio web UI for interactive diagrams
• Or keep both: Mermaid for web, Matplotlib for static exports
""")

print("="*100)
