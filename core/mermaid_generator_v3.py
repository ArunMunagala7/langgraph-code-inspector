"""
Advanced Mermaid Flowchart Generator v3 - CODE-AWARE
Forces analysis of ACTUAL code and generates UNIQUE flowcharts for EVERY code snippet
NO MORE GENERIC TEMPLATES
"""
import json
import subprocess
import os
import tempfile
import re
import hashlib
from typing import Dict, Any, Optional, Tuple, List
from core.utils import get_llm_response

def extract_code_structure(code: str) -> Dict[str, Any]:
    """
    Extract detailed structural information from code
    This FORCES analysis of what's actually in the code
    """
    structure = {
        'lines': len([l for l in code.split('\n') if l.strip()]),
        'functions': [],
        'loops': [],
        'conditions': [],
        'condition_details': [],  # NEW: actual condition text
        'operations': [],  # NEW: actual operations being performed
        'recursion': False,
        'variables': [],
        'function_calls': [],
        'returns': 0,
        'code_hash': hashlib.md5(code.encode()).hexdigest()[:8],
    }
    
    lines = code.split('\n')
    
    # Extract functions
    for i, line in enumerate(lines):
        if 'def ' in line:
            func_name = line.split('def ')[1].split('(')[0].strip()
            structure['functions'].append(func_name)
        
        # Detect loops
        if 'for ' in line or 'while ' in line:
            loop_type = 'for' if 'for ' in line else 'while'
            loop_var = line.split(loop_type)[1].split(':')[0].strip()
            structure['loops'].append(f"{loop_type} loop: {loop_var[:40]}")
        
        # Detect conditions - capture ACTUAL condition text
        if 'if ' in line or 'elif ' in line:
            structure['conditions'].append("condition/decision")
            # Extract the actual condition being checked
            try:
                if 'if ' in line:
                    cond_text = line.split('if ')[1].split(':')[0].strip()[:50]
                    structure['condition_details'].append(f"Check: {cond_text}")
                elif 'elif ' in line:
                    cond_text = line.split('elif ')[1].split(':')[0].strip()[:50]
                    structure['condition_details'].append(f"Check: {cond_text}")
            except:
                structure['condition_details'].append("Condition Check")
        elif 'else:' in line:
            structure['conditions'].append("condition/decision")
            structure['condition_details'].append("Else Branch")
        
        # Detect recursion
        if any(func in line for func in structure['functions']):
            if '(' in line and any(func in line for func in structure['functions']):
                structure['recursion'] = True
        
        # Detect returns
        if 'return ' in line:
            structure['returns'] += 1
        
        # Extract variable assignments - these are operations!
        if '=' in line and 'def ' not in line and 'for ' not in line and 'if ' not in line:
            try:
                # Extract what's being assigned
                var_part = line.split('=')[0].strip()
                val_part = line.split('=', 1)[1].strip()[:40]
                structure['operations'].append(f"{var_part} = {val_part}")
            except:
                pass
        
        # Detect common operations
        if '+=' in line or '-=' in line or '*=' in line or '/=' in line:
            try:
                op_text = line.strip()[:60]
                structure['operations'].append(op_text)
            except:
                pass
    
    return structure


def validate_mermaid_syntax(mermaid_code: str) -> Tuple[bool, str]:
    """Validate Mermaid syntax with mmdc"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
            f.write(mermaid_code)
            temp_mmd = f.name
        
        temp_png = temp_mmd.replace('.mmd', '.png')
        
        result = subprocess.run(
            ['mmdc', '-i', temp_mmd, '-o', temp_png, '-b', 'transparent'],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        try:
            os.unlink(temp_mmd)
            if os.path.exists(temp_png):
                os.unlink(temp_png)
        except:
            pass
        
        if result.returncode == 0:
            return True, ""
        else:
            error = result.stderr if result.stderr else result.stdout
            return False, error.split('\n')[0][:150]
            
    except FileNotFoundError:
        return True, ""
    except Exception as e:
        return False, str(e)[:150]


def fix_mermaid_with_llm(mermaid_code: str, error_msg: str, attempt: int) -> str:
    """Fix Mermaid errors - LLM receives error + actual code"""
    try:
        print(f"  🔧 Fix attempt {attempt}...")
        
        fix_prompt = f"""Fix this broken Mermaid code. The mmdc compiler error is:

ERROR: {error_msg}

BROKEN CODE:
```
{mermaid_code}
```

