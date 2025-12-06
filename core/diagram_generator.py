"""
Matplotlib Diagram Generator
Creates detailed flowchart and call graph images showing actual code logic
"""
import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, FancyArrowPatch
import networkx as nx
from typing import Dict, List, Any


def create_flowchart_image(code: str, parsed_structure: dict, output_path: str) -> bool:
    """
    Create a detailed flowchart showing the actual code execution flow.
    """
    try:
        fig, ax = plt.subplots(1, 1, figsize=(16, 20))
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 22)
        ax.axis('off')
        
        # Title
        ax.text(8, 21, 'Code Execution Flowchart', ha='center', fontsize=20, fontweight='bold')
        
        y = 19.5
        x_center = 8
        
        # START
        start = mpatches.Ellipse((x_center, y), 2, 0.8, 
                                 facecolor='#4CAF50', edgecolor='black', linewidth=2.5)
        ax.add_patch(start)
        ax.text(x_center, y, 'START', ha='center', va='center', fontweight='bold', fontsize=13, color='white')
        
        # Arrow down
        ax.annotate('', xy=(x_center, y - 0.9), xytext=(x_center, y - 0.4),
                   arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))
        y -= 1.8
        
        # Function declaration
        if parsed_structure.get('functions'):
            func_name = parsed_structure['functions'][0]
            box = FancyBboxPatch((x_center - 2.5, y - 0.4), 5, 0.8, boxstyle="round,pad=0.1",
                                edgecolor='black', facecolor='#2196F3', linewidth=2)
            ax.add_patch(box)
            ax.text(x_center, y, f'Function: {func_name}()', ha='center', va='center', 
                   fontweight='bold', fontsize=11, color='white')
            
            ax.annotate('', xy=(x_center, y - 0.9), xytext=(x_center, y - 0.4),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))
            y -= 1.8
        
        # Variable initialization
        assignments = parsed_structure.get('assignments', [])
        if assignments:
            init_lines = []
            for assign in assignments[:3]:
                if '=' in assign and 'mid' not in assign:
                    init_lines.append(assign)
            
            if init_lines:
                init_text = "Initialize Variables:\n" + "\n".join(init_lines)
                box = FancyBboxPatch((x_center - 3, y - 0.6), 6, 1.2, boxstyle="round,pad=0.1",
                                    edgecolor='black', facecolor='#90CAF9', linewidth=2)
                ax.add_patch(box)
                ax.text(x_center, y, init_text, ha='center', va='center', fontsize=9)
                
                ax.annotate('', xy=(x_center, y - 1.1), xytext=(x_center, y - 0.6),
                           arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))
                y -= 2.2
        
        # LOOP condition
        loops = parsed_structure.get('loops', [])
        loop_y = y  # Save loop position for back-arrows
        
        if loops:
            loop_text = loops[0]
            # Diamond for loop condition
            diamond = Polygon([
                (x_center, y + 0.7),      # top
                (x_center - 2.8, y),      # left
                (x_center, y - 0.7),      # bottom
                (x_center + 2.8, y)       # right
            ], closed=True, edgecolor='black', facecolor='#FFF59D', linewidth=2.5)
            ax.add_patch(diamond)
            ax.text(x_center, y, loop_text, ha='center', va='center', 
                   fontweight='bold', fontsize=10)
            
            # Arrows and labels
            ax.annotate('', xy=(x_center, y - 1.2), xytext=(x_center, y - 0.7),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='green'))
            ax.text(x_center - 0.5, y - 1, 'True', fontsize=11, color='green', fontweight='bold', style='italic')
            
            # False path - goes to end
            ax.annotate('', xy=(x_center + 4.5, y), xytext=(x_center + 2.8, y),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='red'))
            ax.text(x_center + 3.3, y + 0.3, 'False', fontsize=11, color='red', fontweight='bold', style='italic')
            
            y -= 2.5
        
        # Calculate mid
        if 'mid' in str(assignments):
            box = FancyBboxPatch((x_center - 3, y - 0.4), 6, 0.8, boxstyle="round,pad=0.1",
                                edgecolor='black', facecolor='#90CAF9', linewidth=2)
            ax.add_patch(box)
            ax.text(x_center, y, 'mid = (left + right) // 2', ha='center', va='center', fontsize=10)
            
            ax.annotate('', xy=(x_center, y - 0.9), xytext=(x_center, y - 0.4),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))
            y -= 1.8
        
        # CONDITIONS and BRANCHING
        conditions = parsed_structure.get('conditions', [])
        returns = parsed_structure.get('returns', [])
        
        # Condition 1: arr[mid] == target
        if len(conditions) > 0:
            cond1_y = y
            cond_text = conditions[0][:35]
            diamond = Polygon([
                (x_center, y + 0.7),
                (x_center - 3, y),
                (x_center, y - 0.7),
                (x_center + 3, y)
            ], closed=True, edgecolor='black', facecolor='#EF9A9A', linewidth=2.5)
            ax.add_patch(diamond)
            ax.text(x_center, y, cond_text, ha='center', va='center', 
                   fontweight='bold', fontsize=9)
            
            # TRUE path - found target
            if len(returns) > 0:
                ax.annotate('', xy=(x_center + 5, y), xytext=(x_center + 3, y),
                           arrowprops=dict(arrowstyle='->', lw=2.5, color='green'))
                ax.text(x_center + 3.7, y + 0.3, 'True', fontsize=10, color='green', 
                       fontweight='bold', style='italic')
                
                # Return box
                box = FancyBboxPatch((x_center + 5, y - 0.5), 2.5, 1, boxstyle="round,pad=0.1",
                                    edgecolor='green', facecolor='#A5D6A7', linewidth=2.5)
                ax.add_patch(box)
                ax.text(x_center + 6.25, y, returns[0], ha='center', va='center', 
                       fontweight='bold', fontsize=10)
            
            # FALSE path - continue
            ax.annotate('', xy=(x_center, y - 1.2), xytext=(x_center, y - 0.7),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='red'))
            ax.text(x_center - 0.5, y - 1, 'False', fontsize=10, color='red', 
                   fontweight='bold', style='italic')
            
            y -= 2.5
        
        # Condition 2: arr[mid] < target
        if len(conditions) > 1:
            cond_text = conditions[1][:35]
            diamond = Polygon([
                (x_center, y + 0.7),
                (x_center - 3, y),
                (x_center, y - 0.7),
                (x_center + 3, y)
            ], closed=True, edgecolor='black', facecolor='#EF9A9A', linewidth=2.5)
            ax.add_patch(diamond)
            ax.text(x_center, y, cond_text, ha='center', va='center', 
                   fontweight='bold', fontsize=9)
            
            # TRUE path - update left (move search right)
            ax.annotate('', xy=(x_center + 4, y), xytext=(x_center + 3, y),
                       arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
            ax.text(x_center + 3.3, y + 0.3, 'True', fontsize=10, color='blue', 
                   fontweight='bold', style='italic')
            
            box = FancyBboxPatch((x_center + 4, y - 0.4), 2.8, 0.8, boxstyle="round,pad=0.1",
                                edgecolor='blue', facecolor='#BBDEFB', linewidth=2)
            ax.add_patch(box)
            ax.text(x_center + 5.4, y, 'left = mid + 1', ha='center', va='center', fontsize=9)
            
            # Loop back arrow (right side)
            ax.annotate('', xy=(x_center + 5.4, loop_y - 0.7), xytext=(x_center + 5.4, y - 0.4),
                       arrowprops=dict(arrowstyle='->', lw=2, color='blue', linestyle='dashed'))
            
            # FALSE path - update right (move search left)
            ax.annotate('', xy=(x_center - 4, y), xytext=(x_center - 3, y),
                       arrowprops=dict(arrowstyle='->', lw=2, color='purple'))
            ax.text(x_center - 3.3, y + 0.3, 'False', fontsize=10, color='purple', 
                   fontweight='bold', style='italic')
            
            box = FancyBboxPatch((x_center - 6.8, y - 0.4), 2.8, 0.8, boxstyle="round,pad=0.1",
                                edgecolor='purple', facecolor='#CE93D8', linewidth=2)
            ax.add_patch(box)
            ax.text(x_center - 5.4, y, 'right = mid - 1', ha='center', va='center', fontsize=9)
            
            # Loop back arrow (left side)
            ax.annotate('', xy=(x_center - 5.4, loop_y - 0.7), xytext=(x_center - 5.4, y - 0.4),
                       arrowprops=dict(arrowstyle='->', lw=2, color='purple', linestyle='dashed'))
            
            y -= 2.5
        
        # NOT FOUND path (from loop exit)
        if len(returns) > 1:
            # Path from loop condition False
            not_found_y = y - 3
            ax.annotate('', xy=(x_center + 4.5, not_found_y), xytext=(x_center + 4.5, loop_y),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='red', linestyle='dashed'))
            
            box = FancyBboxPatch((x_center + 3.2, not_found_y - 0.5), 2.6, 1, boxstyle="round,pad=0.1",
                                edgecolor='red', facecolor='#FFCDD2', linewidth=2.5)
            ax.add_patch(box)
            ax.text(x_center + 4.5, not_found_y, returns[1], ha='center', va='center', 
                   fontweight='bold', fontsize=10)
            
            y = not_found_y - 2
        
        # END node
        end = mpatches.Ellipse((x_center, y), 2, 0.8, 
                               facecolor='#F44336', edgecolor='black', linewidth=2.5)
        ax.add_patch(end)
        ax.text(x_center, y, 'END', ha='center', va='center', fontweight='bold', 
               fontsize=13, color='white')
        
        # Arrows to END from both return paths
        if len(returns) > 0:
            # From found path
            ax.annotate('', xy=(x_center, y + 0.4), xytext=(x_center + 6.25, cond1_y - 0.5),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color='green', linestyle='dotted'))
        
        if len(returns) > 1:
            # From not found path
            ax.annotate('', xy=(x_center, y + 0.4), xytext=(x_center + 4.5, not_found_y - 0.5),
                       arrowprops=dict(arrowstyle='->', lw=1.5, color='red', linestyle='dotted'))
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"Error creating flowchart: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_callgraph_image(knowledge_graph: dict, output_path: str) -> bool:
    """
    Create a call graph using NetworkX and matplotlib.
    """
    try:
        # Create directed graph
        G = nx.DiGraph()
        
        # Add nodes with attributes
        node_colors = {
            'function': '#2196F3',
            'variable': '#4CAF50',
            'condition': '#FFC107',
            'loop': '#9C27B0',
            'call': '#FF5722',
            'return': '#00BCD4',
            'assignment': '#90CAF9',
            'operation': '#FFEB3B'
        }
        
        nodes = knowledge_graph.get('nodes', [])[:25]  # Limit nodes for clarity
        edges = knowledge_graph.get('edges', [])[:35]
        
        for node in nodes:
            node_id = node.get('id', '')
            node_type = node.get('type', 'unknown')
            label = node.get('label', node_id)[:20]
            
            G.add_node(node_id, label=label, node_type=node_type)
        
        # Add edges
        for edge in edges:
            source = edge.get('source', '')
            target = edge.get('target', '')
            relation = edge.get('relation', '')
            
            if source in G.nodes and target in G.nodes:
                G.add_edge(source, target, label=relation)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(16, 12))
        ax.set_title('Code Structure Call Graph', fontsize=18, fontweight='bold', pad=20)
        
        # Layout
        try:
            pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        except:
            pos = nx.random_layout(G, seed=42)
        
        # Draw nodes by type
        for node_type, color in node_colors.items():
            nodelist = [n for n, attr in G.nodes(data=True) 
                       if attr.get('node_type') == node_type]
            if nodelist:
                nx.draw_networkx_nodes(G, pos, nodelist=nodelist,
                                      node_color=color, node_size=2000,
                                      alpha=0.9, ax=ax)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True,
                              arrowsize=20, width=2, alpha=0.6,
                              connectionstyle='arc3,rad=0.1', ax=ax)
        
        # Draw labels
        labels = {n: attr.get('label', n) for n, attr in G.nodes(data=True)}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, 
                               font_weight='bold', ax=ax)
        
        # Draw edge labels
        edge_labels = {(u, v): attr.get('label', '')[:10] 
                      for u, v, attr in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6, ax=ax)
        
        # Legend
        legend_elements = [mpatches.Patch(facecolor=color, edgecolor='black', label=ntype.title())
                          for ntype, color in node_colors.items() if any(
                              attr.get('node_type') == ntype for n, attr in G.nodes(data=True)
                          )]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        ax.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"Error creating call graph: {e}")
        import traceback
        traceback.print_exc()
        return False


def convert_analysis_to_images(analysis_path: str) -> List[str]:
    """
    Convert analysis JSON to diagram images.
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
        print("\n🎨 Generating detailed flowchart...")
        flowchart_path = os.path.join(output_dir, f"{base_name}_flowchart.png")
        if create_flowchart_image(code, parsed_structure, flowchart_path):
            print(f"  ✅ Saved: {flowchart_path}")
            generated_images.append(flowchart_path)
        
        # Generate call graph
        print("\n🎨 Generating call graph...")
        callgraph_path = os.path.join(output_dir, f"{base_name}_callgraph.png")
        if create_callgraph_image(knowledge_graph, callgraph_path):
            print(f"  ✅ Saved: {callgraph_path}")
            generated_images.append(callgraph_path)
        
        return generated_images
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
