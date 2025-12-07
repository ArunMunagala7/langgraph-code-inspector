"""
Simple standalone test for Mermaid flowchart generation
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock minimal data for testing
test_code = '''
def binary_search(arr, target):
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

mock_analysis = {
    "bugs": [],
    "edge_cases": ["Empty array", "Target not in array", "Single element"],
    "complexity": {"time": "O(log n)", "space": "O(1)"},
    "suggestions": ["Add input validation", "Handle empty array case"]
}

mock_explanations = {
    "line_by_line": []
}

print("="*100)
print("🧪 MERMAID FLOWCHART GENERATOR TEST")
print("="*100)

# Test Mermaid generation
from core.mermaid_generator import generate_mermaid_flowchart

print("\n📝 Test Code: Binary Search")
print(test_code)

print("\n🎨 Generating Mermaid flowchart...")
print("-" * 100)

mermaid_code = generate_mermaid_flowchart(test_code, mock_explanations, mock_analysis)

if mermaid_code:
    print("\n✅ SUCCESS! Generated Mermaid code:")
    print("="*100)
    print(mermaid_code)
    print("="*100)
    
    # Save to file
    os.makedirs('temp', exist_ok=True)
    mmd_path = 'temp/test_flowchart.mmd'
    with open(mmd_path, 'w') as f:
        f.write(mermaid_code)
    
    print(f"\n💾 Saved to: {mmd_path}")
    
    print("\n📖 How to view this flowchart:")
    print("   1. Copy the Mermaid code above")
    print("   2. Go to https://mermaid.live")
    print("   3. Paste the code in the editor")
    print("   4. See the rendered flowchart!")
    
    print("\n🔧 Or install mermaid-cli to render PNG:")
    print("   npm install -g @mermaid-js/mermaid-cli")
    print(f"   mmdc -i {mmd_path} -o temp/test_flowchart.png")
    
    # Try to render
    from core.mermaid_generator import render_mermaid_to_png
    png_path = 'temp/test_flowchart.png'
    
    print(f"\n🎨 Attempting to render PNG to: {png_path}")
    success = render_mermaid_to_png(mermaid_code, png_path)
    
    if success and os.path.exists(png_path):
        size = os.path.getsize(png_path)
        print(f"   ✅ PNG generated: {size:,} bytes")
    else:
        print("   ℹ️  PNG preview saved (install mermaid-cli for full rendering)")
    
else:
    print("\n❌ Failed to generate Mermaid code")

print("\n" + "="*100)
