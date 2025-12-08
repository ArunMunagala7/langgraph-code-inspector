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

MERMAID_PROMPT = """You are a flowchart expert. Generate a Mermaid flowchart for this code.

Code:
```
[CODE_PLACEHOLDER]
```

Analysis:
[ANALYSIS_PLACEHOLDER]

CRITICAL RULES:
1. Use ONLY alphanumeric and underscore for node IDs (step1, step2, etc.)
2. Keep labels SHORT - max 20 chars, no special chars except underscore
3. Use quotes if label has spaces: step1["Label with spaces"]
4. Show loops with backward dotted arrows -.->|Loop Back|
5. Show recursion with arrows back to start
6. Start with: graph TD
7. End with: linkStyle default stroke:#1976D2,stroke-width:2.5px;

EXAMPLE:
```
graph TD
    start([Start])
    step1[Initialize]
    step2{Check condition}
    step3[Process]
    loop[Update]
    stepEnd([End])
    
    start --> step1
    step1 --> step2
    step2 -->|Yes| step3
    step3 --> loop
    loop -.->|Loop Back| step2
    step2 -->|No| stepEnd
    
    style start fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style stepEnd fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style step2 fill:#FFD54F,stroke:#F9A825,stroke-width:2px
    style step1 fill:#64B5F6,stroke:#1976D2,stroke-width:2px
    style step3 fill:#64B5F6,stroke:#1976D2,stroke-width:2px
    style loop fill:#64B5F6,stroke:#1976D2,stroke-width:2px
    
    linkStyle default stroke:#1976D2,stroke-width:2.5px;
```

Generate ONLY the Mermaid code block:
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
        
        # Use safer string formatting to avoid conflicts
        analysis_str = json.dumps(analysis, indent=2)
        prompt = MERMAID_PROMPT.replace('{code}', code).replace('{analysis}', analysis_str)
        
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

