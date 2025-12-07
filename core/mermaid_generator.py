"""
Hybrid Flowchart Generator: LLM → Mermaid Syntax → Rendered Diagram
Combines AI semantic understanding with industry-standard diagram rendering
"""
import json
import subprocess
import os
from typing import Dict, Any, Optional
from core.utils import get_llm_response


MERMAID_FLOWCHART_PROMPT = """You are a flowchart design expert. Create a SIMPLE, CLEAR flowchart for this code.

Code:
```
{code}
```

Analysis:
{analysis}

STRICT RULES:
1. Maximum 10 steps (keep it simple!)
2. Each label ≤ 40 characters
3. Maximum 2 decision nodes
4. Prefer linear flow over complex branching
5. Use clear, concise labels

Return a JSON object with this structure:
{{
  "steps": [
    {{"id": "start", "type": "start", "label": "Start", "next": "step1"}},
    {{"id": "step1", "type": "process", "label": "Initialize variables", "next": "step2"}},
    {{"id": "step2", "type": "decision", "label": "Valid input?", "yes": "step3", "no": "error"}},
    {{"id": "step3", "type": "process", "label": "Process data", "next": "end"}},
    {{"id": "error", "type": "return", "label": "Return error", "next": "end"}},
    {{"id": "end", "type": "end", "label": "End"}}
  ],
  "main_path": ["start", "step1", "step2", "step3", "end"],
  "error_paths": ["error"]
}}

Step types:
- "start": Entry point
- "end": Exit point  
- "process": Action/computation
- "decision": Yes/No question
- "return": Return statement
- "loop": Loop condition (treat as decision)

IMPORTANT: Keep flowchart simple and readable. Return ONLY valid JSON.
"""


def generate_mermaid_flowchart(code: str, explanations: dict, analysis: dict) -> Optional[str]:
    """
    Generate Mermaid flowchart syntax using LLM.
    
    Args:
        code: Source code
        explanations: Code explanations
        analysis: Code analysis
        
    Returns:
        Mermaid syntax string or None
    """
    try:
        print("  🤖 Generating flowchart description with AI...")
        
        # Format prompt
        prompt = MERMAID_FLOWCHART_PROMPT.format(
            code=code,
            analysis=json.dumps(analysis, indent=2)
        )
        
        # Get LLM response
        response = get_llm_response(prompt, model="gpt-4o-mini")
        
        # Parse JSON
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            print("  ⚠️  Could not parse LLM response")
            return None
            
        description = json.loads(json_match.group())
        steps = description.get('steps', [])
        
        if not steps:
            print("  ⚠️  No steps generated")
            return None
        
        # Validate flowchart quality
        valid, msg = validate_flowchart(description)
        if not valid:
            print(f"  ⚠️  Flowchart validation failed: {msg}")
            # Continue anyway, but warn user
        
        print(f"  ✅ Generated {len(steps)} flowchart steps")
        
        # Convert to Mermaid syntax
        mermaid_code = convert_to_mermaid(description)
        
        return mermaid_code
        
    except Exception as e:
        print(f"  ❌ Error generating Mermaid flowchart: {e}")
        import traceback
        traceback.print_exc()
        return None


