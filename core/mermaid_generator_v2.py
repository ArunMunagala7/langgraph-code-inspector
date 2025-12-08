"""
Reliable Mermaid Flowchart Generator - Simplified & Robust
Guarantees proper rendering with visible arrows and loop handling
"""
import json
import subprocess
import os
import tempfile
from typing import Dict, Any, Optional
from core.utils import get_llm_response

MERMAID_PROMPT = """You are a flowchart expert. Generate a Mermaid flowchart for this code.

Code:
```
{code}
```

Analysis:
{analysis}

CREATE A CLEAN FLOWCHART:
1. Start node → process steps → decision nodes → end node
2. Show ALL loops with arrow back to loop condition
3. Show ALL recursion with arrow back to start
4. Keep labels SHORT (max 30 chars)
5. Use simple step names: step1, step2, etc.

RETURN ONLY VALID MERMAID CODE (no JSON):

graph TD
    start([Start])
    step1[Initialize]
    step2{{Loop condition?}}
    step3[Process]
    stepEnd([End])
    
    start --> step1
    step1 --> step2
    step2 -->|Yes| step3
    step3 -.->|Loop Back| step2
    step2 -->|No| stepEnd
    
    style start fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style stepEnd fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style step2 fill:#FFD54F,stroke:#F9A825,stroke-width:2px
    style step1 fill:#64B5F6,stroke:#1976D2,stroke-width:2px
    style step3 fill:#64B5F6,stroke:#1976D2,stroke-width:2px
    
    linkStyle default stroke:#1976D2,stroke-width:2.5px;
"""

def generate_mermaid_code(code: str, analysis: dict) -> str:
    """Generate Mermaid flowchart code using LLM."""
    try:
        print("  🤖 Generating Mermaid flowchart...")
        
        prompt = MERMAID_PROMPT.format(
            code=code,
            analysis=json.dumps(analysis, indent=2)
        )
        
        response = get_llm_response(prompt, model="gpt-4o-mini")
        
        # Extract Mermaid code
        if '```' in response:
            import re
            match = re.search(r'```(?:mermaid)?\n(.*?)\n```', response, re.DOTALL)
            if match:
                mermaid_code = match.group(1).strip()
            else:
                mermaid_code = response
        else:
            mermaid_code = response.strip()
        
        # Ensure it starts with "graph"
        if not mermaid_code.startswith('graph'):
            print("  ⚠️  Invalid Mermaid code format")
            return None
        
        return mermaid_code
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def render_to_png(mermaid_code: str, output_path: str) -> bool:
    """Render Mermaid code to PNG. Simple, reliable, no fallbacks."""
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
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def create_flowchart(code: str, analysis: dict, output_path: str) -> bool:
    """Main function: Generate and render flowchart."""
    try:
        print("\n🎨 Generating Mermaid Flowchart...")
        
        # Generate Mermaid code
        mermaid_code = generate_mermaid_code(code, analysis)
        if not mermaid_code:
            print("  ❌ Failed to generate Mermaid code")
            return False
        
        print(f"  📄 Generated {len(mermaid_code.split(chr(10)))} lines of Mermaid")
        
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
