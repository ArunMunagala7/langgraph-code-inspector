"""
Gradio Web UI for Multi-Agent Code Understanding System
Launch with: python app.py
"""
import gradio as gr
import os
import base64
from graph.workflow import run_code_inspector
from data.samples import SAMPLES
from core.smart_diagram_generator import create_smart_flowchart
from core.diagram_generator import create_callgraph_image


def analyze_code(code, language, generate_images):
    """
    Analyze code and return results.
    
    Args:
        code: Source code to analyze
        language: Programming language
        generate_images: Whether to generate diagram images
        
    Returns:
        Tuple of (explanation, analysis, flowchart_img, callgraph_img)
    """
    try:
        if not code.strip():
            return "⚠️ Please enter some code to analyze", "", None, None
        
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
        
        flowchart_img = None
        callgraph_img = None
        
        # Generate images if requested
        if generate_images:
            print("🎨 Generating diagrams...")
            
            # Create temp directory for images
            os.makedirs("temp", exist_ok=True)
            
            # Generate flowchart
            flowchart_path = "temp/flowchart.png"
            if create_smart_flowchart(
                result['code'],
                result['explanations'],
                result['analysis'],
                flowchart_path
            ):
                flowchart_img = flowchart_path
            
            # Generate call graph
            callgraph_path = "temp/callgraph.png"
            if create_callgraph_image(result['knowledge_graph'], callgraph_path):
                callgraph_img = callgraph_path
            
            print("✅ Diagrams generated!")
        
        return explanation, analysis, flowchart_img, callgraph_img
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg, "", None, None


def load_sample(sample_name):
    """Load a sample code snippet."""
    if sample_name in SAMPLES:
        return SAMPLES[sample_name]['code'], SAMPLES[sample_name]['language']
    return "", "python"


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
            
            # Sample selector
            sample_dropdown = gr.Dropdown(
                choices=[""] + list(SAMPLES.keys()),
                label="📚 Load Sample Code",
                info="Choose a pre-loaded algorithm"
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
            
            with gr.Tab("📈 Flowchart"):
                flowchart_output = gr.Image(label="Code Flowchart", type="filepath")
            
            with gr.Tab("🕸️ Call Graph"):
                callgraph_output = gr.Image(label="Call Graph", type="filepath")
    
    # Examples
    gr.Markdown("### 📚 Quick Examples")
    gr.Examples(
        examples=[
            ["def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)", "python", True],
            ["function fibonacci(n) {\n    if (n <= 1) return n;\n    return fibonacci(n-1) + fibonacci(n-2);\n}", "javascript", True],
        ],
        inputs=[code_input, language_input, generate_images_checkbox],
        label="Try these examples"
    )
    
    # Event handlers
    sample_dropdown.change(
        fn=load_sample,
        inputs=[sample_dropdown],
        outputs=[code_input, language_input]
    )
    
    analyze_btn.click(
        fn=analyze_code,
        inputs=[code_input, language_input, generate_images_checkbox],
        outputs=[explanation_output, analysis_output, flowchart_output, callgraph_output]
    )
    
    gr.Markdown("""
    ---
    ### 🔧 Features
    - **5 AI Agents**: Specialized agents for parsing, knowledge graph building, analysis, visualization, and explanation
    - **Multi-Language Support**: Python, JavaScript, Java, C++, Go, Rust
    - **Smart Flowcharts**: AI-generated flowcharts with intelligent layout
    - **Knowledge Graphs**: Lightweight JSON-based code structure graphs
    - **Comprehensive Analysis**: Bug detection, complexity analysis, edge cases, and improvement suggestions
    
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