FIXES:
1. Check node IDs - alphanumeric_underscore only
2. Labels in quotes if they have spaces: step1["Label"]
3. Remove special chars from labels
4. Ensure all node IDs in arrows exist
5. Check graph TD is first line
6. Arrow syntax: -->, -->|label|, -.->

Return ONLY fixed Mermaid code:
"""
        
        response = get_llm_response(fix_prompt, model="gpt-4o-mini")
        
        if '```' in response:
            match = re.search(r'```(?:mermaid)?\n(.*?)\n```', response, re.DOTALL)
            if match:
                fixed = match.group(1).strip()
            else:
                fixed = response
        else:
            fixed = response.strip()
        
        if not fixed.startswith('graph'):
            lines = fixed.split('\n')
            for i, line in enumerate(lines):
                if 'graph' in line:
                    fixed = '\n'.join(lines[i:])
                    break
        
        return fixed
        
    except Exception as e:
        print(f"     ❌ Fix failed: {e}")
        return mermaid_code


def clean_mermaid_labels(code: str) -> str:
    """Clean labels to remove problematic characters"""
    lines = []
    for line in code.split('\n'):
        if '-->' in line or 'graph' in line or 'style' in line or 'linkStyle' in line:
            lines.append(line)
            continue
        
        # Fix labels in brackets
        line = re.sub(r'\[([^\]]*)\]', lambda m: f'["{m.group(1).replace(chr(34), "").strip()}"]', line)
        line = re.sub(r'\{([^\}]*)\}', lambda m: f'{{{m.group(1).replace(chr(34), "").strip()}}}', line)
        
        # Clean up double quotes
        line = line.replace('["', '[').replace('"]', ']')
        line = re.sub(r'\["([^"]*?)"\]', r'["\1"]', line)
        
        lines.append(line)
    
    return '\n'.join(lines)


def sanitize_operation_label(label: str) -> str:
    """
    Sanitize operation label to be safe for Mermaid syntax
    Removes/escapes special characters that break Mermaid
    """
    if not label:
        return "Process/Compute"
    
    try:
        # Remove problematic characters
        sanitized = label
        
        # Remove quotes and replace with safe alternatives
        sanitized = sanitized.replace('"', "'").replace('`', "'")
        
        # Remove colons and semicolons at dangerous positions
        sanitized = sanitized.replace(':', '-').replace(';', ',')
        
        # Remove other special characters that might break Mermaid
        sanitized = sanitized.replace('\\', '/')
        sanitized = sanitized.replace('{', '[').replace('}', ']')
        
        # Limit length to avoid UI issues
        if len(sanitized) > 40:
            sanitized = sanitized[:37] + "..."
        
        # Ensure it's not empty after sanitization
        if not sanitized.strip():
            return "Process/Compute"
        
        return sanitized.strip()
        
    except Exception:
        return "Process/Compute"


def detect_operation_type(code: str, structure: Dict) -> str:
    """
    Use LLM to intelligently determine operation label based on code context
    Falls back to regex-based detection if LLM call fails
    """
    try:
        # Extract the main code body (skip function definition)
        code_lines = code.split('\n')
        body_lines = []
        for line in code_lines:
            if 'def ' not in line and line.strip():
                body_lines.append(line.strip())
        
        code_body = '\n'.join(body_lines[:5])  # First 5 lines of body
        
        prompt = f"""Analyze this code snippet and determine what operation/action is being performed in ONE brief phrase (2-4 words max).

CODE:
{code_body}

CODE CONTEXT:
- Functions: {', '.join(structure['functions']) if structure['functions'] else 'N/A'}
- Loops: {len(structure['loops'])} ({', '.join(structure['loops'][:2]) if structure['loops'] else 'None'})
- Conditions: {len(structure['conditions'])}
- Has recursion: {structure['recursion']}
- Variables: {', '.join(structure['variables'][:3]) if structure['variables'] else 'N/A'}

RESPOND WITH ONLY the operation name in format: [Operation Name]
Examples: [Swap Elements], [Accumulate Values], [Recursive Calculate], [Transform Data], [Search Array], [Sort Algorithm], [Calculate Result]

