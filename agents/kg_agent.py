"""
BuildKGAgent: Constructs lightweight JSON knowledge graph from parsed structure.
"""
from typing import Dict, Any
import json
from core.state import CodeInspectorState
from core.prompts import BUILD_KG_PROMPT
from core.utils import get_llm, parse_json_response


def build_kg_agent(state: CodeInspectorState) -> Dict[str, Any]:
    """
    Build a lightweight JSON knowledge graph from parsed code structure.
    
    Args:
        state: Current state with 'parsed_structure'
        
    Returns:
        Updated state with 'knowledge_graph'
    """
    print("\n📊 BuildKGAgent: Constructing knowledge graph...")
    
    llm = get_llm()
    
    # Format prompt
    prompt = BUILD_KG_PROMPT.format(
        language=state["language"],
        code=state["code"],
        parsed_structure=json.dumps(state["parsed_structure"], indent=2)
    )
    
    # Get LLM response
    response = llm.invoke(prompt)
    
    # Parse JSON response
    knowledge_graph = parse_json_response(response.content)
    
    print(f"✓ Built KG with {len(knowledge_graph.get('nodes', []))} nodes, "
          f"{len(knowledge_graph.get('edges', []))} edges")
    
    return {"knowledge_graph": knowledge_graph}
