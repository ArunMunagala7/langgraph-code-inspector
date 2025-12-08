# 🔧 READY-TO-IMPLEMENT CODE SNIPPETS

## Feature 1: Code Comparison (2.5 hours total)

### Step 1: Create `core/comparison_engine.py`

```python
"""
Code Comparison Engine - Compare two code analyses side-by-side
"""

def compare_analyses(analysis1, analysis2):
    """
    Compare two code analyses and highlight differences.
    
    Args:
        analysis1: First code analysis result
        analysis2: Second code analysis result
    
    Returns:
        Dictionary with comparison metrics
    """
    
    bugs1 = len(analysis1.get('bugs', []))
    bugs2 = len(analysis2.get('bugs', []))
    
    quality1 = analysis1.get('code_quality', {}).get('readability_score', 0)
    quality2 = analysis2.get('code_quality', {}).get('readability_score', 0)
    
    comparison = {
        'bug_reduction': bugs1 - bugs2,
        'bug_percentage_improvement': round((bugs1 - bugs2) / max(bugs1, 1) * 100),
        'quality_improvement': quality2 - quality1,
        'complexity_delta': {
            'time': analysis2.get('complexity', {}).get('time', 'N/A'),
            'vs_previous': analysis1.get('complexity', {}).get('time', 'N/A'),
        },
        'new_suggestions': [
            s for s in analysis2.get('suggestions', [])
            if s not in analysis1.get('suggestions', [])
        ],
        'resolved_issues': [
            s for s in analysis1.get('suggestions', [])
            if s not in analysis2.get('suggestions', [])
        ]
    }
    
    return comparison


def format_comparison_html(comparison, explain1, explain2, analysis1, analysis2):
    """
    Format comparison results as HTML for Gradio output.
    """
    
    bug_delta = comparison['bug_reduction']
    bug_color = "🟢" if bug_delta > 0 else "🔴" if bug_delta < 0 else "⚪"
    
    quality_delta = comparison['quality_improvement']
    quality_color = "🟢" if quality_delta > 0 else "🔴" if quality_delta < 0 else "⚪"
    
    html = f"""
    <div style="font-family: Arial; padding: 20px; background: #f5f5f5; border-radius: 8px;">
        <h2>📊 Code Comparison Results</h2>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
            
            <!-- Left Column: Code 1 -->
            <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #ff6b6b;">
                <h3>Code A</h3>
                <p><strong>Bugs Found:</strong> {len(analysis1.get('bugs', []))}</p>
                <p><strong>Quality Score:</strong> {analysis1.get('code_quality', {}).get('readability_score', 'N/A')}/10</p>
            </div>
            
            <!-- Right Column: Code 2 -->
            <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #51cf66;">
                <h3>Code B</h3>
                <p><strong>Bugs Found:</strong> {len(analysis2.get('bugs', []))}</p>
                <p><strong>Quality Score:</strong> {analysis2.get('code_quality', {}).get('readability_score', 'N/A')}/10</p>
            </div>
            
        </div>
        
        <div style="background: white; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h3>📈 Improvements</h3>
            <p style="font-size: 18px;">
                {bug_color} <strong>Bugs Reduced:</strong> {bug_delta} 
                ({comparison['bug_percentage_improvement']}% improvement)
            </p>
            <p style="font-size: 18px;">
                {quality_color} <strong>Quality Improved:</strong> +{quality_delta} points
            </p>
        </div>
        
        <div style="background: white; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h3>✅ Issues Resolved</h3>
            <ul>
    """
    
    for issue in comparison.get('resolved_issues', [])[:5]:
        html += f"<li>{issue.get('suggestion', issue) if isinstance(issue, dict) else issue}</li>"
    
    html += """
            </ul>
        </div>
        
        <div style="background: white; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h3>💡 New Recommendations in Code B</h3>
            <ul>
    """
    
    for suggestion in comparison.get('new_suggestions', [])[:5]:
        html += f"<li>{suggestion.get('suggestion', suggestion) if isinstance(suggestion, dict) else suggestion}</li>"
    
    html += """
            </ul>
        </div>
        
    </div>
    """
    
    return html
```

### Step 2: Add to `app.py` (find the line with `with gr.Tab` and add after it)