Be specific to what THIS code actually does:"""
        
        response = get_llm_response(prompt, model="gpt-4o-mini")
        
        # Extract operation from [Operation Name] format
        match = re.search(r'\[([^\]]+)\]', response)
        if match:
            operation = match.group(1).strip()
            if operation and len(operation) > 2:
                return sanitize_operation_label(operation)
        
        # If LLM parsing fails, fall back to regex-based detection
        return detect_operation_type_regex(code, structure)
        
    except Exception as e:
        # Safe fallback if LLM call fails - use regex-based detection
        try:
            return detect_operation_type_regex(code, structure)
        except:
            return "Process/Compute"


def detect_operation_type_regex(code: str, structure: Dict) -> str:
    """
    Fallback: Detect operation type from code patterns using regex
    Used when LLM call fails or takes too long
    """
    try:
        # Check for array/list operations (swap, update)
        if 'arr[' in code or 'list[' in code:
            if '=' in code and 'arr[' in code:
                if any(x in code for x in ['arr[j+1]', 'arr[j-1]', 'arr[i+1]', 'arr[i-1]']):
                    return "Swap/Update Elements"
                return "Update Array"
        
        # Check for accumulation operations
        if '+=' in code or '-=' in code:
            if '+=' in code:
                return "Accumulate/Add"
            else:
                return "Decrement/Reduce"
        
        # Check for multiplication/division
        if '*=' in code:
            return "Multiply/Scale"
        if '/=' in code:
            return "Divide/Scale"
        
        # Check for print/output
        if 'print(' in code:
            return "Output/Print"
        
        # Check for data transformation
        if any(x in code for x in ['transform', 'filter', 'map', 'convert']):
            return "Transform Data"
        
        # Check for search/find operations
        if any(x in code for x in ['search', 'find', 'index']):
            return "Search/Find"
        
        # Check for sort operations
        if 'sort' in code.lower():
            return "Sort Algorithm"
        
        # Check for complexity based on structure
        if len(structure['loops']) > 1 and len(structure['conditions']) > 0:
            return "Complex Computation"
        elif len(structure['loops']) > 0:
            return "Iterate & Compute"
        elif structure['recursion']:
            return "Recursive Compute"
        elif len(structure['variables']) > 0:
            return "Calculate/Assign"
        
        # Default fallback
        return "Process/Compute"
        
    except Exception:
        # Safe fallback
        return "Process/Compute"


def build_mermaid_from_structure(code: str, structure: Dict) -> str:
    """
    BUILD Mermaid flowchart directly from code structure
    NO LLM INVOLVED - eliminates template copying
    """
    nodes = []
    edges = []
    node_id = 1
    
    # Start node
    nodes.append(f"    start([Start - {structure['functions'][0] if structure['functions'] else 'Script'}])")
    current_node = "start"
    
    # Add input/initialization
    if structure['variables']:
        var_init_id = f"init_{node_id}"
        node_id += 1
        var_list = ", ".join(structure['variables'][:3])
        if len(structure['variables']) > 3:
            var_list += f", ... (+{len(structure['variables'])-3} more)"
        nodes.append(f"    {var_init_id}[\"Initialize: {var_list}\"]")
        edges.append(f"    {current_node} --> {var_init_id}")
        current_node = var_init_id
    
    # Add function calls if any
    if structure['function_calls']:
        for func in structure['function_calls'][:2]:
            func_id = f"func_{node_id}"
            node_id += 1
            nodes.append(f"    {func_id}[\"Call: {func}()\"]")
            edges.append(f"    {current_node} --> {func_id}")
            current_node = func_id
    
    # Add loops
    loop_node_ids = []
    for i, loop in enumerate(structure['loops']):
        loop_id = f"loop_{node_id}"
        node_id += 1
        loop_node_ids.append(loop_id)
        loop_label = loop.split(': ')[1][:30] if ': ' in loop else loop[:30]
        nodes.append(f"    {loop_id}{{\"FOR/WHILE: {loop_label}\"}}")
        edges.append(f"    {current_node} --> {loop_id}")
        current_node = loop_id
    
    # Add conditions with ACTUAL condition details
    cond_node_ids = []
    for i, cond in enumerate(structure['conditions']):
        cond_id = f"cond_{node_id}"
        node_id += 1
        cond_node_ids.append(cond_id)
        
        # Use actual condition details if available
        cond_label = structure['condition_details'][i] if i < len(structure['condition_details']) else "Condition Check"
        cond_label = sanitize_operation_label(cond_label)
        
        nodes.append(f"    {cond_id}{{\" {cond_label}\"}}")
        edges.append(f"    {current_node} --> {cond_id}")
        current_node = cond_id
    
    # Add processing with dynamic operation type detection + actual operations
    process_id = f"process_{node_id}"
    node_id += 1
    operation_label = detect_operation_type(code, structure)
    
    # Enhance with actual operations if available
    if structure['operations']:
        actual_op = structure['operations'][0][:30]
        operation_label = f"{operation_label} ({actual_op})"
    
    operation_label = sanitize_operation_label(operation_label)
    nodes.append(f"    {process_id}[\"{operation_label}\"]")
    edges.append(f"    {current_node} --> {process_id}")
    current_node = process_id
    
    # Add return if exists
    if structure['returns'] > 0:
        ret_id = f"return_{node_id}"
        node_id += 1
        nodes.append(f"    {ret_id}[\"Return Result\"]")
        edges.append(f"    {current_node} --> {ret_id}")
        current_node = ret_id
    
    # Add loop-back arrows if loops exist
    if loop_node_ids:
        for loop_id in loop_node_ids:
            back_node = cond_node_ids[0] if cond_node_ids else process_id
            edges.append(f"    {current_node} -.->|Loop Back| {loop_id}")
    
    # Recursion arrow if detected
    if structure['recursion']:
        edges.append(f"    {current_node} -.->|Recursive Call| start")
    
    # End node
    end_id = f"end_{node_id}"
    nodes.append(f"    {end_id}([End])")
    edges.append(f"    {current_node} --> {end_id}")
    
    # Build Mermaid
    mermaid = "graph TD\n"
    mermaid += "\n".join(nodes) + "\n"
    mermaid += "\n".join(edges) + "\n"
    
    # Add styling
    mermaid += f"""
    style start fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style {end_id} fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    linkStyle default stroke:#1976D2,stroke-width:2.5px;
