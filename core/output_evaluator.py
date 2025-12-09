"""
LLM-as-Judge Output Quality Evaluator
Evaluates the quality of generated analysis outputs
"""
import json
import re
from datetime import datetime
from core.utils import get_llm_response


def evaluate_outputs(code: str, result: dict) -> dict:
    """
    Use LLM to evaluate the quality of generated outputs.
    
    Args:
        code: Original source code
        result: Analysis results from run_code_inspector
        
    Returns:
        Dictionary with evaluation scores and reasoning
    """
    try:
        # Extract outputs for evaluation
        explanations = result.get('explanations', {})
        analysis = result.get('analysis', {})
        
        simple_explanation = explanations.get('simple', 'N/A')[:400]
        technical_explanation = explanations.get('technical', 'N/A')[:400]
        bugs = analysis.get('bugs', [])[:3]
        edge_cases = analysis.get('edge_cases', [])[:3]
        complexity = analysis.get('complexity', {})
        
        evaluation_prompt = f"""You are evaluating the quality of AI-generated code analysis outputs.

INPUT CODE (first 500 chars):
```
{code[:500]}
```

GENERATED OUTPUTS:

1. SIMPLE EXPLANATION:
{simple_explanation}

2. TECHNICAL EXPLANATION:
{technical_explanation}

3. BUGS DETECTED ({len(analysis.get('bugs', []))} total):
{json.dumps(bugs, indent=2)}

4. EDGE CASES ({len(analysis.get('edge_cases', []))} total):
{json.dumps(edge_cases, indent=2)}

5. COMPLEXITY ANALYSIS:
{json.dumps(complexity, indent=2)}

Evaluate each output category on a scale of 0-10. Be critical but fair.

Return ONLY this JSON structure (no other text):
{{
  "explanation_quality": {{
    "score": <0-10>,
    "reasoning": "<brief reason why this score>"
  }},
  "bug_detection_accuracy": {{
    "score": <0-10>,
    "reasoning": "<are these real bugs? are they relevant?>"
  }},
  "edge_case_relevance": {{
    "score": <0-10>,
    "reasoning": "<are these valid edge cases for this code?>"
  }},
  "complexity_correctness": {{
    "score": <0-10>,
    "reasoning": "<is the Big-O notation correct?>"
  }},
  "overall_usefulness": {{
    "score": <0-10>,
    "reasoning": "<would this help a developer understand the code?>"
  }}
}}
"""
        
        response = get_llm_response(evaluation_prompt, model="gpt-4o-mini")
        
        # Parse JSON response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            evaluation = json.loads(json_match.group())
            
            # Calculate average score
            scores = []
            for category, data in evaluation.items():
                if isinstance(data, dict) and 'score' in data:
                    scores.append(data['score'])
            
            avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0
            evaluation['average_score'] = avg_score
            evaluation['total_categories'] = len(scores)
            
            return evaluation
        else:
            return {
                "error": "Could not parse evaluation response",
                "raw_response": response[:200]
            }
            
    except Exception as e:
        return {
            "error": f"Evaluation failed: {str(e)}",
            "average_score": 0.0
        }


def save_evaluation_to_file(code: str, result: dict, evaluation: dict, output_dir: str = "outputs") -> str:
    """
    Save evaluation results to a JSON file.
    
    Args:
        code: Original source code
        result: Analysis results
        evaluation: Evaluation scores
        output_dir: Directory to save file
        
    Returns:
        Path to saved file
    """
    import os
    import hashlib
    
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    code_hash = hashlib.md5(code.encode()).hexdigest()[:8]
    filename = f"evaluation_{timestamp}_{code_hash}.json"
    filepath = os.path.join(output_dir, filename)
    
    evaluation_data = {
        "timestamp": datetime.now().isoformat(),
        "code_snippet": code[:200] + "..." if len(code) > 200 else code,
        "code_length": len(code),
        "language": result.get('language', 'unknown'),
        "evaluation_scores": evaluation,
        "analysis_stats": {
            "bugs_found": len(result.get('analysis', {}).get('bugs', [])),
            "edge_cases": len(result.get('analysis', {}).get('edge_cases', [])),
            "has_flowchart": bool(result.get('flowchart')),
            "has_call_graph": bool(result.get('call_graph')),
            "kg_nodes": len(result.get('knowledge_graph', {}).get('nodes', [])),
            "kg_edges": len(result.get('knowledge_graph', {}).get('edges', []))
        }
    }
    
    with open(filepath, 'w') as f:
        json.dump(evaluation_data, f, indent=2)
    
    print(f"📊 Evaluation saved: {filepath}")
    return filepath


def format_evaluation_for_display(evaluation: dict) -> str:
    """
    Format evaluation results as markdown for display.
    
    Args:
        evaluation: Evaluation dictionary
        
    Returns:
        Formatted markdown string
    """
    if "error" in evaluation:
        return f"# ⚠️ Evaluation Error\n\n{evaluation.get('error', 'Unknown error')}"
    
    avg_score = evaluation.get('average_score', 0.0)
    
    # Determine rating
    if avg_score >= 8:
        rating = "🌟 Excellent"
    elif avg_score >= 6:
        rating = "✅ Good"
    elif avg_score >= 4:
        rating = "⚠️ Fair"
    else:
        rating = "❌ Needs Improvement"
    
    markdown = f"""# 📊 Output Quality Evaluation

## Overall Score: {avg_score}/10 - {rating}

---

"""
    
    categories = [
        ("explanation_quality", "📝 Explanation Quality"),
        ("bug_detection_accuracy", "🐛 Bug Detection Accuracy"),
        ("edge_case_relevance", "⚠️ Edge Case Relevance"),
        ("complexity_correctness", "📊 Complexity Analysis"),
        ("overall_usefulness", "💡 Overall Usefulness")
    ]
    
    for key, title in categories:
        if key in evaluation and isinstance(evaluation[key], dict):
            data = evaluation[key]
            score = data.get('score', 0)
            reasoning = data.get('reasoning', 'N/A')
            
            # Score bar
            filled = "█" * int(score)
            empty = "░" * (10 - int(score))
            
            markdown += f"""### {title}
**Score:** {score}/10 `{filled}{empty}`

**Assessment:** {reasoning}

---

"""
    
    markdown += f"""
### 📈 Summary Statistics
- **Categories Evaluated:** {evaluation.get('total_categories', 0)}
- **Average Score:** {avg_score}/10
- **Evaluation Method:** LLM-as-Judge (GPT-4o-mini)
"""
    
    return markdown
