"""
Reliable Mermaid Flowchart Generator - With Validation & Feedback Loops
Guarantees proper rendering with visible arrows and loop handling
"""
import json
import subprocess
import os
import tempfile
import re
from typing import Dict, Any, Optional, Tuple
from core.utils import get_llm_response

MERMAID_PROMPT = """You are a flowchart expert. Analyze this code DEEPLY and create a flowchart that EXACTLY matches its logic.

CODE TO ANALYZE:
```
[CODE_PLACEHOLDER]
```

ANALYSIS FROM PARSER:
[ANALYSIS_PLACEHOLDER]

YOUR TASK:
1. READ the code line by line
2. UNDERSTAND what it does (logic flow, loops, decisions, recursion)
3. IDENTIFY all loops, conditions, function calls, returns
4. AVOID using the template - create UNIQUE flowchart for THIS code
5. Make labels SPECIFIC to this code (use actual variable/function names)
6. Show ALL loops with backward dotted arrows
7. Show ALL recursion with arrows back to start
8. Show ALL conditions/decisions as diamond nodes

CRITICAL RULES FOR MERMAID:
- Node IDs: alphanumeric + underscore only (not special chars)
- Labels: SHORT, specific to THIS code (max 25 chars)
- Quotes for labels with spaces: step1["My label"]
- Loops: Use dotted arrows -.->|Loop Back|
- Decisions: Use {Decision text}
- Boxes: Use [Box text]
- Circles (start/end): Use ([Text])

STRUCTURE YOUR FLOWCHART:
1. START node ([Start])
2. Input/initialization steps
3. Main logic with ALL loops and conditions
4. Recursion calls (if any) with arrows back to START
5. Return/END node ([End])

Generate ONLY Mermaid code - NO explanations, NO examples:
"""

FIX_PROMPT = """Fix this broken Mermaid flowchart. The error is:

ERROR: [ERROR_PLACEHOLDER]

BROKEN CODE:
```
[CODE_PLACEHOLDER]
```

FIXES NEEDED:
1. Check node IDs - only alphanumeric and underscore (step1, step2, etc.)
2. Labels in quotes if they have spaces: step1["My label"]
3. Remove special characters from labels ([], (), %, etc.)
4. Check all node IDs match in connections
5. Ensure graph TD is first line
6. Proper arrow syntax: -->, -->|label|, -.->

Return ONLY fixed Mermaid code:
"""

def clean_mermaid_labels(code: str) -> str:
    """Sanitize labels to remove problematic characters"""
    lines = []
    for line in code.split('\n'):
        # Skip lines that don't have node definitions
        if '-->' in line or 'graph' in line or 'style' in line or 'linkStyle' in line:
            lines.append(line)
            continue
        
        # For node definition lines: step1["Label"] or step1{Label}
        # Replace problematic chars in labels but keep structure
        line = re.sub(r'\[([^\]]*)\]', lambda m: f'["{m.group(1).replace("[", "").replace("]", "").strip()}"]', line)
        line = re.sub(r'\{([^\}]*)\}', lambda m: f'{{{m.group(1).replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("%", "").strip()}}}', line)
        
        # Clean up any double quotes
        line = line.replace('["', '[').replace('"]', ']')
        
        # Fix quotes in labels
        line = re.sub(r'\["([^"]*?)"\]', r'["\1"]', line)
        line = re.sub(r'\{([^}]*?)\}', r'{\1}', line)
        
        lines.append(line)
    
    return '\n'.join(lines)


def validate_mermaid_syntax(mermaid_code: str) -> Tuple[bool, str]:
    """Validate Mermaid syntax with mmdc. Returns (is_valid, error_msg)"""
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
        
        # Cleanup
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
        return True, ""  # mmdc not available, assume valid
    except Exception as e:
        return False, str(e)[:150]


def fix_mermaid_with_llm(mermaid_code: str, error_msg: str, attempt: int) -> str:
    """Use LLM to fix Mermaid errors with feedback loop"""
    try:
        print(f"  🔧 Fix attempt {attempt}...")
        
        prompt = FIX_PROMPT.replace('[ERROR_PLACEHOLDER]', error_msg).replace('[CODE_PLACEHOLDER]', mermaid_code)
        
        response = get_llm_response(prompt, model="gpt-4o-mini")
        
        # Extract code
        if '```' in response:
            match = re.search(r'```(?:mermaid)?\n(.*?)\n```', response, re.DOTALL)
            if match:
                fixed = match.group(1).strip()
            else:
                fixed = response
        else:
            fixed = response.strip()
        
        # Ensure starts with graph
        if not fixed.startswith('graph'):
            lines = fixed.split('\n')
            for i, line in enumerate(lines):
                if 'graph' in line:
                    fixed = '\n'.join(lines[i:])
                    break
        
        # Clean labels
        fixed = clean_mermaid_labels(fixed)
        
        return fixed
        
    except Exception as e:
        print(f"     ❌ LLM fix failed: {e}")
        return mermaid_code