def validate_flowchart(description: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate flowchart quality before rendering.
    
    Args:
        description: Flowchart description
        
    Returns:
        (is_valid, error_message)
    """
    steps = description.get('steps', [])
    
    # Rule 1: Not too complex
    if len(steps) > 15:
        return False, f"Too many steps ({len(steps)}), maximum 15"
    
    # Rule 2: Reasonable branching
    decision_nodes = [s for s in steps if s.get('type') in ['decision', 'loop']]
    if len(decision_nodes) > 4:
        return False, f"Too many decisions ({len(decision_nodes)}), maximum 4"
    
    # Rule 3: Labels are readable
    for step in steps:
        label = step.get('label', '')
        if len(label) > 60:
            return False, f"Label too long in {step.get('id')}: {len(label)} chars"
    
    # Rule 4: All steps have valid connections
    step_ids = {s['id'] for s in steps}
    for step in steps:
        next_id = step.get('next')
        yes_id = step.get('yes')
        no_id = step.get('no')
        
        for target in [next_id, yes_id, no_id]:
            if target and target not in step_ids:
                return False, f"Invalid connection: {step['id']} → {target}"
    
    return True, "Valid"


def convert_to_mermaid(description: Dict[str, Any]) -> str:
    """
    Convert flowchart description to Mermaid syntax with validation.
    
    Args:
        description: Flowchart description with steps
        
    Returns:
        Mermaid flowchart code
    """
    steps = description.get('steps', [])
    main_path = set(description.get('main_path', []))
    error_paths = set(description.get('error_paths', []))
    
    # Mermaid reserved keywords to avoid
    RESERVED = {'end', 'class', 'click', 'call', 'style', 'linkStyle', 'classDef', 'direction'}
    
    # Fix reserved keyword IDs
    id_mapping = {}
    for step in steps:
        original_id = step['id']
        if original_id in RESERVED:
            new_id = f'{original_id}Node'
            id_mapping[original_id] = new_id
            step['id'] = new_id
        else:
            id_mapping[original_id] = original_id
    
    # Update references in connections
    for step in steps:
        if 'next' in step and step['next']:
            step['next'] = id_mapping.get(step['next'], step['next'])
        if 'yes' in step and step['yes']:
            step['yes'] = id_mapping.get(step['yes'], step['yes'])
        if 'no' in step and step['no']:
            step['no'] = id_mapping.get(step['no'], step['no'])
    
    # Update path lists
    main_path = {id_mapping.get(sid, sid) for sid in main_path}
    error_paths = {id_mapping.get(sid, sid) for sid in error_paths}
    
    # Start Mermaid graph
    lines = ['graph TD']
    
    # Define node styles based on type and path
    for step in steps:
        step_id = step['id']
        step_type = step.get('type', 'process')
        label = step.get('label', step_id)
        
        # Clean label: remove special characters and excessive punctuation
        # Replace brackets and parentheses with safe alternatives
        label = label.replace('[', ' at ').replace(']', ' ')
        label = label.replace('(', ' - ').replace(')', ' ')
        label = label.replace('"', "'")
        # Remove double question marks (common LLM error)
        label = label.replace('??', '?')
        # Trim whitespace and normalize spaces
        label = ' '.join(label.split())
        label = label.strip()
        
        # Choose shape based on type
        if step_type == 'start':
            node_def = f'{step_id}([{label}])'
        elif step_type == 'end':
            node_def = f'{step_id}([{label}])'
        elif step_type in ['decision', 'loop']:
            # Ensure decision labels end with single ?
            if not label.endswith('?'):
                label += '?'
            node_def = f'{step_id}{{{label}}}'
        elif step_type == 'return':
            node_def = f'{step_id}[{label}]'
        else:  # process
            node_def = f'{step_id}[{label}]'
        
        lines.append(f'    {node_def}')
    
    # Add blank line
    lines.append('')
    
    # Define connections
    for step in steps:
        step_id = step['id']
        step_type = step.get('type', 'process')
        
        if step_type in ['decision', 'loop']:
            # Decision node has yes/no branches
            yes_target = step.get('yes')
            no_target = step.get('no')
            
            if yes_target:
                lines.append(f'    {step_id} -->|Yes| {yes_target}')
            if no_target:
                lines.append(f'    {step_id} -->|No| {no_target}')
        else:
            # Regular connection
            next_target = step.get('next')
            if next_target:
                lines.append(f'    {step_id} --> {next_target}')
    
    # Add blank line
    lines.append('')
    
    # Add styling for different path types
    lines.append('    %% Styling')
    
    # Style main path nodes
    for step in steps:
        step_id = step['id']
        step_type = step.get('type', 'process')
        
        if step_type == 'start':
            lines.append(f'    style {step_id} fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff')
        elif step_type == 'end':
            lines.append(f'    style {step_id} fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff')
        elif step_id in error_paths:
            lines.append(f'    style {step_id} fill:#FFB74D,stroke:#F57C00,stroke-width:2px')
        elif step_id in main_path:
            lines.append(f'    style {step_id} fill:#90CAF9,stroke:#1976D2,stroke-width:2px')
        elif step_type in ['decision', 'loop']:
            lines.append(f'    style {step_id} fill:#FFF59D,stroke:#F57F17,stroke-width:2px')
    
    # Join and ensure no trailing special characters
    mermaid_code = '\n'.join(lines)
    
    # Final cleanup: remove any stray % or other artifacts at the end
    mermaid_code = mermaid_code.rstrip('%').rstrip()
    
    return mermaid_code


def validate_and_fix_mermaid(mermaid_code: str) -> tuple[bool, str, str]:
    """
    Validate Mermaid code by attempting to render it.
    If it fails, use LLM to fix errors.
    
    Args:
        mermaid_code: Original Mermaid syntax
        
    Returns:
        (is_valid, fixed_code, error_message)
    """
    import tempfile
    
    # Try to validate with mermaid-cli
    try:
        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
            f.write(mermaid_code)
            temp_mmd = f.name
        
        temp_png = temp_mmd.replace('.mmd', '.png')
        
        # Try to render
        result = subprocess.run(
            ['mmdc', '-i', temp_mmd, '-o', temp_png, '-b', 'transparent'],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        # Clean up temp files
        try:
            os.unlink(temp_mmd)
            if os.path.exists(temp_png):
                os.unlink(temp_png)
        except:
            pass
        
        if result.returncode == 0:
            return True, mermaid_code, ""
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return False, mermaid_code, error_msg
            error_msg = result.stderr.strip()
            print(f"  ⚠️  Mermaid validation failed: {error_msg[:200]}")
            return False, mermaid_code, error_msg
            
    except FileNotFoundError:
        # mmdc not installed, assume code is valid
        print("  ℹ️  Skipping validation (mmdc not installed)")
        return True, mermaid_code, ""
    except Exception as e:
        print(f"  ⚠️  Validation error: {e}")
        return False, mermaid_code, str(e)


def fix_mermaid_with_llm(mermaid_code: str, error_msg: str) -> str:
    """
    Use LLM to fix Mermaid syntax errors.
    
    Args:
        mermaid_code: Broken Mermaid code
        error_msg: Error message from validator
        
    Returns:
        Fixed Mermaid code
    """
    fix_prompt = f"""You are a Mermaid diagram expert. Fix the syntax errors in this Mermaid flowchart.

BROKEN CODE:
```mermaid
{mermaid_code}
```

ERROR MESSAGE:
{error_msg}

COMMON ISSUES TO FIX:
1. Reserved keywords: 'end', 'class', 'click' (rename to 'endNode', 'classNode', etc.)
2. Double question marks (??) in labels (use single ?)
3. Invalid characters in node IDs or labels
4. Unclosed brackets or parentheses
5. Trailing special characters like %

Return ONLY the fixed Mermaid code, no explanations.
"""
    
    try:
        fixed_code = get_llm_response(fix_prompt, model="gpt-4o-mini")
        
        # Extract code from potential markdown blocks
        import re
        code_match = re.search(r'```(?:mermaid)?\n(.*?)\n```', fixed_code, re.DOTALL)
        if code_match:
            fixed_code = code_match.group(1)
        
        # Clean up
        fixed_code = fixed_code.strip()
        
        return fixed_code
        
    except Exception as e:
        print(f"  ❌ LLM fix failed: {e}")
        return mermaid_code  # Return original if fix fails


def render_mermaid_to_png(mermaid_code: str, output_path: str, max_retries: int = 2) -> bool:
    """
    Render Mermaid code to PNG using mermaid-cli (mmdc) with auto-fix.
    Falls back to saving Mermaid code if mmdc not available.
    
    Args:
        mermaid_code: Mermaid syntax
        output_path: Path to save PNG
        max_retries: Maximum correction attempts
        
    Returns:
        True if successful
    """
    try:
        # Save Mermaid code to temp file
        mmd_path = output_path.replace('.png', '.mmd')
        with open(mmd_path, 'w') as f:
            f.write(mermaid_code)
        print(f"  💾 Saved Mermaid code: {mmd_path}")
        
        # Try to render with mermaid-cli directly
        try:
            result = subprocess.run(
                ['mmdc', '-i', mmd_path, '-o', output_path, '-b', 'transparent'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"  ✅ Rendered PNG with mmdc: {size:,} bytes")
                return True
            else:
                # Rendering failed, try validation and fix
                error_msg = result.stderr if result.stderr else result.stdout
                print(f"  ⚠️  Initial rendering failed, attempting fixes...")
                
                current_code = mermaid_code
                for attempt in range(max_retries):
                    print(f"  🔧 Fix attempt {attempt + 1}/{max_retries}...")
                    current_code = fix_mermaid_with_llm(current_code, error_msg)
                    
                    # Save and try again
                    with open(mmd_path, 'w') as f:
                        f.write(current_code)
                    
                    result = subprocess.run(
                        ['mmdc', '-i', mmd_path, '-o', output_path, '-b', 'transparent'],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0 and os.path.exists(output_path):
                        size = os.path.getsize(output_path)
                        print(f"  ✅ Rendered PNG after fix: {size:,} bytes")
                        return True
                    
                    error_msg = result.stderr if result.stderr else result.stdout
                
                print(f"  ❌ Could not fix errors after {max_retries} attempts")
                        
        except FileNotFoundError:
            print("  ℹ️  mermaid-cli (mmdc) not installed")
            print("  📦 Install with: npm install -g @mermaid-js/mermaid-cli")
            return create_mermaid_preview(mermaid_code, output_path)
            
        except subprocess.TimeoutExpired:
            print("  ⚠️  mmdc rendering timed out")
            return create_mermaid_preview(mermaid_code, output_path)
        
        # If we get here, rendering failed even after fixes
        print("  📝 Creating fallback visualization...")
        return create_mermaid_preview(mermaid_code, output_path)
        
    except Exception as e:
        print(f"  ❌ Error rendering Mermaid: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_mermaid_preview(mermaid_code: str, output_path: str):
    """
    Create a simple preview image showing the Mermaid code.
    This is a fallback when mermaid-cli is not available.
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Mermaid Flowchart', ha='center', fontsize=18, fontweight='bold')
    ax.text(5, 9, '(Install mermaid-cli for full rendering)', ha='center', fontsize=10, style='italic', color='gray')
    
    # Show Mermaid code
    code_lines = mermaid_code.split('\n')
    y_pos = 8.5
    
    for line in code_lines[:30]:  # Show first 30 lines
        ax.text(0.5, y_pos, line, fontfamily='monospace', fontsize=9, va='top')
        y_pos -= 0.25
        if y_pos < 0.5:
            break
    
    if len(code_lines) > 30:
        ax.text(0.5, y_pos, f'... ({len(code_lines) - 30} more lines)', 
                fontsize=9, style='italic', color='gray')
    
    # Info box
    info_box = mpatches.FancyBboxPatch((0.3, 0.1), 9.4, 0.8, 
                                       boxstyle="round,pad=0.1",
                                       edgecolor='#2196F3', 
                                       facecolor='#E3F2FD',
                                       linewidth=2)
    ax.add_patch(info_box)
    ax.text(5, 0.5, '💡 Install mermaid-cli: npm install -g @mermaid-js/mermaid-cli', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return True


def create_mermaid_flowchart(code: str, explanations: dict, analysis: dict, output_path: str) -> bool:
    """
    Main function: Generate and render Mermaid flowchart.
    
    Args:
        code: Source code
        explanations: Code explanations
        analysis: Code analysis
        output_path: Path to save PNG
        
    Returns:
        True if successful
    """
    print("\n🎨 Generating Mermaid flowchart...")
    
    # Generate Mermaid syntax using LLM
    mermaid_code = generate_mermaid_flowchart(code, explanations, analysis)
    
    if not mermaid_code:
        print("  ❌ Failed to generate Mermaid code")
        return False
    
    # Render to PNG
    success = render_mermaid_to_png(mermaid_code, output_path)
    
    if success:
        print("  ✅ Mermaid flowchart complete!")
    
    return success