```python
# Add this after the existing tabs, before "Repository Analysis Tab"

with gr.Tab("🔀 Compare Code"):
    gr.Markdown("""
    ### 📊 Compare Two Code Snippets
    Upload two versions of code (original and refactored) to see detailed comparison:
    - Quality improvements
    - Bug reduction
    - Suggestion differences
    - Complexity changes
    """)
    
    with gr.Row():
        with gr.Column():
            code1_input = gr.Textbox(
                label="Code A (Original)",
                lines=15,
                placeholder="Paste first code snippet here...",
                info="Original or less optimized version"
            )
            lang1_input = gr.Dropdown(
                choices=["python", "javascript", "java", "cpp", "go", "rust"],
                value="python",
                label="Language"
            )
        with gr.Column():
            code2_input = gr.Textbox(
                label="Code B (Refactored)",
                lines=15,
                placeholder="Paste second code snippet here...",
                info="Improved or optimized version"
            )
            lang2_input = gr.Dropdown(
                choices=["python", "javascript", "java", "cpp", "go", "rust"],
                value="python",
                label="Language"
            )
    
    compare_btn = gr.Button("📊 Compare Analyses", variant="primary")
    comparison_output = gr.HTML(label="Comparison Results")
    
    def compare_code_handler(c1, c2, lang1, lang2):
        if not c1.strip() or not c2.strip():
            return "<p style='color: red;'>❌ Please enter code in both fields</p>"
        
        # Analyze both codes
        from core.comparison_engine import compare_analyses, format_comparison_html
        
        result1 = run_code_inspector(c1, lang1)
        result2 = run_code_inspector(c2, lang2)
        
        # Generate explanations for display
        explain1 = result1['explanations'].get('simple', 'Analysis complete')
        explain2 = result2['explanations'].get('simple', 'Analysis complete')
        
        # Compare
        comparison = compare_analyses(result1['analysis'], result2['analysis'])
        
        # Format and return
        return format_comparison_html(
            comparison, 
            explain1, 
            explain2,
            result1['analysis'],
            result2['analysis']
        )
    
    compare_btn.click(
        fn=compare_code_handler,
        inputs=[code1_input, code2_input, lang1_input, lang2_input],
        outputs=[comparison_output]
    )
```

---

## Feature 2: Learning Modes (2 hours)

### Step 1: Update `core/prompts.py` - Add these new prompts:

```python
# Add to prompts.py (around line 50, after existing prompts)

EXPLAIN_PROMPT_BEGINNER = """
You are teaching someone who is JUST STARTING to learn programming.

Explain the given code as if explaining to a 12-year-old learning to code:
- Use SIMPLE words (no technical jargon)
- Use real-world ANALOGIES and METAPHORS
- Explain WHY the code does what it does
- Break it down into tiny, understandable chunks
- Use emojis and simple formatting
- End with: "What did we learn?"

Example analogy: "A loop is like reading the same book chapter multiple times"

Code to explain:
{code}

Provide your explanation in this exact JSON format:
{{
    "title": "Simple explanation of what the code does",
    "analogy": "Real-world analogy that explains the concept",
    "step_by_step": [
        "Step 1: ...",
        "Step 2: ...",
        "Step 3: ..."
    ],
    "what_we_learned": "Key takeaway for beginners"
}}
"""

EXPLAIN_PROMPT_INTERVIEW = """
You are preparing someone for a CODING INTERVIEW.

Explain the given code in a technical, interview-ready way:
- Assume the person knows programming fundamentals
- Focus on TIME and SPACE complexity
- Discuss algorithmic approach
- Mention edge cases
- Discuss potential interview follow-up questions
- Be precise and technical

Code to explain:
{code}

Provide your explanation in this exact JSON format:
{{
    "algorithm_name": "Name of the algorithm or approach",
    "time_complexity": "O(...) with explanation",
    "space_complexity": "O(...) with explanation",
    "key_insight": "What makes this algorithm clever or efficient",
    "edge_cases": ["edge case 1", "edge case 2"],
    "interview_questions": [
        "How would you optimize this?",
        "What if the constraints changed?"
    ],
    "similar_problems": ["Problem name 1", "Problem name 2"]
}}
"""

EXPLAIN_PROMPT_OPTIMIZATION = """
You are a PERFORMANCE OPTIMIZATION EXPERT.

Analyze the given code ONLY from a performance perspective:
- Identify performance bottlenecks
- Explain why it's slow
- Show optimization techniques with tradeoffs
- Estimate performance improvement percentage
- Provide concrete optimization suggestions

Code to analyze:
{code}

Provide your analysis in this exact JSON format:
{{
    "current_performance": "Current Big-O and practical performance",
    "bottlenecks": [
        {{
            "issue": "Description of bottleneck",
            "impact": "Why this is slow",
            "severity": "High/Medium/Low"
        }}
    ],
    "optimization_techniques": [
        {{
            "technique": "Name of optimization",
            "explanation": "How it works",
            "expected_improvement": "X% faster",
            "tradeoffs": "What we sacrifice for speed"
        }}
    ],
    "optimized_approach": "High-level description of optimized version",
    "estimated_speedup": "3-5x faster",
    "when_to_optimize": "When is this important?"
}}
"""
```

