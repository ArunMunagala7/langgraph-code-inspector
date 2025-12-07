# 🎯 Multi-Agent Code Understanding System

**An intelligent, AI-powered code analysis platform using LangGraph multi-agent orchestration and GPT-4o-mini to transform code into human-friendly explanations, interactive visualizations, and actionable insights.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0.4-green.svg)](https://github.com/langchain-ai/langgraph)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

### 🤖 **5 Specialized AI Agents**
- 🔍 **ParseAgent**: Extract structural components (functions, loops, conditions, variables)
- 📊 **BuildKGAgent**: Create lightweight JSON-based knowledge graphs
- 🔬 **AnalyzeAgent**: Detect bugs, edge cases, complexity, and code smells
- 📈 **VisualizeAgent**: Generate AI-powered flowcharts and call graphs
- 📝 **ExplainAgent**: Generate multi-level explanations (beginner, technical, line-by-line)

### 🎨 **Advanced Visualizations**
- **AI-Generated Flowcharts**: Smart layout algorithm with collision-free arrow routing
- **Interactive Call Graphs**: NetworkX-powered function dependency visualization
- **Real-time Rendering**: Matplotlib-based diagram generation with guaranteed no overlaps

### 🌐 **Web Interface**
- **Gradio UI**: Professional web interface with tabbed navigation
- **Live Analysis**: Real-time code analysis with visual feedback
- **Sample Library**: Pre-loaded algorithms for quick demos
- **Image Export**: Download flowcharts and diagrams

### 📊 **Comprehensive Analysis**
- Bug detection and security issues
- Time/space complexity (Big-O notation)
- Edge case identification
- Code improvement suggestions
- Best practice recommendations

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Orchestration** | LangGraph 1.0.4 | Multi-agent workflow management |
| **AI Engine** | OpenAI GPT-4o-mini | Natural language understanding & code analysis |
| **Visualization** | Matplotlib 3.10.7 + NetworkX 3.6 | Diagram generation |
| **Web UI** | Gradio 6.0.2 | Interactive web interface |
| **Language** | Python 3.11+ | Core implementation |

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/ArunMunagala7/langgraph-code-inspector.git
cd langgraph-code-inspector
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your OpenAI API key
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
```

---

## 🚀 Usage

### 🌐 Web Interface (Recommended)
```bash
python app.py
# Open http://localhost:7860 in your browser
```

**Features:**
- 📝 Paste code or select from samples
- 🔄 Real-time analysis with progress indicators
- 📊 Tabbed results: Explanations | Analysis | Flowchart | Call Graph
- 💾 Download generated diagrams
- 🎨 Clean, professional UI for presentations

### 💻 Command Line Interface

#### Interactive Mode
```bash
python main.py
```

#### Analyze Specific Samples
```bash
python main.py --sample python_binary_search --generate-images
python main.py --sample python_fibonacci --generate-images
python main.py --sample python_bubble_sort --generate-images
```

#### Analyze Custom Code
```bash
python main.py --code "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"
```

#### Analyze from File
```bash
python main.py --file path/to/code.py --generate-images
```

---

## 📊 Output Examples

### 1. Web UI Output
- **Explanations Tab**: Beginner-friendly, technical, and line-by-line breakdowns
- **Analysis Tab**: Bugs, complexity, edge cases, suggestions (formatted with markdown)
- **Flowchart Tab**: AI-generated control flow diagram with color-coded nodes
- **Call Graph Tab**: Function dependency visualization

### 2. CLI Output
```
outputs/
├── binary_search_analysis_20250106_143022.json    # Complete analysis
├── binary_search_flowchart_20250106_143022.png     # AI flowchart
├── binary_search_flowchart_description.json        # Flowchart steps
└── binary_search_callgraph_20250106_143022.png     # Call graph
```

---

## 🏗️ Architecture

### Multi-Agent Workflow (LangGraph)

```
                    START
                      ↓
         ┌───────────────────────┐
         │   ParseCodeAgent      │ → Extract functions, loops, conditions
         │  (Structure Analysis) │    variables, and code components
         └───────────────────────┘
                      ↓
         ┌───────────────────────┐
         │   BuildKGAgent        │ → Build JSON knowledge graph
         │ (Graph Construction)  │    with nodes and relationships
         └───────────────────────┘
                      ↓
         ┌───────────────────────┐
         │   AnalyzeAgent        │ → Detect bugs, complexity,
         │  (Deep Analysis)      │    edge cases, suggestions
         └───────────────────────┘
                      ↓
         ┌───────────────────────┐
         │   VisualizeAgent      │ → Generate AI-powered flowcharts
         │  (Diagram Generator)  │    and NetworkX call graphs
         └───────────────────────┘
                      ↓
         ┌───────────────────────┐
         │   ExplainAgent        │ → Create beginner, technical,
         │  (NLP Explanation)    │    and line-by-line explanations
         └───────────────────────┘
                      ↓
                     END
```

### Key Innovation: AI-Powered Flowcharts

Unlike traditional AST-based generators, this system uses **LLM-generated descriptions**:

1. **LLM analyzes code** → Understands logic semantically
2. **Generates structured JSON** → Step-by-step flowchart
3. **Smart layout** → BFS-based positioning
4. **Collision-free routing** → Guaranteed no overlaps

---

## 🌟 Key Highlights

- **Collision-Free Visualizations**: Boxes spaced 8+ units horizontally, 4.5 units vertically
- **Lightweight Knowledge Graph**: Pure JSON, no database required
- **Modular Multi-Agent Design**: Easy to extend and customize
- **Natural Language Processing**: Beginner to expert explanations

---

## 📄 License

MIT License

---

## 👤 Author

**Arun Munagala**
- GitHub: [@ArunMunagala7](https://github.com/ArunMunagala7)

---

**⭐ Star this repo if you find it useful!**
