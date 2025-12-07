# 🎯 Quick Test Reference Card

## One-Line Test Commands

```bash
# Generate all test files
python test_dataset.py

# Run single test
python run_tests.py --tests perfect_code

# Run category - Data Structures
python run_tests.py --tests bst_operations linked_list hash_table heap_operations graph_bfs_dfs trie_implementation

# Run category - Sorting Algorithms  
python run_tests.py --tests quicksort merge_sort

# Run category - High Quality Code
python run_tests.py --tests perfect_code good_practices complex_algorithm

# Run category - Bug Detection
python run_tests.py --tests buggy_code security_issues edge_cases_missing memory_leak

# Run category - Performance Issues
python run_tests.py --tests inefficient_code nested_complexity

# Run ALL tests
python run_tests.py

# Check flowchart quality
python evaluate_flowcharts.py
```

## Web UI Testing

```bash
# Start web UI
python app.py

# Then upload from: test_cases/
# Best for demos:
- perfect_code.py (A+ baseline)
- security_issues.py (finds 6 bugs)
- dynamic_programming.py (complex algorithms)
- test_notebook.ipynb (Jupyter support)
```

## Expected Results

| Test | Grade | Bugs | Time | Key Features |
|------|-------|------|------|--------------|
| perfect_code | A+ | 0 | 15s | Documentation, tests, edge cases |
| quicksort | A- | 0 | 18s | Classic algorithm, in-place variant |
| merge_sort | A | 0 | 18s | Stable sort, O(n log n) |
| bst_operations | A- | 0 | 20s | Insert, delete, search |
| linked_list | B+ | 0 | 17s | Reverse, cycle detection |
| hash_table | B+ | 0 | 17s | Chaining, rehashing |
| heap_operations | A- | 0 | 17s | Min heap, heapify |
| graph_bfs_dfs | A | 0 | 19s | BFS, DFS, path finding |
| dynamic_programming | A- | 0 | 22s | Fibonacci, LCS, knapsack |
| trie_implementation | A- | 0 | 20s | Prefix matching, autocomplete |
| good_practices | A | 0 | 18s | Type hints, SOLID |
| complex_algorithm | B+ | 0 | 20s | Dijkstra's algorithm |
| buggy_code | D | 5 | 15s | Validation missing |
| inefficient_code | C | 2 | 16s | O(n²) vs O(n) |
| unreadable_code | D- | 3 | 14s | Poor naming, no comments |
| edge_cases_missing | C+ | 4 | 15s | No null checks |
| security_issues | F | 6 | 16s | Injections, hardcoded secrets |
| nested_complexity | C- | 2 | 17s | Deep nesting |
| memory_leak | D+ | 3 | 16s | Resource leaks |
| javascript_async | B+ | 1 | 17s | Promise handling |
| recursive_algorithm | A- | 0 | 18s | Tree traversal |

## Quick Validation

```bash
# 1. System works? (should get A+)
python run_tests.py --tests perfect_code

# 2. Finds bugs? (should find 5+)
python run_tests.py --tests buggy_code

# 3. Grades correctly? (should range A to F)
python run_tests.py --tests perfect_code good_practices inefficient_code security_issues

# 4. All pass? (should complete without crashes)
python run_tests.py
```

## Demo Script (5 minutes)

```
1. Perfect Code (30s)
   - Upload perfect_code.py
   - Show A+ grade, quality scores
   - Point out clean flowchart

2. Bug Detection (1m)
   - Upload security_issues.py
   - Highlight 6 bugs found
   - Show SQL injection detection
   
3. Quality Comparison (1m)
   - Upload buggy_code.py → D grade
   - Upload good_practices.py → A grade
   - Compare side-by-side

4. Complex Algorithm (1m)
   - Upload dynamic_programming.py
   - Show it understands DP patterns
   - Flowchart shows recursion clearly

5. Jupyter Notebook (1m)
   - Upload test_notebook.ipynb
   - Show all cells combined
   - Per-cell bug detection

6. File Upload Demo (30s)
   - Drag and drop any .py file
   - Auto-language detection
   - Instant analysis
```

## Key Metrics

- **Total Tests**: 21
- **Languages**: Python (20), JavaScript (1)
- **Data Structures**: 8 implementations
- **Algorithms**: 10+ covered
- **Quality Range**: A+ to F
- **Bug Range**: 0 to 6 per test
- **Avg Time**: ~17 seconds/test
- **Success Rate Target**: >90%

## Files Generated

```
test_dataset.py           → Test definitions
run_tests.py             → Automated runner
evaluate_flowcharts.py   → Quality checker
test_cases/*.py          → Individual files
test_results.json        → JSON output
test_report.txt          → Human-readable
TESTING_GUIDE.md         → Full documentation
TEST_DATASET_SUMMARY.md  → This summary
```

## Troubleshooting

```bash
# Tests fail?
python run_tests.py --tests perfect_code  # Try simple one

# Too slow?
python run_tests.py --tests perfect_code buggy_code  # Run subset

# JSON format issue?
cat test_results.json | python -m json.tool  # Validate JSON

# Flowchart problems?
python evaluate_flowcharts.py  # Check quality
```

## Pro Tips

1. **Always test perfect_code first** - Establishes baseline
2. **Use security_issues for demos** - Most impressive bug detection
3. **Compare before/after** - Show quality improvements
4. **Save test results** - Track improvements over time
5. **Focus on flowcharts** - Visual impact for presentations

---

**Ready to test!** Run `python test_dataset.py` to start. 🚀
