import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up environment
os.environ.setdefault('OPENAI_API_KEY', open('.env').read().strip().split('=')[1])

from app import analyze_repository_ui

print("🔍 Testing Repository Analysis with clinical-trial-matcher...")
print("=" * 80)

# Simple progress callback
def progress(msg):
    print(f"📊 {msg}")

# Analyze repository
summary_md, bugs_md, json_output = analyze_repository_ui(
    github_url="https://github.com/ArunMunagala7/clinical-trial-matcher",
    max_files=20,
    progress=progress
)

print("\n" + "=" * 80)
print("SUMMARY:")
print("=" * 80)
print(summary_md)

print("\n" + "=" * 80)
print("BUGS FOUND:")
print("=" * 80)
print(bugs_md[:1000] if len(bugs_md) > 1000 else bugs_md)

print("\n✅ Test complete!")
