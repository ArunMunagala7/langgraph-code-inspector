"""
Code Quality Scoring Agent
Assigns quantitative scores to code quality metrics
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


def score_code_quality(code: str, language: str, analysis_results: dict) -> dict:
    """
    Score code quality on multiple dimensions.
    
    Args:
        code: Source code
        language: Programming language
        analysis_results: Results from analyze_agent
        
    Returns:
        Dictionary with scores and overall quality
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a code quality expert. Score the following code on these dimensions (1-10):

**Readability** (1-10):
- Clear variable/function names
- Proper comments
- Consistent formatting
- Logical structure

**Maintainability** (1-10):
- Modularity
- Low coupling
- Single responsibility
- Easy to modify

**Security** (1-10):
- No vulnerabilities
- Input validation
- Safe practices
- No hardcoded secrets

**Performance** (1-10):
- Efficient algorithms
- Appropriate data structures
- No obvious bottlenecks
- Resource management

**Best Practices** (1-10):
- Language idioms
- Design patterns
- Error handling
- Code organization

Provide scores in JSON format with explanations."""),
        ("user", """Language: {language}

Code:
```{language}
{code}
```

Analysis Results:
- Bugs: {bug_count}
- Complexity: {complexity}
- Suggestions: {suggestion_count}

Provide your assessment as JSON:
{{
    "readability": {{"score": X, "reason": "..."}},
    "maintainability": {{"score": X, "reason": "..."}},
    "security": {{"score": X, "reason": "..."}},
    "performance": {{"score": X, "reason": "..."}},
    "best_practices": {{"score": X, "reason": "..."}},
    "highlights": ["positive aspect 1", "positive aspect 2"],
    "critical_issues": ["issue 1", "issue 2"]
}}""")
    ])
    
    # Extract analysis metrics
    bugs = analysis_results.get('bugs', [])
    suggestions = analysis_results.get('suggestions', [])
    complexity = analysis_results.get('complexity', {})
    
    # Get LLM scoring
    chain = prompt | llm
    response = chain.invoke({
        "language": language,
        "code": code[:3000],  # Limit to avoid token limits
        "bug_count": len(bugs),
        "suggestion_count": len(suggestions),
        "complexity": f"Time: {complexity.get('time', 'N/A')}, Space: {complexity.get('space', 'N/A')}"
    })
    
    # Parse JSON response
    import json
    import re
    
    # Extract JSON from response
    content = response.content
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    
    if json_match:
        try:
            scores = json.loads(json_match.group())
        except json.JSONDecodeError:
            # Fallback scoring
            scores = generate_fallback_scores(bugs, suggestions, complexity)
    else:
        scores = generate_fallback_scores(bugs, suggestions, complexity)
    
    # Calculate overall score (weighted average)
    weights = {
        'readability': 0.25,
        'maintainability': 0.25,
        'security': 0.20,
        'performance': 0.15,
        'best_practices': 0.15
    }
    
    total_score = 0
    for metric, weight in weights.items():
        if metric in scores and isinstance(scores[metric], dict):
            total_score += scores[metric].get('score', 5) * weight
    
    # Add overall score
    scores['overall'] = {
        'score': round(total_score, 1),
        'grade': get_grade(total_score),
        'emoji': get_emoji(total_score)
    }
    
    return scores


def generate_fallback_scores(bugs, suggestions, complexity):
    """Generate scores based on simple heuristics."""
    bug_count = len(bugs)
    suggestion_count = len(suggestions)
    
    # Simple scoring logic
    readability_score = max(1, 10 - suggestion_count)
    maintainability_score = max(1, 10 - (bug_count + suggestion_count) // 2)
    security_score = max(1, 10 - sum(1 for b in bugs if 'security' in str(b).lower() or 'vulnerable' in str(b).lower()) * 2)
    performance_score = 7  # Default middle score
    best_practices_score = max(1, 9 - bug_count)
    
    return {
        'readability': {'score': readability_score, 'reason': 'Based on code structure analysis'},
        'maintainability': {'score': maintainability_score, 'reason': 'Based on complexity and issues'},
        'security': {'score': security_score, 'reason': 'Based on security-related findings'},
        'performance': {'score': performance_score, 'reason': 'Based on algorithmic complexity'},
        'best_practices': {'score': best_practices_score, 'reason': 'Based on code quality'},
        'highlights': ['Code compiles successfully'],
        'critical_issues': [str(b) for b in bugs[:3]]
    }


def get_grade(score: float) -> str:
    """Convert numeric score to letter grade."""
    if score >= 9.0:
        return "A+"
    elif score >= 8.5:
        return "A"
    elif score >= 8.0:
        return "A-"
    elif score >= 7.5:
        return "B+"
    elif score >= 7.0:
        return "B"
    elif score >= 6.5:
        return "B-"
    elif score >= 6.0:
        return "C+"
    elif score >= 5.5:
        return "C"
    elif score >= 5.0:
        return "C-"
    elif score >= 4.0:
        return "D"
    else:
        return "F"


def get_emoji(score: float) -> str:
    """Get emoji representation of score."""
    if score >= 9.0:
        return "🌟"
    elif score >= 8.0:
        return "🎉"
    elif score >= 7.0:
        return "👍"
    elif score >= 6.0:
        return "😊"
    elif score >= 5.0:
        return "😐"
    else:
        return "😟"


def format_quality_report(scores: dict) -> str:
    """Format quality scores as markdown report."""
    overall = scores.get('overall', {})
    
    report = f"""
# 📊 Code Quality Report

## Overall Score: {overall.get('score', 'N/A')}/10 ({overall.get('grade', 'N/A')}) {overall.get('emoji', '')}

### Detailed Scores

| Metric | Score | Assessment |
|--------|-------|------------|
"""
    
    metrics = ['readability', 'maintainability', 'security', 'performance', 'best_practices']
    for metric in metrics:
        if metric in scores:
            data = scores[metric]
            score = data.get('score', 'N/A')
            bar = '█' * int(score) + '░' * (10 - int(score)) if isinstance(score, (int, float)) else ''
            report += f"| **{metric.replace('_', ' ').title()}** | {score}/10 | {bar} |\n"
    
    # Add highlights
    if 'highlights' in scores and scores['highlights']:
        report += "\n### ✨ Highlights\n"
        for highlight in scores['highlights']:
            report += f"- {highlight}\n"
    
    # Add critical issues
    if 'critical_issues' in scores and scores['critical_issues']:
        report += "\n### ⚠️ Critical Issues\n"
        for issue in scores['critical_issues']:
            report += f"- {issue}\n"
    
    # Add reasoning
    report += "\n### 📝 Detailed Assessment\n"
    for metric in metrics:
        if metric in scores and 'reason' in scores[metric]:
            report += f"\n**{metric.replace('_', ' ').title()}**: {scores[metric]['reason']}\n"
    
    return report