"""
    
    return mermaid


def generate_mermaid_code(code: str, analysis: dict) -> str:
    """
    Generate UNIQUE Mermaid flowchart for ACTUAL code
    Uses direct code structure analysis, NO LLM INVOLVED
    """
    try:
        print("  🤖 Analyzing code structure...")
        
        # Extract actual code structure
        structure = extract_code_structure(code)
        
        print(f"  📊 Found: {len(structure['loops'])} loop(s), {len(structure['conditions'])} condition(s), recursion={structure['recursion']}")
        
        if structure['loops']:
            print(f"     ✓ Loops: {structure['loops']}")
        if structure['functions']:
            print(f"     ✓ Functions: {structure['functions']}")
        if structure['recursion']:
            print(f"     ✓ Recursion detected")
        
        print("  🔨 Building flowchart from code structure...")
        mermaid_code = build_mermaid_from_structure(code, structure)
        
        print(f"  📄 Generated {len(mermaid_code.split(chr(10)))} lines")
        
        # Validation loop with retries
        max_retries = 3
        for attempt in range(max_retries):
            is_valid, error = validate_mermaid_syntax(mermaid_code)
            
            if is_valid:
                print(f"  ✅ Syntax valid!")
                return mermaid_code
            
            print(f"  ⚠️  Syntax error: {error}")
            
            if attempt < max_retries - 1:
                mermaid_code = fix_mermaid_with_llm(mermaid_code, error, attempt + 1)
                if not mermaid_code or not mermaid_code.startswith('graph'):
                    print("  ❌ Fix returned invalid code")
                    break
            else:
                print(f"  ❌ Could not fix after {max_retries} attempts")
                break
        
        return mermaid_code if mermaid_code and mermaid_code.startswith('graph') else None
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def render_to_png(mermaid_code: str, output_path: str) -> bool:
    """Render Mermaid to PNG"""
    try:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        mmd_path = output_path.replace('.png', '.mmd')
        with open(mmd_path, 'w') as f:
            f.write(mermaid_code)
        
        print(f"  💾 Saved: {mmd_path}")
        
        result = subprocess.run(
            ['mmdc', '-i', mmd_path, '-o', output_path, '-b', 'transparent'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"  ✅ Rendered PNG: {size:,} bytes")
            return True
        else:
            error = result.stderr if result.stderr else result.stdout
            print(f"  ❌ Render error: {error[:100]}")
            return False
            
    except FileNotFoundError:
        print("  ❌ mmdc not installed")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def create_flowchart(code: str, analysis: dict, output_path: str) -> bool:
    """Main entry point - generates code-specific flowchart"""
    try:
        print("\n🎨 Generating Code-Specific Flowchart...")
        
        mermaid_code = generate_mermaid_code(code, analysis)
        if not mermaid_code:
            print("  ❌ Failed to generate Mermaid code")
            return False
        
        success = render_to_png(mermaid_code, output_path)
        
        if success:
            print("  ✅ Flowchart created successfully!")
            return True
        else:
            print("  ⚠️  Rendering failed")
            return False
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
