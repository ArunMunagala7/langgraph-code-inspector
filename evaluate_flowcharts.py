"""
Flowchart Quality Evaluator
Evaluates the quality of generated flowcharts and mermaid diagrams
"""
import re
from typing import Dict, List


def evaluate_flowchart_quality(flowchart_mermaid: str, code: str, language: str) -> Dict:
    """
    Evaluate flowchart quality based on multiple criteria.
    
    Args:
        flowchart_mermaid: Mermaid flowchart code
        code: Original source code
        language: Programming language
        
    Returns:
        Dictionary with quality metrics and score
    """
    metrics = {
        'has_start_end': False,
        'node_count': 0,
        'edge_count': 0,
        'has_conditionals': False,
        'has_loops': False,
        'proper_syntax': True,
        'coverage_score': 0,
        'readability_score': 0,
        'completeness_score': 0,
        'issues': []
    }
    
    # Check for start/end nodes
    if 'start' in flowchart_mermaid.lower() or 'begin' in flowchart_mermaid.lower():
        metrics['has_start_end'] = True
    if 'end' in flowchart_mermaid.lower() or 'return' in flowchart_mermaid.lower():
        metrics['has_start_end'] = metrics['has_start_end'] and True
    
    # Count nodes and edges
    node_pattern = r'(\w+)\[.*?\]'
    edge_pattern = r'-->'
    metrics['node_count'] = len(re.findall(node_pattern, flowchart_mermaid))
    metrics['edge_count'] = len(re.findall(edge_pattern, flowchart_mermaid))
    
    # Check for conditionals (diamonds)
    if '{' in flowchart_mermaid or 'if' in flowchart_mermaid.lower():
        metrics['has_conditionals'] = True
    
    # Check for loops
    loop_keywords = ['while', 'for', 'loop', 'repeat']
    if any(kw in flowchart_mermaid.lower() for kw in loop_keywords):
        metrics['has_loops'] = True
    
    # Syntax check
    if 'graph' not in flowchart_mermaid.lower() and 'flowchart' not in flowchart_mermaid.lower():
        metrics['proper_syntax'] = False
        metrics['issues'].append("Missing graph/flowchart declaration")
    
    # Coverage score (how much of the code is represented)
    code_functions = len(re.findall(r'def \w+|function \w+|class \w+', code))
    code_conditionals = len(re.findall(r'if |else |elif ', code))
    code_loops = len(re.findall(r'for |while ', code))
    
    expected_nodes = code_functions + code_conditionals + code_loops + 2  # +2 for start/end
    if expected_nodes > 0:
        metrics['coverage_score'] = min(100, (metrics['node_count'] / expected_nodes) * 100)
    else:
        metrics['coverage_score'] = 100 if metrics['node_count'] > 0 else 0
    
    # Readability score (based on structure)
    readability = 100
    if metrics['node_count'] > 20:
        readability -= 20
        metrics['issues'].append("Too many nodes (>20), may be hard to read")
    if metrics['edge_count'] < metrics['node_count'] - 1:
        readability -= 10
        metrics['issues'].append("Disconnected nodes detected")
    if not metrics['has_start_end']:
        readability -= 15
        metrics['issues'].append("Missing start/end nodes")
    
    metrics['readability_score'] = max(0, readability)
    
    # Completeness score
    completeness = 0
    if metrics['has_start_end']:
        completeness += 25
    if metrics['node_count'] >= 3:
        completeness += 25
    if metrics['has_conditionals'] and 'if' in code.lower():
        completeness += 25
    if metrics['has_loops'] and ('for' in code.lower() or 'while' in code.lower()):
        completeness += 25
    
    metrics['completeness_score'] = completeness
    
    # Overall quality score
    metrics['overall_score'] = (
        metrics['coverage_score'] * 0.4 +
        metrics['readability_score'] * 0.3 +
        metrics['completeness_score'] * 0.3
    )
    
    # Grade
    score = metrics['overall_score']
    if score >= 90:
        metrics['grade'] = 'A'
    elif score >= 80:
        metrics['grade'] = 'B'
    elif score >= 70:
        metrics['grade'] = 'C'
    elif score >= 60:
        metrics['grade'] = 'D'
    else:
        metrics['grade'] = 'F'
    
    return metrics


