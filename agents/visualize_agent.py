"""
VisualizeAgent: Generates Mermaid flowcharts and call graphs.
"""
from typing import Dict, Any
import json
from core.state import CodeInspectorState
from core.prompts import VISUALIZE_PROMPT
from core.utils import get_llm, parse_json_response


def visualize_agent(state: CodeInspectorState) -> Dict[str, Any]:
    """
    Generate Mermaid diagrams (flowchart and call graph).
    
    Args:
        state: Current state with 'parsed_structure' and 'knowledge_graph'
        
    Returns:
        Updated state with 'flowchart' and 'call_graph'
    """
    print("\n📈 VisualizeAgent: Generating diagrams...")
    
    llm = get_llm()
    
    # Format prompt
    prompt = VISUALIZE_PROMPT.format(
        language=state["language"],
        code=state["code"],
        parsed_structure=json.dumps(state["parsed_structure"], indent=2),
        knowledge_graph=json.dumps(state["knowledge_graph"], indent=2)
    )
    
    # Get LLM response
    response = llm.invoke(prompt)
    
    # Parse JSON response
    diagrams = parse_json_response(response.content)
    
    print(f"✓ Generated flowchart and call graph")
    
    return {
        "flowchart": diagrams.get("flowchart", ""),
        "call_graph": diagrams.get("call_graph", "")
    }
