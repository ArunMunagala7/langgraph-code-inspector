"""
Graphviz DOT to Image Converter
Uses Graphviz's online API for reliable diagram generation
"""
import os
import json
import urllib.request
import urllib.parse
from typing import Optional, Dict, List
from pathlib import Path
import ssl


def generate_flowchart_dot(code: str, parsed_structure: dict, knowledge_graph: dict) -> str:
    """
    Generate a Graphviz DOT flowchart from code structure.
    
    Args:
        code: Source code
        parsed_structure: Parsed code structure
        knowledge_graph: Knowledge graph
        
    Returns:
        DOT format string
    """
    dot = """digraph Flowchart {
    rankdir=TD;
    node [shape=box, style=rounded, fontname="Arial"];
    edge [fontname="Arial"];
    
    // Start and End
    start [label="Start", shape=ellipse, style=filled, fillcolor=lightgreen];
    end [label="End", shape=ellipse, style=filled, fillcolor=lightcoral];
    
"""
    
    # Build flowchart from knowledge graph
    node_id = 1
    nodes_map = {}
    
    # Add function nodes
    for func in parsed_structure.get('functions', []):
        node_name = f"n{node_id}"
        nodes_map[f"func_{func}"] = node_name
        dot += f'    {node_name} [label="{func}()", shape=box];\n'
        node_id += 1
    
    # Add condition nodes (diamonds)
    for cond in parsed_structure.get('conditions', []):
        node_name = f"n{node_id}"
        # Clean condition text
        cond_text = cond.replace('"', '\\"')[:40]
        nodes_map[f"cond_{cond}"] = node_name
        dot += f'    {node_name} [label="{cond_text}", shape=diamond, style=filled, fillcolor=lightyellow];\n'
        node_id += 1
    
    # Add loop nodes
    for loop in parsed_structure.get('loops', []):
        node_name = f"n{node_id}"
        loop_text = loop.replace('"', '\\"')[:40]
        nodes_map[f"loop_{loop}"] = node_name
        dot += f'    {node_name} [label="{loop_text}", shape=hexagon, style=filled, fillcolor=lightblue];\n'
        node_id += 1
    
    # Add return nodes
    for ret in parsed_structure.get('returns', []):
        node_name = f"n{node_id}"
        ret_text = ret.replace('"', '\\"')[:40]
        nodes_map[f"return_{ret}"] = node_name
        dot += f'    {node_name} [label="{ret_text}", shape=box];\n'
        node_id += 1
    
    # Connect start to first function
    if parsed_structure.get('functions'):
        first_func = parsed_structure['functions'][0]
        if f"func_{first_func}" in nodes_map:
            dot += f'    start -> {nodes_map[f"func_{first_func}"]};\n'
    
    # Add edges from knowledge graph
    dot += "\n    // Control flow\n"
    for edge in knowledge_graph.get('edges', []):
        source = edge.get('source', '')
        target = edge.get('target', '')
        relation = edge.get('relation', '')
        
        # Map source and target to node names
        source_node = None
        target_node = None
        
        for key, val in nodes_map.items():
            if source in key:
                source_node = val
            if target in key:
                target_node = val
        
        if source_node and target_node:
            if relation in ['leads_to', 'contains']:
                dot += f'    {source_node} -> {target_node};\n'
            elif relation == 'returns':
                dot += f'    {source_node} -> {target_node} [label="return"];\n'
    
    # Connect last nodes to end
    if parsed_structure.get('returns'):
        for ret in parsed_structure['returns'][:2]:  # Limit to avoid clutter
            if f"return_{ret}" in nodes_map:
                dot += f'    {nodes_map[f"return_{ret}"]} -> end;\n'
    
    dot += "}\n"
    return dot


