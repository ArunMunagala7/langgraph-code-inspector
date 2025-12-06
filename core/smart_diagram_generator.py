"""
Smart Diagram Generator using LLM
First generates a flowchart description, then renders it visually
"""
import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Polygon
from typing import Dict, List, Any
from core.utils import get_llm_response


FLOWCHART_DESCRIPTION_PROMPT = """You are a flowchart design expert. Based on the code analysis, create a detailed step-by-step flowchart description.

Code:
```
{code}
```

Line-by-Line Explanation:
{line_by_line}

Analysis:
{analysis}

Create a detailed flowchart description with these components:

1. **Steps**: Each logical step in the code execution
2. **Decisions**: Conditional branches (if/else, loops)
3. **Flow**: How steps connect to each other

Return a JSON object with this structure:
{{
  "steps": [
    {{"id": "step1", "type": "start", "label": "Start", "next": "step2"}},
    {{"id": "step2", "type": "process", "label": "Initialize variables", "next": "step3"}},
    {{"id": "step3", "type": "decision", "label": "Is left <= right?", "yes": "step4", "no": "step10"}},
    {{"id": "step4", "type": "process", "label": "Calculate mid", "next": "step5"}},
    {{"id": "step5", "type": "decision", "label": "Is arr[mid] == target?", "yes": "step6", "no": "step7"}},
    {{"id": "step6", "type": "return", "label": "Return mid", "next": "end"}},
    {{"id": "step7", "type": "decision", "label": "Is arr[mid] < target?", "yes": "step8", "no": "step9"}},
    {{"id": "step8", "type": "process", "label": "Update left = mid + 1", "next": "step3"}},
    {{"id": "step9", "type": "process", "label": "Update right = mid - 1", "next": "step3"}},
    {{"id": "step10", "type": "return", "label": "Return -1", "next": "end"}},
    {{"id": "end", "type": "end", "label": "End"}}
  ]
}}

Step types:
- "start": Entry point (green oval)
- "end": Exit point (red oval)
- "process": Action/computation (blue rectangle)
- "decision": Yes/No question (yellow diamond)
- "return": Return statement (green rectangle)
- "loop": Loop condition (yellow diamond)

For "next", "yes", "no" fields, use the ID of the next step.
Make sure the flow is logical and complete. Return ONLY the JSON object.
"""


def generate_flowchart_description(code: str, explanations: dict, analysis: dict) -> Dict[str, Any]:
    """
    Use LLM to generate a structured flowchart description.
    
    Args:
        code: Source code
        explanations: Code explanations
        analysis: Code analysis
        
    Returns:
        Flowchart description dict
    """
    try:
        # Format line-by-line explanation
        line_by_line = explanations.get('line_by_line', [])
        formatted_lines = "\n".join([
            f"Line {item.get('line', '')}: {item.get('code', '')} - {item.get('explanation', '')}"
            for item in line_by_line
        ])
        
        prompt = FLOWCHART_DESCRIPTION_PROMPT.format(
            code=code,
            line_by_line=formatted_lines,
            analysis=json.dumps(analysis, indent=2)
        )
        
        response = get_llm_response(prompt, model="gpt-4o-mini")
        
        # Parse JSON response
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            description = json.loads(json_match.group())
            return description
        else:
            print("⚠️  Could not parse LLM response, using fallback")
            return {"steps": []}
            
    except Exception as e:
        print(f"Error generating flowchart description: {e}")
        import traceback
        traceback.print_exc()
        return {"steps": []}


