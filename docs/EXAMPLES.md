# 📚 Usage Examples

This document provides practical examples of using the Code Understanding System.

---

## Example 1: Quick Analysis of Built-in Sample

### Command
```bash
python main.py --sample python_sum_array
```

### What Happens
1. Loads the `sum_array` function from samples
2. Runs through all 5 agents
3. Displays formatted results
4. Saves to `outputs/analysis_TIMESTAMP.json`

### Expected Output
```
🚀 Starting Code Inspector workflow for python code...
================================================================================

🔍 ParseCodeAgent: Extracting code structure...
✓ Extracted 1 functions, 1 loops, 0 conditions

📊 BuildKGAgent: Constructing knowledge graph...
✓ Built KG with 10 nodes, 9 edges

🔬 AnalyzeAgent: Analyzing code quality...
✓ Found 0 potential bugs, 2 edge cases, 2 suggestions

📈 VisualizeAgent: Generating diagrams...
✓ Generated flowchart and call graph

📝 ExplainAgent: Generating explanations...
✓ Generated multi-level explanations

================================================================================
✅ Workflow completed successfully!
```

---

## Example 2: Analyze Your Own Python File

### Command
```bash
python main.py --file my_script.py
```

### Use Case
- Code review
- Documentation generation
- Understanding legacy code
- Learning from examples

### Sample File (`my_script.py`)
```python
def calculate_average(numbers):
    if not numbers:
        return 0
    total = sum(numbers)
    return total / len(numbers)
```

### What You Get
- Explanation of the function's purpose
- Edge case: Empty list handling ✓
- Suggestion: Consider using statistics.mean()
- Complexity: O(n) time, O(1) space
- Flowchart showing control flow

---

## Example 3: Inline Code Analysis

### Command
```bash
python main.py --code "def greet(name): return f'Hello, {name}!'"
```

### Use Case
- Quick checks
- Testing concepts
- Learning exercises
- Code snippets from documentation

### Output Highlights
- Simple: "This function returns a greeting message with the provided name."
- Complexity: O(1) time, O(1) space
- No bugs detected
- Clean, simple implementation

---

## Example 4: JavaScript Analysis

### Command
```bash
python main.py --sample javascript_factorial
```

### Sample Code
```javascript
function factorial(n) {
    if (n === 0 || n === 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
```

### Analysis Results
- Language: JavaScript (auto-detected)
- Complexity: O(n) time, O(n) space (recursion)
- Edge case: Negative numbers not handled
- Suggestion: Add input validation

---

## Example 5: Algorithm Complexity Analysis

### Command
```bash
python main.py --sample python_binary_search
```

### What to Look For
1. **Flowchart**: Shows the divide-and-conquer logic
2. **Complexity**: O(log n) - correctly identified
3. **Edge Cases**: Empty array, single element, not found
4. **Suggestions**: Type hints, docstrings

### Knowledge Graph Highlights
- 23 nodes representing all operations
- 29 edges showing relationships
- Clear visualization of algorithm structure

---

## Example 6: Bug Detection Demo

### Command
```bash
python main.py --sample python_fibonacci
```

### Bug Detected ✅
```
Potential Bugs:
  • The function does not handle negative input values for n,
    which could lead to infinite recursion.
```

### Why This Matters
- System correctly identifies runtime risks
- Suggests adding input validation
- Recommends memoization for performance

---

## Example 7: Custom Output Location

### Command
```bash
python main.py --sample python_bubble_sort --output reports/bubble_sort_analysis.json
```

### Use Case
- Organizing multiple analyses
- Creating documentation
- Sharing with team members
- Version control tracking

---

## Example 8: Console-Only Mode (No File Save)

### Command
```bash
python main.py --sample python_sum_array --no-save
```

### Use Case
- Quick experiments
- Learning without cluttering outputs
- Temporary checks
- Testing changes

---

## Example 9: Specify Language Manually

### Command
```bash
python main.py --code "console.log('test')" --language javascript
```

### When to Use
- Auto-detection fails
- Ambiguous syntax
- Mixed language files
- Forcing specific parser

---

## Example 10: Interactive Mode

### Command
```bash
python main.py
```

### What Happens
```
================================================================================
🎯 MULTI-AGENT CODE UNDERSTANDING SYSTEM
================================================================================

Available samples:
  1. python_sum_array
  2. python_fibonacci
  3. python_binary_search
  4. javascript_factorial
  5. python_bubble_sort

Options:
  - Enter a number to select a sample
  - Enter 'custom' to paste your own code
  - Enter 'quit' to exit

Your choice: 
```

### Use Case
- First-time users
- Exploring samples
- Guided experience
- Learning the system

---

## Example 11: Batch Analysis (Custom Script)

