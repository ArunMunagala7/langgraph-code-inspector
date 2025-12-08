#!/usr/bin/env python3
"""
Test script to verify Explanation and Analysis enhancements
"""
import json
from graph.workflow import run_code_inspector

# Test code samples
test_cases = {
    "binary_search": """
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
""",
    "two_sum": """
def two_sum(arr, target):
    seen = set()
    for num in arr:
        complement = target - num
        if complement in seen:
            return (complement, num)
        seen.add(num)
    return None
""",
    "bubble_sort": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""
}

def test_code(name, code):
    print(f"\n{'='*80}")
    print(f"🧪 Testing: {name.upper()}")
    print(f"{'='*80}\n")
    
    try:
        print(f"⏳ Analyzing {name}...")
        result = run_code_inspector(code, "python")
        
        # Check Explanations
        explanations = result.get('explanations', {})
        print(f"\n✅ EXPLANATIONS:")
        print(f"   - simple: {len(explanations.get('simple', ''))} chars")
        print(f"   - technical: {len(explanations.get('technical', ''))} chars")
        print(f"   - purpose: {len(explanations.get('purpose', ''))} chars")
        print(f"   - use_case: {len(explanations.get('use_case', ''))} chars")
        print(f"   - key_concepts: {len(explanations.get('key_concepts', []))} items")
        print(f"   - sections: {len(explanations.get('sections', []))} sections")
        print(f"   - data_structures: {len(explanations.get('data_structures', []))} items")
        print(f"   - complexity_insight: {len(str(explanations.get('complexity_insight', {})))} chars")
        print(f"   - learning_points: {len(explanations.get('learning_points', []))} points")
        print(f"   - summary: {len(explanations.get('summary', ''))} chars")
        
        # Show sample content
        if explanations.get('simple'):
            print(f"\n   📝 Sample Simple Explanation:")
            print(f"   {explanations['simple'][:150]}...\n")
        
        # Check Analysis
        analysis = result.get('analysis', {})
        print(f"\n✅ ANALYSIS:")
        print(f"   - bugs: {len(analysis.get('bugs', []))} items")
        print(f"   - edge_cases: {len(analysis.get('edge_cases', []))} items")
        print(f"   - complexity: {len(str(analysis.get('complexity', {})))} chars")
        print(f"   - performance_issues: {len(analysis.get('performance_issues', []))} items")
        print(f"   - security_concerns: {len(analysis.get('security_concerns', []))} items")
        print(f"   - code_quality: {len(str(analysis.get('code_quality', {})))} chars")
        print(f"   - suggestions: {len(analysis.get('suggestions', []))} items")
        print(f"   - anti_patterns: {len(analysis.get('anti_patterns', []))} items")
        print(f"   - test_coverage: {len(str(analysis.get('test_coverage', {})))} chars")
        print(f"   - summary: {len(analysis.get('summary', ''))} chars")
        
        # Show sample content
        if analysis.get('bugs') and isinstance(analysis['bugs'][0], dict):
            print(f"\n   🐛 Sample Bug Detail:")
            bug = analysis['bugs'][0]
            print(f"      Description: {bug.get('description', 'N/A')}")
            print(f"      Severity: {bug.get('severity', 'N/A')}")
            print(f"      When: {bug.get('when_triggered', 'N/A')[:80]}...\n")
        
        if analysis.get('suggestions') and isinstance(analysis['suggestions'][0], dict):
            print(f"\n   💡 Sample Suggestion:")
            sugg = analysis['suggestions'][0]
            print(f"      Priority: {sugg.get('priority', 'N/A')}")
            print(f"      Suggestion: {sugg.get('suggestion', 'N/A')[:100]}...\n")
        
        print(f"✅ {name} test PASSED!\n")
        return True
        
    except Exception as e:
        print(f"❌ {name} test FAILED!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 TESTING ENHANCED EXPLANATION AND ANALYSIS SECTIONS")
    print("="*80)
    
    results = {}
    for name, code in test_cases.items():
        results[name] = test_code(name, code)
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 TEST SUMMARY")
    print(f"{'='*80}\n")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name.upper()}: {'PASS' if status else 'FAIL'}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print(f"{'='*80}\n")
