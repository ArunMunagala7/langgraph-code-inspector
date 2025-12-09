"""
Gradio Web UI for Multi-Agent Code Understanding System
Launch with: python app.py
"""
import gradio as gr
import os
import base64
import json
from graph.workflow import run_code_inspector
from data.samples import SAMPLES
from core.smart_diagram_generator import create_smart_flowchart
from core.diagram_generator import create_callgraph_image
from core.repo_analyzer import analyze_repository
from core.notebook_parser import parse_notebook, is_notebook_file, get_notebook_summary
from agents.quality_agent import score_code_quality, format_quality_report


def generate_test_cases(code, language, analysis):
    """
    Generate pytest test cases from code analysis using LLM.
    
    Args:
        code: Source code to test
        language: Programming language
        analysis: Analysis result from run_code_inspector
        
    Returns:
        String containing copy-paste ready pytest code
    """
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        
        # Extract key information from analysis
        functions = analysis.get('functions', [])
        edge_cases = analysis.get('edge_cases', [])
        bugs = analysis.get('bugs', [])
        
        # Build prompt
        prompt_text = f"""You are a Python testing expert. Generate comprehensive pytest test cases for this code.

Code:
```{language}
{code}
```

Key information:
- Functions: {json.dumps(functions, indent=2) if functions else 'None'}
- Edge Cases: {json.dumps([str(e) for e in edge_cases], indent=2) if edge_cases else 'None'}
- Known Bugs/Issues: {json.dumps([str(b) for b in bugs], indent=2) if bugs else 'None'}

Generate pytest test cases that:
1. Test all functions identified
2. Cover all edge cases mentioned
3. Verify bugs are handled or fixed
4. Include boundary condition tests
5. Include error/exception tests

Return ONLY valid, copy-paste ready pytest code. No explanations.
Start with imports, then test functions.

Generate tests now:"""
        
        # Call LLM with invoke method
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        message = HumanMessage(content=prompt_text)
        response = llm.invoke([message])
        
        # Extract text from response
        response_text = response.content
        
        # Clean up response (remove markdown if present)
        if "```python" in response_text:
            response_text = response_text.split("```python")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        return response_text.strip()
        
    except Exception as e:
        import traceback
        error_msg = f"# ⚠️ Could not generate tests: {str(e)}\n# Error: {type(e).__name__}\n# Traceback:\n"
        error_msg += "# " + "\n# ".join(traceback.format_exc().split("\n"))
        return error_msg


