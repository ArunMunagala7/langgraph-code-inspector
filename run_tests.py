"""
Automated Test Runner for Code Analysis System
Runs all test cases and generates comprehensive quality report
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_dataset import TEST_CASES
from graph.workflow import run_code_inspector
from agents.quality_agent import score_code_quality
import json
from datetime import datetime


def analyze_test_case(test_key, test_data):
    """Analyze a single test case and return results."""
    print(f"\n{'='*80}")
    print(f"Analyzing: {test_data['name']}")
    print(f"{'='*80}")
    
    try:
        # Run code inspector
        result = run_code_inspector(
            code=test_data['code'],
            language=test_data['language']
        )
        
        # Calculate quality scores
        quality_scores = score_code_quality(
            test_data['code'],
            test_data['language'],
            result['analysis']
        )
        
        # Extract metrics
        bugs = result['analysis'].get('bugs', [])
        suggestions = result['analysis'].get('suggestions', [])
        edge_cases = result['analysis'].get('edge_cases', [])
        
        return {
            'test_key': test_key,
            'name': test_data['name'],
            'language': test_data['language'],
            'expected_quality': test_data['expected_quality'],
            'expected_bugs': test_data['expected_bugs'],
            'actual_quality': quality_scores['overall']['grade'],
            'actual_score': quality_scores['overall']['score'],
            'bugs_found': len(bugs),
            'suggestions_found': len(suggestions),
            'edge_cases_found': len(edge_cases),
            'quality_scores': quality_scores,
            'bugs': bugs,
            'suggestions': suggestions,
            'flowchart': result.get('flowchart', ''),
            'explanations': result['explanations'],
            'success': True
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'test_key': test_key,
            'name': test_data['name'],
            'success': False,
            'error': str(e)
        }


def run_all_tests(selected_tests=None):
    """Run all test cases or selected ones."""
    results = []
    
    tests_to_run = selected_tests if selected_tests else TEST_CASES.keys()
    
    print(f"\n{'#'*80}")
    print(f"RUNNING {len(tests_to_run)} TEST CASES")
    print(f"{'#'*80}\n")
    
    for test_key in tests_to_run:
        if test_key not in TEST_CASES:
            print(f"⚠️ Test '{test_key}' not found, skipping...")
            continue
        
        result = analyze_test_case(test_key, TEST_CASES[test_key])
        results.append(result)
        
        if result['success']:
            print(f"\n✅ Completed: {result['name']}")
            print(f"   Quality: {result['actual_quality']} ({result['actual_score']}/10)")
            print(f"   Bugs Found: {result['bugs_found']} (Expected: {result['expected_bugs']})")
    
    return results


def generate_report(results):
    """Generate comprehensive test report."""
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    report = f"""
{'='*80}
CODE ANALYSIS SYSTEM - TEST REPORT
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY
-------
Total Tests: {len(results)}
Successful: {len(successful)}
Failed: {len(failed)}
Success Rate: {len(successful)/len(results)*100:.1f}%

"""
    
    if successful:
        report += f"""
DETAILED RESULTS
----------------

"""
        for r in successful:
            accuracy = "✅" if abs(r['bugs_found'] - r['expected_bugs']) <= 2 else "⚠️"
            
            report += f"""
{r['name']}
{'-'*80}
Expected Quality: {r['expected_quality']} | Actual: {r['actual_quality']} ({r['actual_score']}/10)
Expected Bugs: {r['expected_bugs']} | Found: {r['bugs_found']} {accuracy}
Suggestions: {r['suggestions_found']} | Edge Cases: {r['edge_cases_found']}

Quality Breakdown:
  - Readability:      {r['quality_scores']['readability']['score']}/10
  - Maintainability:  {r['quality_scores']['maintainability']['score']}/10
  - Security:         {r['quality_scores']['security']['score']}/10
  - Performance:      {r['quality_scores']['performance']['score']}/10
  - Best Practices:   {r['quality_scores']['best_practices']['score']}/10

"""
            
            if r['bugs']:
                report += "Top Bugs Found:\n"
                for i, bug in enumerate(r['bugs'][:3], 1):
                    bug_text = bug if isinstance(bug, str) else bug.get('description', str(bug))
                    report += f"  {i}. {bug_text[:100]}\n"
                report += "\n"
    
    if failed:
        report += f"""
FAILED TESTS
------------
"""
        for r in failed:
            report += f"❌ {r['name']}: {r.get('error', 'Unknown error')}\n"
    
    report += f"""
{'='*80}
ANALYSIS QUALITY METRICS
{'='*80}

Average Quality Score: {sum(r['actual_score'] for r in successful)/len(successful):.2f}/10
Average Bugs Detected: {sum(r['bugs_found'] for r in successful)/len(successful):.1f}
Average Suggestions: {sum(r['suggestions_found'] for r in successful)/len(successful):.1f}

Test Cases by Quality Grade:
"""
    
    grade_counts = {}
    for r in successful:
        grade = r['actual_quality']
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    
    for grade in sorted(grade_counts.keys(), reverse=True):
        report += f"  {grade}: {'█' * grade_counts[grade]} ({grade_counts[grade]})\n"
    
    report += f"\n{'='*80}\n"
    
    return report


def save_results(results, filename="test_results.json"):
    """Save detailed results to JSON file."""
    # Remove non-serializable parts
    clean_results = []
    for r in results:
        clean_r = r.copy()
        if 'quality_scores' in clean_r:
            clean_r['quality_scores'] = {
                k: v for k, v in clean_r['quality_scores'].items()
                if k in ['overall', 'readability', 'maintainability', 'security', 'performance', 'best_practices']
            }
        clean_results.append(clean_r)
    
    with open(filename, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'results': clean_results
        }, f, indent=2)
    
    print(f"\n💾 Results saved to {filename}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run code analysis tests')
    parser.add_argument('--tests', nargs='+', help='Specific tests to run')
    parser.add_argument('--output', default='test_results.json', help='Output file for results')
    parser.add_argument('--report', default='test_report.txt', help='Report file')
    
    args = parser.parse_args()
    
    # Run tests
    results = run_all_tests(args.tests)
    
    # Generate report
    report = generate_report(results)
    
    # Print report
    print(report)
    
    # Save results
    save_results(results, args.output)
    
    # Save report
    with open(args.report, 'w') as f:
        f.write(report)
    
    print(f"📄 Report saved to {args.report}")
    print("\n✅ All tests completed!")