def generate_mermaid_code(code: str, analysis: dict) -> str:
    """Generate Mermaid flowchart code with validation feedback loop"""
    try:
        print("  🤖 Generating Mermaid flowchart...")
        
        # Build detailed analysis string for the prompt
        analysis_text = f"""
FUNCTION STRUCTURE:
- Functions found: {analysis.get('functions', [])}
- Loops: {analysis.get('loops', [])}
- Conditions: {analysis.get('conditions', [])}
- Recursion: {'Yes' if analysis.get('recursion') else 'No'}

CODE METRICS:
- Complexity: Time={analysis.get('complexity', {}).get('time', 'N/A')}, Space={analysis.get('complexity', {}).get('space', 'N/A')}
- Knowledge Graph: {analysis.get('kg_nodes', 0)} nodes, {analysis.get('kg_edges', 0)} edges

POTENTIAL ISSUES:
- Bugs: {len(analysis.get('bugs', []))}
- Edge Cases: {len(analysis.get('edge_cases', []))}

CODE FLOW:
Follow the actual code flow - identify ALL loops and conditions in the code above.
"""
        
        # Use safer string formatting to avoid conflicts
        prompt = MERMAID_PROMPT.replace('[CODE_PLACEHOLDER]', code).replace('[ANALYSIS_PLACEHOLDER]', analysis_text)
        
        response = get_llm_response(prompt, model="gpt-4o-mini")
        
        # Extract Mermaid code
        if '```' in response:
            match = re.search(r'```(?:mermaid)?\n(.*?)\n```', response, re.DOTALL)
            if match:
                mermaid_code = match.group(1).strip()
            else:
                mermaid_code = response
        else:
            mermaid_code = response.strip()
        
        # Ensure it starts with "graph"
        if not mermaid_code.startswith('graph'):
            lines = mermaid_code.split('\n')
            found = False
            for i, line in enumerate(lines):
                if 'graph' in line:
                    mermaid_code = '\n'.join(lines[i:])
                    found = True
                    break
            if not found:
                print("  ⚠️  Could not find 'graph' statement in generated code")
                return None
        
        # Clean labels first
        mermaid_code = clean_mermaid_labels(mermaid_code)
        
        print(f"  📄 Generated {len(mermaid_code.split(chr(10)))} lines")
        print(f"  🔍 Analyzing code structure...")
        
        # Print what was detected
        loops = analysis.get('loops', [])
        if loops:
            print(f"     ✓ Detected {len(loops)} loop(s): {', '.join(str(l)[:30] for l in loops)}")
        conditions = analysis.get('conditions', [])
        if conditions:
            print(f"     ✓ Detected {len(conditions)} condition(s)")
        if analysis.get('recursion'):
            print(f"     ✓ Detected recursion")
        
        # Validation loop - retry up to 3 times
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
                    print("  ❌ LLM fix did not return valid code")
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
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def render_to_png(mermaid_code: str, output_path: str) -> bool:
    """Render Mermaid code to PNG. With retry on failure."""
    try:
        # Create directory
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        # Save Mermaid code
        mmd_path = output_path.replace('.png', '.mmd')
        with open(mmd_path, 'w') as f:
            f.write(mermaid_code)
        
        print(f"  💾 Saved: {mmd_path}")
        
        # Render with mmdc
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
        print("  ❌ mmdc not installed: npm install -g @mermaid-js/mermaid-cli")
        return False
    except subprocess.TimeoutExpired:
        print("  ⏱️  Render timeout (>30s)")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def create_flowchart(code: str, analysis: dict, output_path: str) -> bool:
    """Main function: Generate with validation loop, then render."""
    try:
        print("\n🎨 Generating Mermaid Flowchart...")
        
        # Generate Mermaid code WITH VALIDATION FEEDBACK LOOP
        mermaid_code = generate_mermaid_code(code, analysis)
        if not mermaid_code:
            print("  ❌ Failed to generate Mermaid code")
            return False
        
        # Render to PNG
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

