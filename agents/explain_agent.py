"""
ExplainAgent: Generates multi-level code explanations.
"""
from typing import Dict, Any
import json
from core.state import CodeInspectorState
from core.prompts import EXPLAIN_PROMPT
from core.utils import get_llm, parse_json_response


def explain_agent(state: CodeInspectorState) -> Dict[str, Any]:
    """
    Generate multi-level explanations for the code.
    
    Args:
        state: Current state with 'knowledge_graph' and 'analysis'
        
    Returns:
        Updated state with 'explanations'
    """
    print("\n📝 ExplainAgent: Generating explanations...")
    
    llm = get_llm()
    
    # Format prompt
    prompt = EXPLAIN_PROMPT.format(
        language=state["language"],
        code=state["code"],
        knowledge_graph=json.dumps(state["knowledge_graph"], indent=2),
        analysis=json.dumps(state["analysis"], indent=2)
    )
    
    # Get LLM response
    response = llm.invoke(prompt)
    
    # Parse JSON response
    explanations = parse_json_response(response.content)
    
    print(f"✓ Generated multi-level explanations")
    
    return {"explanations": explanations}
