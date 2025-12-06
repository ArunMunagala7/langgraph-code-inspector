# System Architecture

## High-Level Architecture Diagram

```mermaid
graph TB
    User[👤 User] -->|Code Input| CLI[🖥️ main.py CLI]
    CLI --> Workflow[🔄 LangGraph Workflow]
    
    Workflow --> Parse[🔍 ParseCodeAgent]
    Parse --> KG[📊 BuildKGAgent]
    KG --> Analyze[🔬 AnalyzeAgent]
    Analyze --> Visualize[📈 VisualizeAgent]
    Visualize --> Explain[📝 ExplainAgent]
    
    Parse -.->|Updates| State[(📦 Shared State)]
    KG -.->|Updates| State
    Analyze -.->|Updates| State
    Visualize -.->|Updates| State
    Explain -.->|Updates| State
    
    State --> Output[📄 Output Formatter]
    Output --> Console[💻 Console Display]
    Output --> JSON[💾 JSON File]
    
    Parse --> OpenAI[🤖 OpenAI API]
    KG --> OpenAI
    Analyze --> OpenAI
    Visualize --> OpenAI
    Explain --> OpenAI
```

## Agent Flow Diagram

```mermaid
flowchart TD
    Start([🚀 Start]) --> Input[📝 Code Input]
    Input --> Detect{Auto-detect<br/>Language?}
    Detect -->|Yes| Auto[🔍 Language Detection]
    Detect -->|No| Manual[✍️ Use Provided Language]
    Auto --> Init[⚙️ Initialize State]
    Manual --> Init
    
    Init --> Agent1[🔍 ParseCodeAgent]
    Agent1 -->|Extract Structure| Agent2[📊 BuildKGAgent]
    Agent2 -->|Build Graph| Agent3[🔬 AnalyzeAgent]
    Agent3 -->|Analyze| Agent4[📈 VisualizeAgent]
    Agent4 -->|Generate Diagrams| Agent5[📝 ExplainAgent]
    
    Agent5 --> Format[🎨 Format Output]
    Format --> Display[💻 Display Results]
    Format --> Save{Save to<br/>File?}
    Save -->|Yes| File[💾 Save JSON]
    Save -->|No| Skip[⏭️ Skip]
    
    File --> End([✅ Complete])
    Skip --> End
    Display --> End
```

## Data Flow Diagram

```mermaid
graph LR
    subgraph Input
        Code[Source Code]
        Lang[Language]
    end
    
    subgraph "Agent Pipeline"
        A1[Parse] --> A2[Build KG]
        A2 --> A3[Analyze]
        A3 --> A4[Visualize]
        A4 --> A5[Explain]
    end
    
    subgraph State
        S1[parsed_structure]
        S2[knowledge_graph]
        S3[analysis]
        S4[flowchart<br/>call_graph]
        S5[explanations]
    end
    
    subgraph Output
        O1[Console Text]
        O2[JSON File]
    end
    
    Code --> A1
    Lang --> A1
    A1 --> S1
    S1 --> A2
    A2 --> S2
    S2 --> A3
    A3 --> S3
    S3 --> A4
    A4 --> S4
    S4 --> A5
    A5 --> S5
    
    S1 --> O1
    S2 --> O1
    S3 --> O1
    S4 --> O1
    S5 --> O1
    
    S1 --> O2
    S2 --> O2
    S3 --> O2
    S4 --> O2
    S5 --> O2
```

## Knowledge Graph Structure

```mermaid
graph TD
    Function[🔧 Function Node] -->|contains| Loop[🔁 Loop Node]
    Function -->|initializes| Var1[📦 Variable: total]
    Loop -->|iterates_over| Var2[📦 Variable: arr]
    Loop -->|updates| Var1
    Function -->|returns| Return[↩️ Return Node]
    Return -->|value| Var1
    
    style Function fill:#e1f5ff
    style Loop fill:#fff4e1
    style Var1 fill:#e8f5e9
    style Var2 fill:#e8f5e9
    style Return fill:#fce4ec
```

