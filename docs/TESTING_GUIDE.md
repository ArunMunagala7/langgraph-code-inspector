# Testing Guide for Code Analysis System

## 📋 Overview

This testing framework provides comprehensive tools to evaluate the quality of:
1. **Code Analysis** - Bug detection, suggestions, edge cases
2. **Quality Scoring** - Readability, maintainability, security, performance
3. **Flowchart Generation** - Structure, coverage, readability

---

## 🗂️ Test Dataset

**File**: `test_dataset.py`

Contains 12 diverse test cases covering:
- ✅ Perfect code (binary search)
- 🐛 Buggy code (multiple issues)
- 🧮 Complex algorithms (Dijkstra's)
- 🐌 Inefficient code (poor performance)
- 😕 Unreadable code (poor style)
- 🚨 Security vulnerabilities
- 🔄 Recursive algorithms
- 💾 Memory issues
- 🌐 JavaScript async patterns

Each test case includes:
- Source code
- Expected quality grade
- Expected number of bugs
- Programming language

---

## 🚀 Quick Start

### 1. Generate Test Files

```bash
python test_dataset.py
```

This creates a `test_cases/` directory with individual files for each test case.

### 2. Run All Tests

```bash
python run_tests.py
```

**Output**:
- Console report with all results
- `test_results.json` - Detailed JSON results
- `test_report.txt` - Formatted text report

### 3. Run Specific Tests

```bash
# Test only specific cases
python run_tests.py --tests perfect_code buggy_code security_issues

# Custom output files
python run_tests.py --output my_results.json --report my_report.txt
```

### 4. Evaluate Flowchart Quality

```python
from evaluate_flowcharts import evaluate_flowchart_quality, format_flowchart_report

# After analyzing code
metrics = evaluate_flowchart_quality(
    flowchart_mermaid=result['flowchart'],
    code=original_code,
    language='python'
)

print(format_flowchart_report(metrics))
```

---

## 📊 Understanding Results

### Test Report Structure

```
CODE ANALYSIS SYSTEM - TEST REPORT
==================================
Generated: 2025-12-06 14:30:00

SUMMARY
-------
Total Tests: 12
Successful: 11
Failed: 1
Success Rate: 91.7%

DETAILED RESULTS
----------------

Perfect Code - Binary Search
---------------------------
Expected Quality: A+ | Actual: A (9.2/10)
Expected Bugs: 0 | Found: 0 ✅
Suggestions: 2 | Edge Cases: 3

Quality Breakdown:
  - Readability:      9/10
  - Maintainability:  9/10
  - Security:         10/10
  - Performance:      9/10
  - Best Practices:   9/10
```

### Accuracy Indicators

- ✅ **Green Check**: Bugs found within ±2 of expected
- ⚠️ **Warning**: Bugs found differs by >2 from expected

---

## 🎯 What to Test

### 1. Bug Detection Accuracy

**Good Test Cases**:
- `buggy_code` - Should find 5+ bugs
- `security_issues` - Should find 6+ security vulnerabilities
- `edge_cases_missing` - Should find 4+ missing edge case checks

**Expected Behavior**:
- Division by zero detection
- Null/None checks
- Array bounds checking
- SQL injection detection
- Hardcoded credentials

### 2. Quality Scoring

**High Quality Tests**:
- `perfect_code` - Should score A/A+
- `good_practices` - Should score A
- `complex_algorithm` - Should score B+/A-

**Low Quality Tests**:
- `buggy_code` - Should score D
- `unreadable_code` - Should score D-/F
- `security_issues` - Should score F

### 3. Flowchart Quality

**Good Flowcharts Should Have**:
- Start and End nodes
- All conditionals represented
- All loops represented
- Proper connections between nodes
- Coverage score >80%

**Test**:
```python
from test_dataset import TEST_CASES
from graph.workflow import run_code_inspector
from evaluate_flowcharts import evaluate_flowchart_quality

test = TEST_CASES['recursive_algorithm']
result = run_code_inspector(test['code'], test['language'])
metrics = evaluate_flowchart_quality(
    result['flowchart'],
    test['code'],
    test['language']
)

print(f"Flowchart Score: {metrics['overall_score']:.1f}/100")
print(f"Grade: {metrics['grade']}")
```

---

## 📈 Performance Benchmarks

### Expected Analysis Times

| Test Case | Expected Time | Complexity |
|-----------|--------------|------------|
| perfect_code | ~15s | Low |
| complex_algorithm | ~20s | High |
| nested_complexity | ~18s | High |
| buggy_code | ~15s | Medium |

### Quality Score Distribution

**Target Distribution** (for all 12 tests):
- A/A+: 2-3 tests
- B/B+: 2-3 tests  
- C: 2-3 tests
- D/F: 4-5 tests

---

## 🔍 Manual Testing via Web UI

### Test with Web Interface

1. Start the app:
```bash
python app.py
```

2. Upload test files:
   - Go to http://localhost:7860
   - Click "Upload Code File"
   - Select from `test_cases/` directory
   - Click "Analyze Code"

3. Check results in tabs:
   - **Explanations**: Simple & technical explanations
   - **Analysis**: Bugs, suggestions, edge cases
   - **Quality Score**: New scoring tab with grades
   - **Flowchart**: Visual representation
   - **Call Graph**: Function relationships

### Test Jupyter Notebooks

```bash
# Use the sample notebook
# Upload test_notebook.ipynb in web UI
# Verify all cells are combined and analyzed
```

---

## 🧪 Custom Test Cases

### Add Your Own Test

```python
# In test_dataset.py, add to TEST_CASES:

TEST_CASES["my_test"] = {
    "name": "My Custom Test",
    "language": "python",
    "expected_quality": "B+",
    "expected_bugs": 2,
    "code": """
def my_function():
    # Your code here
    pass
"""
}
```

Then run:
```bash
python run_tests.py --tests my_test
```

---

## 📝 Interpreting Quality Scores

### Readability (1-10)
- **8-10**: Clear names, good comments, logical structure
- **5-7**: Decent structure, some unclear parts
- **1-4**: Poor naming, no comments, confusing logic

### Maintainability (1-10)
- **8-10**: Modular, low coupling, SOLID principles
- **5-7**: Some modularity, moderate coupling
- **1-4**: Monolithic, high coupling, hard to change

### Security (1-10)
- **8-10**: No vulnerabilities, input validation, safe practices
- **5-7**: Minor issues, mostly safe
- **1-4**: Critical vulnerabilities, unsafe code

### Performance (1-10)
- **8-10**: Optimal algorithms, efficient data structures
- **5-7**: Acceptable performance, some inefficiencies
- **1-4**: Poor algorithms, significant bottlenecks

### Best Practices (1-10)
- **8-10**: Follows language idioms, design patterns
- **5-7**: Some good practices, room for improvement
- **1-4**: Ignores conventions, poor patterns

---

## 🎓 Best Practices for Testing

### 1. Baseline Test
Run all tests first to establish baseline:
```bash
python run_tests.py > baseline_results.txt
```

### 2. Compare Changes
After improving analysis agents:
```bash
python run_tests.py > new_results.txt
diff baseline_results.txt new_results.txt
```

### 3. Focus on Failures
If tests fail:
```bash
python run_tests.py --tests failed_test_name
```

### 4. Verify Flowcharts Manually
Always check flowchart images for:
- Logical flow
- No overlapping boxes
- Clear arrow directions
- All code paths represented

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: Tests taking too long
```bash
# Solution: Run subset of tests
python run_tests.py --tests perfect_code buggy_code
```

**Issue**: Quality scores seem off
```bash
# Solution: Check agents/quality_agent.py
# Verify LLM temperature and prompt
```

---

## 📊 Success Criteria

Your code analysis system is working well if:

✅ **Bug Detection**: Finds >80% of expected bugs  
✅ **Quality Scoring**: Grades match expected within ±1 letter grade  
✅ **Flowchart Quality**: Average score >75/100  
✅ **No Crashes**: All tests complete successfully  
✅ **Performance**: Each test completes in <30 seconds

---

## 🎯 Next Steps

After testing:

1. **Analyze Results**: Look for patterns in failures
2. **Improve Prompts**: Update agent prompts based on results
3. **Add More Tests**: Create edge cases specific to your use case
4. **Benchmark**: Track improvements over time
5. **Demo Ready**: Use best test cases for presentations

---

## 📚 Files Reference

- `test_dataset.py` - 12 test cases with expected results
- `run_tests.py` - Automated test runner
- `evaluate_flowcharts.py` - Flowchart quality evaluator
- `test_cases/` - Individual test case files
- `test_results.json` - JSON results from last run
- `test_report.txt` - Text report from last run

---

## 💡 Pro Tips

1. **Start Simple**: Test with `perfect_code` first
2. **Validate Manually**: Check a few results by hand
3. **Iterative Testing**: Run tests after each improvement
4. **Track Metrics**: Keep history of test results
5. **Use for Demos**: Show before/after quality improvements

---

Happy Testing! 🚀
