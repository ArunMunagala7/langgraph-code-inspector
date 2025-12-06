"""
State definition for the LangGraph workflow.
This state is shared across all agents in the system.
"""
from typing import TypedDict, Dict, List, Optional


class CodeInspectorState(TypedDict):
    """
    Shared state object for the multi-agent code understanding system.
    
    Attributes:
        language: Programming language of the code (e.g., 'python', 'javascript')
        code: The raw code snippet to analyze
        parsed_structure: Extracted structural elements (functions, loops, etc.)
        knowledge_graph: JSON-based lightweight knowledge graph
        analysis: Bug detection, complexity analysis, suggestions
        flowchart: Mermaid flowchart representation
        call_graph: Mermaid call graph representation
        explanations: Multi-level explanations (simple, technical, line-by-line)
    """
    language: str
    code: str
    parsed_structure: Optional[Dict]
    knowledge_graph: Optional[Dict]
    analysis: Optional[Dict]
    flowchart: Optional[str]
    call_graph: Optional[str]
    explanations: Optional[Dict]
