"""
ParseCodeAgent: Extracts structural components from code.
"""
from typing import Dict, Any
from core.state import CodeInspectorState
from core.prompts import PARSE_CODE_PROMPT
from core.utils import get_llm, parse_json_response


def parse_code_agent(state: CodeInspectorState) -> Dict[str, Any]:
    """
    Parse code and extract structural components.
    
    Args:
        state: Current state with 'language' and 'code'
        
    Returns:
        Updated state with 'parsed_structure'
    """
    print("\n🔍 ParseCodeAgent: Extracting code structure...")
    
    llm = get_llm()
    
    # Format prompt with code
    prompt = PARSE_CODE_PROMPT.format(
        language=state["language"],
        code=state["code"]
    )
    
    # Get LLM response
    response = llm.invoke(prompt)
    
    # Parse JSON response
    parsed_structure = parse_json_response(response.content)
    
    print(f"✓ Extracted {len(parsed_structure.get('functions', []))} functions, "
          f"{len(parsed_structure.get('loops', []))} loops, "
          f"{len(parsed_structure.get('conditions', []))} conditions")
    
    return {"parsed_structure": parsed_structure}