### Custom Script (`analyze_all.sh`)
```bash
#!/bin/bash
for sample in python_sum_array python_fibonacci python_binary_search; do
    echo "Analyzing $sample..."
    python main.py --sample $sample --output "reports/${sample}.json"
done
```

### Use Case
- Analyzing multiple files
- Generating documentation suite
- Code review process
- CI/CD integration

---

## Example 12: Review Output File

### Command
```bash
# Run analysis
python main.py --sample python_binary_search

# View JSON output
cat outputs/analysis_TIMESTAMP.json | python -m json.tool
```

### JSON Structure
```json
{
  "language": "python",
  "code": "...",
  "parsed_structure": {
    "functions": ["binary_search"],
    "loops": ["while left <= right"],
    ...
  },
  "knowledge_graph": {
    "nodes": [...],
    "edges": [...]
  },
  "analysis": {
    "bugs": [],
    "edge_cases": [...],
    "complexity": {...},
    "suggestions": [...]
  },
  "flowchart": "mermaid syntax...",
  "call_graph": "mermaid syntax...",
  "explanations": {
    "simple": "...",
    "technical": "...",
    "summary": "..."
  }
}
```

---

## Example 13: Visualize Diagrams

### Steps
1. Run analysis:
   ```bash
   python main.py --sample python_binary_search
   ```

2. Copy the Mermaid flowchart from output

3. Paste into:
   - [Mermaid Live Editor](https://mermaid.live)
   - GitHub markdown
   - VSCode Mermaid extension
   - Notion, Obsidian, etc.

### Result
Beautiful, interactive flowchart visualization!

---

## Example 14: Extract Knowledge Graph

### Python Script
```python
import json

# Load analysis
with open('outputs/analysis_TIMESTAMP.json') as f:
    data = json.load(f)

# Extract KG
kg = data['knowledge_graph']

# Analyze nodes
print(f"Total nodes: {len(kg['nodes'])}")
for node in kg['nodes']:
    print(f"  {node['type']}: {node['label']}")

# Analyze edges
print(f"\nTotal edges: {len(kg['edges'])}")
for edge in kg['edges']:
    print(f"  {edge['source']} --{edge['relation']}--> {edge['target']}")
```

### Use Case
- Custom processing
- Integration with other tools
- Graph analytics
- Research and analysis

---

## Example 15: Demo Mode

### Command
```bash
python demo.py
```

### What It Does
- Runs 4 curated examples
- Shows key highlights for each
- Interactive (press ENTER between demos)
- Educational walkthrough

### Perfect For
- First-time users
- Demonstrations
- Teaching
- Showcasing features

---

## Common Patterns

### Pattern 1: Code Review Workflow
```bash
# 1. Analyze the code
python main.py --file code_to_review.py

# 2. Check for bugs in output
# 3. Review suggestions
# 4. Check edge cases
# 5. Save report for team
```

### Pattern 2: Learning Algorithm
```bash
# 1. Analyze sample algorithm
python main.py --sample python_binary_search

# 2. Study the flowchart
# 3. Read line-by-line explanation
# 4. Understand complexity
# 5. Try variations
```

### Pattern 3: Documentation Generation
```bash
# 1. Analyze each function
python main.py --file module.py --output docs/module_analysis.json

# 2. Extract explanations from JSON
# 3. Add to project documentation
# 4. Include diagrams
```

---

## Tips and Tricks

### Tip 1: Use Shell Aliases
```bash
# Add to ~/.bashrc or ~/.zshrc
alias codeanalyze='cd ~/langgraph-code-inspector && source venv/bin/activate && python main.py'

# Then use:
codeanalyze --file ~/my_code.py
```

### Tip 2: Quick Sample Test
```bash
# Test all samples quickly
for s in python_sum_array python_fibonacci python_binary_search; do
    python main.py --sample $s --no-save
done
```

### Tip 3: Format Output for Sharing
```bash
# Run and capture output
python main.py --sample python_fibonacci > analysis_report.txt

# Share the text file
```

### Tip 4: Monitor Outputs Directory
```bash
# See recent analyses
ls -lt outputs/ | head -5

# Count total analyses
ls outputs/ | wc -l
```

---

## Troubleshooting Examples

### Issue: "Module not found"
```bash
# Solution: Activate virtual environment
source venv/bin/activate
python main.py --sample python_sum_array
```

### Issue: "API key not found"
```bash
# Solution: Check .env file
cat .env
# Should show: OPENAI_API_KEY=sk-...
```

### Issue: "Command not found: python"
```bash
# Solution: Use python3
python3 main.py --sample python_sum_array
```

---

## Next Steps

1. **Try the samples**: `python main.py --sample python_fibonacci`
2. **Analyze your code**: `python main.py --file your_code.py`
3. **Run the demo**: `python demo.py`
4. **Read the docs**: `DOCUMENTATION.md`
5. **Explore outputs**: Check `outputs/` directory

---

**Happy Analyzing!** 🚀