def generate_callgraph_dot(code: str, parsed_structure: dict, knowledge_graph: dict) -> str:
    """
    Generate a Graphviz DOT call graph from code structure.
    
    Args:
        code: Source code
        parsed_structure: Parsed code structure
        knowledge_graph: Knowledge graph
        
    Returns:
        DOT format string
    """
    dot = """digraph CallGraph {
    rankdir=LR;
    node [shape=box, style=rounded, fontname="Arial"];
    edge [fontname="Arial"];
    
"""
    
    # Create nodes from knowledge graph
    nodes_added = set()
    
    for node in knowledge_graph.get('nodes', [])[:20]:  # Limit nodes
        node_id = node.get('id', '')
        node_label = node.get('label', node_id)
        node_type = node.get('type', '')
        
        # Clean label
        label = node_label.replace('"', '\\"')[:50]
        
        # Choose shape and color based on type
        if node_type == 'function':
            style = 'shape=box, style=filled, fillcolor=lightblue'
        elif node_type == 'variable':
            style = 'shape=ellipse, style=filled, fillcolor=lightgreen'
        elif node_type == 'condition':
            style = 'shape=diamond, style=filled, fillcolor=lightyellow'
        elif node_type == 'loop':
            style = 'shape=hexagon, style=filled, fillcolor=lightcoral'
        else:
            style = 'shape=box'
        
        # Use safe node ID (replace special chars)
        safe_id = node_id.replace('-', '_').replace(' ', '_')
        dot += f'    {safe_id} [label="{label}", {style}];\n'
        nodes_added.add(node_id)
    
    # Add edges
    dot += "\n    // Relationships\n"
    for edge in knowledge_graph.get('edges', [])[:30]:  # Limit edges
        source = edge.get('source', '')
        target = edge.get('target', '')
        relation = edge.get('relation', '')
        
        if source in nodes_added and target in nodes_added:
            safe_source = source.replace('-', '_').replace(' ', '_')
            safe_target = target.replace('-', '_').replace(' ', '_')
            dot += f'    {safe_source} -> {safe_target} [label="{relation}"];\n'
    
    dot += "}\n"
    return dot


def convert_dot_to_image(dot_code: str, output_path: str, format: str = "png") -> bool:
    """
    Convert DOT code to image using online Graphviz API.
    
    Args:
        dot_code: Graphviz DOT code
        output_path: Path to save image
        format: Output format (png, svg)
        
    Returns:
        True if successful
    """
    try:
        # Use quickchart.io Graphviz API (no auth required)
        url = "https://quickchart.io/graphviz"
        
        data = {
            'graph': dot_code,
            'format': format
        }
        
        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        
        print(f"  🌐 Generating image via Graphviz API...")
        
        # Create SSL context
        ssl_context = ssl._create_unverified_context()
        
        # Make POST request
        req = urllib.request.Request(url, data=encoded_data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
            if response.status == 200:
                image_data = response.read()
                
                # Save to file
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
                print(f"  ✅ Saved: {output_path}")
                return True
            else:
                print(f"  ❌ Error: HTTP {response.status}")
                return False
                
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False


def convert_analysis_to_images_graphviz(analysis_path: str) -> List[str]:
    """
    Convert analysis JSON to diagram images using Graphviz.
    
    Args:
        analysis_path: Path to analysis JSON file
        
    Returns:
        List of generated image paths
    """
    try:
        print(f"\n📊 Converting diagrams from: {analysis_path}")
        print("=" * 80)
        
        # Load analysis
        with open(analysis_path, 'r') as f:
            data = json.load(f)
        
        code = data.get('code', '')
        parsed_structure = data.get('parsed_structure', {})
        knowledge_graph = data.get('knowledge_graph', {})
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(analysis_path), 'images')
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate base filename
        base_name = os.path.splitext(os.path.basename(analysis_path))[0]
        
        generated_images = []
        
        # Generate flowchart
        print("\n🎨 Generating flowchart...")
        flowchart_dot = generate_flowchart_dot(code, parsed_structure, knowledge_graph)
        flowchart_path = os.path.join(output_dir, f"{base_name}_flowchart.png")
        
        if convert_dot_to_image(flowchart_dot, flowchart_path):
            generated_images.append(flowchart_path)
        
        # Generate call graph
        print("\n🎨 Generating call graph...")
        callgraph_dot = generate_callgraph_dot(code, parsed_structure, knowledge_graph)
        callgraph_path = os.path.join(output_dir, f"{base_name}_callgraph.png")
        
        if convert_dot_to_image(callgraph_dot, callgraph_path):
            generated_images.append(callgraph_path)
        
        return generated_images
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    """Test the converter with the most recent analysis file."""
    import glob
    
    # Find most recent analysis
    analyses = glob.glob("outputs/analysis_*.json")
    if analyses:
        latest = max(analyses, key=os.path.getctime)
        print(f"🔍 Found analysis: {latest}\n")
        
        images = convert_analysis_to_images_graphviz(latest)
        
        if images:
            print(f"\n✅ CONVERSION COMPLETE!")
            print(f"Generated {len(images)} images:")
            for img in images:
                print(f"  • {img}")
        else:
            print("\n❌ Conversion failed!")
    else:
        print("❌ No analysis files found in outputs/")
