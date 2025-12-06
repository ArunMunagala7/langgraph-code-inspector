"""
LangGraph workflow definition for the multi-agent code understanding system.

Workflow:
    START → ParseCodeAgent → BuildKGAgent → [AnalyzeAgent, VisualizeAgent] → ExplainAgent → END
"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from core.state import CodeInspectorState
from agents.parse_agent import parse_code_agent
from agents.kg_agent import build_kg_agent
from agents.analyze_agent import analyze_agent
from agents.visualize_agent import visualize_agent
from agents.explain_agent import explain_agent


def create_workflow() -> StateGraph:
    """
    Create and configure the LangGraph workflow.
    
    Returns:
        Compiled StateGraph workflow
    """
    # Initialize the graph with our state schema
    workflow = StateGraph(CodeInspectorState)
    
    # Add all agent nodes
    workflow.add_node("parse", parse_code_agent)
    workflow.add_node("build_kg", build_kg_agent)
    workflow.add_node("analyze", analyze_agent)
    workflow.add_node("visualize", visualize_agent)
    workflow.add_node("explain", explain_agent)
    
    # Define the workflow edges
    # Linear flow: parse → build_kg
    workflow.add_edge("parse", "build_kg")
    
    # After KG is built, we can run analyze and visualize in parallel
    # But LangGraph executes sequentially, so we chain them
    workflow.add_edge("build_kg", "analyze")
    workflow.add_edge("analyze", "visualize")
    
    # Finally, explain uses results from both analyze and visualize
    workflow.add_edge("visualize", "explain")
    
    # End after explanation
    workflow.add_edge("explain", END)
    
    # Set entry point
    workflow.set_entry_point("parse")
    
    # Compile the graph
    return workflow.compile()


def run_code_inspector(code: str, language: str = None) -> Dict[str, Any]:
    """
    Run the complete code inspection workflow.
    
    Args:
        code: Source code to analyze
        language: Programming language (auto-detected if None)
        
    Returns:
        Complete state with all analysis results
    """
    from core.utils import detect_language
    
    # Auto-detect language if not provided
    if language is None:
        language = detect_language(code)
    
    # Initialize state
    initial_state = CodeInspectorState(
        language=language,
        code=code,
        parsed_structure=None,
        knowledge_graph=None,
        analysis=None,
        flowchart=None,
        call_graph=None,
        explanations=None
    )
    
    # Create and run workflow
    print(f"\n🚀 Starting Code Inspector workflow for {language} code...")
    print("=" * 80)
    
    workflow = create_workflow()
    final_state = workflow.invoke(initial_state)
    
    print("\n" + "=" * 80)
    print("✅ Workflow completed successfully!")
    
    return final_state