## Component Interaction

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Workflow
    participant Agents
    participant OpenAI
    participant State
    participant Output
    
    User->>CLI: Provide code
    CLI->>Workflow: Initialize workflow
    Workflow->>State: Create initial state
    
    loop For each agent
        Workflow->>Agents: Execute agent
        Agents->>OpenAI: Send prompt
        OpenAI-->>Agents: Return analysis
        Agents->>State: Update state
    end
    
    Workflow->>Output: Format results
    Output->>User: Display console output
    Output->>User: Save JSON file
```

## State Transition Diagram

```mermaid
stateDiagram-v2
    [*] --> Initial: User Input
    Initial --> Parsing: ParseCodeAgent
    Parsing --> Building: BuildKGAgent
    Building --> Analyzing: AnalyzeAgent
    Analyzing --> Visualizing: VisualizeAgent
    Visualizing --> Explaining: ExplainAgent
    Explaining --> Complete: Output
    Complete --> [*]
    
    state Initial {
        language
        code
    }
    
    state Parsing {
        parsed_structure
    }
    
    state Building {
        knowledge_graph
    }
    
    state Analyzing {
        analysis
    }
    
    state Visualizing {
        flowchart
        call_graph
    }
    
    state Explaining {
        explanations
    }
```

## Directory Structure

```
langgraph-code-inspector/
│
├── 📁 agents/              # Agent implementations
│   ├── parse_agent.py      # Extract code structure
│   ├── kg_agent.py         # Build knowledge graph
│   ├── analyze_agent.py    # Analyze code quality
│   ├── visualize_agent.py  # Generate diagrams
│   └── explain_agent.py    # Create explanations
│
├── 📁 graph/               # LangGraph workflow
│   └── workflow.py         # Workflow orchestration
│
├── 📁 core/                # Core utilities
│   ├── state.py            # State definition
│   ├── prompts.py          # LLM prompts
│   └── utils.py            # Helper functions
│
├── 📁 data/                # Data and samples
│   ├── samples.py          # Sample code snippets
│   └── samples.json        # Generated samples
│
├── 📁 outputs/             # Generated analyses
│   └── analysis_*.json     # Timestamped results
│
├── 📄 main.py              # CLI entry point
├── 📄 demo.py              # Demo script
├── 📄 requirements.txt     # Dependencies
├── 📄 .env                 # API configuration
├── 📄 README.md            # Main documentation
├── 📄 QUICKSTART.md        # Quick start guide
└── 📄 DOCUMENTATION.md     # Detailed docs
```

## Technology Stack

```mermaid
graph TB
    subgraph "Frontend Layer"
        CLI[Command Line Interface]
    end
    
    subgraph "Application Layer"
        LG[LangGraph<br/>Workflow Engine]
        Agents[5 Specialized Agents]
    end
    
    subgraph "AI Layer"
        OpenAI[OpenAI API<br/>GPT-4o-mini]
    end
    
    subgraph "Data Layer"
        State[In-Memory State]
        JSON[JSON Output]
    end
    
    subgraph "Visualization"
        Mermaid[Mermaid.js<br/>Diagrams]
    end
    
    CLI --> LG
    LG --> Agents
    Agents --> OpenAI
    Agents --> State
    State --> JSON
    Agents --> Mermaid
```

## Prompt Engineering Flow

```mermaid
graph LR
    Code[Source Code] --> Template[Prompt Template]
    Context[Context Data] --> Template
    Template --> Prompt[Formatted Prompt]
    Prompt --> LLM[OpenAI LLM]
    LLM --> Response[Raw Response]
    Response --> Parse[JSON Parser]
    Parse --> Valid{Valid JSON?}
    Valid -->|Yes| Result[Structured Result]
    Valid -->|No| Error[Error Handler]
    Error --> Retry[Retry Logic]
    Retry --> LLM
```

## Error Handling Strategy

```mermaid
graph TD
    Start[Agent Execution] --> Try{Try Block}
    Try -->|Success| Parse[Parse Response]
    Try -->|Exception| Catch[Catch Exception]
    
    Parse --> Valid{Valid JSON?}
    Valid -->|Yes| Return[Return Result]
    Valid -->|No| JSONError[JSON Parse Error]
    
    Catch --> Log[Log Error]
    JSONError --> Log
    Log --> Display[Display Error Message]
    Display --> End[End Gracefully]
    
    Return --> Next[Next Agent]
```

---

*These diagrams provide a visual representation of the system architecture and can be rendered using Mermaid.js in any compatible viewer.*
