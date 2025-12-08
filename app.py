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


def analyze_code(code, language, generate_images, use_mermaid=True):
    """
    Analyze code and return results.
    
    Args:
        code: Source code to analyze
        language: Programming language
        generate_images: Whether to generate diagram images
        use_mermaid: Whether to use Mermaid for flowcharts (default: True)
        
    Returns:
        Tuple of (explanation, analysis, quality_report, flowchart_img, callgraph_img)
    """
    try:
        if not code.strip():
            return "⚠️ Please enter some code to analyze", "", "", None, None
        
        # Run analysis
        print(f"\n🔍 Analyzing {language} code...")
        result = run_code_inspector(code, language)
        
        # Format explanation
        explanation = f"""
## 📝 Simple Explanation
{result['explanations']['simple']}

## 🔬 Technical Explanation
{result['explanations']['technical']}

## 📊 Summary
{result['explanations']['summary']}
"""
        
        # Format analysis
        bugs = result['analysis'].get('bugs', [])
        suggestions = result['analysis'].get('suggestions', [])
        edge_cases = result['analysis'].get('edge_cases', [])
        complexity = result['analysis'].get('complexity', {})
        
        analysis = f"""
## 🐛 Potential Bugs ({len(bugs)})
{chr(10).join(['• ' + (b if isinstance(b, str) else b.get('description', str(b))) for b in bugs]) if bugs else '✅ No bugs detected'}

## 💡 Suggestions ({len(suggestions)})
{chr(10).join(['• ' + (s if isinstance(s, str) else s.get('description', str(s))) for s in suggestions]) if suggestions else '✅ No suggestions'}

## ⚠️ Edge Cases ({len(edge_cases)})
{chr(10).join(['• ' + (e if isinstance(e, str) else e.get('description', str(e))) for e in edge_cases]) if edge_cases else '✅ No edge cases identified'}

## ⏱️ Complexity
- **Time**: {complexity.get('time', 'N/A')}
- **Space**: {complexity.get('space', 'N/A')}

## 📈 Knowledge Graph
- **Nodes**: {len(result['knowledge_graph'].get('nodes', []))}
- **Edges**: {len(result['knowledge_graph'].get('edges', []))}
"""
        
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
            
            # Generate flowchart
            flowchart_path = os.path.abspath("temp/flowchart.png")
            if use_mermaid:
                try:
                    from core.mermaid_generator import generate_mermaid_flowchart, render_mermaid_to_png
                    
                    # Generate Mermaid flowchart (returns Mermaid code string)
                    mermaid_code = generate_mermaid_flowchart(
                        code,
                        result['explanations'],
                        result['analysis']
                    )
                    
                    if mermaid_code:
                        success = render_mermaid_to_png(mermaid_code, flowchart_path)
                        if success and os.path.exists(flowchart_path):
                            flowchart_img = flowchart_path
                            print("✅ Mermaid flowchart generated!")
                        else:
                            print(f"⚠️ Render returned {success}, file exists: {os.path.exists(flowchart_path)}")
                except Exception as e:
                    print(f"⚠️ Mermaid generation failed, using matplotlib: {e}")
                    import traceback
                    traceback.print_exc()
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
            
            # Generate call graph
            callgraph_path = os.path.abspath("temp/callgraph.png")
            if create_callgraph_image(result['knowledge_graph'], callgraph_path):
                callgraph_img = callgraph_path
            
            print("✅ Diagrams generated!")
        
        return explanation, analysis, quality_report, flowchart_img, callgraph_img
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg, "", "", None, None


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
                explanation_output = gr.Textbox(label="Explanations", interactive=False, lines=15, max_lines=20)
            
            with gr.Tab("🔍 Analysis"):
                analysis_output = gr.Textbox(label="Analysis", interactive=False, lines=15, max_lines=20)
            
            with gr.Tab("⭐ Quality Score"):
                quality_output = gr.Textbox(label="Code Quality Report", interactive=False, lines=15, max_lines=20)
            
            with gr.Tab("📈 Flowchart"):
                flowchart_output = gr.Image(label="Code Flowchart", type="filepath")
            
            with gr.Tab("🕸️ Call Graph"):
                callgraph_output = gr.Image(label="Call Graph", type="filepath")
    
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
        outputs=[explanation_output, analysis_output, quality_output, flowchart_output, callgraph_output]
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
    demo.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=False,  # Set to True to create a public link
        show_error=True
    )