def format_flowchart_report(metrics: Dict) -> str:
    """Format flowchart quality metrics as report."""
    report = f"""
FLOWCHART QUALITY REPORT
{'='*80}

Overall Score: {metrics['overall_score']:.1f}/100 (Grade: {metrics['grade']})

Structure Metrics:
  ✓ Nodes: {metrics['node_count']}
  ✓ Edges: {metrics['edge_count']}
  ✓ Has Start/End: {'Yes' if metrics['has_start_end'] else 'No'}
  ✓ Has Conditionals: {'Yes' if metrics['has_conditionals'] else 'No'}
  ✓ Has Loops: {'Yes' if metrics['has_loops'] else 'No'}

Quality Scores:
  ✓ Coverage: {metrics['coverage_score']:.1f}/100 (How much code is represented)
  ✓ Readability: {metrics['readability_score']:.1f}/100 (Visual clarity)
  ✓ Completeness: {metrics['completeness_score']:.1f}/100 (All elements included)

"""
    
    if metrics['issues']:
        report += "Issues Found:\n"
        for issue in metrics['issues']:
            report += f"  ⚠️  {issue}\n"
    else:
        report += "✅ No issues found!\n"
    
    report += f"\n{'='*80}\n"
    
    return report


def compare_flowcharts(flowchart1: str, flowchart2: str, code: str, language: str):
    """Compare two flowcharts for the same code."""
    metrics1 = evaluate_flowchart_quality(flowchart1, code, language)
    metrics2 = evaluate_flowchart_quality(flowchart2, code, language)
    
    print("\n" + "="*80)
    print("FLOWCHART COMPARISON")
    print("="*80)
    
    print("\nFlowchart 1:")
    print(format_flowchart_report(metrics1))
    
    print("\nFlowchart 2:")
    print(format_flowchart_report(metrics2))
    
    print("\nComparison Summary:")
    print("-"*80)
    
    if metrics1['overall_score'] > metrics2['overall_score']:
        print(f"✅ Flowchart 1 is better ({metrics1['overall_score']:.1f} vs {metrics2['overall_score']:.1f})")
    elif metrics2['overall_score'] > metrics1['overall_score']:
        print(f"✅ Flowchart 2 is better ({metrics2['overall_score']:.1f} vs {metrics1['overall_score']:.1f})")
    else:
        print(f"⚖️  Both flowcharts are equal ({metrics1['overall_score']:.1f})")
    
    print("\nDifferences:")
    if metrics1['node_count'] != metrics2['node_count']:
        print(f"  - Nodes: {metrics1['node_count']} vs {metrics2['node_count']}")
    if metrics1['coverage_score'] != metrics2['coverage_score']:
        print(f"  - Coverage: {metrics1['coverage_score']:.1f} vs {metrics2['coverage_score']:.1f}")
    if metrics1['readability_score'] != metrics2['readability_score']:
        print(f"  - Readability: {metrics1['readability_score']:.1f} vs {metrics2['readability_score']:.1f}")


if __name__ == "__main__":
    # Example usage
    sample_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
"""
    
    sample_flowchart = """
flowchart TD
    Start([Start])
    Input[/Input n/]
    Check{n <= 1?}
    ReturnOne[Return 1]
    Calculate[Calculate n * factorial n-1]
    ReturnResult[Return result]
    End([End])
    
    Start --> Input
    Input --> Check
    Check -->|Yes| ReturnOne
    Check -->|No| Calculate
    ReturnOne --> End
    Calculate --> ReturnResult
    ReturnResult --> End
"""
    
    metrics = evaluate_flowchart_quality(sample_flowchart, sample_code, "python")
    print(format_flowchart_report(metrics))
