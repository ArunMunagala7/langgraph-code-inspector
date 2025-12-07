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

### 🎨 **Advanced Visualizations** ✨ NEW
- **Mermaid Flowcharts** (Recommended): Industry-standard diagrams with automatic validation and error correction
  - Auto-renders on GitHub, Notion, VS Code, and other platforms
  - 60% smaller file size vs matplotlib (58KB vs 149KB)
  - LLM-based error detection and auto-fix loop
  - Editable `.mmd` source files + rendered PNG
- **Matplotlib Flowcharts** (Legacy): Smart layout algorithm with collision-free arrow routing
- **Interactive Call Graphs**: NetworkX-powered function dependency visualization
- **Real-time Rendering**: Professional diagrams with optimized layouts

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
| **Visualization** | Mermaid.js + mermaid-cli 11.12.0 | Modern flowchart generation (primary) |
| **Legacy Viz** | Matplotlib 3.10.7 + NetworkX 3.6 | Fallback diagram generation |
| **Web UI** | Gradio 6.0.2 | Interactive web interface |
| **Language** | Python 3.11+ | Core implementation |
| **Runtime** | Node.js 25.2.1 (optional) | For Mermaid PNG rendering |

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

### 5. (Optional) Install Mermaid CLI for enhanced flowcharts
```bash
# Install Node.js first (if not installed)
brew install node  # macOS
# Or download from https://nodejs.org

# Install mermaid-cli globally
npm install -g @mermaid-js/mermaid-cli

# Verify installation
mmdc --version  # Should show 11.x.x
```

> **Note:** Without mermaid-cli, flowcharts will use matplotlib fallback. Mermaid provides cleaner, industry-standard diagrams.

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
- 📊 Tabbed results: Explanations | Analysis | Quality Score | Flowchart | Call Graph
- 🎨 Toggle between Mermaid (modern) and Matplotlib (legacy) flowcharts
- 💾 Download generated diagrams (.png and .mmd files)
- 🎯 Clean, professional UI for presentations

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
├── binary_search_flowchart_20250106_143022.png    # AI flowchart
├── binary_search_flowchart_20250106_143022.mmd    # Mermaid source (editable)
├── binary_search_flowchart_description.json       # Flowchart steps
└── binary_search_callgraph_20250106_143022.png    # Call graph
```

---

## 🆕 Recent Updates (December 2024)

### ✨ Mermaid Flowchart Integration
- **Hybrid approach**: LLM generates semantic descriptions → Mermaid syntax → Professional diagrams
- **Auto-validation**: Detects syntax errors before rendering
- **Error correction**: LLM-based auto-fix with retry loop (max 2 attempts)
- **Smart label cleaning**: Removes reserved keywords, special characters, and formatting issues
- **60% file size reduction**: 58KB vs 149KB for equivalent matplotlib flowcharts
- **Universal compatibility**: Auto-renders on GitHub, Notion, VS Code, Confluence, Obsidian
- **Editable source**: `.mmd` text files can be manually edited and re-rendered

### 🗂️ Project Restructuring
- **`docs/`**: All documentation and markdown files (16 files)
- **`tests/`**: All test scripts with updated imports (5 files)
- **Cleaner root**: Only essential files in project root
- **README files**: Added to docs/ and tests/ for navigation

### 🔧 Technical Improvements
- Fixed matplotlib arrow rendering (6 arrow types using `ax.annotate()`)
- Implemented reserved keyword detection (`end` → `endNode`)
- Label sanitization (removes `()`, `[]`, `??`, trailing `%`)
- Direct mmdc rendering with fallback to preview mode
- Updated Gradio UI with Mermaid/Matplotlib toggle

---

## 📚 Documentation

Comprehensive guides available in the `docs/` folder:
- **[MERMAID_SETUP.md](docs/MERMAID_SETUP.md)** - Complete Mermaid installation and usage guide
- **[MERMAID_COMPLETE.md](docs/MERMAID_COMPLETE.md)** - Technical details and troubleshooting
- **[QUICKSTART.md](docs/QUICKSTART.md)** - Quick start guide
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture details
- **[TESTING_GUIDE.md](docs/TESTING_GUIDE.md)** - How to run tests

See [docs/README.md](docs/README.md) for full documentation index.

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

### Key Innovation: Hybrid Flowchart Generation

**NEW: Mermaid Approach (Recommended)**
1. **LLM analyzes code** → Understands logic semantically
2. **Generates flowchart JSON** → Structured step-by-step description
3. **Converts to Mermaid** → Industry-standard syntax with auto-validation
4. **Renders with mmdc** → Professional PNG + editable .mmd source
5. **Auto-error correction** → LLM fixes syntax issues if validation fails

**Legacy: Matplotlib Approach (Fallback)**
1. **LLM analyzes code** → Understands logic semantically
2. **Generates structured JSON** → Step-by-step flowchart
3. **Smart layout** → BFS-based positioning
4. **Collision-free routing** → Guaranteed no overlaps

---

## 🌟 Key Highlights

- **🎨 Mermaid Integration**: Modern, industry-standard flowcharts with 60% smaller file sizes
- **🔄 Auto-Validation**: Syntax checking and LLM-based error correction
- **📝 Editable Diagrams**: `.mmd` source files can be edited and re-rendered
- **🌍 Universal Compatibility**: Auto-renders on GitHub, Notion, VS Code, Confluence
- **🚫 Collision-Free Visualizations**: Boxes spaced 8+ units horizontally, 4.5 units vertically
- **📊 Lightweight Knowledge Graph**: Pure JSON, no database required
- **🧩 Modular Multi-Agent Design**: Easy to extend and customize
- **💡 Natural Language Processing**: Beginner to expert explanations
- **🗂️ Clean Project Structure**: Organized docs/ and tests/ folders

---

## 🧪 Testing

Run tests from project root:
```bash
# Test Mermaid flowchart generation
python tests/test_mermaid_simple.py

# Compare Mermaid vs Matplotlib
python tests/test_hybrid_flowchart.py

# Full integration test
python tests/test_integration.py

# All tests
python run_tests.py
```

See [tests/README.md](tests/README.md) for detailed testing guide.

---

## 📄 License

MIT License

---

## 👤 Author

**Arun Munagala**
- GitHub: [@ArunMunagala7](https://github.com/ArunMunagala7)

---

**⭐ Star this repo if you find it useful!**