def analyze_code(code, language, generate_images, use_mermaid=True):
    """
    Analyze code and return results.
    
    Args:
        code: Source code to analyze
        language: Programming language
        generate_images: Whether to generate diagram images
        use_mermaid: Whether to use Mermaid for flowcharts (default: True)
        
    Returns:
        Tuple of (explanation, analysis, quality_report, flowchart_img, callgraph_img, test_cases)
    """
    try:
        if not code.strip():
            return "⚠️ Please enter some code to analyze", "", "", None, None
        
        # Update progress: Running analysis
        print(f"\n🔍 Analyzing {language} code...")
        result = run_code_inspector(code, language)
        
        # Format explanation with detailed styling
        explanation = f"""
# 📝 Code Explanation

---

## 📌 Simple Explanation
> {result['explanations'].get('simple', 'N/A')}

---

## 🔬 Technical Deep Dive
{result['explanations'].get('technical', 'N/A')}

---

## 🎯 Purpose & Goals
{result['explanations'].get('purpose', 'N/A')}

---

## 🌍 Real-World Use Cases
{result['explanations'].get('use_case', 'N/A')}

---

## 🧮 Key Concepts
"""
        # Add key concepts
        key_concepts = result['explanations'].get('key_concepts', [])
        if key_concepts:
            for concept in key_concepts:
                if isinstance(concept, dict):
                    explanation += f"""
### {concept.get('concept', 'Concept')}
**Explanation:** {concept.get('explanation', 'N/A')}
**Importance:** {concept.get('importance', 'N/A')}

"""
                else:
                    explanation += f"- {concept}\n"
        else:
            explanation += "No key concepts identified\n"
        
        explanation += """
---

## 📂 Section-by-Section Breakdown
"""
        # Add sections
        sections = result['explanations'].get('sections', [])
        if sections:
            for i, section in enumerate(sections, 1):
                if isinstance(section, dict):
                    explanation += f"""
### Section {i}: {section.get('section_name', 'Unnamed')}
**Lines:** {section.get('code_lines', 'N/A')}
**Purpose:** {section.get('purpose', 'N/A')}

**Detailed Explanation:**
{section.get('detailed_explanation', 'N/A')}

**Key Operations:**
"""
                    ops = section.get('key_operations', [])
                    if ops:
                        for op in ops:
                            explanation += f"- {op}\n"
                    explanation += "\n"
                else:
                    explanation += f"- {section}\n"
        
        explanation += """
---

## 💾 Data Structures Used
"""
        # Add data structures
        data_structures = result['explanations'].get('data_structures', [])
        if data_structures:
            for ds in data_structures:
                if isinstance(ds, dict):
                    explanation += f"""
**{ds.get('structure', 'Unknown')}**
- Usage: {ds.get('usage', 'N/A')}
- Why chosen: {ds.get('why_chosen', 'N/A')}

"""
                else:
                    explanation += f"- {ds}\n"
        
        explanation += """
---

## 📊 Complexity Insights
"""
        complexity_insight = result['explanations'].get('complexity_insight', {})
        if isinstance(complexity_insight, dict):
            explanation += f"""
**Time Complexity:** {complexity_insight.get('time_complexity_explanation', 'N/A')}

**Space Complexity:** {complexity_insight.get('space_complexity_explanation', 'N/A')}

**Scalability:** {complexity_insight.get('scalability', 'N/A')}

"""
        
        explanation += """
---

## 🎓 Learning Points
"""
        learning_points = result['explanations'].get('learning_points', [])
        if learning_points:
            for point in learning_points:
                explanation += f"- {point}\n"
        
        explanation += f"""
---

## 📋 Summary
{result['explanations'].get('summary', 'N/A')}
"""
        
        # Format analysis with detailed styling
        bugs = result['analysis'].get('bugs', [])
        suggestions = result['analysis'].get('suggestions', [])
        edge_cases = result['analysis'].get('edge_cases', [])
        complexity = result['analysis'].get('complexity', {})
        perf_issues = result['analysis'].get('performance_issues', [])
        security = result['analysis'].get('security_concerns', [])
        code_quality = result['analysis'].get('code_quality', {})
        anti_patterns = result['analysis'].get('anti_patterns', [])
        test_coverage = result['analysis'].get('test_coverage', {})
        analysis_summary = result['analysis'].get('summary', 'N/A')
        
        analysis = f"""
# 🔍 Code Analysis Report

---

## 📊 Overall Assessment
{analysis_summary}

---

## 🐛 Potential Bugs ({len(bugs)})
"""
        if bugs:
            for i, bug in enumerate(bugs, 1):
                if isinstance(bug, dict):
                    analysis += f"""
### Bug {i}: {bug.get('description', 'Unknown')}
- **Severity:** {bug.get('severity', 'N/A').upper()}
- **When Triggered:** {bug.get('when_triggered', 'N/A')}
- **Impact:** {bug.get('impact', 'N/A')}
- **Fix:** {bug.get('fix', 'N/A')}

"""
                else:
                    analysis += f"- {bug}\n"
        else:
            analysis += "✅ No bugs detected\n"
        
        analysis += f"""
---

## ⚠️ Edge Cases ({len(edge_cases)})
"""
        if edge_cases:
            for i, case in enumerate(edge_cases, 1):
                if isinstance(case, dict):
                    analysis += f"""
### Edge Case {i}: {case.get('case', 'Unknown')}
- **Expected:** {case.get('expected_behavior', 'N/A')}
- **Current:** {case.get('current_behavior', 'N/A')}
- **Fix:** {case.get('fix', 'N/A')}

"""
                else:
                    analysis += f"- {case}\n"
        else:
            analysis += "✅ No edge cases identified\n"
        
        analysis += """
---

## ⏱️ Complexity Analysis
"""
        if complexity:
            analysis += f"""
| Metric | Details |
|--------|---------|
| **Time Complexity** | {complexity.get('time', 'N/A')} |
| **Space Complexity** | {complexity.get('space', 'N/A')} |
| **Bottlenecks** | {complexity.get('bottlenecks', 'N/A')} |

**Optimizations:**
"""
            opts = complexity.get('optimizations', [])
            if opts:
                for opt in opts:
                    analysis += f"- {opt}\n"
            else:
                analysis += "- No specific optimizations identified\n"
        else:
            analysis += "No complexity analysis available\n"
        
        analysis += f"""
---

## ⚡ Performance Issues ({len(perf_issues)})
"""
        if perf_issues:
            for i, issue in enumerate(perf_issues, 1):
                if isinstance(issue, dict):
                    analysis += f"""
### Performance Issue {i}
- **Issue:** {issue.get('issue', 'Unknown')}
- **Impact:** {issue.get('impact', 'N/A')}
- **Fix:** {issue.get('fix', 'N/A')}

"""
                else:
                    analysis += f"- {issue}\n"
        else:
            analysis += "✅ No major performance issues detected\n"
        
        analysis += f"""
---

## 🔐 Security Concerns ({len(security)})
"""
        if security:
            for i, concern in enumerate(security, 1):
                if isinstance(concern, dict):
                    analysis += f"""
### Security Concern {i}
- **Concern:** {concern.get('concern', 'Unknown')}
- **Risk Level:** {concern.get('risk_level', 'medium').upper()}
- **Example:** {concern.get('example', 'N/A')}
- **Mitigation:** {concern.get('mitigation', 'N/A')}

"""
                else:
                    analysis += f"- {concern}\n"
        else:
            analysis += "✅ No security concerns identified\n"
        
        analysis += """
---

## 📋 Code Quality Metrics
"""
        if code_quality:
            analysis += f"""
| Metric | Score | Assessment |
|--------|-------|------------|
| **Readability** | {code_quality.get('readability_score', 'N/A')}/10 | {code_quality.get('readability_reasons', 'N/A')} |
| **Maintainability** | {code_quality.get('maintainability_score', 'N/A')}/10 | {code_quality.get('maintainability_reasons', 'N/A')} |

**Maintainability Issues:**
"""
            maint_issues = code_quality.get('maintainability_issues', [])
            if maint_issues:
                for issue in maint_issues:
                    analysis += f"- {issue}\n"
            else:
                analysis += "- None identified\n"
        else:
            analysis += "No code quality metrics available\n"
        
        analysis += f"""
---

## 💡 Improvement Suggestions ({len(suggestions)})
"""
        if suggestions:
            for i, sugg in enumerate(suggestions, 1):
                if isinstance(sugg, dict):
                    analysis += f"""
### Suggestion {i}
- **Priority:** {sugg.get('priority', 'medium').upper()}
- **Suggestion:** {sugg.get('suggestion', 'Unknown')}
- **Benefit:** {sugg.get('benefit', 'N/A')}

**Before:**
```
{sugg.get('before_code', 'N/A')}
```

**After:**
```
{sugg.get('after_code', 'N/A')}
```

"""
                else:
                    analysis += f"- {sugg}\n"
        else:
            analysis += "✅ No specific suggestions\n"
        
        analysis += f"""
---

## 🚩 Code Smells & Anti-Patterns ({len(anti_patterns)})
"""
        if anti_patterns:
            for i, pattern in enumerate(anti_patterns, 1):
                if isinstance(pattern, dict):
                    analysis += f"""
### Anti-Pattern {i}: {pattern.get('pattern', 'Unknown')}
- **Description:** {pattern.get('description', 'N/A')}
- **Impact:** {pattern.get('impact', 'N/A')}
- **Refactoring:** {pattern.get('refactoring', 'N/A')}

"""
                else:
                    analysis += f"- {pattern}\n"
        else:
            analysis += "✅ No major anti-patterns detected\n"
        
        analysis += """
---

## 🧪 Recommended Test Cases
"""
        if test_coverage:
            test_cases = test_coverage.get('recommended_test_cases', [])
            if test_cases:
                for i, test in enumerate(test_cases, 1):
                    if isinstance(test, dict):
                        analysis += f"""
### Test {i}: {test.get('case_name', 'Unnamed')}
- **Input:** {test.get('input', 'N/A')}
- **Expected Output:** {test.get('expected_output', 'N/A')}
- **Purpose:** {test.get('purpose', 'N/A')}

"""
                    else:
                        analysis += f"- {test}\n"
            else:
                analysis += "No specific test cases recommended\n"
        else:
            analysis += "No test coverage recommendations\n"
        
        # Generate quality scores
        
        # Generate quality scores
        print("📊 Calculating quality scores...")
        quality_scores = score_code_quality(code, language, result['analysis'])
        quality_report = format_quality_report(quality_scores)
        
        flowchart_img = None
        callgraph_img = None
        
        # Generate images if requested
        if generate_images:
            print("🎨 Generating diagrams...")
            
            # Create temp directory for images
            os.makedirs("temp", exist_ok=True)
            
            # Generate unique filenames based on code hash (ensures different codes get different flowcharts)
            import hashlib
            code_hash = hashlib.md5(code.encode()).hexdigest()[:8]
            
            # Generate flowchart with unique name
            flowchart_path = os.path.abspath(f"temp/flowchart_{code_hash}.png")
            if use_mermaid:
                try:
                    from core.mermaid_generator_v3 import create_flowchart
                    
                    # Build comprehensive analysis for flowchart generation
                    flowchart_analysis = {
                        'code': code,
                        'parsed_code': result.get('code', code),
                        'functions': result['analysis'].get('functions', []),
                        'loops': result['analysis'].get('loops', []),
                        'conditions': result['analysis'].get('conditions', []),
                        'recursion': result['analysis'].get('recursion', False),
                        'bugs': result['analysis'].get('bugs', []),
                        'complexity': result['analysis'].get('complexity', {}),
                        'edge_cases': result['analysis'].get('edge_cases', []),
                        'kg_nodes': len(result['knowledge_graph'].get('nodes', [])),
                        'kg_edges': len(result['knowledge_graph'].get('edges', [])),
                    }
                    
                    success = create_flowchart(
                        code,
                        flowchart_analysis,
                        flowchart_path
                    )
                    
                    if success and os.path.exists(flowchart_path):
                        flowchart_img = flowchart_path
                        print("✅ Mermaid flowchart generated!")
                    else:
                        print("⚠️ Mermaid rendering failed")
                        if create_smart_flowchart(
                            result['code'],
                            result['explanations'],
                            result['analysis'],
                            flowchart_path
                        ):
                            flowchart_img = flowchart_path
                except Exception as e:
                    print(f"⚠️ Mermaid error: {e}")
                    if create_smart_flowchart(
                        result['code'],
                        result['explanations'],
                        result['analysis'],
                        flowchart_path
                    ):
                        flowchart_img = flowchart_path
            else:
                if create_smart_flowchart(
                    result['code'],
                    result['explanations'],
                    result['analysis'],
                    flowchart_path
                ):
                    flowchart_img = flowchart_path
            
            # Generate call graph with unique name
            callgraph_path = os.path.abspath(f"temp/callgraph_{code_hash}.png")
            if create_callgraph_image(result['knowledge_graph'], callgraph_path):
                callgraph_img = callgraph_path
            
            print("✅ Diagrams generated!")
        
        # Generate test cases
        test_cases = ""
        print("🧪 Generating test cases...")
        try:
            test_cases = generate_test_cases(code, language, result['analysis'])
        except Exception as e:
            print(f"⚠️ Test generation error: {e}")
            test_cases = f"# ⚠️ Could not generate tests\n# Error: {str(e)}"
        
        return explanation, analysis, quality_report, flowchart_img, callgraph_img, test_cases
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg, "", "", None, None, ""


