# Multi-Agent Code Understanding System

An intelligent code analysis platform built with LangGraph and GPT-4o-mini that provides comprehensive code understanding through multi-agent orchestration, knowledge graph construction, and automated visualization.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0.4-green.svg)](https://github.com/langchain-ai/langgraph)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)
[![Gradio](https://img.shields.io/badge/Gradio-6.0.2-red.svg)](https://gradio.app)

---

## Overview

This system employs a multi-agent architecture to analyze source code and generate detailed explanations, visualizations, and quality assessments. The core innovation is the use of knowledge graphs as an intermediate representation that enables sophisticated code understanding and analysis.

**Key Capabilities:**
- Multi-level code explanations (beginner to expert)
- Automated bug and security vulnerability detection
- Visual flowchart and call graph generation
- Code quality scoring with detailed metrics
- LeetCode-style test case generation
- AI-powered code generation from natural language queries

---

## Architecture

### Multi-Agent Workflow

The system uses five specialized agents that execute sequentially, each building upon the previous agent's output:

```
Input Code
    ↓
┌─────────────────┐
│  Parse Agent    │  Extracts structural elements (functions, loops, variables)
└────────┬────────┘
         ↓
┌─────────────────┐
│  BuildKG Agent  │  Constructs JSON knowledge graph (nodes & edges)
└────────┬────────┘
         ↓
┌─────────────────┐
│ Analyze Agent   │  Detects bugs, complexity, security issues using KG
└────────┬────────┘
         ↓
┌─────────────────┐
│Visualize Agent  │  Generates Mermaid flowcharts and call graphs from KG
└────────┬────────┘
         ↓
┌─────────────────┐
│ Explain Agent   │  Creates multi-level explanations using KG insights
└────────┬────────┘
         ↓
    Output (6 tabs)
```

### Knowledge Graph Structure

The knowledge graph serves as the backbone data structure, representing code as a directed graph:

**Nodes:** Functions, loops, conditions, variables, function calls, return statements
**Edges:** Relationships such as "contains", "calls", "updates", "leads_to"

Example structure:
```json
{
  "nodes": [
    {"id": "f_binary_search", "type": "function", "label": "binary_search"},
    {"id": "loop_1", "type": "loop", "label": "while left <= right"},
    {"id": "cond_1", "type": "condition", "label": "arr[mid] == target"}
  ],
  "edges": [
    {"source": "f_binary_search", "target": "loop_1", "relation": "contains"},
    {"source": "loop_1", "target": "cond_1", "relation": "contains"}
  ]
}
```

This graph structure enables:
- Tracing execution paths for bug detection
- Generating accurate control flow diagrams
- Understanding data dependencies
- Providing context-aware explanations

---

## Features

### Core Analysis Capabilities

**1. Code Parsing and Structure Extraction**
- Identifies functions, classes, methods
- Extracts control flow (loops, conditionals, recursion)
- Captures variable assignments and updates
- Detects function calls and dependencies

**2. Knowledge Graph Construction**
- Lightweight JSON representation (no external database)
- Node-edge graph structure
- Relationship mapping (contains, calls, updates, leads_to)
- Serves as input for all downstream agents

**3. Comprehensive Code Analysis**
- Bug detection with severity classification (critical/high/medium/low)
- Security vulnerability identification (injection attacks, unsafe operations)
- Performance bottleneck detection
- Time and space complexity analysis (Big-O notation)
- Edge case identification (empty inputs, null handling, boundary conditions)
- Code smell and anti-pattern detection

**4. Visual Flowchart Generation**

Two rendering options:

**Mermaid (Recommended):**
- Industry-standard text-based diagram format
- 60% smaller file size compared to matplotlib (53KB vs 149KB)
- Auto-renders on GitHub, Notion, VS Code, Confluence
- Editable .mmd source files
- Intelligent label generation using LLM analysis
- Displays actual code conditions and operations
- Automatic syntax validation with error correction

**Matplotlib (Fallback):**
- Programmatic diagram generation
- Custom layout algorithm
- Collision-free arrow routing
- Suitable for offline environments

**5. Call Graph Visualization**
- Function dependency mapping
- Built from knowledge graph edges
- NetworkX-based graph rendering
- Shows "caller → callee" relationships

**6. Code Quality Metrics**
- Readability score (0-10 scale)
- Maintainability score (0-10 scale)
- Detailed justifications for each metric
- Identification of maintainability issues

**7. Test Case Generation**
- Generates 8-12 test cases in LeetCode format
- Structure: Input → Output → Explanation
- Covers normal cases, edge cases, boundary conditions, error scenarios
- Based on detected bugs and edge cases from analysis
- Copy-paste ready for immediate use

**8. Code Generation from Questions**
- Natural language query → Production-ready code
- Supports Python, JavaScript, Java, C++, Go, Rust
- Generates clean, commented, idiomatic code
- Immediate analysis of generated solution

---

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Orchestration | LangGraph | 1.0.4 | Multi-agent workflow management |
| LLM | OpenAI GPT-4o-mini | Latest | Natural language understanding and generation |
| Web Framework | Gradio | 6.0.2 | Interactive web interface |
| Diagrams | Mermaid.js | 11.12.0 | Flowchart generation and rendering |
| Graph Library | NetworkX | Latest | Call graph construction |
| Visualization | Matplotlib | Latest | Fallback diagram rendering |
| Type Validation | Pydantic | Latest | State management and validation |
| Language | Python | 3.11+ | Core implementation |

**Supported Languages for Analysis:**
- Python
- JavaScript
- Java
- C++
- Go
- Rust

---

## Installation

### Prerequisites
- Python 3.11 or higher
- Node.js (for Mermaid CLI, optional)
- OpenAI API key

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/ArunMunagala7/langgraph-code-inspector.git
cd langgraph-code-inspector
```

2. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Configure OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your API key:
# OPENAI_API_KEY=sk-your-key-here
```

5. (Optional) Install Mermaid CLI for enhanced diagrams:
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc --version  # Verify installation
```

---

## Usage

### Web Interface (Primary Method)

Start the Gradio server:
```bash
python app.py
```

Access at `http://localhost:7860`

**Interface Features:**
- Code input via text area, file upload (.py, .js, .java, .cpp, .ipynb), or sample selection
- Code generation panel for natural language queries
- Real-time analysis with progress tracking (8-15 seconds typical)
- Six output tabs:
  1. Explanations (multi-level breakdown)
  2. Analysis (bugs, edge cases, complexity)
  3. Quality Score (metrics and recommendations)
  4. Flowchart (algorithm visualization)
  5. Call Graph (function dependencies)
  6. Generated Tests (LeetCode-format test cases)
- Export options for diagrams (.png, .mmd) and analysis (JSON)
- Mermaid/Matplotlib toggle for flowchart rendering

### Command Line Interface

Interactive mode:
```bash
python main.py
```

Analyze specific samples:
```bash
python main.py --sample python_binary_search --generate-images
python main.py --sample python_merge_sort --generate-images
```

Available samples:
- python_two_sum
- python_fibonacci  
- python_binary_search
- python_bubble_sort
- python_merge_sort
- python_quick_sort
- python_dfs
- python_bfs
- python_dijkstra
- python_lcs

---

## System Workflow

### Detailed Agent Pipeline

**Stage 1: Parse Agent**
- Input: Raw source code + language identifier
- Processing: Structural analysis to extract functions, loops, conditions, variables
- Output: Parsed structure (JSON dictionary)
- LLM Usage: Code structure extraction

**Stage 2: BuildKG Agent**  
- Input: Parsed structure from Stage 1
- Processing: Converts parsed structure into knowledge graph representation
- Output: Knowledge graph (nodes and edges in JSON)
- LLM Usage: Graph construction and relationship mapping

**Stage 3: Analyze Agent**
- Input: Knowledge graph + original code
- Processing: Traverses KG to detect bugs, complexity, security issues
- Output: Analysis results (bugs, edge cases, suggestions, complexity)
- LLM Usage: Deep code analysis using KG context

**Stage 4: Visualize Agent**
- Input: Knowledge graph + parsed structure
- Processing: Generates Mermaid diagram syntax from KG structure
- Output: Mermaid diagram code + call graph data
- LLM Usage: Intelligent label generation for diagram nodes

**Stage 5: Explain Agent**
- Input: Knowledge graph + analysis results
- Processing: Creates explanations at multiple abstraction levels
- Output: Multi-level explanations (simple, technical, detailed)
- LLM Usage: Natural language explanation generation

### Data Flow

```
Code Input (string)
      ↓
[Parse Agent] → parsed_structure (dict)
      ↓
[BuildKG Agent] → knowledge_graph (dict)
      ↓
      ├─→ [Analyze Agent] → analysis (dict)
      │         ↓
      ├─→ [Visualize Agent] → diagrams (Mermaid/PNG)
      │         ↓
      └─→ [Explain Agent] → explanations (dict)
            ↓
Final State (all outputs combined)
      ↓
Web UI Rendering (6 tabs)
```

---

## Project Structure

```
langgraph-code-inspector/
├── agents/              # AI agent implementations
│   ├── parse_agent.py
│   ├── kg_agent.py
│   ├── analyze_agent.py
│   ├── visualize_agent.py
│   ├── explain_agent.py
│   └── quality_agent.py
├── core/               # Core functionality
│   ├── prompts.py      # LLM prompt templates
│   ├── state.py        # State management (Pydantic)
│   ├── mermaid_generator_v3.py  # Intelligent flowchart generation
│   ├── diagram_generator.py     # Call graph generation
│   └── utils.py        # Utility functions
├── graph/              # LangGraph workflow
│   └── workflow.py     # Agent orchestration
├── data/               # Sample code library
│   └── samples.py
├── app.py             # Gradio web interface
├── main.py            # CLI interface
└── requirements.txt   # Python dependencies
```

---

## Technical Implementation Details

### State Management

The system uses a TypedDict schema for state management across agents:

```python
class CodeInspectorState(TypedDict):
    code: str                    # Original source code
    language: str                # Programming language
    parsed_structure: dict       # Extracted code structure
    knowledge_graph: dict        # Graph representation
    analysis: dict               # Analysis results
    explanations: dict           # Generated explanations
    visualizations: dict         # Diagram outputs
```

Each agent reads from and writes to specific fields in this shared state.

### Prompt Engineering

The system uses structured prompts with JSON schema specifications to ensure consistent LLM outputs:

- **Parse Prompt**: Structured extraction of code elements
- **BuildKG Prompt**: Node-edge graph construction rules
- **Analyze Prompt**: Comprehensive analysis template with severity levels
- **Visualize Prompt**: Mermaid syntax generation guidelines
- **Explain Prompt**: Multi-level explanation structure

All prompts use temperature=0.3 for consistency and include few-shot examples.

### Mermaid Generation Algorithm

Version 3 intelligent flowchart generation process:

1. **Structure Extraction**: Direct code parsing (no LLM for structure)
2. **Label Generation**: LLM analyzes code semantics to create specific labels
3. **Condition Extraction**: Regex patterns extract actual condition text
4. **Graph Construction**: Mermaid syntax generation from extracted data
5. **Validation**: LLM-based syntax checking
6. **Error Correction**: Automatic fix loop (max 3 attempts)
7. **Rendering**: Execute mmdc command to generate PNG

### Performance Characteristics

- Average analysis time: 8-15 seconds
- Optimized for code snippets: 10-200 lines
- Knowledge graph overhead: Minimal (pure JSON, no database)
- Concurrent request support: Multiple simultaneous analyses
- API cost per analysis: ~$0.02-0.05 (OpenAI pricing)

---

## Future Enhancements

**Short-term:**
- Code comparison feature (diff analysis between versions)
- Interactive learning mode with step-by-step walkthroughs
- Enhanced dependency graph analysis with version tracking

**Medium-term:**
- Extended language support (Swift, Kotlin, TypeScript)
- Code metrics dashboard (cyclomatic complexity, LOC, coupling)
- Result caching and analysis history

**Long-term:**
- Repository-level analysis with cross-file dependency tracking
- IDE plugin integration (VS Code, PyCharm)
- Custom rule engine for domain-specific analysis

---

## License

MIT License - see LICENSE file for details

---

## Acknowledgments

Built using:
- LangGraph by LangChain
- OpenAI GPT-4o-mini API
- Gradio web framework
- Mermaid.js diagramming library
- NetworkX graph library

---

## Contact

**Author:** Arun Munagala  
**GitHub:** [@ArunMunagala7](https://github.com/ArunMunagala7)  
**Repository:** [langgraph-code-inspector](https://github.com/ArunMunagala7/langgraph-code-inspector)

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

**Core Features:**
- 📝 **Code Input**: Paste code, upload files (.py, .js, .java, .cpp), or select from 10+ samples
- ❓ **NEW: Code Generation**: Enter questions like "Write merge sort" → Get instant solutions
- 🔄 **Real-time Analysis**: Progress indicators for each agent (8-15 seconds total)
- 📊 **6 Result Tabs**:
  1. 💬 Explanations (Simple → Technical breakdown)
  2. 🔍 Analysis (Bugs, edge cases, complexity)
  3. ⭐ Quality Score (Metrics & recommendations)
  4. 📈 Flowchart (Algorithm visualization)
  5. 🕸️ Call Graph (Function dependencies)
  6. 🧪 **NEW: Generated Tests** (LeetCode-style test cases)
- 🎨 **Toggle Visualizations**: Mermaid (modern) vs Matplotlib (legacy)
- 💾 **Export**: Download diagrams (.png, .mmd) and analysis JSON
- 🎯 **Clean UI**: Professional interface for demos & presentations

**Quick Demo Flow:**
1. Click "Load Sample Code" → Select "Binary Search"
2. Click "🚀 Analyze Code"
3. Navigate through 6 tabs to see comprehensive analysis
4. Try **Code Generation**: Enter "Write a BFS for graphs" → Analyze generated code

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

### ✨ **Key Technical Achievements**

**1. Knowledge Graph Architecture**
- Lightweight JSON structure (no database required)
- Powers all analysis, visualization, and explanations
- Enables deep code understanding through graph traversal
- Nodes: Functions, loops, conditions, variables, calls
- Edges: Relationships (contains, calls, updates, leads_to)

**2. Mermaid Flowchart Generator v3** - Intelligent Diagram Generation
- **Structure-Aware**: Direct code parsing (NO LLM template copying)
- **Intelligent Labels**: LLM analyzes code semantics for specific operation names
  - Examples: "Find Two Sum", "Sort Algorithm", "Calculate LCS", "Search Array"
- **Real Conditions**: Shows actual conditions from code
  - Examples: `arr[mid] == target`, `complement in seen`, `arr[j] > arr[j + 1]`
- **Operation Context**: Displays variable assignments and operations
- **Auto-Validation**: LLM-based syntax checking with error correction
- **60% smaller files**: 53KB vs 149KB compared to matplotlib
- **Universal compatibility**: Auto-renders on GitHub, Notion, VS Code

**3. Test Case Generation System**
- LeetCode-format test cases (Input → Output → Explanation)
- Covers normal, edge, boundary, and error scenarios
- Based on AI analysis of code bugs and edge cases
- 8-12 comprehensive test cases per code snippet
- Copy-paste ready for interviews and practice

**4. Code Generation from Questions**
- Natural language → Production-ready code
- Supports 6 languages (Python, JavaScript, Java, C++, Go, Rust)
- Clean, commented, idiomatic code
- Immediate analysis of generated solutions

**5. Multi-Agent Orchestration**
- Sequential workflow: Parse → BuildKG → Analyze → Visualize → Explain
- State management with TypedDict
- Knowledge Graph shared across all agents
- Modular design for easy extension

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
