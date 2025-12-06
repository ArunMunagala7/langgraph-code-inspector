# 📖 Project Documentation

## Overview

This document provides detailed information about the **Multi-Agent Code Understanding System** implementation.

## System Design

### State Management

The system uses a shared state object (`CodeInspectorState`) that is passed through all agents in the LangGraph workflow:

```python
class CodeInspectorState(TypedDict):
    language: str                    # Programming language
    code: str                        # Source code
    parsed_structure: Optional[Dict] # Extracted components
    knowledge_graph: Optional[Dict]  # JSON KG
    analysis: Optional[Dict]         # Bug analysis
    flowchart: Optional[str]        # Mermaid flowchart
    call_graph: Optional[str]       # Mermaid call graph
    explanations: Optional[Dict]     # Multi-level explanations
```

### Agent Responsibilities

#### 1. ParseCodeAgent
**Input**: `language`, `code`  
**Output**: `parsed_structure`

Extracts:
- Function definitions
- Loop constructs
- Conditional statements
- Variable declarations
- Function calls
- Return statements
- Assignments and operations

#### 2. BuildKGAgent
**Input**: `language`, `code`, `parsed_structure`  
**Output**: `knowledge_graph`

Creates a JSON knowledge graph with:
- **Nodes**: function, loop, condition, variable, call, update, return, operation, error
- **Edges**: contains, calls, compares, updates, initializes, returns, leads_to, may_cause

#### 3. AnalyzeAgent
**Input**: `language`, `code`, `knowledge_graph`  
**Output**: `analysis`

Provides:
- Potential bugs
- Edge cases to consider
- Time complexity (Big-O)
- Space complexity (Big-O)
- Improvement suggestions
- Anti-patterns detection

#### 4. VisualizeAgent
**Input**: `language`, `code`, `parsed_structure`, `knowledge_graph`  
**Output**: `flowchart`, `call_graph`

Generates:
- **Flowchart**: Control flow visualization
- **Call Graph**: Function relationship diagram

Both in Mermaid syntax for easy rendering.

#### 5. ExplainAgent
**Input**: `language`, `code`, `knowledge_graph`, `analysis`  
**Output**: `explanations`

Produces:
- **Simple**: Beginner-friendly explanation (1-2 sentences)
- **Technical**: Developer-focused explanation (2-3 sentences)
- **Line-by-line**: Detailed breakdown of each line
- **Summary**: Overall purpose and approach

## Workflow Execution

### Sequential Flow

```
1. User provides code
2. Language detection (if not specified)
3. Initialize state
4. Execute agents in sequence:
   - ParseCodeAgent
   - BuildKGAgent
   - AnalyzeAgent
   - VisualizeAgent
   - ExplainAgent
5. Format and display results
6. Save to JSON file
```

### Why Sequential?

Although some agents could theoretically run in parallel (e.g., VisualizeAgent and AnalyzeAgent), we use a sequential flow because:
1. Simpler debugging
2. Clearer progress tracking
3. Better error handling
4. LangGraph manages state transitions cleanly

## LLM Configuration

### Model Selection
- **Default**: GPT-4o-mini
- **Temperature**: 0.0 (deterministic)
- **Why GPT-4o-mini**: 
  - Cost-effective
  - Fast responses
  - Sufficient for code analysis tasks
  - Better for JSON output formatting

### Prompt Engineering

All prompts follow a consistent pattern:
1. Role definition ("You are a code parsing expert...")
2. Context (language, code, previous analysis)
3. Clear task specification
4. Structured output format (JSON schema)
5. Explicit instruction: "Return ONLY the JSON object, no additional text"

## Knowledge Graph Schema

### Node Types
```json
{
  "id": "unique_identifier",
  "type": "node_type",
  "label": "human_readable_label"
}
```

**Node Types**:
- `function` - Function definitions
- `loop` - For/while loops
- `condition` - If/else statements
- `variable` - Variable declarations
- `call` - Function calls
- `update` - Variable updates
- `return` - Return statements
- `operation` - Arithmetic/logical operations
- `error` - Potential error sources

### Edge Types
```json
{
  "source": "source_node_id",
  "target": "target_node_id",
  "relation": "relation_type"
}
```

