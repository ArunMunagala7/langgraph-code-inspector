# 🚀 Quick Start Guide

Get up and running with the Multi-Agent Code Understanding System in 5 minutes!

## Step 1: Setup (2 minutes)

```bash
# Navigate to project directory
cd langgraph-code-inspector

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Key (1 minute)

Your OpenAI API key is already configured in `.env`. You're ready to go! ✅

## Step 3: Run Your First Analysis (30 seconds)

```bash
python main.py --sample python_sum_array
```

You should see:
- 🔍 Code structure extraction
- 📊 Knowledge graph construction
- 🔬 Bug and complexity analysis
- 📈 Diagram generation
- 📝 Multi-level explanations

## Step 4: Try More Examples (1 minute)

```bash
# Simple recursion with bug detection
python main.py --sample python_fibonacci

# Binary search algorithm
python main.py --sample python_binary_search

# Bubble sort
python main.py --sample python_bubble_sort
```

## Step 5: Analyze Your Own Code (30 seconds)

### Option 1: From command line
```bash
python main.py --code "def greet(name): return f'Hello, {name}!'"
```

### Option 2: From a file
```bash
python main.py --file path/to/your/script.py
```

### Option 3: Interactive mode
```bash
python main.py
# Then select 'custom' and paste your code
```

## 📊 Understanding the Output

### Console Output
You'll see 5 main sections:

1. **Explanations** - Simple, technical, and summary views
2. **Analysis** - Bugs, edge cases, complexity
3. **Flowchart** - Mermaid diagram of control flow
4. **Call Graph** - Function relationships
5. **Knowledge Graph Summary** - Node and edge counts

### JSON Output
Find detailed results in `outputs/analysis_TIMESTAMP.json`

```bash
# View the latest analysis
ls -lt outputs/ | head -2
```

## 🎯 Common Use Cases

### Use Case 1: Code Review
```bash
python main.py --file teammate_code.py
# Review suggestions and edge cases
```

### Use Case 2: Learning
```bash
python main.py --sample python_binary_search
# Study the flowchart and explanations
```

### Use Case 3: Documentation
```bash
python main.py --file my_function.py --output docs/analysis.json
# Generate documentation automatically
```

## 🔧 Customization

### Change Output Location
```bash
python main.py --sample python_fibonacci --output my_custom_path.json
```

### Skip File Saving
```bash
python main.py --sample python_sum_array --no-save
```

### Specify Language Manually
```bash
python main.py --code "console.log('hi')" --language javascript
```

## ⚡ Pro Tips

1. **Start simple** - Test with built-in samples first
2. **Check outputs folder** - All analyses are saved automatically
3. **Use --no-save** - For quick experiments without saving
4. **Read the flowcharts** - They visualize complex logic clearly
5. **Review edge cases** - Often reveals important considerations

## 🐛 Troubleshooting

### "Command not found: python"
Try `python3` instead:
```bash
python3 main.py --sample python_sum_array
```

### "No module named 'langgraph'"
Make sure your virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "API key not found"
Check that `.env` file exists and contains:
```
OPENAI_API_KEY=your_key_here
```

## 📚 Next Steps

- Read `README.md` for full documentation
- Check `DOCUMENTATION.md` for technical details
- Explore `data/samples.py` for more examples
- View saved analyses in `outputs/`

## 🎉 You're Ready!

You now know how to:
- ✅ Run the code inspector
- ✅ Analyze different code samples
- ✅ Interpret the results
- ✅ Use custom code
- ✅ Customize output

Happy analyzing! 🚀
