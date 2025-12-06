"""
Prompt templates for all agents in the system.
"""

PARSE_CODE_PROMPT = """You are a code parsing expert. Analyze the following code and extract its structural components.

Language: {language}
Code:
```
{code}
```

Extract and return a JSON object with the following structure:
{{
  "functions": [list of function names],
  "loops": [list of loop descriptions, e.g., "for x in arr"],
  "conditions": [list of conditional statements],
  "variables": [list of variable names],
  "calls": [list of function calls],
  "returns": [list of return statements],
  "assignments": [list of variable assignments/updates],
  "operations": [list of key operations]
}}

Be thorough and precise. Return ONLY the JSON object, no additional text.
"""

BUILD_KG_PROMPT = """You are a knowledge graph construction expert. Convert the parsed code structure into a lightweight JSON knowledge graph.

Language: {language}
Code:
```
{code}
```

Parsed Structure:
{parsed_structure}

Create a knowledge graph with nodes and edges. Use these node types:
- function
- loop
- condition
- variable
- call
- update
- return
- operation
- error (if potential errors exist)

Use these edge relation types:
- contains
- calls
- compares
- updates
- initializes
- returns
- leads_to
- may_cause (for errors)

Return a JSON object with this exact structure:
{{
  "nodes": [
    {{"id": "unique_id", "type": "node_type", "label": "descriptive_label"}},
    ...
  ],
  "edges": [
    {{"source": "source_node_id", "target": "target_node_id", "relation": "relation_type"}},
    ...
  ]
}}

Be comprehensive. Create meaningful node IDs (e.g., "f_sum_array", "loop_1", "var_total").
Return ONLY the JSON object, no additional text.
"""

ANALYZE_PROMPT = """You are a code analysis expert. Using the knowledge graph and code, identify potential issues and provide insights.

Language: {language}
Code:
```
{code}
```

Knowledge Graph:
{knowledge_graph}

Analyze the code and return a JSON object with:
{{
  "bugs": [list of potential bugs with descriptions],
  "edge_cases": [list of edge cases to consider],
  "complexity": {{
    "time": "Big O time complexity",
    "space": "Big O space complexity"
  }},
  "suggestions": [list of improvement suggestions],
  "anti_patterns": [list of code smells or anti-patterns]
}}

Be thorough but concise. Return ONLY the JSON object, no additional text.
"""

VISUALIZE_PROMPT = """You are a code visualization expert. Generate Mermaid diagrams based on the code structure and knowledge graph.

Language: {language}
Code:
```
{code}
```

Parsed Structure:
{parsed_structure}

Knowledge Graph:
{knowledge_graph}

Generate TWO Mermaid diagrams:

1. **Flowchart**: Show the control flow with proper symbols
2. **Call Graph**: Show code structure and relationships

Return a JSON object with:
{{
  "flowchart": "flowchart syntax",
  "call_graph": "graph syntax or empty string"
}}

MERMAID FLOWCHART SYNTAX (use these shapes):
- Start/End nodes: Start([Start]) and End([End])
- Process boxes: Step[Do something]
- Decision diamonds: Check{{Question?}}  
- Note: Use SINGLE curly braces {{ }} for diamonds in the actual Mermaid syntax

FLOWCHART RULES:
1. Start with: Start([Start])
2. End with: End([End])
3. Decisions use: Name{{Question?}}
4. Label branches: -->|Yes|, -->|No|, -->|True|, -->|False|
5. Show loops with back arrows
6. Use descriptive names

CRITICAL FOR JSON:
- The curly braces in Mermaid diamond syntax {{text}} will be automatically handled
- Just write them normally: Check{{Is valid?}}
- Do NOT escape them as {{{{text}}}}
- Do NOT use double quotes inside node labels

Example (copy this style):
flowchart TD
    Start([Start])
    Start --> Init[Initialize counter]
    Init --> Check{{Has items?}}
    Check -->|Yes| Process[Process item]
    Process --> Update[Increment counter]
    Update --> Check
    Check -->|No| Done[Return result]
    Done --> End([End])

Example with nested conditions:
flowchart TD
    Start([Start])
    Start --> Read[Get input]
    Read --> Validate{{Is valid?}}
    Validate -->|No| Error[Show error]
    Error --> End([End])
    Validate -->|Yes| CheckType{{Is positive?}}
    CheckType -->|Yes| PosPath[Handle positive]
    CheckType -->|No| NegPath[Handle negative]
    PosPath --> Output[Display result]
    NegPath --> Output
    Output --> End

CALL GRAPH RULES:
1. Use 'graph LR' for left-to-right or 'graph TD' for top-down
2. ALL node IDs must be wrapped in quotes if they contain underscores or special chars
3. Use square brackets for labels: "node_id"[Label Text]
4. Arrows: --> for connections
5. Keep it simple and readable

Call graph examples:
graph LR
    "binary_search"[binary_search] --> "var_arr"[arr]
    "binary_search"[binary_search] --> "var_target"[target]
    "var_left"[left] --> "loop_1"[while loop]
    
OR simpler without underscores:
graph TD
    main[Main Function]
    helper[Helper Function]
    util[Utility]
    main --> helper
    helper --> util
    
Return ONLY valid JSON with these two fields. Ensure all Mermaid syntax is valid.
"""

EXPLAIN_PROMPT = """You are a code explanation expert. Generate multi-level explanations for the code.

Language: {language}
Code:
```
{code}
```

Knowledge Graph:
{knowledge_graph}

Analysis:
{analysis}

Generate explanations at multiple levels and return a JSON object:
{{
  "simple": "A simple 1-2 sentence explanation for beginners",
  "technical": "A technical explanation for developers (2-3 sentences)",
  "line_by_line": [
    {{"line": 1, "code": "actual code line", "explanation": "what this line does"}},
    ...
  ],
  "summary": "A brief summary of the code's purpose and approach"
}}

Be clear, accurate, and educational. Return ONLY the JSON object, no additional text.
"""
