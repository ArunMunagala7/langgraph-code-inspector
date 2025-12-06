# 🎯 Multi-Agent Code Understanding System

A lightweight, modular system that converts code into human-friendly explanations, flowcharts, and knowledge graphs using **LangGraph** and **OpenAI**.

## ✨ Features

- 🔍 **Parse Code**: Extract structural components (functions, loops, conditions, variables)
- 📊 **Build Knowledge Graph**: Create lightweight JSON-based knowledge graphs
- 🔬 **Analyze Code**: Detect bugs, edge cases, and complexity analysis
- 📈 **Generate Visualizations**: Create Mermaid flowcharts and call graphs
- 📝 **Explain Code**: Generate multi-level explanations (simple, technical, line-by-line)

## 🛠️ Tech Stack

- **Python** 3.11+
- **LangGraph** - Multi-agent workflow orchestration
- **OpenAI API** - GPT-4o-mini for code analysis
- **Mermaid.js** - Diagram generation

## 📦 Installation

### 1. Clone the repository
```bash
cd langgraph-code-inspector
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your OpenAI API key
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## 🚀 Usage

### Interactive Mode (Recommended for first-time users)
```bash
python main.py
```

This will show you a menu of sample code snippets to analyze.

### Analyze a Specific Sample
```bash
python main.py --sample python_sum_array
python main.py --sample python_binary_search
python main.py --sample python_fibonacci
```

### Analyze Custom Code from Command Line
```bash
python main.py --code "def hello(): print('Hello, World!')"
```

### Analyze Code from a File
```bash
python main.py --file path/to/your/code.py
```

### Advanced Options
```bash
# Specify language (auto-detected by default)
python main.py --sample python_fibonacci --language python

# Custom output path
python main.py --sample python_binary_search --output my_analysis.json

# Don't save to file (console output only)
python main.py --sample python_sum_array --no-save
```

## 📊 Output

The system produces:

1. **Console Output** - Formatted, human-readable analysis
2. **JSON File** - Complete analysis data saved to `outputs/` directory

### Sample Output Includes:
- ✅ Simple explanation (for beginners)
- ✅ Technical explanation (for developers)
- ✅ Line-by-line breakdown
- ✅ Bug detection
- ✅ Edge case identification
- ✅ Time/Space complexity analysis
- ✅ Improvement suggestions
- ✅ Mermaid flowchart
- ✅ Mermaid call graph
- ✅ JSON knowledge graph

## 🏗️ Architecture

### Multi-Agent Workflow

```
START
  ↓
ParseCodeAgent ────────► Extract functions, loops, conditions, variables
  ↓
BuildKGAgent ──────────► Build JSON knowledge graph
  ↓
AnalyzeAgent ──────────► Detect bugs, complexity, suggestions
  ↓
VisualizeAgent ────────► Generate Mermaid diagrams
  ↓
ExplainAgent ──────────► Create multi-level explanations
  ↓
END
```

### Project Structure

```
langgraph-code-inspector/
│
├── agents/                    # Individual agent implementations
│   ├── parse_agent.py        # Code structure extraction
│   ├── kg_agent.py           # Knowledge graph construction
│   ├── analyze_agent.py      # Bug & complexity analysis
│   ├── visualize_agent.py    # Mermaid diagram generation
│   └── explain_agent.py      # Multi-level explanations
│
├── graph/
│   └── workflow.py           # LangGraph workflow definition
│
├── core/
│   ├── state.py              # Shared state definition
│   ├── prompts.py            # LLM prompts for each agent
│   └── utils.py              # Helper functions
│
├── data/
│   ├── samples.py            # Sample code snippets
│   └── samples.json          # Sample data (generated)
│
├── outputs/                  # Generated analysis files
│
├── main.py                   # CLI entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🧪 Examples

### Example 1: Simple Array Sum
```bash
python main.py --sample python_sum_array
```

**Output includes:**
- Detected: O(n) time complexity, O(1) space
- Suggested: Use built-in `sum()` function
- Edge cases: Empty array, non-numeric values

### Example 2: Binary Search
```bash
python main.py --sample python_binary_search
```

**Output includes:**
- Detected: O(log n) time complexity
- Flowchart showing the binary search logic
- Edge cases: Empty array, single element, target not found

### Example 3: Fibonacci (Recursive)
```bash
python main.py --sample python_fibonacci
```

**Output includes:**
- **Bug detected**: No handling for negative inputs (infinite recursion)
- Detected: O(2^n) time complexity
- Suggested: Use memoization or iterative approach

## 🌟 Key Highlights

### Lightweight Knowledge Graph
- **No database required** - Pure JSON representation
- **Fast and portable** - Easy to inspect and debug
- **Perfect for code snippets** - Optimized for 10-100 line code samples

### Intelligent Analysis
- Detects potential bugs and edge cases
- Provides Big-O complexity analysis
- Suggests improvements and best practices

### Beautiful Visualizations
- **Flowcharts** - Show control flow and logic
- **Call Graphs** - Visualize function relationships
- **Mermaid format** - Render in GitHub, VSCode, or online tools

## 🔧 Configuration

Edit `core/prompts.py` to customize agent behaviors and analysis depth.

## 📝 Supported Languages

Currently optimized for:
- Python ✅
- JavaScript ✅
- Java ✅
- C/C++ (basic support)

Auto-detection works for most common patterns.

## 🤝 Contributing

This is a demonstration project showcasing LangGraph multi-agent workflows. Feel free to:
- Add more sample code
- Improve agent prompts
- Add support for more languages
- Enhance visualization

## 👤 Author

**Arun Munagala**

## 📄 License

MIT

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [OpenAI](https://openai.com)
- Diagrams with [Mermaid](https://mermaid.js.org)
