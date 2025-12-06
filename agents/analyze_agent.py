"""
AnalyzeAgent: Analyzes code for bugs, complexity, and improvements.
"""
from typing import Dict, Any
import json
from core.state import CodeInspectorState
from core.prompts import ANALYZE_PROMPT
from core.utils import get_llm, parse_json_response


def analyze_agent(state: CodeInspectorState) -> Dict[str, Any]:
    """
    Analyze code using the knowledge graph to detect issues and provide insights.
    
    Args:
        state: Current state with 'knowledge_graph'
        
    Returns:
        Updated state with 'analysis'
    """
    print("\n🔬 AnalyzeAgent: Analyzing code quality...")
    
    llm = get_llm()
    
    # Format prompt
    prompt = ANALYZE_PROMPT.format(
        language=state["language"],
        code=state["code"],
        knowledge_graph=json.dumps(state["knowledge_graph"], indent=2)
    )
    
    # Get LLM response
    response = llm.invoke(prompt)
    
    # Parse JSON response
    analysis = parse_json_response(response.content)
    
    print(f"✓ Found {len(analysis.get('bugs', []))} potential bugs, "
          f"{len(analysis.get('edge_cases', []))} edge cases, "
          f"{len(analysis.get('suggestions', []))} suggestions")
    
    return {"analysis": analysis}
