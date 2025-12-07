"""
Repository-level code analysis
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any
from .repo_utils import (
    clone_repository, 
    discover_code_files, 
    read_file_content,
    cleanup_repository,
    get_repository_stats
)
from graph.workflow import run_code_inspector


def analyze_repository(github_url: str, 
                       max_files: int = 50,
                       languages: List[str] = None,
                       generate_images: bool = False,
                       progress_callback=None) -> Dict[str, Any]:
    """
    Analyze an entire GitHub repository.
    
    Args:
        github_url: GitHub repository URL
        max_files: Maximum files to analyze
        languages: Languages to include (None = all)
        generate_images: Whether to generate flowcharts
        progress_callback: Function to call with progress updates
        
    Returns:
        Complete repository analysis
    """
    repo_path = None
    
    try:
        # Progress update helper
        def update_progress(message: str):
            if progress_callback:
                progress_callback(message)
            print(message)
        
        # Step 1: Clone repository
        update_progress("🔄 Cloning repository...")
        repo_path, repo_metadata = clone_repository(github_url)
        
        # Step 2: Discover code files
        update_progress("📁 Discovering code files...")
        code_files = discover_code_files(
            repo_path, 
            languages=languages,
            max_files=max_files
        )
        
        if not code_files:
            return {
                'error': 'No code files found in repository',
                'metadata': repo_metadata
            }
        
        update_progress(f"📁 Found {len(code_files)} files to analyze")
        
        # Step 3: Analyze each file
        file_analyses = []
        successful = 0
        failed = 0
        
        for i, file_info in enumerate(code_files):
            try:
                update_progress(
                    f"🔍 Analyzing {i+1}/{len(code_files)}: {file_info['relative_path']}"
                )
                
                # Read file content
                code = read_file_content(file_info['absolute_path'])
                
                # Skip empty files
                if not code.strip():
                    continue
                
                # Run analysis
                analysis = run_code_inspector(
                    code=code,
                    language=file_info['language']
                )
                
                # Store result
                file_analyses.append({
                    'file': file_info['relative_path'],
                    'language': file_info['language'],
                    'size': file_info['size'],
                    'lines_of_code': len(code.splitlines()),
                    'analysis': analysis
                })
                
                successful += 1
                
            except Exception as e:
                failed += 1
                print(f"❌ Error analyzing {file_info['relative_path']}: {e}")
                file_analyses.append({
                    'file': file_info['relative_path'],
                    'error': str(e)
                })
        
        update_progress(f"✅ Analysis complete: {successful} successful, {failed} failed")
        
        # Step 4: Aggregate results
        update_progress("📊 Calculating repository metrics...")
        aggregated_results = aggregate_analyses(file_analyses, repo_metadata)
        
        # Step 5: Cleanup
        cleanup_repository(repo_path)
        
        return aggregated_results
        
    except Exception as e:
        # Cleanup on error
        if repo_path:
            cleanup_repository(repo_path)
        
        return {
            'error': f"Repository analysis failed: {str(e)}",
            'metadata': {}
        }


def aggregate_analyses(file_analyses: List[dict], 
                      repo_metadata: dict) -> Dict[str, Any]:
    """
    Aggregate individual file analyses into repository-level insights.
    
    Args:
        file_analyses: List of file analysis results
        repo_metadata: Repository metadata
        
    Returns:
        Aggregated analysis with summary and per-file results
    """
    # Filter successful analyses
    successful = [f for f in file_analyses if 'analysis' in f]
    
    # Calculate totals
    total_lines = sum(f.get('lines_of_code', 0) for f in successful)
    total_functions = sum(
        len(f['analysis'].get('code_structure', {}).get('functions', []))
        for f in successful
    )
    
    # Collect all bugs
    all_bugs = []
    for f in successful:
        bugs = f['analysis'].get('bugs', [])
        for bug in bugs:
            all_bugs.append({
                'file': f['file'],
                'bug': bug
            })
    
    # Collect all suggestions
    all_suggestions = []
    for f in successful:
        suggestions = f['analysis'].get('suggestions', [])
        for suggestion in suggestions:
            all_suggestions.append({
                'file': f['file'],
                'suggestion': suggestion
            })
    
    # Find most complex files
    complexity_scores = []
    for f in successful:
        # Simple complexity: count loops + conditions
        structure = f['analysis'].get('code_structure', {})
        complexity = (
            len(structure.get('loops', [])) + 
            len(structure.get('conditions', []))
        )
        complexity_scores.append({
            'file': f['file'],
            'complexity': complexity,
            'loc': f.get('lines_of_code', 0)
        })
    
    # Sort by complexity
    most_complex = sorted(
        complexity_scores, 
        key=lambda x: x['complexity'], 
        reverse=True
    )[:5]
    
    # Language breakdown
    language_stats = {}
    for f in successful:
        lang = f['language']
        if lang not in language_stats:
            language_stats[lang] = {'files': 0, 'lines': 0}
        language_stats[lang]['files'] += 1
        language_stats[lang]['lines'] += f.get('lines_of_code', 0)
    
    return {
        'metadata': {
            **repo_metadata,
            'analyzed_at': datetime.now().isoformat(),
            'analysis_version': '1.0'
        },
        'summary': {
            'total_files_found': len(file_analyses),
            'total_files_analyzed': len(successful),
            'total_files_failed': len(file_analyses) - len(successful),
            'total_lines_of_code': total_lines,
            'total_functions': total_functions,
            'total_bugs_found': len(all_bugs),
            'total_suggestions': len(all_suggestions),
            'languages': language_stats,
            'most_complex_files': most_complex
        },
        'bugs': all_bugs,
        'suggestions': all_suggestions,
        'files': file_analyses
    }
