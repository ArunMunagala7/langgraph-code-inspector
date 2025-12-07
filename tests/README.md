# 🧪 Tests

This folder contains all test scripts for the project.

## Test Files

### Mermaid Flowchart Tests
- **`test_mermaid_simple.py`** - Simple Mermaid flowchart generation test
  ```bash
  python tests/test_mermaid_simple.py
  ```

- **`test_hybrid_flowchart.py`** - Compare Mermaid vs Matplotlib approaches
  ```bash
  python tests/test_hybrid_flowchart.py
  ```

- **`test_integration.py`** - End-to-end Mermaid integration test
  ```bash
  python tests/test_integration.py
  ```

### Repository & Dataset Tests
- **`test_repo.py`** - Repository analysis testing
  ```bash
  python tests/test_repo.py
  ```

- **`test_dataset.py`** - Test dataset validation
  ```bash
  python tests/test_dataset.py
  ```

## Running Tests

### From Project Root
```bash
# Run specific test
.venv/bin/python tests/test_mermaid_simple.py

# Run all tests
.venv/bin/python run_tests.py
```

### Quick Test Commands
See [docs/QUICK_TEST_REFERENCE.md](../docs/QUICK_TEST_REFERENCE.md) for more test commands.

## Test Output

Tests generate output in the `temp/` directory:
- `temp/*.mmd` - Mermaid source files
- `temp/*.png` - Rendered flowchart images
- `temp/*.json` - Test result data

## Adding New Tests

When creating new test files:
1. Name them `test_*.py`
2. Place them in this `tests/` directory
3. Use proper imports:
   ```python
   import sys
   import os
   sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   ```
4. Update this README with test description
