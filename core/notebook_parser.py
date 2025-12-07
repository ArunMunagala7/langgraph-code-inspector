"""
Jupyter Notebook Parser
Extracts code cells from .ipynb files for analysis
"""
import json
from typing import Dict, List, Tuple, Any


def parse_notebook(notebook_path_or_content: str) -> Dict[str, Any]:
    """
    Parse Jupyter notebook and extract code cells.
    
    Args:
        notebook_path_or_content: File path or JSON string content
        
    Returns:
        Dictionary with:
        - cells: List of code cell contents
        - cell_metadata: List of metadata for each cell
        - combined_code: All code cells concatenated
        - language: Detected kernel language
        - cell_count: Number of code cells
    """
    try:
        # Try to load as file first
        try:
            with open(notebook_path_or_content, 'r', encoding='utf-8') as f:
                notebook_data = json.load(f)
        except (FileNotFoundError, OSError):
            # Assume it's JSON content
            notebook_data = json.loads(notebook_path_or_content)
        
        # Extract metadata
        metadata = notebook_data.get('metadata', {})
        kernel_spec = metadata.get('kernelspec', {})
        language = kernel_spec.get('language', 'python').lower()
        
        # Extract code cells
        cells = notebook_data.get('cells', [])
        code_cells = []
        cell_metadata = []
        
        for idx, cell in enumerate(cells):
            if cell.get('cell_type') == 'code':
                # Get cell source
                source = cell.get('source', [])
                
                # Handle both list and string formats
                if isinstance(source, list):
                    code = ''.join(source)
                else:
                    code = source
                
                # Skip empty cells
                if code.strip():
                    code_cells.append(code)
                    cell_metadata.append({
                        'cell_number': idx + 1,
                        'execution_count': cell.get('execution_count'),
                        'has_output': bool(cell.get('outputs', []))
                    })
        
        # Combine all code cells
        combined_code = '\n\n# ' + '='*70 + '\n\n'.join(
            [f"# Cell {meta['cell_number']}\n{code}" 
             for meta, code in zip(cell_metadata, code_cells)]
        )
        
        return {
            'cells': code_cells,
            'cell_metadata': cell_metadata,
            'combined_code': combined_code,
            'language': language,
            'cell_count': len(code_cells),
            'total_cells': len(cells),
            'notebook_metadata': {
                'kernel': kernel_spec.get('name', 'unknown'),
                'language_version': metadata.get('language_info', {}).get('version', 'unknown')
            }
        }
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid notebook format: {e}")
    except Exception as e:
        raise ValueError(f"Error parsing notebook: {e}")


def analyze_notebook_per_cell(notebook_path_or_content: str,
                               analyze_function) -> Dict[str, Any]:
    """
    Analyze each cell of a notebook separately.
    
    Args:
        notebook_path_or_content: File path or JSON string
        analyze_function: Function that takes (code, language) and returns analysis
        
    Returns:
        Dictionary with per-cell and combined analysis
    """
    parsed = parse_notebook(notebook_path_or_content)
    
    cell_analyses = []
    all_bugs = []
    all_suggestions = []
    
    for idx, (code, metadata) in enumerate(zip(parsed['cells'], parsed['cell_metadata'])):
        try:
            # Analyze individual cell
            analysis = analyze_function(code, parsed['language'])
            
            cell_analysis = {
                'cell_number': metadata['cell_number'],
                'analysis': analysis,
                'code_preview': code[:200] + '...' if len(code) > 200 else code
            }
            cell_analyses.append(cell_analysis)
            
            # Collect bugs and suggestions
            if 'analysis' in analysis:
                bugs = analysis['analysis'].get('bugs', [])
                suggestions = analysis['analysis'].get('suggestions', [])
                
                # Add cell context to bugs
                for bug in bugs:
                    if isinstance(bug, dict):
                        bug['cell'] = metadata['cell_number']
                    all_bugs.append(bug)
                
                for suggestion in suggestions:
                    if isinstance(suggestion, dict):
                        suggestion['cell'] = metadata['cell_number']
                    all_suggestions.append(suggestion)
                    
        except Exception as e:
            cell_analyses.append({
                'cell_number': metadata['cell_number'],
                'error': str(e)
            })
    
    return {
        'notebook_info': parsed['notebook_metadata'],
        'language': parsed['language'],
        'total_cells': parsed['total_cells'],
        'code_cells': parsed['cell_count'],
        'cell_analyses': cell_analyses,
        'all_bugs': all_bugs,
        'all_suggestions': all_suggestions,
        'combined_code': parsed['combined_code']
    }


def is_notebook_file(filename: str) -> bool:
    """Check if file is a Jupyter notebook."""
    return filename.lower().endswith('.ipynb')


def get_notebook_summary(notebook_path_or_content: str) -> str:
    """
    Get a quick summary of notebook contents.
    
    Args:
        notebook_path_or_content: File path or JSON string
        
    Returns:
        Formatted summary string
    """
    parsed = parse_notebook(notebook_path_or_content)
    
    summary = f"""
📓 **Notebook Summary**
- Language: {parsed['language'].title()}
- Kernel: {parsed['notebook_metadata']['kernel']}
- Total Cells: {parsed['total_cells']}
- Code Cells: {parsed['cell_count']}
- Lines of Code: {len(parsed['combined_code'].splitlines())}
"""
    return summary
