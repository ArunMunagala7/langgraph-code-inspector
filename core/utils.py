"""
Utility functions for the code inspector system.
"""
import os
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


def get_llm(temperature: float = 0.0, model: str = "gpt-4o-mini") -> ChatOpenAI:
    """
    Initialize and return an OpenAI LLM instance.
    
    Args:
        temperature: Sampling temperature (0.0 for deterministic)
        model: OpenAI model name
        
    Returns:
        ChatOpenAI instance
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key
    )


def get_llm_response(prompt: str, temperature: float = 0.0, model: str = "gpt-4o-mini") -> str:
    """
    Get a response from the LLM for a given prompt.
    
    Args:
        prompt: The prompt to send to the LLM
        temperature: Sampling temperature
        model: Model name
        
    Returns:
        LLM response as string
    """
    llm = get_llm(temperature=temperature, model=model)
    response = llm.invoke(prompt)
    return response.content


def parse_json_response(response: str) -> Dict[str, Any]:
    """
    Parse JSON from LLM response, handling markdown code blocks and Mermaid syntax.
    
    Args:
        response: Raw response string from LLM
        
    Returns:
        Parsed JSON dictionary
    """
    # Remove markdown code blocks if present
    response = response.strip()
    if response.startswith("```"):
        # Extract content between code blocks
        match = re.search(r'```(?:json)?\s*\n(.*?)\n```', response, re.DOTALL)
        if match:
            response = match.group(1)
        else:
            # Remove first and last lines
            lines = response.split('\n')
            response = '\n'.join(lines[1:-1])
    
    try:
        # First attempt: try to parse directly
        data = json.loads(response)
    except json.JSONDecodeError:
        # If that fails, try to fix common issues with Mermaid syntax in JSON
        # Replace single {{ }} with double {{{{ }}}} for proper JSON escaping
        # This regex finds {{text}} patterns and escapes them properly
        fixed_response = re.sub(r'(\{)(\{[^}]+\})(\})', r'\1\1\2\3\3', response)
        try:
            data = json.loads(fixed_response)
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"Original Response: {response[:500]}")
            raise
    
    # Clean up Mermaid diagrams if present
    if 'flowchart' in data and data['flowchart']:
        data['flowchart'] = clean_mermaid_syntax(data['flowchart'])
    if 'call_graph' in data and data['call_graph']:
        data['call_graph'] = clean_mermaid_syntax(data['call_graph'])
        
    return data


def clean_mermaid_syntax(diagram: str) -> str:
    """
    Clean Mermaid diagram syntax by removing markdown wrappers.
    
    Args:
        diagram: Mermaid diagram string
        
    Returns:
        Cleaned diagram string
    """
    if not diagram:
        return diagram
    
    diagram = diagram.strip()
    
    # Remove markdown code block wrappers
    if diagram.startswith("```"):
        lines = diagram.split('\n')
        # Remove first and last lines if they're code block markers
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        diagram = '\n'.join(lines)
    
    # Remove "mermaid" prefix if present at the start
    diagram = diagram.strip()
    if diagram.startswith("mermaid\n"):
        diagram = diagram[8:]  # Remove "mermaid\n"
    elif diagram.startswith("mermaid "):
        diagram = diagram[8:]  # Remove "mermaid "
    
    return diagram.strip()


def save_output(data: Dict[str, Any], filename: str, output_dir: str = "outputs") -> str:
    """
    Save data to a JSON file in the outputs directory.
    
    Args:
        data: Data to save
        filename: Output filename
        output_dir: Output directory path
        
    Returns:
        Path to saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filepath


def format_code_output(state: Dict[str, Any]) -> str:
    """
    Format the complete state into a readable output string.
    
    Args:
        state: Complete state dictionary
        
    Returns:
        Formatted string for console output
    """
    output = []
    output.append("=" * 80)
    output.append("CODE UNDERSTANDING ANALYSIS")
    output.append("=" * 80)
    output.append(f"\nLanguage: {state.get('language', 'Unknown')}")
    output.append(f"\nCode:\n{'-' * 40}")
    output.append(state.get('code', ''))
    output.append('-' * 40)
    
    # Explanations
    if state.get('explanations'):
        exp = state['explanations']
        output.append(f"\n{'=' * 80}")
        output.append("EXPLANATIONS")
        output.append('=' * 80)
        output.append(f"\nSimple: {exp.get('simple', 'N/A')}")
        output.append(f"\nTechnical: {exp.get('technical', 'N/A')}")
        output.append(f"\nSummary: {exp.get('summary', 'N/A')}")
    
    # Analysis
    if state.get('analysis'):
        analysis = state['analysis']
        output.append(f"\n{'=' * 80}")
        output.append("ANALYSIS")
        output.append('=' * 80)
        
        if analysis.get('bugs'):
            output.append("\nPotential Bugs:")
            for bug in analysis['bugs']:
                output.append(f"  • {bug}")
        
        if analysis.get('edge_cases'):
            output.append("\nEdge Cases:")
            for case in analysis['edge_cases']:
                output.append(f"  • {case}")
        
        if analysis.get('complexity'):
            comp = analysis['complexity']
            output.append(f"\nComplexity:")
            output.append(f"  • Time: {comp.get('time', 'N/A')}")
            output.append(f"  • Space: {comp.get('space', 'N/A')}")
        
        if analysis.get('suggestions'):
            output.append("\nSuggestions:")
            for suggestion in analysis['suggestions']:
                output.append(f"  • {suggestion}")
    
    # Flowchart
    if state.get('flowchart'):
        output.append(f"\n{'=' * 80}")
        output.append("FLOWCHART (Mermaid)")
        output.append('=' * 80)
        output.append(f"\n{state['flowchart']}")
    
    # Call Graph
    if state.get('call_graph') and state['call_graph'].strip():
        output.append(f"\n{'=' * 80}")
        output.append("CALL GRAPH (Mermaid)")
        output.append('=' * 80)
        output.append(f"\n{state['call_graph']}")
    
    # Knowledge Graph Summary
    if state.get('knowledge_graph'):
        kg = state['knowledge_graph']
        output.append(f"\n{'=' * 80}")
        output.append("KNOWLEDGE GRAPH SUMMARY")
        output.append('=' * 80)
        output.append(f"\nNodes: {len(kg.get('nodes', []))}")
        output.append(f"Edges: {len(kg.get('edges', []))}")
    
    output.append(f"\n{'=' * 80}\n")
    
    return '\n'.join(output)


def detect_language(code: str) -> str:
    """
    Simple language detection based on code syntax patterns.
    
    Args:
        code: Source code string
        
    Returns:
        Detected language name
    """
    code = code.strip()
    
    # Python indicators
    if re.search(r'\bdef\s+\w+\s*\(', code) or re.search(r'\bimport\s+\w+', code):
        return "python"
    
    # JavaScript indicators
    if re.search(r'\bfunction\s+\w+\s*\(', code) or re.search(r'\bconst\s+\w+\s*=', code) or re.search(r'\blet\s+\w+\s*=', code):
        return "javascript"
    
    # Java indicators
    if re.search(r'\bpublic\s+class\s+\w+', code) or re.search(r'\bpublic\s+static\s+void\s+main', code):
        return "java"
    
    # C/C++ indicators
    if re.search(r'#include\s*<', code) or re.search(r'\bint\s+main\s*\(', code):
        return "c/c++"
    
    return "unknown"


def create_timestamp_filename(prefix: str = "output", extension: str = "json") -> str:
    """
    Create a filename with timestamp.
    
    Args:
        prefix: Filename prefix
        extension: File extension
        
    Returns:
        Filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"