**Relation Types**:
- `contains` - Structural containment
- `calls` - Function invocation
- `compares` - Comparison operations
- `updates` - Variable modification
- `initializes` - Variable initialization
- `returns` - Return value
- `leads_to` - Control flow
- `may_cause` - Potential error

## Output Format

### Console Output
Formatted sections:
1. Code display
2. Explanations (simple, technical, summary)
3. Analysis (bugs, edge cases, complexity, suggestions)
4. Flowchart (Mermaid)
5. Call Graph (Mermaid)
6. KG summary (node/edge counts)

### JSON Output
Complete state object with all analysis results, saved to `outputs/` directory.

## Testing Strategy

### Built-in Samples
Five curated examples covering:
1. **Simple iteration** (sum_array) - Basic loops
2. **Recursion** (fibonacci) - Recursive calls, potential bugs
3. **Algorithm** (binary_search) - Complex control flow
4. **Functional** (factorial) - JavaScript example
5. **Sorting** (bubble_sort) - Nested loops

### Testing Checklist
- ✅ Simple functions work correctly
- ✅ Recursive functions handled properly
- ✅ Bug detection works (negative input handling)
- ✅ Complexity analysis accurate
- ✅ Edge cases identified
- ✅ Diagrams generated correctly
- ✅ Multi-language support

## Performance Considerations

### API Calls
Each analysis makes **5 sequential API calls** (one per agent).

**Optimization opportunities**:
- Caching repeated code analysis
- Batch processing multiple files
- Async API calls (requires LangGraph modifications)

### Token Usage
Approximate tokens per analysis:
- Input: ~500-1000 tokens (code + prompts)
- Output: ~1000-2000 tokens (all responses)
- Total: ~2000-4000 tokens per analysis

**Cost estimate** (GPT-4o-mini):
- ~$0.001-0.002 per analysis
- Very cost-effective for demonstrations

## Error Handling

### Common Issues

1. **API Key not found**
   - Solution: Check `.env` file exists and contains valid key

2. **Import errors**
   - Solution: Ensure virtual environment is activated

3. **JSON parsing errors**
   - Solution: LLM occasionally returns malformed JSON; retry or adjust temperature

4. **Long code snippets**
   - Limitation: Optimized for 10-100 lines; larger code may exceed context

## Extension Ideas

### Easy Extensions
1. Add more sample code
2. Support additional languages
3. Customize prompt templates
4. Add CLI color output
5. Generate HTML reports

### Advanced Extensions
1. **Multi-file analysis** - Analyze entire projects
2. **Persistent storage** - Save KGs to database
3. **Interactive visualization** - Web UI for KG exploration
4. **Code suggestions** - Auto-generate fixes
5. **Diff analysis** - Compare code versions
6. **Custom rules** - User-defined analysis patterns

## Deployment

### Local Development
```bash
source venv/bin/activate
python main.py
```

### Production Considerations
- Use environment variables for API keys
- Add rate limiting for API calls
- Implement proper logging
- Add monitoring for errors
- Consider API cost management

## Troubleshooting

### Virtual Environment Issues
```bash
# Recreate venv if corrupted
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### API Rate Limits
If you hit OpenAI rate limits:
- Add retry logic with exponential backoff
- Reduce concurrent requests
- Upgrade API tier

### Performance Issues
If analysis is slow:
- Check internet connection
- Verify OpenAI API status
- Consider using faster model (gpt-3.5-turbo)

## Best Practices

### For Users
1. Start with built-in samples
2. Test with simple code first
3. Review JSON output for detailed results
4. Use `--no-save` for quick tests

### For Developers
1. Keep prompts focused and specific
2. Validate JSON responses carefully
3. Test with edge cases
4. Monitor API costs
5. Version control prompt changes

## Future Roadmap

- [ ] Web interface
- [ ] Support for more languages (Go, Rust, TypeScript)
- [ ] Real-time code analysis in IDE
- [ ] Team collaboration features
- [ ] Integration with GitHub
- [ ] Code quality scoring
- [ ] Automated test generation
- [ ] Security vulnerability detection

## References

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Mermaid Documentation](https://mermaid.js.org/intro/)
- [TypedDict Documentation](https://docs.python.org/3/library/typing.html#typing.TypedDict)