def load_sample(sample_name):
    """Load a sample code snippet."""
    if not sample_name:
        return "", "python"
    
    # Extract actual sample name from "[Difficulty] name" format
    if sample_name.startswith("["):
        # Format: "[Easy] python_sum_array" -> "python_sum_array"
        sample_key = sample_name.split("] ", 1)[1] if "] " in sample_name else sample_name
    else:
        sample_key = sample_name
    
    if sample_key in SAMPLES:
        return SAMPLES[sample_key]['code'], SAMPLES[sample_key]['language']
    return "", "python"


def handle_file_upload(file):
    """
    Handle uploaded code file (including .ipynb notebooks).
    
    Args:
        file: Gradio file upload object
        
    Returns:
        Tuple of (code, language, message)
    """
    if file is None:
        return "", "python", ""
    
    try:
        filename = file.name if hasattr(file, 'name') else str(file)
        
        # Detect language from extension
        ext = filename.split('.')[-1].lower()
        language_map = {
            'py': 'python',
            'js': 'javascript',
            'java': 'java',
            'cpp': 'c++',
            'c': 'c',
            'go': 'go',
            'rs': 'rust',
            'ts': 'typescript',
            'ipynb': 'python'
        }
        detected_language = language_map.get(ext, 'python')
        
        # Handle Jupyter notebooks
        if is_notebook_file(filename):
            parsed = parse_notebook(file.name if hasattr(file, 'name') else file)
            code = parsed['combined_code']
            summary = get_notebook_summary(file.name if hasattr(file, 'name') else file)
            message = f"✅ Loaded Jupyter Notebook\n{summary}\n\n📝 **Note**: All code cells have been combined for analysis"
            return code, parsed['language'], message
        
        # Handle regular code files
        with open(file.name if hasattr(file, 'name') else file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        lines = len(code.splitlines())
        chars = len(code)
        message = f"✅ Loaded {filename}\n- Lines: {lines}\n- Characters: {chars}\n- Detected Language: {detected_language.title()}"
        
        return code, detected_language, message
        
    except Exception as e:
        return "", "python", f"❌ Error loading file: {str(e)}"


def analyze_repository_ui(github_url, max_files, progress=gr.Progress()):
    """
    Analyze GitHub repository from UI.
    """
    if not github_url or not github_url.strip():
        return "❌ Please enter a GitHub URL", "", ""
    
    try:
        # Progress callback
        def update_progress(msg):
            if progress is not None and hasattr(progress, '__call__'):
                try:
                    # Try Gradio Progress object first
                    if hasattr(progress, 'tqdm'):
                        progress(0.5, desc=msg)
                    else:
                        # Fall back to simple callable
                        progress(msg)
                except TypeError:
                    # If it fails, just print
                    print(msg)
            else:
                print(msg)
        
        # Run analysis
        result = analyze_repository(
            github_url=github_url.strip(),
            max_files=int(max_files),
            progress_callback=update_progress
        )
        
        if 'error' in result:
            return f"❌ Error: {result['error']}", "", ""
        
        # Format summary
        summary = result['summary']
        summary_md = f"""
# 📊 Repository Analysis Results

## Overview
- **Repository**: {result['metadata']['repo_name']}
- **Files Analyzed**: {summary['total_files_analyzed']} / {summary['total_files_found']}
- **Total Lines of Code**: {summary['total_lines_of_code']:,}
- **Total Functions**: {summary['total_functions']}

## Issues Found
- 🐛 **Bugs**: {summary['total_bugs_found']}
- 💡 **Suggestions**: {summary['total_suggestions']}

## Language Breakdown
"""
        for lang, stats in summary['languages'].items():
            summary_md += f"- **{lang.title()}**: {stats['files']} files, {stats['lines']:,} lines\n"
        
        summary_md += "\n## 🔥 Most Complex Files\n"
        for f in summary['most_complex_files']:
            summary_md += f"- `{f['file']}` (Complexity: {f['complexity']}, LOC: {f['loc']})\n"
        
        # Format bugs
        bugs_md = "# 🐛 Bugs Found\n\n"
        if result['bugs']:
            for bug in result['bugs']:
                bugs_md += f"### {bug['file']}\n"
                bugs_md += f"{bug['bug']}\n\n"
        else:
            bugs_md += "No bugs detected! ✅"
        
        # Format JSON for download
        json_output = json.dumps(result, indent=2)
        
        return summary_md, bugs_md, json_output
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"❌ Error: {str(e)}", "", ""


# Create Gradio interface
with gr.Blocks(title="AI Code Understanding System") as demo:
    gr.Markdown("""
    # 🤖 Multi-Agent Code Understanding System
    ### Powered by LangGraph & GPT-4o-mini
    
    Analyze code with 5 AI agents: **Parse** → **BuildKG** → **Analyze** → **Visualize** → **Explain**
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📥 Input")
            
            # File upload
            file_upload = gr.File(
                label="📂 Upload Code File (.py, .js, .ipynb, etc.)",
                file_types=[".py", ".js", ".java", ".cpp", ".c", ".go", ".rs", ".ts", ".ipynb"],
                type="filepath"
            )
            file_status = gr.Markdown("", visible=True)
            
            # Sample selector
            sample_choices = [""] + [
                f"[{sample['difficulty']}] {name}" 
                for name, sample in SAMPLES.items()
            ]
            sample_dropdown = gr.Dropdown(
                choices=sample_choices,
                label="📚 Load Sample Code",
                info="Choose a pre-loaded algorithm (Easy → Hard)"
            )
            
            # Code input
            code_input = gr.Code(
                label="Code to Analyze",
                language="python",
                lines=15
            )
            
            # Language selector
            language_input = gr.Dropdown(
                choices=["python", "javascript", "java", "c++", "go", "rust"],
                value="python",
                label="Programming Language",
                info="Select the language of your code"
            )
            
            # Generate images checkbox
            generate_images_checkbox = gr.Checkbox(
                label="Generate Flowchart & Call Graph Images",
                value=True,
                info="⚠️ May take 5-10 seconds"
            )
            
            # Mermaid toggle
            use_mermaid_checkbox = gr.Checkbox(
                label="🎨 Use Mermaid for Flowcharts (Recommended)",
                value=True,
                info="Modern, clean flowcharts via Mermaid.js"
            )
            
            # Analyze button
            analyze_btn = gr.Button("🚀 Analyze Code", variant="primary", size="lg")
    
    # Results section
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Results")
            
            with gr.Tab("💬 Explanations"):
                explanation_output = gr.Markdown(label="Explanations")
            
            with gr.Tab("🔍 Analysis"):
                analysis_output = gr.Markdown(label="Analysis")
            
            with gr.Tab("⭐ Quality Score"):
                quality_output = gr.Markdown(label="Code Quality Report")
            
            with gr.Tab("📈 Flowchart"):
                flowchart_output = gr.Image(label="Code Flowchart", type="filepath")
            
            with gr.Tab("🕸️ Call Graph"):
                callgraph_output = gr.Image(label="Call Graph", type="filepath")
            
            with gr.Tab("🧪 Generated Tests"):
                test_output = gr.Code(
                    language="python",
                    label="Generated Test Cases",
                    lines=20,
                    max_lines=50
                )
    
    # Examples
    gr.Markdown("### 📚 Quick Examples")
    gr.Examples(
        examples=[
            ["def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)", "python", True, True],
            ["function fibonacci(n) {\n    if (n <= 1) return n;\n    return fibonacci(n-1) + fibonacci(n-2);\n}", "javascript", True, True],
        ],
        inputs=[code_input, language_input, generate_images_checkbox, use_mermaid_checkbox],
        label="Try these examples"
    )
    
    # Event handlers
    file_upload.change(
        fn=handle_file_upload,
        inputs=[file_upload],
        outputs=[code_input, language_input, file_status]
    )
    
    sample_dropdown.change(
        fn=load_sample,
        inputs=[sample_dropdown],
        outputs=[code_input, language_input]
    )
    
    analyze_btn.click(
        fn=analyze_code,
        inputs=[code_input, language_input, generate_images_checkbox, use_mermaid_checkbox],
        outputs=[explanation_output, analysis_output, quality_output, flowchart_output, callgraph_output, test_output]
    )
    
    # Repository Analysis Tab
    with gr.Tab("🗂️ Repository Analysis"):
        gr.Markdown("""
        ### Analyze Entire GitHub Repositories
        Enter a GitHub URL to analyze all code files in the repository.
        This feature clones the repo, discovers all code files, and runs AI analysis on each one.
        """)
        
        with gr.Row():
            with gr.Column(scale=4):
                repo_url_input = gr.Textbox(
                    label="GitHub Repository URL",
                    placeholder="https://github.com/username/repository",
                    lines=1,
                    info="Enter the full GitHub repository URL"
                )
            with gr.Column(scale=1):
                max_files_slider = gr.Slider(
                    minimum=5,
                    maximum=100,
                    value=30,
                    step=5,
                    label="Max Files",
                    info="Limit analysis to prevent timeouts"
                )
        
        analyze_repo_btn = gr.Button("🔍 Analyze Repository", variant="primary", size="lg")
        
        gr.Markdown("### 📊 Results")
        
        with gr.Tabs():
            with gr.Tab("Summary"):
                repo_summary_output = gr.Markdown(label="Repository Summary")
            
            with gr.Tab("Bugs & Issues"):
                repo_bugs_output = gr.Markdown(label="Bugs Found")
            
            with gr.Tab("JSON Output"):
                repo_json_output = gr.Textbox(
                    label="Full Results (JSON)",
                    lines=20,
                    max_lines=30,
                    info="Complete analysis data - copy this to save results"
                )
        
        gr.Markdown("""
        ### ⚠️ Notes
        - Analysis time depends on repository size (expect 30-60 seconds per 10 files)
        - Large files (>100KB) are automatically skipped
        - Common directories like `node_modules`, `.git`, `venv` are excluded
        - Results are aggregated across all analyzed files
        """)
        
        # Repository analysis event handler
        analyze_repo_btn.click(
            fn=analyze_repository_ui,
            inputs=[repo_url_input, max_files_slider],
            outputs=[repo_summary_output, repo_bugs_output, repo_json_output]
        )
    
    gr.Markdown("""
    ---
    ### 🔧 Features
    - **5 AI Agents**: Specialized agents for parsing, knowledge graph building, analysis, visualization, and explanation
    - **Multi-Language Support**: Python, JavaScript, Java, C++, Go, Rust
    - **Smart Flowcharts**: AI-generated flowcharts with intelligent layout
    - **Knowledge Graphs**: Lightweight JSON-based code structure graphs
    - **Comprehensive Analysis**: Bug detection, complexity analysis, edge cases, and improvement suggestions
    - **Repository Analysis**: Clone and analyze entire GitHub repositories
    
    ### 📖 About
    Built with **LangGraph** for multi-agent orchestration and **GPT-4o-mini** for intelligent code understanding.
    """)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 Starting Gradio Web UI...")
    print("="*80 + "\n")
    
    # Create temp directory
    os.makedirs("temp", exist_ok=True)
    
    # Launch the app
    print("\n" + "="*80)
    print("🚀 Gradio Web UI Starting...")
    print("="*80)
    print("\n🌐 Open your browser at: http://localhost:7860")
    print("\n📚 Features:")
    print("   • 10 Test Cases (Easy → Hard)")
    print("   • AI-powered code analysis")
    print("   • Flowcharts with loops/recursion")
    print("   • Call graphs & complexity analysis")
    print("   • Quality scoring")
    print("\n" + "="*80 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=False,  # Set to True to create a public link
        show_error=True
    )
