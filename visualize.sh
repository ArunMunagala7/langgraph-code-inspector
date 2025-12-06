#!/bin/bash

# Script to visualize the latest code analysis in browser

echo "🎨 Code Analysis Visualizer"
echo "======================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if there are any analysis files
if [ ! "$(ls -A outputs/)" ]; then
    echo "❌ No analysis files found in outputs/"
    echo "Run an analysis first:"
    echo "  python main.py --sample python_sum_array"
    exit 1
fi

# Get the latest analysis file
LATEST_FILE=$(ls -t outputs/analysis_*.json | head -1)
echo "📄 Latest analysis: $LATEST_FILE"
echo ""

# Extract the diagrams using Python
python3 << EOF
import json
import sys

try:
    with open('$LATEST_FILE', 'r') as f:
        data = json.load(f)
    
    print("📊 Flowchart Preview:")
    print("=" * 50)
    print(data.get('flowchart', 'N/A')[:200] + "...")
    print("")
    print("🔗 Call Graph Preview:")
    print("=" * 50)
    print(data.get('call_graph', 'N/A')[:200] + "...")
    print("")
    
    # Check if code is in the analysis
    if 'code' in data:
        print("💻 Code analyzed:")
        print("=" * 50)
        print(data['code'][:300])
        print("")
        
except Exception as e:
    print(f"❌ Error reading file: {e}")
    sys.exit(1)
EOF

echo ""
echo "✅ Diagrams are ready!"
echo ""
echo "📖 To visualize in browser:"
echo "  1. Open: visualize_mermaid.html"
echo "  2. Copy diagrams from the terminal output above"
echo "  3. Or open: https://mermaid.live/"
echo "  4. Paste the flowchart/call graph there"
echo ""
echo "🚀 Or generate a new analysis:"
echo "  python main.py --sample <sample_name>"
echo ""