### Step 2: Update `app.py` - Modify the Explanations tab:

Find this section in app.py:
```python
with gr.Tab("💬 Explanations"):
```

And replace it with:

```python
with gr.Tab("💬 Explanations"):
    with gr.Row():
        with gr.Column(scale=4):
            explanation_output = gr.Markdown(label="Explanation")
        with gr.Column(scale=1):
            mode_selector = gr.Radio(
                choices=["📖 Beginner", "💼 Interview", "⚡ Optimization"],
                value="Beginner",
                label="Explanation Mode",
                info="Choose level of detail"
            )
```

Then modify the `analyze_code()` function signature:
```python
# Change from:
def analyze_code(code, language, generate_images, use_mermaid=True):

# To:
def analyze_code(code, language, generate_images, use_mermaid=True, mode="Beginner"):
```

Then inside `analyze_code()`, before generating explanation, add:
```python
# Add mode-specific prompts
from core.prompts import (
    EXPLAIN_PROMPT_BEGINNER, 
    EXPLAIN_PROMPT_INTERVIEW, 
    EXPLAIN_PROMPT_OPTIMIZATION
)

# Select appropriate prompt based on mode
mode_map = {
    "Beginner": EXPLAIN_PROMPT_BEGINNER,
    "Interview": EXPLAIN_PROMPT_INTERVIEW,
    "Optimization": EXPLAIN_PROMPT_OPTIMIZATION
}

selected_prompt = mode_map.get(mode, EXPLAIN_PROMPT_BEGINNER)
# Use selected_prompt instead of default EXPLAIN_PROMPT when calling LLM
```

Then update the button click to include mode:
```python
analyze_btn.click(
    fn=analyze_code,
    inputs=[code_input, language_input, generate_images_checkbox, use_mermaid_checkbox, mode_selector],
    outputs=[explanation_output, analysis_output, quality_output, flowchart_output, callgraph_output]
)
```

---

## Testing Checklist

### Test Code Comparison:
```python
code_a = """
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"""

code_b = """
def bubble_sort_optimized(arr):
    for i in range(len(arr)):
        swapped = False
        for j in range(len(arr)-1-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
"""
# Should show "Bug reduction: 0, Quality improvement: 2-3 points"
```

### Test Learning Modes:
```python
test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

# Beginner mode: "Like adding numbers you got before"
# Interview mode: "Time: O(2^n), Space: O(n) due to recursion depth, follow-up: optimize with memoization?"
# Optimization mode: "Exponential growth is slow. Use memoization or iterative approach for O(n) time"
```

---

## Time Estimates Breakdown

**Code Comparison:**
- Create comparison_engine.py: 30 min
- Add tab to app.py: 30 min
- Test and fix: 30 min
- Create demo: 30 min
- **Total: 2 hours (buffer: 30 min = 2.5 hours)**

**Learning Modes:**
- Create 3 new prompts: 45 min
- Modify app.py: 30 min
- Test all modes: 30 min
- Polish and demo: 15 min
- **Total: 2 hours**

---

## UI/UX Tips

1. **For Code Comparison:**
   - Use colors: Red for Code A (original), Green for Code B (improved)
   - Show emoji indicators: 🟢 for improvements, 🔴 for regressions
   - Make comparison output scannable with clear sections

2. **For Learning Modes:**
   - Show mode description on hover: "Explains code like teaching beginners"
   - Highlight active mode with color
   - Show mode benefits in tooltip

---

**Ready to implement? Start with Code Comparison - it's the most impressive feature! 🚀**
