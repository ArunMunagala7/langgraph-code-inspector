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

ANALYZE_PROMPT = """You are a comprehensive code analysis expert. Analyze the code deeply using the knowledge graph and identify issues, performance concerns, and improvements.

Language: {language}
Code:
```
{code}
```

Knowledge Graph:
{knowledge_graph}

Analyze the code thoroughly and return a JSON object with DETAILED information:
{{
  "bugs": [
    {{
      "description": "What the bug is",
      "severity": "critical/high/medium/low",
      "when_triggered": "Under what conditions this occurs",
      "impact": "What happens when this bug occurs",
      "fix": "How to fix this bug with a brief code example"
    }},
    ...
  ],
  "edge_cases": [
    {{
      "case": "Description of edge case",
      "expected_behavior": "What should happen",
      "current_behavior": "What currently happens or might happen",
      "fix": "How to handle this case"
    }},
    ...
  ],
  "complexity": {{
    "time": "Big O time complexity with explanation",
    "space": "Big O space complexity with explanation",
    "bottlenecks": "Key performance bottlenecks in the code",
    "optimizations": ["Possible optimizations to improve performance"]
  }},
  "performance_issues": [
    {{
      "issue": "What the performance issue is",
      "impact": "How it affects performance",
      "fix": "Suggested optimization"
    }},
    ...
  ],
  "security_concerns": [
    {{
      "concern": "Security risk description",
      "risk_level": "high/medium/low",
      "example": "Example scenario where this could be problematic",
      "mitigation": "How to mitigate this risk"
    }},
    ...
  ],
  "code_quality": {{
    "readability_score": "1-10 rating",
    "readability_reasons": "Why this score (specific observations)",
    "maintainability_score": "1-10 rating",
    "maintainability_reasons": "Why this score (specific observations)",
    "maintainability_issues": ["List of issues that make code hard to maintain"]
  }},
  "suggestions": [
    {{
      "suggestion": "Improvement recommendation",
      "priority": "critical/high/medium/low",
      "benefit": "What improves (readability/performance/maintainability/correctness)",
      "before_code": "Current approach (code snippet)",
      "after_code": "Improved approach (code snippet)"
    }},
    ...
  ],
  "anti_patterns": [
    {{
      "pattern": "Code smell or anti-pattern name",
      "description": "Why this is problematic",
      "impact": "Negative consequences",
      "refactoring": "How to refactor this"
    }},
    ...
  ],
  "test_coverage": {{
    "recommended_test_cases": [
      {{
        "case_name": "Name of test case",
        "input": "Test input",
        "expected_output": "Expected output",
        "purpose": "Why this test is important"
      }},
      ...
    ]
  }},
  "summary": "Overall assessment of code quality, key strengths, and main areas for improvement"
}}

Be thorough, detailed, and specific with examples. Return ONLY the JSON object, no additional text.
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

EXPLAIN_PROMPT = """You are a comprehensive code explanation expert. Generate detailed multi-level explanations for the code.

Language: {language}
Code:
```
{code}
```

Knowledge Graph:
{knowledge_graph}

Analysis:
{analysis}

Generate comprehensive explanations and return a JSON object:
{{
  "simple": "A simple 1-2 sentence explanation suitable for beginners or non-programmers",
  "technical": "A detailed technical explanation for developers (4-5 sentences), covering the algorithm/approach",
  "purpose": "What is the code trying to accomplish? What problem does it solve?",
  "use_case": "Real-world scenarios where this code pattern or algorithm is used",
  "key_concepts": [
    {{
      "concept": "Name of the algorithm/technique/pattern used (e.g., 'Two-pointer', 'Memoization', 'Binary Search')",
      "explanation": "Brief explanation of what this concept is and how it's applied in this code",
      "importance": "Why this concept is important or useful in this context"
    }},
    ...
  ],
  "sections": [
    {{
      "section_name": "Name of code section (e.g., 'Initialization', 'Main Loop', 'Validation', 'Return Logic')",
      "code_lines": "Which lines comprise this section (e.g., 'lines 1-5')",
      "purpose": "What does this section do?",
      "detailed_explanation": "Detailed explanation (3-4 sentences) of what happens in this section and why",
      "key_operations": ["List of key operations/variables/logic in this section"]
    }},
    ...
  ],
  "data_structures": [
    {{
      "structure": "Name of data structure (e.g., 'array', 'dictionary', 'stack')",
      "usage": "How is this data structure used?",
      "why_chosen": "Why is this data structure appropriate for this code?"
    }},
    ...
  ],
  "complexity_insight": {{
    "time_complexity_explanation": "Why is the time complexity what it is? Walk through the reasoning",
    "space_complexity_explanation": "Why is the space complexity what it is?",
    "scalability": "How does this code perform as input size grows?"
  }},
  "learning_points": [
    "Key takeaway 1 that developers should learn from this code",
    "Key takeaway 2",
    "Key takeaway 3"
  ],
  "summary": "A comprehensive summary covering purpose, approach, key algorithms, complexity characteristics, and the main insight of the code (5-7 sentences)"
}}

Be clear, detailed, accurate, and educational. Include multiple sections for different code blocks/logical parts.
Return ONLY the JSON object, no additional text.
"""