def render_flowchart_from_description(description: Dict[str, Any], output_path: str) -> bool:
    """
    Render a flowchart image from the LLM-generated description.
    
    Args:
        description: Flowchart description with steps
        output_path: Path to save image
        
    Returns:
        True if successful
    """
    try:
        steps = description.get('steps', [])
        if not steps:
            print("No steps to render")
            return False
        
        # Build step lookup
        step_map = {s['id']: s for s in steps}
        
        # Calculate positions using improved layout algorithm
        step_positions = {}
        
        # Assign levels based on topological order
        levels = {}  # level -> list of step_ids
        step_levels = {}  # step_id -> level
        
        def assign_levels_bfs():
            """Use BFS to assign levels"""
            from collections import deque
            
            queue = deque([(steps[0]['id'], 0)])
            visited = set()
            
            while queue:
                step_id, level = queue.popleft()
                
                if step_id in visited or step_id not in step_map:
                    continue
                
                visited.add(step_id)
                
                # Update level if not set or if we found a shorter path
                if step_id not in step_levels:
                    step_levels[step_id] = level
                    if level not in levels:
                        levels[level] = []
                    levels[level].append(step_id)
                
                step = step_map[step_id]
                step_type = step.get('type', 'process')
                
                # Add children to queue
                if step_type in ['decision', 'loop']:
                    yes_id = step.get('yes')
                    no_id = step.get('no')
                    
                    if yes_id and yes_id not in visited:
                        queue.append((yes_id, level + 1))
                    if no_id and no_id not in visited:
                        queue.append((no_id, level + 1))
                else:
                    next_id = step.get('next')
                    if next_id and next_id not in visited:
                        # Check if it's a loop back
                        if next_id in visited or (next_id in step_map and next_id in step_levels):
                            continue  # Don't add loop backs
                        queue.append((next_id, level + 1))
        
        assign_levels_bfs()
        
        # Assign horizontal positions with better spacing for branches
        x_positions = {}
        
        for level, step_ids in sorted(levels.items()):
            num_steps = len(step_ids)
            
            if num_steps == 1:
                x_positions[step_ids[0]] = 9
            elif num_steps == 2:
                # For yes/no branches: spread them out more
                parent_x = 9
                # Check if these are decision branches
                for step_id in step_ids:
                    step = step_map[step_id]
                    # Position based on step type or return type
                    if step.get('type') == 'return':
                        x_positions[step_id] = 13  # Right side for returns
                    else:
                        x_positions[step_id] = 5   # Left side for continues
                
                # If not returns, spread evenly
                if all(step_map[sid].get('type') != 'return' for sid in step_ids):
                    x_positions[step_ids[0]] = 5
                    x_positions[step_ids[1]] = 13
            else:
                # Spread multiple items
                spacing = 14 / (num_steps + 1)
                for i, step_id in enumerate(step_ids):
                    x_positions[step_id] = 2 + spacing * (i + 1)
        
        # Calculate Y positions
        y_base = 19.5
        y_spacing = 3.0
        
        for step_id, level in step_levels.items():
            x = x_positions.get(step_id, 9)
            y = y_base - (level * y_spacing)
            step_positions[step_id] = (x, y)
        
        # Determine figure height based on max level
        max_level = max(step_levels.values()) if step_levels else 0
        fig_height = max(22, y_base + (max_level * y_spacing) + 2)
        
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(18, fig_height))
        ax.set_xlim(0, 18)
        ax.set_ylim(0, fig_height)
        ax.axis('off')
        
        # Title
        ax.text(9, fig_height - 1.5, 'AI-Generated Code Flowchart', ha='center', fontsize=20, fontweight='bold')
        
        # Draw all steps
        for step in steps:
            step_id = step['id']
            step_type = step.get('type', 'process')
            label = step.get('label', step_id)
            
            if step_id not in step_positions:
                continue
            
            x, y = step_positions[step_id]
            
            # Draw shape based on type
            if step_type == 'start':
                shape = mpatches.Ellipse((x, y), 2.5, 0.9, 
                                        facecolor='#4CAF50', edgecolor='black', linewidth=2.5)
                ax.add_patch(shape)
                ax.text(x, y, label, ha='center', va='center', fontweight='bold', 
                       fontsize=12, color='white')
            
            elif step_type == 'end':
                shape = mpatches.Ellipse((x, y), 2.5, 0.9, 
                                        facecolor='#F44336', edgecolor='black', linewidth=2.5)
                ax.add_patch(shape)
                ax.text(x, y, label, ha='center', va='center', fontweight='bold', 
                       fontsize=12, color='white')
            
            elif step_type in ['decision', 'loop']:
                diamond = Polygon([
                    (x, y + 0.8), (x - 3.2, y), (x, y - 0.8), (x + 3.2, y)
                ], closed=True, edgecolor='black', facecolor='#FFF59D', linewidth=2.5)
                ax.add_patch(diamond)
                
                # Wrap long text
                wrapped_label = label[:50] + '...' if len(label) > 50 else label
                ax.text(x, y, wrapped_label, ha='center', va='center', 
                       fontweight='bold', fontsize=10)
            
            elif step_type == 'return':
                box = FancyBboxPatch((x - 2.5, y - 0.5), 5, 1, boxstyle="round,pad=0.1",
                                    edgecolor='green', facecolor='#A5D6A7', linewidth=2.5)
                ax.add_patch(box)
                ax.text(x, y, label, ha='center', va='center', fontweight='bold', fontsize=11)
            
            else:  # process
                box = FancyBboxPatch((x - 3, y - 0.45), 6, 0.9, boxstyle="round,pad=0.1",
                                    edgecolor='black', facecolor='#90CAF9', linewidth=2)
                ax.add_patch(box)
                
                wrapped_label = label[:55] + '...' if len(label) > 55 else label
                ax.text(x, y, wrapped_label, ha='center', va='center', fontsize=10)
        
        # Draw arrows with smart routing
        drawn_arrows = set()
        
        for step in steps:
            step_id = step['id']
            step_type = step.get('type', 'process')
            
            if step_id not in step_positions:
                continue
            
            x1, y1 = step_positions[step_id]
            
            if step_type in ['decision', 'loop']:
                yes_id = step.get('yes')
                no_id = step.get('no')
                
                # Yes arrow (typically straight down or loop back)
                if yes_id and yes_id in step_positions:
                    x2, y2 = step_positions[yes_id]
                    arrow_key = f"{step_id}-yes-{yes_id}"
                    
                    if arrow_key not in drawn_arrows:
                        # Check if it's a loop back (going up or same level)
                        if y2 >= y1 - 0.5:
                            # Loop back arrow - route around the left side
                            mid_x = x1 - 5  # Go far left
                            ax.plot([x1, mid_x, mid_x, x2 + 3.2], 
                                   [y1 - 0.8, y1 - 0.8, y2, y2],
                                   color='green', linewidth=2.5, linestyle='dashed')
                            ax.annotate('', xy=(x2 + 3.2, y2), xytext=(x2 + 3.5, y2),
                                       arrowprops=dict(arrowstyle='->', lw=2.5, color='green'))
                            ax.text(mid_x - 0.5, (y1 + y2) / 2, 'Yes', fontsize=10, 
                                   color='green', fontweight='bold', style='italic')
                        else:
                            # Normal down arrow
                            ax.annotate('', xy=(x2, y2 + 0.8), xytext=(x1, y1 - 0.8),
                                       arrowprops=dict(arrowstyle='->', lw=2.5, color='green'))
                            ax.text(x1 - 0.5, (y1 + y2) / 2, 'Yes', fontsize=10, 
                                   color='green', fontweight='bold', style='italic')
                        
                        drawn_arrows.add(arrow_key)
                
                # No arrow (typically to the right or down-right)
                if no_id and no_id in step_positions:
                    x2, y2 = step_positions[no_id]
                    arrow_key = f"{step_id}-no-{no_id}"
                    
                    if arrow_key not in drawn_arrows:
                        # Route to the right side
                        if abs(x2 - x1) > 3:
                            # Wide separation - curved arc
                            ax.annotate('', xy=(x2 - 2.5, y2), xytext=(x1 + 3.2, y1),
                                       arrowprops=dict(arrowstyle='->', lw=2.5, color='red',
                                                     connectionstyle='arc3,rad=0.4'))
                            ax.text((x1 + x2) / 2, y1 + 0.5, 'No', fontsize=10, 
                                   color='red', fontweight='bold', style='italic')
                        else:
                            # Close together - gentle curve
                            ax.annotate('', xy=(x2, y2 + 0.5), xytext=(x1 + 3.2, y1),
                                       arrowprops=dict(arrowstyle='->', lw=2.5, color='red',
                                                     connectionstyle='arc3,rad=0.2'))
                            ax.text(x1 + 2, (y1 + y2) / 2, 'No', fontsize=10, 
                                   color='red', fontweight='bold', style='italic')
                        
                        drawn_arrows.add(arrow_key)
            
            else:
                # Regular next arrow
                next_id = step.get('next')
                if next_id and next_id in step_positions:
                    x2, y2 = step_positions[next_id]
                    arrow_key = f"{step_id}-next-{next_id}"
                    
                    if arrow_key not in drawn_arrows:
                        # Check if it's a loop back (going up)
                        if y2 > y1:
                            # Loop back - route around the right side
                            mid_x = x1 + 6  # Go far right
                            ax.plot([x1, mid_x, mid_x, x2 - 3.2], 
                                   [y1 - 0.5, y1 - 0.5, y2, y2],
                                   color='blue', linewidth=2.5, linestyle='dashed')
                            ax.annotate('', xy=(x2 - 3.2, y2), xytext=(x2 - 3.5, y2),
                                       arrowprops=dict(arrowstyle='->', lw=2.5, color='blue'))
                        else:
                            # Normal forward arrow
                            if abs(x2 - x1) > 2:
                                # Diagonal arrow with gentle curve
                                ax.annotate('', xy=(x2, y2 + 0.5), xytext=(x1, y1 - 0.5),
                                           arrowprops=dict(arrowstyle='->', lw=2.5, color='black',
                                                         connectionstyle='arc3,rad=0.15'))
                            else:
                                # Straight down
                                ax.annotate('', xy=(x2, y2 + 0.5), xytext=(x1, y1 - 0.5),
                                           arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))
                        
                        drawn_arrows.add(arrow_key)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"Error rendering flowchart: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_smart_flowchart(code: str, explanations: dict, analysis: dict, output_path: str) -> bool:
    """
    Create a flowchart using LLM-generated description.
    
    Args:
        code: Source code
        explanations: Code explanations
        analysis: Code analysis
        output_path: Output path
        
    Returns:
        True if successful
    """
    try:
        print("  🤖 Generating flowchart description with AI...")
        description = generate_flowchart_description(code, explanations, analysis)
        
        if not description.get('steps'):
            print("  ❌ Failed to generate description")
            return False
        
        print(f"  ✅ Generated {len(description['steps'])} flowchart steps")
        print("  🎨 Rendering flowchart...")
        
        success = render_flowchart_from_description(description, output_path)
        
        # Also save the description
        desc_path = output_path.replace('.png', '_description.json')
        with open(desc_path, 'w') as f:
            json.dump(description, f, indent=2)
        print(f"  💾 Saved description: {desc_path}")
        
        return success
        
    except Exception as e:
        print(f"Error creating smart flowchart: {e}")
        import traceback
        traceback.print_exc()
        return False
